# Agent execution plan — WTI APO 2020–2026 longitudinal study

Read `AGENTS.md`, `research/AI_HANDOFF.md`, `research/CHECKPOINT_2026-10-25_AAO_EXPANSION.md`, `docs/architecture.md`, `docs/agent_guide.md` and `research/DATABENTO_AAO_EXPANSION_PLAN.md` first. **No Databento charge or scientific result is authorized by this task list.**

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

- Run current offline `experiments.wti_databento_aao_inventory --months 2023-06 2025-06 2026-06`, then `--all` after smoke-test.
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
