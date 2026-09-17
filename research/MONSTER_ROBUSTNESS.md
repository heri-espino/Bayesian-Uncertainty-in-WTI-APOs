# Monster robustness phase

This phase is deliberately separate from the ordinary publication runner. It uses the full university workstation budget to attack model, numerical, calibration, and validation criticisms that remain after the baseline empirical study.

## Scientific questions

1. **Where does posterior integration matter?** Map the exact quadrature difference
   \(E[C(\sigma)\mid D]-C(E[\sigma\mid D])\) over sample size, true volatility, moneyness, time horizon, and partial fixing.
2. **Is the tiny PI-PM effect numerically resolved?** Reprice deliberately difficult empirical contracts with both multi-million-path pseudo-random GPU Monte Carlo and an independent randomized Sobol QMC engine.
3. **Does the empirical conclusion survive heavy-tailed returns under P?** Replace Gaussian innovations with standardized Student-t innovations while leaving Q pricing unchanged.
4. **Does APO-implied Q volatility work without same-day option information?** Fit IV smiles only to earlier dates and price the next completed date.
5. **Is the Gaussian posterior implementation calibrated?** Run large simulation-based calibration using exact-in-mu sigma quadrature.
6. **Are pricing improvements robust to dependence and liquidity?** Cluster-bootstrap valuation dates and stratify by volume/open interest.

## One-command run

From the repository root in the `asian-options` environment on the RTX workstation:

```powershell
python -m scripts.run_monster_robustness_suite --backend cupy
```

The runner executes tests first, then the stages below. The longest Monte Carlo, QMC, mechanism-map, and Student-t stages checkpoint reusable work. Use `--force` only for a deliberate complete rerun.

A single stage can be omitted with repeated `--skip`, for example:

```powershell
python -m scripts.run_monster_robustness_suite --backend cupy `
  --skip student-t `
  --skip high-precision
```

## 1. Massive mechanism map

```powershell
python -m experiments.massive_mechanism_map --preset monster --backend cupy
```

The monster preset uses 175,000 synthetic historical datasets and 4,097 sigma quadrature nodes. The Gaussian prior on `mu` is integrated analytically, so this experiment is independent of Random-Walk Metropolis numerical error while retaining the paper's exact Gaussian GBM posterior model.

The output reports exact quadrature PI-PM gaps and the second-order approximation

\[
\frac12 C''(E[\sigma\mid D])\operatorname{Var}(\sigma\mid D)
\]

for each WTI-like contract state. The top 100 adverse states are retained explicitly. Calls are sufficient for the phase map: under deterministic discounting, arithmetic-average put-call parity subtracts a sigma-independent term, so the PI-PM gap and volatility curvature are the same for the corresponding put.

Primary outputs:

```text
results/analysis/massive_mechanism_map/<fingerprint>/
├── mechanism_map_summary.csv
├── posterior_cell_summary.csv
├── scenario_grid.csv
├── top_100_adverse_scenarios.csv
└── mechanism_map_report.json
```

Local `checkpoints/` and `*.npz` price-curve caches are intentionally ignored by Git.

## 2. High-precision pseudo-random empirical pricing

```powershell
python -m experiments.wti_high_precision_pricing --preset monster --backend cupy
```

Targets are selected mechanically from the union of contracts with the largest baseline PI-PM gaps, largest absolute settlement errors, and largest errors among positive-volume observations. The monster preset uses 121 sigma nodes, 5,000,000 paths per sigma per randomization, and four independent randomizations.

The Monte Carlo control variate is the discounted arithmetic average minus its known Q expectation. Antithetic paths and common random numbers are used across sigma nodes within each randomization. The standard deviation of the independently randomized PI-PM gaps provides a direct Monte Carlo uncertainty estimate for the quantity of interest.

Each completed `(target, randomization, sigma)` cell is atomically checkpointed. The monster GPU chunk is one million paths, chosen to use the RTX memory efficiently while remaining well below the workstation's VRAM capacity.

## 3. Randomized Sobol QMC numerical benchmark

```powershell
python -m experiments.wti_randomized_qmc_benchmark --preset monster --backend cupy
```

This deliberately uses a different numerical estimator from the pseudo-random benchmark. The monster preset audits up to eight adverse contracts using 121 sigma nodes, eight independently scrambled Sobol sequences, and \(2^{21}=2,097,152\) low-discrepancy Brownian paths per scramble.

No fitted control variate is used in the QMC engine. Cross-scramble dispersion therefore supplies a randomized-QMC uncertainty estimate that is independent of the pseudo-random antithetic/control-variate construction. Agreement of PI, PM, and PI-PM across Curran, pseudo-random MC, and randomized Sobol QMC is the key numerical robustness check.

Each completed `(target, scramble, sigma)` price is checkpointed.

## 4. Student-t robustness under P

```powershell
python -m experiments.wti_student_t_robustness --preset monster
```

Only the historical return innovation distribution changes. The model is

\[
r_t=(\mu-\sigma^2/2)\Delta t+\sigma\sqrt{\Delta t}\,\varepsilon_t,
\qquad
\operatorname{Var}(\varepsilon_t)=1,
\]

with standardized Student-t innovations and inferred degrees of freedom. The baseline priors on `mu` and `sigma`, the Q futures dynamics, realized fixings, futures strip, and Curran price map remain unchanged.

The monster preset uses eight chains of 100,000 iterations per unique valuation date. Posterior draws are checkpointed by valuation date so an interrupted run does not discard completed MCMC work.

## 5. Strict forward-in-time Q validation

```powershell
python -m experiments.wti_forward_q_validation
```

For every target date, the fitted IV smile uses only observations with valuation dates strictly earlier than the target. Two schemes are reported:

- `previous_day_smile`: most recent earlier completed date only;
- `expanding_smile`: all earlier dates with a five-calendar-day exponential half-life.

The observed same-day implied volatility is retained only as an ex-post diagnostic and never enters the fit or target price.

## 6. Simulation-based calibration

```powershell
python -m experiments.simulation_based_calibration --preset monster --backend cupy
```

The monster preset draws 50,000 prior-predictive datasets at each of `n = 21, 63, 252, 1260` and evaluates a 4,097-node sigma posterior grid. It reports posterior CDF rank uniformity and 50%, 80%, and 95% credible-interval coverage.

The raw 200,000-row table is local-only (`*_raw.csv` is ignored by Git); summary and rank-histogram tables are versioned.

## 7. Liquidity/date cluster bootstrap

```powershell
python -m experiments.wti_liquidity_bootstrap --preset monster
```

The monster preset performs 100,000 valuation-date cluster resamples per eligible comparison. It reports changes in MAE/RMSE relative to the historical-volatility PI baseline, percentile 95% intervals, and bootstrap probabilities of improvement for:

- all observations;
- positive-volume observations;
- open interest at least 1, 10, 100, and 500.

Resampling individual option contracts is intentionally avoided because same-date contracts share the same futures curve, posterior, and market shock.

## Version-control policy

Commit the small final CSV/JSON summaries, figures, and reports. Do **not** commit:

- `results/**/checkpoints/`;
- `results/**/*.npz`;
- `results/**/*_raw.csv`;
- temporary GPU arrays or process logs.

After the suite completes, inspect all outputs before moving numerical claims into `paper/manuscript/`.