from __future__ import annotations

import pandas as pd
import pytest

from bayesian_asian_options.american_futures_option import (
    american_futures_option_crr,
)
from experiments.wti_databento_external_q_iv import build_iv_panel


def test_build_iv_panel_recovers_known_sigma() -> None:
    expiry = pd.Timestamp("2026-10-15T18:30:00Z")
    asof = pd.Timestamp("2026-08-24T20:00:00Z")
    maturity = (expiry - asof).total_seconds() / (365.25 * 24 * 3600)
    true_sigma = 0.38
    rate = 0.04
    option_price = american_futures_option_crr(
        90.0,
        90.0,
        maturity,
        rate,
        true_sigma,
        "call",
        steps=100,
    )

    definitions = pd.DataFrame(
        {
            "instrument_id": [101],
            "underlying_id": [201],
            "raw_symbol": ["LOX6 C9000"],
            "underlying": ["CLX6"],
            "strike_price": [90.0],
            "expiration": [expiry.isoformat()],
            "option_type": ["call"],
        }
    )
    option_stats = pd.DataFrame(
        [
            {
                "instrument_id": 101,
                "stat_type": 3,
                "ts_ref": "2026-08-24T00:00:00Z",
                "ts_recv": asof.isoformat(),
                "stat_flags": 3,
                "price": option_price,
                "quantity": 0,
            }
        ]
    )
    futures_stats = pd.DataFrame(
        [
            {
                "instrument_id": 201,
                "stat_type": 3,
                "ts_ref": "2026-08-24T00:00:00Z",
                "ts_recv": asof.isoformat(),
                "stat_flags": 3,
                "price": 90.0,
                "quantity": 0,
            }
        ]
    )
    treasury = pd.DataFrame(
        {
            "date": [
                pd.Timestamp("2026-08-24"),
                pd.Timestamp("2026-08-24"),
            ],
            "maturity_years": [0.08, 0.25],
            "par_yield": [rate, rate],
        }
    )

    panel = build_iv_panel(
        definitions=definitions,
        option_stats=option_stats,
        futures_stats=futures_stats,
        treasury=treasury,
        steps=100,
        sigma_upper=2.0,
    )

    assert len(panel) == 1
    assert panel.loc[0, "iv_status"] == "ok"
    assert panel.loc[0, "implied_volatility"] == pytest.approx(
        true_sigma, abs=1e-7
    )
    assert panel.loc[0, "futures_settlement"] == 90.0
