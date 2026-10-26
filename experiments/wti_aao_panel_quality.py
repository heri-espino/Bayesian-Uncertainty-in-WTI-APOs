"""Offline AAO panel diagnostic; only aggregate numbers, no vendor price rows.

Scans the previously generated private SQLite; optionally scans 81 local DBN
statistics files in chunks to identify missing final reference day(s).
No Databento API calls and no writes to the existing source data.
"""
from __future__ import annotations

import argparse
from collections import Counter
import json
from pathlib import Path
import sqlite3

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "results" / "analysis" / "wti_aao_history_feasibility"
DB = ROOT / "data" / "databento" / "wti_aao_bulk" / "derived_private" / "aao_cross_month_PROVISIONAL_81_months.sqlite3"
INV = BASE / "inventory" / "aao_inventory_summary.json"
RAW = ROOT / "data" / "databento" / "wti_aao_bulk" / "raw"
OUT = BASE / "quality" / "cross_month_quality.json"
SELECTED = (
    "action=1 AND (flags & 1)!=0 AND (flags & 8)=0 "
    "AND price IS NOT NULL AND price>=0 AND tie_conflict=0"
)


def audit_state(conn: sqlite3.Connection) -> tuple[dict, set[str]]:
    """Aggregate annual counts and price bins without disclosing price rows."""
    rows = conn.execute(f"""
      SELECT substr(ref_date,1,4), count(*), count(DISTINCT ref_date),
        sum((flags & 2)!=0), sum(price=0),
        sum(price>0 AND price<.01), sum(price>=.01 AND price<1),
        sum(price>=1 AND price<10), sum(price>=10 AND price<100),
        sum(price>=100), sum(source_month!=substr(ref_date,1,7))
      FROM states WHERE {SELECTED}
      GROUP BY substr(ref_date,1,4) ORDER BY 1
    """).fetchall()
    years = {}
    for (year, n, days, actual, zero, tiny, under1, under10, under100,
         high, late) in rows:
        years[str(year)] = {
            "candidate_keys": int(n),
            "reference_dates": int(days),
            "actual_flagged": int(actual or 0),
            "theoretical_flagged": int(n - (actual or 0)),
            "zero_price_keys": int(zero or 0),
            "price_bins": {
                "positive_below_0_01": int(tiny or 0),
                "0_01_to_1": int(under1 or 0),
                "1_to_10": int(under10 or 0),
                "10_to_100": int(under100 or 0),
                "100_and_above": int(high or 0),
            },
            "latest_report_source_month_differs": int(late or 0),
        }
    days = {
        str(row[0]) for row in conn.execute(
            f"SELECT DISTINCT ref_date FROM states WHERE {SELECTED}"
        )
    }
    return {
        "by_year": years,
        "total_candidate_keys": sum(x["candidate_keys"] for x in years.values()),
        "distinct_candidate_dates": len(days),
        "price_units_verified": False,
        "price_bins_are_diagnostic_only": True,
    }, days


def compare_raw_days(source: dict[str, int], selected: set[str],
                     expected: int) -> dict:
    if len(source) != expected:
        raise ValueError(f"Expected {expected} inventory final days; found {len(source)}")
    missing = sorted(set(source) - selected)
    return {
        "source_final_dates": len(source),
        "candidate_final_dates": len(selected),
        "source_dates_missing_from_candidates": missing,
        "final_source_events_on_missing_dates": {
            day: int(source[day]) for day in missing
        },
        "unexpected_candidate_days": sorted(selected - set(source)),
    }


def source_final_dates(raw: Path) -> dict[str, int]:
    """Optional heavy, bounded-memory DBN-only scan; never transmit data."""
    import databento as db

    files = sorted(raw.glob("aao_statistics__*.dbn.zst"))
    if len(files) != 81:
        raise ValueError(f"Expected 81 statistics DBNs; found {len(files)}")
    days: Counter[str] = Counter()
    for path in files:
        for frame in db.DBNStore.from_file(path).to_df(
            count=200000, map_symbols=False
        ):
            kinds = pd.to_numeric(frame["stat_type"], errors="raise")
            flags = pd.to_numeric(frame["stat_flags"], errors="coerce")
            final = kinds.eq(3) & flags.notna() & (
                flags.fillna(0).astype("int64") & 1
            ).eq(1)
            refs = frame.loc[final, "ts_ref"]
            if pd.api.types.is_numeric_dtype(refs):
                ts = pd.to_datetime(refs, unit="ns", utc=True, errors="coerce")
            else:
                ts = pd.to_datetime(refs, utc=True, errors="coerce")
            if ts.isna().any():
                raise ValueError(f"Unparseable settlement reference date: {path.name}")
            days.update(ts.dt.strftime("%Y-%m-%d").value_counts().to_dict())
    return dict(days)



