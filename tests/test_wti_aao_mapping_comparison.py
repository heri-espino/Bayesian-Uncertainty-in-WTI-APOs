"""Synthetic definition and settlement fixtures; no licensed market records."""
import pandas as pd
import pytest

from experiments.wti_aao_mapping_comparison import compare


def fixtures():
    d = pd.DataFrame([
        ("2026-06-01 00:00", 1, 10, "C1", "C", "2026-07-01", 70, "NYMEX", "CL", "AAO", 0, "A"),
        ("2026-06-01 12:00", 1, 11, "P1", "P", "2026-07-01", 70, "NYMEX", "CL", "AAO", 0, "A"),
        ("2026-06-02 18:00", 1, 10, "C2", "C", "2026-07-01", 70, "NYMEX", "CL", "AAO", 0, "A"),
        ("2026-06-01 09:00", 1, 12, "S", "T", "2026-07-01", 70, "NYMEX", "CL", "AAO", 2, "A"),
    ], columns=[
        "ts_event", "publisher_id", "instrument_id", "raw_symbol",
        "instrument_class", "expiration", "strike_price",
        "exchange", "underlying", "asset", "leg_count", "security_update_action",
    ])
    s = pd.DataFrame([
        ("2026-06-02 02:00", "2026-06-01", 1, 10, 3, 3),
        ("2026-06-02 02:00", "2026-06-01", 1, 11, 3, 1),
        ("2026-06-02 02:00", "2026-06-01", 1, 12, 3, 3),
        ("2026-06-02 19:00", "2026-06-02", 1, 10, 3, 3),
    ], columns=[
        "ts_event", "ts_ref", "publisher_id", "instrument_id",
        "stat_type", "stat_flags",
    ])
    return d, s


def test_reference_day_resolves_off_day_publication():
    d, s = fixtures()
    r = compare(d, s)
    assert r["final_events"] == 4
    assert r["publication_reference_date_disagreement"] == 3
    assert r["reference_date"]["unambiguous_active_outright_match"] == 3
    assert r["publication_utc_day"]["unambiguous_active_outright_match"] == 1
    assert r["preceding_publication_day"]["unambiguous_active_outright_match"] == 3
    assert r["events_with_at_least_one_candidate_mapping"] == 3


def test_ambiguous_day_definition_excluded():
    d, s = fixtures()
    clash = d.iloc[[0]].copy()
    clash["raw_symbol"] = "DIFFERENT"
    d = pd.concat([d, clash], ignore_index=True)
    r = compare(d, s)
    assert r["ambiguous_definition_id_days"] == 1
    assert r["reference_date"]["unambiguous_active_outright_match"] == 2


def test_no_future_definition_even_if_day_matches():
    d, s = fixtures()
    d.loc[1, "ts_event"] = "2026-06-02 20:00"
    r = compare(d, s)
    assert r["events_with_at_least_one_candidate_mapping"] == 2


def test_deletion_flags_day_as_inactive():
    d, s = fixtures()
    d.loc[len(d)] = (
        "2026-06-01 22:00", 1, 11, "P1", "P", "2026-07-01",
        70, "NYMEX", "CL", "AAO", 0, "D",
    )
    r = compare(d, s)
    assert r["reference_date"]["unambiguous_active_outright_match"] == 2


def test_schema_and_actions_fail_closed():
    d, s = fixtures()
    with pytest.raises(ValueError, match="Missing"):
        compare(d.drop(columns=["leg_count"]), s)
    d.loc[0, "security_update_action"] = "Q"
    with pytest.raises(ValueError, match="Unknown"):
        compare(d, s)


def test_reused_id_across_days_flags_conflicting_contract_mapping():
    d, s = fixtures()
    r = compare(d, s)
    # A June 2 event sees C1 on the prior day and C2 on the current day.
    assert r["events_with_conflicting_candidate_contracts"] == 1
    assert r["events_with_at_least_one_consistent_candidate"] == 2
