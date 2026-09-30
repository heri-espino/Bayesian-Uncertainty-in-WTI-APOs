# Publication experiment sequence

This document is the execution order for the additional evidence needed before the JFM manuscript is rewritten. Experiment generation remains separate from manuscript claims: numbers should enter `paper/manuscript/` only after the corresponding versioned outputs have been inspected.

## Scientific targets

The extension tests six questions distinct from absolute model fit:

1. **Mechanism:** does the posterior-integrated versus posterior-mean gap follow \(\tfrac12 C''(\bar\sigma)\operatorname{Var}(\sigma\mid D)\)?
2. **Path dependence:** does that gap contract as the APO becomes progressively fixed during its averaging month?
3. **Numerics:** are sub-cent PI-PM differences resolved relative to Monte Carlo simulation noise?
4. **Statistical robustness:** does the conclusion survive shorter estimation windows and materially different inverse-gamma hyperparameters?
5. **Independent pricing benchmark:** how close is the canonical Monte Carlo engine to a Curran (1994) geometric-conditioning approximation under the same one-factor futures dynamics?
6. **Physical versus risk-neutral volatility:** what APO-implied \(\sigma_Q\) is encoded in observed settlements, how does it differ from the historical posterior for \(\sigma_P\), and does an APO-calibrated \(\sigma_Q\) improve pricing on contracts excluded from calibration?

The sixth experiment does **not** require new data. The committed APO settlements and CL futures fixing curves already identify an APO-implied volatility under the paper's pricing model. Vanilla CL options would be useful later only as an *independent external* Q-volatility validation source.

## 0. Validate the branch

From the repository root in the `asian-options` environment:

```bash
python -m scripts.check_repo_structure
python paper/build.py --check
python -m pytest -q
python -m sphinx -W --keep-going -b html docs docs/_build/html
```

## 1. Taylor mechanism from the completed extreme synthetic run

Reuse the existing extreme checkpoints:

```bash
python -m experiments.taylor_mechanism \
  --run-dir results/large_scale_synthetic/f497062f0c571126
```

If those local checkpoints were deleted, the committed summary is insufficient to reconstruct posterior variance. Only then resume the exact extreme configuration:

```bash
python -m experiments.large_scale_synthetic --preset extreme --backend cupy
```

Primary diagnostics are actual-versus-Taylor gap correlation, slope through the origin, MAE, and RMSE.

## 2. September 2026 partial-fixing panel

Audit supported in-month dates:

```bash
python -m experiments.wti_apo_date_panel \
  --apo-expiry 2026-09 \
  --start-date 2026-09-01 \
  --end-date 2026-09-17 \
  --list-dates
```

Run the production panel over every eligible date:

```bash
python -m experiments.wti_apo_date_panel \
  --apo-expiry 2026-09 \
  --start-date 2026-09-01 \
  --end-date 2026-09-17
```

The canonical driver fails closed when an exact realized first-nearby fixing is unavailable; do not forward-fill settlements.

Analyze the all-date panel:

```bash
python -m experiments.analyze_partial_fixing \
  --panel results/wti_apo_empirical/panel_202609/all_dates/panel_contract_pricing.csv
```

The within-contract slope of `|PI-PM|` on `fraction_fixed` is descriptive rather than causal because moneyness, time to payoff, posterior dispersion, and the futures curve co-move with date.

## 3. Monte Carlo convergence of the empirical PI-PM gap

Use the research preset:

```bash
python -m experiments.wti_mc_convergence --preset research
```

Inspect `sd_pi_minus_pm`, `mcse_mean_pi_minus_pm`, and convergence relative to the largest path budget before interpreting sub-cent differences.

## 4. Prior and historical-window sensitivity

Run the research configuration:

```bash
python -m experiments.wti_prior_window_sensitivity --preset research
```

Windows are 63, 126, 252, 504 and all available returns. Priors are the paper baseline `InvGamma(2, 0.1)`, a broad WTI-centered `InvGamma(3, 0.8)`, and a moderate WTI-centered `InvGamma(10, 3.6)`. Curran pricing is used here to isolate posterior/window sensitivity from fresh Monte Carlo noise.

## 5. Curran benchmark across completed empirical dates

Run both empirical expiries:

```bash
python -m experiments.wti_curran_benchmark --apo-expiry 2026-10
python -m experiments.wti_curran_benchmark --apo-expiry 2026-09
```

The benchmark uses the same posterior, realized first-nearby fixings, remaining futures curve, discount factor, and one-factor Q dynamics as the canonical Monte Carlo run. Do not describe the implementation as an exact reproduction of CME's complete settlement engine.

## 6. APO-implied risk-neutral volatility using existing data

No additional market download is required for this experiment. For each completed contract-date observation, solve

\[
C_{\text{Curran}}\!\left(\sigma_{Q,\mathrm{APO}};F_1,\ldots,F_m,K,r,\text{realized fixings}\right)
= C_{\text{settlement}}.
\]

Run all completed September and October empirical dates together:

```bash
python -m experiments.wti_apo_implied_volatility \
  --expiries 2026-09 2026-10
```

The experiment produces three distinct diagnostics:

