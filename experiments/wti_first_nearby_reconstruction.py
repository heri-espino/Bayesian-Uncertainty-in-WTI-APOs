"""Reconstruct historical first-nearby CL settlements and compare P posteriors.

This experiment consumes locally cached Databento CL statistics acquired by
``experiments.wti_databento_first_nearby``. It constructs the daily first-nearby
series from official final CL settlements, excludes returns spanning contract
rolls, compares the result with Yahoo ``CL=F`` over the same information window,
and estimates the same Gaussian-GBM volatility posterior for both return sources.

Raw Databento and Yahoo snapshots remain local. Versioned outputs contain only
roll boundaries, diagnostics, posterior summaries, and permitted derived results.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
from scipy.stats import gaussian_kde

from bayesian_asian_options.bayesian_gbm import (
    gbm_mle,
    random_walk_metropolis_gbm,
)
from bayesian_asian_options.databento_wti import (
    final_settlements,
    load_databento_csv,
)
from bayesian_asian_options.wti_first_nearby import (
    reconstruct_first_nearby_settlement_history,
)
from bayesian_asian_options.wti_yahoo import (
    dataframe_sha256,
    download_yahoo_wti,
    normalize_yahoo_history,
    prepare_wti_model_sample,
)
from experiments.wti_databento_first_nearby import (
    DEFAULT_HISTORY_START,
    DEFAULT_INFERENCE_END,
    DEFAULT_QUERY_END,
    requested_contracts,
    _raw_cl_symbol,
)

ROOT = Path(__file__).resolve().parents[1]


def _rhat(chains: np.ndarray) -> float:
    """Return split-free Gelman--Rubin R-hat for equal-length chains."""
    x = np.asarray(chains, dtype=float)
    if x.ndim != 2 or x.shape[0] < 2 or x.shape[1] < 2:
        raise ValueError("R-hat requires at least two chains with two draws each")
    m, n = x.shape
    means = x.mean(axis=1)
    within = x.var(axis=1, ddof=1).mean()
    between = n * means.var(ddof=1)
    if within <= 0:
        return 1.0
    var_hat = ((n - 1) / n) * within + between / n
    return float(np.sqrt(var_hat / within))


def _sigma_mode(draws: np.ndarray) -> float:
    """Return the marginal posterior mode of sigma using a KDE."""
    values = np.asarray(draws, dtype=float)
    lo, hi = np.quantile(values, [0.001, 0.999])
    if not np.isfinite(lo) or not np.isfinite(hi) or hi <= lo:
        return float(np.median(values))
    grid = np.linspace(max(1e-8, 0.9 * lo), 1.1 * hi, 2048)
    density = gaussian_kde(values)(grid)
    return float(grid[int(np.argmax(density))])


def _fit_gbm_posterior(
    returns: np.ndarray,
    *,
    chains: int,
    n_iter: int,
    burn_in: int,
    seed: int,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Fit the paper baseline Gaussian GBM posterior to one return vector."""
    values = np.asarray(returns, dtype=float)
    values = values[np.isfinite(values)]
    if len(values) < 100:
        raise RuntimeError(f"Only {len(values)} usable returns are available")
    dt = 1.0 / 252.0
    mu_mle, sigma_mle = gbm_mle(values, dt)
    mu_chains: list[np.ndarray] = []
    sigma_chains: list[np.ndarray] = []
    diagnostics: list[dict[str, Any]] = []
    for chain_id in range(chains):
        result = random_walk_metropolis_gbm(
            values,
            dt,
            n_iter=n_iter,
            burn_in=burn_in,
            theta_init=(mu_mle, float(np.log(max(sigma_mle, 1e-8)))),
            seed=seed + 10_000 * chain_id,
        )
        mu_chains.append(result.mu)
        sigma_chains.append(result.sigma)
        diagnostics.append(
            {
                "chain": chain_id + 1,
                "acceptance_rate": result.acceptance_rate,
                "mu_mean": float(np.mean(result.mu)),
                "sigma_mean": float(np.mean(result.sigma)),
            }
        )
    mu_matrix = np.vstack(mu_chains)
    sigma_matrix = np.vstack(sigma_chains)
    pooled = sigma_matrix.reshape(-1)
    summary = pd.DataFrame(
        [
            {
                "n_returns": int(len(values)),
                "mu_mle": float(mu_mle),
                "sigma_mle": float(sigma_mle),
                "mu_rhat": _rhat(mu_matrix),
                "sigma_rhat": _rhat(sigma_matrix),
                "sigma_posterior_mean": float(np.mean(pooled)),
                "sigma_posterior_sd": float(np.std(pooled, ddof=1)),
                "sigma_posterior_mode": _sigma_mode(pooled),
                "sigma_q025": float(np.quantile(pooled, 0.025)),
                "sigma_q50": float(np.quantile(pooled, 0.50)),
                "sigma_q975": float(np.quantile(pooled, 0.975)),
            }
        ]
    )
    return summary, pd.DataFrame(diagnostics)


