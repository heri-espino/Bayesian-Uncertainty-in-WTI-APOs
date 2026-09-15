import numpy as np
import pandas as pd

from src.volatility_regimes import classify_volatility_regimes, realized_volatility


def test_realized_volatility_is_positive_after_window():
    prices = pd.Series(100 * np.exp(np.linspace(0, 0.1, 40) + 0.01 * np.sin(np.arange(40))))
    rv = realized_volatility(prices, window=5)
    assert rv.dropna().gt(0).all()


def test_regime_labels_cover_three_buckets():
    rv = pd.Series(np.arange(1.0, 10.0))
    labels = classify_volatility_regimes(rv)
    assert set(labels.dropna()) == {"low", "medium", "high"}
