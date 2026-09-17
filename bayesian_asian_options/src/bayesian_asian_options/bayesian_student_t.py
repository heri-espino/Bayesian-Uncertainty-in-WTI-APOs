"""Bayesian Student-t robustness model for physical-measure WTI log returns.

The baseline paper assumes Gaussian GBM returns under P.  This module changes only the
innovation distribution while preserving the same drift/volatility interpretation:

    r_t = (mu - sigma^2 / 2) dt + sigma sqrt(dt) epsilon_t,

where ``epsilon_t`` is a standardized Student-t random variable with unit variance.  If
``z ~ t_nu``, then ``epsilon = z * sqrt((nu-2)/nu)`` for ``nu > 2``.

Sampling uses ``theta = (mu, log_sigma, log(nu-2))``.  The baseline priors on ``mu`` and
``sigma`` are unchanged.  A weak Gaussian prior is placed directly on ``log(nu-2)``.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import lgamma

import numpy as np
from scipy.special import gammaln


@dataclass(frozen=True)
class StudentTMCMCResult:
    mu: np.ndarray
    sigma: np.ndarray
    nu: np.ndarray
    acceptance_rate: float
    burn_in: int
    n_iter: int


def standardized_student_t_log_returns(
    *,
    mu: float,
    sigma: float,
    nu: float,
    dt: float,
    n_obs: int,
    seed: int | None = None,
) -> np.ndarray:
    """Simulate unit-variance Student-t GBM-style log returns under P."""
    if sigma <= 0 or nu <= 2 or dt <= 0 or n_obs < 1:
        raise ValueError("require sigma>0, nu>2, dt>0, n_obs>=1")
    rng = np.random.default_rng(seed)
    eps = rng.standard_t(float(nu), size=int(n_obs)) * np.sqrt((nu - 2.0) / nu)
    return (mu - 0.5 * sigma**2) * dt + sigma * np.sqrt(dt) * eps


def log_posterior_student_t(
    theta: np.ndarray,
    log_returns: np.ndarray,
    dt: float,
    *,
    mu_prior_sd: float = 1.0,
    sigma_prior_alpha: float = 2.0,
    sigma_prior_beta: float = 0.1,
    log_nu_minus_two_prior_mean: float = np.log(8.0),
    log_nu_minus_two_prior_sd: float = 1.0,
) -> float:
    """Unnormalized posterior for ``(mu, log_sigma, log(nu-2))``."""
    theta = np.asarray(theta, dtype=float)
    returns = np.asarray(log_returns, dtype=float)
    if theta.shape != (3,):
        raise ValueError("theta must contain (mu, log_sigma, log_nu_minus_two)")
    if returns.ndim != 1 or returns.size == 0:
        raise ValueError("log_returns must be a non-empty one-dimensional array")
    if dt <= 0:
        raise ValueError("dt must be positive")
    if (
        mu_prior_sd <= 0
        or sigma_prior_alpha <= 0
        or sigma_prior_beta <= 0
        or log_nu_minus_two_prior_sd <= 0
    ):
        raise ValueError("prior scales and inverse-gamma hyperparameters must be positive")

    mu, eta, xi = theta
    sigma = float(np.exp(eta))
    nu_minus_two = float(np.exp(xi))
    nu = 2.0 + nu_minus_two
    if not np.isfinite(sigma) or not np.isfinite(nu) or sigma <= 0 or nu <= 2:
        return -np.inf

    mean = (mu - 0.5 * sigma**2) * dt
    # Standardized t has variance one.  scipy's/standard t scale is therefore reduced by
    # sqrt((nu-2)/nu) before multiplication by sigma sqrt(dt).
    scale = sigma * np.sqrt(dt) * np.sqrt((nu - 2.0) / nu)
    residual = (returns - mean) / scale
    n = returns.size
    log_lik = n * (
        gammaln((nu + 1.0) / 2.0)
        - gammaln(nu / 2.0)
        - 0.5 * np.log(nu * np.pi)
        - np.log(scale)
    )
    log_lik -= 0.5 * (nu + 1.0) * np.sum(np.log1p((residual**2) / nu))

    log_prior_mu = -np.log(mu_prior_sd) - 0.5 * (mu / mu_prior_sd) ** 2
    alpha = float(sigma_prior_alpha)
    beta = float(sigma_prior_beta)
    log_prior_sigma = (
        alpha * np.log(beta)
        - lgamma(alpha)
        - (alpha + 1.0) * eta
        - beta / sigma
    )
    # Sampling in log sigma requires p(eta)=p(sigma)*sigma.
    log_jacobian_sigma = eta

    z = (xi - float(log_nu_minus_two_prior_mean)) / float(log_nu_minus_two_prior_sd)
    log_prior_xi = -np.log(float(log_nu_minus_two_prior_sd)) - 0.5 * z**2

    return float(log_lik + log_prior_mu + log_prior_sigma + log_jacobian_sigma + log_prior_xi)


def random_walk_metropolis_student_t(
    log_returns: np.ndarray,
    dt: float,
    *,
    n_iter: int = 30_000,
    burn_in: int = 6_000,
    theta_init: tuple[float, float, float] = (0.05, np.log(0.25), np.log(8.0)),
    proposal_sd: tuple[float, float, float] = (0.25, 0.06, 0.12),
    mu_prior_sd: float = 1.0,
    sigma_prior_alpha: float = 2.0,
    sigma_prior_beta: float = 0.1,
    log_nu_minus_two_prior_mean: float = np.log(8.0),
    log_nu_minus_two_prior_sd: float = 1.0,
    seed: int | None = None,
) -> StudentTMCMCResult:
    """Random-walk Metropolis for the standardized Student-t return model."""
    if n_iter < 2 or burn_in < 0 or burn_in >= n_iter:
        raise ValueError("invalid n_iter/burn_in")
    proposal = np.asarray(proposal_sd, dtype=float)
    if proposal.shape != (3,) or np.any(proposal <= 0):
        raise ValueError("proposal_sd must contain three positive values")

    rng = np.random.default_rng(seed)
    chain = np.empty((n_iter, 3), dtype=float)
    chain[0] = np.asarray(theta_init, dtype=float)
    current = log_posterior_student_t(
        chain[0],
        log_returns,
        dt,
        mu_prior_sd=mu_prior_sd,
        sigma_prior_alpha=sigma_prior_alpha,
        sigma_prior_beta=sigma_prior_beta,
        log_nu_minus_two_prior_mean=log_nu_minus_two_prior_mean,
        log_nu_minus_two_prior_sd=log_nu_minus_two_prior_sd,
    )
    accepted = 0
    for i in range(1, n_iter):
        candidate = chain[i - 1] + rng.normal(0.0, proposal, size=3)
        value = log_posterior_student_t(
            candidate,
            log_returns,
            dt,
            mu_prior_sd=mu_prior_sd,
            sigma_prior_alpha=sigma_prior_alpha,
            sigma_prior_beta=sigma_prior_beta,
            log_nu_minus_two_prior_mean=log_nu_minus_two_prior_mean,
            log_nu_minus_two_prior_sd=log_nu_minus_two_prior_sd,
        )
        if np.log(rng.uniform()) < value - current:
            chain[i] = candidate
            current = value
            accepted += 1
        else:
            chain[i] = chain[i - 1]

    posterior = chain[burn_in:]
    return StudentTMCMCResult(
        mu=posterior[:, 0].copy(),
        sigma=np.exp(posterior[:, 1]).copy(),
        nu=2.0 + np.exp(posterior[:, 2]).copy(),
        acceptance_rate=float(accepted / (n_iter - 1)),
        burn_in=int(burn_in),
        n_iter=int(n_iter),
    )
