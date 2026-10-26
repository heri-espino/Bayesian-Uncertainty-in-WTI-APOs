"""Fail-closed publication-time-aware AAO settlement diagnostic.

One month at a time; only derived aggregate counts are written locally.
NOT a stable cross-month instrument master or a pricing panel. No network calls.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "databento" / "wti_aao_bulk" / "raw"
OUT = (ROOT / "results" / "analysis" / "wti_aao_history_feasibility"
       / "settlement_gate")
KEY = ["publisher_id", "instrument_id", "_event_day"]


def timestamps(series: pd.Series) -> pd.Series:
    """Parse event instants as UTC; ts_ref is a CME reference date."""
    if pd.api.types.is_numeric_dtype(series):
        return pd.to_datetime(series, utc=True, unit="ns", errors="coerce")
    return pd.to_datetime(series, utc=True, errors="coerce")


def evaluate(definitions: pd.DataFrame, statistics: pd.DataFrame) -> dict[str, Any]:
    """Audit conservative same-day, as-of definition joins and final updates."""
    required_def = {
        "ts_event", "publisher_id", "instrument_id", "asset",
        "instrument_class", "raw_symbol", "expiration",
        "strike_price", "leg_count", "security_update_action",
    }
    required_stat = {
        "ts_event", "ts_ref", "publisher_id", "instrument_id",
        "stat_type", "stat_flags", "update_action", "sequence",
    }
    missing_def = required_def - set(definitions)
    missing_stat = required_stat - set(statistics)
    if missing_def or missing_stat:
        raise ValueError(
            f"Missing schema fields: definition={sorted(missing_def)}, "
            f"statistics={sorted(missing_stat)}"
        )
    d = definitions[sorted(required_def)].copy()
    types = pd.to_numeric(statistics["stat_type"], errors="coerce")
    s = statistics.loc[types.eq(3), sorted(required_stat)].copy()
    if s.empty:
        raise ValueError("No settlement statistics present")
    d["_def_time"] = timestamps(d["ts_event"])
    s["_stat_time"] = timestamps(s["ts_event"])
    s["_ref_date"] = timestamps(s["ts_ref"]).dt.strftime("%Y-%m-%d")
    if (d["_def_time"].isna().any() or s["_stat_time"].isna().any()
            or s["_ref_date"].isna().any()):
        raise ValueError("Undefined definition, publication or reference time")
    d["_event_day"] = d["_def_time"].dt.strftime("%Y-%m-%d")
    s["_event_day"] = s["_stat_time"].dt.strftime("%Y-%m-%d")
    for column in ("publisher_id", "instrument_id"):
        d[column] = pd.to_numeric(d[column], errors="raise").astype("int64")
        s[column] = pd.to_numeric(s[column], errors="raise").astype("int64")
    s["_flags"] = pd.to_numeric(s["stat_flags"], errors="raise").astype("int64")
    s["_action"] = pd.to_numeric(s["update_action"], errors="raise").astype("int64")
    s["_sequence"] = pd.to_numeric(s["sequence"], errors="raise").astype("int64")
    if not s["_action"].isin([1, 2]).all():
        raise ValueError("Unknown statistics update action")
    # Do NOT filter classes or deleted definitions before as-of matching.
    # Definition IDs are only guaranteed unique within a calendar day.
    d = d.sort_values("_def_time", kind="stable").drop_duplicates(
        KEY + ["_def_time"], keep="last",
    )
    s = s.sort_values("_stat_time", kind="stable")
    merged = pd.merge_asof(
        s, d, left_on="_stat_time", right_on="_def_time", by=KEY,
        direction="backward", allow_exact_matches=True,
    )
    found = merged["_def_time"].notna()
    outright = (
        found
        & merged["asset"].astype("string").eq("AAO").fillna(False)
        & merged["instrument_class"].astype("string").isin(("C", "P"))
        & pd.to_numeric(merged["leg_count"], errors="coerce").eq(0)
        & merged["raw_symbol"].astype("string").str.strip().ne("").fillna(False)
    )
    actions = (
        merged.loc[outright, "security_update_action"]
        .astype("string").str.strip()
    )
    accepted = {
        "A", "M", "a", "m", "ADD", "MODIFY", "Add", "Modify",
        "D", "d", "DELETE", "Delete",
    }
    if (~actions.isin(accepted)).any():
        raise ValueError(
            "Unknown definition security_update_action; inspect local schema first"
        )
    deleted = actions.isin(("D", "d", "DELETE", "Delete"))
    if deleted.any():
        outright.loc[actions.index[deleted]] = False
    valid = merged.loc[outright].copy()
    # Not unique stable *contract*-date keys; these use temporary venue IDs.
    group = KEY + ["_ref_date"]
    valid = valid.sort_values(["_stat_time", "_sequence"], kind="stable")
    ambiguous = valid.duplicated(
        group + ["_stat_time", "_sequence"], keep=False,
    )
    ambiguous_keys = valid.loc[ambiguous, group].drop_duplicates()
    if len(ambiguous_keys):
        invalid = ambiguous_keys.assign(_conflict=True)
        valid = valid.merge(invalid, on=group, how="left")
        valid = valid.loc[valid["_conflict"].isna()].drop(
            columns="_conflict",
        )
    last = valid.drop_duplicates(group, keep="last")
    final = last["_flags"].astype("int64").mod(2).eq(1)
    active = last["_action"].eq(1)
    selected = last.loc[final & active]
    actual = (selected["_flags"].astype("int64") & 2).eq(2)
    late = selected["_stat_time"].dt.strftime("%Y-%m-%d").ne(
        selected["_ref_date"]
    )
    return {
        "data_contacted_provider": False,
        "settlement_events": int(len(s)),
        "without_same_event_day_asof_definition": int((~found).sum()),
        "matched_asof_definition_events": int(found.sum()),
        "outright_matched_events": int(outright.sum()),
        "excluded_non_outright_or_inactive_events": int((found & ~outright).sum()),
        "tentative_publisher_id_day_reference_keys": int(len(last)),
        "ambiguous_tied_keys_excluded": int(len(ambiguous_keys)),
        "selected_final_active_keys": int(len(selected)),
        "selected_actual_flagged": int(actual.sum()),
        "selected_theoretical_flagged": int((~actual).sum()),
        "selected_published_on_different_utc_date": int(late.sum()),
        "distinct_selected_reference_dates": int(selected["_ref_date"].nunique()),
        "warning": (
            "Strict same-event-day as-of diagnostic only. Publication UTC day "
            "may differ from CME ts_ref; not stable contract identity, not "
            "price-level panel, and not forward-eligible dates."
        ),
    }


def run(month: str, raw: Path, out: Path) -> dict[str, Any]:
    """Read one locally stored month; only emit safe aggregated counts."""
    import databento as db

    definitions = sorted(raw.glob(f"aao_definition__{month}-*.dbn.zst"))
    if len(definitions) != 1:
        raise FileNotFoundError(
            f"Expected exactly one definition file for {month}"
        )
    stats_path = raw / definitions[0].name.replace(
        "aao_definition__", "aao_statistics__", 1
    )
    if not stats_path.is_file():
        raise FileNotFoundError(f"Missing statistics for {month}")
    d = db.DBNStore.from_file(definitions[0]).to_df()
    s = db.DBNStore.from_file(stats_path).to_df()
    report = evaluate(d, s)
    report["month"] = month
    out.mkdir(parents=True, exist_ok=True)
    (out / f"gate_{month}.json").write_text(
        json.dumps(report, indent=2) + "\n", encoding="utf-8"
    )
    return report


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--months", nargs="+", default=["2021-02", "2026-06"],
    )
    parser.add_argument("--data-dir", type=Path, default=RAW)
    parser.add_argument("--output-dir", type=Path, default=OUT)
    args = parser.parse_args()
    for month in args.months:
        print(json.dumps(run(month, args.data_dir, args.output_dir), indent=2))


if __name__ == "__main__":
    main()
