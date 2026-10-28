# Experiment 005 — Conditional AAO price-interval calibration: full results and handoff

**Date:** 2026-10-27. **Status:** real local study completed by author and outputs committed. **Results commit:** b6ebffe6ffdf5e1e6b71d1844eeae9eef6b763ac. This document adds interpretation and exploratory read-only aggregations; it does **not** change models, rerun the experiment, execute GitHub Actions or mutate Databento source files.

## 1. Objective, interpretation and data

The next question after Experiments 003 and 004 was whether a **Bayesian predictive uncertainty model** could improve the *coverage and interval score of option settlement-mark pricing intervals*, despite no clear Bayesian market-IV point-price MAE advantage over unchanged lagged AAO IV.

**Crucial distinction:** Experiment 005 implements a **Bayesian normal-inverse-gamma predictive model for past settlement price residuals**, not direct credible intervals from Experiment 004's Bayesian volatility draws. The target is a retrospective, **conditional AAO option settlement mark**, with contemporaneous disjoint-strike put/call parity anchors reused inside frozen Experiment 004 point prices. This is NOT an Asian payoff distribution, fully ex-ante independent forecast, direct first-nearby CL realized volatility model or proof of a Bayesian trading strategy. The 2025–Sep 2026 period had already been inspected in previous experiments, so it is an **inspected retrospective holdout**, not a genuinely untouched holdout for model selection.

### Source-of-truth files

- Code: experiments/wti_aao_predictive_calibration.py.
- Synthetic tests: tests/test_aao_predictive_calibration.py.
- Fixed research protocol: research/experiments/experiment005/README.md.
- Official result manifest: results/analysis/wti_aao_predictive_calibration/experiment005/experiment_manifest.json.
- Official CSVs in that same folder: summary_by_split.csv, summary_by_year.csv, summary_by_maturity.csv, summary_by_moneyness.csv, daily_actual_scores.csv, paired_month_block_intervals.csv.
- Source private Experiment 004 LFS asset: data/databento/wti_aao_bulk/derived_private/experiment004/AAO_MARKET_IV_BAYES_CONTRACT_PRICING.csv.gz. Underlying binary is **not** exported into this report.
- Background: research/experiments/experiment004/FULL_RESULTS_AND_HOLDOUT_REVIEW_2026-10-27.md and research/experiments/experiment003/DATABENTO_AAO_EMPIRICAL_RESULTS_AND_HANDOFF_2026-10-27.md.

The manifest verifies **97,341 source actual-flagged contract-date records on 189 dates**. After the 15-date calibration warm-up/stratum eligibility, **89,696 distinct actual-flagged contract-dates on 174 dates** enter interval evaluation. Each is scored for 3 frozen point methods (unchanged lagged_IV, bayes_IV_PM, bayes_IV_PI), 2 interval calibrators (bayesian_nig and rolling_empirical), and nominal levels 90% and 95%: **1,076,352 interval-score rows**. Never treat these repeated forecasts as 1,076,352 independent data points. Development has 86 dates and 42,167 actual-flagged contracts; 2025–Sep 2026 inspected holdout has 88 dates and 47,529.

Methodological integrity from implementation: all calibration residuals use strictly **earlier** dates, history is updated only after scoring all targets on a given date, and prior contracts are date-weighted to reduce within-date pseudo-replication. A rolling history of at most 63 dates, minimum 15, is stratified by frozen point method, option side and maturity bucket. Bayesian NIG prior: mu0=0 USD/bbl, kappa0=0.5, alpha0=2.5, beta0=0.125 (USD/bbl)^2, with fractional/date-balanced Gaussian likelihood and Student-t posterior predictive. Rolling benchmark uses signed empirical quantiles and the same historical dates/weights. Both produce central 90% and 95% residual-mark intervals. This is NOT a full hierarchical correlated error model nor distribution-free conformal calibration.

Primary proper interval score for nominal level 1-alpha: width plus (2/alpha) times the magnitude of interval violation below or above. **Lower is better**. Coverage and width must be discussed together. A completely sharp but under-covering interval is not satisfactory; an extremely wide interval can cover everything but score poorly.

## 2. Core inspected holdout comparison

**Frozen point price: bayes_IV_PI**. Each comparison at one interval level uses the **same 47,529 actual-flagged contract-date targets on 88 valuation dates**; contract-weighted averages:

| Measure | NIG Bayesian residual | Rolling empirical residual |
| --- | ---: | ---: |
| 90% empirical coverage | **86.43%** | 84.72% |
| 90% average interval width, USD/bbl | 0.71068 | **0.64447** |
| 90% average interval score | **1.40781** | 1.44077 |
| 95% empirical coverage | 90.11% | **90.66%** |
| 95% average interval width, USD/bbl | **0.85042** | 0.85983 |
| 95% average interval score | 1.92897 | **1.86599** |

**Both are under-calibrated at nominal 90% and 95%.** Bayesian NIG has higher coverage and better point-weighted interval score at 90%, at the cost of wider intervals; at 95%, rolling empirical has higher coverage and better score. There is no uniformly superior interval calibrator.

