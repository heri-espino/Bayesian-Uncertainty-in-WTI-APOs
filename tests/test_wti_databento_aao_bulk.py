"""Offline tests: no Databento API credentials, network, or chargeable calls."""

import json
from pathlib import Path

import pytest

from experiments.wti_databento_aao_bulk import (
    acquire, monthly_windows, quote_plan,
)


class Metadata:
    def __init__(self, price=0.10, missing=None):
        self.price = price
        self.missing = missing
        self.calls = []

    def list_datasets(self):
        return ["GLBX.MDP3"]

    def list_schemas(self, **kwargs):
        return ["definition", "statistics"]

    def get_record_count(self, **kwargs):
        self.calls.append(("count", kwargs))
        return 0 if kwargs["schema"] == self.missing else 100

    def get_cost(self, **kwargs):
        self.calls.append(("cost", kwargs))
        return self.price


class Timeseries:
    def __init__(self):
        self.calls = []

    def get_range(self, **kwargs):
        self.calls.append(kwargs)
        assert kwargs["stype_in"] == "parent"
        assert kwargs["symbols"] == ["AAO.OPT"]
        assert str(kwargs["path"]).endswith(".partial.dbn.zst")
        Path(kwargs["path"]).write_bytes(b"offline test fixture")


class Client:
    def __init__(self, **kwargs):
        self.metadata = Metadata(**kwargs)
        self.timeseries = Timeseries()


def test_monthly_windows_leap_and_partial_boundaries():
    assert monthly_windows("2024-02-28", "2024-03-02") == [
        ("2024-02-28", "2024-03-01"),
        ("2024-03-01", "2024-03-02"),
    ]
    with pytest.raises(ValueError):
        monthly_windows("2025-01-01", "2024-12-31")


def test_quote_never_downloads_market_data():
    client = Client()
    plan = quote_plan(client, start="2025-01-01", end="2025-02-01")
    assert plan["eligible_months"] == 1
    assert plan["eligible_quote_usd"] == pytest.approx(.20)
    assert len(client.metadata.calls) == 4
    assert not client.timeseries.calls


def test_month_requires_positive_definitions_and_statistics():
    client = Client(missing="definition")
    plan = quote_plan(client, start="2025-01-01", end="2025-02-01")
    assert plan["eligible_months"] == 0
    assert plan["eligible_quote_usd"] == 0


def test_preflight_exceeding_ceiling_refuses_before_purchase(tmp_path):
    client = Client(price=16.10)
    plan = quote_plan(client, start="2025-01-01", end="2025-02-01")
    with pytest.raises(RuntimeError, match="no new purchases"):
        acquire(
            client, plan=plan, data_dir=tmp_path / "raw",
            report_dir=tmp_path / "reports",
            max_budget_usd=40.0,
        )
    assert not client.timeseries.calls


def test_successful_download_is_resumable_without_double_charge(tmp_path):
    client = Client()
    plan = quote_plan(client, start="2025-01-01", end="2025-02-01")
    raw, reports = tmp_path / "raw", tmp_path / "reports"
    ledger = acquire(
        client, plan=plan, data_dir=raw, report_dir=reports,
        max_budget_usd=40.0,
    )
    assert len(client.timeseries.calls) == 2
    assert len(ledger["completed"]) == 2
    assert len(list(raw.glob("*.dbn.zst"))) == 2
    assert not list(raw.glob("*.partial.dbn.zst"))
    saved = json.loads(
        (reports / "bulk_acquisition_manifest.json").read_text()
    )
    assert saved["completed_all_eligible"]
    again = acquire(
        client, plan=plan, data_dir=raw, report_dir=reports,
        max_budget_usd=40.0,
    )
    assert again["total_quoted_usd"] == pytest.approx(.2)
    assert len(client.timeseries.calls) == 2


def test_untracked_local_file_refuses_purchase(tmp_path):
    client = Client()
    plan = quote_plan(client, start="2025-01-01", end="2025-02-01")
    raw = tmp_path / "raw"
    raw.mkdir()
    (raw / "aao_definition__2025-01-01__2025-02-01.dbn.zst").write_bytes(
        b"untracked"
    )
    with pytest.raises(RuntimeError, match="Untracked"):
        acquire(
            client, plan=plan, data_dir=raw,
            report_dir=tmp_path / "reports", max_budget_usd=40.0,
        )
    assert not client.timeseries.calls


def test_hard_user_maximum_rejects_higher_budget(tmp_path):
    client = Client()
    plan = quote_plan(client, start="2025-01-01", end="2025-02-01")
    with pytest.raises(ValueError, match="Unsafe budget"):
        acquire(
            client, plan=plan, data_dir=tmp_path / "raw",
            report_dir=tmp_path / "reports", max_budget_usd=41.0,
        )



def test_reacquisition_refuses_incomplete_months_without_billing(tmp_path):
    client = Client(missing="definition")
    plan = quote_plan(client, start="2025-01-01", end="2025-02-01")
    assert plan["eligible_months"] == 0
    with pytest.raises(RuntimeError, match="require all 81 months"):
        acquire(
            client, plan=plan, data_dir=tmp_path / "raw",
            report_dir=tmp_path / "reports", max_budget_usd=40.0,
        )
    assert not client.timeseries.calls