def _symbol_mapping(start: str, inference_end: str) -> pd.DataFrame:
    contracts = requested_contracts(start, inference_end)
    return pd.DataFrame(
        {
            "contract": contracts,
            "raw_symbol": [_raw_cl_symbol(x) for x in contracts],
        }
    )


def _settlement_panel(
    raw_statistics: pd.DataFrame, mapping: pd.DataFrame
) -> pd.DataFrame:
    """Return canonical contract/date official final settlements."""
    settlements = final_settlements(raw_statistics).copy()
    symbol_col = next(
        (c for c in ("symbol", "raw_symbol") if c in settlements.columns),
        None,
    )
    if symbol_col is None:
        raise ValueError(
            "Databento statistics must retain mapped raw symbols for reconstruction"
        )
    lookup = mapping.rename(columns={"raw_symbol": "_raw_symbol"})
    settlements["_raw_symbol"] = settlements[symbol_col].astype(str).str.strip()
    out = settlements.merge(
        lookup, on="_raw_symbol", how="inner", validate="many_to_one"
    )
    if out.empty:
        raise RuntimeError("No final CL settlements matched the requested contracts")
    out["trade_date"] = pd.to_datetime(out["reference_date"]).dt.normalize()
    out["settlement"] = pd.to_numeric(out["price"], errors="coerce")
    keep = [
        "trade_date",
        "contract",
        "_raw_symbol",
        "settlement",
        "settlement_actual",
        "settlement_final",
        "received_timestamp",
    ]
    return (
        out[keep]
        .sort_values(["trade_date", "contract"])
        .drop_duplicates(["trade_date", "contract"], keep="last")
        .reset_index(drop=True)
    )


def _expiry_table(
    settlements: pd.DataFrame,
    mapping: pd.DataFrame,
    *,
    inference_end: str,
) -> pd.DataFrame:
    """Derive explicit roll boundaries from each contract last final settlement."""
    observed = (
        settlements.groupby("contract", as_index=False)["trade_date"]
        .max()
        .rename(columns={"trade_date": "last_trade_date"})
    )
    out = mapping[["contract"]].merge(observed, on="contract", how="left")
    required = out.loc[
        out["last_trade_date"].notna()
        & (out["last_trade_date"] < pd.Timestamp(inference_end))
    ].copy()
    if required.empty:
        raise RuntimeError("No completed contract roll boundaries were observed")
    # Keep the first still-active contract after the last completed boundary so
    # dates through inference_end can always be mapped.
    future = out.loc[
        out["last_trade_date"].notna()
        & (out["last_trade_date"] >= pd.Timestamp(inference_end))
    ].sort_values("last_trade_date")
    if not future.empty:
        required = pd.concat([required, future.head(1)], ignore_index=True)
    required["source"] = "Databento latest final settlement reference date"
    return required.sort_values("last_trade_date").reset_index(drop=True)


