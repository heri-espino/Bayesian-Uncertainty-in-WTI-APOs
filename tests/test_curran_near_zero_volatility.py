import numpy as np

from bayesian_asian_options.asian_futures_pricing import curran_arithmetic_futures_option


def test_curran_is_stable_at_near_zero_volatility():
    price = curran_arithmetic_futures_option(
        realized_fixings=np.array([79.0]),
        forward_fixings=np.array([80.0, 81.0, 82.0]),
        fixing_times=np.array([0.05, 0.10, 0.15]),
        strike=82.0,
        sigma=1e-6,
        discount_factor=0.99,
        option_type="call",
    )
    assert np.isfinite(price)
    assert price >= 0.0


def test_curran_near_zero_matches_deterministic_limit():
    kwargs = dict(
        realized_fixings=np.array([79.0]),
        forward_fixings=np.array([80.0, 81.0, 82.0]),
        fixing_times=np.array([0.05, 0.10, 0.15]),
        strike=82.0,
        discount_factor=0.99,
        option_type="call",
    )
    near_zero = curran_arithmetic_futures_option(sigma=1e-6, **kwargs)
    deterministic = curran_arithmetic_futures_option(sigma=0.0, **kwargs)
    assert abs(near_zero - deterministic) < 1e-8
