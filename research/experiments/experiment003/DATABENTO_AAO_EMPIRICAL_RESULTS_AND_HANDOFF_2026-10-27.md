# Experiment 003: WTI AAO Databento-only empirical evidence and research handoff

**Evidence frozen:** 2026-10-27. **Repository branch:** `results/aao-databento-pilot-2023h1-20261026`. **Status:** pilot, full reduced-form benchmark, graphics and diagnostic complete and pushed; future model extensions **not yet implemented or executed**.

> **Scope / scientific boundary.** This experiment is **not** a structural Asian option model using actual first-nearby CL settlement fixings. Purchased Databento AAO option definitions and reconciled settlement statistics do **not** provide CL fixings or a risk-free curve. Instead, the code infers an AAO terminal-average forward and effective discount from **same-date, disjoint-strike AAO call/put parity**, then uses a reduced-form lognormal Black approximation for the terminal arithmetic average. Volatility methods use dates strictly before the evaluation date. Therefore the reported errors are **conditional cross-sectional retrospective valuation errors**, **not** fully ex-ante independently sourced forecasts, not direct historical-CL-volatility estimates, and not a structural comparison of actual realized Asian volatility and implied volatility.

## 1. Evidence index and provenance

| Artifact | Repository path |
| --- | --- |
| Experiment runner | `experiments/wti_aao_databento_only.py` |
| Mathematics and estimators | `bayesian_asian_options/src/bayesian_asian_options/aao_databento_only.py` |
| Pilot (2023 H1), manifest and score tables | `results/analysis/wti_aao_databento_only/pilot_2023h1/` |
| Full benchmark, manifest and score tables | `results/analysis/wti_aao_databento_only/full_2023_2026/` |
| Full compressed **private** contract-level results (Git LFS) | `data/databento/wti_aao_bulk/derived_private/full_2023_2026/AAO_DATABENTO_REDUCED_FORM_CONTRACT_PRICING.csv.gz` |
| Pilot compressed **private** contract-level results (Git LFS) | `data/databento/wti_aao_bulk/derived_private/pilot_2023h1/AAO_DATABENTO_REDUCED_FORM_CONTRACT_PRICING.csv.gz` |
| Figure-generation code | `scripts/plot_aao_databento_only.py` |
| Published-figure candidates, SVG/PDF/PNG and manifest | `figures/aao_databento_only/full_2023_2026/` |
| Read-only diagnostic script | `scripts/diagnose_aao_volatility_gap.py` |
| Diagnostic summary, grouped near-ATM IVs, 45-month inference, annual/maturity/moneyness tables | `results/analysis/wti_aao_databento_only/volatility_gap_diagnostic/` |
| Local source-integrity checks | `scripts.aao_lfs_preflight`, `scripts.audit_aao_manifests` |
| Original paid option records | `data/databento/wti_aao_bulk/raw/` (162 Git LFS DBN files) |
| Reconstructed settlement database | `data/databento/wti_aao_bulk/derived_private/aao_cross_month_PROVISIONAL_81_months.sqlite3` (Git LFS) |

Source acquisition: 81 months, January 2020–September 2026, 162 original definition/statistics DBNs. The author's earlier local complete-source preflight reported 162/162 files and the original SHA256 manifest audit passed. These checks do **not** independently verify a fresh remote download of the complete LFS payloads. All expensive experiments were run **locally by the author**; no study was executed by GitHub Actions. Do not infer anything from the presence of LFS pointers alone. Preserve original files and independent backups.

Pilot result commit `267a99d8`; full result commit `7c89cc65`; figure commit `cba8f13c`; volatility-gap script commit `7abc8ab1`; diagnostics commit `6d363b8b`. See the Git history for exact snapshots. The work is on the results branch, **not necessarily merged to `main`**.

## 2. Exact design and estimators

For each admissible pre-fixing expiry/date group, select up to 7 actual-flagged matched call/put strike pairs, require at least 4, sufficient strike span, acceptable linear-parity fit and sensible implied effective discount/forward. **Exclude all their strikes (both sides) from targets.** Restrict target moneyness to [0.75, 1.25] of parity-implied forward, maturity approximately 7–366 days and dates before the first fixing month. Use identical targets for every method. A fixed subset of up to 40 (pilot) or 80 (full) target contracts per expiry-date group is selected by sorted strike and side. Targets may be actual- or theoretical-flagged; main interpretation uses **actual-flagged only**.

