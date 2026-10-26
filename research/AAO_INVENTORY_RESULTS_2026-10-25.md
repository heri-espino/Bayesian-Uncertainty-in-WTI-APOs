# Databento AAO offline inventory — author's VM output, 2026-10-25

**Evidence level:** Counts were copied from the author's **local** terminal output for the existing `experiments.wti_databento_aao_inventory` command. The raw Databento files, complete JSON report and file SHA256 checksums are *not* available in GitHub, and were **not** independently examined in this PR. This is an exploratory feed/settlement **event inventory**, NOT a validated contract-date pricing panel and NOT a new backtest.

## Commands already run successfully on the author's VM

```powershell
conda activate asian-options
python -m experiments.wti_databento_aao_inventory --months 2023-06 2025-06 2026-06
python -m experiments.wti_databento_aao_inventory --all
```

Both commands reported empty `errors`. The complete run overwrote the sample report, leaving the full local result at:

`results/analysis/wti_aao_history_feasibility/inventory/aao_inventory_summary.json`

No Databento API download or new charge is required to rerun this **offline** inventory. Script is in `experiments/wti_databento_aao_inventory.py`.

## Complete downloaded-window summary

| Metric | Reported count | Interpretation / limitation |
|---|---:|---|
| Monthly windows read | 80 | Definitions and statistics data read without processing exceptions |
| Distinct final `ts_ref` dates | **1,682** | Dates represented by at least one *final* settlement event; **not** forward-eligible or independent model validations |
| `statistics` records | **69,579,736** | The script's `records` summary sums **statistics DataFrames only**, not definitions |
| Settlement events, `stat_type=3` | **13,284,087** | Preliminary + final; includes repeated instruments/updates |
| Flagged final settlement events | **5,843,770** | `stat_flags & 1`; **not** deduplicated date × contract |
| Flagged final + actual events | **3,989,698** | `stat_flags & 1` and `stat_flags & 2`; **actual is a CME mark designation, not proof of a trade** |
| Flagged final + theoretical events | **1,854,072** | Final and not `stat_flags & 2`; theoretical/model-derived market marks require separate analysis |
| Positive cleared-volume statistic events | **98,152** | Positive volume *events*, not matched liquid final settlements |
| Positive open-interest statistic events | **5,719,204** | Positive OI *events*, not matched unique contracts |

Among **final** settlement events in this inventory, approximately **68.27%** are flagged actual and **31.73%** theoretical. This is an event-weighted split only, before deduplication and before deciding which options are usable.

Definition `asset` was consistently reported as **AAO** in all 80 printed months; each printed month included `C` (calls) and `P` (puts), sometimes `T` class entries. This is good **asset-level corroboration** of product coverage, **not** proof that every record is an outright target option or compatible with our fixing conventions.

The 81 monthly windows from January 2020 through September 2026 have an apparent missing **February 2021** in the decoded file list. The original latest `bulk_quote_plan.json` must still be inspected to establish *why* that month was excluded (zero count, failed quote, permission, API error, or another condition). **Do not purchase February 2021 just to fill the gap until its metadata reason is understood.**

## Representative-month result details (after correcting only for no facts)

| Month | Definition `AAO` events | Final settle events | Final + actual events |
|---|---:|---:|---:|
| 2020-01 | 137,464 | 117,815 | 115,944 |
| 2023-06 | 172,378 | 59,106 | 38,900 |
| 2025-06 | 201,198 | 70,841 | 41,562 |
| 2026-06 | 206,136 | 118,094 | 53,377 |
| 2026-09 | 208,752 | 84,224 | 56,086 |

**Do not infer a liquidity or pricing-model trend solely from these event counts.** Different numbers of actively listed contracts and repeated updates can change the mix.

## Technical interpretation: Databento / CME

Databento's official [CME Globex MDP3 guide](https://databento.com/docs/datasets/glbx-mdp3) says:

- `stat_type=3`: settlement; `6`: cleared volume; `9`: open interest.
- Settlement flag bit 0 (`1`) means **final**, bit 1 (`2`) means **actual** rather than theoretical, bit 2 (`4`) is trading vs clearing tick and bit 3 (`8`) denotes **intraday**.
- `ts_ref` comes from CME's `TradingReferenceDate` and should **not** be timezone-localized.
- CME publishes multiple daily statistic updates for the same reference trading day; one should choose the final, latest admissible update by an explicit contract/date-level rule, respecting deletions/corrections.
- Definitions in newer DBN v3 include extra records for strategy legs. `C` and `P` classes, `T` classes, and `leg_*` records need identity/strategy filtering before computing unique contracts or pairing with statistics.
- Cleared volume and OI are distinct statistic types with possibly different timing and reference dates; the event count alone cannot determine liquidity on settlement contract-date rows.

**Important research risk:** Since May 2020, CME Clearing has used Curran-based modeling for WTI Average Price Option settlement valuation. Comparison with exchange official marks, particularly theoretical ones, need not test predictive transaction prices.

## What remains open / instruction to the next agent

**Do not rerun the paid download.** Gate A is now *partially* complete: downloaded DBNs decode, 80 months yielded no inventory errors, the `AAO` asset exists, and 1,682 reference dates contain final *events*. Gate A is **not finished** until integrity, correct instrument mapping, and source-specific unique marks are audited.

1. Read `research/AAO_AGENT_TASKS.md` and `research/CHECKPOINT_2026-10-25_AAO_EXPANSION.md`; retain the old 15-day baseline results untouched. Do not submit this report as a new empirical result to JCM or REMEF.
2. Verify *all 160* downloaded file sizes/SHA256 with the local acquisition ledger, and inspect excluded 2021-02 metadata from `bulk_quote_plan.json`. Report missing/degraded days, but do not invent/impute marks.
3. Implement/tests for a **date-aware instrument master**: map statistics `instrument_id` (and `publisher_id` where needed) to historical `definition` events/symbols and raw expiry, strike, call/put, underlying and exchange. Handle corrections/revisions, expiring IDs and strategy legs, and compare stable Barchart contract identities.
4. Create **one final settlement record per actual option contract × CME `ts_ref` date** (and separately an actual-flagged subset), accounting for `update_action` and `ts_event`/publication cutoffs. Include independently verified volume and OI joins; no `symbol`-level or `instrument_id`-only uniqueness assumption across contract lifetimes.
5. Produce a dated **eligibility waterfall** by year/expiry: available market marks → final unique APO outright records → valid fixing/CL term structure/rates → at least one strictly earlier valid smile/calibration → independent forward prediction date. Compare the old 2,381 rows / 15 dates and 253 LO rows / 10 dates on exact common keys before expanded testing.
6. Only then consider any additional LO/CL data quote and new author-approved purchase (if indispensable), preserve zero price lookahead, run chronological held-out PI/PM and IV comparisons with date-cluster/time-block inference, and reassess [journal strategy](../docs/journal_strategy.md).

This derived-count checkpoint contains **no raw option-level prices, proprietary symbol lists, private user file paths, or API secrets**.
