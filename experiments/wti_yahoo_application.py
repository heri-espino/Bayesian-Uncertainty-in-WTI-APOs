"""Empirical WTI application using Yahoo Finance ticker CL=F.

This is an empirical *illustration*, not a validation against an observed Asian-option
market price. Yahoo's CL=F history is treated as a continuous/front-month proxy and
not as a first-nearby series whose historical roll rule was reconstructed by us.

Examples
--------
Download and estimate the historical posterior only:
    conda run -n asian-options python -m experiments.wti_yahoo_application

Also price hypothetical Asian calls on the futures proxy:
    conda run -n asian-options python -m experiments.wti_yahoo_application \
        --price-asian --risk-free-rate 0.04 --backend cupy
"""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd

from bayesian_asian_options.asian_futures_pricing import asian_futures_arithmetic_call_mc_chunked
from bayesian_asian_options.bayesian_gbm import gbm_mle, random_walk_metropolis_gbm
from bayesian_asian_options.wti_yahoo import (
    DEFAULT_MODEL_START,
    DEFAULT_TICKER,
    download_yahoo_wti,
    prepare_wti_model_sample,
    write_local_snapshot,
)


def _float_list(value: str) -> list[float]:
    out = [float(x.strip()) for x in value.split(",") if x.strip()]
    if not out:
        raise argparse.ArgumentTypeError("at least one numeric value is required")
    return out


def _sigma_map(samples: np.ndarray) -> float:
    try:
        from scipy.stats import gaussian_kde

        lo, hi = np.quantile(samples, [0.001, 0.999])
        grid = np.linspace(max(1e-6, 0.9 * lo), 1.1 * hi, 512)
        return float(grid[np.argmax(gaussian_kde(samples)(grid))])
    except Exception:
        hist, edges = np.histogram(samples, bins="fd")
        i = int(np.argmax(hist))
        return float(0.5 * (edges[i] + edges[i + 1]))


def _posterior_summary(result, mu_mle: float, sigma_mle: float) -> dict[str, float]:
    mu_q = np.quantile(result.mu, [0.025, 0.5, 0.975])
    s_q = np.quantile(result.sigma, [0.025, 0.5, 0.975])
    return {
        "mu_mle": float(mu_mle),
        "sigma_mle": float(sigma_mle),
        "mu_posterior_mean": float(np.mean(result.mu)),
        "mu_posterior_median": float(mu_q[1]),
        "mu_q025": float(mu_q[0]),
        "mu_q975": float(mu_q[2]),
        "sigma_posterior_mean": float(np.mean(result.sigma)),
        "sigma_posterior_median": float(s_q[1]),
        "sigma_posterior_map": _sigma_map(result.sigma),
        "sigma_q025": float(s_q[0]),
        "sigma_q975": float(s_q[2]),
        "acceptance_rate": float(result.acceptance_rate),
    }