In terms of the terminal average `A`, the proxy is `A_T ~ Lognormal` with its risk-neutral expectation determined from put/call parity, and its lognormal width `sigma * sqrt(T)`. The expected forward average and discount are estimated contemporaneously from *other* strikes, not from external CL futures or a rate curve.

Six volatility methods on **strictly prior** information:
- **PI:** average option price over 128 inverse-gamma posterior variance draws.
- **PM:** option price at mean posterior sigma from the same draws.
- **rolling21 / rolling63:** standard deviation of trailing 21/63 available log changes in same-expiry parity-implied forward average, annualized by sqrt(252).
- **ewma63:** exponentially weighted standard deviation on the same changes (63-observation half-life in implementation).
- **lagged_IV:** median near-ATM implied terminal-average sigma from up to 12 non-anchor actual-flagged AAO option prices on an earlier reference date (lookback <=10 calendar days), inverted under this *same* lognormal pricing proxy.

The Bayesian proxy estimates variance of **parity-implied AAO forward-average changes**, **not** historical returns of first-nearby CL futures and **not** the risk-neutral distribution of the terminal average. This fundamental input mismatch is crucial. The previous-date AAO IV is itself derived from option prices, so the test compares instruments more closely matched to its output. Current-day target IV is **never allowed into an admissible prediction**; it is only used retrospectively in the later diagnostics.

Sampling: pilot source start 2022-01-01, evaluate 2023-01-01–2023-06-30, date stride 15, max 40 contracts per expiry, 99 valuation-date bootstrap replications; full source start 2021-01-01, evaluate 2023-01-01–2026-09-30, date stride 5, max 80 per expiry, 1,999 bootstrap replications. The model requires >=20 past observations and eligible lagged IV. Missing eligible groups are excluded **from every method**, yielding equal support but selection conditional on an IV history.

## 3. Completed pilot (Jan–Jun 2023)

Manifest: 377 selected source days, 4,146 groups seen, 3,943 parity-eligible, 81 groups with lagged history and priced, **9 priced valuation dates** (2023-01-06–2023-06-29), 3,135 unique contract-dates (**2,829 actual**, 306 theoretical), 128 posterior draws; six methods => 18,810 predictions.

| Method | Actual MAE (USD/bbl) | Actual RMSE (USD/bbl) | Actual bias (predicted - observed) |
| --- | ---: | ---: | ---: |
| lagged_IV | **0.283367** | **0.349197** | -0.003142 |
| PI | 0.984578 | 1.323936 | -0.828078 |
| PM | 0.986957 | 1.327342 | -0.832073 |
| ewma63 | 1.027116 | 1.390956 | -0.875300 |
| rolling63 | 1.072848 | 1.417518 | -0.851364 |
| rolling21 | 1.209654 | 1.555430 | -0.709327 |

Pilot inference is fragile because it uses only 9 date clusters and 99 resamples. Later full and month-block diagnostics supersede it for headline uncertainty claims. Pilot proves local end-to-end feasibility, not a definitive paper conclusion.

## 4. Full benchmark (Jan 2023–Sep 2026)

Manifest: 1,448 selected source days; 15,971 expiry-date groups seen, 14,847 parity eligible, 1,689 with sufficient history and priced. **189 valuation dates** (2023-01-03–2026-09-28), **111,585 unique contract-date observations**: 97,341 actual flagged and 14,244 theoretical flagged; same 6 methods => **669,510 prediction rows**. One must **not** treat these as 669,510 or 111,585 independent dates.

| Method | Actual MAE | Actual RMSE | Actual bias | Theoretical MAE |
| --- | ---: | ---: | ---: | ---: |
| lagged_IV | **0.218420** | **0.297907** | **-0.001969** | **0.313206** |
| PI | 0.804044 | 1.137151 | -0.697368 | 0.825226 |
| PM | 0.806818 | 1.140106 | -0.701837 | 0.829088 |
| ewma63 | 0.805424 | 1.127485 | -0.706941 | 0.834812 |
| rolling63 | 0.827716 | 1.128168 | -0.664500 | 0.801613 |
| rolling21 | 0.943683 | 1.247748 | -0.589977 | 0.910642 |

