"""Local-only tests for the WTI APO historical coverage decision gate."""

from __future__ import annotations

import pandas as pd
import pytest

from experiments.wti_aao_existing_attrition import (
    _summarize_holdouts,
    build_attrition_report,
)
from experiments.wti_databento_aao_feasibility import (
    _anchor,
    _is_within_schema_range,
    _normalize_parent,
    _safe_exception,
    probe_aao_quotes,
)


def _raw_panel() -> pd.DataFrame:
    rows = []
    for expiry in ("2026-10", "2027-03"):
        for date in ("2026-08-24", "2026-08-25", "2026-08-26"):
            rows += [
                {
                    "trade_date": date,
                    "expiry_month": expiry,
                    "contract_id": f"{expiry}-{date}-{strike}",
                    "option_type": "call",
                    "strike": strike,
                    "market_price": 1.0,
                    "volume": 3 if strike == 91 else 0,
                    "open_interest": 100,
                }
                for strike in (90, 91, 92)
            ]
    rows.append(dict(rows[-1]))  # one genuinely duplicated option/date key
    return pd.DataFrame(rows)


def test_holdout_distinct_rows_not_repeated_methods() -> None:
    frame = pd.DataFrame({
        "apo_expiry": ["2026-10", "2026-10", "2026-10"],
        "valuation_date": ["2026-08-26"] * 3,
        "contract_id": ["a", "a", "b"],
        "method": ["expanding", "previous_day", "expanding"],
    })
    counts = _summarize_holdouts(frame)
    assert len(counts) == 1
    assert counts.iloc[0]["n_forward_holdout_keys"] == 2


def test_existing_history_attrition_tracks_earlier_smile_and_unmatched() -> None:
    raw = _raw_panel()
    a = pd.DataFrame({
        "valuation_date": ["2026-08-24", "2026-08-25", "2026-08-26"],
        "n_main_sample": [3, 3, 3],
        "eligible": [True, True, True],
        "n_positive_volume": [1, 1, 1],
        "curve_available": [True, True, True],
        "realized_fixings_available": [True, True, True],
    })
    b = a.copy()
    b["n_main_sample"] = [0, 3, 3]
    b["eligible"] = [False, True, True]
    targets = pd.DataFrame({
        "apo_expiry": ["2026-10", "2026-10", "2026-10"],
        "valuation_date": ["2026-08-25", "2026-08-25", "2026-08-26"],
        "contract_id": ["a", "a", "b"],
    })
    details, report = build_attrition_report(
        raw, {"2026-10": a, "2027-03": b},
        targets, min_smile_contracts=3,
    )
    x = details[details["apo_expiry"].eq("2026-10")].reset_index(drop=True)
    y = details[details["apo_expiry"].eq("2027-03")].reset_index(drop=True)
    assert not bool(x.loc[0, "has_strictly_earlier_smile_date"])
    assert bool(x.loc[1, "has_strictly_earlier_smile_date"])
    assert not bool(y.loc[1, "has_strictly_earlier_smile_date"])
    assert bool(y.loc[2, "has_strictly_earlier_smile_date"])
    assert report["raw_market_rows"] == 19
    assert report["raw_distinct_market_keys"] == 18
    assert report["recorded_forward_unique_contract_date_keys"] == 2
    assert report["recorded_forward_unique_dates"] == 2
    assert details["n_duplicate_option_keys"].sum() == 1


def test_existing_history_rejects_missing_or_unusable_audits() -> None:
    with pytest.raises(ValueError, match="No Barchart"):
        build_attrition_report(
            _raw_panel(), {"2026-10": pd.DataFrame()},
            pd.DataFrame(), min_smile_contracts=3,
        )
    with pytest.raises(ValueError, match="positive"):
        build_attrition_report(
            _raw_panel(), {"2026-10": pd.DataFrame()},
            pd.DataFrame(), min_smile_contracts=0,
        )


