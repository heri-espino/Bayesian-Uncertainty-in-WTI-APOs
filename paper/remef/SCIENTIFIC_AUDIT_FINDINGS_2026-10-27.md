# REMEF Paper A — scientific-audit findings

**Audited October 27, 2026, on the completed-results branch. Status: numerical checks substantially complete; scientific and editorial clearance STILL BLOCKED.** This report distinguishes independent recalculation from source-manifest corroboration and unresolved market-data checks. No new experiment, data purchase, price-file mutation, or GitHub Actions job was performed.

## Verified directly from contract-level rows

| Manuscript claim | Independent recomputation | Assessment |
| --- | --- | --- |
| October 2026 **expiry** sample | 310 options on 12 valuation dates, **August 25–September 10, 2026** | PASS. The manuscript should not imply October valuation dates |
| Posterior-integrated October RMSE | 0.5177412470 USD/bbl; signed bias -0.4064854680 | PASS, rounded paper RMSE 0.5177 |
| Posterior-mean plug-in October RMSE | 0.5183370736 USD/bbl; signed bias -0.4072303956 | PASS, rounded paper RMSE 0.5183 |
| Mean absolute PI–PM difference | 0.000745132275 USD/bbl | PASS, paper reports 0.000745 |
| Average 95% conditional posterior **model-price** interval width | 0.2732726840 USD/bbl | PASS, paper reports 0.2733; **NOT empirical settlement-price coverage** |
| Historical PI, main earlier dataset | 2,381 actual contract-date records on **15 dates**, MAE 2.6186993843, RMSE 3.4089906045 | PASS |
| First-nearby CL physical-volatility robustness on same 2,381 | MAE 2.6468078947, RMSE 3.4450875335 | PASS |
| LO external implied-volatility common-support sample | 253 date/contract rows on **10 dates**, LO prior IV MAE 0.1558843083, RMSE 0.2598941819 | PASS |
| Original historical PI on those same 253 | MAE 0.4463621973, RMSE 0.5561653970 | PASS |
| Prior AAO IV on those same 253 | MAE 0.1676320452, RMSE 0.2686030905 | PASS |

**Exact direct input files.** The October calculation used all 12 results/wti_apo_empirical/YYYY-MM-DD_202610/contract_pricing.csv files dated 2026-08-25, 26, 27, 28, 31; 2026-09-01, 02, 03, 04, 08, 09, 10. Individual date counts: 3, 27, 27, 27, 27, 27, 28, 28, 29, 29, 29, 29. The 2,381-row calculation used results/analysis/wti_first_nearby/pricing_holdout_comparison.csv (columns baseline_pi_error_yahoo and baseline_pi_error_first_nearby). The external LO calculation used all 253 rows of results/analysis/wti_external_vanilla_q_validation/surface_common_support_paired_errors.csv, separately recalculating historical PI, vanilla previous/expanding, and AAO previous/expanding errors.

These results independently agree with the reported source summary tables. This is a genuine row-to-result arithmetic check, **not** independent regeneration from vendor raw files. The old manuscript's 310-row example is for **October expiry**, with Aug–Sep *valuation dates*. This is a wording correction to make before submission.

## The 10-million synthetic experiment

Checked completed-run JSON: results/analysis/massive_mechanism_map/6e23d5aabc519982/mechanism_map_report.json and figure 1 metadata: figures/publication/ten_million/figure_manifest.json.

- Synthetic histories **10,000,000**, root seed **2468**, scenario summary rows **5,880**, 168 underlying scenario states.
- Maximum absolute observed PI–PM price difference **0.1565361744** (paper 0.1565).
- Highest within-cell 99th percentile **0.1273379489** (paper 0.1273).
- Figure 1 second-order mechanism correlation **0.9995456742** (paper ~0.9995).
- Distinct earlier experimental fingerprint 200169bc7780a11d covers only **175,000** histories; must not be conflated with the 10M run.

**Pass is for manuscript-to-run metadata consistency.** No CuPy/GPU rerun or full independent replay of all scenario-cell posterior operations occurred.

## Partially corroborated, NOT independently rederived

1. Earlier prior-day AAO implied-volatility **smile** MAE **0.1075458**, RMSE **0.1593563**, 2,381 observations on 15 dates: present in the committed forward_q_error_summary.csv and Results README, but independent aggregation of all 1.19MB forward_q_predictions.csv was unavailable via connected GitHub content response. This claim is **source-aggregate consistent**, not fully row-audited.
2. Earlier **same-contract** lagged IV sample with **2,366** observations and MAE **0.0992**: cited in manuscript and supplement; independent row-level reconstruction remains **OPEN**.
3. The LO tree's exact American early-exercise numerical settings and prior-date information cutoffs are described by run manifests and source; a complete raw-market-vintage replay has **NOT** been performed.
4. Sample-wide leave-one-contract-out calibration and prior-date smile timing are supported by code descriptions, not a comprehensive field-by-field historical input availability test.
5. Actual versus theoretical exchange settlement flags and positive trading volume are economically distinct. Mark replication is not necessarily an independent tradable-price prediction.

