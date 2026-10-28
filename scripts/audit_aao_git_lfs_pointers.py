"""Offline verification of the *tracked Git LFS pointers* against the correct AAO reacquisition ledger.

No market API, network requests, Git LFS downloads, mutation of the worktree,
or fee-incurring operations. Operates on Git object history rather than the
worktree, so it can audit metadata even when the local checkout is sparse.

IMPORTANT: A valid LFS pointer is NOT proof that its binary object was
uploaded to, or can be downloaded from, the Git LFS server. To prove remote
retrievability, perform a separately authorized independent restore of actual
payloads into a clean temporary workspace, compare SHA-256 and retain the log.

Run from any full/sparse checkout of this repo:
    python -m scripts.audit_aao_git_lfs_pointers
    python -m scripts.audit_aao_git_lfs_pointers --write-report
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / "results/analysis/wti_aao_history_feasibility/reacquisition_20261026/bulk_acquisition_manifest.json"
PREFIX = "data/databento/wti_aao_bulk/raw/"
OUT = ROOT / "results/analysis/wti_aao_history_feasibility/integrity/lfs_reacquisition_pointer_check.json"
POINTER = re.compile(
    rb"\Aversion https://git-lfs.github.com/spec/v1\n"
    rb"oid sha256:([0-9a-f]{64})\nsize ([0-9]+)\n\Z"
)


def git(*args: str) -> bytes:
    result = subprocess.run(
        ["git", *args], cwd=ROOT, check=False,
        capture_output=True,
    )
    if result.returncode:
        raise RuntimeError(f"git {' '.join(args)} failed: {result.stderr.decode(errors='replace')[:450]}")
    return result.stdout


def audit() -> dict:
    ledger = json.loads(LEDGER.read_text(encoding="utf-8"))
    expected = {item["file"]: item for item in ledger["completed"].values()}
    all_git = git("ls-tree", "-r", "--name-only", "HEAD", "--", PREFIX)
    actual = set(all_git.decode("utf-8").splitlines())
    errors: list[dict] = []
    verified = 0
    total = 0
    if len(expected) != 162:
        errors.append({"problem": "expected_162_reacquisition_records", "found": len(expected)})
    for name, item in sorted(expected.items()):
        path = PREFIX + name
        if path not in actual:
            errors.append({"problem": "missing_tracked_path", "path": path})
            continue
        raw = git("show", "HEAD:" + path)
        match = POINTER.fullmatch(raw)
        if match is None:
            errors.append({"problem": "not_a_valid_lfs_pointer", "path": path, "git_blob_bytes": len(raw)})
            continue
        digest = match.group(1).decode("ascii")
        size = int(match.group(2))
        if digest != item["sha256"] or size != item["size_bytes"]:
            errors.append({
                "problem": "pointer_disagrees_with_reacquisition_manifest",
                "path": path,
                "expected_oid": item["sha256"],
                "actual_oid": digest,
                "expected_bytes": item["size_bytes"],
                "actual_bytes": size,
            })
            continue
        verified += 1
        total += size
    extras = sorted(actual - {PREFIX + name for name in expected})
    for path in extras:
        errors.append({"problem": "extra_tracked_raw_path", "path": path})
    return {
        "scope": "GIT_POINTERS_ONLY_NO_BINARY_REMOTE_RESTORE",
        "success": not errors and verified == 162,
        "git_head": git("rev-parse", "HEAD").decode().strip(),
        "manifest": LEDGER.relative_to(ROOT).as_posix(),
        "expected_chunks": len(expected),
        "verified_pointer_chunks": verified,
        "expected_definitions": sum(x["schema"] == "definition" for x in expected.values()),
        "expected_statistics": sum(x["schema"] == "statistics" for x in expected.values()),
        "sum_verified_payload_bytes": total,
        "verified_remote_lfs_payloads": False,
        "market_provider_contacted": False,
        "new_downloads_or_spend": False,
        "issues": errors,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write-report", action="store_true")
    args = parser.parse_args()
    result = audit()
    output = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.write_report:
        OUT.parent.mkdir(parents=True, exist_ok=True)
        OUT.write_text(output, encoding="utf-8")
    print(output)
    if not result["success"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
