"""Recent-history volatility benchmarks on the strict forward APO holdouts.

This experiment evaluates a small, pre-specified set of purely historical
volatility estimators on exactly the same contract-date holdouts used by the
strict forward APO validation:

* rolling 63-business-day realized volatility;
* rolling 126-business-day realized volatility;
* rolling 252-business-day realized volatility;
* exponentially weighted realized volatility with a 63-business-day half-life.

Only returns marked usable in each target-date run inference audit are used.
Those audits were already constructed with the target-date information cutoff,
so no future return enters any benchmark. Pricing uses the same Curran
one-factor APO engine used for the forward option-implied predictions.

The script is deterministic and does not re-estimate any option-implied surface.
"""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

from experiments.wti_forward_q_validation import _price_targets, _run_lookup


DEFAULT_FORWARD = Path(
    "results/analysis/wti_extended_forward/forward_q_validation/forward_q_predictions.csv"
)
DEFAULT_RUNS = Path("results/wti_apo_empirical")
DEFAULT_OUTPUT = Path("results/analysis/wti_recent_historical_benchmarks")
DEFAULT_EXPIRIES = (
    "2026-09",
    "2026-10",
    "2026-11",
    "2027-03",
    "2027-09",
    "2028-03",
    "2028-09",
)


def rolling_sigma(
    returns: np.ndarray,
    window: int,
    periods_per_year: int = 252,
) -> float:
    """Annualized sample volatility from the most recent return window."""
    x = np.asarray(returns, dtype=float)
    if window < 2:
        raise ValueError("window must be at least 2")
    if x.size < window:
        raise ValueError(f"need at least {window} returns, got {x.size}")
    tail = x[-window:]
    return float(np.std(tail, ddof=1) * np.sqrt(periods_per_year))


def ewma_sigma(
    returns: np.ndarray,
    half_life: float,
    periods_per_year: int = 252,
) -> float:
    """Annualized exponentially weighted volatility around a weighted mean."""
    x = np.asarray(returns, dtype=float)
    if x.size < 2:
        raise ValueError("at least two returns are required")
    if half_life <= 0:
        raise ValueError("half_life must be positive")
    age = np.arange(x.size - 1, -1, -1, dtype=float)
    weights = np.exp(-np.log(2.0) * age / float(half_life))
    weights /= weights.sum()
    mean = float(np.sum(weights * x))
    variance = float(np.sum(weights * (x - mean) ** 2))
    return float(np.sqrt(max(variance, 0.0) * periods_per_year))


def _usable_returns(run_dir: Path) -> np.ndarray:
    audit = pd.read_csv(run_dir / "inference_return_audit.csv")
    required = {"log_return", "usable_inference_return"}
    missing = required.difference(audit.columns)
    if missing:
        raise ValueError(
            f"{run_dir} return audit missing columns: {sorted(missing)}"
        )
    usable = (
        audit["usable_inference_return"]
        .astype(str)
        .str.lower()
        .isin({"true", "1"})
    )
    values = pd.to_numeric(
        audit.loc[usable, "log_return"], errors="coerce"
    ).dropna()
    if values.empty:
        raise ValueError(f"{run_dir} has no usable returns")
    return values.to_numpy(dtype=float)


def _targets(
    forward_path: Path,
    expiries: tuple[str, ...],
) -> pd.DataFrame:
    frame = pd.read_csv(forward_path)
    frame = frame[frame["apo_expiry"].astype(str).isin(expiries)].copy()
    keep = [
        "valuation_date",
        "apo_expiry",
        "contract_id",
        "option_type",
        "strike",
        "log_moneyness",
        "market_settlement",
        "open_interest",
        "volume",
        "positive_volume",
        "baseline_pi_price",
        "baseline_pi_error",
    ]
    missing = set(keep).difference(frame.columns)
    if missing:
        raise ValueError(
            f"forward predictions missing columns: {sorted(missing)}"
        )
    frame = frame[keep].drop_duplicates(
        ["valuation_date", "apo_expiry", "contract_id"],
        keep="first",
    )
    frame["valuation_date"] = pd.to_datetime(
        frame["valuation_date"]
    ).dt.normalize()
    return frame.sort_values(
        ["valuation_date", "apo_expiry", "contract_id"]
    ).reset_index(drop=True)


