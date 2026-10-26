"""Synthetic AAO correction/add/delete tests; no licensed market prices."""
import pandas as pd
import pytest

from bayesian_asian_options.aao_settlements import normalize


def samples():
    d = pd.DataFrame([
        (1, "ABC", "C", "AAO", 0, "A", "2026-07-01", 70., "NYMEX", "CL"),
        (1, "ABC", "C", "AAO", 0, "M", "2026-07-01", 70., "NYMEX", "CL"),
        (1, "XYZ", "P", "AAO", 0, "A", "2026-07-01", 72., "NYMEX", "CL"),
        (1, "STRAT", "T", "AAO", 2, "A", "2026-07-01", 72., "NYMEX", "CL"),
    ], columns=[
        "publisher_id", "raw_symbol", "instrument_class", "asset",
        "leg_count", "security_update_action", "expiration", "strike_price",
        "exchange", "underlying",
    ])
    s = pd.DataFrame([
        (1, "ABC", "2026-06-01", "2026-06-02T01:00:00Z", 3, 0, 1, 1, 1.0),
        (1, "ABC", "2026-06-01", "2026-06-02T02:00:00Z", 3, 3, 1, 2, 1.1),
        (1, "ABC", "2026-06-01", "2026-06-02T03:00:00Z", 3, 3, 2, 3, 1.1),
        (1, "XYZ", "2026-06-01", "2026-06-02T01:00:00Z", 3, 1, 1, 1, 2.0),
        (1, "XYZ", "2026-06-01", "2026-06-02T04:00:00Z", 3, 3, 1, 4, 2.1),
        (1, "STRAT", "2026-06-01", "2026-06-02T04:00:00Z", 3, 3, 1, 5, 2.2),
    ], columns=[
        "publisher_id", "symbol", "ts_ref", "ts_event", "stat_type",
        "stat_flags", "update_action", "sequence", "price",
    ])
    return d, s


def test_delete_tombstones_final():
    d, s = samples()
    panel, result = normalize(d, s)
    assert result["selected_final_nonintraday_keys"] == 1
    assert result["latest_deleted_keys"] == 1
    assert panel.iloc[0]["symbol"] == "XYZ"
    assert panel.iloc[0]["price"] == 2.1
    assert bool(panel.iloc[0]["final_actual"])


def test_preliminary_after_final_removes_candidate():
    d, s = samples()
    s.loc[len(s)] = (
        1, "XYZ", "2026-06-01", "2026-06-02T05:00:00Z",
        3, 0, 1, 10, 2.2,
    )
    panel, result = normalize(d, s)
    assert len(panel) == 0
    assert result["latest_not_final_keys"] == 1


def test_reused_symbol_with_conflicting_strike_is_rejected():
    d, s = samples()
    d.loc[len(d)] = (
        1, "XYZ", "P", "AAO", 0, "A", "2026-07-01",
        75., "NYMEX", "CL",
    )
    panel, result = normalize(d, s)
    assert len(panel) == 0
    assert result["ambiguous_or_non_outright_definition_groups"] == 2


def test_same_rank_conflicting_price_rejected():
    d, s = samples()
    s.loc[len(s)] = (
        1, "XYZ", "2026-06-01", "2026-06-02T04:00:00Z",
        3, 3, 1, 4, 8.0,
    )
    panel, result = normalize(d, s)
    assert len(panel) == 0
    assert result["conflicting_latest_rank_keys_rejected"] == 1


def test_intraday_final_not_selected():
    d, s = samples()
    s.loc[4, "stat_flags"] = 11
    panel, result = normalize(d, s)
    assert len(panel) == 0
    assert result["latest_intraday_final_keys"] == 1


def test_unknown_statistic_action_refused():
    d, s = samples()
    s.loc[0, "update_action"] = 3
    with pytest.raises(ValueError, match="unknown statistic"):
        normalize(d, s)


def test_multiple_reference_dates_are_distinct():
    d, s = samples()
    s.loc[len(s)] = (
        1, "XYZ", "2026-06-02", "2026-06-03T04:00:00Z",
        3, 1, 1, 20, 3.,
    )
    panel, result = normalize(d, s)
    assert len(panel) == 2
    assert result["distinct_candidate_reference_dates"] == 2


def test_unknown_definition_action_refused():
    d, s = samples()
    d.loc[0, "security_update_action"] = "Q"
    with pytest.raises(ValueError, match="definition security_update_action"):
        normalize(d, s)


def test_empty_mapped_symbol_cannot_be_selected():
    d, s = samples()
    s.loc[4, "symbol"] = None
    panel, result = normalize(d, s)
    assert len(panel) == 0
    assert result["events_without_safe_outright_mapping"] >= 1
