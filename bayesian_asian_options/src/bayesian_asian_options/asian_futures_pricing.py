"""Asian-option pricing for lognormal futures processes under Q.

With deterministic interest rates, a futures price is modeled here as

    dF_t = sigma F_t dW_t^Q,

so its risk-neutral drift is zero.  The module provides both Monte Carlo wrappers and a
Curran-style geometric-conditioning approximation for an arithmetic average.  The latter is
useful as an independent, fast benchmark for the WTI Average Price Option study.
"""

from __future__ import annotations

import numpy as np
from scipy.optimize import brentq
from scipy.special import ndtr

from bayesian_asian_options.accelerated_pricing import (
    AcceleratedMonteCarloEstimate,
    asian_arithmetic_call_mc_chunked,
)
from bayesian_asian_options.asian_pricing import MonteCarloEstimate, asian_arithmetic_call_mc


def asian_futures_arithmetic_call_mc(
    F0: float,
    K: float,
    r: float,
    sigma: float,
    T: float,
    *,
    n_steps: int = 252,
    n_paths: int = 100_000,
    seed: int | None = None,
) -> MonteCarloEstimate:
    """Price an arithmetic Asian call on a lognormal futures-price process."""
    return asian_arithmetic_call_mc(
        F0,
        K,
        r,
        sigma,
        T,
        q=r,
        n_steps=n_steps,
        n_paths=n_paths,
        seed=seed,
        antithetic=True,
        geometric_control=True,
    )


def asian_futures_arithmetic_call_mc_chunked(
    F0: float,
    K: float,
    r: float,
    sigma: float,
    T: float,
    *,
    n_steps: int = 252,
    n_paths: int = 1_000_000,
    seed: int = 12345,
    backend: str = "auto",
    chunk_size: int = 100_000,
) -> AcceleratedMonteCarloEstimate:
    """CPU/GPU chunked version of the lognormal-futures Asian pricer."""
    return asian_arithmetic_call_mc_chunked(
        F0,
        K,
        r,
        sigma,
        T,
        q=r,
        n_steps=n_steps,
        n_paths=n_paths,
        seed=seed,
        backend=backend,
        chunk_size=chunk_size,
        antithetic=True,
        geometric_control=True,
    )


