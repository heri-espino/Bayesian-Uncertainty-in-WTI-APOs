"""Reusable synthetic/theoretical validation utilities for the Asian-option study.

The functions in this module are intentionally deterministic when a seed is supplied.
They provide low-level checks used by ``experiments/synthetic_validation.py`` and by
unit tests. Historical data are generated under the physical measure P, whereas all
pricing checks are performed under the risk-neutral measure Q.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import sqrt

import numpy as np

from bayesian_asian_options.asian_pricing import asian_arithmetic_call_mc, discrete_geometric_asian_call_price


@dataclass(frozen=True)
class ScalarMonteCarloCheck:
    """A scalar Monte Carlo estimate compared with a known target."""

    estimate: float
    target: float
    standard_error: float

    @property
    def error(self) -> float:
        return self.estimate - self.target

    @property
    def z_score(self) -> float:
        if self.standard_error == 0.0:
            return 0.0 if self.error == 0.0 else float("inf")
        return self.error / self.standard_error


def deterministic_arithmetic_asian_call_price(
    S0: float,
    K: float,
    r: float,
    T: float,
    *,
    q: float = 0.0,
    n_steps: int = 252,
) -> float:
    """Exact arithmetic-Asian call price in the deterministic sigma=0 limit.

    Monitoring times are ``t_j = j*T/n_steps`` for ``j=1,...,n_steps``.
    Under Q and sigma=0, ``S_t = S0 * exp((r-q)t)`` deterministically.
    """
    if S0 <= 0.0:
        raise ValueError("S0 must be positive")
    if K < 0.0:
        raise ValueError("K must be non-negative")
    if T <= 0.0:
        raise ValueError("T must be positive")
    if n_steps < 1:
        raise ValueError("n_steps must be at least one")
    if not np.all(np.isfinite([S0, K, r, T, q])):
        raise ValueError("model inputs must be finite")

    times = T * np.arange(1, n_steps + 1, dtype=float) / n_steps
    deterministic_path = S0 * np.exp((r - q) * times)
    arithmetic_average = float(np.mean(deterministic_path))
    return float(np.exp(-r * T) * max(arithmetic_average - K, 0.0))


def geometric_asian_call_mc(
    S0: float,
    K: float,
    r: float,
    sigma: float,
    T: float,
    *,
    q: float = 0.0,
    n_steps: int = 252,
    n_paths: int = 50_000,
    seed: int = 12345,
    antithetic: bool = True,
) -> ScalarMonteCarloCheck:
    """Simulate a geometric Asian call and compare it with its closed form.

    This provides an independent stochastic check of the path generator and of the
    discrete geometric-Asian formula used as a control variate by the arithmetic
    pricer.
    """
    if sigma <= 0.0:
        raise ValueError("sigma must be positive")
    if n_paths < 2:
        raise ValueError("n_paths must be at least two")

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
    geometric_average = np.exp(np.mean(log_paths, axis=1))
    discounted_payoff = np.exp(-r * T) * np.maximum(geometric_average - K, 0.0)

    estimate = float(np.mean(discounted_payoff))
    standard_error = float(np.std(discounted_payoff, ddof=1) / np.sqrt(n_paths))
    target = discrete_geometric_asian_call_price(
        S0,
        K,
        r,
        sigma,
        T,
        q=q,
        n_steps=n_steps,
    )
    return ScalarMonteCarloCheck(estimate, target, standard_error)


def risk_neutral_martingale_check(
    S0: float,
    r: float,
    sigma: float,
    T: float,
    *,
    q: float = 0.0,
    n_paths: int = 100_000,
    seed: int = 12345,
    antithetic: bool = True,
) -> ScalarMonteCarloCheck:
    """Check E_Q[e^{-(r-q)T} S_T] = S0 by Monte Carlo."""
    if S0 <= 0.0 or sigma <= 0.0 or T <= 0.0:
        raise ValueError("S0, sigma and T must be positive")
    if n_paths < 2:
        raise ValueError("n_paths must be at least two")

    rng = np.random.default_rng(seed)
    if antithetic:
        half = (n_paths + 1) // 2
        z_half = rng.standard_normal(half)
        z = np.concatenate((z_half, -z_half))[:n_paths]
    else:
        z = rng.standard_normal(n_paths)

    terminal = S0 * np.exp(
        (r - q - 0.5 * sigma**2) * T + sigma * sqrt(T) * z
    )
    transformed = np.exp(-(r - q) * T) * terminal
    estimate = float(np.mean(transformed))
    standard_error = float(np.std(transformed, ddof=1) / np.sqrt(n_paths))
    return ScalarMonteCarloCheck(estimate, S0, standard_error)


def zero_volatility_limit_check(
    S0: float,
    K: float,
    r: float,
    T: float,
    *,
    q: float = 0.0,
    n_steps: int = 252,
    n_paths: int = 20_000,
    sigma_epsilon: float = 1.0e-4,
    seed: int = 12345,
) -> ScalarMonteCarloCheck:
    """Compare a tiny-volatility MC price with the exact sigma=0 limit."""
    if sigma_epsilon <= 0.0:
        raise ValueError("sigma_epsilon must be positive")

    estimate = asian_arithmetic_call_mc(
        S0,
        K,
        r,
        sigma_epsilon,
        T,
        q=q,
        n_steps=n_steps,
        n_paths=n_paths,
        seed=seed,
        antithetic=True,
        geometric_control=False,
    )
    target = deterministic_arithmetic_asian_call_price(
        S0,
        K,
        r,
        T,
        q=q,
        n_steps=n_steps,
    )
    return ScalarMonteCarloCheck(
        estimate=estimate.raw_price,
        target=target,
        standard_error=estimate.raw_standard_error,
    )


def arithmetic_price_curve_by_strike(
    strikes: tuple[float, ...] | list[float] | np.ndarray,
    *,
    S0: float,
    r: float,
    sigma: float,
    T: float,
    q: float = 0.0,
    n_steps: int = 252,
    n_paths: int = 30_000,
    seed: int = 12345,
) -> np.ndarray:
    """Return common-random-number arithmetic prices over a strike grid."""
    strike_array = np.asarray(strikes, dtype=float)
    if strike_array.ndim != 1 or strike_array.size < 2:
        raise ValueError("strikes must contain at least two values")
    if np.any(strike_array < 0.0) or np.any(np.diff(strike_array) <= 0.0):
        raise ValueError("strikes must be non-negative and strictly increasing")

    return np.asarray(
        [
            asian_arithmetic_call_mc(
                S0,
                float(K),
                r,
                sigma,
                T,
                q=q,
                n_steps=n_steps,
                n_paths=n_paths,
                seed=seed,
                antithetic=True,
                geometric_control=False,
            ).raw_price
            for K in strike_array
        ],
        dtype=float,
    )


def arithmetic_price_curve_by_volatility(
    volatilities: tuple[float, ...] | list[float] | np.ndarray,
    *,
    S0: float,
    K: float,
    r: float,
    T: float,
    q: float = 0.0,
    n_steps: int = 252,
    n_paths: int = 30_000,
    seed: int = 12345,
) -> np.ndarray:
    """Return common-random-number arithmetic prices over a volatility grid."""
    sigma_array = np.asarray(volatilities, dtype=float)
    if sigma_array.ndim != 1 or sigma_array.size < 2:
        raise ValueError("volatilities must contain at least two values")
    if np.any(sigma_array <= 0.0) or np.any(np.diff(sigma_array) <= 0.0):
        raise ValueError("volatilities must be positive and strictly increasing")

    return np.asarray(
        [
            asian_arithmetic_call_mc(
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
            for sigma in sigma_array
        ],
        dtype=float,
    )
