from __future__ import annotations

import pandas as pd

from bayesian_asian_options.databento_wti import normalize_statistics
from experiments.wti_databento_external_q_audit import build_audit


def _stats(rows: list[dict[str, object]]) -> pd.DataFrame:
    return pd.DataFrame(rows)


def test_normalize_statistics_uses_ts_ref_and_cme_settlement_flags() -> None:
    frame = _stats(
        [
            {
                "instrument_id": 1,
                "stat_type": "SETTLEMENT_PRICE",
                "ts_ref": "2026-08-24T00:00:00+00:00",
                "stat_flags": 3,
            },
            {
                "instrument_id": 1,
                "stat_type": 6,
                "ts_ref": "2026-08-24T00:00:00+00:00",
                "stat_flags": 0,
            },
        ]
    )

    out = normalize_statistics(frame)

    assert out["reference_date"].tolist() == ["2026-08-24", "2026-08-24"]
    assert out["stat_type"].tolist() == [3, 6]
    assert bool(out.loc[0, "settlement_final"])
    assert bool(out.loc[0, "settlement_actual"])
    assert not bool(out.loc[0, "settlement_intraday"])


def test_build_audit_reports_settlement_coverage_without_direct_iv() -> None:
    selected = pd.DataFrame(
        {
            "instrument_id": [101, 102],
            "raw_symbol": ["LOX6 C9000", "LOX6 P9000"],
            "underlying": ["CLX6", "CLX6"],
            "strike_price": [90.0, 90.0],
            "option_type": ["call", "put"],
        }
    )
    option_stats = _stats(
        [
            {
                "instrument_id": 101,
                "stat_type": 3,
                "ts_ref": "2026-08-24T00:00:00+00:00",
                "stat_flags": 3,
            },
            {
                "instrument_id": 102,
                "stat_type": 3,
                "ts_ref": "2026-08-24T00:00:00+00:00",
                "stat_flags": 3,
            },
            {
                "instrument_id": 101,
                "stat_type": 6,
                "ts_ref": "2026-08-24T00:00:00+00:00",
                "stat_flags": 0,
            },
            {
                "instrument_id": 102,
                "stat_type": 9,
                "ts_ref": "2026-08-24T00:00:00+00:00",
                "stat_flags": 0,
            },
        ]
    )
    futures_stats = _stats(
        [
            {
                "instrument_id": 201,
                "stat_type": 3,
                "ts_ref": "2026-08-24T00:00:00+00:00",
                "stat_flags": 3,
            }
        ]
    )

    stat_summary, instrument_coverage, daily_coverage, summary = build_audit(
        selected=selected,
        option_stats=option_stats,
        futures_stats=futures_stats,
        target_start="2026-08-24",
        target_end="2026-08-24",
    )

    assert set(stat_summary["stat_type"]) == {3, 6, 9}
    assert instrument_coverage["settlement_dates"].tolist() == [1, 1]
    assert daily_coverage.loc[0, "final_settlement_instruments"] == 2
    assert summary["option_instruments_with_settlement"] == 2
    assert summary["option_instruments_with_final_settlement"] == 2
    assert summary["target_expected_dates_with_futures_settlement"] == 1
    assert summary["strict_forward_data_ready"] is True
    assert summary["glbx_direct_settlement_iv_available"] is False
