# Experiment 004 — Bayesian AAO market-IV pricing: preregistration and handoff

Created: 2026-10-27. **Status: code and tests committed, purchased-market-data experiment NOT YET RUN.** All expensive runs are manual and local. No changes to the established Experiment 003 benchmark, figures or paid source data.

## Scientific motivation

Experiment 003, based on the reduced-form WTI AAO terminal-average lognormal approximation, found full-period actual-mark MAE 0.80404 USD/bbl for historical-volatility posterior integration (PI) and 0.21842 USD/bbl for unchanged previous-date AAO implied volatility (lagged_IV). Diagnoses on 1,689 eligible groups found mean target-date AAO IV 30.97%, historical-proxy Bayesian PM volatility 26.68%, and lagged market IV 30.88%. This motivates a FAIRER *market-information-matched* comparison, not a guarantee that Bayes will win.

Core research question: **Does Bayesian uncertainty integration improve AAO pricing after both methods have comparable strictly lagged market-implied volatility information?**

The study stays *conditional cross-sectional*, using disjoint current-date AAO call/put parity anchors to infer forward-average and effective discount for ALL methods. It does not observe actual first-nearby CL fixings or model structural Asian GBM. No current evaluation target prices or target implied-volatilities feed the volatility predictors.

## Files added

- bayesian_asian_options/src/bayesian_asian_options/aao_market_iv_bayes.py — NIG Bayesian posterior and Student-t predictive log-IV.
- experiments/wti_aao_bayesian_market_iv.py — separate, local-only eight-method runner and output validation.
- tests/test_aao_market_iv_bayes.py — synthetic tests, chronological leakage guards and no-provider SQLite integration fixture.
- research/experiments/experiment004/README.md — this preregistration and reproducibility handoff.
- .gitattributes — Git LFS pattern for private Experiment 004 compressed outputs.

Original six methods are preserved: PI, PM, rolling21, rolling63, ewma63, lagged_IV. The new methods are bayes_IV_PM and bayes_IV_PI. The original baseline predictions are recreated with the unchanged original implementation and exactly the same eligible non-anchor evaluation contracts for all eight methods.

## Mathematical design — frozen before the market experiment

For each AAO expiry separately, collect historical near-ATM market IV estimated from actual AAO settlements on dates *strictly earlier* than the evaluation date. Use the existing previous-date IV construction. On consecutive weekday observations, define x_j = log(sigma_j/sigma_(j-1)). Skip observations not a single business-weekday apart. Use up to 63 recent changes, require at least 8.

One-day x_j conditional on drift mu and variance v is Gaussian, with normal-inverse-gamma prior:

- v ~ InvGamma(alpha0=3, beta0=0.002).
- mu | v ~ N(0, v/kappa0), with kappa0=10.
- kappa_n = kappa0+n; mu_n = n * xbar / kappa_n.
- alpha_n = alpha0+n/2.
- beta_n = beta0 + sum((x_j-xbar)^2)/2 + kappa0*n*xbar^2/(2*kappa_n).

From most recent strictly prior market IV, extrapolate h weekdays. The log-IV posterior predictive is Student t with df=2*alpha_n, location log(previous IV)+h*mu_n and squared scale (beta_n/alpha_n)*(h+h^2/kappa_n). h uses weekdays, not an exchange holiday calendar. The model is a simplified local log-IV innovation law and may be misspecified for gaps, term structure, volatility smiles and shifting regimes.

Generate 256 deterministically seeded predictive draws. To make E(sigma) finite (untruncated exponentiated Student-t has no finite moment), explicitly clip sampled sigma to [0.005,3.0], recording clipped draws. New models are (i) bayes_IV_PM: price at the empirical sigma mean of these draws and (ii) bayes_IV_PI: mean option price over the very same sigma draws. Original lagged_IV remains the Black price at the latest prior IV, *not adjusted or recalibrated*. The latter is the primary benchmark.

The benchmark comparison is conditional on having enough lagged IV observations, so the new common cohort may be smaller than Experiment 003; NEVER compare unadjusted headline MAEs across different cohort supports. Save date/expiry eligibility attrition.

## Chronological holdout and scoring

**Development:** 2023-01-01 through 2024-12-31. **Primary holdout:** 2025-01-01 through 2026-09-30. No parameter tuning after viewing holdout data. Fixed source-start 2021-01-01, evaluate dates every 5 selected source dates, cap 80 contracts per expiry-date group, posterior 256 draws, bootstrap 1999 calendar-month resamples.

Primary metric: actual-flagged paired date-level MAE difference, MAE(lagged_IV) minus MAE(bayes_IV_PI), positive meaning new Bayesian integration is better. Secondary comparisons: bayes_IV_PI vs bayes_IV_PM, original PI/PM, RMSE/bias, and separate theoretical-flagged targets. Bootstrap resamples *calendar months* of daily paired actual-only errors; do not treat individual contract prices as independent observations. Segment MAE/RMSE/bias by valuation year, maturity buckets 1–30 / 31–60 / 61–120 / 121–240 / >240 calendar days, and moneyness relative to same-date parity-forward (<0.90, 0.90–0.97, 0.97–1.03, 1.03–1.10, >1.10).

