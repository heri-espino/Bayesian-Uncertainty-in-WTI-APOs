"""Experiment 005: rolling, strictly lagged AAO price-residual uncertainty calibration.

Reads ONLY Experiment 004's existing locally accessible contract-level CSV.gz.
Does not rerun option valuation, call data providers or alter previous results.

IMPORTANT: these are intervals for *observed settlement-mark errors conditional on
same-day AAO parity anchors*, NOT risk-neutral terminal-average payoff intervals.
Bayesian NIG residual uncertainty is distinct from Bayesian volatility integration.
Never advertise the already-examined 2025–2026 dates as an untouched holdout.
"""
from __future__ import annotations

import argparse
from collections import defaultdict, deque
import json
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import t as student_t

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data/databento/wti_aao_bulk/derived_private/experiment004/AAO_MARKET_IV_BAYES_CONTRACT_PRICING.csv.gz"
OUTPUT = ROOT / "results/analysis/wti_aao_predictive_calibration/experiment005"
POINTS = ("lagged_IV", "bayes_IV_PM", "bayes_IV_PI")
CALIBRATORS = ("bayesian_nig", "rolling_empirical")
LEVELS = (0.90, 0.95)
KEY = ("date", "expiry", "side", "strike", "actual")


def weighted_quantile(values: np.ndarray, weights: np.ndarray, p: float) -> float:
    """Deterministic weighted signed-residual quantile, with endpoint protection."""
    if not 0 <= p <= 1 or not len(values):
        raise ValueError("Invalid quantile request")
    order = np.argsort(values, kind="stable")
    v = values[order]
    w = weights[order]
    if np.any(~np.isfinite(v)) or np.any(~np.isfinite(w)) or np.any(w <= 0):
        raise ValueError("Nonfinite values / invalid weights")
    c = np.cumsum(w)
    # Step-quantile is a conservative, deterministic choice for finite samples.
    return float(v[min(np.searchsorted(c, p * c[-1], side="left"), len(v)-1)])


def interval_from_past(past: list[tuple[str, np.ndarray]], level: float,
                       calibrator: str, *, mu0: float = 0.,
                       kappa0: float = 0.5, alpha0: float = 2.5,
                       beta0: float = 0.125) -> tuple[float, float]:
    """Equal-weight *dates*, not contracts; fit on strictly earlier residuals.

    Bayes method is the power-likelihood normal-inverse-gamma posterior
    predictive, with each historical date supplying total weight one. This
    controls pseudo-replication but is not an exact clustered hierarchical
    posterior. Empirical comparator uses same date-balanced signed residuals.
    """
    if calibrator not in CALIBRATORS or not 0 < level < 1 or not past:
        raise ValueError("Invalid calibrator/level/past data")
    vals = []
    wts = []
    for _, residuals in past:
        a = np.asarray(residuals, dtype=float)
        if not len(a) or not np.all(np.isfinite(a)):
            raise ValueError("Invalid historical residuals")
        vals.append(a)
        wts.append(np.full(len(a), 1.0 / len(a), dtype=float))
    x = np.concatenate(vals)
    w = np.concatenate(wts)
    alpha = (1.0-level)/2.0
    if calibrator == "rolling_empirical":
        return weighted_quantile(x, w, alpha), weighted_quantile(x, w, 1-alpha)
    n = float(w.sum())  # number of historical valuation-date clusters
    mean = float(np.dot(w, x) / n)
    kappa_n = kappa0+n
    mu_n = (kappa0*mu0+n*mean)/kappa_n
    alpha_n = alpha0+n/2.0
    beta_n = beta0 + 0.5*float(np.dot(w, (x-mean)**2)) + (
        0.5*kappa0*n/kappa_n*(mean-mu0)**2)
    scale = np.sqrt(beta_n/alpha_n*(kappa_n+1.0)/kappa_n)
    q = student_t.ppf([alpha, 1-alpha], df=2.0*alpha_n, loc=mu_n, scale=scale)
    return float(q[0]), float(q[1])


