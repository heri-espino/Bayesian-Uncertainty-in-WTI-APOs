"""Provisional cross-month AAO settlement state from native DBN symbols.

Uses a complete-scan identity registry and on-disk SQLite latest-update
state, so memory is bounded by one source-file month's statistics.
This is *not* a validated valuation panel or a trade-price history.
"""
from __future__ import annotations

import sqlite3
from pathlib import Path

import numpy as np
import pandas as pd

FINGERPRINT = ("asset", "instrument_class", "expiration", "strike_price",
               "exchange", "underlying")
DEF_FIELDS = {"publisher_id", "raw_symbol", "leg_count",
              "security_update_action", *FINGERPRINT}
STAT_FIELDS = {"publisher_id", "symbol", "ts_event", "ts_ref", "stat_type",
               "stat_flags", "update_action", "sequence", "price"}
KEY = ("publisher_id", "symbol", "ref_date")
STAT_ORDER = ("ts_ns", "sequence")


def _time(series: pd.Series) -> pd.Series:
    if pd.api.types.is_numeric_dtype(series):
        return pd.to_datetime(series, unit="ns", utc=True, errors="coerce")
    return pd.to_datetime(series, utc=True, errors="coerce")


def fingerprint_rows(definitions: pd.DataFrame) -> dict[tuple[int, str], tuple]:
    """One local symbol identity, or an explicitly unusable/ambiguous state."""
    missing = DEF_FIELDS - set(definitions.columns)
    if missing:
        raise ValueError(f"Definition columns missing: {sorted(missing)}")
    d = definitions[list(DEF_FIELDS)].copy()
    d["publisher_id"] = pd.to_numeric(
        d["publisher_id"], errors="raise"
    ).astype("int64")
    d["raw_symbol"] = d["raw_symbol"].astype("string").str.strip()
    d = d.loc[d["raw_symbol"].notna() & d["raw_symbol"].ne("")].copy()
    actions = d["security_update_action"].astype("string").str.upper()
    if (~actions.isin(["A", "M", "D", "ADD", "MODIFY", "DELETE"])).any():
        raise ValueError("Unknown definition update action")
    d["outright"] = (
        d["asset"].astype("string").eq("AAO").fillna(False)
        & d["instrument_class"].astype("string").isin(("C", "P"))
        & pd.to_numeric(d["leg_count"], errors="coerce").eq(0)
    )
    for col in FINGERPRINT:
        d[col] = d[col].astype("string").str.strip().fillna("<missing>")
    # Fingerprints include key economic terms, never temporary instrument IDs.
    d["fingerprint"] = d[list(FINGERPRINT)].agg("|".join, axis=1)
    result = {}
    for key, frame in d.groupby(["publisher_id", "raw_symbol"], sort=False):
        values = frame["fingerprint"].unique()
        safe = (
            len(values) == 1 and bool(frame["outright"].all())
            and all("<missing>" not in str(v) for v in values)
        )
        result[(int(key[0]), str(key[1]))] = (str(values[0]), safe, len(values) != 1)
    return result


def merge_registry(registry: dict, definitions: pd.DataFrame) -> dict:
    """Accumulate full-history symbol conflicts *before* examining prices."""
    for key, (fp, usable, clash) in fingerprint_rows(definitions).items():
        previous = registry.get(key)
        if previous is None:
            registry[key] = (fp, usable, clash)
        else:
            prev_fp, prev_usable, prev_clash = previous
            conflict = clash or prev_clash or (fp != prev_fp)
            registry[key] = (
                prev_fp, usable and prev_usable and not conflict, conflict
            )
    return registry


