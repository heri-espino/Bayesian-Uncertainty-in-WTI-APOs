"""Build contract-level WTI vanilla implied volatilities from Databento settlements.

This experiment uses only locally cached Databento GLBX.MDP3 records:
- official final LO option settlements;
- official final CL futures settlements;
- option definitions carrying strike, underlying and expiration.

No APO price enters the inversion. Standard monthly LO is American style, so
the primary inversion uses the reusable CRR American futures-option pricer.
Treasury par yields are used under the same explicitly labelled zero-rate proxy
already used elsewhere in the empirical WTI pipeline.

The output is intentionally contract-level. Aggregation/interpolation to the
APO fixing horizon is a separate stage so strike and liquidity diagnostics can
be inspected first.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

from bayesian_asian_options.american_futures_option import (
    implied_volatility_american_futures,
)
from bayesian_asian_options.databento_wti import (
    final_settlements,
    load_databento_csv,
    normalize_option_definitions,
    normalize_statistics,
)
from bayesian_asian_options.rates import (
    download_treasury_par_yield_csv,
    load_treasury_par_yields,
    treasury_curve_on_or_before,
)

ROOT = Path(__file__).resolve().parents[1]


def _latest_reference_stat(
    frame: pd.DataFrame,
    stat_type: int,
) -> pd.DataFrame:
    stats = normalize_statistics(frame)
    subset = stats.loc[stats["stat_type"].eq(stat_type)].copy()
    if subset.empty:
        return subset
    subset = subset.sort_values(
        ["instrument_id", "reference_date", "received_timestamp"]
    )
    return subset.drop_duplicates(
        ["instrument_id", "reference_date"], keep="last"
    ).reset_index(drop=True)


def _load_rates(
    treasury_dir: Path,
    *,
    year: int,
    allow_download: bool,
) -> pd.DataFrame:
    treasury_dir.mkdir(parents=True, exist_ok=True)
    paths = sorted(treasury_dir.glob("*.csv"))
    if not paths and allow_download:
        path = treasury_dir / f"treasury_par_yields_{year}.csv"
        download_treasury_par_yield_csv(year, path)
        paths = [path]
    if not paths:
        raise RuntimeError(
            f"No Treasury CSV found under {treasury_dir}. "
            "Use --download-treasury or add the official file."
        )
    return load_treasury_par_yields(paths)


def _underlying_settlements(
    futures_stats: pd.DataFrame,
    definitions: pd.DataFrame,
) -> pd.DataFrame:
    futures = final_settlements(futures_stats)
    lookup = (
        definitions[["underlying_id", "underlying"]]
        .drop_duplicates()
        .rename(columns={"underlying_id": "instrument_id"})
    )
    lookup["instrument_id"] = pd.to_numeric(
        lookup["instrument_id"], errors="coerce"
    ).astype("Int64")

    matched = futures.merge(
        lookup,
        on="instrument_id",
        how="inner",
        validate="many_to_one",
    )

    # Databento to_df() normally includes a mapped raw symbol. Keep a fallback
    # in case instrument IDs in a historical slice do not match the definition
    # snapshot but symbol mappings are present.
    expected = set(definitions["underlying"].astype(str).unique())
    found = set(matched["underlying"].astype(str).unique())
    missing = expected.difference(found)
    if missing and "symbol" in futures.columns:
        fallback = futures.loc[
            futures["symbol"].astype(str).isin(missing)
        ].copy()
        if not fallback.empty:
            fallback["underlying"] = fallback["symbol"].astype(str)
            matched = pd.concat([matched, fallback], ignore_index=True)

    matched = matched.sort_values(
        ["underlying", "reference_date", "received_timestamp"]
    ).drop_duplicates(
        ["underlying", "reference_date"], keep="last"
    )
    return matched.reset_index(drop=True)


def _attach_diagnostics(
    panel: pd.DataFrame,
    option_stats: pd.DataFrame,
) -> pd.DataFrame:
    out = panel.copy()
    for stat_type, label in ((6, "cleared_volume"), (9, "open_interest")):
        stat = _latest_reference_stat(option_stats, stat_type)
        if stat.empty:
            out[label] = np.nan
            continue
        value_col = "quantity" if "quantity" in stat.columns else "price"
        stat = stat[
            ["instrument_id", "reference_date", value_col]
        ].rename(columns={value_col: label})
        out = out.merge(
            stat,
            on=["instrument_id", "reference_date"],
            how="left",
            validate="many_to_one",
        )
    return out


def build_iv_panel(
    *,
    definitions: pd.DataFrame,
    option_stats: pd.DataFrame,
    futures_stats: pd.DataFrame,
    treasury: pd.DataFrame,
    steps: int,
    sigma_upper: float,
) -> pd.DataFrame:
    """Build the contract-date American implied-volatility panel."""
    definitions = normalize_option_definitions(definitions)
    options = final_settlements(option_stats)
    futures = _underlying_settlements(futures_stats, definitions)

    metadata_cols = [
        "instrument_id",
        "raw_symbol",
        "underlying_id",
        "underlying",
        "strike_price",
        "option_type",
        "expiration_timestamp",
    ]
    metadata = definitions[metadata_cols].drop_duplicates(
        "instrument_id", keep="last"
    )
    options = options.merge(
        metadata,
        on="instrument_id",
        how="inner",
        validate="many_to_one",
    )

    future_cols = [
        "underlying",
        "reference_date",
        "price",
        "received_timestamp",
        "settlement_actual",
        "settlement_final",
    ]
    futures = futures[future_cols].rename(
        columns={
            "price": "futures_settlement",
            "received_timestamp": "futures_received_timestamp",
            "settlement_actual": "futures_settlement_actual",
            "settlement_final": "futures_settlement_final",
        }
    )

    panel = options.merge(
        futures,
        on=["underlying", "reference_date"],
        how="left",
        validate="many_to_one",
    ).rename(
        columns={
            "price": "option_settlement",
            "received_timestamp": "option_received_timestamp",
            "settlement_actual": "option_settlement_actual",
            "settlement_final": "option_settlement_final",
        }
    )

    panel = _attach_diagnostics(panel, option_stats)
    rows: list[dict[str, Any]] = []

    for row in panel.itertuples(index=False):
        option_received = pd.Timestamp(row.option_received_timestamp)
        futures_received = pd.Timestamp(row.futures_received_timestamp)
        expiry = pd.Timestamp(row.expiration_timestamp)

        if pd.isna(futures_received) or pd.isna(row.futures_settlement):
            rows.append(
                {
                    **row._asdict(),
                    "asof_timestamp": pd.NaT,
                    "maturity_years": np.nan,
                    "rate_proxy": np.nan,
                    "log_moneyness": np.nan,
                    "implied_volatility": np.nan,
                    "iv_status": "missing_futures_settlement",
                    "iv_model_price": np.nan,
                    "intrinsic_value": np.nan,
                }
            )
            continue

        asof_timestamp = max(option_received, futures_received)
        seconds = (expiry - asof_timestamp).total_seconds()
        maturity_years = max(0.0, seconds / (365.25 * 24.0 * 3600.0))

        curve = treasury_curve_on_or_before(
            treasury,
            pd.Timestamp(row.reference_date),
        )
        rate = curve.interpolated_par_yield(maturity_years)

        result = implied_volatility_american_futures(
            float(row.option_settlement),
            float(row.futures_settlement),
            float(row.strike_price),
            maturity_years,
            rate,
            str(row.option_type),
            steps=steps,
            sigma_upper=sigma_upper,
        )
        rows.append(
            {
                **row._asdict(),
                "asof_timestamp": asof_timestamp,
                "maturity_years": maturity_years,
                "rate_proxy": rate,
                "rate_source_date": curve.source_date.date().isoformat(),
                "log_moneyness": float(
                    np.log(
                        float(row.strike_price)
                        / float(row.futures_settlement)
                    )
                ),
                "implied_volatility": result.sigma,
                "iv_status": result.status,
                "iv_model_price": result.model_price,
                "intrinsic_value": result.intrinsic_value,
            }
        )

    out = pd.DataFrame(rows)
    if not out.empty:
        out["reference_date"] = out["reference_date"].astype(str)
        out = out.sort_values(
            [
                "reference_date",
                "underlying",
                "strike_price",
                "option_type",
            ]
        ).reset_index(drop=True)
    return out


def summarize_iv_panel(
    panel: pd.DataFrame,
    *,
    near_atm_log_moneyness: float,
) -> tuple[pd.DataFrame, dict[str, Any]]:
    """Return underlying-date surface summaries and global diagnostics."""
    good = panel.loc[
        panel["iv_status"].isin({"ok", "ok_lower_bound"})
        & np.isfinite(panel["implied_volatility"])
    ].copy()
    good["near_atm"] = (
        good["log_moneyness"].abs() <= near_atm_log_moneyness
    )

    daily_rows: list[dict[str, Any]] = []
    for (date, underlying), group in good.groupby(
        ["reference_date", "underlying"], sort=True
    ):
        near = group.loc[group["near_atm"]]
        source = near if not near.empty else group
        daily_rows.append(
            {
                "reference_date": date,
                "underlying": underlying,
                "n_iv": int(len(group)),
                "n_near_atm_iv": int(len(near)),
                "median_iv": float(group["implied_volatility"].median()),
                "near_atm_median_iv": float(
                    source["implied_volatility"].median()
                ),
                "near_atm_mean_iv": float(
                    source["implied_volatility"].mean()
                ),
                "near_atm_min_abs_log_moneyness": float(
                    source["log_moneyness"].abs().min()
                ),
                "calls": int(group["option_type"].eq("call").sum()),
                "puts": int(group["option_type"].eq("put").sum()),
                "actual_option_settlements": int(
                    group["option_settlement_actual"].sum()
                ),
                "theoretical_option_settlements": int(
                    (~group["option_settlement_actual"]).sum()
                ),
            }
        )
    daily = pd.DataFrame(daily_rows)

    statuses = {
        str(k): int(v)
        for k, v in panel["iv_status"].value_counts(dropna=False).items()
    }
    summary: dict[str, Any] = {
        "rows": int(len(panel)),
        "successful_iv_rows": int(len(good)),
        "successful_iv_fraction": (
            float(len(good) / len(panel)) if len(panel) else 0.0
        ),
        "reference_dates": int(
            panel["reference_date"].nunique()
        ),
        "underlyings": sorted(
            panel["underlying"].dropna().astype(str).unique().tolist()
        ),
        "iv_status_counts": statuses,
        "actual_option_settlement_rows": int(
            panel["option_settlement_actual"].fillna(False).sum()
        ),
        "theoretical_option_settlement_rows": int(
            (~panel["option_settlement_actual"].fillna(False)).sum()
        ),
        "near_atm_abs_log_moneyness_threshold": (
            near_atm_log_moneyness
        ),
        "median_successful_iv": (
            None
            if good.empty
            else float(good["implied_volatility"].median())
        ),
        "min_successful_iv": (
            None
            if good.empty
            else float(good["implied_volatility"].min())
        ),
        "max_successful_iv": (
            None
            if good.empty
            else float(good["implied_volatility"].max())
        ),
        "next_step": (
            "Inspect smile/actual-vs-theoretical diagnostics, then define "
            "strict t-1 strike/maturity aggregation to the APO fixing horizon."
        ),
    }
    return daily, summary


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--data-dir",
        type=Path,
        default=(
            ROOT / "data" / "databento" / "wti_external_q" / "raw"
        ),
    )
    parser.add_argument("--definition-date", default="2026-08-24")
    parser.add_argument("--download-start", default="2026-08-24")
    parser.add_argument("--download-end", default="2026-09-11")
    parser.add_argument(
        "--treasury-dir",
        type=Path,
        default=ROOT / "data" / "rates" / "treasury",
    )
    parser.add_argument("--download-treasury", action="store_true")
    parser.add_argument("--steps", type=int, default=160)
    parser.add_argument("--sigma-upper", type=float, default=3.0)
    parser.add_argument(
        "--near-atm-log-moneyness", type=float, default=0.03
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=(
            ROOT
            / "results"
            / "analysis"
            / "wti_databento_external_q"
        ),
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.steps < 25:
        raise ValueError("--steps must be at least 25")
    if args.sigma_upper <= 0:
        raise ValueError("--sigma-upper must be positive")

    definitions = load_databento_csv(
        args.data_dir / f"lo_selected_{args.definition_date}.csv"
    )
    option_stats = load_databento_csv(
        args.data_dir
        / f"lo_statistics_{args.download_start}_{args.download_end}.csv"
    )
    futures_stats = load_databento_csv(
        args.data_dir
        / f"cl_statistics_{args.download_start}_{args.download_end}.csv"
    )
    treasury = _load_rates(
        args.treasury_dir,
        year=2026,
        allow_download=args.download_treasury,
    )

    panel = build_iv_panel(
        definitions=definitions,
        option_stats=option_stats,
        futures_stats=futures_stats,
        treasury=treasury,
        steps=args.steps,
        sigma_upper=args.sigma_upper,
    )
    daily, summary = summarize_iv_panel(
        panel,
        near_atm_log_moneyness=args.near_atm_log_moneyness,
    )
    summary.update(
        {
            "american_tree_steps": args.steps,
            "sigma_upper": args.sigma_upper,
            "rate_model": (
                "dated U.S. Treasury par yield interpolated in maturity "
                "and treated as a continuously compounded zero-rate proxy"
            ),
            "raw_data_committed": False,
        }
    )

    args.output_dir.mkdir(parents=True, exist_ok=True)
    panel.to_csv(
        args.output_dir / "vanilla_iv_panel.csv", index=False
    )
    daily.to_csv(
        args.output_dir / "daily_vanilla_iv_summary.csv", index=False
    )
    (
        args.output_dir / "iv_inversion_summary.json"
    ).write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
