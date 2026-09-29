from __future__ import annotations

import math

import numpy as np

from experiments.wti_recent_historical_benchmarks import (
    ewma_sigma,
    rolling_sigma,
)
from experiments.wti_rms_plugin_comparison import sigma_rms


def test_rolling_sigma_uses_recent_window_and_annualizes() -> None:
    returns = np.array([0.0, 0.01, -0.01, 0.02, -0.02], dtype=float)
    expected = float(np.std(returns[-4:], ddof=1) * np.sqrt(252.0))
    assert math.isclose(
        rolling_sigma(returns, 4),
        expected,
        rel_tol=1e-12,
        abs_tol=1e-12,
    )


def test_ewma_sigma_is_positive_and_recency_sensitive() -> None:
    quiet_then_volatile = np.array(
        [0.001] * 20 + [0.03, -0.03, 0.025, -0.025],
        dtype=float,
    )
    short = ewma_sigma(quiet_then_volatile, half_life=2.0)
    long = ewma_sigma(quiet_then_volatile, half_life=20.0)
    assert short > 0.0
    assert long > 0.0
    assert short > long


def test_sigma_rms_matches_second_posterior_moment() -> None:
    mean = 0.40
    sd = 0.03
    expected = math.sqrt(mean**2 + sd**2)
    assert math.isclose(
        sigma_rms(mean, sd),
        expected,
        rel_tol=1e-12,
        abs_tol=1e-12,
    )
    assert sigma_rms(mean, sd) > mean
