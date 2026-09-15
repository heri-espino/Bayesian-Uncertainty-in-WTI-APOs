"""Data-driven volatility-regime labels for the empirical WTI application."""

from __future__ import annotations

import numpy as np
import pandas as pd


def realized_volatility(
    prices: pd.Series,
    *,
    window: int = 21,
    periods_per_year: int = 252,
) -> pd.Series:
    """Rolling annualized realized volatility from log returns."""
    if window < 2:
        raise ValueError("window must be at least two")
    p = pd.to_numeric(prices, errors="coerce")
    if (p.dropna() <= 0).any():
        raise ValueError("prices must be positive")
    log_returns = np.log(p).diff()
    return log_returns.rolling(window).std(ddof=1) * np.sqrt(periods_per_year)


def classify_volatility_regimes(
    realized_vol: pd.Series,
    *,
    lower_quantile: float = 1 / 3,
    upper_quantile: float = 2 / 3,
) -> pd.Series:
    """Classify realized volatility into low/medium/high sample quantiles."""
    if not 0 < lower_quantile < upper_quantile < 1:
        raise ValueError("quantiles must satisfy 0 < lower < upper < 1")
    rv = pd.to_numeric(realized_vol, errors="coerce")
    valid = rv.dropna()
    if valid.empty:
        return pd.Series(pd.NA, index=rv.index, dtype="string")
    lo = float(valid.quantile(lower_quantile))
    hi = float(valid.quantile(upper_quantile))

    out = pd.Series(pd.NA, index=rv.index, dtype="string")
    out.loc[rv <= lo] = "low"
    out.loc[(rv > lo) & (rv <= hi)] = "medium"
    out.loc[rv > hi] = "high"
    return out
