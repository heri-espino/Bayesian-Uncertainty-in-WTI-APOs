"""Audit posterior price-interval grid sensitivity without new Monte Carlo.

Recreates the original JFM independent-seed sufficient statistics, recomputes
Curran curves for 513/1025/2049/4097 sigma grids, and checks all 1440 state
rows and coverage decisions against the frozen 513-point study. Manual-only.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd

from experiments import jfm_confirmatory as model

GRIDS = (513, 1025, 2049, 4097)
RHO = (1.0, 0.75, 0.5)
INDEX = ["sigma_true", "n_obs", "replication", "strike", "rho"]


def archived_original(path: Path) -> pd.DataFrame:
    with zipfile.ZipFile(path) as z:
        names = [name for name in z.namelist() if name.endswith("/confirmatory_rows.csv") or name == "confirmatory_rows.csv"]
        if len(names) != 1:
            raise ValueError("Expected exactly one original confirmatory_rows.csv in archive")
        with z.open(names[0]) as file:
            return pd.read_csv(file)


def run(ref: Path, archive: Path, out: Path) -> dict:
    out.mkdir(parents=True, exist_ok=True)
    original = archived_original(archive).set_index(INDEX).sort_index()
    reference = pd.read_csv(ref)
    prices = {(float(row.sigma_true), float(row.strike), float(row.rho)):
              float(row.qmc_reference_price) for row in reference.itertuples()}
    grids = {size: np.linspace(.02, 1.5, size) for size in GRIDS}
    curves = {size: {strike: np.asarray(
        [model.curran(sigma, strike) for sigma in grid]
    ) for strike in model.STRIKES} for size, grid in grids.items()}
    rng = np.random.default_rng(model.SEED)
    records = []
    for sigma_true in model.VOL:
        for n_obs in model.SIZES:
            normals = rng.normal(size=model.REPS)
            chisq = rng.chisquare(n_obs - 1, size=model.REPS)
            mu = (.08 - .5 * sigma_true**2) / 252
            var = sigma_true**2 / 252
            sample_mean = mu + np.sqrt(var / n_obs) * normals
            sums = n_obs * sample_mean
            sumsq = var * chisq + n_obs * sample_mean**2
            for replication in range(model.REPS):
                for size, grid in grids.items():
                    weights = model.posterior_weights(grid, n_obs, sums[replication], sumsq[replication])
                    mean_sigma = float(weights @ grid)
                    for strike in model.STRIKES:
                        curve = curves[size][strike]
                        pi = float(weights @ curve)
                        pm = float(np.interp(mean_sigma, grid, curve))
                        lo = model.qtile(grid, weights, curve, .025)
                        hi = model.qtile(grid, weights, curve, .975)
                        for rho in RHO:
                            target = prices[(sigma_true, strike, rho)]
                            records.append(dict(sigma_true=sigma_true,
                                n_obs=n_obs, replication=replication,
                                strike=strike, rho=rho, grid=size,
                                price_pi=pi, price_pm=pm, lower=lo, upper=hi,
                                covered=int(lo <= target <= hi)))
    frame = pd.DataFrame(records).set_index(INDEX)
    baseline = frame.loc[frame.grid.eq(513)].sort_index()
    if len(baseline) != 1440 or len(original) != 1440:
        raise AssertionError("Unexpected historical sample size")
    for actual, frozen in (("price_pi", "price_pi"),
                            ("price_pm", "price_pm"),
                            ("lower", "posterior_interval_low"),
                            ("upper", "posterior_interval_high")):
        if float((baseline[actual] - original[frozen]).abs().max()) > 5e-10:
            raise AssertionError(f"Cannot reproduce archived 513-grid {actual}")
    summary = []
    finest = frame.loc[frame.grid.eq(4097)].sort_index()
    for size in GRIDS:
        current = frame.loc[frame.grid.eq(size)].sort_index()
        max_endpoint = max(float((current.lower - finest.lower).abs().max()),
                           float((current.upper - finest.upper).abs().max()))
        flips = int((current.covered != finest.covered).sum())
        for rho in RHO:
            subset = current.loc[current.index.get_level_values("rho") == rho]
            summary.append(dict(grid=size, rho=rho, states=len(subset),
                coverage=float(subset.covered.mean()),
                flips_vs4097=flips, max_endpoint_diff_vs4097=max_endpoint))
    result = pd.DataFrame(summary)
    result.to_csv(out / "summary.csv", index=False, float_format="%.14g")
    report = dict(status="GRID_STABILITY_CHECK_NOT_MARKET_CALIBRATION",
       seed=model.SEED, original_rows=len(original), grid_sizes=GRIDS,
       historical_replications=160, option_states_per_rho=480,
       total_scenario_rows_per_grid=1440,
       coverage_stable=all(row["flips_vs4097"] == 0 for row in summary),
       max_513_vs4097_endpoint_diff=max(
           row["max_endpoint_diff_vs4097"] for row in summary if row["grid"] == 513),
       limitations=[
          "Grid-stable binary classifications do not imply sub-cent interval endpoint accuracy",
          "Pilot-informed synthetic study, not independent market validation",
          "CME settlement model and proprietary market data are not verified by this calculation"
       ], original_archive_sha256=hashlib.sha256(archive.read_bytes()).hexdigest())
    (out / "manifest.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(result.to_string(index=False))
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--reference", type=Path, default=Path("results/analysis/jfm_confirmatory/reference_prices.csv"))
    parser.add_argument("--archive", type=Path, default=Path("results/analysis/jfm_confirmatory/jfm_confirmatory_execution_20261029.zip"))
    parser.add_argument("--output", type=Path, default=Path("results/analysis/jfm_grid_sensitivity"))
    args = parser.parse_args()
    run(args.reference, args.archive, args.output)


if __name__ == "__main__":
    main()
