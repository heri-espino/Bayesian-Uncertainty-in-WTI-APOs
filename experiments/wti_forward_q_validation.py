"""Strict forward-in-time validation of APO-implied Q volatility surfaces.

Same-day leave-one-out calibration is useful but still uses contemporaneous option prices.
This experiment removes that information.  For each target date and APO expiry, it fits an
implied-volatility smile using only earlier completed dates, predicts sigma_Q for the target
contracts, and prices them using the target day's futures curve and realized fixings.

Two information sets are reported:

* ``previous_day_smile``: only the most recent earlier completed date;
* ``expanding_smile``: all earlier dates, with a five-calendar-day exponential half-life.

The smile is a separate quadratic in log-moneyness for calls and puts, implemented as a
single ridge regression with option-type interactions.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

from bayesian_asian_options.asian_futures_pricing import curran_arithmetic_futures_option
from experiments.wti_curran_benchmark import _discover_runs, _state


DEFAULT_IV_PATH = Path(
    "results/analysis/wti_apo_implied_volatility/apo_contract_implied_volatility.csv"
)
DEFAULT_RUNS_ROOT = Path("results/wti_apo_empirical")
DEFAULT_OUTPUT_ROOT = Path("results/analysis/wti_forward_q_validation")


def _design(frame: pd.DataFrame) -> np.ndarray:
    x = frame["log_moneyness"].to_numpy(dtype=float)
    call = (
        frame["option_type"].astype(str).str.lower().eq("call").to_numpy(dtype=float)
    )
    return np.column_stack(
        [
            np.ones(len(frame)),
            x,
            x**2,
            call,
            call * x,
            call * x**2,
        ]
    )


def _fit_smile(
    train: pd.DataFrame,
    *,
    target_date: pd.Timestamp,
    ridge: float,
    half_life_days: float | None,
) -> np.ndarray:
    if len(train) < 6:
        raise ValueError("at least six observations are required to fit the smile")
    X = _design(train)
    y = train["apo_implied_sigma_q"].to_numpy(dtype=float)
    if half_life_days is None:
        w = np.ones(len(train))
    else:
        dates = pd.to_datetime(train["valuation_date"]).dt.normalize()
        age = (target_date - dates).dt.days.to_numpy(dtype=float)
        w = np.exp(-np.log(2.0) * np.maximum(age, 0.0) / float(half_life_days))
    root_w = np.sqrt(w)
    Xw = X * root_w[:, None]
    yw = y * root_w
    penalty = np.eye(X.shape[1]) * float(ridge)
    penalty[0, 0] = 0.0
    lhs = Xw.T @ Xw + penalty
    rhs = Xw.T @ yw
    try:
        beta = np.linalg.solve(lhs, rhs)
    except np.linalg.LinAlgError:
        beta = np.linalg.pinv(lhs) @ rhs
    return beta


def _predict(frame: pd.DataFrame, beta: np.ndarray) -> np.ndarray:
    return np.clip(_design(frame) @ beta, 1e-6, 3.0)


def _run_lookup(runs_root: Path, expiries: list[str]) -> dict[tuple[str, str], Path]:
    lookup: dict[tuple[str, str], Path] = {}
    for expiry in expiries:
        for run in _discover_runs(runs_root, expiry):
            manifest = json.loads((run / "manifest.json").read_text(encoding="utf-8"))
            lookup[(str(manifest["valuation_date"]), str(manifest["apo_expiry"]))] = run
    return lookup


def _price_targets(
    targets: pd.DataFrame,
    sigma_hat: np.ndarray,
    *,
    run_dir: Path,
) -> np.ndarray:
    manifest = json.loads((run_dir / "manifest.json").read_text(encoding="utf-8"))
    realized, forwards, times = _state(run_dir, manifest)
    discount = float(manifest["discounting"]["discount_factor"])
    prices = np.empty(len(targets), dtype=float)
    for i, (row, sigma) in enumerate(zip(targets.itertuples(index=False), sigma_hat)):
        prices[i] = curran_arithmetic_futures_option(
            realized_fixings=realized,
            forward_fixings=forwards,
            fixing_times=times,
            strike=float(row.strike),
            sigma=float(sigma),
            discount_factor=discount,
            option_type=str(row.option_type),
        )
    return prices


def _error_summary(frame: pd.DataFrame) -> pd.DataFrame:
    """Summarize errors pooled across expiries and separately by expiry."""
    rows: list[dict[str, Any]] = []
    scopes: list[tuple[str, str, pd.DataFrame]] = [("pooled", "all", frame)]
    for expiry, group in frame.groupby("apo_expiry", sort=True):
        scopes.append(("expiry", str(expiry), group.copy()))

    for scope, expiry_label, scoped in scopes:
        for method in sorted(scoped["method"].unique()):
            method_frame = scoped[scoped["method"] == method]
            samples: dict[str, pd.DataFrame] = {"all": method_frame}
            samples["positive_volume"] = method_frame[method_frame["positive_volume"]]
            for threshold in (1, 10, 100, 500):
                samples[f"open_interest_ge_{threshold}"] = method_frame[
                    method_frame["open_interest"].fillna(-np.inf) >= threshold
                ]
            for sample_name, sample in samples.items():
                if sample.empty:
                    continue
                for label, column in (
                    ("forward_q", "forward_error"),
                    ("baseline_pi", "baseline_pi_error"),
                ):
                    e = sample[column].to_numpy(dtype=float)
                    rows.append(
                        {
                            "scope": scope,
                            "apo_expiry": expiry_label,
                            "method": method,
                            "sample": sample_name,
                            "model": label,
                            "n": int(len(sample)),
                            "n_dates": int(sample["valuation_date"].nunique()),
                            "mean_error": float(np.mean(e)),
                            "mae": float(np.mean(np.abs(e))),
                            "rmse": float(np.sqrt(np.mean(e**2))),
                        }
                    )
    return pd.DataFrame(rows)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--iv-path", type=Path, default=DEFAULT_IV_PATH)
    parser.add_argument("--runs-root", type=Path, default=DEFAULT_RUNS_ROOT)
    parser.add_argument("--output-root", type=Path, default=DEFAULT_OUTPUT_ROOT)
    parser.add_argument("--expiries", nargs="+", default=["2026-09", "2026-10"])
    parser.add_argument("--ridge", type=float, default=1e-6)
    parser.add_argument("--half-life-days", type=float, default=5.0)
    parser.add_argument("--force", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    args.output_root.mkdir(parents=True, exist_ok=True)
    output = args.output_root / "forward_q_predictions.csv"
    if output.exists() and not args.force:
        print(f"Reusing completed output: {output}", flush=True)
        return
    if not args.iv_path.exists():
        raise FileNotFoundError(
            f"missing {args.iv_path}; run experiments.wti_apo_implied_volatility first"
        )

    iv = pd.read_csv(args.iv_path)
    iv = iv[
        iv["apo_expiry"].astype(str).isin(args.expiries)
        & iv["apo_implied_sigma_q"].notna()
    ].copy()
    iv["valuation_ts"] = pd.to_datetime(iv["valuation_date"]).dt.normalize()
    lookup = _run_lookup(args.runs_root, list(args.expiries))
    rows: list[dict[str, Any]] = []

    for expiry in args.expiries:
        eframe = iv[iv["apo_expiry"].astype(str) == expiry].copy()
        dates = sorted(eframe["valuation_ts"].unique())
        for target_ts_raw in dates:
            target_ts = pd.Timestamp(target_ts_raw).normalize()
            target = eframe[eframe["valuation_ts"] == target_ts].copy()
            earlier = eframe[eframe["valuation_ts"] < target_ts].copy()
            if earlier.empty:
                continue
            latest_prior = pd.Timestamp(earlier["valuation_ts"].max()).normalize()
            training_sets = {
                "previous_day_smile": (
                    earlier[earlier["valuation_ts"] == latest_prior].copy(),
                    None,
                ),
                "expanding_smile": (earlier.copy(), float(args.half_life_days)),
            }
            key = (target_ts.strftime("%Y-%m-%d"), expiry)
            run_dir = lookup.get(key)
            if run_dir is None:
                continue

            for method, (train, half_life) in training_sets.items():
                train = train[train["apo_implied_sigma_q"].notna()].copy()
                if len(train) < 6:
                    continue
                beta = _fit_smile(
                    train,
                    target_date=target_ts,
                    ridge=float(args.ridge),
                    half_life_days=half_life,
                )
                sigma_hat = _predict(target, beta)
                prices = _price_targets(target, sigma_hat, run_dir=run_dir)
                for i, row in enumerate(target.itertuples(index=False)):
                    market = float(row.market_settlement)
                    volume = float(row.volume) if pd.notna(row.volume) else np.nan
                    oi = float(row.open_interest) if pd.notna(row.open_interest) else np.nan
                    baseline = float(row.baseline_pi_price)
                    rows.append(
                        {
                            "method": method,
                            "valuation_date": target_ts.strftime("%Y-%m-%d"),
                            "apo_expiry": expiry,
                            "training_end_date": latest_prior.strftime("%Y-%m-%d"),
                            "n_training_rows": int(len(train)),
                            "contract_id": str(row.contract_id),
                            "option_type": str(row.option_type),
                            "strike": float(row.strike),
                            "log_moneyness": float(row.log_moneyness),
                            "market_settlement": market,
                            "open_interest": oi,
                            "volume": volume,
                            "positive_volume": bool(np.isfinite(volume) and volume > 0),
                            "predicted_sigma_q": float(sigma_hat[i]),
                            "observed_same_day_implied_sigma_q": float(row.apo_implied_sigma_q),
                            "sigma_prediction_error": float(sigma_hat[i] - row.apo_implied_sigma_q),
                            "forward_q_price": float(prices[i]),
                            "forward_error": float(prices[i] - market),
                            "baseline_pi_price": baseline,
                            "baseline_pi_error": float(baseline - market),
                        }
                    )

    result = pd.DataFrame(rows)
    if result.empty:
        raise RuntimeError("no forward Q predictions could be produced")
    result.to_csv(output, index=False)
    summary = _error_summary(result)
    summary.to_csv(args.output_root / "forward_q_error_summary.csv", index=False)

    report = {
        "expiries": list(args.expiries),
        "prediction_rows": int(len(result)),
        "target_dates": int(result["valuation_date"].nunique()),
        "methods": sorted(result["method"].unique().tolist()),
        "information_guardrail": "Every sigma_Q prediction uses only APO implied-volatility observations from dates strictly earlier than the target valuation date.",
        "same_day_iv_usage": "Observed same-day IV is retained only as an ex-post diagnostic target and is never used in fitting or pricing the target date.",
    }
    (args.output_root / "forward_q_report.json").write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(f"Completed strict forward-Q validation: {args.output_root}", flush=True)


if __name__ == "__main__":
    main()
