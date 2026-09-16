"""Yahoo Finance utilities for individual NYMEX WTI (CL) futures contracts.

The empirical APO application uses contract-specific Yahoo symbols such as
``CLV26.NYM`` rather than treating ``CL=F`` as a contractually exact
first-nearby series. Yahoo ``Close`` is retained as an end-of-day settlement
*proxy* and should be cross-validated against exchange/Barchart observations.

Network access is deliberately lazy. Unit tests can exercise all cleaning,
curve construction and first-nearby reconstruction functions without yfinance.
"""

from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
import json
from pathlib import Path
import re
import time
from typing import Any, Iterable

import numpy as np
import pandas as pd

from bayesian_asian_options.wti_first_nearby import assign_first_nearby_contract

CL_MONTH_CODES = {
    1: "F", 2: "G", 3: "H", 4: "J", 5: "K", 6: "M",
    7: "N", 8: "Q", 9: "U", 10: "V", 11: "X", 12: "Z",
}
CL_CODE_MONTHS = {code: month for month, code in CL_MONTH_CODES.items()}
CL_RE = re.compile(r"^CL(?P<month>[FGHJKMNQUVXZ])(?P<year>\d{1,2})(?:\.NYM)?$", re.IGNORECASE)


@dataclass(frozen=True)
class CLContract:
    """Decoded WTI futures contract metadata."""

    contract: str
    year: int
    month: int

    @property
    def yahoo_symbol(self) -> str:
        return f"{self.contract}.NYM"


def cl_contract_symbol(year: int, month: int, *, yahoo: bool = False) -> str:
    """Return the canonical CL contract symbol for a delivery year/month."""
    if month not in CL_MONTH_CODES:
        raise ValueError("month must be in 1..12")
    if year < 2000 or year > 2099:
        raise ValueError("year must be a four-digit year in 2000..2099")
    symbol = f"CL{CL_MONTH_CODES[month]}{year % 100:02d}"
    return f"{symbol}.NYM" if yahoo else symbol


def parse_cl_contract(symbol: str) -> CLContract:
    """Decode ``CLV26`` or ``CLV26.NYM`` into delivery year/month."""
    match = CL_RE.fullmatch(symbol.strip())
    if match is None:
        raise ValueError(f"Unrecognized CL contract symbol: {symbol}")
    token = match.group("year")
    year = 2020 + int(token) if len(token) == 1 else 2000 + int(token)
    month = CL_CODE_MONTHS[match.group("month").upper()]
    contract = cl_contract_symbol(year, month)
    return CLContract(contract=contract, year=year, month=month)


def cl_contract_strip(start: str | pd.Timestamp, end: str | pd.Timestamp, *, lead_months: int = 2) -> list[str]:
    """Generate monthly CL symbols spanning a historical interval.

    ``lead_months`` extends the delivery strip beyond ``end`` so the active
    first-nearby contract and the next curve points are available.
    """
    if lead_months < 0:
        raise ValueError("lead_months must be non-negative")
    start_ts = pd.Timestamp(start).normalize()
    end_ts = pd.Timestamp(end).normalize()
    if end_ts < start_ts:
        raise ValueError("end precedes start")
    first = start_ts.to_period("M") + 1
    last = end_ts.to_period("M") + lead_months
    return [
        cl_contract_symbol(period.year, period.month)
        for period in pd.period_range(first, last, freq="M")
    ]


def _flatten_columns(frame: pd.DataFrame) -> pd.DataFrame:
    out = frame.copy()
    if isinstance(out.columns, pd.MultiIndex):
        out.columns = [str(col[0]) for col in out.columns]
    return out


