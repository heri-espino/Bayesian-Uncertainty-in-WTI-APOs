import numpy as np
import pandas as pd

from bayesian_asian_options.wti_yahoo_futures import (
    cl_contract_strip,
    cl_contract_symbol,
    compare_futures_reference,
    expiry_table_from_yahoo_metadata,
    extract_yahoo_settlement_date,
    futures_curve_on_date,
    normalize_yahoo_contract_history,
    parse_cl_contract,
    reconstruct_first_nearby_history,
)


def test_cl_symbols_and_strip() -> None:
    assert cl_contract_symbol(2026, 10) == "CLV26"
    assert cl_contract_symbol(2026, 10, yahoo=True) == "CLV26.NYM"
    decoded = parse_cl_contract("CLX26.NYM")
    assert (decoded.year, decoded.month, decoded.contract) == (2026, 11, "CLX26")
    strip = cl_contract_strip("2026-09-01", "2026-10-31", lead_months=2)
    assert strip[0] == "CLV26"
    assert "CLX26" in strip
    assert "CLZ26" in strip


def test_normalize_yahoo_contract_history() -> None:
    frame = pd.DataFrame(
        {
            "Date": pd.to_datetime(["2026-09-04", "2026-09-03"]),
            "Open": [91.0, 90.0],
            "High": [92.0, 91.0],
            "Low": [89.0, 88.0],
            "Close": [91.48, 90.50],
            "Volume": [100, 200],
        }
    ).set_index("Date")
    out = normalize_yahoo_contract_history(frame, "CLV26")
    assert out["contract"].unique().tolist() == ["CLV26"]
    assert out["close"].tolist() == [90.50, 91.48]
    assert out["trade_date"].iloc[-1] == pd.Timestamp("2026-09-04")


def test_extract_yahoo_settlement_date() -> None:
    epoch = int(pd.Timestamp("2026-09-22", tz="UTC").timestamp())
    date, source = extract_yahoo_settlement_date({"expireDate": epoch})
    assert date == pd.Timestamp("2026-09-22")
    assert source == "yahoo_info:expireDate"


def test_reconstruction_excludes_roll_return() -> None:
    panel = pd.DataFrame(
        {
            "trade_date": pd.to_datetime(
                ["2026-09-21", "2026-09-22", "2026-09-23", "2026-09-24"]
            ),
            "contract": ["CLV26", "CLV26", "CLX26", "CLX26"],
            "close": [100.0, 101.0, 95.0, 96.0],
        }
    )
    expiries = pd.DataFrame(
        {
            "contract": ["CLV26", "CLX26"],
            "last_trade_date": pd.to_datetime(["2026-09-22", "2026-10-20"]),
        }
    )
    out = reconstruct_first_nearby_history(panel, expiries)
    assert out["contract"].tolist() == ["CLV26", "CLV26", "CLX26", "CLX26"]
    assert np.isnan(out.loc[2, "log_return"])
    assert not bool(out.loc[2, "usable_inference_return"])
    assert np.isclose(out.loc[3, "log_return"], np.log(96.0 / 95.0))


def test_exact_date_curve_and_reference_comparison() -> None:
    panel = pd.DataFrame(
        {
            "trade_date": pd.to_datetime(["2026-09-04", "2026-09-04"]),
            "contract": ["CLV26", "CLX26"],
            "close": [91.48, 88.57],
        }
    )
    curve = futures_curve_on_date(panel, "2026-09-04", contracts=["CLV26", "CLX26"])
    assert curve["settlement"].tolist() == [91.48, 88.57]

    reference = pd.DataFrame(
        {
            "trade_date": ["2026-09-04"],
            "contract": ["CLV26"],
            "close": [91.48],
        }
    )
    checked = compare_futures_reference(panel, reference)
    assert checked.loc[0, "absolute_difference"] == 0.0


def test_expiry_table_requires_complete_metadata() -> None:
    metadata = pd.DataFrame(
        {
            "contract": ["CLV26", "CLX26"],
            "settlement_date": ["2026-09-22", "2026-10-20"],
            "settlement_date_source": ["yahoo_info:expireDate", "yahoo_info:expireDate"],
        }
    )
    table = expiry_table_from_yahoo_metadata(metadata)
    assert table["last_trade_date"].tolist() == [
        pd.Timestamp("2026-09-22"),
        pd.Timestamp("2026-10-20"),
    ]
