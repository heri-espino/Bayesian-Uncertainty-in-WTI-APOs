from __future__ import annotations

import pandas as pd

from bayesian_asian_options.databento_wti import (
    final_settlements,
    normalize_option_definitions,
)


def test_final_settlements_keeps_latest_final_eod_value() -> None:
    frame = pd.DataFrame(
        [
            {
                "instrument_id": 1,
                "stat_type": 3,
                "ts_ref": "2026-08-24T00:00:00Z",
                "ts_recv": "2026-08-24T18:00:00Z",
                "stat_flags": 0,
                "price": 1.10,
            },
            {
                "instrument_id": 1,
                "stat_type": 3,
                "ts_ref": "2026-08-24T00:00:00Z",
                "ts_recv": "2026-08-24T18:10:00Z",
                "stat_flags": 1,
                "price": 1.20,
            },
            {
                "instrument_id": 1,
                "stat_type": 3,
                "ts_ref": "2026-08-24T00:00:00Z",
                "ts_recv": "2026-08-24T18:20:00Z",
                "stat_flags": 1,
                "price": 1.25,
            },
            {
                "instrument_id": 1,
                "stat_type": 3,
                "ts_ref": "2026-08-24T00:00:00Z",
                "ts_recv": "2026-08-24T17:00:00Z",
                "stat_flags": 9,
                "price": 1.30,
            },
        ]
    )

    out = final_settlements(frame)

    assert len(out) == 1
    assert out.loc[0, "price"] == 1.25
    assert bool(out.loc[0, "settlement_final"])
    assert not bool(out.loc[0, "settlement_intraday"])


def test_normalize_option_definitions_parses_expiration_and_ids() -> None:
    frame = pd.DataFrame(
        {
            "instrument_id": ["101"],
            "underlying_id": ["201"],
            "raw_symbol": ["LOX6 C9000"],
            "underlying": ["CLX6"],
            "strike_price": ["90.0"],
            "expiration": ["2026-10-15T18:30:00Z"],
            "option_type": ["call"],
        }
    )

    out = normalize_option_definitions(frame)

    assert int(out.loc[0, "instrument_id"]) == 101
    assert int(out.loc[0, "underlying_id"]) == 201
    assert out.loc[0, "expiration_timestamp"] == pd.Timestamp(
        "2026-10-15T18:30:00Z"
    )