**Paired month-block inference (actual-only daily mean interval scores; improvement positive means Bayesian better):**

| Period and frozen point price | Level | Mean daily NIG advantage vs rolling | 95% month-block interval | Number of month blocks |
| --- | --- | ---: | --- | ---: |
| **Inspected holdout, bayes_IV_PI** | 90% | +0.01471 | [-0.04132, +0.08478] | 21 |
| **Inspected holdout, bayes_IV_PI** | 95% | -0.04970 | [-0.12471, +0.00441] | 21 |
| Inspected holdout, lagged_IV | 90% | +0.01006 | [-0.04507, +0.07754] | 21 |
| **Inspected holdout, lagged_IV** | **95%** | **-0.05851** | **[-0.12160, -0.01036]** | 21 |
| Development, bayes_IV_PI | 90% | -0.03566 | [-0.06783, -0.00454] | 21 |
| Development, bayes_IV_PI | 95% | -0.05298 | [-0.08888, -0.01939] | 21 |

The intervals for the preidentified bayes_IV_PI comparisons in the 2025–26 inspected holdout **span zero at both nominal levels**: no reliable Bayesian interval-score gain is established. Rolling empirical *does* have a negative CI excluding zero for the secondary, unchanged lagged_IV 95% holdout comparison, subject to multiplicity and retrospectively inspected data caveats. In development, empirical quantiles beat Bayesian NIG in interval score at 90% and 95% with similarly negative month-block CIs. **Do not call the negative CI universal Bayesian failure or confirmatory evidence following repeated data inspection.**

**Ablation of point pricing method:** On the inspected holdout, with NIG residual calibration, the paired mean daily interval-score advantage of bayes_IV_PI over unchanged lagged_IV was -0.01119 at 90% (CI [-0.02482, +0.00228]) and -0.01336 at 95% (CI [-0.03444, +0.00771]). Both CIs contain zero. The posterior-integrated IV point price also produces no compelling incremental uncertainty-score benefit over plain lagged IV under the same NIG residual calibration.

## 3. Central finding: nonstationary coverage collapse during early 2026

Year-by-year contract-weighted coverage for **bayes_IV_PI**:

| Year | NIG 90% | Rolling 90% | NIG 95% | Rolling 95% | Eligible actual contracts |
| --- | ---: | ---: | ---: | ---: | ---: |
| 2023 (after warm-up) | 90.34% | 89.01% | 94.83% | 93.88% | 16,101 |
| 2024 | 96.15% | 97.12% | 98.30% | 98.87% | 26,066 |
| 2025 | 95.89% | 95.39% | 97.71% | 97.59% | 25,012 |
| **2026 Jan–Sep** | **75.92%** | **72.87%** | **81.67%** | **82.96%** | 22,517 |

The most important substantive result is **unstable predictive coverage**, not a few hundredths of USD differences in interval score. 2024–25 generally **overcovered**, whereas 2026 **undercovered sharply**. This invalidates a claim of stable 90%/95% calibration over market regimes.

The monthly breakdown was recomputed from the **committed daily_actual_scores.csv** as contracts-weighted coverage by calendar month. It shows the collapse was **particularly severe in March and April 2026**:

| Month 2026 | NIG 90% | Rolling 90% | NIG 95% | Rolling 95% | Eligible targets |
| --- | ---: | ---: | ---: | ---: | ---: |
| Jan | 77.3% | 72.2% | 85.2% | 84.3% | 2,467 |
| Feb | 66.9% | 64.3% | 72.5% | 74.0% | 3,099 |
| **Mar** | **59.0%** | **51.7%** | **64.7%** | **62.9%** | 3,743 |
| **Apr** | **56.9%** | **51.6%** | **63.2%** | **67.6%** | 2,893 |
| May | 80.6% | 73.7% | 91.1% | 93.0% | 2,700 |
| Jun | 90.1% | 94.2% | 94.7% | 97.9% | 2,377 |
| Jul | 94.1% | 93.8% | 97.4% | 98.1% | 1,450 |
| Aug | 95.2% | 95.6% | 97.4% | 99.0% | 1,241 |
| Sep | 94.0% | 95.4% | 96.6% | 98.4% | 2,547 |

This pattern is **consistent with a period of unusually large pricing residuals relative to recent calibration history**, followed by delayed interval widening/recalibration and later overcoverage. Causation is NOT determined: potential factors include market regime, pricing-vintage changes, underlying WTI dynamics, option mark discontinuities, maturity/strike composition, skew, stale settlements, and the reduced-form model. No claim about actual external historical events or their dates is made by these metrics alone. Do not fit a new model to this already-inspected episode and claim it is an untouched test.

2026 NIG 90% average interval score (bayes_IV_PI point price) rose to **2.16379 USD/bbl** versus **0.72724** in 2025; rolling empirical rose to **2.27193** from **0.69253**. The stressed episode also appears in 95% interval scores. Large undercoverage can dominate proper-score penalties even when average interval widths grow.

