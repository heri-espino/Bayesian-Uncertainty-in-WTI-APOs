"""Plot *event* coverage from the complete local AAO inventory; no API usage.

Never equate settlement statistic events with deduplicated option prices,
market trades, independent backtest observations, or valid target dates.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = (ROOT / "results" / "analysis" / "wti_aao_history_feasibility"
          / "inventory" / "aao_inventory_summary.json")
OUTPUT = ROOT / "figures" / "extended_aao"


def extract_coverage(report: dict) -> list[dict]:
    """Accept only a complete, internally consistent 81-month source report."""
    if report.get("errors"):
        raise ValueError("Input inventory has processing errors")
    months = report.get("months", [])
    if report.get("summary", {}).get("months_processed") != 81 or len(months) != 81:
        raise ValueError("Requires refreshed 81-month inventory, not old 80-month results")
    expected = []
    year, month = 2020, 1
    for _ in range(81):
        expected.append(f"{year:04d}-{month:02d}")
        month += 1
        if month == 13:
            year, month = year + 1, 1
    actual_months = [row.get("month") for row in months]
    if actual_months != expected:
        raise ValueError("Missing, repeated or out-of-order 2020-2026 reference months")
    rows = []
    for row in months:
        d = row.get("definitions", {})
        s = row.get("statistics", {})
        if d.get("top_asset", {}).get("AAO", 0) <= 0:
            raise ValueError(f"No AAO asset in {row['month']}")
        counts = [s.get("final_events"), s.get("final_actual_events"),
                  s.get("final_theoretical_events")]
        if any(not isinstance(v, int) or v < 0 for v in counts):
            raise ValueError(f"Invalid event counts in {row['month']}")
        if counts[0] != counts[1] + counts[2]:
            raise ValueError(f"Inconsistent final flags in {row['month']}")
        rows.append({"month": row["month"], "actual": counts[1],
                     "theoretical": counts[2]})
    return rows


def draw(rows: list[dict], output: Path, source_sha256: str) -> dict:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import matplotlib.dates as mdates
    import pandas as pd

    dates = pd.to_datetime([x["month"] for x in rows], format="%Y-%m")
    actual = [x["actual"] for x in rows]
    theoretical = [x["theoretical"] for x in rows]
    fig, ax = plt.subplots(figsize=(10.8, 4.5), layout="constrained")
    ax.bar(dates, actual, width=25, label="Final, actual-flagged",
           color="#3076AB")
    ax.bar(dates, theoretical, width=25, bottom=actual,
           label="Final, theoretical-flagged", color="#D4A34D")
    ax.xaxis.set_major_locator(mdates.YearLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
    ax.set_xlabel("CME reference month")
    ax.set_ylabel("Settlement statistic events")
    ax.set_title("WTI AAO settlement-event history, 2020–2026")
    ax.legend(frameon=False, loc="upper left", ncol=2)
    ax.spines[["top", "right"]].set_visible(False)
    ax.grid(axis="y", alpha=.2)
    fig.text(.01, -.015,
             "Event counts only: not contract-day prices, trades, or forward-test dates.",
             fontsize=8, ha="left", va="top")
    output.mkdir(parents=True, exist_ok=True)
    stem = "fig05_aao_final_settlement_event_coverage"
    for ext in ("pdf", "png", "svg"):
        fig.savefig(output / f"{stem}.{ext}", dpi=220, bbox_inches="tight")
    plt.close(fig)
    manifest = {
        "source": "results/analysis/wti_aao_history_feasibility/inventory/aao_inventory_summary.json",
        "source_sha256": source_sha256,
        "months": len(rows),
        "status": "diagnostic_only_not_validated_option_pricing",
        "figures": [f"{stem}.{ext}" for ext in ("pdf", "png", "svg")],
    }
    (output / "coverage_figure_manifest.json").write_text(
        json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    return manifest


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=SOURCE)
    parser.add_argument("--output-dir", type=Path, default=OUTPUT)
    args = parser.parse_args()
    source = args.input.read_bytes()
    rows = extract_coverage(json.loads(source))
    result = draw(rows, args.output_dir,
                  hashlib.sha256(source).hexdigest())
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