def normalize_yahoo_contract_history(frame: pd.DataFrame, contract: str) -> pd.DataFrame:
    """Normalize one Yahoo futures history to a stable contract/date schema."""
    decoded = parse_cl_contract(contract)
    if frame is None or len(frame) == 0:
        raise ValueError(f"Yahoo history is empty for {decoded.contract}")

    out = _flatten_columns(frame)
    if "trade_date" not in out.columns and "date" not in out.columns:
        out = out.reset_index()
        date_col = "Date" if "Date" in out.columns else out.columns[0]
        out = out.rename(columns={date_col: "trade_date"})
    elif "date" in out.columns and "trade_date" not in out.columns:
        out = out.rename(columns={"date": "trade_date"})

    rename = {
        "Open": "open", "High": "high", "Low": "low", "Close": "close",
        "Adj Close": "adj_close", "Volume": "volume",
    }
    out = out.rename(columns=rename)
    if "trade_date" not in out.columns or "close" not in out.columns:
        raise ValueError("Yahoo contract history requires a date and Close column")

    keep = [
        col for col in ["trade_date", "open", "high", "low", "close", "adj_close", "volume"]
        if col in out.columns
    ]
    out = out[keep].copy()
    out["trade_date"] = (
        pd.to_datetime(out["trade_date"], utc=True, errors="coerce")
        .dt.tz_convert(None).dt.normalize()
    )
    for col in [c for c in keep if c != "trade_date"]:
        out[col] = pd.to_numeric(out[col], errors="coerce")
    out = out.dropna(subset=["trade_date", "close"])
    out = out.sort_values("trade_date").drop_duplicates("trade_date", keep="last")
    out["contract"] = decoded.contract
    out["yahoo_symbol"] = decoded.yahoo_symbol
    out["delivery_year"] = decoded.year
    out["delivery_month"] = decoded.month
    return out.reset_index(drop=True)


def _parse_expiry_value(value: Any) -> pd.Timestamp | None:
    if value is None or (isinstance(value, float) and np.isnan(value)):
        return None
    try:
        if isinstance(value, (int, float, np.integer, np.floating)):
            ts = pd.to_datetime(int(value), unit="s", utc=True)
        else:
            ts = pd.to_datetime(value, utc=True)
        return pd.Timestamp(ts).tz_convert(None).normalize()
    except Exception:
        return None


def extract_yahoo_settlement_date(info: dict[str, Any]) -> tuple[pd.Timestamp | None, str | None]:
    """Extract a futures expiration/settlement date from Yahoo quote metadata."""
    for key in ("expireDate", "expirationDate", "settlementDate", "lastTradeDate"):
        if key in info:
            parsed = _parse_expiry_value(info.get(key))
            if parsed is not None:
                return parsed, f"yahoo_info:{key}"
    return None, None


def _frame_sha256(frame: pd.DataFrame) -> str:
    payload = frame.to_csv(index=False, date_format="%Y-%m-%d").encode("utf-8")
    return sha256(payload).hexdigest()


def download_yahoo_cl_contract(
    contract: str,
    *,
    start: str | None = None,
    end: str | None = None,
    period: str = "max",
) -> tuple[pd.DataFrame, dict[str, Any]]:
    """Download one individual WTI futures contract from Yahoo via yfinance."""
    decoded = parse_cl_contract(contract)
    try:
        import yfinance as yf  # type: ignore
    except ImportError as exc:
        raise RuntimeError("yfinance is required; install the project with the 'market' extra") from exc

    ticker = yf.Ticker(decoded.yahoo_symbol)
    kwargs: dict[str, Any] = {
        "interval": "1d", "auto_adjust": False, "actions": False,
        "repair": False, "raise_errors": True,
    }
    if start is not None or end is not None:
        kwargs.update({"start": start, "end": end})
    else:
        kwargs["period"] = period

    raw = ticker.history(**kwargs)
    history = normalize_yahoo_contract_history(raw, decoded.contract)
    info: dict[str, Any] = {}
    try:
        candidate = ticker.info
        if isinstance(candidate, dict):
            info = candidate
    except Exception:
        info = {}

    settlement_date, expiry_source = extract_yahoo_settlement_date(info)
    metadata: dict[str, Any] = {
        "provider": "Yahoo Finance via yfinance",
        "contract": decoded.contract,
        "yahoo_symbol": decoded.yahoo_symbol,
        "first_observation": history["trade_date"].min().date().isoformat(),
        "last_observation": history["trade_date"].max().date().isoformat(),
        "rows": int(len(history)),
        "settlement_date": None if settlement_date is None else settlement_date.date().isoformat(),
        "settlement_date_source": expiry_source,
        "close_interpretation": "Yahoo daily Close; settlement proxy pending source validation",
        "sha256": _frame_sha256(history),
        "yfinance_version": getattr(yf, "__version__", None),
    }
    return history, metadata


