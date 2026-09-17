"""Prior-hyperparameter and historical-window sensitivity for WTI volatility uncertainty.

This experiment reuses the physical-return audit and fixing state of a completed empirical
WTI APO run.  It varies two statistical design choices while holding the Q-pricing model and
contract state fixed:

1. the number of most-recent daily returns entering the physical-measure likelihood;
2. hyperparameters of the existing inverse-gamma prior on sigma.

The baseline prior is preserved exactly.  Two WTI-centered alternatives are included to
show whether the posterior-integrated minus posterior-mean (PI-PM) conclusion is an artifact
of the original prior.  These are same-family sensitivity checks, not a claim that the
inverse-gamma family is uniquely appropriate.

For numerical separation from Monte Carlo noise, the experiment maps each posterior through
the Curran (1994) geometric-conditioning approximation under the same one-factor futures
model.  The resulting sensitivity is a robustness diagnostic for the parameter-uncertainty
mechanism; the manuscript's baseline market comparison remains the Monte Carlo engine.

Example
-------
    python -m experiments.wti_prior_window_sensitivity \
        --run-dir results/wti_apo_empirical/2026-09-04_202610 \
        --preset research
"""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

from bayesian_asian_options.asian_futures_pricing import curran_arithmetic_futures_option
from bayesian_asian_options.bayesian_gbm import gbm_mle, random_walk_metropolis_gbm


DEFAULT_RUN = Path("results/wti_apo_empirical/2026-09-04_202610")
DEFAULT_OUTPUT = Path("results/analysis/wti_prior_window_sensitivity")


@dataclass(frozen=True)
class PriorProfile:
    name: str
    alpha: float
    beta: float

    @property
    def mean(self) -> float:
        return self.beta / (self.alpha - 1.0) if self.alpha > 1 else float("inf")

    @property
    def sd(self) -> float:
        if self.alpha <= 2:
            return float("inf")
        variance = self.beta**2 / ((self.alpha - 1.0) ** 2 * (self.alpha - 2.0))
        return float(np.sqrt(variance))


PRIORS = (
    PriorProfile("baseline", 2.0, 0.1),
    PriorProfile("wti_centered_broad", 3.0, 0.8),
    PriorProfile("wti_centered_moderate", 10.0, 3.6),
)


def _rhat(chains: np.ndarray) -> float:
    x = np.asarray(chains, dtype=float)
    if x.ndim != 2 or x.shape[0] < 2 or x.shape[1] < 2:
        return float("nan")
    n = x.shape[1]
    within = float(np.mean(np.var(x, axis=1, ddof=1)))
    if within <= 0:
        return 1.0
    between = float(n * np.var(np.mean(x, axis=1), ddof=1))
    var_hat = ((n - 1) / n) * within + between / n
    return float(np.sqrt(var_hat / within))


def _proposal(n_obs: int) -> tuple[float, float]:
    scale = float(np.sqrt(252.0 / n_obs))
    return 0.30 * scale, 0.08 * scale


def _load_returns(run_dir: Path) -> np.ndarray:
    audit = pd.read_csv(run_dir / "inference_return_audit.csv")
    required = {"log_return", "usable_inference_return"}
    missing = required.difference(audit.columns)
    if missing:
        raise ValueError(f"inference return audit is missing {sorted(missing)}")
    usable = audit["usable_inference_return"].astype(str).str.lower().isin({"true", "1"})
    returns = audit.loc[usable, "log_return"].dropna().to_numpy(dtype=float)
    if returns.size < 63:
        raise ValueError("at least 63 usable returns are required")
    return returns


def _load_contract_state(
    run_dir: Path, contract_id: str | None
) -> tuple[pd.Series, np.ndarray, np.ndarray, np.ndarray, float, float]:
    manifest = json.loads((run_dir / "manifest.json").read_text(encoding="utf-8"))
    valuation_date = pd.Timestamp(manifest["valuation_date"]).normalize()
    pricing = pd.read_csv(run_dir / "contract_pricing.csv")
    if contract_id is None:
        contract = pricing.loc[pricing["fb_minus_pm"].abs().idxmax()]
    else:
        matches = pricing[pricing["contract_id"].astype(str) == str(contract_id)]
        if matches.empty:
            raise ValueError(f"contract_id {contract_id!r} not found")
        contract = matches.iloc[0]

    state = pd.read_csv(run_dir / "apo_fixing_state.csv")
    state["fixing_date"] = pd.to_datetime(state["fixing_date"]).dt.normalize()
    if "fixing_status" in state.columns:
        realized = state[state["fixing_status"] == "realized"].copy()
        remaining = state[state["fixing_status"] == "remaining"].copy()
    else:
        realized = state[state["fixing_date"] <= valuation_date].copy()
        remaining = state[state["fixing_date"] > valuation_date].copy()
    realized_fixings = realized["settlement"].to_numpy(dtype=float)
    forward_fixings = remaining["settlement"].to_numpy(dtype=float)
    fixing_times = (
        (remaining["fixing_date"] - valuation_date).dt.days.to_numpy(dtype=float) / 365.25
    )
    discount = float(manifest["discounting"]["discount_factor"])
    time_to_payoff = float(manifest["discounting"]["time_to_payoff_years"])
    return contract, realized_fixings, forward_fixings, fixing_times, discount, time_to_payoff


