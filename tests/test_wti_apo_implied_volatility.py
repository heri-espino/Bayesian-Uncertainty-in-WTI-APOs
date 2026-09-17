from types import SimpleNamespace

import numpy as np
import pandas as pd

from bayesian_asian_options.asian_futures_pricing import curran_arithmetic_futures_option
from experiments.wti_apo_implied_volatility import (
    calibrate_sigma_q,
    implied_sigma_from_price,
)


def _price(strike: float, option_type: str, sigma: float) -> float:
    return curran_arithmetic_futures_option(
        realized_fixings=np.array([79.0]),
        forward_fixings=np.array([80.0, 81.0, 82.0]),
        fixing_times=np.array([0.05, 0.10, 0.15]),
        strike=strike,
        sigma=sigma,
        discount_factor=0.99,
        option_type=option_type,
    )


def test_implied_sigma_recovers_curran_input():
    true_sigma = 0.47
    market = _price(82.0, "call", true_sigma)
    sigma, status, _, _ = implied_sigma_from_price(
        market,
        lambda value: _price(82.0, "call", value),
        sigma_min=1e-6,
        sigma_max=2.0,
    )
    assert status == "interior"
    assert sigma is not None
    assert abs(sigma - true_sigma) < 1e-7


def test_implied_sigma_reports_price_outside_model_range():
    _, status, _, upper = implied_sigma_from_price(
        1e6,
        lambda value: _price(82.0, "call", value),
        sigma_min=1e-6,
        sigma_max=2.0,
    )
    assert status == "above_model_upper_bound"
    assert np.isfinite(upper)


def test_cross_sectional_calibration_recovers_common_sigma():
    true_sigma = 0.38
    contracts = []
    for strike, option_type in [
        (76.0, "call"),
        (80.0, "call"),
        (84.0, "call"),
        (78.0, "put"),
        (82.0, "put"),
        (86.0, "put"),
    ]:
        contracts.append(
            {
                "strike": strike,
                "option_type": option_type,
                "market_price": _price(strike, option_type, true_sigma),
            }
        )
    pricing = pd.DataFrame(contracts)
    sigma, mse = calibrate_sigma_q(
        pricing,
        realized=np.array([79.0]),
        forwards=np.array([80.0, 81.0, 82.0]),
        times=np.array([0.05, 0.10, 0.15]),
        discount=0.99,
        sigma_min=1e-6,
        sigma_max=2.0,
    )
    assert abs(sigma - true_sigma) < 1e-5
    assert mse < 1e-10
