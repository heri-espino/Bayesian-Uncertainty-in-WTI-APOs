"""Strictly lagged Bayesian AAO market-IV innovations.

For a fixed AAO expiry, consecutive business-day changes in log near-ATM
option-implied volatility are modeled as conditionally normal, with a
normal-inverse-gamma prior for their drift and variance. The next log-IV
state follows a Student-t posterior predictive distribution centered on
the latest *strictly earlier* AAO market IV.

This is NOT structural first-nearby CL volatility. The Student-t
predictive distribution has no finite untruncated exponential moment.
Sigma is therefore explicitly clipped to [0.005, 3.0] before computing
the Monte Carlo plug-in mean and Bayesian-integrated Black option prices.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

import numpy as np
import pandas as pd

SIGMA_MIN = 0.005
SIGMA_MAX = 3.0


@dataclass(frozen=True)
class IVForecast:
    sigma_draws: np.ndarray
    sigma_mean: float
    sigma_median: float
    sigma_sd: float
    lagged_sigma: float
    age_business_days: int
    n_changes: int
    n_clipped: int
    posterior_drift: float
    posterior_shape: float
    posterior_scale: float
    latest_iv_date: str


def _business_days(d0: str, d1: str) -> int:
    """Business-weekday approximation; exchange holidays are not excluded."""
    a = np.datetime64(d0, "D")
    b = np.datetime64(d1, "D")
    if b <= a:
        return 0
    return max(1, int(np.busday_count(a, b)))


def predict_market_iv(
    history: Sequence[tuple[str, float, float]],
    *,
    asof: str,
    seed: int,
    n_draws: int = 256,
    min_changes: int = 8,
    max_changes: int = 63,
    max_gap_days: int = 10,
    kappa0: float = 10.0,
    alpha0: float = 3.0,
    beta0: float = 0.002,
) -> IVForecast | None:
    """Use previous-date same-expiry IVs; refuse current or future history.

    History consists of (observation_date, parity_forward, near_ATM_IV)
    constructed only after the previous observation date is processed.
    Only single-weekday transitions inform the one-step innovation law.
    Latest market IV must be at most max_gap_days calendar days old.
    Multi-day extrapolation scales innovation variance with the weekday
    horizon and parameter-uncertainty variance with horizon squared.
    """
    if (n_draws < 32 or min_changes < 2 or max_changes < min_changes
        or max_gap_days < 1 or kappa0 <= 0 or alpha0 <= 1 or beta0 <= 0):
        raise ValueError("Invalid Bayesian market-IV hyperparameters")
    if not history:
        return None
    if any(pd.Timestamp(d) >= pd.Timestamp(asof) for d, _, _ in history):
        raise ValueError("IV forecast received current/future-date history")
    ordered = sorted(history, key=lambda x: x[0])
    valid = [(str(d), float(s)) for d, _, s in ordered
             if np.isfinite(s) and SIGMA_MIN < s < SIGMA_MAX]
    if not valid:
        return None
    last_date, last_sigma = valid[-1]
    calendar_age = (pd.Timestamp(asof) - pd.Timestamp(last_date)).days
    if calendar_age <= 0 or calendar_age > max_gap_days:
        return None
    innovations = []
    for (d0, s0), (d1, s1) in zip(valid, valid[1:]):
        gap = (pd.Timestamp(d1) - pd.Timestamp(d0)).days
        if 0 < gap <= max_gap_days and _business_days(d0, d1) == 1:
            innovations.append(float(np.log(s1 / s0)))
    if len(innovations) < min_changes:
        return None
    x = np.asarray(innovations[-max_changes:], dtype=float)
    n = len(x)
    xbar = float(x.mean())
    kappa_n = kappa0 + n
    mu_n = n * xbar / kappa_n  # Predeclared prior drift zero.
    alpha_n = alpha0 + 0.5*n
    beta_n = (beta0 + .5*float(np.sum((x - xbar)**2))
              + .5*kappa0*n/kappa_n*xbar*xbar)
    horizon = _business_days(last_date, asof)
    # Normal-inverse-gamma posterior predictive for a horizon-step
    # sum: Student-t(df=2*alpha_n), location=h*mu_n,
    # scale^2=(beta_n/alpha_n)*(h+h^2/kappa_n).
    location = np.log(last_sigma) + horizon*mu_n
    scale = np.sqrt(beta_n/alpha_n * (horizon + horizon*horizon/kappa_n))
    rng = np.random.default_rng(seed)
    log_draws = location + scale*rng.standard_t(df=2*alpha_n, size=n_draws)
    clipped = np.clip(log_draws, np.log(SIGMA_MIN), np.log(SIGMA_MAX))
    draws = np.exp(clipped)
    return IVForecast(
        sigma_draws=draws,
        sigma_mean=float(draws.mean()),
        sigma_median=float(np.exp(np.clip(location, np.log(SIGMA_MIN),
                                          np.log(SIGMA_MAX)))),
        sigma_sd=float(draws.std(ddof=1)),
        lagged_sigma=last_sigma,
        age_business_days=horizon,
        n_changes=n,
        n_clipped=int(np.count_nonzero(clipped != log_draws)),
        posterior_drift=mu_n,
        posterior_shape=alpha_n,
        posterior_scale=beta_n,
        latest_iv_date=last_date,
    )
