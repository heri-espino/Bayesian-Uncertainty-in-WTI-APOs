# Experiment 004: Full historical results and holdout review

**Verified:** October 27, 2026. **Status:** Author executed the full real-data run on a local PC, committed results (76e3c4bd8a3710c8a56a8f70cc267217472ed894); GitHub results inspected. This report documents analyses only. No new experiment was run by the assistant or by GitHub Actions.

**Research question.** Does Bayesian posterior-predictive integration of strictly earlier AAO market-implied volatility improve option-mark pricing relative to the **unchanged lagged-IV baseline**, when the information set is comparable?

**Main finding.** NO statistically persuasive or economically material improvement is established. On the predeclared 2025–September 2026 holdout, lagged IV has marginally better MAE and RMSE than either new Bayesian IV method. Month-block bootstrap intervals for paired improvements encompass zero. Posterior integration does not meaningfully improve upon its matched posterior-mean plug-in either. This is a null result for the tested implementation, not a universal indictment of Bayesian inference.

## Data and artifacts

- Pricing model and source-data caveats are identical to the completed Experiment 003, documented at research/experiments/experiment003/DATABENTO_AAO_EMPIRICAL_RESULTS_AND_HANDOFF_2026-10-27.md.
- Fixed design, priors and local run instructions: research/experiments/experiment004/README.md.
- New Python modules: bayesian_asian_options/src/bayesian_asian_options/aao_market_iv_bayes.py and experiments/wti_aao_bayesian_market_iv.py.
- Unit/synthetic checks supplied at tests/test_aao_market_iv_bayes.py. The author's pytest output was not shared; do not claim the tests passed on their PC.
- Official full-run summary JSON: results/analysis/wti_aao_market_iv_bayes/experiment004/experiment_manifest.json.
- Metric tables: method_metrics_by_split.csv, method_metrics_by_year.csv, method_metrics_by_maturity.csv, method_metrics_by_moneyness.csv in the same folder.
- Actual-only daily data: results/analysis/wti_aao_market_iv_bayes/experiment004/daily_actual_mae.csv.
- Date/month-block paired bootstrap: results/analysis/wti_aao_market_iv_bayes/experiment004/paired_actual_month_block_ci.csv.
- Private contract-level output (Git LFS): data/databento/wti_aao_bulk/derived_private/experiment004/AAO_MARKET_IV_BAYES_CONTRACT_PRICING.csv.gz. Its remote LFS pointer was verified: expected 21,361,152 bytes, SHA256 e802457151f9968bb28c197b979aff3e40be77c30cbb595f0c7eb7031cf6996c. The complete binary was not separately downloaded during this inspection.
- First smoke run: research/experiments/experiment004/SMOKE_RUN_2026-10-27.md.

The repository's authoritative numeric evidence is the committed CSV and JSON files above. Keep Databento contracts and records private. No paid-market raw data or price-level extracts are included here.

## Study design and sample

Source observations start 2021-01-01; evaluation 2023-01-01 to 2026-09-30. Date stride 5; up to 80 target contracts per eligible expiry/date. Eight methods; identical target support across methods: original historical PI/PM, rolling21, rolling63, ewma63, unchanged previous AAO lagged_IV, and new bayes_IV_PM/bayes_IV_PI. The new posterior models recent same-expiry, strictly prior-date, one-weekday log near-ATM AAO IV innovations via normal-inverse-gamma prior and Student-t predictive distribution, with 256 seeded sigma draws. All use **disjoint, contemporaneous, same-date AAO put/call parity anchors** for the expected terminal average and discount. There are no actual first-nearby CL fixing histories in this analysis, so pricing is a **reduced-form lognormal terminal-average approximation**, not full structural Asian option valuation, and **not** fully ex-ante independent-price prediction. Current evaluation option prices and current implied vols are not Bayesian volatility predictors.

Source days 1,448; expiry-date groups examined 15,971; groups with original and new eligible lagged histories 1,689; groups priced 1,689. **189 priced valuation dates, 111,585 distinct contract-date observations**, of which **97,341 actual-flagged** and **14,244 theoretical-flagged**. Eight models imply 892,680 total recorded price predictions; these are NOT independent samples. 0 clipped predictive sigma draws. Experiment manifest indicates no provider calls and no original-data writes.

