"""WTI robustness to heavy-tailed physical-measure return innovations.

The experiment replaces only the Gaussian return innovations under P with standardized
Student-t innovations.  Pricing under Q, the observed futures curve, realized APO fixings,
and the Curran pricing map are held fixed.  This isolates whether the empirical conclusion
about posterior parameter integration is an artifact of Gaussian historical returns.

Examples
--------
    python -m experiments.wti_student_t_robustness --preset research
    python -m experiments.wti_student_t_robustness --preset monster
"""

from __future__ import annotations

import argparse
import json
from concurrent.futures import ProcessPoolExecutor
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

from bayesian_asian_options.asian_futures_pricing import curran_arithmetic_futures_option
from bayesian_asian_options.bayesian_gbm import gbm_mle
from bayesian_asian_options.bayesian_student_t import random_walk_metropolis_student_t
from experiments.wti_curran_benchmark import _discover_runs, _state, _usable_returns


DEFAULT_RUNS_ROOT = Path("results/wti_apo_empirical")
DEFAULT_OUTPUT_ROOT = Path("results/analysis/wti_student_t_robustness")


@dataclass(frozen=True)
class Config:
    chains: int = 4
    n_iter: int = 30_000
    burn_in: int = 6_000
    thin: int = 4
    price_grid_points: int = 501
    workers: int = 8
    root_seed: int = 20260917


@dataclass(frozen=True)
class MonsterConfig(Config):
    chains: int = 8
    n_iter: int = 100_000
    burn_in: int = 20_000
    thin: int = 5
    price_grid_points: int = 1001
    workers: int = 16


def _chain_worker(payload: tuple[np.ndarray, float, int, int, tuple[float, float, float], int]):
    returns, dt, n_iter, burn_in, init, seed = payload
    result = random_walk_metropolis_student_t(
        returns,
        dt,
        n_iter=n_iter,
        burn_in=burn_in,
        theta_init=init,
        seed=seed,
    )
    return result.mu, result.sigma, result.nu, result.acceptance_rate


def _student_posterior(
    returns: np.ndarray,
    *,
    cfg: Config,
    date_key: int,
) -> dict[str, Any]:
    dt = 1.0 / 252.0
    mu_mle, sigma_mle = gbm_mle(returns, dt)
    init = (float(mu_mle), float(np.log(max(sigma_mle, 1e-6))), float(np.log(8.0)))
    payloads = [
        (
            returns,
            dt,
            cfg.n_iter,
            cfg.burn_in,
            init,
            cfg.root_seed + 100_000 * date_key + 10_000 * chain_id,
        )
        for chain_id in range(cfg.chains)
    ]
    with ProcessPoolExecutor(max_workers=min(cfg.workers, cfg.chains)) as pool:
        results = list(pool.map(_chain_worker, payloads))
    mu = np.concatenate([x[0][:: cfg.thin] for x in results])
    sigma = np.concatenate([x[1][:: cfg.thin] for x in results])
    nu = np.concatenate([x[2][:: cfg.thin] for x in results])
    acceptance = np.asarray([x[3] for x in results], dtype=float)
    return {
        "mu": mu,
        "sigma": sigma,
        "nu": nu,
        "acceptance": acceptance,
        "mu_mle": float(mu_mle),
        "sigma_mle": float(sigma_mle),
    }


def _price_curve(
    *,
    row: Any,
    realized: np.ndarray,
    forwards: np.ndarray,
    times: np.ndarray,
    discount: float,
    sigma_grid: np.ndarray,
) -> np.ndarray:
    return np.asarray(
        [
            curran_arithmetic_futures_option(
                realized_fixings=realized,
                forward_fixings=forwards,
                fixing_times=times,
                strike=float(row.strike),
                sigma=float(sigma),
                discount_factor=float(discount),
                option_type=str(row.option_type),
            )
            for sigma in sigma_grid
        ],
        dtype=float,
    )


