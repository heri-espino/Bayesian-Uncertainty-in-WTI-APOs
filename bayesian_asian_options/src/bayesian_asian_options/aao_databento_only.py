"""Databento-only AAO benchmark mathematics; explicitly *reduced-form*.

CME AAO pays (arithmetic average of first-nearby CL settlements - K)+.
The downloaded AAO definition/statistics DBNs do NOT themselves contain
first-nearby CL fixing histories or contemporaneous futures curves.
This module therefore models the *terminal average* as approximately
lognormal and infers its risk-neutral expected value and discount factor
from DISJOINT same-date call/put anchor strikes via Asian put-call parity.

This is NOT the canonical structural WTI-APO GBM/first-nearby simulator
and historical return volatility here is a proxy inferred from successive
option-implied forward averages, NOT directly observed CL P-measure sigma.
Never describe the exercise as ex-ante pricing with no contemporaneous
market information or as model-independent risk-neutral forecasting.
"""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd
from scipy.optimize import brentq
from scipy.special import ndtr

METHODS = ("PI", "PM", "rolling21", "rolling63", "ewma63", "lagged_IV")


@dataclass(frozen=True)
class ParityAnchor:
    forward_average: float
    discount_factor: float
    anchor_strikes: tuple[float, ...]
    parity_rmse: float
    available_strikes: int


def average_black(
    forward: float, strike: np.ndarray | float, sigma: np.ndarray | float,
    maturity: float, discount: float, side: np.ndarray | str,
) -> np.ndarray:
    """Lognormal-terminal-average reduced-form option price, USD/bbl."""
    k = np.asarray(strike, dtype=float)
    v = np.asarray(sigma, dtype=float)
    rights = np.asarray(side)
    if (not np.isfinite(forward) or forward <= 0 or
        not np.isfinite(maturity) or maturity <= 0 or
        not np.isfinite(discount) or not 0 < discount <= 1.05 or
        np.any(~np.isfinite(k)) or np.any(k <= 0) or
        np.any(~np.isfinite(v)) or np.any(v <= 0) or
        np.any(~np.isin(rights, ["C", "P"]))):
        raise ValueError("Invalid positive F/K/sigma/T/discount or option right")
    width = v * np.sqrt(maturity)
    d1 = (np.log(forward / k) + .5 * width**2) / width
    d2 = d1 - width
    calls = discount * (forward * ndtr(d1) - k * ndtr(d2))
    puts = calls - discount * (forward - k)
    return np.maximum(np.where(rights == "C", calls, puts), 0.0)


def reserve_parity_anchors(
    frame: pd.DataFrame, *, n_anchors: int = 7,
    min_strike_span: float = 3.0, max_parity_rmse: float = 0.40,
    actual_only: bool = True,
) -> ParityAnchor | None:
    """Estimate DF and E_Q[A] from reserved C/P matched strikes.

    Current-date strikes used here are NEVER included among evaluated
    targets. At least four paired strikes are required to identify
    intercept and discount. Market-implied information at date t is
    used for the forward, so this is CROSS-SECTIONAL valuation, not a
    completely prior-day forecast.
    """
    required = {"strike", "side", "price", "actual"}
    if not required.issubset(frame):
        raise ValueError(f"Missing columns: {sorted(required-set(frame))}")
    f = frame.copy()
    if actual_only:
        f = f.loc[f["actual"]].copy()
    f = f.loc[
        np.isfinite(f["strike"]) & np.isfinite(f["price"])
        & (f["strike"] > 0) & (f["price"] >= 0)
        & f["side"].isin(("C", "P"))
    ]
    pairs = f.pivot_table(
        index="strike", columns="side", values="price", aggfunc="median"
    )
    if not {"C", "P"}.issubset(pairs):
        return None
    pairs = pairs.dropna(subset=["C", "P"]).sort_index()
    if len(pairs) < 4:
        return None
    chosen = np.unique(np.linspace(
        0, len(pairs) - 1, min(n_anchors, len(pairs)), dtype=int
    ))
    anchors = pairs.iloc[chosen]
    strikes = anchors.index.to_numpy(dtype=float)
    if np.ptp(strikes) < min_strike_span:
        return None
    difference = (anchors["C"] - anchors["P"]).to_numpy(dtype=float)
    slope, intercept = np.polyfit(strikes, difference, deg=1)
    discount = float(-slope)
    if not 0.75 <= discount <= 1.05:
        return None
    forward = float(intercept / discount)
    if not 5.0 <= forward <= 300.0:
        return None
    rmse = float(np.sqrt(np.mean(
        (difference - (intercept + slope * strikes))**2
    )))
    if rmse > max_parity_rmse:
        return None
    return ParityAnchor(
        forward, discount, tuple(strikes), rmse, int(len(pairs)),
    )


