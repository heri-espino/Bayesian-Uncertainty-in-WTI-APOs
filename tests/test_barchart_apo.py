from pathlib import Path

import numpy as np
import pandas as pd

from src.barchart_apo import (
    add_effective_moneyness,
    build_apo_panel,
    load_barchart_option_history,
    parse_barchart_option_filename,
    rank_representative_contracts,
)


def _write_history(path: Path, prices=(1.0, 0.5, 0.01), oi=(10, 12, 14)) -> None:
    pd.DataFrame(
        {
            "Time": ["2026-09-01", "2026-09-02", "2026-09-03"],
            "Open": prices,
            "High": prices,
            "Low": prices,
            "Latest": prices,
            "Change": [0.0, -0.5, -0.49],
            "%Change": ["0.0%", "-50.0%", "-98.0%"],
            "Volume": [1, 0, 0],
            "Open Int": oi,
        }
    ).to_csv(path, index=False)


def test_parse_observed_barchart_filename():
    c = parse_barchart_option_filename(
        "jaou6_10000c_daily_historical-data-09-10-2026.csv"
    )
    assert c.symbol_root == "JAO"
    assert c.expiry_label == "2026-09"
    assert c.strike == 100.0
    assert c.option_type == "call"


def test_history_loader_standardizes_fields(tmp_path):
    path = tmp_path / "jaou6_10000c_daily_historical-data.csv"
    _write_history(path)
    df = load_barchart_option_history(path, expiry_date="2026-09-30")
    assert list(df["market_price"]) == [1.0, 0.5, 0.01]
    assert list(df["open_interest"]) == [10, 12, 14]
    assert df["at_min_tick"].tolist() == [False, False, True]
    assert df["days_to_expiry"].iloc[0] == 29


def test_panel_and_moneyness_ranking(tmp_path):
    call = tmp_path / "jaou6_10000c_daily_historical-data.csv"
    put = tmp_path / "jaou6_10000p_daily_historical-data.csv"
    _write_history(call, prices=(1.5, 1.0, 0.5), oi=(100, 100, 100))
    _write_history(put, prices=(0.5, 1.0, 1.5), oi=(80, 80, 80))

    panel = build_apo_panel([call, put], expiry_dates={"2026-09": "2026-09-30"})
    expected = pd.DataFrame(
        {
            "trade_date": pd.to_datetime(["2026-09-01", "2026-09-02", "2026-09-03"]),
            "expiry_month": ["2026-09"] * 3,
            "expected_average": [95.0, 100.0, 105.0],
        }
    )
    enriched = add_effective_moneyness(panel, expected)
    ranked = rank_representative_contracts(enriched)
    assert len(ranked) == 2
    assert ranked["atm_days"].max() >= 1
    assert np.isfinite(ranked["score"]).all()
