# Research checkpoint — 2026-09-29

## Status

The scientific core of the WTI APO paper is now complete enough to move from empirical validation to final paper integration and reproducibility freeze.

Issue #38, the contract-reconstructed historical first-nearby robustness, is complete in production. Its result does **not** weaken the paper's central empirical hierarchy.

Current manuscript:

> **When Does Posterior Integration Change Option Values? Evidence from WTI Average Price Options**

Target journal:

**Journal of Futures Markets**

## Main scientific conclusion

The project now supports two distinct statements.

First, posterior integration can matter when posterior dispersion and pricing curvature are jointly large:

[
C_{PI}-C_{PM}
approx
rac12 C^{Qprimeprime}(arsigma)
operatorname{Var}(sigmamid D).
]

The 175,000-history synthetic mechanism map reaches a maximum observed absolute PI--PM gap of **0.1384** and identifies the adverse states: short histories, high volatility, long remaining horizons, extreme moneyness, and little realized fixing.

Second, in the observed WTI APO sample, the largest established pricing difference is between the maintained long-window historical-volatility input and recent option-informed volatility inputs. That comparison is much larger than the PI--PM mean-price correction.

This should **not** be summarized as a pure physical-versus-risk-neutral volatility decomposition. The option-informed inputs also differ in recency, maturity dependence, strike dependence, and flexibility. The current evidence establishes that the option-informed advantage over the long-window historical benchmark:

1. appears in strict forward-in-time APO validation across seven expiries;
2. survives construction from independent prior-date standard WTI vanilla-option (LO) information;
3. is not an artifact of the Yahoo continuous/front-month return construction, because the contract-reconstructed first-nearby historical baseline is nearly unchanged.

A pre-specified recent-history historical-volatility suite is now the main referee-facing test of how much of the remaining advantage is attributable specifically to recency.

---

## Observed PI versus PM

October-2026 baseline:

- 310 eligible option-date observations;
- posterior-integrated RMSE: **0.5177**;
- posterior-mean plug-in RMSE: **0.5183**;
- six positive-volume contract-date observations:
  - PI RMSE **0.1864**;
  - PM RMSE **0.1869**.

High-precision pseudo-random Monte Carlo, randomized Sobol, and Curran conditioning resolve the approximately (10^{-3}) PI--PM gaps well below their magnitude.

Interpretation:

> In observed WTI states, posterior integration is a second-order point-price refinement, even though the synthetic mechanism map shows regimes where it becomes material.

---

## Strict forward APO-implied-Q result

Seven expiries, 2,381 exact holdouts.

Original Yahoo-`CL=F` physical baseline:

| Method | MAE | RMSE |
|---|---:|---:|
| Historical PI | 2.6187 | 3.4090 |
| Prior-date APO expanding smile | 0.1088 | 0.1725 |
| Prior-date APO previous-day smile | 0.1075 | 0.1594 |

The option-informed methods use only information strictly earlier than each target date.

The result appears across every admitted expiry from Sep-2026 through Sep-2028.

---

## Independent vanilla-WTI result

The external risk-neutral state is constructed from prior-date standard monthly WTI options (LO), not from APO prices.

Final LO IV inversion:

- 5,220 / 5,220 successful inversions;
- 13 reference dates;
- strikes 70--120;
- CLX6 and CLZ6;
- 5,214 actual settlements;
- 6 theoretical settlements.

Exact no-clipping common support:

- 253 / 280 matched contract-dates;
- 10 valuation dates;
- 90.4% of matched observations.

Original historical baseline versus option-informed states:

| Method | MAE | RMSE |
|---|---:|---:|
| Historical PI | 0.4464 | 0.5562 |
| External LO previous-day | 0.1559 | 0.2599 |
| External LO expanding | 0.1604 | 0.2858 |
| Prior-date APO previous-day | 0.1676 | 0.2686 |
| Prior-date APO expanding | 0.1612 | 0.2912 |

