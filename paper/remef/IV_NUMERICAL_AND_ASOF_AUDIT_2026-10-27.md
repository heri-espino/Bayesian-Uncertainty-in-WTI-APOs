# REMEF Paper A — original implied-volatility numerical and as-of audit

**Audit executed:** 2026-10-27, on the manuscript PR #115 branch.  
**Scope:** Original Barchart/CL/Curran forward-in-time panel, the 2,381-row prior-APO-IV smile, the 2,366-row same-contract IV carry, and the availability claims supported by their archived inputs. Added a bounded external-LO date-order check.  
**Final status:**
- **PASS: all original 2,381 / 2,366 contract-level price-error arithmetic and joins.**
- **PASS: independent re-estimation of all 4,762 stored previous-day/expanding IV-smile forecasts from the 2,574-row source-IV history, including documented source-date precedence.**
- **PASS: archived-model `training_end_date < valuation_date` checks and same-contract prior-IV source identity.**
- **NOT CLEARED: raw-vendor as-of/publication timestamps, historical snapshot vintage/revision history, original terminal-pricing source state, same-day data release timing, vendor redistribution rights, and settlement-mark versus executable-price identity.** The source files do not encode enough information to establish these things, so **publication-grade temporal availability cannot be certified** and the broad input-vintage gate remains open.

**Provenance:** Calculated directly from fetched GitHub **Git blob contents**, with independent numerical code, not by copying existing aggregate reports. Repeatable local standalone audit code has been committed in [`scripts/audit_remef_forward_iv.py`](../../scripts/audit_remef_forward_iv.py), but its Python implementation **has not been executed on the author's full checkout** in this review; the independent JS calculations below **were executed** against the three complete Git blobs. The script will produce a JSON report when run locally with `--write-json`, refusing to overwrite an existing report. Neither original paper files nor price data were modified; no vendor calls, simulation or paid GPU computation.

## 1. Exact committed inputs audited

| Meaning | Repository file | Git blob SHA |
| --- | --- | --- |
| Two fitted volatility-smile forecasts for each held-out option | `results/analysis/wti_extended_forward/forward_q_validation/forward_q_predictions.csv` | `a51ea9b98098256521fe5ce7bab69dbcc9923573` |
| Same-contract last-available IV carry, exact-date target and matched comparators | `results/analysis/wti_prior_contract_iv_carry/prior_contract_iv_carry_predictions.csv` | `08d6ebd961acefe6518185a762763441077bd1ed` |
| Underlying option-derived implied volatility inputs | `results/analysis/wti_extended_forward/apo_implied_volatility/apo_contract_implied_volatility.csv` | `33c6910911972eaffb4adfa56b8d992e583bbf11` |

The sources contain **4,762** forward-prediction rows (2 methods × 2,381 targets), **2,366** carry predictions and **2,574** individual source implied-volatility observations. Original valuation targets span **15 dates, August 24–September 14, 2026**, rather than 2,381 independent forecasting dates.

### Directly reaggregated pricing errors (USD/barrel)

| Design / precisely matched support | n option-date rows | n valuation dates | Signed mean error | MAE | RMSE |
| --- | ---: | ---: | ---: | ---: | ---: |
| Historical posterior-integrated, 2,381 complete forward rows | 2,381 | 15 | +2.402985469 | **2.618699384** | 3.408990604 |
| Previous-day AAO implied-volatility smile | 2,381 | 15 | –0.035221543 | **0.107545780** | 0.159356305 |
| Expanding earlier-date AAO-IV smile | 2,381 | 15 | –0.069675622 | **0.108809964** | 0.172497626 |
| Same-contract prior AAO-IV carry | 2,366 | 15 | –0.026886098 | **0.099156325** | 0.140280394 |
| Previous-day AAO-IV smile, **restricted to same carry observations** | 2,366 | 15 | –0.035482230 | **0.107416950** | 0.159401184 |
| Historical PI, **restricted to same carry observations** | 2,366 | 15 | +2.412022183 | **2.627911077** | 3.417337414 |

**New meaningful finding:** The simple **same-contract lagged IV persistence** has *lower* pooled mark MAE than fitting the previous-day smile on exactly the same 2,366 targets: **USD 0.099156 vs 0.107417 per barrel** (MAE advantage approximately **USD 0.008261/bbl**). This should be prominently reported: the fitted smile is **not** an incremental improvement over the simpler persistence control in this sample. Do not compare its 2,366-row error directly to a different 2,381-row baseline without the matched-support figures.

