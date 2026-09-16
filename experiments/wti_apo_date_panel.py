"""Run the canonical WTI APO experiment over multiple pre-averaging dates.

This module is orchestration only. It discovers dates for which both the APO
cross-section and the required committed Barchart CL curve are available, then
invokes :mod:`experiments.wti_apo_empirical` once per date. The resulting run
folders remain canonical; this driver only aggregates their summaries.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

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


def _collect_panel_outputs(output_dir: Path, apo_expiry: str, dates: list[str]) -> None:
    """Aggregate single-date outputs into analysis-ready panel tables."""
    pricing_frames: list[pd.DataFrame] = []
    error_frames: list[pd.DataFrame] = []
    posterior_frames: list[pd.DataFrame] = []
    expiry_code = apo_expiry.replace("-", "")

    for date in dates:
        run_dir = output_dir / f"{date}_{expiry_code}"
        pricing_path = run_dir / "contract_pricing.csv"
        error_path = run_dir / "error_summary.csv"
        posterior_path = run_dir / "posterior_summary.csv"
        manifest_path = run_dir / "manifest.json"

        posterior: pd.DataFrame | None = None
        if posterior_path.exists():
            posterior = pd.read_csv(posterior_path)
            posterior.insert(0, "valuation_date", date)
            posterior_frames.append(posterior.copy())

        manifest: dict[str, object] = {}
        if manifest_path.exists():
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))

        if pricing_path.exists():
            frame = pd.read_csv(pricing_path)
            frame.insert(0, "valuation_date_panel", date)
            frame["positive_volume"] = pd.to_numeric(
                frame["volume"], errors="coerce"
            ).fillna(0.0) > 0.0
            frame["abs_fb_minus_pm"] = frame["fb_minus_pm"].abs()
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
                        frame[f"run_{column}"] = row[column]
            discounting = manifest.get("discounting", {})
            if isinstance(discounting, dict):
                frame["time_to_payoff_years"] = discounting.get(
                    "time_to_payoff_years"
                )
                frame["discount_factor"] = discounting.get("discount_factor")
            frame["n_usable_returns"] = manifest.get("n_usable_returns")
            pricing_frames.append(frame)

        if error_path.exists():
            frame = pd.read_csv(error_path)
            frame.insert(0, "valuation_date", date)
            error_frames.append(frame)

    panel_dir = output_dir / f"panel_{expiry_code}"
    panel_dir.mkdir(parents=True, exist_ok=True)
    if pricing_frames:
        pd.concat(pricing_frames, ignore_index=True).to_csv(
            panel_dir / "panel_contract_pricing.csv", index=False
        )
    if error_frames:
        pd.concat(error_frames, ignore_index=True).to_csv(
            panel_dir / "panel_error_summary.csv", index=False
        )
    if posterior_frames:
        pd.concat(posterior_frames, ignore_index=True).to_csv(
            panel_dir / "panel_posterior_summary.csv", index=False
        )


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--apo-expiry", default="2026-10")
    parser.add_argument("--history-start", default="2024-01-01")
    parser.add_argument("--dates", nargs="*", default=None)
    parser.add_argument("--start-date", default=None)
    parser.add_argument("--end-date", default=None)
    parser.add_argument("--require-positive-volume", action="store_true")
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

    _collect_panel_outputs(args.output_dir, args.apo_expiry, dates)
    print(f"\nCompleted {len(dates)} valuation dates. Panel outputs: {panel_dir}")


if __name__ == "__main__":
    main()
