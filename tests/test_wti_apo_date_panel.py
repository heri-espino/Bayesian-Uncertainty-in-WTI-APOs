from pathlib import Path

import pandas as pd

from experiments.wti_apo_date_panel import (
    _error_summary_by_date,
    _fixing_availability,
    _sample_frames,
    _selected_dates,
    _write_sample,
)


def _audit() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "valuation_date": ["2026-09-02", "2026-09-03", "2026-09-04"],
            "n_raw_options": [10, 10, 10],
            "n_main_sample": [8, 0, 9],
            "n_positive_volume": [1, 2, 0],
            "total_volume": [12.0, 5.0, 0.0],
            "curve_available": [True, True, True],
            "eligible": [True, False, True],
        }
    )


def test_selected_dates_respect_eligibility_range_and_volume() -> None:
    audit = _audit()

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
    ) == ["2026-09-02"]


def test_selected_dates_can_be_explicitly_requested() -> None:
    audit = _audit()
    assert _selected_dates(
        audit,
        requested=["2026-09-02"],
        start_date=None,
        end_date=None,
        require_positive_volume=False,
    ) == ["2026-09-02"]


def test_fixing_availability_supports_partial_fixing() -> None:
    fixing_dates = pd.DatetimeIndex(
        pd.to_datetime(["2026-09-01", "2026-09-02", "2026-09-03"])
    )
    expiries = pd.DataFrame(
        {
            "contract": ["CLV26"],
            "last_trade_date": pd.to_datetime(["2026-09-22"]),
        }
    )
    futures = pd.DataFrame(
        {
            "trade_date": pd.to_datetime(
                ["2026-09-01", "2026-09-02", "2026-09-03"]
            ),
            "contract": ["CLV26", "CLV26", "CLV26"],
            "latest": [90.0, 91.0, 92.0],
        }
    )

    result = _fixing_availability(
        valuation_date=pd.Timestamp("2026-09-02"),
        fixing_dates=fixing_dates,
        futures=futures,
        expiry_table=expiries,
    )

    assert result["n_realized_fixings"] == 2
    assert result["n_remaining_fixings"] == 1
    assert result["fraction_fixed"] == 2 / 3
    assert result["realized_fixings_available"] is True
    assert result["curve_available"] is True
    assert result["availability_note"] == ""


def test_fixing_availability_rejects_missing_realized_fixing() -> None:
    fixing_dates = pd.DatetimeIndex(
        pd.to_datetime(["2026-09-01", "2026-09-02", "2026-09-03"])
    )
    expiries = pd.DataFrame(
        {
            "contract": ["CLV26"],
            "last_trade_date": pd.to_datetime(["2026-09-22"]),
        }
    )
    futures = pd.DataFrame(
        {
            "trade_date": pd.to_datetime(["2026-09-02", "2026-09-03"]),
            "contract": ["CLV26", "CLV26"],
            "latest": [91.0, 92.0],
        }
    )

    result = _fixing_availability(
        valuation_date=pd.Timestamp("2026-09-02"),
        fixing_dates=fixing_dates,
        futures=futures,
        expiry_table=expiries,
    )

    assert result["realized_fixings_available"] is False
    assert result["curve_available"] is True
    assert "2026-09-01:CLV26" in str(result["availability_note"])


def test_sample_frames_separate_date_and_contract_volume_filters() -> None:
    pricing = pd.DataFrame(
        {
            "valuation_date_panel": ["2026-09-02", "2026-09-02", "2026-09-04"],
            "contract_id": ["a", "b", "c"],
            "positive_volume": [True, False, False],
            "fb_error": [1.0, -1.0, 0.5],
            "pm_error": [1.1, -0.9, 0.4],
            "sigma_mode_error": [1.2, -0.8, 0.3],
            "mle_error": [1.3, -0.7, 0.2],
        }
    )
    posterior = pd.DataFrame(
        {
            "valuation_date": ["2026-09-02", "2026-09-04"],
            "sigma_posterior_mean": [0.4, 0.41],
        }
    )

    samples = _sample_frames(pricing, posterior, _audit())

    all_dates, _, _ = samples["all_dates"]
    positive_dates, positive_dates_posterior, _ = samples["positive_volume_dates"]
    positive_contracts, positive_contracts_posterior, _ = samples[
        "positive_volume_contracts"
    ]

    assert len(all_dates) == 3
    assert positive_dates["contract_id"].tolist() == ["a", "b"]
    assert positive_dates_posterior["valuation_date"].tolist() == ["2026-09-02"]
    assert positive_contracts["contract_id"].tolist() == ["a"]
    assert positive_contracts_posterior["valuation_date"].tolist() == ["2026-09-02"]


def test_error_summary_is_recomputed_after_contract_filtering() -> None:
    pricing = pd.DataFrame(
        {
            "valuation_date_panel": ["2026-09-02", "2026-09-02"],
            "fb_error": [1.0, -1.0],
            "pm_error": [2.0, -2.0],
            "sigma_mode_error": [3.0, -3.0],
            "mle_error": [4.0, -4.0],
        }
    )
    summary = _error_summary_by_date(pricing).set_index("method")
    assert summary.loc["Full Bayes", "n"] == 2
    assert summary.loc["Full Bayes", "mean_error"] == 0.0
    assert summary.loc["Full Bayes", "mae"] == 1.0
    assert summary.loc["Posterior mean", "rmse"] == 2.0


def test_sample_writer_namespaces_outputs(tmp_path: Path) -> None:
    pricing = pd.DataFrame(
        {
            "valuation_date_panel": ["2026-09-02"],
            "positive_volume": [True],
            "fb_error": [0.1],
            "pm_error": [0.2],
            "sigma_mode_error": [0.3],
            "mle_error": [0.4],
        }
    )
    posterior = pd.DataFrame(
        {"valuation_date": ["2026-09-02"], "sigma_posterior_mean": [0.4]}
    )

    _write_sample(
        panel_dir=tmp_path,
        sample_name="positive_volume_contracts",
        pricing=pricing,
        posterior=posterior,
        description="test sample",
        apo_expiry="2026-10",
    )

    sample_dir = tmp_path / "positive_volume_contracts"
    assert (sample_dir / "panel_contract_pricing.csv").exists()
    assert (sample_dir / "panel_error_summary.csv").exists()
    assert (sample_dir / "panel_overall_error_summary.csv").exists()
    assert (sample_dir / "panel_posterior_summary.csv").exists()
    assert (sample_dir / "sample_manifest.json").exists()
    assert not (tmp_path / "panel_contract_pricing.csv").exists()
