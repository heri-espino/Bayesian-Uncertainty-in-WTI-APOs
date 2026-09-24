from __future__ import annotations

import pandas as pd

from experiments.wti_databento_first_nearby import (
    DEFAULT_INFERENCE_END,
    DEFAULT_QUERY_END,
    _raw_cl_symbol,
    requested_contracts,
)
from experiments.wti_first_nearby_reconstruction import (
    _expiry_table,
    _settlement_panel,
)


def test_raw_cl_symbol_and_requested_contract_strip() -> None:
    assert _raw_cl_symbol("CLG24") == "CLG4"
    assert _raw_cl_symbol("CLV26") == "CLV6"

    contracts = requested_contracts("2024-01-01", "2026-09-11")
    assert contracts[0] == "CLG24"
    assert contracts[-1] == "CLV26"
    assert "CLX24" in contracts
    assert "CLF26" in contracts


def test_settlement_panel_keeps_latest_final_settlement() -> None:
    raw = pd.DataFrame(
        {
            "instrument_id": [1, 1, 2],
            "stat_type": [3, 3, 3],
            "ts_ref": [
                "2024-01-22T00:00:00+00:00",
                "2024-01-22T00:00:00+00:00",
                "2024-02-20T00:00:00+00:00",
            ],
            "ts_recv": [
                "2024-01-22T20:00:00+00:00",
                "2024-01-22T21:00:00+00:00",
                "2024-02-20T21:00:00+00:00",
            ],
            "stat_flags": [3, 3, 3],
            "price": [74.0, 74.5, 75.0],
            "symbol": ["CLG4", "CLG4", "CLH4"],
        }
    )
    mapping = pd.DataFrame(
        {
            "contract": ["CLG24", "CLH24"],
            "raw_symbol": ["CLG4", "CLH4"],
        }
    )

    out = _settlement_panel(raw, mapping)

    assert out["contract"].tolist() == ["CLG24", "CLH24"]
    assert out["settlement"].tolist() == [74.5, 75.0]


def test_expiry_table_uses_last_observed_final_settlement() -> None:
    settlements = pd.DataFrame(
        {
            "trade_date": pd.to_datetime(
                [
                    "2024-01-19",
                    "2024-01-22",
                    "2024-02-19",
                    "2024-02-20",
                    "2024-03-01",
                ]
            ),
            "contract": ["CLG24", "CLG24", "CLH24", "CLH24", "CLJ24"],
            "settlement": [73.0, 74.0, 75.0, 76.0, 77.0],
        }
    )
    mapping = pd.DataFrame(
        {
            "contract": ["CLG24", "CLH24", "CLJ24"],
            "raw_symbol": ["CLG4", "CLH4", "CLJ4"],
        }
    )

    out = _expiry_table(
        settlements,
        mapping,
        inference_end="2024-02-21",
    )

    assert out["contract"].tolist() == ["CLG24", "CLH24", "CLJ24"]
    assert out["last_trade_date"].dt.strftime("%Y-%m-%d").tolist() == [
        "2024-01-22",
        "2024-02-20",
        "2024-03-01",
    ]


def test_default_query_end_is_available_as_of_study_date() -> None:
    assert DEFAULT_QUERY_END == "2026-09-24"
    assert pd.Timestamp(DEFAULT_QUERY_END) > pd.Timestamp(DEFAULT_INFERENCE_END)