- **Contract IVs:** an APO-implied volatility for every contract whose settlement lies inside the model-attainable price range. Contracts outside that range are retained with an explicit failure/status code rather than silently clipped.
- **Leave-one-contract-out calibration:** for every target contract, fit one scalar \(\sigma_Q\) to all other contracts on that date and price the excluded target. This prevents same-contract calibration/evaluation circularity.
- **Call/put transfer:** calibrate \(\sigma_Q\) using calls and evaluate puts, then calibrate using puts and evaluate calls. This is a stronger cross-sectional out-of-sample check when both option types are available.

Outputs are written to:

```text
results/analysis/wti_apo_implied_volatility/
├── apo_contract_implied_volatility.csv
├── apo_loo_predictions.csv
├── apo_cross_type_predictions.csv
├── apo_implied_volatility_by_date.csv
├── apo_implied_volatility_error_summary.csv
└── apo_implied_volatility_report.json
```

The key comparison is

\[
E[\sigma_P\mid D]
\quad\text{versus}\quad
\widehat{\sigma}_{Q,\mathrm{APO}},
\]

alongside out-of-sample settlement errors under the APO-calibrated Q volatility versus the paper's posterior-integrated historical-volatility baseline.

This experiment uses the APO cross-section itself, so \(\widehat{\sigma}_{Q,\mathrm{APO}}\) is not an independent external volatility source. Vanilla CL options remain a useful future extension if an independent Q-volatility surface is desired, but they are not required for the present robustness analysis.

## 7. One-command production run

After the experiment code is merged, the currently feasible production evidence can be run with:

```bash
python -m scripts.run_publication_experiments
```

The runner validates the repository, reuses completed final outputs when safe, verifies that the September panel is production-budget before reusing it, runs the research MC/prior-window experiments, benchmarks Curran, and finishes with the full APO-implied volatility analysis. Use `--force` only when a deliberate rerun is desired.

## 8. Only after experiments are frozen

Once the outputs above have been inspected and versioned:

1. synchronize abstract/introduction/results numerical values;
2. replace preliminary synthetic evidence with the completed extreme-run evidence;
3. add the Taylor mechanism result and figure;
4. add the September partial-fixing result;
5. add Curran and numerical-convergence robustness;
6. add the \(\sigma_P\) versus APO-implied \(\sigma_Q\) comparison and its out-of-sample pricing results;
7. replace future-tense robustness promises with completed analyses or explicit limitations;
8. consider renaming `Full Bayes` to `posterior-integrated` pricing throughout.

The manuscript should continue to distinguish the size of the PI-PM gap from absolute model-to-settlement error.


## 9. Referee-requested robustness checks

The current referee pass raises four distinct identification and implementation questions that can be answered without rerunning the heavy synthetic or Monte Carlo suites:

1. does a recent historical-volatility benchmark materially narrow the option-informed advantage on the exact 2,381 strict-forward holdouts?
2. does the PI--PM near-equivalence depend on using the posterior mean rather than the variance-matching scalar `sigma_RMS = sqrt(E[sigma^2 | D])`?
3. is the external LO result sensitive to the fixing-count RMS transfer rule?
4. are the 160-step American CRR inversion and the fitted prior-date LO surfaces numerically and shape-wise well behaved?

Run all checks with:

```bash
python -m scripts.run_reviewer_robustness
```

This runner is intentionally lightweight. It reuses committed target-date empirical runs, posterior summaries, and the existing LO IV panel. It does **not** rerun MCMC, APO smile fitting, the massive mechanism map, or the high-precision Monte Carlo experiments.

Outputs:

```text
results/analysis/wti_recent_historical_benchmarks/
├── recent_historical_predictions.csv
└── recent_historical_error_summary.csv

results/analysis/wti_rms_plugin_comparison/
├── rms_plugin_predictions.csv
└── rms_plugin_error_summary.csv

results/analysis/wti_prior_contract_iv_carry/
├── prior_contract_iv_carry_predictions.csv
└── prior_contract_iv_carry_summary.csv

results/analysis/wti_external_vanilla_q_validation_moment_matched/
├── external_vanilla_q_predictions.csv
├── external_vanilla_q_error_summary.csv
├── external_q_comparison.csv
├── external_q_matched_comparison.csv
├── external_q_surface_common_support.csv
├── external_vanilla_q_state.csv
└── external_vanilla_q_report.json

results/analysis/wti_databento_external_q/tree_convergence/
├── tree_convergence_detail.csv
└── tree_convergence_summary.csv

results/analysis/wti_databento_external_q/surface_shape_audit/
├── surface_shape_detail.csv
└── surface_shape_summary.csv
```

The recent-history choices are fixed in advance: 63, 126, and 252 most-recent usable returns plus an EWMA with a 63-business-day half-life. Do not tune those windows after inspecting pricing errors. The LO transfer sensitivity keeps the scalar near-ATM reduction at its baseline fixing-weighted RMS rule but replaces the fitted-surface reduction with a variance moment match of the unresolved arithmetic-average component under the maintained one-common-factor representation.

After running the suite, inspect and version the summaries before adding numerical claims to the manuscript. In particular, do not state that the option-informed advantage survives recent-history benchmarks until the exact-holdout results have been checked.
