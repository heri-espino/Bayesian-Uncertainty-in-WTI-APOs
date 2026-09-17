"""Exact one-dimensional sigma quadrature for the Gaussian GBM posterior.

The production sampler works in ``(mu, log_sigma)``.  For large simulation studies we can
integrate ``mu`` analytically because the Gaussian likelihood is linear in ``mu`` and the
paper uses a Gaussian prior on ``mu``.  This leaves a one-dimensional posterior density for
``sigma`` that can be integrated accurately on a dense grid.

This module is intentionally independent of MCMC.  It therefore provides a numerical
reference for sampler validation and enables very large posterior-pricing experiments
without changing the statistical model used by the paper.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import lgamma
from typing import Any

import numpy as np


@dataclass(frozen=True)
class SigmaQuadratureResult:
    sigma_grid: np.ndarray
    weights: np.ndarray
    mean: np.ndarray
    variance: np.ndarray


def trapezoid_weights(grid: np.ndarray) -> np.ndarray:
    """Return integration weights for an increasing one-dimensional grid."""
    x = np.asarray(grid, dtype=float)
    if x.ndim != 1 or x.size < 2 or np.any(~np.isfinite(x)) or np.any(np.diff(x) <= 0):
        raise ValueError("grid must be a finite, strictly increasing one-dimensional array")
    w = np.empty_like(x)
    w[0] = 0.5 * (x[1] - x[0])
    w[-1] = 0.5 * (x[-1] - x[-2])
    if x.size > 2:
        w[1:-1] = 0.5 * (x[2:] - x[:-2])
    return w


def _quadrature_density_and_node_cdf(
    grid: np.ndarray,
    weights: np.ndarray,
) -> tuple[np.ndarray, np.ndarray]:
    """Recover normalized node densities and a correct trapezoidal CDF.

    ``normalized_sigma_weights`` returns *integration masses* ``q_i f_i / Z`` at the
    quadrature nodes, where ``q_i`` are the composite-trapezoid node weights.  A cumulative
    sum of those masses is suitable for expectations but is not the posterior CDF at the
    grid nodes: an interior ``q_i`` includes half of the interval to the right of ``x_i``.

    This helper first recovers ``f_i / Z`` by dividing by ``q_i`` and then accumulates the
    actual trapezoidal interval masses.  The distinction matters when the posterior becomes
    narrow relative to the grid, as in large-sample simulation-based calibration.
    """
    x = np.asarray(grid, dtype=float)
    q = trapezoid_weights(x)
    w = np.asarray(weights, dtype=float)
    if w.ndim < 1 or w.shape[-1] != x.size:
        raise ValueError("last weights dimension must match grid")
    if np.any(~np.isfinite(w)) or np.any(w < 0):
        raise ValueError("quadrature weights must be finite and non-negative")
    totals = np.sum(w, axis=-1, keepdims=True)
    if np.any(totals <= 0):
        raise ValueError("quadrature weights must have positive total mass")
    w = w / totals

    density = w / q
    dx = np.diff(x)
    interval_mass = 0.5 * (density[..., :-1] + density[..., 1:]) * dx
    cdf = np.concatenate(
        [np.zeros(w.shape[:-1] + (1,), dtype=float), np.cumsum(interval_mass, axis=-1)],
        axis=-1,
    )
    # Roundoff can make the final value differ microscopically from one.
    cdf /= cdf[..., -1:]
    cdf[..., -1] = 1.0
    return density, cdf


def quadrature_cdf_at(
    grid: np.ndarray,
    weights: np.ndarray,
    values: np.ndarray | float,
) -> np.ndarray:
    """Evaluate a trapezoidal quadrature posterior CDF at arbitrary values.

    The density is treated as piecewise linear between grid nodes, matching the composite
    trapezoid rule used to normalize the posterior.  ``values`` must broadcast to the batch
    dimensions of ``weights`` (all dimensions except the final grid dimension).
    """
    x = np.asarray(grid, dtype=float)
    density, node_cdf = _quadrature_density_and_node_cdf(x, weights)
    batch_shape = density.shape[:-1]
    value_array = np.broadcast_to(np.asarray(values, dtype=float), batch_shape)
    out = np.empty(batch_shape, dtype=float)
    dx = np.diff(x)

    for index in np.ndindex(batch_shape):
        value = float(value_array[index])
        if value <= x[0]:
            out[index] = 0.0
            continue
        if value >= x[-1]:
            out[index] = 1.0
            continue
        j = int(np.searchsorted(x, value, side="right") - 1)
        fraction = (value - x[j]) / dx[j]
        d0 = float(density[index + (j,)])
        d1 = float(density[index + (j + 1,)])
        partial_mass = dx[j] * (
            d0 * fraction + 0.5 * (d1 - d0) * fraction**2
        )
        out[index] = float(node_cdf[index + (j,)]) + partial_mass
    return np.clip(out, 0.0, 1.0)


def quadrature_quantile(
    grid: np.ndarray,
    weights: np.ndarray,
    probability: float,
) -> np.ndarray:
    """Return posterior quantiles consistent with trapezoidal normalization.

    Within each grid interval the normalized density is linearly interpolated, so the CDF is
    quadratic.  The inverse below solves that local quadratic rather than treating node
    integration weights as point probabilities.
    """
    if not 0.0 <= probability <= 1.0:
        raise ValueError("probability must lie in [0, 1]")
    x = np.asarray(grid, dtype=float)
    density, node_cdf = _quadrature_density_and_node_cdf(x, weights)
    batch_shape = density.shape[:-1]
    out = np.empty(batch_shape, dtype=float)
    dx = np.diff(x)

    if probability == 0.0:
        out.fill(x[0])
        return out
    if probability == 1.0:
        out.fill(x[-1])
        return out

    for index in np.ndindex(batch_shape):
        cdf = node_cdf[index]
        j = int(np.searchsorted(cdf, probability, side="right") - 1)
        j = max(0, min(j, x.size - 2))
        delta = float(probability - cdf[j])
        h = float(dx[j])
        d0 = float(density[index + (j,)])
        d1 = float(density[index + (j + 1,)])
        target = delta / h
        a = 0.5 * (d1 - d0)
        b = d0

        if abs(a) <= 1e-14 * max(1.0, abs(b)):
            fraction = target / b if b > 0 else 0.0
        else:
            discriminant = max(b * b + 4.0 * a * target, 0.0)
            root = np.sqrt(discriminant)
            candidates = ((-b + root) / (2.0 * a), (-b - root) / (2.0 * a))
            valid = [value for value in candidates if -1e-12 <= value <= 1.0 + 1e-12]
            if valid:
                fraction = valid[0]
            else:
                interval_probability = float(cdf[j + 1] - cdf[j])
                fraction = delta / interval_probability if interval_probability > 0 else 0.0

        out[index] = x[j] + float(np.clip(fraction, 0.0, 1.0)) * h
    return out


def gaussian_gbm_marginal_log_posterior_sigma(
    sigma_grid: np.ndarray,
    *,
    n_obs: int,
    sum_returns: np.ndarray | float,
    sumsq_returns: np.ndarray | float,
    dt: float,
    mu_prior_sd: float = 1.0,
    sigma_prior_alpha: float = 2.0,
    sigma_prior_beta: float = 0.1,
    xp: Any = np,
) -> Any:
    """Evaluate ``log p(sigma | returns)`` up to a sigma-independent constant.

    ``sum_returns`` and ``sumsq_returns`` may be scalars or arrays of replicated datasets.
    The returned shape is ``broadcast(sum_returns, sumsq_returns) + (len(sigma_grid),)``.

    The derivation uses ``y_i = r_i + 0.5 sigma^2 dt = mu dt + eps_i`` with
    ``eps_i ~ N(0, sigma^2 dt)`` and ``mu ~ N(0, tau^2)``.  Integrating out ``mu`` gives
    covariance ``v I + tau^2 dt^2 11'`` where ``v = sigma^2 dt``.  The determinant and
    inverse then follow from the matrix determinant lemma and Sherman-Morrison formula.
    """
    if n_obs < 1:
        raise ValueError("n_obs must be positive")
    if dt <= 0 or mu_prior_sd <= 0 or sigma_prior_alpha <= 0 or sigma_prior_beta <= 0:
        raise ValueError("dt and prior hyperparameters must be positive")

    sigma = xp.asarray(sigma_grid, dtype=xp.float64)
    if sigma.ndim != 1 or sigma.size < 2:
        raise ValueError("sigma_grid must be one-dimensional with at least two points")
    if bool(xp.any(~xp.isfinite(sigma))) or bool(xp.any(sigma <= 0)):
        raise ValueError("sigma_grid must be positive and finite")

    sr = xp.asarray(sum_returns, dtype=xp.float64)[..., None]
    ss = xp.asarray(sumsq_returns, dtype=xp.float64)[..., None]
    if sr.shape != ss.shape:
        sr, ss = xp.broadcast_arrays(sr, ss)

    sigma2 = sigma[None, :] ** 2
    shift = 0.5 * sigma2 * float(dt)
    sum_y = sr + float(n_obs) * shift
    sumsq_y = ss + 2.0 * shift * sr + float(n_obs) * shift**2

    v = sigma2 * float(dt)
    prior_rank_one = float(mu_prior_sd**2 * dt**2)
    logdet = float(n_obs) * xp.log(v) + xp.log1p(prior_rank_one * float(n_obs) / v)
    correction = prior_rank_one / (v * (v + prior_rank_one * float(n_obs)))
    quadratic = sumsq_y / v - correction * sum_y**2
    log_marginal = -0.5 * (logdet + quadratic)

    alpha = float(sigma_prior_alpha)
    beta = float(sigma_prior_beta)
    log_prior = (
        alpha * np.log(beta)
        - lgamma(alpha)
        - (alpha + 1.0) * xp.log(sigma)[None, :]
        - beta / sigma[None, :]
    )
    return log_marginal + log_prior


def normalized_sigma_weights(
    log_density: Any,
    sigma_grid: np.ndarray,
    *,
    xp: Any = np,
) -> Any:
    """Normalize a batch of log densities using trapezoidal quadrature."""
    logp = xp.asarray(log_density, dtype=xp.float64)
    if logp.ndim < 1 or logp.shape[-1] != len(sigma_grid):
        raise ValueError("last log-density dimension must match sigma_grid")
    q = xp.asarray(trapezoid_weights(np.asarray(sigma_grid, dtype=float)), dtype=xp.float64)
    maximum = xp.max(logp, axis=-1, keepdims=True)
    raw = xp.exp(logp - maximum) * q
    denominator = xp.sum(raw, axis=-1, keepdims=True)
    if bool(xp.any(~xp.isfinite(denominator))) or bool(xp.any(denominator <= 0)):
        raise RuntimeError("failed to normalize sigma posterior")
    return raw / denominator


def posterior_sigma_quadrature(
    sigma_grid: np.ndarray,
    *,
    n_obs: int,
    sum_returns: np.ndarray | float,
    sumsq_returns: np.ndarray | float,
    dt: float,
    mu_prior_sd: float = 1.0,
    sigma_prior_alpha: float = 2.0,
    sigma_prior_beta: float = 0.1,
) -> SigmaQuadratureResult:
    """Return posterior sigma weights, means, and variances for one or many datasets."""
    grid = np.asarray(sigma_grid, dtype=float)
    logp = gaussian_gbm_marginal_log_posterior_sigma(
        grid,
        n_obs=n_obs,
        sum_returns=sum_returns,
        sumsq_returns=sumsq_returns,
        dt=dt,
        mu_prior_sd=mu_prior_sd,
        sigma_prior_alpha=sigma_prior_alpha,
        sigma_prior_beta=sigma_prior_beta,
        xp=np,
    )
    weights = normalized_sigma_weights(logp, grid, xp=np)
    mean = np.sum(weights * grid, axis=-1)
    second = np.sum(weights * grid**2, axis=-1)
    variance = np.maximum(second - mean**2, 0.0)
    return SigmaQuadratureResult(
        sigma_grid=grid,
        weights=np.asarray(weights),
        mean=np.asarray(mean),
        variance=np.asarray(variance),
    )


def gaussian_sufficient_statistics_simulation(
    *,
    n_obs: int,
    mu_true: float,
    sigma_true: float,
    dt: float,
    replications: int,
    seed: int,
) -> tuple[np.ndarray, np.ndarray]:
    """Simulate exact Gaussian sufficient statistics without materializing all returns."""
    if n_obs < 2 or replications < 1 or sigma_true <= 0 or dt <= 0:
        raise ValueError("invalid sufficient-statistic simulation inputs")
    rng = np.random.default_rng(seed)
    mean_true = (float(mu_true) - 0.5 * float(sigma_true) ** 2) * float(dt)
    variance_true = float(sigma_true) ** 2 * float(dt)
    sample_mean = mean_true + np.sqrt(variance_true / n_obs) * rng.standard_normal(replications)
    centered_ss = variance_true * rng.chisquare(df=n_obs - 1, size=replications)
    sums = float(n_obs) * sample_mean
    sumsquares = centered_ss + float(n_obs) * sample_mean**2
    return sums.astype(float), sumsquares.astype(float)
