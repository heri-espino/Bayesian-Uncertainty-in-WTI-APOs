"""Audit downloaded vanilla WTI option histories for external-Q validation.

This is a lightweight data-readiness check. It does not estimate implied volatility or price APOs.
It parses Barchart-style CSV filenames such as
`clx6_850c_price-history-09-23-2026.csv`, summarizes strike/type coverage, and checks whether
the downloaded option histories overlap the target APO valuation window required for a strict
lagged experiment.

Example
-------
python -m experiments.wti_vanilla_cl_audit \
    --input-dir data/csv/CLX26 \
    --underlying CLX26 \
    --option-expiry 2026-10-15 \
    --target-start 2026-08-25 \
    --target-end 2026-09-10
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]

_FILENAME_RE = re.compile(
    r"cl(?P<month>[a-z])(?P<year>\d)_(?P<strike>\d+)(?P<type>[cp])_price-history",
    re.IGNORECASE,
)


def _parse_contract(path: Path) -> dict[str, object]:
    match = _FILENAME_RE.search(path.name)
    if match is None:
        raise ValueError(f"Unrecognized vanilla-option filename: {path.name}")
    return {
        "strike": float(match.group("strike")) / 10.0,
        "option_type": "call" if match.group("type").lower() == "c" else "put",
    }


def audit(
    *,
    input_dir: Path,
    underlying: str,
    option_expiry: str,
    target_start: str,
    target_end: str,
) -> tuple[pd.DataFrame, dict[str, object]]:
    files = sorted(input_dir.glob("*.csv"))
    if not files:
        raise FileNotFoundError(f"No CSV files found under {input_dir}")

    rows: list[dict[str, object]] = []
    for path in files:
        contract = _parse_contract(path)
        frame = pd.read_csv(path)
        frame.columns = [str(c).lstrip("\ufeff") for c in frame.columns]
        if "Time" not in frame.columns:
            raise ValueError(f"{path}: missing Time column")
        dates = pd.to_datetime(frame["Time"], errors="coerce").dropna().sort_values()
        if dates.empty:
            first_date = last_date = None
            target_rows = 0
        else:
            first_date = dates.iloc[0].date().isoformat()
            last_date = dates.iloc[-1].date().isoformat()
            target_rows = int(
                ((dates >= pd.Timestamp(target_start)) & (dates <= pd.Timestamp(target_end))).sum()
            )
        rows.append(
            {
                "file": path.name,
                "underlying": underlying,
                "option_expiry": option_expiry,
                **contract,
                "rows": int(len(frame)),
                "first_date": first_date,
                "last_date": last_date,
                "target_window_rows": target_rows,
            }
        )

    detail = pd.DataFrame(rows).sort_values(["strike", "option_type"]).reset_index(drop=True)
    strikes = sorted(detail["strike"].unique().tolist())
    first_dates = pd.to_datetime(detail["first_date"], errors="coerce")
    last_dates = pd.to_datetime(detail["last_date"], errors="coerce")
    target_files = int((detail["target_window_rows"] > 0).sum())

    summary: dict[str, object] = {
        "underlying": underlying,
        "option_expiry": option_expiry,
        "file_count": int(len(detail)),
        "strike_count": int(len(strikes)),
        "min_strike": float(min(strikes)),
        "max_strike": float(max(strikes)),
        "all_strikes_have_call_and_put": bool(
            all(
                {"call", "put"}
                <= set(detail.loc[detail["strike"].eq(strike), "option_type"])
                for strike in strikes
            )
        ),
        "earliest_observation": (
            first_dates.min().date().isoformat() if first_dates.notna().any() else None
        ),
        "latest_observation": (
            last_dates.max().date().isoformat() if last_dates.notna().any() else None
        ),
        "target_start": target_start,
        "target_end": target_end,
        "files_with_target_window_observations": target_files,
        "strict_forward_ready": bool(target_files >= 6),
    }
    return detail, summary


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input-dir", type=Path, default=ROOT / "data" / "csv" / "CLX26")
    parser.add_argument("--underlying", default="CLX26")
    parser.add_argument("--option-expiry", default="2026-10-15")
    parser.add_argument("--target-start", default="2026-08-25")
    parser.add_argument("--target-end", default="2026-09-10")
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=ROOT / "results" / "analysis" / "wti_vanilla_cl_audit",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    detail, summary = audit(
        input_dir=args.input_dir,
        underlying=str(args.underlying),
        option_expiry=str(args.option_expiry),
        target_start=str(args.target_start),
        target_end=str(args.target_end),
    )
    args.output_dir.mkdir(parents=True, exist_ok=True)
    detail.to_csv(args.output_dir / "vanilla_history_audit.csv", index=False)
    (args.output_dir / "vanilla_history_audit.json").write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
