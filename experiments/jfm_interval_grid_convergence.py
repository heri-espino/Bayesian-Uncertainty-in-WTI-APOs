"""Reproduce grid convergence for every history in JFM's bounded study.

No Monte Carlo or new historical samples: replay the frozen seed/sufficient
statistics and reuse the independent numerical payoff reference. Strikes and
hypothetical correlation references share each return history.
Run manually from repository root:
    python -m experiments.jfm_interval_grid_convergence
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import numpy as np
import pandas as pd

from experiments import jfm_confirmatory as c

NODES = (513, 1025, 2049, 4097)
RHO = (1.0, 0.75, 0.5)


def replay_sufficient_statistics():
    rng = np.random.default_rng(c.SEED)
    for true in c.VOL:
        for n in c.SIZES:
            z = rng.normal(size=c.REPS)
            chi = rng.chisquare(n - 1, size=c.REPS)
            drift = (.08 - .5 * true**2) / 252
            variance = true**2 / 252
            means = drift + np.sqrt(variance / n) * z
            for j in range(c.REPS):
                yield true, n, j, float(n * means[j]), float(variance * chi[j] + n * means[j]**2)


def calculate(out: Path):
    source = pd.read_csv(out / "reference_prices.csv")
    oracle = {(float(x.sigma_true), float(x.strike), float(x.rho)):
              (float(x.qmc_reference_price), float(x.ci95_halfwidth))
              for x in source.itertuples()}
    prepared = {}
    for nodes in NODES:
        grid = np.linspace(.02, 1.5, nodes)
        prepared[nodes] = (grid, {strike: np.array([c.curran(s, strike) for s in grid])
                                  for strike in c.STRIKES})
    rows = []
    for true, n, j, sumr, ss in replay_sufficient_statistics():
        for nodes, (grid, prices) in prepared.items():
            w = c.posterior_weights(grid, n, sumr, ss)
            mean_sigma = float(w @ grid)
            for strike in c.STRIKES:
                curve = prices[strike]
                pi = float(w @ curve)
                pm = float(np.interp(mean_sigma, grid, curve))
                lo = c.qtile(grid, w, curve, .025)
                hi = c.qtile(grid, w, curve, .975)
                for rho in RHO:
                    ref, half = oracle[true, strike, rho]
                    definitely_inside = lo <= ref - half and ref + half <= hi
                    definitely_outside = ref + half < lo or ref - half > hi
                    rows.append(dict(sigma_true=true, n_obs=n, replication=j,
                                     strike=strike, rho=rho, grid_nodes=nodes,
                                     price_pi=pi, price_pm=pm,
                                     interval_lo=lo, interval_hi=hi,
                                     qmc_reference=ref, qmc_halfwidth=half,
                                     covered=int(lo <= ref <= hi),
                                     clearly_covered=int(definitely_inside),
                                     clearly_not_covered=int(definitely_outside),
                                     oracle_boundary_ambiguous=int(not
                                        (definitely_inside or definitely_outside))))
    data = pd.DataFrame(rows)
    archived = pd.read_csv(out / "confirmatory_rows.csv")
    original = data.loc[data.grid_nodes.eq(513)].merge(
        archived, on=["sigma_true", "n_obs", "replication", "strike", "rho"],
        how="outer", indicator=True, suffixes=("", "_original"))
    assert len(original) == 1440 and (original._merge == "both").all()
    for now, previous in (("price_pi", "price_pi_original"),
                          ("price_pm", "price_pm_original"),
                          ("interval_lo", "posterior_interval_low"),
                          ("interval_hi", "posterior_interval_high")):
        diff = np.max(abs(original[now] - original[previous]))
        assert diff < 2e-9, (now, diff)

    widths = data["interval_hi"] - data["interval_lo"]
    data["interval_width"] = widths
    summary = data.groupby(["grid_nodes", "rho"], sort=True).agg(
        covered=("covered", "sum"), state_rows=("covered", "size"),
        coverage=("covered", "mean"),
        certainly_covered=("clearly_covered", "sum"),
        boundary_ambiguous=("oracle_boundary_ambiguous", "sum"),
        mean_interval_width=("interval_width", "mean"))
    full = data.loc[data.grid_nodes.eq(max(NODES))].set_index(
        ["sigma_true", "n_obs", "replication", "strike", "rho"])
    differences = []
    for nodes in NODES[:-1]:
        subset = data.loc[data.grid_nodes.eq(nodes)].set_index(full.index.names)
        for col in ("price_pi", "price_pm", "interval_lo", "interval_hi"):
            delta = (subset[col] - full[col]).abs()
            differences.append(dict(grid_nodes=nodes, reference_grid=max(NODES),
                metric=col, max_abs_difference=float(delta.max()),
                p99_abs_difference=float(delta.quantile(.99))))
    return data.drop(columns=["interval_width"]), summary.reset_index(), pd.DataFrame(differences)


def main():
    out = Path("results/analysis/jfm_confirmatory")
    data, summary, diffs = calculate(out)
    outputs = {}
    for name, frame in (
        ("grid_coverage_rows.csv", data),
        ("grid_coverage_summary.csv", summary),
        ("grid_coverage_differences.csv", diffs)
    ):
        path = out / name
        frame.to_csv(path, index=False, float_format="%.14g")
        outputs[name] = hashlib.sha256(path.read_bytes()).hexdigest()
    manifest = dict(status="BOUNDED_NUMERIC_GRID_CHECK_NOT_MARKET_VALIDATION",
                    original_seed=c.SEED, independent_histories=160,
                    option_state_rows_per_rho=480, grid_nodes=NODES,
                    shared_history="3 strikes and 3 correlation references",
                    reused_qmc_reference="reference_prices.csv",
                    boundary_rule="95% QMC halfwidth compared with posterior endpoints",
                    sha256=outputs)
    (out / "grid_coverage_manifest.json").write_text(
        json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(summary.to_string(index=False))
    print(diffs.to_string(index=False))


if __name__ == "__main__":
    main()
