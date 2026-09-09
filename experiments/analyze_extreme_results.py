"""Analyze the publication-scale synthetic experiment.

This module turns the compact scenario-level summary produced by
``experiments.large_scale_synthetic`` into paper-oriented diagnostics.  It does not
need the large ``.npz`` checkpoints or the raw 162,000-row CSV, so the published
analysis can be regenerated from the small files committed to the repository.

Example
-------
    conda run -n asian-options python -m experiments.analyze_extreme_results
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd


DEFAULT_EXTREME = Path(
    "results/large_scale_synthetic/f497062f0c571126/pricing_results_summary.csv"
)
DEFAULT_BACKEND = Path(
    "results/large_scale_synthetic/f497062f0c571126/pricing_backend_summary.csv"
)
DEFAULT_RESEARCH = Path(
    "results/large_scale_synthetic/7843e0b3b9c2c562/pricing_results_summary.csv"
)
DEFAULT_OUTPUT = Path("results/analysis/extreme_analysis.json")

SCENARIO = ["n_obs", "sigma_true", "moneyness_K_over_S0", "maturity"]
METHODS = ["full_bayes", "postmean_plugin", "map_plugin", "mle_plugin"]


def _pivot(df: pd.DataFrame, metric: str) -> pd.DataFrame:
    out = df.pivot(index=SCENARIO, columns="method", values=metric).reset_index()
    out.columns.name = None
    return out


def _records(frame: pd.DataFrame, n: int = 10) -> list[dict[str, Any]]:
    records = frame.head(n).to_dict(orient="records")
    clean: list[dict[str, Any]] = []
    for row in records:
        clean.append(
            {
                str(k): (
                    int(v)
                    if isinstance(v, (np.integer,))
                    else float(v)
                    if isinstance(v, (np.floating,))
                    else v
                )
                for k, v in row.items()
            }
        )
    return clean


def analyze(
    extreme_path: Path = DEFAULT_EXTREME,
    backend_path: Path = DEFAULT_BACKEND,
    research_path: Path | None = DEFAULT_RESEARCH,
) -> tuple[dict[str, Any], pd.DataFrame]:
    df = pd.read_csv(extreme_path)
    expected = set(SCENARIO + ["method", "bias", "mae", "rmse", "coverage_95", "mean_acceptance_rate"])
    missing = expected.difference(df.columns)
    if missing:
        raise ValueError(f"missing columns: {sorted(missing)}")

    scenarios = df[SCENARIO].drop_duplicates()
    if len(df) != len(scenarios) * len(METHODS):
        raise ValueError("summary does not contain exactly one row per method/scenario")

    rmse = _pivot(df, "rmse")
    mae = _pivot(df, "mae")
    bias = _pivot(df, "bias")

    for frame, metric in ((rmse, "rmse"), (mae, "mae")):
        method_cols = [m for m in METHODS if m in frame]
        frame[f"best_{metric}"] = frame[method_cols].idxmin(axis=1)

    # Full Bayes versus posterior-mean plug-in is the main conceptual comparison.
    rmse["fb_minus_pm_rmse"] = rmse["full_bayes"] - rmse["postmean_plugin"]
    rmse["fb_vs_pm_rmse_pct"] = 100.0 * rmse["fb_minus_pm_rmse"] / rmse["postmean_plugin"]
    bias["fb_minus_pm_price_mean"] = bias["full_bayes"] - bias["postmean_plugin"]
    bias["abs_fb_minus_pm_price_mean"] = bias["fb_minus_pm_price_mean"].abs()

    winner_counts_rmse = rmse["best_rmse"].value_counts().reindex(METHODS, fill_value=0)
    winner_counts_mae = mae["best_mae"].value_counts().reindex(METHODS, fill_value=0)

    pairwise = {}
    for competitor in ("postmean_plugin", "map_plugin", "mle_plugin"):
        d = rmse["full_bayes"] - rmse[competitor]
        pairwise[competitor] = {
            "fb_lower_rmse_count": int((d < 0).sum()),
            "tie_count": int(np.isclose(d, 0.0, rtol=1e-12, atol=1e-12).sum()),
            "fb_higher_rmse_count": int((d > 0).sum()),
            "mean_rmse_difference_fb_minus_competitor": float(d.mean()),
            "median_rmse_difference_fb_minus_competitor": float(d.median()),
        }

    by_n_rows = []
    for n_obs, group in rmse.groupby("n_obs"):
        for method in METHODS:
            by_n_rows.append(
                {
                    "n_obs": int(n_obs),
                    "method": method,
                    "mean_rmse_across_contract_regimes": float(group[method].mean()),
                    "median_rmse_across_contract_regimes": float(group[method].median()),
                }
            )
    by_n = pd.DataFrame(by_n_rows)

    # Reduction in estimation error when history expands from 63 to 1260 daily observations.
    shrink_rows = []
    for method in METHODS:
        a = rmse[rmse.n_obs == 63].set_index(["sigma_true", "moneyness_K_over_S0", "maturity"])[method]
        b = rmse[rmse.n_obs == 1260].set_index(["sigma_true", "moneyness_K_over_S0", "maturity"])[method]
        ratio = a / b
        shrink_rows.append(
            {
                "method": method,
                "median_rmse_ratio_n63_over_n1260": float(ratio.median()),
                "mean_rmse_ratio_n63_over_n1260": float(ratio.mean()),
                "min_ratio": float(ratio.min()),
                "max_ratio": float(ratio.max()),
            }
        )

    # Coverage and acceptance depend on the historical-data scenario, not the contract,
    # so deduplicate strike/maturity repetitions before summarizing.
    diagnostics = (
        df[["n_obs", "sigma_true", "coverage_95", "mean_acceptance_rate"]]
        .drop_duplicates()
        .sort_values(["n_obs", "sigma_true"])
    )

    backend: dict[str, Any] = {}
    if backend_path.exists():
        be = pd.read_csv(backend_path)
        backend = {
            "all_gpu_backend": bool((be["backend"] == "cupy").all()),
            "max_pricing_se": float(be["max_pricing_se"].max()),
            "median_pricing_se": float(be["max_pricing_se"].median()),
            "min_pricing_se": float(be["max_pricing_se"].min()),
            "rows": _records(be, len(be)),
        }

    # Stability check against the 1,000-replication research run.
    robustness: dict[str, Any] = {}
    if research_path is not None and research_path.exists():
        old = pd.read_csv(research_path)
        merged = df.merge(
            old,
            on=SCENARIO + ["method"],
            suffixes=("_extreme", "_research"),
            validate="one_to_one",
        )
        delta = merged["rmse_extreme"] - merged["rmse_research"]
        rel = delta / merged["rmse_research"].replace(0.0, np.nan)
        robustness = {
            "rows_compared": int(len(merged)),
            "mean_abs_rmse_change": float(delta.abs().mean()),
            "median_abs_rmse_change": float(delta.abs().median()),
            "median_abs_relative_rmse_change_pct": float(100.0 * rel.abs().median()),
            "max_abs_relative_rmse_change_pct": float(100.0 * rel.abs().max()),
            "mean_abs_coverage_change": float(
                (merged["coverage_95_extreme"] - merged["coverage_95_research"]).abs().mean()
            ),
        }

    top_jensen = bias.sort_values("abs_fb_minus_pm_price_mean", ascending=False)
    top_relative_rmse_gap = rmse.reindex(rmse["fb_vs_pm_rmse_pct"].abs().sort_values(ascending=False).index)

    report: dict[str, Any] = {
        "source": str(extreme_path),
        "scenario_count": int(len(scenarios)),
        "summary_row_count": int(len(df)),
        "replications_per_scenario": sorted(int(x) for x in df["replications"].unique()),
        "rmse_winner_counts": {m: int(winner_counts_rmse[m]) for m in METHODS},
        "mae_winner_counts": {m: int(winner_counts_mae[m]) for m in METHODS},
        "pairwise_full_bayes_rmse": pairwise,
        "fb_vs_pm": {
            "fb_lower_rmse_scenarios": int((rmse["fb_minus_pm_rmse"] < 0).sum()),
            "pm_lower_rmse_scenarios": int((rmse["fb_minus_pm_rmse"] > 0).sum()),
            "median_abs_relative_rmse_gap_pct": float(rmse["fb_vs_pm_rmse_pct"].abs().median()),
            "mean_abs_relative_rmse_gap_pct": float(rmse["fb_vs_pm_rmse_pct"].abs().mean()),
            "median_abs_mean_price_gap": float(bias["abs_fb_minus_pm_price_mean"].median()),
            "max_abs_mean_price_gap": float(bias["abs_fb_minus_pm_price_mean"].max()),
            "largest_mean_price_gaps": _records(
                top_jensen[SCENARIO + ["fb_minus_pm_price_mean", "abs_fb_minus_pm_price_mean"]], 8
            ),
            "largest_relative_rmse_gaps": _records(
                top_relative_rmse_gap[
                    SCENARIO
                    + ["full_bayes", "postmean_plugin", "fb_minus_pm_rmse", "fb_vs_pm_rmse_pct"]
                ],
                8,
            ),
        },
        "rmse_by_history_length": _records(by_n, len(by_n)),
        "rmse_shrinkage_n63_to_n1260": shrink_rows,
        "coverage": {
            "min": float(diagnostics["coverage_95"].min()),
            "max": float(diagnostics["coverage_95"].max()),
            "mean": float(diagnostics["coverage_95"].mean()),
            "by_n_sigma": _records(diagnostics, len(diagnostics)),
        },
        "acceptance": {
            "min": float(diagnostics["mean_acceptance_rate"].min()),
            "max": float(diagnostics["mean_acceptance_rate"].max()),
            "mean": float(diagnostics["mean_acceptance_rate"].mean()),
            "by_n_sigma": _records(diagnostics, len(diagnostics)),
        },
        "pricing_backend": backend,
        "research_vs_extreme_robustness": robustness,
    }

    scenario_metrics = rmse.merge(
        bias[SCENARIO + ["fb_minus_pm_price_mean", "abs_fb_minus_pm_price_mean"]],
        on=SCENARIO,
        validate="one_to_one",
    )
    return report, scenario_metrics


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--extreme", type=Path, default=DEFAULT_EXTREME)
    parser.add_argument("--backend", type=Path, default=DEFAULT_BACKEND)
    parser.add_argument("--research", type=Path, default=DEFAULT_RESEARCH)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    report, scenario_metrics = analyze(args.extreme, args.backend, args.research)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    scenario_metrics.to_csv(args.output.with_name("extreme_scenario_metrics.csv"), index=False)
    print(json.dumps(report, indent=2, sort_keys=True))
    print(f"analysis_json={args.output}")
    print(f"scenario_csv={args.output.with_name('extreme_scenario_metrics.csv')}")


if __name__ == "__main__":
    main()
