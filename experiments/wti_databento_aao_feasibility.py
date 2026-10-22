"""Query Databento AAO/AO availability and quoted costs WITHOUT downloading data.

Only Historical.metadata.* and Historical.symbology.resolve are permitted.
The LO.OPT positive control uses the existing validated 2026-08-24 data date.
Zero symbology.resolve mappings NEVER suppress independent cost/count probes.
No timeseries.get_range(), batch.submit_job(), or chargeable acquisition.
Parent symbol syntax is [ROOT].OPT (e.g. AAO.OPT); bare product-code
aliases AAO and AO are normalized automatically. Each probe uses a trading
weekday rather than an arbitrary Saturday/Sunday.
Even positive record counts and a positive quote do NOT prove that
historical WTI Asian option final settlements are available.

PowerShell
----------
python -m experiments.wti_databento_aao_feasibility --mode quote --parents AAO.OPT AO.OPT

DATABENTO_API_KEY is read only from the local environment.
"""

from __future__ import annotations

import argparse
import json
import os
import re
from pathlib import Path
from typing import Any

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "results" / "analysis" / "wti_aao_history_feasibility"
DATASET = "GLBX.MDP3"
DEFAULT_YEARS = (2023, 2024, 2025, 2026)
CANDIDATE_PARENTS = ("AAO.OPT", "AO.OPT")
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


_PARENT_RE = re.compile(r"^[A-Z0-9]+\.OPT$")


def _normalize_parent(value: str) -> str:
    """Accept CME product-code aliases but query Databento option parents."""
    raw = value.strip().upper()
    if "." not in raw:
        raw += ".OPT"
    if not _PARENT_RE.fullmatch(raw):
        raise ValueError(
            f"Invalid option parent {value!r}. Expected [ROOT].OPT "
            "(for example AAO.OPT); .FUT is not an option parent."
        )
    return raw


def _anchor(year: int) -> tuple[str, str]:
    """Use June's second Wednesday, avoiding weekend-only metadata probes."""
    if not 2000 <= year <= 2100:
        raise ValueError(f"Invalid anchor year: {year}")
    first = pd.Timestamp(f"{year}-06-01")
    # Mon=0, Wed=2; second Wednesday is the first + seven days.
    day = first + pd.Timedelta(days=(2 - first.weekday()) % 7 + 7)
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


