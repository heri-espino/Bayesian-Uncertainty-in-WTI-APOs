"""Run the publication-support experiments in their production order.

Completed outputs are reused when a reliable final sentinel is available; pass ``--force``
to rerun those stages.  The expensive extreme synthetic run is never regenerated implicitly.
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]
TAYLOR_RUN = ROOT / "results" / "large_scale_synthetic" / "f497062f0c571126"
TAYLOR_REPORT = ROOT / "results" / "analysis" / "taylor_mechanism" / "taylor_mechanism_report.json"
SEPTEMBER_PANEL = ROOT / "results" / "wti_apo_empirical" / "panel_202609" / "all_dates" / "panel_contract_pricing.csv"
SEPTEMBER_AUDIT = ROOT / "results" / "wti_apo_empirical" / "panel_202609" / "panel_date_audit.csv"
PARTIAL_REPORT = ROOT / "results" / "analysis" / "partial_fixing_202609" / "partial_fixing_report.json"
CURRAN_OCT_REPORT = ROOT / "results" / "analysis" / "curran_benchmark" / "202610" / "curran_report.json"
CURRAN_SEP_REPORT = ROOT / "results" / "analysis" / "curran_benchmark" / "202609" / "curran_report.json"
IMPLIED_VOL_REPORT = ROOT / "results" / "analysis" / "wti_apo_implied_volatility" / "apo_implied_volatility_report.json"

STAGES = (
    "taylor",
    "september",
    "partial-fixing",
    "mc-convergence",
    "prior-window",
    "curran-october",
    "curran-september",
    "implied-vol",
)


def _run(label: str, args: list[str]) -> None:
    command = [sys.executable, *args]
    print(f"\n=== {label} ===", flush=True)
    print("+ " + " ".join(command), flush=True)
    subprocess.run(command, cwd=ROOT, check=True)


def _eligible_september_dates(start_date: str, end_date: str) -> list[str]:
    if not SEPTEMBER_AUDIT.exists():
        return []
    dates: list[str] = []
    with SEPTEMBER_AUDIT.open(newline="", encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            date = str(row.get("valuation_date", ""))
            eligible = str(row.get("eligible", "")).strip().lower() in {"true", "1", "yes"}
            if eligible and start_date <= date <= end_date:
                dates.append(date)
    return sorted(dates)


def _production_manifest(run_dir: Path) -> bool:
    path = run_dir / "manifest.json"
    if not path.exists():
        return False
    try:
        manifest = json.loads(path.read_text(encoding="utf-8"))
        mcmc = manifest["mcmc"]
        pricing = manifest["pricing"]
        return bool(
            int(mcmc["chains"]) >= 4
            and int(mcmc["n_iter_per_chain"]) >= 20_000
            and int(mcmc["burn_in_per_chain"]) >= 4_000
            and int(pricing["n_paths_per_sigma"]) >= 100_000
            and int(pricing["sigma_grid_size"]) >= 41
        )
    except (KeyError, TypeError, ValueError, json.JSONDecodeError):
        return False


def _september_production_complete(start_date: str, end_date: str) -> bool:
    if not SEPTEMBER_PANEL.exists():
        return False
    dates = _eligible_september_dates(start_date, end_date)
    if not dates:
        return False
    root = ROOT / "results" / "wti_apo_empirical"
    return all(_production_manifest(root / f"{date}_202609") for date in dates)


def _has_taylor_checkpoints() -> bool:
    checkpoint_root = TAYLOR_RUN / "checkpoints" / "inference"
    return checkpoint_root.exists() and next(checkpoint_root.rglob("*.npz"), None) is not None


def _skip(stage: str, skipped: set[str]) -> bool:
    if stage in skipped:
        print(f"\n=== {stage}: skipped by request ===", flush=True)
        return True
    return False


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--skip-validation", action="store_true")
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--skip", action="append", choices=STAGES, default=[], metavar="STAGE")
    parser.add_argument("--start-date", default="2026-09-01")
    parser.add_argument("--end-date", default="2026-09-17")
    parser.add_argument("--resume-extreme-if-needed", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    skipped = set(args.skip)

    if not args.skip_validation:
        _run("repository structure", ["-m", "scripts.check_repo_structure"])
        _run("manuscript layout", ["paper/build.py", "--check"])
        _run("pytest", ["-m", "pytest", "-q"])
        _run("Sphinx warnings-as-errors", ["-m", "sphinx", "-W", "--keep-going", "-b", "html", "docs", "docs/_build/html"])

    if not _skip("taylor", skipped):
        if TAYLOR_REPORT.exists() and not args.force:
            print(f"\n=== taylor: reusing {TAYLOR_REPORT.relative_to(ROOT)} ===", flush=True)
        else:
            if not _has_taylor_checkpoints() and args.resume_extreme_if_needed:
                _run("resume extreme synthetic checkpoints", ["-m", "experiments.large_scale_synthetic", "--preset", "extreme", "--backend", "cupy"])
            if _has_taylor_checkpoints():
                _run("Taylor mechanism", ["-m", "experiments.taylor_mechanism", "--run-dir", str(TAYLOR_RUN.relative_to(ROOT))])
            else:
                print("\n=== taylor: skipped; extreme checkpoints absent. Use --resume-extreme-if-needed to regenerate. ===", flush=True)

    if not _skip("september", skipped):
        if _september_production_complete(args.start_date, args.end_date) and not args.force:
            print("\n=== september: existing production-budget panel is complete; reusing it ===", flush=True)
        else:
            common = ["-m", "experiments.wti_apo_date_panel", "--apo-expiry", "2026-09", "--start-date", args.start_date, "--end-date", args.end_date]
            _run("September eligible-date audit", [*common, "--list-dates"])
            _run("September production partial-fixing panel", common)

    if not _skip("partial-fixing", skipped):
        if PARTIAL_REPORT.exists() and not args.force and _september_production_complete(args.start_date, args.end_date):
            print(f"\n=== partial-fixing: reusing {PARTIAL_REPORT.relative_to(ROOT)} ===", flush=True)
        else:
            _run("partial-fixing analysis", ["-m", "experiments.analyze_partial_fixing", "--panel", str(SEPTEMBER_PANEL.relative_to(ROOT))])

    if not _skip("mc-convergence", skipped):
        _run("Monte Carlo convergence (research)", ["-m", "experiments.wti_mc_convergence", "--preset", "research"])

    if not _skip("prior-window", skipped):
        _run("prior/window sensitivity (research)", ["-m", "experiments.wti_prior_window_sensitivity", "--preset", "research"])

    if not _skip("curran-october", skipped):
        if CURRAN_OCT_REPORT.exists() and not args.force:
            print(f"\n=== curran-october: reusing {CURRAN_OCT_REPORT.relative_to(ROOT)} ===", flush=True)
        else:
            _run("Curran benchmark October", ["-m", "experiments.wti_curran_benchmark", "--apo-expiry", "2026-10"])

    if not _skip("curran-september", skipped):
        if CURRAN_SEP_REPORT.exists() and not args.force:
            print(f"\n=== curran-september: reusing {CURRAN_SEP_REPORT.relative_to(ROOT)} ===", flush=True)
        else:
            _run("Curran benchmark September", ["-m", "experiments.wti_curran_benchmark", "--apo-expiry", "2026-09"])

    if not _skip("implied-vol", skipped):
        if IMPLIED_VOL_REPORT.exists() and not args.force:
            print(f"\n=== implied-vol: reusing {IMPLIED_VOL_REPORT.relative_to(ROOT)} ===", flush=True)
        else:
            _run(
                "APO-implied Q volatility, LOO and call/put transfer",
                ["-m", "experiments.wti_apo_implied_volatility", "--expiries", "2026-09", "2026-10"],
            )

    print(
        "\nAll requested publication experiments completed. APO-implied Q volatility uses the "
        "existing APO settlements and CL futures curves, with leave-one-out and cross-option-type "
        "evaluation to avoid same-contract calibration/evaluation circularity. Vanilla CL options "
        "remain optional as a future independent external Q-volatility validation source.",
        flush=True,
    )


if __name__ == "__main__":
    main()
