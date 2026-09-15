"""Risk-neutral Monte Carlo utilities for arithmetic Asian call options.

The physical drift ``mu`` is intentionally absent from this module. Under the
Black-Scholes complete-market model, contingent claims are priced under the
risk-neutral measure Q, so the stock drift used by the pricing simulation is
``r - q``.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import erf, sqrt

import numpy as np


@dataclass(frozen=True)
class MonteCarloEstimate:
    """Monte Carlo price estimate and diagnostics."""

    price: float
    standard_error: float
    raw_price: float
    raw_standard_error: float
    control_beta: float
    n_paths: int


def _norm_cdf(x: float) -> float:
    return 0.5 * (1.0 + erf(x / sqrt(2.0)))


def _validate_inputs(
    S0: float,
    K: float,
    r: float,
    sigma: float,
    T: float,
    q: float,
    n_steps: int,
    n_paths: int,
) -> None:
    if S0 <= 0:
        raise ValueError("S0 must be positive.")
    if K < 0:
        raise ValueError("K must be non-negative.")
    if sigma <= 0:
        raise ValueError("sigma must be positive.")
    if T <= 0:
        raise ValueError("T must be positive.")
    if n_steps < 1:
        raise ValueError("n_steps must be at least 1.")
    if n_paths < 2:
        raise ValueError("n_paths must be at least 2.")
    if not np.all(np.isfinite([S0, K, r, sigma, T, q])):
        raise ValueError("Model inputs must be finite.")


def discrete_geometric_asian_call_price(
    S0: float,
    K: float,
    r: float,
    sigma: float,
    T: float,
    *,
    q: float = 0.0,
    n_steps: int = 252,
) -> float:
    """Closed-form price of a discretely monitored geometric Asian call.

    Monitoring times are ``t_i = i*T/n_steps``, for ``i=1,...,n_steps``.
    Under Q,

        dS_t = (r-q) S_t dt + sigma S_t dW_t^Q.

    The log of the discrete geometric average is Gaussian, which gives the
    closed-form expectation used here and later as a control variate.
    """
    _validate_inputs(S0, K, r, sigma, T, q, n_steps, 2)

    n = float(n_steps)
    mean_time = T * (n + 1.0) / (2.0 * n)
    log_mean = np.log(S0) + (r - q - 0.5 * sigma**2) * mean_time
    log_var = sigma**2 * T * (n + 1.0) * (2.0 * n + 1.0) / (6.0 * n**2)

    if K == 0:
        return float(np.exp(-r * T + log_mean + 0.5 * log_var))

    sqrt_v = np.sqrt(log_var)
    d2 = (log_mean - np.log(K)) / sqrt_v
    d1 = d2 + sqrt_v
    expected_payoff = (
        np.exp(log_mean + 0.5 * log_var) * _norm_cdf(float(d1))
        - K * _norm_cdf(float(d2))
    )
    return float(np.exp(-r * T) * expected_payoff)


def asian_arithmetic_call_mc(
    S0: float,
    K: float,
    r: float,
    sigma: float,
    T: float,
    *,
    q: float = 0.0,
    n_steps: int = 252,
    n_paths: int = 100_000,
    seed: int | None = None,
    antithetic: bool = True,
    geometric_control: bool = True,
) -> MonteCarloEstimate:
    """Price a discrete arithmetic-average Asian call under Q.

    The physical drift ``mu`` is intentionally not an argument. Black-Scholes
    no-arbitrage pricing uses the risk-neutral drift ``r-q``.
    """
    _validate_inputs(S0, K, r, sigma, T, q, n_steps, n_paths)

    rng = np.random.default_rng(seed)
    dt = T / n_steps

    if antithetic:
        half = (n_paths + 1) // 2
        z_half = rng.standard_normal((half, n_steps))
        z = np.concatenate((z_half, -z_half), axis=0)[:n_paths]
    else:
        z = rng.standard_normal((n_paths, n_steps))

    log_increments = (
        (r - q - 0.5 * sigma**2) * dt
        + sigma * np.sqrt(dt) * z
    )
    log_paths = np.log(S0) + np.cumsum(log_increments, axis=1)
    paths = np.exp(log_paths)

    arithmetic_average = np.mean(paths, axis=1)
    arithmetic_payoff = np.maximum(arithmetic_average - K, 0.0)

    discount = np.exp(-r * T)
    raw_discounted = discount * arithmetic_payoff
    raw_price = float(np.mean(raw_discounted))
    raw_se = float(np.std(raw_discounted, ddof=1) / np.sqrt(n_paths))

    beta = 0.0
    adjusted_discounted = raw_discounted

    if geometric_control:
        geometric_average = np.exp(np.mean(log_paths, axis=1))
        geometric_payoff = np.maximum(geometric_average - K, 0.0)
        geometric_discounted = discount * geometric_payoff
        control_mean = discrete_geometric_asian_call_price(
            S0,
            K,
            r,
            sigma,
            T,
            q=q,
            n_steps=n_steps,
        )
        control_var = np.var(geometric_discounted, ddof=1)
        if control_var > 0:
            beta = float(
                np.cov(raw_discounted, geometric_discounted, ddof=1)[0, 1]
                / control_var
            )
            adjusted_discounted = (
                raw_discounted
                - beta * (geometric_discounted - control_mean)
            )

    price = float(np.mean(adjusted_discounted))
    standard_error = float(
        np.std(adjusted_discounted, ddof=1) / np.sqrt(n_paths)
    )

    return MonteCarloEstimate(
        price=price,
        standard_error=standard_error,
        raw_price=raw_price,
        raw_standard_error=raw_se,
        control_beta=beta,
        n_paths=n_paths,
    )


def posterior_price_samples(
    sigma_samples: np.ndarray,
    *,
    S0: float,
    K: float,
    r: float,
    T: float,
    q: float = 0.0,
    n_steps: int = 252,
    n_paths: int = 20_000,
    seed: int = 12345,
) -> np.ndarray:
    """Push posterior draws of sigma into risk-neutral Asian option prices.

    The same pseudo-random seed is reset for every draw. This common-random-
    numbers design reduces Monte Carlo noise when comparing prices across
    different posterior values of ``sigma``.
    """
    sigma_samples = np.asarray(sigma_samples, dtype=float)
    if sigma_samples.ndim != 1:
        raise ValueError("sigma_samples must be one-dimensional.")
    if sigma_samples.size == 0:
        raise ValueError("sigma_samples cannot be empty.")
    if np.any(~np.isfinite(sigma_samples)) or np.any(sigma_samples <= 0):
        raise ValueError("sigma_samples must contain finite positive values.")

    prices = np.empty(sigma_samples.size, dtype=float)
    for i, sigma in enumerate(sigma_samples):
        prices[i] = asian_arithmetic_call_mc(
            S0,
            K,
            r,
            float(sigma),
            T,
            q=q,
            n_steps=n_steps,
            n_paths=n_paths,
            seed=seed,
            antithetic=True,
            geometric_control=True,
        ).price
    return prices