def _run_chains(
    returns: np.ndarray,
    *,
    prior: PriorProfile,
    chains: int,
    n_iter: int,
    burn_in: int,
    seed: int,
) -> tuple[np.ndarray, dict[str, float]]:
    if chains < 2:
        raise ValueError("at least two chains are required")
    dt = 1.0 / 252.0
    mu_mle, sigma_mle = gbm_mle(returns, dt)
    sigma_chains: list[np.ndarray] = []
    acceptance: list[float] = []
    for chain in range(chains):
        result = random_walk_metropolis_gbm(
            returns,
            dt,
            n_iter=n_iter,
            burn_in=burn_in,
            theta_init=(mu_mle, float(np.log(max(sigma_mle, 1e-8)))),
            proposal_sd=_proposal(len(returns)),
            sigma_prior_alpha=prior.alpha,
            sigma_prior_beta=prior.beta,
            seed=seed + 100_003 * chain,
        )
        sigma_chains.append(result.sigma)
        acceptance.append(result.acceptance_rate)
    matrix = np.vstack(sigma_chains)
    pooled = matrix.reshape(-1)
    return pooled, {
        "sigma_mle": float(sigma_mle),
        "sigma_rhat": _rhat(matrix),
        "mean_acceptance_rate": float(np.mean(acceptance)),
    }


def _preset(name: str) -> tuple[int, int, int]:
    if name == "quick":
        return 2, 3_000, 600
    if name == "research":
        return 4, 20_000, 4_000
    if name == "extreme":
        return 6, 40_000, 8_000
    raise ValueError(name)


