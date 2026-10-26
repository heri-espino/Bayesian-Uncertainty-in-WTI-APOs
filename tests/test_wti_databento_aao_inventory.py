"""Synthetic offline unit tests for AAO DBN inventory counts."""
import pandas as pd

from experiments.wti_databento_aao_inventory import (
    reference_dates,
    summarize_definition,
    summarize_statistics,
)


def test_definition_inventory_groups_contract_types():
    frame = pd.DataFrame({
        "asset": ["AAO", "AAO", "AAO"],
        "group": ["AAO"] * 3,
        "exchange": ["NYMEX"] * 3,
        "instrument_class": ["C", "P", "C"],
        "raw_symbol": ["a", "b", "a"],
        "strike_price": [75, 80, 75],
        "expiration": pd.to_datetime([
            "2025-07-01", "2025-07-01", "2025-07-01",
        ]),
    })
    result = summarize_definition(frame)
    assert result["records"] == 3
    assert result["unique_symbols"] == 2
    assert result["distinct_expirations"] == 1
    assert result["top_instrument_class"] == {"C": 2, "P": 1}


def test_flags_distinguish_final_actual_and_theoretical():
    frame = pd.DataFrame({
        "stat_type": [3, 3, 3, 6, 9],
        "stat_flags": [3, 1, 0, 0, 0],
        "ts_ref": ["2025-06-11", "2025-06-12",
                   "2025-06-12", None, None],
        "symbol": ["a", "b", "c", "a", "b"],
        "quantity": [None, None, None, 7, 0],
    })
    result = summarize_statistics(frame)
    assert result["settlement_events"] == 3
    assert result["final_events"] == 2
    assert result["final_actual_events"] == 1
    assert result["final_theoretical_events"] == 1
    assert result["preliminary_events"] == 1
    assert result["final_reference_dates"] == 2
    assert result["final_symbol_date_pairs"] == 2
    assert result["positive_cleared_volume_events"] == 1
    assert result["positive_open_interest_events"] == 0


def test_ts_ref_nanosecond_input():
    values = pd.Series([1749686400000000000, 1749686400000000000])
    result = reference_dates(values)
    assert result.nunique() == 1


def test_missing_flags_is_diagnostic_not_success():
    frame = pd.DataFrame({"stat_type": [3, 3]})
    assert summarize_statistics(frame)["error"] == "No stat_flags column"
