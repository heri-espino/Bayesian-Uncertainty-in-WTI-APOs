"""Experiment 004: Bayesian AAO implied-volatility innovations, LOCAL ONLY.

Compares the original six methods, including the UNMODIFIED lagged_IV
baseline, to Bayesian market-IV posterior-predictive integration and its
matched plug-in sigma-mean pricing. All instruments use exactly the same
eligible non-anchor strikes. All volatility histories end STRICTLY
before the valuation date.

The original Databento-only model is a retrospective, conditional
lognormal approximation for the terminal average, NOT a structural
first-nearby CL Asian simulator nor a wholly ex-ante forecast.

No purchases, Databento API, writing to source SQLite, or GitHub Actions.
Heavy computation requires --execute; dry-run is default.
"""
from __future__ import annotations

import argparse
from collections import defaultdict
import hashlib
import json
from pathlib import Path
import sqlite3

import numpy as np
import pandas as pd

from bayesian_asian_options.aao_databento_only import (
    METHODS as ORIGINAL_METHODS, average_black, reserve_parity_anchors,
)
from bayesian_asian_options.aao_market_iv_bayes import predict_market_iv
from experiments import wti_aao_databento_only as legacy

ROOT = Path(__file__).resolve().parents[1]
METHODS = (*ORIGINAL_METHODS, "bayes_IV_PM", "bayes_IV_PI")
DEFAULT_OUTPUT = ROOT / "results/analysis/wti_aao_market_iv_bayes/experiment004"
DEFAULT_PRIVATE = ROOT / "data/databento/wti_aao_bulk/derived_private/experiment004"

def _grouping(frame: pd.DataFrame, fields: list[str]) -> pd.DataFrame:
    f = frame.copy()
    f["abs_error"] = f["error"].abs()
    return f.groupby(fields, observed=True).agg(
        n_contract_dates=("error", "size"),
        n_dates=("date", "nunique"),
        mae=("abs_error", "mean"),
        rmse=("error", lambda x: float(np.sqrt(np.mean(x.to_numpy()**2)))),
        bias=("error", "mean"),
    ).reset_index()


def _month_block_intervals(actual: pd.DataFrame, *,
                           n_boot: int, seed: int) -> pd.DataFrame:
    """Paired daily MAE, resampling full calendar months, not contract rows."""
    by = _grouping(actual, ["date", "method"])
    piv = by.pivot(index="date", columns="method", values="mae").dropna()
    if set(piv.columns) != set(METHODS):
        raise ValueError("Incomplete paired method support in month bootstrap")
    months = piv.index.to_period("M")
    rng = np.random.default_rng(seed)
    comparisons = []
    for method, baseline in (
        [(m, "lagged_IV") for m in METHODS if m != "lagged_IV"]
        + [("bayes_IV_PI", "bayes_IV_PM"), ("PI", "PM")]
    ):
        delta = piv[baseline] - piv[method]
        groups = delta.groupby(months).agg(["sum", "count"])
        if len(groups) < 3:
            continue
        sm = groups["sum"].to_numpy(dtype=float)
        ns = groups["count"].to_numpy(dtype=float)
        draw = rng.integers(0, len(groups), size=(n_boot, len(groups)))
        means = sm[draw].sum(axis=1) / ns[draw].sum(axis=1)
        comparisons.append({
            "method": method, "baseline": baseline,
            "n_paired_dates": int(len(delta)), "n_month_blocks": int(len(groups)),
            "mean_daily_mae_improvement": float(delta.mean()),
            "ci_low": float(np.quantile(means, .025)),
            "ci_high": float(np.quantile(means, .975)),
        })
    return pd.DataFrame(comparisons)


