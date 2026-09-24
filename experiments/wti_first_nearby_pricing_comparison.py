"""Compare Yahoo-CL=F and reconstructed-first-nearby pricing baselines.

Run this only after both extended forward-validation namespaces are complete.
The comparison fails closed unless the contract-date holdouts match exactly.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]


def _contract_key(frame: pd.DataFrame) -> list[str]:
    return (
        frame["valuation_date"].astype(str)
        + "|"
        + frame["apo_expiry"].astype(str)
        + "|"
        + frame["contract_id"].astype(str)
    ).tolist()


def _deduplicated_baseline(frame: pd.DataFrame) -> pd.DataFrame:
    required = {
        "valuation_date",
        "apo_expiry",
        "contract_id",
        "market_settlement",
        "baseline_pi_price",
        "baseline_pi_error",
    }
    missing = required.difference(frame.columns)
    if missing:
        raise ValueError(f"Forward predictions missing columns: {sorted(missing)}")
    cols = [
        "valuation_date",
        "apo_expiry",
        "contract_id",
        "market_settlement",
        "baseline_pi_price",
        "baseline_pi_error",
    ]
    return frame[cols].drop_duplicates(
        ["valuation_date", "apo_expiry", "contract_id"], keep="first"
    ).sort_values(
        ["valuation_date", "apo_expiry", "contract_id"]
    ).reset_index(drop=True)


def _metrics(errors: np.ndarray) -> dict[str, float]:
    e = np.asarray(errors, dtype=float)
    return {
        "mean_error": float(np.mean(e)),
        "mae": float(np.mean(np.abs(e))),
        "rmse": float(np.sqrt(np.mean(e**2))),
    }


def compare_baselines(
    yahoo: pd.DataFrame,
    first_nearby: pd.DataFrame,
) -> tuple[pd.DataFrame, pd.DataFrame, dict[str, Any]]:
    """Compare historical-P baselines on exact common holdouts."""
    y = _deduplicated_baseline(yahoo)
    f = _deduplicated_baseline(first_nearby)

    y_keys = set(_contract_key(y))
    f_keys = set(_contract_key(f))
    if y_keys != f_keys:
        only_yahoo = sorted(y_keys - f_keys)
        only_first = sorted(f_keys - y_keys)
        raise RuntimeError(
            "Holdout mismatch between Yahoo and first-nearby runs. "
            f"Yahoo-only={only_yahoo[:5]}, first-nearby-only={only_first[:5]}"
        )

    merged = y.merge(
        f,
        on=["valuation_date", "apo_expiry", "contract_id"],
        suffixes=("_yahoo", "_first_nearby"),
        validate="one_to_one",
    )
    market_gap = (
        merged["market_settlement_yahoo"]
        - merged["market_settlement_first_nearby"]
    ).abs().max()
    if float(market_gap) > 1e-12:
        raise RuntimeError("Market settlements differ between the two holdout panels")

    rows: list[dict[str, Any]] = []
    scopes: list[tuple[str, str, pd.DataFrame]] = [
        ("pooled", "all", merged)
    ]
    for expiry, group in merged.groupby("apo_expiry", sort=True):
        scopes.append(("expiry", str(expiry), group))

    for scope, expiry, group in scopes:
        for source, column in (
            ("yahoo_CL=F", "baseline_pi_error_yahoo"),
            ("reconstructed_first_nearby", "baseline_pi_error_first_nearby"),
        ):
            metrics = _metrics(group[column].to_numpy(dtype=float))
            rows.append(
                {
                    "scope": scope,
                    "apo_expiry": expiry,
                    "source": source,
                    "n": int(len(group)),
                    "n_dates": int(group["valuation_date"].nunique()),
                    **metrics,
                }
            )
    summary = pd.DataFrame(rows)

    pooled = summary.loc[summary["scope"].eq("pooled")].set_index("source")
    yahoo_rmse = float(pooled.loc["yahoo_CL=F", "rmse"])
    first_rmse = float(pooled.loc["reconstructed_first_nearby", "rmse"])
    yahoo_mae = float(pooled.loc["yahoo_CL=F", "mae"])
    first_mae = float(pooled.loc["reconstructed_first_nearby", "mae"])

    report = {
        "holdouts_match_exactly": True,
        "n_contract_dates": int(len(merged)),
        "n_valuation_dates": int(merged["valuation_date"].nunique()),
        "expiries": sorted(merged["apo_expiry"].astype(str).unique().tolist()),
        "yahoo_baseline_mae": yahoo_mae,
        "yahoo_baseline_rmse": yahoo_rmse,
        "first_nearby_baseline_mae": first_mae,
        "first_nearby_baseline_rmse": first_rmse,
        "delta_mae_first_nearby_minus_yahoo": first_mae - yahoo_mae,
        "delta_rmse_first_nearby_minus_yahoo": first_rmse - yahoo_rmse,
        "rmse_ratio_first_nearby_to_yahoo": first_rmse / yahoo_rmse,
        "interpretation_guardrail": (
            "This table measures sensitivity of the historical-P pricing baseline "
            "to return-source/roll construction. Option-informed Q results must be "
            "compared on the same holdouts before revising the manuscript hierarchy."
        ),
    }
    return merged, summary, report


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--yahoo-forward",
        type=Path,
        default=(
            ROOT
            / "results"
            / "analysis"
            / "wti_extended_forward"
            / "forward_q_validation"
            / "forward_q_predictions.csv"
        ),
    )
    parser.add_argument(
        "--first-nearby-forward",
        type=Path,
        default=(
            ROOT
            / "results"
            / "analysis"
            / "wti_extended_forward_first_nearby"
            / "forward_q_validation"
            / "forward_q_predictions.csv"
        ),
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=ROOT / "results" / "analysis" / "wti_first_nearby",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if not args.yahoo_forward.exists():
        raise FileNotFoundError(args.yahoo_forward)
    if not args.first_nearby_forward.exists():
        raise FileNotFoundError(args.first_nearby_forward)

    merged, summary, report = compare_baselines(
        pd.read_csv(args.yahoo_forward),
        pd.read_csv(args.first_nearby_forward),
    )
    args.output_dir.mkdir(parents=True, exist_ok=True)
    merged.to_csv(
        args.output_dir / "pricing_holdout_comparison.csv",
        index=False,
    )
    summary.to_csv(
        args.output_dir / "pricing_baseline_summary.csv",
        index=False,
    )
    (args.output_dir / "pricing_comparison_report.json").write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