class _Metadata:
    def __init__(self):
        self.calls = []

    def list_datasets(self):
        self.calls.append(("list_datasets",))
        return ["GLBX.MDP3"]

    def list_schemas(self, **kwargs):
        self.calls.append(("list_schemas", kwargs))
        return ["definition", "statistics"]

    def get_dataset_range(self, **kwargs):
        self.calls.append(("get_dataset_range", kwargs))
        return {
            "start": "2022-01-01",
            "end": "2027-01-01",
            "schema": {
                "definition": {"start": "2023-01-01", "end": "2027-01-01"},
                "statistics": {"start": "2024-01-01", "end": "2027-01-01"},
            },
        }

    def get_cost(self, **kwargs):
        self.calls.append(("get_cost", kwargs))
        assert kwargs["stype_in"] == "parent"
        assert kwargs["symbols"][0] in {"AAO.OPT", "AO.OPT", "LO.OPT"}
        parent = kwargs["symbols"][0]
        if parent == "AO.OPT":
            raise ValueError("No matching AO records for quote")
        if parent == "LO.OPT":
            return 0.20
        return 0.25 if kwargs["schema"] == "definition" else 0.40

    def get_record_count(self, **kwargs):
        self.calls.append(("get_record_count", kwargs))
        assert kwargs["stype_in"] == "parent"
        parent = kwargs["symbols"][0]
        if parent == "LO.OPT":
            return 26411 if kwargs["schema"] == "definition" else 863567
        if parent == "AAO.OPT":
            return 17 if kwargs["schema"] == "definition" else 8
        raise ValueError("No matching AO records")


class _Symbology:
    def __init__(self):
        self.calls = []

    def resolve(self, **kwargs):
        self.calls.append(kwargs)
        assert kwargs["stype_in"] == "parent"
        assert kwargs["stype_out"] == "instrument_id"
        parent = kwargs["symbols"][0]
        return {
            "result": {
                parent: ([{"d0": kwargs["start_date"], "d1": kwargs["end_date"], "s": "TEST"}]
                         if parent == "AAO.OPT" else [])
            },
            "message": "OK" if parent == "AAO.OPT" else "Not found",
            "not_found": [] if parent == "AAO.OPT" else [parent],
        }


class _FakeClient:
    def __init__(self):
        self.metadata = _Metadata()
        self.symbology = _Symbology()
        # No timeseries/batch attribute exists: an accidental download fails.


def test_quote_only_candidate_resolution_never_downloads() -> None:
    client = _FakeClient()
    report = probe_aao_quotes(
        client, years=(2025,), parents=("AAO", "AO"),
        max_quote_usd=0.7,
    )
    assert report["no_timeseries_download"]
    assert report["historical_aao_settlements_confirmed"] is False
    assert report["candidate_parents"] == ["AAO.OPT", "AO.OPT"]
    assert len(report["probes"]) == 2
    found, missing = report["probes"]
    assert found["parent_candidate"] == "AAO.OPT"
    assert found["start_inclusive"] == "2025-06-11"
    assert found["parent_symbology_verified"]
    assert found["mapping_count"] == 1
    assert found["record_counts"] == {"definition": 17, "statistics": 8}
    assert found["status"] == (
        "metadata_records_reported_not_final_settlement_proven"
    )
    assert found["quotes_usd"] == {"definition": 0.25, "statistics": 0.4}
    assert found["within_quote_ceiling"]
    assert found["total_one_day_quote_usd"] == 0.65
    assert not missing["parent_symbology_verified"]
    assert missing["status"] == "inconclusive_metadata_query"
    assert not missing["metadata_records_reported"]
    assert len(client.symbology.calls) == 3
    assert report["positive_control"]["parent_candidate"] == "LO.OPT"
    assert report["positive_control"]["mapping_count"] == 0
    assert report["positive_control"]["record_counts"]["definition"] == 26411
    assert report["positive_control_metadata_pass"]
    assert len([n for n in client.metadata.calls if n[0] == "get_cost"]) == 6


