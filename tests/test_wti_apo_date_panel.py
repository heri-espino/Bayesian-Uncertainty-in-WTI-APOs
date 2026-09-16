import pandas as pd

from experiments.wti_apo_date_panel import _selected_dates


def test_selected_dates_respect_eligibility_range_and_volume() -> None:
    audit = pd.DataFrame(
        {
            "valuation_date": ["2026-09-02", "2026-09-03", "2026-09-04"],
            "n_raw_options": [10, 10, 10],
            "n_main_sample": [8, 0, 9],
            "n_positive_volume": [0, 2, 3],
            "total_volume": [0.0, 5.0, 12.0],
            "curve_available": [True, True, True],
            "eligible": [True, False, True],
        }
    )

    assert _selected_dates(
        audit,
        requested=None,
        start_date="2026-09-03",
        end_date=None,
        require_positive_volume=False,
    ) == ["2026-09-04"]

    assert _selected_dates(
        audit,
        requested=None,
        start_date=None,
        end_date=None,
        require_positive_volume=True,
    ) == ["2026-09-04"]


def test_selected_dates_can_be_explicitly_requested() -> None:
    audit = pd.DataFrame(
        {
            "valuation_date": ["2026-09-02", "2026-09-04"],
            "n_raw_options": [10, 10],
            "n_main_sample": [8, 9],
            "n_positive_volume": [0, 3],
            "total_volume": [0.0, 12.0],
            "curve_available": [True, True],
            "eligible": [True, True],
        }
    )
    assert _selected_dates(
        audit,
        requested=["2026-09-02"],
        start_date=None,
        end_date=None,
        require_positive_volume=False,
    ) == ["2026-09-02"]
