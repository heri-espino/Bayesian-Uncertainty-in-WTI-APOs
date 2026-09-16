"""Run and aggregate the canonical WTI APO experiment over valuation dates.

This module is orchestration only. It discovers dates for which both the APO
cross-section and the required committed Barchart CL curve are available,
invokes :mod:`experiments.wti_apo_empirical` once per date, and writes three
non-overlapping empirical sample views:

``all_dates``
    Every eligible valuation date and every contract in its main sample.
``positive_volume_dates``
    Every contract on dates where at least one main-sample contract reports
    positive daily volume.
``positive_volume_contracts``
    Only contract-date observations whose own reported daily volume is positive.

The single-date run folders remain canonical scientific outputs. Panel tables are
derived summaries and can be rebuilt from those folders with ``--aggregate-only``
without rerunning MCMC or Monte Carlo pricing.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd

from bayesian_asian_options.barchart_apo import (
    apply_main_sample_filters,
    build_apo_panel,
    discover_barchart_histories,
)
from bayesian_asian_options.barchart_cl import load_barchart_cl_strip
from experiments.wti_apo_empirical import (
    ROOT,
    _candidate_curve_contracts,
    _pilot_fixing_dates,
    main as run_single_date,
)


_METHODS = [
    ("Full Bayes", "fb"),
    ("Posterior mean", "pm"),
    ("Sigma posterior mode", "sigma_mode"),
    ("MLE", "mle"),
]


def _date_audit(
    *,
    option_data_dir: Path,
    cl_data_dir: Path,
    apo_expiry: str,
    min_open_interest: float,
    exclude_min_tick: bool,
) -> pd.DataFrame:
    """Return availability/liquidity diagnostics by candidate valuation date."""
    option_paths = discover_barchart_histories(option_data_dir)
    options = build_apo_panel(option_paths, deduplicate_contracts=True)
    options["trade_date"] = pd.to_datetime(options["trade_date"]).dt.normalize()
    options = options[options["expiry_month"] == apo_expiry].copy()

    first_fixing = _pilot_fixing_dates(apo_expiry).min()
    options = options[options["trade_date"] < first_fixing].copy()
    if options.empty:
        return pd.DataFrame(
            columns=[
                "valuation_date",
                "n_raw_options",
                "n_main_sample",
                "n_positive_volume",
                "total_volume",
                "curve_available",
                "eligible",
            ]
        )

    curve_contracts = _candidate_curve_contracts(apo_expiry)
    futures, _ = load_barchart_cl_strip(cl_data_dir, contracts=curve_contracts)
    futures["trade_date"] = pd.to_datetime(futures["trade_date"]).dt.normalize()
    curve_counts = futures.groupby("trade_date")["contract"].nunique()
    curve_dates = set(curve_counts[curve_counts >= len(curve_contracts)].index)

    rows: list[dict[str, object]] = []
    for date, group in options.groupby("trade_date", sort=True):
        filtered = apply_main_sample_filters(
            group,
            min_open_interest=min_open_interest,
            exclude_min_tick=exclude_min_tick,
        )
        if "volume" in filtered:
            volume = pd.to_numeric(filtered["volume"], errors="coerce")
        else:
            volume = pd.Series(0.0, index=filtered.index, dtype=float)
        n_positive_volume = int((volume.fillna(0.0) > 0.0).sum())
        total_volume = float(volume.fillna(0.0).sum())
        curve_available = pd.Timestamp(date) in curve_dates
        rows.append(
            {
                "valuation_date": pd.Timestamp(date).date().isoformat(),
                "n_raw_options": int(len(group)),
                "n_main_sample": int(len(filtered)),
                "n_positive_volume": n_positive_volume,
                "total_volume": total_volume,
                "curve_available": bool(curve_available),
                "eligible": bool(curve_available and len(filtered) > 0),
            }
        )
    return pd.DataFrame(rows)


def _selected_dates(
    audit: pd.DataFrame,
    *,
    requested: list[str] | None,
    start_date: str | None,
    end_date: str | None,
    require_positive_volume: bool,
) -> list[str]:
    """Select eligible valuation dates from an audit table."""
    if audit.empty:
        return []
    selected = audit[audit["eligible"]].copy()
    dates = pd.to_datetime(selected["valuation_date"])
    if start_date is not None:
        selected = selected[dates >= pd.Timestamp(start_date)]
        dates = pd.to_datetime(selected["valuation_date"])
    if end_date is not None:
        selected = selected[dates <= pd.Timestamp(end_date)]
    if require_positive_volume:
        selected = selected[selected["n_positive_volume"] > 0]
    if requested:
        requested_set = {pd.Timestamp(value).date().isoformat() for value in requested}
        selected = selected[selected["valuation_date"].isin(requested_set)]
    return selected["valuation_date"].astype(str).tolist()


def _enrich_pricing_frame(
    frame: pd.DataFrame,
    *,
    date: str,
    posterior: pd.DataFrame | None,
    manifest: dict[str, object],
) -> pd.DataFrame:
    """Attach run-level inference/discounting metadata to contract prices."""
    out = frame.copy()
    out.insert(0, "valuation_date_panel", date)
    out["positive_volume"] = pd.to_numeric(
        out["volume"], errors="coerce"
    ).fillna(0.0) > 0.0
    out["abs_fb_minus_pm"] = out["fb_minus_pm"].abs()

    if posterior is not None and not posterior.empty:
        row = posterior.iloc[0]
        for column in [
            "sigma_mle",
            "sigma_posterior_mean",
            "sigma_posterior_sd",
            "sigma_q025",
            "sigma_q50",
            "sigma_q975",
            "mu_rhat",
            "sigma_rhat",
        ]:
            if column in row:
                out[f"run_{column}"] = row[column]

    discounting = manifest.get("discounting", {})
    if isinstance(discounting, dict):
        out["time_to_payoff_years"] = discounting.get("time_to_payoff_years")
        out["discount_factor"] = discounting.get("discount_factor")
    out["n_usable_returns"] = manifest.get("n_usable_returns")
    return out


def _error_summary_by_date(pricing: pd.DataFrame) -> pd.DataFrame:
    """Recompute method errors by date for an arbitrary contract-level sample."""
    columns = ["valuation_date", "method", "n", "mean_error", "mae", "rmse"]
    if pricing.empty:
        return pd.DataFrame(columns=columns)

    rows: list[dict[str, object]] = []
    for date, group in pricing.groupby("valuation_date_panel", sort=True):
        for method, prefix in _METHODS:
            err = pd.to_numeric(group[f"{prefix}_error"], errors="coerce").dropna().to_numpy()
            if len(err) == 0:
                continue
            rows.append(
                {
                    "valuation_date": str(date),
                    "method": method,
                    "n": int(len(err)),
                    "mean_error": float(np.mean(err)),
                    "mae": float(np.mean(np.abs(err))),
                    "rmse": float(np.sqrt(np.mean(err**2))),
                }
            )
    return pd.DataFrame(rows, columns=columns)


def _overall_error_summary(pricing: pd.DataFrame) -> pd.DataFrame:
    """Return pooled contract-date errors for an arbitrary panel sample."""
    columns = ["method", "n_contract_dates", "mean_error", "mae", "rmse"]
    if pricing.empty:
        return pd.DataFrame(columns=columns)

    rows: list[dict[str, object]] = []
    for method, prefix in _METHODS:
        err = pd.to_numeric(pricing[f"{prefix}_error"], errors="coerce").dropna().to_numpy()
        if len(err) == 0:
            continue
        rows.append(
            {
                "method": method,
                "n_contract_dates": int(len(err)),
                "mean_error": float(np.mean(err)),
                "mae": float(np.mean(np.abs(err))),
                "rmse": float(np.sqrt(np.mean(err**2))),
            }
        )
    return pd.DataFrame(rows, columns=columns)


def _sample_frames(
    pricing: pd.DataFrame,
    posterior: pd.DataFrame,
    audit: pd.DataFrame,
) -> dict[str, tuple[pd.DataFrame, pd.DataFrame, str]]:
    """Split an eligible-date panel into the three documented sample views."""
    if pricing.empty:
        return {
            "all_dates": (pricing.copy(), posterior.copy(), "all eligible dates and main-sample contracts"),
            "positive_volume_dates": (
                pricing.copy(),
                posterior.iloc[0:0].copy(),
                "all contracts on dates with at least one positive-volume main-sample contract",
            ),
            "positive_volume_contracts": (
                pricing.copy(),
                posterior.iloc[0:0].copy(),
                "only contract-date observations with reported daily volume > 0",
            ),
        }

    date_col = pricing["valuation_date_panel"].astype(str)
    eligible_audit = audit[audit["eligible"]].copy()
    positive_dates = set(
        eligible_audit.loc[
            eligible_audit["n_positive_volume"] > 0, "valuation_date"
        ].astype(str)
    )
    observed_dates = set(date_col)
    positive_dates &= observed_dates

    positive_date_pricing = pricing[date_col.isin(positive_dates)].copy()
    positive_contract_pricing = pricing[pricing["positive_volume"].fillna(False)].copy()

    posterior_dates = posterior["valuation_date"].astype(str) if not posterior.empty else pd.Series(dtype=str)
    positive_date_posterior = posterior[posterior_dates.isin(positive_dates)].copy()
    positive_contract_dates = set(positive_contract_pricing["valuation_date_panel"].astype(str))
    positive_contract_posterior = posterior[
        posterior_dates.isin(positive_contract_dates)
    ].copy()

    return {
        "all_dates": (
            pricing.copy(),
            posterior.copy(),
            "all eligible dates and main-sample contracts",
        ),
        "positive_volume_dates": (
            positive_date_pricing,
            positive_date_posterior,
            "all contracts on dates with at least one positive-volume main-sample contract",
        ),
        "positive_volume_contracts": (
            positive_contract_pricing,
            positive_contract_posterior,
            "only contract-date observations with reported daily volume > 0",
        ),
    }


def _write_sample(
    *,
    panel_dir: Path,
    sample_name: str,
    pricing: pd.DataFrame,
    posterior: pd.DataFrame,
    description: str,
    apo_expiry: str,
) -> None:
    """Write one namespaced derived panel sample without touching other samples."""
    sample_dir = panel_dir / sample_name
    sample_dir.mkdir(parents=True, exist_ok=True)

    pricing.to_csv(sample_dir / "panel_contract_pricing.csv", index=False)
    _error_summary_by_date(pricing).to_csv(
        sample_dir / "panel_error_summary.csv", index=False
    )
    _overall_error_summary(pricing).to_csv(
        sample_dir / "panel_overall_error_summary.csv", index=False
    )
    posterior.to_csv(sample_dir / "panel_posterior_summary.csv", index=False)

    dates = sorted(set(pricing.get("valuation_date_panel", pd.Series(dtype=str)).astype(str)))
    manifest = {
        "sample_name": sample_name,
        "description": description,
        "apo_expiry": apo_expiry,
        "n_dates": len(dates),
        "first_valuation_date": dates[0] if dates else None,
        "last_valuation_date": dates[-1] if dates else None,
        "n_contract_dates": int(len(pricing)),
        "n_positive_volume_contract_dates": int(
            pricing.get("positive_volume", pd.Series(dtype=bool)).fillna(False).sum()
        ),
        "derived_from": "canonical single-date run folders",
        "note": "derived aggregation only; single-date manifests remain the provenance authority",
    }
    (sample_dir / "sample_manifest.json").write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )


def _collect_panel_outputs(
    output_dir: Path,
    apo_expiry: str,
    dates: list[str],
    audit: pd.DataFrame,
    *,
    positive_dates_only: bool,
) -> None:
    """Aggregate canonical runs and write collision-free empirical sample views."""
    pricing_frames: list[pd.DataFrame] = []
    posterior_frames: list[pd.DataFrame] = []
    expiry_code = apo_expiry.replace("-", "")

    for date in dates:
        run_dir = output_dir / f"{date}_{expiry_code}"
        pricing_path = run_dir / "contract_pricing.csv"
        posterior_path = run_dir / "posterior_summary.csv"
        manifest_path = run_dir / "manifest.json"

        if not pricing_path.exists():
            raise FileNotFoundError(
                f"Missing canonical output for {date}: {pricing_path}. "
                "Run without --aggregate-only first or remove the date from the request."
            )

        posterior: pd.DataFrame | None = None
        if posterior_path.exists():
            posterior = pd.read_csv(posterior_path)
            posterior.insert(0, "valuation_date", date)
            posterior_frames.append(posterior.copy())

        manifest: dict[str, object] = {}
        if manifest_path.exists():
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))

        frame = pd.read_csv(pricing_path)
        pricing_frames.append(
            _enrich_pricing_frame(
                frame,
                date=date,
                posterior=posterior,
                manifest=manifest,
            )
        )

    pricing = pd.concat(pricing_frames, ignore_index=True) if pricing_frames else pd.DataFrame()
    posterior = (
        pd.concat(posterior_frames, ignore_index=True) if posterior_frames else pd.DataFrame()
    )

    panel_dir = output_dir / f"panel_{expiry_code}"
    panel_dir.mkdir(parents=True, exist_ok=True)
    samples = _sample_frames(pricing, posterior, audit)

    if positive_dates_only:
        names = ["positive_volume_dates", "positive_volume_contracts"]
    else:
        names = ["all_dates", "positive_volume_dates", "positive_volume_contracts"]

    for name in names:
        sample_pricing, sample_posterior, description = samples[name]
        _write_sample(
            panel_dir=panel_dir,
            sample_name=name,
            pricing=sample_pricing,
            posterior=sample_posterior,
            description=description,
            apo_expiry=apo_expiry,
        )


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--apo-expiry", default="2026-10")
    parser.add_argument("--history-start", default="2024-01-01")
    parser.add_argument("--dates", nargs="*", default=None)
    parser.add_argument("--start-date", default=None)
    parser.add_argument("--end-date", default=None)
    parser.add_argument(
        "--require-positive-volume",
        action="store_true",
        help=(
            "Run/read only dates with at least one positive-volume contract. Outputs are "
            "namespaced under positive_volume_dates/ and positive_volume_contracts/."
        ),
    )
    parser.add_argument(
        "--aggregate-only",
        action="store_true",
        help="Rebuild namespaced panel summaries from existing single-date run folders.",
    )
    parser.add_argument("--list-dates", action="store_true")
    parser.add_argument("--quick", action="store_true")
    parser.add_argument("--option-data-dir", type=Path, default=ROOT / "data" / "csv")
    parser.add_argument("--cl-data-dir", type=Path, default=ROOT / "data" / "csv" / "CL")
    parser.add_argument(
        "--cl-expiry-file",
        type=Path,
        default=ROOT / "data" / "csv" / "CL" / "contract_expiries.csv",
    )
    parser.add_argument(
        "--inference-cache-dir", type=Path, default=ROOT / "data" / "wti_yahoo"
    )
    parser.add_argument(
        "--treasury-dir", type=Path, default=ROOT / "data" / "rates" / "treasury"
    )
    parser.add_argument(
        "--output-dir", type=Path, default=ROOT / "results" / "wti_apo_empirical"
    )
    parser.add_argument("--min-open-interest", type=float, default=1.0)
    parser.add_argument("--include-min-tick", action="store_true")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> None:
    args = parse_args(argv)
    audit = _date_audit(
        option_data_dir=args.option_data_dir,
        cl_data_dir=args.cl_data_dir,
        apo_expiry=args.apo_expiry,
        min_open_interest=args.min_open_interest,
        exclude_min_tick=not args.include_min_tick,
    )
    dates = _selected_dates(
        audit,
        requested=args.dates,
        start_date=args.start_date,
        end_date=args.end_date,
        require_positive_volume=args.require_positive_volume,
    )

    panel_dir = args.output_dir / f"panel_{args.apo_expiry.replace('-', '')}"
    panel_dir.mkdir(parents=True, exist_ok=True)
    audit.to_csv(panel_dir / "panel_date_audit.csv", index=False)

    print(audit.to_string(index=False))
    if args.list_dates:
        return
    if not dates:
        raise SystemExit("No eligible valuation dates match the requested panel filters")

    if not args.aggregate_only:
        for date in dates:
            child_args = [
                "--valuation-date",
                date,
                "--apo-expiry",
                args.apo_expiry,
                "--history-start",
                args.history_start,
                "--option-data-dir",
                str(args.option_data_dir),
                "--cl-data-dir",
                str(args.cl_data_dir),
                "--cl-expiry-file",
                str(args.cl_expiry_file),
                "--inference-cache-dir",
                str(args.inference_cache_dir),
                "--treasury-dir",
                str(args.treasury_dir),
                "--output-dir",
                str(args.output_dir),
                "--download-treasury",
                "--min-open-interest",
                str(args.min_open_interest),
            ]
            if args.include_min_tick:
                child_args.append("--include-min-tick")
            if args.quick:
                child_args.extend(
                    [
                        "--chains",
                        "2",
                        "--n-iter",
                        "4000",
                        "--burn-in",
                        "1000",
                        "--pricing-paths",
                        "20000",
                        "--sigma-grid-size",
                        "21",
                    ]
                )
            print(f"\n=== {date} / {args.apo_expiry} ===")
            run_single_date(child_args)

    _collect_panel_outputs(
        args.output_dir,
        args.apo_expiry,
        dates,
        audit,
        positive_dates_only=args.require_positive_volume,
    )
    print(
        f"\nAggregated {len(dates)} valuation dates. Namespaced panel outputs: {panel_dir}"
    )


if __name__ == "__main__":
    main()
