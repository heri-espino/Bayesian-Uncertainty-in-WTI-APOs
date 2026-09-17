"""High-precision GPU Monte Carlo benchmark for empirically difficult WTI APO states.

The existing empirical pipeline is intentionally economical.  This stress test selects the
contracts with the largest PI-PM gaps and largest settlement errors, then recomputes the
entire price-versus-sigma curve with independent high-path-count GPU Monte Carlo
randomizations.  Posterior-integrated and posterior-mean prices are obtained by interpolating
that numerical curve, and the seed-to-seed dispersion supplies a direct Monte Carlo standard
error for the PI-PM gap.

An arithmetic-average control variate is used because its Q expectation is known exactly from
the realized fixings and contemporaneous futures strip.  Common random numbers are preserved
across sigma nodes within each randomization.  Every completed sigma/randomization cell is
checkpointed, so an interrupted monster run resumes rather than discarding GPU work.
"""

from __future__ import annotations

import argparse
import json
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

from bayesian_asian_options.asian_futures_pricing import curran_arithmetic_futures_option
from experiments.wti_curran_benchmark import _discover_runs, _posterior_draws, _state


DEFAULT_RUNS_ROOT = Path("results/wti_apo_empirical")
DEFAULT_OUTPUT_ROOT = Path("results/analysis/wti_high_precision_pricing")


@dataclass(frozen=True)
class Config:
    targets_per_family: int = 3
    sigma_grid_points: int = 61
    n_paths: int = 1_000_000
    randomizations: int = 3
    chunk_size: int = 250_000
    root_seed: int = 20260917


@dataclass(frozen=True)
class MonsterConfig(Config):
    targets_per_family: int = 6
    sigma_grid_points: int = 121
    n_paths: int = 5_000_000
    randomizations: int = 4
    chunk_size: int = 1_000_000


def _backend(name: str):
    name = name.lower()
    if name not in {"auto", "numpy", "cupy"}:
        raise ValueError("backend must be auto, numpy, or cupy")
    if name in {"auto", "cupy"}:
        try:
            import cupy as cp  # type: ignore

            if cp.cuda.runtime.getDeviceCount() > 0:
                return cp, "cupy"
        except Exception:
            if name == "cupy":
                raise RuntimeError("CuPy backend requested but unavailable")
    return np, "numpy"


def _scalar(value: Any, resolved: str) -> float:
    if resolved == "cupy":
        import cupy as cp  # type: ignore

        return float(cp.asnumpy(value))
    return float(value)