def load_contracts(source: Path) -> pd.DataFrame:
    """Never read raw Databento price data or mutate source files."""
    if not source.is_file():
        raise FileNotFoundError(
            f"Missing local Experiment 004 LFS payload: {source}. "
            "Run 'git lfs pull' in the private repo on your PC."
        )
    required = [*KEY, "method", "observed", "predicted", "error",
                "expected_average"]
    pieces = []
    for chunk in pd.read_csv(source, chunksize=150_000, low_memory=False):
        missing = set(required).difference(chunk.columns)
        if missing:
            raise ValueError(f"Missing input columns: {sorted(missing)}")
        actual = chunk["actual"].astype(str).str.lower().isin(("true", "1"))
        keep = actual & chunk["method"].isin(POINTS)
        pieces.append(chunk.loc[keep, required].copy())
    if not pieces:
        raise ValueError("Empty experiment004 output")
    data = pd.concat(pieces, ignore_index=True)
    if data.empty:
        raise ValueError("No actual-flagged target rows")
    data["date"] = pd.to_datetime(data["date"], errors="raise")
    data["expiry"] = pd.to_datetime(data["expiry"], errors="raise")
    data["actual"] = True
    if not np.all(np.isfinite(data[["observed", "predicted", "error", "strike",
                                    "expected_average"]].to_numpy(dtype=float))):
        raise ValueError("Nonfinite observed/predicted/error inputs")
    if not np.allclose(data["predicted"]-data["observed"], data["error"], atol=1e-7):
        raise ValueError("Contract errors inconsistent with recorded predictions")
    counts = data.groupby(list(KEY), observed=True)["method"].agg(["nunique", "size"])
    if not (counts["nunique"].eq(len(POINTS)).all() and
            counts["size"].eq(len(POINTS)).all()):
        raise ValueError("Different point methods have different or duplicate support")
    data["maturity_days"] = (data["expiry"]-data["date"]).dt.days
    if (data["maturity_days"] <= 0).any():
        raise ValueError("Matured target present")
    data["tenor"] = pd.cut(data["maturity_days"],
        [0, 30, 60, 120, 240, np.inf],
        labels=["1-30", "31-60", "61-120", "121-240", ">240"])
    data["moneyness"] = pd.cut(data["strike"] / data["expected_average"],
        [0, .9, .97, 1.03, 1.10, np.inf],
        labels=["<.90", ".90-.97", ".97-1.03", "1.03-1.10", ">1.10"])
    if data[["tenor", "moneyness"]].isna().any().any():
        raise ValueError("Unclassified maturity/moneyness")
    return data.sort_values(["date", "method", "side", "expiry", "strike"]).reset_index(drop=True)


def interval_score(y: np.ndarray, lower: np.ndarray, upper: np.ndarray,
                   level: float) -> np.ndarray:
    alpha = 1.-level
    return (upper-lower + 2/alpha * np.maximum(lower-y, 0.)
            + 2/alpha * np.maximum(y-upper, 0.))


def _summarize(predictions: pd.DataFrame, groups: list[str]) -> pd.DataFrame:
    return predictions.groupby(groups, observed=True).agg(
        n=("covered", "size"), n_dates=("date", "nunique"),
        coverage=("covered", "mean"),
        mean_width=("width", "mean"),
        mean_interval_score=("interval_score", "mean"),
    ).reset_index()


def month_block_ci(daily: pd.DataFrame, method_a: str, method_b: str,
                   *, n_boot: int = 1999, seed: int = 5505) -> pd.DataFrame:
    """Paired, equal-valuation-date mean interval-score improvement over baseline."""
    subset = daily[daily["calibrator"].isin((method_a, method_b))]
    pivot = subset.pivot(index="date", columns="calibrator", values="mean_interval_score")
    if not {method_a, method_b}.issubset(pivot.columns):
        raise ValueError("Missing calibrator in daily comparisons")
    pivot = pivot.dropna(subset=[method_a, method_b])
    if len(pivot) < 4:
        return pd.DataFrame()
    delta = pivot[method_b] - pivot[method_a]
    blocks = delta.groupby(delta.index.to_period("M")).agg(["sum", "count"])
    if len(blocks) < 3:
        return pd.DataFrame()
    rng = np.random.default_rng(seed)
    picks = rng.integers(0, len(blocks), size=(n_boot, len(blocks)))
    draws = blocks["sum"].to_numpy()[picks].sum(axis=1) / (
        blocks["count"].to_numpy()[picks].sum(axis=1))
    return pd.DataFrame([{
        "candidate": method_a, "baseline": method_b,
        "mean_daily_interval_score_improvement": float(delta.mean()),
        "ci_low": float(np.quantile(draws, .025)),
        "ci_high": float(np.quantile(draws, .975)),
        "n_dates": int(len(delta)), "n_month_blocks": int(len(blocks)),
    }])


