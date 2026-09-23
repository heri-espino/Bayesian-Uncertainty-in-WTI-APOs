"""Acquire a minimal Databento WTI vanilla-option panel for external-Q validation.

The command is deliberately fail-closed on cost. It reads the API key only from the
``DATABENTO_API_KEY`` environment variable and never writes it to disk.

Modes
-----
quote
    Free metadata quote only. If a local definition snapshot already exists, also quote
    the exact statistics request. No billable time-series data are downloaded.
discover
    Quote and, if below the hard cost cap, download one daily ``LO.OPT`` definition
    snapshot. Filter to the requested CL underlyings/strike range and quote the exact
    option/futures ``statistics`` request. Stop before downloading statistics.
download
    Perform ``discover`` and then download only the selected option/futures statistics
    when the estimated new cost remains below the hard cap.

Examples
--------
PowerShell::

    $env:DATABENTO_API_KEY = "<your key>"
    python -m experiments.wti_databento_external_q --mode quote
    python -m experiments.wti_databento_external_q --mode discover
    python -m experiments.wti_databento_external_q --mode download
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
from pathlib import Path
from typing import Any

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATASET = "GLBX.MDP3"
OPTION_PARENT = "LO.OPT"
DEFAULT_START = "2026-08-24"
DEFAULT_END = "2026-09-11"  # exclusive
DEFAULT_DEFINITION_DATE = "2026-08-24"
DEFAULT_UNDERLYINGS = ("CLX26", "CLZ26")
DEFAULT_MAX_COST_USD = 5.0

_CL_LONG_YEAR_RE = re.compile(
    r"^CL(?P<month>[FGHJKMNQUVXZ])(?P<yy>\d{2}|20\d{2})$",
    re.IGNORECASE,
)


def _raw_cl_symbol(symbol: str) -> str:
    """Convert a Barchart-style CLX26 symbol to CME/Databento raw CLX6 form."""
    value = symbol.strip().upper()
    match = _CL_LONG_YEAR_RE.fullmatch(value)
    if match:
        return f"CL{match.group('month').upper()}{match.group('yy')[-1]}"
    return value


def _require_api_key() -> None:
    if not os.environ.get("DATABENTO_API_KEY"):
        raise RuntimeError(
            "DATABENTO_API_KEY is not set. Set it in the local shell; never commit the key."
        )


def _client() -> Any:
    _require_api_key()
    try:
        import databento as db
    except ImportError as exc:
        raise RuntimeError(
            "Databento client is not installed. Run: python -m pip install -e '.[market]'"
        ) from exc
    return db.Historical()


def _definition_query(definition_date: str) -> dict[str, Any]:
    start = pd.Timestamp(definition_date)
    end = start + pd.Timedelta(days=1)
    return {
        "dataset": DATASET,
        "schema": "definition",
        "symbols": OPTION_PARENT,
        "stype_in": "parent",
        "start": start.date().isoformat(),
        "end": end.date().isoformat(),
    }


def _statistics_query(
    *, symbols: list[str], start: str, end: str
) -> dict[str, Any]:
    return {
        "dataset": DATASET,
        "schema": "statistics",
        "symbols": symbols,
        "stype_in": "raw_symbol",
        "start": start,
        "end": end,
    }


def _instrument_side(value: object) -> str | None:
    text = str(value).strip().upper()
    if text in {"C", "CALL", "INSTRUMENTCLASS.CALL"}:
        return "call"
    if text in {"P", "PUT", "INSTRUMENTCLASS.PUT"}:
        return "put"
    return None


def select_option_definitions(
    definitions: pd.DataFrame,
    *,
    underlyings: tuple[str, ...],
    strike_min: float,
    strike_max: float,
) -> pd.DataFrame:
    """Select outright LO calls/puts on requested CL futures and strikes."""
    required = {"raw_symbol", "underlying", "strike_price", "instrument_class"}
    missing = required.difference(definitions.columns)
    if missing:
        raise ValueError(f"Definition data missing columns: {sorted(missing)}")

    wanted = {_raw_cl_symbol(x) for x in underlyings}
    frame = definitions.copy()
    frame["underlying"] = frame["underlying"].astype(str).str.strip().str.upper()
    frame["strike_price"] = pd.to_numeric(frame["strike_price"], errors="coerce")
    frame["option_type"] = frame["instrument_class"].map(_instrument_side)

    frame = frame[
        frame["underlying"].isin(wanted)
        & frame["option_type"].notna()
        & frame["strike_price"].between(strike_min, strike_max, inclusive="both")
    ].copy()

    if frame.empty:
        available = sorted(
            x for x in definitions["underlying"].dropna().astype(str).unique().tolist() if x
        )
        sample = available[:30]
        raise RuntimeError(
            "No LO option definitions matched the requested CL underlyings/strikes. "
            f"Requested={sorted(wanted)}; sample available underlyings={sample}"
        )

    sort_cols = [c for c in ("ts_event", "ts_recv") if c in frame.columns]
    if sort_cols:
        frame = frame.sort_values(sort_cols)
    frame = frame.drop_duplicates(subset=["raw_symbol"], keep="last")
    cols = [
        c
        for c in (
            "raw_symbol",
            "instrument_id",
            "underlying",
            "underlying_id",
            "strike_price",
            "expiration",
            "instrument_class",
            "option_type",
            "asset",
            "exchange",
        )
        if c in frame.columns
    ]
    return frame[cols].sort_values(
        ["underlying", "strike_price", "option_type", "raw_symbol"]
    ).reset_index(drop=True)


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _write_csv(frame: pd.DataFrame, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    frame.to_csv(path, index=True)


def _load_csv(path: Path) -> pd.DataFrame:
    return pd.read_csv(path, index_col=0)


def _quote(client: Any, query: dict[str, Any]) -> float:
    return float(client.metadata.get_cost(**query))


def _fetch_df(client: Any, query: dict[str, Any]) -> pd.DataFrame:
    return client.timeseries.get_range(**query).to_df()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mode", choices=("quote", "discover", "download"), default="quote")
    parser.add_argument("--start", default=DEFAULT_START)
    parser.add_argument("--end", default=DEFAULT_END)
    parser.add_argument("--definition-date", default=DEFAULT_DEFINITION_DATE)
    parser.add_argument("--underlyings", nargs="+", default=list(DEFAULT_UNDERLYINGS))
    parser.add_argument("--strike-min", type=float, default=85.0)
    parser.add_argument("--strike-max", type=float, default=94.5)
    parser.add_argument("--max-cost-usd", type=float, default=DEFAULT_MAX_COST_USD)
    parser.add_argument(
        "--data-dir",
        type=Path,
        default=ROOT / "data" / "databento" / "wti_external_q" / "raw",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=ROOT / "results" / "analysis" / "wti_databento_external_q",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Allow replacing local raw files, which can cause a repeated billable request.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.max_cost_usd <= 0:
        raise ValueError("--max-cost-usd must be positive.")
    if args.strike_min > args.strike_max:
        raise ValueError("--strike-min cannot exceed --strike-max.")

    client = _client()
    args.data_dir.mkdir(parents=True, exist_ok=True)
    args.output_dir.mkdir(parents=True, exist_ok=True)

    raw_underlyings = tuple(_raw_cl_symbol(x) for x in args.underlyings)
    def_path = args.data_dir / f"lo_definitions_{args.definition_date}.csv"
    selected_path = args.data_dir / f"lo_selected_{args.definition_date}.csv"
    option_stats_path = args.data_dir / f"lo_statistics_{args.start}_{args.end}.csv"
    futures_stats_path = args.data_dir / f"cl_statistics_{args.start}_{args.end}.csv"
    manifest_path = args.output_dir / "acquisition_manifest.json"

    definition_query = _definition_query(args.definition_date)
    definition_quote = _quote(client, definition_query)

    manifest: dict[str, Any] = {
        "dataset": DATASET,
        "option_parent": OPTION_PARENT,
        "mode": args.mode,
        "date_window": {"start_inclusive": args.start, "end_exclusive": args.end},
        "definition_date": args.definition_date,
        "requested_underlyings": list(args.underlyings),
        "raw_underlyings": list(raw_underlyings),
        "strike_range": [args.strike_min, args.strike_max],
        "hard_cost_cap_usd": args.max_cost_usd,
        "quotes_usd": {"definition": definition_quote},
        "new_download_estimate_usd": 0.0,
        "downloaded": [],
        "reused_local": [],
        "selected_option_count": None,
        "selected_call_count": None,
        "selected_put_count": None,
        "files": {},
        "notes": [
            "API key is read only from DATABENTO_API_KEY and is not recorded.",
            "Raw Databento files are local/proprietary inputs and are gitignored.",
            "statistics stat_type=3 is settlement; stat_type=14 is settlement-associated IV when published.",
        ],
    }

    if args.mode == "quote" and not def_path.exists():
        manifest["new_download_estimate_usd"] = definition_quote
        manifest["next_action"] = (
            "Run --mode discover to buy only the quoted definition snapshot, "
            "filter exact instruments, and quote statistics."
        )
        manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n")
        print(json.dumps(manifest, indent=2, sort_keys=True))
        return

    if def_path.exists() and not args.force:
        definitions = _load_csv(def_path)
        manifest["reused_local"].append(str(def_path.relative_to(ROOT)))
    else:
        if definition_quote > args.max_cost_usd:
            raise RuntimeError(
                f"Definition quote ${definition_quote:.4f} exceeds hard cap "
                f"${args.max_cost_usd:.2f}; nothing downloaded."
            )
        definitions = _fetch_df(client, definition_query)
        _write_csv(definitions, def_path)
        manifest["downloaded"].append(str(def_path.relative_to(ROOT)))
        manifest["new_download_estimate_usd"] += definition_quote

    selected = select_option_definitions(
        definitions,
        underlyings=raw_underlyings,
        strike_min=args.strike_min,
        strike_max=args.strike_max,
    )
    _write_csv(selected, selected_path)

    option_symbols = selected["raw_symbol"].astype(str).tolist()
    option_query = _statistics_query(symbols=option_symbols, start=args.start, end=args.end)
    futures_query = _statistics_query(
        symbols=list(raw_underlyings), start=args.start, end=args.end
    )
    option_quote = _quote(client, option_query)
    futures_quote = _quote(client, futures_query)
    manifest["quotes_usd"]["option_statistics"] = option_quote
    manifest["quotes_usd"]["futures_statistics"] = futures_quote
    manifest["selected_option_count"] = int(len(selected))
    manifest["selected_call_count"] = int(selected["option_type"].eq("call").sum())
    manifest["selected_put_count"] = int(selected["option_type"].eq("put").sum())

    option_already_local = option_stats_path.exists() and not args.force
    futures_already_local = futures_stats_path.exists() and not args.force
    additional_quote = (0.0 if option_already_local else option_quote) + (
        0.0 if futures_already_local else futures_quote
    )
    projected_new_cost = float(manifest["new_download_estimate_usd"]) + additional_quote
    manifest["new_download_estimate_usd"] = projected_new_cost

    if args.mode in {"quote", "discover"}:
        manifest["next_action"] = (
            "Run --mode download only if the quoted new-download estimate is acceptable."
        )
        manifest["files"][str(def_path.relative_to(ROOT))] = {
            "sha256": _sha256(def_path),
            "rows": int(len(definitions)),
        }
        manifest["files"][str(selected_path.relative_to(ROOT))] = {
            "sha256": _sha256(selected_path),
            "rows": int(len(selected)),
        }
        manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n")
        print(json.dumps(manifest, indent=2, sort_keys=True))
        return

    if projected_new_cost > args.max_cost_usd:
        raise RuntimeError(
            f"Projected new cost ${projected_new_cost:.4f} exceeds hard cap "
            f"${args.max_cost_usd:.2f}; statistics not downloaded."
        )

    if option_already_local:
        manifest["reused_local"].append(str(option_stats_path.relative_to(ROOT)))
    else:
        option_stats = _fetch_df(client, option_query)
        _write_csv(option_stats, option_stats_path)
        manifest["downloaded"].append(str(option_stats_path.relative_to(ROOT)))

    if futures_already_local:
        manifest["reused_local"].append(str(futures_stats_path.relative_to(ROOT)))
    else:
        futures_stats = _fetch_df(client, futures_query)
        _write_csv(futures_stats, futures_stats_path)
        manifest["downloaded"].append(str(futures_stats_path.relative_to(ROOT)))

    for path in (def_path, selected_path, option_stats_path, futures_stats_path):
        if path.exists():
            frame = _load_csv(path)
            manifest["files"][str(path.relative_to(ROOT))] = {
                "sha256": _sha256(path),
                "rows": int(len(frame)),
            }

    manifest["completed"] = True
    manifest["next_action"] = (
        "Inspect stat_type=3 settlements and stat_type=14 IV availability before pricing."
    )
    manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n")
    print(json.dumps(manifest, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
