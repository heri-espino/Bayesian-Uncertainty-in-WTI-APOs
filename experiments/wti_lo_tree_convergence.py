"""CRR tree-step convergence audit for external vanilla-WTI implied volatility.

The production LO inversion uses 160 CRR steps. This diagnostic selects a
deterministic stratified subset spanning reference date, underlying futures
contract, option type, and moneyness, then re-inverts implied volatility at
80, 160, and 320 steps.

Within each date/underlying/option-type group, the lowest-moneyness,
nearest-ATM, and highest-moneyness contracts are retained. This keeps the audit
small while covering the observed strike range.
"""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

from bayesian_asian_options.american_futures_option import (
    implied_volatility_american_futures,
)


DEFAULT_PANEL = Path(
    "results/analysis/wti_databento_external_q/vanilla_iv_panel.csv"
)
DEFAULT_OUTPUT = Path(
    "results/analysis/wti_databento_external_q/tree_convergence"
)
DEFAULT_STEPS = (80, 160, 320)


def select_stratified(panel: pd.DataFrame) -> pd.DataFrame:
    """Select low/ATM/high moneyness rows in each date-underlying-side group."""
    required = {
        "reference_date",
        "underlying",
        "option_type",
        "log_moneyness",
        "option_settlement",
        "futures_settlement",
        "strike_price",
        "maturity_years",
        "rate_proxy",
        "symbol",
    }
    missing = required.difference(panel.columns)
    if missing:
        raise ValueError(f"panel missing columns: {sorted(missing)}")

    frame = panel.copy()
    if "iv_status" in frame.columns:
        frame = frame[
            frame["iv_status"].astype(str).isin({"ok", "ok_lower_bound"})
        ].copy()
    frame = frame.dropna(
        subset=[
            "log_moneyness",
            "option_settlement",
            "futures_settlement",
            "strike_price",
            "maturity_years",
            "rate_proxy",
        ]
    )
    selected: list[pd.DataFrame] = []
    group_cols = ["reference_date", "underlying", "option_type"]
    for _, group in frame.groupby(group_cols, sort=True):
        group = group.sort_values("log_moneyness").reset_index(drop=True)
        if group.empty:
            continue
        indices = {
            0,
            len(group) - 1,
            int(np.abs(group["log_moneyness"].to_numpy(dtype=float)).argmin()),
        }
        selected.append(group.iloc[sorted(indices)].copy())
    if not selected:
        raise ValueError("no rows selected for convergence audit")
    return pd.concat(selected, ignore_index=True).drop_duplicates(
        ["reference_date", "symbol"],
        keep="first",
    )


def run(
    panel_path: Path,
    output_dir: Path,
    *,
    steps_grid: tuple[int, ...] = DEFAULT_STEPS,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    panel = pd.read_csv(panel_path)
    selected = select_stratified(panel)
    rows: list[dict[str, Any]] = []

    for row in selected.itertuples(index=False):
        record: dict[str, Any] = {
            "reference_date": str(row.reference_date),
            "symbol": str(row.symbol),
            "underlying": str(row.underlying),
            "option_type": str(row.option_type),
            "strike_price": float(row.strike_price),
            "log_moneyness": float(row.log_moneyness),
        }
        for steps in steps_grid:
            result = implied_volatility_american_futures(
                float(row.option_settlement),
                float(row.futures_settlement),
                float(row.strike_price),
                float(row.maturity_years),
                float(row.rate_proxy),
                str(row.option_type),
                steps=int(steps),
            )
            record[f"status_{steps}"] = result.status
            record[f"sigma_{steps}"] = float(result.sigma)
            record[f"model_price_{steps}"] = float(result.model_price)
        rows.append(record)

    detail = pd.DataFrame(rows)
    if 160 in steps_grid and 320 in steps_grid:
        detail["abs_sigma_160_minus_320"] = (
            detail["sigma_160"] - detail["sigma_320"]
        ).abs()
    if 80 in steps_grid and 160 in steps_grid:
        detail["abs_sigma_80_minus_160"] = (
            detail["sigma_80"] - detail["sigma_160"]
        ).abs()

    summary_rows: list[dict[str, Any]] = []
    for column in (
        "abs_sigma_80_minus_160",
        "abs_sigma_160_minus_320",
    ):
        if column not in detail.columns:
            continue
        values = pd.to_numeric(detail[column], errors="coerce").dropna()
        summary_rows.append(
            {
                "comparison": column.removeprefix("abs_sigma_"),
                "n": int(len(values)),
                "mean_abs_sigma_difference": float(values.mean()),
                "median_abs_sigma_difference": float(values.median()),
                "p95_abs_sigma_difference": float(values.quantile(0.95)),
                "max_abs_sigma_difference": float(values.max()),
            }
        )
    summary = pd.DataFrame(summary_rows)
    output_dir.mkdir(parents=True, exist_ok=True)
    detail.to_csv(output_dir / "tree_convergence_detail.csv", index=False)
    summary.to_csv(output_dir / "tree_convergence_summary.csv", index=False)
    return detail, summary


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--panel-path", type=Path, default=DEFAULT_PANEL)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--steps", default="80,160,320")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    steps = tuple(
        int(value.strip())
        for value in args.steps.split(",")
        if value.strip()
    )
    _, summary = run(
        args.panel_path,
        args.output_dir,
        steps_grid=steps,
    )
    print(summary.to_string(index=False))
    print(f"output_dir={args.output_dir}")


if __name__ == "__main__":
    main()
