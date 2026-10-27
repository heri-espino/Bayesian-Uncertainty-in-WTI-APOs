# REMEF manuscript evidence-to-claim map and completion status

**Date:** October 27, 2026. **Scope:** REMEF-specific Paper A scientific draft; does not alter the JFM/Wiley sections or new JCM Paper B project. This is a **research manuscript revision, not final submission clearance**.

## Current source structure

- Frontmatter: paper/remef/frontmatter.tex — bilingual title, objective/method/results/recommendation/limitation/originality/conclusion abstracts (148 English, 178 Spanish words), exactly five keywords and six JEL codes.
- Journal-specific introduction: paper/remef/introduction.tex — literature, economic motivation, three separated questions and explicit data-design distinctions.
- Journal-specific body: paper/remef/sections/02_posterior_pricing.tex through 06_conclusion.tex, including original one-factor/Curran Barchart/LO study and **explicitly separate** reduced-form Databento evidence.
- Word builder: paper/remef/build.py — now reads paper/remef/sections/ rather than the frozen paper/manuscript/sections_short/ copies.
- Required Word layout/native-equation adaptation: paper/remef/postprocess.py and tests/test_remef_build.py.
- Bibliography: original paper/manuscript/references.bib plus journal-specific paper/remef/references.bib, including CME Clearing Advisory 20-198.
- Scientific direct-output audit: paper/remef/SCIENTIFIC_AUDIT_FINDINGS_2026-10-27.md.
- Original journal/evidence blockers: paper/remef/PRESUBMISSION_AUDIT.md.

## Claim-evidence mapping

| Draft claim | Dataset / quantitative source | Evidence status | Critical qualifications |
| --- | --- | --- | --- |
| Ten-million histories; maximum absolute PI−PM 0.1565; scenario-level curvature correlation ~0.9995 | results/analysis/massive_mechanism_map/6e23d5aabc519982/mechanism_map_report.json; figures/publication/ten_million/figure_manifest.json | **Run manifest corroborated** by scientific audit; no independent GPU replay | Synthetic mechanism, NOT 10 million independent market observations or original novelty by itself |
| October-**expiry** 310 contract-dates on 12 **Aug–Sep** valuation dates; PI RMSE 0.5177, PM RMSE 0.5183, mean absolute PI−PM 0.000745; 95% posterior conditional MODEL price width 0.2733 | results/wti_apo_empirical/2026-08-25_202610/ through 2026-09-10_202610/ contract_pricing.csv | **Independently recomputed from saved contract rows** in scientific audit | Posterior model-price width is NOT future-market error coverage; original raw vendor timestamps still not independently audited |
| Original historical PI main forward-in-time panel, 2,381 rows/15 dates: MAE 2.6187, RMSE 3.4090 | results/analysis/wti_first_nearby/pricing_holdout_comparison.csv | **Independently row-recomputed** | Original Barchart/LO design, not comparable raw pooled cohort with Databento |
| Original earlier APO fitted smile on those 2,381: MAE 0.1075, RMSE 0.1594 | results/analysis/wti_extended_forward/forward_q_error_summary.csv | **Committed summary corroborated**; full row-level smile reaggregation OPEN | Current 15-date inference fragile; exact earlier market timestamps/mark definitions OPEN |
| Original same-contract earlier APO IV on 2,366: MAE ~0.0992 | Existing original forward-panel source reports | **Independent row-level recalculation OPEN** | Do not claim statistical superiority over fitted smile without paired inference |
| Original vanilla LO cross-instrument 253 targets / 10 dates: historical PI 0.4464; earlier LO IV 0.1559; earlier APO IV 0.1676 | results/analysis/wti_external_vanilla_q_validation/surface_common_support_paired_errors.csv | **Independently row-recomputed** | Vendor LO inputs not independently replayed from original raw records; 10 date clusters |
| New independent Databento 189 dates, 111,585 targets, 97,341 actual flagged: lagged AAO IV MAE 0.2184, historical proxy PI 0.8040, PM 0.8068 | results/analysis/wti_aao_databento_only/full_2023_2026/method_metrics.csv, experiment_manifest.json | **Committed aggregate verified; private LFS source not independently downloaded** | Terminal-average Black proxy using current-date OTHER-strike parity anchors; historical proxy uses parity-forward changes, not CL physical returns |
| New Databento near-ATM implied volatility 30.97% target / 30.88% lagged / Bayesian price-equivalent 26.68% | results/analysis/wti_aao_databento_only/volatility_gap_diagnostic/diagnostic_summary.json | **Committed group diagnostic verified** | Current-date implied volatility is strictly retrospective explanatory inversion, never model feature |
| New market-IV model, 2025–Sep 2026, 47,718 actual contract-dates / 88 dates: lagged-IV MAE 0.208924, Bayes market-IV PI 0.209830 | results/analysis/wti_aao_market_iv_bayes/experiment004/method_metrics_by_split.csv and paired_actual_month_block_ci.csv | **Committed full local experiment and aggregate paired intervals verified** | Same support; prior-date IV features only, contemporaneous OTHER-strike parity anchors; inspected holdout; monthly CI includes zero |
| Residual predictive uncertainty 89,696 actual targets/174 dates: Bayesian 90% mark coverage 86.43% in inspected holdout, early-2026 monthly coverage 59.0% Mar / 56.9% Apr | results/analysis/wti_aao_predictive_calibration/experiment005/summary_by_split.csv, summary_by_year.csv and daily_actual_scores.csv | **Committed experiment and descriptive monthly reaggregation** | Conditional settlement-PRICE ERROR intervals, not Bayesian parameter-conditional model-price width or Asian terminal payoff credible bands |
| CME switched AAO settlement valuation to Curran May 18, 2020 | CME Clearing Advisory 20-198, https://www.cmegroup.com/notices/clearing/2020/05/Chadv20-198.pdf | **Exchange primary source confirmed** | Exchange-settlement-mark replication differs from independent trade price validation |
| Dollar-per-barrel original PI−PM correction economically smaller than standard minimum tick | Original 0.000745, CME Chapter 341 minimum tick USD 0.01/bbl | **Arithmetic and documented contract spec** | Do not equate statistical price improvements with feasible trading profits |

