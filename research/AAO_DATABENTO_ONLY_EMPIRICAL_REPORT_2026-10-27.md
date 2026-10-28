# WTI AAO Databento-only study — completed empirical evidence and handoff

**Status (2026-10-27):** The author completed the local real-data pilot, 2023–2026 six-method benchmark, publication-figure postprocessing, and volatility-gap diagnostic. These results are committed on branch **results/aao-databento-pilot-2023h1-20261026**. This dated report supersedes older statements that AAO-only pricing experiments were pending. **Manuscript not finished or submitted.** No GitHub-hosted experiments were run.

## 1. Source of truth, safe workflow, and provenance

Primary evidence in this branch:

- Pilot: results/analysis/wti_aao_databento_only/pilot_2023h1/{experiment_manifest.json,method_metrics.csv,daily_metrics.csv,cluster_intervals.csv}
- Full: results/analysis/wti_aao_databento_only/full_2023_2026/{experiment_manifest.json,method_metrics.csv,daily_metrics.csv,cluster_intervals.csv}
- Diagnostics: results/analysis/wti_aao_databento_only/volatility_gap_diagnostic/ (eight aggregate CSV/JSON files).
- Private contract-level records: data/databento/wti_aao_bulk/derived_private/{pilot_2023h1,full_2023_2026}/AAO_DATABENTO_REDUCED_FORM_CONTRACT_PRICING.csv.gz (Git LFS).
- Sources/code: experiments/wti_aao_databento_only.py; bayesian_asian_options/src/bayesian_asian_options/aao_databento_only.py; scripts/plot_aao_databento_only.py; scripts/diagnose_aao_volatility_gap.py; tests/test_aao_databento_only.py.
- Figures: figures/aao_databento_only/full_2023_2026/{fig06_databento_benchmark_mae,fig07_databento_date_cluster_intervals,fig08_databento_mae_time_series}.{pdf,png,svg} plus figure_manifest.json.

Git commits: full run **7c89cc65050b3f6a3486fca3b2b1a9a17b2ce4f1**; figures **cba8f13c46e0a1db737e3eafbbae76984c7cdd27**; diagnostic script **7abc8ab160234593b7278c2aed925a32b5cab995**; diagnostics **6d363b8b47aa36c05514b920c462997d5d1d62f1**. User reported **12 passing synthetic tests** before launching the first pilot. Figures were created manually, no extra pricing computation.

Data provenance: 81 months of Databento AAO.OPT definitions and statistics, January 2020–September 2026, **162 compressed source DBNs**. Author's local preflight returned ready=true and 162/162 present; earlier 162/162 SHA256 manifest audit succeeded. Reconstructed provisional cross-month settlement SQLite was present locally. Earlier source reconciliation contained 5,105,603 selected final nonintraday candidates on 1,700 reference dates (including 2019-12-31). **Candidates are not the priced test sample.** Raw DBNs and SQLite Git LFS pointers are versioned in the private repository; independent remote downloading of all LFS payloads was not carried out here.

**IMPORTANT BRANCH WARNING:** On 2026-10-27 this results branch was **5 commits ahead and 45 behind main** before documenting this result. Main has newer paper/handoff infrastructure; this branch has completed empirical results. Do not merge, rebase, reset, force-push, change sparse checkout, or overwrite local market files casually. Do not infer that the new results are already present in main. The author explicitly wants heavy studies to run **locally**, not GitHub Actions; manual Git push is allowed. Any later integration must preserve both histories and all local user changes.

## 2. Model, information boundary, and measurement

The CME AAO payoff uses an arithmetic average of first-nearby CL settlements during the fixing window. The purchased **AAO definition/statistics alone do not contain those underlying CL fixings or a CL forward curve**. This particular study is a **reduced-form lognormal approximation for the terminal average**, NOT a structural simulated arithmetic Asian payoff. All prices and errors reported here are USD per barrel.

For each option expiry on a valuation date **before averaging begins**, the script fits an affine put/call parity relation from **up to seven (minimum four) matched actual-flagged same-date call-put strikes**:

    C_t(K) - P_t(K) = intercept_t - discount_t * K
    implied_expected_average_t = intercept_t / discount_t.

