"""Canonical real-market WTI Average Price Option pricing experiment.

The empirical driver intentionally separates the source used for historical
physical-measure inference from the contract-specific futures curve used for
risk-neutral valuation:

* Yahoo ``CL=F`` is a labelled continuous/front-month proxy for historical
  returns under :math:`P`;
* committed Barchart ``Daily Prices`` histories provide realized first-nearby
  fixings and the individual CL futures curve entering the remaining APO
  fixing schedule;
* U.S. Treasury daily par-yield data provide dated discounting under the
  documented pilot approximation.

The default pilot prices the October-2026 APO cross-section observed on
2026-09-04.  The same driver also supports valuation dates inside the averaging
month: end-of-day fixings through the valuation date are treated as realized,
while later fixings are priced from the contemporaneous futures curve. Output
manifests use repository-relative paths and record the code commit plus runtime
package versions without storing a hostname or user path.
"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import platform
import subprocess
import sys

import numpy as np
import pandas as pd
import scipy

from bayesian_asian_options.barchart_apo import (
    apply_main_sample_filters,
    build_apo_panel,
    discover_barchart_histories,
)
from bayesian_asian_options.barchart_cl import (
    barchart_cl_curve_on_date,
    compare_barchart_cl_reference,
    load_barchart_cl_strip,
    load_cl_expiry_table,
)
from bayesian_asian_options.bayesian_gbm import gbm_mle, random_walk_metropolis_gbm
from bayesian_asian_options.rates import (
    download_treasury_par_yield_csv,
    load_treasury_par_yields,
    treasury_curve_on_or_before,
)
from bayesian_asian_options.wti_apo_pricing import wti_apo_cross_section_mc
from bayesian_asian_options.wti_first_nearby import (
    assign_first_nearby_contract,
    build_forward_fixing_curve,
    build_realized_fixing_curve,
)
from bayesian_asian_options.wti_yahoo import (
    dataframe_sha256,
    download_yahoo_wti,
    normalize_yahoo_history,
    prepare_wti_model_sample,
)
from bayesian_asian_options.wti_yahoo_futures import cl_contract_symbol


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_VALUATION_DATE = "2026-09-04"
DEFAULT_APO_EXPIRY = "2026-10"


def _portable_path(path: str | Path) -> str:
    """Return a manifest-safe path without workstation-specific directories."""
    resolved = Path(path).expanduser().resolve()
    try:
        return resolved.relative_to(ROOT.resolve()).as_posix()
    except ValueError:
        return f"<external>/{resolved.name}"


def _git_output(*args: str) -> str | None:
    try:
        result = subprocess.run(
            ["git", *args],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        )
    except (OSError, subprocess.CalledProcessError):
        return None
    return result.stdout.strip()


def _runtime_metadata() -> dict[str, object]:
    """Return reproducibility metadata that excludes host/user identifiers."""
    commit = _git_output("rev-parse", "HEAD")
    status = _git_output("status", "--porcelain")
    return {
        "git_commit": commit,
        "git_dirty": None if status is None else bool(status),
        "python": platform.python_version(),
        "platform": platform.platform(),
        "numpy": np.__version__,
        "pandas": pd.__version__,
        "scipy": scipy.__version__,
    }


def _rhat(chains: np.ndarray) -> float:
    """Classical Gelman-Rubin R-hat for equal-length scalar chains."""
    x = np.asarray(chains, dtype=float)
    if x.ndim != 2 or x.shape[0] < 2 or x.shape[1] < 2:
        return float("nan")
    n = x.shape[1]
    within = float(np.mean(np.var(x, axis=1, ddof=1)))
    if within <= 0:
        return 1.0
    between = float(n * np.var(np.mean(x, axis=1), ddof=1))
    var_hat = ((n - 1) / n) * within + between / n
    return float(np.sqrt(var_hat / within))


def _sigma_mode(samples: np.ndarray) -> float:
    from scipy.stats import gaussian_kde

    lo, hi = np.quantile(samples, [0.001, 0.999])
    if hi <= lo:
        return float(np.mean(samples))
    grid = np.linspace(max(1e-8, 0.9 * lo), 1.1 * hi, 1024)
    density = gaussian_kde(samples)(grid)
    return float(grid[int(np.argmax(density))])


def _month_bounds(expiry_month: str) -> tuple[pd.Timestamp, pd.Timestamp]:
    period = pd.Period(expiry_month, freq="M")
    return period.start_time.normalize(), period.end_time.normalize()


def _pilot_fixing_dates(expiry_month: str) -> pd.DatetimeIndex:
    """Return the weekday fixing schedule used by the current empirical pilot."""
    start, end = _month_bounds(expiry_month)
    return pd.bdate_range(start, end)


def _split_fixing_dates(
    fixing_dates: pd.DatetimeIndex,
    valuation_date: str | pd.Timestamp,
) -> tuple[pd.DatetimeIndex, pd.DatetimeIndex]:
    """Split the APO calendar into realized and remaining end-of-day fixings.

    Barchart option marks and CL ``Latest`` observations are end-of-day fields.
    Accordingly, a fixing dated on the valuation date is treated as known for
    that same end-of-day valuation.  Dates strictly after the valuation date
    remain stochastic.
    """
    target = pd.Timestamp(valuation_date).normalize()
    dates = pd.DatetimeIndex(pd.to_datetime(fixing_dates)).normalize()
    return dates[dates <= target], dates[dates > target]


def _candidate_curve_contracts(apo_expiry: str) -> list[str]:
    """Return the two CL delivery months used during one APO averaging month."""
    period = pd.Period(apo_expiry, freq="M")
    return [
        cl_contract_symbol((period + offset).year, (period + offset).month)
        for offset in (1, 2)
    ]


def _load_option_cross_section(
    input_dir: Path,
    valuation_date: pd.Timestamp,
    expiry_month: str,
    *,
    min_open_interest: float,
    exclude_min_tick: bool,
) -> pd.DataFrame:
    paths = discover_barchart_histories(input_dir)
    panel = build_apo_panel(paths, deduplicate_contracts=True)
    panel["trade_date"] = pd.to_datetime(panel["trade_date"]).dt.normalize()
    panel = panel[
        (panel["trade_date"] == valuation_date)
        & (panel["expiry_month"] == expiry_month)
    ].copy()
    if panel.empty:
        raise ValueError(
            f"No Barchart APO observations for {expiry_month} on {valuation_date.date()}"
        )
    panel = apply_main_sample_filters(
        panel,
        min_open_interest=min_open_interest,
        exclude_min_tick=exclude_min_tick,
    )
    if panel.empty:
        raise ValueError("All option observations were removed by the main-sample filters")
    return panel.sort_values(["option_type", "strike"]).reset_index(drop=True)


def _load_or_download_continuous_inference(
    *,
    cache_dir: Path,
    history_start: str,
    valuation_date: pd.Timestamp,
    refresh: bool,
) -> tuple[pd.DataFrame, np.ndarray, dict[str, object]]:
    """Return a cached/downloaded Yahoo CL=F inference sample through valuation date."""
    cache_dir.mkdir(parents=True, exist_ok=True)
    csv_path = cache_dir / "CL_F_inference.csv"
    meta_path = cache_dir / "CL_F_inference.json"
    end_exclusive = valuation_date + pd.Timedelta(days=1)

    use_cache = csv_path.exists() and not refresh
    history: pd.DataFrame
    metadata: dict[str, object]
    if use_cache:
        history = normalize_yahoo_history(pd.read_csv(csv_path))
        min_date = pd.Timestamp(history["date"].min()).normalize()
        max_date = pd.Timestamp(history["date"].max()).normalize()
        if min_date > pd.Timestamp(history_start) or max_date < valuation_date:
            use_cache = False

    if not use_cache:
        history, raw_meta = download_yahoo_wti(
            ticker="CL=F",
            start=history_start,
            end=end_exclusive.date().isoformat(),
        )
        history.to_csv(csv_path, index=False, date_format="%Y-%m-%d")
        metadata = dict(raw_meta)
        metadata.update(
            {
                "role": "physical-measure volatility inference proxy",
                "interpretation": (
                    "Yahoo continuous/front-month proxy; historical roll rule "
                    "not treated as contractual first-nearby"
                ),
                "sha256": dataframe_sha256(history),
            }
        )
        meta_path.write_text(
            json.dumps(metadata, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
    else:
        metadata = (
            json.loads(meta_path.read_text(encoding="utf-8"))
            if meta_path.exists()
            else {
                "provider": "Yahoo Finance via yfinance",
                "ticker": "CL=F",
                "role": "physical-measure volatility inference proxy",
                "interpretation": (
                    "Yahoo continuous/front-month proxy; historical roll rule "
                    "not treated as contractual first-nearby"
                ),
                "sha256": dataframe_sha256(history),
            }
        )

    sample = prepare_wti_model_sample(
        history,
        start=history_start,
        end=end_exclusive.date().isoformat(),
    )
    if sample.n_returns < 100:
        raise RuntimeError(
            f"Only {sample.n_returns} usable CL=F returns are available for the requested inference window"
        )
    return sample.history, sample.log_returns, metadata


def _return_audit(history: pd.DataFrame) -> pd.DataFrame:
    out = history[["date", "close"]].copy()
    out["log_return"] = np.nan
    if len(out) > 1:
        values = out["close"].to_numpy(dtype=float)
        out.loc[out.index[1:], "log_return"] = np.diff(np.log(values))
    out["usable_inference_return"] = out["log_return"].notna()
    return out


def _run_mcmc(
    returns: np.ndarray,
    *,
    chains: int,
    n_iter: int,
    burn_in: int,
    seed: int,
) -> tuple[np.ndarray, pd.DataFrame, dict[str, float]]:
    if chains < 2:
        raise ValueError("At least two MCMC chains are required for the empirical pilot")
    dt = 1.0 / 252.0
    mu_mle, sigma_mle = gbm_mle(returns, dt)
    mu_chains: list[np.ndarray] = []
    sigma_chains: list[np.ndarray] = []
    diagnostics: list[dict[str, float | int]] = []
    for chain_id in range(chains):
        result = random_walk_metropolis_gbm(
            returns,
            dt,
            n_iter=n_iter,
            burn_in=burn_in,
            theta_init=(mu_mle, float(np.log(max(sigma_mle, 1e-8)))),
            seed=seed + 10_000 * chain_id,
        )
        mu_chains.append(result.mu)
        sigma_chains.append(result.sigma)
        diagnostics.append(
            {
                "chain": chain_id + 1,
                "acceptance_rate": result.acceptance_rate,
                "mu_mean": float(np.mean(result.mu)),
                "sigma_mean": float(np.mean(result.sigma)),
            }
        )

    mu_matrix = np.vstack(mu_chains)
    sigma_matrix = np.vstack(sigma_chains)
    pooled_sigma = sigma_matrix.reshape(-1)
    summary = {
        "mu_mle": float(mu_mle),
        "sigma_mle": float(sigma_mle),
        "mu_rhat": _rhat(mu_matrix),
        "sigma_rhat": _rhat(sigma_matrix),
        "sigma_posterior_mean": float(np.mean(pooled_sigma)),
        "sigma_posterior_sd": float(np.std(pooled_sigma, ddof=1)),
        "sigma_posterior_mode": _sigma_mode(pooled_sigma),
        "sigma_q025": float(np.quantile(pooled_sigma, 0.025)),
        "sigma_q50": float(np.quantile(pooled_sigma, 0.50)),
        "sigma_q975": float(np.quantile(pooled_sigma, 0.975)),
    }
    return pooled_sigma, pd.DataFrame(diagnostics), summary


def _price_cross_section(
    contracts: pd.DataFrame,
    sigma_samples: np.ndarray,
    *,
    sigma_mle: float,
    realized_fixings: np.ndarray,
    forward_fixings: np.ndarray,
    fixing_times: np.ndarray,
    time_to_expiry: float,
    discount_factor: float,
    pricing_paths: int,
    sigma_grid_size: int,
    seed: int,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    lo = max(1e-6, 0.9 * float(np.quantile(sigma_samples, 0.001)))
    hi = 1.1 * float(max(np.quantile(sigma_samples, 0.999), sigma_mle))
    grid = np.linspace(lo, hi, sigma_grid_size)
    sigma_mean = float(np.mean(sigma_samples))
    sigma_mode = _sigma_mode(sigma_samples)

    strikes = contracts["strike"].to_numpy(dtype=float)
    kinds = contracts["option_type"].astype(str).tolist()
    grid_matrix = np.empty((len(grid), len(contracts)))
    grid_rows: list[dict[str, float | int | str]] = []

    for j, sigma in enumerate(grid):
        estimate = wti_apo_cross_section_mc(
            realized_fixings=realized_fixings,
            forward_fixings=forward_fixings,
            fixing_times=fixing_times,
            strikes=strikes,
            option_types=kinds,
            sigma=float(sigma),
            rate=None,
            time_to_expiry=time_to_expiry,
            discount_factor=discount_factor,
            n_paths=pricing_paths,
            seed=seed,
            antithetic=True,
        )
        grid_matrix[j] = estimate.prices
        for i, contract in contracts.iterrows():
            grid_rows.append(
                {
                    "contract_id": contract["contract_id"],
                    "sigma": float(sigma),
                    "model_price": float(estimate.prices[i]),
                    "pricing_se": float(estimate.standard_errors[i]),
                    "n_paths": pricing_paths,
                }
            )

    n_realized = int(len(realized_fixings))
    n_remaining = int(len(forward_fixings))
    n_fixings = n_realized + n_remaining
    if n_fixings == 0:
        raise ValueError("The APO fixing schedule is empty")
    fraction_fixed = n_realized / n_fixings
    expected_average = float(
        (realized_fixings.sum() + forward_fixings.sum()) / n_fixings
    )

    rows: list[dict[str, float | str | int | bool]] = []
    for i, contract in contracts.iterrows():
        price_grid = grid_matrix[:, i]
        posterior_prices = np.interp(sigma_samples, grid, price_grid)
        fb = float(np.mean(posterior_prices))
        pm = float(np.interp(sigma_mean, grid, price_grid))
        mode_price = float(np.interp(sigma_mode, grid, price_grid))
        mle = float(np.interp(sigma_mle, grid, price_grid))
        q025, q50, q975 = np.quantile(posterior_prices, [0.025, 0.5, 0.975])
        market = float(contract["market_price"])
        rows.append(
            {
                "contract_id": str(contract["contract_id"]),
                "trade_date": pd.Timestamp(contract["trade_date"]).date().isoformat(),
                "expiry_month": str(contract["expiry_month"]),
                "option_type": str(contract["option_type"]),
                "strike": float(contract["strike"]),
                "market_price": market,
                "open_interest": float(contract["open_interest"]),
                "volume": float(contract["volume"])
                if pd.notna(contract["volume"])
                else np.nan,
                "n_realized_fixings": n_realized,
                "n_remaining_fixings": n_remaining,
                "fraction_fixed": fraction_fixed,
                "expected_average": expected_average,
                "log_moneyness": float(
                    np.log(float(contract["strike"]) / expected_average)
                ),
                "full_bayes_price": fb,
                "postmean_plugin_price": pm,
                "sigma_mode_plugin_price": mode_price,
                "mle_plugin_price": mle,
                "posterior_price_q025": float(q025),
                "posterior_price_median": float(q50),
                "posterior_price_q975": float(q975),
                "fb_minus_pm": fb - pm,
                "fb_error": fb - market,
                "pm_error": pm - market,
                "sigma_mode_error": mode_price - market,
                "mle_error": mle - market,
                "fb_abs_error": abs(fb - market),
                "pm_abs_error": abs(pm - market),
                "sigma_mode_abs_error": abs(mode_price - market),
                "mle_abs_error": abs(mle - market),
            }
        )
    return pd.DataFrame(rows), pd.DataFrame(grid_rows)


def _error_summary(pricing: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for method, prefix in [
        ("Full Bayes", "fb"),
        ("Posterior mean", "pm"),
        ("Sigma posterior mode", "sigma_mode"),
        ("MLE", "mle"),
    ]:
        err = pricing[f"{prefix}_error"].to_numpy(dtype=float)
        rows.append(
            {
                "method": method,
                "n": len(err),
                "mean_error": float(np.mean(err)),
                "mae": float(np.mean(np.abs(err))),
                "rmse": float(np.sqrt(np.mean(err**2))),
            }
        )
    return pd.DataFrame(rows)


def _combine_fixing_state(
    realized_curve: pd.DataFrame,
    forward_curve: pd.DataFrame,
) -> pd.DataFrame:
    """Return one auditable table containing realized and remaining APO fixings."""
    frames: list[pd.DataFrame] = []
    if not realized_curve.empty:
        realized = realized_curve.copy()
        realized.insert(0, "fixing_status", "realized")
        frames.append(realized)
    if not forward_curve.empty:
        remaining = forward_curve.copy()
        remaining.insert(0, "fixing_status", "remaining")
        frames.append(remaining)
    if not frames:
        return pd.DataFrame(
            columns=[
                "fixing_status",
                "fixing_date",
                "contract",
                "contract_last_trade_date",
                "settlement",
            ]
        )
    return pd.concat(frames, ignore_index=True, sort=False).sort_values(
        "fixing_date"
    ).reset_index(drop=True)


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--valuation-date", default=DEFAULT_VALUATION_DATE)
    parser.add_argument("--apo-expiry", default=DEFAULT_APO_EXPIRY)
    parser.add_argument("--history-start", default="2024-01-01")
    parser.add_argument("--option-data-dir", type=Path, default=Path("data/csv"))
    parser.add_argument("--cl-data-dir", type=Path, default=Path("data/csv/CL"))
    parser.add_argument(
        "--cl-expiry-file",
        type=Path,
        default=Path("data/csv/CL/contract_expiries.csv"),
    )
    parser.add_argument(
        "--inference-cache-dir", type=Path, default=Path("data/wti_yahoo")
    )
    parser.add_argument(
        "--treasury-dir", type=Path, default=Path("data/rates/treasury")
    )
    parser.add_argument("--download-treasury", action="store_true")
    parser.add_argument(
        "--refresh-inference",
        "--refresh-futures",
        dest="refresh_inference",
        action="store_true",
        help=(
            "Refresh Yahoo CL=F inference data; --refresh-futures is retained as "
            "a backwards-compatible alias."
        ),
    )
    parser.add_argument("--futures-reference-csv", type=Path, default=None)
    parser.add_argument(
        "--output-dir", type=Path, default=Path("results/wti_apo_empirical")
    )
    parser.add_argument("--min-open-interest", type=float, default=1.0)
    parser.add_argument("--include-min-tick", action="store_true")
    parser.add_argument("--chains", type=int, default=4)
    parser.add_argument("--n-iter", type=int, default=20_000)
    parser.add_argument("--burn-in", type=int, default=4_000)
    parser.add_argument("--pricing-paths", type=int, default=100_000)
    parser.add_argument("--sigma-grid-size", type=int, default=41)
    parser.add_argument("--seed", type=int, default=20260904)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> None:
    args = parse_args(argv)
    generated_at = datetime.now(timezone.utc)
    valuation_date = pd.Timestamp(args.valuation_date).normalize()
    fixing_dates = _pilot_fixing_dates(args.apo_expiry)
    payoff_date = pd.Timestamp(fixing_dates.max()).normalize()
    if valuation_date > payoff_date:
        raise SystemExit(
            f"Valuation date {valuation_date.date()} is after the last pilot fixing "
            f"date {payoff_date.date()} for {args.apo_expiry}."
        )
    realized_dates, remaining_dates = _split_fixing_dates(
        fixing_dates,
        valuation_date,
    )

    option_cross_section = _load_option_cross_section(
        args.option_data_dir,
        valuation_date,
        args.apo_expiry,
        min_open_interest=args.min_open_interest,
        exclude_min_tick=not args.include_min_tick,
    )

    inference_history, inference_returns, inference_meta = (
        _load_or_download_continuous_inference(
            cache_dir=args.inference_cache_dir,
            history_start=args.history_start,
            valuation_date=valuation_date,
            refresh=args.refresh_inference,
        )
    )
    sigma_samples, chain_diagnostics, posterior = _run_mcmc(
        inference_returns,
        chains=args.chains,
        n_iter=args.n_iter,
        burn_in=args.burn_in,
        seed=args.seed,
    )

    curve_contracts = _candidate_curve_contracts(args.apo_expiry)
    futures_panel, curve_manifest = load_barchart_cl_strip(
        args.cl_data_dir,
        contracts=curve_contracts,
    )
    expiry_table = load_cl_expiry_table(
        args.cl_expiry_file,
        contracts=curve_contracts,
    )

    realized_curve = build_realized_fixing_curve(
        realized_dates,
        expiry_table,
        futures_panel,
    )
    realized_fixings = realized_curve["settlement"].to_numpy(dtype=float)

    if len(remaining_dates):
        future_mapping = assign_first_nearby_contract(remaining_dates, expiry_table)
        required_curve_contracts = (
            future_mapping["contract"].drop_duplicates().tolist()
        )
        valuation_curve = barchart_cl_curve_on_date(
            futures_panel,
            valuation_date,
            contracts=required_curve_contracts,
        )
        forward_curve = build_forward_fixing_curve(
            remaining_dates,
            expiry_table,
            valuation_curve,
        )
        forward_fixings = forward_curve["settlement"].to_numpy(dtype=float)
        fixing_times = (
            (pd.to_datetime(forward_curve["fixing_date"]) - valuation_date)
            .dt.days.to_numpy(dtype=float)
            / 365.25
        )
    else:
        required_curve_contracts = []
        valuation_curve = pd.DataFrame(
            columns=["contract", "settlement", "source_field", "price_interpretation"]
        )
        forward_curve = pd.DataFrame(
            columns=[
                "fixing_date",
                "contract",
                "contract_last_trade_date",
                "settlement",
            ]
        )
        forward_fixings = np.array([], dtype=float)
        fixing_times = np.array([], dtype=float)

    fixing_state = _combine_fixing_state(realized_curve, forward_curve)

    args.treasury_dir.mkdir(parents=True, exist_ok=True)
    rate_paths = sorted(args.treasury_dir.glob("*.csv"))
    if not rate_paths and args.download_treasury:
        destination = (
            args.treasury_dir / f"treasury_par_yields_{valuation_date.year}.csv"
        )
        download_treasury_par_yield_csv(valuation_date.year, destination)
        rate_paths = [destination]
    if not rate_paths:
        raise SystemExit(
            f"No Treasury CSVs found in {args.treasury_dir}; "
            "use --download-treasury or add the official files"
        )
    treasury = load_treasury_par_yields(rate_paths)
    curve = treasury_curve_on_or_before(treasury, valuation_date)
    time_to_expiry = max(0.0, (payoff_date - valuation_date).days / 365.25)
    discount_factor = curve.proxy_discount_factor(time_to_expiry)

    pricing, pricing_grid = _price_cross_section(
        option_cross_section,
        sigma_samples,
        sigma_mle=posterior["sigma_mle"],
        realized_fixings=realized_fixings,
        forward_fixings=forward_fixings,
        fixing_times=fixing_times,
        time_to_expiry=time_to_expiry,
        discount_factor=discount_factor,
        pricing_paths=args.pricing_paths,
        sigma_grid_size=args.sigma_grid_size,
        seed=args.seed + 5_000_000,
    )
    errors = _error_summary(pricing)

    run_dir = args.output_dir / (
        f"{valuation_date.date()}_{args.apo_expiry.replace('-', '')}"
    )
    run_dir.mkdir(parents=True, exist_ok=True)
    inference_history.to_csv(run_dir / "inference_proxy_series.csv", index=False)
    _return_audit(inference_history).to_csv(
        run_dir / "inference_return_audit.csv", index=False
    )
    chain_diagnostics.to_csv(run_dir / "mcmc_diagnostics.csv", index=False)
    pd.DataFrame([posterior]).to_csv(run_dir / "posterior_summary.csv", index=False)
    np.savez_compressed(run_dir / "posterior_draws.npz", sigma=sigma_samples)
    valuation_curve.to_csv(run_dir / "valuation_cl_curve.csv", index=False)
    expiry_table.to_csv(run_dir / "cl_expiry_table.csv", index=False)
    fixing_state.to_csv(run_dir / "apo_fixing_state.csv", index=False)
    pricing_grid.to_csv(run_dir / "pricing_grid.csv", index=False)
    pricing.to_csv(run_dir / "contract_pricing.csv", index=False)
    errors.to_csv(run_dir / "error_summary.csv", index=False)
    curve_manifest.to_csv(run_dir / "barchart_cl_manifest.csv", index=False)

    validation_file: Path | None = None
    if args.futures_reference_csv is not None:
        reference = pd.read_csv(args.futures_reference_csv)
        validation = compare_barchart_cl_reference(futures_panel, reference)
        validation_file = run_dir / "futures_source_validation.csv"
        validation.to_csv(validation_file, index=False)

    curve_snapshot = {
        str(row.contract): float(row.settlement)
        for row in valuation_curve[["contract", "settlement"]].itertuples(index=False)
    }
    n_fixings = int(len(fixing_dates))
    n_realized = int(len(realized_dates))
    n_remaining = int(len(remaining_dates))
    manifest = {
        "manifest_schema_version": 3,
        "generated_at_utc": generated_at.isoformat(),
        "runtime": _runtime_metadata(),
        "valuation_date": valuation_date.date().isoformat(),
        "apo_expiry": args.apo_expiry,
        "market_option_source": "committed Barchart APO histories",
        "physical_inference_source": (
            "Yahoo CL=F continuous/front-month proxy via yfinance"
        ),
        "physical_inference_sha256": inference_meta.get("sha256"),
        "physical_inference_limitation": (
            "Yahoo does not document the historical CL=F roll convention precisely enough "
            "to call this a contract-reconstructed first-nearby series"
        ),
        "curve_source": "committed Barchart CL Daily Prices histories",
        "curve_price_field": "Latest",
        "curve_price_interpretation": (
            "end-of-day settlement proxy; not asserted to be official CME settlement"
        ),
        "curve_contracts_loaded": curve_contracts,
        "curve_contracts_used": required_curve_contracts,
        "valuation_curve": curve_snapshot,
        "expiry_reference_file": _portable_path(args.cl_expiry_file),
        "history_start": args.history_start,
        "n_usable_returns": int(len(inference_returns)),
        "mcmc": {
            "chains": args.chains,
            "n_iter_per_chain": args.n_iter,
            "burn_in_per_chain": args.burn_in,
            "seed": args.seed,
            "mu_rhat": posterior["mu_rhat"],
            "sigma_rhat": posterior["sigma_rhat"],
            "mode_definition": "marginal KDE mode of sigma; not a joint MAP estimate",
        },
        "fixing_calendar": {
            "convention": "weekday pilot schedule",
            "valuation_timestamp_convention": (
                "end-of-day; fixing on valuation date is treated as realized"
            ),
            "n_fixings": n_fixings,
            "n_realized_fixings": n_realized,
            "n_remaining_fixings": n_remaining,
            "fraction_fixed": n_realized / n_fixings,
            "realized_fixing_source": (
                "exact mapped contract/date Barchart Daily Prices Latest"
            ),
            "missing_realized_policy": "fail; never forward-fill a missing fixing",
            "expiry_metadata_rule": "explicit versioned CL last-trade-date table",
        },
        "discounting": {
            "source": "U.S. Treasury Daily Treasury Par Yield Curve Rates",
            "curve_source_date": curve.source_date.date().isoformat(),
            "method": "interpolated par yield treated as continuous zero-rate proxy",
            "time_to_payoff_years": time_to_expiry,
            "discount_factor": discount_factor,
            "limitation": "not a bootstrapped zero/OIS curve",
        },
        "pricing": {
            "n_contracts": int(len(pricing)),
            "n_paths_per_sigma": args.pricing_paths,
            "sigma_grid_size": args.sigma_grid_size,
            "seed": args.seed + 5_000_000,
            "common_random_numbers": True,
            "antithetic": True,
        },
        "futures_reference_validation": (
            None if validation_file is None else _portable_path(validation_file)
        ),
    }
    (run_dir / "manifest.json").write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    print(f"Run directory: {run_dir}")
    print("Inference source: Yahoo CL=F continuous/front-month proxy")
    print(f"Usable inference returns: {len(inference_returns)}")
    print(f"Barchart CL histories loaded: {', '.join(curve_contracts)}")
    print(
        "Fixing state: "
        f"{n_realized} realized / {n_remaining} remaining "
        f"({n_realized / n_fixings:.1%} fixed)"
    )
    if required_curve_contracts:
        print("Valuation-date CL curve:")
        print(valuation_curve[["contract", "settlement"]].to_string(index=False))
    else:
        print("Valuation-date CL curve: no remaining stochastic fixings")
    print(
        "sigma posterior mean / 95% interval: "
        f"{posterior['sigma_posterior_mean']:.6f} "
        f"[{posterior['sigma_q025']:.6f}, {posterior['sigma_q975']:.6f}]"
    )
    print(f"sigma R-hat: {posterior['sigma_rhat']:.4f}")
    print(f"Treasury curve date: {curve.source_date.date()}")
    print(f"Discount factor: {discount_factor:.8f}")
    print(errors.to_string(index=False))


if __name__ == "__main__":
    main()
