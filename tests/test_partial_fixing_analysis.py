import pandas as pd

from experiments.analyze_partial_fixing import within_contract_slope


def test_within_contract_slope_detects_declining_gap():
    frame = pd.DataFrame(
        {
            "contract_id": ["a", "a", "a", "b", "b", "b"],
            "fraction_fixed": [0.0, 0.5, 1.0, 0.0, 0.5, 1.0],
            "abs_fb_minus_pm": [3.0, 2.0, 1.0, 6.0, 5.0, 4.0],
        }
    )
    slope, contracts, rows = within_contract_slope(frame)
    assert slope == -2.0
    assert contracts == 2
    assert rows == 6


def test_within_contract_slope_ignores_single_date_contracts():
    frame = pd.DataFrame(
        {
            "contract_id": ["a", "b"],
            "fraction_fixed": [0.25, 0.25],
            "abs_fb_minus_pm": [1.0, 2.0],
        }
    )
    slope, contracts, rows = within_contract_slope(frame)
    assert slope is None
    assert contracts == 0
    assert rows == 0
