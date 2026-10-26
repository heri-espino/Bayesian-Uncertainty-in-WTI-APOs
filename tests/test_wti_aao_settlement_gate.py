"""Synthetic offline fixtures, never licensed market records."""
import pandas as pd
import pytest

from experiments.wti_aao_settlement_gate import evaluate


def frames():
    definitions = pd.DataFrame([
        ("2026-06-02 00:00", 1, 10, "AAO", "C",
         "C-TEST", "2026-07-01", 70000, 0, "A"),
        ("2026-06-02 00:00", 1, 11, "AAO", "T",
         "STRATEGY-TEST", "2026-07-01", 70000, 2, "A"),
        ("2026-06-02 11:00", 1, 10, "AAO", "C",
         "C-TEST", "2026-07-01", 70000, 0, "M"),
        ("2026-06-03 15:00", 1, 10, "AAO", "C",
         "NEW-C-TEST", "2026-07-01", 72000, 0, "A"),
    ], columns=[
        "ts_event", "publisher_id", "instrument_id", "asset",
        "instrument_class", "raw_symbol", "expiration",
        "strike_price", "leg_count", "security_update_action",
    ])
    statistics = pd.DataFrame([
        ("2026-06-02 09:00", "2026-06-02", 1, 10, 3, 0, 1, 1),
        ("2026-06-02 14:00", "2026-06-02", 1, 10, 3, 3, 1, 2),
        ("2026-06-02 14:15", "2026-06-02", 1, 10, 3, 1, 1, 3),
        ("2026-06-02 14:20", "2026-06-02", 1, 11, 3, 3, 1, 4),
        ("2026-06-03 14:00", "2026-06-03", 1, 10, 3, 3, 1, 5),
        ("2026-06-03 16:00", "2026-06-02", 1, 10, 3, 3, 1, 6),
    ], columns=[
        "ts_event", "ts_ref", "publisher_id", "instrument_id",
        "stat_type", "stat_flags", "update_action", "sequence",
    ])
    return definitions, statistics


def test_same_event_day_asof_excludes_unknown_and_spreads():
    d, s = frames()
    r = evaluate(d, s)
    assert r["settlement_events"] == 6
    assert r["without_same_event_day_asof_definition"] == 1
    assert r["matched_asof_definition_events"] == 5
    assert r["excluded_non_outright_or_inactive_events"] == 1
    assert r["selected_final_active_keys"] == 2
    assert r["selected_actual_flagged"] == 1
    assert r["selected_theoretical_flagged"] == 1
    assert r["selected_published_on_different_utc_date"] == 1
    assert r["distinct_selected_reference_dates"] == 1


def test_deleted_definition_is_not_backfilled_from_old_definition():
    d, s = frames()
    d.loc[len(d)] = (
        "2026-06-02 14:10", 1, 10, "AAO", "C", "C-TEST",
        "2026-07-01", 70000, 0, "D",
    )
    r = evaluate(d, s)
    assert r["selected_final_active_keys"] == 1
    assert r["excluded_non_outright_or_inactive_events"] >= 2


def test_deletion_of_last_statistic_removes_that_final_key():
    d, s = frames()
    s.loc[len(s)] = (
        "2026-06-03 17:00", "2026-06-02",
        1, 10, 3, 3, 2, 7,
    )
    r = evaluate(d, s)
    assert r["selected_final_active_keys"] == 1


def test_future_definition_does_not_resolve_past_statistic():
    d, s = frames()
    d.loc[d["instrument_id"].eq(10), "ts_event"] = "2026-06-03 18:00"
    r = evaluate(d, s)
    assert r["without_same_event_day_asof_definition"] >= 4


def test_unknown_definition_action_fails_closed():
    d, s = frames()
    d.loc[0, "security_update_action"] = "UNKNOWN"
    with pytest.raises(ValueError, match="Unknown definition"):
        evaluate(d, s)


def test_unknown_statistic_action_fails_closed():
    d, s = frames()
    s.loc[0, "update_action"] = 255
    with pytest.raises(ValueError, match="Unknown statistics"):
        evaluate(d, s)


def test_tied_updates_are_not_selected_arbitrarily():
    d, s = frames()
    duplicate = s.iloc[[2]].copy()
    duplicate["stat_flags"] = 3
    s = pd.concat([s, duplicate], ignore_index=True)
    r = evaluate(d, s)
    assert r["ambiguous_tied_keys_excluded"] == 1
    assert r["selected_final_active_keys"] == 1


def test_missing_required_field_fails_closed():
    d, s = frames()
    with pytest.raises(ValueError, match="Missing schema"):
        evaluate(d.drop(columns=["leg_count"]), s)
