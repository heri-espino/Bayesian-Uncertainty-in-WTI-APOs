# Evidence ledger: what can be claimed, source and remaining proof

**Date:** 2026-10-26. **Rule:** "historically observed on user's VM" is *not* the same as "independently reproduced from data currently present in GitHub". Numerical values below preserve user-reported terminal output from the previous work and identify source files that survive. For current implementation status and future requirements see [master plan](PAPER_COMPLETION_MASTER_PLAN_2026-10-26.md).

## Evidence classes

- **A — directly in current remote Git:** source code, manuscript, old machine-readable outputs, graphs, tests and documentation. Can be inspected immediately, but code existence does not prove that a heavy experiment has executed.
- **B — user-run terminal evidence:** historical VM logs transcribed in project notes, but exact original raw files/results not currently in remote. Strong evidence of previous execution, NOT current reproducibility.
- **C — conceptual or research plan:** conjectures, desired experiments, expected output; must not be represented as completed results.
- **D — independently reproduced after re-acquisition:** **none for the 81-month extension as of this checkpoint**. Update this category only with commit/manifest hashes and successful rerun.

## I. Prior validated research and paper (class A)

| Claim | Value | Source / caveat |
| --- | --- | --- |
| Archived Barchart APO histories (original archive) | 11,179 contract/date marks across 213 contracts | `research/CHECKPOINT_2026-10-25_AAO_EXPANSION.md`; original `data/csv/`; verify any exact restoration independently. |
| Forward historical vs prior APO IV comparisons | 2,381 APO contract/date holdouts on **15 dates**, 7 expiries | `results/analysis/wti_extended_forward/README.md`; `paper/manuscript/sections_short/04_results.tex`; `paper/remef/PRESUBMISSION_AUDIT.md`. |
| Cross-instrument LO comparison | 253 APO rows on **10 dates** | `paper/manuscript/sections_short/04_results.tex`; compare only within LO-supported moneyness. |
| Historical PI on old 2,381-row main support | MAE 2.6187; RMSE 3.4090 USD/barrel | Prior concise manuscript table, old data. NOT 2020–26 AAO result. |
| Prior-date APO IV on same main support | MAE 0.1075; RMSE 0.1594 USD/barrel | Same old table. Check pricing-engine variants. |
| Rolling 63-return historical comparator | MAE 4.5201; RMSE 5.6465 USD/barrel | Same old table; not a winner in the old paper. |
| Horizon-matched Gaussian GARCH(1,1) old support | MAE 2.6730; RMSE 3.4441 USD/barrel | Same old table; ensure same fitting cutoff in extension. |
| Historical PI on old LO-supported sample | MAE 0.4464; RMSE 0.5562 USD/barrel | Prior short results, **253 rows/10 days**. |
| Previous-date LO-IV comparison on that sample | MAE 0.1559; RMSE 0.2599 USD/barrel | Same old sample, independent *source*, not independent sample dates. |
| Previous-day APO-IV comparison on LO-supported sample | MAE 0.1676; RMSE 0.2686 USD/barrel | Same old sample. |
| Gaussian posterior curvature/mechanism map | 175,000 synthetic datasets; curvature-correction correlation about 0.999545 | `results/analysis/massive_mechanism_map/200169bc7780a11d/mechanism_map_report.json`; `figures/publication/figure_manifest.json`; `paper/remef/PRESUBMISSION_AUDIT.md`. Correlation supports Taylor mechanism, not novelty theorem. |
| Ten-million-history computational figure family | Existing `figures/publication/ten_million/` | Figures and build notes survive; **do not confuse simulation paths/histories with empirical valuation days**. |
| Numerical calibration/robustness checks | Posterior RMS, CRR, Currran, randomized QMC, Student-t, LO surface, prior-date IV, liquidity, first-nearby | Historical scripts and outputs in `experiments/`, `results/analysis/`, `research/REVIEWER_REVISION_2026-09-29.md`; do not claim every check independently rerun in this documentation task. |

**Paper note:** Mixed execution engines matter. Canonical historical PI may use Monte Carlo posterior integration while some scalar volatility substitutions are priced by deterministic Curran. Label them transparently, and validate engine error separately.

## II. AAO metadata, acquisition and first 80 months (class B)

