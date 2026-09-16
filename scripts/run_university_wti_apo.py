"""University-workstation launcher for the canonical real WTI APO experiment.

Examples
--------
Environment/data check only:
    python -m scripts.run_university_wti_apo --check-only

Fast end-to-end pilot:
    python -m scripts.run_university_wti_apo --quick

Higher-precision run:
    python -m scripts.run_university_wti_apo
"""

from __future__ import annotations

import argparse
import importlib.util
from pathlib import Path
import platform
import subprocess
import sys

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--quick", action="store_true")
    parser.add_argument("--check-only", action="store_true")
    parser.add_argument("--valuation-date", default="2026-09-04")
    parser.add_argument("--apo-expiry", default="2026-10")
    parser.add_argument("--history-start", default="2024-01-01")
    parser.add_argument(
        "--refresh-inference",
        "--refresh-futures",
        dest="refresh_inference",
        action="store_true",
        help=(
            "Refresh Yahoo CL=F inference data. --refresh-futures remains as a "
            "backwards-compatible alias."
        ),
    )
    parser.add_argument("--include-min-tick", action="store_true")
    parser.add_argument("--futures-reference-csv", type=Path, default=None)
    parser.add_argument("--option-data-dir", type=Path, default=ROOT / "data" / "csv")
    parser.add_argument(
        "--cl-data-dir",
        type=Path,
        default=ROOT / "data" / "csv" / "CL",
    )
    parser.add_argument(
        "--cl-expiry-file",
        type=Path,
        default=ROOT / "data" / "csv" / "CL" / "contract_expiries.csv",
    )
    parser.add_argument(
        "--inference-cache-dir",
        type=Path,
        default=ROOT / "data" / "wti_yahoo",
    )
    parser.add_argument(
        "--treasury-dir",
        type=Path,
        default=ROOT / "data" / "rates" / "treasury",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=ROOT / "results" / "wti_apo_empirical",
    )
    return parser.parse_args(argv)


def _print_check(args: argparse.Namespace) -> None:
    print(f"Python: {sys.version.split()[0]}")
    print(f"Platform: {platform.platform()}")
    print(f"NumPy: {np.__version__}")
    print(f"pandas: {pd.__version__}")
    print(f"Repository: {ROOT}")
    print(f"Option data exists: {args.option_data_dir.exists()} ({args.option_data_dir})")
    print(f"yfinance installed: {importlib.util.find_spec('yfinance') is not None}")
    treasury_files = (
        sorted(args.treasury_dir.glob("*.csv")) if args.treasury_dir.exists() else []
    )
    cl_files = (
        sorted(args.cl_data_dir.glob("CL*.csv")) if args.cl_data_dir.exists() else []
    )
    print(f"Local Treasury CSVs: {len(treasury_files)}")
    print(f"Barchart CL files: {len(cl_files)} ({args.cl_data_dir})")
    print(
        f"CL expiry reference exists: {args.cl_expiry_file.exists()} "
        f"({args.cl_expiry_file})"
    )
    print(f"Yahoo CL=F inference cache: {args.inference_cache_dir}")
    print(
        "Network requirements for a fresh run: Yahoo Finance CL=F history; "
        "U.S. Treasury only if the local Treasury directory is empty. "
        "Individual CL curve data are read locally from committed Barchart CSVs."
    )


def main(argv: list[str] | None = None) -> None:
    args = parse_args(argv)
    _print_check(args)
    if args.check_only:
        return

    command = [
        sys.executable,
        "-m",
        "experiments.wti_apo_empirical",
        "--valuation-date",
        args.valuation_date,
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
    ]
    if args.refresh_inference:
        command.append("--refresh-inference")
    if args.include_min_tick:
        command.append("--include-min-tick")
    if args.futures_reference_csv is not None:
        command.extend(["--futures-reference-csv", str(args.futures_reference_csv)])

    if args.quick:
        command.extend(
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
    else:
        command.extend(
            [
                "--chains",
                "4",
                "--n-iter",
                "20000",
                "--burn-in",
                "4000",
                "--pricing-paths",
                "100000",
                "--sigma-grid-size",
                "41",
            ]
        )

    print("\nRunning:")
    print(" ".join(command))
    subprocess.run(command, cwd=ROOT, check=True)


if __name__ == "__main__":
    main()
