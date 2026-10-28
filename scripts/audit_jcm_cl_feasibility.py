"""Read-only JCM Paper B CL futures/AAO data feasibility inventory.

No API/purchases/provider access, no pricing/hedging, no edits to underlying files.
By default this prints aggregate local-manifest findings. --write-json creates a
new aggregate output; it refuses to overwrite an existing file. This is a
repository data-availability preflight, not a raw-vintage or license audit.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
S = ROOT / "results/analysis/wti_first_nearby"
CL = ROOT / "data/csv/CL"
RAW = ROOT / "data/databento/wti_first_nearby/raw/cl_statistics_2024-01-01_2026-09-23.csv"
AAO = ROOT / "data/databento/wti_aao_bulk/raw"
RATES = ROOT / "data/rates/treasury"
OUTPUT = ROOT / "results/analysis/jcm_cl_data_feasibility/metadata_inventory.json"


def _csv_rows(path: Path) -> tuple[int, str | None, str | None]:
    """Return number of date rows and min/max date, avoiding price reporting."""
    first = None
    last = None
    n = 0
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        if not reader.fieldnames or "Time" not in reader.fieldnames:
            raise ValueError(f"Unexpected CL CSV headers: {path}")
        for row in reader:
            day = row["Time"]
            if not day:
                continue
            if first is None or day < first:
                first = day
            if last is None or day > last:
                last = day
            n += 1
    return n, first, last


def _bool(v: str) -> bool:
    return str(v).strip().lower() in ("1", "true")


def _hash(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as fp:
        for block in iter(lambda: fp.read(4*1024*1024), b""):
            hasher.update(block)
    return hasher.hexdigest()


def inspect(*, verify_large_raw_hash=False) -> dict:
    manifest = json.loads((S/"acquisition_manifest.json").read_text("utf-8"))
    recon = json.loads((S/"reconstruction_report.json").read_text("utf-8"))
    rows = []
    with (S/"first_nearby_reconstruction_raw.csv").open(
        "r", encoding="utf-8", newline=""
    ) as f:
        for row in csv.DictReader(f):
            rows.append(row)
    dates = sorted({r["trade_date"] for r in rows})
    n_usable = sum(_bool(r.get("usable_inference_return","")) for r in rows)
    n_missing = sum(_bool(r.get("missing_settlement","")) for r in rows)
    if len(rows) != recon["comparison"]["first_nearby_prices"]:
        raise AssertionError("First-nearby reconstruction row count mismatch")
    if n_usable != recon["comparison"]["first_nearby_usable_returns"]:
        raise AssertionError("Usable return count mismatch")
    if n_missing != recon["missing_settlement_count"]:
        raise AssertionError("Missing fixings count mismatch")
    individual=[]
    for f in sorted(CL.glob("CL*.csv")):
        if f.name == "contract_expiries.csv":
            continue
        n, low, high = _csv_rows(f)
        individual.append({"contract":f.stem,"rows":n,"first":low,"last":high})
    if not individual:
        raise FileNotFoundError("No CL futures Barchart CSV files")
    aao_defs=sorted(AAO.glob("aao_definition__*.dbn.zst"))
    aao_stats=sorted(AAO.glob("aao_statistics__*.dbn.zst"))
    if RAW.exists():
        with RAW.open("rb") as fh:
            beginning=fh.read(90)
        payload = not beginning.startswith(b"version https://git-lfs.github.com/spec/v1")
        raw_meta={"tracked_path_present":True, "lfs_binary_materialized":payload,
                  "size_bytes":RAW.stat().st_size}
        if verify_large_raw_hash and payload:
            actual=_hash(RAW)
            declared=manifest.get("raw_file",{}).get("sha256")
            raw_meta["sha256_matches_local_acquisition_manifest"]=(actual==declared)
            raw_meta["sha256_local_payload"] = actual
            raw_meta["sha256_acquisition_manifest"] = declared
            raw_meta["integrity_blocked"] = bool(declared and actual != declared)
            # Preserve a machine-readable *failed* integrity result instead of
            # aborting before --write-json can save the discrepancy. Do NOT
            # treat this mismatch as validated source input.
    else:
        raw_meta={"tracked_path_present":False, "lfs_binary_materialized":False}
    treasury=[x.name for x in sorted(RATES.glob("*.csv"))]
    result={
        "purpose":"JCM Paper B independent CL-data availability feasibility",
        "status":"metadata_only_partial_coverage_not_structural_pricing_ready",
        "provider_requests":0,"source_files_modified":False,
        "AAO_option_only_DBNS":{
            "definition_monthly_files":len(aao_defs),
            "statistics_monthly_files":len(aao_stats),
            "does_not_imply_CL_fixings_or_quotes":True
        },
        "Databento_CL_first_nearby":{
            "source_query_start":manifest["history_start_inclusive"],
            "query_end_exclusive":manifest["query_end_exclusive"],
            "inference_end_exclusive":manifest["inference_end_exclusive"],
            "declared_requested_CL_contracts":manifest["contract_count"],
            "declared_raw_source_rows":manifest["raw_file"]["rows"],
            "source_asset":raw_meta,
            "reconstruction_dates":len(dates),
            "reconstruction_first":dates[0] if dates else None,
            "reconstruction_last":dates[-1] if dates else None,
            "usable_inference_returns":n_usable,
            "missing_settlement_dates":recon["missing_settlement_dates"],
            "do_not_interpret_as_complete_future_curve":True,
        },
        "Barchart_CL_forward_strip":{
            "contracts":len(individual),
            "earliest_source_date":min(x["first"] for x in individual),
            "latest_source_date":max(x["last"] for x in individual),
            "by_contract":individual,
            "only_2026_late_summer_quotes":True,
        },
        "Treasury_files":{
            "locally_tracked_csv_files":treasury,
            "par_yield_not_zero_curve":True,
        },
        "gating_issues":[
            "No demonstrated CL fixing path for 2020-2023 AAO months",
            "CL reconstructed daily first-nearby series is not a full futures curve",
            "Only a narrow 2026 Barchart CL futures strip is versioned",
            "Historical per-day futures term structure not proven for the full AAO panel",
            "No independent AAO trades/bid-ask 2020-26 certified",
            "Reference-day versus actually published input-vintage timing unverified",
            "Public data redistribution rights and LFS payload integrity review pending",
            "Treasury par yields are not independently bootstrapped OIS/zero rates",
        ],
    }
    return result


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--verify-large-raw-sha256",action="store_true",
                        help="Optional local 311MB file hash check; no network")
    parser.add_argument("--write-json",action="store_true")
    args=parser.parse_args()
    answer=inspect(verify_large_raw_hash=args.verify_large_raw_sha256)
    print(json.dumps(answer,indent=2))
    if args.write_json:
        if OUTPUT.exists():
            raise FileExistsError(f"Preserving prior report: {OUTPUT}")
        OUTPUT.parent.mkdir(parents=True,exist_ok=True)
        OUTPUT.write_text(json.dumps(answer,indent=2)+"\n",encoding="utf-8")
        print(f"Saved: {OUTPUT}")


if __name__=="__main__":
    main()
