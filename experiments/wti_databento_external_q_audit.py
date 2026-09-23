"""Audit locally downloaded Databento WTI vanilla-option statistics.

The audit is read-only with respect to market-data inputs. It summarizes official
statistics by reference date (`ts_ref`), instrument, and statistic type before any
implied-volatility inversion or APO-pricing experiment is attempted.

For CME Globex GLBX.MDP3 the relevant official daily statistics are:
- 3: settlement price
- 6: cleared volume
- 9: open interest

CME can publish multiple updates for one reference date. Settlement `stat_flags` bit 0
marks a final rather than preliminary settlement, and bit 1 marks actual rather than
theoretical settlement.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]

STAT_NAMES = {
    1: "opening_price",
    2: "indicative_opening_price",
    3: "settlement_price",
    4: "session_low",
    5: "session_high",
    6: "cleared_volume",
    7: "lowest_offer",
    8: "highest_bid",
    9: "open_interest",
    10: "fixing_price",
    17: "upper_price_limit",
    18: "lower_price_limit",
}


def _load_csv(path: Path) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(path)
    frame = pd.read_csv(path, index_col=0)
    if frame.index.name and frame.index.name not in frame.columns:
        frame = frame.reset_index()
    return frame


def _coerce_stat_type(series: pd.Series) -> pd.Series:
    numeric = pd.to_numeric(series, errors="coerce")
    if numeric.notna().all():
        return numeric.astype("Int64")
    text = series.astype(str).str.extract(r"(\d+)", expand=False)
    return pd.to_numeric(text, errors="coerce").astype("Int64")


def _reference_date(frame: pd.DataFrame) -> pd.Series:
    for column in ("ts_ref", "ts_event", "ts_recv"):
        if column not in frame.columns:
            continue
        values = frame[column]
        numeric = pd.to_numeric(values, errors="coerce")
        if numeric.notna().sum() >= max(1, int(0.9 * len(values))):
            parsed = pd.to_datetime(numeric, unit="ns", utc=True, errors="coerce")
        else:
            parsed = pd.to_datetime(values, utc=True, errors="coerce")
        if parsed.notna().any():
            return parsed.dt.date.astype("string")
    raise ValueError("Statistics data have no usable ts_ref/ts_event/ts_recv timestamp.")


def _normalize_statistics(frame: pd.DataFrame) -> pd.DataFrame:
    required = {"instrument_id", "stat_type"}
    missing = required.difference(frame.columns)
    if missing:
        raise ValueError(f"Statistics data missing columns: {sorted(missing)}")

    out = frame.copy()
    out["instrument_id"] = pd.to_numeric(out["instrument_id"], errors="coerce").astype("Int64")
    out["stat_type"] = _coerce_stat_type(out["stat_type"])
    out["reference_date"] = _reference_date(out)
    out["stat_name"] = out["stat_type"].map(STAT_NAMES).fillna("other")

    flags = pd.to_numeric(out.get("stat_flags", 0), errors="coerce").fillna(0).astype("int64")
    out["settlement_final"] = out["stat_type"].eq(3) & flags.map(lambda x: bool(x & 1))
    out["settlement_actual"] = out["stat_type"].eq(3) & flags.map(lambda x: bool(x & 2))
    out["settlement_intraday"] = out["stat_type"].eq(3) & flags.map(lambda x: bool(x & 8))
    return out


def _attach_option_metadata(option_stats: pd.DataFrame, selected: pd.DataFrame) -> pd.DataFrame:
    required = {"instrument_id", "raw_symbol", "underlying", "strike_price", "option_type"}
    missing = required.difference(selected.columns)
    if missing:
        raise ValueError(f"Selected definitions missing columns: {sorted(missing)}")

    metadata = selected[list(required)].copy()
    metadata["instrument_id"] = pd.to_numeric(metadata["instrument_id"], errors="coerce").astype("Int64")
    metadata["strike_price"] = pd.to_numeric(metadata["strike_price"], errors="coerce")
    metadata = metadata.drop_duplicates(subset=["instrument_id"], keep="last")

    merged = option_stats.merge(
        metadata,
        on="instrument_id",
        how="left",
        validate="many_to_one",
        indicator=True,
    )
    unmatched = int(merged["_merge"].ne("both").sum())
    if unmatched:
        raise RuntimeError(
            f"{unmatched} option-statistics rows could not be matched to selected definitions."
        )
    return merged.drop(columns="_merge")


def _stat_type_summary(frame: pd.DataFrame, source: str) -> pd.DataFrame:
    grouped = (
        frame.groupby(["stat_type", "stat_name"], dropna=False)
        .agg(
            rows=("instrument_id", "size"),
            instruments=("instrument_id", "nunique"),
            reference_dates=("reference_date", "nunique"),
            first_reference_date=("reference_date", "min"),
            last_reference_date=("reference_date", "max"),
        )
        .reset_index()
    )
    grouped.insert(0, "source", source)
    return grouped


def build_audit(
    *,
    selected: pd.DataFrame,
    option_stats: pd.DataFrame,
    futures_stats: pd.DataFrame,
    target_start: str,
    target_end: str,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, dict[str, Any]]:
    """Build coverage tables and a JSON-serializable readiness summary."""
    options = _attach_option_metadata(_normalize_statistics(option_stats), selected)
    futures = _normalize_statistics(futures_stats)

    stat_summary = pd.concat(
        [_stat_type_summary(options, "options"), _stat_type_summary(futures, "futures")],
        ignore_index=True,
    )

    instrument_rows: list[dict[str, Any]] = []
    selected_norm = selected.copy()
    selected_norm["instrument_id"] = pd.to_numeric(
        selected_norm["instrument_id"], errors="coerce"
    ).astype("Int64")
    selected_norm["strike_price"] = pd.to_numeric(
        selected_norm["strike_price"], errors="coerce"
    )
    for instrument_id, meta in (
        selected_norm.drop_duplicates("instrument_id").set_index("instrument_id").iterrows()
    ):
        sub = options.loc[options["instrument_id"].eq(instrument_id)]
        settlement = sub.loc[sub["stat_type"].eq(3)]
        final_settlement = settlement.loc[settlement["settlement_final"]]
        actual_settlement = settlement.loc[settlement["settlement_actual"]]
        volume = sub.loc[sub["stat_type"].eq(6)]
        oi = sub.loc[sub["stat_type"].eq(9)]
        instrument_rows.append(
            {
                "instrument_id": int(instrument_id),
                "raw_symbol": meta["raw_symbol"],
                "underlying": meta["underlying"],
                "strike_price": float(meta["strike_price"]),
                "option_type": meta["option_type"],
                "observed_rows": int(len(sub)),
                "settlement_dates": int(settlement["reference_date"].nunique()),
                "final_settlement_dates": int(final_settlement["reference_date"].nunique()),
                "actual_settlement_dates": int(actual_settlement["reference_date"].nunique()),
                "cleared_volume_dates": int(volume["reference_date"].nunique()),
                "open_interest_dates": int(oi["reference_date"].nunique()),
            }
        )
    instrument_coverage = pd.DataFrame(instrument_rows).sort_values(
        ["underlying", "strike_price", "option_type", "raw_symbol"]
    )

    dates = sorted(
        str(d)
        for d in options["reference_date"].dropna().unique().tolist()
        if target_start <= str(d) <= target_end
    )
    daily_rows: list[dict[str, Any]] = []
    for date in dates:
        day = options.loc[options["reference_date"].eq(date)]
        settlements = day.loc[day["stat_type"].eq(3)]
        finals = settlements.loc[settlements["settlement_final"]]
        actuals = settlements.loc[settlements["settlement_actual"]]
        volume = day.loc[day["stat_type"].eq(6)]
        oi = day.loc[day["stat_type"].eq(9)]
        daily_rows.append(
            {
                "reference_date": date,
                "instruments_any_stat": int(day["instrument_id"].nunique()),
                "settlement_instruments": int(settlements["instrument_id"].nunique()),
                "final_settlement_instruments": int(finals["instrument_id"].nunique()),
                "actual_settlement_instruments": int(actuals["instrument_id"].nunique()),
                "cleared_volume_instruments": int(volume["instrument_id"].nunique()),
                "open_interest_instruments": int(oi["instrument_id"].nunique()),
                "call_settlement_instruments": int(
                    settlements.loc[settlements["option_type"].eq("call"), "instrument_id"].nunique()
                ),
                "put_settlement_instruments": int(
                    settlements.loc[settlements["option_type"].eq("put"), "instrument_id"].nunique()
                ),
            }
        )
    daily_coverage = pd.DataFrame(daily_rows)

    selected_count = int(selected_norm["instrument_id"].nunique())
    settlement_instruments = int(
        options.loc[options["stat_type"].eq(3), "instrument_id"].nunique()
    )
    final_instruments = int(
        options.loc[
            options["stat_type"].eq(3) & options["settlement_final"], "instrument_id"
        ].nunique()
    )
    stat_types_options = sorted(int(x) for x in options["stat_type"].dropna().unique())
    stat_types_futures = sorted(int(x) for x in futures["stat_type"].dropna().unique())

    business_dates = [
        d.date().isoformat() for d in pd.date_range(target_start, target_end, freq="B")
    ]
    observed_dates = set(options["reference_date"].dropna().astype(str))
    settlement_dates = set(
        options.loc[options["stat_type"].eq(3), "reference_date"].dropna().astype(str)
    )
    futures_settlement_dates = set(
        futures.loc[futures["stat_type"].eq(3), "reference_date"].dropna().astype(str)
    )

    summary: dict[str, Any] = {
        "target_window": {"start": target_start, "end": target_end},
        "selected_option_instruments": selected_count,
        "option_statistics_rows": int(len(options)),
        "futures_statistics_rows": int(len(futures)),
        "option_stat_types": stat_types_options,
        "option_stat_type_names": [
            STAT_NAMES.get(x, f"stat_{x}") for x in stat_types_options
        ],
        "futures_stat_types": stat_types_futures,
        "futures_stat_type_names": [
            STAT_NAMES.get(x, f"stat_{x}") for x in stat_types_futures
        ],
        "option_reference_date_first": (
            None if options["reference_date"].dropna().empty else str(options["reference_date"].min())
        ),
        "option_reference_date_last": (
            None if options["reference_date"].dropna().empty else str(options["reference_date"].max())
        ),
        "target_business_dates": len(business_dates),
        "target_business_dates_with_any_option_stat": int(
            sum(d in observed_dates for d in business_dates)
        ),
        "target_business_dates_with_option_settlement": int(
            sum(d in settlement_dates for d in business_dates)
        ),
        "target_business_dates_with_futures_settlement": int(
            sum(d in futures_settlement_dates for d in business_dates)
        ),
        "option_instruments_with_settlement": settlement_instruments,
        "option_instruments_with_final_settlement": final_instruments,
        "all_selected_options_have_some_settlement": bool(
            settlement_instruments == selected_count
        ),
        "all_selected_options_have_some_final_settlement": bool(
            final_instruments == selected_count
        ),
        "glbx_direct_settlement_iv_available": False,
        "next_modeling_step": (
            "Infer vanilla implied volatility from official LO option settlements and CL "
            "futures settlements with an American futures-option model."
        ),
        "notes": [
            "Coverage uses CME trading reference date ts_ref when available.",
            "CME can publish multiple updates for one trading reference date.",
            "Settlement stat_flags bit 0 marks final vs preliminary; bit 1 marks actual vs theoretical.",
            "GLBX.MDP3 does not publish statistics stat_type=14; direct settlement IV is unavailable in this dataset.",
        ],
    }
    return stat_summary, instrument_coverage, daily_coverage, summary


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--data-dir",
        type=Path,
        default=ROOT / "data" / "databento" / "wti_external_q" / "raw",
    )
    parser.add_argument("--definition-date", default="2026-08-24")
    parser.add_argument("--download-start", default="2026-08-24")
    parser.add_argument("--download-end", default="2026-09-11")
    parser.add_argument("--target-start", default="2026-08-24")
    parser.add_argument("--target-end", default="2026-09-10")
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=ROOT / "results" / "analysis" / "wti_databento_external_q",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    selected_path = args.data_dir / f"lo_selected_{args.definition_date}.csv"
    option_path = (
        args.data_dir / f"lo_statistics_{args.download_start}_{args.download_end}.csv"
    )
    futures_path = (
        args.data_dir / f"cl_statistics_{args.download_start}_{args.download_end}.csv"
    )

    stat_summary, instrument_coverage, daily_coverage, summary = build_audit(
        selected=_load_csv(selected_path),
        option_stats=_load_csv(option_path),
        futures_stats=_load_csv(futures_path),
        target_start=args.target_start,
        target_end=args.target_end,
    )

    args.output_dir.mkdir(parents=True, exist_ok=True)
    stat_summary.to_csv(args.output_dir / "stat_type_summary.csv", index=False)
    instrument_coverage.to_csv(
        args.output_dir / "option_instrument_coverage.csv", index=False
    )
    daily_coverage.to_csv(args.output_dir / "option_daily_coverage.csv", index=False)
    (args.output_dir / "coverage_audit.json").write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