Historical author-run progression:
- A parent-symbol lookup reporting zero mappings could not establish absence. `metadata.get_record_count` and `metadata.get_cost` diagnosed AAO.OPT data even when a symbology snapshot mapping was zero; LO.OPT was used as a positive control.
- Candidate identifiers `AO.OPT` and `JAO.OPT` returned invalid-request errors in sampled probes; AAO.OPT yielded accessible statistics/definition metadata. Native JAO **Barchart filename prefixes are not assumed Databento parent symbols**.
- Download **first** quote: 81 months, ~USD 17.49357489; first transfer obtained 160 files/80 eligible months (not February 2021), quote USD 17.33487324. The missing February monthly definition quote initially failed with `504` despite positive record count.
- **2021-02 independently quoted and downloaded**: 2 chunks; quote USD 0.15870165. Combined 81 months/162 files; all SHA256 verified in local `scripts.audit_aao_manifests` output: `success:true`, `files_verified:162`, `sha256_verified:true`, `issues:[]`, `combined_quoted_usd:17.49357489`.
- The provider **actual charged USD amount is NOT independently verified**. All old 162 original binary files and 81-month SQLite were subsequently lost locally; GitHub remote contains only a tracked source-directory README and LFS config, not the original DBNs or generated SQLite.
- Initial 80-month inventory (before February backfill): 69,579,736 records; 13,284,087 settlement events; 5,843,770 final events, 3,989,698 actual-flagged, 1,854,072 theoretical-flagged; 1,682 raw-final reference dates. **Historical interim state only**, not final 81-month totals.

Potential local diagnostics source notes: `research/CHECKPOINT_2026-10-25_AAO_EXPANSION.md`, `research/AAO_INVENTORY_RESULTS_2026-10-25.md`, `research/DATABENTO_AAO_BULK_ACQUISITION.md`.

## III. All 81 months: inventory (class B, **not post-recovery validated**)

Author's final 81-month inventory terminal result:

| Measure | Reported value |
| --- | ---: |
| Source months | 81 |
| Total combined records | 70,154,064 |
| Settlement events | 13,412,045 |
| All raw final settlement events | 5,899,096 |
| Raw final actual-flagged events | 4,027,696 |
| Raw final theoretical-flagged events | 1,871,400 |
| Distinct raw-final CME reference dates | 1,701 |
| Positive cleared-volume events | 99,878 |
| Positive open-interest events | 5,781,953 |

These numbers count **events**, not validated pricing candidates, executable trades or distinct forward-eligible pricing dates. The source monthly window is January 2020 through September 2026 inclusive; a CME settlement event's reference date can be outside the file month.

## IV. Instrument, timestamp and settlement-state diagnostics (class B)

**February 2021 sample**:
- `experiments.wti_aao_identity_probe`: 140,790 definition events; 574,328 statistics events; 127,958 settlement events; 55,326 raw final events (37,998 actual, 17,328 theoretical); 19 raw final reference dates; mapped outright ID pairs in same month: 55,326.
- `wti_aao_settlement_gate`: among 127,958 settlement events, 30,520 strict same-publication-day as-of definition matches; 23,900 selected latest final active keys, but this is **not** an authoritative CME reference-date mapping.
- `wti_aao_mapping_comparison`: among 55,326 final events, reference-day definition match 264, publication-day match 30,496, preceding-publication-day match 12; **30,508** had at least one candidate mapping, 24,818 none. Alternative hypotheses, not validated union.
- `wti_aao_symbol_mapping`: 55,326/55,326 final events had mapped native symbol, definition match and tentative outright identity; 48,730 tentative final symbol/reference-date keys, 19 reference dates.
- `wti_aao_contract_day_candidates`: 48,730 selected final nonintraday *monthly* keys; 31,414 actual, 17,316 theoretical.

**June 2026 sample**:
- 206,136 definition events; 1,099,983 statistics events; 248,275 settlement events; 118,094 final events (53,377 actual, 64,717 theoretical); 23 raw final reference dates.
- Strict same-publication-day `wti_aao_settlement_gate`: 46,982 as-of matched settlement events and 32,258 selected latest final active keys; note 31,902 of selected were published on a different UTC date from their CME reference date. This diagnostic is not the final panel.
- Alternative snapshot mapping: reference-day 653, publication-day 46,673, preceding-publication-day 22,162; at least one candidate for 68,835 of 118,094 final events.
- Native symbol probe: 118,094/118,094 final events had mapped symbols, matching raw definition, unambiguous month-local outright identity; 101,397 tentative final native-symbol/reference keys, 23 reference dates.
- Month-local candidate normalizer: 101,397 selected final nonintraday keys; 43,067 actual-flagged and 58,330 theoretical-flagged.

The reason to use **native publisher/symbol and as-of definition** is that local numeric `instrument_id` is not a stable global contract key. These observations do not establish historical option premium scaling, update vintage or causal availability.

## V. Full 81-month cross-month reconciliation (class B)

| Quantity | Four-month smoke test | Historical full 81-month run |
| --- | ---: | ---: |
| Settlement events read | 711,542 | 13,412,045 |
| Distinct tentative native-symbol/reference keys | 276,325 | 5,157,894 |
| Tentative keys in multiple file months | 0 | 71,145 |
| Latest preliminary keys | 2,636 | 52,290 |
| Latest invalid price keys | 0 | 1 |
| Latest deleted/tied/intraday-final | 0/0/0 | 0/0/0 |
| **Selected final nonintraday candidates** | **273,689** | **5,105,603** |
| Selected actual-flagged | 156,945 | 3,299,087 |
| Selected theoretical-flagged | 116,744 | 1,806,516 |
| Unique selected reference dates | 85 | 1,700 |
| Publisher/symbol identities | 15,090 | 38,926 |
| Fingerprint conflicts across source months | 0 | 0 |
| Symbol groups not safe as outright | 20 | 296 |
| Latest-update source month != reference month | 300 | 190,064 |

