# JCM Paper B — independent CL futures-data feasibility audit

**Inspection date:** 2026-10-27. **Status:** metadata/committed-result audit performed; independent structural pricing experiment **NOT yet feasible at full 2020–2026 coverage**. No provider queries, vendor purchases, raw source export, source modification, pricing backtest or hedge simulations occurred. Distinct Paper A REMEF evidence is preserved.

## 1. Main discovery: underlying CL data DOES already exist

The earlier Paper B initial protocol correctly identified missing full-period inputs but underestimated the amount of existing first-nearby CL source material. **Do not claim there are no CL fixings anywhere in the repo.**

| Asset and precise repository location | Evidence seen | Coverage / limits | Gate |
| --- | --- | --- | --- |
| AAO option definitions/statistics, data/databento/wti_aao_bulk/raw | 81 monthly windows × 2 schemas = **162 Git LFS DBN source files** (Jan 2020–Sep 2026), plus provisional settlement SQLite and source reconcilers | **AAO option market** metadata/statistics, not CL outright futures fixings, CL forward curve or bid/ask trades | Present only for option-side histories |
| Previously acquired CL outright statistics, data/databento/wti_first_nearby/raw/cl_statistics_2024-01-01_2026-09-23.csv | **Tracked via Git LFS**, expected payload **311,855,991 bytes**. Manifest declares **2,223,975 raw rows** over **33 explicitly requested CL contracts** for the 2024-01-01 to 2026-09-23 request range | Not yet a verified full multi-tenor daily forward curve; underlying **binary LFS payload not independently downloaded in this remote inspection**; critically, see SHA mismatch below | **Partly present; integrity review required** |
| First-nearby CL reconstruction, results/analysis/wti_first_nearby/first_nearby_reconstruction_raw.csv | **673 date rows**, earliest **2024-01-02**, latest **2026-09-10**; **632 usable roll-clean returns**, **four missing CL settlements** | Verified date/row inventory and historical return robustness for old Paper A; does not create CL fixing paths for 2020–2023 or the entire term structure at every earlier AAO date | **Pass as pre-existing partial reconstruction, not full Paper B** |
| CL history audit, results/analysis/wti_first_nearby/reconstruction_report.json | Official **final nonintraday** CL settlement selection stated; 33 roll switches, 4 missing settlements, Yahoo CL=F comparator | Reported missing dates **2024-11-26, 2025-01-09, 2025-01-13, 2025-08-01**. Excludes roll-boundary changes and returns spanning missing days | Existing report checked, raw-source replay pending |
| Small Barchart futures strip, data/csv/CL/*.csv | **14 CL outright contract files** and contract_expiries.csv | One CLV26 file **49** dated rows, **2026-07-09 to 2026-09-16**; most other files **16–17 rows**, **2026-08-21/25 to 2026-09-15/16**. No observations in these files before 2026 | **Narrow 2026 futures curve subset only** |
| U.S. Treasury rates, data/rates/treasury | README and versioned treasury_par_yields_2026.csv | Only **2026** Treasury par-yield file confirmed in tracked tree; README describes earlier local year files but no corresponding 2024/2025 tracked CSV on the examined branch. Par yields treated as a zero-rate proxy, not a bootstrapped curve | **Incomplete historical discount input** |
| LO WTI vanilla options, data/databento/wti_external_q/raw | Private LFS inputs for late August–early Sep 2026 options and underlying CL; external IV results for original 253-row comparison | Useful cross-instrument calibration subset for **old Paper A**; not proven to contain independently executable 2020–2026 AAO quotes/trades | **Narrow cross-instrument source, not independent option execution panel** |
| Yahoo CL=F, data/wti_yahoo/ | Versioned first-nearby comparison 2024-01-02–2026-09-10 | A continuous/front-month proxy with a different roll convention; useful diagnostics, not a substitute for exact exchange fixing contract series | Comparator only |

**Evidence source:** existing repository tree, each of the 14 source CL CSVs, data/csv/CL/README.md, results/analysis/wti_first_nearby/acquisition_manifest.json, reconstruction_report.json and reconstruction_raw.csv, plus data/rates/treasury/README.md. Numbers **33 contracts and 2,223,975 raw rows** are attributed to the acquisition manifest, **not independently counted in the 311MB LFS binary**. The 673 reconstructed row/date count and 14 individual CL CSV date coverage were independently counted from accessible text files.

## 2. Critical integrity discrepancy — must reconcile before reuse

The *same nominal raw Databento CL statistics path* has two different SHA256 identifiers:

- Git LFS pointer for data/databento/wti_first_nearby/raw/cl_statistics_2024-01-01_2026-09-23.csv: **oid sha256 bbc5356c7fc5e41b898bdf316cc3dcc8e918e3b0d8be351fbbabfa3dff7c3602**, LFS declared payload **311,855,991 bytes**.
- results/analysis/wti_first_nearby/acquisition_manifest.json declares a **raw-file SHA256 f52ec758ace7bb7f924c69009e686bfdb09196cdbfdb09e1b505822626e57204** for that same nominal path.

The source acquisition code (experiments/wti_databento_first_nearby.py, _sha256) explicitly hashes file bytes with SHA256. A Git LFS oid likewise identifies bytes by SHA256. Thus, **if these records refer to precisely the same version of the same file, the digests should match**. They do not. This is **NOT evidence of malicious alteration, a particular source being corrupt, or a proven pricing error**: a later rewrite/re-encoding, alternate version, stale manifest, source identity drift or other benign explanation is possible. It is a **hard reproducibility gate** until checked.

**Required local verification, no purchases:**

1. Materialize the real CL file in your existing authorized private checkout (git lfs pull if needed; avoid sparse checkout modifications).
2. Compute its byte SHA256 and compare to BOTH strings. A local result matching the LFS oid but not the acquisition manifest indicates the committed file version differs from the version manifest describes; determine when/why, and whether that version was used to construct the 673-row series. If neither matches, inspect local status and LFS restoration without destructive reset.
3. Verify source header, row count, **final vs preliminary**, stat_type, actual/theoretical flags where available, ts_event, ts_ref, symbol and 33-contract identity; verify the 4 missing dates and rule for selecting first-nearby expiry.
4. Rebuild selected 673-day first-nearby reconstruction read-only on a **new output path**, compare its SHA or row-level priced aggregate statistics to the stored result. Keep an explicit versioned discrepancy report.
5. Do NOT repurchase or overwrite the source in response to a hash discrepancy without author's permission.

A safe metadata-only preflight has been added as scripts/audit_jcm_cl_feasibility.py. It can optionally calculate the SHA256 of the large raw source when authorized locally; it never makes vendor calls. The code is committed but **not executed on the 311MB local LFS file in this remote session**.

## 3. Existing structural ingredients versus missing economics

**Some path-dependent modeling already exists in Paper A's older Barchart/LO study.** Its source code uses current-date futures curves, realized first-nearby fixings, an explicit expiry table and a Curran approximation; it also reconstructed first-nearby physical returns using official CL settlements for a historical P-volatility sensitivity. **A new JCM study cannot legitimately claim novelty simply from adding these already-implemented components.**

Paper B must materially extend this into a different economic question, with documented full-month exact fixing calendar, genuine multi-tenor dated futures curves, defensible risk-free discounting, true independent AAO trade/bid–ask targets if available, and possibly hedge P&L/turnover/risks after costs. Model improvements alone without source-timing and observable economic outcomes are unlikely to solve the journal-quality issue.

**Calendar/product rules, externally checked:** CME Chapter 341 AAO is a cash-settled European average-price put/call on the **calendar-month daily first-nearby NYMEX CL settlements**; contract payout multiplier **1,000 barrels**; standard quoted tick **$0.01/barrel**; expires **last business day of option month**. This specifies the high-level payoff, not the full historical business-day holiday/roll/reference-timestamp mapping. Source (2021 rules revision): https://www.cmegroup.com/market-regulation/rule-filings/2021/6/21-201.pdf (PDF p. 72, printed 71).

**Timestamps:** Databento normalizes CME daily settlement flags and date via ts_ref while publication messages may occur later and may be revised. Final vs preliminary is determined by flag 1; actual vs theoretical by flag 2. A latest-end-of-archive "final" mark may not have been known at the reference date used for an ex-ante hedge. Source: https://databento.com/docs/datasets/glbx-mdp3 . Therefore reconstructed records must preserve BOTH event publication and trading reference dates and only use a price after it was actually published.

**Independent trade quote audit:** Nothing in the presently archived **AAO definition/statistics** source manifests proves availability of AAO bid/ask order book or actual traded price points across 2020–2026. An actual-flagged settlement is not an executed trade; original Barchart "Latest" is a settlement proxy. A strictly independent market-price or executable hedging test is still a major feasibility blocker.

## 4. Chronological feasibility table

| Evaluation period | AAO option definitions/statistics | Verified CL first-nearby daily series | Verified full CL futures curve each valuation date | Independent AAO quotes/trades |
| --- | --- | --- | --- | --- |
| 2020–2023 | Option DBN LFS paths present | **NO:** available reconstructed CL source begins 2024 | **NO evidence** | **NO evidence** |
| Jan 2024–June 2026 | Option DBN paths present | **PARTIAL:** reconstructed 2024–Sep2026 history with 4 missing dates; LFS/manifest SHA discrepancy | **NOT VERIFIED**; raw CL file includes multiple contracts but completeness/timing not checked | **NO evidence** |
| July–Sep 2026 | Option DBNs present | **PARTIAL** reconstructed series until Sep10, plus Barchart subset through Sep16 | **NARROW** 14-contract strip at some Aug–Sep dates, not full cross-date history | **NO evidence** |
| After Sep 2026 | No post-Sep AAO source evidenced | No source verified | No source verified | No source verified |

This matrix is **not an instruction to purchase new data**. First audit already paid bytes and available local archives. A new data-cost estimate is permitted only as a separate quote-only step after discovering genuine gaps and must not be automatically followed by a purchase.

## 5. Recommended safe next sequence

1. **Reconcile CL LFS SHA mismatch first**. This controls whether the prior 673-day physical-return reconstruction can be trusted/reproduced from the current Git LFS source.
2. Run metadata-only scanner and optional SHA verification **locally** after confirming the full source is materialized: python -m scripts.audit_jcm_cl_feasibility --verify-large-raw-sha256 --write-json . The report contains aggregate paths/counts and no raw prices; commit its JSON to the private research branch after review.
3. Audit dated CL contract-by-date source coverage and timestamp availability without buying more data. Pay particular attention to the **historical forward curve**, not merely one first-nearby path.
4. Verify 2020–2023 missing CL source coverage before promising an 81-month structural study; possible smaller 2024–26 exploratory structural pilot if raw integrity and curve coverage pass.
5. Examine available AAO order-book/quote/trade access **without purchases** first. If no independent market prices can be obtained, explicitly narrow the research question to exchange settlement pricing and demonstrate other meaningful economic novelty (possibly controlled payoff/fixing error attribution).
6. Only then implement a NEW Paper B structural Monte Carlo/Curran benchmark and hedging experiment, with documented, genuinely distinct primary results, baselines, new predeclared evaluation and publication-overlap ledger. Do not silently reuse the REMEF 310/2,381/253 claim sets or the reduced-form Databento 189-date sample as independent new findings.

**Status: PRELIMINARY FEASIBILITY PASSED FOR A PARTIAL CL RECONSTRUCTION, FULL JCM STRUCTURAL EMPIRICAL FEASIBILITY OPEN.** No new hedge/backtest outcome or additional vendor bill has been invented.

See the separate [Paper B structural protocol](STRUCTURAL_WTI_AAO_PAPER_FEASIBILITY_PLAN_2026-10-27.md), the [REMEF arithmetic audit](../paper/remef/SCIENTIFIC_AUDIT_FINDINGS_2026-10-27.md), and the [publication-overlap ledger](../docs/two_paper_publication_strategy_2026-10-27.md).
