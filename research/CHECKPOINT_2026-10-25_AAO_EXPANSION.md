# Research checkpoint — 2026-10-25: historical Databento WTI APO acquisition

**Status: historical acquisition reported complete on the author's Windows VM; settlement identity, data quality, and new scientific results NOT yet verified.** This checkpoint supersedes older **acquisition-status** statements in `research/CHECKPOINT_2026-09-29.md`, `research/AI_HANDOFF.md`, `research/DATABENTO_AAO_EXPANSION_PLAN.md`, and archived REMEF planning text. It does **not** supersede the validated earlier empirical results or overwrite their numerical outputs.

## Scientific purpose

Question: **How large is the effect of integrating over posterior uncertainty compared with changing volatility information when pricing WTI Asian (average-price) options?**

Old production benchmark: 11,179 archived Barchart APO contract-date marks across 213 contracts, reduced to **2,381 strict-forward option-date holdouts on 15 target dates** (seven expiries), plus **253 LO-to-APO comparisons on 10 dates**. Correlated options on the same date are not independent tests. Preserve the 10-million-path synthetic study and all old reproducible results as a fallback.

The prospective improvement is a *longer series of independently eligible valuation dates*, not raw record count or another huge Monte Carlo run. New data can also reveal limitations from theoretical versus actual exchange settlements.

## Completed stages and evidence provenance

1. **Issue #90 and PR #91** created the initial feasibility plan. No acquisition then.
2. Early `symbology.resolve` tests returned zero mappings for `AAO.OPT`, and HTTP 422 for `AO.OPT`. The known-working **`LO.OPT` positive control also returned zero mappings**, so zero mappings were demonstrated to be an invalid absence test.
3. **PR #94 (merged)** added independent `metadata.get_record_count` and `metadata.get_cost` probes regardless of empty mappings, plus a 2026-08-24 LO positive control. The author's live result showed LO definitions 26,411 and statistics 347,846 (one day), and **positive AAO.OPT definition/statistics metadata estimates on one sampled day in each of 2023, 2024, 2025 and 2026**. Those metadata values were not settlement confirmation.
4. The author authorized **up to USD 40** of then-reported **USD 120** Databento credits. The quote-first bulk workflow in **PR #95 (merged, squash commit `56263f9`)** downloads compressed monthly `AAO.OPT` `definition` and `statistics` schemas, with an **USD 32 quoted-cost planning cutoff**. The cutoff is NOT a provider-enforced billing cap.
5. Author-reported live quote for 2020-01-01 through 2026-10-01 (exclusive): initially 81/81 months, USD **17.49357489** estimated. The subsequently executed download re-quoted **80/81 eligible months** at USD **17.33487324**.
6. **Author's completed CLI output:** `downloaded_chunks: 160`, `quoted_usd: 17.33487324`, saved manifest `results/analysis/wti_aao_history_feasibility/bulk/bulk_acquisition_manifest.json`. Thus the acquisition routine *reported completion of the 80 eligible months × two schemas*, not that all 160 files have been independently inspected or that the account was actually billed USD 17.33.
7. Databento emitted degraded-feed warnings on **2021-12-05; 2022-01-02; 2022-11-06; 2024-09-18; 2025-09-17; 2025-09-24; 2025-11-28; 2026-01-31; 2026-03-15; 2026-03-16; 2026-03-21; 2026-04-10; 2026-05-24; 2026-08-29**. These are dataset-level data-quality warnings; do NOT discard whole months or assert specific option marks are corrupted without a date/contract-level audit. Find the one ineligible month in the *latest* `bulk_quote_plan.json`; do not guess which it is.
8. **PR #95** also provides `experiments/wti_databento_aao_inventory.py` and its synthetic tests to examine locally saved DBN files with no Databento historical API purchase. **No live inventory report has been supplied yet.**

## Important status distinctions

- **Confirmed by reported VM logs:** download program finished and wrote a manifest; 160 chunks; the quote and warnings above.
- **Still unverified:** file integrity audit on VM, exact month excluded, actual account billing, decoded asset/product identity and metadata, counts of distinct *final* WTI APO settlement days, theoretical/actual mix, liquidity and Barchart agreement, trading reference dates, independent qualifying strict-forward test dates, expanded LO/CL coverage, new PI/PM or IV model results, and journal suitability after expansion.
- **Never assert:** 80 complete months of valid APO settlements; hundreds of independent pricing dates; successful new backtests; USD 17.33 exact charged; stronger journal acceptance odds; user approval for any further data purchases beyond the already executed authorization.

## Author's VM and data locations

