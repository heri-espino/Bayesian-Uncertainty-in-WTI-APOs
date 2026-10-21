"""Query Databento AAO/AO availability and quoted costs WITHOUT downloading data.

Only Historical.metadata.* and Historical.symbology.resolve are permitted.
No timeseries.get_range(), batch.submit_job(), or chargeable acquisition.
A resolved candidate parent and a positive cost quote do NOT prove that
historical WTI Asian option final settlements are available.

PowerShell
----------
python -m experiments.wti_databento_aao_feasibility --mode quote

DATABENTO_API_KEY is read only from the local environment.
"""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
from typing import Any

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "results" / "analysis" / "wti_aao_history_feasibility"
DATASET = "GLBX.MDP3"
DEFAULT_YEARS = (2023, 2024, 2025, 2026)
CANDIDATE_PARENTS = ("AAO", "AO")
DEFAULT_MAX_QUOTE_USD = 5.0


def _historical_client() -> Any:
    if not os.environ.get("DATABENTO_API_KEY"):
        raise RuntimeError(
            "DATABENTO_API_KEY is missing; set it in the local shell only."
        )
    try:
        import databento as db
    except ImportError as exc:
        raise RuntimeError(
            "Databento not installed; use python -m pip install -e '.[market]'"
        ) from exc
    return db.Historical()


def _safe_exception(exc: Exception) -> str:
    """Strip the local credential even if a third-party exception echoes it."""
    message = f"{type(exc).__name__}: {exc}"
    key = os.environ.get("DATABENTO_API_KEY")
    if key:
        message = message.replace(key, "[REDACTED]")
    return message[:450]


def _anchor(year: int) -> tuple[str, str]:
    """One whole UTC day, not a full-year billable statistics request."""
    if not 2000 <= year <= 2100:
        raise ValueError(f"Invalid anchor year: {year}")
    day = pd.Timestamp(f"{year}-06-17")
    return day.strftime("%Y-%m-%d"), (
        day + pd.Timedelta(days=1)
    ).strftime("%Y-%m-%d")


def _is_within_schema_range(
    day: str, *, ranges: dict[str, Any], schema: str,
) -> bool:
    record = ranges.get("schema", {}).get(schema)
    if not isinstance(record, dict):
        # A schema without a stated range is unverified: fail closed.
        return False
    start = pd.to_datetime(record.get("start"), utc=True, errors="coerce")
    end = pd.to_datetime(record.get("end"), utc=True, errors="coerce")
    target = pd.Timestamp(day, tz="UTC")
    return bool(pd.notna(start) and pd.notna(end) and start <= target < end)


