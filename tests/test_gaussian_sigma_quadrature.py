import numpy as np
from scipy.stats import invgamma, multivariate_normal

from bayesian_asian_options.gaussian_sigma_quadrature import (
    gaussian_gbm_marginal_log_posterior_sigma,
    gaussian_sufficient_statistics_simulation,
    normalized_sigma_weights,
    posterior_sigma_quadrature,
    quadrature_cdf_at,
    quadrature_quantile,
)


def test_marginal_log_posterior_matches_direct_gaussian_marginal():
    returns = np.array([0.012, -0.007, 0.004, 0.015, -0.003], dtype=float)
    dt = 1.0 / 252.0
    tau = 1.0
    grid = np.array([0.15, 0.25, 0.45])
    ours = gaussian_gbm_marginal_log_posterior_sigma(
        grid,
        n_obs=len(returns),
        sum_returns=float(returns.sum()),
        sumsq_returns=float(np.sum(returns**2)),
        dt=dt,
        mu_prior_sd=tau,
        sigma_prior_alpha=2.0,
        sigma_prior_beta=0.1,
    ).reshape(-1)

    direct = []
    for sigma in grid:
        y = returns + 0.5 * sigma**2 * dt
        covariance = sigma**2 * dt * np.eye(len(returns)) + tau**2 * dt**2 * np.ones(
            (len(returns), len(returns))
        )
        value = multivariate_normal.logpdf(y, mean=np.zeros(len(returns)), cov=covariance)
        value += invgamma.logpdf(sigma, a=2.0, scale=0.1)
        direct.append(value)
    direct = np.asarray(direct)

    # The implementation intentionally drops sigma-independent normalizing constants.
    np.testing.assert_allclose(ours - ours[0], direct - direct[0], rtol=1e-10, atol=1e-10)


def test_quadrature_weights_normalize_and_recover_sigma_with_long_sample():
    sums, sumsquares = gaussian_sufficient_statistics_simulation(
        n_obs=5000,
        mu_true=0.08,
        sigma_true=0.30,
        dt=1.0 / 252.0,
        replications=1,
        seed=1234,
    )
    grid = np.linspace(0.05, 0.80, 2001)
    result = posterior_sigma_quadrature(
        grid,
        n_obs=5000,
        sum_returns=sums,
        sumsq_returns=sumsquares,
        dt=1.0 / 252.0,
    )
    np.testing.assert_allclose(result.weights.sum(axis=-1), 1.0, atol=1e-12)
    assert abs(float(result.mean[0]) - 0.30) < 0.02
    assert float(result.variance[0]) > 0.0


def test_quadrature_cdf_is_exact_for_uniform_density_on_nonuniform_grid():
    grid = np.array([0.0, 0.1, 0.4, 1.0])
    weights = normalized_sigma_weights(np.zeros((2, len(grid))), grid)
    values = np.array([0.05, 0.75])
    ranks = quadrature_cdf_at(grid, weights, values)
    np.testing.assert_allclose(ranks, values, atol=1e-12)


def test_quadrature_quantiles_are_exact_for_uniform_density_on_nonuniform_grid():
    grid = np.array([0.0, 0.1, 0.4, 1.0])
    weights = normalized_sigma_weights(np.zeros((2, len(grid))), grid)
    for probability in (0.025, 0.25, 0.5, 0.9, 0.975):
        quantiles = quadrature_quantile(grid, weights, probability)
        np.testing.assert_allclose(quantiles, probability, atol=1e-12)
