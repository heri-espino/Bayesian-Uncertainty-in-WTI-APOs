"""Test the second-order mechanism behind posterior-integrated Asian pricing.

The large-scale synthetic experiment stores posterior volatility draws and smooth
common-random-number pricing grids.  This analysis reuses those checkpoints to compare

    C_PI - C_PM

with the second-order approximation

    0.5 * C''(E[sigma|D]) * Var(sigma|D).

No posterior fitting or path simulation is repeated.  The script is therefore intended
as the publication analysis layer for an already completed ``large_scale_synthetic`` run.

Examples
--------
    python -m experiments.taylor_mechanism
    python -m experiments.taylor_mechanism \
        --run-dir results/large_scale_synthetic/f497062f0c571126
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd


DEFAULT_RUN = Path("results/large_scale_synthetic/f497062f0c571126")
DEFAULT_OUTPUT = Path("results/analysis/taylor_mechanism")
SCENARIO = ["n_obs", "sigma_true", "moneyness_K_over_S0", "maturity"]


def _clean_float(value: Any) -> float:
    return float(np.asarray(value).item())


def _load_inference(path: Path) -> tuple[np.ndarray, dict[str, Any]]:
    with np.load(path, allow_pickle=False) as data:
        draws = data["sigma_draws"].astype(float)
        meta = json.loads(str(data["meta_json"].item()))
    if draws.ndim != 1 or draws.size < 3:
        raise ValueError(f"invalid sigma checkpoint: {path}")
    return draws, meta


def _load_price_grid(path: Path) -> dict[str, Any]:
    with np.load(path, allow_pickle=False) as data:
        sigma = data["sigma_grid"].astype(float)
        prices = data["prices"].astype(float)
        moneyness = _clean_float(data["moneyness"])
        maturity = _clean_float(data["maturity"])
    if sigma.ndim != 1 or prices.ndim != 1 or sigma.size != prices.size:
        raise ValueError(f"invalid pricing checkpoint: {path}")
    if sigma.size < 5 or np.any(np.diff(sigma) <= 0):
        raise ValueError(f"pricing grid must be strictly increasing with >=5 points: {path}")
    return {
        "sigma_grid": sigma,
        "prices": prices,
        "moneyness": moneyness,
        "maturity": maturity,
    }


def local_quadratic_curvature(
    sigma_grid: np.ndarray,
    prices: np.ndarray,
    sigma0: float,
    *,
    points: int = 9,
) -> float:
    """Estimate ``d^2 C / d sigma^2`` by a local quadratic fit.

    Common random numbers make the stored price curve very smooth, but a local quadratic
    is more stable than differencing three Monte Carlo points directly.  ``points`` is
    forced to an odd number and clipped to the available grid size.
    """
    x = np.asarray(sigma_grid, dtype=float)
    y = np.asarray(prices, dtype=float)
    if x.ndim != 1 or y.ndim != 1 or x.size != y.size:
        raise ValueError("sigma_grid and prices must be equal-length one-dimensional arrays")
    if x.size < 5 or np.any(np.diff(x) <= 0):
        raise ValueError("sigma_grid must contain at least five strictly increasing points")
    if not np.isfinite(sigma0) or sigma0 < x[0] or sigma0 > x[-1]:
        raise ValueError("sigma0 must lie inside the pricing grid")

    k = max(5, min(int(points), x.size))
    if k % 2 == 0:
        k -= 1
    center = int(np.searchsorted(x, sigma0))
    half = k // 2
    lo = max(0, min(center - half, x.size - k))
    hi = lo + k
    dx = x[lo:hi] - sigma0
    coeff = np.polyfit(dx, y[lo:hi], deg=2)
    return float(2.0 * coeff[0])


def _safe_corr(x: pd.Series, y: pd.Series) -> float | None:
    a = np.asarray(x, dtype=float)
    b = np.asarray(y, dtype=float)
    if a.size < 2 or np.std(a) == 0 or np.std(b) == 0:
        return None
    return float(np.corrcoef(a, b)[0, 1])


def _slope_through_origin(x: np.ndarray, y: np.ndarray) -> float | None:
    denom = float(np.dot(x, x))
    if denom <= 0:
        return None
    return float(np.dot(x, y) / denom)


def analyze(run_dir: Path) -> tuple[pd.DataFrame, pd.DataFrame, dict[str, Any]]:
    inference_paths = sorted((run_dir / "checkpoints" / "inference").glob("**/rep_*.npz"))
    pricing_paths = sorted((run_dir / "checkpoints" / "pricing").glob("m*_t*.npz"))
    if not inference_paths:
        raise FileNotFoundError(f"no inference checkpoints below {run_dir}")
    if not pricing_paths:
        raise FileNotFoundError(f"no pricing checkpoints below {run_dir}")

    grids = [_load_price_grid(path) for path in pricing_paths]
    rows: list[dict[str, Any]] = []
    for path in inference_paths:
        draws, meta = _load_inference(path)
        sigma_mean = float(np.mean(draws))
        sigma_var = float(np.var(draws, ddof=1))
        for grid in grids:
            sg = grid["sigma_grid"]
            prices = grid["prices"]
            if draws.min() < sg[0] or draws.max() > sg[-1]:
                raise RuntimeError(
                    f"posterior support in {path} falls outside pricing grid "
                    f"[{sg[0]:.4f}, {sg[-1]:.4f}]"
                )
            posterior_prices = np.interp(draws, sg, prices)
            posterior_integrated = float(np.mean(posterior_prices))
            posterior_mean_plugin = float(np.interp(sigma_mean, sg, prices))
            actual_gap = posterior_integrated - posterior_mean_plugin
            curvature = local_quadratic_curvature(sg, prices, sigma_mean)
            taylor_gap = 0.5 * curvature * sigma_var
            rows.append(
                {
                    "n_obs": int(meta["n_obs"]),
                    "sigma_true": float(meta["sigma_true"]),
                    "replication": int(meta["replication"]),
                    "moneyness_K_over_S0": float(grid["moneyness"]),
                    "maturity": float(grid["maturity"]),
                    "sigma_post_mean": sigma_mean,
                    "sigma_post_variance": sigma_var,
                    "pricing_curvature": curvature,
                    "actual_pi_minus_pm": actual_gap,
                    "taylor_pi_minus_pm": taylor_gap,
                    "taylor_residual": actual_gap - taylor_gap,
                    "abs_actual_gap": abs(actual_gap),
                    "abs_taylor_gap": abs(taylor_gap),
                    "abs_taylor_residual": abs(actual_gap - taylor_gap),
                }
            )

    raw = pd.DataFrame(rows)
    summary_rows: list[dict[str, Any]] = []
    for keys, group in raw.groupby(SCENARIO, sort=True):
        actual = group["actual_pi_minus_pm"].to_numpy(dtype=float)
        approx = group["taylor_pi_minus_pm"].to_numpy(dtype=float)
        residual = actual - approx
        summary_rows.append(
            {
                **dict(zip(SCENARIO, keys)),
                "replications": int(len(group)),
                "mean_sigma_post_variance": float(group["sigma_post_variance"].mean()),
                "mean_pricing_curvature": float(group["pricing_curvature"].mean()),
                "mean_actual_gap": float(actual.mean()),
                "mean_taylor_gap": float(approx.mean()),
                "median_abs_actual_gap": float(np.median(np.abs(actual))),
                "median_abs_taylor_gap": float(np.median(np.abs(approx))),
                "mae_taylor_approximation": float(np.mean(np.abs(residual))),
                "rmse_taylor_approximation": float(np.sqrt(np.mean(residual**2))),
                "corr_actual_taylor": _safe_corr(
                    group["actual_pi_minus_pm"], group["taylor_pi_minus_pm"]
                ),
                "slope_actual_on_taylor_through_origin": _slope_through_origin(approx, actual),
            }
        )
    summary = pd.DataFrame(summary_rows)

    actual = raw["actual_pi_minus_pm"].to_numpy(dtype=float)
    approx = raw["taylor_pi_minus_pm"].to_numpy(dtype=float)
    residual = actual - approx
    report = {
        "source_run": str(run_dir),
        "inference_checkpoints": len(inference_paths),
        "pricing_grids": len(pricing_paths),
        "raw_rows": int(len(raw)),
        "scenario_rows": int(len(summary)),
        "overall": {
            "correlation_actual_vs_taylor": _safe_corr(
                raw["actual_pi_minus_pm"], raw["taylor_pi_minus_pm"]
            ),
            "slope_actual_on_taylor_through_origin": _slope_through_origin(approx, actual),
            "mae_taylor_approximation": float(np.mean(np.abs(residual))),
            "rmse_taylor_approximation": float(np.sqrt(np.mean(residual**2))),
            "median_abs_actual_gap": float(np.median(np.abs(actual))),
            "median_abs_taylor_gap": float(np.median(np.abs(approx))),
        },
        "interpretation": (
            "The Taylor diagnostic is mechanism evidence, not a pricing estimator. "
            "Agreement near slope one supports the decomposition of the PI-PM gap into "
            "posterior volatility dispersion times local pricing curvature."
        ),
    }
    return raw, summary, report


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-dir", type=Path, default=DEFAULT_RUN)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    raw, summary, report = analyze(args.run_dir)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    raw.to_csv(args.output_dir / "taylor_mechanism_raw.csv", index=False)
    summary.to_csv(args.output_dir / "taylor_mechanism_summary.csv", index=False)
    with (args.output_dir / "taylor_mechanism_report.json").open("w", encoding="utf-8") as fh:
        json.dump(report, fh, indent=2, sort_keys=True)
        fh.write("\n")
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