def _apo_option_mc_chunked(
    *,
    realized: np.ndarray,
    forwards: np.ndarray,
    times: np.ndarray,
    strike: float,
    option_type: str,
    sigma: float,
    discount: float,
    n_paths: int,
    seed: int,
    backend: str,
    chunk_size: int,
) -> tuple[float, float, float, float]:
    """Return CV price, CV SE, raw price, raw SE for one APO contract."""
    xp, resolved = _backend(backend)
    realized = np.asarray(realized, dtype=float)
    forwards = np.asarray(forwards, dtype=float)
    times = np.asarray(times, dtype=float)
    n_total_fixings = len(realized) + len(forwards)
    if n_total_fixings < 1 or sigma <= 0 or n_paths < 2:
        raise ValueError("invalid APO Monte Carlo inputs")
    kind = str(option_type).lower()
    if kind not in {"call", "put"}:
        raise ValueError("option_type must be call or put")

    expected_average = float((realized.sum() + forwards.sum()) / n_total_fixings)
    n_future = len(forwards)
    if n_future == 0:
        payoff = (
            max(expected_average - strike, 0.0)
            if kind == "call"
            else max(strike - expected_average, 0.0)
        )
        price = discount * payoff
        return price, 0.0, price, 0.0

    dt = np.diff(np.concatenate([[0.0], times]))
    sqrt_dt = xp.asarray(np.sqrt(dt), dtype=xp.float64)
    times_xp = xp.asarray(times, dtype=xp.float64)
    forwards_xp = xp.asarray(forwards, dtype=xp.float64)
    rng = xp.random.RandomState(int(seed))

    count = 0
    sum_y = sum_x = sum_y2 = sum_x2 = sum_xy = 0.0
    while count < n_paths:
        m = min(chunk_size, n_paths - count)
        half = (m + 1) // 2
        z_half = rng.standard_normal((half, n_future))
        z = xp.concatenate((z_half, -z_half), axis=0)[:m]
        w = xp.cumsum(z * sqrt_dt[None, :], axis=1)
        future = forwards_xp[None, :] * xp.exp(
            -0.5 * float(sigma) ** 2 * times_xp[None, :] + float(sigma) * w
        )
        average = (float(realized.sum()) + xp.sum(future, axis=1)) / float(n_total_fixings)
        if kind == "call":
            payoff = xp.maximum(average - float(strike), 0.0)
        else:
            payoff = xp.maximum(float(strike) - average, 0.0)
        y = float(discount) * payoff
        # E_Q[A] is known exactly, so X has zero mean and is a valid control variate.
        x = float(discount) * (average - expected_average)
        sum_y += _scalar(xp.sum(y), resolved)
        sum_x += _scalar(xp.sum(x), resolved)
        sum_y2 += _scalar(xp.sum(y * y), resolved)
        sum_x2 += _scalar(xp.sum(x * x), resolved)
        sum_xy += _scalar(xp.sum(x * y), resolved)
        count += m
        del z_half, z, w, future, average, payoff, y, x

    n = float(count)
    mean_y = sum_y / n
    mean_x = sum_x / n
    var_y = max((sum_y2 - n * mean_y**2) / (n - 1.0), 0.0)
    var_x = max((sum_x2 - n * mean_x**2) / (n - 1.0), 0.0)
    cov = (sum_xy - n * mean_x * mean_y) / (n - 1.0)
    raw_se = float(np.sqrt(var_y / n))
    if var_x > 0:
        beta = cov / var_x
        price = mean_y - beta * mean_x
        adjusted_var = max(var_y + beta**2 * var_x - 2.0 * beta * cov, 0.0)
        se = float(np.sqrt(adjusted_var / n))
    else:
        price = mean_y
        se = raw_se
    return float(price), se, float(mean_y), raw_se


def _candidate_targets(runs_root: Path, expiries: list[str], per_family: int) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    for expiry in expiries:
        for run_dir in _discover_runs(runs_root, expiry):
            manifest = json.loads((run_dir / "manifest.json").read_text(encoding="utf-8"))
            pricing = pd.read_csv(run_dir / "contract_pricing.csv")
            for row in pricing.itertuples(index=False):
                rows.append(
                    {
                        "run_dir": str(run_dir),
                        "valuation_date": str(manifest["valuation_date"]),
                        "apo_expiry": expiry,
                        "contract_id": str(row.contract_id),
                        "option_type": str(row.option_type),
                        "strike": float(row.strike),
                        "market_price": float(row.market_price),
                        "pi_pm_abs": abs(
                            float(row.full_bayes_price) - float(row.postmean_plugin_price)
                        ),
                        "market_abs_error": abs(
                            float(row.full_bayes_price) - float(row.market_price)
                        ),
                        "volume": float(row.volume) if pd.notna(row.volume) else np.nan,
                    }
                )
    frame = pd.DataFrame(rows)
    selected = pd.concat(
        [
            frame.nlargest(per_family, "pi_pm_abs"),
            frame.nlargest(per_family, "market_abs_error"),
            frame[frame["volume"].fillna(0) > 0].nlargest(per_family, "market_abs_error"),
        ],
        ignore_index=True,
    )
    return selected.drop_duplicates(["run_dir", "contract_id"]).reset_index(drop=True)


