"""Liquidity-stratified cluster bootstrap for WTI pricing-error comparisons.

Contract observations on the same valuation date are strongly dependent.  This experiment
therefore resamples valuation dates, not individual contracts.  It reports uncertainty for
the change in MAE and RMSE relative to the historical-volatility posterior-integrated
baseline across volume/open-interest strata.

The implementation bootstraps date-level sufficient error sums, so 100k+ replications are
cheap even though the underlying option panel is cross-sectionally dense.
"""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd


DEFAULT_IV = Path("results/analysis/wti_apo_implied_volatility/apo_contract_implied_volatility.csv")
DEFAULT_LOO = Path("results/analysis/wti_apo_implied_volatility/apo_loo_predictions.csv")
DEFAULT_TRANSFER = Path("results/analysis/wti_apo_implied_volatility/apo_cross_type_predictions.csv")
DEFAULT_FORWARD = Path("results/analysis/wti_forward_q_validation/forward_q_predictions.csv")
DEFAULT_OUTPUT_ROOT = Path("results/analysis/wti_liquidity_bootstrap")


def _merge_liquidity(frame: pd.DataFrame, iv: pd.DataFrame) -> pd.DataFrame:
    keys = ["valuation_date", "apo_expiry", "contract_id"]
    meta = iv[keys + ["open_interest", "volume", "positive_volume"]].drop_duplicates(keys)
    drop = [c for c in ("open_interest", "volume", "positive_volume") if c in frame.columns]
    return frame.drop(columns=drop).merge(meta, on=keys, how="left", validate="many_to_one")


def _cluster_bootstrap(
    frame: pd.DataFrame,
    *,
    model_error: str,
    baseline_error: str,
    iterations: int,
    seed: int,
) -> dict[str, Any]:
    if frame.empty:
        raise ValueError("cannot bootstrap an empty frame")
    work = frame[["valuation_date", model_error, baseline_error]].dropna().copy()
    work["model_abs"] = work[model_error].abs()
    work["base_abs"] = work[baseline_error].abs()
    work["model_sq"] = work[model_error] ** 2
    work["base_sq"] = work[baseline_error] ** 2
    grouped = (
        work.groupby("valuation_date", sort=True)
        .agg(
            n=(model_error, "size"),
            model_abs=("model_abs", "sum"),
            base_abs=("base_abs", "sum"),
            model_sq=("model_sq", "sum"),
            base_sq=("base_sq", "sum"),
        )
        .reset_index()
    )
    k = len(grouped)
    if k < 2:
        raise ValueError("at least two valuation-date clusters are required")
    rng = np.random.default_rng(seed)
    counts = rng.multinomial(k, np.full(k, 1.0 / k), size=iterations).astype(float)
    n = counts @ grouped["n"].to_numpy(dtype=float)
    model_abs = counts @ grouped["model_abs"].to_numpy(dtype=float)
    base_abs = counts @ grouped["base_abs"].to_numpy(dtype=float)
    model_sq = counts @ grouped["model_sq"].to_numpy(dtype=float)
    base_sq = counts @ grouped["base_sq"].to_numpy(dtype=float)
    delta_mae = model_abs / n - base_abs / n
    delta_rmse = np.sqrt(model_sq / n) - np.sqrt(base_sq / n)

    model_error_values = work[model_error].to_numpy(dtype=float)
    base_error_values = work[baseline_error].to_numpy(dtype=float)
    point_mae = float(np.mean(np.abs(model_error_values)) - np.mean(np.abs(base_error_values)))
    point_rmse = float(
        np.sqrt(np.mean(model_error_values**2)) - np.sqrt(np.mean(base_error_values**2))
    )
    return {
        "n": int(len(work)),
        "clusters": int(k),
        "delta_mae": point_mae,
        "delta_mae_ci025": float(np.quantile(delta_mae, 0.025)),
        "delta_mae_ci975": float(np.quantile(delta_mae, 0.975)),
        "probability_mae_improvement": float(np.mean(delta_mae < 0)),
        "delta_rmse": point_rmse,
        "delta_rmse_ci025": float(np.quantile(delta_rmse, 0.025)),
        "delta_rmse_ci975": float(np.quantile(delta_rmse, 0.975)),
        "probability_rmse_improvement": float(np.mean(delta_rmse < 0)),
    }


def _samples(frame: pd.DataFrame) -> dict[str, pd.DataFrame]:
    samples = {"all": frame}
    if "positive_volume" in frame.columns:
        samples["positive_volume"] = frame[frame["positive_volume"].fillna(False)]
    if "open_interest" in frame.columns:
        for threshold in (1, 10, 100, 500):
            samples[f"open_interest_ge_{threshold}"] = frame[
                frame["open_interest"].fillna(-np.inf) >= threshold
            ]
    return samples


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--preset", choices=("research", "monster"), default="research")
    parser.add_argument("--iv", type=Path, default=DEFAULT_IV)
    parser.add_argument("--loo", type=Path, default=DEFAULT_LOO)
    parser.add_argument("--transfer", type=Path, default=DEFAULT_TRANSFER)
    parser.add_argument("--forward", type=Path, default=DEFAULT_FORWARD)
    parser.add_argument("--output-root", type=Path, default=DEFAULT_OUTPUT_ROOT)
    parser.add_argument("--seed", type=int, default=20260917)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    iterations = 100_000 if args.preset == "monster" else 20_000
    if not args.iv.exists():
        raise FileNotFoundError(args.iv)
    iv = pd.read_csv(args.iv)
    datasets: list[tuple[str, pd.DataFrame, str, str]] = []

    if args.loo.exists():
        datasets.append(
            (
                "leave_one_contract_out",
                _merge_liquidity(pd.read_csv(args.loo), iv),
                "loo_error",
                "baseline_pi_error",
            )
        )
    if args.transfer.exists():
        datasets.append(
            (
                "cross_option_type_transfer",
                _merge_liquidity(pd.read_csv(args.transfer), iv),
                "transfer_error",
                "baseline_pi_error",
            )
        )
    if args.forward.exists():
        forward = pd.read_csv(args.forward)
        for method, group in forward.groupby("method"):
            datasets.append(
                (
                    f"forward_q_{method}",
                    group.copy(),
                    "forward_error",
                    "baseline_pi_error",
                )
            )
    if not datasets:
        raise RuntimeError("no pricing-comparison datasets were found")

    rows: list[dict[str, Any]] = []
    sequence = 0
    for experiment, frame, model_error, baseline_error in datasets:
        for sample_name, sample in _samples(frame).items():
            # A cluster CI is undefined with fewer than two dates; retain that fact rather
            # than silently falling back to an iid contract bootstrap.
            if sample.empty or sample["valuation_date"].nunique() < 2:
                continue
            sequence += 1
            stats = _cluster_bootstrap(
                sample,
                model_error=model_error,
                baseline_error=baseline_error,
                iterations=iterations,
                seed=args.seed + sequence,
            )
            rows.append(
                {
                    "experiment": experiment,
                    "sample": sample_name,
                    "bootstrap_iterations": iterations,
                    **stats,
                }
            )

    result = pd.DataFrame(rows)
    args.output_root.mkdir(parents=True, exist_ok=True)
    result.to_csv(args.output_root / f"liquidity_cluster_bootstrap_{args.preset}.csv", index=False)
    print(
        f"Completed {iterations:,} valuation-date cluster bootstraps per eligible comparison: "
        f"{args.output_root}",
        flush=True,
    )


if __name__ == "__main__":
    main()