def monthly_latest(statistics: pd.DataFrame, registry: dict) -> tuple[pd.DataFrame, dict]:
    """Reduce one month to last *all-action* report for each symbol/reference day."""
    missing = STAT_FIELDS - set(statistics.columns)
    if missing:
        raise ValueError(f"Statistic columns missing: {sorted(missing)}")
    types = pd.to_numeric(statistics["stat_type"], errors="raise")
    s = statistics.loc[types.eq(3), list(STAT_FIELDS)].copy()
    n = len(s)
    if not n:
        raise ValueError("No settlement statistics in source month")
    s["publisher_id"] = pd.to_numeric(
        s["publisher_id"], errors="raise"
    ).astype("int64")
    s["symbol"] = s["symbol"].astype("string").str.strip()
    good_symbol = s["symbol"].notna() & s["symbol"].ne("")
    s = s.loc[good_symbol].copy()
    s["ref_date"] = _time(s["ts_ref"]).dt.strftime("%Y-%m-%d")
    ts = _time(s["ts_event"])
    if s["ref_date"].isna().any() or ts.isna().any():
        raise ValueError("Unparseable settlement publication or reference date")
    s["ts_ns"] = ts.astype("int64")
    for field in ("stat_flags", "update_action", "sequence"):
        s[field] = pd.to_numeric(s[field], errors="raise").astype("int64")
    if not s["update_action"].isin([1, 2]).all():
        raise ValueError("Unknown statistics update_action; abort")
    s["price"] = pd.to_numeric(s["price"], errors="coerce")

    safe_keys = {key for key, value in registry.items() if value[1]}
    is_safe = [
        (int(p), str(symbol)) in safe_keys
        for p, symbol in zip(s["publisher_id"], s["symbol"])
    ]
    mapped = s.loc[is_safe].copy()
    mapped = mapped.rename(columns={
        "update_action": "action", "stat_flags": "flags",
    })
    mapped = mapped.sort_values(
        list(KEY + STAT_ORDER), kind="stable"
    )
    # Detect different message content at the highest identical timestamp+seq.
    ranks = list(KEY + STAT_ORDER)
    tied = mapped.loc[mapped.duplicated(ranks, keep=False)]
    bad = set()
    if not tied.empty:
        count = tied.groupby(ranks, dropna=False)[
            ["action", "flags", "price"]
        ].nunique(dropna=False)
        for idx in count.index[count.gt(1).any(axis=1)]:
            bad.add(idx)
    last = mapped.drop_duplicates(list(KEY), keep="last").copy()
    if not last.empty:
        last["tie_conflict"] = [
            int(tuple(row) in bad)
            for row in last[ranks].itertuples(index=False, name=None)
        ]
    info = {
        "settlement_events": n,
        "events_with_safe_global_symbol": len(mapped),
        "events_unmapped_or_ambiguous": n - len(mapped),
        "month_last_update_keys": len(last),
        "month_top_rank_conflicts": int(last["tie_conflict"].sum())
            if len(last) else 0,
    }
    return last, info


def initialize_db(path: Path) -> sqlite3.Connection:
    """An explicitly private, recreated SQLite checkpoint with economic prices."""
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        path.unlink()  # only this caller-selected private output database
    conn = sqlite3.connect(path)
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA synchronous=NORMAL")
    conn.execute("""
        CREATE TABLE states (
          publisher_id INTEGER NOT NULL, symbol TEXT NOT NULL,
          ref_date TEXT NOT NULL, ts_ns INTEGER NOT NULL,
          sequence INTEGER NOT NULL, action INTEGER NOT NULL,
          flags INTEGER NOT NULL, price REAL,
          source_month TEXT NOT NULL, tie_conflict INTEGER NOT NULL,
          file_months_seen INTEGER NOT NULL DEFAULT 1,
          PRIMARY KEY (publisher_id, symbol, ref_date)
        )
    """)
    return conn


