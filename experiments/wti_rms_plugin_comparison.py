"""Posterior-RMS volatility plug-in comparison on committed WTI APO runs.

For each target-date empirical run, this experiment compares pricing at the
posterior mean volatility with pricing at

    sigma_RMS = sqrt(E[sigma^2 | D]) = sqrt(mean^2 + variance).

The calculation uses the already committed posterior summaries and contract
states.  It is a deterministic sensitivity analysis and does not rerun MCMC.
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
DEFAULT_OUTPUT = Path("results/analysis/wti_rms_plugin_comparison")
DEFAULT_EXPIRIES = (
    "2026-09",
    "2026-10",
    "2026-11",
    "2027-03",
    "2027-09",
    "2028-03",
    "2028-09",
)


def sigma_rms(mean: float, sd: float) -> float:
    """Return sqrt(E[sigma^2]) from posterior mean and standard deviation."""
    if mean <= 0 or sd < 0:
        raise ValueError("mean must be positive and sd non-negative")
    return float(np.sqrt(mean**2 + sd**2))


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


def _posterior_moments(run_dir: Path) -> tuple[float, float]:
    summary = pd.read_csv(run_dir / "posterior_summary.csv")
    if len(summary) != 1:
        raise ValueError(
            f"expected one posterior summary row in {run_dir}"
        )
    mean = float(summary.iloc[0]["sigma_posterior_mean"])
    sd = float(summary.iloc[0]["sigma_posterior_sd"])
    return mean, sd


def summarize(predictions: pd.DataFrame) -> pd.DataFrame:
    """Summarize PM and RMS pricing errors pooled and by expiry."""
    rows: list[dict[str, Any]] = []
    scopes: list[tuple[str, str, pd.DataFrame]] = [
        ("pooled", "all", predictions)
    ]
    for expiry, group in predictions.groupby("apo_expiry", sort=True):
        scopes.append(("expiry", str(expiry), group))

    for scope, expiry, scoped in scopes:
        for method in ("posterior_mean", "posterior_rms"):
            error = scoped[f"{method}_error"].to_numpy(dtype=float)
            rows.append(
                {
                    "scope": scope,
                    "apo_expiry": expiry,
                    "method": method,
                    "n": int(len(scoped)),
                    "n_dates": int(scoped["valuation_date"].nunique()),
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

        mean, sd = _posterior_moments(run_dir)
        rms = sigma_rms(mean, sd)
        pm_prices = _price_targets(
            target,
            np.full(len(target), mean, dtype=float),
            run_dir=run_dir,
        )
        rms_prices = _price_targets(
            target,
            np.full(len(target), rms, dtype=float),
            run_dir=run_dir,
        )

        for row, pm_price, rms_price in zip(
            target.itertuples(index=False),
            pm_prices,
            rms_prices,
            strict=True,
        ):
            market = float(row.market_settlement)
            rows.append(
                {
                    "valuation_date": date.strftime("%Y-%m-%d"),
                    "apo_expiry": str(expiry),
                    "contract_id": str(row.contract_id),
                    "option_type": str(row.option_type),
                    "strike": float(row.strike),
                    "market_settlement": market,
                    "sigma_posterior_mean": mean,
                    "sigma_posterior_sd": sd,
                    "sigma_rms": rms,
                    "sigma_rms_minus_mean": rms - mean,
                    "posterior_mean_price": float(pm_price),
                    "posterior_rms_price": float(rms_price),
                    "rms_minus_mean_price": float(
                        rms_price - pm_price
                    ),
                    "posterior_mean_error": float(pm_price - market),
                    "posterior_rms_error": float(rms_price - market),
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
        output_dir / "rms_plugin_predictions.csv",
        index=False,
    )
    summary.to_csv(
        output_dir / "rms_plugin_error_summary.csv",
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
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    _, summary = run(
        args.forward_path,
        args.runs_root,
        args.output_dir,
        expiries=tuple(args.expiries),
    )
    print(summary.to_string(index=False))
    print(f"output_dir={args.output_dir}")


if __name__ == "__main__":
    main()
