"""Offline Barchart availability checks; no DBN state or credentials."""
import json

from experiments.wti_aao_barchart_inventory import inventory


def test_absent_csv_root(tmp_path):
    report = inventory(tmp_path / "missing")
    assert report["available"] is False
    assert report["csv_root_exists"] is False
    assert report["no_databento_requests"] is True


def test_csv_present_but_not_jao_history(tmp_path):
    (tmp_path / "other.csv").write_text("Time,Latest\n2026-06-01,1.00\n")
    report = inventory(tmp_path)
    assert report["available"] is False
    assert report["all_csv_files"] == 1
    assert report["barchart_option_history_files"] == 0


def test_jao_history_without_any_sqlite(tmp_path):
    root = tmp_path / "csv" / "sep2026"
    root.mkdir(parents=True)
    (root / "jaou6_10000c_price-history-09-12-2026.csv").write_text(
        "Time,Latest,Volume,Open Int\n"
        "2026-06-01,1.20,10,50\n"
        "2026-06-02,1.30,0,49\n"
    )
    report = inventory(tmp_path / "csv")
    assert report["available"] is True
    assert report["barchart_option_history_files"] == 1
    assert report["distinct_option_contracts"] == 1
    assert report["deduplicated_history_rows"] == 2
    assert report["rows_with_latest_price"] == 2
    assert report["distinct_history_dates"] == 2
    assert report["first_history_date"] == "2026-06-01"
    assert report["last_history_date"] == "2026-06-02"
    assert report["barchart_aao_overlap_calculated"] is False
    assert report["contract_price_parity_checked"] is False
