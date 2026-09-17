import numpy as np

from bayesian_asian_options.bayesian_gbm import (
    gbm_log_returns,
    gbm_mle,
    log_posterior_mu_logsigma,
    random_walk_metropolis_gbm,
)


def test_gbm_log_returns_are_reproducible():
    x1 = gbm_log_returns(mu=0.08, sigma=0.25, dt=1 / 252, n_obs=20, seed=7)
    x2 = gbm_log_returns(mu=0.08, sigma=0.25, dt=1 / 252, n_obs=20, seed=7)
    assert np.array_equal(x1, x2)


def test_log_posterior_is_finite_on_valid_state():
    data = gbm_log_returns(mu=0.08, sigma=0.25, dt=1 / 252, n_obs=50, seed=3)
    value = log_posterior_mu_logsigma(np.array([0.05, np.log(0.25)]), data, 1 / 252)
    assert np.isfinite(value)


def test_mle_recovers_positive_volatility():
    data = gbm_log_returns(mu=0.08, sigma=0.25, dt=1 / 252, n_obs=1000, seed=4)
    _, sigma_hat = gbm_mle(data, 1 / 252)
    assert sigma_hat > 0
    assert abs(sigma_hat - 0.25) < 0.03


def test_metropolis_returns_positive_sigma_and_valid_acceptance():
    data = gbm_log_returns(mu=0.08, sigma=0.25, dt=1 / 252, n_obs=100, seed=9)
    result = random_walk_metropolis_gbm(
        data,
        1 / 252,
        n_iter=1000,
        burn_in=200,
        seed=10,
    )
    assert result.mu.shape == (800,)
    assert result.sigma.shape == (800,)
    assert np.all(result.sigma > 0)
    assert 0.0 < result.acceptance_rate < 1.0


def test_metropolis_accepts_explicit_prior_hyperparameters():
    data = gbm_log_returns(mu=0.08, sigma=0.25, dt=1 / 252, n_obs=80, seed=13)
    baseline = random_walk_metropolis_gbm(
        data,
        1 / 252,
        n_iter=800,
        burn_in=200,
        seed=14,
    )
    alternative = random_walk_metropolis_gbm(
        data,
        1 / 252,
        n_iter=800,
        burn_in=200,
        sigma_prior_alpha=4.0,
        sigma_prior_beta=0.6,
        seed=14,
    )
    assert np.all(alternative.sigma > 0)
    assert not np.array_equal(baseline.sigma, alternative.sigma)
