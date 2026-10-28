"""Bounded JFM *pilot* for distinguishing integration, estimation, and model risk.

No market data, no vendor API calls, and no automatic experimental sweep.
This pilot reuses the project's exact Gaussian volatility-posterior quadrature
and existing Curran Asian pricer. The fixed-volatility "reference" in its
statistical study is a Curran-model reference, NOT an exact Asian option price.
The separate multi-futures experiment computes a simulation reference and
reports its Monte Carlo standard error; these must not be conflated.

From the repo root:
    python -m experiments.jfm_oracle_pilot --quick
    python -m experiments.jfm_oracle_pilot --quick --seed 20261103

All outputs go to results/analysis/jfm_oracle_pilot/<config-hash>/.
Commit the generated CSV/JSON and interpretation notes before ending the VM.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import subprocess
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

from bayesian_asian_options.asian_futures_pricing import curran_arithmetic_futures_option
from bayesian_asian_options.gaussian_sigma_quadrature import (
    gaussian_sufficient_statistics_simulation,
    posterior_sigma_quadrature,
    quadrature_quantile,
)


@dataclass(frozen=True)
class Pilot:
    seed: int = 20261103
    annual_drift: float = 0.08
    risk_free_rate: float = 0.03
    dt: float = 1.0 / 252.0
    historical_sizes: tuple[int, ...] = (21, 252)
    volatilities: tuple[float, ...] = (0.20, 0.50)
    strikes: tuple[float, ...] = (95.0, 100.0, 105.0)
    repetitions: int = 20
    sigma_grid_points: int = 257
    sigma_min: float = 0.02
    sigma_max: float = 1.5
    forward: float = 100.0
    fixing_days: tuple[int, ...] = (7, 14, 21, 28, 35, 42, 49, 56)
    # Two fixings of each contract share the SAME idiosyncratic driver.
    contract_by_fixing: tuple[int, ...] = (0, 0, 1, 1, 2, 2, 3, 3)
    correlations: tuple[float, ...] = (1.0, 0.75, 0.50)
    # Antithetic PAIRS, not individual paths, are independent.
    mc_pairs: int = 12000
    tolerances: tuple[float, ...] = (0.001, 0.005, 0.01)


def _seed(root: int, *parts: int) -> int:
    return int(np.random.SeedSequence([root, *parts]).generate_state(1, dtype=np.uint32)[0])


def _price_curve(sigma_grid: np.ndarray, cfg: Pilot, strike: float) -> np.ndarray:
    times = np.asarray(cfg.fixing_days, dtype=float) / 252.0
    forwards = np.full(len(times), cfg.forward)
    disc = float(np.exp(-cfg.risk_free_rate * times[-1]))
    return np.array([
        curran_arithmetic_futures_option(
            realized_fixings=np.empty(0),
            forward_fixings=forwards,
            fixing_times=times,
            strike=float(strike),
            sigma=float(sig),
            discount_factor=disc,
        ) for sig in sigma_grid
    ], dtype=float)


def _price_at_sigma(cfg: Pilot, strike: float, sigma: float) -> float:
    return float(_price_curve(np.asarray([sigma]), cfg, strike)[0])


def _interpolated_curvature(x: np.ndarray, y: np.ndarray, sigma: float) -> float:
    # A cubic grid derivative is a PILOT approximation, not a validated volga.
    second = np.gradient(np.gradient(y, x, edge_order=2), x, edge_order=2)
    return float(np.interp(sigma, x, second))


def _posterior_price_interval(
    grid: np.ndarray, weights: np.ndarray, prices: np.ndarray
) -> tuple[float, float]:
    # Sort price nodes; model prices need not be monotone in sigma for every payoff.
    order = np.argsort(prices)
    sorted_prices = prices[order]
    sorted_w = weights[order]
    # Midpoint of discrete quadrature node masses is an approximate posterior CDF.
    cdf = np.cumsum(sorted_w) - 0.5 * sorted_w
    return (float(np.interp(0.025, cdf, sorted_prices)),
            float(np.interp(0.975, cdf, sorted_prices)))


def _squared_error_rmse(values: list[float]) -> float:
    v = np.asarray(values, dtype=float)
    return float(np.sqrt(np.mean(v * v)))


def _statistical_pilot(cfg: Pilot) -> tuple[list[dict], list[dict]]:
    grid = np.linspace(cfg.sigma_min, cfg.sigma_max, cfg.sigma_grid_points)
    rows: list[dict] = []
    decision: list[dict] = []
    for vi, sigma_true in enumerate(cfg.volatilities):
        for ni, n in enumerate(cfg.historical_sizes):
            sums, squares = gaussian_sufficient_statistics_simulation(
                n_obs=n, mu_true=cfg.annual_drift, sigma_true=sigma_true,
                dt=cfg.dt, replications=cfg.repetitions,
                seed=_seed(cfg.seed, 1, vi, ni),
            )
            posterior = posterior_sigma_quadrature(
                grid, n_obs=n, sum_returns=sums, sumsq_returns=squares, dt=cfg.dt
            )
            for ki, strike in enumerate(cfg.strikes):
                price_curve = _price_curve(grid, cfg, strike)
                reference = _price_at_sigma(cfg, strike, sigma_true)
                for j in range(cfg.repetitions):
                    weights = posterior.weights[j]
                    mean_sig = float(posterior.mean[j])
                    variance = float(posterior.variance[j])
                    pi = float(np.dot(weights, price_curve))
                    pm = float(np.interp(mean_sig, grid, price_curve))
                    gap = abs(pi - pm)
                    approx_gap = abs(0.5 * _interpolated_curvature(
                        grid, price_curve, mean_sig) * variance)
                    lo, hi = _posterior_price_interval(grid, weights, price_curve)
                    row = {
                        "sigma_true": sigma_true, "n_obs": n, "strike": strike,
                        "replication": j, "posterior_mean_sigma": mean_sig,
                        "posterior_variance_sigma": variance,
                        "curran_reference_at_true_sigma": reference,
                        "price_pi": pi, "price_pm": pm, "abs_integration_gap": gap,
                        "abs_pm_error_vs_curran_reference": abs(pm-reference),
                        "abs_pi_error_vs_curran_reference": abs(pi-reference),
                        "posterior_price_interval_low": lo,
                        "posterior_price_interval_high": hi,
                        "curran_reference_covered": int(lo <= reference <= hi),
                        "taylor_abs_gap_prediction": approx_gap,
                    }
                    rows.append(row)
                    for tol in cfg.tolerances:
                        use_plugin = approx_gap <= tol
                        actual_small = gap <= tol
                        decision.append({
                            "sigma_true": sigma_true, "n_obs": n,
                            "strike": strike, "replication": j,
                            "price_tolerance": tol,
                            "use_plugin": int(use_plugin),
                            "false_reassurance": int(use_plugin and not actual_small),
                            "unnecessary_integration": int(not use_plugin and actual_small),
                        })
    return rows, decision


def _mc_correlated_average(
    cfg: Pilot, sigma_true: float, strike: float, seed: int
) -> list[dict]:
    times = np.asarray(cfg.fixing_days, dtype=float) / 252.0
    if len(cfg.contract_by_fixing) != len(times):
        raise ValueError("Each fixing date must have a futures-contract ID")
    contract_ids = np.asarray(cfg.contract_by_fixing, dtype=int)
    if np.any(contract_ids < 0) or np.any(contract_ids >= len(set(contract_ids))):
        raise ValueError("Use consecutive contract IDs starting at zero")
    if np.any(np.diff(times) <= 0) or cfg.mc_pairs < 2:
        raise ValueError("Fixing times must increase and mc_pairs >= 2")
    if any(not (0.0 <= r <= 1.0) for r in cfg.correlations):
        raise ValueError("Correlation weights must lie in [0,1]")
    # Brownian increments are shared across rho, and antithetic halves are paired.
    rng = np.random.default_rng(seed)
    z = rng.standard_normal((cfg.mc_pairs, len(times), len(set(contract_ids)) + 1))
    dt_sqrt = np.sqrt(np.diff(np.concatenate(([0.0], times))))
    forward_discount = np.exp(-cfg.risk_free_rate * times[-1])
    payoffs = {rho: np.zeros(cfg.mc_pairs) for rho in cfg.correlations}
    for sign in (1.0, -1.0):
        w = np.cumsum(sign * z * dt_sqrt[None, :, None], axis=1)
        common = w[:, :, 0]
        idiosyncratic = w[:, np.arange(len(times)), contract_ids + 1]
        for rho in cfg.correlations:
            driver = np.sqrt(rho) * common + np.sqrt(1.0-rho) * idiosyncratic
            levels = cfg.forward * np.exp(
                -0.5 * sigma_true**2 * times[None, :] + sigma_true * driver
            )
            average = levels.mean(axis=1)
            payoffs[rho] += 0.5 * forward_discount * np.maximum(average - strike, 0)
    baseline = payoffs.get(1.0)
    rows = []
    for rho in cfg.correlations:
        vals = payoffs[rho]
        paired_difference = vals - baseline if baseline is not None else np.zeros_like(vals)
        rows.append({
            "sigma_true": sigma_true, "strike": strike, "rho": rho,
            "unique_contracts": len(set(contract_ids)),
            "mc_antithetic_pairs": cfg.mc_pairs,
            "mc_reference_price": float(vals.mean()),
            "mc_standard_error": float(vals.std(ddof=1) / np.sqrt(cfg.mc_pairs)),
            "difference_from_rho1": float(paired_difference.mean()),
            "paired_difference_standard_error": float(
                paired_difference.std(ddof=1) / np.sqrt(cfg.mc_pairs)
            ),
            "curran_onefactor_at_true_sigma": _price_at_sigma(cfg, strike, sigma_true),
        })
    return rows


def _write_csv(path: Path, rows: list[dict]) -> None:
    if not rows:
        raise RuntimeError("No simulated rows to save")
    with path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def run(cfg: Pilot, out_root: Path) -> Path:
    if cfg.sigma_grid_points < 9 or cfg.repetitions < 1:
        raise ValueError("Insufficient pilot quadrature or repetitions")
    params = json.dumps(asdict(cfg), sort_keys=True)
    digest = hashlib.sha256(params.encode()).hexdigest()[:16]
    out = out_root / digest
    out.mkdir(parents=True, exist_ok=True)
    stats, decisions = _statistical_pilot(cfg)
    oracle = []
    for i, sigma in enumerate(cfg.volatilities):
        for j, strike in enumerate(cfg.strikes):
            oracle.extend(_mc_correlated_average(
                cfg, sigma, strike, _seed(cfg.seed, 2, i, j)
            ))
    _write_csv(out / "pilot_pricing.csv", stats)
    _write_csv(out / "pilot_decisions.csv", decisions)
    _write_csv(out / "pilot_correlation_mc.csv", oracle)

    def sha(filename: str) -> str:
        return hashlib.sha256((out / filename).read_bytes()).hexdigest()

    try:
        commit = subprocess.check_output(
            ["git", "rev-parse", "HEAD"], stderr=subprocess.DEVNULL, text=True
        ).strip()
    except (OSError, subprocess.CalledProcessError):
        commit = None
    manifest = {
        "status": "PILOT_ONLY_NOT_CONFIRMATORY",
        "utc_generated": datetime.now(timezone.utc).isoformat(),
        "git_head": commit,
        "configuration": asdict(cfg),
        "price_reference": "Curran approximation evaluated at known generating volatility",
        "misspecification_reference": "antithetic multi-futures Monte Carlo with reported MC standard errors",
        "caution": "Numerical precision must be independently tightened before any JFM scientific claim",
        "outputs_sha256": {
            file: sha(file) for file in (
                "pilot_pricing.csv", "pilot_decisions.csv", "pilot_correlation_mc.csv"
            )
        },
    }
    (out / "pilot_manifest.json").write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    (out / "NOTES.md").write_text(
        "# JFM pilot — not a manuscript result\n\n"
        "This bounded synthetic experiment uses no purchased data. The statistical "
        "reference is a Curran-model price at known sigma, NOT an exact payoff value. "
        "Correlation stress uses a separate antithetic MC oracle with standard errors. "
        "Check numerical error before interpreting small differences. This run is "
        "development evidence, not a frozen confirmatory experiment.\n",
        encoding="utf-8",
    )
    return out


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--quick", action="store_true", help="Pilot is bounded by default.")
    parser.add_argument("--seed", type=int, default=Pilot.seed)
    parser.add_argument("--output-root", type=Path,
                        default=Path("results/analysis/jfm_oracle_pilot"))
    args = parser.parse_args()
    cfg = Pilot(seed=args.seed)
    output = run(cfg, args.output_root)
    print(f"Saved JFM pilot artifacts to {output}")
    print("PILOT ONLY: inspect and commit every CSV/JSON/NOTES file; no JFM claim yet.")


if __name__ == "__main__":
    main()