def probe_aao_quotes(
    client: Any,
    *,
    years: tuple[int, ...] = DEFAULT_YEARS,
    parents: tuple[str, ...] = CANDIDATE_PARENTS,
    max_quote_usd: float = DEFAULT_MAX_QUOTE_USD,
) -> dict[str, Any]:
    """Return metadata-only AAO candidate symbol resolution and cost quotes.

    \`symbology.resolve\` confirms only a parent mapping at the specific day.
    \`get_cost\` is a quote for that parent/schema/day; it does not confirm
    actual settlements, active trading, available definition rows or
    rights to publish/download. This function never requests time series.
    """
    if not 0 < max_quote_usd < float("inf"):
        raise ValueError("max_quote_usd must be a finite positive number")
    if not years or not parents:
        raise ValueError("years and parents must be nonempty")
    years = tuple(sorted(set(int(y) for y in years)))
    parents = tuple(dict.fromkeys(p.strip().upper() for p in parents if p.strip()))
    if not parents:
        raise ValueError("No nonblank candidate parent symbols")

    present_datasets = client.metadata.list_datasets()
    if DATASET not in present_datasets:
        return {
            "dataset": DATASET, "dataset_accessible": False,
            "candidate_parents": list(parents), "years": list(years),
            "probes": [], "historical_aao_settlements_confirmed": False,
            "recommendation": "STOP: GLBX.MDP3 not listed in account metadata.",
            "no_timeseries_download": True,
        }
    schemas = list(client.metadata.list_schemas(dataset=DATASET))
    available = client.metadata.get_dataset_range(dataset=DATASET)
    report: dict[str, Any] = {
        "dataset": DATASET,
        "dataset_accessible": True,
        "available_schemas": schemas,
        "range": available,
        "candidate_parents": list(parents),
        "years": list(years),
        "max_quote_usd": float(max_quote_usd),
        "quotes_are_usd_not_incurred_charges": True,
        "no_timeseries_download": True,
        "historical_aao_settlements_confirmed": False,
        "probes": [],
        "interpretation": (
            "Positive parent mapping or nonzero quote does not confirm "
            "historical final settlement availability. Requires a separately "
            "approved and capped definition/statistics pilot."
        ),
    }
    for year in years:
        start, end = _anchor(year)
        for parent in parents:
            row: dict[str, Any] = {
                "year": year, "parent_candidate": parent,
                "start_inclusive": start, "end_exclusive": end,
                "parent_symbology_verified": False,
                "mapping_count": 0,
                "quotes_usd": {},
                "historical_final_settlements_verified": False,
            }
            if not _is_within_schema_range(
                start, ranges=available, schema="definition"
            ):
                row["status"] = "definition_schema_day_outside_available_range"
                report["probes"].append(row)
                continue
            try:
                mapping = client.symbology.resolve(
                    dataset=DATASET, symbols=[parent],
                    stype_in="parent", stype_out="raw_symbol",
                    start_date=start, end_date=end,
                )
                found = mapping.get("result", {}).get(parent, [])
                row["mapping_count"] = int(len(found))
                row["parent_symbology_verified"] = bool(found) and (
                    parent not in mapping.get("not_found", [])
                )
                row["mapping_status"] = str(mapping.get("message", "unknown"))
            except Exception as exc:
                row["status"] = "symbology_resolution_error"
                row["error"] = _safe_exception(exc)
                report["probes"].append(row)
                continue
            if not row["parent_symbology_verified"]:
                row["status"] = "candidate_parent_not_resolved_on_anchor_day"
                report["probes"].append(row)
                continue
            for schema in ("definition", "statistics"):
                if schema not in schemas or not _is_within_schema_range(
                    start, ranges=available, schema=schema
                ):
                    row["quotes_usd"][schema] = None
                    continue
                try:
                    quote = float(client.metadata.get_cost(
                        dataset=DATASET, start=start, end=end,
                        symbols=[parent], schema=schema, stype_in="parent",
                    ))
                    if not 0 <= quote < float("inf"):
                        raise ValueError("Nonfinite or negative USD quote")
                    row["quotes_usd"][schema] = quote
                except Exception as exc:
                    row["quotes_usd"][schema] = None
                    row.setdefault("quote_errors", {})[schema] = _safe_exception(exc)
            total = sum(
                value for value in row["quotes_usd"].values()
                if isinstance(value, (int, float))
            )
            missing_quotes = any(
                row["quotes_usd"].get(k) is None for k in ("definition", "statistics")
            )
            row["total_one_day_quote_usd"] = None if missing_quotes else round(total, 9)
            row["within_quote_ceiling"] = (
                not missing_quotes and total <= max_quote_usd
            )
            row["status"] = "parent_resolved_quote_only_not_settlement_proven"
            report["probes"].append(row)
    report["recommendation"] = (
        "Review parent coverage and quoted USD amounts; no download performed. "
        "Only if verified promising, explicitly approve a small cost-capped "
        "historical definition/statistics pilot."
    )
    return report


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mode", choices=("quote",), default="quote")
    parser.add_argument("--years", nargs="+", type=int, default=list(DEFAULT_YEARS))
    parser.add_argument(
        "--parents", nargs="+", default=list(CANDIDATE_PARENTS),
        help="Unverified Databento parent candidates (NOT guaranteed product symbols).",
    )
    parser.add_argument(
        "--max-quote-usd", type=float, default=DEFAULT_MAX_QUOTE_USD,
        help="Flag estimates above this ceiling. Never authorizes a download.",
    )
    parser.add_argument("--output-dir", type=Path, default=OUTPUT)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    report = probe_aao_quotes(
        _historical_client(),
        years=tuple(args.years),
        parents=tuple(args.parents),
        max_quote_usd=float(args.max_quote_usd),
    )
    args.output_dir.mkdir(parents=True, exist_ok=True)
    target = args.output_dir / "aao_metadata_quotes.json"
    target.write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