**Arithmetic exactness:** zero incorrect or duplicated contract/date keys; identical 2,381-key support for expanding and prior-date smiles; every one of 2,366 carry keys belongs to the earlier-smile panel. Independent reaggregation of source-row errors passes at floating point precision (max carry arithmetic residual <2×10⁻¹⁵, zero recorded forward arithmetic discrepancy). Every carry `market_settlement` and prior-day-smile/baseline comparator matches its original full-panel record to 1e-8.

## 2. Independent reconstruction of fitted volatility inputs

Reimplemented the committed six-parameter ridge-smile design from `experiments/wti_forward_q_validation.py` rather than trusting `predicted_sigma_q`:
- Columns `[1, x, x², I(call), I(call)*x, I(call)*x²]`, with `x = log_moneyness`; ridge penalty **1e-6** excluding the intercept.
- Previous-day method: `apo_implied_sigma_q` inputs at the most recent source date **strictly before** each target, separately per expiry.
- Expanding method: inputs **only before** the target, down-weighted with a **5-calendar-day** exponential half-life.
- Recomputed regression coefficients with a separate Gaussian-elimination implementation, then clipped predictions to `[1e-6, 3.0]`.

**Result:** all **170 expiry × target date × method** regressions and all **4,762 individual volatility predictions reproduced**, with maximum absolute `predicted_sigma_q` discrepancy **7.55×10⁻¹⁴**; zero fitted-group training-row-count discrepancies; zero `training_end_date` mismatches. No price/model rerun was required. This is stronger evidence than agreement with a reported MAE alone.

The 2,366 carried sigmas were also matched **one by one** against the identical `(prior_iv_date, expiry, contract_id)` row in the 2,574-row original IV source table, at absolute tolerance **1e-9**. **Zero missing or mismatched sources.** Carry calendar-date lag ranges **1 to 7 days** (median **1 day**).

**Caution:** This independently re-estimates `sigma_q` from the **saved source-IV table** and checks arithmetic of already saved option prices. It does **not** independently regenerate each Curran option price from archived vendor Barchart raw inputs, nor independently certify that the older source-IV inversion was based on a contemporaneously available *unrevised* settlement.

## 3. Dependence-robust exploratory comparison

Treat the **valuation date** rather than an individual strike/date row as the primary repeat unit. Define the per-day gain in absolute price error (positive means the second method is better):

`g_t = mean_{contracts on date t}(|error_baseline| − |error_candidate|).`

| Date-equal-weight contrast | 15-date mean gain, USD/bbl | Exploratory 95% interval, date resample | Exploratory 95% interval, circular 3-date blocks |
| --- | ---: | --- | --- |
| Historical PI minus previous-day IV smile | +2.813280 | [2.337696, 3.399610] | [2.231595, 3.637375] |
| Previous-day IV smile minus same-contract IV carry (matched 2,366) | +0.009205 | [0.003681, 0.014479] | [0.005232, 0.013067] |

These are **descriptive exploratory** percentile intervals calculated with **20,000 resamples** and a deterministic custom seeded resampler; the complete local Python audit uses a separate NumPy seeded generator and its resulting endpoint numbers need not exactly match. The second comparison shows positive carry gains on **13 of 15 dates**, but it is only about one standard AAO price tick (`$0.01/bbl`). With just **15 adjacent valuation dates**, the resampling cannot make the result an independently validated broad market law, and the non-independent settlement marks remain a bigger source of uncertainty than the conditional bootstrap standard error. Do **not** claim deployable trading significance.

## 4. Liquidity and exchange-mark sensitivity

From the 2,381 stored target observations:

| Stratum | Rows | Distinct dates | Historical PI MAE | Prior-day IV smile MAE |
| --- | ---: | ---: | ---: | ---: |
| All original targets | 2,381 | 15 | 2.618699 | 0.107546 |
| **Positive recorded volume** | **62** | **13** | 1.634008 | 0.108442 |
| Zero recorded volume | **2,319** | 15 | 2.645026 | 0.107522 |
| Open interest ≥100 | 553 | 15 | 1.989613 | 0.106866 |
| Open interest ≥500 | 200 | 13 | 1.252585 | 0.101464 |

