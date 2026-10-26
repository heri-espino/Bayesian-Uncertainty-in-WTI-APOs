"""Synthetic fixtures for local DBN symbology coverage; no licensed prices."""
import pandas as pd
import pytest

from experiments.wti_aao_symbol_mapping import assess


def frames():
    definitions = pd.DataFrame([
        (1, "C1", "AAO", "C", 0, "2026-07-01", 70000, "NYMEX", "CL"),
        (1, "C1", "AAO", "C", 0, "2026-07-01", 70000, "NYMEX", "CL"),
        (1, "P1", "AAO", "P", 0, "2026-07-01", 70000, "NYMEX", "CL"),
        (1, "C2", "AAO", "C", 0, "2026-07-01", 71000, "NYMEX", "CL"),
        (1, "S", "AAO", "T", 2, "2026-07-01", 70000, "NYMEX", "CL"),
    ], columns=[
        "publisher_id", "raw_symbol", "asset", "instrument_class",
        "leg_count", "expiration", "strike_price", "exchange", "underlying",
    ])
    statistics = pd.DataFrame([
        (1, "C1", 3, 3, "2026-06-01"),
        (1, "C1", 3, 1, "2026-06-01"),
        (1, "P1", 3, 3, "2026-06-01"),
        (1, "C2", 3, 3, "2026-06-02"),
        (1, "S", 3, 3, "2026-06-02"),
        (1, "NOT_LISTED", 3, 3, "2026-06-02"),
        (1, None, 3, 3, "2026-06-02"),
        (1, "C1", 6, 0, "2026-06-02"),
    ], columns=[
        "publisher_id", "symbol", "stat_type", "stat_flags", "ts_ref",
    ])
    return definitions, statistics


def test_symbol_coverage_and_tentative_keys():
    d, s = frames()
    r = assess(d, s)
    assert r["final_settlement_events"] == 7
    assert r["final_events_with_nonempty_mapped_symbol"] == 6
    assert r["final_events_without_mapped_symbol"] == 1
    assert r["final_mapped_events_with_matching_raw_symbol"] == 5
    assert r["final_mapped_events_missing_matching_definition"] == 1
    assert r["final_mapped_events_with_unambiguous_outright_identity"] == 4
    assert r["final_mapped_events_with_ambiguous_or_non_outright_identity"] == 1
    assert r["tentative_unique_out_right_symbol_reference_date_keys"] == 3
    assert r["matched_reference_dates"] == 2


def test_reused_raw_symbol_with_different_strike_is_ambiguous():
    d, s = frames()
    d.loc[len(d)] = (
        1, "C1", "AAO", "C", 0, "2026-07-01", 72000, "NYMEX", "CL"
    )
    r = assess(d, s)
    assert r["definition_symbol_groups_with_multiple_contract_fingerprints"] == 1
    assert r["final_mapped_events_with_unambiguous_outright_identity"] == 2


def test_nonmatching_publisher_does_not_match_same_symbol():
    d, s = frames()
    s.loc[2, "publisher_id"] = 999
    r = assess(d, s)
    assert r["final_mapped_events_missing_matching_definition"] == 2


def test_missing_required_fields_are_errors():
    d, s = frames()
    with pytest.raises(ValueError, match="Missing definition"):
        assess(d.drop(columns="raw_symbol"), s)
    with pytest.raises(ValueError, match="statistics fields"):
        assess(d, s.drop(columns="symbol"))


def test_missing_settlement_flags_are_rejected():
    d, s = frames()
    s.loc[0, "stat_flags"] = None
    with pytest.raises(ValueError, match="unknown"):
        assess(d, s)


def test_no_recognized_settlements_rejected():
    d, s = frames()
    s["stat_type"] = 6
    with pytest.raises(ValueError, match="stat_type"):
        assess(d, s)