Paired valuation-date bootstrap with 100,000 resamples strongly separates either option-informed specification from historical volatility. LO and APO surfaces remain broadly comparable; do not claim universal LO superiority.

---

# Issue #38 — contract-reconstructed first-nearby physical volatility

## Construction

Historical first-nearby CL settlements were reconstructed from official final Databento GLBX.MDP3 CL statistics over the January-2024 to September-2026 inference window.

The acquisition used 33 monthly CL contracts.

Roll rule:

> On each trading date, select the earliest CL contract whose observed final-settlement last-trade date has not passed.

Data handling:

- 33 mapped contract switches;
- every return spanning a contract switch is excluded;
- 4 isolated mapped settlement gaps:
  - 2024-11-26;
  - 2025-01-09;
  - 2025-01-13;
  - 2025-08-01;
- missing settlements are **not imputed**;
- any one-day return that depends on a missing settlement is excluded.

Usable returns:

- reconstructed first-nearby: **632**;
- Yahoo `CL=F`: **676**.

After normalizing Yahoo's 04:00/05:00 timestamps to trading dates:

- paired usable return dates: **632**;
- return correlation: **0.99348**;
- mean absolute return difference: **0.000509**.

The earlier `paired_return_dates=0` report was a timestamp-normalization diagnostic bug, not a scientific discrepancy. The comparison code is corrected in the current paper-integration branch.

## Physical volatility comparison

Annualized realized volatility:

- reconstructed first-nearby: **0.41834**;
- Yahoo `CL=F`: **0.41670**.

Gaussian posterior:

| Source | Posterior mean sigma | Posterior SD | 2.5% | median | 97.5% |
|---|---:|---:|---:|---:|---:|
| First-nearby | 0.41824 | 0.01174 | 0.39611 | 0.41796 | 0.44234 |
| Yahoo `CL=F` | 0.41651 | 0.01124 | 0.39542 | 0.41640 | 0.43939 |

Mean-sigma difference:

**+0.00172**, or only **+0.41%** relative to Yahoo.

Thus the historical volatility level is not materially an artifact of Yahoo's continuous-contract construction.

## Identical-holdout pricing comparison

All 2,381 holdouts match exactly.

| Physical source | MAE | RMSE |
|---|---:|---:|
| Yahoo `CL=F` | 2.6187 | 3.4090 |
| Reconstructed first-nearby | 2.6468 | 3.4451 |

Changes from Yahoo to first-nearby:

- MAE: **+0.0281**;
- RMSE: **+0.0361**;
- RMSE ratio: **1.0106**.

The reconstructed baseline is, if anything, slightly worse overall. Near-dated 2026 expiries improve modestly, while longer maturities worsen modestly. The option-informed (Q) predictions are unchanged.

Therefore the contract-reconstruction exercise supports a narrower conclusion: the option-informed advantage over the **long-window historical baseline** is not a continuous-contract roll artifact.


## External LO comparison under reconstructed P

On the same 253 exact common-support observations:

| Method | MAE | RMSE |
|---|---:|---:|
| Reconstructed first-nearby historical PI | 0.4362 | 0.5466 |
| External LO previous-day | 0.1559 | 0.2599 |
| External LO expanding | 0.1604 | 0.2858 |
| Prior-date APO previous-day | 0.1676 | 0.2686 |
| Prior-date APO expanding | 0.1612 | 0.2912 |

External previous-day LO versus reconstructed historical PI:

- delta MAE: **-0.28036**;
- 95% cluster-bootstrap CI: **[-0.33294, -0.22426]**;
- delta RMSE: **-0.28672**;
- 95% CI: **[-0.33994, -0.24900]**;
- bootstrap probability of improvement: **1.0** for both metrics.

The independent external-(Q) conclusion is therefore unchanged.

---

# Data-source conventions

## Barchart

For the Barchart histories used by this project, `Latest` is the **CME settlement field**.

Do not describe it as:

- an intraday last trade;
- merely a settlement proxy;
- an unverified target requiring a new scientific validation experiment.

