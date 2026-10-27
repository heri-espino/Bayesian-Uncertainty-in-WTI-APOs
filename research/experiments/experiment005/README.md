# Experiment 005: AAO predictive uncertainty calibration

**Created:** 2026-10-27. **Status:** code authored and synthetic checks performed; real Databento-backed evaluation **not executed in this remote environment** because the 21 MB Experiment 004 private contract file is represented by a Git LFS pointer in connected GitHub. The user runs the experiment locally. Do not report a real-data performance result before that local run.

## Research question

Experiment 004 compared unchanged previous-date AAO market-implied volatility (holdout actual-mark MAE 0.208924 USD/bbl) with Bayesian-IV PM (0.209752) and Bayesian-IV PI (0.209830), finding no reliable incremental improvement in price MAE. Experiment 005 instead asks whether **Bayesian residual uncertainty modeling improves the calibration and sharpness of conditional AAO settlement-mark price intervals**, relative to an identically informed rolling empirical residual quantile baseline.

**Scope:** predictive intervals for observed option settlement marks *conditional on same-date disjoint-strike parity anchors*. This is **NOT** a posterior over the first-nearby CL Asian payoff, a structural AAO path simulation, or a direct validation of Experiment 004 volatility posterior draws. The Bayesian NIG model targets **past pricing residuals**. The 2025–26 evaluation window has already been inspected for Experiment 004 and is **not an untouched holdout**.

## Files

- Source runner: experiments/wti_aao_predictive_calibration.py.
- Synthetic checks: tests/test_aao_predictive_calibration.py.
- Fixed protocol and research context: this README.
- Input: private file data/databento/wti_aao_bulk/derived_private/experiment004/AAO_MARKET_IV_BAYES_CONTRACT_PRICING.csv.gz (real Git LFS payload required, 21 MB).
- New aggregate results: results/analysis/wti_aao_predictive_calibration/experiment005/ (only after local execution).

The runner does not import the raw DBN, SQLite, data-provider clients or the original AAO pricing simulator. It reads the EXISTING Experiment 004 price-prediction file, verifies original prediction-error identity and equal contract support, and evaluates three **frozen** point estimators on identical actual-flagged targets: lagged_IV, bayes_IV_PM and bayes_IV_PI.

## Prespecified methods

On each valuation date and for each (point method, option side, expiry-day bucket), use up to the last 63 **prior valuation dates** of residuals (observed settlement mark minus predicted price). Require at least 15 dates of prior history. Expiry-day buckets: 1–30, 31–60, 61–120, 121–240 and >240. Stratify reporting further by year and strike/forward moneyness.

All previous-day errors are known before the target valuation day in this retrospective setup. Critically, **all target-date intervals are issued before any target-date residual is appended to history**. History is checked for strictly earlier dates. Each historical date contributes total weight 1, split across its own contracts, reducing within-date pseudo-replication.

**Candidate: NIG Bayesian residual predictive.** Fixed prior on Gaussian residual mean and variance, normal-inverse-gamma with mu0=0 USD/bbl, kappa0=0.5, alpha0=2.5, beta0=0.125 (USD/bbl)^2. A fractional/power likelihood with date-balanced weights yields a Student-t residual predictive, whose central 90% and 95% quantiles are added to the frozen point forecast. Because correlated residuals remain, this is not a fully specified hierarchical posterior, and nominal Bayesian quantiles have no promised frequentist coverage.

**Benchmark: rolling empirical signed residual quantiles.** Estimate the same central 90% and 95% quantiles using the *same prior dates* and same date-balanced weights, without a posterior. This is a transparent benchmark, **not** exchangeability-valid split conformal inference or a guaranteed-coverage procedure.

## Evaluation

For each 90%/95% interval evaluate empirical coverage, mean interval width, and **interval score** (smaller better):

    IS_alpha(L,U;y) = U-L + (2/alpha)*(L-y)_+ + (2/alpha)*(y-U)_+ .

Scores and coverages are produced by development (2023–24) and retrospectively inspected holdout (2025–Sep26), by year, maturity and moneyness, plus daily actual-only scores. Compare Bayesian-NIG vs rolling-empirical on the SAME frozen point method, and Bayesian-IV PI vs unchanged lagged_IV with SAME Bayesian NIG residual calibration. Date-level paired score differences are evaluated with calendar-month-block bootstrap (1999 resamples); improvement means score(baseline) minus score(candidate), positive favors the candidate.

**Do not infer success from coverage alone:** extremely wide intervals can achieve high coverage. Jointly report proper interval score and interval width. Do not use contract rows as independent replicates. All numerical results and subgroups are exploratory and the 2025–26 marks have already been inspected; changing the model based on those outcomes does not yield fresh out-of-sample evidence.

## Local commands (PowerShell)

Synchronize your current results branch and run tests before the real dataset:

    git pull --ff-only origin results/aao-databento-pilot-2023h1-20261026
    python -m pytest tests/test_aao_predictive_calibration.py -q
    python -m experiments.wti_aao_predictive_calibration

The last command is a safe **dry-run** by default. Perform the real historical analysis manually:

    python -m experiments.wti_aao_predictive_calibration --execute --min-dates 15 --window-dates 63 --bootstrap 1999 --test-start 2025-01-01 --output-dir results/analysis/wti_aao_predictive_calibration/experiment005

No provider calls, purchases, SQL writes, heavy risk-neutral Asian Monte Carlo, automatic GitHub Actions or mutations of Experiment 003/004 files. Output directory must be initially absent or empty; the runner refuses to overwrite existing nonempty results.

Expected aggregate output files: experiment_manifest.json, summary_by_split.csv, summary_by_year.csv, summary_by_maturity.csv, summary_by_moneyness.csv, daily_actual_scores.csv, paired_month_block_intervals.csv. No new raw/provider price-level file is exported.

After a successful run:

    git add --sparse -- results/analysis/wti_aao_predictive_calibration/experiment005/
    git commit -m "Record Experiment005 AAO predictive interval calibration"
    git push origin results/aao-databento-pilot-2023h1-20261026

Preserve all findings, including failures, numerical values, negative results, caveats and further research instructions in this repository as the scientific handoff.

## Integrity and stopping rules

1. Stop on unequal method support, inconsistent error data or future-date calibration inputs. Preserve failure diagnostics.
2. Do not conflate posterior **residual-mark** intervals with structural Asian option payoff distributions or market risk-neutral probabilities.
3. These are retrospective conditional cross-sectional option mark experiments, using archive-end settlement revisions and same-date AAO parity anchors. Not a deployable fully ex-ante independent-price forecast.
4. Bayesian residual calibration might lose to rolling empirical intervals. Report any null finding without tuning the already-inspected comparison period.
5. Keep original paid Databento source data, existing private output and Experiment 003/004 results unchanged; user executes locally only.