def run(
    run_dir: Path,
    output_dir: Path,
    *,
    contract_id: str | None,
    windows: tuple[int, ...],
    chains: int,
    n_iter: int,
    burn_in: int,
    seed: int,
) -> tuple[pd.DataFrame, pd.DataFrame, dict[str, Any]]:
    returns_all = _load_returns(run_dir)
    contract, realized, forwards, fixing_times, discount, _ = _load_contract_state(
        run_dir, contract_id
    )
    output_dir.mkdir(parents=True, exist_ok=True)
    checkpoint_dir = output_dir / "checkpoints"
    checkpoint_dir.mkdir(parents=True, exist_ok=True)

    effective_windows = sorted(set(min(int(n), len(returns_all)) for n in windows) | {len(returns_all)})
    posterior_objects: list[tuple[int, PriorProfile, np.ndarray, dict[str, float]]] = []
    for n_obs in effective_windows:
        returns = returns_all[-n_obs:]
        for prior_index, prior in enumerate(PRIORS):
            checkpoint = checkpoint_dir / f"n{n_obs}_{prior.name}.npz"
            if checkpoint.exists():
                with np.load(checkpoint, allow_pickle=False) as data:
                    draws = data["sigma"].astype(float)
                    meta = json.loads(str(data["meta_json"].item()))
            else:
                draws, meta = _run_chains(
                    returns,
                    prior=prior,
                    chains=chains,
                    n_iter=n_iter,
                    burn_in=burn_in,
                    seed=seed + 1_000_003 * n_obs + 10_007 * prior_index,
                )
                np.savez_compressed(
                    checkpoint,
                    sigma=draws,
                    meta_json=np.array(json.dumps(meta, sort_keys=True)),
                )
            posterior_objects.append((n_obs, prior, draws, meta))

    lower = min(float(np.quantile(draws, 0.0005)) for _, _, draws, _ in posterior_objects)
    upper = max(float(np.quantile(draws, 0.9995)) for _, _, draws, _ in posterior_objects)
    lower = max(1e-5, 0.9 * lower)
    upper = 1.1 * upper
    sigma_grid = np.linspace(lower, upper, 501)
    curran_grid = np.array(
        [
            curran_arithmetic_futures_option(
                realized_fixings=realized,
                forward_fixings=forwards,
                fixing_times=fixing_times,
                strike=float(contract["strike"]),
                sigma=float(sigma),
                discount_factor=discount,
                option_type=str(contract["option_type"]),
            )
            for sigma in sigma_grid
        ],
        dtype=float,
    )
    pd.DataFrame({"sigma": sigma_grid, "curran_price": curran_grid}).to_csv(
        output_dir / "curran_pricing_map.csv", index=False
    )

    rows: list[dict[str, Any]] = []
    for n_obs, prior, draws, meta in posterior_objects:
        posterior_prices = np.interp(draws, sigma_grid, curran_grid)
        sigma_mean = float(np.mean(draws))
        pi_price = float(np.mean(posterior_prices))
        pm_price = float(np.interp(sigma_mean, sigma_grid, curran_grid))
        q025, q50, q975 = np.quantile(draws, [0.025, 0.5, 0.975])
        rows.append(
            {
                "n_obs": int(n_obs),
                "history_years": float(n_obs / 252.0),
                "prior": prior.name,
                "prior_alpha": prior.alpha,
                "prior_beta": prior.beta,
                "prior_mean_sigma": prior.mean,
                "prior_sd_sigma": prior.sd,
                "sigma_mle": float(meta["sigma_mle"]),
                "sigma_posterior_mean": sigma_mean,
                "sigma_posterior_sd": float(np.std(draws, ddof=1)),
                "sigma_q025": float(q025),
                "sigma_q50": float(q50),
                "sigma_q975": float(q975),
                "sigma_rhat": float(meta["sigma_rhat"]),
                "mean_acceptance_rate": float(meta["mean_acceptance_rate"]),
                "curran_posterior_integrated_price": pi_price,
                "curran_posterior_mean_plugin_price": pm_price,
                "curran_pi_minus_pm": pi_price - pm_price,
                "abs_curran_pi_minus_pm": abs(pi_price - pm_price),
            }
        )
    results = pd.DataFrame(rows).sort_values(["n_obs", "prior"]).reset_index(drop=True)

    baseline = results[results["prior"] == "baseline"][[
        "n_obs",
        "sigma_posterior_mean",
        "sigma_posterior_sd",
        "curran_posterior_integrated_price",
        "curran_pi_minus_pm",
    ]].rename(
        columns={
            "sigma_posterior_mean": "baseline_sigma_mean",
            "sigma_posterior_sd": "baseline_sigma_sd",
            "curran_posterior_integrated_price": "baseline_curran_pi",
            "curran_pi_minus_pm": "baseline_curran_gap",
        }
    )
    comparison = results.merge(baseline, on="n_obs", how="left", validate="many_to_one")
    comparison["sigma_mean_minus_baseline"] = (
        comparison["sigma_posterior_mean"] - comparison["baseline_sigma_mean"]
    )
    comparison["curran_pi_minus_baseline"] = (
        comparison["curran_posterior_integrated_price"] - comparison["baseline_curran_pi"]
    )
    comparison["gap_minus_baseline"] = (
        comparison["curran_pi_minus_pm"] - comparison["baseline_curran_gap"]
    )

    report = {
        "source_run": str(run_dir),
        "contract_id": str(contract["contract_id"]),
        "option_type": str(contract["option_type"]),
        "strike": float(contract["strike"]),
        "available_returns": int(len(returns_all)),
        "windows": effective_windows,
        "priors": [
            {
                "name": prior.name,
                "alpha": prior.alpha,
                "beta": prior.beta,
                "mean_sigma": prior.mean,
                "sd_sigma": prior.sd,
            }
            for prior in PRIORS
        ],
        "pricing_engine": "Curran (1994) geometric-conditioning approximation under the baseline one-factor futures Q model",
        "max_sigma_rhat": float(results["sigma_rhat"].max()),
        "max_abs_pi_minus_pm": float(results["abs_curran_pi_minus_pm"].max()),
        "max_abs_pi_change_vs_baseline_same_window": float(
            comparison["curran_pi_minus_baseline"].abs().max()
        ),
        "interpretation": (
            "This isolates sensitivity to estimation-window length and inverse-gamma "
            "hyperparameters. It does not replace the Monte Carlo market-pricing baseline "
            "or constitute robustness to every possible prior family."
        ),
    }
    return results, comparison, report


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-dir", type=Path, default=DEFAULT_RUN)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--contract-id", default=None)
    parser.add_argument("--windows", default="63,126,252,504")
    parser.add_argument("--preset", choices=("quick", "research", "extreme"), default="research")
    parser.add_argument("--seed", type=int, default=20260917)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    windows = tuple(int(x.strip()) for x in args.windows.split(",") if x.strip())
    if not windows or any(n < 20 for n in windows):
        raise ValueError("windows must contain integers >= 20")
    chains, n_iter, burn_in = _preset(args.preset)
    results, comparison, report = run(
        args.run_dir,
        args.output_dir,
        contract_id=args.contract_id,
        windows=windows,
        chains=chains,
        n_iter=n_iter,
        burn_in=burn_in,
        seed=args.seed,
    )
    results.to_csv(args.output_dir / "prior_window_results.csv", index=False)
    comparison.to_csv(args.output_dir / "prior_window_vs_baseline.csv", index=False)
    with (args.output_dir / "prior_window_report.json").open("w", encoding="utf-8") as fh:
        json.dump(report, fh, indent=2, sort_keys=True)
        fh.write("\n")
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
