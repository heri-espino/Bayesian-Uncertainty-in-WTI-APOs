"""Utilities for a reproducible WTI futures empirical application using Yahoo Finance.

Yahoo ticker ``CL=F`` is treated as a *continuous/front-month proxy*.  Yahoo exposes
historical OHLCV observations but does not document a sufficiently precise historical
roll rule for this symbol, so this module deliberately does not call the series a
self-reconstructed first-nearby contract.

Raw Yahoo data should remain local.  The experiment writes hashes and metadata that
identify the exact local snapshot used for inference.
"""

from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd


DEFAULT_TICKER = "CL=F"
DEFAULT_MODEL_START = "2021-01-01"


@dataclass(frozen=True)
class WTIModelSample:
    history: pd.DataFrame
    log_returns: np.ndarray
    first_date: str
    last_date: str
    n_prices: int
    n_returns: int


def _flatten_columns(frame: pd.DataFrame) -> pd.DataFrame:
    out = frame.copy()
    if isinstance(out.columns, pd.MultiIndex):
        # Ticker.history() is normally flat, but this also tolerates yf.download().
        out.columns = [str(col[0]) for col in out.columns]
    return out


def normalize_yahoo_history(frame: pd.DataFrame) -> pd.DataFrame:
    """Return a stable, lowercase OHLCV schema from a Yahoo/yfinance DataFrame."""
    if frame is None or len(frame) == 0:
        raise ValueError("Yahoo history is empty")

    out = _flatten_columns(frame)
    out = out.reset_index()
    date_col = "Date" if "Date" in out.columns else out.columns[0]
    out = out.rename(columns={date_col: "date"})

    rename = {
        "Open": "open",
        "High": "high",
        "Low": "low",
        "Close": "close",
        "Adj Close": "adj_close",
        "Volume": "volume",
    }
    out = out.rename(columns=rename)
    if "close" not in out.columns:
        raise ValueError("Yahoo history does not contain a Close column")

    keep = [c for c in ["date", "open", "high", "low", "close", "adj_close", "volume"] if c in out]
    out = out[keep].copy()
    out["date"] = pd.to_datetime(out["date"], utc=True, errors="coerce").dt.tz_convert(None)
    for col in [c for c in keep if c != "date"]:
        out[col] = pd.to_numeric(out[col], errors="coerce")

    out = out.dropna(subset=["date", "close"])
    out = out.sort_values("date").drop_duplicates("date", keep="last").reset_index(drop=True)
    if out.empty:
        raise ValueError("No usable Yahoo observations remain after normalization")
    return out


def download_yahoo_wti(
    *,
    ticker: str = DEFAULT_TICKER,
    period: str = "max",
    start: str | None = None,
    end: str | None = None,
) -> tuple[pd.DataFrame, dict[str, Any]]:
    """Download daily WTI futures-proxy data through yfinance.

    The yfinance import is lazy so unit tests for cleaning/inference do not require
    network dependencies.
    """
    try:
        import yfinance as yf  # type: ignore
    except ImportError as exc:  # pragma: no cover - depends on local environment
        raise RuntimeError(
            "yfinance is required. Install/update the Conda environment from environment.yml"
        ) from exc

    tkr = yf.Ticker(ticker)
    kwargs: dict[str, Any] = {
        "interval": "1d",
        "auto_adjust": False,
        "actions": False,
        "repair": False,
        "raise_errors": True,
    }
    if start is not None or end is not None:
        kwargs.update({"start": start, "end": end})
    else:
        kwargs["period"] = period

    raw = tkr.history(**kwargs)
    history = normalize_yahoo_history(raw)
    metadata = {
        "provider": "Yahoo Finance via yfinance",
        "ticker": ticker,
        "query_period": None if start is not None or end is not None else period,
        "query_start": start,
        "query_end": end,
        "interval": "1d",
        "auto_adjust": False,
        "repair": False,
        "first_observation": history["date"].iloc[0].date().isoformat(),
        "last_observation": history["date"].iloc[-1].date().isoformat(),
        "rows": int(len(history)),
        "yfinance_version": getattr(yf, "__version__", None),
    }
    return history, metadata


def prepare_wti_model_sample(
    history: pd.DataFrame,
    *,
    start: str | None = DEFAULT_MODEL_START,
    end: str | None = None,
) -> WTIModelSample:
    """Create positive-price daily log returns for GBM inference.

    No non-positive observation is silently deleted.  If one appears inside the
    requested modeling window, the function raises and asks the caller to choose a
    scientifically explicit positive-price window.
    """
    frame = normalize_yahoo_history(history)
    if start is not None:
        frame = frame[frame["date"] >= pd.Timestamp(start)]
    if end is not None:
        frame = frame[frame["date"] < pd.Timestamp(end)]
    frame = frame.reset_index(drop=True)
    if len(frame) < 3:
        raise ValueError("At least three prices are required for a modeling sample")

    bad = frame[frame["close"] <= 0]
    if not bad.empty:
        dates = ", ".join(d.date().isoformat() for d in bad["date"].head(5))
        raise ValueError(
            "GBM log returns require positive prices. Non-positive closes were found "
            f"inside the requested window (first examples: {dates}). Choose a later --model-start."
        )

    log_returns = np.diff(np.log(frame["close"].to_numpy(dtype=float)))
    if not np.all(np.isfinite(log_returns)):
        raise ValueError("Non-finite log returns were produced")

    return WTIModelSample(
        history=frame,
        log_returns=log_returns,
        first_date=frame["date"].iloc[0].date().isoformat(),
        last_date=frame["date"].iloc[-1].date().isoformat(),
        n_prices=int(len(frame)),
        n_returns=int(len(log_returns)),
    )


def dataframe_csv_bytes(frame: pd.DataFrame) -> bytes:
    """Serialize a normalized snapshot deterministically for hashing/storage."""
    return frame.to_csv(index=False, date_format="%Y-%m-%d").encode("utf-8")


def dataframe_sha256(frame: pd.DataFrame) -> str:
    return sha256(dataframe_csv_bytes(frame)).hexdigest()


def write_local_snapshot(frame: pd.DataFrame, path: Path) -> str:
    """Write a normalized CSV snapshot and return its SHA-256 digest."""
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = dataframe_csv_bytes(frame)
    path.write_bytes(payload)
    return sha256(payload).hexdigest()
