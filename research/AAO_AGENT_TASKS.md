# Agent execution plan — WTI APO 2020–2026 longitudinal study

## Latest transfer state: February recovered, no new purchases (2026-10-25)

The author ran a February-only `AAO.OPT` **free metadata quote** followed by an **explicit billable two-file backfill**, both successfully: `eligible_months=1`, **USD 0.15870165 quoted**, `downloaded_chunks=2`. It used `--max-budget-usd 1 --confirm-budget-usd 1` and `--report-dir results/analysis/wti_aao_history_feasibility/bulk_feb2021`. Added to the prior 160 chunks / USD 17.33487324 quote, the acquisition has **162 files over 81/81 months, total USD 17.49357489 quoted**; actual billing remains unverified.

**The older “February missing” and “retry February” passages below document past states only. Do not execute a quote or paid recovery again.** Keep separate ledgers (`bulk/` for the original 160, `bulk_feb2021/` for the two new ones). On the VM rerun **only** `python -m experiments.wti_databento_aao_inventory --all` (offline), and reconcile SHA256/size for all 162 files. The previous counts of 80 months, 1,682 final reference dates and 5,843,770 final settlement *events* were obtained *before* the backfill, not after. Contract mapping/uniqueness, source comparisons, strict lagged-IV eligibility and forward-test research remain open. No additional purchases or manuscript claims authorized.


Read `AGENTS.md`, `research/AI_HANDOFF.md`, `research/CHECKPOINT_2026-10-25_AAO_EXPANSION.md`, `docs/architecture.md`, `docs/agent_guide.md` and `research/DATABENTO_AAO_EXPANSION_PLAN.md` first. **No Databento charge or scientific result is authorized by this task list.**

## Latest VM evidence — 2026-10-25 (inventory already executed)

The author ran both the small sample and **all-month** offline inventory successfully:
**80 months processed, zero decode exceptions**, `AAO` asset in the monthly definition reports,
**1,682 distinct final settlement reference dates** and **5,843,770 final settlement events**
(3,989,698 flagged actual; 1,854,072 flagged theoretical). The downloaded month
**2021-02** is missing; reason not yet established. See
`research/AAO_INVENTORY_RESULTS_2026-10-25.md` for complete counts.

**Agent A is partially done, NOT scientifically closed.** Skip unnecessary reruns.
Finish manifest SHA256 integrity, actual outright definition/instrument mapping,
strategy-leg filtering and unique contract/date deduplication. Do not mistake the
1,682 reference dates for eligible model test dates. Agents B–E still await
verified data-model joins and forward eligibility.

## February 2021 recovery diagnosis — 2026-10-25

The author's original bulk metadata plan confirms **positive** February
2021 record counts: `definition=140790`, `statistics=574328`. The
`definition` **price estimate** (not the count) failed with a remote
HTTP **504 gateway timeout**, whereas `statistics` quoted
USD `0.042790770531`. This was a metadata outage, **not absent
market coverage**. The one-month total cost remains unknown.

Use a **USD 1 separate one-month budget** (USD 0.80 quote-based planning
threshold), not another USD 40 authorization. Next action is only the
targeted **free quote** (see
`research/AAO_INVENTORY_RESULTS_2026-10-25.md`). Use the separate
`--report-dir results/analysis/wti_aao_history_feasibility/bulk_feb2021`
to avoid overwriting the original acquisition manifest. Do not rerun
the paid 80-month acquisition and do not assume that February is
already downloaded. If backfilled, its separate acquisition ledger
must be reconciled with the original 160 file hashes.

## Implemented post-acquisition tools — stage gates

Read `research/AAO_81_MONTH_EXECUTION_PLAN.md`. The repo includes a
fail-closed two-ledger offline SHA256 validator
(`python -m scripts.audit_aao_manifests`), a complete-inventory-only
diagnostic coverage-figure generator
(`python -m scripts.plot_aao_history_coverage`), and a separate manual
Elsevier CAS manuscript source in `paper/jcm/` with
`python paper/jcm/build.py --check`.

