import numpy as np

from bayesian_asian_options.synthetic_validation import (
    arithmetic_price_curve_by_strike,
    arithmetic_price_curve_by_volatility,
    deterministic_arithmetic_asian_call_price,
    geometric_asian_call_mc,
    risk_neutral_martingale_check,
    zero_volatility_limit_check,
)


def test_deterministic_asian_price_with_flat_risk_neutral_path():
    price = deterministic_arithmetic_asian_call_price(
        100.0,
        90.0,
        0.0,
        1.0,
        q=0.0,
        n_steps=12,
    )
    assert price == 10.0


def test_geometric_monte_carlo_matches_closed_form():
    check = geometric_asian_call_mc(
        100.0,
        100.0,
        0.03,
        0.25,
        1.0,
        n_steps=16,
        n_paths=8_000,
        seed=20260909,
    )
    assert abs(check.z_score) < 5.0


def test_risk_neutral_discounted_stock_is_martingale():
    check = risk_neutral_martingale_check(
        100.0,
        0.03,
        0.25,
        1.0,
        q=0.01,
        n_paths=20_000,
        seed=31415,
    )
    assert abs(check.z_score) < 5.0


def test_tiny_volatility_converges_to_deterministic_asian_price():
    check = zero_volatility_limit_check(
        100.0,
        100.0,
        0.03,
        1.0,
        n_steps=16,
        n_paths=4_000,
        sigma_epsilon=1.0e-4,
        seed=27182,
    )
    assert abs(check.error) < max(5.0 * check.standard_error, 1.0e-3)


def test_call_price_is_nonincreasing_in_strike_with_common_random_numbers():
    prices = arithmetic_price_curve_by_strike(
        (80.0, 100.0, 120.0),
        S0=100.0,
        r=0.03,
        sigma=0.25,
        T=1.0,
        n_steps=16,
        n_paths=4_000,
        seed=16180,
    )
    assert np.all(np.diff(prices) <= 0.0)


def test_atm_call_price_increases_with_volatility():
    prices = arithmetic_price_curve_by_volatility(
        (0.15, 0.25, 0.40),
        S0=100.0,
        K=100.0,
        r=0.03,
        T=1.0,
        n_steps=16,
        n_paths=6_000,
        seed=14142,
    )
    assert np.all(np.diff(prices) > 0.0)


def test_seeded_geometric_check_is_exactly_reproducible():
    kwargs = dict(
        S0=100.0,
        K=100.0,
        r=0.03,
        sigma=0.25,
        T=1.0,
        n_steps=12,
        n_paths=2_000,
        seed=123456,
    )
    first = geometric_asian_call_mc(**kwargs)
    second = geometric_asian_call_mc(**kwargs)
    assert first == second
