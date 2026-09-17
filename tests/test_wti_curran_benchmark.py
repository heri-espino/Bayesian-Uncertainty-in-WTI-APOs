import json

import numpy as np
import pandas as pd

from experiments.wti_curran_benchmark import _discover_runs, _posterior_draws


def _write_legacy_run(tmp_path):
    run_dir = tmp_path / "2026-09-04_202610"
    run_dir.mkdir()
    returns = np.linspace(-0.015, 0.018, 80)
    audit = pd.DataFrame(
        {
            "log_return": returns,
            "usable_inference_return": np.ones(len(returns), dtype=bool),
        }
    )
    audit.to_csv(run_dir / "inference_return_audit.csv", index=False)
    pd.DataFrame({"contract_id": ["x"]}).to_csv(
        run_dir / "contract_pricing.csv", index=False
    )
    pd.DataFrame(
        {
            "fixing_status": ["remaining"],
            "fixing_date": ["2026-10-01"],
            "settlement": [80.0],
        }
    ).to_csv(run_dir / "apo_fixing_state.csv", index=False)
    manifest = {
        "valuation_date": "2026-09-04",
        "n_usable_returns": len(returns),
        "mcmc": {
            "chains": 2,
            "n_iter_per_chain": 300,
            "burn_in_per_chain": 60,
            "seed": 1234,
        },
        "discounting": {"discount_factor": 0.99},
    }
    (run_dir / "manifest.json").write_text(json.dumps(manifest), encoding="utf-8")
    return run_dir, manifest


def test_discover_runs_accepts_legacy_run_without_posterior_npz(tmp_path):
    run_dir, _ = _write_legacy_run(tmp_path)
    assert _discover_runs(tmp_path, "2026-10") == [run_dir]


def test_posterior_draws_reconstructs_legacy_run(tmp_path):
    run_dir, manifest = _write_legacy_run(tmp_path)
    draws, source = _posterior_draws(run_dir, manifest)
    assert source == "reconstructed_from_inference_return_audit"
    assert draws.shape == (2 * (300 - 60),)
    assert np.all(np.isfinite(draws))
    assert np.all(draws > 0)
