"""Monte Carlo convergence study for an already completed empirical WTI APO run.

The experiment holds fixed the empirical posterior, contract, fixing state, discount factor,
and sigma grid.  Only the number of pricing paths and the Monte Carlo seed change.  This
isolates whether a small posterior-integrated minus posterior-mean (PI-PM) price gap is
numerically resolved rather than an artifact of one simulation draw.

By default the script chooses the contract with the largest absolute PI-PM gap in the source
run, making the diagnostic conservative for the manuscript's main comparison.

Example
-------
    python -m experiments.wti_mc_convergence \
        --run-dir results/wti_apo_empirical/2026-09-04_202610 \
        --preset research
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

from bayesian_asian_options.wti_apo_pricing import wti_apo_cross_section_mc


DEFAULT_RUN = Path("results/wti_apo_empirical/2026-09-04_202610")
DEFAULT_OUTPUT = Path("results/analysis/wti_mc_convergence")


def _load_manifest(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _split_fixing_state(
    fixing_state: pd.DataFrame, valuation_date: pd.Timestamp
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    frame = fixing_state.copy()
    frame["fixing_date"] = pd.to_datetime(frame["fixing_date"]).dt.normalize()
    if "fixing_status" in frame.columns:
        realized = frame[frame["fixing_status"] == "realized"].copy()
        remaining = frame[frame["fixing_status"] == "remaining"].copy()
    else:
        realized = frame[frame["fixing_date"] <= valuation_date].copy()
        remaining = frame[frame["fixing_date"] > valuation_date].copy()
    realized_values = realized["settlement"].to_numpy(dtype=float)
    forward_values = remaining["settlement"].to_numpy(dtype=float)
    times = (
        (remaining["fixing_date"] - valuation_date).dt.days.to_numpy(dtype=float) / 365.25
    )
    return realized_values, forward_values, times


def _select_contract(pricing: pd.DataFrame, contract_id: str | None) -> pd.Series:
    if contract_id is not None:
        selected = pricing[pricing["contract_id"].astype(str) == str(contract_id)]
        if selected.empty:
            raise ValueError(f"contract_id {contract_id!r} not found in source run")
        return selected.iloc[0]
    if "fb_minus_pm" not in pricing.columns:
        raise ValueError("contract_pricing.csv has no fb_minus_pm column")
    index = pricing["fb_minus_pm"].abs().idxmax()
    return pricing.loc[index]


def _preset(name: str) -> tuple[tuple[int, ...], int]:
    if name == "quick":
        return (5_000, 20_000), 3
    if name == "research":
        return (10_000, 25_000, 50_000, 100_000, 250_000, 500_000), 12
    if name == "extreme":
        return (25_000, 50_000, 100_000, 250_000, 500_000, 1_000_000), 24
    raise ValueError(name)


def run(
    run_dir: Path,
    *,
    contract_id: str | None,
    path_budgets: tuple[int, ...],
    replications: int,
    seed: int,
) -> tuple[pd.DataFrame, pd.DataFrame, dict[str, Any]]:
    manifest = _load_manifest(run_dir / "manifest.json")
    valuation_date = pd.Timestamp(manifest["valuation_date"]).normalize()
    discounting = manifest["discounting"]
    discount_factor = float(discounting["discount_factor"])
    time_to_expiry = float(discounting["time_to_payoff_years"])

    pricing = pd.read_csv(run_dir / "contract_pricing.csv")
    contract = _select_contract(pricing, contract_id)
    fixing_state = pd.read_csv(run_dir / "apo_fixing_state.csv")
    realized, forwards, fixing_times = _split_fixing_state(fixing_state, valuation_date)
    with np.load(run_dir / "posterior_draws.npz", allow_pickle=False) as data:
        sigma_samples = data["sigma"].astype(float)
    if sigma_samples.ndim != 1 or sigma_samples.size == 0:
        raise ValueError("posterior_draws.npz contains no one-dimensional sigma posterior")

    sigma_mean = float(np.mean(sigma_samples))
    sigma_mle = float(pd.read_csv(run_dir / "posterior_summary.csv")["sigma_mle"].iloc[0])
    lo = max(1e-6, 0.9 * float(np.quantile(sigma_samples, 0.001)))
    hi = 1.1 * float(max(np.quantile(sigma_samples, 0.999), sigma_mle))
    grid_size = int(manifest.get("pricing", {}).get("sigma_grid_size", 41))
    sigma_grid = np.linspace(lo, hi, grid_size)

    rows: list[dict[str, Any]] = []
    for n_paths in path_budgets:
        if n_paths < 2:
            raise ValueError("all path budgets must be at least two")
        for replication in range(replications):
            common_seed = seed + 1_000_003 * replication + 101 * int(n_paths)
            grid_prices = np.empty_like(sigma_grid)
            grid_ses = np.empty_like(sigma_grid)
            for j, sigma in enumerate(sigma_grid):
                estimate = wti_apo_cross_section_mc(
                    realized_fixings=realized,
                    forward_fixings=forwards,
                    fixing_times=fixing_times,
                    strikes=np.array([float(contract["strike"])]),
                    option_types=[str(contract["option_type"])],
                    sigma=float(sigma),
                    rate=None,
                    time_to_expiry=time_to_expiry,
                    discount_factor=discount_factor,
                    n_paths=int(n_paths),
                    seed=common_seed,
                    antithetic=True,
                )
                grid_prices[j] = estimate.prices[0]
                grid_ses[j] = estimate.standard_errors[0]
            posterior_prices = np.interp(sigma_samples, sigma_grid, grid_prices)
            pi_price = float(np.mean(posterior_prices))
            pm_price = float(np.interp(sigma_mean, sigma_grid, grid_prices))
            rows.append(
                {
                    "contract_id": str(contract["contract_id"]),
                    "n_paths": int(n_paths),
                    "replication": replication,
                    "seed": common_seed,
                    "posterior_integrated_price": pi_price,
                    "posterior_mean_plugin_price": pm_price,
                    "pi_minus_pm": pi_price - pm_price,
                    "abs_pi_minus_pm": abs(pi_price - pm_price),
                    "max_grid_pricing_se": float(np.max(grid_ses)),
                }
            )

    raw = pd.DataFrame(rows)
    summary_rows: list[dict[str, Any]] = []
    for n_paths, group in raw.groupby("n_paths", sort=True):
        gaps = group["pi_minus_pm"].to_numpy(dtype=float)
        pi = group["posterior_integrated_price"].to_numpy(dtype=float)
        pm = group["posterior_mean_plugin_price"].to_numpy(dtype=float)
        summary_rows.append(
            {
                "n_paths": int(n_paths),
                "replications": int(len(group)),
                "mean_pi_price": float(np.mean(pi)),
                "sd_pi_price": float(np.std(pi, ddof=1)) if len(pi) > 1 else 0.0,
                "mean_pm_price": float(np.mean(pm)),
                "sd_pm_price": float(np.std(pm, ddof=1)) if len(pm) > 1 else 0.0,
                "mean_pi_minus_pm": float(np.mean(gaps)),
                "sd_pi_minus_pm": float(np.std(gaps, ddof=1)) if len(gaps) > 1 else 0.0,
                "mcse_mean_pi_minus_pm": (
                    float(np.std(gaps, ddof=1) / np.sqrt(len(gaps))) if len(gaps) > 1 else 0.0
                ),
                "mean_max_grid_pricing_se": float(group["max_grid_pricing_se"].mean()),
            }
        )
    summary = pd.DataFrame(summary_rows).sort_values("n_paths")
    reference = summary.iloc[-1]
    summary["gap_difference_from_largest_budget"] = (
        summary["mean_pi_minus_pm"] - float(reference["mean_pi_minus_pm"])
    )

    report = {
        "source_run": str(run_dir),
        "contract_id": str(contract["contract_id"]),
        "option_type": str(contract["option_type"]),
        "strike": float(contract["strike"]),
        "market_price": float(contract["market_price"]),
        "source_run_pi_minus_pm": float(contract["fb_minus_pm"]),
        "sigma_posterior_mean": sigma_mean,
        "posterior_draws": int(sigma_samples.size),
        "n_realized_fixings": int(realized.size),
        "n_remaining_fixings": int(forwards.size),
        "largest_path_budget": int(reference["n_paths"]),
        "largest_budget_mean_gap": float(reference["mean_pi_minus_pm"]),
        "largest_budget_gap_mcse": float(reference["mcse_mean_pi_minus_pm"]),
        "interpretation": (
            "The standard deviation across independent pricing seeds measures numerical "
            "Monte Carlo variability with the posterior and market state held fixed."
        ),
    }
    return raw, summary, report


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-dir", type=Path, default=DEFAULT_RUN)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--contract-id", default=None)
    parser.add_argument("--preset", choices=("quick", "research", "extreme"), default="research")
    parser.add_argument("--replications", type=int, default=None)
    parser.add_argument("--seed", type=int, default=20260917)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    budgets, default_replications = _preset(args.preset)
    replications = default_replications if args.replications is None else args.replications
    if replications < 1:
        raise ValueError("replications must be positive")
    raw, summary, report = run(
        args.run_dir,
        contract_id=args.contract_id,
        path_budgets=budgets,
        replications=replications,
        seed=args.seed,
    )
    args.output_dir.mkdir(parents=True, exist_ok=True)
    raw.to_csv(args.output_dir / "wti_mc_convergence_raw.csv", index=False)
    summary.to_csv(args.output_dir / "wti_mc_convergence_summary.csv", index=False)
    with (args.output_dir / "wti_mc_convergence_report.json").open("w", encoding="utf-8") as fh:
        json.dump(report, fh, indent=2, sort_keys=True)
        fh.write("\n")
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