def _save_target_checkpoint(
    path: Path,
    *,
    grid: np.ndarray,
    seed_curves: np.ndarray,
    seed_ses: np.ndarray,
    seed_raw_ses: np.ndarray,
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(".tmp.npz")
    np.savez_compressed(
        temporary,
        grid=grid,
        seed_curves=seed_curves,
        seed_ses=seed_ses,
        seed_raw_ses=seed_raw_ses,
    )
    os.replace(temporary, path)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--preset", choices=("research", "monster"), default="research")
    parser.add_argument("--backend", choices=("auto", "numpy", "cupy"), default="auto")
    parser.add_argument("--expiries", nargs="+", default=["2026-09", "2026-10"])
    parser.add_argument("--runs-root", type=Path, default=DEFAULT_RUNS_ROOT)
    parser.add_argument("--output-root", type=Path, default=DEFAULT_OUTPUT_ROOT)
    parser.add_argument("--force", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    cfg: Config = MonsterConfig() if args.preset == "monster" else Config()
    args.output_root.mkdir(parents=True, exist_ok=True)
    checkpoint_dir = args.output_root / "checkpoints" / args.preset
    checkpoint_dir.mkdir(parents=True, exist_ok=True)
    report_path = args.output_root / f"high_precision_report_{args.preset}.json"
    if report_path.exists() and not args.force:
        print(f"Reusing completed output: {report_path}", flush=True)
        return

    targets = _candidate_targets(args.runs_root, list(args.expiries), cfg.targets_per_family)
    targets.to_csv(args.output_root / f"selected_targets_{args.preset}.csv", index=False)
    curve_rows: list[dict[str, Any]] = []
    summary_rows: list[dict[str, Any]] = []

    for target_index, target in enumerate(targets.itertuples(index=False)):
        run_dir = Path(target.run_dir)
        manifest = json.loads((run_dir / "manifest.json").read_text(encoding="utf-8"))
        realized, forwards, times = _state(run_dir, manifest)
        discount = float(manifest["discounting"]["discount_factor"])
        sigma_draws, posterior_source = _posterior_draws(run_dir, manifest)
        sigma_mean = float(np.mean(sigma_draws))
        lo = max(0.005, float(np.min(sigma_draws)) * 0.95)
        hi = max(lo + 0.02, float(np.max(sigma_draws)) * 1.05)
        grid = np.linspace(lo, hi, cfg.sigma_grid_points)
        checkpoint = checkpoint_dir / f"target_{target_index:03d}.npz"

        if checkpoint.exists() and not args.force:
            with np.load(checkpoint, allow_pickle=False) as data:
                stored_grid = data["grid"].astype(float)
                if not np.array_equal(stored_grid, grid):
                    raise RuntimeError(
                        f"checkpoint grid mismatch for target {target_index}; remove {checkpoint} "
                        "or use --force after changing the experiment configuration"
                    )
                seed_curves = data["seed_curves"].astype(float)
                seed_ses = data["seed_ses"].astype(float)
                seed_raw_ses = data["seed_raw_ses"].astype(float)
        else:
            seed_curves = np.full(
                (cfg.randomizations, cfg.sigma_grid_points), np.nan, dtype=float
            )
            seed_ses = np.full_like(seed_curves, np.nan)
            seed_raw_ses = np.full_like(seed_curves, np.nan)

        print(
            f"High-precision target {target_index + 1}/{len(targets)}: {target.valuation_date} "
            f"{target.contract_id}, grid={cfg.sigma_grid_points}, paths={cfg.n_paths}, "
            f"randomizations={cfg.randomizations}",
            flush=True,
        )
        for seed_id in range(cfg.randomizations):
            seed = cfg.root_seed + 100_000 * target_index + 10_000 * seed_id
            for j, sigma in enumerate(grid):
                if np.isfinite(seed_curves[seed_id, j]):
                    continue
                price, se, _raw, raw_se = _apo_option_mc_chunked(
                    realized=realized,
                    forwards=forwards,
                    times=times,
                    strike=float(target.strike),
                    option_type=str(target.option_type),
                    sigma=float(sigma),
                    discount=discount,
                    n_paths=cfg.n_paths,
                    seed=seed,
                    backend=args.backend,
                    chunk_size=cfg.chunk_size,
                )
                seed_curves[seed_id, j] = price
                seed_ses[seed_id, j] = se
                seed_raw_ses[seed_id, j] = raw_se
                _save_target_checkpoint(
                    checkpoint,
                    grid=grid,
                    seed_curves=seed_curves,
                    seed_ses=seed_ses,
                    seed_raw_ses=seed_raw_ses,
                )
                print(
                    f"  target {target_index + 1}: randomization {seed_id + 1}/{cfg.randomizations}, "
                    f"sigma {j + 1}/{cfg.sigma_grid_points}",
                    flush=True,
                )

        if np.any(~np.isfinite(seed_curves)):
            raise RuntimeError(f"incomplete high-precision checkpoint: {checkpoint}")

        for seed_id in range(cfg.randomizations):
            for j, sigma in enumerate(grid):
                curve_rows.append(
                    {
                        "target_index": target_index,
                        "valuation_date": target.valuation_date,
                        "apo_expiry": target.apo_expiry,
                        "contract_id": target.contract_id,
                        "seed_id": seed_id,
                        "sigma": float(sigma),
                        "mc_price": float(seed_curves[seed_id, j]),
                        "mc_standard_error": float(seed_ses[seed_id, j]),
                        "raw_standard_error": float(seed_raw_ses[seed_id, j]),
                    }
                )

        mc_curve = seed_curves.mean(axis=0)
        curran_curve = np.asarray(
            [
                curran_arithmetic_futures_option(
                    realized_fixings=realized,
                    forward_fixings=forwards,
                    fixing_times=times,
                    strike=float(target.strike),
                    sigma=float(sigma),
                    discount_factor=discount,
                    option_type=str(target.option_type),
                )
                for sigma in grid
            ]
        )
        seed_gaps = np.empty(cfg.randomizations)
        seed_pi = np.empty(cfg.randomizations)
        seed_pm = np.empty(cfg.randomizations)
        for seed_id in range(cfg.randomizations):
            seed_pi[seed_id] = float(
                np.mean(np.interp(sigma_draws, grid, seed_curves[seed_id]))
            )
            seed_pm[seed_id] = float(np.interp(sigma_mean, grid, seed_curves[seed_id]))
            seed_gaps[seed_id] = seed_pi[seed_id] - seed_pm[seed_id]

        mc_pi = float(np.mean(np.interp(sigma_draws, grid, mc_curve)))
        mc_pm = float(np.interp(sigma_mean, grid, mc_curve))
        curran_pi = float(np.mean(np.interp(sigma_draws, grid, curran_curve)))
        curran_pm = float(np.interp(sigma_mean, grid, curran_curve))
        summary_rows.append(
            {
                "target_index": target_index,
                "valuation_date": target.valuation_date,
                "apo_expiry": target.apo_expiry,
                "contract_id": target.contract_id,
                "option_type": target.option_type,
                "strike": target.strike,
                "market_price": target.market_price,
                "posterior_source": posterior_source,
                "posterior_sigma_mean": sigma_mean,
                "mc_pi": mc_pi,
                "mc_pm": mc_pm,
                "mc_pi_minus_pm": mc_pi - mc_pm,
                "mc_pi_minus_pm_mcse": (
                    float(np.std(seed_gaps, ddof=1) / np.sqrt(cfg.randomizations))
                    if cfg.randomizations > 1
                    else np.nan
                ),
                "curran_pi": curran_pi,
                "curran_pm": curran_pm,
                "curran_pi_minus_pm": curran_pi - curran_pm,
                "curran_minus_mc_pi": curran_pi - mc_pi,
                "curran_minus_mc_pm": curran_pm - mc_pm,
                "max_mean_grid_mcse": float(np.max(seed_ses.mean(axis=0))),
                "seed_pi_sd": (
                    float(np.std(seed_pi, ddof=1)) if cfg.randomizations > 1 else np.nan
                ),
                "seed_pm_sd": (
                    float(np.std(seed_pm, ddof=1)) if cfg.randomizations > 1 else np.nan
                ),
            }
        )

    pd.DataFrame(curve_rows).to_csv(
        args.output_root / f"high_precision_curves_{args.preset}.csv", index=False
    )
    summary = pd.DataFrame(summary_rows)
    summary.to_csv(
        args.output_root / f"high_precision_summary_{args.preset}.csv", index=False
    )
    report = {
        "preset": args.preset,
        "targets": int(len(targets)),
        "sigma_grid_points": cfg.sigma_grid_points,
        "paths_per_sigma_per_randomization": cfg.n_paths,
        "randomizations": cfg.randomizations,
        "path_sigma_evaluations": int(
            len(targets) * cfg.sigma_grid_points * cfg.n_paths * cfg.randomizations
        ),
        "selection": "union of largest baseline PI-PM gaps, largest settlement errors, and largest settlement errors among positive-volume contracts",
        "control_variate": "discounted arithmetic average minus its exact Q expectation",
        "checkpoint_policy": "Each completed target/randomization/sigma cell is atomically checkpointed and reused after interruption.",
    }
    report_path.write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(f"Completed high-precision benchmark: {args.output_root}", flush=True)


if __name__ == "__main__":
    main()
