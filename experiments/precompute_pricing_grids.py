"""Precompute risk-neutral pricing grids with one atomic checkpoint per sigma point.

Run this before ``experiments.large_scale_synthetic`` on machines that may disconnect.
The completed grid files use exactly the paths expected by the large-scale experiment,
so the later stage detects them and skips all completed GPU pricing work.
"""

from __future__ import annotations

import argparse
import os
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

from experiments.large_scale_synthetic import (
    _atomic_json,
    _atomic_npz,
    _config_for_preset,
    _fingerprint,
    _monitoring_steps,
    _price_grid_path,
    _seed,
)
from bayesian_asian_options.accelerated_pricing import asian_arithmetic_call_mc_chunked


def _point_path(run_dir: Path, mi: int, ti: int, point: int) -> Path:
    return (
        run_dir
        / "checkpoints"
        / "pricing_points"
        / f"m{mi:02d}_t{ti:02d}"
        / f"sigma_{point:04d}.npz"
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--preset", choices=("quick", "research", "extreme"), default="research")
    parser.add_argument("--backend", choices=("auto", "numpy", "cupy"), default="auto")
    parser.add_argument("--output-root", type=Path, default=Path("results/large_scale_synthetic"))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    cfg = _config_for_preset(args.preset)
    run_dir = args.output_root / _fingerprint(cfg)
    run_dir.mkdir(parents=True, exist_ok=True)

    sigma_grid = np.linspace(cfg.price_sigma_min, cfg.price_sigma_max, cfg.price_grid_points)
    total = len(cfg.moneyness_values) * len(cfg.maturities) * len(sigma_grid)
    done = 0

    for mi, moneyness in enumerate(cfg.moneyness_values):
        for ti, maturity in enumerate(cfg.maturities):
            full_path = _price_grid_path(run_dir, mi, ti)
            if full_path.exists():
                done += len(sigma_grid)
                continue

            common_seed = _seed(cfg.root_seed, 601, mi, ti)
            K = cfg.S0 * moneyness
            steps = _monitoring_steps(maturity)
            prices = np.empty_like(sigma_grid)
            ses = np.empty_like(sigma_grid)
            resolved_backend = "unknown"

            for i, sigma in enumerate(sigma_grid):
                point_path = _point_path(run_dir, mi, ti, i)
                if point_path.exists():
                    with np.load(point_path, allow_pickle=False) as data:
                        prices[i] = float(data["price"].item())
                        ses[i] = float(data["standard_error"].item())
                        resolved_backend = str(data["backend"].item())
                else:
                    estimate = asian_arithmetic_call_mc_chunked(
                        cfg.S0,
                        K,
                        cfg.r,
                        float(sigma),
                        maturity,
                        q=cfg.q,
                        n_steps=steps,
                        n_paths=cfg.pricing_paths,
                        seed=common_seed,
                        backend=args.backend,
                        chunk_size=cfg.pricing_chunk_size,
                        antithetic=True,
                        geometric_control=True,
                    )
                    prices[i] = estimate.price
                    ses[i] = estimate.standard_error
                    resolved_backend = estimate.backend
                    _atomic_npz(
                        point_path,
                        sigma=np.array(float(sigma)),
                        price=np.array(estimate.price),
                        standard_error=np.array(estimate.standard_error),
                        raw_price=np.array(estimate.raw_price),
                        raw_standard_error=np.array(estimate.raw_standard_error),
                        control_beta=np.array(estimate.control_beta),
                        backend=np.array(estimate.backend),
                        seed=np.array(common_seed),
                        n_paths=np.array(cfg.pricing_paths),
                        monitoring_steps=np.array(steps),
                    )

                done += 1
                _atomic_json(
                    run_dir / "pricing_progress.json",
                    {
                        "stage": "pricing_grid_points",
                        "preset": args.preset,
                        "backend_requested": args.backend,
                        "completed_points": done,
                        "total_points": total,
                        "remaining_points": total - done,
                        "current": {
                            "moneyness_index": mi,
                            "maturity_index": ti,
                            "sigma_index": i,
                            "sigma": float(sigma),
                        },
                        "updated_at_utc": datetime.now(timezone.utc).isoformat(),
                    },
                )
                print(
                    f"[{done}/{total}] m={moneyness:.2f} T={maturity:.2f} "
                    f"sigma={sigma:.4f} backend={resolved_backend}",
                    flush=True,
                )

            _atomic_npz(
                full_path,
                sigma_grid=sigma_grid,
                prices=prices,
                standard_errors=ses,
                backend=np.array(resolved_backend),
                moneyness=np.array(moneyness),
                maturity=np.array(maturity),
                monitoring_steps=np.array(steps),
                seed=np.array(common_seed),
            )

    _atomic_json(
        run_dir / "pricing_progress.json",
        {
            "stage": "pricing_complete",
            "preset": args.preset,
            "completed_points": total,
            "total_points": total,
            "remaining_points": 0,
            "updated_at_utc": datetime.now(timezone.utc).isoformat(),
        },
    )
    print(f"pricing grids complete: {run_dir}")


if __name__ == "__main__":
    main()