Units: USD per barrel for all pricing errors. All bias numbers are `predicted - observed`; negative = underpricing. Lagged IV lowers actual MAE versus PI by `(0.8040437119 - 0.2184197928)/0.8040437119 = 72.8%` (rounded). PI improves over PM by just **0.002774 USD/bbl in contract-weighted actual MAE**, an economically small difference. Lagged IV has lowest daily MAE on **181/189** sampled dates, vs EWMA 4, rolling63 3, PM 1; PI wins no daily comparisons against the other five jointly.

**Actual-only month-block paired inference** (45 calendar-month blocks, 1,999 bootstrap draws): improvement defined `MAE(PM) - MAE(method)`, using the **mean of date-level MAEs**, distinct from the contract-weighted MAE above.

| Method vs PM | Mean daily improvement | Month-block 95% percentile CI |
| --- | ---: | --- |
| PI | +0.002670 | [0.002136, 0.003228] |
| lagged_IV | **+0.543825** | **[0.418308, 0.679754]** |
| rolling21 | -0.142341 | [-0.263037, -0.016668] |
| rolling63 | -0.026878 | [-0.097502, 0.046414] |
| ewma63 | -0.001750 | [-0.040929, 0.041896] |

Earlier `full_2023_2026/cluster_intervals.csv` pools actual and theoretical observations in its date means (189-date bootstrap). Its values, such as PI +0.002761 and lagged IV +0.546634, **should not be represented as actual-only inference**. Use the corrected `volatility_gap_diagnostic/paired_actual_month_block_ci.csv` for primary inferential statements. These are still retrospective, exploratory intervals; month-blocks handle some temporal dependence but do not eliminate selection, model risk or dependence across nearby expiries.

## 5. Volatility-gap diagnosis

The diagnostic script reads the *already-computed* compressed price-level LFS artifact; it **does not refit models** or query a market provider. On **1,689** expiry-date groups with >=2 invertible actual near-ATM evaluation marks, it constructs:
- `sigma_current_target_implied`: near-ATM inversion of target-date **observed option marks**, strictly an **ex-post explanation**, prohibited in forecast features.
- `sigma_bayesian_PM` and `sigma_bayesian_PI_price_equivalent`: inversions of the saved PM/PI *predicted option prices* under the same proxy, not independent sigma forecasts.
- `sigma_lagged_option_implied`: saved previous-date AAO implied sigma, valid as lagged benchmark input.

**Equal-weighted across eligible expiry-date groups:**

| Volatility statistic | Mean | Median |
| --- | ---: | ---: |
| Current target-day AAO implied | 30.9748% | 29.8216% |
| Bayesian PM / price-equivalent | 26.6787% | 26.6594% |
| Bayesian PI / price-equivalent | 26.6800% | 26.6574% |
| Earlier-date AAO implied | 30.8839% | 29.7849% |
| Current IV minus PM | **+4.2961 percentage points** | +3.8823 pp |
| Current IV minus lagged IV | +0.0910 pp | +0.0026 pp |
| Lagged IV minus PM | +4.2051 pp | +3.8463 pp |

Current IV exceeds PM sigma in **80.99%** of groups, whereas it exceeds lagged IV in **50.21%**; lagged IV is **closer in absolute IV units** than PM in **94.38%** of groups. The overall pattern supports a **systematic historical-proxy-to-market-implied calibration gap**. It **does not prove** that the risk premium, information content, volatility scaling, term structure or absence of true CL fixings is *the* cause in isolation.

**Yearly group-equal mean volatility (%):**

| Evaluation year | Current implied | PM price-equivalent | Lagged IV | Current minus PM (pp) |
| --- | ---: | ---: | ---: | ---: |
| 2023 | 32.65 | 29.25 | 32.65 | +3.40 |
| 2024 | 26.61 | 25.30 | 26.61 | +1.30 |
| 2025 | 27.79 | 23.57 | 27.61 | +4.22 |
| 2026 (Jan–Sep) | 37.54 | 28.78 | 37.35 | **+8.76** |

