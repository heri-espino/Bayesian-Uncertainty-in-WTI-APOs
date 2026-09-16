import numpy as np
import pandas as pd

from bayesian_asian_options.rates import (
    normalize_treasury_par_yields,
    treasury_curve_on_or_before,
    treasury_csv_url,
    treasury_tenor_years,
)


def test_treasury_tenor_parser_handles_uploaded_schema() -> None:
    assert treasury_tenor_years("1 Mo") == 1 / 12
    assert treasury_tenor_years("1.5 Month") == 1.5 / 12
    assert treasury_tenor_years("2 Yr") == 2.0
    assert treasury_tenor_years("Date") is None


def test_curve_selection_interpolation_and_discount_factor() -> None:
    frame = pd.DataFrame(
        {
            "Date": ["09/03/2026", "09/04/2026"],
            "1 Mo": [4.0, 4.1],
            "3 Mo": [4.2, 4.3],
            "1 Yr": [4.5, 4.6],
            "2 Yr": [4.7, 4.8],
        }
    )
    table = normalize_treasury_par_yields(frame)
    curve = treasury_curve_on_or_before(table, "2026-09-05")
    assert curve.source_date == pd.Timestamp("2026-09-04")
    rate = curve.interpolated_par_yield(0.25)
    assert np.isclose(rate, 0.043)
    assert np.isclose(curve.proxy_discount_factor(0.25), np.exp(-0.043 * 0.25))


def test_treasury_url_is_year_specific_and_official() -> None:
    url = treasury_csv_url(2026)
    assert "home.treasury.gov" in url
    assert "2026" in url
    assert "daily_treasury_yield_curve" in url
