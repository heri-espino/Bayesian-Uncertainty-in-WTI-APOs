"""First real-market WTI Average Price Option pricing experiment.

The pilot prices one observed APO expiry/date cross-section using:
1. contract-specific Yahoo Finance CL futures histories and curve points;
2. a reconstructed first-nearby historical return series with roll returns removed;
3. Bayesian GBM volatility inference under P;
4. date-specific U.S. Treasury discounting;
5. the CME-style first-nearby arithmetic-average pricer under Q.

The default pilot is October-2026 APOs observed on 2026-09-04.  Raw Yahoo
downloads are cached locally and are intentionally gitignored.
"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
from pathlib import Path

import numpy as np
import pandas as pd

from bayesian_asian_options.barchart_apo import (
    apply_main_sample_filters,
    build_apo_panel,
    discover_barchart_histories,
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
)
from bayesian_asian_options.wti_yahoo_futures import (
    cl_contract_strip,
    compare_futures_reference,
    download_or_load_yahoo_cl_strip,
    expiry_table_from_yahoo_metadata,
    futures_curve_on_date,
    reconstruct_first_nearby_history,
)

DEFAULT_VALUATION_DATE = "2026-09-04"
DEFAULT_APO_EXPIRY = "2026-10"


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
    """Weekday fixing schedule used by the first October-2026 pilot.

    The selected pilot month has no full-day CME energy closure.  General
    production runs should replace this fallback with an explicit CME settlement
    calendar/fixing-date file; the manifest records the convention.
    """
    start, end = _month_bounds(expiry_month)
    return pd.bdate_range(start, end)


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

    rows: list[dict[str, float | str | int | bool]] = []
    expected_average = float(
        (realized_fixings.sum() + forward_fixings.sum())
        / (len(realized_fixings) + len(forward_fixings))
    )
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
                "volume": float(contract["volume"]) if pd.notna(contract["volume"]) else np.nan,
                "expected_average": expected_average,
                "log_moneyness": float(np.log(float(contract["strike"]) / expected_average)),
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


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--valuation-date", default=DEFAULT_VALUATION_DATE)
    parser.add_argument("--apo-expiry", default=DEFAULT_APO_EXPIRY)
    parser.add_argument("--history-start", default="2024-01-01")
    parser.add_argument("--option-data-dir", type=Path, default=Path("data/csv"))
    parser.add_argument(
        "--futures-cache-dir",
        type=Path,
        default=Path("data/wti_yahoo_contracts"),
    )
    parser.add_argument(
        "--treasury-dir",
        type=Path,
        default=Path("data/rates/treasury"),
    )
    parser.add_argument("--download-treasury", action="store_true")
    parser.add_argument("--refresh-futures", action="store_true")
    parser.add_argument("--futures-reference-csv", type=Path, default=None)
    parser.add_argument("--output-dir", type=Path, default=Path("results/wti_apo_empirical"))
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
    if valuation_date >= fixing_dates.min():
        raise SystemExit(
            "The first empirical driver currently targets pre-averaging valuation dates; "
            "partial-fixing panel support is the next extension."
        )

    option_cross_section = _load_option_cross_section(
        args.option_data_dir,
        valuation_date,
        args.apo_expiry,
        min_open_interest=args.min_open_interest,
        exclude_min_tick=not args.include_min_tick,
    )

    _, averaging_end = _month_bounds(args.apo_expiry)
    contracts = cl_contract_strip(args.history_start, averaging_end, lead_months=2)
    futures_panel, futures_metadata = download_or_load_yahoo_cl_strip(
        contracts,
        directory=args.futures_cache_dir,
        refresh=args.refresh_futures,
    )
    expiry_table = expiry_table_from_yahoo_metadata(futures_metadata)

    first_nearby = reconstruct_first_nearby_history(
        futures_panel,
        expiry_table,
        start=args.history_start,
        end=valuation_date,
    )
    inference_returns = first_nearby.loc[
        first_nearby["usable_inference_return"], "log_return"
    ].to_numpy(dtype=float)
    if len(inference_returns) < 100:
        raise RuntimeError(
            f"Only {len(inference_returns)} usable within-contract returns; "
            "the Yahoo strip is too incomplete for the requested inference window"
        )

    sigma_samples, chain_diagnostics, posterior = _run_mcmc(
        inference_returns,
        chains=args.chains,
        n_iter=args.n_iter,
        burn_in=args.burn_in,
        seed=args.seed,
    )

    future_mapping = assign_first_nearby_contract(fixing_dates, expiry_table)
    required_curve_contracts = future_mapping["contract"].drop_duplicates().tolist()
    valuation_curve = futures_curve_on_date(
        futures_panel,
        valuation_date,
        contracts=required_curve_contracts,
    )
    forward_curve = build_forward_fixing_curve(
        fixing_dates,
        expiry_table,
        valuation_curve,
    )
    forward_fixings = forward_curve["settlement"].to_numpy(dtype=float)
    fixing_times = (
        (pd.to_datetime(forward_curve["fixing_date"]) - valuation_date).dt.days.to_numpy(dtype=float)
        / 365.25
    )
    realized_fixings = np.array([], dtype=float)

    args.treasury_dir.mkdir(parents=True, exist_ok=True)
    rate_paths = sorted(args.treasury_dir.glob("*.csv"))
    if not rate_paths and args.download_treasury:
        destination = args.treasury_dir / f"treasury_par_yields_{valuation_date.year}.csv"
        download_treasury_par_yield_csv(valuation_date.year, destination)
        rate_paths = [destination]
    if not rate_paths:
        raise SystemExit(
            f"No Treasury CSVs found in {args.treasury_dir}. "
            "Place the downloaded daily Treasury par-yield files there or use --download-treasury."
        )
    treasury = load_treasury_par_yields(rate_paths)
    curve = treasury_curve_on_or_before(treasury, valuation_date)
    payoff_date = pd.Timestamp(fixing_dates.max()).normalize()
    time_to_expiry = (payoff_date - valuation_date).days / 365.25
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

    run_dir = args.output_dir / f"{valuation_date.date()}_{args.apo_expiry.replace('-', '')}"
    run_dir.mkdir(parents=True, exist_ok=True)
    first_nearby.to_csv(run_dir / "first_nearby_series.csv", index=False)
    first_nearby[
        ["trade_date", "contract", "roll_switch", "log_return", "usable_inference_return"]
    ].to_csv(run_dir / "first_nearby_return_audit.csv", index=False)
    chain_diagnostics.to_csv(run_dir / "mcmc_diagnostics.csv", index=False)
    pd.DataFrame([posterior]).to_csv(run_dir / "posterior_summary.csv", index=False)
    np.savez_compressed(run_dir / "posterior_draws.npz", sigma=sigma_samples)
    forward_curve.to_csv(run_dir / "apo_fixing_state.csv", index=False)
    pricing_grid.to_csv(run_dir / "pricing_grid.csv", index=False)
    pricing.to_csv(run_dir / "contract_pricing.csv", index=False)
    errors.to_csv(run_dir / "error_summary.csv", index=False)
    futures_metadata.to_csv(run_dir / "futures_download_manifest.csv", index=False)

    validation_file = None
    if args.futures_reference_csv is not None:
        reference = pd.read_csv(args.futures_reference_csv)
        validation = compare_futures_reference(futures_panel, reference)
        validation_file = run_dir / "futures_source_validation.csv"
        validation.to_csv(validation_file, index=False)

    manifest = {
        "generated_at_utc": generated_at.isoformat(),
        "valuation_date": valuation_date.date().isoformat(),
        "apo_expiry": args.apo_expiry,
        "market_option_source": "committed Barchart APO histories",
        "futures_source": "Yahoo Finance individual CL contracts via yfinance",
        "futures_close_interpretation": "daily Close used as settlement proxy",
        "first_nearby_return_rule": "exclude every return spanning a contract switch",
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
            "note": (
                "Default October-2026 pilot has no full-day CME energy closure; "
                "general production panel must use an explicit exchange settlement calendar."
            ),
            "n_fixings": int(len(fixing_dates)),
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
        "futures_reference_validation": None if validation_file is None else str(validation_file),
    }
    (run_dir / "manifest.json").write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    print(f"Run directory: {run_dir}")
    print(f"Usable within-contract returns: {len(inference_returns)}")
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