def summarize(predictions: pd.DataFrame) -> pd.DataFrame:
    """Summarize errors pooled and by expiry."""
    rows: list[dict[str, Any]] = []
    scopes: list[tuple[str, str, pd.DataFrame]] = [
        ("pooled", "all", predictions)
    ]
    for expiry, group in predictions.groupby("apo_expiry", sort=True):
        scopes.append(("expiry", str(expiry), group))

    for scope, expiry, scoped in scopes:
        for method, group in scoped.groupby("method", sort=True):
            error = group["error"].to_numpy(dtype=float)
            rows.append(
                {
                    "scope": scope,
                    "apo_expiry": expiry,
                    "method": method,
                    "n": int(len(group)),
                    "n_dates": int(group["valuation_date"].nunique()),
                    "mean_sigma": float(group["sigma_hat"].mean()),
                    "mean_error": float(np.mean(error)),
                    "mae": float(np.mean(np.abs(error))),
                    "rmse": float(np.sqrt(np.mean(error**2))),
                }
            )
    return pd.DataFrame(rows)


def run(
    forward_path: Path,
    runs_root: Path,
    output_dir: Path,
    *,
    expiries: tuple[str, ...],
    windows: tuple[int, ...],
    ewma_half_life: float,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    targets = _targets(forward_path, expiries)
    lookup = _run_lookup(runs_root, list(expiries))
    rows: list[dict[str, Any]] = []

    grouped = targets.groupby(
        ["valuation_date", "apo_expiry"],
        sort=True,
    )
    for (date_raw, expiry), target in grouped:
        date = pd.Timestamp(date_raw).normalize()
        key = (date.strftime("%Y-%m-%d"), str(expiry))
        run_dir = lookup.get(key)
        if run_dir is None:
            raise FileNotFoundError(f"missing empirical run for {key}")
        returns = _usable_returns(run_dir)

        estimates: dict[str, float] = {}
        for window in windows:
            if len(returns) >= window:
                estimates[f"rolling_{window}"] = rolling_sigma(
                    returns, window
                )
        estimates[f"ewma_hl_{int(ewma_half_life)}"] = ewma_sigma(
            returns,
            ewma_half_life,
        )

        for method, sigma in estimates.items():
            sigma_vector = np.full(len(target), sigma, dtype=float)
            prices = _price_targets(
                target,
                sigma_vector,
                run_dir=run_dir,
            )
            for row, price in zip(
                target.itertuples(index=False),
                prices,
                strict=True,
            ):
                market = float(row.market_settlement)
                rows.append(
                    {
                        "method": method,
                        "valuation_date": date.strftime("%Y-%m-%d"),
                        "apo_expiry": str(expiry),
                        "contract_id": str(row.contract_id),
                        "option_type": str(row.option_type),
                        "strike": float(row.strike),
                        "log_moneyness": float(row.log_moneyness),
                        "market_settlement": market,
                        "open_interest": float(row.open_interest)
                        if pd.notna(row.open_interest)
                        else np.nan,
                        "volume": float(row.volume)
                        if pd.notna(row.volume)
                        else np.nan,
                        "positive_volume": bool(row.positive_volume),
                        "n_usable_returns": int(len(returns)),
                        "sigma_hat": float(sigma),
                        "price": float(price),
                        "error": float(price - market),
                        "baseline_pi_price": float(row.baseline_pi_price),
                        "baseline_pi_error": float(
                            row.baseline_pi_error
                        ),
                    }
                )

    predictions = pd.DataFrame(rows)
    summary = summarize(predictions)
    output_dir.mkdir(parents=True, exist_ok=True)
    predictions.to_csv(
        output_dir / "recent_historical_predictions.csv",
        index=False,
    )
    summary.to_csv(
        output_dir / "recent_historical_error_summary.csv",
        index=False,
    )
    return predictions, summary


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--forward-path",
        type=Path,
        default=DEFAULT_FORWARD,
    )
    parser.add_argument(
        "--runs-root",
        type=Path,
        default=DEFAULT_RUNS,
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=DEFAULT_OUTPUT,
    )
    parser.add_argument(
        "--expiries",
        nargs="+",
        default=list(DEFAULT_EXPIRIES),
    )
    parser.add_argument("--windows", default="63,126,252")
    parser.add_argument("--ewma-half-life", type=float, default=63.0)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    windows = tuple(
        int(value.strip())
        for value in args.windows.split(",")
        if value.strip()
    )
    if not windows:
        raise ValueError("at least one rolling window is required")
    _, summary = run(
        args.forward_path,
        args.runs_root,
        args.output_dir,
        expiries=tuple(args.expiries),
        windows=windows,
        ewma_half_life=float(args.ewma_half_life),
    )
    print(summary.to_string(index=False))
    print(f"output_dir={args.output_dir}")


if __name__ == "__main__":
    main()