Accounting checks: `5,157,894 = 52,290 + 1 + 5,105,603` and `5,105,603 = 3,299,087 + 1,806,516`. **71,145 cross-source-month repeats** are different from **190,064 source/reference-month mismatches**, and neither measures a confirmed count of settlements corrected by the exchange.

Annual selected candidate values from the historical `wti_aao_panel_quality --scan-final-dates`:

| CME reference year | Selected candidates | Reference days | Actual-flagged | Theoretical-flagged | Zero-price candidates |
| --- | ---: | ---: | ---: | ---: | ---: |
| 2019 | 4,706 | 1 | 4,614 | 92 | 92 |
| 2020 | 951,147 | 251 | 805,424 | 145,723 | 3,218 |
| 2021 | 678,637 | 253 | 439,655 | 238,982 | 3,316 |
| 2022 | 754,632 | 252 | 448,070 | 306,562 | 2,845 |
| 2023 | 689,570 | 251 | 412,639 | 276,931 | 582 |
| 2024 | 690,312 | 251 | 394,737 | 295,575 | 556 |
| 2025 | 707,400 | 252 | 418,150 | 289,250 | 1,666 |
| 2026 through Sep | 629,199 | 189 | 375,798 | 253,401 | 2,377 |
| **Total** | **5,105,603** | **1,700** | **3,299,087** | **1,806,516** | **14,652** |

**2019-12-31** is a selected CME reference date in source files collected beginning January 2020; **1,699 of 1,700 selected days fall in 2020–2026**. Do NOT conflate this with 1,699 viable held-out date-level tests.

**Lost final-event date**: raw inventory counted 1,701 reference dates, reconciled selected candidate set 1,700. Only `2024-01-26` had 2 raw final settlement events but **7,868 latest publisher/native-symbol/reference-day keys, all preliminary**, zero deleted, invalid, intraday, ambiguous or surviving final keys. Latest-state selection explains the mismatch at aggregate level, but an event-by-event history of the two original finals has not been reconstructed.

Price magnitudes were summarized in coarse bins, but **price units and contract multiplier are unverified**. Likewise actual-flagged settlements are not direct evidence of trade executions.

Primary historical notes: `research/AAO_FULL_HISTORY_RECONCILIATION_2026-10-26.md`, `research/AAO_PANEL_QUALITY_FINDINGS_2026-10-26.md`, `research/AAO_NATIVE_SYMBOL_CANDIDATE_PANEL_2026-10-26.md`.

## VI. Barchart cross-vendor reconciliation (current class C; **not completed**)

- Barchart APO histories and original pricing sample are tracked in `data/csv`, with known JAO filename. These were restored to the local sparse checkout and the target file produced `Test-Path=True`.
- Prior `wti_aao_panel_quality` returned `barchart_date_only_overlap.available:false, root_exists:false` only **before** the user restored `data/csv`. Its JSON persisted and was shown after a later audit errored for the **missing SQLite**.
- **No successful post-restoration Barchart-date overlap run exists**. No verified same-contract/maturity/strike/call-put/data-time match count or Databento-Barchart option price comparison exists. **Do not claim agreement or disagreement between providers.**
- Existing Barchart/LO original paper results remain valid only for the earlier sample/vintage and maintained model. After reacquisition do an overlap funnel and reproduce previous Barchart metrics on exact matched contracts before extrapolating findings to the new years.

## VII. Evidence and research deliverables that do not yet exist

As of the remote-tree inspection at this checkpoint:
- No replacement 162 Databento AAO source DBNs in GitHub's `data/databento/wti_aao_bulk/raw/`, no rebuilt 81-month SQLite in its `derived_private/`, and no `results/analysis/wti_aao_history_feasibility/` replacement acquisition manifest. **PR #109 configures LFS and tools; it does not upload this data.**
- No accepted strike/expiry/call-put publisher-native-symbol contract match between Barchart and Databento.
- No validated USD/barrel tick/display factor and multiplier cross-provider comparison.
- No complete reconstructed 2020–2026 strictly forward-eligible CL schedule, rate curve, historical/LO/APO IV panel.
- No approved date-block sample split, new market model-comparison MAE/RMSE/uncertainty for AAO 2020–2026, or new pricing-performance figures.
- No finished new JCM paper or author-approved submission.

**Label these as missing/unverified in future reports.** An absent source artifact cannot be inferred from filename/path in a historical handoff note. A future agent must add the exact new file path/commit/sha and results to this ledger after each milestone.