def reference_date_status(
    conn: sqlite3.Connection, date: str
) -> dict:
    """Explain a raw final-event date by latest private SQLite statuses."""
    try:
        target = pd.Timestamp(date)
        if target.strftime("%Y-%m-%d") != date:
            raise ValueError
    except (TypeError, ValueError):
        raise ValueError("Date must be YYYY-MM-DD") from None
    row = conn.execute("""
      SELECT COUNT(*),
        COALESCE(SUM(action!=1),0),
        COALESCE(SUM(action=1 AND (flags & 1)=0),0),
        COALESCE(SUM(action=1 AND (flags & 1)!=0 AND (flags & 8)!=0),0),
        COALESCE(SUM(action=1 AND (flags & 1)!=0 AND (flags & 8)=0
          AND (price IS NULL OR price<0)),0),
        COALESCE(SUM(action=1 AND (flags & 1)!=0 AND (flags & 8)=0
          AND price>=0 AND tie_conflict!=0),0),
        COALESCE(SUM(action=1 AND (flags & 1)!=0 AND (flags & 8)=0
          AND price>=0 AND tie_conflict=0),0)
      FROM states WHERE ref_date=?
    """, (date,)).fetchone()
    labels = (
        "last_update_keys", "last_deleted", "last_preliminary",
        "last_intraday_final", "last_invalid_price", "last_tied_conflict",
        "last_selected_final",
    )
    return {
        "reference_date": date,
        **{key: int(value or 0) for key, value in zip(labels, row)},
        "raw_final_events_on_day": "Use --scan-final-dates for source-event count",
        "warning": (
            "Current latest state only; the two original final events may "
            "have been superseded or excluded. No symbols/prices disclosed."
        ),
    }


def barchart_overlap(selected: set[str], root: Path | None = None) -> dict:
    """Only counts dates shared with Barchart, not matched option contracts."""
    from bayesian_asian_options.barchart_apo import (
        build_apo_panel, discover_barchart_histories,
    )
    folder = root if root is not None else ROOT / "data" / "csv"
    files = discover_barchart_histories(folder)
    if not files:
        return {
            "available": False,
            "root_exists": folder.is_dir(),
            "csv_files_found": sum(1 for _ in folder.rglob("*.csv"))
                if folder.is_dir() else 0,
            "filename_matching_apo_history_count": 0,
            "reason": (
                "No local CSV names matched the existing Barchart APO "
                "filename parser; check checkout/sparse checkout, location "
                "or use --barchart-root. This is NOT zero market overlap."
            ),
        }
    panel = build_apo_panel(files)
    dates = pd.to_datetime(panel["trade_date"]).dt.strftime("%Y-%m-%d")
    return {
        "available": True,
        "barchart_contract_files": len(files),
        "barchart_rows": int(len(panel)),
        "barchart_dates": int(dates.nunique()),
        "overlapping_reference_dates": len(set(dates) & selected),
        "barchart_rows_on_common_dates": int(dates.isin(selected).sum()),
        "price_and_contract_identity_matching_done": False,
    }


def audit(db_path: Path, inventory: Path, *, raw: Path | None = None,
          include_barchart: bool = True,
          barchart_root: Path | None = None,
          explain_date: str | None = None) -> dict:
    if not db_path.is_file():
        raise FileNotFoundError(f"Private cross-month state not found: {db_path}")
    source = json.loads(inventory.read_text(encoding="utf-8"))
    summary = source.get("summary", {})
    if summary.get("months_processed") != 81 or source.get("errors"):
        raise ValueError("Needs 81-month, error-free inventory")
    conn = sqlite3.connect(db_path.resolve().as_uri() + "?mode=ro", uri=True)
    try:
        result, selected = audit_state(conn)
        if explain_date is not None:
            result["reference_date_status"] = reference_date_status(
                conn, explain_date
            )
    finally:
        conn.close()
    result.update({
        "no_vendor_api_calls": True,
        "status": "quality_diagnostic_not_model_validation",
        "inventory_final_reference_dates": int(
            summary["distinct_final_reference_dates"]
        ),
    })
    if raw is not None:
        result["raw_reference_dates"] = compare_raw_days(
            source_final_dates(raw), selected,
            int(summary["distinct_final_reference_dates"]),
        )
    if include_barchart:
        result["barchart_date_only_overlap"] = barchart_overlap(
            selected, barchart_root
        )
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--sqlite", type=Path, default=DB)
    parser.add_argument("--inventory", type=Path, default=INV)
    parser.add_argument("--scan-final-dates", action="store_true",
                        help="Heavy offline scan of all 81 original statistics DBNs")
    parser.add_argument("--skip-barchart", action="store_true")
    parser.add_argument("--barchart-root", type=Path,
                        help="Alternative local Barchart APO CSV root")
    parser.add_argument("--explain-date",
                        help="Aggregate latest update state for YYYY-MM-DD")
    parser.add_argument("--output", type=Path, default=OUT)
    args = parser.parse_args()
    result = audit(args.sqlite, args.inventory,
                   raw=RAW if args.scan_final_dates else None,
                   include_barchart=not args.skip_barchart,
                   barchart_root=args.barchart_root,
                   explain_date=args.explain_date)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
