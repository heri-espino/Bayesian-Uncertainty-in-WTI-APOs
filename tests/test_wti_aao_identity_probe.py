"""Synthetic no-vendor-value fixtures for AAO identity diagnostics."""
import pandas as pd

from experiments.wti_aao_identity_probe import analyze


def test_id_coverage_does_not_infer_unique_contract_prices():
    defs = pd.DataFrame({
        "publisher_id": [1, 1, 1, 1],
        "instrument_id": [10, 10, 11, 12],
        "asset": ["AAO", "AAO", "AAO", "AAO"],
        "instrument_class": ["C", "C", "P", "T"],
        "raw_symbol": ["A", "A-new", "B", "spread"],
    })
    stats = pd.DataFrame({
        "publisher_id": [1, 1, 1, 1],
        "instrument_id": [10, 10, 11, 12],
        "stat_type": [3, 3, 3, 3],
        "stat_flags": [3, 1, 0, 3],
        "ts_ref": ["2021-02-02", "2021-02-02",
                   "2021-02-03", "2021-02-03"],
    })
    report = analyze(defs, stats)
    assert report["final_settlement_events"] == 3
    assert report["final_actual_events"] == 2
    assert report["unique_outright_id_pairs_observed"] == 2
    assert report["final_events_matching_outright_id_in_same_month"] == 2
    assert report["final_events_missing_outright_id_in_same_month"] == 1
    assert report["id_pairs_with_multiple_raw_symbols"] == 1
    assert report["tentative_unique_final_id_day_keys"] == 2


def test_missing_join_key_fails_closed():
    report = analyze(pd.DataFrame({"asset": ["AAO"]}),
                     pd.DataFrame({"stat_type": [3], "stat_flags": [1]}))
    assert "blocking_error" in report


def test_unsupported_statistics_code_fails_closed():
    defs = pd.DataFrame({"publisher_id": [1], "instrument_id": [1]})
    stats = pd.DataFrame({
        "publisher_id": [1], "instrument_id": [1],
        "stat_type": ["unknown"], "stat_flags": [1],
    })
    assert "blocking_error" in analyze(defs, stats)
