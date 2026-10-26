"""Inventory local Barchart APO histories independently of AAO private SQLite.

Use when Barchart CSVs are rehydrated by sparse-checkout but the
private Databento cross-month SQLite state cannot be located.
This is a *source-availability* check, not a Databento/Barchart price
comparison. Reads CSVs only. No paid API requests or licensed price rows
are exported.
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

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CSV_ROOT = ROOT / "data" / "csv"
DEFAULT_OUTPUT = (
    ROOT / "results" / "analysis" / "wti_aao_history_feasibility"
    / "barchart" / "barchart_source_inventory.json"
)


def inventory(csv_root: Path) -> dict:
    """Aggregate existing Barchart contract histories without AAO inputs."""
    csv_root = Path(csv_root)
    if not csv_root.is_dir():
        return {
            "available": False,
            "csv_root_exists": False,
            "all_csv_files": 0,
            "barchart_option_history_files": 0,
            "reason": "Local CSV directory missing; check sparse checkout or path",
            "barchart_aao_overlap_calculated": False,
            "contract_price_parity_checked": False,
            "no_databento_requests": True,
        }

    paths = discover_barchart_histories(csv_root)
    all_csv_count = sum(1 for _ in csv_root.rglob("*.csv"))
    if not paths:
        return {
            "available": False,
            "csv_root_exists": True,
            "all_csv_files": all_csv_count,
            "barchart_option_history_files": 0,
            "reason": "No files match the existing JAO contract filename parser",
            "barchart_aao_overlap_calculated": False,
            "contract_price_parity_checked": False,
            "no_databento_requests": True,
        }

    panel = build_apo_panel(paths)
    dates = pd.to_datetime(panel["trade_date"], errors="raise")
    valid_marks = pd.to_numeric(panel["market_price"], errors="coerce").notna()
    return {
        "available": True,
        "csv_root_exists": True,
        "all_csv_files": all_csv_count,
        "barchart_option_history_files": len(paths),
        "distinct_option_contracts": int(panel["contract_id"].nunique()),
        "deduplicated_history_rows": int(len(panel)),
        "rows_with_latest_price": int(valid_marks.sum()),
        "distinct_history_dates": int(dates.dt.date.nunique()),
        "first_history_date": dates.min().strftime("%Y-%m-%d"),
        "last_history_date": dates.max().strftime("%Y-%m-%d"),
        "barchart_aao_overlap_calculated": False,
        "contract_price_parity_checked": False,
        "no_databento_requests": True,
        "warning": (
            "Only validates local Barchart history availability. "
            "Date overlap with AAO and identical-contract price parity "
            "require the separate private Databento SQLite state."
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--csv-root", type=Path, default=DEFAULT_CSV_ROOT)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    report = inventory(args.csv_root)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(report, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(report, indent=2))
    if not report["available"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
