"""Infer WTI APO-implied Q volatility and test it out of sample across contracts.

This experiment uses only data already present in completed empirical WTI APO runs:
Barchart APO settlements, the contemporaneous CL futures fixing curve, realized fixings,
and the stored discount factor.  It does *not* relabel historical volatility as risk-neutral
volatility and it does not require a vanilla CL option surface.

Three complementary objects are produced for every completed valuation date:

1. contract-level APO implied volatility, obtained by inverting the Curran approximation;
2. leave-one-contract-out (LOO) cross-sectional calibration of one scalar sigma_Q per target;
3. call-to-put and put-to-call transfer, where sigma_Q is calibrated on one option type and
   evaluated on the other.

The LOO and cross-type exercises avoid the trivial circularity of calibrating sigma to a
contract and then evaluating fit on that same contract.  The resulting sigma_Q is still an
APO-implied quantity, not an independent external market-volatility source.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Iterable

import numpy as np
import pandas as pd
from scipy.optimize import brentq, minimize_scalar

from bayesian_asian_options.asian_futures_pricing import curran_arithmetic_futures_option
from experiments.wti_curran_benchmark import _discover_runs, _state


DEFAULT_RUNS_ROOT = Path("results/wti_apo_empirical")
DEFAULT_OUTPUT_ROOT = Path("results/analysis/wti_apo_implied_volatility")


def _curran_price(
    row: Any,
    *,
    realized: np.ndarray,
    forwards: np.ndarray,
    times: np.ndarray,
    discount: float,
    sigma: float,
) -> float:
    return curran_arithmetic_futures_option(
        realized_fixings=realized,
        forward_fixings=forwards,
        fixing_times=times,
        strike=float(row.strike),
        sigma=float(sigma),
        discount_factor=float(discount),
        option_type=str(row.option_type),
    )


def implied_sigma_from_price(
    market_price: float,
    price_fn,
    *,
    sigma_min: float = 1e-6,
    sigma_max: float = 3.0,
    price_tolerance: float = 1e-8,
) -> tuple[float | None, str, float, float]:
    """Invert a non-decreasing option-pricing map on a bounded volatility interval.

    Returns ``(sigma, status, lower_price, upper_price)``.  A missing sigma is explicit:
    the observed settlement can lie outside the model-attainable range, or the price map can
    be effectively flat (for example after realized fixings guarantee a linear payoff).
    """
    market = float(market_price)
    if not np.isfinite(market) or market < 0:
        return None, "invalid_market_price", np.nan, np.nan
    if not (0 <= sigma_min < sigma_max):
        raise ValueError("require 0 <= sigma_min < sigma_max")

    lo_price = float(price_fn(float(sigma_min)))
    hi_price = float(price_fn(float(sigma_max)))
    if not np.isfinite(lo_price) or not np.isfinite(hi_price):
        return None, "nonfinite_model_price", lo_price, hi_price
    if hi_price < lo_price - price_tolerance:
        return None, "nonmonotone_price_map", lo_price, hi_price
    if abs(hi_price - lo_price) <= price_tolerance:
        if abs(market - lo_price) <= price_tolerance:
            return None, "flat_price_map_unidentified", lo_price, hi_price
        return None, "outside_flat_price_map", lo_price, hi_price
    if market < lo_price - price_tolerance:
        return None, "below_model_lower_bound", lo_price, hi_price
    if market > hi_price + price_tolerance:
        return None, "above_model_upper_bound", lo_price, hi_price
    if abs(market - lo_price) <= price_tolerance:
        return float(sigma_min), "lower_boundary", lo_price, hi_price
    if abs(market - hi_price) <= price_tolerance:
        return float(sigma_max), "upper_boundary", lo_price, hi_price

    def root(sigma: float) -> float:
        return float(price_fn(float(sigma))) - market

    try:
        sigma = float(brentq(root, sigma_min, sigma_max, xtol=1e-10, rtol=1e-10))
    except (ValueError, RuntimeError):
        return None, "root_failure", lo_price, hi_price
    return sigma, "interior", lo_price, hi_price


def calibrate_sigma_q(
    pricing: pd.DataFrame,
    *,
    realized: np.ndarray,
    forwards: np.ndarray,
    times: np.ndarray,
    discount: float,
    sigma_min: float,
    sigma_max: float,
) -> tuple[float, float]:
    """Fit one scalar Q volatility by unweighted cross-sectional settlement MSE."""
    if pricing.empty:
        raise ValueError("cannot calibrate sigma_Q on an empty contract set")
    rows = list(pricing.itertuples(index=False))

    def objective(sigma: float) -> float:
        errors = [
            _curran_price(
                row,
                realized=realized,
                forwards=forwards,
                times=times,
                discount=discount,
                sigma=float(sigma),
            )
            - float(row.market_price)
            for row in rows
        ]
        return float(np.mean(np.square(errors)))

    result = minimize_scalar(
        objective,
        bounds=(float(sigma_min), float(sigma_max)),
        method="bounded",
        options={"xatol": 1e-8, "maxiter": 500},
    )
    if not result.success or not np.isfinite(result.fun):
        raise RuntimeError(f"Q-volatility calibration failed: {result.message}")
    return float(result.x), float(result.fun)


def _posterior_sigma_mean(run_dir: Path) -> float:
    path = run_dir / "posterior_summary.csv"
    if not path.exists():
        raise FileNotFoundError(f"missing posterior summary: {path}")
    frame = pd.read_csv(path)
    if frame.empty or "sigma_posterior_mean" not in frame.columns:
        raise ValueError(f"invalid posterior summary: {path}")
    return float(frame.iloc[0]["sigma_posterior_mean"])


def _one_run(
    run_dir: Path,
    *,
    sigma_min: float,
    sigma_max: float,
    min_calibration_contracts: int,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, dict[str, Any]]:
    manifest = json.loads((run_dir / "manifest.json").read_text(encoding="utf-8"))
    valuation_date = str(manifest["valuation_date"])
    apo_expiry = str(manifest["apo_expiry"])
    discount = float(manifest["discounting"]["discount_factor"])
    realized, forwards, times = _state(run_dir, manifest)
    sigma_p = _posterior_sigma_mean(run_dir)

    pricing = pd.read_csv(run_dir / "contract_pricing.csv").copy()
    required = {
        "contract_id",
        "option_type",
        "strike",
        "market_price",
        "open_interest",
        "volume",
        "log_moneyness",
        "full_bayes_price",
        "postmean_plugin_price",
    }
    missing = required.difference(pricing.columns)
    if missing:
        raise ValueError(f"{run_dir}: contract pricing missing {sorted(missing)}")
    pricing = pricing.reset_index(drop=True)

    iv_rows: list[dict[str, Any]] = []
    for row in pricing.itertuples(index=False):
        def price_fn(sigma: float, row=row) -> float:
            return _curran_price(
                row,
                realized=realized,
                forwards=forwards,
                times=times,
                discount=discount,
                sigma=sigma,
            )

        iv, status, lower_price, upper_price = implied_sigma_from_price(
            float(row.market_price),
            price_fn,
            sigma_min=sigma_min,
            sigma_max=sigma_max,
        )
        volume = float(row.volume) if pd.notna(row.volume) else np.nan
        iv_rows.append(
            {
                "valuation_date": valuation_date,
                "apo_expiry": apo_expiry,
                "contract_id": str(row.contract_id),
                "option_type": str(row.option_type),
                "strike": float(row.strike),
                "market_settlement": float(row.market_price),
                "open_interest": float(row.open_interest) if pd.notna(row.open_interest) else np.nan,
                "volume": volume,
                "positive_volume": bool(np.isfinite(volume) and volume > 0),
                "log_moneyness": float(row.log_moneyness),
                "sigma_p_posterior_mean": sigma_p,
                "apo_implied_sigma_q": iv,
                "iv_status": status,
                "model_price_sigma_min": lower_price,
                "model_price_sigma_max": upper_price,
                "iv_minus_sigma_p": None if iv is None else float(iv - sigma_p),
                "baseline_pi_price": float(row.full_bayes_price),
                "baseline_pm_price": float(row.postmean_plugin_price),
                "baseline_pi_error": float(row.full_bayes_price) - float(row.market_price),
                "baseline_pm_error": float(row.postmean_plugin_price) - float(row.market_price),
            }
        )
    iv_frame = pd.DataFrame(iv_rows)

    full_sigma_q, full_mse = calibrate_sigma_q(
        pricing,
        realized=realized,
        forwards=forwards,
        times=times,
        discount=discount,
        sigma_min=sigma_min,
        sigma_max=sigma_max,
    )

    loo_rows: list[dict[str, Any]] = []
    if len(pricing) > min_calibration_contracts:
        for idx, target in pricing.iterrows():
            calibration = pricing.drop(index=idx)
            if len(calibration) < min_calibration_contracts:
                continue
            loo_sigma, calibration_mse = calibrate_sigma_q(
                calibration,
                realized=realized,
                forwards=forwards,
                times=times,
                discount=discount,
                sigma_min=sigma_min,
                sigma_max=sigma_max,
            )
            target_row = next(pd.DataFrame([target]).itertuples(index=False))
            predicted = _curran_price(
                target_row,
                realized=realized,
                forwards=forwards,
                times=times,
                discount=discount,
                sigma=loo_sigma,
            )
            market = float(target["market_price"])
            volume = float(target["volume"]) if pd.notna(target["volume"]) else np.nan
            loo_rows.append(
                {
                    "valuation_date": valuation_date,
                    "apo_expiry": apo_expiry,
                    "contract_id": str(target["contract_id"]),
                    "option_type": str(target["option_type"]),
                    "strike": float(target["strike"]),
                    "log_moneyness": float(target["log_moneyness"]),
                    "market_settlement": market,
                    "volume": volume,
                    "positive_volume": bool(np.isfinite(volume) and volume > 0),
                    "n_calibration_contracts": int(len(calibration)),
                    "loo_sigma_q": loo_sigma,
                    "sigma_p_posterior_mean": sigma_p,
                    "loo_sigma_q_minus_sigma_p": loo_sigma - sigma_p,
                    "calibration_mse": calibration_mse,
                    "loo_price": predicted,
                    "loo_error": predicted - market,
                    "loo_abs_error": abs(predicted - market),
                    "baseline_pi_price": float(target["full_bayes_price"]),
                    "baseline_pi_error": float(target["full_bayes_price"]) - market,
                    "baseline_pi_abs_error": abs(float(target["full_bayes_price"]) - market),
                }
            )
    loo_frame = pd.DataFrame(loo_rows)

    transfer_rows: list[dict[str, Any]] = []
    for calibration_type, target_type in (("call", "put"), ("put", "call")):
        calibration = pricing[pricing["option_type"].astype(str).str.lower() == calibration_type]
        targets = pricing[pricing["option_type"].astype(str).str.lower() == target_type]
        if len(calibration) < min_calibration_contracts or targets.empty:
            continue
        transfer_sigma, calibration_mse = calibrate_sigma_q(
            calibration,
            realized=realized,
            forwards=forwards,
            times=times,
            discount=discount,
            sigma_min=sigma_min,
            sigma_max=sigma_max,
        )
        for target in targets.itertuples(index=False):
            predicted = _curran_price(
                target,
                realized=realized,
                forwards=forwards,
                times=times,
                discount=discount,
                sigma=transfer_sigma,
            )
            market = float(target.market_price)
            volume = float(target.volume) if pd.notna(target.volume) else np.nan
            transfer_rows.append(
                {
                    "valuation_date": valuation_date,
                    "apo_expiry": apo_expiry,
                    "calibration_type": calibration_type,
                    "target_type": target_type,
                    "contract_id": str(target.contract_id),
                    "strike": float(target.strike),
                    "log_moneyness": float(target.log_moneyness),
                    "market_settlement": market,
                    "volume": volume,
                    "positive_volume": bool(np.isfinite(volume) and volume > 0),
                    "n_calibration_contracts": int(len(calibration)),
                    "transfer_sigma_q": transfer_sigma,
                    "sigma_p_posterior_mean": sigma_p,
                    "transfer_sigma_q_minus_sigma_p": transfer_sigma - sigma_p,
                    "calibration_mse": calibration_mse,
                    "transfer_price": predicted,
                    "transfer_error": predicted - market,
                    "transfer_abs_error": abs(predicted - market),
                    "baseline_pi_price": float(target.full_bayes_price),
                    "baseline_pi_error": float(target.full_bayes_price) - market,
                    "baseline_pi_abs_error": abs(float(target.full_bayes_price) - market),
                }
            )
    transfer_frame = pd.DataFrame(transfer_rows)

    solved = iv_frame[iv_frame["apo_implied_sigma_q"].notna()]
    date_summary = {
        "valuation_date": valuation_date,
        "apo_expiry": apo_expiry,
        "contracts": int(len(pricing)),
        "positive_volume_contracts": int(iv_frame["positive_volume"].sum()),
        "iv_solved": int(len(solved)),
        "iv_solved_fraction": float(len(solved) / len(pricing)) if len(pricing) else np.nan,
        "sigma_p_posterior_mean": sigma_p,
        "full_sample_sigma_q": full_sigma_q,
        "full_sample_sigma_q_minus_sigma_p": full_sigma_q - sigma_p,
        "full_sample_calibration_rmse": float(np.sqrt(full_mse)),
        "median_contract_iv": float(solved["apo_implied_sigma_q"].median()) if not solved.empty else np.nan,
        "mean_contract_iv": float(solved["apo_implied_sigma_q"].mean()) if not solved.empty else np.nan,
        "sd_contract_iv": float(solved["apo_implied_sigma_q"].std(ddof=1)) if len(solved) > 1 else np.nan,
    }
    return iv_frame, loo_frame, transfer_frame, date_summary


def _error_summary(
    frame: pd.DataFrame,
    *,
    predicted_error: str,
    baseline_error: str,
    label: str,
) -> pd.DataFrame:
    columns = ["experiment", "sample", "n", "model_mean_error", "model_mae", "model_rmse", "baseline_pi_mean_error", "baseline_pi_mae", "baseline_pi_rmse"]
    if frame.empty:
        return pd.DataFrame(columns=columns)
    rows: list[dict[str, Any]] = []
    samples = {"all": frame}
    if "positive_volume" in frame.columns:
        samples["positive_volume"] = frame[frame["positive_volume"]]
    for sample_name, sample in samples.items():
        if sample.empty:
            continue
        model = sample[predicted_error].to_numpy(dtype=float)
        baseline = sample[baseline_error].to_numpy(dtype=float)
        rows.append(
            {
                "experiment": label,
                "sample": sample_name,
                "n": int(len(sample)),
                "model_mean_error": float(np.mean(model)),
                "model_mae": float(np.mean(np.abs(model))),
                "model_rmse": float(np.sqrt(np.mean(model**2))),
                "baseline_pi_mean_error": float(np.mean(baseline)),
                "baseline_pi_mae": float(np.mean(np.abs(baseline))),
                "baseline_pi_rmse": float(np.sqrt(np.mean(baseline**2))),
            }
        )
    return pd.DataFrame(rows, columns=columns)


def run(
    runs_root: Path,
    *,
    expiries: Iterable[str],
    sigma_min: float,
    sigma_max: float,
    min_calibration_contracts: int,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame, dict[str, Any]]:
    if min_calibration_contracts < 2:
        raise ValueError("min_calibration_contracts must be at least 2")
    expiry_list = list(dict.fromkeys(str(x) for x in expiries))
    run_dirs: list[Path] = []
    for expiry in expiry_list:
        run_dirs.extend(_discover_runs(runs_root, expiry))
    run_dirs = sorted(set(run_dirs))
    if not run_dirs:
        raise FileNotFoundError("no completed empirical WTI APO runs found")

    iv_frames: list[pd.DataFrame] = []
    loo_frames: list[pd.DataFrame] = []
    transfer_frames: list[pd.DataFrame] = []
    date_rows: list[dict[str, Any]] = []
    for run_dir in run_dirs:
        iv, loo, transfer, date_summary = _one_run(
            run_dir,
            sigma_min=sigma_min,
            sigma_max=sigma_max,
            min_calibration_contracts=min_calibration_contracts,
        )
        iv_frames.append(iv)
        if not loo.empty:
            loo_frames.append(loo)
        if not transfer.empty:
            transfer_frames.append(transfer)
        date_rows.append(date_summary)

    iv_all = pd.concat(iv_frames, ignore_index=True) if iv_frames else pd.DataFrame()
    loo_all = pd.concat(loo_frames, ignore_index=True) if loo_frames else pd.DataFrame()
    transfer_all = pd.concat(transfer_frames, ignore_index=True) if transfer_frames else pd.DataFrame()
    by_date = pd.DataFrame(date_rows).sort_values(["apo_expiry", "valuation_date"]).reset_index(drop=True)

    summaries = [
        _error_summary(
            loo_all,
            predicted_error="loo_error",
            baseline_error="baseline_pi_error",
            label="leave_one_contract_out",
        ),
        _error_summary(
            transfer_all,
            predicted_error="transfer_error",
            baseline_error="baseline_pi_error",
            label="cross_option_type_transfer",
        ),
    ]
    error_summary = pd.concat(summaries, ignore_index=True)

    solved = iv_all[iv_all["apo_implied_sigma_q"].notna()]
    report = {
        "expiries": expiry_list,
        "completed_dates": int(len(by_date)),
        "contract_date_rows": int(len(iv_all)),
        "iv_solved_rows": int(len(solved)),
        "iv_solved_fraction": float(len(solved) / len(iv_all)) if len(iv_all) else None,
        "sigma_bounds": [float(sigma_min), float(sigma_max)],
        "min_calibration_contracts": int(min_calibration_contracts),
        "median_apo_implied_sigma_q": float(solved["apo_implied_sigma_q"].median()) if not solved.empty else None,
        "median_sigma_p_posterior_mean": float(by_date["sigma_p_posterior_mean"].median()) if not by_date.empty else None,
        "median_full_sample_sigma_q": float(by_date["full_sample_sigma_q"].median()) if not by_date.empty else None,
        "median_full_sample_sigma_q_minus_sigma_p": float(by_date["full_sample_sigma_q_minus_sigma_p"].median()) if not by_date.empty else None,
        "definition": (
            "APO-implied Q volatility under the paper's one-factor lognormal futures dynamics, "
            "using Curran (1994) conditioning and observed Barchart APO settlements"
        ),
        "out_of_sample_design": (
            "Leave-one-contract-out calibration excludes each target contract; cross-option-type "
            "transfer calibrates on calls and evaluates puts, and vice versa."
        ),
        "interpretation_guardrail": (
            "These are risk-neutral volatilities implied by the APO cross-section itself. They are "
            "not an independent external Q-volatility source and should not be presented as one."
        ),
    }
    return iv_all, loo_all, transfer_all, by_date, error_summary, report


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--runs-root", type=Path, default=DEFAULT_RUNS_ROOT)
    parser.add_argument("--output-root", type=Path, default=DEFAULT_OUTPUT_ROOT)
    parser.add_argument("--expiries", nargs="+", default=["2026-09", "2026-10"])
    parser.add_argument("--sigma-min", type=float, default=1e-6)
    parser.add_argument("--sigma-max", type=float, default=3.0)
    parser.add_argument("--min-calibration-contracts", type=int, default=3)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    iv, loo, transfer, by_date, errors, report = run(
        args.runs_root,
        expiries=args.expiries,
        sigma_min=args.sigma_min,
        sigma_max=args.sigma_max,
        min_calibration_contracts=args.min_calibration_contracts,
    )
    args.output_root.mkdir(parents=True, exist_ok=True)
    iv.to_csv(args.output_root / "apo_contract_implied_volatility.csv", index=False)
    loo.to_csv(args.output_root / "apo_loo_predictions.csv", index=False)
    transfer.to_csv(args.output_root / "apo_cross_type_predictions.csv", index=False)
    by_date.to_csv(args.output_root / "apo_implied_volatility_by_date.csv", index=False)
    errors.to_csv(args.output_root / "apo_implied_volatility_error_summary.csv", index=False)
    with (args.output_root / "apo_implied_volatility_report.json").open("w", encoding="utf-8") as fh:
        json.dump(report, fh, indent=2, sort_keys=True)
        fh.write("\n")
    print(json.dumps(report, indent=2, sort_keys=True))
    print(f"output_dir={args.output_root}")


if __name__ == "__main__":
    main()
