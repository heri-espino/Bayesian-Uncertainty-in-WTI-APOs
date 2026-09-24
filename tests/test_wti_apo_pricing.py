import numpy as np
import pandas as pd
import pytest

from bayesian_asian_options.wti_apo_pricing import expected_average_level, wti_average_price_option_mc
from bayesian_asian_options.wti_first_nearby import (
    assign_first_nearby_contract,
    build_forward_fixing_curve,
    build_realized_fixing_curve,
    reconstruct_first_nearby_settlement_history,
)


def test_fully_realized_option_is_exact():
    est = wti_average_price_option_mc(
        realized_fixings=np.array([90.0, 100.0, 110.0]),
        forward_fixings=np.array([]),
        fixing_times=np.array([]),
        strike=95.0,
        sigma=0.30,
        rate=0.0,
        time_to_expiry=0.0,
        option_type="call",
        n_paths=1000,
        seed=1,
    )
    assert est.price == 5.0
    assert est.standard_error == 0.0
    assert est.expected_average == 100.0


def test_expected_average_combines_realized_and_forward():
    assert expected_average_level(np.array([90.0]), np.array([100.0, 110.0])) == 100.0


def test_call_and_put_monotonicity_in_strike():
    common = dict(
        realized_fixings=np.array([]),
        forward_fixings=np.array([95.0, 100.0, 105.0]),
        fixing_times=np.array([10, 20, 30]) / 365.0,
        sigma=0.35,
        rate=0.03,
        time_to_expiry=30 / 365.0,
        n_paths=20_000,
        seed=7,
    )
    call95 = wti_average_price_option_mc(strike=95.0, option_type="call", **common).price
    call105 = wti_average_price_option_mc(strike=105.0, option_type="call", **common).price
    put95 = wti_average_price_option_mc(strike=95.0, option_type="put", **common).price
    put105 = wti_average_price_option_mc(strike=105.0, option_type="put", **common).price
    assert call95 > call105
    assert put95 < put105


def test_first_nearby_roll_mapping():
    expiries = pd.DataFrame(
        {
            "contract": ["CLV26", "CLX26", "CLZ26"],
            "last_trade_date": ["2026-09-22", "2026-10-20", "2026-11-20"],
        }
    )
    fixing_dates = pd.to_datetime(["2026-09-21", "2026-09-23", "2026-10-21"])
    mapped = assign_first_nearby_contract(fixing_dates, expiries)
    assert mapped["contract"].tolist() == ["CLV26", "CLX26", "CLZ26"]

    curve = pd.DataFrame(
        {"contract": ["CLV26", "CLX26", "CLZ26"], "settlement": [100.0, 98.0, 96.0]}
    )
    forward = build_forward_fixing_curve(fixing_dates, expiries, curve)
    assert forward["settlement"].tolist() == [100.0, 98.0, 96.0]


def test_realized_first_nearby_fixings_use_exact_contract_dates():
    expiries = pd.DataFrame(
        {
            "contract": ["CLV26", "CLX26"],
            "last_trade_date": ["2026-09-22", "2026-10-20"],
        }
    )
    history = pd.DataFrame(
        {
            "trade_date": pd.to_datetime(
                ["2026-09-21", "2026-09-23", "2026-09-23"]
            ),
            "contract": ["CLV26", "CLV26", "CLX26"],
            "latest": [100.0, 999.0, 98.0],
            "source_field": ["Latest", "Latest", "Latest"],
        }
    )

    realized = build_realized_fixing_curve(
        pd.to_datetime(["2026-09-21", "2026-09-23"]),
        expiries,
        history,
    )

    assert realized["contract"].tolist() == ["CLV26", "CLX26"]
    assert realized["settlement"].tolist() == [100.0, 98.0]
    assert realized["source_field"].tolist() == ["Latest", "Latest"]


def test_realized_first_nearby_fixings_reject_missing_settlement():
    expiries = pd.DataFrame(
        {
            "contract": ["CLV26"],
            "last_trade_date": ["2026-09-22"],
        }
    )
    history = pd.DataFrame(
        {
            "trade_date": pd.to_datetime(["2026-09-01"]),
            "contract": ["CLV26"],
            "latest": [90.0],
        }
    )

    with pytest.raises(ValueError, match="Missing realized first-nearby settlements"):
        build_realized_fixing_curve(
            pd.to_datetime(["2026-09-01", "2026-09-02"]),
            expiries,
            history,
        )


def test_reconstructed_first_nearby_history_excludes_roll_return():
    expiries = pd.DataFrame(
        {
            "contract": ["CLV26", "CLX26"],
            "last_trade_date": ["2026-09-22", "2026-10-20"],
        }
    )
    history = pd.DataFrame(
        {
            "trade_date": pd.to_datetime(
                ["2026-09-21", "2026-09-22", "2026-09-23", "2026-09-24"]
            ),
            "contract": ["CLV26", "CLV26", "CLX26", "CLX26"],
            "settlement": [100.0, 101.0, 95.0, 96.0],
        }
    )

    out = reconstruct_first_nearby_settlement_history(history, expiries)

    assert out["contract"].tolist() == ["CLV26", "CLV26", "CLX26", "CLX26"]
    assert bool(out.loc[2, "roll_switch"])
    assert np.isnan(out.loc[2, "log_return"])
    assert not bool(out.loc[2, "usable_inference_return"])
    assert np.isclose(out.loc[3, "log_return"], np.log(96.0 / 95.0))


def test_reconstructed_first_nearby_history_flags_missing_front_settlement():
    expiries = pd.DataFrame(
        {
            "contract": ["CLV26", "CLX26"],
            "last_trade_date": ["2026-09-22", "2026-10-20"],
        }
    )
    history = pd.DataFrame(
        {
            "trade_date": pd.to_datetime(
                ["2026-09-21", "2026-09-22", "2026-09-22"]
            ),
            "contract": ["CLV26", "CLX26", "CLX26"],
            "settlement": [100.0, 96.0, 96.0],
        }
    )

    out = reconstruct_first_nearby_settlement_history(history, expiries)

    missing = out.loc[out["trade_date"].eq(pd.Timestamp("2026-09-22"))].iloc[0]
    assert bool(missing["missing_settlement"])
    assert not bool(missing["usable_inference_return"])
