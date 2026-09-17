"""Benchmark completed WTI APO runs against a Curran conditioning approximation.

For every completed single-date run matching an APO expiry, this script reconstructs the
stored fixing state and posterior volatility draws, prices every retained contract with the
Curran (1994) geometric-conditioning approximation, and compares:

* Curran posterior-integrated (PI) pricing;
* Curran posterior-mean (PM) plug-in pricing;
* the canonical Monte Carlo PI and PM prices already stored by the empirical driver;
* the observed Barchart settlement retained as ``market_price`` in the source run.

The Curran implementation uses the same one-factor Q dynamics, first-nearby fixing map,
realized fixings, and discount factor as the Monte Carlo baseline.  It is an independent
numerical/industry benchmark; it is not labeled as an exact reproduction of CME's internal
settlement engine.

Examples
--------
    python -m experiments.wti_curran_benchmark --apo-expiry 2026-10
    python -m experiments.wti_curran_benchmark --apo-expiry 2026-09
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

from bayesian_asian_options.asian_futures_pricing import curran_arithmetic_futures_option


DEFAULT_RUNS_ROOT = Path("results/wti_apo_empirical")
DEFAULT_OUTPUT_ROOT = Path("results/analysis/curran_benchmark")


def _discover_runs(root: Path, expiry: str) -> list[Path]:
    suffix = f"_{expiry.replace('-', '')}"
    runs = sorted(
        path
        for path in root.iterdir()
        if path.is_dir()
        and path.name.endswith(suffix)
        and (path / "manifest.json").exists()
        and (path / "contract_pricing.csv").exists()
        and (path / "posterior_draws.npz").exists()
    )
    if not runs:
        raise FileNotFoundError(f"no completed {expiry} runs found below {root}")
    return runs


def _state(run_dir: Path, manifest: dict[str, Any]) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    valuation_date = pd.Timestamp(manifest["valuation_date"]).normalize()
    state = pd.read_csv(run_dir / "apo_fixing_state.csv")
    state["fixing_date"] = pd.to_datetime(state["fixing_date"]).dt.normalize()
    if "fixing_status" in state.columns:
        realized = state[state["fixing_status"] == "realized"].copy()
        remaining = state[state["fixing_status"] == "remaining"].copy()
    else:
        realized = state[state["fixing_date"] <= valuation_date].copy()
        remaining = state[state["fixing_date"] > valuation_date].copy()
    realized_values = realized["settlement"].to_numpy(dtype=float)
    forward_values = remaining["settlement"].to_numpy(dtype=float)
    times = (
        (remaining["fixing_date"] - valuation_date).dt.days.to_numpy(dtype=float) / 365.25
    )
    return realized_values, forward_values, times


def _error_summary(frame: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    methods = {
        "curran_pi": "curran_pi_price",
        "curran_pm": "curran_pm_price",
        "mc_pi": "full_bayes_price",
        "mc_pm": "postmean_plugin_price",
    }
    for sample_name, sample in {
        "all": frame,
        "positive_volume": frame[frame["positive_volume"]],
    }.items():
        if sample.empty:
            continue
        for method, column in methods.items():
            error = sample[column].to_numpy(dtype=float) - sample["market_settlement"].to_numpy(dtype=float)
            rows.append(
                {
                    "sample": sample_name,
                    "method": method,
                    "n": int(len(sample)),
                    "mean_error": float(np.mean(error)),
                    "mae": float(np.mean(np.abs(error))),
                    "rmse": float(np.sqrt(np.mean(error**2))),
                }
            )
    return pd.DataFrame(rows)


def _one_run(run_dir: Path, grid_points: int) -> pd.DataFrame:
    manifest = json.loads((run_dir / "manifest.json").read_text(encoding="utf-8"))
    valuation_date = str(manifest["valuation_date"])
    discount = float(manifest["discounting"]["discount_factor"])
    pricing = pd.read_csv(run_dir / "contract_pricing.csv")
    with np.load(run_dir / "posterior_draws.npz", allow_pickle=False) as data:
        sigma_draws = data["sigma"].astype(float)
    if sigma_draws.ndim != 1 or sigma_draws.size == 0:
        raise ValueError(f"invalid posterior draws in {run_dir}")
    sigma_mean = float(np.mean(sigma_draws))
    realized, forwards, times = _state(run_dir, manifest)

    lo = max(1e-6, 0.9 * float(np.quantile(sigma_draws, 0.0005)))
    hi = 1.1 * float(np.quantile(sigma_draws, 0.9995))
    sigma_grid = np.linspace(lo, hi, grid_points)

    rows: list[dict[str, Any]] = []
    for contract in pricing.itertuples(index=False):
        grid_prices = np.array(
            [
                curran_arithmetic_futures_option(
                    realized_fixings=realized,
                    forward_fixings=forwards,
                    fixing_times=times,
                    strike=float(contract.strike),
                    sigma=float(sigma),
                    discount_factor=discount,
                    option_type=str(contract.option_type),
                )
                for sigma in sigma_grid
            ],
            dtype=float,
        )
        posterior_prices = np.interp(sigma_draws, sigma_grid, grid_prices)
        curran_pi = float(np.mean(posterior_prices))
        curran_pm = float(np.interp(sigma_mean, sigma_grid, grid_prices))
        volume = float(contract.volume) if pd.notna(contract.volume) else np.nan
        market = float(contract.market_price)
        rows.append(
            {
                "valuation_date": valuation_date,
                "contract_id": str(contract.contract_id),
                "option_type": str(contract.option_type),
                "strike": float(contract.strike),
                "market_settlement": market,
                "volume": volume,
                "positive_volume": bool(np.isfinite(volume) and volume > 0),
                "fraction_fixed": float(getattr(contract, "fraction_fixed", len(realized) / (len(realized) + len(forwards)))),
                "sigma_posterior_mean": sigma_mean,
                "curran_pi_price": curran_pi,
                "curran_pm_price": curran_pm,
                "curran_pi_minus_pm": curran_pi - curran_pm,
                "full_bayes_price": float(contract.full_bayes_price),
                "postmean_plugin_price": float(contract.postmean_plugin_price),
                "mc_pi_minus_pm": float(contract.fb_minus_pm),
                "curran_pi_minus_mc_pi": curran_pi - float(contract.full_bayes_price),
                "curran_pm_minus_mc_pm": curran_pm - float(contract.postmean_plugin_price),
                "curran_pi_error": curran_pi - market,
                "curran_pm_error": curran_pm - market,
            }
        )
    return pd.DataFrame(rows)


def run(
    runs_root: Path,
    *,
    apo_expiry: str,
    grid_points: int,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, dict[str, Any]]:
    if grid_points < 41:
        raise ValueError("grid_points must be at least 41")
    runs = _discover_runs(runs_root, apo_expiry)
    frames = [_one_run(path, grid_points) for path in runs]
    contracts = pd.concat(frames, ignore_index=True)
    errors = _error_summary(contracts)

    date_rows: list[dict[str, Any]] = []
    for date, group in contracts.groupby("valuation_date", sort=True):
        diff_pi = group["curran_pi_minus_mc_pi"].to_numpy(dtype=float)
        diff_pm = group["curran_pm_minus_mc_pm"].to_numpy(dtype=float)
        date_rows.append(
            {
                "valuation_date": date,
                "n": int(len(group)),
                "positive_volume_n": int(group["positive_volume"].sum()),
                "fraction_fixed": float(group["fraction_fixed"].iloc[0]),
                "mean_abs_curran_pi_minus_mc_pi": float(np.mean(np.abs(diff_pi))),
                "max_abs_curran_pi_minus_mc_pi": float(np.max(np.abs(diff_pi))),
                "mean_abs_curran_pm_minus_mc_pm": float(np.mean(np.abs(diff_pm))),
                "mean_abs_curran_pi_minus_pm": float(np.mean(np.abs(group["curran_pi_minus_pm"]))),
                "mean_abs_mc_pi_minus_pm": float(np.mean(np.abs(group["mc_pi_minus_pm"]))),
            }
        )
    by_date = pd.DataFrame(date_rows)

    report = {
        "apo_expiry": apo_expiry,
        "source_runs_root": str(runs_root),
        "completed_dates": len(runs),
        "contract_date_rows": int(len(contracts)),
        "positive_volume_rows": int(contracts["positive_volume"].sum()),
        "curran_sigma_grid_points": grid_points,
        "mean_abs_curran_pi_minus_mc_pi": float(
            contracts["curran_pi_minus_mc_pi"].abs().mean()
        ),
        "max_abs_curran_pi_minus_mc_pi": float(
            contracts["curran_pi_minus_mc_pi"].abs().max()
        ),
        "mean_abs_curran_pm_minus_mc_pm": float(
            contracts["curran_pm_minus_mc_pm"].abs().mean()
        ),
        "mean_abs_curran_pi_minus_pm": float(
            contracts["curran_pi_minus_pm"].abs().mean()
        ),
        "mean_abs_mc_pi_minus_pm": float(
            contracts["mc_pi_minus_pm"].abs().mean()
        ),
        "benchmark_definition": (
            "Curran (1994) geometric-conditioning approximation under the paper's same "
            "one-factor lognormal futures dynamics and stored first-nearby fixing state"
        ),
        "market_field_interpretation": (
            "Barchart Latest is treated as the end-of-day settlement supplied in the source histories"
        ),
        "caution": (
            "This experiment does not assert that the implemented Curran approximation is an "
            "exact reproduction of CME's complete settlement implementation."
        ),
    }
    return contracts, by_date, errors, report


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--runs-root", type=Path, default=DEFAULT_RUNS_ROOT)
    parser.add_argument("--apo-expiry", default="2026-10")
    parser.add_argument("--output-root", type=Path, default=DEFAULT_OUTPUT_ROOT)
    parser.add_argument("--grid-points", type=int, default=401)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    contracts, by_date, errors, report = run(
        args.runs_root,
        apo_expiry=args.apo_expiry,
        grid_points=args.grid_points,
    )
    output_dir = args.output_root / args.apo_expiry.replace("-", "")
    output_dir.mkdir(parents=True, exist_ok=True)
    contracts.to_csv(output_dir / "curran_contract_benchmark.csv", index=False)
    by_date.to_csv(output_dir / "curran_by_date.csv", index=False)
    errors.to_csv(output_dir / "curran_error_summary.csv", index=False)
    with (output_dir / "curran_report.json").open("w", encoding="utf-8") as fh:
        json.dump(report, fh, indent=2, sort_keys=True)
        fh.write("\n")
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
