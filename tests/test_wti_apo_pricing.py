import numpy as np
import pandas as pd

from src.wti_apo_pricing import expected_average_level, wti_average_price_option_mc
from src.wti_first_nearby import assign_first_nearby_contract, build_forward_fixing_curve


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
