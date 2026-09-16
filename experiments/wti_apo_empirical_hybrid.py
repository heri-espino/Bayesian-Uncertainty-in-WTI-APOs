"""Hybrid Yahoo pilot for the first real WTI Average Price Option experiment.

Yahoo does not reliably retain quote pages for old individual CL contracts.  The
empirical pilot therefore separates the two data needs:

* physical-measure volatility inference uses Yahoo ``CL=F`` as an explicitly
  labelled continuous/front-month proxy;
* risk-neutral APO valuation uses only the live individual CL contracts needed
  for the averaging-month term structure (for example CLV26/CLX26/CLZ26 for
  the October-2026 pilot).

This keeps the contract-specific curve required by the APO payoff without
requiring dozens of delisted Yahoo symbols such as ``CLG24.NYM``.
"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
from pathlib import Path

import numpy as np
import pandas as pd

from experiments.wti_apo_empirical import (
    DEFAULT_APO_EXPIRY,
    DEFAULT_VALUATION_DATE,
    _error_summary,
    _load_option_cross_section,
    _month_bounds,
    _pilot_fixing_dates,
    _price_cross_section,
    _run_mcmc,
)
from bayesian_asian_options.rates import (
    download_treasury_par_yield_csv,
    load_treasury_par_yields,
    treasury_curve_on_or_before,
)
from bayesian_asian_options.wti_first_nearby import (
    assign_first_nearby_contract,
    build_forward_fixing_curve,
)
from bayesian_asian_options.wti_yahoo import (
    dataframe_sha256,
    download_yahoo_wti,
    normalize_yahoo_history,
    prepare_wti_model_sample,
)
from bayesian_asian_options.wti_yahoo_futures import (
    cl_contract_symbol,
    compare_futures_reference,
    download_or_load_yahoo_cl_strip,
    expiry_table_from_yahoo_metadata,
    futures_curve_on_date,
    parse_cl_contract,
)


def _candidate_curve_contracts(apo_expiry: str) -> list[str]:
    """Return the delivery-month strip needed around one APO averaging month."""
    period = pd.Period(apo_expiry, freq="M")
    candidates: list[str] = []
    for offset in range(3):
        delivery = period + offset
        candidates.append(cl_contract_symbol(delivery.year, delivery.month))
    return candidates


def _previous_weekday(date: pd.Timestamp) -> pd.Timestamp:
    out = pd.Timestamp(date).normalize()
    while out.weekday() >= 5:
        out -= pd.Timedelta(days=1)
    return out


def _subtract_weekdays(date: pd.Timestamp, n: int) -> pd.Timestamp:
    out = pd.Timestamp(date).normalize()
    remaining = int(n)
    while remaining:
        out -= pd.Timedelta(days=1)
        if out.weekday() < 5:
            remaining -= 1
    return out


def _cl_last_trade_rule_weekday(contract: str) -> pd.Timestamp:
    """Pilot fallback for the standard CL three-business-day termination rule.

    This fallback intentionally handles weekends only.  Yahoo contract metadata
    remains preferred.  Production-panel work must replace this with a validated
    CME settlement/holiday calendar before dates affected by exchange holidays
    are admitted.
    """
    decoded = parse_cl_contract(contract)
    delivery = pd.Period(f"{decoded.year:04d}-{decoded.month:02d}", freq="M")
    preceding = delivery - 1
    twenty_fifth = pd.Timestamp(year=preceding.year, month=preceding.month, day=25)
    reference = _previous_weekday(twenty_fifth)
    return _subtract_weekdays(reference, 3)


def _complete_expiry_metadata(metadata: pd.DataFrame) -> pd.DataFrame:
    """Fill missing active-contract expiry metadata with the named pilot rule."""
    out = metadata.copy()
    if "settlement_date" not in out:
        out["settlement_date"] = None
    if "settlement_date_source" not in out:
        out["settlement_date_source"] = None
    for idx, row in out.iterrows():
        observed = pd.to_datetime(row.get("settlement_date"), errors="coerce")
        if pd.isna(observed):
            fallback = _cl_last_trade_rule_weekday(str(row["contract"]))
            out.at[idx, "settlement_date"] = fallback.date().isoformat()
            out.at[idx, "settlement_date_source"] = "cme_standard_rule_weekday_pilot_fallback"
    return out


def _load_or_download_continuous_inference(
    *,
    cache_dir: Path,
    history_start: str,
    valuation_date: pd.Timestamp,
    refresh: bool,
) -> tuple[pd.DataFrame, np.ndarray, dict[str, object]]:
    """Return a cached/downloaded CL=F inference sample through valuation date."""
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
                "interpretation": "Yahoo continuous/front-month proxy; historical roll rule not treated as contractual first-nearby",
                "sha256": dataframe_sha256(history),
            }
        )
        meta_path.write_text(json.dumps(metadata, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    else:
        metadata = (
            json.loads(meta_path.read_text(encoding="utf-8"))
            if meta_path.exists()
            else {
                "provider": "Yahoo Finance via yfinance",
                "ticker": "CL=F",
                "role": "physical-measure volatility inference proxy",
                "interpretation": "Yahoo continuous/front-month proxy; historical roll rule not treated as contractual first-nearby",
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


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--valuation-date", default=DEFAULT_VALUATION_DATE)
    parser.add_argument("--apo-expiry", default=DEFAULT_APO_EXPIRY)
    parser.add_argument("--history-start", default="2024-01-01")
    parser.add_argument("--option-data-dir", type=Path, default=Path("data/csv"))
    parser.add_argument("--inference-cache-dir", type=Path, default=Path("data/wti_yahoo"))
    parser.add_argument("--futures-cache-dir", type=Path, default=Path("data/wti_yahoo_contracts"))
    parser.add_argument("--treasury-dir", type=Path, default=Path("data/rates/treasury"))
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
        raise SystemExit("The first pilot currently targets a pre-averaging valuation date")

    option_cross_section = _load_option_cross_section(
        args.option_data_dir,
        valuation_date,
        args.apo_expiry,
        min_open_interest=args.min_open_interest,
        exclude_min_tick=not args.include_min_tick,
    )

    inference_history, inference_returns, inference_meta = _load_or_download_continuous_inference(
        cache_dir=args.inference_cache_dir,
        history_start=args.history_start,
        valuation_date=valuation_date,
        refresh=args.refresh_futures,
    )
    sigma_samples, chain_diagnostics, posterior = _run_mcmc(
        inference_returns,
        chains=args.chains,
        n_iter=args.n_iter,
        burn_in=args.burn_in,
        seed=args.seed,
    )

    curve_contracts = _candidate_curve_contracts(args.apo_expiry)
    futures_panel, futures_metadata = download_or_load_yahoo_cl_strip(
        curve_contracts,
        directory=args.futures_cache_dir,
        refresh=args.refresh_futures,
    )
    futures_metadata = _complete_expiry_metadata(futures_metadata)
    expiry_table = expiry_table_from_yahoo_metadata(futures_metadata)

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
            f"No Treasury CSVs found in {args.treasury_dir}; use --download-treasury or add the official files"
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
    inference_history.to_csv(run_dir / "inference_proxy_series.csv", index=False)
    _return_audit(inference_history).to_csv(run_dir / "inference_return_audit.csv", index=False)
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
        "physical_inference_source": "Yahoo CL=F continuous/front-month proxy via yfinance",
        "physical_inference_sha256": inference_meta.get("sha256"),
        "physical_inference_limitation": (
            "Yahoo does not document the historical CL=F roll convention precisely enough to call this a contract-reconstructed first-nearby series"
        ),
        "curve_source": "Yahoo Finance individual CL contracts via yfinance",
        "curve_contracts_downloaded": curve_contracts,
        "curve_contracts_used": required_curve_contracts,
        "futures_close_interpretation": "Yahoo daily Close used as settlement proxy",
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
            "n_fixings": int(len(fixing_dates)),
            "expiry_metadata_rule": (
                "Yahoo contract expiry/settlement metadata when available; weekend-only implementation of the standard CL termination rule as a pilot fallback"
            ),
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
    print(f"Inference source: Yahoo CL=F continuous/front-month proxy")
    print(f"Usable inference returns: {len(inference_returns)}")
    print(f"Individual CL curve contracts: {', '.join(curve_contracts)}")
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
