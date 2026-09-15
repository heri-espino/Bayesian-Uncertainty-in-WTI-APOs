"""Build a tidy empirical WTI Average Price Option panel from repository CSVs.

The current repository stores per-contract histories below ``data/csv/<expiry>``.
This script recursively discovers only filenames that decode as JAO contracts,
so aggregate files such as ``option_series_properties.csv`` are ignored.

Examples
--------
python -m experiments.build_wti_apo_panel
python -m experiments.build_wti_apo_panel --input-dir data/csv --output-dir results/wti_apo
"""

from __future__ import annotations

import argparse
from pathlib import Path

from src.barchart_apo import (
    build_apo_panel,
    discover_barchart_histories,
    rank_representative_contracts,
    summarize_contracts,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input-dir", type=Path, default=Path("data/csv"))
    parser.add_argument("--output-dir", type=Path, default=Path("results/wti_apo"))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    paths = discover_barchart_histories(args.input_dir)
    if not paths:
        raise SystemExit(f"No individual JAO history CSVs found under {args.input_dir}")

    panel = build_apo_panel(paths, deduplicate_contracts=True)
    quality = summarize_contracts(panel)
    ranking = rank_representative_contracts(panel)

    args.output_dir.mkdir(parents=True, exist_ok=True)
    panel.to_csv(args.output_dir / "apo_panel_raw.csv", index=False)
    quality.to_csv(args.output_dir / "apo_contract_quality.csv", index=False)
    ranking.to_csv(args.output_dir / "apo_representative_ranking_pre_moneyness.csv", index=False)

    maturity = (
        quality.groupby(["expiry_month", "option_type"], as_index=False)
        .agg(
            contracts=("contract_id", "nunique"),
            median_sessions=("sessions", "median"),
            median_open_interest=("median_open_interest", "median"),
            mean_nonzero_volume_share=("nonzero_volume_share", "mean"),
            folder_mismatches=("folder_mismatch", "sum"),
        )
        .sort_values(["expiry_month", "option_type"])
    )
    maturity.to_csv(args.output_dir / "apo_maturity_summary.csv", index=False)

    mismatches = quality.loc[quality["folder_mismatch"]].copy()
    mismatches.to_csv(args.output_dir / "apo_folder_mismatches.csv", index=False)

    print(f"discovered files: {len(paths)}")
    print(f"unique contracts after de-duplication: {len(quality)}")
    print(f"panel rows: {len(panel)}")
    print(f"folder/expiry mismatches: {len(mismatches)}")
    print(maturity.to_string(index=False))


if __name__ == "__main__":
    main()