Requires strike span >=3, acceptable parity RMSE <=0.40, positive plausible expected average (5–300), discount within 0.75–1.05. Eligible options have 7–366 days to expiry and their date precedes the start of the fixing month. All call and put contracts with reserved **anchor strikes** are excluded from targets. Targets are sampled from remaining strikes with strike/F between .75 and 1.25 (up to 40 pilot or 80 full option rows per expiry). Methods use identical target rows. Actual/theoretical settlement flags are separate; **actual-flagged does not prove an executable transaction**. Marks use last-known archive-end revisions, not audited point-in-time event availability.

All methods use **same-day inferred expected average and discount**; only their volatility inputs are strictly from earlier reference dates. Therefore the work is a **retrospective conditional cross-sectional settlement-price comparison**, not a fully ex-ante independently sourced forecast, not hedge P&L, and not a study using true WTI P-measure futures returns.

Methods:
1. **PI**: average Black terminal-average proxy prices across **128** posterior sigma draws.
2. **PM**: Black price using the **mean of the same sigma draws**.
3. **rolling21/rolling63**: annualized SD of last 21/63 usable **same-expiry parity-forward log changes**.
4. **ewma63**: exponentially weighted SD of previous returns using **63-observation half-life**.
5. **lagged_IV**: median of invertible prior-date **AAO near-ATM actual-flagged** option implied sigmas from up to 12 nearest non-anchor observations; latest finite earlier reference date within 10 calendar days; not today's target price.

The historical proxy observations are log(F_{t,T}/F_{t-1,T}) for a **fixed expiry T** and reference-date gaps <=4 calendar days, annualized by sqrt(252). These are **changes in expected average**, not actual front-month CL returns, nor a constant-horizon average-volatility series. Inverse-gamma variance prior parameters are alpha0=3, beta0=.16 and the Gaussian sample mean is profiled out. History is updated only AFTER scoring each date. In general, posterior-integrating prices cannot repair systematic miscalibration of the sigma estimand.

## 3. Executed study designs and exact sample size

| Field | Pilot 2023 H1 | Full 2023–Sep 2026 |
| --- | ---: | ---: |
| Source start | 2022-01-01 | 2021-01-01 |
| Evaluation start | 2023-01-01 | 2023-01-01 |
| Evaluation end inclusive | 2023-06-30 | 2026-09-30 |
| Date stride | 15 | 5 |
| Maximum targets per expiry | 40 | 80 |
| Date bootstrap resamples | 99 | 1,999 |
| Source reference dates scanned | 377 | 1,448 |
| Expiry-date groups seen | 4,146 | 15,971 |
| Groups with valid parity anchor | 3,943 | 14,847 |
| Groups priced (lagged history eligible) | 81 | 1,689 |
| Unique priced valuation dates | **9** | **189** |
| Non-anchor target contract-dates | **3,135** | **111,585** |
| Actual-flagged target rows | 2,829 | **97,341** |
| Theoretical-flagged target rows | 306 | **14,244** |
| Posterior sigma draws per group | 128 | 128 |

Pilot evaluation dates 2023-01-06–2023-06-29. Full evaluation dates **2023-01-03–2026-09-28**. Full actual marks span **189 dates** and theoretical marks span only **51 dates**. The 111,585 target rows, multiplied by six identical-method predictions, yield **669,510 predictions**, NOT independent trials. The 14,847 groups with anchors are not 14,847 independently priced groups. Inclusion requires availability of **lagged_IV**, causing IV-availability sample selection.

## 4. Primary result: full actual-flagged sample

Source: full_2023_2026/method_metrics.csv. Error = predicted minus observed, USD/bbl. All methods share **97,341** actual-flagged target contract-dates on **189** valuation dates.

| Model | MAE | RMSE | Mean bias |
| --- | ---: | ---: | ---: |
| **lagged_IV** | **0.218420** | **0.297907** | **-0.001969** |
| PI | 0.804044 | 1.137151 | -0.697368 |
| ewma63 | 0.805424 | 1.127485 | -0.706941 |
| PM | 0.806818 | 1.140106 | -0.701837 |
| rolling63 | 0.827716 | 1.128168 | -0.664500 |
| rolling21 | 0.943683 | 1.247748 | -0.589977 |

