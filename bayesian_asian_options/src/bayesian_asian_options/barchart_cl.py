"""Barchart NYMEX WTI (CL) futures-history utilities.

The empirical APO application stores one Barchart ``Daily Prices`` CSV per CL
contract under ``data/csv/CL``.  Files contain the Barchart fields ``Time``,
``Open``, ``High``, ``Low``, ``Latest``, ``Change``, ``%Change``, ``Volume``
and ``Open Int``.

``Latest`` is retained as the source field and is used as an end-of-day futures
price / settlement proxy for the empirical pilot.  It is not silently relabeled
as an official CME settlement.  Exact contract last-trade dates are supplied
through a separate versioned reference table.
"""

from __future__ import annotations

from hashlib import sha256
from pathlib import Path
import re
from typing import Iterable

import numpy as np
import pandas as pd

from bayesian_asian_options.wti_yahoo_futures import parse_cl_contract


_BARCHART_CL_RE = re.compile(r"^CL[FGHJKMNQUVXZ]\d{2}\.csv$", re.IGNORECASE)


def _numeric(series: pd.Series) -> pd.Series:
    return pd.to_numeric(
        series.astype(str)
        .str.replace(",", "", regex=False)
        .replace({"N/A": np.nan, "NA": np.nan, "nan": np.nan, "": np.nan, "unch": 0.0}),
        errors="coerce",
    )


def discover_barchart_cl_histories(root: str | Path) -> list[Path]:
    """Return contract-level Barchart CL history CSVs below ``root``."""
    root = Path(root)
    return sorted(path for path in root.rglob("*.csv") if _BARCHART_CL_RE.fullmatch(path.name))


