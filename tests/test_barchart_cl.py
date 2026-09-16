from pathlib import Path

import pandas as pd
import pytest

from bayesian_asian_options.barchart_cl import (
    barchart_cl_curve_on_date,
    discover_barchart_cl_histories,
    load_barchart_cl_history,
    load_barchart_cl_strip,
    load_cl_expiry_table,
)


ROOT = Path(__file__).resolve().parents[1]

SAMPLE = """Time,Open,High,Low,Latest,Change,%Change,Volume,Open Int
2026-09-04,88.35,88.84,85.92,88.57,+0.54,+0.61%,\"149,311\",\"196,888\"
2026-09-03,87.89,89.46,86.80,88.03,-0.25,-0.28%,\"198,266\",\"186,786\"
"""


def test_load_barchart_cl_history_normalizes_daily_prices(tmp_path: Path) -> None:
    path = tmp_path / "CLX26.csv"
    path.write_text(SAMPLE, encoding="utf-8")
    frame = load_barchart_cl_history(path)
    assert frame["contract"].unique().tolist() == ["CLX26"]
    assert frame["trade_date"].tolist() == [pd.Timestamp("2026-09-03"), pd.Timestamp("2026-09-04")]
    assert frame.loc[1, "latest"] == pytest.approx(88.57)
    assert frame.loc[1, "volume"] == pytest.approx(149311.0)
    assert frame.loc[1, "open_interest"] == pytest.approx(196888.0)
    assert frame.loc[1, "pct_change"] == pytest.approx(0.0061)


def test_strip_and_exact_date_curve_are_strict(tmp_path: Path) -> None:
    (tmp_path / "CLX26.csv").write_text(SAMPLE, encoding="utf-8")
    z_sample = SAMPLE.replace("88.57", "85.46").replace("88.03", "84.79")
    (tmp_path / "CLZ26.csv").write_text(z_sample, encoding="utf-8")

    panel, manifest = load_barchart_cl_strip(tmp_path, contracts=["CLX26", "CLZ26"])
    curve = barchart_cl_curve_on_date(
        panel,
        "2026-09-04",
        contracts=["CLX26", "CLZ26"],
    ).set_index("contract")
    assert curve.loc["CLX26", "settlement"] == pytest.approx(88.57)
    assert curve.loc["CLZ26", "settlement"] == pytest.approx(85.46)
    assert set(manifest["contract"]) == {"CLX26", "CLZ26"}
    assert manifest["sha256"].str.len().eq(64).all()

    with pytest.raises(ValueError, match="Missing Barchart CL histories"):
        load_barchart_cl_strip(tmp_path, contracts=["CLF27"])


def test_discovery_skips_non_contract_csv(tmp_path: Path) -> None:
    (tmp_path / "CLX26.csv").write_text(SAMPLE, encoding="utf-8")
    (tmp_path / "contract_expiries.csv").write_text(
        "contract,last_trade_date\nCLX26,2026-10-20\n",
        encoding="utf-8",
    )
    assert [path.name for path in discover_barchart_cl_histories(tmp_path)] == ["CLX26.csv"]


def test_load_expiry_table_requires_requested_contracts(tmp_path: Path) -> None:
    path = tmp_path / "contract_expiries.csv"
    path.write_text(
        "contract,last_trade_date,source\n"
        "CLX26,2026-10-20,explicit\n"
        "CLZ26,2026-11-20,explicit\n",
        encoding="utf-8",
    )
    table = load_cl_expiry_table(path, contracts=["CLX26", "CLZ26"])
    assert table["last_trade_date"].tolist() == [
        pd.Timestamp("2026-10-20"),
        pd.Timestamp("2026-11-20"),
    ]
    with pytest.raises(ValueError, match="Expiry table missing contracts"):
        load_cl_expiry_table(path, contracts=["CLF27"])


def test_committed_october_2026_curve_matches_barchart_files() -> None:
    cl_dir = ROOT / "data" / "csv" / "CL"
    histories = discover_barchart_cl_histories(cl_dir)
    assert len(histories) == 14
    panel, manifest = load_barchart_cl_strip(
        cl_dir,
        contracts=["CLX26", "CLZ26"],
    )
    curve = barchart_cl_curve_on_date(
        panel,
        "2026-09-04",
        contracts=["CLX26", "CLZ26"],
    ).set_index("contract")
    assert curve.loc["CLX26", "settlement"] == pytest.approx(88.57)
    assert curve.loc["CLZ26", "settlement"] == pytest.approx(85.46)
    assert manifest["rows"].min() >= 16
