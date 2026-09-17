"""Large-scale simulation-based calibration for the Gaussian GBM sigma posterior.

Parameters are drawn from the paper's prior, synthetic returns are drawn from the model, and
the exact-in-mu sigma quadrature is used to compute posterior CDF ranks and credible-interval
coverage.  Under a calibrated Bayesian implementation, posterior ranks are Uniform(0,1) and
nominal credible intervals have their nominal prior-predictive coverage.

The monster preset processes hundreds of thousands of synthetic datasets in GPU batches and
is intentionally much larger than the lightweight posterior-recovery checks used elsewhere.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
from scipy.stats import kstest

from bayesian_asian_options.gaussian_sigma_quadrature import (
    gaussian_gbm_marginal_log_posterior_sigma,
    normalized_sigma_weights,
    quadrature_cdf_at,
    quadrature_quantile,
)


DEFAULT_OUTPUT_ROOT = Path("results/analysis/simulation_based_calibration")


@dataclass(frozen=True)
class Config:
    sample_sizes: tuple[int, ...] = (21, 63, 252, 1260)
    replications_per_n: int = 10_000
    sigma_grid_min: float = 1e-4
    sigma_grid_max: float = 10.0
    sigma_grid_points: int = 2049
    batch_size: int = 500
    dt: float = 1.0 / 252.0
    mu_prior_sd: float = 1.0
    sigma_prior_alpha: float = 2.0
    sigma_prior_beta: float = 0.1
    root_seed: int = 20260917


@dataclass(frozen=True)
class MonsterConfig(Config):
    replications_per_n: int = 50_000
    sigma_grid_points: int = 4097
    batch_size: int = 1000


def _backend(name: str):
    if name in {"auto", "cupy"}:
        try:
            import cupy as cp  # type: ignore

            if cp.cuda.runtime.getDeviceCount() > 0:
                return cp, "cupy"
        except Exception:
            if name == "cupy":
                raise RuntimeError("CuPy backend requested but unavailable")
    if name not in {"auto", "numpy", "cupy"}:
        raise ValueError("backend must be auto, numpy, or cupy")
    return np, "numpy"


def _to_numpy(value: Any, resolved: str) -> np.ndarray:
    if resolved == "cupy":
        import cupy as cp  # type: ignore

        return np.asarray(cp.asnumpy(value))
    return np.asarray(value)


def _prior_draws(cfg: Config, rng: np.random.Generator, n: int) -> tuple[np.ndarray, np.ndarray]:
    mu = rng.normal(0.0, cfg.mu_prior_sd, size=n)
    precision_like = rng.gamma(
        shape=cfg.sigma_prior_alpha,
        scale=1.0 / cfg.sigma_prior_beta,
        size=n,
    )
    sigma = 1.0 / precision_like
    return mu, sigma


def _simulate_stats(
    *,
    n_obs: int,
    mu: np.ndarray,
    sigma: np.ndarray,
    dt: float,
    rng: np.random.Generator,
) -> tuple[np.ndarray, np.ndarray]:
    variance = sigma**2 * dt
    mean = (mu - 0.5 * sigma**2) * dt
    sample_mean = mean + np.sqrt(variance / n_obs) * rng.standard_normal(len(mu))
    centered_ss = variance * rng.chisquare(n_obs - 1, size=len(mu))
    sums = n_obs * sample_mean
    sumsquares = centered_ss + n_obs * sample_mean**2
    return sums, sumsquares


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--preset", choices=("research", "monster"), default="research")
    parser.add_argument("--backend", choices=("auto", "numpy", "cupy"), default="auto")
    parser.add_argument("--output-root", type=Path, default=DEFAULT_OUTPUT_ROOT)
    parser.add_argument("--force", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    cfg: Config = MonsterConfig() if args.preset == "monster" else Config()
    args.output_root.mkdir(parents=True, exist_ok=True)
    raw_path = args.output_root / f"sbc_raw_{args.preset}.csv"
    if raw_path.exists() and not args.force:
        print(f"Reusing completed output: {raw_path}", flush=True)
        return

    xp, resolved = _backend(args.backend)
    # Geometric spacing is important because the baseline inverse-gamma prior places mass
    # near zero and has a long right tail.
    grid = np.geomspace(cfg.sigma_grid_min, cfg.sigma_grid_max, cfg.sigma_grid_points)
    rows: list[pd.DataFrame] = []

    for n_obs in cfg.sample_sizes:
        rng = np.random.default_rng(cfg.root_seed + n_obs)
        remaining = cfg.replications_per_n
        offset = 0
        print(
            f"SBC n={n_obs}: reps={cfg.replications_per_n}, grid={cfg.sigma_grid_points}, backend={resolved}",
            flush=True,
        )
        while remaining > 0:
            batch = min(cfg.batch_size, remaining)
            mu_true, sigma_true = _prior_draws(cfg, rng, batch)
            sums, sumsquares = _simulate_stats(
                n_obs=n_obs,
                mu=mu_true,
                sigma=sigma_true,
                dt=cfg.dt,
                rng=rng,
            )
            logp = gaussian_gbm_marginal_log_posterior_sigma(
                grid,
                n_obs=n_obs,
                sum_returns=xp.asarray(sums),
                sumsq_returns=xp.asarray(sumsquares),
                dt=cfg.dt,
                mu_prior_sd=cfg.mu_prior_sd,
                sigma_prior_alpha=cfg.sigma_prior_alpha,
                sigma_prior_beta=cfg.sigma_prior_beta,
                xp=xp,
            )
            weights = normalized_sigma_weights(logp, grid, xp=xp)
            weights_np = _to_numpy(weights, resolved)

            # The quadrature weights are integration masses, not point probabilities.  Ranks
            # and quantiles must therefore reconstruct the trapezoidal interval CDF rather
            # than cumulatively summing node weights.  The latter assigns half of the next
            # interval to each interior node and becomes visibly biased for narrow posteriors.
            rank = quadrature_cdf_at(grid, weights_np, sigma_true)
            q025 = quadrature_quantile(grid, weights_np, 0.025)
            q10 = quadrature_quantile(grid, weights_np, 0.10)
            q25 = quadrature_quantile(grid, weights_np, 0.25)
            q75 = quadrature_quantile(grid, weights_np, 0.75)
            q90 = quadrature_quantile(grid, weights_np, 0.90)
            q975 = quadrature_quantile(grid, weights_np, 0.975)
            post_mean = weights_np @ grid
            rows.append(
                pd.DataFrame(
                    {
                        "n_obs": n_obs,
                        "replication": np.arange(offset, offset + batch),
                        "mu_true": mu_true,
                        "sigma_true": sigma_true,
                        "sigma_inside_grid": (sigma_true >= grid[0]) & (sigma_true <= grid[-1]),
                        "posterior_rank": rank,
                        "posterior_sigma_mean": post_mean,
                        "covered_50": (sigma_true >= q25) & (sigma_true <= q75),
                        "covered_80": (sigma_true >= q10) & (sigma_true <= q90),
                        "covered_95": (sigma_true >= q025) & (sigma_true <= q975),
                    }
                )
            )
            offset += batch
            remaining -= batch
            del logp, weights, weights_np
            if resolved == "cupy":
                xp.get_default_memory_pool().free_all_blocks()

    raw = pd.concat(rows, ignore_index=True)
    raw.to_csv(raw_path, index=False)
    summary_rows: list[dict[str, Any]] = []
    histogram_rows: list[dict[str, Any]] = []
    for n_obs, group in raw.groupby("n_obs"):
        valid = group[group["sigma_inside_grid"]]
        ranks = valid["posterior_rank"].to_numpy(dtype=float)
        ks = kstest(ranks, "uniform")
        summary_rows.append(
            {
                "n_obs": int(n_obs),
                "replications": int(len(group)),
                "inside_grid": int(len(valid)),
                "inside_grid_fraction": float(len(valid) / len(group)),
                "rank_mean": float(np.mean(ranks)),
                "rank_variance": float(np.var(ranks, ddof=1)),
                "ks_uniform_statistic": float(ks.statistic),
                "ks_uniform_pvalue": float(ks.pvalue),
                "coverage_50": float(valid["covered_50"].mean()),
                "coverage_80": float(valid["covered_80"].mean()),
                "coverage_95": float(valid["covered_95"].mean()),
                "mean_sigma_posterior_bias": float(
                    np.mean(valid["posterior_sigma_mean"] - valid["sigma_true"])
                ),
            }
        )
        counts, edges = np.histogram(ranks, bins=np.linspace(0.0, 1.0, 21))
        for i, count in enumerate(counts):
            histogram_rows.append(
                {
                    "n_obs": int(n_obs),
                    "bin_left": float(edges[i]),
                    "bin_right": float(edges[i + 1]),
                    "count": int(count),
                    "expected_count": float(len(ranks) / len(counts)),
                }
            )

    pd.DataFrame(summary_rows).to_csv(
        args.output_root / f"sbc_summary_{args.preset}.csv", index=False
    )
    pd.DataFrame(histogram_rows).to_csv(
        args.output_root / f"sbc_rank_histogram_{args.preset}.csv", index=False
    )
    report = {
        "preset": args.preset,
        "backend": resolved,
        "sample_sizes": list(cfg.sample_sizes),
        "replications_per_n": cfg.replications_per_n,
        "total_datasets": int(len(raw)),
        "sigma_grid_points": cfg.sigma_grid_points,
        "posterior_grid_evaluations": int(len(raw) * cfg.sigma_grid_points),
        "cdf_construction": "piecewise-linear density with trapezoidal interval integration",
        "calibration_targets": {"rank_mean": 0.5, "rank_variance": 1.0 / 12.0, "coverage_50": 0.50, "coverage_80": 0.80, "coverage_95": 0.95},
    }
    (args.output_root / f"sbc_report_{args.preset}.json").write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(f"Completed SBC: {args.output_root}", flush=True)


if __name__ == "__main__":
    main()