def ingest_latest(conn: sqlite3.Connection, latest: pd.DataFrame, source_month: str) -> None:
    """Merge each source-month's last message; newer delete/preliminary wins."""
    newer = ("excluded.ts_ns > states.ts_ns OR "
             "(excluded.ts_ns = states.ts_ns AND "
             "excluded.sequence > states.sequence)")
    equal = ("excluded.ts_ns = states.ts_ns AND "
             "excluded.sequence = states.sequence")
    different = ("excluded.action IS NOT states.action OR "
                 "excluded.flags IS NOT states.flags OR "
                 "excluded.price IS NOT states.price")
    fields = ["ts_ns", "sequence", "action", "flags", "price", "source_month"]
    clauses = ",\n".join(
        f"{name} = CASE WHEN {newer} THEN excluded.{name} "
        f"ELSE states.{name} END"
        for name in fields
    )
    statement = f"""
    INSERT INTO states (
       publisher_id,symbol,ref_date,ts_ns,sequence,action,flags,price,
       source_month,tie_conflict,file_months_seen
    ) VALUES (?,?,?,?,?,?,?,?,?,?,1)
    ON CONFLICT (publisher_id,symbol,ref_date)
    DO UPDATE SET
      {clauses},
      tie_conflict = CASE
        WHEN {newer} THEN excluded.tie_conflict
        WHEN {equal} THEN MAX(
          states.tie_conflict,excluded.tie_conflict,({different}))
        ELSE states.tie_conflict END,
      file_months_seen = states.file_months_seen+1
    """
    rows = []
    for r in latest.itertuples(index=False):
        price = float(r.price) if pd.notna(r.price) else None
        if price is not None and not np.isfinite(price):
            price = None
        rows.append((
            int(r.publisher_id), str(r.symbol), str(r.ref_date),
            int(r.ts_ns), int(r.sequence), int(r.action), int(r.flags),
            price, source_month, int(r.tie_conflict),
        ))
    with conn:
        conn.executemany(statement, rows)


def summarize(conn: sqlite3.Connection, registry: dict, months: list[str],
              ingestion: list[dict]) -> dict:
    row = conn.execute("""
    SELECT COUNT(*),
      SUM(file_months_seen > 1),
      SUM(tie_conflict != 0),
      SUM(action != 1),
      SUM(action = 1 AND (flags & 1)=0),
      SUM(action = 1 AND (flags & 1)!=0 AND (flags & 8)!=0),
      SUM(action = 1 AND (flags & 1)!=0 AND (flags & 8)=0
          AND (price IS NULL OR price < 0)),
      SUM(action = 1 AND (flags & 1)!=0 AND (flags & 8)=0
          AND price >= 0 AND tie_conflict=0),
      SUM(action = 1 AND (flags & 1)!=0 AND (flags & 8)=0
          AND price >= 0 AND tie_conflict=0 AND (flags & 2)!=0),
      COUNT(DISTINCT CASE
        WHEN action = 1 AND (flags & 1)!=0 AND (flags & 8)=0
          AND price >= 0 AND tie_conflict=0
        THEN ref_date END),
      SUM(source_month != SUBSTR(ref_date,1,7))
    FROM states
    """).fetchone()
    columns = (
        "distinct_tentative_symbol_reference_keys",
        "keys_seen_in_multiple_file_months",
        "top_rank_ambiguous_keys",
        "latest_deleted_keys",
        "latest_preliminary_keys",
        "latest_intraday_final_keys",
        "latest_invalid_price_keys",
        "selected_final_nonintraday_keys",
        "selected_actual_flagged",
        "distinct_selected_reference_dates",
        "latest_update_source_month_differs_from_reference",
    )
    output = {key: int(value or 0) for key, value in zip(columns, row)}
    output["selected_theoretical_flagged"] = (
        output["selected_final_nonintraday_keys"]
        - output["selected_actual_flagged"]
    )
    output.update({
        "months_processed": len(months),
        "source_months": months,
        "symbol_identities_observed": len(registry),
        "symbol_groups_conflicting_across_months": sum(
            1 for v in registry.values() if v[2]
        ),
        "symbol_groups_not_safe_for_outright": sum(
            1 for v in registry.values() if not v[1]
        ),
        "settlement_events_read": sum(x["settlement_events"] for x in ingestion),
        "settlement_events_with_safe_identity": sum(
            x["events_with_safe_global_symbol"] for x in ingestion
        ),
        "no_databento_api_calls": True,
        "source_data_private": True,
        "status": "cross_month_provisional_not_validated_settlement_panel",
        "warning": (
            "All source months were replayed for latest actions, including "
            "preliminary and deletions. The DB has proprietary price records. "
            "Historical contract/price-scale validation, exchange corrections "
            "after the collection cutoff, and strictly lagged market inputs "
            "remain unverified."
        ),
    })
    return output