def _augment(original: list[dict], forecast) -> list[dict]:
    """Append Bayesian variants for every retained original target row."""
    targets = [r for r in original if r["method"] == "lagged_IV"]
    if not targets:
        return []
    ref = targets[0]
    maturity = (pd.Timestamp(ref["expiry"]) - pd.Timestamp(ref["date"])).days/365.25
    strike = np.asarray([r["strike"] for r in targets])
    side = np.asarray([r["side"] for r in targets])
    fwd = float(ref["expected_average"])
    df = float(ref["parity_discount_factor"])
    pi = average_black(
        fwd, strike[None, :], forecast.sigma_draws[:, None], maturity,
        df, side[None, :]
    ).mean(axis=0)
    pm = average_black(fwd, strike, forecast.sigma_mean, maturity, df, side)
    augmented = list(original)
    for k, row in enumerate(targets):
        for method, price in (("bayes_IV_PM", pm[k]), ("bayes_IV_PI", pi[k])):
            record = dict(row)
            record.update({
                "method": method, "predicted": float(price),
                "error": float(price) - row["observed"],
            })
            augmented.append(record)
    # Match diagnostics across all methods for a given contract-date.
    diag = {
        "market_iv_latest_date": forecast.latest_iv_date,
        "market_iv_age_business_days": forecast.age_business_days,
        "market_iv_past_innovations": forecast.n_changes,
        "market_iv_posterior_sigma_mean": forecast.sigma_mean,
        "market_iv_posterior_sigma_sd": forecast.sigma_sd,
        "market_iv_predictive_clipped_draws": forecast.n_clipped,
        "market_iv_posterior_drift": forecast.posterior_drift,
    }
    for row in augmented:
        row.update(diag)
    return augmented


def _write_outputs(frame: pd.DataFrame, out: Path, private: Path,
                   audit: dict, bootstrap: int) -> dict:
    frame["date"] = pd.to_datetime(frame["date"])
    frame["year"] = frame["date"].dt.year
    frame["split"] = np.where(frame["date"] >= pd.Timestamp(audit["test_start"]),
                              "holdout", "development")
    maturity = (pd.to_datetime(frame["expiry"]) - frame["date"]).dt.days
    frame["maturity_bucket"] = pd.cut(
        maturity, bins=[0, 30, 60, 120, 240, np.inf],
        labels=["1-30d", "31-60d", "61-120d", "121-240d", ">240d"])
    frame["moneyness_bucket"] = pd.cut(
        frame["strike"]/frame["expected_average"],
        bins=[0, .9, .97, 1.03, 1.10, np.inf],
        labels=["<0.90", "0.90-0.97", "0.97-1.03", "1.03-1.10", ">1.10"])
    frame["settlement_type"] = np.where(frame["actual"],
                                        "actual_flagged", "theoretical_flagged")
    key = ["date", "expiry", "side", "strike", "actual"]
    support = frame.groupby(key, observed=True)["method"].agg(["nunique", "size"])
    if not (support["nunique"].eq(len(METHODS)).all()
            and support["size"].eq(len(METHODS)).all()):
        raise AssertionError("Contract method support is unequal or duplicated")
    if not (frame["market_iv_latest_date"] < frame["date"].dt.strftime("%Y-%m-%d")).all():
        raise AssertionError("Current/future-date IV leaked into the study")
    if not np.allclose(frame["predicted"] - frame["observed"], frame["error"],
                       atol=1e-7, equal_nan=False):
        raise AssertionError("Inconsistent pricing errors")
    out.mkdir(parents=True, exist_ok=True)
    private.mkdir(parents=True, exist_ok=True)
    frame.to_csv(private/"AAO_MARKET_IV_BAYES_CONTRACT_PRICING.csv.gz",
                 index=False, compression="gzip", date_format="%Y-%m-%d")
    summary = _grouping(frame, ["split", "settlement_type", "method"])
    summary.to_csv(out/"method_metrics_by_split.csv", index=False)
    _grouping(frame, ["year", "settlement_type", "method"]).to_csv(
        out/"method_metrics_by_year.csv", index=False)
    _grouping(frame, ["split", "maturity_bucket", "settlement_type", "method"]).to_csv(
        out/"method_metrics_by_maturity.csv", index=False)
    _grouping(frame, ["split", "moneyness_bucket", "settlement_type", "method"]).to_csv(
        out/"method_metrics_by_moneyness.csv", index=False)
    actual = frame.loc[frame["actual"]]
    _grouping(actual, ["split", "date", "method"]).to_csv(
        out/"daily_actual_mae.csv", index=False)
    intervals = []
    for split in ("development", "holdout", "all"):
        sample = actual if split == "all" else actual[actual["split"] == split]
        if sample.empty:
            continue
        z = _month_block_intervals(sample, n_boot=bootstrap, seed=2810)
        z.insert(0, "split", split)
        intervals.append(z)
    pd.concat(intervals, ignore_index=True).to_csv(
        out/"paired_actual_month_block_ci.csv", index=False)
    unique = frame.loc[frame["method"] == "lagged_IV"]
    audit.update({
        "n_priced_dates": int(unique["date"].nunique()),
        "n_target_contract_dates": int(len(unique)),
        "n_actual_target_rows": int(unique["actual"].sum()),
        "n_theoretical_target_rows": int((~unique["actual"]).sum()),
        "n_holdout_dates": int(unique[unique["split"] == "holdout"]["date"].nunique()),
        "n_holdout_actual_target_rows": int(
            unique[(unique["split"] == "holdout") & unique["actual"]].shape[0]),
        "n_clipped_predictive_draws": int(
            unique.groupby(["date", "expiry"], observed=True)["market_iv_predictive_clipped_draws"].first().sum()),
        "methods": list(METHODS),
        "private_contract_file":
            "data/databento/wti_aao_bulk/derived_private/experiment004/AAO_MARKET_IV_BAYES_CONTRACT_PRICING.csv.gz",
        "primary_comparison": "bayes_IV_PI vs unchanged lagged_IV on heldout actual marks",
        "disclosure": (
            "Retrospective conditional AAO cross-sectional pricing, using same-date "
            "disjoint parity anchors and strictly prior-date market-IV innovation "
            "histories. Bayesian market IV is not CL structural Asian volatility; "
            "no current evaluation target premium or target IV is used by predictors. "
            "Only user-computed full local experiment outputs support quantitative claims."
        ),
    })
    (out/"experiment_manifest.json").write_text(
        json.dumps(audit, indent=2)+"\n", encoding="utf-8")
    return audit


