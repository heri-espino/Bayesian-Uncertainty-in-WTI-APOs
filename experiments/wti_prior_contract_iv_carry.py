"""Prior contract-IV carry benchmark on strict forward APO holdouts.

For each target contract-date, the benchmark finds that same contract's latest
available APO implied volatility strictly before the target date and reprices the
contract under the current target-date futures curve, realized fixings, discount
factor, and remaining fixing schedule.

This is a persistence benchmark: it asks how much the fitted previous-day smile
adds beyond simply carrying a contract's own prior mark forward after a transparent
current-state adjustment. No same-day APO price enters the prediction.
"""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

from experiments.wti_forward_q_validation import _price_targets, _run_lookup


DEFAULT_APO_IV = Path(
    "results/analysis/wti_extended_forward/apo_implied_volatility/apo_contract_implied_volatility.csv"
)
DEFAULT_FORWARD = Path(
    "results/analysis/wti_extended_forward/forward_q_validation/forward_q_predictions.csv"
)
DEFAULT_RUNS = Path("results/wti_apo_empirical")
DEFAULT_OUTPUT = Path("results/analysis/wti_prior_contract_iv_carry")
DEFAULT_EXPIRIES = (
    "2026-09",
    "2026-10",
    "2026-11",
    "2027-03",
    "2027-09",
    "2028-03",
    "2028-09",
)


def _targets(forward_path: Path, expiries: tuple[str, ...]) -> pd.DataFrame:
    frame = pd.read_csv(forward_path)
    frame = frame[
        frame["apo_expiry"].astype(str).isin(expiries)
        & frame["method"].astype(str).eq("previous_day_smile")
    ].copy()
    keep = [
        "valuation_date",
        "apo_expiry",
        "contract_id",
        "option_type",
        "strike",
        "market_settlement",
        "open_interest",
        "volume",
        "positive_volume",
        "baseline_pi_price",
        "baseline_pi_error",
        "forward_q_price",
        "forward_error",
    ]
    frame = frame[keep].drop_duplicates(
        ["valuation_date", "apo_expiry", "contract_id"],
        keep="first",
    )
    frame["valuation_date"] = pd.to_datetime(
        frame["valuation_date"]
    ).dt.normalize()
    return frame


def _latest_prior_iv(
    history: pd.DataFrame,
    *,
    contract_id: str,
    target_date: pd.Timestamp,
) -> tuple[float, pd.Timestamp] | None:
    prior = history[
        history["contract_id"].astype(str).eq(str(contract_id))
        & (history["valuation_ts"] < target_date)
        & history["apo_implied_sigma_q"].notna()
    ].copy()
    if prior.empty:
        return None
    latest = pd.Timestamp(prior["valuation_ts"].max()).normalize()
    row = prior[prior["valuation_ts"].eq(latest)].iloc[-1]
    return float(row["apo_implied_sigma_q"]), latest


def summarize(predictions: pd.DataFrame) -> pd.DataFrame:
    """Compare carry, previous-day smile, and historical PI on exact rows."""
    rows: list[dict[str, Any]] = []
    scopes: list[tuple[str, str, pd.DataFrame]] = [
        ("pooled", "all", predictions)
    ]
    for expiry, group in predictions.groupby("apo_expiry", sort=True):
        scopes.append(("expiry", str(expiry), group))

    methods = (
        ("prior_contract_iv_carry", "carry_error"),
        ("previous_day_smile", "previous_day_smile_error"),
        ("historical_pi", "baseline_pi_error"),
    )
    for scope, expiry, scoped in scopes:
        for method, column in methods:
            error = scoped[column].to_numpy(dtype=float)
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
    apo_iv_path: Path,
    forward_path: Path,
    runs_root: Path,
    output_dir: Path,
    *,
    expiries: tuple[str, ...],
) -> tuple[pd.DataFrame, pd.DataFrame]:
    history = pd.read_csv(apo_iv_path)
    history = history[history["apo_expiry"].astype(str).isin(expiries)].copy()
    history["valuation_ts"] = pd.to_datetime(
        history["valuation_date"]
    ).dt.normalize()

    targets = _targets(forward_path, expiries)
    lookup = _run_lookup(runs_root, list(expiries))
    rows: list[dict[str, Any]] = []

    grouped = targets.groupby(
        ["valuation_date", "apo_expiry"],
        sort=True,
    )
    for (date_raw, expiry), target in grouped:
        date = pd.Timestamp(date_raw).normalize()
        run_dir = lookup.get((date.strftime("%Y-%m-%d"), str(expiry)))
        if run_dir is None:
            raise FileNotFoundError(
                f"missing empirical run for {(date, expiry)}"
            )

        available_rows = []
        sigmas = []
        prior_dates = []
        for row in target.itertuples(index=False):
            prior = _latest_prior_iv(
                history,
                contract_id=str(row.contract_id),
                target_date=date,
            )
            if prior is None:
                continue
            sigma, prior_date = prior
            available_rows.append(row._asdict())
            sigmas.append(sigma)
            prior_dates.append(prior_date)

        if not available_rows:
            continue
        available = pd.DataFrame(available_rows)
        prices = _price_targets(
            available,
            np.asarray(sigmas, dtype=float),
            run_dir=run_dir,
        )
        for row, sigma, prior_date, price in zip(
            available.itertuples(index=False),
            sigmas,
            prior_dates,
            prices,
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
                    "prior_iv_date": prior_date.strftime("%Y-%m-%d"),
                    "days_since_prior_iv": int((date - prior_date).days),
                    "carried_sigma_q": float(sigma),
                    "carry_price": float(price),
                    "carry_error": float(price - market),
                    "previous_day_smile_price": float(row.forward_q_price),
                    "previous_day_smile_error": float(row.forward_error),
                    "baseline_pi_price": float(row.baseline_pi_price),
                    "baseline_pi_error": float(row.baseline_pi_error),
                }
            )

    predictions = pd.DataFrame(rows)
    if predictions.empty:
        raise RuntimeError("no contracts have a strictly prior contract IV")
    if not (
        pd.to_datetime(predictions["prior_iv_date"])
        < pd.to_datetime(predictions["valuation_date"])
    ).all():
        raise RuntimeError("same-day APO information entered carry benchmark")

    summary = summarize(predictions)
    output_dir.mkdir(parents=True, exist_ok=True)
    predictions.to_csv(
        output_dir / "prior_contract_iv_carry_predictions.csv",
        index=False,
    )
    summary.to_csv(
        output_dir / "prior_contract_iv_carry_summary.csv",
        index=False,
    )
    return predictions, summary


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--apo-iv-path", type=Path, default=DEFAULT_APO_IV)
    parser.add_argument("--forward-path", type=Path, default=DEFAULT_FORWARD)
    parser.add_argument("--runs-root", type=Path, default=DEFAULT_RUNS)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument(
        "--expiries",
        nargs="+",
        default=list(DEFAULT_EXPIRIES),
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    _, summary = run(
        args.apo_iv_path,
        args.forward_path,
        args.runs_root,
        args.output_dir,
        expiries=tuple(args.expiries),
    )
    print(summary.to_string(index=False))
    print(f"output_dir={args.output_dir}")


if __name__ == "__main__":
    main()
