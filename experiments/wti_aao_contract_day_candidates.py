"""Offline AAO contract/reference-date settlement candidates.

This is a *within-file-month* candidate stage, not a validated settlement
price panel. It resolves DBN-native mapped symbols against unambiguous AAO
call/put definitions, then applies latest add/delete, final and intraday flags.

No Databento API calls. Price-level output is opt-in, PRIVATE and gitignored.
A later stage must reconcile late corrections across monthly file boundaries,
historical symbol reuse, cross-vendor prices and ex-ante information cutoffs.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "databento" / "wti_aao_bulk" / "raw"
REPORT = (ROOT / "results" / "analysis" /
          "wti_aao_history_feasibility" / "contract_day_candidates")
PRIVATE = ROOT / "data" / "databento" / "wti_aao_bulk" / "derived_private"
IDENTITY = ["instrument_class", "expiration", "strike_price",
            "exchange", "underlying", "asset"]
OUTPUT_COLUMNS = ["publisher_id", "symbol", "ref_date", "ts_event",
                  "sequence", "price", "side", "expiration", "strike_price",
                  "exchange", "underlying", "final_actual"]


def _utc(series: pd.Series) -> pd.Series:
    if pd.api.types.is_numeric_dtype(series):
        return pd.to_datetime(series, unit="ns", utc=True, errors="coerce")
    return pd.to_datetime(series, utc=True, errors="coerce")


def _clean(series: pd.Series) -> pd.Series:
    return series.astype("string").str.strip()


def normalize(definitions: pd.DataFrame,
              statistics: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    """Select conservative per-month final non-intraday candidate updates.

    This does not join same-symbol corrections across file months; no output
    should be called a validated contract/day price before that stage.
    """
    req_d = {"publisher_id", "raw_symbol", "leg_count",
             "security_update_action", *IDENTITY}
    req_s = {"publisher_id", "symbol", "ts_ref", "ts_event", "stat_type",
             "stat_flags", "update_action", "sequence", "price"}
    missing_d, missing_s = req_d-set(definitions), req_s-set(statistics)
    if missing_d or missing_s:
        raise ValueError(
            f"Missing required fields: definitions={sorted(missing_d)}, "
            f"statistics={sorted(missing_s)}"
        )
    d = definitions[["publisher_id", "raw_symbol", "leg_count",
                     "security_update_action", *IDENTITY]].copy()
    d["publisher_id"] = pd.to_numeric(
        d["publisher_id"], errors="raise"
    ).astype("int64")
    d["symbol"] = _clean(d["raw_symbol"])
    d = d.loc[d["symbol"].notna() & d["symbol"].ne("")].copy()
    if d.empty:
        raise ValueError("No instrument definitions with native symbols")
    d["side"] = _clean(d["instrument_class"])
    d["outright"] = (
        _clean(d["asset"]).eq("AAO").fillna(False)
        & d["side"].isin(["C", "P"])
        & pd.to_numeric(d["leg_count"], errors="coerce").eq(0)
    )
    for column in IDENTITY:
        d[column] = _clean(d[column]).fillna("<missing>")
    d["fingerprint"] = d[IDENTITY].agg("|".join, axis=1)
    d["security_update_action"] = (
        _clean(d["security_update_action"]).str.upper()
    )
    if not d["security_update_action"].isin(
        {"A", "M", "D", "ADD", "MODIFY", "DELETE"}
    ).all():
        raise ValueError("Unrecognized definition security_update_action")
    groups = d.groupby(
        ["publisher_id", "symbol"], sort=False
    ).agg(
        n_identities=("fingerprint", "nunique"),
        all_outright=("outright", "all"),
    )
    reps = d.drop_duplicates(
        ["publisher_id", "symbol"], keep="first"
    )
    groups = groups.join(
        reps.set_index(["publisher_id", "symbol"])[
            ["side", "expiration", "strike_price", "exchange", "underlying"]
        ]
    )
    groups["usable"] = (
        groups["n_identities"].eq(1) & groups["all_outright"]
    )
    groups = groups.reset_index()

    types = pd.to_numeric(statistics["stat_type"], errors="raise")
    s = statistics.loc[types.eq(3), [
        "publisher_id", "symbol", "ts_ref", "ts_event",
        "stat_flags", "update_action", "sequence", "price",
    ]].copy()
    if s.empty:
        raise ValueError("No settlement records in month")
    s["publisher_id"] = pd.to_numeric(
        s["publisher_id"], errors="raise"
    ).astype("int64")
    s["symbol"] = _clean(s["symbol"])
    s["ts_event"] = _utc(s["ts_event"])
    s["ref_date"] = _utc(s["ts_ref"]).dt.strftime("%Y-%m-%d")
    for field in ("stat_flags", "update_action", "sequence"):
        s[field] = pd.to_numeric(s[field], errors="raise").astype("int64")
    s["price"] = pd.to_numeric(s["price"], errors="coerce")
    if (s[["ts_event", "ref_date"]].isna().any().any()
            or not s["update_action"].isin([1, 2]).all()):
        raise ValueError("Invalid dates or unknown statistic update_action")
    event_count = len(s)
    joined = s.merge(
        groups, on=["publisher_id", "symbol"], how="left",
        validate="many_to_one", sort=False,
    )
    usable = joined["usable"].fillna(False).astype(bool)
    joined = joined.loc[usable].copy()

    # Choose the last chronological update of every tentative native-symbol
    # reference-date key, including preliminary and delete messages. A later
    # deletion or preliminary is NOT an eligible final settlement.
    key = ["publisher_id", "symbol", "ref_date"]
    rank = ["ts_event", "sequence"]
    joined = joined.sort_values(key + rank, kind="stable")
    highest = joined.drop_duplicates(key, keep="last")[key + rank]
    candidates = joined.merge(
        highest, on=key + rank, how="inner",
        validate="many_to_one", sort=False,
    )
    decision = ["update_action", "stat_flags", "price"]
    conflicts = (
        candidates.groupby(key, dropna=False)[decision]
        .nunique(dropna=False).max(axis=1).gt(1)
    )
    invalid = (
        conflicts[conflicts].reset_index()[key].assign(_conflict=True)
    )
    latest = candidates.drop_duplicates(key, keep="last")
    if len(invalid):
        latest = latest.merge(
            invalid, on=key, how="left", validate="one_to_one"
        )
        latest = latest.loc[
            latest["_conflict"].isna()
        ].drop(columns="_conflict")
    added = latest["update_action"].eq(1)
    final = latest["stat_flags"].mod(2).eq(1)
    not_intraday = (latest["stat_flags"] & 8).eq(0)
    price_valid = (
        np.isfinite(latest["price"]) & latest["price"].ge(0)
    )
    selected = latest.loc[
        added & final & not_intraday & price_valid
    ].copy()
    selected["final_actual"] = (
        selected["stat_flags"] & 2
    ).eq(2)
    output = selected[OUTPUT_COLUMNS].sort_values(
        ["ref_date", "publisher_id", "symbol"], kind="stable"
    )
    report = {
        "no_api_requests": True,
        "status": "within_month_candidates_not_validated_prices",
        "settlement_events": int(event_count),
        "definition_publisher_symbol_groups": int(len(groups)),
        "ambiguous_or_non_outright_definition_groups": int(
            (~groups["usable"]).sum()
        ),
        "definition_groups_containing_delete_events": int(
            d.loc[d["security_update_action"].isin(["D", "DELETE"]),
                  ["publisher_id", "symbol"]].drop_duplicates().shape[0]
        ),
        "events_with_unambiguous_outright_mapping": int(len(joined)),
        "events_without_safe_outright_mapping": int(event_count-len(joined)),
        "distinct_publisher_symbol_reference_keys": int(len(highest)),
        "conflicting_latest_rank_keys_rejected": int(conflicts.sum()),
        "latest_deleted_keys": int((~added).sum()),
        "latest_not_final_keys": int((added & ~final).sum()),
        "latest_intraday_final_keys": int(
            (added & final & ~not_intraday).sum()
        ),
        "latest_invalid_price_keys": int(
            (added & final & not_intraday & ~price_valid).sum()
        ),
        "selected_final_nonintraday_keys": int(len(output)),
        "selected_actual_flagged": int(output["final_actual"].sum()),
        "selected_theoretical_flagged": int((~output["final_actual"]).sum()),
        "distinct_candidate_reference_dates": int(
            output["ref_date"].nunique()
        ),
        "candidate_updates_reduced": int(len(joined)-len(highest)),
        "requires_cross_month_amendment_reconciliation": True,
    }
    return output, report


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024*1024), b""):
            digest.update(block)
    return digest.hexdigest()


def run_month(month: str, raw_dir: Path, report_dir: Path,
              private_dir: Path | None = None) -> dict:
    """Read one local month and write aggregate diagnostics, optionally private rows."""
    import databento as db

    definitions = sorted(
        raw_dir.glob(f"aao_definition__{month}-*.dbn.zst")
    )
    if len(definitions) != 1:
        raise FileNotFoundError(
            f"Expected one local definition DBN for {month}; found {len(definitions)}"
        )
    stats_path = raw_dir / definitions[0].name.replace(
        "aao_definition__", "aao_statistics__", 1
    )
    if not stats_path.is_file():
        raise FileNotFoundError(f"Missing local statistics DBN for {month}")
    d = db.DBNStore.from_file(definitions[0]).to_df(map_symbols=True)
    s = db.DBNStore.from_file(stats_path).to_df(map_symbols=True)
    candidates, report = normalize(d, s)
    report["month"] = month
    report["source_hashes"] = {
        "definition_sha256": file_sha256(definitions[0]),
        "statistics_sha256": file_sha256(stats_path),
    }
    if private_dir is not None:
        private_dir.mkdir(parents=True, exist_ok=True)
        target = private_dir / f"AAO_CANDIDATES_NOT_VALIDATED_{month}.csv.gz"
        candidates.to_csv(target, index=False, compression="gzip")
        report["private_panel_created"] = True
    else:
        report["private_panel_created"] = False
    report_dir.mkdir(parents=True, exist_ok=True)
    path = report_dir / f"contract_day_candidates_{month}.json"
    path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    return report


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--months", nargs="+", default=["2021-02", "2026-06"])
    parser.add_argument("--all", action="store_true",
                        help="Process all 81 local months, one at a time")
    parser.add_argument("--data-dir", type=Path, default=RAW)
    parser.add_argument("--report-dir", type=Path, default=REPORT)
    parser.add_argument(
        "--export-private", action="store_true",
        help="Write licensed row-level candidate prices locally; gitignored",
    )
    args = parser.parse_args()
    months = (
        [str(period) for period in pd.period_range(
            "2020-01", "2026-09", freq="M"
        )]
        if args.all else args.months
    )
    for month in months:
        print(json.dumps(
            run_month(
                month, args.data_dir, args.report_dir,
                PRIVATE if args.export_private else None,
            ), indent=2,
        ))


if __name__ == "__main__":
    main()