Preserve the raw field name for provenance.

## Databento

The scientific workflow was designed under the rule that proprietary raw Databento inputs remain local and that the repository versions query metadata, hashes, diagnostics, and derived results.

**Temporary retention decision as of 2026-09-29:** the current tree intentionally keeps LFS-tracked raw/external data, including `data/databento/**/raw/`, as a short-term continuity backup because the active experiment is being run on an external machine whose local storage may be wiped without notice.

Do **not** delete or untrack these data during normal research work, cleanup, branch maintenance, or manuscript integration unless the author explicitly authorizes the cleanup.

This is a temporary operational retention decision, not a claim that Git LFS grants redistribution rights. The final public/reproducibility artifact must still reconcile the repository contents with the applicable data licenses. The intended sequence is to preserve the backup through submission, then perform the raw-data/licensing cleanup after the paper has been sent and the scientific state is safely archived elsewhere.

---

# Milestone status

## M1 — Literature & positioning

Scientifically complete.

Archival literature-file cleanup remains non-blocking.

## M2 — Empirical validation

**Complete.**

Completed:

- #35 extended strict-forward APO validation;
- #36 independent vanilla-WTI LO validation;
- #38 contract-reconstructed historical first-nearby robustness.

#37 is documentation/provenance cleanup rather than a scientific blocker.

## M3 — Model robustness & paper integration

Current focus.

Required:

- integrate first-nearby robustness into the manuscript;
- final figures/tables integration (#40);
- final language consistency pass.

Optional:

- #39 richer commodity-volatility robustness, only if a specific unresolved referee-facing question remains.

Do not add richer models merely to accumulate experiments.

## M4 — Reproducibility freeze

Next after manuscript integration.

Required:

- preserve the temporary external-machine backup through submission unless the author explicitly changes this decision;
- after submission, resolve raw-data tracking/licensing consistency before the final archival/public snapshot;
- run structure checks and tests;
- compile and visually inspect the Wiley PDF;
- verify all manuscript numbers against versioned outputs;
- freeze exact code/data provenance;
- create final version tag.

## M5 — JFM submission

After M4:

- anonymized review manuscript / title page as required;
- corresponding-author metadata;
- acknowledgments;
- AI-use disclosure as required by the target journal/publisher;
- final data/code statement;
- supplement;
- cover letter;
- submission checklist.

---

# Current blocker hierarchy

There is no remaining **large** scientific experiment required by the evidence presently in the paper. One lightweight referee-requested robustness suite remains before the scientific freeze.

Immediate blockers:

1. run `python -m scripts.run_reviewer_robustness` on the external machine;
2. inspect and version the recent-history, posterior-RMS, prior-contract-IV carry, moment-matched LO transfer, CRR convergence, and LO-surface-shape summaries;
3. integrate only supported numerical conclusions into Results/Robustness;
4. recompile and visually inspect the Wiley PDF;
5. preserve the temporary raw/external-data backup through submission and defer licensing/tracking cleanup to the archival step;
6. reproducibility freeze and submission package.

The next default action is this targeted lightweight suite, **not** a richer stochastic-volatility model or another broad experiment grid.

---

# Current paper claim

> Bayesian posterior integration has a predictable, state-dependent mean-price effect governed by posterior dispersion and pricing curvature, while posterior model-price dispersion is a distinct quantity. In the observed WTI APO sample, the PI--PM mean-price correction is small. Recent option-informed volatility inputs provide a much larger strict-forward pricing improvement than the maintained long-window historical-volatility benchmark; that result survives both an independent standard-vanilla WTI construction and a contract-by-contract reconstruction of the historical first-nearby return series. The remaining referee-facing question is how much of that advantage survives pre-specified recent-history historical-volatility comparators.

Interpret option-implied volatilities as effective/model-equivalent states under the maintained pricing map, not unique structural diffusion coefficients.

Do not claim that LO globally dominates APO information.