## Critical input-interpretation checks

**Old study and new studies must remain separate.** The original Barchart/LO design uses CL contract-date curves, first-nearby fixing logic, an approximate weekday calendar, Curran pricing, Yahoo or reconstructed first-nearby P returns, and Treasury par-yield discount proxies. It is not the same model as Databento Experiments 003–005, which use a terminal-average lognormal **reduced-form** approximation, same-day disjoint AAO parity anchors and previous-AAO-IV inputs. Do not replace the older manuscript's 15 independent valuation dates with the 189 newer dates without rewriting design and limitations.

**Original source risks:** Barchart CSV column Latest is called an end-of-day settlement **proxy**, not independently certified official exchange final marks. The representative original manifest results/wti_apo_empirical/2026-09-10_202610/manifest.json records approximate par-yield discounting, approximate weekday fixings, and git_dirty=true at original generation. All original outputs must be traced to a precise source configuration before publication-level reproducibility claims.

**Exchange observations:** CME clearing notice 20-198 changed AAO settlement valuation to Curran effective May 18, 2020. It is possible to reproduce exchange **model-generated** marks without matching independent transactions. The minimum standard AAO price increment is $0.01/bbl, much larger than the average 0.000745 PI–PM difference. This limits claims of direct tradeability and economic significance. Rules identify the payoff as 1,000 times the nonnegative difference between the month-average daily first-nearby CL settlement and strike, with last-business-day expiration; actual historical fixing/roll and publication timestamp must still be matched.

**External sources used for methodology reference (not raw price verification):**
- https://www.cmegroup.com/market-regulation/rule-filings/2021/6/21-201.pdf — 2021 CME chapter 341 AAO terms (PDF p. 72/printed 71).
- https://www.cmegroup.com/notices/clearing/2020/05/Chadv20-198.pdf — settlement model change.
- https://databento.com/docs/datasets/glbx-mdp3 — settlement flags, final/actual distinction, ts_ref and publication timing.

## Gate outcome

**Numerical checks CLOSED:**
- [x] Independent 310-row October-expiry PI/PM errors, absolute PI−PM difference and posterior model-price width.
- [x] Independent 2,381-row historical PI point-error arithmetic and first-nearby robustness.
- [x] Independent 253-row LO previous-day vs AAO previous-day vs historical PI common-support errors.
- [x] Completed 10M run metadata, extreme statistics and figure 1 correlation compared against manuscript.
- [x] Distinct new Databento reduced-form evidence and adverse 2026 uncertainty interval performance documented in separate research reports.

**Submission blockers OPEN:**
- [ ] Independent contract-level prior-AAO-smile 2,381-row and same-contract 2,366-row IV error recalculation.
- [ ] Independent input-time proof for all Barchart futures marks, CL fixings, Treasury dates and earlier LO/AAO implied volatilities; resolve after-publication archive revisions.
- [ ] True source-vendor original-file SHA256 check and redistributability, including previously public Git history.
- [ ] Independent market-quote/trade validation, theoretical versus actual settlement treatment, liquidity splits and small-sample date dependence, including only **15/10** clusters for key earlier results.
- [ ] Independently verify all scientific code snapshots/configuration, the git-dirty source run, numerical reproducibility and dependencies.
- [ ] Assess mathematical/economic novelty versus Curran, Bayesian options, Asian options, REMEF precedents, crude-oil implied-volatility work, and related empirical forecasting.
- [ ] Correct the October-expiry versus valuation-date wording and reconcile old versus new datasets in the final chosen manuscript.
- [ ] Journal Word/native-math layouts, blinded/author output, bilingual abstracts, citation format, complete data statement, legal/AI disclosures and signed submission forms (see existing PRESUBMISSION_AUDIT.md).

**Conclusion: AUDIT PARTIALLY COMPLETED, NOT CLEARED FOR REMEF SUBMISSION.** The most prominent old headline numbers now have independent output-level arithmetic traceability. Input vintage, rights and reproducibility risks cannot be honestly closed from GitHub aggregate artifacts alone.

For repeatable local evidence checks without provider calls, run:
    python -m scripts.audit_remef_science

Optional new aggregate JSON output (refuses overwrite):
    python -m scripts.audit_remef_science --write-json

This newly written Python audit runner has not yet been run in the author's full local checkout. The row-level recalculations reported above were performed directly against the saved repository CSVs independently of that runner.

**Related documents:** Scientific revision gate: SCIENTIFIC_REVISION_AND_SUBMISSION_GATE_2026-10-27.md; distinct Paper B CL feasibility: ../../research/JCM_CL_FUTURES_FEASIBILITY_AUDIT_2026-10-27.md; publication overlap: ../../docs/two_paper_publication_strategy_2026-10-27.md.
