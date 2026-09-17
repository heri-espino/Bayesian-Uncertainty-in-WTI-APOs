import numpy as np

from bayesian_asian_options.bayesian_student_t import (
    log_posterior_student_t,
    random_walk_metropolis_student_t,
    standardized_student_t_log_returns,
)


def test_standardized_student_t_returns_have_target_scale():
    dt = 1.0 / 252.0
    sigma = 0.35
    returns = standardized_student_t_log_returns(
        mu=0.0,
        sigma=sigma,
        nu=6.0,
        dt=dt,
        n_obs=200_000,
        seed=123,
    )
    empirical_sigma = np.std(returns, ddof=0) / np.sqrt(dt)
    assert abs(empirical_sigma - sigma) < 0.015


def test_student_t_log_posterior_is_finite_for_regular_inputs():
    returns = standardized_student_t_log_returns(
        mu=0.08,
        sigma=0.25,
        nu=8.0,
        dt=1.0 / 252.0,
        n_obs=100,
        seed=7,
    )
    value = log_posterior_student_t(
        np.array([0.08, np.log(0.25), np.log(6.0)]),
        returns,
        1.0 / 252.0,
    )
    assert np.isfinite(value)


def test_student_t_sampler_returns_positive_sigma_and_nu_above_two():
    returns = standardized_student_t_log_returns(
        mu=0.05,
        sigma=0.30,
        nu=7.0,
        dt=1.0 / 252.0,
        n_obs=150,
        seed=99,
    )
    result = random_walk_metropolis_student_t(
        returns,
        1.0 / 252.0,
        n_iter=1200,
        burn_in=200,
        proposal_sd=(0.15, 0.05, 0.10),
        seed=100,
    )
    assert len(result.sigma) == 1000
    assert np.all(np.isfinite(result.sigma))
    assert np.all(result.sigma > 0)
    assert np.all(result.nu > 2)
    assert 0.0 < result.acceptance_rate < 1.0
