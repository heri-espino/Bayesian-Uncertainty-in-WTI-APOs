"""Offline diagnostic of whether AAO definition IDs join settlement statistics.

This is NOT a historically time-aware contract master, pricing panel, or
independent-date experiment. No symbol/price-level market values are exported.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "databento" / "wti_aao_bulk" / "raw"
REPORT = (ROOT / "results" / "analysis" / "wti_aao_history_feasibility"
          / "identity_probe")


def analyze(definitions: pd.DataFrame, statistics: pd.DataFrame) -> dict[str, Any]:
    """Count tentative same-month instrument-ID coverage without guessing."""
    report: dict[str, Any] = {
        "definition_events": int(len(definitions)),
        "statistics_events": int(len(statistics)),
        "definition_columns": list(map(str, definitions.columns)),
        "statistics_columns": list(map(str, statistics.columns)),
        "warning": (
            "Identity coverage is not a time-aware as-of join. An instrument "
            "ID can be reused; never treat these counts as validated contract prices."
        ),
    }
    if "asset" in definitions:
        report["asset_counts"] = {
            str(x): int(y) for x, y in
            definitions["asset"].astype(str).value_counts().items()
        }
    if "instrument_class" in definitions:
        report["instrument_class_counts"] = {
            str(x): int(y) for x, y in
            definitions["instrument_class"].astype(str).value_counts().items()
        }

    keys = ["publisher_id", "instrument_id"]
    if any(col not in definitions for col in keys):
        report["blocking_error"] = "Definitions lack publisher_id/instrument_id"
        return report
    if any(col not in statistics for col in keys):
        report["blocking_error"] = "Statistics lack publisher_id/instrument_id"
        return report
    if "stat_type" not in statistics or "stat_flags" not in statistics:
        report["blocking_error"] = "Statistics lack stat_type/stat_flags"
        return report
    types = pd.to_numeric(statistics["stat_type"], errors="coerce")
    if types.notna().sum() == 0:
        report["blocking_error"] = "stat_type was not interpreted as integer codes"
        return report
    settlements = statistics.loc[types.eq(3)]
    report["settlement_events"] = int(len(settlements))
    flags = pd.to_numeric(settlements["stat_flags"], errors="coerce")
    if flags.isna().any():
        report["blocking_error"] = "Settlement flags contain unknown codes"
        return report
    final = (flags.astype("int64") & 1) == 1
    final_events = settlements.loc[final]
    report["final_settlement_events"] = int(len(final_events))
    report["final_actual_events"] = int(
        ((flags[final].astype("int64") & 2) == 2).sum()
    )
    report["final_theoretical_events"] = (
        report["final_settlement_events"] - report["final_actual_events"]
    )

    target = definitions
    if "asset" in target:
        target = target.loc[target["asset"].astype(str).eq("AAO")]
    if "instrument_class" in target:
        target = target.loc[target["instrument_class"].astype(str).isin(("C", "P"))]
    unique_keys = target[keys].dropna().drop_duplicates()
    report["unique_outright_id_pairs_observed"] = int(len(unique_keys))
    matched = final_events[keys].merge(
        unique_keys.assign(_present=1), how="left", on=keys, sort=False
    )["_present"].notna()
    report["final_events_matching_outright_id_in_same_month"] = int(matched.sum())
    report["final_events_missing_outright_id_in_same_month"] = int((~matched).sum())
    if "raw_symbol" in target:
        names_per_id = target.groupby(keys, dropna=True)["raw_symbol"].nunique()
        report["id_pairs_with_multiple_raw_symbols"] = int(
            names_per_id.gt(1).sum()
        )
    if "ts_ref" in final_events:
        dates = pd.to_datetime(
            final_events["ts_ref"], utc=True, errors="coerce",
            unit="ns" if pd.api.types.is_numeric_dtype(final_events["ts_ref"])
            else None,
        )
        report["distinct_final_reference_dates"] = int(dates.dt.date.nunique())
        report["missing_final_reference_dates"] = int(dates.isna().sum())
        valid = final_events[keys].copy()
        valid["_day"] = dates.dt.date
        report["tentative_unique_final_id_day_keys"] = int(
            len(valid.dropna().drop_duplicates())
        )
        report["note"] = (
            "Tentative keys use local instrument IDs and are NOT stable "
            "cross-month contract identities; no revision-aware deduplication."
        )
    return report


def run(month: str, raw_dir: Path, output_dir: Path) -> dict[str, Any]:
    import databento as db

    matching = sorted(raw_dir.glob(f"aao_definition__{month}-*.dbn.zst"))
    if len(matching) != 1:
        raise FileNotFoundError(
            f"Expected one definition month file for {month}; found {len(matching)}"
        )
    definition_path = matching[0]
    stats_path = raw_dir / definition_path.name.replace(
        "aao_definition__", "aao_statistics__", 1
    )
    if not stats_path.is_file():
        raise FileNotFoundError(f"Missing statistics for {month}")
    defs = db.DBNStore.from_file(definition_path).to_df()
    stats = db.DBNStore.from_file(stats_path).to_df()
    result = analyze(defs, stats)
    result["month"] = month
    result["data_contacted_provider"] = False
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / f"identity_probe_{month}.json").write_text(
        json.dumps(result, indent=2) + "\n", encoding="utf-8"
    )
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--month", default="2021-02",
                        help="One month YYYY-MM; no paid access")
    parser.add_argument("--data-dir", type=Path, default=RAW)
    parser.add_argument("--output-dir", type=Path, default=REPORT)
    args = parser.parse_args()
    result = run(args.month, args.data_dir, args.output_dir)
    print(json.dumps(result, indent=2))
    if result.get("blocking_error"):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
