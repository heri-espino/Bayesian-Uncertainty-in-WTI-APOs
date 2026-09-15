"""Risk-neutral Monte Carlo baseline for CME WTI Average Price Options.

CME WTI APOs average daily settlements of the *first-nearby* CL futures
contract during the calendar month.  This module therefore takes a vector of
current forward/futures levels for the remaining fixing dates, rather than one
spot price or one fixed futures maturity.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

import numpy as np


@dataclass(frozen=True)
class APOMonteCarloEstimate:
    """Monte Carlo estimate for one WTI Average Price Option."""

    price: float
    standard_error: float
    expected_average: float
    n_paths: int
    n_realized_fixings: int
    n_future_fixings: int


@dataclass(frozen=True)
class APOCrossSectionEstimate:
    """Joint Monte Carlo estimates for contracts sharing one APO fixing state."""

    prices: np.ndarray
    standard_errors: np.ndarray
    expected_average: float
    n_paths: int
    n_realized_fixings: int
    n_future_fixings: int


def expected_average_level(realized_fixings: np.ndarray, forward_fixings: np.ndarray) -> float:
    """Risk-neutral expected final arithmetic average at valuation time."""
    realized = np.asarray(realized_fixings, dtype=float)
    forwards = np.asarray(forward_fixings, dtype=float)
    values = np.concatenate([realized, forwards])
    if values.size == 0:
        raise ValueError("At least one realized or future fixing is required")
    if np.any(~np.isfinite(values)) or np.any(values <= 0):
        raise ValueError("Fixing and forward levels must be finite and positive")
    return float(values.mean())


def _resolve_discount_factor(
    *,
    rate: float | None,
    time_to_expiry: float,
    discount_factor: float | None,
) -> float:
    if not np.isfinite(time_to_expiry) or time_to_expiry < 0:
        raise ValueError("time_to_expiry must be finite and non-negative")
    if discount_factor is not None:
        value = float(discount_factor)
        if not np.isfinite(value) or value <= 0 or value > 1.5:
            raise ValueError("discount_factor must be positive and finite")
        return value
    if rate is None or not np.isfinite(rate):
        raise ValueError("provide either a finite rate or discount_factor")
    return float(np.exp(-float(rate) * time_to_expiry))


def _simulate_average(
    *,
    realized_fixings: np.ndarray,
    forward_fixings: np.ndarray,
    fixing_times: np.ndarray,
    sigma: float,
    n_paths: int,
    seed: int | None,
    antithetic: bool,
) -> tuple[np.ndarray, int, int]:
    realized = np.asarray(realized_fixings, dtype=float)
    forwards = np.asarray(forward_fixings, dtype=float)
    times = np.asarray(fixing_times, dtype=float)
    if realized.ndim != 1 or forwards.ndim != 1 or times.ndim != 1:
        raise ValueError("fixing arrays must be one-dimensional")
    if len(forwards) != len(times):
        raise ValueError("forward_fixings and fixing_times must have equal length")
    values = np.concatenate([realized, forwards])
    if values.size == 0 or np.any(~np.isfinite(values)) or np.any(values <= 0):
        raise ValueError("fixing levels must be finite and positive")
    if sigma <= 0 or not np.isfinite(sigma) or n_paths < 2:
        raise ValueError("sigma must be positive and n_paths at least two")
    if np.any(times < 0) or np.any(np.diff(times) < 0):
        raise ValueError("fixing_times must be non-negative and sorted")

    rng = np.random.default_rng(seed)
    n_future = len(forwards)
    if n_future:
        dt = np.diff(np.concatenate([[0.0], times]))
        if antithetic:
            half = (n_paths + 1) // 2
            z_half = rng.standard_normal((half, n_future))
            z = np.concatenate([z_half, -z_half], axis=0)[:n_paths]
        else:
            z = rng.standard_normal((n_paths, n_future))
        w = np.cumsum(np.sqrt(dt) * z, axis=1)
        future_values = forwards[None, :] * np.exp(
            -0.5 * sigma**2 * times[None, :] + sigma * w
        )
        future_sum = future_values.sum(axis=1)
    else:
        future_sum = np.zeros(n_paths)
    average = (float(realized.sum()) + future_sum) / (len(realized) + n_future)
    return average, len(realized), n_future


def wti_average_price_option_mc(
    *,
    realized_fixings: np.ndarray,
    forward_fixings: np.ndarray,
    fixing_times: np.ndarray,
    strike: float,
    sigma: float,
    rate: float | None,
    time_to_expiry: float,
    discount_factor: float | None = None,
    option_type: str = "call",
    n_paths: int = 100_000,
    seed: int | None = None,
    antithetic: bool = True,
) -> APOMonteCarloEstimate:
    """Price a first-nearby WTI arithmetic-average call or put under Q.

    For remaining fixing date j the transparent one-factor baseline is

        F_j(t_j) = F_j(0) exp(-0.5 sigma^2 t_j + sigma W^Q_{t_j}).

    Every F_j is a Q-martingale.  The observed WTI term structure and roll
    mapping enter through the vector F_j(0).  ``discount_factor`` can be passed
    directly for a date-specific rate curve; otherwise ``exp(-rate*T)`` is used.
    """
    if strike < 0 or not np.isfinite(strike):
        raise ValueError("strike must be finite and non-negative")
    kind = option_type.lower()
    if kind not in {"call", "put"}:
        raise ValueError("option_type must be 'call' or 'put'")
    discount = _resolve_discount_factor(
        rate=rate,
        time_to_expiry=time_to_expiry,
        discount_factor=discount_factor,
    )
    average, n_realized, n_future = _simulate_average(
        realized_fixings=realized_fixings,
        forward_fixings=forward_fixings,
        fixing_times=fixing_times,
        sigma=sigma,
        n_paths=n_paths,
        seed=seed,
        antithetic=antithetic,
    )
    payoff = (
        np.maximum(average - strike, 0.0)
        if kind == "call"
        else np.maximum(strike - average, 0.0)
    )
    discounted = discount * payoff
    return APOMonteCarloEstimate(
        price=float(discounted.mean()),
        standard_error=float(discounted.std(ddof=1) / np.sqrt(n_paths)),
        expected_average=expected_average_level(realized_fixings, forward_fixings),
        n_paths=n_paths,
        n_realized_fixings=n_realized,
        n_future_fixings=n_future,
    )


def wti_apo_cross_section_mc(
    *,
    realized_fixings: np.ndarray,
    forward_fixings: np.ndarray,
    fixing_times: np.ndarray,
    strikes: np.ndarray,
    option_types: Iterable[str],
    sigma: float,
    rate: float | None,
    time_to_expiry: float,
    discount_factor: float | None = None,
    n_paths: int = 100_000,
    seed: int | None = None,
    antithetic: bool = True,
) -> APOCrossSectionEstimate:
    """Price a call/put cross-section with one shared set of simulated averages.

    This is substantially faster than simulating independent paths for every
    strike.  It also enforces common random numbers across contracts that share
    the same expiry/fixing state.
    """
    strike_array = np.asarray(strikes, dtype=float)
    if strike_array.ndim != 1 or strike_array.size == 0:
        raise ValueError("strikes must be a non-empty one-dimensional array")
    if np.any(~np.isfinite(strike_array)) or np.any(strike_array < 0):
        raise ValueError("strikes must be finite and non-negative")
    kinds = [str(x).lower() for x in option_types]
    if len(kinds) != len(strike_array):
        raise ValueError("option_types and strikes must have equal length")
    if any(kind not in {"call", "put"} for kind in kinds):
        raise ValueError("option_types must contain only 'call' or 'put'")

    discount = _resolve_discount_factor(
        rate=rate,
        time_to_expiry=time_to_expiry,
        discount_factor=discount_factor,
    )
    average, n_realized, n_future = _simulate_average(
        realized_fixings=realized_fixings,
        forward_fixings=forward_fixings,
        fixing_times=fixing_times,
        sigma=sigma,
        n_paths=n_paths,
        seed=seed,
        antithetic=antithetic,
    )

    prices = np.empty(len(strike_array))
    ses = np.empty(len(strike_array))
    for i, (strike, kind) in enumerate(zip(strike_array, kinds)):
        payoff = (
            np.maximum(average - strike, 0.0)
            if kind == "call"
            else np.maximum(strike - average, 0.0)
        )
        discounted = discount * payoff
        prices[i] = discounted.mean()
        ses[i] = discounted.std(ddof=1) / np.sqrt(n_paths)

    return APOCrossSectionEstimate(
        prices=prices,
        standard_errors=ses,
        expected_average=expected_average_level(realized_fixings, forward_fixings),
        n_paths=n_paths,
        n_realized_fixings=n_realized,
        n_future_fixings=n_future,
    )


def posterior_wti_apo_prices(
    sigma_samples: np.ndarray,
    *,
    realized_fixings: np.ndarray,
    forward_fixings: np.ndarray,
    fixing_times: np.ndarray,
    strike: float,
    rate: float | None,
    time_to_expiry: float,
    discount_factor: float | None = None,
    option_type: str = "call",
    n_paths: int = 20_000,
    seed: int = 20260915,
) -> np.ndarray:
    """Push posterior sigma draws through the WTI APO pricer using common random numbers."""
    samples = np.asarray(sigma_samples, dtype=float)
    if (
        samples.ndim != 1
        or samples.size == 0
        or np.any(samples <= 0)
        or np.any(~np.isfinite(samples))
    ):
        raise ValueError("sigma_samples must be a non-empty positive finite 1-D array")
    prices = np.empty(samples.size)
    for i, sigma in enumerate(samples):
        prices[i] = wti_average_price_option_mc(
            realized_fixings=realized_fixings,
            forward_fixings=forward_fixings,
            fixing_times=fixing_times,
            strike=strike,
            sigma=float(sigma),
            rate=rate,
            time_to_expiry=time_to_expiry,
            discount_factor=discount_factor,
            option_type=option_type,
            n_paths=n_paths,
            seed=seed,
            antithetic=True,
        ).price
    return prices
