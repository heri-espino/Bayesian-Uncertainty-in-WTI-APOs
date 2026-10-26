"""Offline CLI for conservative AAO contract/day candidate normalization.

Only reads local DBN source files. Exports aggregate JSON by default;
price-level candidate rows require --export-private and remain gitignored.
Cross-month correction reconciliation and market validation are still open.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import pandas as pd

from bayesian_asian_options.aao_settlements import normalize

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "databento" / "wti_aao_bulk" / "raw"
REPORT = (ROOT / "results" / "analysis" /
          "wti_aao_history_feasibility" / "contract_day_candidates")
PRIVATE = ROOT / "data" / "databento" / "wti_aao_bulk" / "derived_private"


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024*1024), b""):
            digest.update(block)
    return digest.hexdigest()


def run_month(month: str, raw_dir: Path, report_dir: Path,
              private_dir: Path | None = None) -> dict:
    """Read one local month and write aggregate diagnostics, optionally private rows."""
    import databento as db

    definitions = sorted(
        raw_dir.glob(f"aao_definition__{month}-*.dbn.zst")
    )
    if len(definitions) != 1:
        raise FileNotFoundError(
            f"Expected one local definition DBN for {month}; found {len(definitions)}"
        )
    stats_path = raw_dir / definitions[0].name.replace(
        "aao_definition__", "aao_statistics__", 1
    )
    if not stats_path.is_file():
        raise FileNotFoundError(f"Missing local statistics DBN for {month}")
    d = db.DBNStore.from_file(definitions[0]).to_df(map_symbols=True)
    s = db.DBNStore.from_file(stats_path).to_df(map_symbols=True)
    candidates, report = normalize(d, s)
    report["month"] = month
    report["source_hashes"] = {
        "definition_sha256": file_sha256(definitions[0]),
        "statistics_sha256": file_sha256(stats_path),
    }
    if private_dir is not None:
        private_dir.mkdir(parents=True, exist_ok=True)
        target = private_dir / f"AAO_CANDIDATES_NOT_VALIDATED_{month}.csv.gz"
        candidates.to_csv(target, index=False, compression="gzip")
        report["private_panel_created"] = True
    else:
        report["private_panel_created"] = False
    report_dir.mkdir(parents=True, exist_ok=True)
    path = report_dir / f"contract_day_candidates_{month}.json"
    path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    return report


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--months", nargs="+", default=["2021-02", "2026-06"])
    parser.add_argument("--all", action="store_true",
                        help="Process all 81 local months, one at a time")
    parser.add_argument("--data-dir", type=Path, default=RAW)
    parser.add_argument("--report-dir", type=Path, default=REPORT)
    parser.add_argument(
        "--export-private", action="store_true",
        help="Write licensed row-level candidate prices locally; gitignored",
    )
    args = parser.parse_args()
    months = (
        [str(period) for period in pd.period_range(
            "2020-01", "2026-09", freq="M"
        )]
        if args.all else args.months
    )
    for month in months:
        print(json.dumps(
            run_month(
                month, args.data_dir, args.report_dir,
                PRIVATE if args.export_private else None,
            ), indent=2,
        ))


if __name__ == "__main__":
    main()