**Expiry-dependent current-minus-PM (group-equal average):**

| Days to expiry | Current minus PM (pp) | Groups |
| --- | ---: | ---: |
| <=60 | **-1.28** | 192 |
| 61–120 | +3.35 | 372 |
| 121–240 | +5.23 | 729 |
| >240 | **+6.17** | 396 |

**Important qualification:** it is *incorrect* to say PM undershoots IV at **all maturities**: the shortest bucket has **negative** average current-minus-PM sigma. The positive gap increases for longer-dated options.

**Actual-flagged price MAE by maturity:**

| Days to expiry | PI | Lagged IV | Actual target contract-dates |
| --- | ---: | ---: | ---: |
| 1–30 | 0.2963 | **0.0548** | 557 |
| 31–60 | 0.3758 | **0.1104** | 11,533 |
| 61–120 | 0.5325 | **0.1765** | 22,945 |
| 121–240 | 0.8570 | **0.2335** | 41,973 |
| >240 | 1.2580 | **0.3004** | 20,333 |

The lagged-IV price advantage is observed in every maturity bucket. The paper must distinguish volatility calibration from pricing errors (maturity, strike, option rights and Black-vega weighting affect the translation between them).

The diagnostic contains detailed `pricing_by_year.csv`, `pricing_by_moneyness.csv`, `pricing_by_maturity.csv` and `group_near_atm_volatility_comparison.csv`; do not quote inferred row-level results absent from these files. The current target IV was obtained from **observed evaluation prices** and must never be introduced into a forward-looking estimator.

## 6. Interpretation: known vs hypothesized

**Supported by results:**
1. Lagged AAO IV has much smaller actual-mark pricing errors than all five alternatives on the common eligible sample, robust to year/maturity slices and month-block paired inference.
2. Bayesian PI is marginally but consistently superior to PM; the absolute mean improvement is a few tenths of a cent per barrel, not an economically major win.
3. PM and PI estimates price below observed marks on average; lagged IV is close to zero mean bias for actual-flagged marks.
4. A sizeable market-implied vs Bayesian historical-proxy volatility gap, concentrated particularly in longer tenors and in 2026, explains the *direction* of much of the pricing difference.
5. The lagged-IV input resembles the target-market implied volatility far more closely than the historical AAO parity-forward-return proxy does.

**Interpretations requiring a new experiment (NOT established causally):**
- Size of a volatility/variance risk premium; needs genuinely comparable P and Q objects and/or actual CL price/fixing data.
- Whether the Bayesian inverse-gamma prior is too influential, nonstationarity/regime breaks, price scaling, stale marks, temporal alignment, smile skew, option microstructure or observed settlement conventions drive the precise gap.
- Whether the terminal-average lognormal approximation introduces an important maturity-dependent distortion.
- Whether a Bayesian model **using lagged implied-volatility information on the same footing as the IV baseline** can improve out-of-sample accuracy or predictive uncertainty calibration.
- Whether a new result generalizes to a complete, strictly *ex-ante* Asian option hedge/prediction setting.

**Do not claim:** that Bayesian inference per se fails; that the market-implied baseline is a true first-nearby CL volatility observation; that actual benchmark prices are independent of all contemporaneous AAO information; that 111,585 prices are independent observations; that the 2026 subset is an entirely calendar-year sample; or that model parameters and priors have been tuned on a held-out set.

## 7. Figures, manuscript readiness and integrity

The three figure sets are generated under `figures/aao_databento_only/full_2023_2026/`:
- `fig06_databento_benchmark_mae`: actual vs theoretical flag benchmark MAE.
- `fig07_databento_date_cluster_intervals`: legacy full-study mixed-flag paired date CIs. **Should be updated/relabelled using corrected actual-only month-block intervals before publication.**
- `fig08_databento_mae_time_series`: running median of per-date MAE across methods (method trend, not independent daily samples).

Each has PDF/SVG/PNG plus `figure_manifest.json`. The user-generated figures are evidence artifacts, not necessarily final submission-ready graphics. Recalculate/relabel fig07 so plotted inference matches primary actual-flagged claim. Document the option data licensing and avoid publishing raw Databento source DBNs in a public repository. Keep source and contract-level outputs in the **private** Git LFS repo.

