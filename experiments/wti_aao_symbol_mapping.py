"""Offline AAO embedded-DBN-symbol mapping audit.

Databento DBNStore.to_df(map_symbols=True) maps record-level instrument
identifiers to publisher raw symbols using local DBN metadata. Compare the
mapped symbols against in-file definition identities, in bounded months.

Exploratory aggregate counts only: not a canonical instrument master,
revision-resolved settlement panel, executable trade series, or backtest.
Never contacts Databento, prints raw symbols, or exports prices.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "databento" / "wti_aao_bulk" / "raw"
OUTPUT = (ROOT / "results" / "analysis"
          / "wti_aao_history_feasibility" / "symbol_mapping")
FINGERPRINT = [
    "instrument_class", "expiration", "strike_price",
    "exchange", "underlying", "asset",
]


def _text(series: pd.Series) -> pd.Series:
    return series.astype("string").str.strip()


def _dates(series: pd.Series) -> pd.Series:
    if pd.api.types.is_numeric_dtype(series):
        result = pd.to_datetime(series, unit="ns", utc=True, errors="coerce")
    else:
        result = pd.to_datetime(series, utc=True, errors="coerce")
    return result.dt.strftime("%Y-%m-%d")


def assess(definitions: pd.DataFrame, statistics: pd.DataFrame) -> dict[str, Any]:
    """Count event-level symbol coverage and reject ambiguous identities."""
    required_def = {
        "publisher_id", "raw_symbol", "asset", "instrument_class",
        "leg_count", *FINGERPRINT,
    }
    required_stats = {
        "publisher_id", "symbol", "stat_type", "stat_flags", "ts_ref",
    }
    missing_d = sorted(required_def - set(definitions.columns))
    missing_s = sorted(required_stats - set(statistics.columns))
    if missing_d or missing_s:
        raise ValueError(
            f"Missing definition fields={missing_d}; statistics fields={missing_s}"
        )

    types = pd.to_numeric(statistics["stat_type"], errors="coerce")
    if not types.eq(3).any():
        raise ValueError("No recognized settlement stat_type=3")
    settlements = statistics.loc[types.eq(3), [
        "publisher_id", "symbol", "stat_flags", "ts_ref"
    ]].copy()
    flags = pd.to_numeric(settlements["stat_flags"], errors="coerce")
    if flags.isna().any():
        raise ValueError("Settlement flags contain unknown values")
    final_mask = flags.astype("int64").mod(2).eq(1)
    final = settlements.loc[final_mask].copy()
    final_flags = flags.loc[final_mask].astype("int64")
    if final.empty:
        raise ValueError("No final settlements in the selected month")
    final["_symbol"] = _text(final["symbol"])
    valid_symbol = (
        final["_symbol"].notna()
        & final["_symbol"].str.len().gt(0).fillna(False)
        & ~final["_symbol"].str.upper().isin(
            ("NAN", "NONE", "NULL", "UNKNOWN", "<UNDEF>")
        ).fillna(True)
    )
    final["_ref_date"] = _dates(final["ts_ref"])
    if final["_ref_date"].isna().any():
        raise ValueError("Final settlement contains undefined ts_ref")
    final["publisher_id"] = pd.to_numeric(
        final["publisher_id"], errors="raise"
    ).astype("int64")

    d = definitions[[
        "publisher_id", "raw_symbol", "leg_count", *FINGERPRINT,
    ]].copy()
    d["publisher_id"] = pd.to_numeric(
        d["publisher_id"], errors="raise"
    ).astype("int64")
    d["_raw_symbol"] = _text(d["raw_symbol"])
    d = d.loc[d["_raw_symbol"].notna() & d["_raw_symbol"].str.len().gt(0)].copy()
    if d.empty:
        raise ValueError("No raw_symbol definitions available")
    d["_outright"] = (
        _text(d["asset"]).eq("AAO").fillna(False)
        & _text(d["instrument_class"]).isin(["C", "P"])
        & pd.to_numeric(d["leg_count"], errors="coerce").eq(0)
    )
    for col in FINGERPRINT:
        d[col] = _text(d[col]).fillna("<missing>")
    d["_identity"] = d[FINGERPRINT].agg("|".join, axis=1)
    groups = d.groupby(
        ["publisher_id", "_raw_symbol"], as_index=False, sort=False
    ).agg(
        distinct_identities=("_identity", "nunique"),
        all_outright=("_outright", "all"),
    )
    groups["_safe"] = (
        groups["distinct_identities"].eq(1) & groups["all_outright"]
    )

    available = final.loc[valid_symbol, [
        "publisher_id", "_symbol", "_ref_date"
    ]].copy()
    matched = available.merge(
        groups, how="left",
        left_on=["publisher_id", "_symbol"],
        right_on=["publisher_id", "_raw_symbol"],
        validate="many_to_one", sort=False,
    )
    has_def = matched["distinct_identities"].notna()
    safe = matched["_safe"].fillna(False).astype(bool)
    usable = matched.loc[safe, [
        "publisher_id", "_symbol", "_ref_date"
    ]]
    # Keys are only tentative, though matched symbol is less vulnerable to
    # daily numeric instrument_id reuse than joining instrument IDs alone.
    keys = usable.drop_duplicates()
    return {
        "source": "local DBNStore.to_df(map_symbols=True)",
        "no_network_requests": True,
        "definition_events": int(len(definitions)),
        "settlement_events": int(len(settlements)),
        "final_settlement_events": int(len(final)),
        "final_actual_events": int((final_flags & 2).eq(2).sum()),
        "final_theoretical_events": int((final_flags & 2).eq(0).sum()),
        "final_events_with_nonempty_mapped_symbol": int(valid_symbol.sum()),
        "final_events_without_mapped_symbol": int((~valid_symbol).sum()),
        "final_mapped_events_with_matching_raw_symbol": int(has_def.sum()),
        "final_mapped_events_missing_matching_definition": int((~has_def).sum()),
        "final_mapped_events_with_unambiguous_outright_identity": int(safe.sum()),
        "final_mapped_events_with_ambiguous_or_non_outright_identity": int(
            (has_def & ~safe).sum()
        ),
        "definition_publisher_symbol_groups": int(len(groups)),
        "definition_symbol_groups_with_multiple_contract_fingerprints": int(
            groups["distinct_identities"].gt(1).sum()
        ),
        "tentative_unique_out_right_symbol_reference_date_keys": int(len(keys)),
        "matched_reference_dates": int(keys["_ref_date"].nunique()),
        "warning": (
            "A mapped symbol is only a candidate historical contract identity. "
            "Symbols can be reused, correction/deletion and publication time "
            "are not resolved, and this is not a model-validation panel."
        ),
    }


def run(month: str, data_dir: Path, output_dir: Path) -> dict[str, Any]:
    import databento as db

    paths = sorted(data_dir.glob(f"aao_definition__{month}-*.dbn.zst"))
    if len(paths) != 1:
        raise FileNotFoundError(
            f"Expected one definition DBN file for {month}; found {len(paths)}"
        )
    stat = data_dir / paths[0].name.replace(
        "aao_definition__", "aao_statistics__", 1
    )
    if not stat.is_file():
        raise FileNotFoundError(f"Missing statistics DBN for {month}")
    defs = db.DBNStore.from_file(paths[0]).to_df(map_symbols=True)
    stats = db.DBNStore.from_file(stat).to_df(map_symbols=True)
    result = assess(defs, stats)
    result["month"] = month
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / f"mapped_symbol_{month}.json").write_text(
        json.dumps(result, indent=2) + "\n", encoding="utf-8"
    )
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--months", nargs="+", default=["2021-02", "2026-06"])
    parser.add_argument("--data-dir", type=Path, default=RAW)
    parser.add_argument("--output-dir", type=Path, default=OUTPUT)
    args = parser.parse_args()
    for month in args.months:
        print(json.dumps(run(month, args.data_dir, args.output_dir), indent=2))


if __name__ == "__main__":
    main()
