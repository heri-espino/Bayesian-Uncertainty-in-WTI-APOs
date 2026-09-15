"""Build and rank a research panel from Barchart WTI APO CSV downloads.

Usage
-----
python experiments/build_wti_apo_panel.py \
    --input-dir data/raw/barchart_apo \
    --output data/processed/wti_apo_panel.csv \
    --ranking results/wti_apo_representative_contracts.csv

Raw Barchart files should normally remain local because redistribution rights
may differ from research-use rights. Commit code and derived summaries only
when permitted by the applicable license.
"""

from __future__ import annotations

import argparse
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.barchart_apo import build_apo_panel, rank_representative_contracts

# Exchange expiry dates for the deliberately spaced empirical maturity buckets.
# CME Rule 341 states expiration is the last business day of the calendar month;
# exact dates are listed explicitly so holidays are never guessed in code.
EXPIRY_DATES = {
    "2026-09": "2026-09-30",
    "2026-10": "2026-10-30",
    "2026-11": "2026-11-30",
    "2027-03": "2027-03-31",
    "2027-09": "2027-09-30",
    "2028-03": "2028-03-31",
    "2028-09": "2028-09-29",
    "2029-06": "2029-06-29",
}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-dir", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--ranking", required=True, type=Path)
    args = parser.parse_args()

    paths = sorted(args.input_dir.glob("*.csv"))
    if not paths:
        raise SystemExit(f"No CSV files found in {args.input_dir}")

    panel = build_apo_panel(paths, expiry_dates=EXPIRY_DATES)
    ranking = rank_representative_contracts(panel)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.ranking.parent.mkdir(parents=True, exist_ok=True)
    panel.to_csv(args.output, index=False)
    ranking.to_csv(args.ranking, index=False)

    summary = (
        panel.groupby(["expiry_month", "option_type"])
        .agg(
            contracts=("strike", "nunique"),
            observations=("trade_date", "size"),
            first_date=("trade_date", "min"),
            last_date=("trade_date", "max"),
        )
        .reset_index()
    )
    print(summary.to_string(index=False))


if __name__ == "__main__":
    main()
