"""Synthetic multi-month settlement corrections; never real vendor values."""
import sqlite3

import pandas as pd
import pytest

from bayesian_asian_options.aao_cross_month import (
    initialize_db, ingest_latest, merge_registry, monthly_latest, summarize,
)


def definitions(strike=70., symbol="AAO-C"):
    return pd.DataFrame([{
        "publisher_id": 1, "raw_symbol": symbol, "asset": "AAO",
        "instrument_class": "C", "expiration": "2026-07-01",
        "strike_price": strike, "underlying": "CL", "exchange": "NYMEX",
        "leg_count": 0, "security_update_action": "A",
    }])


def statistic(ref_date, pub_time, price, *, symbol="AAO-C",
              action=1, flags=3, sequence=1):
    return {
        "publisher_id": 1, "symbol": symbol, "ts_event": pub_time,
        "ts_ref": ref_date, "stat_type": 3, "stat_flags": flags,
        "update_action": action, "sequence": sequence, "price": price,
    }


def test_next_month_deletion_supersedes_prior_final(tmp_path):
    registry = {}
    merge_registry(registry, definitions())
    merge_registry(registry, definitions())
    january = pd.DataFrame([
        statistic("2026-01-30", "2026-01-30T21:00:00Z", 1.5),
    ])
    february = pd.DataFrame([
        statistic("2026-01-30", "2026-02-02T10:00:00Z", 1.5,
                  action=2, flags=3),
        statistic("2026-02-02", "2026-02-03T00:00:00Z", 2.0,
                  sequence=2, flags=1),
    ])
    conn = initialize_db(tmp_path / "private.sqlite3")
    i1, r1 = monthly_latest(january, registry)
    i2, r2 = monthly_latest(february, registry)
    ingest_latest(conn, i1, "2026-01")
    ingest_latest(conn, i2, "2026-02")
    report = summarize(conn, registry, ["2026-01", "2026-02"], [r1, r2])
    assert report["distinct_tentative_symbol_reference_keys"] == 2
    assert report["keys_seen_in_multiple_file_months"] == 1
    assert report["latest_deleted_keys"] == 1
    assert report["selected_final_nonintraday_keys"] == 1
    assert report["selected_theoretical_flagged"] == 1
    assert report["latest_update_source_month_differs_from_reference"] == 1
    conn.close()


def test_later_preliminary_overrides_earlier_final(tmp_path):
    registry = merge_registry({}, definitions())
    initial = pd.DataFrame([statistic(
        "2026-01-30", "2026-01-30T20:00:00Z", 1.0, flags=3,
    )])
    correction = pd.DataFrame([statistic(
        "2026-01-30", "2026-02-01T00:00:00Z", 2.0, flags=0,
    )])
    conn = initialize_db(tmp_path / "state.sqlite3")
    a, ai = monthly_latest(initial, registry)
    b, bi = monthly_latest(correction, registry)
    ingest_latest(conn, a, "2026-01")
    ingest_latest(conn, b, "2026-02")
    info = summarize(conn, registry, ["2026-01", "2026-02"], [ai, bi])
    assert info["latest_preliminary_keys"] == 1
    assert info["selected_final_nonintraday_keys"] == 0
    conn.close()


def test_symbol_fingerprint_change_quarantines_both_months():
    registry = merge_registry({}, definitions(strike=70.))
    merge_registry(registry, definitions(strike=75.))
    assert not registry[(1, "AAO-C")][1]
    assert registry[(1, "AAO-C")][2]
    rows = pd.DataFrame([statistic(
        "2026-01-30", "2026-01-30T20:00:00Z", 1.0,
    )])
    latest, info = monthly_latest(rows, registry)
    assert latest.empty
    assert info["events_unmapped_or_ambiguous"] == 1


def test_cross_file_same_rank_disagreement_is_quarantined(tmp_path):
    registry = merge_registry({}, definitions())
    row = statistic("2026-01-30", "2026-01-30T20:00:00Z", 1.0)
    a, ai = monthly_latest(pd.DataFrame([row]), registry)
    b, bi = monthly_latest(pd.DataFrame([{**row, "price": 1.5}]), registry)
    conn = initialize_db(tmp_path / "tie.sqlite3")
    ingest_latest(conn, a, "2026-01")
    ingest_latest(conn, b, "2026-02")
    info = summarize(conn, registry, ["2026-01", "2026-02"], [ai, bi])
    assert info["top_rank_ambiguous_keys"] == 1
    assert info["selected_final_nonintraday_keys"] == 0
    conn.close()


def test_newer_unique_event_clears_earlier_tie_conflict(tmp_path):
    registry = merge_registry({}, definitions())
    a = statistic("2026-01-30", "2026-01-30T20:00:00Z", 1.0)
    two = pd.DataFrame([a, {**a, "price": 2.0}])
    later = pd.DataFrame([statistic(
        "2026-01-30", "2026-02-01T20:00:00Z", 3.0, sequence=2,
    )])
    conn = initialize_db(tmp_path / "fix.sqlite3")
    first, info1 = monthly_latest(two, registry)
    next_, info2 = monthly_latest(later, registry)
    assert info1["month_top_rank_conflicts"] == 1
    ingest_latest(conn, first, "2026-01")
    ingest_latest(conn, next_, "2026-02")
    report = summarize(conn, registry, ["2026-01", "2026-02"], [info1, info2])
    assert report["top_rank_ambiguous_keys"] == 0
    assert report["selected_final_nonintraday_keys"] == 1
    conn.close()


def test_cross_month_same_symbol_without_same_month_definition_is_counted(tmp_path):
    registry = merge_registry({}, definitions())
    # An update in February can use an identity established in January.
    february = pd.DataFrame([statistic(
        "2026-01-30", "2026-02-03T20:00:00Z", 1.8,
    )])
    out, info = monthly_latest(february, registry)
    assert len(out) == 1
    assert info["events_with_safe_global_symbol"] == 1


def test_reject_unexpected_statistics_action():
    registry = merge_registry({}, definitions())
    bad = pd.DataFrame([statistic(
        "2026-01-30", "2026-01-30T20:00:00Z", 1.0,
        action=8,
    )])
    with pytest.raises(ValueError, match="Unknown statistics update_action"):
        monthly_latest(bad, registry)


def test_missing_definitions_and_source_codes_fail_closed():
    with pytest.raises(ValueError, match="Definition columns missing"):
        merge_registry({}, definitions().drop(columns="expiration"))
    d = definitions()
    d.loc[0, "security_update_action"] = "?"
    with pytest.raises(ValueError, match="Unknown definition update action"):
        merge_registry({}, d)
