"""Benchmark completed WTI APO runs against a Curran conditioning approximation.

For every completed single-date run matching an APO expiry, this script reconstructs the
stored fixing state and volatility posterior, prices every retained contract with the
Curran (1994) geometric-conditioning approximation, and compares:

* Curran posterior-integrated (PI) pricing;
* Curran posterior-mean (PM) plug-in pricing;
* the canonical Monte Carlo PI and PM prices already stored by the empirical driver;
* the observed Barchart settlement retained as ``market_price`` in the source run.

Newer empirical runs store ``posterior_draws.npz`` directly.  Legacy completed runs may not.
For those runs the benchmark deterministically reconstructs the original volatility draws
from the committed ``inference_return_audit.csv`` plus the MCMC settings recorded in the run
manifest.  The reconstructed mean is checked against ``posterior_summary.csv`` before it is
used.  This avoids rerunning the market-data pipeline or weakening the benchmark to PM-only
pricing.

The Curran implementation uses the same one-factor Q dynamics, first-nearby fixing map,
realized fixings, and discount factor as the Monte Carlo baseline.  It is an independent
numerical/industry benchmark; it is not labeled as an exact reproduction of CME's internal
settlement engine.

Examples
--------
    python -m experiments.wti_curran_benchmark --apo-expiry 2026-10
    python -m experiments.wti_curran_benchmark --apo-expiry 2026-09
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

from bayesian_asian_options.asian_futures_pricing import curran_arithmetic_futures_option
from bayesian_asian_options.bayesian_gbm import gbm_mle, random_walk_metropolis_gbm


DEFAULT_RUNS_ROOT = Path("results/wti_apo_empirical")
DEFAULT_OUTPUT_ROOT = Path("results/analysis/curran_benchmark")


def _discover_runs(root: Path, expiry: str) -> list[Path]:
    """Return completed single-date runs, including legacy runs without saved draws."""
    if not root.exists():
        raise FileNotFoundError(f"runs root does not exist: {root}")
    suffix = f"_{expiry.replace('-', '')}"
    required = (
        "manifest.json",
        "contract_pricing.csv",
        "apo_fixing_state.csv",
        "inference_return_audit.csv",
    )
    runs = sorted(
        path
        for path in root.iterdir()
        if path.is_dir()
        and path.name.endswith(suffix)
        and all((path / name).exists() for name in required)
    )
    if not runs:
        raise FileNotFoundError(
            f"no completed {expiry} runs found below {root}; expected directories ending "
            f"with {suffix!r} containing {', '.join(required)}"
        )
    return runs


def _usable_returns(run_dir: Path, manifest: dict[str, Any]) -> np.ndarray:
    audit = pd.read_csv(run_dir / "inference_return_audit.csv")
    required = {"log_return", "usable_inference_return"}
    missing = required.difference(audit.columns)
    if missing:
        raise ValueError(f"{run_dir}: inference return audit missing {sorted(missing)}")
    flag = audit["usable_inference_return"]
    if pd.api.types.is_bool_dtype(flag):
        usable = flag
    else:
        usable = flag.astype(str).str.strip().str.lower().isin({"true", "1", "yes"})
    returns = audit.loc[usable, "log_return"].dropna().to_numpy(dtype=float)
    if returns.ndim != 1 or returns.size == 0 or np.any(~np.isfinite(returns)):
        raise ValueError(f"{run_dir}: invalid usable inference returns")
    expected = manifest.get("n_usable_returns")
    if expected is not None and int(expected) != int(returns.size):
        raise RuntimeError(
            f"{run_dir}: manifest records {expected} usable returns but audit contains "
            f"{returns.size}"
        )
    return returns


def _reconstruct_sigma_draws(run_dir: Path, manifest: dict[str, Any]) -> np.ndarray:
    """Replay the canonical empirical MCMC from a legacy run's recorded inputs."""
    settings = manifest.get("mcmc", {})
    required = {"chains", "n_iter_per_chain", "burn_in_per_chain", "seed"}
    missing = required.difference(settings)
    if missing:
        raise ValueError(f"{run_dir}: MCMC manifest missing {sorted(missing)}")

    returns = _usable_returns(run_dir, manifest)
    dt = 1.0 / 252.0
    mu_mle, sigma_mle = gbm_mle(returns, dt)
    chains = int(settings["chains"])
    n_iter = int(settings["n_iter_per_chain"])
    burn_in = int(settings["burn_in_per_chain"])
    root_seed = int(settings["seed"])
    if chains < 2:
        raise ValueError(f"{run_dir}: at least two MCMC chains are required")

    sigma_chains: list[np.ndarray] = []
    for chain_id in range(chains):
        result = random_walk_metropolis_gbm(
            returns,
            dt,
            n_iter=n_iter,
            burn_in=burn_in,
            theta_init=(mu_mle, float(np.log(max(sigma_mle, 1e-8)))),
            seed=root_seed + 10_000 * chain_id,
        )
        sigma_chains.append(result.sigma)
    draws = np.concatenate(sigma_chains).astype(float, copy=False)

    summary_path = run_dir / "posterior_summary.csv"
    if summary_path.exists():
        summary = pd.read_csv(summary_path)
        if not summary.empty and "sigma_posterior_mean" in summary.columns:
            recorded = float(summary.iloc[0]["sigma_posterior_mean"])
            replayed = float(np.mean(draws))
            tolerance = max(5e-6, 5e-4 * max(abs(recorded), 1.0))
            if abs(replayed - recorded) > tolerance:
                raise RuntimeError(
                    f"{run_dir}: reconstructed posterior mean {replayed:.8f} does not "
                    f"match recorded mean {recorded:.8f} within tolerance {tolerance:.2g}; "
                    "do not use reconstructed draws until the legacy inference settings "
                    "are reconciled"
                )
    return draws