def _summarize_errors(frame: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    samples: dict[str, pd.DataFrame] = {"all": frame}
    if "positive_volume" in frame:
        samples["positive_volume"] = frame[frame["positive_volume"]]
    for threshold in (1, 10, 100, 500):
        samples[f"open_interest_ge_{threshold}"] = frame[
            frame["open_interest"].fillna(-np.inf) >= threshold
        ]
    for name, sample in samples.items():
        if sample.empty:
            continue
        for model in ("student_t_pi", "student_t_pm", "gaussian_baseline_pi"):
            err = sample[f"{model}_error"].to_numpy(dtype=float)
            rows.append(
                {
                    "sample": name,
                    "model": model,
                    "n": int(len(sample)),
                    "mean_error": float(np.mean(err)),
                    "mae": float(np.mean(np.abs(err))),
                    "rmse": float(np.sqrt(np.mean(err**2))),
                }
            )
    return pd.DataFrame(rows)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--preset", choices=("research", "monster"), default="research")
    parser.add_argument("--expiries", nargs="+", default=["2026-09", "2026-10"])
    parser.add_argument("--runs-root", type=Path, default=DEFAULT_RUNS_ROOT)
    parser.add_argument("--output-root", type=Path, default=DEFAULT_OUTPUT_ROOT)
    parser.add_argument("--force", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    cfg: Config = MonsterConfig() if args.preset == "monster" else Config()
    args.output_root.mkdir(parents=True, exist_ok=True)
    contract_path = args.output_root / f"student_t_contract_pricing_{args.preset}.csv"
    if contract_path.exists() and not args.force:
        print(f"Reusing completed output: {contract_path}", flush=True)
        return

    runs: list[Path] = []
    for expiry in args.expiries:
        runs.extend(_discover_runs(args.runs_root, expiry))
    runs = sorted(set(runs))

    posterior_cache: dict[str, dict[str, Any]] = {}
    contract_rows: list[dict[str, Any]] = []
    date_rows: list[dict[str, Any]] = []

    for run_index, run_dir in enumerate(runs):
        manifest = json.loads((run_dir / "manifest.json").read_text(encoding="utf-8"))
        valuation_date = str(manifest["valuation_date"])
        expiry = str(manifest["apo_expiry"])
        if valuation_date not in posterior_cache:
            returns = _usable_returns(run_dir, manifest)
            print(
                f"Student-t posterior {valuation_date}: n={len(returns)}, chains={cfg.chains}, "
                f"iter={cfg.n_iter}",
                flush=True,
            )
            posterior_cache[valuation_date] = _student_posterior(
                returns,
                cfg=cfg,
                date_key=run_index + 1,
            )
        posterior = posterior_cache[valuation_date]
        sigma_draws = np.asarray(posterior["sigma"], dtype=float)
        sigma_mean = float(np.mean(sigma_draws))
        sigma_sd = float(np.std(sigma_draws, ddof=1))
        nu_draws = np.asarray(posterior["nu"], dtype=float)

        realized, forwards, times = _state(run_dir, manifest)
        discount = float(manifest["discounting"]["discount_factor"])
        pricing = pd.read_csv(run_dir / "contract_pricing.csv")
        sigma_lo = max(1e-4, float(np.min(sigma_draws)) * 0.90)
        sigma_hi = max(sigma_lo + 1e-3, float(np.max(sigma_draws)) * 1.10)
        grid = np.linspace(sigma_lo, sigma_hi, cfg.price_grid_points)

        for row in pricing.itertuples(index=False):
            curve = _price_curve(
                row=row,
                realized=realized,
                forwards=forwards,
                times=times,
                discount=discount,
                sigma_grid=grid,
            )
            draw_prices = np.interp(sigma_draws, grid, curve)
            t_pi = float(np.mean(draw_prices))
            t_pm = float(np.interp(sigma_mean, grid, curve))
            market = float(row.market_price)
            volume = float(row.volume) if pd.notna(row.volume) else np.nan
            oi = float(row.open_interest) if pd.notna(row.open_interest) else np.nan
            baseline = float(row.full_bayes_price)
            contract_rows.append(
                {
                    "valuation_date": valuation_date,
                    "apo_expiry": expiry,
                    "contract_id": str(row.contract_id),
                    "option_type": str(row.option_type),
                    "strike": float(row.strike),
                    "log_moneyness": float(row.log_moneyness),
                    "market_settlement": market,
                    "volume": volume,
                    "open_interest": oi,
                    "positive_volume": bool(np.isfinite(volume) and volume > 0),
                    "student_t_sigma_mean": sigma_mean,
                    "student_t_sigma_sd": sigma_sd,
                    "student_t_nu_mean": float(np.mean(nu_draws)),
                    "student_t_nu_median": float(np.median(nu_draws)),
                    "student_t_pi_price": t_pi,
                    "student_t_pm_price": t_pm,
                    "student_t_pi_minus_pm": t_pi - t_pm,
                    "student_t_pi_error": t_pi - market,
                    "student_t_pm_error": t_pm - market,
                    "gaussian_baseline_pi_price": baseline,
                    "gaussian_baseline_pi_error": baseline - market,
                }
            )

        date_rows.append(
            {
                "valuation_date": valuation_date,
                "apo_expiry": expiry,
                "posterior_draws": int(len(sigma_draws)),
                "student_t_sigma_mean": sigma_mean,
                "student_t_sigma_sd": sigma_sd,
                "student_t_nu_mean": float(np.mean(nu_draws)),
                "student_t_nu_median": float(np.median(nu_draws)),
                "student_t_nu_q05": float(np.quantile(nu_draws, 0.05)),
                "student_t_nu_q95": float(np.quantile(nu_draws, 0.95)),
                "mean_acceptance_rate": float(np.mean(posterior["acceptance"])),
            }
        )

    contracts = pd.DataFrame(contract_rows)
    dates = pd.DataFrame(date_rows).drop_duplicates(["valuation_date", "apo_expiry"])
    errors = _summarize_errors(contracts)
    contracts.to_csv(contract_path, index=False)
    dates.to_csv(args.output_root / f"student_t_date_summary_{args.preset}.csv", index=False)
    errors.to_csv(args.output_root / f"student_t_error_summary_{args.preset}.csv", index=False)

    report = {
        "preset": args.preset,
        "expiries": list(args.expiries),
        "completed_runs": int(len(runs)),
        "contract_rows": int(len(contracts)),
        "unique_valuation_dates": int(contracts["valuation_date"].nunique()),
        "chains": cfg.chains,
        "n_iter_per_chain": cfg.n_iter,
        "burn_in_per_chain": cfg.burn_in,
        "thin": cfg.thin,
        "interpretation": "Heavy-tail robustness under P only; Q pricing dynamics and market state are unchanged from the baseline experiment.",
    }
    (args.output_root / f"student_t_report_{args.preset}.json").write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(f"Completed Student-t robustness: {args.output_root}", flush=True)


if __name__ == "__main__":
    main()
