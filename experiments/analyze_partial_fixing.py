"""Analyze how posterior-integration effects evolve as a WTI APO becomes fixed.

The input is a contract-level panel produced by ``experiments.wti_apo_date_panel`` for an
averaging month with in-month valuation dates.  The analysis is descriptive: it summarizes
``|PI-PM|`` by valuation date/fraction fixed and estimates a within-contract slope after
removing each contract's time-invariant level.

The within-contract transformation is useful because strike and option type are fixed within
a contract while ``fraction_fixed`` changes through the averaging month.  It is not presented
as a causal estimator; moneyness, posterior dispersion, time to payoff, and the futures curve
also evolve with date.

Example
-------
    python -m experiments.analyze_partial_fixing \
        --panel results/wti_apo_empirical/panel_202609/all_dates/panel_contract_pricing.csv
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd


DEFAULT_PANEL = Path(
    "results/wti_apo_empirical/panel_202609/all_dates/panel_contract_pricing.csv"
)
DEFAULT_OUTPUT = Path("results/analysis/partial_fixing_202609")

REQUIRED_COLUMNS = {
    "valuation_date_panel",
    "contract_id",
    "fraction_fixed",
    "n_realized_fixings",
    "n_remaining_fixings",
    "abs_fb_minus_pm",
    "fb_minus_pm",
    "fb_abs_error",
    "pm_abs_error",
    "market_price",
    "log_moneyness",
    "run_sigma_posterior_sd",
    "positive_volume",
}


def within_contract_slope(
    frame: pd.DataFrame,
    *,
    x: str = "fraction_fixed",
    y: str = "abs_fb_minus_pm",
    contract: str = "contract_id",
) -> tuple[float | None, int, int]:
    """Return the fixed-effect/within slope of ``y`` on ``x``.

    The function de-means both variables within contract and then fits a no-intercept OLS
    coefficient. Contracts observed at only one distinct x value do not identify the slope.
    """
    pieces: list[pd.DataFrame] = []
    informative_contracts = 0
    for _, group in frame.groupby(contract):
        clean = group[[x, y]].dropna().astype(float)
        if clean.empty or clean[x].nunique() < 2:
            continue
        informative_contracts += 1
        centered = clean - clean.mean()
        pieces.append(centered)
    if not pieces:
        return None, 0, 0
    within = pd.concat(pieces, ignore_index=True)
    xv = within[x].to_numpy(dtype=float)
    yv = within[y].to_numpy(dtype=float)
    denom = float(np.dot(xv, xv))
    if denom <= 0:
        return None, informative_contracts, int(len(within))
    return float(np.dot(xv, yv) / denom), informative_contracts, int(len(within))


def _corr(a: pd.Series, b: pd.Series) -> float | None:
    x = np.asarray(a, dtype=float)
    y = np.asarray(b, dtype=float)
    mask = np.isfinite(x) & np.isfinite(y)
    x, y = x[mask], y[mask]
    if x.size < 2 or np.std(x) == 0 or np.std(y) == 0:
        return None
    return float(np.corrcoef(x, y)[0, 1])


def analyze(panel_path: Path) -> tuple[pd.DataFrame, pd.DataFrame, dict[str, Any]]:
    panel = pd.read_csv(panel_path)
    missing = REQUIRED_COLUMNS.difference(panel.columns)
    if missing:
        raise ValueError(
            "partial-fixing panel is missing columns "
            f"{sorted(missing)}; rebuild the panel with the current date-panel driver"
        )
    panel["valuation_date_panel"] = pd.to_datetime(panel["valuation_date_panel"])
    panel["positive_volume"] = panel["positive_volume"].astype(bool)

    date_rows: list[dict[str, Any]] = []
    for date, group in panel.groupby("valuation_date_panel", sort=True):
        fraction_values = group["fraction_fixed"].dropna().unique()
        if len(fraction_values) != 1:
            raise ValueError(f"fraction_fixed is not unique within valuation date {date.date()}")
        date_rows.append(
            {
                "valuation_date": date.date().isoformat(),
                "contracts": int(len(group)),
                "positive_volume_contracts": int(group["positive_volume"].sum()),
                "fraction_fixed": float(fraction_values[0]),
                "n_realized_fixings": int(group["n_realized_fixings"].iloc[0]),
                "n_remaining_fixings": int(group["n_remaining_fixings"].iloc[0]),
                "mean_abs_pi_minus_pm": float(group["abs_fb_minus_pm"].mean()),
                "median_abs_pi_minus_pm": float(group["abs_fb_minus_pm"].median()),
                "max_abs_pi_minus_pm": float(group["abs_fb_minus_pm"].max()),
                "mean_signed_pi_minus_pm": float(group["fb_minus_pm"].mean()),
                "mean_fb_abs_error": float(group["fb_abs_error"].mean()),
                "mean_pm_abs_error": float(group["pm_abs_error"].mean()),
                "mean_abs_log_moneyness": float(group["log_moneyness"].abs().mean()),
                "posterior_sigma_sd": float(group["run_sigma_posterior_sd"].iloc[0]),
            }
        )
    by_date = pd.DataFrame(date_rows).sort_values("valuation_date")

    slope, n_contracts, n_rows = within_contract_slope(panel)
    slope_volume, n_contracts_volume, n_rows_volume = within_contract_slope(
        panel[panel["positive_volume"]]
    )

    # A second descriptive object normalizes the PI-PM gap by posterior variance.  This
    # does not isolate curvature perfectly, but it helps distinguish a shrinking fixing
    # exposure from changes in posterior dispersion across dates.
    panel = panel.copy()
    variance = panel["run_sigma_posterior_sd"].astype(float) ** 2
    panel["abs_gap_per_sigma_variance"] = np.where(
        variance > 0,
        panel["abs_fb_minus_pm"].astype(float) / variance,
        np.nan,
    )

    report = {
        "source_panel": str(panel_path),
        "rows": int(len(panel)),
        "contracts": int(panel["contract_id"].nunique()),
        "dates": int(panel["valuation_date_panel"].nunique()),
        "fraction_fixed_min": float(panel["fraction_fixed"].min()),
        "fraction_fixed_max": float(panel["fraction_fixed"].max()),
        "correlation_fraction_fixed_abs_gap": _corr(
            panel["fraction_fixed"], panel["abs_fb_minus_pm"]
        ),
        "correlation_fraction_fixed_gap_per_sigma_variance": _corr(
            panel["fraction_fixed"], panel["abs_gap_per_sigma_variance"]
        ),
        "within_contract": {
            "slope_abs_gap_on_fraction_fixed": slope,
            "informative_contracts": n_contracts,
            "rows": n_rows,
        },
        "positive_volume_within_contract": {
            "slope_abs_gap_on_fraction_fixed": slope_volume,
            "informative_contracts": n_contracts_volume,
            "rows": n_rows_volume,
        },
        "interpretation": (
            "A negative within-contract slope is consistent with declining effective "
            "volatility exposure as realized fixings accumulate. It is descriptive, not "
            "causal, because moneyness, the futures curve, and time to payoff also change."
        ),
    }
    return panel, by_date, report


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--panel", type=Path, default=DEFAULT_PANEL)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    panel, by_date, report = analyze(args.panel)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    panel.to_csv(args.output_dir / "partial_fixing_contract_rows.csv", index=False)
    by_date.to_csv(args.output_dir / "partial_fixing_by_date.csv", index=False)
    with (args.output_dir / "partial_fixing_report.json").open("w", encoding="utf-8") as fh:
        json.dump(report, fh, indent=2, sort_keys=True)
        fh.write("\n")
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