Lagged_IV's pooled MAE is **72.8% lower** than PI's; PI improves pooled MAE relative to PM by only **0.002774 USD/bbl**. Lagged IV has the lowest actual-only daily MAE on **181 of 189 dates**. It beats PI on **186/189** dates; PI beats PM on **166/189**. There is a large *negative* PI/PM pricing bias; near-zero aggregate lagged_IV bias can mask offsetting maturity/strike-level errors. **RMSE ranking differs from MAE ranking:** ewma63's RMSE is slightly smaller than PI's.

Full theoretical-flagged marks (n=14,244, 51 dates):
| Model | MAE | RMSE | Bias |
| --- | ---: | ---: | ---: |
| lagged_IV | **0.313206** | **0.919894** | -0.054939 |
| PI | 0.825226 | 1.222001 | -0.647853 |
| PM | 0.829088 | 1.225203 | -0.652629 |
| ewma63 | 0.834812 | 1.238455 | -0.639318 |
| rolling63 | 0.801613 | 1.213716 | -0.517076 |
| rolling21 | 0.910642 | 1.346617 | -0.617290 |

Theoretical-flagged exchange settlement marks should not be equated with independent traded prices.

## 5. Corrected inference, not 97,341 independent samples

**Original main-study intervals** (full_2023_2026/cluster_intervals.csv): bootstrap **valuation days**, 1,999 resamples, but **mix actual-flagged and theoretical-flagged marks** when forming each date-level MAE. These are **not the proper primary intervals for the actual-only headline table**. Paired improvement over PM (positive favors alternative):
- PI +0.002761, 95% [+0.002427,+0.003098]
- lagged_IV +0.546634, [+0.480876,+0.615381]
- rolling21 -0.138732, [-0.209353,-0.066720]
- rolling63 -0.024406, [-0.064419,+0.016500]
- ewma63 -0.001875, [-0.024615,+0.020497]

**Primary corrected robustness check:** volatility_gap_diagnostic/paired_actual_month_block_ci.csv recomputes **actual-only** daily errors and resamples **45 calendar-month blocks**, 1,999 resamples (189 paired valuation days):
| Model vs PM | Mean daily MAE improvement | 95% month-block interval |
| --- | ---: | ---: |
| PI | +0.002670 | [+0.002136,+0.003228] |
| **lagged_IV** | **+0.543825** | **[+0.418308,+0.679754]** |
| rolling21 | -0.142341 | [-0.263037,-0.016668] |
| rolling63 | -0.026878 | [-0.097502,+0.046414] |
| ewma63 | -0.001750 | [-0.040929,+0.041896] |

The PI/PM gain is distinguishable from zero under this procedure but **economically very small**. Mean date-level improvements are NOT the same statistic as differences in contract-weighted overall MAEs. Calendar-month block bootstrap mitigates some serial dependence; does **not** establish independence across adjacent months or validate a fully ex-ante trading experiment.

**Figure warning:** fig07_databento_date_cluster_intervals displays the **original mixed-mark** interval, not the corrected actual-only month-block intervals. Do **not** use it unmodified as a chart of actual-only inference in the manuscript.

## 6. Actual-only regime, maturity and strike-ratio breakdowns

Source: volatility_gap_diagnostic/pricing_by_year.csv. Year 2026 ends September.

| Year | Actual targets | PI MAE | PM MAE | lagged_IV MAE | PI bias |
| --- | ---: | ---: | ---: | ---: | ---: |
| 2023 | 23,315 | 0.825791 | 0.828170 | **0.267987** | -0.631134 |
| 2024 | 26,308 | 0.420836 | 0.421931 | **0.191716** | -0.266959 |
| 2025 | 25,157 | 0.609061 | 0.612933 | **0.164358** | -0.553915 |
| 2026 Jan–Sep | 22,561 | 1.445840 | 1.449756 | **0.258617** | -1.427667 |

