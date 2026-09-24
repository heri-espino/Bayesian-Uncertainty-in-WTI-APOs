"""Run the complete first-nearby physical-volatility robustness suite.

Prerequisite: acquire local proprietary CL settlement statistics with
experiments.wti_databento_first_nearby --mode download.

This runner is production-oriented and potentially expensive. It does not buy
market data and does not use GitHub Actions.
"""

from __future__ import annotations

import argparse
import subprocess
import sys

from experiments.wti_apo_empirical import ROOT


def _run(command: list[str]) -> None:
    print("\n$", " ".join(command), flush=True)
    subprocess.run(command, cwd=ROOT, check=True)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--refresh-yahoo", action="store_true")
    parser.add_argument(
        "--bootstrap-preset",
        choices=("research", "monster"),
        default="monster",
    )
    parser.add_argument("--skip-reconstruction", action="store_true")
    parser.add_argument("--skip-extended", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    reconstruction_root = (
        ROOT / "results" / "analysis" / "wti_first_nearby"
    )
    first_history = (
        reconstruction_root / "first_nearby_reconstruction_raw.csv"
    )
    runs_root = ROOT / "results" / "wti_apo_empirical_first_nearby"
    extended_root = (
        ROOT
        / "results"
        / "analysis"
        / "wti_extended_forward_first_nearby"
    )
    external_root = (
        ROOT
        / "results"
        / "analysis"
        / "wti_external_vanilla_q_validation_first_nearby"
    )

    if not args.skip_reconstruction:
        cmd = [
            sys.executable,
            "-m",
            "experiments.wti_first_nearby_reconstruction",
        ]
        if args.refresh_yahoo:
            cmd.append("--refresh-yahoo")
        _run(cmd)

    if not first_history.exists():
        raise FileNotFoundError(
            f"Missing {first_history}; run the reconstruction stage first."
        )

    if not args.skip_extended:
        _run(
            [
                sys.executable,
                "-m",
                "scripts.run_extended_forward_validation",
                "--physical-inference-source",
                "first-nearby",
                "--first-nearby-history",
                str(first_history),
                "--bootstrap-preset",
                args.bootstrap_preset,
            ]
        )

    apo_iv = (
        extended_root
        / "apo_implied_volatility"
        / "apo_contract_implied_volatility.csv"
    )
    apo_forward = (
        extended_root
        / "forward_q_validation"
        / "forward_q_predictions.csv"
    )
    if not apo_iv.exists() or not apo_forward.exists():
        raise FileNotFoundError(
            "First-nearby extended forward outputs are incomplete."
        )

    _run(
        [
            sys.executable,
            "-m",
            "experiments.wti_external_vanilla_q_validation",
            "--runs-root",
            str(runs_root),
            "--apo-iv-path",
            str(apo_iv),
            "--apo-forward-path",
            str(apo_forward),
            "--output-root",
            str(external_root),
            "--force",
        ]
    )

    _run(
        [
            sys.executable,
            "-m",
            "experiments.wti_external_q_cluster_bootstrap",
            "--external",
            str(external_root / "external_vanilla_q_predictions.csv"),
            "--apo",
            str(apo_forward),
            "--output",
            str(
                external_root
                / "surface_common_support_cluster_bootstrap.csv"
            ),
        ]
    )

    _run(
        [
            sys.executable,
            "-m",
            "experiments.wti_first_nearby_pricing_comparison",
        ]
    )

    print("\nFirst-nearby robustness suite complete.", flush=True)
    print(
        "Inspect:\n"
        f"  {reconstruction_root / 'reconstruction_report.json'}\n"
        f"  {reconstruction_root / 'posterior_comparison.csv'}\n"
        f"  {reconstruction_root / 'pricing_comparison_report.json'}\n"
        f"  {reconstruction_root / 'pricing_baseline_summary.csv'}\n"
        f"  {external_root / 'surface_common_support_cluster_bootstrap.csv'}",
        flush=True,
    )


if __name__ == "__main__":
    main()
