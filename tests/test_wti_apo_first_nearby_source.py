from __future__ import annotations

import numpy as np
import pandas as pd

from experiments.wti_apo_empirical import (
    _load_first_nearby_inference,
    _return_audit,
)


def test_first_nearby_inference_preserves_roll_exclusion(tmp_path) -> None:
    dates = pd.bdate_range("2024-01-01", periods=130)
    settlements = 70.0 * np.exp(np.linspace(0.0, 0.08, len(dates)))
    frame = pd.DataFrame(
        {
            "trade_date": dates,
            "contract": ["CLG24"] * 65 + ["CLH24"] * 65,
            "settlement": settlements,
            "roll_switch": [True]
            + [False] * 64
            + [True]
            + [False] * 64,
            "missing_settlement": False,
        }
    )
    frame["log_return"] = np.log(
        frame["settlement"] / frame["settlement"].shift(1)
    )
    frame.loc[frame["roll_switch"], "log_return"] = np.nan
    frame["usable_inference_return"] = frame["log_return"].notna()
    path = tmp_path / "first_nearby.csv"
    frame.to_csv(path, index=False)

    history, returns, metadata = _load_first_nearby_inference(
        path=path,
        history_start="2024-01-01",
        valuation_date=dates[-1],
    )

    assert len(returns) == 128
    rolled = history.loc[history["roll_switch"]]
    assert rolled["log_return"].isna().all()
    assert not rolled["usable_inference_return"].any()
    assert metadata["roll_return_policy"].startswith("exclude first return")

    audit = _return_audit(history)
    assert audit.loc[audit["roll_switch"], "log_return"].isna().all()
    assert int(audit["usable_inference_return"].sum()) == 128


def test_first_nearby_inference_allows_sparse_missing_settlement(tmp_path) -> None:
    dates = pd.bdate_range("2024-01-01", periods=140)
    settlements = 70.0 * np.exp(np.linspace(0.0, 0.08, len(dates)))
    frame = pd.DataFrame(
        {
            "trade_date": dates,
            "contract": ["CLG24"] * 70 + ["CLH24"] * 70,
            "settlement": settlements,
            "roll_switch": [True]
            + [False] * 69
            + [True]
            + [False] * 69,
            "missing_settlement": False,
        }
    )
    gap = 30
    frame.loc[gap, "settlement"] = np.nan
    frame.loc[gap, "missing_settlement"] = True
    frame["log_return"] = np.log(
        frame["settlement"] / frame["settlement"].shift(1)
    )
    frame.loc[frame["roll_switch"], "log_return"] = np.nan
    frame["usable_inference_return"] = frame["log_return"].notna()
    path = tmp_path / "first_nearby_sparse.csv"
    frame.to_csv(path, index=False)

    history, returns, metadata = _load_first_nearby_inference(
        path=path,
        history_start="2024-01-01",
        valuation_date=dates[-1],
    )

    assert history["close"].isna().sum() == 1
    assert len(returns) >= 100
    assert metadata["missing_settlement_count"] == 1
    assert "do not impute" in metadata["missing_settlement_policy"]
