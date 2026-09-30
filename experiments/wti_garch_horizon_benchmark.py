"""Horizon-matched Gaussian GARCH(1,1) benchmark on strict APO holdouts.

This experiment strengthens the historical-volatility comparison by replacing a
backward-looking scalar volatility with a genuine conditional variance forecast.

For each target valuation date:
1. estimate Gaussian GARCH(1,1) parameters using only usable CL returns dated
   strictly before the target date;
2. assimilate the target-date CL return with the fitted parameters to update the
   end-of-day conditional variance state, without re-estimating parameters;
3. forecast daily variance over the remaining APO fixing horizon;
4. map that time-varying forecast to one constant annualized volatility by
   matching the variance of the unresolved arithmetic-average component under
   the maintained one-common-factor pricing representation;
5. price the exact same strict-forward APO holdouts with the existing Curran
   engine.

The parameter fit uses only NumPy/SciPy and adds no external GARCH dependency.
The default experiment is Gaussian GARCH(1,1); richer GARCH variants are
deliberately excluded to avoid specification mining.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
from scipy.optimize import brentq, minimize

from experiments.wti_forward_q_validation import _price_targets, _run_lookup


DEFAULT_FORWARD = Path(
    "results/analysis/wti_extended_forward/forward_q_validation/forward_q_predictions.csv"
)
DEFAULT_RUNS = Path("results/wti_apo_empirical")
DEFAULT_OUTPUT = Path("results/analysis/wti_garch_horizon_benchmark")
DEFAULT_EXPIRIES = (
    "2026-09",
    "2026-10",
    "2026-11",
    "2027-03",
    "2027-09",
    "2028-03",
    "2028-09",
)


@dataclass(frozen=True)
class GarchFit:
    """Gaussian GARCH(1,1) fit in decimal-return units."""

    mu: float
    omega: float
    alpha: float
    beta: float
    loglik: float
    n_obs: int
    last_variance: float
    last_residual: float
    optimizer_success: bool
    optimizer_message: str

    @property
    def persistence(self) -> float:
        return float(self.alpha + self.beta)

    @property
    def unconditional_variance(self) -> float:
        return float(self.omega / (1.0 - self.persistence))


def _softmax_garch_parameters(
    theta: np.ndarray,
) -> tuple[float, float, float, float]:
    """Map unconstrained parameters to mu, omega, alpha, beta."""
    mu = float(theta[0])
    omega = float(np.exp(theta[1]))
    logits = np.array([theta[2], theta[3], 0.0], dtype=float)
    logits -= np.max(logits)
    weights = np.exp(logits)
    weights /= weights.sum()
    alpha = float(weights[0])
    beta = float(weights[1])
    return mu, omega, alpha, beta


def _garch_filter(
    returns: np.ndarray,
    *,
    mu: float,
    omega: float,
    alpha: float,
    beta: float,
) -> tuple[np.ndarray, np.ndarray]:
    """Filter conditional variances for a return series."""
    x = np.asarray(returns, dtype=float)
    if x.ndim != 1 or x.size < 2:
        raise ValueError("at least two returns are required")
    if omega <= 0 or alpha < 0 or beta < 0 or alpha + beta >= 1:
        raise ValueError("invalid stationary GARCH parameters")

    residuals = x - float(mu)
    base = float(np.var(x, ddof=1))
    unconditional = float(omega / (1.0 - alpha - beta))
    h0 = max(base, unconditional, 1e-12)

    variances = np.empty_like(x)
    variances[0] = h0
    for i in range(1, x.size):
        variances[i] = (
            omega
            + alpha * residuals[i - 1] ** 2
            + beta * variances[i - 1]
        )
        if not np.isfinite(variances[i]) or variances[i] <= 0:
            raise FloatingPointError("non-positive GARCH variance")
    return variances, residuals


def fit_gaussian_garch11(returns: np.ndarray) -> GarchFit:
    """Fit stationary Gaussian GARCH(1,1) by maximum likelihood.

    Optimization is performed on returns expressed in percentage points for
    numerical stability. The returned parameters are converted back to decimal
    return units.
    """
    x = np.asarray(returns, dtype=float)
    x = x[np.isfinite(x)]
    if x.size < 63:
        raise ValueError(f"GARCH benchmark requires at least 63 returns; got {x.size}")

    scale = 100.0
    y = scale * x
    sample_var = max(float(np.var(y, ddof=1)), 1e-8)
    sample_mu = float(np.mean(y))

    def objective(theta: np.ndarray) -> float:
        mu, omega, alpha, beta = _softmax_garch_parameters(theta)
        try:
            variances, residuals = _garch_filter(
                y,
                mu=mu,
                omega=omega,
                alpha=alpha,
                beta=beta,
            )
        except (ValueError, FloatingPointError):
            return 1e100
        if np.any(~np.isfinite(variances)) or np.any(variances <= 0):
            return 1e100
        nll = 0.5 * np.sum(
            np.log(2.0 * np.pi)
            + np.log(variances)
            + residuals**2 / variances
        )
        return float(nll) if np.isfinite(nll) else 1e100

    starts: list[np.ndarray] = []
    for alpha0, beta0 in ((0.05, 0.90), (0.10, 0.80), (0.03, 0.95)):
        gamma0 = 1.0 - alpha0 - beta0
        omega0 = max(sample_var * gamma0, 1e-8)
        starts.append(
            np.array(
                [
                    sample_mu,
                    np.log(omega0),
                    np.log(alpha0 / gamma0),
                    np.log(beta0 / gamma0),
                ],
                dtype=float,
            )
        )

    bounds = [
        (-20.0, 20.0),
        (-30.0, 10.0),
        (-12.0, 12.0),
        (-12.0, 12.0),
    ]
    candidates = [
        minimize(
            objective,
            start,
            method="L-BFGS-B",
            bounds=bounds,
            options={"maxiter": 5000, "ftol": 1e-12, "gtol": 1e-8},
        )
        for start in starts
    ]
    finite = [result for result in candidates if np.isfinite(result.fun)]
    if not finite:
        raise RuntimeError("all GARCH optimizations failed")
    best = min(finite, key=lambda result: float(result.fun))

    mu_s, omega_s, alpha, beta = _softmax_garch_parameters(best.x)
    variances_s, residuals_s = _garch_filter(
        y,
        mu=mu_s,
        omega=omega_s,
        alpha=alpha,
        beta=beta,
    )

    return GarchFit(
        mu=mu_s / scale,
        omega=omega_s / scale**2,
        alpha=alpha,
        beta=beta,
        loglik=-float(best.fun),
        n_obs=int(x.size),
        last_variance=float(variances_s[-1] / scale**2),
        last_residual=float(residuals_s[-1] / scale),
        optimizer_success=bool(best.success),
        optimizer_message=str(best.message),
    )


def update_variance_with_return(
    fit: GarchFit,
    target_return: float,
) -> float:
    """Update the GARCH state through the target-date return.

    The fitted sample ends on the preceding date. First form the conditional
    variance for the target-date return, then assimilate that observed return to
    obtain the next-business-day variance.
    """
    h_target = (
        fit.omega
        + fit.alpha * fit.last_residual**2
        + fit.beta * fit.last_variance
    )
    residual_target = float(target_return) - fit.mu
    h_next = (
        fit.omega
        + fit.alpha * residual_target**2
        + fit.beta * h_target
    )
    if not np.isfinite(h_next) or h_next <= 0:
        raise FloatingPointError("invalid target-date GARCH update")
    return float(h_next)


def forecast_variances(
    fit: GarchFit,
    *,
    first_variance: float,
    horizon: int,
) -> np.ndarray:
    """Forecast expected daily variances from the next business day onward."""
    if horizon < 1:
        raise ValueError("forecast horizon must be positive")
    if first_variance <= 0:
        raise ValueError("first_variance must be positive")

    persistence = fit.persistence
    long_run = fit.unconditional_variance
    steps = np.arange(horizon, dtype=float)
    path = long_run + persistence**steps * (float(first_variance) - long_run)
    if np.any(~np.isfinite(path)) or np.any(path <= 0):
        raise FloatingPointError("invalid GARCH variance forecast")
    return path


def _return_information(
    run_dir: Path,
    valuation_date: pd.Timestamp,
) -> tuple[np.ndarray, float]:
    """Return strictly-prior estimation returns and the target-date return."""
    audit = pd.read_csv(run_dir / "inference_return_audit.csv")
    required = {"date", "log_return", "usable_inference_return"}
    missing = required.difference(audit.columns)
    if missing:
        raise ValueError(
            f"{run_dir} return audit missing columns: {sorted(missing)}"
        )

    audit["return_date"] = pd.to_datetime(audit["date"]).dt.normalize()
    usable = (
        audit["usable_inference_return"]
        .astype(str)
        .str.lower()
        .isin({"true", "1"})
    )
    audit["log_return_numeric"] = pd.to_numeric(
        audit["log_return"], errors="coerce"
    )
    frame = audit[usable & audit["log_return_numeric"].notna()].copy()
    if frame.empty:
        raise ValueError(f"{run_dir} has no usable returns")
    if (frame["return_date"] > valuation_date).any():
        raise RuntimeError("future return entered target-date GARCH information set")

    prior = frame[frame["return_date"] < valuation_date]
    target = frame[frame["return_date"] == valuation_date]
    if len(target) != 1:
        raise ValueError(
            f"expected exactly one target-date return for {valuation_date.date()}, "
            f"got {len(target)}"
        )
    return (
        prior["log_return_numeric"].to_numpy(dtype=float),
        float(target.iloc[0]["log_return_numeric"]),
    )


def _remaining_fixing_state(
    run_dir: Path,
    valuation_date: pd.Timestamp,
) -> pd.DataFrame:
    """Return unresolved fixing levels and calendar/business horizons."""
    state = pd.read_csv(run_dir / "apo_fixing_state.csv")
    required = {"fixing_date", "settlement"}
    missing = required.difference(state.columns)
    if missing:
        raise ValueError(f"{run_dir} fixing state missing columns: {sorted(missing)}")

    state["fixing_date"] = pd.to_datetime(state["fixing_date"]).dt.normalize()
    if "fixing_status" in state.columns:
        remaining = state[state["fixing_status"].astype(str).eq("remaining")].copy()
    else:
        remaining = state[state["fixing_date"] > valuation_date].copy()
    remaining = remaining[remaining["fixing_date"] > valuation_date].copy()
    if remaining.empty:
        raise ValueError(f"{run_dir} has no unresolved fixings")

    remaining["settlement"] = pd.to_numeric(
        remaining["settlement"], errors="raise"
    )
    remaining["time_years"] = (
        (remaining["fixing_date"] - valuation_date).dt.days.astype(float) / 365.25
    )
    start = np.datetime64(valuation_date.date(), "D")
    remaining["business_horizon"] = [
        int(
            np.busday_count(
                start,
                np.datetime64(date.date(), "D"),
            )
        )
        for date in remaining["fixing_date"]
    ]
    if (remaining["business_horizon"] < 1).any():
        raise ValueError("remaining fixing has non-positive business horizon")
    return remaining.sort_values("fixing_date").reset_index(drop=True)


def _average_variance_from_garch_path(
    fixing_state: pd.DataFrame,
    forecast_daily_variance: np.ndarray,
) -> float:
    """Unnormalized variance of unresolved average under time-varying variance."""
    levels = fixing_state["settlement"].to_numpy(dtype=float)
    horizons = fixing_state["business_horizon"].to_numpy(dtype=int)
    cumulative = np.cumsum(np.asarray(forecast_daily_variance, dtype=float))
    if horizons.max() > cumulative.size:
        raise ValueError("GARCH forecast path is shorter than fixing horizon")

    min_horizon = np.minimum.outer(horizons, horizons)
    integrated = cumulative[min_horizon - 1]
    covariance = np.outer(levels, levels) * np.expm1(integrated)
    return float(np.sum(covariance))


def _average_variance_constant_sigma(
    fixing_state: pd.DataFrame,
    sigma: float,
) -> float:
    """Unnormalized unresolved-average variance under constant annual sigma."""
    if sigma <= 0:
        raise ValueError("sigma must be positive")
    levels = fixing_state["settlement"].to_numpy(dtype=float)
    times = fixing_state["time_years"].to_numpy(dtype=float)
    integrated = float(sigma) ** 2 * np.minimum.outer(times, times)
    covariance = np.outer(levels, levels) * np.expm1(integrated)
    return float(np.sum(covariance))


def moment_matched_garch_sigma(
    fixing_state: pd.DataFrame,
    forecast_daily_variance: np.ndarray,
) -> float:
    """Match GARCH forecast average variance with one annualized constant sigma."""
    target = _average_variance_from_garch_path(
        fixing_state,
        forecast_daily_variance,
    )
    if not np.isfinite(target) or target <= 0:
        raise ValueError("target GARCH average variance must be positive")

    def objective(sigma: float) -> float:
        return _average_variance_constant_sigma(fixing_state, sigma) - target

    lower = 1e-8
    upper = 5.0
    if objective(upper) < 0:
        raise ValueError("effective GARCH volatility exceeds supported bracket")
    return float(
        brentq(
            objective,
            lower,
            upper,
            xtol=1e-12,
            rtol=1e-12,
            maxiter=200,
        )
    )


def _targets(
    forward_path: Path,
    expiries: tuple[str, ...],
) -> pd.DataFrame:
    """Build one exact target row with both APO smile comparator errors."""
    frame = pd.read_csv(forward_path)
    frame = frame[frame["apo_expiry"].astype(str).isin(expiries)].copy()

    keys = ["valuation_date", "apo_expiry", "contract_id"]
    previous = frame[frame["method"].astype(str).eq("previous_day_smile")].copy()
    expanding = frame[frame["method"].astype(str).eq("expanding_smile")][
        keys + ["forward_error"]
    ].rename(columns={"forward_error": "expanding_smile_error"})

    keep = keys + [
        "option_type",
        "strike",
        "log_moneyness",
        "market_settlement",
        "open_interest",
        "volume",
        "positive_volume",
        "baseline_pi_price",
        "baseline_pi_error",
        "forward_error",
    ]
    missing = set(keep).difference(previous.columns)
    if missing:
        raise ValueError(
            f"forward predictions missing columns: {sorted(missing)}"
        )
    previous = previous[keep].rename(
        columns={"forward_error": "previous_day_smile_error"}
    )
    target = previous.merge(
        expanding,
        on=keys,
        how="inner",
        validate="one_to_one",
    )
    target["valuation_date"] = pd.to_datetime(
        target["valuation_date"]
    ).dt.normalize()
    return target.sort_values(keys).reset_index(drop=True)


def summarize(predictions: pd.DataFrame) -> pd.DataFrame:
    """Summarize GARCH and comparator errors pooled and by expiry."""
    rows: list[dict[str, Any]] = []
    scopes: list[tuple[str, str, pd.DataFrame]] = [("pooled", "all", predictions)]
    for expiry, group in predictions.groupby("apo_expiry", sort=True):
        scopes.append(("expiry", str(expiry), group))

    methods = (
        ("garch_horizon_matched", "garch_error"),
        ("historical_pi", "baseline_pi_error"),
        ("previous_day_smile", "previous_day_smile_error"),
        ("expanding_smile", "expanding_smile_error"),
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
    forward_path: Path,
    runs_root: Path,
    output_dir: Path,
    *,
    expiries: tuple[str, ...],
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    targets = _targets(forward_path, expiries)
    lookup = _run_lookup(runs_root, list(expiries))

    # Fit once per valuation date because the physical return history is shared
    # across expiries. An arbitrary available expiry run supplies the audit.
    fit_by_date: dict[pd.Timestamp, tuple[GarchFit, float]] = {}
    for date in sorted(targets["valuation_date"].unique()):
        valuation_date = pd.Timestamp(date).normalize()
        candidate = targets[targets["valuation_date"].eq(valuation_date)].iloc[0]
        run_dir = lookup.get(
            (
                valuation_date.strftime("%Y-%m-%d"),
                str(candidate["apo_expiry"]),
            )
        )
        if run_dir is None:
            raise FileNotFoundError(
                f"missing empirical run for {valuation_date.date()}"
            )
        prior_returns, target_return = _return_information(
            run_dir,
            valuation_date,
        )
        fit = fit_gaussian_garch11(prior_returns)
        first_variance = update_variance_with_return(fit, target_return)
        fit_by_date[valuation_date] = (fit, first_variance)

    state_rows: list[dict[str, Any]] = []
    prediction_rows: list[dict[str, Any]] = []

    grouped = targets.groupby(
        ["valuation_date", "apo_expiry"],
        sort=True,
    )
    for (date_raw, expiry), target in grouped:
        valuation_date = pd.Timestamp(date_raw).normalize()
        key = (valuation_date.strftime("%Y-%m-%d"), str(expiry))
        run_dir = lookup.get(key)
        if run_dir is None:
            raise FileNotFoundError(f"missing empirical run for {key}")

        fit, first_variance = fit_by_date[valuation_date]
        fixing_state = _remaining_fixing_state(run_dir, valuation_date)
        max_horizon = int(fixing_state["business_horizon"].max())
        forecast = forecast_variances(
            fit,
            first_variance=first_variance,
            horizon=max_horizon,
        )
        sigma_eff = moment_matched_garch_sigma(fixing_state, forecast)
        prices = _price_targets(
            target,
            np.full(len(target), sigma_eff, dtype=float),
            run_dir=run_dir,
        )

        state_rows.append(
            {
                "valuation_date": valuation_date.strftime("%Y-%m-%d"),
                "apo_expiry": str(expiry),
                "n_estimation_returns": fit.n_obs,
                "mu": fit.mu,
                "omega": fit.omega,
                "alpha": fit.alpha,
                "beta": fit.beta,
                "persistence": fit.persistence,
                "unconditional_annual_sigma": float(
                    np.sqrt(fit.unconditional_variance * 252.0)
                ),
                "next_day_annual_sigma": float(
                    np.sqrt(first_variance * 252.0)
                ),
                "max_business_horizon": max_horizon,
                "n_remaining_fixings": int(len(fixing_state)),
                "garch_effective_sigma": sigma_eff,
                "loglik": fit.loglik,
                "optimizer_success": fit.optimizer_success,
                "optimizer_message": fit.optimizer_message,
            }
        )

        for row, price in zip(
            target.itertuples(index=False),
            prices,
            strict=True,
        ):
            market = float(row.market_settlement)
            prediction_rows.append(
                {
                    "valuation_date": valuation_date.strftime("%Y-%m-%d"),
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
                    "garch_effective_sigma": sigma_eff,
                    "garch_price": float(price),
                    "garch_error": float(price - market),
                    "baseline_pi_price": float(row.baseline_pi_price),
                    "baseline_pi_error": float(row.baseline_pi_error),
                    "previous_day_smile_error": float(
                        row.previous_day_smile_error
                    ),
                    "expanding_smile_error": float(
                        row.expanding_smile_error
                    ),
                }
            )

    predictions = pd.DataFrame(prediction_rows)
    states = pd.DataFrame(state_rows)
    summary = summarize(predictions)

    if len(predictions) != len(targets):
        raise RuntimeError("GARCH benchmark lost target rows")
    if predictions[["garch_price", "garch_error"]].isna().any().any():
        raise RuntimeError("GARCH benchmark produced missing prices")

    output_dir.mkdir(parents=True, exist_ok=True)
    predictions.to_csv(
        output_dir / "garch_horizon_predictions.csv",
        index=False,
    )
    states.to_csv(
        output_dir / "garch_horizon_states.csv",
        index=False,
    )
    summary.to_csv(
        output_dir / "garch_horizon_error_summary.csv",
        index=False,
    )
    report = {
        "model": "Gaussian GARCH(1,1)",
        "parameter_estimation_cutoff": (
            "strictly before target valuation date; target-date return is used "
            "only to update the conditional variance state after parameter fitting"
        ),
        "forecast_mapping": (
            "daily conditional variance forecast mapped to the unresolved APO "
            "fixing schedule and collapsed to one annualized sigma by matching "
            "the arithmetic-average variance under the maintained common-factor model"
        ),
        "n_contract_dates": int(len(predictions)),
        "n_target_dates": int(predictions["valuation_date"].nunique()),
        "n_expiries": int(predictions["apo_expiry"].nunique()),
        "all_optimizers_successful": bool(states["optimizer_success"].all()),
    }
    (output_dir / "garch_horizon_report.json").write_text(
        json.dumps(report, indent=2) + "\n",
        encoding="utf-8",
    )
    return predictions, states, summary


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
    _, states, summary = run(
        args.forward_path,
        args.runs_root,
        args.output_dir,
        expiries=tuple(args.expiries),
    )
    print(summary.to_string(index=False))
    print()
    print(
        states[
            [
                "valuation_date",
                "apo_expiry",
                "alpha",
                "beta",
                "persistence",
                "unconditional_annual_sigma",
                "next_day_annual_sigma",
                "garch_effective_sigma",
                "optimizer_success",
            ]
        ].to_string(index=False)
    )
    print(f"output_dir={args.output_dir}")


if __name__ == "__main__":
    main()
