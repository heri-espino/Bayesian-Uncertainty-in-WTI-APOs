import pandas as pd

from experiments.wti_apo_empirical_hybrid import (
    _candidate_curve_contracts,
    _cl_last_trade_rule_weekday,
    _complete_expiry_metadata,
)


def test_october_2026_curve_strip_avoids_old_delisted_contracts() -> None:
    assert _candidate_curve_contracts("2026-10") == ["CLV26", "CLX26", "CLZ26"]


def test_october_2026_cl_termination_dates_from_pilot_rule() -> None:
    assert _cl_last_trade_rule_weekday("CLV26") == pd.Timestamp("2026-09-22")
    assert _cl_last_trade_rule_weekday("CLX26") == pd.Timestamp("2026-10-20")
    assert _cl_last_trade_rule_weekday("CLZ26") == pd.Timestamp("2026-11-20")


def test_missing_yahoo_expiry_metadata_gets_named_fallback() -> None:
    raw = pd.DataFrame(
        {
            "contract": ["CLV26", "CLX26"],
            "settlement_date": ["2026-09-22", None],
            "settlement_date_source": ["yahoo_info:expireDate", None],
        }
    )
    completed = _complete_expiry_metadata(raw)
    assert completed.loc[0, "settlement_date_source"] == "yahoo_info:expireDate"
    assert completed.loc[1, "settlement_date"] == "2026-10-20"
    assert (
        completed.loc[1, "settlement_date_source"]
        == "cme_standard_rule_weekday_pilot_fallback"
    )
