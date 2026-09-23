from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from experiments.wti_external_vanilla_q_validation import (
    _effective_sigma,
    _prior_sigma,
)


def _vanilla(date: str, sx: float, sz: float) -> pd.DataFrame:
    return pd.DataFrame(
        {
            "reference_date": [date, date],
            "reference_ts": pd.to_datetime([date, date]),
            "underlying": ["CLX6", "CLZ6"],
            "near_atm_median_iv": [sx, sz],
        }
    )


def test_effective_sigma_uses_fixing_weighted_rms() -> None:
    frame = _vanilla("2026-08-24", 0.40, 0.50)
    weights = {"CLX6": 14 / 22, "CLZ6": 8 / 22}

    sigma = _effective_sigma(
        frame,
        weights,
        column="near_atm_median_iv",
        aggregation="weighted_rms",
    )

    expected = np.sqrt((14 / 22) * 0.40**2 + (8 / 22) * 0.50**2)
    assert sigma == pytest.approx(expected)


def test_prior_sigma_never_uses_same_day() -> None:
    vanilla = pd.concat(
        [
            _vanilla("2026-08-24", 0.40, 0.50),
            _vanilla("2026-08-25", 0.90, 0.90),
        ],
        ignore_index=True,
    )
    weights = {"CLX6": 0.5, "CLZ6": 0.5}

    sigma, training_end, n_dates = _prior_sigma(
        vanilla,
        target_date=pd.Timestamp("2026-08-25"),
        fixing_weights=weights,
        aggregation="weighted_rms",
        half_life_days=None,
    )

    assert sigma == pytest.approx(np.sqrt(0.5 * 0.40**2 + 0.5 * 0.50**2))
    assert training_end == "2026-08-24"
    assert n_dates == 1


def test_prior_sigma_expanding_uses_only_earlier_dates() -> None:
    vanilla = pd.concat(
        [
            _vanilla("2026-08-24", 0.40, 0.40),
            _vanilla("2026-08-25", 0.50, 0.50),
            _vanilla("2026-08-26", 0.95, 0.95),
        ],
        ignore_index=True,
    )

    sigma, training_end, n_dates = _prior_sigma(
        vanilla,
        target_date=pd.Timestamp("2026-08-26"),
        fixing_weights={"CLX6": 0.5, "CLZ6": 0.5},
        aggregation="weighted_rms",
        half_life_days=5.0,
    )

    assert 0.40 < sigma < 0.50
    assert training_end == "2026-08-25"
    assert n_dates == 2
