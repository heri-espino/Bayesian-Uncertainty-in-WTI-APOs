"""Bayesian inference for a GBM under the physical measure P.

The module deliberately stops at parameter inference. Derivative pricing belongs in
``bayesian_asian_options.asian_pricing`` and is performed under the risk-neutral measure Q.

We sample ``theta = (mu, eta)`` with ``eta = log(sigma)``.  This removes the
positivity boundary for volatility.  If the prior is specified on sigma, the
log-posterior in eta includes the Jacobian ``+ eta``.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import lgamma

import numpy as np


@dataclass(frozen=True)
class MCMCResult:
    """Posterior draws and basic Random-Walk Metropolis diagnostics."""

    mu: np.ndarray
    sigma: np.ndarray
    acceptance_rate: float
    burn_in: int
    n_iter: int


def gbm_log_returns(
    *,
    mu: float,
    sigma: float,
    dt: float,
    n_obs: int,
    seed: int | None = None,
) -> np.ndarray:
    """Simulate GBM log returns under the physical measure P."""
    if sigma <= 0:
        raise ValueError("sigma must be positive")
    if dt <= 0:
        raise ValueError("dt must be positive")
    if n_obs < 1:
        raise ValueError("n_obs must be at least one")

    rng = np.random.default_rng(seed)
    z = rng.standard_normal(n_obs)
    return (mu - 0.5 * sigma**2) * dt + sigma * np.sqrt(dt) * z


def log_posterior_mu_logsigma(
    theta: np.ndarray,
    log_returns: np.ndarray,
    dt: float,
    *,
    mu_prior_sd: float = 1.0,
    sigma_prior_alpha: float = 2.0,
    sigma_prior_beta: float = 0.1,
) -> float:
    """Unnormalised log posterior for ``(mu, log(sigma))``.

    Model under P:
        r_i ~ N((mu - sigma^2/2) dt, sigma^2 dt).

    Priors:
        mu ~ N(0, mu_prior_sd^2),
        sigma ~ InverseGamma(alpha, beta),

    where the inverse-gamma density is proportional to
    ``sigma^(-alpha-1) exp(-beta/sigma)``.  Because sampling is performed in
    ``eta = log(sigma)``, the density contains the transformation Jacobian
    ``d sigma / d eta = sigma``.
    """
    theta = np.asarray(theta, dtype=float)
    returns = np.asarray(log_returns, dtype=float)
    if theta.shape != (2,):
        raise ValueError("theta must contain (mu, log_sigma)")
    if returns.ndim != 1 or returns.size == 0:
        raise ValueError("log_returns must be a non-empty one-dimensional array")
    if dt <= 0:
        raise ValueError("dt must be positive")
    if mu_prior_sd <= 0 or sigma_prior_alpha <= 0 or sigma_prior_beta <= 0:
        raise ValueError("prior hyperparameters must be positive")

    mu, eta = theta
    sigma = float(np.exp(eta))
    if not np.isfinite(sigma):
        return -np.inf

    mean = (mu - 0.5 * sigma**2) * dt
    var = sigma**2 * dt
    n = returns.size

    log_lik = -0.5 * n * np.log(2.0 * np.pi * var)
    log_lik -= 0.5 * np.sum((returns - mean) ** 2) / var

    log_prior_mu = -np.log(mu_prior_sd) - 0.5 * (mu / mu_prior_sd) ** 2

    alpha = sigma_prior_alpha
    beta = sigma_prior_beta
    log_prior_sigma = (
        alpha * np.log(beta)
        - lgamma(alpha)
        - (alpha + 1.0) * eta
        - beta / sigma
    )

    # Change-of-variable Jacobian: p(eta) = p(sigma) * sigma.
    log_jacobian = eta
    return float(log_lik + log_prior_mu + log_prior_sigma + log_jacobian)


def random_walk_metropolis_gbm(
    log_returns: np.ndarray,
    dt: float,
    *,
    n_iter: int = 20_000,
    burn_in: int = 4_000,
    theta_init: tuple[float, float] = (0.05, np.log(0.25)),
    proposal_sd: tuple[float, float] = (0.30, 0.08),
    seed: int | None = None,
) -> MCMCResult:
    """Sample the physical-measure GBM posterior by Random-Walk Metropolis.

    ``theta_init`` and ``proposal_sd`` are expressed in ``(mu, log_sigma)``.
    The function returns sigma on its natural positive scale.
    """
    if n_iter < 2:
        raise ValueError("n_iter must be at least two")
    if burn_in < 0 or burn_in >= n_iter:
        raise ValueError("burn_in must satisfy 0 <= burn_in < n_iter")

    proposal = np.asarray(proposal_sd, dtype=float)
    if proposal.shape != (2,) or np.any(proposal <= 0):
        raise ValueError("proposal_sd must contain two positive values")

    rng = np.random.default_rng(seed)
    chain = np.empty((n_iter, 2), dtype=float)
    chain[0] = np.asarray(theta_init, dtype=float)
    current_logp = log_posterior_mu_logsigma(chain[0], log_returns, dt)
    accepted = 0

    for i in range(1, n_iter):
        candidate = chain[i - 1] + rng.normal(0.0, proposal, size=2)
        candidate_logp = log_posterior_mu_logsigma(candidate, log_returns, dt)
        if np.log(rng.uniform()) < candidate_logp - current_logp:
            chain[i] = candidate
            current_logp = candidate_logp
            accepted += 1
        else:
            chain[i] = chain[i - 1]

    posterior = chain[burn_in:]
    return MCMCResult(
        mu=posterior[:, 0].copy(),
        sigma=np.exp(posterior[:, 1]).copy(),
        acceptance_rate=accepted / (n_iter - 1),
        burn_in=burn_in,
        n_iter=n_iter,
    )


def gbm_mle(log_returns: np.ndarray, dt: float) -> tuple[float, float]:
    """Return the Gaussian/GBM maximum-likelihood estimates of mu and sigma."""
    returns = np.asarray(log_returns, dtype=float)
    if returns.ndim != 1 or returns.size == 0:
        raise ValueError("log_returns must be a non-empty one-dimensional array")
    if dt <= 0:
        raise ValueError("dt must be positive")

    variance = float(np.var(returns, ddof=0))
    sigma_hat = float(np.sqrt(variance / dt))
    mu_hat = float(np.mean(returns) / dt + 0.5 * sigma_hat**2)
    return mu_hat, sigma_hat
