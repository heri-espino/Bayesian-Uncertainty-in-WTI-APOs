"""Offline AAO daily-definition mapping comparison (diagnostics, not pricing).

Compare candidate daily snapshots for CME settlement statistics using:
reference trading date, publication UTC date, and preceding UTC date.
Exclude ambiguous/deleted/multileg definitions and report identity conflicts.
Outputs aggregate counts only; no network use, prices or individual symbols.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "databento" / "wti_aao_bulk" / "raw"
REPORT = ROOT / "results" / "analysis" / "wti_aao_history_feasibility" / "mapping_comparison"
JOIN = ["publisher_id", "instrument_id"]
IDENTITY = ("raw_symbol", "instrument_class", "expiration", "strike_price",
            "exchange", "underlying")


def _timestamps(series: pd.Series) -> pd.Series:
    if pd.api.types.is_numeric_dtype(series):
        return pd.to_datetime(series, unit="ns", utc=True, errors="coerce")
    return pd.to_datetime(series, utc=True, errors="coerce")


def compare(definitions: pd.DataFrame, statistics: pd.DataFrame) -> dict:
    """Compare daily definitions under three candidate event-date conventions."""
    required_def = set(JOIN) | set(IDENTITY) | {
        "ts_event", "asset", "leg_count", "security_update_action"
    }
    required_stat = set(JOIN) | {
        "ts_event", "ts_ref", "stat_type", "stat_flags"
    }
    missing_def = sorted(required_def - set(definitions))
    missing_stat = sorted(required_stat - set(statistics))
    if missing_def or missing_stat:
        raise ValueError(
            f"Missing definition={missing_def}, statistics={missing_stat}"
        )
    d = definitions[list(required_def)].copy()
    s = statistics[list(required_stat)].copy()
    types = pd.to_numeric(s["stat_type"], errors="raise")
    flags = pd.to_numeric(s["stat_flags"], errors="coerce")
    mask = types.eq(3) & flags.notna() & flags.fillna(0).astype("int64").mod(2).eq(1)
    s = s.loc[mask].copy()
    if s.empty:
        raise ValueError("No final settlement events found")
    s["_event_ts"] = _timestamps(s["ts_event"])
    s["_ref_ts"] = _timestamps(s["ts_ref"])
    d["_def_ts"] = _timestamps(d["ts_event"])
    if (s["_event_ts"].isna().any() or s["_ref_ts"].isna().any()
            or d["_def_ts"].isna().any()):
        raise ValueError("Unparseable event/reference/definition timestamp")
    for column in JOIN:
        s[column] = pd.to_numeric(s[column], errors="raise").astype("int64")
        d[column] = pd.to_numeric(d[column], errors="raise").astype("int64")
    d["_def_day"] = d["_def_ts"].dt.strftime("%Y-%m-%d")
    s["_pub_day"] = s["_event_ts"].dt.strftime("%Y-%m-%d")
    s["_ref_day"] = s["_ref_ts"].dt.strftime("%Y-%m-%d")
    s["_prev_pub_day"] = (
        s["_event_ts"] - pd.Timedelta(days=1)
    ).dt.strftime("%Y-%m-%d")

    # Same-day consensus is a conservative hypothesis: if an ID is used
    # for two different contract fingerprints on one day, reject that day.
    for column in IDENTITY:
        d[column] = (
            d[column].astype("string").fillna("<missing>").str.strip()
        )
    d["_identity"] = d[list(IDENTITY)].agg("|".join, axis=1)
    d["_is_outright"] = (
        d["asset"].astype("string").eq("AAO")
        & d["instrument_class"].isin(("C", "P"))
        & pd.to_numeric(d["leg_count"], errors="coerce").eq(0)
        & d["raw_symbol"].ne("<missing>")
        & d["raw_symbol"].ne("")
    )
    d["_action"] = (
        d["security_update_action"].astype("string").str.upper()
    )
    if not d["_action"].isin(
        ("A", "M", "D", "ADD", "MODIFY", "DELETE")
    ).all():
        raise ValueError("Unknown security definition update action")
    d = d.sort_values("_def_ts", kind="stable")
    gkeys = JOIN + ["_def_day"]
    grouped = d.groupby(gkeys, as_index=False, sort=False).agg(
        _first_def=("_def_ts", "min"),
        _distinct_identities=("_identity", "nunique"),
        _identity_value=("_identity", "last"),
        _all_outright=("_is_outright", "all"),
        _last_action=("_action", "last"),
    )
    grouped["_safe"] = (
        grouped["_distinct_identities"].eq(1)
        & grouped["_all_outright"]
        & ~grouped["_last_action"].isin(("D", "DELETE"))
    )
    answer = {
        "final_events": int(len(s)),
        "definition_id_days": int(len(grouped)),
        "ambiguous_definition_id_days": int(
            grouped["_distinct_identities"].gt(1).sum()
        ),
        "publication_reference_date_disagreement": int(
            s["_pub_day"].ne(s["_ref_day"]).sum()
        ),
        "source": "local DBN, no historical API request",
        "counts_are": "candidate daily links, NOT valid prices or backtest dates",
    }
    matches_by_method = []
    identity_by_method = {}
    for label, day_column in (
        ("reference_date", "_ref_day"),
        ("publication_utc_day", "_pub_day"),
        ("preceding_publication_day", "_prev_pub_day"),
    ):
        candidates = s[JOIN + [day_column, "_event_ts"]].rename(
            columns={day_column: "_def_day"}
        )
        matches = candidates.merge(
            grouped, how="left", on=gkeys, validate="many_to_one",
            sort=False,
        )
        exists = matches["_first_def"].notna()
        prior = exists & matches["_first_def"].le(matches["_event_ts"])
        accepted = prior & matches["_safe"].fillna(False)
        answer[label] = {
            "found_day_definition": int(exists.sum()),
            "definition_available_before_publication": int(prior.sum()),
            "unambiguous_active_outright_match": int(accepted.sum()),
            "missing_day_definition": int((~exists).sum()),
            "ambiguous_or_inactive_day_definition": int(
                (prior & ~matches["_safe"].fillna(False)).sum()
            ),
        }
        matches_by_method.append(accepted.reset_index(drop=True))
        identity_by_method[label] = (
            matches["_identity_value"].where(accepted).reset_index(drop=True)
        )
    any_candidate = (
        matches_by_method[0] | matches_by_method[1]
        | matches_by_method[2]
    )
    identity_frame = pd.DataFrame(identity_by_method)
    conflicts = identity_frame.nunique(axis=1, dropna=True).gt(1)
    answer["events_with_at_least_one_candidate_mapping"] = int(
        any_candidate.sum()
    )
    answer["events_with_conflicting_candidate_contracts"] = int(
        conflicts.sum()
    )
    answer["events_with_at_least_one_consistent_candidate"] = int(
        (any_candidate & ~conflicts).sum()
    )
    answer["events_with_no_candidate_mapping"] = int(
        (~any_candidate).sum()
    )
    answer["warning"] = (
        "Reference-day, publication-day and preceding-day snapshots are "
        "ALTERNATIVE hypotheses. Neither their union nor their agreeing "
        "subset is a validated as-of price panel: daily ID reuse, settlement "
        "amendments, venue session boundaries and cross-month contract "
        "identity remain unresolved."
    )
    return answer


def run(month: str, raw_dir: Path, report_dir: Path) -> dict:
    import databento as db

    files = sorted(raw_dir.glob(f"aao_definition__{month}-*.dbn.zst"))
    if len(files) != 1:
        raise FileNotFoundError(
            f"Expected one definition file for {month}, got {len(files)}"
        )
    stats_path = raw_dir / files[0].name.replace(
        "aao_definition__", "aao_statistics__", 1
    )
    if not stats_path.is_file():
        raise FileNotFoundError(
            f"Missing corresponding statistics file for {month}"
        )
    report = compare(
        db.DBNStore.from_file(files[0]).to_df(),
        db.DBNStore.from_file(stats_path).to_df(),
    )
    report["month"] = month
    report_dir.mkdir(parents=True, exist_ok=True)
    (report_dir / f"mapping_comparison_{month}.json").write_text(
        json.dumps(report, indent=2) + "\n", encoding="utf-8"
    )
    return report


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--months", nargs="+", default=["2021-02", "2026-06"]
    )
    parser.add_argument("--data-dir", type=Path, default=RAW)
    parser.add_argument("--report-dir", type=Path, default=REPORT)
    args = parser.parse_args()
    for month in args.months:
        print(json.dumps(run(month, args.data_dir, args.report_dir), indent=2))


if __name__ == "__main__":
    main()