Chronological development 2023–2024: **101 valuation dates / 49,623 actual contract-dates**. Prespecified holdout 2025–Sep 2026: **88 dates / 47,718 actual contract-dates**. The author's prior smoke test had already exposed January–March 2025 holdout results on a subset of sampled dates and contracts; the full 2025–26 period must therefore NOT be described as wholly untouched after that review. The implementation and fixed priors were not altered in response to the smoke result.

## Main actual-mark metrics (USD/bbl)

Errors are relative to settlement marks, lower MAE/RMSE is better. Signed bias = prediction - observed.

| Method | Development MAE | Holdout MAE | Holdout RMSE | Holdout bias |
| --- | ---: | ---: | ---: | ---: |
| **Unchanged lagged IV** | 0.227552 | **0.208924** | **0.301378** | -0.026425 |
| Bayesian IV posterior-mean plug-in | **0.226969** | 0.209752 | 0.302318 | -0.017422 |
| Bayesian IV posterior-predictive integration | 0.227001 | 0.209830 | 0.302422 | -0.016690 |
| Original historical-proxy PI | 0.611101 | 1.004689 | 1.348835 | -0.967024 |
| Original historical-proxy PM | 0.612799 | 1.008582 | 1.352022 | -0.971431 |
| EWMA-63 | 0.655809 | 0.961013 | 1.281477 | -0.912837 |
| Rolling-63 | 0.724141 | 0.935427 | 1.222813 | -0.798683 |
| Rolling-21 | 0.859475 | 1.031253 | 1.327652 | -0.662821 |

The holdout contract-weighted absolute MAE disadvantage of Bayesian IV PI vs lagged IV is about **0.000907 USD/bbl**, i.e. **0.43% of lagged IV's MAE**. Bayesian IV PM's disadvantage is about 0.000828 USD/bbl. PI's incremental disadvantage relative to its own PM is about 0.000079 USD/bbl. The market-IV model has virtually closed the large gap versus historical-proxy models, but that improvement is primarily an *information-set difference*, not evidence for posterior integration in isolation.

## Calendar-month-block paired inference (actual flags only)

Daily MAE(baseline) minus daily MAE(candidate); **positive favors candidate**. Group calendar dates by month and resample month blocks, 1,999 bootstrap replicates. These are **date-equal** averages, not contract-weighted MAE differences.

| Split/comparison | Dates | Months | Mean daily improvement | 95% CI |
| --- | ---: | ---: | ---: | --- |
| Holdout Bayesian IV PI vs lagged IV | 88 | 21 | **-0.001002** | **[-0.003307, 0.000820]** |
| Holdout Bayesian IV PM vs lagged IV | 88 | 21 | -0.000932 | [-0.003248, 0.000837] |
| Holdout Bayesian IV PI vs Bayesian IV PM | 88 | 21 | -0.000070 | [-0.000240, 0.000055] |
| Development Bayesian IV PI vs lagged IV | 101 | 24 | 0.000706 | [-0.000479, 0.001823] |
| Full sample Bayesian IV PI vs lagged IV | 189 | 45 | -0.000089 | [-0.001452, 0.001090] |
| Full sample original PI vs PM | 189 | 45 | +0.002670 | [0.002089, 0.003218] |

The main holdout interval **contains zero**. The matched Bayesian IV PI-minus-PM interval also contains zero. Do not frame either as statistically established gains. Month-block inference does not resolve residual dependence across expiries, data-vintage issues, model misspecification, or the adaptive interpretation problem created by earlier smoke inspection.

## Separate April 2025 to September 2026 comparison

A read-only reaggregation of committed daily_actual_mae.csv after the earlier smoke window (date >= 2025-04-01; first sampled date 2025-04-03, last 2026-09-28) gives **76 dates, 18 months, 39,492 actual contract-dates on equal method support**.

| Method | Contract-weighted MAE | Date-equal mean daily MAE |
| --- | ---: | ---: |
| **Lagged IV** | **0.219174** | **0.208246** |
| Bayesian IV PM | 0.220624 | 0.209652 |
| Bayesian IV PI | 0.220713 | 0.209729 |