Source: volatility_gap_diagnostic/pricing_by_maturity.csv (actual-only):
| Days to expiry | Targets | PI MAE | PM MAE | lagged_IV MAE | PI bias |
| --- | ---: | ---: | ---: | ---: | ---: |
| 1–30 | 557 | 0.296318 | 0.295447 | **0.054806** | +0.157040 |
| 31–60 | 11,533 | 0.375810 | 0.375555 | **0.110350** | -0.008923 |
| 61–120 | 22,945 | 0.532519 | 0.533660 | **0.176531** | -0.385117 |
| 121–240 | 41,973 | 0.856951 | 0.860000 | **0.233467** | -0.821773 |
| >240 | 20,333 | 1.258039 | 1.263905 | **0.300408** | -1.206820 |

Source: volatility_gap_diagnostic/pricing_by_moneyness.csv. On actual near-ATM marks with **0.97 <= K/F <= 1.03** (11,685 targets), PI MAE **1.013934**, lagged_IV **0.121711**. K/F bins are *strike-ratio bins*, not automatically put/call-aware moneyness categories; stratify option side in future.

## 7. Measured volatility gap explaining the ranking

Source: volatility_gap_diagnostic/group_near_atm_volatility_comparison.csv and diagnostic_summary.json. For each expiry-date group the diagnostic selects up to eight near-ATM **actual-flagged, non-anchor** target observations and **inverts current target settlement prices** in the same reduced-form model. Groups with >=2 invertible prices: **1,689**. Current target IV is *ex post explanatory only*; it **must NEVER be fed into a lagged prediction, fitted model or backtest**.

| Volatility summary, group equal-weighted | Mean | Median |
| --- | ---: | ---: |
| Current target-date IV (retrospective) | **30.9748%** | 29.8216% |
| Strictly lagged option IV | **30.8839%** | 29.7849% |
| Bayesian PM price-equivalent volatility | **26.6787%** | 26.6594% |
| Bayesian PI price-equivalent volatility | **26.6800%** | 26.6574% |
| Current IV minus PM | **+4.2961 pp** | +3.8823 pp |
| Current IV minus lagged IV | +0.0910 pp | +0.0026 pp |

**80.99%** of groups have current IV above PM. **50.21%** have current IV above lagged IV. In **94.38%** of eligible groups lagged IV is closer, in absolute volatility distance, to retrospective current IV than PM is.

Volatility comparison, group-equal means by year:
| Year | Groups | Current IV | PM equivalent sigma | Lagged IV | Current minus PM |
| --- | ---: | ---: | ---: | ---: | ---: |
| 2023 | 443 | 32.65% | 29.25% | 32.65% | +3.40 pp |
| 2024 | 428 | 26.61% | 25.30% | 26.61% | +1.30 pp |
| 2025 | 435 | 27.79% | 23.57% | 27.61% | +4.22 pp |
| 2026 Jan–Sep | 383 | 37.54% | 28.78% | 37.35% | **+8.76 pp** |

Volatility gap by residual maturity:
| Remaining days | Groups | Current IV minus PM |
| --- | ---: | ---: |
| 1–60 | 192 | **-1.28 pp** |
| 61–120 | 372 | +3.35 pp |
| 121–240 | 729 | +5.23 pp |
| >240 | 396 | +6.17 pp |

The **sign reversal at short expiry** and larger gaps for long maturities mean that a universal fixed volatility uplift is *not* supported. Also note remaining days to expiry is not equivalent to count of CL monthly fixing dates. The 2026 change can reflect market regimes, group composition, volatility mismatch or data-generation mechanics: **do not claim it identifies a causal mechanism**.

## 8. Interpretation: established facts versus hypotheses

**Supported:**
- Lagged AAO option IV prices this conditional cross-section much more accurately than historical parity-forward-return volatility.
- Historical-proxy PI and PM systematically underprice actual-flagged options; lagged IV is approximately unbiased on average.
- Previous-date IV tracks retrospective market-equivalent volatility much more closely (94.38% of groups).
- Bayesian integration over this posterior improves PM slightly, but cannot fix a badly targeted volatility distribution by itself.
- The mismatch is tenor-dependent, and 2026 is particularly pronounced.