Original unrelated Barchart/LO/JFM/REMEF analyses and manuscripts must not be silently conflated with, overwritten by or merged into this Databento-only paper. The appropriate manuscript `paper/jcm/databento_main.tex` requires a scientifically honest methods/results/limitations rewrite and correct sample provenance before submission.

## 8. Next experiment: Bayesian model with comparable lagged market information (NOT YET RUN)

**Question:** Once both Bayesian and non-Bayesian models use strictly historical AAO-implied volatility information, does Bayesian uncertainty integration improve AAO option valuation relative to a simple lagged-IV benchmark?

Predeclare before executing:
1. **Read-only, local, no provider purchases.** Preserve existing source DBNs, SQLite, pilot, full, diagnostics and figures. Create a **new named experiment** and output path; do not overwrite experiment003.
2. **Information parity:** baseline `lagged_IV` unchanged. Bayesian posterior likelihood should consume **only observations strictly preceding t** (e.g., past near-ATM AAO implied sigmas with an explicit measurement-error or time-series model), with past forward-proxy changes optional as an additional feature arm. Absolutely no current target prices, target IV or current target residuals in features. Current-date disjoint parity anchors remain shared for apples-to-apples *conditional* cross-sectional evaluation, with their use disclosed.
3. **Honest comparison arms:** unchanged original PI/PM, unchanged lagged_IV, Bayesian market-IV posterior mean, Bayesian market-IV posterior predictive price integration; optional shrinkage/combined historical-proxy+lagged-IV arm. The Bayesian method must not be declared superior in advance.
4. **Time-ordering:** chronological train/calibration/test separation (e.g., explicit earlier training dates, later untouched test dates); no tuning on the same test set. Lag posterior update order must be verifiable.
5. **Equal contract support:** evaluate exactly the same eligible actual-flagged disjoint target strikes across methods, and separately tabulate theoretical flags. Preserve counts and failures, do not relax filters to manufacture improved outcomes.
6. **Scoring:** MAE, RMSE, signed bias, errors by maturity/moneyness/year and date-cluster/month-block paired differences. If returning predictive intervals, assess coverage, width and calibration rather than claiming a posterior standard deviation directly measures predictive option-price risk.
7. **Robustness:** sensitivity to Bayesian priors, lookback windows, smile/moneyness selection, previous-IV age and market regimes; report limitations due to true CL path absence and same-date parity anchors.
8. **Reproducibility:** save executable code, tests, configs, seeds, posterior diagnostics, negative results, contracts/group count attrition, concise score tables, plots, manifest and next steps in repo. Use Git LFS for large or private derived data. Keep all heavy workflows **manual-only**; user runs experiments on PC and pushes the meaningful outputs to the research branch.

**Stop/go rule:** do not write claims that the new Bayesian model wins until an independent local evaluation demonstrates it, including economically meaningful differences and correctly clustered uncertainty. If it loses, report that transparently; consider framing the paper as a controlled empirical analysis of statistical versus option-market volatility signals.

## 9. Continuation checklist

- [x] Local raw-source completeness and original manifest audit reported passed.
- [x] Databento-only 2023 H1 pilot executed and committed.
- [x] 2023–Sep 2026 benchmark executed and committed.
- [x] 3 figure families in three formats committed.
- [x] Read-only contract-level volatility-gap diagnosis and corrected actual-only month-block intervals committed.
- [x] Findings/limitations/provenance documented in this handoff.
- [ ] Verify full LFS binaries from a separate clean remote checkout when feasible.
- [ ] Upgrade confidence-interval figure to actual-only month-block result.
- [ ] Implement and execute **new** comparable-information Bayesian market-IV experiment **locally**.
- [ ] Fully audit contract settlement definitions, stale marks, posterior priors, maturity/tenor and selection before paper-level claims.
- [ ] Revise Databento-only manuscript after experiments; preserve older manuscript families.

**Git commands for author after reading this remote commit:** fetch the current branch and use a safe fast-forward if no local modifications conflict. **Do not** reset, clean, force-push, change sparse checkout or trigger GitHub Actions. This document is the repo-side handoff; use the actual CSV/JSON artifacts above, not conversational summaries, as final quantitative source of truth.
