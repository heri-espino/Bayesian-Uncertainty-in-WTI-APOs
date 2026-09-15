from pathlib import Path

import numpy as np
import pandas as pd

from bayesian_asian_options.barchart_apo import (
    add_effective_moneyness,
    build_apo_panel,
    discover_barchart_histories,
    load_barchart_option_history,
    parse_barchart_option_filename,
    rank_representative_contracts,
)


def _write(path: Path, prices=(1.0, 0.5, 0.01), oi=(10, 12, 14)) -> None:
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


def test_parse_observed_filename():
    c = parse_barchart_option_filename("jaou6_10000c_price-history-09-12-2026.csv")
    assert c.root_symbol == "JAOU6"
    assert c.expiry_label == "2026-09"
    assert c.strike == 100.0
    assert c.option_type == "call"


def test_recursive_discovery_ignores_aggregate_csv(tmp_path):
    nested = tmp_path / "sep2026"
    nested.mkdir()
    history = nested / "jaou6_10000c_price-history-09-12-2026.csv"
    _write(history)
    (tmp_path / "option_series_properties.csv").write_text("x\n1\n", encoding="utf-8")
    assert discover_barchart_histories(tmp_path) == [history]


def test_loader_flags_folder_mismatch(tmp_path):
    wrong = tmp_path / "jun2029"
    wrong.mkdir()
    path = wrong / "jaou8_6151c_price-history-09-14-2026.csv"
    _write(path)
    df = load_barchart_option_history(path)
    assert not bool(df["folder_expiry_match"].iloc[0])
    assert df["expiry_month"].iloc[0] == "2028-09"


def test_panel_moneyness_and_ranking(tmp_path):
    folder = tmp_path / "sep2026"
    folder.mkdir()
    call = folder / "jaou6_10000c_price-history-09-12-2026.csv"
    put = folder / "jaou6_10000p_price-history-09-12-2026.csv"
    _write(call, prices=(1.5, 1.0, 0.5), oi=(100, 100, 100))
    _write(put, prices=(0.5, 1.0, 1.5), oi=(80, 80, 80))
    panel = build_apo_panel([call, put])
    expected = pd.DataFrame(
        {
            "trade_date": pd.to_datetime(["2026-09-01", "2026-09-02", "2026-09-03"]),
            "expiry_month": ["2026-09"] * 3,
            "expected_average": [95.0, 100.0, 105.0],
        }
    )
    enriched = add_effective_moneyness(panel, expected)
    ranking = rank_representative_contracts(enriched)
    assert len(ranking) == 2
    assert ranking["atm_days"].max() >= 1
    assert np.isfinite(ranking["representative_score"]).all()
