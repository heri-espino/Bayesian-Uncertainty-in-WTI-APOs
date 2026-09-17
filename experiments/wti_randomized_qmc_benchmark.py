"""Randomized Sobol QMC benchmark for difficult empirical WTI APO states.

This experiment is a numerically independent companion to the pseudo-random GPU Monte Carlo
stress test.  For each selected target it generates scrambled Sobol Brownian paths, reuses the
same low-discrepancy paths over a dense sigma grid, and prices the complete posterior map.
Independent Sobol scrambles provide an empirical randomization error for PI, PM, and PI-PM.

The target set defaults to the contracts selected by ``wti_high_precision_pricing`` when that
file exists; otherwise it recreates the same mechanical adverse-target selection.
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
from scipy.special import ndtri
from scipy.stats import qmc

from bayesian_asian_options.asian_futures_pricing import curran_arithmetic_futures_option
from experiments.wti_curran_benchmark import _posterior_draws, _state
from experiments.wti_high_precision_pricing import _backend, _candidate_targets, _scalar


DEFAULT_RUNS_ROOT = Path("results/wti_apo_empirical")
DEFAULT_HIGH_PRECISION_ROOT = Path("results/analysis/wti_high_precision_pricing")
DEFAULT_OUTPUT_ROOT = Path("results/analysis/wti_randomized_qmc")


@dataclass(frozen=True)
class Config:
    targets: int = 6
    sigma_grid_points: int = 61
    sobol_power: int = 19
    scrambles: int = 6
    root_seed: int = 20260918


@dataclass(frozen=True)
class MonsterConfig(Config):
    targets: int = 8
    sigma_grid_points: int = 121
    sobol_power: int = 21
    scrambles: int = 8


def _atomic_checkpoint(
    path: Path,
    *,
    grid: np.ndarray,
    prices: np.ndarray,
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(".tmp.npz")
    np.savez_compressed(temporary, grid=grid, prices=prices)
    os.replace(temporary, path)


def _selected_targets(
    *,
    preset: str,
    runs_root: Path,
    high_precision_root: Path,
    expiries: list[str],
    limit: int,
) -> pd.DataFrame:
    existing = high_precision_root / f"selected_targets_{preset}.csv"
    if existing.exists():
        frame = pd.read_csv(existing)
    else:
        frame = _candidate_targets(runs_root, expiries, max(3, limit))
    if frame.empty:
        raise RuntimeError("no QMC target contracts were available")
    # Preserve the deterministic selection order and limit the QMC audit to the most adverse
    # subset so each target can receive substantially more low-discrepancy paths.
    return frame.head(limit).reset_index(drop=True)


def _brownian_paths(
    *,
    times: np.ndarray,
    power: int,
    scramble_seed: int,
    backend: str,
) -> tuple[Any, Any, str]:
    xp, resolved = _backend(backend)
    n_future = len(times)
    if n_future < 1:
        return xp.empty((1, 0), dtype=xp.float64), xp, resolved
    engine = qmc.Sobol(d=n_future, scramble=True, seed=int(scramble_seed))
    uniforms = engine.random_base2(m=int(power))
    eps = np.finfo(float).eps
    np.clip(uniforms, eps, 1.0 - eps, out=uniforms)
    z = ndtri(uniforms)
    del uniforms
    dt = np.diff(np.concatenate([[0.0], np.asarray(times, dtype=float)]))
    w = np.cumsum(z * np.sqrt(dt)[None, :], axis=1)
    del z
    return xp.asarray(w, dtype=xp.float64), xp, resolved


def _qmc_price(
    *,
    brownian: Any,
    xp: Any,
    resolved: str,
    realized: np.ndarray,
    forwards: np.ndarray,
    times: np.ndarray,
    strike: float,
    option_type: str,
    sigma: float,
    discount: float,
) -> float:
    n_paths = int(brownian.shape[0])
    n_future = len(forwards)
    total = len(realized) + n_future
    expected_average = float((np.sum(realized) + np.sum(forwards)) / total)
    if n_future == 0:
        payoff = (
            max(expected_average - strike, 0.0)
            if option_type == "call"
            else max(strike - expected_average, 0.0)
        )
        return float(discount * payoff)

    forwards_xp = xp.asarray(forwards, dtype=xp.float64)
    times_xp = xp.asarray(times, dtype=xp.float64)
    future = forwards_xp[None, :] * xp.exp(
        -0.5 * float(sigma) ** 2 * times_xp[None, :] + float(sigma) * brownian
    )
    average = (float(np.sum(realized)) + xp.sum(future, axis=1)) / float(total)
    if option_type == "call":
        payoff = xp.maximum(average - float(strike), 0.0)
    else:
        payoff = xp.maximum(float(strike) - average, 0.0)
    y = float(discount) * payoff

    # The arithmetic average itself is a zero-mean control after subtracting its exact Q
    # expectation.  Estimating beta within each randomized QMC replicate preserves the target
    # expectation; cross-scramble dispersion is the numerical uncertainty diagnostic.
    x = float(discount) * (average - expected_average)
    mean_y = _scalar(xp.mean(y), resolved)
    mean_x = _scalar(xp.mean(x), resolved)
    xc = x - mean_x
    yc = y - mean_y
    var_x = _scalar(xp.mean(xc * xc), resolved)
    if var_x > 0:
        cov_xy = _scalar(xp.mean(xc * yc), resolved)
        beta = cov_xy / var_x
        price = mean_y - beta * mean_x
    else:
        price = mean_y
    del future, average, payoff, y, x, xc, yc
    return float(price)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--preset", choices=("research", "monster"), default="research")
    parser.add_argument("--backend", choices=("auto", "numpy", "cupy"), default="auto")
    parser.add_argument("--expiries", nargs="+", default=["2026-09", "2026-10"])
    parser.add_argument("--runs-root", type=Path, default=DEFAULT_RUNS_ROOT)
    parser.add_argument("--high-precision-root", type=Path, default=DEFAULT_HIGH_PRECISION_ROOT)
    parser.add_argument("--output-root", type=Path, default=DEFAULT_OUTPUT_ROOT)
    parser.add_argument("--force", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    cfg: Config = MonsterConfig() if args.preset == "monster" else Config()
    args.output_root.mkdir(parents=True, exist_ok=True)
    checkpoint_dir = args.output_root / "checkpoints" / args.preset
    checkpoint_dir.mkdir(parents=True, exist_ok=True)
    report_path = args.output_root / f"qmc_report_{args.preset}.json"
    if report_path.exists() and not args.force:
        print(f"Reusing completed output: {report_path}", flush=True)
        return

    targets = _selected_targets(
        preset=args.preset,
        runs_root=args.runs_root,
        high_precision_root=args.high_precision_root,
        expiries=list(args.expiries),
        limit=cfg.targets,
    )
    targets.to_csv(args.output_root / f"qmc_targets_{args.preset}.csv", index=False)
    curve_rows: list[dict[str, Any]] = []
    summary_rows: list[dict[str, Any]] = []
    n_paths = 2**cfg.sobol_power

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
                    raise RuntimeError(f"QMC checkpoint grid mismatch: {checkpoint}")
                prices = data["prices"].astype(float)
        else:
            prices = np.full((cfg.scrambles, len(grid)), np.nan, dtype=float)

        print(
            f"QMC target {target_index + 1}/{len(targets)}: {target.valuation_date} "
            f"{target.contract_id}; paths/scramble={n_paths:,}, scrambles={cfg.scrambles}, "
            f"sigma_nodes={len(grid)}",
            flush=True,
        )
        for scramble in range(cfg.scrambles):
            missing = np.flatnonzero(~np.isfinite(prices[scramble]))
            if missing.size == 0:
                continue
            brownian, xp, resolved = _brownian_paths(
                times=times,
                power=cfg.sobol_power,
                scramble_seed=cfg.root_seed + 100_000 * target_index + 10_000 * scramble,
                backend=args.backend,
            )
            for j in missing:
                sigma = float(grid[j])
                prices[scramble, j] = _qmc_price(
                    brownian=brownian,
                    xp=xp,
                    resolved=resolved,
                    realized=realized,
                    forwards=forwards,
                    times=times,
                    strike=float(target.strike),
                    option_type=str(target.option_type).lower(),
                    sigma=sigma,
                    discount=discount,
                )
                _atomic_checkpoint(checkpoint, grid=grid, prices=prices)
                print(
                    f"  scramble {scramble + 1}/{cfg.scrambles}, sigma {j + 1}/{len(grid)}",
                    flush=True,
                )
            del brownian
            if resolved == "cupy":
                xp.get_default_memory_pool().free_all_blocks()

        if np.any(~np.isfinite(prices)):
            raise RuntimeError(f"incomplete QMC checkpoint: {checkpoint}")

        scramble_pi = np.asarray(
            [float(np.mean(np.interp(sigma_draws, grid, curve))) for curve in prices]
        )
        scramble_pm = np.asarray(
            [float(np.interp(sigma_mean, grid, curve)) for curve in prices]
        )
        scramble_gap = scramble_pi - scramble_pm
        mean_curve = prices.mean(axis=0)
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
            ],
            dtype=float,
        )
        qmc_pi = float(np.mean(scramble_pi))
        qmc_pm = float(np.mean(scramble_pm))
        curran_pi = float(np.mean(np.interp(sigma_draws, grid, curran_curve)))
        curran_pm = float(np.interp(sigma_mean, grid, curran_curve))

        for scramble in range(cfg.scrambles):
            for j, sigma in enumerate(grid):
                curve_rows.append(
                    {
                        "target_index": target_index,
                        "valuation_date": target.valuation_date,
                        "apo_expiry": target.apo_expiry,
                        "contract_id": target.contract_id,
                        "scramble": scramble,
                        "sigma": float(sigma),
                        "qmc_price": float(prices[scramble, j]),
                    }
                )

        summary_rows.append(
            {
                "target_index": target_index,
                "valuation_date": target.valuation_date,
                "apo_expiry": target.apo_expiry,
                "contract_id": target.contract_id,
                "option_type": target.option_type,
                "strike": float(target.strike),
                "market_price": float(target.market_price),
                "posterior_source": posterior_source,
                "posterior_sigma_mean": sigma_mean,
                "qmc_pi": qmc_pi,
                "qmc_pm": qmc_pm,
                "qmc_pi_minus_pm": qmc_pi - qmc_pm,
                "qmc_pi_mcse": float(np.std(scramble_pi, ddof=1) / np.sqrt(cfg.scrambles)),
                "qmc_pm_mcse": float(np.std(scramble_pm, ddof=1) / np.sqrt(cfg.scrambles)),
                "qmc_gap_mcse": float(np.std(scramble_gap, ddof=1) / np.sqrt(cfg.scrambles)),
                "curran_pi": curran_pi,
                "curran_pm": curran_pm,
                "curran_pi_minus_pm": curran_pi - curran_pm,
                "curran_minus_qmc_pi": curran_pi - qmc_pi,
                "curran_minus_qmc_pm": curran_pm - qmc_pm,
                "mean_curve_pi": float(np.mean(np.interp(sigma_draws, grid, mean_curve))),
            }
        )

    pd.DataFrame(curve_rows).to_csv(
        args.output_root / f"qmc_curves_{args.preset}.csv", index=False
    )
    pd.DataFrame(summary_rows).to_csv(
        args.output_root / f"qmc_summary_{args.preset}.csv", index=False
    )
    report = {
        "preset": args.preset,
        "targets": int(len(targets)),
        "sobol_power": cfg.sobol_power,
        "paths_per_scramble": int(n_paths),
        "scrambles": cfg.scrambles,
        "sigma_grid_points": cfg.sigma_grid_points,
        "path_sigma_evaluations": int(
            len(targets) * n_paths * cfg.scrambles * cfg.sigma_grid_points
        ),
        "randomization": "independently scrambled Sobol sequences; cross-scramble dispersion is used for numerical uncertainty",
        "control_variate": "discounted arithmetic average minus its exact Q expectation",
        "checkpoint_policy": "Each completed scramble/sigma price is checkpointed and reused after interruption.",
    }
    report_path.write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(f"Completed randomized QMC benchmark: {args.output_root}", flush=True)


if __name__ == "__main__":
    main()