def _posterior_draws(
    run_dir: Path, manifest: dict[str, Any]
) -> tuple[np.ndarray, str]:
    stored = run_dir / "posterior_draws.npz"
    if stored.exists():
        with np.load(stored, allow_pickle=False) as data:
            if "sigma" not in data:
                raise ValueError(f"{stored}: missing sigma array")
            draws = data["sigma"].astype(float)
        source = "stored_posterior_draws"
    else:
        draws = _reconstruct_sigma_draws(run_dir, manifest)
        source = "reconstructed_from_inference_return_audit"
    if draws.ndim != 1 or draws.size == 0 or np.any(~np.isfinite(draws)) or np.any(draws <= 0):
        raise ValueError(f"invalid posterior sigma draws for {run_dir}")
    return draws, source


def _state(run_dir: Path, manifest: dict[str, Any]) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    valuation_date = pd.Timestamp(manifest["valuation_date"]).normalize()
    state = pd.read_csv(run_dir / "apo_fixing_state.csv")
    state["fixing_date"] = pd.to_datetime(state["fixing_date"]).dt.normalize()
    if "fixing_status" in state.columns:
        realized = state[state["fixing_status"] == "realized"].copy()
        remaining = state[state["fixing_status"] == "remaining"].copy()
    else:
        realized = state[state["fixing_date"] <= valuation_date].copy()
        remaining = state[state["fixing_date"] > valuation_date].copy()
    realized_values = realized["settlement"].to_numpy(dtype=float)
    forward_values = remaining["settlement"].to_numpy(dtype=float)
    times = (
        (remaining["fixing_date"] - valuation_date).dt.days.to_numpy(dtype=float) / 365.25
    )
    return realized_values, forward_values, times


