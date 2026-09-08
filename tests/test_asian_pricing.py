import inspect

import numpy as np

from src.asian_pricing import (
    asian_arithmetic_call_mc,
    discrete_geometric_asian_call_price,
)


def test_pricer_has_no_physical_drift_argument():
    """Regression test for the P-vs-Q pricing distinction."""
    params = inspect.signature(asian_arithmetic_call_mc).parameters
    assert "mu" not in params


def test_geometric_control_reduces_monte_carlo_error():
    estimate = asian_arithmetic_call_mc(
        100.0,
        100.0,
        0.03,
        0.25,
        1.0,
        n_steps=64,
        n_paths=20_000,
        seed=7,
        antithetic=True,
        geometric_control=True,
    )
    assert estimate.standard_error < estimate.raw_standard_error
    assert estimate.standard_error < 0.01


def test_arithmetic_call_increases_with_volatility_for_atm_case():
    low = asian_arithmetic_call_mc(
        100.0,
        100.0,
        0.03,
        0.15,
        1.0,
        n_steps=64,
        n_paths=20_000,
        seed=11,
    ).price
    high = asian_arithmetic_call_mc(
        100.0,
        100.0,
        0.03,
        0.35,
        1.0,
        n_steps=64,
        n_paths=20_000,
        seed=11,
    ).price
    assert high > low


def test_geometric_closed_form_is_finite_and_bounded():
    price = discrete_geometric_asian_call_price(
        100.0,
        100.0,
        0.03,
        0.25,
        1.0,
        n_steps=252,
    )
    assert np.isfinite(price)
    assert 0.0 < price < 100.0
