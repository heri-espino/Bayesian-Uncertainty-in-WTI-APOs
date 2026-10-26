"""Read-only Git LFS/sparse-checkout safety preflight for AAO re-download.

Call BEFORE any paid Databento request and before attempting Git LFS upload.
This script neither changes the worktree nor contacts the market provider.
"""
from __future__ import annotations

import argparse
import json
from datetime import date
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]
PREFIX = Path("data/databento/wti_aao_bulk")
ANCHOR = PREFIX / "README.md"


def windows() -> list[tuple[str, str]]:
    dates = []
    start = date(2020, 1, 1)
    end = date(2026, 10, 1)
    while start < end:
        next_month = (date(start.year + 1, 1, 1) if start.month == 12
                      else date(start.year, start.month + 1, 1))
        dates.append((start.isoformat(), next_month.isoformat()))
        start = next_month
    return dates


def expected_source_paths() -> list[Path]:
    return [
        PREFIX / "raw" / f"aao_{schema}__{start}__{end}.dbn.zst"
        for start, end in windows()
        for schema in ("definition", "statistics")
    ]


def git(root: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args], cwd=root, capture_output=True,
        text=True, check=False,
    )


def inspect(root: Path = ROOT, *, require_complete: bool = False) -> dict:
    root = root.resolve()
    errors = []
    top = git(root, "rev-parse", "--show-toplevel")
    if top.returncode or Path(top.stdout.strip()).resolve() != root:
        errors.append("not_running_from_expected_git_repository")
    anchor = root / ANCHOR
    if not anchor.is_file():
        errors.append(
            "missing_tracked_data_anchor: include data/databento/wti_aao_bulk "
            "in sparse checkout BEFORE downloading"
        )
    elif git(root, "ls-files", "--error-unmatch", "--",
             ANCHOR.as_posix()).returncode:
        errors.append("data_anchor_not_tracked_in_local_git_index")

    lfs = git(root, "lfs", "version")
    if lfs.returncode:
        errors.append("git_lfs_unavailable: install Git LFS and run git lfs install")

    paths = expected_source_paths()
    if len(paths) != 162:
        errors.append(f"unexpected_source_path_count:{len(paths)}")
    # Read the actual index/worktree rules; never assume a .gitattributes
    # or .gitignore edit itself made the data safely stageable.
    for path in (paths[0], paths[1], paths[-1]):
        text_path = path.as_posix()
        attr = git(root, "check-attr", "filter", "--", text_path)
        if attr.returncode or not attr.stdout.strip().endswith(": filter: lfs"):
            errors.append(f"missing_lfs_filter:{text_path}")
        # IMPORTANT: check-ignore -q RETURNS 0 for negation (!pattern)
        # with --no-index. Parse the verbose matching rule instead.
        ignored = git(root, "check-ignore", "--no-index", "-v",
                      "--", text_path)
        if ignored.returncode == 0:
            fields = ignored.stdout.strip().split("\t", 1)
            matching_rule = fields[0].rsplit(":", 1)[-1].strip()
            if not matching_rule.startswith("!"):
                errors.append(f"source_file_still_ignored:{text_path}")
        elif ignored.returncode != 1:
            errors.append(f"unable_to_verify_ignore_rules:{text_path}")

    present = sum((root / p).is_file() for p in paths)
    partials = list((root / PREFIX / "raw").glob("*.partial.dbn.zst"))
    if partials:
        errors.append(f"incomplete_download_partial_files:{len(partials)}")
    if require_complete and present != 162:
        errors.append(f"missing_source_files:{162-present}")

    return {
        "ready": not errors,
        "expected_source_files": len(paths),
        "source_files_currently_present": present,
        "git_lfs_available": lfs.returncode == 0,
        "sparse_checkout_data_anchor_present": anchor.is_file(),
        "market_provider_contacted": False,
        "issues": errors,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--require-complete", action="store_true",
                        help="Fail unless all 162 source DBN files exist")
    args = parser.parse_args()
    report = inspect(require_complete=args.require_complete)
    print(json.dumps(report, indent=2))
    if not report["ready"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