def _probe_parent_day(
    client: Any,
    *,
    parent: str,
    start: str,
    end: str,
    schemas: list[str],
    available: dict[str, Any],
    max_quote_usd: float,
) -> dict[str, Any]:
    """Probe parent resolution and independently query counts/quotes for one day.

    A parent-to-instrument_id resolution may not enumerate a large options
    family. The metadata queries are attempted independently of its status.
    No time-series API is called.
    """
    row: dict[str, Any] = {
        "parent_candidate": parent,
        "start_inclusive": start,
        "end_exclusive": end,
        "parent_symbology_verified": False,
        "mapping_count": 0,
        "record_counts": {},
        "quotes_usd": {},
        "historical_final_settlements_verified": False,
    }
    if not _is_within_schema_range(
        start, ranges=available, schema="definition"
    ):
        row["status"] = "definition_schema_day_outside_available_range"
        return row

    try:
        mapping = client.symbology.resolve(
            dataset=DATASET, symbols=[parent],
            stype_in="parent", stype_out="instrument_id",
            start_date=start, end_date=end,
        )
        found = mapping.get("result", {}).get(parent, [])
        row["mapping_count"] = int(len(found))
        row["parent_symbology_verified"] = bool(found) and (
            parent not in mapping.get("not_found", [])
        )
        row["mapping_status"] = str(mapping.get("message", "unknown"))
    except Exception as exc:
        row["symbology_error"] = _safe_exception(exc)
        # Preserve the old field for user-side PowerShell report compatibility.
        row["error"] = row["symbology_error"]

    # Key correction: do NOT gate metadata on symbology.resolve.
    # Databento publishes record counts and USD quotes via free metadata APIs.
    for schema in ("definition", "statistics"):
        if schema not in schemas or not _is_within_schema_range(
            start, ranges=available, schema=schema
        ):
            row["record_counts"][schema] = None
            row["quotes_usd"][schema] = None
            continue
        request = {
            "dataset": DATASET, "start": start, "end": end,
            "symbols": [parent], "schema": schema, "stype_in": "parent",
        }
        try:
            count = int(client.metadata.get_record_count(**request))
            if count < 0:
                raise ValueError("Negative record count")
            row["record_counts"][schema] = count
        except Exception as exc:
            row["record_counts"][schema] = None
            row.setdefault("record_count_errors", {})[schema] = (
                _safe_exception(exc)
            )
        try:
            quote = float(client.metadata.get_cost(**request))
            if not 0 <= quote < float("inf"):
                raise ValueError("Nonfinite or negative USD quote")
            row["quotes_usd"][schema] = quote
        except Exception as exc:
            row["quotes_usd"][schema] = None
            row.setdefault("quote_errors", {})[schema] = _safe_exception(exc)

    values = tuple(row["quotes_usd"].get(k) for k in ("definition", "statistics"))
    if all(isinstance(v, (float, int)) for v in values):
        total = float(sum(values))
        row["total_one_day_quote_usd"] = round(total, 9)
        row["within_quote_ceiling"] = total <= max_quote_usd
    else:
        row["total_one_day_quote_usd"] = None
        row["within_quote_ceiling"] = False
    row["metadata_records_reported"] = any(
        isinstance(x, int) and x > 0
        for x in row["record_counts"].values()
    )
    if row["metadata_records_reported"]:
        row["status"] = "metadata_records_reported_not_final_settlement_proven"
    elif all(
        isinstance(row["record_counts"].get(k), int)
        for k in ("definition", "statistics")
    ):
        row["status"] = "zero_metadata_records_on_anchor_day"
    else:
        row["status"] = "inconclusive_metadata_query"
    return row


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
    parents = tuple(dict.fromkeys(_normalize_parent(p) for p in parents if p.strip()))
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
            row = _probe_parent_day(
                client, parent=parent, start=start, end=end,
                schemas=schemas, available=available,
                max_quote_usd=max_quote_usd,
            )
            row["year"] = year
            report["probes"].append(row)

    # Positive control: the repository's previously verified LO acquisition
    # covers 2026-08-24. If LO counts are positive but symbology mapping is
    # empty, an empty mapping alone is not meaningful evidence of absence.
    control = _probe_parent_day(
        client, parent="LO.OPT", start="2026-08-24",
        end="2026-08-25", schemas=schemas, available=available,
        max_quote_usd=max_quote_usd,
    )
    report["positive_control"] = control
    report["positive_control_expected_source"] = (
        "Existing local Databento LO definition/statistics acquisition "
        "for 2026-08-24, independently documented in "
        "results/analysis/wti_databento_external_q/acquisition_manifest.json."
    )
    report["positive_control_metadata_pass"] = bool(
        control["metadata_records_reported"]
    ) if "metadata_records_reported" in control else False
    report["interpretation"] = (
        "Parent resolution, estimated record counts and USD cost quotes are "
        "metadata-only. A count>0 does not prove a specific instrument, "
        "official final settlement, or continuous historical coverage. "
        "A count=0 on one date does not rule out other dates. "
        "Always inspect the known LO.OPT 2026-08-24 positive control "
        "before concluding anything about AAO availability."
    )
    report["recommendation"] = (
        "Review record counts, parent mappings, positive control and quoted USD amounts; no download performed. "
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
        help=(
            "Databento option parents, e.g. AAO.OPT AO.OPT. Bare CME codes "
            "AAO AO are accepted and normalized to .OPT; coverage is unverified."
        ),
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
