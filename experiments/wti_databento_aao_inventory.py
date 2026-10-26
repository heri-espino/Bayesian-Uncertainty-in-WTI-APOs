"""Audit local AAO monthly DBN files without making any Databento API calls.

Exploratory inventory only: final settlement reference dates are not yet
verified as usable independent pricing/test dates. Run --all after a sample.
"""

from __future__ import annotations

import argparse
from collections import Counter
import json
from pathlib import Path
from typing import Any

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data" / "databento" / "wti_aao_bulk" / "raw"
OUTPUT_DIR = ROOT / "results" / "analysis" / "wti_aao_history_feasibility" / "inventory"


def frequencies(frame: pd.DataFrame, column: str, limit: int = 12) -> dict[str, int]:
    if column not in frame.columns:
        return {}
    values = frame[column].dropna().astype(str).str.strip().value_counts().head(limit)
    return {str(k): int(v) for k, v in values.items()}


def reference_dates(series: pd.Series) -> pd.Series:
    if pd.api.types.is_numeric_dtype(series):
        return pd.to_datetime(series, unit="ns", utc=True, errors="coerce").dt.date
    return pd.to_datetime(series, utc=True, errors="coerce").dt.date


def summarize_definition(frame: pd.DataFrame) -> dict[str, Any]:
    row: dict[str, Any] = {"records": int(len(frame))}
    for column in ("asset", "group", "exchange", "instrument_class",
                   "security_type", "underlying"):
        row["top_" + column] = frequencies(frame, column)
    if "raw_symbol" in frame:
        row["unique_symbols"] = int(frame["raw_symbol"].nunique(dropna=True))
    if "expiration" in frame:
        row["distinct_expirations"] = int(
            reference_dates(frame["expiration"]).nunique()
        )
    if "strike_price" in frame:
        row["distinct_strikes"] = int(
            pd.to_numeric(frame["strike_price"], errors="coerce").nunique()
        )
    return row


def summarize_statistics(frame: pd.DataFrame) -> dict[str, Any]:
    row: dict[str, Any] = {"records": int(len(frame))}
    if "stat_type" not in frame:
        row["error"] = "No stat_type column"
        return row
    types = pd.to_numeric(frame["stat_type"], errors="coerce")
    row["stat_type_counts"] = {
        str(k): int(v) for k, v in types.value_counts().items()
    }
    settles = frame.loc[types.eq(3)].copy()
    row["settlement_events"] = int(len(settles))
    if "stat_flags" not in settles:
        row["error"] = "No stat_flags column"
        return row
    flags = pd.to_numeric(
        settles["stat_flags"], errors="coerce"
    ).fillna(0).astype("int64")
    final = flags.mod(2).eq(1)
    actual = (flags // 2).mod(2).eq(1)
    row["final_events"] = int(final.sum())
    row["final_actual_events"] = int((final & actual).sum())
    row["final_theoretical_events"] = int((final & ~actual).sum())
    row["preliminary_events"] = int((~final).sum())
    if "ts_ref" in settles:
        dates = reference_dates(settles["ts_ref"])
        row["settlement_reference_dates"] = int(dates.nunique())
        row["final_reference_dates"] = int(dates[final].nunique())
        row["final_actual_reference_dates"] = int(
            dates[final & actual].nunique()
        )
        row["_final_dates"] = sorted(
            str(item) for item in set(dates[final].dropna())
        )
        if dates.notna().any():
            row["first_reference_date"] = str(dates.min())
            row["last_reference_date"] = str(dates.max())
        if "symbol" in settles and settles["symbol"].notna().any():
            keys = pd.DataFrame({
                "trading_date": dates[final],
                "symbol": settles.loc[final, "symbol"],
            }).dropna().drop_duplicates()
            row["final_symbol_date_pairs"] = int(len(keys))
            row["pair_key"] = "mapped symbol, needs contract validation"
        else:
            row["pair_key"] = "unavailable: no mapped symbol"
    for stat_code, label in ((6, "cleared_volume"), (9, "open_interest")):
        entries = frame.loc[types.eq(stat_code)]
        row[label + "_events"] = int(len(entries))
        if "quantity" in entries:
            row["positive_" + label + "_events"] = int(
                pd.to_numeric(
                    entries["quantity"], errors="coerce"
                ).gt(0).sum()
            )
    return row


def inspect(
    raw_directory: Path, *, months: set[str] | None
) -> dict[str, Any]:
    import databento as db

    report: dict[str, Any] = {
        "no_network_requests": True,
        "months": [],
        "errors": [],
    }
    definitions = sorted(raw_directory.glob("aao_definition__*.dbn.zst"))
    for definitions_path in definitions:
        suffix = definitions_path.name.removeprefix("aao_definition__")
        month = suffix[:7]
        if months is not None and month not in months:
            continue
        statistics_path = raw_directory / ("aao_statistics__" + suffix)
        if not statistics_path.is_file():
            report["errors"].append({
                "month": month, "error": "statistics file missing"
            })
            continue
        try:
            defs = db.DBNStore.from_file(definitions_path).to_df()
            defs_result = summarize_definition(defs)
            del defs
            stats = db.DBNStore.from_file(statistics_path).to_df()
            stats_result = summarize_statistics(stats)
            del stats
            report["months"].append({
                "month": month,
                "definitions": defs_result,
                "statistics": stats_result,
            })
        except Exception as exc:
            report["errors"].append({
                "month": month,
                "error": f"{type(exc).__name__}: {str(exc)[:300]}",
            })
    totals: Counter[str] = Counter()
    unique_final_dates: set[str] = set()
    for pair in report["months"]:
        stats = pair["statistics"]
        unique_final_dates.update(stats.pop("_final_dates", []))
        for key in ("records", "settlement_events", "final_events",
                    "final_actual_events", "final_theoretical_events",
                    "positive_cleared_volume_events",
                    "positive_open_interest_events"):
            totals[key] += int(stats.get(key, 0))
    report["summary"] = {
        "months_processed": len(report["months"]),
        "distinct_final_reference_dates": len(unique_final_dates),
        **dict(totals),
    }
    return report


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--all", action="store_true")
    parser.add_argument(
        "--months", nargs="+",
        default=["2023-06", "2025-06", "2026-06"],
    )
    parser.add_argument("--data-dir", type=Path, default=DATA_DIR)
    parser.add_argument("--output-dir", type=Path, default=OUTPUT_DIR)
    args = parser.parse_args()
    if not args.data_dir.is_dir():
        parser.error(f"Local data not found: {args.data_dir}")
    report = inspect(
        args.data_dir,
        months=None if args.all else set(args.months),
    )
    args.output_dir.mkdir(parents=True, exist_ok=True)
    output = args.output_dir / "aao_inventory_summary.json"
    output.write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps({
        "summary": report["summary"],
        "errors": report["errors"],
        "report": str(output),
    }, indent=2))
    for pair in report["months"]:
        stats = pair["statistics"]
        print(json.dumps({
            "month": pair["month"],
            "assets": pair["definitions"].get("top_asset"),
            "classes": pair["definitions"].get("top_instrument_class"),
            "settlement_events": stats.get("settlement_events"),
            "final_events": stats.get("final_events"),
            "final_actual_events": stats.get("final_actual_events"),
        }, indent=2))


if __name__ == "__main__":
    main()
