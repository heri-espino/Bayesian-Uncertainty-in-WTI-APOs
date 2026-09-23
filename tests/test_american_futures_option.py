from __future__ import annotations

import math

import pytest

from bayesian_asian_options.american_futures_option import (
    american_futures_option_crr,
    black76_futures_option_price,
    futures_option_intrinsic,
    implied_volatility_american_futures,
)


@pytest.mark.parametrize("option_type", ["call", "put"])
def test_american_price_is_at_least_intrinsic(option_type: str) -> None:
    price = american_futures_option_crr(
        90.0, 92.0, 0.20, 0.04, 0.35, option_type, steps=150
    )
    intrinsic = futures_option_intrinsic(90.0, 92.0, option_type)
    assert price >= intrinsic


@pytest.mark.parametrize("option_type", ["call", "put"])
def test_zero_rate_crr_converges_near_black76(option_type: str) -> None:
    american = american_futures_option_crr(
        90.0, 92.0, 0.20, 0.0, 0.35, option_type, steps=500
    )
    european = black76_futures_option_price(
        90.0, 92.0, 0.20, 0.0, 0.35, option_type
    )
    assert american == pytest.approx(european, abs=0.02)


@pytest.mark.parametrize("option_type", ["call", "put"])
def test_implied_volatility_recovers_tree_price(option_type: str) -> None:
    true_sigma = 0.42
    market = american_futures_option_crr(
        89.0, 90.0, 0.15, 0.045, true_sigma, option_type, steps=180
    )
    result = implied_volatility_american_futures(
        market,
        89.0,
        90.0,
        0.15,
        0.045,
        option_type,
        steps=180,
    )
    assert result.status == "ok"
    assert result.sigma == pytest.approx(true_sigma, abs=1e-7)
    assert result.model_price == pytest.approx(market, abs=1e-8)


def test_implied_volatility_rejects_price_below_intrinsic() -> None:
    result = implied_volatility_american_futures(
        4.0,
        100.0,
        95.0,
        0.10,
        0.04,
        "call",
        steps=100,
    )
    assert result.status == "below_intrinsic"
    assert math.isnan(result.sigma)
