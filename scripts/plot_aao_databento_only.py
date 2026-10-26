"""Publication-ready reduced-form AAO figures from COMPLETE run results.

Pure post-processing. This script NEVER estimates volatility, purchases
data, or invents missing results. Run manually after experiment completes.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
ANALYSIS = ROOT / "results" / "analysis" / "wti_aao_databento_only"
OUTPUT = ROOT / "figures" / "aao_databento_only"
METHODS = ("PI", "PM", "rolling21", "rolling63", "ewma63", "lagged_IV")
COLORS = ("#0072B2", "#D55E00", "#009E73", "#CC79A7", "#E69F00", "#555555")


def check_results(path: Path) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, dict]:
    necessary = [
        path / "method_metrics.csv", path / "daily_metrics.csv",
        path / "cluster_intervals.csv", path / "experiment_manifest.json"
    ]
    missing = [str(f) for f in necessary if not f.is_file()]
    if missing:
        raise FileNotFoundError(
            "Missing completed experiment outputs: " + ", ".join(missing)
        )
    m = pd.read_csv(necessary[0])
    d = pd.read_csv(necessary[1])
    ci = pd.read_csv(necessary[2])
    manifest = json.loads(necessary[3].read_text(encoding="utf-8"))
    if manifest.get("groups_priced", 0) <= 0 or manifest.get("no_provider_calls") is not True:
        raise ValueError("Invalid or incomplete Databento-only experiment")
    if set(m["method"]) != set(METHODS):
        raise ValueError("Metrics missing benchmark methods")
    if not {"date", "method", "mae", "n"}.issubset(d):
        raise ValueError("Missing daily errors in completed run")
    if not {"method", "ci_low", "ci_high", "mean_daily_mae_improvement"}.issubset(ci):
        raise ValueError("Missing clustered benchmark comparisons")
    return m, d, ci, manifest


def save(fig, root: Path, name: str) -> None:
    for ext in ("pdf", "svg", "png"):
        fig.savefig(root / f"{name}.{ext}", dpi=200, bbox_inches="tight")
    plt.close(fig)


def draw(analysis: Path, output: Path) -> dict:
    metrics, daily, intervals, manifest = check_results(analysis)
    output.mkdir(parents=True, exist_ok=True)
    palette = dict(zip(METHODS, COLORS))
    labels = {
        "PI": "Posterior integrated",
        "PM": "Posterior mean",
        "rolling21": "Historical 21-day",
        "rolling63": "Historical 63-day",
        "ewma63": "EWMA (63-day half-life)",
        "lagged_IV": "Previous-date AAO implied",
    }
    # Figure 1: actual/theoretical point-mark quality explicitly separated.
    fig, ax = plt.subplots(figsize=(9.6, 4.6))
    subsets = ("actual_flagged", "theoretical_flagged")
    width = .12
    for i, method in enumerate(METHODS):
        vals = []
        for kind in subsets:
            view = metrics.loc[
                (metrics["settlement_type"]==kind)
                & (metrics["method"]==method), "mae"
            ]
            vals.append(float(view.iloc[0]) if len(view) else np.nan)
        ax.bar(
            np.arange(len(subsets))+(i-2.5)*width, vals,
            width=width, color=palette[method], label=labels[method]
        )
    ax.set_xticks(range(len(subsets)), ["Actual-flagged", "Theoretical-flagged"])
    ax.set_ylabel("Mean absolute pricing error (USD per barrel)")
    ax.set_title("AAO reduced-form valuation errors by settlement mark type")
    ax.legend(ncol=3, fontsize=8, frameon=False, loc="upper center",
              bbox_to_anchor=(.5, -.12))
    ax.grid(axis="y", alpha=.2)
    save(fig, output, "fig06_databento_benchmark_mae")

    # Figure 2: cluster-resampled improvements. Positive = PI/other better.
    s = intervals.set_index("method").reindex([
        m for m in METHODS if m != "PM"
    ])
    fig, ax = plt.subplots(figsize=(8.2, 4.2))
    indices = np.arange(len(s))
    for y, method in enumerate(s.index):
        point = float(s.loc[method, "mean_daily_mae_improvement"])
        lo = float(s.loc[method, "ci_low"])
        hi = float(s.loc[method, "ci_high"])
        ax.plot([lo, hi], [y, y], color=palette[method], lw=2.4)
        ax.plot(point, y, "o", color=palette[method], markersize=7)
    ax.axvline(0, color=".45", linestyle="--", lw=1)
    ax.set_yticks(indices, [labels[m] for m in s.index])
    ax.set_xlabel("Mean date-level MAE improvement over posterior mean (USD/bbl)")
    ax.set_title("Paired, valuation-date clustered comparisons (95% interval)")
    ax.grid(axis="x", alpha=.2)
    fig.tight_layout()
    save(fig, output, "fig07_databento_date_cluster_intervals")

    # Figure 3: balanced date-level trend, not 5m independent observations.
    daily["date"] = pd.to_datetime(daily["date"])
    pivot = daily.pivot(index="date", columns="method", values="mae")
    if not pivot.empty:
        fig, ax = plt.subplots(figsize=(10.0, 4.8))
        for method in METHODS:
            if method in pivot:
                values = pivot[method].sort_index()
                smooth = values.rolling(12, min_periods=3).median()
                ax.plot(smooth.index, smooth.to_numpy(), label=labels[method],
                        lw=1.6, color=palette[method])
        ax.set_ylabel("Rolling median of date-level MAE (USD/bbl)")
        ax.set_xlabel("CME settlement reference date")
        ax.set_title("Pricing errors through time — reduced-form model")
        ax.legend(ncol=2, frameon=False, fontsize=8)
        ax.grid(alpha=.2)
        fig.tight_layout()
        save(fig, output, "fig08_databento_mae_time_series")
    response = {
        "source_experiment": str(analysis),
        "source_priced_dates": manifest["n_priced_dates"],
        "source_contract_dates": manifest["n_target_contract_dates"],
        "figures": ["fig06_databento_benchmark_mae",
                    "fig07_databento_date_cluster_intervals",
                    "fig08_databento_mae_time_series"],
        "formats": ["pdf", "png", "svg"],
        "no_new_model_computation": True,
        "pricing_scope": "AAO-only reduced-form terminal-average lognormal",
    }
    (output/"figure_manifest.json").write_text(
        json.dumps(response, indent=2)+"\n", encoding="utf-8"
    )
    return response


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input-dir", type=Path, default=ANALYSIS)
    parser.add_argument("--output-dir", type=Path, default=OUTPUT)
    args = parser.parse_args()
    print(json.dumps(draw(args.input_dir, args.output_dir), indent=2))


if __name__ == "__main__":
    main()
