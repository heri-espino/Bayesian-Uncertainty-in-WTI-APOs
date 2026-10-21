"""Audit how existing Barchart APO history becomes strict-forward evaluation dates.

This is a diagnostic only. It reuses the canonical source/date eligibility
logic and does *not* refit volatility, price contracts, or download data.

Example
-------
python -m experiments.wti_aao_existing_attrition
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import pandas as pd

from bayesian_asian_options.barchart_apo import (
    build_apo_panel,
    discover_barchart_histories,
)
from experiments.wti_apo_date_panel import _date_audit
from experiments.wti_expiry_coverage_audit import DEFAULT_EXPIRIES

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "results" / "analysis" / "wti_aao_history_feasibility"


def _summarize_raw(panel: pd.DataFrame) -> pd.DataFrame:
    """Count distinct market keys, reported marks and liquidity by expiry/date."""
    keys = ("trade_date", "expiry_month", "strike", "option_type")
    missing = set(keys).difference(panel.columns)
    if missing:
        raise ValueError(f"Barchart panel is missing columns: {sorted(missing)}")
    data = panel.copy()
    data["valuation_date"] = pd.to_datetime(
        data["trade_date"], errors="coerce"
    ).dt.strftime("%Y-%m-%d")
    if data["valuation_date"].isna().any():
        raise ValueError("Invalid Barchart valuation date")
    data["market_price_numeric"] = pd.to_numeric(
        data["market_price"], errors="coerce"
    )
    data["vol_numeric"] = pd.to_numeric(
        data["volume"], errors="coerce"
    )
    data["oi_numeric"] = pd.to_numeric(
        data["open_interest"], errors="coerce"
    )
    data["duplicate_key"] = data.duplicated(
        ["valuation_date", "expiry_month", "strike", "option_type"],
        keep="first",
    )
    data["valid_mark"] = (
        data["market_price_numeric"].notna()
        & data["market_price_numeric"].ge(0)
    )
    data["positive_volume_contract"] = data["vol_numeric"].gt(0)
    data["positive_oi_contract"] = data["oi_numeric"].gt(0)
    rows = (
        data.groupby(["expiry_month", "valuation_date"], sort=True)
        .agg(
            n_raw_options=("contract_id", "size"),
            n_unique_option_keys=("duplicate_key", lambda x: int((~x).sum())),
            n_duplicate_option_keys=("duplicate_key", "sum"),
            n_valid_market_marks=("valid_mark", "sum"),
            n_positive_volume_contracts_raw=("positive_volume_contract", "sum"),
            n_positive_oi_contracts_raw=("positive_oi_contract", "sum"),
        )
        .reset_index()
        .rename(columns={"expiry_month": "apo_expiry"})
    )
    return rows


def _summarize_holdouts(frame: pd.DataFrame) -> pd.DataFrame:
    """Report genuinely distinct matched targets, never method-duplicated rows."""
    columns = [
        "apo_expiry", "valuation_date", "n_forward_holdout_keys",
    ]
    if frame.empty:
        return pd.DataFrame(columns=columns)
    required = {"apo_expiry", "valuation_date", "contract_id"}
    if not required.issubset(frame.columns):
        raise ValueError(
            "Forward holdout file lacks apo_expiry/valuation_date/contract_id"
        )
    dedup = frame.drop_duplicates(
        ["apo_expiry", "valuation_date", "contract_id"]
    )
    return (
        dedup.groupby(["apo_expiry", "valuation_date"], sort=True)
        .size().rename("n_forward_holdout_keys").reset_index()
    )


def build_attrition_report(
    raw: pd.DataFrame,
    audits: dict[str, pd.DataFrame],
    forward_holdouts: pd.DataFrame,
    *,
    min_smile_contracts: int = 6,
) -> tuple[pd.DataFrame, dict[str, object]]:
    """Construct descriptive, date/expiry-specific eligibility decomposition.

    "Prior smile available" means an earlier *eligible* day had at least
    min_smile_contracts; it is only a necessary coverage condition and does
    not certify that the full smile/IV calibration succeeded.
    """
    if min_smile_contracts < 1:
        raise ValueError("min_smile_contracts must be positive")
    raw_summary = _summarize_raw(raw)
    if raw_summary.empty:
        raise ValueError("The source APO panel is empty")
    audit_frames = []
    for expiry, audit in audits.items():
        if audit.empty:
            continue
        copy = audit.copy()
        copy["apo_expiry"] = str(expiry)
        audit_frames.append(copy)
    if not audit_frames:
        raise ValueError("No Barchart/CL coverage audits were available")
    audited = pd.concat(audit_frames, ignore_index=True)
    joined = raw_summary.merge(
        audited.drop(columns=["n_raw_options"], errors="ignore"),
        on=["apo_expiry", "valuation_date"], how="left", validate="one_to_one",
    )
    joined["audited_date"] = joined["eligible"].notna()
    joined["eligible"] = joined["eligible"].fillna(False).astype(bool)
    joined["smile_ready"] = (
        joined["eligible"] & joined["n_main_sample"].fillna(0).ge(min_smile_contracts)
    )
    joined = joined.sort_values(["apo_expiry", "valuation_date"]).reset_index(drop=True)
    joined["has_strictly_earlier_smile_date"] = False
    for _, positions in joined.groupby("apo_expiry", sort=False).groups.items():
        ix = list(positions)
        ready = joined.loc[ix, "smile_ready"]
        joined.loc[ix, "has_strictly_earlier_smile_date"] = (
            ready.cumsum().shift(fill_value=0).gt(0).to_numpy()
        )
    joined["forward_coverage_candidate"] = (
        joined["smile_ready"] & joined["has_strictly_earlier_smile_date"]
    )
    actual = _summarize_holdouts(forward_holdouts)
    joined = joined.merge(
        actual, on=["apo_expiry", "valuation_date"],
        how="left", validate="one_to_one",
    )
    joined["n_forward_holdout_keys"] = (
        joined["n_forward_holdout_keys"].fillna(0).astype(int)
    )
    joined["in_recorded_forward_panel"] = joined["n_forward_holdout_keys"].gt(0)
    summary = {
        "scope": "diagnostic_only_not_a_reestimated_forward_model",
        "raw_market_rows": int(len(raw)),
        "raw_distinct_market_keys": int(raw.drop_duplicates(
            ["trade_date", "expiry_month", "strike", "option_type"]
        ).shape[0]),
        "raw_distinct_dates": int(pd.to_datetime(raw["trade_date"]).dt.date.nunique()),
        "raw_distinct_expiries": int(raw["expiry_month"].nunique()),
        "expiry_date_pairs": int(len(joined)),
        "dates_with_eligible_curve_and_marks": int(
            joined.loc[joined["eligible"], "valuation_date"].nunique()
        ),
        "dates_with_at_least_one_smile_ready_expiry": int(
            joined.loc[joined["smile_ready"], "valuation_date"].nunique()
        ),
        "dates_with_prior_smile_coverage_candidate": int(
            joined.loc[joined["forward_coverage_candidate"], "valuation_date"].nunique()
        ),
        "recorded_forward_unique_dates": int(
            joined.loc[joined["in_recorded_forward_panel"], "valuation_date"].nunique()
        ),
        "recorded_forward_unique_contract_date_keys": int(
            joined["n_forward_holdout_keys"].sum()
        ),
        "prior_smile_condition_is_necessary_not_sufficient": True,
        "warning": (
            "Date eligibility and prior smile availability alone do not prove "
            "successful IV calibration, historical posterior support, or LO availability."
        ),
        "by_expiry": [],
    }
    for expiry, group in joined.groupby("apo_expiry", sort=True):
        summary["by_expiry"].append({
            "apo_expiry": str(expiry),
            "raw_rows": int(group["n_raw_options"].sum()),
            "raw_dates": int(len(group)),
            "eligible_dates": int(group["eligible"].sum()),
            "smile_ready_dates": int(group["smile_ready"].sum()),
            "prior_smile_candidate_dates": int(group["forward_coverage_candidate"].sum()),
            "recorded_forward_dates": int(group["in_recorded_forward_panel"].sum()),
            "recorded_forward_holdout_keys": int(group["n_forward_holdout_keys"].sum()),
        })
    return joined, summary


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--option-data-dir", type=Path, default=ROOT / "data" / "csv")
    parser.add_argument("--cl-data-dir", type=Path, default=ROOT / "data" / "csv" / "CL")
    parser.add_argument(
        "--cl-expiry-file", type=Path,
        default=ROOT / "data" / "csv" / "CL" / "contract_expiries.csv",
    )
    parser.add_argument("--forward-predictions", type=Path, default=(
        ROOT / "results" / "analysis" / "wti_extended_forward"
        / "forward_q_validation" / "forward_q_predictions.csv"
    ))
    parser.add_argument("--expiries", nargs="+", default=DEFAULT_EXPIRIES)
    parser.add_argument("--min-open-interest", type=float, default=1.0)
    parser.add_argument("--min-smile-contracts", type=int, default=6)
    parser.add_argument("--include-min-tick", action="store_true")
    parser.add_argument("--output-dir", type=Path, default=OUTPUT)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    files = discover_barchart_histories(args.option_data_dir)
    raw = build_apo_panel(files, deduplicate_contracts=True)
    expiry_names = list(dict.fromkeys(map(str, args.expiries)))
    audits = {}
    failures = {}
    for expiry in expiry_names:
        try:
            audits[expiry] = _date_audit(
                option_data_dir=args.option_data_dir,
                cl_data_dir=args.cl_data_dir,
                cl_expiry_file=args.cl_expiry_file,
                apo_expiry=expiry,
                min_open_interest=float(args.min_open_interest),
                exclude_min_tick=not args.include_min_tick,
            )
        except (FileNotFoundError, ValueError, RuntimeError) as exc:
            failures[expiry] = f"{type(exc).__name__}: {exc}"
    if args.forward_predictions.exists():
        forward = pd.read_csv(args.forward_predictions, low_memory=False)
        forward_status = "loaded_exact_forward_predictions"
    else:
        forward = pd.DataFrame()
        forward_status = "missing_forward_predictions; recorded counts unknown"
    detail, summary = build_attrition_report(
        raw, audits, forward,
        min_smile_contracts=args.min_smile_contracts,
    )
    summary["forward_source_status"] = forward_status
    summary["audit_failures"] = failures
    summary["raw_file_count"] = len(files)
    summary["min_open_interest"] = float(args.min_open_interest)
    summary["exclude_min_tick"] = not args.include_min_tick
    summary["min_smile_contracts"] = args.min_smile_contracts
    args.output_dir.mkdir(parents=True, exist_ok=True)
    detail.to_csv(args.output_dir / "existing_sample_attrition.csv", index=False)
    (args.output_dir / "existing_sample_attrition.json").write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