These tools **do not constitute** a cleaned 81-month contract/day panel,
new Bayesian pricing experiments, fresh model-comparison figures or
an approved Journal of Commodity Markets submission. Those deliverables
remain explicitly gated on file hashes, source normalization, Barchart
agreement, exact CL fixings and lagged information, frozen dates and
out-of-sample model results. Do not regenerate old model performance
figures as if their data came from the 81-month history.

## Completed local SHA256 + identity checks; newest gate (2026-10-25)

Confirmed by user VM console: **162/162 verified SHA256 files**,
**81/81 months**, and a successful 81-month diagnostic event coverage
figure. For 2021-02: 55,326 final settlement events, 48,730 tentative
ID/date keys, zero missing same-month outright ID joins. For 2026-06:
118,094 final events, 101,397 tentative ID/date keys, again zero
missing same-month outright joins. **These are not stable contract-date
prices or forward-validation dates.**

Use the new strictly offline
`experiments/wti_aao_settlement_gate.py` on `2021-02` and `2026-06`
before broader normalization. It applies a conservative *as-of same
publication UTC day* definition match and last-update check and reports
only aggregate counts. **This is a diagnostic gate**, not final
multi-month contract identity or market validation. Read
`research/AAO_POST_DOWNLOAD_VALIDATION_2026-10-25.md`.
No fees, API requests, inference, large figures or paper rewriting.

## 81-month final inventory and settlement timestamp anomaly

The completed offline inventory contains **1,701 unique final settlement
reference dates**, **5,899,096 final settlement statistic events** (4,027,696
actual-flagged; 1,871,400 theoretical-flagged). These numbers supersede the
old 80-month aggregate figures but do **not** establish eligible forward
valuation dates or unique contract prices. Hash integrity of all 162
files has passed.

The conservative same-UTC-publication-day **as-of** definition check
missed 97,438/127,958 (76.1%) February 2021 settlement events and
201,293/248,275 (81.1%) June 2026 events. In the limited matched subset,
23,660/23,900 February and 31,902/32,258 June selected final ID/date
keys had a different CME `ts_ref` date from the publication UTC date.
The rule is too restrictive to construct a research sample; **do not**
discard unmatched events as missing prices.

Read `research/AAO_81_MONTH_SETTLEMENT_MAPPING_FINDINGS.md`.
New synthetic-tested, strictly offline
`experiments/wti_aao_mapping_comparison.py` compares day-level
reference, publication and previous-publication snapshot mapping,
reports mismatches, and rejects ambiguous instrument-ID fingerprints.
This is **only a diagnostic**, not permission to merge all candidate
matches. Next agent must validate a stable outright contract master,
CME trading sessions and revision history before pricing experiments.

## Latest result: daily snapshot matching is insufficient

User-run `experiments.wti_aao_mapping_comparison` matched at least
one candidate definition for **30,508 / 55,326 (55.1%)** February 2021
final settlement events and **68,835 / 118,094 (58.3%)** June 2026 events.
No alternate-identity conflicts were found among these matches, but
the remaining records are not verified absent or invalid.

**Next no-charge task:** run
`python -m experiments.wti_aao_symbol_mapping --months 2021-02 2026-06`
and inspect in-file mapped `statistics.symbol` against publisher-scoped
`definition.raw_symbol` and full unambiguous contract fingerprints.
Read `research/AAO_SYMBOL_MAPPING_NEXT_GATE_2026-10-25.md`. This audit
has no licensed row-level output. Resolve symbol reuse and final update
chronology before pricing any real option or updating CAS results.

## Symbol identity solved in two sampled months: normalize updates next

The author confirmed **55,326/55,326** February 2021 and
**118,094/118,094** June 2026 final settlement events have native
`statistics.symbol` mapping to unambiguous `AAO` C/P contract
definitions by publisher+raw symbol, with no within-month
fingerprint conflicts. Tentative unique symbol/reference-day pairs:
**48,730** (February) and **101,397** (June). This is stronger than
the low-coverage daily numeric ID joins but does not validate a global
multiyear pricing sample.

