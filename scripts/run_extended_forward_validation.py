"""Run the extended multi-expiry WTI APO forward-volatility validation suite.

The runner is checkpointable.  It audits every requested expiry, skips canonical single-date
runs that already contain the required scientific outputs, executes only missing dates, rebuilds
the panel aggregations, and then runs:

1. APO-implied effective Q volatility inversion;
2. strict previous-day and expanding prior-date smile validation;
3. valuation-date cluster bootstrap, pooled and by expiry.

The default production set includes every downloaded expiry that passes the six-contract smile
coverage audit.  June 2029 is intentionally excluded because the committed cross-section has at
most three usable contracts.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

from experiments.wti_apo_date_panel import _date_audit, _selected_dates
from experiments.wti_apo_empirical import ROOT


DEFAULT_EXPIRIES = [
    "2026-09",
    "2026-10",
    "2026-11",
    "2027-03",
    "2027-09",
    "2028-03",
    "2028-09",
]


def _run(args: list[str]) -> None:
    print("\n$", " ".join(args), flush=True)
    subprocess.run(args, cwd=ROOT, check=True)


def _run_complete(run_dir: Path) -> bool:
    required = [
        "manifest.json",
        "contract_pricing.csv",
        "posterior_summary.csv",
        "apo_fixing_state.csv",
    ]
    return run_dir.is_dir() and all((run_dir / name).is_file() for name in required)


def _eligible_dates(
    *,
    expiry: str,
    option_data_dir: Path,
    cl_data_dir: Path,
    cl_expiry_file: Path,
    min_open_interest: float,
    include_min_tick: bool,
) -> list[str]:
    audit = _date_audit(
        option_data_dir=option_data_dir,
        cl_data_dir=cl_data_dir,
        cl_expiry_file=cl_expiry_file,
        apo_expiry=expiry,
        min_open_interest=min_open_interest,
        exclude_min_tick=not include_min_tick,
    )
    return _selected_dates(
        audit,
        requested=None,
        start_date=None,
        end_date=None,
        require_positive_volume=False,
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--expiries", nargs="+", default=DEFAULT_EXPIRIES)
    parser.add_argument("--quick", action="store_true")
    parser.add_argument("--no-resume", action="store_true")
    parser.add_argument("--skip-panels", action="store_true")
    parser.add_argument(
        "--bootstrap-preset",
        choices=("research", "monster"),
        default="monster",
    )
    parser.add_argument("--min-open-interest", type=float, default=1.0)
    parser.add_argument("--include-min-tick", action="store_true")
    parser.add_argument(
        "--option-data-dir", type=Path, default=ROOT / "data" / "csv"
    )
    parser.add_argument(
        "--cl-data-dir", type=Path, default=ROOT / "data" / "csv" / "CL"
    )
    parser.add_argument(
        "--cl-expiry-file",
        type=Path,
        default=ROOT / "data" / "csv" / "CL" / "contract_expiries.csv",
    )
    parser.add_argument(
        "--treasury-dir", type=Path, default=ROOT / "data" / "rates" / "treasury"
    )
    parser.add_argument(
        "--inference-cache-dir", type=Path, default=ROOT / "data" / "wti_yahoo"
    )
    parser.add_argument(
        "--physical-inference-source",
        choices=("yahoo", "first-nearby"),
        default="yahoo",
    )
    parser.add_argument(
        "--first-nearby-history",
        type=Path,
        default=(
            ROOT
            / "results"
            / "analysis"
            / "wti_first_nearby"
            / "first_nearby_reconstruction_raw.csv"
        ),
    )
    parser.add_argument("--runs-root", type=Path, default=None)
    parser.add_argument("--analysis-root", type=Path, default=None)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    expiries = list(dict.fromkeys(str(x) for x in args.expiries))
    if "2029-06" in expiries:
        raise SystemExit(
            "2029-06 is excluded from the forward suite: the committed cross-section "
            "never reaches the six contracts required by the smile specification."
        )

    source_suffix = (
        "_first_nearby"
        if args.physical_inference_source == "first-nearby"
        else ""
    )
    if args.runs_root is None:
        if args.quick:
            runs_root = (
                ROOT
                / "results"
                / f"wti_apo_empirical_extended_quick{source_suffix}"
            )
        else:
            runs_root = (
                ROOT
                / "results"
                / f"wti_apo_empirical{source_suffix}"
            )
    else:
        runs_root = args.runs_root

    if args.analysis_root is None:
        if args.quick:
            analysis_root = (
                ROOT
                / "results"
                / "analysis"
                / f"wti_extended_forward_quick{source_suffix}"
            )
        else:
            analysis_root = (
                ROOT
                / "results"
                / "analysis"
                / f"wti_extended_forward{source_suffix}"
            )
    else:
        analysis_root = args.analysis_root

    runs_root.mkdir(parents=True, exist_ok=True)
    analysis_root.mkdir(parents=True, exist_ok=True)

    if not args.skip_panels:
        for expiry in expiries:
            dates = _eligible_dates(
                expiry=expiry,
                option_data_dir=args.option_data_dir,
                cl_data_dir=args.cl_data_dir,
                cl_expiry_file=args.cl_expiry_file,
                min_open_interest=float(args.min_open_interest),
                include_min_tick=bool(args.include_min_tick),
            )
            if not dates:
                raise RuntimeError(f"{expiry}: no eligible valuation dates")

            expiry_code = expiry.replace("-", "")
            if args.no_resume:
                missing = list(dates)
            else:
                missing = [
                    date
                    for date in dates
                    if not _run_complete(runs_root / f"{date}_{expiry_code}")
                ]

            print(
                f"\n{expiry}: eligible_dates={len(dates)}, "
                f"already_complete={len(dates) - len(missing)}, missing={len(missing)}",
                flush=True,
            )
            if missing:
                cmd = [
                    sys.executable,
                    "-m",
                    "experiments.wti_apo_date_panel",
                    "--apo-expiry",
                    expiry,
                    "--dates",
                    *missing,
                    "--option-data-dir",
                    str(args.option_data_dir),
                    "--cl-data-dir",
                    str(args.cl_data_dir),
                    "--cl-expiry-file",
                    str(args.cl_expiry_file),
                    "--inference-cache-dir",
                    str(args.inference_cache_dir),
                    "--physical-inference-source",
                    args.physical_inference_source,
                    "--first-nearby-history",
                    str(args.first_nearby_history),
                    "--treasury-dir",
                    str(args.treasury_dir),
                    "--output-dir",
                    str(runs_root),
                    "--min-open-interest",
                    str(args.min_open_interest),
                ]
                if args.include_min_tick:
                    cmd.append("--include-min-tick")
                if args.quick:
                    cmd.append("--quick")
                _run(cmd)

            # Rebuild the complete aggregation, including runs that pre-dated this suite.
            cmd = [
                sys.executable,
                "-m",
                "experiments.wti_apo_date_panel",
                "--apo-expiry",
                expiry,
                "--dates",
                *dates,
                "--aggregate-only",
                "--option-data-dir",
                str(args.option_data_dir),
                "--cl-data-dir",
                str(args.cl_data_dir),
                "--cl-expiry-file",
                str(args.cl_expiry_file),
                "--output-dir",
                str(runs_root),
                "--min-open-interest",
                str(args.min_open_interest),
            ]
            if args.include_min_tick:
                cmd.append("--include-min-tick")
            _run(cmd)

    iv_root = analysis_root / "apo_implied_volatility"
    forward_root = analysis_root / "forward_q_validation"
    bootstrap_root = analysis_root / "liquidity_bootstrap"

    _run(
        [
            sys.executable,
            "-m",
            "experiments.wti_apo_implied_volatility",
            "--runs-root",
            str(runs_root),
            "--output-root",
            str(iv_root),
            "--expiries",
            *expiries,
        ]
    )
    _run(
        [
            sys.executable,
            "-m",
            "experiments.wti_forward_q_validation",
            "--iv-path",
            str(iv_root / "apo_contract_implied_volatility.csv"),
            "--runs-root",
            str(runs_root),
            "--output-root",
            str(forward_root),
            "--expiries",
            *expiries,
            "--force",
        ]
    )
    _run(
        [
            sys.executable,
            "-m",
            "experiments.wti_liquidity_bootstrap",
            "--preset",
            args.bootstrap_preset,
            "--iv",
            str(iv_root / "apo_contract_implied_volatility.csv"),
            "--loo",
            str(iv_root / "apo_loo_predictions.csv"),
            "--transfer",
            str(iv_root / "apo_cross_type_predictions.csv"),
            "--forward",
            str(forward_root / "forward_q_predictions.csv"),
            "--output-root",
            str(bootstrap_root),
        ]
    )

    print("\nExtended forward-validation suite complete.", flush=True)
    print(f"runs_root={runs_root}", flush=True)
    print(f"analysis_root={analysis_root}", flush=True)
    print(
        "Key outputs:\n"
        f"  {forward_root / 'forward_q_error_summary.csv'}\n"
        f"  {forward_root / 'forward_q_predictions.csv'}\n"
        f"  {bootstrap_root / ('liquidity_cluster_bootstrap_' + args.bootstrap_preset + '.csv')}",
        flush=True,
    )


if __name__ == "__main__":
    main()
