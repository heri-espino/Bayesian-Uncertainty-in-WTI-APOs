# Publication experiment sequence

This document is the execution order for the additional evidence needed before the JFM manuscript is rewritten.  It intentionally keeps experiment generation separate from manuscript claims: numbers should enter `paper/manuscript/` only after the corresponding versioned outputs have been inspected.

## Scientific targets

The extension tests five questions that are distinct from absolute model fit:

1. **Mechanism:** does the observed posterior-integrated versus posterior-mean gap follow
   \(\tfrac12 C''(\bar\sigma)\operatorname{Var}(\sigma\mid D)\)?
2. **Path dependence:** does that gap contract as the APO becomes progressively fixed during its averaging month?
3. **Numerics:** are sub-cent PI-PM differences resolved relative to Monte Carlo simulation noise?
4. **Statistical robustness:** does the conclusion survive shorter estimation windows and materially different inverse-gamma hyperparameters?
5. **Independent pricing benchmark:** how close is the canonical Monte Carlo engine to a Curran (1994) geometric-conditioning approximation under the same one-factor futures dynamics?

A sixth proposed check—using a market-implied/risk-neutral volatility input—requires vanilla CL option data or another independently defensible Q-volatility source.  Such a source is not currently committed to this repository, so that experiment is explicitly data-dependent rather than replaced by another historical-volatility proxy.

## 0. Validate the branch

From the repository root in the `asian-options` environment:

```bash
python -m scripts.check_repo_structure
python paper/build.py --check
python -m pytest -q
python -m sphinx -W --keep-going -b html docs docs/_build/html
```

Do not start publication-scale runs if these checks fail.

## 1. Taylor mechanism from the completed extreme synthetic run

The extreme run already contains 18,000 posterior fits and nine 2-million-path pricing grids.  Do **not** rerun it merely to produce the mechanism diagnostic.  Reuse its local checkpoints:

```bash
python -m experiments.taylor_mechanism \
  --run-dir results/large_scale_synthetic/f497062f0c571126
```

Outputs:

```text
results/analysis/taylor_mechanism/
├── taylor_mechanism_raw.csv
├── taylor_mechanism_summary.csv
└── taylor_mechanism_report.json
```

Primary diagnostics are the correlation between the actual and Taylor PI-PM gaps, the slope through the origin, and approximation MAE/RMSE.  A slope near one over the region where the second-order expansion is accurate would directly support the proposed mechanism.

If the local extreme-run checkpoints have been deleted, the summary CSV committed to GitHub is insufficient to reconstruct posterior variance.  In that case resume the exact extreme configuration rather than creating a new one:

```bash
python -m experiments.large_scale_synthetic --preset extreme --backend cupy
```

The experiment is checkpointed and resumes missing units.

## 2. September 2026 partial-fixing panel

First inspect which in-month dates are supported by the committed APO and CL histories:

```bash
python -m experiments.wti_apo_date_panel \
  --apo-expiry 2026-09 \
  --start-date 2026-09-01 \
  --end-date 2026-09-17 \
  --list-dates
```

Run a quick smoke panel on the eligible date range, then the production panel:

```bash
python -m experiments.wti_apo_date_panel \
  --apo-expiry 2026-09 \
  --start-date 2026-09-01 \
  --end-date 2026-09-17 \
  --quick

python -m experiments.wti_apo_date_panel \
  --apo-expiry 2026-09 \
  --start-date 2026-09-01 \
  --end-date 2026-09-17
```

The canonical driver fails closed when an exact realized first-nearby fixing is unavailable; do not forward-fill missing settlements.

Analyze the resulting all-date panel:

```bash
python -m experiments.analyze_partial_fixing \
  --panel results/wti_apo_empirical/panel_202609/all_dates/panel_contract_pricing.csv
```

The main descriptive quantities are PI-PM gap by `fraction_fixed` and the within-contract slope after demeaning contract-specific levels.  The slope is not interpreted causally because moneyness, time to payoff, posterior dispersion, and the futures curve co-move with date.

## 3. Monte Carlo convergence of the empirical PI-PM gap

Use a completed production single-date run.  The default chooses the retained contract with the largest absolute baseline PI-PM gap, making the check conservative:

```bash
python -m experiments.wti_mc_convergence --preset quick
python -m experiments.wti_mc_convergence --preset research
```

The research preset evaluates 10k, 25k, 50k, 100k, 250k and 500k paths over independent pricing seeds while holding the posterior and contract state fixed.  Inspect `sd_pi_minus_pm`, `mcse_mean_pi_minus_pm`, and convergence relative to the largest path budget before describing a sub-cent gap as economically resolved.

## 4. Prior and historical-window sensitivity

The sampler's defaults are unchanged.  This experiment varies only the existing inverse-gamma hyperparameters and the length of the physical-measure return sample:

```bash
python -m experiments.wti_prior_window_sensitivity --preset quick
python -m experiments.wti_prior_window_sensitivity --preset research
```

Default windows are 63, 126, 252, 504 and all available returns.  Prior profiles are:

- `baseline`: InvGamma(2, 0.1), exactly the paper baseline;
- `wti_centered_broad`: InvGamma(3, 0.8), mean 0.40 and sd 0.40;
- `wti_centered_moderate`: InvGamma(10, 3.6), mean 0.40 and sd about 0.1414.

Each computational configuration receives its own fingerprinted output directory and checkpoints.  The pricing map for this sensitivity exercise uses Curran rather than fresh Monte Carlo so that changes in the reported gap come from the posterior/window choice rather than independent pricing noise.

## 5. Curran benchmark across completed empirical dates

For October 2026:

```bash
python -m experiments.wti_curran_benchmark --apo-expiry 2026-10
```

After the September production panel has produced its single-date runs:

```bash
python -m experiments.wti_curran_benchmark --apo-expiry 2026-09
```

The benchmark uses the same posterior draws, realized first-nearby fixings, remaining futures curve, discount factor, and one-factor Q dynamics as the canonical Monte Carlo run.  It reports Curran PI and PM prices alongside the stored Monte Carlo PI and PM prices and the Barchart settlement.

Do not describe this implementation as the exact CME settlement engine.  It is the Curran (1994) geometric-conditioning approximation implemented under this paper's state/dynamics assumptions.

## 6. Risk-neutral/implied-volatility robustness — data required

This experiment should be added only after obtaining a defensible Q-volatility source, preferably a cross-section of liquid vanilla CL options with contract/date metadata sufficient to estimate or calibrate an implied volatility surface.  Required provenance includes the option quote/settlement field, futures underlying, strike, option type, expiration, timestamp/date, and liquidity diagnostics.

The intended comparison is then:

\[
\sigma_{P,\mathrm{historical}}
\quad\text{versus}\quad
\sigma_{Q,\mathrm{implied}},
\]

with PI and PM pricing recomputed under otherwise identical APO mechanics.  Historical `CL=F` must not be relabeled as an implied or risk-neutral volatility source.

## 7. Only after experiments are frozen

Once the outputs above have been inspected and versioned:

1. synchronize abstract/introduction/results numerical values;
2. replace the preliminary synthetic table with the completed extreme-run evidence;
3. add the Taylor mechanism result and figure;
4. add the September partial-fixing result;
5. add Curran and numerical-convergence robustness;
6. replace future-tense robustness promises with completed analyses or explicit limitations;
7. consider renaming `Full Bayes` to `posterior-integrated` pricing throughout.

The manuscript should continue to distinguish the size of the PI-PM gap from absolute model-to-settlement error.
