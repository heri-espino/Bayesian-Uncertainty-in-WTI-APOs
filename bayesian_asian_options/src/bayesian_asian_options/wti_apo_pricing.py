"""Risk-neutral Monte Carlo baseline for CME WTI Average Price Options.

CME WTI APOs average daily settlements of the *first-nearby* CL futures
contract during the calendar month.  This module therefore takes a vector of
current forward/futures levels for the remaining fixing dates, rather than one
spot price or one fixed futures maturity.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class APOMonteCarloEstimate:
    price: float
    standard_error: float
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


def wti_average_price_option_mc(
    *,
    realized_fixings: np.ndarray,
    forward_fixings: np.ndarray,
    fixing_times: np.ndarray,
    strike: float,
    sigma: float,
    rate: float,
    time_to_expiry: float,
    option_type: str = "call",
    n_paths: int = 100_000,
    seed: int | None = None,
    antithetic: bool = True,
) -> APOMonteCarloEstimate:
    """Price a first-nearby WTI arithmetic-average call or put under Q.

    For remaining fixing date j the transparent one-factor baseline is

        F_j(t_j) = F_j(0) exp(-0.5 sigma^2 t_j + sigma W^Q_{t_j}).

    Every F_j is a Q-martingale.  The observed WTI term structure and the roll
    mapping enter through the vector F_j(0).  This is a baseline specification,
    not a claim that WTI has one constant-volatility factor in reality.
    """
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
    if strike < 0 or sigma <= 0 or time_to_expiry < 0 or n_paths < 2:
        raise ValueError("invalid strike, sigma, time_to_expiry or n_paths")
    if np.any(times < 0) or np.any(np.diff(times) < 0):
        raise ValueError("fixing_times must be non-negative and sorted")
    if not np.all(np.isfinite([strike, sigma, rate, time_to_expiry])):
        raise ValueError("model parameters must be finite")
    kind = option_type.lower()
    if kind not in {"call", "put"}:
        raise ValueError("option_type must be 'call' or 'put'")

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
    payoff = np.maximum(average - strike, 0.0) if kind == "call" else np.maximum(strike - average, 0.0)
    discounted = np.exp(-rate * time_to_expiry) * payoff
    return APOMonteCarloEstimate(
        price=float(discounted.mean()),
        standard_error=float(discounted.std(ddof=1) / np.sqrt(n_paths)),
        expected_average=expected_average_level(realized, forwards),
        n_paths=n_paths,
        n_realized_fixings=len(realized),
        n_future_fixings=n_future,
    )


def posterior_wti_apo_prices(
    sigma_samples: np.ndarray,
    *,
    realized_fixings: np.ndarray,
    forward_fixings: np.ndarray,
    fixing_times: np.ndarray,
    strike: float,
    rate: float,
    time_to_expiry: float,
    option_type: str = "call",
    n_paths: int = 20_000,
    seed: int = 20260915,
) -> np.ndarray:
    """Push posterior sigma draws through the WTI APO pricer using common random numbers."""
    samples = np.asarray(sigma_samples, dtype=float)
    if samples.ndim != 1 or samples.size == 0 or np.any(samples <= 0) or np.any(~np.isfinite(samples)):
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
            option_type=option_type,
            n_paths=n_paths,
            seed=seed,
            antithetic=True,
        ).price
    return prices