**Not established:**
- "Bayesian inference is inferior" in general; only **this historical-proxy posterior/pricing specification** was evaluated.
- A separately identified P-to-Q variance risk premium. The proxy is not CL P-measure realized volatility.
- Fully independent prospective AAO price predictions. Same-day parity anchors, last-known mark vintages, and IV-availability selection remain.
- Structural Asian-option pricing from first-nearby fixing paths, independently identified risk-free term structure, real-time executable trades, or hedging performance.
- Publication-ready novelty or a specific journal acceptance outcome. Earlier Barchart/LO/CL/JFM/REMEF work remains separate.

**Plausible explanation to test:** changes in an expiry-specific *conditional expected average* are a different quantity from option-market dispersion of the future terminal average. A comparatively persistent lagged option IV better represents what these option settlement prices encode. Variance-risk-premium and smile/model misspecification may contribute, but the existing exercise cannot separately identify them.

## 9. Reproducing the study on Windows, locally only

Conda environment: asian-options. From repository root, after ensuring recovered sources, executable modules, and SQLite exist:

~~~powershell
conda activate asian-options
python -m scripts.aao_lfs_preflight --require-complete
python -m pytest tests/test_aao_databento_only.py -q

# Heavy computations: use NEW output locations if reproducing archived results.
python -m experiments.wti_aao_databento_only --execute --source-start 2022-01-01 --eval-start 2023-01-01 --eval-end 2023-06-30 --date-stride 15 --max-contracts 40 --bootstrap 99 --output-dir results/analysis/wti_aao_databento_only/reproduction_pilot --private-dir data/databento/wti_aao_bulk/derived_private/reproduction_pilot

python -m experiments.wti_aao_databento_only --execute --source-start 2021-01-01 --eval-start 2023-01-01 --eval-end 2026-09-30 --date-stride 5 --max-contracts 80 --bootstrap 1999 --output-dir results/analysis/wti_aao_databento_only/reproduction_full --private-dir data/databento/wti_aao_bulk/derived_private/reproduction_full

# Postprocess only, no repricing:
python -m scripts.diagnose_aao_volatility_gap --output-dir results/analysis/wti_aao_databento_only/reproduction_volatility_gap_diagnostic
python -m scripts.plot_aao_databento_only --input-dir results/analysis/wti_aao_databento_only/full_2023_2026 --output-dir figures/aao_databento_only/reproduction_full
~~~

The diagnostic's compressed private source defaults to full_2023_2026, not the fresh reproduction_full. Override --private-file if comparing a new run. Never overwrite versioned completed runs inadvertently. No vendor calls, Barchart inputs or GitHub-hosted study execution are needed. Git pushes are for retaining results, NOT running experiments. Plot figure 07 remains the pre-correction mixed-mark CI.

## 10. Research next steps / handoff

See **research/AAO_DATABENTO_ONLY_MARKET_INFORMED_BAYES_PROTOCOL_2026-10-27.md** for the proposed controlled next experiment.

Before modifying the manuscript: reproduce actual-only month-block figure 07, provide error decomposition by year/maturity and option side, verify information cutoffs, examine the expiry-shrinking forward-return proxy and IV staleness. Study a market-informed Bayesian model with **strictly lagged IV history** and compare it on identical contract-date rows to unchanged lagged_IV and a simple lagged-IV smoothing baseline. Use chronological train/validation/test windows by valuation date, time-series-aware paired uncertainty, and an independent paper contribution assessment. No fitted current-day target option prices are permissible.

The selected manuscript's source and other workstreams live in newer main and may not be present in this historical results branch. **Do not copy older Barchart/LO results into this study** or merge divergent branches without an intentional plan. This report should be linked from a future main handoff only after safe integration.

_This document reports verified pushed artifacts and straightforward derived arithmetic as facts. Everything labelled hypothesis, explanation, next step, validation requirement or unknown remains unproven. It is intended as a durable replacement for chat-based handoff._