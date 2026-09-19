"""Audit which WTI APO expiries can support strict forward-in-time validation.

This audit is deliberately lightweight: it uses only committed APO histories, the committed
Barchart CL strip, and the explicit CL expiry table.  It does not run MCMC or option pricing.

For each expiry it applies the same date-eligibility logic as
:mod:`experiments.wti_apo_date_panel` and then reports how many eligible dates contain enough
main-sample contracts to fit the six-parameter quadratic call/put smile used by
:mod:`experiments.wti_forward_q_validation`.

The output is intended to decide which expiries are worth sending through the expensive
production pipeline before any new MCMC/Monte Carlo run is launched.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

from experiments.wti_apo_date_panel import _date_audit
from experiments.wti_apo_empirical import ROOT


DEFAULT_EXPIRIES = [
    "2026-09",
    "2026-10",
    "2026-11",
    "2027-03",
    "2027-09",
    "2028-03",
    "2028-09",
    "2029-06",
]


def audit_expiries(
    *,
    expiries: list[str],
    option_data_dir: Path,
    cl_data_dir: Path,
    cl_expiry_file: Path,
    min_open_interest: float,
    exclude_min_tick: bool,
    min_smile_contracts: int,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    detail_frames: list[pd.DataFrame] = []
    summary_rows: list[dict[str, object]] = []

    for expiry in expiries:
        audit = _date_audit(
            option_data_dir=option_data_dir,
            cl_data_dir=cl_data_dir,
            cl_expiry_file=cl_expiry_file,
            apo_expiry=expiry,
            min_open_interest=min_open_interest,
            exclude_min_tick=exclude_min_tick,
        ).copy()
        if audit.empty:
            summary_rows.append(
                {
                    "apo_expiry": expiry,
                    "observed_dates": 0,
                    "eligible_dates": 0,
                    "smile_ready_dates": 0,
                    "forward_target_dates": 0,
                    "first_smile_ready_date": None,
                    "last_smile_ready_date": None,
                    "max_main_sample_contracts": 0,
                    "positive_volume_dates": 0,
                    "positive_volume_contract_dates": 0,
                    "oi10_smile_ready_dates": 0,
                }
            )
            continue

        audit.insert(0, "apo_expiry", expiry)
        audit["smile_ready"] = (
            audit["eligible"].fillna(False)
            & (audit["n_main_sample"] >= int(min_smile_contracts))
        )
        # A strict forward target requires at least one earlier smile-ready date.
        smile_dates = pd.to_datetime(
            audit.loc[audit["smile_ready"], "valuation_date"]
        ).sort_values()
        first_smile = smile_dates.iloc[0] if len(smile_dates) else None
        audit["forward_target_ready"] = False
        if first_smile is not None:
            dates = pd.to_datetime(audit["valuation_date"])
            audit["forward_target_ready"] = (
                audit["smile_ready"] & (dates > first_smile)
            )

        # OI>=10 is not the production sample rule, but this diagnostic asks whether
        # a reasonably deep cross-section remains after a simple liquidity screen.
        # The date audit only stores total main-sample counts, so the exact OI>=10
        # contract count is computed later by the pricing/liquidity stage.
        audit["oi10_smile_ready"] = pd.NA

        eligible = audit[audit["eligible"]]
        ready = audit[audit["smile_ready"]]
        summary_rows.append(
            {
                "apo_expiry": expiry,
                "observed_dates": int(len(audit)),
                "eligible_dates": int(audit["eligible"].sum()),
                "smile_ready_dates": int(audit["smile_ready"].sum()),
                "forward_target_dates": int(audit["forward_target_ready"].sum()),
                "first_smile_ready_date": (
                    ready["valuation_date"].iloc[0] if not ready.empty else None
                ),
                "last_smile_ready_date": (
                    ready["valuation_date"].iloc[-1] if not ready.empty else None
                ),
                "max_main_sample_contracts": int(
                    eligible["n_main_sample"].max()
                )
                if not eligible.empty
                else 0,
                "positive_volume_dates": int(
                    ((eligible["n_positive_volume"] > 0)).sum()
                ),
                "positive_volume_contract_dates": int(
                    eligible["n_positive_volume"].sum()
                ),
                "oi10_smile_ready_dates": None,
            }
        )
        detail_frames.append(audit)

    summary = pd.DataFrame(summary_rows)
    detail = (
        pd.concat(detail_frames, ignore_index=True)
        if detail_frames
        else pd.DataFrame()
    )
    return summary, detail


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--expiries", nargs="+", default=DEFAULT_EXPIRIES)
    parser.add_argument(
        "--option-data-dir", type=Path, default=ROOT / "data" / "csv"
    )
    parser.add_argument(
        "--cl-data-dir", type=Path, default=ROOT / "data" / "csv" / "CL"
    )
    parser.add_argument(
        "--cl-expiry-file",
        type=Path,
        default=ROOT / "data" / "csv" / "CL" / "contract_expiries.csv",
    )
    parser.add_argument("--min-open-interest", type=float, default=1.0)
    parser.add_argument("--include-min-tick", action="store_true")
    parser.add_argument("--min-smile-contracts", type=int, default=6)
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=ROOT / "results" / "analysis" / "wti_expiry_coverage_audit",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    summary, detail = audit_expiries(
        expiries=[str(x) for x in args.expiries],
        option_data_dir=args.option_data_dir,
        cl_data_dir=args.cl_data_dir,
        cl_expiry_file=args.cl_expiry_file,
        min_open_interest=float(args.min_open_interest),
        exclude_min_tick=not args.include_min_tick,
        min_smile_contracts=int(args.min_smile_contracts),
    )
    args.output_dir.mkdir(parents=True, exist_ok=True)
    summary.to_csv(args.output_dir / "expiry_coverage_summary.csv", index=False)
    detail.to_csv(args.output_dir / "expiry_date_audit.csv", index=False)

    print("\nWTI APO expiry coverage audit")
    print("=" * 80)
    if summary.empty:
        print("No expiries audited.")
    else:
        print(summary.to_string(index=False))
    print(
        f"\nA forward target requires an eligible date with >= "
        f"{args.min_smile_contracts} main-sample contracts and at least one earlier "
        "smile-ready date."
    )
    print(f"output_dir={args.output_dir}")


if __name__ == "__main__":
    main()
