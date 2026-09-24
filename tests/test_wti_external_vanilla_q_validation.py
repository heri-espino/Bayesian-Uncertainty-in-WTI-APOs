from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from experiments.wti_external_vanilla_q_validation import (
    _effective_sigma,
    _fit_surface_models,
    _prior_sigma,
    _surface_sigma_targets,
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


def test_comparison_summary_uses_exact_common_contract_dates(tmp_path) -> None:
    from experiments.wti_external_vanilla_q_validation import _comparison_summary

    keys_external = [
        ("2026-09-01", "2026-10", "a"),
        ("2026-09-01", "2026-10", "b"),
        ("2026-09-02", "2026-10", "c"),
    ]
    external_rows = []
    for method in (
        "vanilla_previous_day",
        "vanilla_expanding",
        "vanilla_surface_previous_day",
        "vanilla_surface_expanding",
    ):
        for i, (date, expiry, contract) in enumerate(keys_external):
            external_rows.append(
                {
                    "method": method,
                    "valuation_date": date,
                    "apo_expiry": expiry,
                    "contract_id": contract,
                    "forward_error": float(i + 1),
                    "baseline_pi_error": float(i + 2),
                }
            )
    external = pd.DataFrame(external_rows)

    apo_rows = []
    for method in ("previous_day_smile", "expanding_smile"):
        for i, (date, expiry, contract) in enumerate(keys_external[:2]):
            apo_rows.append(
                {
                    "method": method,
                    "valuation_date": date,
                    "apo_expiry": expiry,
                    "contract_id": contract,
                    "forward_error": float(i) + 0.5,
                    "baseline_pi_error": float(i) + 2.0,
                }
            )
    apo_path = tmp_path / "apo.csv"
    pd.DataFrame(apo_rows).to_csv(apo_path, index=False)

    available, matched = _comparison_summary(external, apo_path)

    assert not available.empty
    assert set(matched["n"]) == {2}
    assert set(matched["n_dates"]) == {1}
    assert set(matched["method"]) == {
        "historical_pi",
        "vanilla_previous_day",
        "vanilla_expanding",
        "vanilla_surface_previous_day",
        "vanilla_surface_expanding",
        "apo_previous_day_smile",
        "apo_expanding_smile",
    }



def test_surface_model_uses_prior_smile_and_target_futures() -> None:
    rows = []
    for underlying, base in (("CLX6", 0.40), ("CLZ6", 0.50)):
        for option_type in ("call", "put"):
            for x in (-0.04, -0.02, 0.0, 0.02, 0.04):
                rows.append(
                    {
                        "reference_date": "2026-08-24",
                        "reference_ts": pd.Timestamp("2026-08-24"),
                        "underlying": underlying,
                        "option_type": option_type,
                        "log_moneyness": x,
                        "implied_volatility": (
                            base
                            + 0.10 * x
                            + 0.50 * x**2
                            + (0.01 if option_type == "call" else 0.0)
                        ),
                        "iv_status": "ok",
                    }
                )
    # Same-day observations are deliberately extreme and must not enter.
    for underlying in ("CLX6", "CLZ6"):
        rows.append(
            {
                "reference_date": "2026-08-25",
                "reference_ts": pd.Timestamp("2026-08-25"),
                "underlying": underlying,
                "option_type": "call",
                "log_moneyness": 0.0,
                "implied_volatility": 0.99,
                "iv_status": "ok",
            }
        )
    panel = pd.DataFrame(rows)

    models, supports, training_end, n_dates = _fit_surface_models(
        panel,
        target_date=pd.Timestamp("2026-08-25"),
        half_life_days=None,
        ridge=1e-10,
    )

    targets = pd.DataFrame(
        {
            "strike": [90.0],
            "option_type": ["call"],
        }
    )
    sigma, clipped = _surface_sigma_targets(
        targets,
        models=models,
        supports=supports,
        target_futures={"CLX6": 90.0, "CLZ6": 90.0},
        fixing_weights={"CLX6": 0.5, "CLZ6": 0.5},
    )

    expected = np.sqrt(0.5 * 0.41**2 + 0.5 * 0.51**2)
    assert sigma[0] == pytest.approx(expected, abs=1e-4)
    assert clipped[0] == 0
    assert training_end == "2026-08-24"
    assert n_dates == 1


def test_surface_prediction_clips_to_prior_moneyness_support() -> None:
    panel = pd.DataFrame(
        {
            "reference_date": ["2026-08-24"] * 12,
            "reference_ts": [pd.Timestamp("2026-08-24")] * 12,
            "underlying": ["CLX6"] * 6 + ["CLZ6"] * 6,
            "option_type": ["call"] * 12,
            "log_moneyness": [-0.02, -0.01, 0.0, 0.01, 0.015, 0.02] * 2,
            "implied_volatility": [0.40, 0.40, 0.40, 0.40, 0.40, 0.40] * 2,
            "iv_status": ["ok"] * 12,
        }
    )
    models, supports, _, _ = _fit_surface_models(
        panel,
        target_date=pd.Timestamp("2026-08-25"),
        half_life_days=None,
        ridge=1e-6,
    )
    targets = pd.DataFrame(
        {
            "strike": [110.0],
            "option_type": ["call"],
        }
    )
    _, clipped = _surface_sigma_targets(
        targets,
        models=models,
        supports=supports,
        target_futures={"CLX6": 90.0, "CLZ6": 90.0},
        fixing_weights={"CLX6": 0.5, "CLZ6": 0.5},
    )
    assert clipped[0] == 2



def test_surface_common_support_comparison_requires_zero_clipping(tmp_path) -> None:
    from experiments.wti_external_vanilla_q_validation import (
        _surface_common_support_comparison,
    )

    keys = [
        ("2026-09-01", "2026-10", "a"),
        ("2026-09-01", "2026-10", "b"),
        ("2026-09-02", "2026-10", "c"),
    ]
    rows = []
    for method in (
        "vanilla_surface_previous_day",
        "vanilla_surface_expanding",
    ):
        for i, (date, expiry, contract) in enumerate(keys):
            rows.append(
                {
                    "method": method,
                    "valuation_date": date,
                    "apo_expiry": expiry,
                    "contract_id": contract,
                    "forward_error": 0.1 + i,
                    "baseline_pi_error": 0.2 + i,
                    "surface_components_clipped": 1 if contract == "c" else 0,
                }
            )
    external = pd.DataFrame(rows)

    apo_rows = []
    for method in ("previous_day_smile", "expanding_smile"):
        for i, (date, expiry, contract) in enumerate(keys):
            apo_rows.append(
                {
                    "method": method,
                    "valuation_date": date,
                    "apo_expiry": expiry,
                    "contract_id": contract,
                    "forward_error": 0.05 + i,
                }
            )
    apo_path = tmp_path / "apo.csv"
    pd.DataFrame(apo_rows).to_csv(apo_path, index=False)

    out = _surface_common_support_comparison(external, apo_path)

    assert set(out["n"]) == {2}
    assert set(out["n_dates"]) == {1}
    assert set(out["sample"]) == {"surface_common_support"}
