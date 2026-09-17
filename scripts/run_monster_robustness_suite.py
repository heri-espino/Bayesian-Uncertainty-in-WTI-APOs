"""Run the compute-intensive publication robustness suite.

This runner is deliberately separate from ``run_publication_experiments``.  The default
settings are intended for the university workstation with an RTX 4500 Ada and abundant RAM,
not for CI or laptops.

Example
-------
    python -m scripts.run_monster_robustness_suite --backend cupy
"""

from __future__ import annotations

import argparse
from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]
IMPLIED_REPORT = (
    ROOT
    / "results"
    / "analysis"
    / "wti_apo_implied_volatility"
    / "apo_implied_volatility_report.json"
)

STAGES = (
    "implied-vol",
    "mechanism-map",
    "high-precision",
    "qmc",
    "student-t",
    "forward-q",
    "sbc",
    "bootstrap",
)


def _run(label: str, args: list[str]) -> None:
    command = [sys.executable, *args]
    print(f"\n=== {label} ===", flush=True)
    print("+ " + " ".join(command), flush=True)
    subprocess.run(command, cwd=ROOT, check=True)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--backend", choices=("auto", "numpy", "cupy"), default="cupy")
    parser.add_argument("--skip-validation", action="store_true")
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--skip", action="append", choices=STAGES, default=[], metavar="STAGE")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    skipped = set(args.skip)

    if not args.skip_validation:
        _run("pytest", ["-m", "pytest", "-q"])
        _run("repository structure", ["-m", "scripts.check_repo_structure"])

    force = ["--force"] if args.force else []

    if "implied-vol" not in skipped:
        if IMPLIED_REPORT.exists() and not args.force:
            print("\n=== implied-vol: existing completed outputs reused ===", flush=True)
        else:
            _run(
                "APO implied volatility prerequisite",
                [
                    "-m",
                    "experiments.wti_apo_implied_volatility",
                    "--expiries",
                    "2026-09",
                    "2026-10",
                ],
            )

    if "mechanism-map" not in skipped:
        _run(
            "massive exact-quadrature mechanism map",
            [
                "-m",
                "experiments.massive_mechanism_map",
                "--preset",
                "monster",
                "--backend",
                args.backend,
                *force,
            ],
        )

    if "high-precision" not in skipped:
        _run(
            "high-precision pseudo-random GPU pricing benchmark",
            [
                "-m",
                "experiments.wti_high_precision_pricing",
                "--preset",
                "monster",
                "--backend",
                args.backend,
                *force,
            ],
        )

    if "qmc" not in skipped:
        _run(
            "randomized Sobol QMC pricing benchmark",
            [
                "-m",
                "experiments.wti_randomized_qmc_benchmark",
                "--preset",
                "monster",
                "--backend",
                args.backend,
                *force,
            ],
        )

    if "student-t" not in skipped:
        _run(
            "Student-t physical-measure robustness",
            [
                "-m",
                "experiments.wti_student_t_robustness",
                "--preset",
                "monster",
                *force,
            ],
        )

    if "forward-q" not in skipped:
        _run(
            "strict forward-in-time Q validation",
            ["-m", "experiments.wti_forward_q_validation", *force],
        )

    if "sbc" not in skipped:
        _run(
            "simulation-based calibration",
            [
                "-m",
                "experiments.simulation_based_calibration",
                "--preset",
                "monster",
                "--backend",
                args.backend,
                *force,
            ],
        )

    if "bootstrap" not in skipped:
        _run(
            "liquidity/date cluster bootstrap",
            ["-m", "experiments.wti_liquidity_bootstrap", "--preset", "monster"],
        )

    print(
        "\nMonster robustness suite completed. Commit the small CSV/JSON summaries and figures; "
        "do not commit local checkpoints, raw GPU scratch arrays, or other large intermediate files.",
        flush=True,
    )


if __name__ == "__main__":
    main()
