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



def test_surface_direction_change_counter() -> None:
    from experiments.wti_lo_surface_shape_audit import _direction_changes

    assert _direction_changes(np.array([0.4, 0.41, 0.42])) == 0
    assert _direction_changes(np.array([0.4, 0.39, 0.40])) == 1


def test_tree_convergence_selection_covers_extremes_and_atm() -> None:
    import pandas as pd

    from experiments.wti_lo_tree_convergence import select_stratified

    frame = pd.DataFrame(
        {
            "reference_date": ["2026-08-24"] * 5,
            "underlying": ["CLX6"] * 5,
            "option_type": ["call"] * 5,
            "log_moneyness": [-0.10, -0.02, 0.001, 0.03, 0.12],
            "option_settlement": [1.0] * 5,
            "futures_settlement": [80.0] * 5,
            "strike_price": [72.0, 78.0, 80.1, 82.0, 90.0],
            "maturity_years": [0.1] * 5,
            "rate_proxy": [0.04] * 5,
            "symbol": [f"x{i}" for i in range(5)],
            "iv_status": ["ok"] * 5,
        }
    )
    selected = select_stratified(frame)
    assert len(selected) == 3
    assert set(selected["symbol"]) == {"x0", "x2", "x4"}



def test_prior_contract_iv_carry_uses_strictly_prior_observation() -> None:
    import pandas as pd

    from experiments.wti_prior_contract_iv_carry import _latest_prior_iv

    history = pd.DataFrame(
        {
            "contract_id": ["x", "x", "x"],
            "valuation_ts": pd.to_datetime(
                ["2026-08-24", "2026-08-25", "2026-08-26"]
            ),
            "apo_implied_sigma_q": [0.40, 0.45, 0.99],
        }
    )
    result = _latest_prior_iv(
        history,
        contract_id="x",
        target_date=pd.Timestamp("2026-08-26"),
    )
    assert result is not None
    sigma, date = result
    assert sigma == 0.45
    assert date == pd.Timestamp("2026-08-25")
