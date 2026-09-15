"""Utilities for Barchart WTI Average Price Option (APO) research files.

The module is intentionally data-source focused. It converts the per-contract
CSV downloads from Barchart into a tidy research panel while preserving raw
columns that may be useful later. It does not assume that every row is an
actual trade: for illiquid APOs, daily end-of-day values may be settlement-like
marks even when volume is zero.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re
from typing import Iterable, Mapping

import numpy as np
import pandas as pd

_MONTH_CODES = {
    "F": 1,
    "G": 2,
    "H": 3,
    "J": 4,
    "K": 5,
    "M": 6,
    "N": 7,
    "Q": 8,
    "U": 9,
    "V": 10,
    "X": 11,
    "Z": 12,
}

_SYMBOL_RE = re.compile(
    r"(?P<root>[A-Za-z]+)(?P<month>[FGHJKMNQUVXZ])(?P<year>\d{1,2})"
    r"[_-](?P<strike>\d+)(?P<option_type>[CP])(?:[_-]|$)",
    re.IGNORECASE,
)


@dataclass(frozen=True)
class OptionContract:
    """Contract metadata decoded from a Barchart download filename."""

    symbol_root: str
    month_code: str
    expiry_year: int
    expiry_month: int
    strike: float
    option_type: str

    @property
    def expiry_label(self) -> str:
        return f"{self.expiry_year:04d}-{self.expiry_month:02d}"


def parse_barchart_option_filename(
    path: str | Path,
    *,
    century: int = 2000,
    decade: int = 2020,
    strike_scale: float = 100.0,
) -> OptionContract:
    """Decode root, expiry month/year, strike and call/put from a filename.

    Example
    -------
    ``jaou6_10000c_daily_historical-data-09-10-2026.csv`` decodes to
    root ``JAO``, September 2026, strike 100.00, call.

    Barchart encodes the strike in hundredths in the filenames observed in the
    WTI APO downloads. ``strike_scale`` is configurable so the parser remains
    explicit rather than silently hard-coding a market convention.
    """
    name = Path(path).name
    match = _SYMBOL_RE.search(name)
    if not match:
        raise ValueError(f"Could not decode Barchart option metadata from {name!r}")

    year_token = match.group("year")
    if len(year_token) == 1:
        # Barchart filenames observed here use U6, H7, M9, ... for 2026-2029.
        year = decade + int(year_token)
    else:
        year = century + int(year_token)

    month_code = match.group("month").upper()
    strike = int(match.group("strike")) / strike_scale
    option_type = "call" if match.group("option_type").upper() == "C" else "put"

    return OptionContract(
        symbol_root=match.group("root").upper(),
        month_code=month_code,
        expiry_year=year,
        expiry_month=_MONTH_CODES[month_code],
        strike=float(strike),
        option_type=option_type,
    )


def _clean_numeric(series: pd.Series) -> pd.Series:
    """Coerce Barchart numeric fields, including commas and N/A markers."""
    return pd.to_numeric(
        series.astype(str)
        .str.replace(",", "", regex=False)
        .replace({"N/A": np.nan, "nan": np.nan, "": np.nan}),
        errors="coerce",
    )


def load_barchart_option_history(
    path: str | Path,
    *,
    expiry_date: str | pd.Timestamp | None = None,
    min_tick: float = 0.01,
) -> pd.DataFrame:
    """Load one Barchart APO daily-history CSV into a tidy DataFrame.

    Unknown/raw columns are preserved with ``raw_`` prefixes. This is useful
    for richer Barchart exports whose exact fields may vary by subscription or
    page. The standardized columns are stable across files.
    """
    path = Path(path)
    contract = parse_barchart_option_filename(path)
    raw = pd.read_csv(path)

    if "Time" not in raw.columns:
        raise ValueError(f"{path.name} does not contain the expected 'Time' column")

    # Drop footer or malformed rows such as "Downloaded from Barchart...".
    trade_date = pd.to_datetime(raw["Time"], errors="coerce")
    raw = raw.loc[trade_date.notna()].copy()
    trade_date = trade_date.loc[trade_date.notna()]

    rename = {
        "Open": "open",
        "High": "high",
        "Low": "low",
        "Latest": "market_price",
        "Change": "change",
        "%Change": "pct_change",
        "Volume": "volume",
        "Open Int": "open_interest",
    }
    out = pd.DataFrame(index=raw.index)
    out["trade_date"] = trade_date.values
    for source, target in rename.items():
        if source in raw.columns:
            if source == "%Change":
                out[target] = pd.to_numeric(
                    raw[source].astype(str).str.replace("%", "", regex=False),
                    errors="coerce",
                ) / 100.0
            else:
                out[target] = _clean_numeric(raw[source])
        else:
            out[target] = np.nan

    out["symbol_root"] = contract.symbol_root
    out["expiry_month"] = contract.expiry_label
    out["expiry_year"] = contract.expiry_year
    out["expiry_month_number"] = contract.expiry_month
    out["strike"] = contract.strike
    out["option_type"] = contract.option_type
    out["source_file"] = path.name
    out["at_min_tick"] = np.isclose(out["market_price"], min_tick, atol=1e-12)
    out["traded_today"] = out["volume"].fillna(0.0) > 0.0

    if expiry_date is not None:
        expiry_ts = pd.Timestamp(expiry_date).normalize()
        out["expiry_date"] = expiry_ts
        out["days_to_expiry"] = (expiry_ts - out["trade_date"]).dt.days

    standardized_sources = {"Time", *rename.keys()}
    for col in raw.columns:
        if col not in standardized_sources:
            safe = re.sub(r"\W+", "_", col.strip()).strip("_").lower()
            out[f"raw_{safe}"] = raw[col].values

    return out.reset_index(drop=True)


def build_apo_panel(
    paths: Iterable[str | Path],
    *,
    expiry_dates: Mapping[str, str | pd.Timestamp] | None = None,
    min_tick: float = 0.01,
) -> pd.DataFrame:
    """Combine many individual-contract histories into one tidy APO panel.

    ``expiry_dates`` maps labels such as ``"2026-09"`` to exact exchange
    expiry dates. Exact dates are deliberately supplied rather than inferred
    from weekends/holidays.
    """
    frames: list[pd.DataFrame] = []
    for path in paths:
        contract = parse_barchart_option_filename(path)
        expiry = None
        if expiry_dates is not None:
            expiry = expiry_dates.get(contract.expiry_label)
        frames.append(
            load_barchart_option_history(path, expiry_date=expiry, min_tick=min_tick)
        )

    if not frames:
        raise ValueError("No Barchart option-history files were supplied")

    panel = pd.concat(frames, ignore_index=True, sort=False)
    return panel.sort_values(
        ["trade_date", "expiry_year", "expiry_month_number", "option_type", "strike"]
    ).reset_index(drop=True)


def add_effective_moneyness(
    panel: pd.DataFrame,
    expected_average: pd.DataFrame,
    *,
    expected_average_col: str = "expected_average",
) -> pd.DataFrame:
    """Add log-moneyness relative to the expected terminal arithmetic average.

    ``expected_average`` must contain ``trade_date``, ``expiry_month`` and an
    expected-average level. Using the expected contract average is preferable
    to classifying an APO solely with the current front-month futures price,
    especially once the averaging month has begun.
    """
    required = {"trade_date", "expiry_month", expected_average_col}
    missing = required.difference(expected_average.columns)
    if missing:
        raise ValueError(f"expected_average is missing columns: {sorted(missing)}")

    rhs = expected_average[list(required)].copy()
    rhs["trade_date"] = pd.to_datetime(rhs["trade_date"])
    merged = panel.copy()
    merged["trade_date"] = pd.to_datetime(merged["trade_date"])
    merged = merged.merge(rhs, on=["trade_date", "expiry_month"], how="left")

    avg = merged[expected_average_col].astype(float)
    valid = (avg > 0.0) & (merged["strike"] > 0.0)
    merged["log_moneyness"] = np.nan
    merged.loc[valid, "log_moneyness"] = np.log(
        merged.loc[valid, "strike"] / avg.loc[valid]
    )
    merged["moneyness_bucket"] = pd.cut(
        merged["log_moneyness"].abs(),
        bins=[-np.inf, 0.05, 0.15, np.inf],
        labels=["ATM", "moderate", "deep"],
    )
    return merged


def rank_representative_contracts(panel: pd.DataFrame) -> pd.DataFrame:
    """Rank contracts for figures without filtering the estimation sample.

    The main empirical analysis should retain all contracts that pass objective
    data-quality filters. This ranking is only for choosing representative
    strikes for figures and discussion.
    """
    required = {
        "expiry_month",
        "strike",
        "option_type",
        "trade_date",
        "market_price",
        "open_interest",
        "at_min_tick",
    }
    missing = required.difference(panel.columns)
    if missing:
        raise ValueError(f"panel is missing columns: {sorted(missing)}")

    group_cols = ["expiry_month", "strike", "option_type"]
    rows: list[dict[str, float | str | int]] = []
    for key, group in panel.groupby(group_cols, dropna=False):
        expiry_month, strike, option_type = key
        oi = group["open_interest"].dropna()
        informative = (~group["at_min_tick"].fillna(False)) & group["market_price"].notna()
        row: dict[str, float | str | int] = {
            "expiry_month": str(expiry_month),
            "strike": float(strike),
            "option_type": str(option_type),
            "n_obs": int(group["trade_date"].nunique()),
            "median_open_interest": float(oi.median()) if not oi.empty else 0.0,
            "informative_share": float(informative.mean()) if len(group) else 0.0,
            "min_price": float(group["market_price"].min()),
            "max_price": float(group["market_price"].max()),
        }

        if "log_moneyness" in group.columns:
            lm = group["log_moneyness"].dropna()
            row["atm_days"] = int((lm.abs() <= 0.05).sum())
            if len(lm) >= 2:
                signs = np.sign(lm.to_numpy())
                nonzero = signs != 0
                signs = signs[nonzero]
                row["moneyness_crossings"] = int(np.sum(signs[1:] != signs[:-1])) if len(signs) >= 2 else 0
            else:
                row["moneyness_crossings"] = 0
        else:
            row["atm_days"] = 0
            row["moneyness_crossings"] = 0
        rows.append(row)

    ranked = pd.DataFrame(rows)
    if ranked.empty:
        return ranked

    # Robust, transparent score: long history + informative marks + liquidity;
    # ATM occupancy/crossings receive weight only when moneyness is available.
    ranked["score"] = (
        np.log1p(ranked["n_obs"])
        + 2.0 * ranked["informative_share"]
        + 0.5 * np.log1p(ranked["median_open_interest"])
        + 0.05 * ranked["atm_days"]
        + 0.25 * ranked["moneyness_crossings"]
    )
    return ranked.sort_values(
        ["expiry_month", "option_type", "score"],
        ascending=[True, True, False],
    ).reset_index(drop=True)


def apply_main_sample_filters(
    panel: pd.DataFrame,
    *,
    min_open_interest: float = 1.0,
    exclude_min_tick: bool = True,
) -> pd.DataFrame:
    """Apply objective filters for the primary empirical estimation panel."""
    mask = panel["market_price"].notna()
    mask &= panel["open_interest"].fillna(0.0) >= min_open_interest
    if exclude_min_tick:
        mask &= ~panel["at_min_tick"].fillna(False)
    return panel.loc[mask].copy().reset_index(drop=True)