New source `experiments/wti_aao_contract_day_candidates.py` and
synthetic tests implement **per-file-month**, correction-aware latest
settlement filtering with exchange add/delete and final/actual/intraday
flags; aggregate-only reports are the default, with private licensed
row output opt-in and gitignored. See
`research/AAO_NATIVE_SYMBOL_CANDIDATE_PANEL_2026-10-26.md`.
Run two months first, **then** handle late cross-month amendments and
symbol reuse. New PI/PM empirical results, price-performance plots and
Elsevier CAS paper rewrites are *not yet validated*.

## Coordinating invariants

- PR #95 was merged with the quote-first downloader and offline inventory; all 160 author-reported DBN files live **only on the author's Windows VM**, not on GitHub. Do not use GitHub-hosted CI to access those raw files. Do not request the API key, paste it into a chat, or commit secrets or licensed data.
- The previous 2026 Barchart-based paper and its numerical results are the baseline. Preserve `paper/manuscript/`, `paper/remef/`, `results/analysis/wti_extended_forward/`, the ten-million synthetic study, existing contracts/expiry tables, and previous code paths. New extended-history outputs must be **separately namespaced**.
- Repository's reusable scientific code belongs under `bayesian_asian_options/src/bayesian_asian_options/`, tests in `tests/`, public interface in `docs/api/index.md`, local orchestration under `experiments/`; never introduce a second canonical pricing engine.
- One narrowly scoped agent branch/PR per workstream from freshly fetched `main`. Do not simultaneously modify shared manuscripts, `AGENTS.md`, or the same derived output; do not merge unresolved PRs or auto-commit heavy results. Light automatic CI is allowed, heavy tasks manual-only via local execution or `workflow_dispatch` and `upload-artifact@v4` (30-day default retention, never automatic Git commits).
- Scientific boundaries: P/Q separation; same-day market option prices must not be used to fit the same-day IV input; market marks may be theoretical; use correct CL fixing schedules, true contract expiries, dated discounting, and separate positive-volume-*date* from positive-volume-*contract* samples.
- Each PR contains reproducible commands, bounded fixture tests, provenance, caveats, negative-case results, independent eligibility counts, and exactly scoped acceptance criteria. Never report synthetic fixture numbers as market observations.

## Prioritized, separable agent workstreams

### A. Local DBN integrity and identity (**first**)

**Input:** `data/databento/wti_aao_bulk/raw/`, bulk quote plan and acquisition manifest on the VM. **Output:** local integrity report plus *shareable aggregates only* under `results/analysis/wti_aao_history_feasibility/inventory/`.

- The offline sample and full inventory have already run successfully. Re-run only for code/schema changes or to reproduce the local report. Proceed with SHA256, definition joins and deduplicated settlement analysis.
- Compare 160 expected SHA256s/sizes, identify 80 eligible and the one excluded month, and audit degraded-feed warnings.
- Inspect whether `definition` records have the expected AAO asset/product and outright `C`/`P` classes, realistic strikes, expiry and CL underlying; exclude complex strategies and duplicated leg-definition snapshots. Verify the mapped symbol/instrument IDs in `statistics`. **Warning:** `stat_type` can be an enum rather than a bare integer in `to_df`; inspect the actual DataFrame schema before classifying flags.
- Count final and theoretical settlement *events* and unique `ts_ref` days; do not equate event counts with unique option contract/day or independent evaluations.
- Preserve all rows locally; derive only aggregate reports permitted under Databento terms. Record data gaps/ambiguous fields rather than filling them.

**Done when:** audited file inventory, schema interpretation, product-identity evidence and a reproducible date-coverage summary exist. No pricing claims.

### B. Settlement normalization and source reconciliation