def load_barchart_cl_history(path: str | Path) -> pd.DataFrame:
    """Normalize one Barchart CL ``Daily Prices`` history.

    The contract is decoded from the filename, for example ``CLX26.csv``.
    Returned rows are sorted ascending by trade date.
    """
    path = Path(path)
    if not _BARCHART_CL_RE.fullmatch(path.name):
        raise ValueError(f"Unrecognized Barchart CL filename: {path.name}")
    decoded = parse_cl_contract(path.stem)
    raw = pd.read_csv(path, encoding="utf-8-sig")
    required = {"Time", "Latest"}
    missing = required.difference(raw.columns)
    if missing:
        raise ValueError(f"{path.name}: missing Barchart columns {sorted(missing)}")

    dates = pd.to_datetime(raw["Time"], errors="coerce").dt.normalize()
    valid = dates.notna()
    raw = raw.loc[valid].copy()
    dates = dates.loc[valid]
    if raw.empty:
        raise ValueError(f"{path.name}: no valid daily rows")

    mapping = {
        "Open": "open",
        "High": "high",
        "Low": "low",
        "Latest": "latest",
        "Change": "change",
        "Volume": "volume",
        "Open Int": "open_interest",
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

    out = out.dropna(subset=["trade_date", "latest"])
    out["contract"] = decoded.contract
    out["delivery_year"] = decoded.year
    out["delivery_month"] = decoded.month
    out["source_file"] = path.name
    out["source_field"] = "Latest"
    out["price_interpretation"] = "Barchart Daily Prices Latest; end-of-day settlement proxy"
    return out.sort_values("trade_date").drop_duplicates("trade_date", keep="last").reset_index(drop=True)


def _raw_sha256(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def load_barchart_cl_strip(
    root: str | Path,
    *,
    contracts: Iterable[str] | None = None,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Load a strict set of Barchart CL histories and return panel plus manifest.

    If ``contracts`` is supplied, every requested contract must have exactly one
    matching CSV.  This fail-fast behavior prevents a partially observed term
    structure from being used silently in option valuation.
    """
    root = Path(root)
    paths = discover_barchart_cl_histories(root)
    by_contract: dict[str, list[Path]] = {}
    for path in paths:
        contract = parse_cl_contract(path.stem).contract
        by_contract.setdefault(contract, []).append(path)

    duplicates = {key: value for key, value in by_contract.items() if len(value) > 1}
    if duplicates:
        detail = ", ".join(f"{key} ({len(value)} files)" for key, value in sorted(duplicates.items()))
        raise ValueError(f"Duplicate Barchart CL histories found: {detail}")

    if contracts is None:
        requested = sorted(by_contract)
    else:
        requested = [parse_cl_contract(contract).contract for contract in contracts]
        requested = list(dict.fromkeys(requested))
    missing = [contract for contract in requested if contract not in by_contract]
    if missing:
        raise ValueError(
            f"Missing Barchart CL histories in {root}: " + ", ".join(missing)
        )
    if not requested:
        raise ValueError(f"No Barchart CL histories found in {root}")

    frames: list[pd.DataFrame] = []
    manifest_rows: list[dict[str, object]] = []
    for contract in requested:
        path = by_contract[contract][0]
        frame = load_barchart_cl_history(path)
        frames.append(frame)
        manifest_rows.append(
            {
                "provider": "Barchart Daily Prices",
                "contract": contract,
                "source_file": path.name,
                "rows": int(len(frame)),
                "first_observation": frame["trade_date"].min().date().isoformat(),
                "last_observation": frame["trade_date"].max().date().isoformat(),
                "price_field": "Latest",
                "price_interpretation": "end-of-day settlement proxy",
                "sha256": _raw_sha256(path),
            }
        )

    panel = pd.concat(frames, ignore_index=True, sort=False)
    panel = panel.sort_values(["trade_date", "delivery_year", "delivery_month"]).reset_index(drop=True)
    return panel, pd.DataFrame(manifest_rows)


def barchart_cl_curve_on_date(
    panel: pd.DataFrame,
    valuation_date: str | pd.Timestamp,
    *,
    contracts: Iterable[str] | None = None,
) -> pd.DataFrame:
    """Extract an exact-date CL term structure from normalized Barchart histories.

    The returned ``settlement`` column is the Barchart ``Latest`` field copied
    into the generic pricing interface.  Its source interpretation remains a
    settlement proxy, not an official CME settlement claim.
    """
    required = {"trade_date", "contract", "latest"}
    missing_columns = required.difference(panel.columns)
    if missing_columns:
        raise ValueError(f"Barchart CL panel missing columns: {sorted(missing_columns)}")

    target = pd.Timestamp(valuation_date).normalize()
    work = panel.copy()
    work["trade_date"] = pd.to_datetime(work["trade_date"]).dt.normalize()
    work = work[work["trade_date"] == target]
    if contracts is not None:
        wanted = [parse_cl_contract(contract).contract for contract in contracts]
        wanted = list(dict.fromkeys(wanted))
        work = work[work["contract"].isin(wanted)]
        missing = sorted(set(wanted).difference(set(work["contract"])))
        if missing:
            raise ValueError(
                f"No exact Barchart CL price on {target.date()} for: {', '.join(missing)}"
            )
    if work.empty:
        raise ValueError(f"No Barchart CL observations on {target.date()}")

    columns = [
        "contract", "latest", "open", "high", "low", "volume", "open_interest",
        "source_file", "source_field", "price_interpretation",
    ]
    available = [column for column in columns if column in work.columns]
    out = work[available].drop_duplicates("contract", keep="last").copy()
    out = out.rename(columns={"latest": "settlement"})
    return out.sort_values("contract").reset_index(drop=True)


def load_cl_expiry_table(
    path: str | Path,
    *,
    contracts: Iterable[str] | None = None,
) -> pd.DataFrame:
    """Load an explicit CL contract last-trade-date reference table."""
    path = Path(path)
    raw = pd.read_csv(path, encoding="utf-8-sig")
    required = {"contract", "last_trade_date"}
    missing_columns = required.difference(raw.columns)
    if missing_columns:
        raise ValueError(f"{path.name}: missing columns {sorted(missing_columns)}")

    out = raw.copy()
    out["contract"] = out["contract"].map(lambda value: parse_cl_contract(str(value)).contract)
    out["last_trade_date"] = pd.to_datetime(out["last_trade_date"], errors="raise").dt.normalize()
    if out["contract"].duplicated().any():
        duplicates = sorted(out.loc[out["contract"].duplicated(keep=False), "contract"].unique())
        raise ValueError(f"Duplicate contracts in expiry table: {duplicates}")
    if "source" not in out:
        out["source"] = "unspecified"

    if contracts is not None:
        wanted = [parse_cl_contract(contract).contract for contract in contracts]
        wanted = list(dict.fromkeys(wanted))
        missing = sorted(set(wanted).difference(set(out["contract"])))
        if missing:
            raise ValueError(f"Expiry table missing contracts: {', '.join(missing)}")
        out = out[out["contract"].isin(wanted)]
    return out[["contract", "last_trade_date", "source"]].sort_values("last_trade_date").reset_index(drop=True)


def compare_barchart_cl_reference(
    panel: pd.DataFrame,
    reference: pd.DataFrame,
    *,
    reference_price_col: str = "close",
) -> pd.DataFrame:
    """Compare Barchart ``Latest`` with an external contract/date price table."""
    required = {"trade_date", "contract", reference_price_col}
    missing = required.difference(reference.columns)
    if missing:
        raise ValueError(f"reference missing columns: {sorted(missing)}")
    left = panel[["trade_date", "contract", "latest"]].copy()
    left["trade_date"] = pd.to_datetime(left["trade_date"]).dt.normalize()
    right = reference[["trade_date", "contract", reference_price_col]].copy()
    right["trade_date"] = pd.to_datetime(right["trade_date"]).dt.normalize()
    right["contract"] = right["contract"].map(lambda value: parse_cl_contract(str(value)).contract)
    right[reference_price_col] = pd.to_numeric(right[reference_price_col], errors="coerce")
    out = right.merge(left, on=["trade_date", "contract"], how="left")
    out = out.rename(columns={reference_price_col: "reference_price", "latest": "barchart_latest"})
    out["difference"] = out["barchart_latest"] - out["reference_price"]
    out["absolute_difference"] = out["difference"].abs()
    return out.sort_values(["trade_date", "contract"]).reset_index(drop=True)
