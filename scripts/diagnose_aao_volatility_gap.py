"""Diagnose why prior-date AAO IV outperforms the historical-volatility Bayesian model.

Read-only postprocessing of the full contract-level pricing file. No provider calls,
no SQLite writes, and no GitHub Actions. Output files are aggregate diagnostics.

Usage from repository root:
    python scripts/diagnose_aao_volatility_gap.py \
      --private-file data/databento/wti_aao_bulk/derived_private/full_2023_2026/AAO_DATABENTO_REDUCED_FORM_CONTRACT_PRICING.csv.gz \
      --output-dir results/analysis/wti_aao_databento_only/volatility_gap_diagnostic

Current-date target IV is computed for EXPLANATORY DIAGNOSTICS ONLY, not as a
feasible benchmark or a model feature. Do not leak it into a forecasting model.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd

from bayesian_asian_options.aao_databento_only import implied_average_sigma

METHODS = ("PI", "PM", "rolling21", "rolling63", "ewma63", "lagged_IV")
KEY = ["date", "expiry", "side", "strike", "actual"]


def read_data(source: Path) -> pd.DataFrame:
    if not source.is_file():
        raise FileNotFoundError(f"Missing local contract-level results: {source}")
    d = pd.read_csv(source, low_memory=False)
    required = set(KEY + ["method", "observed", "predicted", "error",
                          "expected_average", "parity_discount_factor", "prior_iv_sigma"])
    absent = required - set(d.columns)
    if absent:
        raise ValueError(f"Missing required columns: {sorted(absent)}")
    d["actual"] = d["actual"].astype(str).str.lower().isin(("true", "1"))
    d["date"] = pd.to_datetime(d["date"])
    d["expiry"] = pd.to_datetime(d["expiry"])
    if set(d["method"]) != set(METHODS):
        raise ValueError("One or more pricing methods missing")
    keys = d.groupby(KEY, observed=True)["method"].agg(["nunique", "size"])
    if not (keys["nunique"].eq(6).all() and keys["size"].eq(6).all()):
        raise ValueError("Nonunique contract rows or incomplete common-method support")
    if not np.allclose(d["predicted"] - d["observed"], d["error"], atol=1e-7):
        raise ValueError("Stored prediction/error columns disagree")
    d["abs_error"] = d["error"].abs()
    d["year"] = d["date"].dt.year
    d["moneyness"] = d["strike"] / d["expected_average"]
    d["moneyness_bin"] = pd.cut(
        d["moneyness"], bins=[0, .9, .97, 1.03, 1.1, np.inf],
        labels=["<0.90", "0.90-0.97", "0.97-1.03", "1.03-1.10", ">1.10"],
    )
    d["days_to_expiry"] = (d["expiry"]-d["date"]).dt.days
    d["maturity_bin"] = pd.cut(
        d["days_to_expiry"], bins=[0, 30, 60, 120, 240, np.inf],
        labels=["1-30d", "31-60d", "61-120d", "121-240d", ">240d"],
    )
    return d


def aggregations(data: pd.DataFrame, output: Path) -> tuple[pd.DataFrame, dict]:
    def error_table(grouping: list[str], dest: str) -> pd.DataFrame:
        result = data.groupby(grouping, observed=True).agg(
            n=("error", "size"),
            mae=("abs_error", "mean"),
            rmse=("error", lambda a: float(np.sqrt(np.mean(np.square(a))))),
            bias=("error", "mean"),
        ).reset_index()
        result.to_csv(output / dest, index=False)
        return result

    actual = data.loc[data["actual"]].copy()
    if actual.empty:
        raise ValueError("No actual-flagged observations")
    error_table(["actual", "method"], "pricing_by_mark_type.csv")
    error_table(["actual", "year", "method"], "pricing_by_year.csv")
    error_table(["actual", "moneyness_bin", "method"], "pricing_by_moneyness.csv")
    error_table(["actual", "maturity_bin", "method"], "pricing_by_maturity.csv")

    date_actual = actual.groupby(["date", "method"], observed=True).agg(
        mae=("abs_error", "mean"), n=("error", "size"),
    ).reset_index()
    date_actual.to_csv(output / "daily_actual_only_mae.csv", index=False,
                       date_format="%Y-%m-%d")
    piv = date_actual.pivot(index="date", columns="method", values="mae").dropna()
    if len(piv) < 10:
        raise ValueError("Insufficient paired actual-mark dates")
    winner = piv.idxmin(axis=1).value_counts().to_dict()
    month = piv.index.to_period("M")
    month_ids = np.unique(month.astype(str))
    rng = np.random.default_rng(23091)
    n_boot = 1999
    comparisons = []
    for method in METHODS:
        if method == "PM":
            continue
        delta = piv["PM"] - piv[method]  # Positive favors method.
        grouped = delta.groupby(month).agg(["sum", "count"])
        sums = grouped["sum"].to_numpy()
        counts = grouped["count"].to_numpy()
        picks = rng.integers(0, len(grouped), size=(n_boot, len(grouped)))
        boot = sums[picks].sum(axis=1) / counts[picks].sum(axis=1)
        comparisons.append({
            "method": method,
            "baseline": "PM",
            "n_dates": int(len(piv)),
            "n_months": int(len(grouped)),
            "mean_actual_daily_mae_improvement": float(delta.mean()),
            "block_month_ci_low": float(np.quantile(boot, .025)),
            "block_month_ci_high": float(np.quantile(boot, .975)),
        })
    pd.DataFrame(comparisons).to_csv(output / "paired_actual_month_block_ci.csv", index=False)
    summary = {
        "n_target_contract_dates": int(len(data) // len(METHODS)),
        "n_actual_contract_dates": int(len(actual) // len(METHODS)),
        "n_actual_priced_dates": int(piv.shape[0]),
        "n_resampled_calendar_months": int(len(month_ids)),
        "daily_lowest_mae_winner_counts_actual_only": {
            name: int(winner.get(name, 0)) for name in METHODS
        },
        "n_actual_dates_PI_beats_PM": int((piv["PI"] < piv["PM"]).sum()),
        "n_actual_dates_lagged_IV_beats_PI": int((piv["lagged_IV"] < piv["PI"]).sum()),
        "interval_method": "Paired, resample calendar months as blocks, actual-flagged only",
        "do_not_construe_as_ex_ante": True,
    }
    return actual, summary


def reconstruct_volatility_gap(data: pd.DataFrame, output: Path) -> dict:
    # Only near-ATM actual contracts. Median target-day IV is an AFTER-THE-FACT
    # diagnostic derived from evaluation prices; it is forbidden as a feature.
    pm = data.loc[(data["method"] == "PM") & data["actual"] &
                  data["moneyness"].between(.85, 1.15)].copy()
    pm["distance"] = np.abs(np.log(pm["moneyness"]))
    pm = pm.sort_values(["date", "expiry", "distance"])
    pm = pm.groupby(["date", "expiry"], sort=False).head(8).copy()
    pi = data.loc[data["method"] == "PI", KEY + ["predicted"]].rename(
        columns={"predicted": "pi_predicted"}
    )
    pm = pm.merge(pi, on=KEY, how="left", validate="one_to_one")
    records = []
    for (day, expiry), group in pm.groupby(["date", "expiry"], sort=False):
        maturity = (expiry - day).days / 365.25
        sig_obs, sig_pm, sig_pi = [], [], []
        for row in group.itertuples(index=False):
            kwargs = dict(
                forward=float(row.expected_average), strike=float(row.strike),
                maturity=float(maturity), discount=float(row.parity_discount_factor),
                side=str(row.side),
            )
            if maturity <= 0:
                continue
            sig_obs.append(implied_average_sigma(float(row.observed), **kwargs))
            sig_pm.append(implied_average_sigma(float(row.predicted), **kwargs))
            sig_pi.append(implied_average_sigma(float(row.pi_predicted), **kwargs))
        sig_obs = np.array(sig_obs, dtype=float)
        sig_pm = np.array(sig_pm, dtype=float)
        sig_pi = np.array(sig_pi, dtype=float)
        if np.isfinite(sig_obs).sum() < 2 or np.isfinite(sig_pm).sum() < 2:
            continue
        observation = {
            "date": day.strftime("%Y-%m-%d"),
            "expiry": expiry.strftime("%Y-%m-%d"),
            "n_near_atm_candidates": int(len(group)),
            "n_valid_target_implied_sigma": int(np.isfinite(sig_obs).sum()),
            "sigma_current_target_implied": float(np.nanmedian(sig_obs)),
            "sigma_bayesian_PM": float(np.nanmedian(sig_pm)),
            "sigma_bayesian_PI_price_equivalent": float(np.nanmedian(sig_pi)),
            "sigma_lagged_option_implied": float(group["prior_iv_sigma"].median()),
            "days_to_expiry": int((expiry - day).days),
        }
        observation["iv_minus_pm"] = observation["sigma_current_target_implied"] - observation["sigma_bayesian_PM"]
        observation["iv_minus_lagged"] = observation["sigma_current_target_implied"] - observation["sigma_lagged_option_implied"]
        observation["lagged_minus_pm"] = observation["sigma_lagged_option_implied"] - observation["sigma_bayesian_PM"]
        records.append(observation)
    if not records:
        raise ValueError("No valid near-ATM contracts for IV inversion; inspect marks")
    sigma = pd.DataFrame(records).sort_values(["date", "expiry"])
    sigma.to_csv(output / "group_near_atm_volatility_comparison.csv", index=False)
    cols = ["sigma_current_target_implied", "sigma_bayesian_PM", "sigma_bayesian_PI_price_equivalent", "sigma_lagged_option_implied", "iv_minus_pm", "iv_minus_lagged", "lagged_minus_pm"]
    stats = {c: {"mean": float(sigma[c].mean()), "median": float(sigma[c].median())} for c in cols}
    return {
        "n_groups_with_at_least_two_invertible_actual_target_marks": int(len(sigma)),
        "fraction_groups_target_IV_above_PM_sigma": float((sigma["iv_minus_pm"] > 0).mean()),
        "fraction_groups_target_IV_above_lagged_IV_sigma": float((sigma["iv_minus_lagged"] > 0).mean()),
        "volatility_comparison": stats,
        "WARNING": "Current target-date IV is computed from evaluation prices ONLY as a retrospective diagnostic and is NOT an admissible prospective forecasting input.",
    }


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--private-file", type=Path, default=Path(
        "data/databento/wti_aao_bulk/derived_private/full_2023_2026/AAO_DATABENTO_REDUCED_FORM_CONTRACT_PRICING.csv.gz"))
    p.add_argument("--output-dir", type=Path, default=Path(
        "results/analysis/wti_aao_databento_only/volatility_gap_diagnostic"))
    args = p.parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    d = read_data(args.private_file)
    _, summary = aggregations(d, args.output_dir)
    summary.update(reconstruct_volatility_gap(d, args.output_dir))
    (args.output_dir / "diagnostic_summary.json").write_text(
        json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
