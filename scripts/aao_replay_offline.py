"""Manually replay all completed offline AAO data-quality comparisons.

The command is dry-run by default. Pass --execute after source files have
been reacquired, hash-verified AND uploaded via Git LFS. Never makes
Databento API requests or starts paid data acquisition.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import subprocess
import sys

from scripts.aao_lfs_preflight import inspect

ROOT = Path(__file__).resolve().parents[1]
REPORT_ROOT = (
    ROOT / "results" / "analysis" / "wti_aao_history_feasibility"
)
RECOVERY_MANIFEST = (
    REPORT_ROOT / "reacquisition_20261026" / "bulk_acquisition_manifest.json"
)

# Preserve every prior diagnostic comparison. None of these is an
# independently validated option-pricing performance backtest.
STEPS: tuple[tuple[str, tuple[str, ...]], ...] = (
    ("hash_audit", (
        "scripts.audit_aao_manifests", "--manifest", str(RECOVERY_MANIFEST)
    )),
    ("inventory_81_months", ("experiments.wti_databento_aao_inventory", "--all")),
    ("coverage_figure", ("scripts.plot_aao_history_coverage",)),
    ("identity_february_2021", (
        "experiments.wti_aao_identity_probe", "--month", "2021-02"
    )),
    ("identity_june_2026", (
        "experiments.wti_aao_identity_probe", "--month", "2026-06"
    )),
    ("same_day_asof_diagnostic", (
        "experiments.wti_aao_settlement_gate",
        "--months", "2021-02", "2026-06"
    )),
    ("snapshot_mapping_comparison", (
        "experiments.wti_aao_mapping_comparison",
        "--months", "2021-02", "2026-06"
    )),
    ("native_symbol_comparison", (
        "experiments.wti_aao_symbol_mapping",
        "--months", "2021-02", "2026-06"
    )),
    ("monthly_settlement_candidates", (
        "experiments.wti_aao_contract_day_candidates",
        "--months", "2021-02", "2026-06"
    )),
    ("cross_month_all", ("experiments.wti_aao_cross_month", "--all")),
    ("final_date_and_barchart_quality", (
        "experiments.wti_aao_panel_quality", "--scan-final-dates"
    )),
)


def command(step: tuple[str, ...]) -> list[str]:
    return [sys.executable, "-m", *step]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--execute", action="store_true",
                        help="Actually run offline diagnostics; manual only")
    args = parser.parse_args()
    if not args.execute:
        print(json.dumps({
            "execution": False,
            "manual_only": True,
            "no_provider_requests": True,
            "steps": [
                {"name": name, "command": command(parts)}
                for name, parts in STEPS
            ],
        }, indent=2))
        return

    preflight = inspect(require_complete=True)
    if not preflight["ready"]:
        raise SystemExit(
            "Cannot replay offline comparisons: source/LFS preflight failed:\n"
            + json.dumps(preflight["issues"], indent=2)
        )
    if not RECOVERY_MANIFEST.is_file():
        raise SystemExit(
            "Missing replacement acquisition manifest; do not claim "
            "the replacement data are verified."
        )
    for name, args_for_step in STEPS:
        print(f"\n=== {name} ===", flush=True)
        subprocess.run(command(args_for_step), cwd=ROOT, check=True)
    print("\nAll 11 historical data-quality comparisons completed.")


if __name__ == "__main__":
    main()