def download_or_load_yahoo_cl_strip(
    contracts: Iterable[str],
    *,
    directory: str | Path,
    start: str | None = None,
    end: str | None = None,
    refresh: bool = False,
    pause_seconds: float = 0.15,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Cache and combine individual Yahoo CL histories."""
    directory = Path(directory)
    directory.mkdir(parents=True, exist_ok=True)
    histories: list[pd.DataFrame] = []
    rows: list[dict[str, Any]] = []

    for raw_contract in contracts:
        decoded = parse_cl_contract(raw_contract)
        csv_path = directory / f"{decoded.contract}.csv"
        meta_path = directory / f"{decoded.contract}.json"

        if csv_path.exists() and meta_path.exists() and not refresh:
            history = normalize_yahoo_contract_history(pd.read_csv(csv_path), decoded.contract)
            metadata = json.loads(meta_path.read_text(encoding="utf-8"))
        else:
            history, metadata = download_yahoo_cl_contract(decoded.contract, start=start, end=end)
            history.to_csv(csv_path, index=False, date_format="%Y-%m-%d")
            meta_path.write_text(json.dumps(metadata, indent=2, sort_keys=True) + "\n", encoding="utf-8")
            if pause_seconds:
                time.sleep(pause_seconds)

        settlement = metadata.get("settlement_date")
        source = metadata.get("settlement_date_source")
        if settlement is None:
            latest = pd.Timestamp(history["trade_date"].max()).normalize()
            today = pd.Timestamp.utcnow().tz_localize(None).normalize()
            if latest <= today - pd.Timedelta(days=3):
                settlement = latest.date().isoformat()
                source = "history_last_observation_fallback"
        metadata = dict(metadata)
        metadata["settlement_date"] = settlement
        metadata["settlement_date_source"] = source
        meta_path.write_text(json.dumps(metadata, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        histories.append(history)
        rows.append(metadata)

    if not histories:
        raise ValueError("No CL contracts supplied")
    panel = pd.concat(histories, ignore_index=True, sort=False)
    panel = panel.sort_values(["trade_date", "delivery_year", "delivery_month"]).reset_index(drop=True)
    return panel, pd.DataFrame(rows)


def expiry_table_from_yahoo_metadata(metadata: pd.DataFrame) -> pd.DataFrame:
    """Return the explicit contract/last-trade table required by APO roll logic."""
    required = {"contract", "settlement_date", "settlement_date_source"}
    missing = required.difference(metadata.columns)
    if missing:
        raise ValueError(f"metadata missing columns: {sorted(missing)}")
    out = metadata[["contract", "settlement_date", "settlement_date_source"]].copy()
    out["last_trade_date"] = pd.to_datetime(out["settlement_date"], errors="coerce")
    missing_contracts = out.loc[out["last_trade_date"].isna(), "contract"].tolist()
    if missing_contracts:
        raise ValueError("Missing Yahoo settlement/expiration metadata for contracts: " + ", ".join(missing_contracts))
    return out[["contract", "last_trade_date", "settlement_date_source"]].sort_values("last_trade_date").reset_index(drop=True)


def futures_curve_on_date(
    panel: pd.DataFrame,
    valuation_date: str | pd.Timestamp,
    *,
    contracts: Iterable[str] | None = None,
) -> pd.DataFrame:
    """Extract an exact-date CL curve from contract-specific Yahoo histories."""
    date = pd.Timestamp(valuation_date).normalize()
    required = {"trade_date", "contract", "close"}
    missing = required.difference(panel.columns)
    if missing:
        raise ValueError(f"panel missing columns: {sorted(missing)}")
    work = panel.copy()
    work["trade_date"] = pd.to_datetime(work["trade_date"]).dt.normalize()
    work = work[work["trade_date"] == date]
    if contracts is not None:
        wanted = {parse_cl_contract(c).contract for c in contracts}
        work = work[work["contract"].isin(wanted)]
        missing_contracts = sorted(wanted.difference(set(work["contract"])))
        if missing_contracts:
            raise ValueError(f"No exact Yahoo close on {date.date()} for: {missing_contracts}")
    if work.empty:
        raise ValueError(f"No exact Yahoo futures observations on {date.date()}")
    out = work[["contract", "close"]].dropna().drop_duplicates("contract", keep="last")
    return out.rename(columns={"close": "settlement"}).reset_index(drop=True)


def reconstruct_first_nearby_history(
    panel: pd.DataFrame,
    contract_expiries: pd.DataFrame,
    *,
    start: str | None = None,
    end: str | None = None,
) -> pd.DataFrame:
    """Reconstruct daily first-nearby CL history and exclude returns spanning rolls."""
    work = panel.copy()
    work["trade_date"] = pd.to_datetime(work["trade_date"]).dt.normalize()
    if start is not None:
        work = work[work["trade_date"] >= pd.Timestamp(start)]
    if end is not None:
        work = work[work["trade_date"] <= pd.Timestamp(end)]
    dates = pd.DatetimeIndex(sorted(work["trade_date"].dropna().unique()))
    mapping = assign_first_nearby_contract(dates, contract_expiries)
    joined = mapping.merge(
        work[["trade_date", "contract", "close"]],
        left_on=["fixing_date", "contract"], right_on=["trade_date", "contract"], how="left",
    )
    joined = joined.drop(columns=["trade_date"]).rename(columns={"fixing_date": "trade_date"})
    joined = joined.sort_values("trade_date").reset_index(drop=True)
    joined["roll_switch"] = joined["contract"].ne(joined["contract"].shift(1))
    previous = joined["close"].shift(1)
    same_contract = ~joined["roll_switch"]
    valid = same_contract & (joined["close"] > 0) & (previous > 0)
    joined["log_return"] = np.nan
    joined.loc[valid, "log_return"] = np.log(joined.loc[valid, "close"] / previous.loc[valid])
    joined["usable_inference_return"] = joined["log_return"].notna()
    return joined


def compare_futures_reference(
    yahoo_panel: pd.DataFrame,
    reference: pd.DataFrame,
    *,
    reference_price_col: str = "close",
) -> pd.DataFrame:
    """Compare Yahoo closes with an external contract/date validation table."""
    required = {"trade_date", "contract", reference_price_col}
    missing = required.difference(reference.columns)
    if missing:
        raise ValueError(f"reference missing columns: {sorted(missing)}")
    lhs = yahoo_panel[["trade_date", "contract", "close"]].copy()
    lhs["trade_date"] = pd.to_datetime(lhs["trade_date"]).dt.normalize()
    rhs = reference[["trade_date", "contract", reference_price_col]].copy()
    rhs["trade_date"] = pd.to_datetime(rhs["trade_date"]).dt.normalize()
    rhs = rhs.rename(columns={reference_price_col: "reference_price"})
    out = rhs.merge(lhs, on=["trade_date", "contract"], how="left")
    out["difference"] = out["close"] - out["reference_price"]
    out["absolute_difference"] = out["difference"].abs()
    return out