def _price_contracts(
    sigma_samples: np.ndarray,
    *,
    F0: float,
    r: float,
    sigma_mle: float,
    moneyness: list[float],
    maturities: list[float],
    n_steps_per_year: int,
    n_paths: int,
    sigma_grid_size: int,
    backend: str,
    chunk_size: int,
    seed: int,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    if sigma_grid_size < 11:
        raise ValueError("sigma_grid_size must be at least 11")
    lo = max(1e-5, 0.9 * float(np.min(sigma_samples)))
    hi = 1.1 * float(max(np.max(sigma_samples), sigma_mle))
    sigma_grid = np.linspace(lo, hi, sigma_grid_size)
    sigma_mean = float(np.mean(sigma_samples))
    sigma_map = _sigma_map(sigma_samples)

    summary_rows: list[dict[str, float | int | str]] = []
    grid_rows: list[dict[str, float | int | str]] = []

    contract_id = 0
    for ratio in moneyness:
        for maturity in maturities:
            K = float(ratio * F0)
            n_steps = max(1, int(round(n_steps_per_year * maturity)))
            prices = np.empty_like(sigma_grid)
            ses = np.empty_like(sigma_grid)
            resolved_backend = None

            for j, sigma in enumerate(sigma_grid):
                estimate = asian_futures_arithmetic_call_mc_chunked(
                    F0,
                    K,
                    r,
                    float(sigma),
                    maturity,
                    n_steps=n_steps,
                    n_paths=n_paths,
                    seed=seed + contract_id * 10_000 + j,
                    backend=backend,
                    chunk_size=chunk_size,
                )
                prices[j] = estimate.price
                ses[j] = estimate.standard_error
                resolved_backend = estimate.backend
                grid_rows.append(
                    {
                        "moneyness_K_over_F0": ratio,
                        "maturity": maturity,
                        "sigma": float(sigma),
                        "price": float(estimate.price),
                        "pricing_se": float(estimate.standard_error),
                        "backend": estimate.backend,
                        "n_paths": n_paths,
                    }
                )

            posterior_prices = np.interp(sigma_samples, sigma_grid, prices)
            fb = float(np.mean(posterior_prices))
            pm = float(np.interp(sigma_mean, sigma_grid, prices))
            map_price = float(np.interp(sigma_map, sigma_grid, prices))
            mle = float(np.interp(sigma_mle, sigma_grid, prices))
            p_q = np.quantile(posterior_prices, [0.025, 0.5, 0.975])
            summary_rows.append(
                {
                    "F0": F0,
                    "K": K,
                    "moneyness_K_over_F0": ratio,
                    "maturity": maturity,
                    "risk_free_rate": r,
                    "full_bayes_price": fb,
                    "postmean_plugin_price": pm,
                    "map_plugin_price": map_price,
                    "mle_plugin_price": mle,
                    "posterior_price_q025": float(p_q[0]),
                    "posterior_price_median": float(p_q[1]),
                    "posterior_price_q975": float(p_q[2]),
                    "fb_minus_pm": fb - pm,
                    "max_grid_pricing_se": float(np.max(ses)),
                    "backend": str(resolved_backend),
                    "n_paths_per_sigma": n_paths,
                    "sigma_grid_size": sigma_grid_size,
                }
            )
            contract_id += 1

    return pd.DataFrame(summary_rows), pd.DataFrame(grid_rows)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ticker", default=DEFAULT_TICKER)
    parser.add_argument("--download-period", default="max")
    parser.add_argument("--model-start", default=DEFAULT_MODEL_START)
    parser.add_argument("--model-end", default=None)
    parser.add_argument("--data-dir", type=Path, default=Path("data/wti_yahoo"))
    parser.add_argument("--output-dir", type=Path, default=Path("results/wti_yahoo"))
    parser.add_argument("--seed", type=int, default=20260909)
    parser.add_argument("--n-iter", type=int, default=50_000)
    parser.add_argument("--burn-in", type=int, default=10_000)
    parser.add_argument("--price-asian", action="store_true")
    parser.add_argument("--risk-free-rate", type=float, default=None)
    parser.add_argument("--moneyness", type=_float_list, default=[0.8, 1.0, 1.2])
    parser.add_argument("--maturities", type=_float_list, default=[0.5, 1.0, 2.0])
    parser.add_argument("--n-steps-per-year", type=int, default=252)
    parser.add_argument("--pricing-paths", type=int, default=500_000)
    parser.add_argument("--sigma-grid-size", type=int, default=61)
    parser.add_argument("--backend", choices=["auto", "numpy", "cupy"], default="auto")
    parser.add_argument("--chunk-size", type=int, default=100_000)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.price_asian and args.risk_free_rate is None:
        raise SystemExit("--risk-free-rate is required when --price-asian is used")

    generated_at = datetime.now(timezone.utc)
    history, yahoo_meta = download_yahoo_wti(ticker=args.ticker, period=args.download_period)
    safe_ticker = args.ticker.replace("=", "_").replace("/", "_")
    snapshot = args.data_dir / f"{safe_ticker}_{yahoo_meta['last_observation']}.csv"
    snapshot_sha = write_local_snapshot(history, snapshot)

    sample = prepare_wti_model_sample(history, start=args.model_start, end=args.model_end)
    dt = 1.0 / 252.0
    mu_mle, sigma_mle = gbm_mle(sample.log_returns, dt)
    mcmc = random_walk_metropolis_gbm(
        sample.log_returns,
        dt,
        n_iter=args.n_iter,
        burn_in=args.burn_in,
        theta_init=(mu_mle, float(np.log(max(sigma_mle, 1e-8)))),
        seed=args.seed,
    )
    posterior = _posterior_summary(mcmc, mu_mle, sigma_mle)

    args.output_dir.mkdir(parents=True, exist_ok=True)
    pd.DataFrame([posterior]).to_csv(args.output_dir / "posterior_summary.csv", index=False)
    np.savez_compressed(
        args.output_dir / "posterior_draws.npz",
        mu=mcmc.mu,
        sigma=mcmc.sigma,
    )

    pricing_file = None
    if args.price_asian:
        F0 = float(sample.history["close"].iloc[-1])
        pricing, grid = _price_contracts(
            mcmc.sigma,
            F0=F0,
            r=float(args.risk_free_rate),
            sigma_mle=sigma_mle,
            moneyness=args.moneyness,
            maturities=args.maturities,
            n_steps_per_year=args.n_steps_per_year,
            n_paths=args.pricing_paths,
            sigma_grid_size=args.sigma_grid_size,
            backend=args.backend,
            chunk_size=args.chunk_size,
            seed=args.seed + 1_000_000,
        )
        pricing_file = args.output_dir / "asian_pricing_summary.csv"
        pricing.to_csv(pricing_file, index=False)
        grid.to_csv(args.output_dir / "asian_pricing_grid.csv", index=False)

    manifest = {
        "generated_at_utc": generated_at.isoformat(),
        "application_type": "empirical illustration; not market-price validation",
        "data_interpretation": (
            "Yahoo CL=F continuous/front-month proxy; historical roll methodology is not reconstructed here"
        ),
        "yahoo": yahoo_meta,
        "local_snapshot": str(snapshot),
        "local_snapshot_sha256": snapshot_sha,
        "model": {
            "measure": "P",
            "dt": dt,
            "model_start_requested": args.model_start,
            "model_end_requested": args.model_end,
            "first_price_used": sample.first_date,
            "last_price_used": sample.last_date,
            "n_prices": sample.n_prices,
            "n_log_returns": sample.n_returns,
            "gbm_requires_positive_prices": True,
        },
        "mcmc": {
            "seed": args.seed,
            "n_iter": args.n_iter,
            "burn_in": args.burn_in,
            "posterior_draws": int(len(mcmc.sigma)),
        },
        "posterior": posterior,
        "asian_pricing": None
        if not args.price_asian
        else {
            "underlying_interpretation": "hypothetical arithmetic Asian call on lognormal futures proxy",
            "q_dynamics": "dF = sigma F dW_Q (zero futures drift)",
            "risk_free_rate": float(args.risk_free_rate),
            "moneyness": args.moneyness,
            "maturities": args.maturities,
            "n_steps_per_year": args.n_steps_per_year,
            "n_paths_per_sigma": args.pricing_paths,
            "sigma_grid_size": args.sigma_grid_size,
            "backend_requested": args.backend,
            "pricing_summary": str(pricing_file),
        },
    }
    (args.output_dir / "manifest.json").write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )

    print(f"Yahoo rows: {len(history)}")
    print(f"Model sample: {sample.first_date} to {sample.last_date} ({sample.n_returns} returns)")
    print(f"Snapshot SHA-256: {snapshot_sha}")
    print(f"sigma MLE: {sigma_mle:.6f}")
    print(
        "sigma posterior mean / 95% interval: "
        f"{posterior['sigma_posterior_mean']:.6f} "
        f"[{posterior['sigma_q025']:.6f}, {posterior['sigma_q975']:.6f}]"
    )
    print(f"acceptance rate: {posterior['acceptance_rate']:.4f}")
    if pricing_file is not None:
        print(f"Asian pricing summary: {pricing_file}")
    print(f"manifest: {args.output_dir / 'manifest.json'}")


if __name__ == "__main__":
    main()