def implied_average_sigma(price: float, *, forward: float, strike: float,
                          maturity: float, discount: float,
                          side: str) -> float:
    """Invert the REDUCED-FORM lognormal terminal-average price."""
    if price < 0 or not np.isfinite(price):
        return float("nan")
    intrinsic = discount * max(
        forward - strike if side == "C" else strike - forward, 0.0
    )
    ceiling = discount * (forward if side == "C" else strike)
    if price <= intrinsic + 1e-5 or price >= ceiling - 1e-5:
        return float("nan")
    def objective(v: float) -> float:
        return float(average_black(
            forward, strike, v, maturity, discount, side
        )) - price
    if objective(.005) * objective(3.) >= 0:
        return float("nan")
    return float(brentq(objective, .005, 3., xtol=1e-7))


def prior_volatility_features(
    returns: np.ndarray, *, seed: int = 23, n_posterior: int = 128,
    alpha0: float = 3.0, beta0: float = 0.16,
) -> dict[str, np.ndarray | float]:
    """Posterior on annualized variance of proxy forward-average returns.

    r*sqrt(252) ~ N(mean, sigma**2), with unknown mean profiled out;
    variance prior InverseGamma(alpha0,beta0). Prior draws and all
    benchmark estimates use only *previous trading dates*.
    """
    r = np.asarray(returns, dtype=float)
    if (r.ndim != 1 or len(r) < 20 or
        np.any(~np.isfinite(r)) or n_posterior < 16 or
        alpha0 <= 0 or beta0 <= 0):
        raise ValueError("Requires >=20 finite lagged returns and valid prior")
    y = r * np.sqrt(252.0)
    shape = alpha0 + (len(y) - 1) / 2.0
    scale = beta0 + .5 * float(np.sum((y-y.mean())**2))
    rng = np.random.default_rng(seed)
    draws = np.sqrt(1.0 / rng.gamma(
        shape=shape, scale=1.0/scale, size=n_posterior
    ))
    def rolling(n: int) -> float:
        z = r[-n:]
        return max(float(z.std(ddof=1) * np.sqrt(252.0)), .005)
    weights = .5**(np.arange(len(r)-1, -1, -1)/63.0)
    weights /= weights.sum()
    mean = float(weights @ r)
    ewma = np.sqrt(max(float(weights @ (r-mean)**2) * 252.0, .005**2))
    return {
        "draws": draws,
        "sigma_pm": float(draws.mean()),
        "rolling21": rolling(21),
        "rolling63": rolling(63),
        "ewma63": float(ewma),
        "posterior_sd": float(draws.std(ddof=1)),
        "n_returns": len(r),
    }


def summarize_errors(prices: pd.DataFrame) -> pd.DataFrame:
    """Common-row MAE/RMSE/bias; DO NOT treat contract rows as independent."""
    required = {"date", "method", "error", "actual"}
    if not required.issubset(prices):
        raise ValueError(f"Missing columns {sorted(required-set(prices))}")
    rows = []
    for (method, kind), f in prices.groupby(["method", "actual"], sort=True):
        errors = f["error"].to_numpy(dtype=float)
        rows.append({
            "method": str(method),
            "settlement_type": "actual_flagged" if kind else "theoretical_flagged",
            "n_contract_dates": len(errors),
            "n_dates": int(f["date"].nunique()),
            "mae": float(np.abs(errors).mean()),
            "rmse": float(np.sqrt(np.mean(errors**2))),
            "bias": float(errors.mean()),
        })
    return pd.DataFrame(rows)


def date_cluster_ci(
    data: pd.DataFrame, method: str, baseline: str = "PM",
    *, n_boot: int = 499, seed: int = 23,
) -> dict:
    """Paired per-date improvements in MAE; resample DAYS not contracts."""
    sub = data[data["method"].isin((method, baseline))]
    bydate = sub.groupby(["date", "method"])["error"].agg(
        lambda e: float(np.abs(e).mean())
    ).unstack()
    bydate = bydate.dropna(subset=[method, baseline])
    if len(bydate) < 2:
        raise ValueError("At least two paired dates needed for cluster inference")
    diffs = (bydate[baseline]-bydate[method]).to_numpy()
    rng = np.random.default_rng(seed)
    draws = diffs[rng.integers(0, len(diffs), size=(n_boot, len(diffs)))]
    return {
        "method": method,
        "baseline": baseline,
        "n_paired_dates": len(diffs),
        "mean_daily_mae_improvement": float(diffs.mean()),
        "ci_low": float(np.quantile(draws.mean(axis=1), .025)),
        "ci_high": float(np.quantile(draws.mean(axis=1), .975)),
    }
