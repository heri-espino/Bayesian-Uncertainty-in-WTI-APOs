from __future__ import annotations

import pandas as pd
import pytest

from experiments.wti_first_nearby_pricing_comparison import compare_baselines


def _forward(baseline_prices: list[float]) -> pd.DataFrame:
    rows = []
    contracts = [
        ("2026-08-27", "2026-10", "A", 1.0),
        ("2026-08-28", "2026-10", "B", 2.0),
    ]
    for method in ("previous_day_smile", "expanding_smile"):
        for (date, expiry, contract_id, market), baseline in zip(
            contracts, baseline_prices
        ):
            rows.append(
                {
                    "method": method,
                    "valuation_date": date,
                    "apo_expiry": expiry,
                    "contract_id": contract_id,
                    "market_settlement": market,
                    "baseline_pi_price": baseline,
                    "baseline_pi_error": baseline - market,
                }
            )
    return pd.DataFrame(rows)


def test_compare_baselines_requires_and_preserves_exact_holdouts() -> None:
    yahoo = _forward([1.5, 2.5])
    first = _forward([1.2, 2.2])

    merged, summary, report = compare_baselines(yahoo, first)

    assert len(merged) == 2
    assert report["holdouts_match_exactly"] is True
    assert report["first_nearby_baseline_rmse"] < report["yahoo_baseline_rmse"]
    assert set(summary["source"]) == {
        "yahoo_CL=F",
        "reconstructed_first_nearby",
    }


def test_compare_baselines_fails_on_holdout_mismatch() -> None:
    yahoo = _forward([1.5, 2.5])
    first = _forward([1.2, 2.2])
    first.loc[first["contract_id"].eq("B"), "contract_id"] = "C"

    with pytest.raises(RuntimeError, match="Holdout mismatch"):
        compare_baselines(yahoo, first)
