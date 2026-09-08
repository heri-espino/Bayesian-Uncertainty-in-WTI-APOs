"""Repeated-sampling experiment for the publication-oriented manuscript.

The outer experiment generates historical returns under P. Each data set is used to
infer the posterior of (mu, sigma) by Metropolis-Hastings. Option prices are then
computed under Q, where the stock drift is r-q and only posterior uncertainty in sigma
enters the Black-Scholes Asian-option value.

The evaluation target is external to the posterior sample: the benchmark
C_Q(sigma_true). Therefore the comparison between posterior integration and plug-in
estimators is not circular.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.optimize import minimize_scalar
from scipy.stats import gaussian_kde

from src.asian_pricing import asian_arithmetic_call_mc
from src.bayesian_gbm import gbm_log_returns, gbm_mle, random_walk_metropolis_gbm


@dataclass(frozen=True)
class ExperimentConfig:
    mu_true: float = 0.08
    sigma_true: float = 0.25
    S0: float = 100.0
    K: float = 100.0
    r: float = 0.03
    q: float = 0.0
    T: float = 1.0
    monitoring_steps: int = 252
    n_obs_values: tuple[int, ...] = (63, 252, 1260)
    replications: int = 80
    mcmc_iter: int = 6_000
    burn_in: int = 1_200
    pricing_paths: int = 12_000
    pricing_grid_points: int = 77
    pricing_seed: int = 20260907


def _build_price_grid(cfg: ExperimentConfig) -> tuple[np.ndarray, np.ndarray]:
    """Build a smooth C_Q(sigma) lookup table using common random numbers."""
    sigma_grid = np.linspace(0.12, 0.50, cfg.pricing_grid_points)
    prices = np.empty_like(sigma_grid)
    for i, sigma in enumerate(sigma_grid):
        prices[i] = asian_arithmetic_call_mc(
            cfg.S0,
            cfg.K,
            cfg.r,
            float(sigma),
            cfg.T,
            q=cfg.q,
            n_steps=cfg.monitoring_steps,
            n_paths=cfg.pricing_paths,
            seed=cfg.pricing_seed,
            antithetic=True,
            geometric_control=True,
        ).price
    return sigma_grid, prices


def _price_from_grid(
    sigma: np.ndarray | float,
    sigma_grid: np.ndarray,
    price_grid: np.ndarray,
) -> np.ndarray | float:
    values = np.asarray(sigma, dtype=float)
    if np.any(values < sigma_grid[0]) or np.any(values > sigma_grid[-1]):
        raise ValueError(
            "posterior volatility fell outside the pricing grid; expand the grid"
        )
    out = np.interp(values, sigma_grid, price_grid)
    return float(out) if values.ndim == 0 else out


def _posterior_mode_kde(samples: np.ndarray) -> float:
    """Estimate a one-dimensional posterior mode with Gaussian KDE."""
    samples = np.asarray(samples, dtype=float)
    kde = gaussian_kde(samples, bw_method="scott")
    result = minimize_scalar(
        lambda x: -float(kde(x)[0]),
        bounds=(float(samples.min()), float(samples.max())),
        method="bounded",
    )
    return float(result.x)


def run_experiment(
    cfg: ExperimentConfig = ExperimentConfig(),
) -> tuple[pd.DataFrame, pd.DataFrame]:
    sigma_grid, price_grid = _build_price_grid(cfg)
    true_price = _price_from_grid(cfg.sigma_true, sigma_grid, price_grid)

    rows: list[dict[str, float | int]] = []
    for n_obs in cfg.n_obs_values:
        dt = cfg.T / n_obs
        for replication in range(cfg.replications):
            # Deterministic seed scheme used for the manuscript pilot.
            data_seed = 1000 * n_obs + replication
            chain_seed = data_seed + 100_000
            returns = gbm_log_returns(
                mu=cfg.mu_true,
                sigma=cfg.sigma_true,
                dt=dt,
                n_obs=n_obs,
                seed=data_seed,
            )
            posterior = random_walk_metropolis_gbm(
                returns,
                dt,
                n_iter=cfg.mcmc_iter,
                burn_in=cfg.burn_in,
                proposal_sd=(0.30, 0.08),
                seed=chain_seed,
            )

            sigma_draws = posterior.sigma
            posterior_prices = _price_from_grid(sigma_draws, sigma_grid, price_grid)
            sigma_map = _posterior_mode_kde(sigma_draws)
            _, sigma_mle = gbm_mle(returns, dt)

            price_full_bayes = float(np.mean(posterior_prices))
            price_postmean_plugin = _price_from_grid(
                float(np.mean(sigma_draws)), sigma_grid, price_grid
            )
            price_map_plugin = _price_from_grid(sigma_map, sigma_grid, price_grid)
            price_mle = _price_from_grid(sigma_mle, sigma_grid, price_grid)
            ci_low, ci_high = np.percentile(posterior_prices, [2.5, 97.5])

            rows.append(
                {
                    "n_obs": n_obs,
                    "replication": replication,
                    "acceptance_rate": posterior.acceptance_rate,
                    "true_price": true_price,
                    "full_bayes": price_full_bayes,
                    "postmean_plugin": price_postmean_plugin,
                    "map_plugin": price_map_plugin,
                    "mle_plugin": price_mle,
                    "price_ci_low": float(ci_low),
                    "price_ci_high": float(ci_high),
                    "sigma_post_mean": float(np.mean(sigma_draws)),
                    "sigma_map": sigma_map,
                    "sigma_mle": sigma_mle,
                }
            )

    raw = pd.DataFrame(rows)
    summary_rows: list[dict[str, float | int | str]] = []
    for n_obs, group in raw.groupby("n_obs"):
        coverage = float(
            np.mean(
                (group["price_ci_low"] <= group["true_price"])
                & (group["true_price"] <= group["price_ci_high"])
            )
        )
        for method in ("full_bayes", "postmean_plugin", "map_plugin", "mle_plugin"):
            error = group[method] - group["true_price"]
            summary_rows.append(
                {
                    "n_obs": int(n_obs),
                    "method": method,
                    "bias": float(error.mean()),
                    "mae": float(np.mean(np.abs(error))),
                    "rmse": float(np.sqrt(np.mean(error**2))),
                    "mean_acceptance_rate": float(group["acceptance_rate"].mean()),
                    "coverage_95": coverage,
                }
            )

    return raw, pd.DataFrame(summary_rows)


def main() -> None:
    raw, summary = run_experiment()
    results_dir = Path("results")
    results_dir.mkdir(exist_ok=True)
    raw.to_csv(results_dir / "publication_experiment_raw.csv", index=False)
    summary.to_csv(results_dir / "publication_experiment_summary.csv", index=False)
    print(summary.to_string(index=False))


if __name__ == "__main__":
    main()
