"""Run the lightweight referee-requested robustness checks.

This runner uses only committed empirical runs and derived market-data panels.
It does not rerun MCMC, APO implied-volatility fitting, the synthetic mechanism
map, or any heavy Monte Carlo experiment.

Outputs:
- recent historical volatility benchmarks on exact strict-forward holdouts;
- posterior-RMS plug-in comparison;
- prior-contract APO IV carry benchmark versus the previous-day smile on exact common rows;
- moment-matched LO-to-APO surface aggregation sensitivity;
- American CRR tree-step convergence audit;
- prior-date LO fitted-surface shape and call/put consistency audit.
"""

from __future__ import annotations

import subprocess
import sys


def _run(args: list[str]) -> None:
    print("+", " ".join(args), flush=True)
    subprocess.run(args, check=True)


def main() -> None:
    python = sys.executable

    _run(
        [
            python,
            "-m",
            "experiments.wti_recent_historical_benchmarks",
        ]
    )
    _run(
        [
            python,
            "-m",
            "experiments.wti_rms_plugin_comparison",
        ]
    )
    _run(
        [
            python,
            "-m",
            "experiments.wti_prior_contract_iv_carry",
        ]
    )
    _run(
        [
            python,
            "-m",
            "experiments.wti_external_vanilla_q_validation",
            "--aggregation",
            "weighted_rms",
            "--surface-aggregation",
            "moment_matched",
            "--output-root",
            "results/analysis/wti_external_vanilla_q_validation_moment_matched",
            "--apo-forward-path",
            "results/analysis/wti_extended_forward/forward_q_validation/forward_q_predictions.csv",
            "--force",
        ]
    )
    _run(
        [
            python,
            "-m",
            "experiments.wti_lo_tree_convergence",
        ]
    )
    _run(
        [
            python,
            "-m",
            "experiments.wti_lo_surface_shape_audit",
        ]
    )

    print("\nReviewer robustness checks complete.", flush=True)
    print(
        "Commit the six result groups only after inspecting the summaries.",
        flush=True,
    )


if __name__ == "__main__":
    main()
