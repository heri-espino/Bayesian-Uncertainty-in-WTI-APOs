"""Quote-first, resumable AAO historical downloader.

Manual only. Quote mode never downloads. Download mode requires explicit
--confirm-budget-usd matching --max-budget-usd (at most 40 USD).
Provider charges actual transferred bytes; metadata quotes are estimates.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from datetime import date
from pathlib import Path
from typing import Any

from experiments.wti_databento_aao_feasibility import DATASET, ROOT, _historical_client

PARENT = "AAO.OPT"
SCHEMAS = ("definition", "statistics")
DATA_DIR = ROOT / "data" / "databento" / "wti_aao_bulk" / "raw"
REPORT_DIR = ROOT / "results" / "analysis" / "wti_aao_history_feasibility" / "bulk"


def monthly_windows(start: str, end: str) -> list[tuple[str, str]]:
    left, right = date.fromisoformat(start), date.fromisoformat(end)
    if left >= right:
        raise ValueError("start must precede end")
    result = []
    while left < right:
        following = (date(left.year + 1, 1, 1) if left.month == 12
                     else date(left.year, left.month + 1, 1))
        right_bound = min(right, following)
        result.append((left.isoformat(), right_bound.isoformat()))
        left = right_bound
    return result


def _query(schema: str, start: str, end: str) -> dict[str, Any]:
    return dict(dataset=DATASET, schema=schema, start=start, end=end,
                symbols=[PARENT], stype_in="parent")


def _sha(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _save(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    pending = path.with_suffix(".tmp")
    pending.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n",
                       encoding="utf-8")
    pending.replace(path)


def quote_plan(client: Any, *, start: str, end: str) -> dict[str, Any]:
    """Metadata requests only; count>0 is not proof of final APO settlements."""
    if DATASET not in client.metadata.list_datasets():
        raise RuntimeError("Databento GLBX.MDP3 not accessible")
    if not set(SCHEMAS).issubset(
        set(client.metadata.list_schemas(dataset=DATASET))
    ):
        raise RuntimeError("definition/statistics schemas unavailable")
    rows = []
    eligible_months = 0
    for left, right in monthly_windows(start, end):
        pair = []
        for schema in SCHEMAS:
            row = dict(schema=schema, start=left, end=right,
                       id=f"{schema}__{left}__{right}",
                       count=None, quote_usd=None, status="error")
            query = _query(schema, left, right)
            try:
                row["count"] = int(client.metadata.get_record_count(**query))
                row["quote_usd"] = float(client.metadata.get_cost(**query))
                if row["count"] < 0 or not (0 <= row["quote_usd"] < float("inf")):
                    raise ValueError("Invalid count or quote")
                row["status"] = "positive" if row["count"] > 0 else "empty"
            except Exception as exc:
                secret = os.environ.get("DATABENTO_API_KEY", "")
                msg = f"{type(exc).__name__}: {exc}"
                row["error"] = (msg.replace(secret, "[REDACTED]") if secret
                                else msg)[:400]
                row["quote_usd"] = None
            pair.append(row)
        eligible = all(row["status"] == "positive" for row in pair)
        eligible_months += int(eligible)
        for row in pair:
            row["eligible"] = eligible
        rows.extend(pair)
    return dict(
        dataset=DATASET, parent=PARENT, start=start, end=end,
        requests=rows, eligible_months=eligible_months,
        total_months=len(monthly_windows(start, end)),
        eligible_quote_usd=round(sum(
            row["quote_usd"] for row in rows if row["eligible"]
        ), 8),
        note="Metadata counts and quotes do not verify actual final settlements",
    )


def acquire(
    client: Any, *, plan: dict[str, Any], data_dir: Path,
    report_dir: Path, max_budget_usd: float, safety_fraction: float = 0.8
) -> dict[str, Any]:
    """Budget-check ALL pending chunks before the first billable request."""
    if not (0 < max_budget_usd <= 40 and 0 < safety_fraction <= 0.8):
        raise ValueError("Unsafe budget or safety fraction")
    if plan["eligible_months"] != plan["total_months"]:
        raise RuntimeError(
            "Refusing incomplete AAO recovery plan: require all 81 months "
            "to have BOTH positive definition and statistics quotes; "
            "no new purchases made"
        )
    data_dir.mkdir(parents=True, exist_ok=True)
    report_dir.mkdir(parents=True, exist_ok=True)
    ledger_path = report_dir / "bulk_acquisition_manifest.json"
    if ledger_path.exists():
        ledger = json.loads(ledger_path.read_text(encoding="utf-8"))
        if any(ledger.get(k) != plan.get(k) for k in
               ("dataset", "parent", "start", "end")):
            raise RuntimeError("Existing ledger refers to a different request")
        if ledger.get("max_budget_usd") != max_budget_usd:
            raise RuntimeError("Existing ledger has a different budget")
    else:
        ledger = dict(
            dataset=plan["dataset"], parent=plan["parent"],
            start=plan["start"], end=plan["end"],
            max_budget_usd=max_budget_usd,
            note="Quoted estimates, not final charges", completed={},
        )
    pending = []
    for row in plan["requests"]:
        if not row["eligible"]:
            continue
        target = data_dir / f"aao_{row['id']}.dbn.zst"
        partial = target.with_name(
            target.name.replace(".dbn.zst", ".partial.dbn.zst")
        )
        if row["id"] in ledger["completed"]:
            if not target.is_file() or (
                _sha(target) != ledger["completed"][row["id"]]["sha256"]
            ):
                raise RuntimeError(f"Recorded file changed: {target}")
            continue
        if target.exists() or partial.exists():
            raise RuntimeError(f"Untracked or partial file: {target}")
        pending.append((row, target, partial))
    used = sum(item["quote_usd"] for item in ledger["completed"].values())
    upcoming = sum(row["quote_usd"] for row, _, _ in pending)
    ceiling = max_budget_usd * safety_fraction
    if used + upcoming > ceiling + 1e-9:
        raise RuntimeError(
            f"Preflight quote USD {used+upcoming:.4f} exceeds safety "
            f"ceiling USD {ceiling:.2f}; no new purchases made"
        )
    _save(ledger_path, ledger)
    for row, target, partial in pending:
        client.timeseries.get_range(
            **_query(row["schema"], row["start"], row["end"]),
            path=partial,
        )
        if not partial.is_file() or partial.stat().st_size == 0:
            raise RuntimeError(
                f"Missing/empty partial file: {partial}; inspect manually"
            )
        partial.replace(target)
        ledger["completed"][row["id"]] = dict(
            quote_usd=row["quote_usd"], count=row["count"],
            schema=row["schema"], start=row["start"], end=row["end"],
            file=target.name, size_bytes=target.stat().st_size,
            sha256=_sha(target),
        )
        _save(ledger_path, ledger)
    ledger["completed_all_eligible"] = True
    ledger["total_quoted_usd"] = round(sum(
        item["quote_usd"] for item in ledger["completed"].values()
    ), 8)
    _save(ledger_path, ledger)
    return ledger


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mode", choices=("quote", "download"), default="quote")
    parser.add_argument("--start", default="2020-01-01")
    parser.add_argument("--end", default="2026-10-01")
    parser.add_argument("--max-budget-usd", type=float, default=40.0)
    parser.add_argument("--confirm-budget-usd", type=float)
    parser.add_argument("--data-dir", type=Path, default=DATA_DIR)
    parser.add_argument("--report-dir", type=Path, default=REPORT_DIR)
    args = parser.parse_args()
    if not 0 < args.max_budget_usd <= 40:
        parser.error("max-budget-usd must be between 0 and 40")
    if (args.mode == "download" and
            args.confirm_budget_usd != args.max_budget_usd):
        parser.error(
            "Download requires --confirm-budget-usd matching max-budget-usd"
        )
    plan = quote_plan(_historical_client(), start=args.start, end=args.end)
    plan["budget_usd"] = args.max_budget_usd
    plan["safety_ceiling_usd"] = round(args.max_budget_usd * 0.8, 2)
    report_path = args.report_dir / "bulk_quote_plan.json"
    _save(report_path, plan)
    print(json.dumps(dict(
        mode=args.mode, eligible_months=plan["eligible_months"],
        total_months=plan["total_months"],
        estimated_cost_usd=plan["eligible_quote_usd"],
        safety_ceiling_usd=plan["safety_ceiling_usd"],
        plan_path=str(report_path),
    ), indent=2))
    if args.mode == "download":
        result = acquire(
            _historical_client(), plan=plan, data_dir=args.data_dir,
            report_dir=args.report_dir, max_budget_usd=args.max_budget_usd,
        )
        print(json.dumps(dict(
            downloaded_chunks=len(result["completed"]),
            quoted_usd=result["total_quoted_usd"],
            manifest=str(args.report_dir / "bulk_acquisition_manifest.json"),
        ), indent=2))


if __name__ == "__main__":
    main()
