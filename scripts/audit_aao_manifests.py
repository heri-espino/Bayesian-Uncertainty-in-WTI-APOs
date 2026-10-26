"""Offline integrity audit of original 80-month and February AAO DBN downloads.

Only reads local files/manifests; no Databento API or network requests.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data" / "databento" / "wti_aao_bulk" / "raw"
REPORT_ROOT = ROOT / "results" / "analysis" / "wti_aao_history_feasibility"
ORIGINAL = REPORT_ROOT / "bulk" / "bulk_acquisition_manifest.json"
FEBRUARY = REPORT_ROOT / "bulk_feb2021" / "bulk_acquisition_manifest.json"
OUTPUT = REPORT_ROOT / "integrity" / "combined_manifest_audit.json"


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def expected_months(start: str, end: str) -> set[str]:
    left, right = date.fromisoformat(start), date.fromisoformat(end)
    result = set()
    while left < right:
        result.add(left.strftime("%Y-%m"))
        left = (date(left.year + 1, 1, 1) if left.month == 12
                else date(left.year, left.month + 1, 1))
    return result


def audit(raw_dir: Path, manifests: list[Path], *,
          verify_sha: bool = True, start: str = "2020-01-01",
          end: str = "2026-10-01") -> dict:
    """Fail closed on missing, altered, duplicate or untracked source chunks."""
    errors = []
    seen = set()
    months: dict[str, set[str]] = {}
    verified = 0
    quoted = 0.0
    for path in manifests:
        if not path.is_file():
            errors.append(f"missing_manifest:{path.parent.name}")
            continue
        ledger = json.loads(path.read_text(encoding="utf-8"))
        if ledger.get("dataset") != "GLBX.MDP3" or ledger.get("parent") != "AAO.OPT":
            errors.append(f"wrong_request:{path.parent.name}")
        if not ledger.get("completed_all_eligible"):
            errors.append(f"incomplete_manifest:{path.parent.name}")
        for key, item in ledger.get("completed", {}).items():
            name = item.get("file", "")
            schema = item.get("schema")
            left = str(item.get("start", ""))
            right = str(item.get("end", ""))
            if not isinstance(name, str) or Path(name).name != name or (
                schema not in ("definition", "statistics")
            ) or name != f"aao_{schema}__{left}__{right}.dbn.zst":
                errors.append(f"invalid_file_identity:{key}")
                continue
            if name in seen:
                errors.append(f"duplicate_chunk:{name}")
                continue
            seen.add(name)
            try:
                start_date, end_date = date.fromisoformat(left), date.fromisoformat(right)
                next_month = (date(start_date.year + 1, 1, 1)
                              if start_date.month == 12 else
                              date(start_date.year, start_date.month + 1, 1))
                if start_date.day != 1 or end_date != next_month:
                    raise ValueError
            except (TypeError, ValueError):
                errors.append(f"invalid_window:{name}")
            months.setdefault(left[:7], set()).add(schema)
            try:
                cost = float(item["quote_usd"])
                if not 0 <= cost < float("inf"):
                    raise ValueError
                quoted += cost
            except (TypeError, KeyError, ValueError):
                errors.append(f"invalid_quote:{name}")
            file = raw_dir / name
            if not file.is_file():
                errors.append(f"missing_file:{name}")
            elif file.stat().st_size != item.get("size_bytes"):
                errors.append(f"size_mismatch:{name}")
            elif verify_sha and sha256_file(file) != item.get("sha256"):
                errors.append(f"checksum_mismatch:{name}")
            else:
                verified += 1
    expected = expected_months(start, end)
    for month in sorted(expected):
        missing = {"definition", "statistics"} - months.get(month, set())
        if missing:
            errors.append(f"missing_schema:{month}:{','.join(sorted(missing))}")
    if set(months) - expected:
        errors.append("unexpected_months:" + ",".join(sorted(set(months) - expected)))
    extras = sorted(p.name for p in raw_dir.glob("aao_*.dbn.zst") if p.name not in seen)
    if extras:
        errors.append("untracked_files:" + ",".join(extras[:10]))
    return {
        "success": not errors,
        "data_contacted_provider": False,
        "sha256_verified": verify_sha,
        "files_verified": verified,
        "files_referenced": len(seen),
        "month_count": len(expected & set(months)),
        "expected_month_count": len(expected),
        "combined_quoted_usd": round(quoted, 8),
        "issues": errors,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data-dir", type=Path, default=DATA_DIR)
    parser.add_argument("--manifest", type=Path, action="append", dest="manifests",
                        help="Use one or more replacement acquisition manifests")
    parser.add_argument("--original", type=Path, default=ORIGINAL)
    parser.add_argument("--february", type=Path, default=FEBRUARY)
    parser.add_argument("--output", type=Path, default=OUTPUT)
    parser.add_argument("--skip-sha", action="store_true",
                        help="File-size check only, NOT integrity certification")
    args = parser.parse_args()
    manifests = args.manifests if args.manifests else [args.original, args.february]
    report = audit(args.data_dir, manifests,
                   verify_sha=not args.skip_sha)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))
    if not report["success"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