The relative mark-error ranking persists in the 62 positive-volume rows, but **97.4% of the headline original target observations have zero recorded volume**. Even the 62 targets with a positive **daily** volume field are still **end-of-day Latest marks**, not documented matched contemporaneous option trades or executable quotes. This is a serious inferential distinction, not a cosmetic limitation.

## 5. As-of timestamp audit: what passes and what cannot be proven

### A. Stored forecasting-date information sets — **PASS**

1. For every previous/expanding smile row, recorded `training_end_date < valuation_date`. **0/4,762** violations. Actual regression inputs were re-selected from earlier `valuation_date` records and reproduce every forecast and training count.
2. For every same-contract carry row, `prior_iv_date < valuation_date`. **0/2,366** violations. All carried volatility values match the source IV history for that contract on that exact earlier date, **0 mismatches**.
3. The three price-error comparison files have no duplicate contract-date keys and match their target-date marks and prices. The target option's **same-day inverted IV** is present only as a saved diagnostic; independently reconstructed fitted smirks do **not** use it as a regressor.
4. `experiments/wti_external_vanilla_q_validation.py` explicitly filters LO surface reference dates `reference_ts < target_date`. Additionally checked all **1,240** rows in `external_vanilla_q_predictions.csv`: **0** non-strict date orderings across four methods, **minimum one calendar day**. This does **not** certify LO official publication timestamps/tree-source histories.

### B. Model target-day conditioning — permitted for a **same-day ex-post conditional mark** comparison, not a strict prior-day pure forecast

| Input | Recorded date rule or code evidence | Scientific treatment |
| --- | --- | --- |
| Option target `market_settlement` | `bayesian_asian_options/barchart_apo.py` maps Barchart `Time` to `trade_date`, `Latest` to `market_price`, with **no source publication timestamp** | Call it a vendor **end-of-day settlement proxy**; do not claim independent traded transaction. |
| Earlier option `sigma_q` | Produced by inverting Barchart `Latest` marks in `experiments/wti_apo_implied_volatility.py`, then filtered to dates earlier than target | **Date-ordered** but original vintage/publication-time **not externally verified**. |
| Target-date CL futures curve | `barchart_cl_curve_on_date` uses Barchart `Latest` on the **same valuation date**, exact-date match; `valuation_cl_curve.csv` records it | A target-day conditioning input; not a forecast that could have been made before the day's close. |
| Already observed CL fixings | `_split_fixing_dates` classifies **fixing_date <= valuation_date** as realized; pilot uses all **weekdays**, not a fully exchange-certified holiday and fixing calendar | Appropriate as explicitly specified **end-of-day** scenario; exact exchange fixing schedule and publication timing unverified. |
| Treasury discount rate | `treasury_curve_on_or_before` selects the latest **dated** par curve `<= valuation_date`, up to seven calendar days old; par yield is approximated as a zero yield | Correct date-order rule, but **same-day publication-time** and risk-free zero-curve interpretation unverified. |
| External LO IV | Earlier `reference_ts` by date, American LO CRR pricing, prior surface | Calendar-date precedes targets, but official settlement publication timestamps, original underlying and tree inputs remain open. |

### C. Evidence of later-retrieved **historical snapshots**, not provable live as-of archives — **BLOCKER**

The committed raw Barchart APO/CL sources have CSV columns `Time, Open, High, Low, Latest, Change, %Change, Volume, Open Int` and **no `published_at`, `received_at`, `snapshot_at`, `revision_id`, or native intraday exchange-status column**.

