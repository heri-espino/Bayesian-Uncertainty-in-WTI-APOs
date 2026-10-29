# JFM bounded oracle pilot — recovered execution and descriptive aggregation

**Status: DEVELOPMENT / PILOT ONLY — NOT CONFIRMATORY; NOT CLEARED FOR JFM CLAIMS.**

Source: [manual PCAG103A-15 run #40822904143](https://github.com/heri-espino/Bayesian-Uncertainty-in-WTI-APOs/actions/runs/40822904143), completed successfully on 2026-10-29 UTC. The run used commit `23baf6a287497de8773ef66d34158a6bb2c37565`, deterministic seed `20261103`, and published artifact `jfm-pilot-PCAG103A-15-23baf6a287497de8773ef66d34158a6bb2c37565-run-40822904143` (GitHub artifact ID `12874803517`; scheduled expiry 2026-11-28 UTC). The ZIP was downloaded and its three CSV files were independently verified against the SHA-256 hashes in `pilot_manifest.json`. **The original CSV/JSON files are in the run artifact, not yet versioned in the Git repository.** Preserve them in Git before the artifact expires.

## Fixed pilot design

- Two generating volatilities (20%, 50%), two historical sample sizes (21, 252), three strikes (95, 100, 105), and 20 historical draws per volatility/sample-size setting.
- **80 distinct simulated return histories**, reused across three strikes, therefore **240 correlated option-state rows**; there are not 240 independent historical replications.
- Three preselected absolute price tolerances: USD/bbl 0.001, 0.005, and 0.010 (720 decision rows).
- The fixed-parameter reference in this portion is the **Curran approximation at generating sigma**, not a true/high-precision Asian-option price.
- Separate stress test: six (sigma, strike) combinations at correlation weight rho in {1.0, 0.75, 0.5}, with 12,000 independent antithetic *pairs* per scenario. Four distinct futures contracts, two fixings per contract.

## Descriptive pricing and coverage results

| Quantity | Pilot aggregate |
| --- | ---: |
| Mean absolute PI–PM difference (USD/bbl) | 0.003690 |
| Median absolute PI–PM difference (USD/bbl) | 0.001034 |
| Maximum absolute PI–PM difference (USD/bbl) | 0.014320 |
| Mean absolute PM error versus known-sigma Curran reference (USD/bbl) | 0.301434 |
| Mean absolute PI error versus known-sigma Curran reference (USD/bbl) | 0.301135 |
| Mean width of nominal 95% posterior *model-price* intervals (USD/bbl) | 1.529393 |
| Known-sigma Curran reference inside posterior price interval | 225 / 240 = **93.75%** |

Breakdown by generating volatility and number of observations, 60 option-state rows per cell:

| Sigma | Historical n | Mean absolute PI–PM | PM MAE vs known-sigma Curran | Nominal 95% interval coverage | Mean interval width |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 0.20 | 21 | 0.008974 | 0.210425 | 95% | 1.241751 |
| 0.20 | 252 | 0.000718 | 0.085612 | 90% | 0.348745 |
| 0.50 | 21 | 0.004667 | 0.712257 | 95% | 3.541432 |
| 0.50 | 252 | 0.000400 | 0.197441 | 95% | 0.985645 |

The interval coverage above is a fixed-parameter *repeated-sample calibration check of the posterior model-price interval* against the known-sigma **Curran** reference. It is **not** coverage for traded settlement prices, predictive price intervals, or an independently verified exact-payoff reference. Only 20 independent history draws per (sigma, n) cell; three strikes reuse each history. Avoid naive binomial confidence intervals over all 240 rows.

## What “false reassurance” means in the pilot implementation

The current `pilot_decisions.csv` defines **false reassurance** narrowly as *the Taylor-estimated PI–PM gap being below tolerance while the actual computed PI–PM gap is above tolerance*. It **does not measure false reassurance about estimation error or misspecification**.

| Tolerance (USD/bbl) | Decision rows | Taylor says plug-in adequate | Taylor false reassurance about PI–PM gap | Unnecessary integration flagged |
| ---: | ---: | ---: | ---: | ---: |
| 0.001 | 240 | 115 | 0 | 0 |
| 0.005 | 240 | 163 | 0 | 3 |
| 0.010 | 240 | 198 | 0 | 1 |

For the *different*, substantive question “does a small PI–PM gap guarantee a small plug-in estimation error?” the answer is no in this pilot. At an identical price tolerance:

- USD/bbl 0.001: 115/115 cases with PI–PM gap ≤ tolerance have PM error > tolerance.
- USD/bbl 0.005: **160/166 = 96.39%** of cases with gap ≤ tolerance have PM error > tolerance.
- USD/bbl 0.010: **190/199 = 95.48%** of cases with gap ≤ tolerance have PM error > tolerance.

These are **exploratory, within-design proportions** with correlated strike reuse; they are not out-of-sample risk probabilities or evidence from independent market transactions. The extremely small tolerances make the contrast partly mechanical, and the numerical reference must be checked independently before interpreting these magnitudes.

## Correlation stress and numerical-resolution gate

Across the six (volatility, strike) cases, the paired change in simulated price relative to rho=1 averaged **−0.333401 USD/bbl** for rho=0.75 and **−0.692427 USD/bbl** for rho=0.50. The respective ranges were [−0.533813, −0.125619] and [−1.104611, −0.257945]. Paired-difference standard errors were reported per state in `pilot_correlation_mc.csv`.

The independent payoff Monte Carlo comparison at rho=1 is *not* yet a high-precision pricing validation. The six absolute differences between rho=1 MC and Curran at generating sigma averaged **0.021028 USD/bbl**, with maximum **0.079380 USD/bbl**. MC standard errors for these six controls were about 0.0118–0.0484 USD/bbl; largest standardized absolute difference was 1.781. **Absence of a statistically detectable discrepancy here is not proof of Curran accuracy below 0.001 USD/bbl**—the MC noise is far larger than the smallest pricing gap under discussion.

The correlation stress uses a stylized multi-futures Brownian dependence model. It does not estimate historical WTI futures correlations or infer a market hedging effect.

## Publication decisions and immediate next steps

1. **Archive all five original pilot files in Git** (three CSVs, manifest, NOTES) without relabeling the run as confirmatory. Preserve source SHA-256 and commit ID above.
2. Before claiming the pilot in the JFM paper, compare rho=1 Curran to an **independent, sufficiently precise** payoff reference and verify posterior quadrature convergence for the small differences discussed. Report unresolved precision as inconclusive.
3. Specify the distinction between (a) Taylor approximation decision errors and (b) *estimation/model* false reassurance in the final metric definitions. Select scenarios and tolerances **before** any confirmatory holdout run.
4. Only after the independent numerical gate, incorporate a concise table/paragraph into `paper/manuscript/sections_short/04_results.tex`. Preserve the existing 10-million-history results and 15-date market evidence; do not conflate this development pilot with those datasets.
5. Regenerate the four Wiley JFM figures using the **manual** `build-paper` workflow on `PCAG103A-15`, `asian-options`. The existing AwesomeFigures `af.paper(..., engine="xelatex", width="text", strict=True)` integration is committed, **but regenerated PGF/PDF outputs are not yet committed or visually proofed**. The workflow intentionally never auto-commits heavy artifacts.

This document records **observed data**, not new simulations, inferentially independent replications, journal clearance, or manuscript-ready findings.