def execute(data: pd.DataFrame, *, min_dates: int = 15,
            window_dates: int = 63, levels=LEVELS,
            bootstrap: int = 1999, test_start: str = "2025-01-01") -> tuple[dict, dict[str, pd.DataFrame]]:
    """Date-by-date walk-forward: forecast ALL contracts before updating history.

    History is keyed by method/side/maturity stratum. No same-date residual
    contributes to the same-date forecast; all three point models compete
    on identical realized contract support, calibration method and level.
    """
    if not 3 <= min_dates <= window_dates or bootstrap < 99:
        raise ValueError("Invalid walk-forward window or bootstrap count")
    history: dict[tuple[str, str, str], deque] = defaultdict(lambda: deque(maxlen=window_dates))
    out = []
    date_count = 0
    for day, today in data.groupby("date", sort=True):
        date_count += 1
        dt = day.strftime("%Y-%m-%d")
        # Compute all intervals using pre-date state, then update (no leakage).
        for (method, side, tenor), group in today.groupby(["method", "side", "tenor"], observed=True):
            k = (str(method), str(side), str(tenor))
            past = list(history[k])
            if len(past) < min_dates:
                continue
            if any(previous_date >= dt for previous_date, _ in past):
                raise AssertionError("Leakage: historical residual dated current/future")
            for level in levels:
                for cal in CALIBRATORS:
                    l, u = interval_from_past(past, float(level), cal)
                    obs = group["observed"].to_numpy(float)
                    point = group["predicted"].to_numpy(float)
                    low, high = point + l, point + u
                    covered = (obs >= low) & (obs <= high)
                    out.append(pd.DataFrame({
                        "date": dt, "method": str(method), "side": str(side),
                        "tenor": str(tenor), "moneyness": group["moneyness"].astype(str).to_numpy(),
                        "level": float(level), "calibrator": cal,
                        "covered": covered.astype(float), "width": high-low,
                        "interval_score": interval_score(obs, low, high, float(level)),
                        "n_historical_dates": len(past),
                        "latest_calibration_date": past[-1][0],
                        "split": "holdout_inspected" if dt >= test_start else "development",
                    }))
        # Advance each history stratum exactly once after all methods/dates scored.
        for (method, side, tenor), group in today.groupby(["method", "side", "tenor"], observed=True):
            k = (str(method), str(side), str(tenor))
            history[k].append((dt, -group["error"].to_numpy(dtype=float)))  # observed - predicted
    if not out:
        raise RuntimeError("No eligible out-of-sample dates; lower min_dates only with new preregistration")
    result = pd.concat(out, ignore_index=True)
    if (result["latest_calibration_date"] >= result["date"]).any():
        raise AssertionError("Same-day leakage in output")
    # Equal point-model support within every date, level and interval family.
    sample = result.groupby(["date", "level", "calibrator", "method"], observed=True).size().unstack("method")
    if sample.isna().any().any() or (sample.nunique(axis=1) != 1).any():
        raise AssertionError("Point methods have different calibration support")
    groupcols = ["split", "method", "calibrator", "level"]
    bysplit = _summarize(result, groupcols)
    result["year"] = result["date"].str[:4]
    byyear = _summarize(result, ["year", "method", "calibrator", "level"])
    bytenor = _summarize(result, ["split", "tenor", "method", "calibrator", "level"])
    bymoney = _summarize(result, ["split", "moneyness", "method", "calibrator", "level"])
    daily = _summarize(result, ["split", "date", "method", "calibrator", "level"])
    cis=[]
    for (split, method, level), sub in daily.groupby(["split", "method", "level"], observed=True):
        x=sub.copy()
        x["date"]=pd.to_datetime(x["date"])
        ci=month_block_ci(x, "bayesian_nig", "rolling_empirical", n_boot=bootstrap)
        if not ci.empty:
            ci.insert(0, "split", split)
            ci.insert(1, "point_method", method)
            ci.insert(2, "level", level)
            cis.append(ci)
    # PI against unmodified lagged IV with identical NIG calibration.
    for (split, level), sub in daily[daily["calibrator"]=="bayesian_nig"].groupby(["split", "level"], observed=True):
        x=sub.pivot(index="date", columns="method", values="mean_interval_score")
        if {"bayes_IV_PI", "lagged_IV"}.issubset(x):
            tmp=x[["bayes_IV_PI", "lagged_IV"]].rename(columns={
                "bayes_IV_PI":"bayesian_nig", "lagged_IV":"rolling_empirical"}).reset_index()
            stacked=tmp.melt(id_vars="date",var_name="calibrator",value_name="mean_interval_score")
            stacked["date"]=pd.to_datetime(stacked["date"])
            ci=month_block_ci(stacked,"bayesian_nig","rolling_empirical",n_boot=bootstrap)
            if not ci.empty:
                ci.insert(0,"split",split)
                ci.insert(1,"point_method","bayes_IV_PI_minus_lagged_IV_same_NIG")
                ci.insert(2,"level",level)
                ci["candidate"]="bayes_IV_PI+bayesian_nig"
                ci["baseline"]="lagged_IV+bayesian_nig"
                cis.append(ci)
    intervals=pd.concat(cis, ignore_index=True) if cis else pd.DataFrame()
    manifest={
        "study":"experiment005_conditional_AAO_mark_residual_calibration",
        "source":"experiment004_saved_contract_predictions_only",
        "n_source_actual_contract_dates":int(len(data)//len(POINTS)),
        "n_source_valuation_dates":int(date_count),
        "n_eligible_scored_rows":int(len(result)),
        "n_eligible_actual_contract_dates": int(len(result)//(len(POINTS)*len(CALIBRATORS)*len(levels))),
        "n_eligible_valuation_dates":int(result["date"].nunique()),
        "calibration_min_historical_dates":min_dates,
        "calibration_max_historical_dates":window_dates,
        "point_models":list(POINTS),
        "calibrators":list(CALIBRATORS),
        "levels":list(map(float,levels)),
        "test_start":test_start,
        "test_inspected_previously":True,
        "no_provider_calls":True,
        "no_source_data_mutation":True,
        "not_fully_ex_ante":True,
        "interpretation":(
            "Empirical intervals for conditional AAO settlement-mark pricing error "
            "after same-date disjoint parity anchoring. They are NOT Asian payoff "
            "prediction intervals, not calibrated probabilities of true option "
            "value, and not an untouched prospective holdout. The NIG power "
            "likelihood balances valuation dates but is not a complete "
            "hierarchical day-cluster model."
        ),
    }
    tables={"summary_by_split":bysplit,"summary_by_year":byyear,
            "summary_by_maturity":bytenor,"summary_by_moneyness":bymoney,
            "daily_actual_scores":daily,"paired_month_block_intervals":intervals}
    return manifest, tables


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--execute", action="store_true", help="Explicit local analysis")
    parser.add_argument("--source",type=Path,default=SOURCE)
    parser.add_argument("--output-dir",type=Path,default=OUTPUT)
    parser.add_argument("--min-dates",type=int,default=15)
    parser.add_argument("--window-dates",type=int,default=63)
    parser.add_argument("--bootstrap",type=int,default=1999)
    parser.add_argument("--test-start",default="2025-01-01")
    args=parser.parse_args()
    if not args.execute:
        print(json.dumps({"execute":False,"source":str(args.source),
              "output":str(args.output_dir),"private_source_read_only":True,
              "no_provider_calls":True,"test_previously_inspected":True},indent=2))
        return
    if args.output_dir.resolve() == args.source.resolve():
        raise ValueError("Cannot overwrite source")
    data=load_contracts(args.source)
    manifest,tables=execute(data,min_dates=args.min_dates,
        window_dates=args.window_dates,bootstrap=args.bootstrap,test_start=args.test_start)
    if args.output_dir.exists() and any(args.output_dir.iterdir()):
        raise FileExistsError("Output directory not empty: choose a new run folder to preserve results")
    args.output_dir.mkdir(parents=True,exist_ok=True)
    for name,table in tables.items():
        table.to_csv(args.output_dir/(name+".csv"),index=False)
    (args.output_dir/"experiment_manifest.json").write_text(
        json.dumps(manifest,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(manifest,indent=2))

if __name__=="__main__":
    main()