## Commands to run on PC (PowerShell or Linux)

Run from repository root with the existing asian-options environment and complete local AAO files:

    python -m pytest tests/test_aao_market_iv_bayes.py tests/test_aao_databento_only.py -q
    python -m experiments.wti_aao_bayesian_market_iv --help
    python -m experiments.wti_aao_bayesian_market_iv

Without --execute the third command is a harmless dry-run.

### Smoke test: local and restricted

    python -m experiments.wti_aao_bayesian_market_iv --execute --source-start 2021-01-01 --eval-start 2023-01-01 --eval-end 2025-03-31 --test-start 2025-01-01 --date-stride 15 --max-contracts 30 --bootstrap 199 --posterior-draws 128 --output-dir results/analysis/wti_aao_market_iv_bayes/smoke --private-dir data/databento/wti_aao_bulk/derived_private/experiment004_smoke

Smoke is for functionality only; it must not be used to pick priors after looking at the primary holdout. In the event of zero eligibility, retain the eligibility_failure.json report and diagnose selection rather than relaxing conditions to manufacture a result.

### Full experiment: local and manually initiated

    python -m experiments.wti_aao_bayesian_market_iv --execute --source-start 2021-01-01 --eval-start 2023-01-01 --eval-end 2026-09-30 --test-start 2025-01-01 --date-stride 5 --max-contracts 80 --bootstrap 1999 --min-iv-changes 8 --max-iv-changes 63 --posterior-draws 256 --output-dir results/analysis/wti_aao_market_iv_bayes/experiment004 --private-dir data/databento/wti_aao_bulk/derived_private/experiment004

No purchases, Databento API calls, source SQLite writes, automatic Github Actions jobs or automatic Git commits are part of this design. The daily history is constructed chronologically; the same-day IV is appended only AFTER scoring that date. Historical observation revisions remain last known at archive end, just as in Experiment 003: this is not fully contemporaneous data-vintage reproducibility.

## Output contract and archiving

Aggregate output: results/analysis/wti_aao_market_iv_bayes/experiment004/

- experiment_manifest.json — provenance, settings, groups seen, groups eligible, holdout counts, models, clipping and model-boundary statement.
- method_metrics_by_split.csv — actual/theoretical MAE, RMSE, signed bias, number of dates and contracts for development vs holdout.
- method_metrics_by_year.csv — evaluation year breakdown.
- method_metrics_by_maturity.csv; method_metrics_by_moneyness.csv — stratified errors and counts.
- daily_actual_mae.csv — actual-mark date-level MAE.
- paired_actual_month_block_ci.csv — actual-only comparisons against unchanged lagged_IV and integration-vs-plug-in.

Private detailed result: data/databento/wti_aao_bulk/derived_private/experiment004/AAO_MARKET_IV_BAYES_CONTRACT_PRICING.csv.gz, including predicted/observed mark, method, prior-IV observation age, posterior sigma mean/sd and number of history changes. Must be committed via Git LFS to the **private** repo only, not circulated publicly.

After a SUCCESSFUL full run, while on the author's results branch:

    git add --sparse -- results/analysis/wti_aao_market_iv_bayes/experiment004/
    git add --force --sparse -- data/databento/wti_aao_bulk/derived_private/experiment004/AAO_MARKET_IV_BAYES_CONTRACT_PRICING.csv.gz
    git diff --cached --name-only
    git commit -m "Record local experiment004 Bayesian market-IV comparison"
    git push

Do not reset/clean/switch sparse checkout without auditing; never overwrite paid source DBNs, original SQLite or previous empirical outputs. Preserve failures, logs (override gitignore explicitly if useful), code, diagnostics, configurations, and negative results. No GitHub workflow may run the heavy study.

## Exit criteria / interpretation

1. Tests pass locally before real-data run.
2. Nonzero holdout actual-flagged eligible dates and contract observations, with all eight methods on IDENTICAL rows.
3. Baseline lagged_IV predictions numerically unchanged from original code.
4. All historical IV dates strictly earlier than valuation dates, including posterior inputs.
5. Report true IV ages, actual/theoretical flags, draw clipping, eligibility exclusions and actual-only month-block inference.
6. Bayesian success is **not** assumed: if the IV-posterior approach loses against previous IV, report the failure. Neither better MAE nor tighter CI establishes structural AAO pricing without actual CL fixings.
7. No result-dependent hyperparameter changes on the same 2025–26 test set. Further alternatives need separate named hypotheses and new holdout data or transparent exploratory qualification.

This document and its implementation are the portable handoff for future agents; the Experiment 003 2026-10-27 handoff is the prior validated empirical reference. **Experiment004 result claims remain pending actual local execution.**
