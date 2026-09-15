import numpy as np
import pandas as pd
import pytest

from bayesian_asian_options.asian_futures_pricing import asian_futures_arithmetic_call_mc
from bayesian_asian_options.asian_pricing import asian_arithmetic_call_mc
from bayesian_asian_options.wti_yahoo import dataframe_sha256, normalize_yahoo_history, prepare_wti_model_sample


def _history(values):
    return pd.DataFrame(
        {
            "Date": pd.date_range("2024-01-02", periods=len(values), freq="B"),
            "Open": values,
            "High": np.asarray(values) + 1.0,
            "Low": np.asarray(values) - 1.0,
            "Close": values,
            "Volume": np.arange(len(values)) + 100,
        }
    ).set_index("Date")


def test_normalize_and_prepare_positive_wti_history():
    raw = _history(np.array([70.0, 71.0, 69.5, 72.0]))
    clean = normalize_yahoo_history(raw)
    sample = prepare_wti_model_sample(clean, start="2024-01-01")
    assert list(clean.columns) == ["date", "open", "high", "low", "close", "volume"]
    assert sample.n_prices == 4
    assert sample.n_returns == 3
    expected = np.diff(np.log([70.0, 71.0, 69.5, 72.0]))
    assert np.allclose(sample.log_returns, expected)


def test_nonpositive_price_is_not_silently_removed():
    raw = _history(np.array([20.0, -5.0, 10.0, 11.0]))
    with pytest.raises(ValueError, match="positive prices"):
        prepare_wti_model_sample(raw, start="2024-01-01")


def test_snapshot_hash_is_deterministic():
    clean = normalize_yahoo_history(_history(np.array([70.0, 71.0, 72.0])))
    assert dataframe_sha256(clean) == dataframe_sha256(clean.copy())


def test_futures_wrapper_is_zero_drift_special_case():
    kwargs = dict(S0=80.0, K=80.0, r=0.04, sigma=0.25, T=0.5, n_steps=20, n_paths=4000, seed=123)
    generic = asian_arithmetic_call_mc(q=kwargs["r"], **kwargs)
    futures = asian_futures_arithmetic_call_mc(
        kwargs["S0"], kwargs["K"], kwargs["r"], kwargs["sigma"], kwargs["T"],
        n_steps=kwargs["n_steps"], n_paths=kwargs["n_paths"], seed=kwargs["seed"]
    )
    assert futures.price == pytest.approx(generic.price, rel=0, abs=1e-12)