def _error_summary(frame: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    methods = {
        "curran_pi": "curran_pi_price",
        "curran_pm": "curran_pm_price",
        "mc_pi": "full_bayes_price",
        "mc_pm": "postmean_plugin_price",
    }
    for sample_name, sample in {
        "all": frame,
        "positive_volume": frame[frame["positive_volume"]],
    }.items():
        if sample.empty:
            continue
        for method, column in methods.items():
            error = sample[column].to_numpy(dtype=float) - sample["market_settlement"].to_numpy(dtype=float)
            rows.append(
                {
                    "sample": sample_name,
                    "method": method,
                    "n": int(len(sample)),
                    "mean_error": float(np.mean(error)),
                    "mae": float(np.mean(np.abs(error))),
                    "rmse": float(np.sqrt(np.mean(error**2))),
                }
            )
    return pd.DataFrame(rows)


def _one_run(run_dir: Path, grid_points: int) -> pd.DataFrame:
    manifest = json.loads((run_dir / "manifest.json").read_text(encoding="utf-8"))
    valuation_date = str(manifest["valuation_date"])
    discount = float(manifest["discounting"]["discount_factor"])
    pricing = pd.read_csv(run_dir / "contract_pricing.csv")
    sigma_draws, posterior_source = _posterior_draws(run_dir, manifest)
    sigma_mean = float(np.mean(sigma_draws))
    realized, forwards, times = _state(run_dir, manifest)

    lo = max(1e-6, 0.9 * float(np.quantile(sigma_draws, 0.0005)))
    hi = 1.1 * float(np.quantile(sigma_draws, 0.9995))
    sigma_grid = np.linspace(lo, hi, grid_points)

    rows: list[dict[str, Any]] = []
    for contract in pricing.itertuples(index=False):
        grid_prices = np.array(
            [
                curran_arithmetic_futures_option(
                    realized_fixings=realized,
                    forward_fixings=forwards,
                    fixing_times=times,
                    strike=float(contract.strike),
                    sigma=float(sigma),
                    discount_factor=discount,
                    option_type=str(contract.option_type),
                )
                for sigma in sigma_grid
            ],
            dtype=float,
        )
        posterior_prices = np.interp(sigma_draws, sigma_grid, grid_prices)
        curran_pi = float(np.mean(posterior_prices))
        curran_pm = float(np.interp(sigma_mean, sigma_grid, grid_prices))
        volume = float(contract.volume) if pd.notna(contract.volume) else np.nan
        market = float(contract.market_price)
        n_fixings = len(realized) + len(forwards)
        rows.append(
            {
                "valuation_date": valuation_date,
                "contract_id": str(contract.contract_id),
                "option_type": str(contract.option_type),
                "strike": float(contract.strike),
                "market_settlement": market,
                "volume": volume,
                "positive_volume": bool(np.isfinite(volume) and volume > 0),
                "fraction_fixed": float(
                    getattr(
                        contract,
                        "fraction_fixed",
                        len(realized) / n_fixings if n_fixings else np.nan,
                    )
                ),
                "posterior_source": posterior_source,
                "posterior_draw_count": int(sigma_draws.size),
                "sigma_posterior_mean": sigma_mean,
                "curran_pi_price": curran_pi,
                "curran_pm_price": curran_pm,
                "curran_pi_minus_pm": curran_pi - curran_pm,
                "full_bayes_price": float(contract.full_bayes_price),
                "postmean_plugin_price": float(contract.postmean_plugin_price),
                "mc_pi_minus_pm": float(contract.fb_minus_pm),
                "curran_pi_minus_mc_pi": curran_pi - float(contract.full_bayes_price),
                "curran_pm_minus_mc_pm": curran_pm - float(contract.postmean_plugin_price),
                "curran_pi_error": curran_pi - market,
                "curran_pm_error": curran_pm - market,
            }
        )
    return pd.DataFrame(rows)


def run(
    runs_root: Path,
    *,
    apo_expiry: str,
    grid_points: int,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, dict[str, Any]]:
    if grid_points < 41:
        raise ValueError("grid_points must be at least 41")
    runs = _discover_runs(runs_root, apo_expiry)
    frames = [_one_run(path, grid_points) for path in runs]
    contracts = pd.concat(frames, ignore_index=True)
    errors = _error_summary(contracts)

    date_rows: list[dict[str, Any]] = []
    for date, group in contracts.groupby("valuation_date", sort=True):
        diff_pi = group["curran_pi_minus_mc_pi"].to_numpy(dtype=float)
        diff_pm = group["curran_pm_minus_mc_pm"].to_numpy(dtype=float)
        date_rows.append(
            {
                "valuation_date": date,
                "n": int(len(group)),
                "positive_volume_n": int(group["positive_volume"].sum()),
                "fraction_fixed": float(group["fraction_fixed"].iloc[0]),
                "posterior_source": str(group["posterior_source"].iloc[0]),
                "mean_abs_curran_pi_minus_mc_pi": float(np.mean(np.abs(diff_pi))),
                "max_abs_curran_pi_minus_mc_pi": float(np.max(np.abs(diff_pi))),
                "mean_abs_curran_pm_minus_mc_pm": float(np.mean(np.abs(diff_pm))),
                "mean_abs_curran_pi_minus_pm": float(np.mean(np.abs(group["curran_pi_minus_pm"]))),
                "mean_abs_mc_pi_minus_pm": float(np.mean(np.abs(group["mc_pi_minus_pm"]))),
            }
        )
    by_date = pd.DataFrame(date_rows)

    source_counts = (
        by_date["posterior_source"].value_counts().sort_index().to_dict()
        if not by_date.empty
        else {}
    )
    report = {
        "apo_expiry": apo_expiry,
        "source_runs_root": str(runs_root),
        "completed_dates": len(runs),
        "contract_date_rows": int(len(contracts)),
        "positive_volume_rows": int(contracts["positive_volume"].sum()),
        "posterior_source_date_counts": {str(k): int(v) for k, v in source_counts.items()},
        "curran_sigma_grid_points": grid_points,
        "mean_abs_curran_pi_minus_mc_pi": float(
            contracts["curran_pi_minus_mc_pi"].abs().mean()
        ),
        "max_abs_curran_pi_minus_mc_pi": float(
            contracts["curran_pi_minus_mc_pi"].abs().max()
        ),
        "mean_abs_curran_pm_minus_mc_pm": float(
            contracts["curran_pm_minus_mc_pm"].abs().mean()
        ),
        "mean_abs_curran_pi_minus_pm": float(
            contracts["curran_pi_minus_pm"].abs().mean()
        ),
        "mean_abs_mc_pi_minus_pm": float(
            contracts["mc_pi_minus_pm"].abs().mean()
        ),
        "benchmark_definition": (
            "Curran (1994) geometric-conditioning approximation under the paper's same "
            "one-factor lognormal futures dynamics and stored first-nearby fixing state"
        ),
        "market_field_interpretation": (
            "Barchart Latest is treated as the end-of-day settlement supplied in the source histories"
        ),
        "legacy_posterior_policy": (
            "If posterior_draws.npz is absent, replay the canonical empirical MCMC from "
            "inference_return_audit.csv and manifest settings, and verify the reconstructed "
            "posterior mean against posterior_summary.csv before pricing."
        ),
        "caution": (
            "This experiment does not assert that the implemented Curran approximation is an "
            "exact reproduction of CME's complete settlement implementation."
        ),
    }
    return contracts, by_date, errors, report


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--runs-root", type=Path, default=DEFAULT_RUNS_ROOT)
    parser.add_argument("--apo-expiry", default="2026-10")
    parser.add_argument("--output-root", type=Path, default=DEFAULT_OUTPUT_ROOT)
    parser.add_argument("--grid-points", type=int, default=401)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    contracts, by_date, errors, report = run(
        args.runs_root,
        apo_expiry=args.apo_expiry,
        grid_points=args.grid_points,
    )
    output_dir = args.output_root / args.apo_expiry.replace("-", "")
    output_dir.mkdir(parents=True, exist_ok=True)
    contracts.to_csv(output_dir / "curran_contract_benchmark.csv", index=False)
    by_date.to_csv(output_dir / "curran_by_date.csv", index=False)
    errors.to_csv(output_dir / "curran_error_summary.csv", index=False)
    with (output_dir / "curran_report.json").open("w", encoding="utf-8") as fh:
        json.dump(report, fh, indent=2, sort_keys=True)
        fh.write("\n")
    print(json.dumps(report, indent=2, sort_keys=True))
    print(f"output_dir={output_dir}")


if __name__ == "__main__":
    main()
