"""Acquire official CL futures statistics for historical first-nearby reconstruction.

The request is deliberately cost-capped and reads the Databento credential only from
DATABENTO_API_KEY. Raw vendor records remain local under a gitignored directory.

PowerShell examples:

    python -m experiments.wti_databento_first_nearby --mode quote
    python -m experiments.wti_databento_first_nearby --mode download
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
from typing import Any

import pandas as pd

from bayesian_asian_options.wti_yahoo_futures import cl_contract_strip

ROOT = Path(__file__).resolve().parents[1]
DATASET = "GLBX.MDP3"
DEFAULT_HISTORY_START = "2024-01-01"
DEFAULT_INFERENCE_END = "2026-09-11"
DEFAULT_QUERY_END = "2026-09-24"  # end-exclusive; includes CLV26 final settlement/roll boundary
DEFAULT_MAX_COST_USD = 5.0

_MONTH_CODES = set("FGHJKMNQUVXZ")


def _raw_cl_symbol(contract: str) -> str:
    """Convert canonical CLG24-style symbols to Databento raw CLG4 form."""
    value = str(contract).strip().upper()
    if not value.startswith("CL") or len(value) < 4:
        raise ValueError(f"Unrecognized CL contract symbol: {contract}")
    month = value[2]
    year = value[3:]
    if month not in _MONTH_CODES or not year.isdigit():
        raise ValueError(f"Unrecognized CL contract symbol: {contract}")
    return f"CL{month}{year[-1]}"

def requested_contracts(start: str, inference_end: str) -> list[str]:
    """Return monthly CL contracts needed for the reconstruction window."""
    return cl_contract_strip(start, inference_end, lead_months=1)

def _require_api_key() -> None:
    if not os.environ.get("DATABENTO_API_KEY"):
        raise RuntimeError(
            "DATABENTO_API_KEY is not set. Set it in the local shell; never commit it."
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

def _query(symbols: list[str], start: str, end: str) -> dict[str, Any]:
    return {
        "dataset": DATASET,
        "schema": "statistics",
        "symbols": symbols,
        "stype_in": "raw_symbol",
        "start": start,
        "end": end,
    }

def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()

def _load_csv(path: Path) -> pd.DataFrame:
    return pd.read_csv(path, index_col=0, low_memory=False)

def _cache_covers(path: Path, symbols: list[str]) -> bool:
    if not path.exists():
        return False
    frame = _load_csv(path)
    symbol_col = next(
        (candidate for candidate in ("symbol", "raw_symbol") if candidate in frame.columns),
        None,
    )
    if symbol_col is None:
        return False
    available = set(frame[symbol_col].dropna().astype(str).str.strip())
    return set(symbols).issubset(available)

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mode", choices=("quote", "download"), default="quote")
    parser.add_argument("--history-start", default=DEFAULT_HISTORY_START)
    parser.add_argument("--inference-end", default=DEFAULT_INFERENCE_END)
    parser.add_argument("--query-end", default=DEFAULT_QUERY_END)
    parser.add_argument("--max-cost-usd", type=float, default=DEFAULT_MAX_COST_USD)
    parser.add_argument(
        "--data-dir",
        type=Path,
        default=ROOT / "data" / "databento" / "wti_first_nearby" / "raw",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=ROOT / "results" / "analysis" / "wti_first_nearby",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Allow replacing a local raw statistics file and risking a repeated billable request.",
    )
    return parser.parse_args()

def main() -> None:
    args = parse_args()
    if args.max_cost_usd <= 0:
        raise ValueError("--max-cost-usd must be positive")
    if pd.Timestamp(args.inference_end) <= pd.Timestamp(args.history_start):
        raise ValueError("--inference-end must be after --history-start")
    if pd.Timestamp(args.query_end) < pd.Timestamp(args.inference_end):
        raise ValueError("--query-end must be on or after --inference-end")

    contracts = requested_contracts(args.history_start, args.inference_end)
    raw_symbols = [_raw_cl_symbol(contract) for contract in contracts]
    query = _query(raw_symbols, args.history_start, args.query_end)

    client = _client()
    quote = float(client.metadata.get_cost(**query))

    args.data_dir.mkdir(parents=True, exist_ok=True)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    raw_path = args.data_dir / f"cl_statistics_{args.history_start}_{args.query_end}.csv"
    symbol_map_path = args.output_dir / "contract_symbol_map.csv"
    manifest_path = args.output_dir / "acquisition_manifest.json"

    mapping = pd.DataFrame({"contract": contracts, "raw_symbol": raw_symbols})
    mapping.to_csv(symbol_map_path, index=False)

    already_local = not args.force and _cache_covers(raw_path, raw_symbols)
    new_cost = 0.0 if already_local else quote
    manifest: dict[str, Any] = {
        "dataset": DATASET,
        "mode": args.mode,
        "history_start_inclusive": args.history_start,
        "inference_end_exclusive": args.inference_end,
        "query_end_exclusive": args.query_end,
        "hard_cost_cap_usd": args.max_cost_usd,
        "quoted_statistics_cost_usd": quote,
        "new_download_estimate_usd": new_cost,
        "contracts": contracts,
        "raw_symbols": raw_symbols,
        "contract_count": len(contracts),
        "raw_data_committed": False,
        "notes": [
            "API key is read only from DATABENTO_API_KEY and is never recorded.",
            "Raw Databento statistics are proprietary local inputs and are gitignored.",
            "The query extends beyond the inference end only to identify the termination date of the active front contract; future settlements are not used as P-measure returns.",
            "Only official final end-of-day settlement statistics are used by the reconstruction stage.",
        ],
    }

    if args.mode == "quote":
        manifest["next_action"] = (
            "Run --mode download only if new_download_estimate_usd is acceptable."
        )
        manifest_path.write_text(
            json.dumps(manifest, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        print(json.dumps(manifest, indent=2, sort_keys=True))
        return

    if new_cost > args.max_cost_usd:
        raise RuntimeError(
            f"Projected cost ${new_cost:.4f} exceeds hard cap ${args.max_cost_usd:.2f}; nothing downloaded."
        )

    if already_local:
        manifest["reused_local"] = str(raw_path.relative_to(ROOT))
    else:
        frame = client.timeseries.get_range(**query).to_df()
        frame.to_csv(raw_path, index=True)
        manifest["downloaded"] = str(raw_path.relative_to(ROOT))

    frame = _load_csv(raw_path)
    manifest["raw_file"] = {
        "path": str(raw_path.relative_to(ROOT)),
        "sha256": _sha256(raw_path),
        "rows": int(len(frame)),
    }
    manifest["completed"] = True
    manifest["next_action"] = (
        "Run python -m experiments.wti_first_nearby_reconstruction"
    )
    manifest_path.write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(manifest, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