**Numerical and source provenance:** The older direct-CSV checks belong to the 2026-10-27 scientific audit and are not claimed to be a complete rerun. The newer Databento figures are committed author-run results with separate audits, not the same modeling pipeline as the older figures. Every paper table caption must disclose its cohort/design.

## Required final cross-checks before submission

1. Recompute the original 2,381-row prior-AAO-IV smile and 2,366-row same-contract IV directly from archived contract-level predictions.
2. Confirm Barchart Latest data type against actual exchange settlements/trades, and the timing of **all** input curves, CL fixing histories, discount inputs, LO/AAO historical IV marks and corrections. Audit date calendar, market-open/close timestamp and admissible vintage by target price publication.
3. Verify legal rights over any vendor-sourced raw or derived values in a public repository, including historical publicly visible commits. Do not quote a right to redistribute merely from Git LFS tracking.
4. Review original git-dirty source experiment snapshots; rerun canonical code only if source inputs and user budget/time permit, with recorded manifest + fresh environment lock.
5. Inspect true liquidity, mark type, positive trade volume and open interest; show that the result is not purely settlement algorithm persistence.
6. Render DOCX **both blinded and author variants**, verify native editable math and tables, figures and captions, APA 7, no identifying reviewer metadata, all headers/footers, and the **<=25 page** REMEF limit. Verify signed forms and the originality statement.
7. Do not submit until author reviews and authorizes the final documents; do not call an unreviewed repository revision “accepted” or “submission-ready.”
8. New Paper B must use genuinely new CL fixing/curve and independent quote or hedge results; the existing Databento mark-comparison tables cannot become a second paper's purported novel core.

## Completed in this manuscript revision

- [x] Separate journal-specific sections from the original Wiley/JFM scientific sources.
- [x] Write coherent introduction, data design, results and conclusion acknowledging two non-equivalent empirical pipelines.
- [x] Include 2023–Sep2026 Databento evidence in clearly labeled standalone comparison.
- [x] Include negative Bayesian-IV incremental-value evidence and 2026 mark-error interval failure.
- [x] Correct original October-**expiry** vs October-valuation-date mistake.
- [x] Update bilingual abstracts (both <=180 words) and CME original exchange citations.
- [x] Adapt REMEF native Word build references, section mapping and source regression checks.
- [ ] Execute full repository pytest/build/Word visual and page-count verification on a complete checkout.
- [ ] Resolve remaining scientific provenance/vendor rights/author signed forms and submit only after explicit approval.