Concrete examples:
- `data/csv/oct2026/jaov6_10000c_price-history-09-12-2026.csv` is named as a **September 12 retrieval** but contains **September 10** option data. Its naming is consistent with retrospective retrieval; the precise file-creation/processing timestamp is not verified.
- `data/csv/CL/CLX26.csv` includes **September 16** rows; the sample `results/wti_apo_empirical/2026-09-10_202610/manifest.json` was generated on **September 16 UTC**, after the September 10 valuation date. The CL source manifest lists last observation **September 16**. This **does not prove leakage**, since the code selects the correct earlier dated rows, but confirms that calculation was **retrospective**, not a timestamped live on-September-10 trading forecast.
- The September 10 run manifest labels futures `Latest` as an **end-of-day proxy**, records a **same-day** Treasury par-yield curve, marks `git_dirty=true`, and notes approximate weekday fixing dates and par-yield discounting. Original source snapshots cannot be reconstructed from the final Git commit alone.
- Barchart's `Latest` historical snapshots may incorporate corrections and exchange settlement-model valuations; original source files alone cannot reveal whether numbers differed when first published at the target cutoff.
- The disclosed **CME AAO settlement model** has used Curran-based valuation since May 18, 2020. The strong IV fit to those model-generated marks may reflect an **algorithmic relationship**, not tradable superiority.

**Therefore:**
- **Certified:** internally chronological use of stored earlier IV marks, price arithmetic, matching and IV-smile calibration.
- **Not certified:** a genuine historical production information set `F_{t-}` reconstructed from first-publication archived vendor snapshots, price-mark independence, target-time quote tradability or a full CL contract calendar.
- **Required before submission of a strong fully out-of-sample/live-market claim:** authorized point-in-time vendor **publication timestamps or saved date-stamped snapshots** for APO source marks and CL/LO inputs, evidence about vendor revision policy, exchange settlement flag/type, plus the exact intended target cutoff and Treasury publication time; verify local original input hashes against their manifests. **Never invent timestamp fields** or mark this verified merely because a CSV has `Time` dates.

## 6. Claim changes required by this audit

**Permitted now:** “In a retrospectively assembled, chronologically date-ordered WTI APO settlement-proxy exercise, earlier option-derived IV yields much smaller conditional model-mark errors than the tested historical-return proxy. For 2,366 comparable contract-date observations, direct same-contract IV persistence outperforms the more elaborate prior-date fitted IV smile on pooled MAE. These findings depend on dated settlement proxies, current-date futures information, a maintained Curran pricing map and only 15 target valuation dates.”

**Not permitted:** “The model predicted live executable WTI Asian-option trades at 95.9% lower forecast error”; “all historical volatility methods fail”; “the IV improvement proves a variance risk premium”; “strict real-time as-of observations are proven”; “Bayesian modeling dominates naive market IV”.

**Editorial option if native point-in-time evidence cannot be obtained:** use this as a **retrospective same-day conditional settlement-mark reproduction exercise**, and make the larger Databento terminal-average mark analysis separately identified rather than claiming a true historical trade forecast. If REMEF's novelty standard requires stronger ex-ante/independent market validation, **do not prematurely submit** based on numbers alone.

## 7. Checklist and handoff

- [x] Recompute 2,381 prior-smile price-error rows, MAE, RMSE and bias.
- [x] Recompute 2,366 same-contract-IV carry price-error rows and compare on exact common support.
- [x] Re-estimate both saved earlier-IV ridge smiles from all 2,574 source-IV rows (170 groups, 4,762 predictions).
- [x] Check all source-IV dates precede target dates; same-contract prior IV values match source table exactly.
- [x] Check same-day source-IV target is not a predictor in the regression code/data reconstruction.
- [x] Recalculate dated and liquidity-stratified descriptive comparisons, including 15-date dependence.
- [x] Inspect original option, CL, Treasury, fixing and LO code and example archived market-source/run records for date availability and missing fields.
- [ ] Certify original **exchange publication-time** and **historical source-vintage** information from time-stamped permitted vendor/exchange records; GitHub histories only include **date** labels. **BLOCKER.**
- [ ] Verify original raw-file SHA256 and contractual redistribution permission; source content may already be visible in older public Git commits. **BLOCKER.**
- [ ] Independently replay original CL/option vendor raw prices, LO tree and exchange official settlement/transaction status; reconcile `git_dirty` code. **BLOCKER.**
- [ ] Execute `python -m scripts.audit_remef_forward_iv` on a full checkout and retain/push its JSON plus environment/run info. The independent arithmetic was already executed in this audit, but the new Python reproduction script is **not yet run**.

**Disposition:** **Numerical-IV and stored calendar-date audit COMPLETE/PASS**. **Market-publication timestamp / historically as-of audit cannot be fully closed with supplied committed fields; leave this editorial data-provenance gate OPEN rather than certifying nonexistent timestamps.** No manuscript submission authorized.
