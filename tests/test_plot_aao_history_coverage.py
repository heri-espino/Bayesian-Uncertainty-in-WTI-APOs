"""Synthetic monthly fixture; no Databento time series or priced records."""
import pytest

from scripts.plot_aao_history_coverage import extract_coverage


def report():
    months = []
    y, m = 2020, 1
    for _ in range(81):
        months.append({
            "month": f"{y:04d}-{m:02d}",
            "definitions": {"top_asset": {"AAO": 100}},
            "statistics": {"final_events": 9,
                           "final_actual_events": 5,
                           "final_theoretical_events": 4},
        })
        m += 1
        if m == 13:
            y, m = y + 1, 1
    return {"errors": [], "months": months,
            "summary": {"months_processed": 81}}


def test_accept_complete_81_months():
    assert len(extract_coverage(report())) == 81


def test_reject_previous_80_months():
    data = report()
    data["months"].pop()
    data["summary"]["months_processed"] = 80
    with pytest.raises(ValueError, match="81-month"):
        extract_coverage(data)


def test_reject_inconsistent_flag_counts():
    data = report()
    data["months"][4]["statistics"]["final_actual_events"] += 1
    with pytest.raises(ValueError, match="Inconsistent"):
        extract_coverage(data)


def test_reject_duplicate_month():
    data = report()
    data["months"][5]["month"] = data["months"][6]["month"]
    with pytest.raises(ValueError, match="Missing, repeated"):
        extract_coverage(data)


def test_reject_non_aao_definitions():
    data = report()
    data["months"][5]["definitions"]["top_asset"] = {"LO": 100}
    with pytest.raises(ValueError, match="No AAO"):
        extract_coverage(data)