Bayesian IV PI wins 34 of 76 dates; lagged IV wins 42. Date-equal mean improvement (lagged IV minus Bayesian PI) is **-0.001483 USD/bbl**. This *post-smoke sensitivity subset* was defined for transparency after initial exposure, not as an independently pre-registered test. It supports the full-holdout null finding.

## Results by year (actual flags, contract-weighted MAE)

| Year | Lagged IV | Bayesian IV PM | Bayesian IV PI | Actual contract-dates |
| --- | ---: | ---: | ---: | ---: |
| 2023 | 0.267987 | **0.266756** | 0.266819 | 23,315 |
| 2024 | 0.191716 | **0.191710** | 0.191713 | 26,308 |
| 2025 | 0.164358 | 0.164040 | **0.164012** | 25,157 |
| 2026 Jan–Sep | **0.258617** | 0.260723 | 0.260920 | 22,561 |

The Bayesian model has a small edge in certain earlier years, effectively ties in 2024 and loses in 2026. Year-specific causal explanations (drift changes, jumps, mean reversion, skew) are **not established** by these aggregate data.

## Results by holdout maturity (actual flags, contract-weighted MAE)

| Days to expiry | Contracts | Lagged IV | Bayesian IV PI | PI minus lagged |
| --- | ---: | ---: | ---: | ---: |
| 1–30 | 189 | **0.062241** | 0.067611 | +0.005370 |
| 31–60 | 5,165 | **0.145681** | 0.151122 | +0.005441 |
| 61–120 | 10,444 | **0.203652** | 0.206816 | +0.003164 |
| 121–240 | 20,636 | **0.208875** | 0.209165 | +0.000290 |
| >240 | 11,284 | 0.245296 | **0.243090** | -0.002206 |

Holdout performance is descriptively slightly better for Bayesian IV PI only at >240 days. **No maturity-specific clustered confidence intervals** are reported here. Differences in vega, mark price, and tenor composition matter.

## Results by holdout moneyness K/F (actual flags, contract-weighted MAE)

| K/F bucket | Contracts | Lagged IV | Bayesian IV PI |
| --- | ---: | ---: | ---: |
| <0.90 | 10,970 | **0.292510** | 0.299452 |
| 0.90–0.97 | 5,886 | **0.247556** | 0.250288 |
| 0.97–1.03 | 5,033 | **0.152227** | 0.153621 |
| 1.03–1.10 | 7,311 | 0.158337 | **0.155798** |
| >1.10 | 18,518 | 0.182509 | **0.180488** |

Both put and call sides appear; moneyness does not describe a clean delta or option-side-specific skew effect. Treat all subgroup advantages as descriptive until matched cluster-aware subgroup inference is preregistered.

## Interpretation and next-work boundaries

1. Lagged AAO option-implied volatility is a very strong and simple benchmark under the existing conditional cross-sectional valuation protocol. Market-IV Bayesian adjustments are extremely close to baseline, with **no established incremental advantage**. The original proxy-volatility Bayesian methods remain much worse, as independently documented in Experiment 003.
2. The model is explicitly Bayesian for *log-IV innovations*, not for underlying CL arithmetic-average fixing-path stochastic volatility. The posterior predictive distribution and the pricing integration should not be confused with validated predictive intervals or an estimated variance risk premium.
3. Source data represent last-known settlement revisions, and contemporaneous parity anchors are used by design. Audit quote vintage/timestamp alignment and AAO fixing calendars before asserting deployable forecast accuracy.
4. Tests, exact LFS binary verification, model uncertainty calibration, IV age and gap distribution, sensitivity to clipping/prior assumptions and year/maturity/moneyness subgroup intervals remain open quality checks.
5. **Do not optimize a new model on the present 2025–Sep 2026 holdout and label the same observations independent test evidence.** Any follow-up should be explicitly exploratory here or evaluated on a new genuinely unexamined period.
6. Preserve all original scripts, paid data, manifests, scoring CSVs and failures. Do not alter the completed Experiment 003/004 results or trigger heavy GitHub Actions. New experiments should be new separately named folders and local manual runs.

**Recommended publication wording:** Under a reduced-form conditional WTI AAO valuation test, a Bayesian model for strictly lagged option-implied-volatility innovations produced almost identical marks to using last observed implied volatility, with no reliable improvement in out-of-sample MAE. This does not establish the absence of Bayesian benefits under structural Asian option models or other information sets.
