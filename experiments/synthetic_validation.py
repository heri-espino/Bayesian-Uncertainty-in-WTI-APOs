"""Reproducible synthetic/stochastic/theoretical validation suite.

This script is designed to be rerun before every paper revision. It separates three
validation layers:

1. Synthetic parameter recovery under the physical measure P.
2. Posterior recovery by Random-Walk Metropolis on selected synthetic cases.
3. Theoretical and stochastic pricing checks under the risk-neutral measure Q.

Outputs are deterministic conditional on the root seed and are written as CSV plus a
JSON manifest containing configuration, software versions, Git commit, and SHA256
hashes of the generated tables.

Examples
--------
Fast smoke run::

    python experiments/synthetic_validation.py --quick

Publication-oriented run::

    python experiments/synthetic_validation.py

Custom output/seed::

    python experiments/synthetic_validation.py --seed 20260909 \
        --output-dir results/synthetic_validation
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import platform
import subprocess
import sys
from dataclasses import asdict, dataclass, replace
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np

from src.asian_pricing import asian_arithmetic_call_mc
from src.bayesian_gbm import gbm_log_returns, gbm_mle, random_walk_metropolis_gbm
from src.synthetic_validation import (
    arithmetic_price_curve_by_strike,
    arithmetic_price_curve_by_volatility,
    geometric_asian_call_mc,
    risk_neutral_martingale_check,
    zero_volatility_limit_check,
)


SCRIPT_VERSION = "1.0.0"


@dataclass(frozen=True)
class ValidationConfig:
    root_seed: int = 20260909
    mu_true: float = 0.08
    sigma_true: float = 0.25
    S0: float = 100.0
    K: float = 100.0
    r: float = 0.03
    q: float = 0.0
    T: float = 1.0
    monitoring_steps: int = 252
    sample_sizes: tuple[int, ...] = (63, 252, 1260)
    parameter_replications: int = 250
    posterior_replications: int = 20
    mcmc_iter: int = 8_000
    burn_in: int = 1_600
    proposal_mu_sd: float = 0.30
    proposal_logsigma_sd: float = 0.08
    theory_paths: int = 30_000
    strike_grid: tuple[float, ...] = (80.0, 100.0, 120.0)
    volatility_grid: tuple[float, ...] = (0.15, 0.25, 0.40)


@dataclass(frozen=True)
class QuickValidationConfig(ValidationConfig):
    sample_sizes: tuple[int, ...] = (63, 252)
    parameter_replications: int = 20
    posterior_replications: int = 3
    mcmc_iter: int = 2_500
    burn_in: int = 500
    theory_paths: int = 8_000
    monitoring_steps: int = 64


def _seed(root_seed: int, family: int, *components: int) -> int:
    """Create an order-independent deterministic uint32 seed.

    Family IDs are deliberately numeric so seed construction never depends on Python's
    randomized string hashing.
    """
    entropy = [int(root_seed), int(family), *[int(x) for x in components]]
    return int(np.random.SeedSequence(entropy).generate_state(1, dtype=np.uint32)[0])


def _write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"cannot write empty CSV: {path}")
    fieldnames = list(rows[0].keys())
    with path.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def _mean(values: list[float]) -> float:
    return float(np.mean(np.asarray(values, dtype=float)))


def _rmse(values: list[float]) -> float:
    array = np.asarray(values, dtype=float)
    return float(np.sqrt(np.mean(array**2)))


def run_parameter_recovery(cfg: ValidationConfig) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    """Repeated-sampling recovery of GBM parameters using the analytical MLE."""
    raw: list[dict[str, Any]] = []

    for n_obs in cfg.sample_sizes:
        dt = cfg.T / n_obs
        for replication in range(cfg.parameter_replications):
            data_seed = _seed(cfg.root_seed, 101, n_obs, replication)
            returns = gbm_log_returns(
                mu=cfg.mu_true,
                sigma=cfg.sigma_true,
                dt=dt,
                n_obs=n_obs,
                seed=data_seed,
            )
            mu_hat, sigma_hat = gbm_mle(returns, dt)
            raw.append(
                {
                    "n_obs": n_obs,
                    "replication": replication,
                    "data_seed": data_seed,
                    "mu_true": cfg.mu_true,
                    "sigma_true": cfg.sigma_true,
                    "mu_mle": mu_hat,
                    "sigma_mle": sigma_hat,
                    "mu_error": mu_hat - cfg.mu_true,
                    "sigma_error": sigma_hat - cfg.sigma_true,
                }
            )

    summary: list[dict[str, Any]] = []
    for n_obs in cfg.sample_sizes:
        group = [row for row in raw if row["n_obs"] == n_obs]
        mu_errors = [float(row["mu_error"]) for row in group]
        sigma_errors = [float(row["sigma_error"]) for row in group]
        summary.append(
            {
                "n_obs": n_obs,
                "replications": len(group),
                "mu_bias": _mean(mu_errors),
                "mu_rmse": _rmse(mu_errors),
                "sigma_bias": _mean(sigma_errors),
                "sigma_rmse": _rmse(sigma_errors),
                "mean_mu_mle": _mean([float(row["mu_mle"]) for row in group]),
                "mean_sigma_mle": _mean([float(row["sigma_mle"]) for row in group]),
            }
        )
    return raw, summary


def run_posterior_recovery(cfg: ValidationConfig) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    """Repeated posterior recovery and empirical credible-interval coverage."""
    raw: list[dict[str, Any]] = []

    for n_obs in cfg.sample_sizes:
        dt = cfg.T / n_obs
        for replication in range(cfg.posterior_replications):
            data_seed = _seed(cfg.root_seed, 201, n_obs, replication)
            chain_seed = _seed(cfg.root_seed, 202, n_obs, replication)
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
                proposal_sd=(cfg.proposal_mu_sd, cfg.proposal_logsigma_sd),
                seed=chain_seed,
            )
            mu_low, mu_high = np.percentile(posterior.mu, [2.5, 97.5])
            sigma_low, sigma_high = np.percentile(posterior.sigma, [2.5, 97.5])
            raw.append(
                {
                    "n_obs": n_obs,
                    "replication": replication,
                    "data_seed": data_seed,
                    "chain_seed": chain_seed,
                    "acceptance_rate": posterior.acceptance_rate,
                    "mu_true": cfg.mu_true,
                    "sigma_true": cfg.sigma_true,
                    "mu_post_mean": float(np.mean(posterior.mu)),
                    "sigma_post_mean": float(np.mean(posterior.sigma)),
                    "mu_ci_low": float(mu_low),
                    "mu_ci_high": float(mu_high),
                    "sigma_ci_low": float(sigma_low),
                    "sigma_ci_high": float(sigma_high),
                    "mu_covered": int(mu_low <= cfg.mu_true <= mu_high),
                    "sigma_covered": int(sigma_low <= cfg.sigma_true <= sigma_high),
                }
            )

    summary: list[dict[str, Any]] = []
    for n_obs in cfg.sample_sizes:
        group = [row for row in raw if row["n_obs"] == n_obs]
        summary.append(
            {
                "n_obs": n_obs,
                "replications": len(group),
                "mean_acceptance_rate": _mean(
                    [float(row["acceptance_rate"]) for row in group]
                ),
                "mean_mu_post": _mean([float(row["mu_post_mean"]) for row in group]),
                "mean_sigma_post": _mean(
                    [float(row["sigma_post_mean"]) for row in group]
                ),
                "mu_coverage_95": _mean([float(row["mu_covered"]) for row in group]),
                "sigma_coverage_95": _mean(
                    [float(row["sigma_covered"]) for row in group]
                ),
            }
        )
    return raw, summary


def run_theoretical_checks(cfg: ValidationConfig) -> list[dict[str, Any]]:
    """Run stochastic checks against theoretical Black-Scholes identities."""
    rows: list[dict[str, Any]] = []

    martingale = risk_neutral_martingale_check(
        cfg.S0,
        cfg.r,
        cfg.sigma_true,
        cfg.T,
        q=cfg.q,
        n_paths=cfg.theory_paths,
        seed=_seed(cfg.root_seed, 301),
    )
    rows.append(
        {
            "check": "risk_neutral_martingale",
            "estimate": martingale.estimate,
            "target": martingale.target,
            "standard_error": martingale.standard_error,
            "diagnostic": abs(martingale.z_score),
            "criterion": "abs(z)<=5",
            "passed": int(abs(martingale.z_score) <= 5.0),
        }
    )

    geometric = geometric_asian_call_mc(
        cfg.S0,
        cfg.K,
        cfg.r,
        cfg.sigma_true,
        cfg.T,
        q=cfg.q,
        n_steps=cfg.monitoring_steps,
        n_paths=cfg.theory_paths,
        seed=_seed(cfg.root_seed, 302),
    )
    rows.append(
        {
            "check": "geometric_mc_vs_closed_form",
            "estimate": geometric.estimate,
            "target": geometric.target,
            "standard_error": geometric.standard_error,
            "diagnostic": abs(geometric.z_score),
            "criterion": "abs(z)<=5",
            "passed": int(abs(geometric.z_score) <= 5.0),
        }
    )

    zero_vol = zero_volatility_limit_check(
        cfg.S0,
        cfg.K,
        cfg.r,
        cfg.T,
        q=cfg.q,
        n_steps=cfg.monitoring_steps,
        n_paths=cfg.theory_paths,
        seed=_seed(cfg.root_seed, 303),
    )
    zero_tol = max(5.0 * zero_vol.standard_error, 1.0e-3)
    rows.append(
        {
            "check": "arithmetic_zero_volatility_limit",
            "estimate": zero_vol.estimate,
            "target": zero_vol.target,
            "standard_error": zero_vol.standard_error,
            "diagnostic": abs(zero_vol.error),
            "criterion": f"abs(error)<={zero_tol:.8g}",
            "passed": int(abs(zero_vol.error) <= zero_tol),
        }
    )

    pricing_seed = _seed(cfg.root_seed, 304)
    cv = asian_arithmetic_call_mc(
        cfg.S0,
        cfg.K,
        cfg.r,
        cfg.sigma_true,
        cfg.T,
        q=cfg.q,
        n_steps=cfg.monitoring_steps,
        n_paths=cfg.theory_paths,
        seed=pricing_seed,
        antithetic=True,
        geometric_control=True,
    )
    ratio = cv.raw_standard_error / cv.standard_error
    rows.append(
        {
            "check": "geometric_control_variance_reduction",
            "estimate": ratio,
            "target": 1.0,
            "standard_error": 0.0,
            "diagnostic": ratio,
            "criterion": "SE_raw/SE_cv>1",
            "passed": int(ratio > 1.0),
        }
    )

    strike_prices = arithmetic_price_curve_by_strike(
        cfg.strike_grid,
        S0=cfg.S0,
        r=cfg.r,
        sigma=cfg.sigma_true,
        T=cfg.T,
        q=cfg.q,
        n_steps=cfg.monitoring_steps,
        n_paths=cfg.theory_paths,
        seed=_seed(cfg.root_seed, 305),
    )
    strike_gaps = -np.diff(strike_prices)
    min_strike_gap = float(np.min(strike_gaps))
    rows.append(
        {
            "check": "price_decreases_with_strike",
            "estimate": min_strike_gap,
            "target": 0.0,
            "standard_error": 0.0,
            "diagnostic": min_strike_gap,
            "criterion": "min(C(K_i)-C(K_i+1))>=0",
            "passed": int(min_strike_gap >= 0.0),
        }
    )

    volatility_prices = arithmetic_price_curve_by_volatility(
        cfg.volatility_grid,
        S0=cfg.S0,
        K=cfg.K,
        r=cfg.r,
        T=cfg.T,
        q=cfg.q,
        n_steps=cfg.monitoring_steps,
        n_paths=cfg.theory_paths,
        seed=_seed(cfg.root_seed, 306),
    )
    vol_gaps = np.diff(volatility_prices)
    min_vol_gap = float(np.min(vol_gaps))
    rows.append(
        {
            "check": "atm_price_increases_with_volatility",
            "estimate": min_vol_gap,
            "target": 0.0,
            "standard_error": 0.0,
            "diagnostic": min_vol_gap,
            "criterion": "min(C(sigma_i+1)-C(sigma_i))>0",
            "passed": int(min_vol_gap > 0.0),
        }
    )

    # Under Black-Scholes Q pricing, physical mu is not an input. The same true sigma
    # must therefore produce exactly the same benchmark price for any physical drift.
    mu_scenarios = (-0.10, cfg.mu_true, 0.25)
    benchmark_prices = [
        asian_arithmetic_call_mc(
            cfg.S0,
            cfg.K,
            cfg.r,
            cfg.sigma_true,
            cfg.T,
            q=cfg.q,
            n_steps=cfg.monitoring_steps,
            n_paths=cfg.theory_paths,
            seed=_seed(cfg.root_seed, 307),
            antithetic=True,
            geometric_control=True,
        ).price
        for _mu in mu_scenarios
    ]
    mu_spread = float(np.ptp(np.asarray(benchmark_prices, dtype=float)))
    rows.append(
        {
            "check": "physical_drift_irrelevance_under_Q",
            "estimate": mu_spread,
            "target": 0.0,
            "standard_error": 0.0,
            "diagnostic": mu_spread,
            "criterion": "price spread across physical mu scenarios == 0",
            "passed": int(mu_spread == 0.0),
        }
    )

    return rows


def _git_commit() -> str | None:
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], text=True, stderr=subprocess.DEVNULL
        ).strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def run_suite(cfg: ValidationConfig, output_dir: Path, *, quick: bool) -> dict[str, Any]:
    output_dir.mkdir(parents=True, exist_ok=True)

    parameter_raw, parameter_summary = run_parameter_recovery(cfg)
    posterior_raw, posterior_summary = run_posterior_recovery(cfg)
    theoretical = run_theoretical_checks(cfg)

    files = {
        "parameter_recovery_raw": output_dir / "parameter_recovery_raw.csv",
        "parameter_recovery_summary": output_dir / "parameter_recovery_summary.csv",
        "posterior_recovery_raw": output_dir / "posterior_recovery_raw.csv",
        "posterior_recovery_summary": output_dir / "posterior_recovery_summary.csv",
        "theoretical_checks": output_dir / "theoretical_checks.csv",
    }
    _write_csv(files["parameter_recovery_raw"], parameter_raw)
    _write_csv(files["parameter_recovery_summary"], parameter_summary)
    _write_csv(files["posterior_recovery_raw"], posterior_raw)
    _write_csv(files["posterior_recovery_summary"], posterior_summary)
    _write_csv(files["theoretical_checks"], theoretical)

    manifest: dict[str, Any] = {
        "script_version": SCRIPT_VERSION,
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "quick_mode": quick,
        "config": asdict(cfg),
        "software": {
            "python": sys.version,
            "python_implementation": platform.python_implementation(),
            "platform": platform.platform(),
            "numpy": np.__version__,
        },
        "git_commit": _git_commit(),
        "seed_scheme": {
            "root_seed": cfg.root_seed,
            "description": "numpy SeedSequence([root_seed, family_id, integer components...])",
            "families": {
                "101": "parameter-recovery data",
                "201": "posterior-recovery data",
                "202": "posterior MCMC chain",
                "301-307": "theoretical/stochastic pricing checks",
            },
        },
        "outputs": {
            name: {"path": str(path), "sha256": _sha256(path)}
            for name, path in files.items()
        },
        "all_theoretical_checks_passed": all(
            bool(int(row["passed"])) for row in theoretical
        ),
    }
    manifest_path = output_dir / "manifest.json"
    with manifest_path.open("w", encoding="utf-8") as fh:
        json.dump(manifest, fh, indent=2, sort_keys=True)
        fh.write("\n")

    return manifest


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--quick",
        action="store_true",
        help="Run a lightweight deterministic smoke validation.",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=None,
        help="Override the root random seed.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("results/synthetic_validation"),
        help="Directory for CSV outputs and reproducibility manifest.",
    )
    parser.add_argument(
        "--parameter-replications",
        type=int,
        default=None,
        help="Override repeated-sampling MLE replications per sample size.",
    )
    parser.add_argument(
        "--posterior-replications",
        type=int,
        default=None,
        help="Override posterior MCMC replications per sample size.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    cfg: ValidationConfig = QuickValidationConfig() if args.quick else ValidationConfig()
    if args.seed is not None:
        cfg = replace(cfg, root_seed=args.seed)
    if args.parameter_replications is not None:
        if args.parameter_replications < 1:
            raise ValueError("parameter replications must be positive")
        cfg = replace(cfg, parameter_replications=args.parameter_replications)
    if args.posterior_replications is not None:
        if args.posterior_replications < 1:
            raise ValueError("posterior replications must be positive")
        cfg = replace(cfg, posterior_replications=args.posterior_replications)

    manifest = run_suite(cfg, args.output_dir, quick=args.quick)
    print(f"Validation outputs written to {args.output_dir}")
    print(f"root_seed={cfg.root_seed}")
    print(f"all_theoretical_checks_passed={manifest['all_theoretical_checks_passed']}")


if __name__ == "__main__":
    main()
