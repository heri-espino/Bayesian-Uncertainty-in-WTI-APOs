"""Massive posterior-pricing phase map using exact Gaussian sigma quadrature.

The experiment keeps the paper's physical-measure GBM model and priors unchanged, but
integrates ``mu`` analytically and evaluates the marginal posterior of ``sigma`` on a dense
grid.  This gives a sampler-independent numerical reference and makes a very large simulation
study practical on the RTX workstation.

For every synthetic history, posterior integration is pushed through a large grid of WTI-like
arithmetic-average option states.  The output maps where

    E[C(sigma) | D] - C(E[sigma | D])

is negligible and where it is economically material.  The second-order prediction
``0.5 * C''(E[sigma|D]) * Var(sigma|D)`` is evaluated alongside the exact quadrature gap.

Examples
--------
Smoke test::

    python -m experiments.massive_mechanism_map --preset quick --backend numpy

Publication stress test::

    python -m experiments.massive_mechanism_map --preset monster --backend cupy
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import platform
import subprocess
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

from bayesian_asian_options.asian_futures_pricing import curran_arithmetic_futures_option
from bayesian_asian_options.gaussian_sigma_quadrature import (
    gaussian_gbm_marginal_log_posterior_sigma,
    gaussian_sufficient_statistics_simulation,
    normalized_sigma_weights,
)


SCRIPT_VERSION = "1.0.0"
DEFAULT_OUTPUT_ROOT = Path("results/analysis/massive_mechanism_map")


@dataclass(frozen=True)
class MechanismConfig:
    root_seed: int = 20260917
    mu_true: float = 0.08
    r: float = 0.03
    historical_dt: float = 1.0 / 252.0
    sample_sizes: tuple[int, ...] = (21, 42, 63, 126, 252, 504, 1260)
    sigma_true_values: tuple[float, ...] = (0.10, 0.20, 0.35, 0.50, 0.80)
    moneyness_values: tuple[float, ...] = (0.60, 0.75, 0.90, 1.00, 1.10, 1.25, 1.50)
    maturity_days: tuple[int, ...] = (21, 63, 126, 252)
    fraction_fixed_values: tuple[float, ...] = (0.0, 0.25, 0.50, 0.75, 0.90, 0.975)
    total_fixings: int = 22
    forward_level: float = 100.0
    replications: int = 1000
    sigma_grid_min: float = 0.005
    sigma_grid_max: float = 2.50
    sigma_grid_points: int = 2049
    mu_prior_sd: float = 1.0
    sigma_prior_alpha: float = 2.0
    sigma_prior_beta: float = 0.1


@dataclass(frozen=True)
class QuickConfig(MechanismConfig):
    sample_sizes: tuple[int, ...] = (21, 63, 252)
    sigma_true_values: tuple[float, ...] = (0.20, 0.50)
    moneyness_values: tuple[float, ...] = (0.75, 1.00, 1.25)
    maturity_days: tuple[int, ...] = (21, 126)
    fraction_fixed_values: tuple[float, ...] = (0.0, 0.50, 0.90)
    replications: int = 40
    sigma_grid_points: int = 257


@dataclass(frozen=True)
class MonsterConfig(MechanismConfig):
    replications: int = 5000
    sigma_grid_points: int = 4097


def _seed(root: int, *parts: int) -> int:
    return int(np.random.SeedSequence([root, *parts]).generate_state(1, dtype=np.uint32)[0])


def _fingerprint(cfg: MechanismConfig) -> str:
    payload = json.dumps(asdict(cfg), sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode()).hexdigest()[:16]


def _backend(name: str) -> tuple[Any, str]:
    name = str(name).lower()
    if name not in {"auto", "numpy", "cupy"}:
        raise ValueError("backend must be auto, numpy, or cupy")
    if name in {"auto", "cupy"}:
        try:
            import cupy as cp  # type: ignore

            if cp.cuda.runtime.getDeviceCount() > 0:
                return cp, "cupy"
        except Exception:
            if name == "cupy":
                raise RuntimeError("CuPy backend requested but a working CUDA device was not found")
    return np, "numpy"


def _to_numpy(value: Any, resolved: str) -> np.ndarray:
    if resolved == "cupy":
        import cupy as cp  # type: ignore

        return np.asarray(cp.asnumpy(value))
    return np.asarray(value)


def _git_commit() -> str | None:
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], text=True, stderr=subprocess.DEVNULL
        ).strip()
    except Exception:
        return None


def _scenario_table(cfg: MechanismConfig) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    sid = 0
    for maturity_days in cfg.maturity_days:
        for fraction_fixed in cfg.fraction_fixed_values:
            n_fixed = min(
                cfg.total_fixings - 1,
                max(0, int(round(float(fraction_fixed) * cfg.total_fixings))),
            )
            n_future = cfg.total_fixings - n_fixed
            for moneyness in cfg.moneyness_values:
                rows.append(
                    {
                        "scenario_id": sid,
                        "maturity_days": int(maturity_days),
                        "maturity_years": float(maturity_days / 252.0),
                        "fraction_fixed": float(n_fixed / cfg.total_fixings),
                        "n_fixed": int(n_fixed),
                        "n_future": int(n_future),
                        "moneyness": float(moneyness),
                        "strike": float(cfg.forward_level * moneyness),
                    }
                )
                sid += 1
    return pd.DataFrame(rows)


def _price_curve_for_scenario(
    scenario: Any,
    sigma_grid: np.ndarray,
    cfg: MechanismConfig,
) -> np.ndarray:
    n_fixed = int(scenario.n_fixed)
    n_future = int(scenario.n_future)
    realized = np.full(n_fixed, cfg.forward_level, dtype=float)
    forwards = np.full(n_future, cfg.forward_level, dtype=float)
    T = float(scenario.maturity_years)
    times = np.linspace(T / n_future, T, n_future, dtype=float)
    discount = float(np.exp(-cfg.r * T))
    prices = np.empty_like(sigma_grid)
    for i, sigma in enumerate(sigma_grid):
        prices[i] = curran_arithmetic_futures_option(
            realized_fixings=realized,
            forward_fixings=forwards,
            fixing_times=times,
            strike=float(scenario.strike),
            sigma=float(sigma),
            discount_factor=discount,
            option_type="call",
        )
    return prices


def _load_or_build_price_curves(
    cfg: MechanismConfig,
    run_dir: Path,
    sigma_grid: np.ndarray,
    scenarios: pd.DataFrame,
) -> np.ndarray:
    checkpoint = run_dir / "checkpoints" / "price_curves.npz"
    checkpoint.parent.mkdir(parents=True, exist_ok=True)
    if checkpoint.exists():
        data = np.load(checkpoint)
        stored_grid = np.asarray(data["sigma_grid"], dtype=float)
        curves = np.asarray(data["price_curves"], dtype=float)
        if np.array_equal(stored_grid, sigma_grid) and curves.shape == (
            len(sigma_grid),
            len(scenarios),
        ):
            return curves

    print(f"Building {len(scenarios)} Curran price curves x {len(sigma_grid)} sigma nodes", flush=True)
    curves = np.empty((len(sigma_grid), len(scenarios)), dtype=float)
    for j, scenario in enumerate(scenarios.itertuples(index=False)):
        curves[:, j] = _price_curve_for_scenario(scenario, sigma_grid, cfg)
        if (j + 1) % 20 == 0 or j + 1 == len(scenarios):
            print(f"  price curves {j + 1}/{len(scenarios)}", flush=True)
    np.savez_compressed(checkpoint, sigma_grid=sigma_grid, price_curves=curves)
    return curves


def _posterior_weights_backend(
    cfg: MechanismConfig,
    *,
    n_obs: int,
    sum_returns: np.ndarray,
    sumsq_returns: np.ndarray,
    sigma_grid: np.ndarray,
    xp: Any,
) -> Any:
    logp = gaussian_gbm_marginal_log_posterior_sigma(
        sigma_grid,
        n_obs=n_obs,
        sum_returns=xp.asarray(sum_returns),
        sumsq_returns=xp.asarray(sumsq_returns),
        dt=cfg.historical_dt,
        mu_prior_sd=cfg.mu_prior_sd,
        sigma_prior_alpha=cfg.sigma_prior_alpha,
        sigma_prior_beta=cfg.sigma_prior_beta,
        xp=xp,
    )
    return normalized_sigma_weights(logp, sigma_grid, xp=xp)


def _interpolate_uniform_curves(
    x: np.ndarray,
    grid: np.ndarray,
    curves: np.ndarray,
) -> np.ndarray:
    """Interpolate every curve at every x; grid is uniform by construction."""
    step = float(grid[1] - grid[0])
    pos = np.clip((x - grid[0]) / step, 0.0, len(grid) - 1.0000000001)
    lo = np.floor(pos).astype(int)
    hi = np.minimum(lo + 1, len(grid) - 1)
    frac = pos - lo
    return curves[lo, :] * (1.0 - frac[:, None]) + curves[hi, :] * frac[:, None]


def _summarize_cell(
    *,
    cfg: MechanismConfig,
    n_obs: int,
    sigma_true: float,
    replications: int,
    sigma_grid: np.ndarray,
    price_curves: np.ndarray,
    scenarios: pd.DataFrame,
    xp: Any,
    resolved: str,
) -> tuple[pd.DataFrame, dict[str, Any]]:
    sum_returns, sumsq_returns = gaussian_sufficient_statistics_simulation(
        n_obs=n_obs,
        mu_true=cfg.mu_true,
        sigma_true=sigma_true,
        dt=cfg.historical_dt,
        replications=replications,
        seed=_seed(cfg.root_seed, n_obs, int(round(1000 * sigma_true))),
    )
    weights = _posterior_weights_backend(
        cfg,
        n_obs=n_obs,
        sum_returns=sum_returns,
        sumsq_returns=sumsq_returns,
        sigma_grid=sigma_grid,
        xp=xp,
    )
    grid_xp = xp.asarray(sigma_grid, dtype=xp.float64)
    curves_xp = xp.asarray(price_curves, dtype=xp.float64)
    post_mean_xp = weights @ grid_xp
    post_second_xp = weights @ (grid_xp**2)
    post_var_xp = xp.maximum(post_second_xp - post_mean_xp**2, 0.0)
    pi_xp = weights @ curves_xp

    post_mean = _to_numpy(post_mean_xp, resolved).reshape(-1)
    post_var = _to_numpy(post_var_xp, resolved).reshape(-1)
    pi = _to_numpy(pi_xp, resolved)
    pm = _interpolate_uniform_curves(post_mean, sigma_grid, price_curves)
    gap = pi - pm

    curvature_curves = np.gradient(
        np.gradient(price_curves, sigma_grid, axis=0, edge_order=2),
        sigma_grid,
        axis=0,
        edge_order=2,
    )
    curvature_at_mean = _interpolate_uniform_curves(post_mean, sigma_grid, curvature_curves)
    taylor = 0.5 * post_var[:, None] * curvature_at_mean

    rows: list[dict[str, Any]] = []
    for j, scenario in enumerate(scenarios.itertuples(index=False)):
        actual = gap[:, j]
        approx = taylor[:, j]
        actual_abs = np.abs(actual)
        denom = float(np.dot(approx, approx))
        slope = float(np.dot(approx, actual) / denom) if denom > 0 else np.nan
        corr = float(np.corrcoef(actual, approx)[0, 1]) if np.std(actual) > 0 and np.std(approx) > 0 else np.nan
        rows.append(
            {
                "n_obs": int(n_obs),
                "sigma_true": float(sigma_true),
                "replications": int(replications),
                "scenario_id": int(scenario.scenario_id),
                "maturity_days": int(scenario.maturity_days),
                "fraction_fixed": float(scenario.fraction_fixed),
                "moneyness": float(scenario.moneyness),
                "mean_posterior_sigma": float(np.mean(post_mean)),
                "mean_posterior_sigma_sd": float(np.mean(np.sqrt(post_var))),
                "mean_pi_minus_pm": float(np.mean(actual)),
                "mean_abs_pi_minus_pm": float(np.mean(actual_abs)),
                "median_abs_pi_minus_pm": float(np.median(actual_abs)),
                "p95_abs_pi_minus_pm": float(np.quantile(actual_abs, 0.95)),
                "p99_abs_pi_minus_pm": float(np.quantile(actual_abs, 0.99)),
                "max_abs_pi_minus_pm": float(np.max(actual_abs)),
                "mean_taylor_gap": float(np.mean(approx)),
                "taylor_mae": float(np.mean(np.abs(actual - approx))),
                "taylor_rmse": float(np.sqrt(np.mean((actual - approx) ** 2))),
                "taylor_corr": corr,
                "taylor_slope_through_origin": slope,
            }
        )

    cell = {
        "n_obs": int(n_obs),
        "sigma_true": float(sigma_true),
        "replications": int(replications),
        "posterior_sigma_mean_mean": float(np.mean(post_mean)),
        "posterior_sigma_mean_bias": float(np.mean(post_mean) - sigma_true),
        "posterior_sigma_sd_mean": float(np.mean(np.sqrt(post_var))),
    }
    del weights, post_mean_xp, post_second_xp, post_var_xp, pi_xp
    if resolved == "cupy":
        xp.get_default_memory_pool().free_all_blocks()
    return pd.DataFrame(rows), cell


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--preset", choices=("quick", "research", "monster"), default="research")
    parser.add_argument("--backend", choices=("auto", "numpy", "cupy"), default="auto")
    parser.add_argument("--output-root", type=Path, default=DEFAULT_OUTPUT_ROOT)
    parser.add_argument("--force", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    cfg: MechanismConfig
    if args.preset == "quick":
        cfg = QuickConfig()
    elif args.preset == "monster":
        cfg = MonsterConfig()
    else:
        cfg = MechanismConfig()

    fingerprint = _fingerprint(cfg)
    run_dir = args.output_root / fingerprint
    run_dir.mkdir(parents=True, exist_ok=True)
    final_path = run_dir / "mechanism_map_summary.csv"
    if final_path.exists() and not args.force:
        print(f"Reusing completed output: {final_path}", flush=True)
        return

    xp, resolved = _backend(args.backend)
    sigma_grid = np.linspace(cfg.sigma_grid_min, cfg.sigma_grid_max, cfg.sigma_grid_points)
    scenarios = _scenario_table(cfg)
    scenarios.to_csv(run_dir / "scenario_grid.csv", index=False)
    price_curves = _load_or_build_price_curves(cfg, run_dir, sigma_grid, scenarios)

    checkpoint_dir = run_dir / "checkpoints" / "cells"
    checkpoint_dir.mkdir(parents=True, exist_ok=True)
    summaries: list[pd.DataFrame] = []
    cell_rows: list[dict[str, Any]] = []

    for n_obs in cfg.sample_sizes:
        for sigma_index, sigma_true in enumerate(cfg.sigma_true_values):
            path = checkpoint_dir / f"n{n_obs}_s{sigma_index:02d}.csv"
            meta_path = checkpoint_dir / f"n{n_obs}_s{sigma_index:02d}.json"
            if path.exists() and meta_path.exists() and not args.force:
                summaries.append(pd.read_csv(path))
                cell_rows.append(json.loads(meta_path.read_text(encoding="utf-8")))
                print(f"Reusing cell n={n_obs}, sigma={sigma_true:.3f}", flush=True)
                continue
            print(
                f"Running cell n={n_obs}, sigma={sigma_true:.3f}, reps={cfg.replications}, "
                f"grid={cfg.sigma_grid_points}, scenarios={len(scenarios)}, backend={resolved}",
                flush=True,
            )
            summary, cell = _summarize_cell(
                cfg=cfg,
                n_obs=n_obs,
                sigma_true=sigma_true,
                replications=cfg.replications,
                sigma_grid=sigma_grid,
                price_curves=price_curves,
                scenarios=scenarios,
                xp=xp,
                resolved=resolved,
            )
            summary.to_csv(path, index=False)
            meta_path.write_text(json.dumps(cell, indent=2) + "\n", encoding="utf-8")
            summaries.append(summary)
            cell_rows.append(cell)

    result = pd.concat(summaries, ignore_index=True)
    result.to_csv(final_path, index=False)
    pd.DataFrame(cell_rows).to_csv(run_dir / "posterior_cell_summary.csv", index=False)

    ranking = result.sort_values("p99_abs_pi_minus_pm", ascending=False).head(100)
    ranking.to_csv(run_dir / "top_100_adverse_scenarios.csv", index=False)

    report = {
        "script_version": SCRIPT_VERSION,
        "completed_at_utc": datetime.now(timezone.utc).isoformat(),
        "preset": args.preset,
        "config_fingerprint": fingerprint,
        "config": asdict(cfg),
        "backend": resolved,
        "git_commit": _git_commit(),
        "platform": platform.platform(),
        "logical_cpu_count": os.cpu_count(),
        "synthetic_datasets": int(len(cfg.sample_sizes) * len(cfg.sigma_true_values) * cfg.replications),
        "posterior_grid_evaluations": int(len(cfg.sample_sizes) * len(cfg.sigma_true_values) * cfg.replications * cfg.sigma_grid_points),
        "contract_scenarios": int(len(scenarios)),
        "summary_rows": int(len(result)),
        "max_p99_abs_pi_minus_pm": float(result["p99_abs_pi_minus_pm"].max()),
        "max_observed_abs_pi_minus_pm": float(result["max_abs_pi_minus_pm"].max()),
        "interpretation": "Exact-in-mu, dense-grid quadrature under the paper's Gaussian GBM posterior; Curran pricing is used to map posterior sigma uncertainty into WTI-like arithmetic-average option values.",
    }
    (run_dir / "mechanism_map_report.json").write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(f"Completed massive mechanism map: {run_dir}", flush=True)


if __name__ == "__main__":
    main()
