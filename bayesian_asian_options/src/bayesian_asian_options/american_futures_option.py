"""American options on futures and implied-volatility inversion.

The standard NYMEX WTI Crude Oil option (LO) is American style. Under the
maintained one-factor lognormal futures model with deterministic rates, the
futures price is treated as a martingale under the pricing measure. A
Cox--Ross--Rubinstein tree therefore uses

    u = exp(sigma * sqrt(dt)), d = 1/u,
    p = (1 - d) / (u - d),

and discounts continuation values at the continuously compounded risk-free
rate. Early exercise compares continuation value with immediate intrinsic
value on the futures contract.
"""

from __future__ import annotations

from dataclasses import dataclass
import math
from typing import Literal

import numpy as np
from scipy.optimize import brentq
from scipy.special import ndtr

OptionType = Literal["call", "put"]


@dataclass(frozen=True)
class ImpliedVolatilityResult:
    """Result of an implied-volatility inversion."""

    sigma: float
    status: str
    model_price: float
    intrinsic_value: float


def _validate_inputs(
    futures_price: float,
    strike: float,
    maturity_years: float,
    rate: float,
    option_type: OptionType,
) -> None:
    if option_type not in {"call", "put"}:
        raise ValueError("option_type must be 'call' or 'put'")
    if not math.isfinite(futures_price) or futures_price <= 0:
        raise ValueError("futures_price must be finite and positive")
    if not math.isfinite(strike) or strike <= 0:
        raise ValueError("strike must be finite and positive")
    if not math.isfinite(maturity_years) or maturity_years < 0:
        raise ValueError("maturity_years must be finite and non-negative")
    if not math.isfinite(rate):
        raise ValueError("rate must be finite")


def futures_option_intrinsic(
    futures_price: float,
    strike: float,
    option_type: OptionType,
) -> float:
    """Return immediate exercise value of an option on futures."""
    sign = 1.0 if option_type == "call" else -1.0
    return float(max(sign * (float(futures_price) - float(strike)), 0.0))


def black76_futures_option_price(
    futures_price: float,
    strike: float,
    maturity_years: float,
    rate: float,
    sigma: float,
    option_type: OptionType,
) -> float:
    """Return the European Black-76 option-on-futures price.

    This is a robustness/reference object only for the WTI study. The
    production external-Q inversion uses `american_futures_option_crr`.
    """
    _validate_inputs(futures_price, strike, maturity_years, rate, option_type)
    if not math.isfinite(sigma) or sigma < 0:
        raise ValueError("sigma must be finite and non-negative")

    intrinsic = futures_option_intrinsic(futures_price, strike, option_type)
    if maturity_years == 0:
        return intrinsic
    discount = math.exp(-rate * maturity_years)
    if sigma <= 1e-14:
        return float(discount * intrinsic)

    vol_sqrt_t = sigma * math.sqrt(maturity_years)
    d1 = (
        math.log(futures_price / strike)
        + 0.5 * sigma * sigma * maturity_years
    ) / vol_sqrt_t
    d2 = d1 - vol_sqrt_t

    if option_type == "call":
        return float(
            discount * (futures_price * ndtr(d1) - strike * ndtr(d2))
        )
    return float(
        discount * (strike * ndtr(-d2) - futures_price * ndtr(-d1))
    )


