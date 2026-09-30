from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from experiments.wti_garch_horizon_benchmark import (
    GarchFit,
    _return_information,
    fit_gaussian_garch11,
    forecast_variances,
    moment_matched_garch_sigma,
    update_variance_with_return,
)


def _fit_fixture() -> GarchFit:
    return GarchFit(
        mu=0.0,
        omega=2.0e-6,
        alpha=0.05,
        beta=0.90,
        loglik=0.0,
        n_obs=500,
        last_variance=4.0e-5,
        last_residual=0.01,
        optimizer_success=True,
        optimizer_message="test",
    )


def test_garch_forecast_reverts_to_unconditional_variance() -> None:
    fit = _fit_fixture()
    first = 9.0e-5
    path = forecast_variances(fit, first_variance=first, horizon=200)

    assert path[0] == pytest.approx(first)
    assert path[-1] == pytest.approx(
        fit.unconditional_variance,
        rel=5e-4,
    )
    assert np.all(path > 0)


def test_target_return_updates_state_without_refitting() -> None:
    fit = _fit_fixture()
    target_return = 0.02

    h_target = (
        fit.omega
        + fit.alpha * fit.last_residual**2
        + fit.beta * fit.last_variance
    )
    expected = (
        fit.omega
        + fit.alpha * (target_return - fit.mu) ** 2
        + fit.beta * h_target
    )

    assert update_variance_with_return(fit, target_return) == pytest.approx(
        expected
    )


def test_moment_match_recovers_constant_sigma_on_consistent_clock() -> None:
    sigma = 0.45
    horizons = np.array([1, 3, 5], dtype=int)
    state = pd.DataFrame(
        {
            "settlement": [80.0, 81.0, 79.0],
            "business_horizon": horizons,
            "time_years": horizons / 252.0,
        }
    )
    daily_variance = np.full(
        int(horizons.max()),
        sigma**2 / 252.0,
        dtype=float,
    )

    matched = moment_matched_garch_sigma(state, daily_variance)

    assert matched == pytest.approx(sigma, rel=1e-10, abs=1e-10)


def test_return_information_uses_prior_for_fit_and_target_for_update(
    tmp_path,
) -> None:
    run_dir = tmp_path / "run"
    run_dir.mkdir()
    pd.DataFrame(
        {
            "date": [
                "2026-08-24 04:00:00",
                "2026-08-25 04:00:00",
                "2026-08-26 04:00:00",
            ],
            "log_return": [0.01, -0.02, 0.005],
            "usable_inference_return": [True, True, True],
        }
    ).to_csv(run_dir / "inference_return_audit.csv", index=False)

    prior, target = _return_information(
        run_dir,
        pd.Timestamp("2026-08-26"),
    )

    np.testing.assert_allclose(prior, [0.01, -0.02])
    assert target == pytest.approx(0.005)


def test_return_information_rejects_future_returns(tmp_path) -> None:
    run_dir = tmp_path / "run"
    run_dir.mkdir()
    pd.DataFrame(
        {
            "date": [
                "2026-08-25 04:00:00",
                "2026-08-26 04:00:00",
                "2026-08-27 04:00:00",
            ],
            "log_return": [0.01, -0.02, 0.005],
            "usable_inference_return": [True, True, True],
        }
    ).to_csv(run_dir / "inference_return_audit.csv", index=False)

    with pytest.raises(RuntimeError, match="future return"):
        _return_information(
            run_dir,
            pd.Timestamp("2026-08-26"),
        )


def test_gaussian_garch_fit_is_stationary_and_finite() -> None:
    rng = np.random.default_rng(20260929)
    returns = rng.normal(0.0002, 0.018, size=500)

    fit = fit_gaussian_garch11(returns)

    assert fit.n_obs == 500
    assert fit.omega > 0
    assert 0 <= fit.alpha < 1
    assert 0 <= fit.beta < 1
    assert fit.persistence < 1
    assert np.isfinite(fit.loglik)
    assert fit.unconditional_variance > 0