def test_schema_range_blocks_outside_year_quote() -> None:
    client = _FakeClient()
    report = probe_aao_quotes(client, years=(2022,), parents=("AAO",))
    assert report["probes"][0]["status"] == (
        "definition_schema_day_outside_available_range"
    )
    assert len(client.symbology.calls) == 1  # LO.OPT control only
    queried_dates = [
        item[1]["start"]
        for item in client.metadata.calls
        if item[0] == "get_cost"
    ]
    assert queried_dates == ["2026-08-24", "2026-08-24"]


def test_missing_dataset_is_no_go() -> None:
    client = _FakeClient()
    client.metadata.list_datasets = lambda: ["SOME.OTHER"]
    report = probe_aao_quotes(client, years=(2025,), parents=("AAO",))
    assert not report["dataset_accessible"]
    assert report["probes"] == []


def test_range_boundary_and_error_redaction(monkeypatch) -> None:
    ranges = {"schema": {"definition": {
        "start": "2025-06-17", "end": "2025-06-18",
    }}}
    assert _is_within_schema_range(
        "2025-06-17", ranges=ranges, schema="definition"
    )
    assert not _is_within_schema_range(
        "2025-06-18", ranges=ranges, schema="definition"
    )
    monkeypatch.setenv("DATABENTO_API_KEY", "db_secret_test_key")
    assert "db_secret_test_key" not in _safe_exception(
        RuntimeError("token=db_secret_test_key")
    )
    with pytest.raises(ValueError, match="finite positive"):
        probe_aao_quotes(_FakeClient(), max_quote_usd=-1)


def test_normalize_parent_aliases_and_reject_other_asset_classes() -> None:
    assert _normalize_parent("aao") == "AAO.OPT"
    assert _normalize_parent(" AO.OPT ") == "AO.OPT"
    with pytest.raises(ValueError, match="Expected"):
        _normalize_parent("AAO.FUT")
    with pytest.raises(ValueError, match="Expected"):
        _normalize_parent("AAO.OPT.FUT")


@pytest.mark.parametrize("year,start", [
    (2023, "2023-06-14"),
    (2024, "2024-06-12"),
    (2025, "2025-06-11"),
    (2026, "2026-06-10"),
])
def test_anchor_is_second_june_wednesday(year: int, start: str) -> None:
    observed, end = _anchor(year)
    assert observed == start
    assert pd.Timestamp(end) == pd.Timestamp(start) + pd.Timedelta(days=1)
    assert pd.Timestamp(observed).weekday() == 2


def test_explicit_databento_parent_and_bare_code_deduplicate() -> None:
    client = _FakeClient()
    report = probe_aao_quotes(
        client, years=(2026,), parents=("AAO", "AAO.OPT"),
    )
    assert report["candidate_parents"] == ["AAO.OPT"]
    assert len(report["probes"]) == 1
    assert client.symbology.calls[0]["symbols"] == ["AAO.OPT"]
    assert client.symbology.calls[1]["symbols"] == ["LO.OPT"]


def test_symbology_failure_does_not_suppress_metadata_cost_or_count() -> None:
    client = _FakeClient()
    def raising_resolve(**kwargs):
        if kwargs["symbols"] == ["AAO.OPT"]:
            raise RuntimeError("Unresolvable parent despite available metadata")
        return _Symbology().resolve(**kwargs)
    client.symbology.resolve = raising_resolve
    result = probe_aao_quotes(
        client, years=(2025,), parents=("AAO.OPT",),
    )
    row = result["probes"][0]
    assert "Unresolvable" in row["error"]
    assert row["record_counts"]["statistics"] == 8
    assert row["quotes_usd"]["statistics"] == 0.40
    assert row["status"] == "metadata_records_reported_not_final_settlement_proven"
    assert result["historical_aao_settlements_confirmed"] is False


def test_positive_control_does_not_prove_aao_availability() -> None:
    client = _FakeClient()
    result = probe_aao_quotes(
        client, years=(2025,), parents=("AO.OPT",),
    )
    assert result["positive_control_metadata_pass"]
    assert result["probes"][0]["status"] == "inconclusive_metadata_query"
    assert result["historical_aao_settlements_confirmed"] is False
