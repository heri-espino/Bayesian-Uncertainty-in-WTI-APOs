"""Risk-neutral Monte Carlo pricing for WTI Average Price Options.

CME's WTI Average Price Option is based on the arithmetic average of daily
settlement prices of the *first-nearby* WTI (CL) futures contract during the
calendar month. This module therefore prices a vector of future fixing prices
rather than evolving one spot asset or one fixed futures maturity.

The baseline model uses one lognormal risk-neutral factor with constant sigma.
Each future fixing starts from its own current forward/futures level, so the
observed WTI term structure and contract roll enter through ``forward_fixings``.
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


def expected_average_level(
    realized_fixings: np.ndarray,
    forward_fixings: np.ndarray,
) -> float:
    """Risk-neutral expected final arithmetic average at valuation time."""
    realized = np.asarray(realized_fixings, dtype=float)
    forwards = np.asarray(forward_fixings, dtype=float)
    all_values = np.concatenate([realized, forwards])
    if all_values.size == 0:
        raise ValueError("At least one realized or future fixing is required")
    if np.any(~np.isfinite(all_values)) or np.any(all_values <= 0):
        raise ValueError("Fixing and forward levels must be finite and positive")
    return float(np.mean(all_values))


def _validate_inputs(
    realized_fixings: np.ndarray,
    forward_fixings: np.ndarray,
    fixing_times: np.ndarray,
    strike: float,
    sigma: float,
    rate: float,
    time_to_expiry: float,
    n_paths: int,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    realized = np.asarray(realized_fixings, dtype=float)
    forwards = np.asarray(forward_fixings, dtype=float)
    times = np.asarray(fixing_times, dtype=float)

    if realized.ndim != 1 or forwards.ndim != 1 or times.ndim != 1:
        raise ValueError("realized_fixings, forward_fixings and fixing_times must be 1-D")
    if forwards.size != times.size:
        raise ValueError("forward_fixings and fixing_times must have equal length")
    if strike < 0 or sigma <= 0 or time_to_expiry < 0 or n_paths < 2:
        raise ValueError("Invalid strike, sigma, time_to_expiry or n_paths")
    if np.any(times < 0) or np.any(np.diff(times) < 0):
        raise ValueError("fixing_times must be non-negative and sorted")
    values = np.concatenate([realized, forwards])
    if values.size == 0 or np.any(~np.isfinite(values)) or np.any(values <= 0):
        raise ValueError("Fixing and forward levels must be finite and positive")
    if not np.all(np.isfinite([strike, sigma, rate, time_to_expiry])):
        raise ValueError("Model parameters must be finite")
    return realized, forwards, times


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
    """Price a CME-style WTI Average Price call or put under Q.

    Parameters
    ----------
    realized_fixings:
        Daily first-nearby settlements already fixed in the averaging month.
    forward_fixings:
        Current futures/forward levels assigned to each remaining daily fixing
        after mapping that date to the first-nearby CL contract.
    fixing_times:
        Year fractions from valuation date to each future fixing date, sorted.
    sigma:
        Annualized volatility of the one-factor lognormal baseline.

    Notes
    -----
    For future fixing j, the model is

        F_j(t_j) = F_j(0) exp(-0.5 sigma^2 t_j + sigma W_{t_j}^Q),

    with the same Brownian factor across fixing dates. Thus each futures price
    is a Q-martingale while the observed term structure enters through F_j(0).
    """
    realized, forwards, times = _validate_inputs(
        realized_fixings,
        forward_fixings,
        fixing_times,
        strike,
        sigma,
        rate,
        time_to_expiry,
        n_paths,
    )
    kind = option_type.lower()
    if kind not in {"call", "put"}:
        raise ValueError("option_type must be 'call' or 'put'")

    rng = np.random.default_rng(seed)
    n_future = forwards.size

    if n_future:
        dt = np.diff(np.concatenate([[0.0], times]))
        if antithetic:
            half = (n_paths + 1) // 2
            z_half = rng.standard_normal((half, n_future))
            z = np.concatenate([z_half, -z_half], axis=0)[:n_paths]
        else:
            z = rng.standard_normal((n_paths, n_future))

        dW = np.sqrt(dt) * z
        W = np.cumsum(dW, axis=1)
        simulated = forwards[None, :] * np.exp(
            -0.5 * sigma**2 * times[None, :] + sigma * W
        )
        future_sum = simulated.sum(axis=1)
    else:
        future_sum = np.zeros(n_paths)

    realized_sum = float(realized.sum())
    n_total = realized.size + n_future
    average = (realized_sum + future_sum) / n_total

    if kind == "call":
        payoff = np.maximum(average - strike, 0.0)
    else:
        payoff = np.maximum(strike - average, 0.0)

    discounted = np.exp(-rate * time_to_expiry) * payoff
    return APOMonteCarloEstimate(
        price=float(np.mean(discounted)),
        standard_error=float(np.std(discounted, ddof=1) / np.sqrt(n_paths)),
        expected_average=expected_average_level(realized, forwards),
        n_paths=n_paths,
        n_realized_fixings=realized.size,
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
    seed: int = 20260910,
) -> np.ndarray:
    """Push posterior sigma draws through the CME-style APO pricer.

    The pseudo-random seed is reset for each sigma draw, implementing common
    random numbers so estimator differences are not dominated by MC noise.
    """
    samples = np.asarray(sigma_samples, dtype=float)
    if samples.ndim != 1 or samples.size == 0:
        raise ValueError("sigma_samples must be a non-empty 1-D array")
    if np.any(~np.isfinite(samples)) or np.any(samples <= 0):
        raise ValueError("sigma_samples must be finite and positive")

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
