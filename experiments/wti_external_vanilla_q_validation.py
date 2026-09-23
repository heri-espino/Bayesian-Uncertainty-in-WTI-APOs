"""Strict forward validation using independent vanilla-WTI implied volatility.

This experiment is the external-Q counterpart to wti_forward_q_validation. It
uses only Databento-derived LO implied-volatility information dated strictly
before each target APO valuation date.

For each vanilla date, a near-ATM volatility is available separately for CLX6
and CLZ6. To map those two maturity-specific vanilla states into the maintained
one-factor constant-volatility APO model, the primary scalar state is the
fixing-count-weighted root-mean-square volatility,

    sigma_eff = sqrt(sum_j w_j * sigma_j**2),

where w_j is the fraction of the target APO fixing schedule mapped to each CL
futures contract. For the pre-averaging October-2026 schedule this corresponds
to 14 CLX26 fixings and 8 CLZ26 fixings. A fixing-weighted arithmetic mean is
also recorded as a transparent aggregation sensitivity.

Two strictly prior information sets are reported:
- vanilla_previous_day: latest completed vanilla date before the target;
- vanilla_expanding: all earlier vanilla dates with exponential recency weights.

No same-day APO or vanilla information enters the target-date prediction.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

from experiments.wti_forward_q_validation import (
    _error_summary,
    _price_targets,
    _run_lookup,
)

DEFAULT_VANILLA_PATH = Path(
    "results/analysis/wti_databento_external_q/daily_vanilla_iv_summary.csv"
)
DEFAULT_APO_IV_PATH = Path(
    "results/analysis/wti_apo_implied_volatility/apo_contract_implied_volatility.csv"
)
DEFAULT_RUNS_ROOT = Path("results/wti_apo_empirical")
DEFAULT_OUTPUT_ROOT = Path(
    "results/analysis/wti_external_vanilla_q_validation"
)

_CL_LONG_RE = re.compile(
    r"^CL(?P<month>[FGHJKMNQUVXZ])(?P<year>\d{2}|20\d{2})$",
    re.IGNORECASE,
)


def _raw_cl_symbol(symbol: str) -> str:
    value = str(symbol).strip().upper()
    match = _CL_LONG_RE.fullmatch(value)
    if match is None:
        return value
    return f"CL{match.group('month').upper()}{match.group('year')[-1]}"


def _fixing_weights(run_dir: Path) -> dict[str, float]:
    path = run_dir / "apo_fixing_state.csv"
    if not path.exists():
        raise FileNotFoundError(path)
    state = pd.read_csv(path)
    if "contract" not in state.columns or state.empty:
        raise ValueError(f"{path} has no usable contract fixing map")
    raw = state["contract"].astype(str).map(_raw_cl_symbol)
    counts = raw.value_counts()
    total = float(counts.sum())
    return {str(k): float(v / total) for k, v in counts.items()}


def _effective_sigma(
    vanilla_date: pd.DataFrame,
    fixing_weights: dict[str, float],
    *,
    column: str,
    aggregation: str,
) -> float:
    required = set(fixing_weights)
    available = set(vanilla_date["underlying"].astype(str))
    missing = sorted(required.difference(available))
    if missing:
        raise ValueError(
            f"vanilla surface missing underlyings required by APO fixings: {missing}"
        )

    by_underlying = (
        vanilla_date.drop_duplicates("underlying", keep="last")
        .set_index("underlying")[column]
        .astype(float)
    )
    weights = np.array(
        [fixing_weights[u] for u in fixing_weights], dtype=float
    )
    sigma = np.array(
        [by_underlying.loc[u] for u in fixing_weights], dtype=float
    )
    if not np.all(np.isfinite(sigma)):
        raise ValueError("non-finite vanilla volatility in required underlying")

    weights = weights / weights.sum()
    if aggregation == "weighted_rms":
        return float(np.sqrt(np.sum(weights * sigma**2)))
    if aggregation == "weighted_mean":
        return float(np.sum(weights * sigma))
    raise ValueError(f"unknown aggregation: {aggregation}")


def _prior_sigma(
    vanilla: pd.DataFrame,
    *,
    target_date: pd.Timestamp,
    fixing_weights: dict[str, float],
    aggregation: str,
    half_life_days: float | None,
) -> tuple[float, str, int]:
    earlier = vanilla[vanilla["reference_ts"] < target_date].copy()
    if earlier.empty:
        raise ValueError("no earlier vanilla dates")

    latest = pd.Timestamp(earlier["reference_ts"].max()).normalize()
    if half_life_days is None:
        chosen = earlier[earlier["reference_ts"] == latest]
        sigma = _effective_sigma(
            chosen,
            fixing_weights,
            column="near_atm_median_iv",
            aggregation=aggregation,
        )
        return sigma, latest.strftime("%Y-%m-%d"), 1

    daily: list[tuple[pd.Timestamp, float]] = []
    for date_raw, group in earlier.groupby("reference_ts", sort=True):
        date = pd.Timestamp(date_raw).normalize()
        try:
            sigma = _effective_sigma(
                group,
                fixing_weights,
                column="near_atm_median_iv",
                aggregation=aggregation,
            )
        except ValueError:
            continue
        daily.append((date, sigma))
    if not daily:
        raise ValueError("no complete earlier vanilla dates")

    dates = pd.DatetimeIndex([x[0] for x in daily])
    sigmas = np.array([x[1] for x in daily], dtype=float)
    age = (target_date - dates).days.to_numpy(dtype=float)
    recency = np.exp(
        -np.log(2.0) * np.maximum(age, 0.0) / float(half_life_days)
    )
    recency = recency / recency.sum()

    # Average variance through time, consistent with the primary maturity
    # aggregation and with the maintained constant-volatility state.
    sigma = float(np.sqrt(np.sum(recency * sigmas**2)))
    return sigma, latest.strftime("%Y-%m-%d"), len(daily)


def _comparison_summary(
    external: pd.DataFrame,
    apo_forward_path: Path | None,
) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    for method, group in external.groupby("method", sort=True):
        for model, error_col in (
            ("external_vanilla_q", "forward_error"),
            ("baseline_pi", "baseline_pi_error"),
        ):
            e = group[error_col].to_numpy(dtype=float)
            rows.append(
                {
                    "method": method,
                    "model": model,
                    "n": int(len(group)),
                    "n_dates": int(group["valuation_date"].nunique()),
                    "mean_error": float(np.mean(e)),
                    "mae": float(np.mean(np.abs(e))),
                    "rmse": float(np.sqrt(np.mean(e**2))),
                }
            )

    if apo_forward_path is not None and apo_forward_path.exists():
        apo = pd.read_csv(apo_forward_path)
        external_dates = set(external["valuation_date"].astype(str))
        apo = apo[
            apo["valuation_date"].astype(str).isin(external_dates)
            & apo["apo_expiry"].astype(str).eq("2026-10")
        ].copy()
        mapping = {
            "previous_day_smile": "apo_previous_day_smile",
            "expanding_smile": "apo_expanding_smile",
        }
        for method, label in mapping.items():
            group = apo[apo["method"].eq(method)]
            if group.empty:
                continue
            e = group["forward_error"].to_numpy(dtype=float)
            rows.append(
                {
                    "method": label,
                    "model": "prior_date_apo_smile",
                    "n": int(len(group)),
                    "n_dates": int(group["valuation_date"].nunique()),
                    "mean_error": float(np.mean(e)),
                    "mae": float(np.mean(np.abs(e))),
                    "rmse": float(np.sqrt(np.mean(e**2))),
                }
            )
    return pd.DataFrame(rows)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--vanilla-path", type=Path, default=DEFAULT_VANILLA_PATH
    )
    parser.add_argument(
        "--apo-iv-path", type=Path, default=DEFAULT_APO_IV_PATH
    )
    parser.add_argument(
        "--runs-root", type=Path, default=DEFAULT_RUNS_ROOT
    )
    parser.add_argument(
        "--apo-forward-path",
        type=Path,
        default=(
            Path("results/analysis/wti_forward_q_validation")
            / "forward_q_predictions.csv"
        ),
    )
    parser.add_argument(
        "--output-root", type=Path, default=DEFAULT_OUTPUT_ROOT
    )
    parser.add_argument("--apo-expiry", default="2026-10")
    parser.add_argument("--half-life-days", type=float, default=5.0)
    parser.add_argument(
        "--aggregation",
        choices=("weighted_rms", "weighted_mean"),
        default="weighted_rms",
    )
    parser.add_argument("--force", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    args.output_root.mkdir(parents=True, exist_ok=True)
    output = args.output_root / "external_vanilla_q_predictions.csv"
    if output.exists() and not args.force:
        print(f"Reusing completed output: {output}", flush=True)
        return

    vanilla = pd.read_csv(args.vanilla_path)
    vanilla["reference_ts"] = pd.to_datetime(
        vanilla["reference_date"]
    ).dt.normalize()
    required = {
        "reference_date",
        "underlying",
        "near_atm_median_iv",
    }
    missing = required.difference(vanilla.columns)
    if missing:
        raise ValueError(
            f"vanilla summary missing columns: {sorted(missing)}"
        )

    apo = pd.read_csv(args.apo_iv_path)
    apo = apo[
        apo["apo_expiry"].astype(str).eq(args.apo_expiry)
        & apo["market_settlement"].notna()
    ].copy()
    apo["valuation_ts"] = pd.to_datetime(
        apo["valuation_date"]
    ).dt.normalize()

    lookup = _run_lookup(args.runs_root, [args.apo_expiry])
    rows: list[dict[str, Any]] = []

    for target_raw in sorted(apo["valuation_ts"].unique()):
        target_date = pd.Timestamp(target_raw).normalize()
        run_dir = lookup.get(
            (target_date.strftime("%Y-%m-%d"), args.apo_expiry)
        )
        if run_dir is None:
            continue
        target = apo[apo["valuation_ts"].eq(target_date)].copy()
        weights = _fixing_weights(run_dir)

        methods = {
            "vanilla_previous_day": None,
            "vanilla_expanding": float(args.half_life_days),
        }
        for method, half_life in methods.items():
            try:
                sigma_hat, training_end, n_dates = _prior_sigma(
                    vanilla,
                    target_date=target_date,
                    fixing_weights=weights,
                    aggregation=args.aggregation,
                    half_life_days=half_life,
                )
            except ValueError:
                continue

            sigma_vector = np.full(len(target), sigma_hat)
            prices = _price_targets(
                target, sigma_vector, run_dir=run_dir
            )

            for i, row in enumerate(target.itertuples(index=False)):
                market = float(row.market_settlement)
                baseline = float(row.baseline_pi_price)
                volume = (
                    float(row.volume)
                    if pd.notna(row.volume)
                    else np.nan
                )
                oi = (
                    float(row.open_interest)
                    if pd.notna(row.open_interest)
                    else np.nan
                )
                rows.append(
                    {
                        "method": method,
                        "valuation_date": target_date.strftime("%Y-%m-%d"),
                        "apo_expiry": args.apo_expiry,
                        "training_end_date": training_end,
                        "n_training_dates": int(n_dates),
                        "aggregation": args.aggregation,
                        "fixing_weights_json": json.dumps(
                            weights, sort_keys=True
                        ),
                        "contract_id": str(row.contract_id),
                        "option_type": str(row.option_type),
                        "strike": float(row.strike),
                        "log_moneyness": float(row.log_moneyness),
                        "market_settlement": market,
                        "open_interest": oi,
                        "volume": volume,
                        "positive_volume": bool(
                            np.isfinite(volume) and volume > 0
                        ),
                        "predicted_sigma_q": sigma_hat,
                        "observed_same_day_apo_implied_sigma_q": (
                            float(row.apo_implied_sigma_q)
                            if pd.notna(row.apo_implied_sigma_q)
                            else np.nan
                        ),
                        "forward_q_price": float(prices[i]),
                        "forward_error": float(prices[i] - market),
                        "baseline_pi_price": baseline,
                        "baseline_pi_error": float(
                            baseline - market
                        ),
                    }
                )

    result = pd.DataFrame(rows)
    if result.empty:
        raise RuntimeError(
            "no strict external-vanilla Q predictions could be produced"
        )
    if not (
        pd.to_datetime(result["training_end_date"])
        < pd.to_datetime(result["valuation_date"])
    ).all():
        raise RuntimeError(
            "information guardrail failed: non-prior vanilla date detected"
        )

    result.to_csv(output, index=False)
    error_summary = _error_summary(result)
    error_summary.to_csv(
        args.output_root / "external_vanilla_q_error_summary.csv",
        index=False,
    )
    comparison = _comparison_summary(
        result, args.apo_forward_path
    )
    comparison.to_csv(
        args.output_root / "external_q_comparison.csv",
        index=False,
    )

    state = (
        result[
            [
                "method",
                "valuation_date",
                "training_end_date",
                "n_training_dates",
                "aggregation",
                "fixing_weights_json",
                "predicted_sigma_q",
            ]
        ]
        .drop_duplicates()
        .sort_values(["method", "valuation_date"])
    )
    state.to_csv(
        args.output_root / "external_vanilla_q_state.csv",
        index=False,
    )

    report = {
        "apo_expiry": args.apo_expiry,
        "aggregation": args.aggregation,
        "prediction_rows": int(len(result)),
        "target_dates": int(result["valuation_date"].nunique()),
        "methods": sorted(result["method"].unique().tolist()),
        "information_guardrail": (
            "Every external vanilla sigma_Q uses only Databento-derived "
            "LO implied-volatility dates strictly earlier than the target "
            "APO valuation date."
        ),
        "maturity_mapping": (
            "Near-ATM CLX6 and CLZ6 volatilities are reduced to the "
            "maintained scalar APO volatility state using target fixing-"
            "count weights. Primary aggregation is weighted RMS variance."
        ),
        "same_day_apo_usage": (
            "Same-day APO implied volatility is retained only as an ex-post "
            "diagnostic and never enters external-Q fitting or pricing."
        ),
    }
    (
        args.output_root / "external_vanilla_q_report.json"
    ).write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
