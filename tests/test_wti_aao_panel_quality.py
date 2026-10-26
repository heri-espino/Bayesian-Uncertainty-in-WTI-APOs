"""Synthetic quality audit regression tests; no licensed option prices."""
import json
import sqlite3

import pytest

from experiments.wti_aao_panel_quality import (
    audit, audit_state, compare_raw_days,
)


def sample_db(tmp_path):
    path = tmp_path / "sample.sqlite3"
    conn = sqlite3.connect(path)
    conn.execute("""
        CREATE TABLE states (
          publisher_id INTEGER, symbol TEXT, ref_date TEXT,
          source_month TEXT, action INTEGER, flags INTEGER,
          price REAL, tie_conflict INTEGER
        )
    """)
    conn.executemany(
        "INSERT INTO states VALUES (?,?,?,?,?,?,?,?)",
        [
            (1, "a", "2025-06-02", "2025-06", 1, 3, 2.0, 0),
            (1, "b", "2025-06-02", "2025-07", 1, 1, 0.0, 0),
            (1, "c", "2025-06-03", "2025-06", 1, 3, 4.5, 0),
            (1, "d", "2025-06-03", "2025-06", 2, 3, 5.0, 0),
            (1, "e", "2025-06-04", "2025-06", 1, 11, 3.0, 0),
            (1, "f", "2025-06-04", "2025-06", 1, 3, 6.0, 1),
            (1, "g", "2026-07-01", "2026-07", 1, 1, 99., 0),
        ],
    )
    conn.commit()
    conn.close()
    return path


def test_annual_candidates_and_price_bins(tmp_path):
    conn = sqlite3.connect(sample_db(tmp_path))
    try:
        summary, dates = audit_state(conn)
    finally:
        conn.close()
    assert summary["total_candidate_keys"] == 4
    assert summary["distinct_candidate_dates"] == 3
    assert summary["by_year"]["2025"]["candidate_keys"] == 3
    assert summary["by_year"]["2025"]["actual_flagged"] == 2
    assert summary["by_year"]["2025"]["zero_price_keys"] == 1
    assert summary["by_year"]["2025"]["price_bins"]["1_to_10"] == 2
    assert summary["by_year"]["2025"]["latest_report_source_month_differs"] == 1
    assert dates == {"2025-06-02", "2025-06-03", "2026-07-01"}


def test_missing_inventory_final_reference_date():
    report = compare_raw_days(
        {"2025-06-02": 5, "2025-06-03": 2, "2025-06-04": 1},
        {"2025-06-02", "2025-06-03"}, 3,
    )
    assert report["source_dates_missing_from_candidates"] == ["2025-06-04"]
    assert report["final_source_events_on_missing_dates"] == {"2025-06-04": 1}


def test_refuse_disagreement_with_authoritative_inventory():
    with pytest.raises(ValueError, match="Expected 3"):
        compare_raw_days({"2025-06-02": 1}, {"2025-06-02"}, 3)


def test_complete_audit_never_accesses_provider(tmp_path):
    db = sample_db(tmp_path)
    summary = tmp_path / "inventory.json"
    summary.write_text(json.dumps({
        "summary": {"months_processed": 81,
                    "distinct_final_reference_dates": 4},
        "errors": [],
    }))
    result = audit(db, summary, include_barchart=False)
    assert result["inventory_final_reference_dates"] == 4
    assert result["no_vendor_api_calls"]
    assert result["total_candidate_keys"] == 4
    assert "raw_reference_dates" not in result


def test_reject_old_inventory(tmp_path):
    db = sample_db(tmp_path)
    summary = tmp_path / "inventory.json"
    summary.write_text(json.dumps({
        "summary": {"months_processed": 80,
                    "distinct_final_reference_dates": 2}, "errors": []
    }))
    with pytest.raises(ValueError, match="81-month"):
        audit(db, summary, include_barchart=False)
