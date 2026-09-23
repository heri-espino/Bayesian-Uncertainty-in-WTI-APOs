"""Databento CME/NYMEX utilities for the WTI external-Q experiment."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

STAT_NAMES = {
    1: "opening_price",
    2: "indicative_opening_price",
    3: "settlement_price",
    4: "session_low",
    5: "session_high",
    6: "cleared_volume",
    7: "lowest_offer",
    8: "highest_bid",
    9: "open_interest",
    10: "fixing_price",
    17: "upper_price_limit",
    18: "lower_price_limit",
}

_STAT_NAME_TO_TYPE = {
    "OPENING_PRICE": 1,
    "INDICATIVE_OPENING_PRICE": 2,
    "SETTLEMENT_PRICE": 3,
    "TRADING_SESSION_LOW_PRICE": 4,
    "TRADING_SESSION_HIGH_PRICE": 5,
    "CLEARED_VOLUME": 6,
    "LOWEST_OFFER": 7,
    "HIGHEST_BID": 8,
    "OPEN_INTEREST": 9,
    "FIXING_PRICE": 10,
    "UPPER_PRICE_LIMIT": 17,
    "LOWER_PRICE_LIMIT": 18,
}


def load_databento_csv(path: str | Path) -> pd.DataFrame:
    """Load one locally cached Databento DataFrame CSV."""
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(path)
    frame = pd.read_csv(path, index_col=0)
    if frame.index.name and frame.index.name not in frame.columns:
        frame = frame.reset_index()
    return frame


def coerce_stat_type(series: pd.Series) -> pd.Series:
    """Normalize numeric or enum-like Databento statistic types."""
    numeric = pd.to_numeric(series, errors="coerce")
    if numeric.notna().all():
        return numeric.astype("Int64")
    text = (
        series.astype(str)
        .str.strip()
        .str.upper()
        .str.replace("STATTYPE.", "", regex=False)
        .str.replace(" ", "_", regex=False)
    )
    mapped = text.map(_STAT_NAME_TO_TYPE)
    return numeric.where(numeric.notna(), mapped).astype("Int64")


def parse_databento_timestamp(series: pd.Series) -> pd.Series:
    """Parse Databento ISO or nanosecond timestamps as UTC pandas timestamps."""
    numeric = pd.to_numeric(series, errors="coerce")
    if numeric.notna().sum() >= max(1, int(0.9 * len(series))):
        return pd.to_datetime(numeric, unit="ns", utc=True, errors="coerce")
    return pd.to_datetime(series, utc=True, errors="coerce")


def normalize_statistics(frame: pd.DataFrame) -> pd.DataFrame:
    """Normalize a Databento statistics DataFrame.

    Adds reference_date, stat_name, received_timestamp, and CME settlement
    flag columns. DataFrame prices from Databento to_df() are already decimal
    floats under its default price_type="float".
    """
    required = {"instrument_id", "stat_type"}
    missing = required.difference(frame.columns)
    if missing:
        raise ValueError(f"Statistics data missing columns: {sorted(missing)}")

    out = frame.copy()
    out["instrument_id"] = pd.to_numeric(
        out["instrument_id"], errors="coerce"
    ).astype("Int64")
    out["stat_type"] = coerce_stat_type(out["stat_type"])

    reference = None
    for column in ("ts_ref", "ts_event", "ts_recv"):
        if column in out.columns:
            parsed = parse_databento_timestamp(out[column])
            if parsed.notna().any():
                reference = parsed
                break
    if reference is None:
        raise ValueError("Statistics data have no usable timestamp")

    out["reference_timestamp"] = reference
    out["reference_date"] = reference.dt.date.astype("string")
    out["stat_name"] = out["stat_type"].map(STAT_NAMES).fillna("other")

    if "ts_recv" in out.columns:
        out["received_timestamp"] = parse_databento_timestamp(out["ts_recv"])
    elif "ts_event" in out.columns:
        out["received_timestamp"] = parse_databento_timestamp(out["ts_event"])
    else:
        out["received_timestamp"] = reference

    if "stat_flags" in out.columns:
        flags = pd.to_numeric(
            out["stat_flags"], errors="coerce"
        ).fillna(0).astype("int64")
    else:
        flags = pd.Series(0, index=out.index, dtype="int64")

    out["settlement_final"] = (
        out["stat_type"].eq(3) & flags.map(lambda x: bool(x & 1))
    )
    out["settlement_actual"] = (
        out["stat_type"].eq(3) & flags.map(lambda x: bool(x & 2))
    )
    out["settlement_trading_tick"] = (
        out["stat_type"].eq(3) & flags.map(lambda x: bool(x & 4))
    )
    out["settlement_intraday"] = (
        out["stat_type"].eq(3) & flags.map(lambda x: bool(x & 8))
    )
    return out


def final_settlements(frame: pd.DataFrame) -> pd.DataFrame:
    """Return latest final end-of-day settlement per instrument/reference date."""
    stats = normalize_statistics(frame)
    settlements = stats[
        stats["stat_type"].eq(3)
        & stats["settlement_final"]
        & ~stats["settlement_intraday"]
    ].copy()
    if settlements.empty:
        return settlements

    if "update_action" in settlements.columns:
        action = settlements["update_action"].astype(str).str.upper()
        settlements = settlements[
            ~action.isin({"2", "DELETE", "DELETED"})
        ].copy()

    settlements = settlements.sort_values(
        ["instrument_id", "reference_date", "received_timestamp"]
    )
    return settlements.drop_duplicates(
        ["instrument_id", "reference_date"], keep="last"
    ).reset_index(drop=True)


def normalize_option_definitions(frame: pd.DataFrame) -> pd.DataFrame:
    """Normalize selected Databento option definitions for IV inversion."""
    required = {
        "instrument_id",
        "underlying_id",
        "raw_symbol",
        "underlying",
        "strike_price",
        "expiration",
        "option_type",
    }
    missing = required.difference(frame.columns)
    if missing:
        raise ValueError(
            f"Selected option definitions missing columns: {sorted(missing)}"
        )

    out = frame.copy()
    out["instrument_id"] = pd.to_numeric(
        out["instrument_id"], errors="coerce"
    ).astype("Int64")
    out["underlying_id"] = pd.to_numeric(
        out["underlying_id"], errors="coerce"
    ).astype("Int64")
    out["strike_price"] = pd.to_numeric(
        out["strike_price"], errors="coerce"
    )

    expiration = out["expiration"]
    numeric = pd.to_numeric(expiration, errors="coerce")
    if numeric.notna().sum() >= max(1, int(0.9 * len(out))):
        out["expiration_timestamp"] = pd.to_datetime(
            numeric, unit="ns", utc=True, errors="coerce"
        )
    else:
        out["expiration_timestamp"] = pd.to_datetime(
            expiration, utc=True, errors="coerce"
        )
    if out["expiration_timestamp"].isna().any():
        raise ValueError("One or more option expirations could not be parsed")
    return out