**Depends on A.** Implement a tested ingest adapter to link dated definitions and statistics via stable contract keys, respecting symbol rollovers/revisions, `ts_ref` trading date, publish/receive timing, `stat_flags`, preliminary/final corrections, and exchange holidays. Validate actual/theoretical flags against Databento's CME documentation; do not treat `stat_flags & 2` as evidence of an executed trade.

- Produce a deduplicated unique `date × contract × statistic` fact table and a flag-aware matched Barchart-vs-Databento reconciliation table.
- Check unit conventions/contract multipliers, expiry, option exercise style and Barchart `Latest` being CME settlement.
- Report missing/price-discrepant/zero-activity cases; label anomalies by source and calendar.

**Done when:** same-instrument/date matches and mismatches are traceable; no forced or invented settlements.

### C. Expanded eligible-date/market-input audit

**Depends on A and B.** Explain old 11,179 → 2,381 → 15 date attrition, and build the new forward-sample funnel *without selecting on desirable results*. Verify the exact CL calendar-month first-nearby fixings, ex-ante underlying curve, true CL expiry schedule, date-specific discounting, and distinct windows for historical P returns versus independent Q volatility.

- First run `python -m experiments.wti_aao_existing_attrition` on the retained old panel.
- Build full/new sample reports: distinct market dates, dates with APO settlements, expiry-supported dates, volume-positive contract dates, adequate prior-date smiles, dates with LO IV, and forward-test dates.
- Require strict prior-date information, meaningful cross-sectional support and explicit missing-data treatment.

**Done when:** each attrition step has machine-readable counts by year, expiry, source and sample definition.

### D. Extended chronological experiment (**only after A–C**)

**Depends on verified quality and adequate eligible dates.** Reuse `experiments.wti_apo_empirical`, `experiments.wti_apo_date_panel`, `scripts/run_extended_forward_validation.py` and established fixed seed/CI architecture. Use a predeclared chronological test holdout and frozen methodological choices; keep prior experiments unmodified. Compare PI, PM, historical volatility variants, prior APO IV and prior LO IV where supported on identical eligible rows. Recalculate MAE/RMSE/bias for each filtered panel, stratify by theoretical/actual settlement, liquidity, fixing progress, expiry and calendar regime. Report date clusters and serial dependence (time-block sensitivity), not naive row-iid confidence bands. Check whether PI-PM differences are substantively material versus source/model-specification differences.

**Done when:** complete manifests, parity on overlapping historical dates, held-out comparisons and uncertainty summaries are reproducible.

### E. Manuscript, literature and journal readiness (**after D**)

Read `docs/journal_strategy.md`. The **proposed next ambitious target is Journal of Commodity Markets (JCM)** because its official scope includes pricing, hedging and risk analysis of commodity derivatives, but **the final target is conditional on an independently validated new study**. REMEF is the prepared realistic fallback; JFM is a stretch alternative with retained Wiley LaTeX source. Do not automatically replace the active JFM/REMEF manuscripts or claim this paper is already acceptable at JCM.

Reassess direct precedents (Asian commodities, Bayesian exotic pricing, WTI options), the differentiation between posterior integration versus volatility-source selection, and the limitations of CME model-generated settlements (including May 2020 Curran adoption). Adapt the manuscript and supplement with only verified results; check each eventual journal's current author requirements, data sharing, APC/optional OA policy, and non-simultaneous submission rules before submitting.

**Done when:** author-approved target, reproducible final numerical manuscript, cleaned supplement, provenance/data licensing decision, and journal-specific package are complete.

## Local execution and branch coordination

```powershell
git switch main
git pull --ff-only origin main
conda activate asian-options
python -m pytest tests/test_wti_databento_aao_bulk.py tests/test_wti_databento_aao_inventory.py -q
python -m experiments.wti_databento_aao_inventory --months 2023-06 2025-06 2026-06
# If sample identity/flags are correct:
python -m experiments.wti_databento_aao_inventory --all
```

Read aggregate JSON outputs and only then allocate workstream B. Do not rerun billable `experiments.wti_databento_aao_bulk --mode download` without a new, explicit reason and authorization.
