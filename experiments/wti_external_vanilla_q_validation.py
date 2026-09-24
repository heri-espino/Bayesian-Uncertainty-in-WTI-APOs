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
    _fit_smile,
    _predict,
    _price_targets,
    _run_lookup,
)

DEFAULT_VANILLA_PATH = Path(
    "results/analysis/wti_databento_external_q/daily_vanilla_iv_summary.csv"
)
DEFAULT_VANILLA_PANEL_PATH = Path(
    "results/analysis/wti_databento_external_q/vanilla_iv_panel.csv"
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



def _target_futures_curve(run_dir: Path) -> dict[str, float]:
    path = run_dir / "valuation_cl_curve.csv"
    if not path.exists():
        raise FileNotFoundError(path)
    curve = pd.read_csv(path)
    required = {"contract", "settlement"}
    missing = required.difference(curve.columns)
    if missing:
        raise ValueError(
            f"{path} missing columns: {sorted(missing)}"
        )
    curve = curve.dropna(subset=["contract", "settlement"]).copy()
    curve["raw_underlying"] = curve["contract"].astype(str).map(
        _raw_cl_symbol
    )
    curve["settlement"] = pd.to_numeric(
        curve["settlement"], errors="coerce"
    )
    curve = curve.dropna(subset=["settlement"])
    return {
        str(row.raw_underlying): float(row.settlement)
        for row in curve.itertuples(index=False)
    }


def _fit_surface_models(
    vanilla_panel: pd.DataFrame,
    *,
    target_date: pd.Timestamp,
    half_life_days: float | None,
    ridge: float,
) -> tuple[
    dict[str, np.ndarray],
    dict[tuple[str, str], tuple[float, float]],
    str,
    int,
]:
    earlier = vanilla_panel[
        vanilla_panel["reference_ts"] < target_date
    ].copy()
    earlier = earlier[
        earlier["iv_status"].isin({"ok", "ok_lower_bound"})
        & np.isfinite(earlier["implied_volatility"])
        & np.isfinite(earlier["log_moneyness"])
    ].copy()
    if earlier.empty:
        raise ValueError("no earlier contract-level vanilla IVs")

    latest = pd.Timestamp(
        earlier["reference_ts"].max()
    ).normalize()
    if half_life_days is None:
        train = earlier[
            earlier["reference_ts"].eq(latest)
        ].copy()
        fit_half_life = None
        n_dates = 1
    else:
        train = earlier.copy()
        fit_half_life = float(half_life_days)
        n_dates = int(train["reference_ts"].nunique())

    models: dict[str, np.ndarray] = {}
    supports: dict[tuple[str, str], tuple[float, float]] = {}
    for underlying, group in train.groupby("underlying", sort=True):
        if len(group) < 6:
            continue
        fit_frame = group.rename(
            columns={
                "implied_volatility": "apo_implied_sigma_q",
                "reference_date": "valuation_date",
            }
        ).copy()
        beta = _fit_smile(
            fit_frame,
            target_date=target_date,
            ridge=float(ridge),
            half_life_days=fit_half_life,
        )
        models[str(underlying)] = beta
        for option_type, side in group.groupby(
            "option_type", sort=True
        ):
            x = side["log_moneyness"].to_numpy(dtype=float)
            supports[(str(underlying), str(option_type))] = (
                float(np.min(x)),
                float(np.max(x)),
            )

    if not models:
        raise ValueError("no vanilla smile model could be fitted")
    return (
        models,
        supports,
        latest.strftime("%Y-%m-%d"),
        n_dates,
    )


def _surface_sigma_targets(
    targets: pd.DataFrame,
    *,
    models: dict[str, np.ndarray],
    supports: dict[tuple[str, str], tuple[float, float]],
    target_futures: dict[str, float],
    fixing_weights: dict[str, float],
) -> tuple[np.ndarray, np.ndarray]:
    required = set(fixing_weights)
    missing_models = sorted(required.difference(models))
    missing_futures = sorted(required.difference(target_futures))
    if missing_models:
        raise ValueError(
            f"missing vanilla smile models: {missing_models}"
        )
    if missing_futures:
        raise ValueError(
            f"missing target futures settlements: {missing_futures}"
        )

    sigma_out = np.empty(len(targets), dtype=float)
    clipped_out = np.zeros(len(targets), dtype=int)

    for i, row in enumerate(targets.itertuples(index=False)):
        component_sigmas: list[float] = []
        component_weights: list[float] = []
        clipped = 0

        for underlying, weight in fixing_weights.items():
            key = (str(underlying), str(row.option_type))
            if key not in supports:
                raise ValueError(
                    f"missing smile support for {key}"
                )
            fwd = float(target_futures[underlying])
            raw_x = float(np.log(float(row.strike) / fwd))
            lo, hi = supports[key]
            x = float(np.clip(raw_x, lo, hi))
            clipped += int(x != raw_x)

            target_design = pd.DataFrame(
                {
                    "log_moneyness": [x],
                    "option_type": [str(row.option_type)],
                }
            )
            sigma = float(
                _predict(target_design, models[underlying])[0]
            )
            component_sigmas.append(sigma)
            component_weights.append(float(weight))

        weights = np.asarray(component_weights, dtype=float)
        weights = weights / weights.sum()
        sigmas = np.asarray(component_sigmas, dtype=float)
        sigma_out[i] = float(
            np.sqrt(np.sum(weights * sigmas**2))
        )
        clipped_out[i] = clipped

    return sigma_out, clipped_out

def _metrics(
    frame: pd.DataFrame,
    *,
    method: str,
    model: str,
    error_col: str,
    sample: str,
) -> dict[str, Any]:
    e = frame[error_col].to_numpy(dtype=float)
    return {
        "sample": sample,
        "method": method,
        "model": model,
        "n": int(len(frame)),
        "n_dates": int(frame["valuation_date"].nunique()),
        "mean_error": float(np.mean(e)),
        "mae": float(np.mean(np.abs(e))),
        "rmse": float(np.sqrt(np.mean(e**2))),
    }


def _comparison_summary(
    external: pd.DataFrame,
    apo_forward_path: Path | None,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Return full-sample and exact common-contract comparison tables."""
    rows: list[dict[str, Any]] = []
    for method, group in external.groupby("method", sort=True):
        rows.append(
            _metrics(
                group,
                method=method,
                model="external_vanilla_q",
                error_col="forward_error",
                sample="method_available",
            )
        )
        rows.append(
            _metrics(
                group,
                method=method,
                model="baseline_pi",
                error_col="baseline_pi_error",
                sample="method_available",
            )
        )

    if apo_forward_path is None or not apo_forward_path.exists():
        return pd.DataFrame(rows), pd.DataFrame()

    apo = pd.read_csv(apo_forward_path)
    apo = apo[
        apo["apo_expiry"].astype(str).eq("2026-10")
    ].copy()
    mapping = {
        "previous_day_smile": "apo_previous_day_smile",
        "expanding_smile": "apo_expanding_smile",
    }
    for method, label in mapping.items():
        group = apo[apo["method"].eq(method)].copy()
        if group.empty:
            continue
        rows.append(
            _metrics(
                group,
                method=label,
                model="prior_date_apo_smile",
                error_col="forward_error",
                sample="method_available",
            )
        )

    key_cols = ["valuation_date", "apo_expiry", "contract_id"]
    required_external = ["vanilla_previous_day", "vanilla_expanding"]
    required_apo = ["previous_day_smile", "expanding_smile"]

    key_sets: list[set[tuple[str, str, str]]] = []
    for method in required_external:
        group = external[external["method"].eq(method)]
        keys = set(
            map(
                tuple,
                group[key_cols].astype(str).to_numpy(),
            )
        )
        if keys:
            key_sets.append(keys)
    for method in required_apo:
        group = apo[apo["method"].eq(method)]
        keys = set(
            map(
                tuple,
                group[key_cols].astype(str).to_numpy(),
            )
        )
        if keys:
            key_sets.append(keys)

    if len(key_sets) != 4:
        return pd.DataFrame(rows), pd.DataFrame()

    common_keys = set.intersection(*key_sets)
    if not common_keys:
        return pd.DataFrame(rows), pd.DataFrame()

    def on_common(frame: pd.DataFrame) -> pd.DataFrame:
        key = pd.MultiIndex.from_frame(
            frame[key_cols].astype(str)
        )
        wanted = pd.MultiIndex.from_tuples(
            sorted(common_keys), names=key_cols
        )
        return frame.loc[key.isin(wanted)].copy()

    matched_rows: list[dict[str, Any]] = []

    # One baseline row is enough because baseline PI is contract-date specific,
    # not method specific. Verify consistency across the two external methods.
    baseline_source = on_common(
        external[
            external["method"].eq("vanilla_previous_day")
        ].copy()
    )
    matched_rows.append(
        _metrics(
            baseline_source,
            method="historical_pi",
            model="baseline_pi",
            error_col="baseline_pi_error",
            sample="common_contract_dates",
        )
    )

    for method in required_external:
        group = on_common(
            external[external["method"].eq(method)].copy()
        )
        matched_rows.append(
            _metrics(
                group,
                method=method,
                model="external_vanilla_q",
                error_col="forward_error",
                sample="common_contract_dates",
            )
        )

    for method, label in mapping.items():
        group = on_common(
            apo[apo["method"].eq(method)].copy()
        )
        matched_rows.append(
            _metrics(
                group,
                method=label,
                model="prior_date_apo_smile",
                error_col="forward_error",
                sample="common_contract_dates",
            )
        )

    matched = pd.DataFrame(matched_rows)
    if not matched.empty:
        expected_n = len(common_keys)
        if not matched["n"].eq(expected_n).all():
            raise RuntimeError(
                "matched comparison did not preserve the exact common "
                "contract-date sample"
            )
    return pd.DataFrame(rows), matched


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--vanilla-path", type=Path, default=DEFAULT_VANILLA_PATH
    )
    parser.add_argument(
        "--vanilla-panel-path",
        type=Path,
        default=DEFAULT_VANILLA_PANEL_PATH,
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
    parser.add_argument("--surface-ridge", type=float, default=1e-6)
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

    vanilla_panel = pd.read_csv(args.vanilla_panel_path)
    vanilla_panel["reference_ts"] = pd.to_datetime(
        vanilla_panel["reference_date"]
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
                        "surface_components_clipped": np.nan,
                    }
                )

        surface_methods = {
            "vanilla_surface_previous_day": None,
            "vanilla_surface_expanding": float(args.half_life_days),
        }
        target_futures = _target_futures_curve(run_dir)
        for method, half_life in surface_methods.items():
            try:
                models, supports, training_end, n_dates = (
                    _fit_surface_models(
                        vanilla_panel,
                        target_date=target_date,
                        half_life_days=half_life,
                        ridge=float(args.surface_ridge),
                    )
                )
                sigma_vector, clipped = _surface_sigma_targets(
                    target,
                    models=models,
                    supports=supports,
                    target_futures=target_futures,
                    fixing_weights=weights,
                )
            except ValueError:
                continue

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
                        "aggregation": "surface_weighted_rms",
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
                        "predicted_sigma_q": float(sigma_vector[i]),
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
                        "surface_components_clipped": int(clipped[i]),
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
    comparison, matched_comparison = _comparison_summary(
        result, args.apo_forward_path
    )
    comparison.to_csv(
        args.output_root / "external_q_comparison.csv",
        index=False,
    )
    matched_comparison.to_csv(
        args.output_root / "external_q_matched_comparison.csv",
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
        "surface_ridge": float(args.surface_ridge),
        "surface_rows": int(
            result["method"].astype(str).str.startswith(
                "vanilla_surface_"
            ).sum()
        ),
        "surface_rows_with_any_support_clipping": int(
            (
                result["surface_components_clipped"]
                .fillna(0)
                .astype(float)
                > 0
            ).sum()
        ),
        "matched_comparison_rows": int(len(matched_comparison)),
        "matched_contract_dates": (
            0
            if matched_comparison.empty
            else int(matched_comparison["n"].iloc[0])
        ),
        "matched_target_dates": (
            0
            if matched_comparison.empty
            else int(matched_comparison["n_dates"].iloc[0])
        ),
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
