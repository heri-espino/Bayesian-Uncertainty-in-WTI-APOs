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

Ten-million-history extension (seed 2468; restartable by cell)::

    python -m experiments.massive_mechanism_map --preset ten-million --backend cupy
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import platform
import subprocess
from dataclasses import asdict, dataclass, replace
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


SCRIPT_VERSION = "1.1.0"
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


@dataclass(frozen=True)
class TenMillionConfig(MonsterConfig):
    """Exactly ten million histories over 35 (sample-size, sigma) cells.

    Unequal cell counts differ by at most one. Replications per cell are
    distributed in main; a 256-history batch keeps GPU memory bounded.
    """
    root_seed: int = 2468
    replications: int = 0
    target_histories: int = 10_000_000
    batch_size: int = 256


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


def _summarize_cell_chunked(
    *,
    cfg: TenMillionConfig,
    n_obs: int,
    sigma_true: float,
    replications: int,
    sigma_grid: np.ndarray,
    price_curves: np.ndarray,
    scenarios: pd.DataFrame,
    xp: Any,
    resolved: str,
    checkpoint_dir: Path,
) -> tuple[pd.DataFrame, dict[str, Any]]:
    """Streaming ten-million run, with exact percentiles using disk-backed gaps.

    A dense (replications x sigma grid) posterior would exceed available RAM
    and GPU memory. Each batch gets its own deterministic SeedSequence-based
    seed. Only the current batch's posterior matrix stays in RAM/GPU memory;
    a temporary per-cell memmap stores absolute pricing gaps to calculate
    exact, rather than approximated, percentiles at the end of the cell.
    Completed cell CSV+JSON files are the durable restart checkpoints.
    """
    n_scenarios = len(scenarios)
    grid_xp = xp.asarray(sigma_grid, dtype=xp.float64)
    curves_xp = xp.asarray(price_curves, dtype=xp.float64)
    curvature = np.gradient(
        np.gradient(price_curves, sigma_grid, axis=0, edge_order=2),
        sigma_grid, axis=0, edge_order=2,
    )
    gap_sum = np.zeros(n_scenarios)
    abs_sum = np.zeros(n_scenarios)
    gap_sq_sum = np.zeros(n_scenarios)
    taylor_sum = np.zeros(n_scenarios)
    taylor_sq_sum = np.zeros(n_scenarios)
    cross_sum = np.zeros(n_scenarios)
    diff_sq_sum = np.zeros(n_scenarios)
    diff_abs_sum = np.zeros(n_scenarios)
    max_abs = np.zeros(n_scenarios)
    post_mean_sum = 0.0
    post_sd_sum = 0.0

    tmp = checkpoint_dir / (
        "temporary_abs_gaps_n" + str(n_obs)
        + "_sigma" + str(int(round(1000 * sigma_true))) + ".dat"
    )
    abs_gaps = np.memmap(
        tmp, dtype=np.float64, mode="w+", shape=(replications, n_scenarios)
    )
    try:
        for start in range(0, replications, cfg.batch_size):
            count = min(cfg.batch_size, replications - start)
            sums, sums2 = gaussian_sufficient_statistics_simulation(
                n_obs=n_obs,
                mu_true=cfg.mu_true,
                sigma_true=sigma_true,
                dt=cfg.historical_dt,
                replications=count,
                seed=_seed(
                    cfg.root_seed, n_obs, int(round(1000 * sigma_true)), start
                ),
            )
            weights = _posterior_weights_backend(
                cfg, n_obs=n_obs, sum_returns=sums,
                sumsq_returns=sums2, sigma_grid=sigma_grid, xp=xp,
            )
            mean_xp = weights @ grid_xp
            var_xp = xp.maximum(
                weights @ (grid_xp**2) - mean_xp**2, 0.0
            )
            mean = _to_numpy(mean_xp, resolved).reshape(-1)
            variance = _to_numpy(var_xp, resolved).reshape(-1)
            pi = _to_numpy(weights @ curves_xp, resolved)
            pm = _interpolate_uniform_curves(mean, sigma_grid, price_curves)
            gap = pi - pm
            taylor = (
                0.5 * variance[:, None] *
                _interpolate_uniform_curves(mean, sigma_grid, curvature)
            )
            abs_chunk = np.abs(gap)
            abs_gaps[start:start + count, :] = abs_chunk
            gap_sum += np.sum(gap, axis=0)
            abs_sum += np.sum(abs_chunk, axis=0)
            gap_sq_sum += np.sum(gap * gap, axis=0)
            taylor_sum += np.sum(taylor, axis=0)
            taylor_sq_sum += np.sum(taylor * taylor, axis=0)
            cross_sum += np.sum(taylor * gap, axis=0)
            diff_sq_sum += np.sum((gap - taylor)**2, axis=0)
            diff_abs_sum += np.sum(np.abs(gap - taylor), axis=0)
            max_abs = np.maximum(max_abs, np.max(abs_chunk, axis=0))
            post_mean_sum += float(np.sum(mean))
            post_sd_sum += float(np.sum(np.sqrt(variance)))
            del weights, mean_xp, var_xp, pi, pm, gap, taylor
            if resolved == "cupy":
                xp.get_default_memory_pool().free_all_blocks()
            if (start // cfg.batch_size + 1) % 50 == 0:
                print(
                    "  cell n=" + str(n_obs)
                    + " sigma=" + str(sigma_true)
                    + ": " + str(start + count) + "/" + str(replications),
                    flush=True,
                )
        abs_gaps.flush()
        rows = []
        for j, scenario in enumerate(scenarios.itertuples(index=False)):
            # Exact medians/percentiles computed on every underlying history.
            quant = np.quantile(abs_gaps[:, j], (0.50, 0.95, 0.99))
            var_actual = gap_sq_sum[j] - gap_sum[j]**2 / replications
            var_approx = taylor_sq_sum[j] - taylor_sum[j]**2 / replications
            cov = cross_sum[j] - gap_sum[j] * taylor_sum[j] / replications
            corr = (
                float(cov / np.sqrt(var_actual * var_approx))
                if var_actual > 0 and var_approx > 0 else np.nan
            )
            slope = (
                float(cross_sum[j] / taylor_sq_sum[j])
                if taylor_sq_sum[j] > 0 else np.nan
            )
            rows.append({
                "n_obs": int(n_obs),
                "sigma_true": float(sigma_true),
                "replications": int(replications),
                "scenario_id": int(scenario.scenario_id),
                "maturity_days": int(scenario.maturity_days),
                "fraction_fixed": float(scenario.fraction_fixed),
                "moneyness": float(scenario.moneyness),
                "mean_posterior_sigma": float(post_mean_sum / replications),
                "mean_posterior_sigma_sd": float(post_sd_sum / replications),
                "mean_pi_minus_pm": float(gap_sum[j] / replications),
                "mean_abs_pi_minus_pm": float(abs_sum[j] / replications),
                "median_abs_pi_minus_pm": float(quant[0]),
                "p95_abs_pi_minus_pm": float(quant[1]),
                "p99_abs_pi_minus_pm": float(quant[2]),
                "max_abs_pi_minus_pm": float(max_abs[j]),
                "mean_taylor_gap": float(taylor_sum[j] / replications),
                "taylor_mae": float(diff_abs_sum[j] / replications),
                "taylor_rmse": float(
                    np.sqrt(diff_sq_sum[j] / replications)
                ),
                "taylor_corr": corr,
                "taylor_slope_through_origin": slope,
            })
        cell = {
            "n_obs": int(n_obs),
            "sigma_true": float(sigma_true),
            "replications": int(replications),
            "posterior_sigma_mean_mean": float(post_mean_sum / replications),
            "posterior_sigma_mean_bias": float(
                post_mean_sum / replications - sigma_true
            ),
            "posterior_sigma_sd_mean": float(post_sd_sum / replications),
        }
        return pd.DataFrame(rows), cell
    finally:
        del abs_gaps
        tmp.unlink(missing_ok=True)



def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--preset", choices=("quick", "research", "monster", "ten-million"), default="research")
    parser.add_argument("--backend", choices=("auto", "numpy", "cupy"), default="auto")
    parser.add_argument("--output-root", type=Path, default=DEFAULT_OUTPUT_ROOT)
    parser.add_argument(
        "--seed", type=int, default=None,
        help="Optional root seed override. The ten-million preset defaults to 2468.",
    )
    parser.add_argument("--force", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    cfg: MechanismConfig
    if args.preset == "quick":
        cfg = QuickConfig()
    elif args.preset == "monster":
        cfg = MonsterConfig()
    elif args.preset == "ten-million":
        cfg = TenMillionConfig()
    else:
        cfg = MechanismConfig()
    if args.seed is not None:
        cfg = replace(cfg, root_seed=args.seed)

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

    cells_total = len(cfg.sample_sizes) * len(cfg.sigma_true_values)
    for n_obs in cfg.sample_sizes:
        for sigma_index, sigma_true in enumerate(cfg.sigma_true_values):
            cell_index = len(cell_rows)
            if isinstance(cfg, TenMillionConfig):
                required_reps = (
                    cfg.target_histories // cells_total
                    + int(cell_index < cfg.target_histories % cells_total)
                )
            else:
                required_reps = cfg.replications
            path = checkpoint_dir / f"n{n_obs}_s{sigma_index:02d}.csv"
            meta_path = checkpoint_dir / f"n{n_obs}_s{sigma_index:02d}.json"
            if path.exists() and meta_path.exists() and not args.force:
                cached = json.loads(meta_path.read_text(encoding="utf-8"))
                if int(cached["replications"]) == required_reps:
                    summaries.append(pd.read_csv(path))
                    cell_rows.append(cached)
                    print(f"Reusing cell n={n_obs}, sigma={sigma_true:.3f}", flush=True)
                    continue
            print(
                f"Running cell n={n_obs}, sigma={sigma_true:.3f}, "
                f"reps={required_reps}, root_seed={cfg.root_seed}, "
                f"grid={cfg.sigma_grid_points}, scenarios={len(scenarios)}, "
                f"backend={resolved}",
                flush=True,
            )
            if isinstance(cfg, TenMillionConfig):
                summary, cell = _summarize_cell_chunked(
                    cfg=cfg, n_obs=n_obs, sigma_true=sigma_true,
                    replications=required_reps, sigma_grid=sigma_grid,
                    price_curves=price_curves, scenarios=scenarios,
                    xp=xp, resolved=resolved, checkpoint_dir=checkpoint_dir,
                )
            else:
                summary, cell = _summarize_cell(
                    cfg=cfg, n_obs=n_obs, sigma_true=sigma_true,
                    replications=required_reps, sigma_grid=sigma_grid,
                    price_curves=price_curves, scenarios=scenarios,
                    xp=xp, resolved=resolved,
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
        "synthetic_datasets": int(sum(x["replications"] for x in cell_rows)),
        "posterior_grid_evaluations": int(
            sum(x["replications"] for x in cell_rows) * cfg.sigma_grid_points
        ),
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