## 4. Maturity and moneyness heterogeneity

All figures below are **inspected 2025–Sep 2026 holdout** and frozen bayes_IV_PI pricing, contract-weighted. Maturity statistics for the 90% level:

| Days to expiry | Eligible targets | NIG 90% coverage | Empirical 90% coverage | NIG score | Empirical score |
| --- | ---: | ---: | ---: | ---: | ---: |
| 31–60 | 5,165 | 87.74% | 82.92% | **1.310** | 1.425 |
| 61–120 | 10,444 | 83.91% | 80.98% | **1.593** | 1.698 |
| 121–240 | 20,636 | 87.96% | 85.57% | **1.394** | 1.453 |
| >240 | 11,284 | 85.34% | 87.44% | 1.306 | **1.188** |

The 1–30-day bucket is absent from this table because the 15-prior-date group history requirement did not yield eligible scores there in the inspected holdout. This is a **sample eligibility effect**, not a missing market price claim. NIG wins the mean 90%-interval score in mid-tenor groups, while rolling empirical wins at >240 days. These are *descriptive* buckets without subgroup month-block CI.

At 90% moneyness level (K/parity-forward F), NIG coverage vs rolling for the same frozen PI price: below 0.90 **81.96% vs 78.30%** (both poor); 0.90–0.97 **82.88% vs 80.66%**; 0.97–1.03 **88.08% vs 86.28%**; 1.03–1.10 **89.05% vs 88.24%**; >1.10 **88.72% vs 88.00%**. The inferior coverage at lower K/F is noteworthy, but the grouping combines calls and puts, so it is **not** a side-specific smile/skew or delta-based risk result.

## 5. Methodological cautions and open checks

1. **Unchanged historical pricing assumption:** the option valuation baseline derives same-day average forward and discount using other (disjoint-strike) AAO option marks. No actual first-nearby CL fixing paths are modeled. Results are conditional cross-sectional retrospective mark prediction, not fully independent ex-ante risk-neutral Asian pricing.
2. **Bayesian uncertainty scope:** the NIG calibrator models historical **observed-minus-predicted AAO price errors**, not parameter uncertainty from Experiment 004 and not the actual payoff. Its date-weighted fractional normal likelihood still ignores correlation of option errors within dates, expiries and neighboring tenors.
3. **Source prices and information timestamps:** Experiment 004 sourced archive-end settlement revisions. Exact live availability and temporal vintage of prior-day residuals must be audited before making true executable forecasting claims.
4. **Sample composition:** 97,341 input actual contracts on 189 dates, with 89,696 evaluated on 174 after warm-up and side/maturity eligibility. Some strata/dates have no fitted calibration at the moment they are scored. All point methods are on equal support in the source code, but this does not make repeated contract predictions statistically independent.
5. **No guarantee:** the rolling empirical residual quantile benchmark is not distribution-free conformal inference. The NIG's Student-t predictive intervals have no guaranteed real-world frequentist coverage under nonstationarity, and the evidence shows they fail to maintain nominal rates during stressed episodes.
6. **Multiple testing, exploratory interpretation:** many calibrator/point/level/subgroup comparisons and multiple inspected test windows have been reviewed. Treat nominal bootstrap intervals as descriptive evidence, not adjusted confirmatory significance.
7. **Potential future independent research:** freeze a genuinely new model prior to new uninspected market dates; consider a **distribution-shift-robust, date-cluster-aware volatility/regime-aware conformal or Bayesian predictive calibration model** with strictly past updates, and compare against strong rolling empirical and lagged-IV baselines. Model 2026 performance as *past evidence of failure*, not a new untouched test. Sensitivity to residual scaling by vega, maturity and option price, robust heavy-tailed noise, residual nonexchangeability and time-vintage integrity are sensible preregistered directions, but none were tested here.
8. **No model alteration:** this report does not change the recorded experiment, its code, source LFS payload or outputs. Any new experiment must use a new named path, manually run locally by the user, and commit meaningful artifacts to the private results branch.

## 6. Final conclusion

**Under the already-inspected, retrospective conditional WTI AAO option-mark exercise, a date-balanced Bayesian normal-inverse-gamma residual predictive distribution did not deliver a consistent or statistically convincing interval-score advantage over simple rolling empirical residual quantiles.** Bayesian NIG had somewhat better pooled 90% coverage, but the rolling method yielded stronger pooled 95% scores; month-block primary Bayesian-PI comparisons included zero. Much more consequentially, **both methods fell far below their nominal 90% and 95% coverages in early 2026**, a warning that residual uncertainty is time-varying and historical calibration can fail abruptly.

**Publication-safe contribution:** a rigorously disclosed failure mode and market-regime sensitivity analysis of conditional AAO pricing uncertainty, potentially useful as an empirical methodological result if pricing definition, quote vintages, sample selection and competing methods are independently verified. No general Bayesian superiority or defeat, or fully ex-ante Asian option performance, is established.