def evaluate(*, sqlite_path: Path, raw_dir: Path, output_dir: Path,
             private_dir: Path, source_start: str, eval_start: str,
             eval_end: str | None, test_start: str,
             date_stride: int, max_contracts: int, bootstrap: int,
             min_iv_changes: int, max_iv_changes: int,
             posterior_draws: int) -> dict:
    if not (source_start <= eval_start < test_start):
        raise ValueError("Require source_start <= eval_start < test_start")
    if eval_end is not None and eval_end < test_start:
        raise ValueError("eval_end must include holdout interval")
    if date_stride < 1 or max_contracts < 1 or bootstrap < 99:
        raise ValueError("Invalid study stride/contracts/bootstrap")
    if not sqlite_path.is_file():
        raise FileNotFoundError(f"Missing local SQLite: {sqlite_path}")
    conn = sqlite3.connect(sqlite_path.resolve().as_uri()+"?mode=ro", uri=True)
    histories = defaultdict(list)
    monthly_defs = {}
    outputs = []
    audit = {
        "study": "experiment004_bayesian_lagged_AAO_market_IV",
        "source_start": source_start, "evaluation_start": eval_start,
        "evaluation_end": eval_end, "test_start": test_start,
        "date_stride": date_stride, "max_contracts_per_expiry": max_contracts,
        "bootstrap_calendar_month_resamples": bootstrap,
        "market_iv_min_changes": min_iv_changes,
        "market_iv_max_changes": max_iv_changes,
        "market_iv_posterior_draws": posterior_draws,
        "groups_seen": 0, "groups_with_eligible_legacy": 0,
        "groups_with_bayesian_IV_history": 0, "groups_priced": 0,
        "no_provider_calls": True, "original_sources_read_only": True,
        "same_day_disjoint_parity_anchors": True, "volatility_inputs_strictly_lagged": True,
        "hyperparameters_fixed_not_test_tuned": True,
    }
    try:
        sql = (f"SELECT DISTINCT ref_date FROM states WHERE {legacy.VALID_SQL} "
               "AND ref_date>=? ORDER BY ref_date")
        dates = [row[0] for row in conn.execute(sql, (source_start,))]
        if eval_end is not None:
            dates = [d for d in dates if d <= eval_end]
        audit["selected_source_days"] = len(dates)
        for counter, day in enumerate(dates):
            month = day[:7]
            if month not in monthly_defs:
                monthly_defs.clear()
                monthly_defs[month] = legacy.date_definitions(raw_dir, day)
            panel = legacy.read_date(conn, day, monthly_defs[month])
            for expiry, group in legacy.option_groups(panel, day):
                audit["groups_seen"] += 1
                anchor = reserve_parity_anchors(group, actual_only=True)
                if anchor is None:
                    continue
                history = histories[expiry]
                old_returns = legacy.previous_returns(history)
                prev_iv = next((
                    iv for d, _, iv in reversed(history)
                    if np.isfinite(iv) and 0 < (pd.Timestamp(day)-pd.Timestamp(d)).days <= 10
                ), float("nan"))
                if (day >= eval_start and counter % date_stride == 0
                        and len(old_returns) >= 20 and np.isfinite(prev_iv)):
                    audit["groups_with_eligible_legacy"] += 1
                    seed = int.from_bytes(hashlib.sha256(
                        f"{day}/{expiry}".encode()).digest()[:4], "big")
                    forecast = predict_market_iv(
                        history, asof=day, seed=seed,
                        min_changes=min_iv_changes, max_changes=max_iv_changes,
                        n_draws=posterior_draws)
                    if forecast is not None:
                        audit["groups_with_bayesian_IV_history"] += 1
                        if not np.isclose(forecast.lagged_sigma, prev_iv,
                                          atol=1e-12, rtol=0):
                            raise AssertionError("Changed lagged-IV baseline")
                        original = legacy.priced_rows(
                            day=day, expiry=expiry, group=group,
                            forward=anchor.forward_average,
                            discount=anchor.discount_factor,
                            anchor_strikes=anchor.anchor_strikes,
                            proxy_returns=old_returns, prev_iv=prev_iv,
                            seed=seed, max_contracts=max_contracts)
                        if original:
                            outputs.extend(_augment(original, forecast))
                            audit["groups_priced"] += 1
                # Update history ONLY AFTER evaluating day, preventing leakage.
                current_iv = legacy.prior_implied_vol(
                    group, forward=anchor.forward_average,
                    discount=anchor.discount_factor,
                    maturity=(pd.Timestamp(expiry)-pd.Timestamp(day)).days/365.25,
                    anchor_strikes=anchor.anchor_strikes)
                history.append((day, anchor.forward_average, current_iv))
    finally:
        conn.close()
    if not outputs:
        output_dir.mkdir(parents=True, exist_ok=True)
        audit["status"] = "no_eligible_groups_under_iv_history_requirements"
        (output_dir/"eligibility_failure.json").write_text(
            json.dumps(audit, indent=2)+"\n", encoding="utf-8")
        raise RuntimeError("No eligible comparison rows; see eligibility_failure.json")
    return _write_outputs(pd.DataFrame(outputs), output_dir, private_dir,
                          audit, bootstrap)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--execute", action="store_true")
    parser.add_argument("--sqlite", type=Path, default=legacy.SQLITE)
    parser.add_argument("--raw-dir", type=Path, default=legacy.RAW)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--private-dir", type=Path, default=DEFAULT_PRIVATE)
    parser.add_argument("--source-start", default="2021-01-01")
    parser.add_argument("--eval-start", default="2023-01-01")
    parser.add_argument("--eval-end", default="2026-09-30")
    parser.add_argument("--test-start", default="2025-01-01")
    parser.add_argument("--date-stride", type=int, default=5)
    parser.add_argument("--max-contracts", type=int, default=80)
    parser.add_argument("--bootstrap", type=int, default=1999)
    parser.add_argument("--min-iv-changes", type=int, default=8)
    parser.add_argument("--max-iv-changes", type=int, default=63)
    parser.add_argument("--posterior-draws", type=int, default=256)
    args = parser.parse_args()
    if not args.execute:
        print(json.dumps({
            "execute": False, "experiment": "004_market_implied_Bayesian",
            "existing_study_untouched": True,
            "offline": True,
            "test_start": args.test_start,
            "posterior_draws": args.posterior_draws,
            "expected_original_methods": list(ORIGINAL_METHODS),
            "new_methods": ["bayes_IV_PM", "bayes_IV_PI"],
        }, indent=2))
        return
    audit = evaluate(
        sqlite_path=args.sqlite, raw_dir=args.raw_dir,
        output_dir=args.output_dir, private_dir=args.private_dir,
        source_start=args.source_start, eval_start=args.eval_start,
        eval_end=args.eval_end, test_start=args.test_start,
        date_stride=args.date_stride, max_contracts=args.max_contracts,
        bootstrap=args.bootstrap, min_iv_changes=args.min_iv_changes,
        max_iv_changes=args.max_iv_changes, posterior_draws=args.posterior_draws,
    )
    print(json.dumps(audit, indent=2))


if __name__ == "__main__":
    main()
