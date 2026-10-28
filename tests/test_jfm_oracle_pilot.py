"""Small smoke checks for the JFM synthetic oracle pilot (no external data)."""
from dataclasses import replace

import numpy as np

from experiments.jfm_oracle_pilot import Pilot, _mc_correlated_average, run


def test_jfm_monte_carlo_reuses_contract_drivers_and_has_finite_se():
    cfg = replace(
        Pilot(), mc_pairs=600, strikes=(0.0,),
        volatilities=(0.2,), correlations=(1.0, 0.75, 0.5),
    )
    rows = _mc_correlated_average(cfg, 0.2, 0.0, 783)
    assert [row["rho"] for row in rows] == [1.0, 0.75, 0.5]
    expected = 100.0 * np.exp(-cfg.risk_free_rate * cfg.fixing_days[-1] / 252.0)
    # For strike zero, the risk-neutral expected average equals the forward.
    for row in rows:
        assert np.isfinite(row["mc_reference_price"])
        assert row["mc_standard_error"] > 0
        assert abs(row["mc_reference_price"] - expected) < 1.0
    assert rows[0]["paired_difference_standard_error"] == 0.0


def test_jfm_pilot_writes_reproducible_structured_artifacts(tmp_path):
    cfg = replace(
        Pilot(),
        historical_sizes=(21,),
        volatilities=(0.2,),
        strikes=(100.0,),
        repetitions=2,
        sigma_grid_points=33,
        mc_pairs=100,
    )
    out = run(cfg, tmp_path)
    assert (out / "pilot_pricing.csv").is_file()
    assert (out / "pilot_decisions.csv").is_file()
    assert (out / "pilot_correlation_mc.csv").is_file()
    assert (out / "pilot_manifest.json").is_file()
    assert (out / "NOTES.md").is_file()
    import json
    manifest = json.loads((out / "pilot_manifest.json").read_text(encoding="utf-8"))
    assert manifest["status"] == "PILOT_ONLY_NOT_CONFIRMATORY"
    assert set(manifest["outputs_sha256"]) == {
        "pilot_pricing.csv", "pilot_decisions.csv", "pilot_correlation_mc.csv"
    }


def test_jfm_correlation_config_rejects_invalid_drivers():
    from pytest import raises
    cfg = replace(Pilot(), mc_pairs=10, correlations=(1.2,))
    with raises(ValueError, match="Correlation weights"):
        _mc_correlated_average(cfg, 0.2, 100.0, 12)