def curran_arithmetic_futures_option(
    *,
    realized_fixings: np.ndarray,
    forward_fixings: np.ndarray,
    fixing_times: np.ndarray,
    strike: float,
    sigma: float,
    discount_factor: float,
    option_type: str = "call",
) -> float:
    """Approximate an arithmetic-average futures option by Curran conditioning.

    The stochastic remaining fixings satisfy

    .. math::

       F_i(t_i)=F_i(0)\exp\{-\tfrac12\sigma^2 t_i+\sigma W_{t_i}\},

    with one common Brownian factor and covariance
    :math:`\operatorname{Cov}(\log F_i,\log F_j)=\sigma^2\min(t_i,t_j)`.
    The function conditions the arithmetic mean of the remaining fixings on their
    geometric mean and replaces the conditional option payoff by the positive part of the
    conditional arithmetic mean, following Curran (1994).

    Already realized fixings are handled exactly.  If ``R`` is their sum, ``M`` is the
    total number of fixings and ``n`` fixings remain, then

    .. math::

       (A_T-K)^+ = \frac{n}{M}(A_f-K_f)^+,
       \qquad K_f=\frac{MK-R}{n}.

    Calls and puts are returned on the same discounted payoff scale as the WTI Monte Carlo
    engine. Puts are obtained from arithmetic-average put-call parity.  The function is an
    approximation benchmark, not an assertion that it reproduces any exchange's proprietary
    settlement implementation.

    Parameters
    ----------
    realized_fixings:
        Already observed first-nearby settlements. May be empty.
    forward_fixings:
        Valuation-date futures levels associated with the remaining fixing dates.
    fixing_times:
        Remaining fixing times in years from valuation, sorted increasingly.
    strike:
        Strike of the option on the final arithmetic average.
    sigma:
        Annualized lognormal volatility shared by the remaining futures fixings.
    discount_factor:
        Discount factor from valuation to payoff.
    option_type:
        ``"call"`` or ``"put"``.

    Returns
    -------
    float
        Curran geometric-conditioning approximation on the discounted price scale.
    """
    realized = np.asarray(realized_fixings, dtype=float)
    forwards = np.asarray(forward_fixings, dtype=float)
    times = np.asarray(fixing_times, dtype=float)
    if realized.ndim != 1 or forwards.ndim != 1 or times.ndim != 1:
        raise ValueError("fixing arrays must be one-dimensional")
    if forwards.size != times.size:
        raise ValueError("forward_fixings and fixing_times must have equal length")
    all_levels = np.concatenate([realized, forwards])
    if all_levels.size == 0 or np.any(~np.isfinite(all_levels)) or np.any(all_levels <= 0):
        raise ValueError("fixing levels must be finite and positive")
    if np.any(~np.isfinite(times)) or np.any(times < 0) or np.any(np.diff(times) < 0):
        raise ValueError("fixing_times must be finite, non-negative, and sorted")
    if not np.isfinite(strike) or strike < 0:
        raise ValueError("strike must be finite and non-negative")
    if not np.isfinite(sigma) or sigma < 0:
        raise ValueError("sigma must be finite and non-negative")
    if not np.isfinite(discount_factor) or discount_factor <= 0:
        raise ValueError("discount_factor must be finite and positive")
    kind = str(option_type).lower()
    if kind not in {"call", "put"}:
        raise ValueError("option_type must be 'call' or 'put'")

    total_fixings = int(realized.size + forwards.size)
    expected_average = float(all_levels.mean())

    # Once all fixings are known, or in the deterministic zero-volatility limit, valuation
    # reduces exactly to discounted intrinsic value of the deterministic final average.
    if forwards.size == 0 or sigma == 0 or np.all(times == 0):
        call = discount_factor * max(expected_average - strike, 0.0)
        put = discount_factor * max(strike - expected_average, 0.0)
        return float(call if kind == "call" else put)

    n_future = int(forwards.size)
    effective_strike = (total_fixings * float(strike) - float(realized.sum())) / n_future

    # If realized fixings alone have already guaranteed a positive call payoff, the payoff
    # is linear in the remaining martingale futures and its expectation is exact.
    if effective_strike <= 0:
        call = discount_factor * (expected_average - strike)
    else:
        mu = np.log(forwards) - 0.5 * sigma**2 * times
        variances = sigma**2 * times
        covariance = sigma**2 * np.minimum.outer(times, times)
        mu_g = float(np.mean(mu))
        var_g = float(np.mean(covariance))
        if var_g <= 0:
            call = discount_factor * max(expected_average - strike, 0.0)
        else:
            sd_g = float(np.sqrt(var_g))
            cov_i_g = covariance.mean(axis=1)
            beta = cov_i_g / var_g
            conditional_variance = np.maximum(
                variances - cov_i_g**2 / var_g,
                0.0,
            )

            def conditional_arithmetic_mean(x: float) -> float:
                conditional_levels = np.exp(
                    mu
                    + beta * (x - mu_g)
                    + 0.5 * conditional_variance
                )
                return float(np.mean(conditional_levels))

            def root_function(x: float) -> float:
                return conditional_arithmetic_mean(x) - effective_strike

            # All Brownian covariances are non-negative, hence the conditional arithmetic
            # mean is monotone. Expand a normal-scale bracket defensively for extreme strikes.
            lo = mu_g - 10.0 * sd_g
            hi = mu_g + 10.0 * sd_g
            for _ in range(12):
                if root_function(lo) <= 0 <= root_function(hi):
                    break
                lo -= 5.0 * sd_g
                hi += 5.0 * sd_g
            else:
                raise RuntimeError("failed to bracket Curran exercise boundary")
            x_star = float(brentq(root_function, lo, hi))

            expected_levels = forwards  # Q-martingale means E[F_i(t_i)] = F_i(0).
            d_asset = (mu_g + cov_i_g - x_star) / sd_g
            d_strike = (mu_g - x_star) / sd_g
            future_call = (
                float(np.mean(expected_levels * ndtr(d_asset)))
                - effective_strike * float(ndtr(d_strike))
            )
            call = discount_factor * (n_future / total_fixings) * future_call

    # Arithmetic-average put-call parity under deterministic discounting.
    put = call - discount_factor * (expected_average - strike)
    price = call if kind == "call" else put
    # Numerical root/normal-function noise can produce tiny negative values near zero.
    return float(max(price, 0.0))
