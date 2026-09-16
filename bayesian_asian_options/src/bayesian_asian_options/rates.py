"""U.S. Treasury par-yield utilities for date-specific APO discounting.

The Treasury CSVs used by the empirical application are the official daily
Treasury *par yield* curve files.  A par yield is not itself a zero-coupon
yield.  The current pilot therefore exposes the approximation explicitly:
the maturity-interpolated par yield is treated as a continuously compounded
zero-rate proxy when constructing a discount factor.  This approximation is
versioned and named so it can later be replaced by a bootstrapped/OIS curve
without silently changing the empirical design.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re
from typing import Iterable
from urllib.request import Request, urlopen

import numpy as np
import pandas as pd

_TENOR_RE = re.compile(r"^\s*(?P<n>\d+(?:\.\d+)?)\s*(?P<unit>Mo|Month|Yr|Year)s?\s*$", re.IGNORECASE)


@dataclass(frozen=True)
class TreasuryCurveSnapshot:
    """One dated Treasury par-yield curve in decimal units."""

    valuation_date: pd.Timestamp
    source_date: pd.Timestamp
    maturities_years: np.ndarray
    par_yields: np.ndarray

    def interpolated_par_yield(self, maturity_years: float) -> float:
        """Linearly interpolate the dated par curve in maturity."""
        t = float(maturity_years)
        if not np.isfinite(t) or t < 0:
            raise ValueError("maturity_years must be finite and non-negative")
        if t == 0:
            return float(self.par_yields[0])
        lo = float(self.maturities_years.min())
        hi = float(self.maturities_years.max())
        if t > hi:
            raise ValueError(f"maturity {t:.6f}y exceeds available Treasury curve {hi:.6f}y")
        if t < lo:
            return float(self.par_yields[np.argmin(self.maturities_years)])
        return float(np.interp(t, self.maturities_years, self.par_yields))

    def proxy_discount_factor(self, maturity_years: float) -> float:
        """Return exp(-y(t)*t) using the interpolated par yield as a zero-rate proxy."""
        t = float(maturity_years)
        if t < 0:
            raise ValueError("maturity_years must be non-negative")
        if t == 0:
            return 1.0
        y = self.interpolated_par_yield(t)
        return float(np.exp(-y * t))


def treasury_tenor_years(label: str) -> float | None:
    """Convert Treasury CSV column labels such as ``1.5 Month`` or ``2 Yr`` to years."""
    match = _TENOR_RE.fullmatch(str(label))
    if match is None:
        return None
    value = float(match.group("n"))
    unit = match.group("unit").lower()
    return value / 12.0 if unit.startswith(("mo", "month")) else value


def normalize_treasury_par_yields(frame: pd.DataFrame) -> pd.DataFrame:
    """Normalize one official Treasury daily par-yield CSV to long format.

    Output columns are ``date``, ``maturity_years`` and ``par_yield`` where
    yields are decimals rather than percentages.
    """
    if frame is None or frame.empty:
        raise ValueError("Treasury rate frame is empty")
    date_col = next((c for c in frame.columns if str(c).strip().lower() == "date"), None)
    if date_col is None:
        raise ValueError("Treasury CSV requires a Date column")

    tenor_cols: list[tuple[str, float]] = []
    for col in frame.columns:
        maturity = treasury_tenor_years(str(col))
        if maturity is not None:
            tenor_cols.append((str(col), maturity))
    if not tenor_cols:
        raise ValueError("Treasury CSV contains no recognized maturity columns")

    work = frame.copy()
    work["date"] = pd.to_datetime(work[date_col], errors="coerce").dt.normalize()
    rows: list[pd.DataFrame] = []
    for col, maturity in tenor_cols:
        values = pd.to_numeric(work[col], errors="coerce") / 100.0
        rows.append(
            pd.DataFrame(
                {
                    "date": work["date"],
                    "maturity_years": maturity,
                    "par_yield": values,
                    "source_column": col,
                }
            )
        )
    out = pd.concat(rows, ignore_index=True)
    out = out.dropna(subset=["date", "par_yield"])
    out = out[np.isfinite(out["par_yield"]) & (out["par_yield"] >= 0)]
    return out.sort_values(["date", "maturity_years"]).reset_index(drop=True)


def load_treasury_par_yields(paths: Iterable[str | Path]) -> pd.DataFrame:
    """Load and combine one or more official Treasury daily-rate CSV files."""
    frames: list[pd.DataFrame] = []
    for path in paths:
        frame = pd.read_csv(Path(path), encoding="utf-8-sig")
        normalized = normalize_treasury_par_yields(frame)
        normalized["source_file"] = Path(path).name
        frames.append(normalized)
    if not frames:
        raise ValueError("No Treasury CSV paths supplied")
    out = pd.concat(frames, ignore_index=True)
    return out.sort_values(["date", "maturity_years"]).drop_duplicates(
        ["date", "maturity_years"], keep="last"
    ).reset_index(drop=True)


def treasury_curve_on_or_before(
    table: pd.DataFrame,
    valuation_date: str | pd.Timestamp,
    *,
    max_backfill_days: int = 7,
) -> TreasuryCurveSnapshot:
    """Select the latest Treasury curve available on or before a valuation date."""
    required = {"date", "maturity_years", "par_yield"}
    missing = required.difference(table.columns)
    if missing:
        raise ValueError(f"Treasury table missing columns: {sorted(missing)}")
    if max_backfill_days < 0:
        raise ValueError("max_backfill_days must be non-negative")

    target = pd.Timestamp(valuation_date).normalize()
    work = table.copy()
    work["date"] = pd.to_datetime(work["date"]).dt.normalize()
    eligible_dates = work.loc[work["date"] <= target, "date"]
    if eligible_dates.empty:
        raise ValueError(f"No Treasury curve available on or before {target.date()}")
    source_date = pd.Timestamp(eligible_dates.max())
    if (target - source_date).days > max_backfill_days:
        raise ValueError(
            f"Latest Treasury curve before {target.date()} is {source_date.date()}, "
            f"more than {max_backfill_days} days stale"
        )
    curve = work[work["date"] == source_date].dropna(subset=["maturity_years", "par_yield"])
    curve = curve.sort_values("maturity_years").drop_duplicates("maturity_years", keep="last")
    if curve.empty:
        raise ValueError(f"Treasury curve is empty on {source_date.date()}")
    return TreasuryCurveSnapshot(
        valuation_date=target,
        source_date=source_date,
        maturities_years=curve["maturity_years"].to_numpy(dtype=float),
        par_yields=curve["par_yield"].to_numpy(dtype=float),
    )


def treasury_csv_url(year: int) -> str:
    """Return the official Treasury CSV endpoint for one calendar year."""
    if year < 1990 or year > 2100:
        raise ValueError("unexpected Treasury year")
    return (
        "https://home.treasury.gov/resource-center/data-chart-center/interest-rates/"
        f"daily-treasury-rates.csv/{year}/all"
        f"?type=daily_treasury_yield_curve&field_tdr_date_value={year}&page&_format=csv"
    )


def download_treasury_par_yield_csv(year: int, destination: str | Path) -> Path:
    """Download one official Treasury par-yield CSV.

    This helper is intended for workstation reproducibility.  Existing local
    files remain the preferred input when network access is unavailable.
    """
    destination = Path(destination)
    destination.parent.mkdir(parents=True, exist_ok=True)
    request = Request(
        treasury_csv_url(year),
        headers={"User-Agent": "bayesian-asian-options-research/0.1"},
    )
    with urlopen(request, timeout=60) as response:  # nosec B310 - fixed Treasury HTTPS host
        payload = response.read()
    if b"Date" not in payload[:2048]:
        raise RuntimeError("Treasury download did not look like a CSV rate file")
    destination.write_bytes(payload)
    return destination
