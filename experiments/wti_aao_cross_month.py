"""Offline cross-month AAO definition and settlement correction audit.

Scans selected months in two passes, streaming the *monthly reductions* to
a local SQLite database. No Databento Historical client is instantiated;
the private database is gitignored and never uploaded. Run a small
four-month sample before opting in to --all (81 source months).
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import pandas as pd

from bayesian_asian_options.aao_cross_month import (
    initialize_db, ingest_latest, merge_registry, monthly_latest, summarize,
)

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "databento" / "wti_aao_bulk" / "raw"
PRIVATE = ROOT / "data" / "databento" / "wti_aao_bulk" / "derived_private"
REPORT = (ROOT / "results" / "analysis" /
          "wti_aao_history_feasibility" / "cross_month")


def paths_for(raw: Path, month: str) -> tuple[Path, Path]:
    definitions = sorted(raw.glob(f"aao_definition__{month}-*.dbn.zst"))
    if len(definitions) != 1:
        raise FileNotFoundError(
            f"Expected exactly one local AAO definition file for {month}, "
            f"found {len(definitions)}"
        )
    stats = raw / definitions[0].name.replace(
        "aao_definition__", "aao_statistics__", 1,
    )
    if not stats.is_file():
        raise FileNotFoundError(f"Missing local AAO statistics file: {month}")
    return definitions[0], stats


def run(months: list[str], data_dir: Path, report_dir: Path,
        private_dir: Path) -> dict:
    import databento as db  # DBNStore only; no network or API client

    if len(months) != len(set(months)) or not months:
        raise ValueError("The month sequence must be nonempty and unique")
    validated = []
    for month in months:
        if len(month) != 7 or str(pd.Period(month, freq="M")) != month:
            raise ValueError(f"Invalid YYYY-MM month: {month}")
        validated.append(paths_for(data_dir, month))
    registry: dict = {}
    for month, (definition_file, _) in zip(months, validated):
        definitions = db.DBNStore.from_file(definition_file).to_df(
            map_symbols=True, price_type="float"
        )
        merge_registry(registry, definitions)

    # A new uniquely named source selection means a new private file. Existing
    # file is only replaced after the full source-file existence preflight.
    suffix = ("81_months" if len(months) == 81 and
              months == [
                  str(p) for p in pd.period_range("2020-01", "2026-09", freq="M")
              ] else "_".join(months))
    private_file = private_dir / f"aao_cross_month_PROVISIONAL_{suffix}.sqlite3"
    conn = initialize_db(private_file)
    counts = []
    try:
        for month, (_, statistics_file) in zip(months, validated):
            stats = db.DBNStore.from_file(statistics_file).to_df(
                map_symbols=True, price_type="float"
            )
            latest, info = monthly_latest(stats, registry)
            ingest_latest(conn, latest, month)
            counts.append({"month": month, **info})
        result = summarize(conn, registry, months, counts)
    finally:
        conn.close()
    result["private_state_created"] = True
    result["within_month_counts"] = counts
    # JSON report excludes source symbols and vendor prices.
    report_dir.mkdir(parents=True, exist_ok=True)
    (report_dir / f"cross_month_audit_{suffix}.json").write_text(
        json.dumps(result, indent=2) + "\n", encoding="utf-8"
    )
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--all", action="store_true",
                        help="Process complete 81 months (local heavy I/O)")
    parser.add_argument("--months", nargs="+",
                        default=["2021-02", "2021-03", "2026-06", "2026-07"])
    parser.add_argument("--data-dir", type=Path, default=RAW)
    parser.add_argument("--report-dir", type=Path, default=REPORT)
    args = parser.parse_args()
    if args.all:
        months = [
            str(p) for p in pd.period_range("2020-01", "2026-09", freq="M")
        ]
    else:
        months = args.months
    result = run(months, args.data_dir, args.report_dir, PRIVATE)
    # Do not dump all 81 monthly reports to console.
    print(json.dumps({k: v for k, v in result.items()
                      if k not in ("source_months", "within_month_counts")},
                     indent=2))


if __name__ == "__main__":
    main()
