"""Barchart WTI Average Price Option (APO) data utilities.

The repository contains one CSV per option contract.  This module decodes the
Barchart symbol, standardizes the daily history, preserves extra/raw fields,
and builds a tidy panel.  It intentionally separates *data richness* from
liquidity/economic relevance: a long, complete series can still have zero
trading volume or low open interest.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re
from typing import Iterable

import numpy as np
import pandas as pd

MONTH_CODES = {
    "F": 1, "G": 2, "H": 3, "J": 4, "K": 5, "M": 6,
    "N": 7, "Q": 8, "U": 9, "V": 10, "X": 11, "Z": 12,
}
MONTH_NAMES = {
    1: "jan", 2: "feb", 3: "mar", 4: "apr", 5: "may", 6: "jun",
    7: "jul", 8: "aug", 9: "sep", 10: "oct", 11: "nov", 12: "dec",
}

# Examples observed in the repository:
# jaou6_10000c_price-history-09-12-2026.csv
# jaou6_10000c_daily_historical-data-09-10-2026.csv
FILENAME_RE = re.compile(
    r"^(?P<root>jao(?P<month>[FGHJKMNQUVXZ])(?P<year>\d{1,2}))_"
    r"(?P<strike>\d+)(?P<right>[cp])_.*\.csv$",
    re.IGNORECASE,
)


@dataclass(frozen=True)
class OptionContract:
    root_symbol: str
    expiry_year: int
    expiry_month: int
    strike: float
    option_type: str

    @property
    def expiry_label(self) -> str:
        return f"{self.expiry_year:04d}-{self.expiry_month:02d}"

    @property
    def contract_id(self) -> str:
        right = "c" if self.option_type == "call" else "p"
        return f"{self.root_symbol.lower()}_{int(round(self.strike * 100))}{right}"

    @property
    def expected_folder(self) -> str:
        return f"{MONTH_NAMES[self.expiry_month]}{self.expiry_year}"


def parse_barchart_option_filename(path: str | Path, *, decade: int = 2020) -> OptionContract:
    """Decode expiry, strike and call/put metadata from a Barchart APO filename."""
    match = FILENAME_RE.fullmatch(Path(path).name)
    if match is None:
        raise ValueError(f"Unrecognized Barchart APO filename: {Path(path).name}")
    token = match.group("year")
    year = decade + int(token) if len(token) == 1 else 2000 + int(token)
    month_code = match.group("month").upper()
    return OptionContract(
        root_symbol=match.group("root").upper(),
        expiry_year=year,
        expiry_month=MONTH_CODES[month_code],
        strike=int(match.group("strike")) / 100.0,
        option_type="call" if match.group("right").lower() == "c" else "put",
    )


def discover_barchart_histories(root: str | Path) -> list[Path]:
    """Recursively discover individual-contract APO history CSVs.

    Aggregate files such as ``option_series_properties.csv`` are skipped because
    they do not match the contract filename convention.
    """
    root = Path(root)
    paths: list[Path] = []
    for path in root.rglob("*.csv"):
        try:
            parse_barchart_option_filename(path)
        except ValueError:
            continue
        paths.append(path)
    return sorted(paths)


def _numeric(series: pd.Series) -> pd.Series:
    return pd.to_numeric(
        series.astype(str)
        .str.replace(",", "", regex=False)
        .replace({"N/A": np.nan, "NA": np.nan, "nan": np.nan, "": np.nan, "unch": 0.0}),
        errors="coerce",
    )


def load_barchart_option_history(path: str | Path, *, min_tick: float = 0.01) -> pd.DataFrame:
    """Load one individual APO history into a stable research schema."""
    path = Path(path)
    contract = parse_barchart_option_filename(path)
    raw = pd.read_csv(path, encoding="utf-8-sig")
    if "Time" not in raw.columns:
        raise ValueError(f"{path.name}: expected a 'Time' column")

    dates = pd.to_datetime(raw["Time"], errors="coerce")
    valid = dates.notna()
    raw = raw.loc[valid].copy()
    dates = dates.loc[valid]
    if raw.empty:
        raise ValueError(f"{path.name}: no valid daily rows")

    mapping = {
        "Open": "open", "High": "high", "Low": "low", "Latest": "market_price",
        "Change": "change", "Volume": "volume", "Open Int": "open_interest",
    }
    out = pd.DataFrame({"trade_date": dates.to_numpy()})
    for source, target in mapping.items():
        out[target] = _numeric(raw[source]).to_numpy() if source in raw else np.nan
    if "%Change" in raw:
        out["pct_change"] = (
            pd.to_numeric(raw["%Change"].astype(str).str.replace("%", "", regex=False), errors="coerce")
            / 100.0
        ).to_numpy()
    else:
        out["pct_change"] = np.nan

    out["contract_id"] = contract.contract_id
    out["root_symbol"] = contract.root_symbol
    out["expiry_month"] = contract.expiry_label
    out["strike"] = contract.strike
    out["option_type"] = contract.option_type
    out["source_file"] = path.name
    out["source_folder"] = path.parent.name
    out["folder_expiry_match"] = path.parent.name.lower() == contract.expected_folder.lower()
    out["at_min_tick"] = np.isclose(out["market_price"], min_tick, atol=1e-12)
    out["traded_today"] = out["volume"].fillna(0.0) > 0.0

    standard = {"Time", "%Change", *mapping.keys()}
    for col in raw.columns:
        if col in standard:
            continue
        safe = re.sub(r"\W+", "_", col.strip()).strip("_").lower()
        out[f"raw_{safe}"] = raw[col].to_numpy()
    return out.sort_values("trade_date").reset_index(drop=True)


def _history_score(frame: pd.DataFrame) -> tuple[int, pd.Timestamp, float]:
    n = int(frame["trade_date"].nunique())
    last = pd.Timestamp(frame["trade_date"].max())
    completeness = float(frame[["open", "high", "low", "market_price", "change", "pct_change", "volume", "open_interest"]].notna().mean().mean())
    return n, last, completeness


def build_apo_panel(paths: Iterable[str | Path], *, deduplicate_contracts: bool = True) -> pd.DataFrame:
    """Combine individual histories, optionally retaining the richest duplicate.

    Duplicate contract downloads can occur on different dates or in a misplaced
    folder.  When ``deduplicate_contracts`` is true, the version with the most
    sessions is kept; ties prefer the latest final date and then field completeness.
    """
    frames: list[pd.DataFrame] = []
    for path in paths:
        frames.append(load_barchart_option_history(path))
    if not frames:
        raise ValueError("No valid Barchart APO history files supplied")

    if deduplicate_contracts:
        by_contract: dict[str, list[pd.DataFrame]] = {}
        for frame in frames:
            by_contract.setdefault(str(frame["contract_id"].iloc[0]), []).append(frame)
        frames = [max(candidates, key=_history_score) for candidates in by_contract.values()]

    panel = pd.concat(frames, ignore_index=True, sort=False)
    return panel.sort_values(["trade_date", "expiry_month", "option_type", "strike"]).reset_index(drop=True)


def add_effective_moneyness(
    panel: pd.DataFrame,
    expected_average: pd.DataFrame,
    *,
    value_col: str = "expected_average",
) -> pd.DataFrame:
    """Add log-moneyness relative to the expected final APO arithmetic average."""
    required = {"trade_date", "expiry_month", value_col}
    missing = required.difference(expected_average.columns)
    if missing:
        raise ValueError(f"expected_average missing columns: {sorted(missing)}")
    rhs = expected_average[["trade_date", "expiry_month", value_col]].copy()
    rhs["trade_date"] = pd.to_datetime(rhs["trade_date"])
    out = panel.copy()
    out["trade_date"] = pd.to_datetime(out["trade_date"])
    out = out.merge(rhs, on=["trade_date", "expiry_month"], how="left")
    valid = (out[value_col] > 0) & (out["strike"] > 0)
    out["log_moneyness"] = np.nan
    out.loc[valid, "log_moneyness"] = np.log(out.loc[valid, "strike"] / out.loc[valid, value_col])
    out["moneyness_bucket"] = pd.cut(
        out["log_moneyness"].abs(),
        bins=[-np.inf, 0.05, 0.15, np.inf],
        labels=["ATM", "moderate", "deep"],
    )
    return out


def summarize_contracts(panel: pd.DataFrame) -> pd.DataFrame:
    """Create data-quality/liquidity diagnostics without selecting the sample."""
    rows: list[dict[str, object]] = []
    keys = ["contract_id", "expiry_month", "strike", "option_type"]
    for key, g in panel.groupby(keys, dropna=False):
        contract_id, expiry, strike, option_type = key
        price = g["market_price"].dropna()
        oi = g["open_interest"].dropna()
        row: dict[str, object] = {
            "contract_id": contract_id,
            "expiry_month": expiry,
            "strike": float(strike),
            "option_type": option_type,
            "sessions": int(g["trade_date"].nunique()),
            "first_date": g["trade_date"].min(),
            "last_date": g["trade_date"].max(),
            "price_completeness": float(g["market_price"].notna().mean()),
            "non_min_tick_share": float((~g["at_min_tick"].fillna(False) & g["market_price"].notna()).mean()),
            "nonzero_volume_share": float((g["volume"].fillna(0) > 0).mean()),
            "median_open_interest": float(oi.median()) if not oi.empty else 0.0,
            "max_open_interest": float(oi.max()) if not oi.empty else 0.0,
            "min_price": float(price.min()) if not price.empty else np.nan,
            "max_price": float(price.max()) if not price.empty else np.nan,
            "folder_mismatch": bool((~g["folder_expiry_match"]).any()),
        }
        if "log_moneyness" in g:
            lm = g["log_moneyness"].dropna().sort_index()
            row["atm_days"] = int((lm.abs() <= 0.05).sum())
            signs = np.sign(lm.to_numpy())
            signs = signs[signs != 0]
            row["moneyness_crossings"] = int(np.sum(signs[1:] != signs[:-1])) if len(signs) >= 2 else 0
        else:
            row["atm_days"] = 0
            row["moneyness_crossings"] = 0
        rows.append(row)
    return pd.DataFrame(rows)


def rank_representative_contracts(panel: pd.DataFrame) -> pd.DataFrame:
    """Rank contracts for plots/case studies, not for estimation-sample inclusion."""
    out = summarize_contracts(panel)
    if out.empty:
        return out
    out["representative_score"] = (
        np.log1p(out["sessions"])
        + 2.0 * out["non_min_tick_share"]
        + 0.5 * np.log1p(out["median_open_interest"])
        + 0.05 * out["atm_days"]
        + 0.25 * out["moneyness_crossings"]
    )
    return out.sort_values(
        ["expiry_month", "option_type", "representative_score"],
        ascending=[True, True, False],
    ).reset_index(drop=True)


def apply_main_sample_filters(
    panel: pd.DataFrame,
    *,
    min_open_interest: float = 1.0,
    exclude_min_tick: bool = True,
) -> pd.DataFrame:
    """Objective baseline filter; raw observations remain preserved separately."""
    keep = panel["market_price"].notna() & (panel["open_interest"].fillna(0) >= min_open_interest)
    if exclude_min_tick:
        keep &= ~panel["at_min_tick"].fillna(False)
    return panel.loc[keep].copy().reset_index(drop=True)