def _load_yahoo(
    *,
    cache_dir: Path,
    start: str,
    end: str,
    refresh: bool,
) -> tuple[pd.DataFrame, dict[str, Any]]:
    cache_dir.mkdir(parents=True, exist_ok=True)
    path = cache_dir / "CL_F_first_nearby_comparison.csv"
    meta_path = cache_dir / "CL_F_first_nearby_comparison.json"
    if path.exists() and not refresh:
        history = normalize_yahoo_history(pd.read_csv(path))
        if (
            history["date"].min() <= pd.Timestamp(start)
            and history["date"].max() >= pd.Timestamp(end) - pd.Timedelta(days=1)
        ):
            meta = (
                json.loads(meta_path.read_text(encoding="utf-8"))
                if meta_path.exists()
                else {}
            )
            return history, meta
    history, meta = download_yahoo_wti(ticker="CL=F", start=start, end=end)
    history.to_csv(path, index=False, date_format="%Y-%m-%d")
    meta = dict(meta)
    meta["sha256"] = dataframe_sha256(history)
    meta_path.write_text(
        json.dumps(meta, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    return history, meta


def _yahoo_return_audit(
    history: pd.DataFrame, *, start: str, end: str
) -> pd.DataFrame:
    sample = prepare_wti_model_sample(history, start=start, end=end)
    out = sample.history[["date", "close"]].copy()
    out["log_return"] = np.nan
    values = out["close"].to_numpy(dtype=float)
    out.loc[out.index[1:], "log_return"] = np.diff(np.log(values))
    out["usable_inference_return"] = out["log_return"].notna()
    return out


def _comparison_summary(
    first: pd.DataFrame, yahoo: pd.DataFrame
) -> dict[str, Any]:
    first_returns = first.loc[first["usable_inference_return"], "log_return"].to_numpy(float)
    yahoo_returns = yahoo.loc[yahoo["usable_inference_return"], "log_return"].to_numpy(float)
    merged = first[["trade_date", "settlement", "log_return"]].merge(
        yahoo[["date", "close", "log_return"]],
        left_on="trade_date",
        right_on="date",
        how="inner",
        suffixes=("_first_nearby", "_yahoo"),
    )
    paired = merged.dropna(
        subset=["log_return_first_nearby", "log_return_yahoo"]
    )
    corr = (
        float(paired["log_return_first_nearby"].corr(paired["log_return_yahoo"]))
        if len(paired) >= 2
        else None
    )
    return {
        "first_nearby_prices": int(len(first)),
        "first_nearby_usable_returns": int(len(first_returns)),
        "first_nearby_roll_switch_rows": int(first["roll_switch"].sum()),
        "first_nearby_missing_settlements": int(first["missing_settlement"].sum()),
        "first_nearby_return_mean": float(np.mean(first_returns)),
        "first_nearby_return_sd": float(np.std(first_returns, ddof=1)),
        "first_nearby_annualized_realized_vol": float(np.std(first_returns, ddof=1) * np.sqrt(252.0)),
        "yahoo_prices": int(len(yahoo)),
        "yahoo_usable_returns": int(len(yahoo_returns)),
        "yahoo_return_mean": float(np.mean(yahoo_returns)),
        "yahoo_return_sd": float(np.std(yahoo_returns, ddof=1)),
        "yahoo_annualized_realized_vol": float(np.std(yahoo_returns, ddof=1) * np.sqrt(252.0)),
        "paired_return_dates": int(len(paired)),
        "paired_return_correlation": corr,
        "paired_return_mae": (
            None
            if paired.empty
            else float(np.mean(np.abs(paired["log_return_first_nearby"] - paired["log_return_yahoo"])))
        ),
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--history-start", default=DEFAULT_HISTORY_START)
    parser.add_argument("--inference-end", default=DEFAULT_INFERENCE_END)
    parser.add_argument("--query-end", default=DEFAULT_QUERY_END)
    parser.add_argument(
        "--data-dir",
        type=Path,
        default=ROOT / "data" / "databento" / "wti_first_nearby" / "raw",
    )
    parser.add_argument(
        "--yahoo-cache-dir",
        type=Path,
        default=ROOT / "data" / "wti_yahoo",
    )
    parser.add_argument("--refresh-yahoo", action="store_true")
    parser.add_argument("--chains", type=int, default=4)
    parser.add_argument("--n-iter", type=int, default=20_000)
    parser.add_argument("--burn-in", type=int, default=4_000)
    parser.add_argument("--seed", type=int, default=20260904)
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=ROOT / "results" / "analysis" / "wti_first_nearby",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    raw_path = args.data_dir / f"cl_statistics_{args.history_start}_{args.query_end}.csv"
    if not raw_path.exists():
        raise FileNotFoundError(
            f"Missing {raw_path}. Run experiments.wti_databento_first_nearby --mode quote/download first."
        )

    mapping = _symbol_mapping(args.history_start, args.inference_end)
    raw = load_databento_csv(raw_path)
    settlements = _settlement_panel(raw, mapping)
    expiries = _expiry_table(
        settlements, mapping, inference_end=args.inference_end
    )
    inference_cutoff = pd.Timestamp(args.inference_end)
    first_input = settlements.loc[
        settlements["trade_date"] < inference_cutoff
    ].copy()
    first = reconstruct_first_nearby_settlement_history(
        first_input, expiries
    )
    first = first.loc[
        (first["trade_date"] >= pd.Timestamp(args.history_start))
        & (first["trade_date"] < inference_cutoff)
    ].reset_index(drop=True)
    missing_dates = (
        first.loc[first["missing_settlement"], "trade_date"]
        .dt.date.astype(str).tolist()
    )
    if missing_dates:
        print(
            "Warning: sparse mapped first-nearby settlement gaps will be "
            "excluded from the likelihood: "
            + ", ".join(missing_dates[:20]),
            flush=True,
        )

    yahoo_history, yahoo_meta = _load_yahoo(
        cache_dir=args.yahoo_cache_dir,
        start=args.history_start,
        end=args.inference_end,
        refresh=args.refresh_yahoo,
    )
    yahoo = _yahoo_return_audit(
        yahoo_history, start=args.history_start, end=args.inference_end
    )

    first_returns = first.loc[first["usable_inference_return"], "log_return"].to_numpy(float)
    yahoo_returns = yahoo.loc[yahoo["usable_inference_return"], "log_return"].to_numpy(float)
    first_summary, first_diag = _fit_gbm_posterior(
        first_returns, chains=args.chains, n_iter=args.n_iter,
        burn_in=args.burn_in, seed=args.seed
    )
    yahoo_summary, yahoo_diag = _fit_gbm_posterior(
        yahoo_returns, chains=args.chains, n_iter=args.n_iter,
        burn_in=args.burn_in, seed=args.seed + 1_000_000
    )
    first_summary.insert(0, "source", "reconstructed_first_nearby")
    yahoo_summary.insert(0, "source", "yahoo_CL=F")
    posterior = pd.concat([first_summary, yahoo_summary], ignore_index=True)
    first_diag.insert(0, "source", "reconstructed_first_nearby")
    yahoo_diag.insert(0, "source", "yahoo_CL=F")
    diagnostics = pd.concat([first_diag, yahoo_diag], ignore_index=True)

    comparison = _comparison_summary(first, yahoo)
    first_sigma = float(first_summary.loc[0, "sigma_posterior_mean"])
    yahoo_sigma = float(yahoo_summary.loc[0, "sigma_posterior_mean"])
    report: dict[str, Any] = {
        "history_start_inclusive": args.history_start,
        "inference_end_exclusive": args.inference_end,
        "query_end_exclusive": args.query_end,
        "roll_rule": "earliest CL contract whose empirically observed final-settlement last-trade date has not passed",
        "roll_return_policy": "exclude the first return after every contract switch",
        "missing_settlement_policy": (
            "do not impute; exclude each missing settlement date and any immediately "
            "following one-day return that depends on the missing price"
        ),
        "missing_settlement_dates": missing_dates,
        "missing_settlement_count": int(len(missing_dates)),
        "settlement_source": "Databento GLBX.MDP3 official final non-intraday CL settlement statistics",
        "yahoo_comparator": "Yahoo CL=F continuous/front-month proxy",
        "comparison": comparison,
        "posterior_sigma_mean_first_nearby": first_sigma,
        "posterior_sigma_mean_yahoo": yahoo_sigma,
        "posterior_sigma_mean_difference": first_sigma - yahoo_sigma,
        "posterior_sigma_mean_ratio": first_sigma / yahoo_sigma,
        "yahoo_snapshot_sha256": yahoo_meta.get("sha256"),
        "scientific_question": "Does replacing Yahoo CL=F by a transparent roll-clean first-nearby settlement history materially change the historical-P volatility baseline?",
        "next_action": "Use first_nearby_reconstruction_raw.csv as the physical-inference source in the canonical WTI APO driver and rerun identical strict-forward holdouts.",
    }

    args.output_dir.mkdir(parents=True, exist_ok=True)
    first.to_csv(args.output_dir / "first_nearby_reconstruction_raw.csv", index=False)
    yahoo.to_csv(args.output_dir / "yahoo_comparison_raw.csv", index=False)
    expiries.to_csv(args.output_dir / "derived_roll_boundaries.csv", index=False)
    first.loc[first["roll_switch"]].to_csv(
        args.output_dir / "roll_switches.csv", index=False
    )
    posterior.to_csv(args.output_dir / "posterior_comparison.csv", index=False)
    diagnostics.to_csv(args.output_dir / "mcmc_diagnostics.csv", index=False)
    (args.output_dir / "reconstruction_report.json").write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