Windows PowerShell, repo `Bayesian-Uncertainty-in-WTI-APOs`, Conda `asian-options`. Private API key is loaded via Windows user-scoped encrypted file and PowerShell profile; never print it, log it, embed it in an issue, or commit it. Opening `(base)` rather than `(asian-options)` can yield `ModuleNotFoundError: databento`. `ConvertTo-SecureString` on an encrypted file using `Get-Content -Raw` previously produced a format error; profile sourcing later worked, so do not confuse those unrelated errors with data availability.

Local licensed files (NOT GitHub): `data/databento/wti_aao_bulk/raw/aao_<schema>__<start>__<end>.dbn.zst`. Reports:
- `results/analysis/wti_aao_history_feasibility/bulk/bulk_quote_plan.json`;
- `results/analysis/wti_aao_history_feasibility/bulk/bulk_acquisition_manifest.json`;
- future `results/analysis/wti_aao_history_feasibility/inventory/aao_inventory_summary.json`.
Raw vendor data are gitignored; preserve local backup and vendor license conditions. Repository contains downloader and inventory code, **not** the author's private local DBN payloads.

## First commands for agents/users — NO further purchases

```powershell
git switch main
git pull --ff-only origin main
conda activate asian-options
python -m pytest tests/test_wti_databento_aao_bulk.py tests/test_wti_databento_aao_inventory.py -q
# View actual acquired-month inventory and the missing month:
$p = Get-Content results/analysis/wti_aao_history_feasibility/bulk/bulk_quote_plan.json -Raw | ConvertFrom-Json
$p.requests | Where-Object { -not $_.eligible } | Select-Object schema,start,end,status,error
# Inventory is 100% local; run a small test then full coverage:
python -m experiments.wti_databento_aao_inventory --months 2023-06 2025-06 2026-06
python -m experiments.wti_databento_aao_inventory --all
```

Before doing anything billable, read `research/DATABENTO_AAO_BULK_ACQUISITION.md`. **Do not rerun `--mode download` by default**: 160 chunks have already been acquired and repeated requests may cost credits.

## Next scientific phases (mandatory gates)

1. **Integrity and identity:** inspect SHA256 against ledger; list absent/incomplete chunks; identify true AAO option product from `definition.asset`, `group`, `raw_symbol`, instrument class, strike, expiration, underlying and exchange. Ensure the parent query did not mix outright options with strategy/combination instruments; deduplicate multi-leg definitions and updates.
2. **Settlement quality:** on `statistics`, `stat_type=3` identifies settlements, `stat_flags & 1` final, `stat_flags & 2` actual (otherwise theoretical), `stat_flags & 8` intraday; use `ts_ref` (UTC *date* reference) rather than `ts_event`/file month for trading day. Compare preliminary and final updates per instrument/day; account for early/late publication and degraded-feed dates. Separate volume `stat_type=6` and open interest `stat_type=9`. Quoted/cleared theoretical marks are **not independent transaction prices**. CME adopted the Curran model for WTI APO settlement valuation effective May 2020; treat model-derived price comparisons appropriately.
3. **Cross-vendor reconciliation:** compare overlapping original Barchart `Latest` CME settlements to matched Databento option contract-date-expiry-strike-side rows; report unmatched, theoretical, inactive/zero-volume, and date-shifted records, not just matched successes.
4. **Eligible date funnel:** derive month-by-month `valuation_date × expiry × strike × side` panel and attrition waterfall; validate CL first-nearby realized fixings and future contract curve from actual, dated contract histories; verify rates and **strictly lagged** APO smile and LO IV availability. Distinct option rows, dates, expiries, and independently eligible forward dates have different denominators.
5. **Only if justified:** quote and explicitly authorize matching additional LO/CL or rates data; add source adapters in the canonical library, and reuse `experiments/wti_apo_empirical.py` and `scripts/run_extended_forward_validation.py`. Do not create a parallel pricing engine.
6. **Inference/robustness:** use predeclared model choices and chronological holdout; same-row PI vs PM vs historic volatility (rolling/EWMA/GARCH), lagged APO IV, lagged same-contract IV and independently lagged LO IV. Report MAE, RMSE, bias, PI-PM gap, date/expiry counts, volume/OI/theoretical status and sensitivity; use date-cluster and temporal-block uncertainty. No leakage and no cherrypicking.
7. **Paper and editorial decision:** update manuscript/table/figures only from committed, reproducible result summaries and verified scientific contribution. Preserve older JFM LaTeX and REMEF Word alternatives unchanged until a new manuscript is validated. Follow `docs/journal_strategy.md`.

Read `research/AAO_AGENT_TASKS.md`, `AGENTS.md` and `research/AI_HANDOFF.md` before a new agent works on the data.