def american_futures_option_crr(
    futures_price: float,
    strike: float,
    maturity_years: float,
    rate: float,
    sigma: float,
    option_type: OptionType,
    *,
    steps: int = 200,
) -> float:
    """Price an American option on futures with a CRR recombining tree.

    Values are per unit of the underlying commodity. For WTI this means
    dollars per barrel; contract multipliers do not enter the IV inversion.
    """
    _validate_inputs(futures_price, strike, maturity_years, rate, option_type)
    if not math.isfinite(sigma) or sigma < 0:
        raise ValueError("sigma must be finite and non-negative")
    if steps < 2:
        raise ValueError("steps must be at least 2")

    intrinsic_0 = futures_option_intrinsic(
        futures_price, strike, option_type
    )
    if maturity_years == 0 or sigma <= 1e-14:
        return intrinsic_0

    dt = maturity_years / int(steps)
    u = math.exp(sigma * math.sqrt(dt))
    d = 1.0 / u
    denominator = u - d
    if abs(denominator) < 1e-15:
        return intrinsic_0

    # Futures are martingales under the maintained deterministic-rate model.
    p = (1.0 - d) / denominator
    if not 0.0 <= p <= 1.0:
        raise ValueError(
            "CRR probability outside [0, 1]; increase steps or inspect inputs"
        )
    disc = math.exp(-rate * dt)
    sign = 1.0 if option_type == "call" else -1.0

    j = np.arange(steps + 1, dtype=float)
    terminal_futures = (
        futures_price * np.power(u, j) * np.power(d, steps - j)
    )
    values = np.maximum(
        sign * (terminal_futures - strike), 0.0
    )

    for n in range(steps - 1, -1, -1):
        continuation = disc * (
            p * values[1 : n + 2]
            + (1.0 - p) * values[: n + 1]
        )
        jn = np.arange(n + 1, dtype=float)
        node_futures = (
            futures_price
            * np.power(u, jn)
            * np.power(d, n - jn)
        )
        exercise = np.maximum(
            sign * (node_futures - strike), 0.0
        )
        values = np.maximum(continuation, exercise)

    return float(values[0])


def implied_volatility_american_futures(
    market_price: float,
    futures_price: float,
    strike: float,
    maturity_years: float,
    rate: float,
    option_type: OptionType,
    *,
    steps: int = 200,
    sigma_lower: float = 1e-6,
    sigma_upper: float = 3.0,
    price_tolerance: float = 1e-8,
) -> ImpliedVolatilityResult:
    """Invert an American futures-option market price to annualized volatility.

    The inversion fails closed instead of clipping prices that lie outside the
    selected volatility bracket or below immediate exercise value.
    """
    _validate_inputs(futures_price, strike, maturity_years, rate, option_type)
    if not math.isfinite(market_price) or market_price < 0:
        raise ValueError("market_price must be finite and non-negative")
    if not 0 < sigma_lower < sigma_upper:
        raise ValueError("require 0 < sigma_lower < sigma_upper")

    intrinsic = futures_option_intrinsic(
        futures_price, strike, option_type
    )
    if maturity_years == 0:
        status = (
            "expired_match"
            if abs(market_price - intrinsic) <= price_tolerance
            else "expired_mismatch"
        )
        return ImpliedVolatilityResult(
            sigma=float("nan"),
            status=status,
            model_price=intrinsic,
            intrinsic_value=intrinsic,
        )

    if market_price < intrinsic - price_tolerance:
        return ImpliedVolatilityResult(
            sigma=float("nan"),
            status="below_intrinsic",
            model_price=float("nan"),
            intrinsic_value=intrinsic,
        )

    def objective(sigma: float) -> float:
        return (
            american_futures_option_crr(
                futures_price,
                strike,
                maturity_years,
                rate,
                sigma,
                option_type,
                steps=steps,
            )
            - market_price
        )

    low_value = objective(sigma_lower)
    if abs(low_value) <= price_tolerance:
        return ImpliedVolatilityResult(
            sigma=float(sigma_lower),
            status="ok_lower_bound",
            model_price=float(market_price + low_value),
            intrinsic_value=intrinsic,
        )

    high_value = objective(sigma_upper)
    if high_value < 0:
        return ImpliedVolatilityResult(
            sigma=float("nan"),
            status="above_sigma_upper_price",
            model_price=float(market_price + high_value),
            intrinsic_value=intrinsic,
        )

    if low_value > 0:
        return ImpliedVolatilityResult(
            sigma=float("nan"),
            status="below_sigma_lower_price",
            model_price=float(market_price + low_value),
            intrinsic_value=intrinsic,
        )

    sigma = float(
        brentq(
            objective,
            sigma_lower,
            sigma_upper,
            xtol=1e-10,
            rtol=1e-10,
            maxiter=100,
        )
    )
    model_price = american_futures_option_crr(
        futures_price,
        strike,
        maturity_years,
        rate,
        sigma,
        option_type,
        steps=steps,
    )
    return ImpliedVolatilityResult(
        sigma=sigma,
        status="ok",
        model_price=float(model_price),
        intrinsic_value=intrinsic,
    )
