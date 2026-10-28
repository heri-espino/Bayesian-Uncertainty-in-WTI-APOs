# WTI AAO settlement availability, purchase decision and preservation audit

**Created:** 2026-10-27.  
**Status:** official-source check + Git metadata inspection. **No charge, purchase, download, live subscription or remote binary-restore verification took place.**  
**Repo:** private `heri-espino/Bayesian-Uncertainty-in-WTI-APOs`, draft REMEF branch `paper/remef-scientific-completion-20261027`.  
**Scope:** separate already-acquired *historical AAO settlement* records from missing *future point-in-time collection* and optional *independent executable prices*.

## 1. Source discovery: Databento ALREADY HAS AAO settlement values

**Verified in provider documentation:**
- [WTI AAO Databento catalog](https://databento.com/catalog/cme/GLBX.MDP3/options/AAO): product `AAO` in CME `GLBX.MDP3` supports `statistics`, `definition`, trades, market depth and other schemas.
- [Databento Statistics schema](https://databento.com/docs/schemas/statistics): **settlement price is `stat_type = 3`**, its actual `price` field contains the settlement; `stat_flags & 1` = final, `stat_flags & 2` = actual as opposed to theoretical; `ts_ref` is CME **session reference date**, and `ts_event`/`ts_recv` are intraday recorded timing fields.
- [Databento CME MDP3 normalization](https://databento.com/docs/datasets/glbx-mdp3): preliminary and final updates can coexist for the same reference date; the market feed **does not disseminate settlement prices for instruments without open interest or volume**. Thus `statistics` is not guaranteed complete for every possible listed strike.
- **Important:** `actual-flagged` official settlement still is **not automatically an executable matched option trade**, and a published settlement can be model-dependent (CME AAO Curran methodology from 2020).
- The repo's own previously completed 2020–September 2026 workflow already used these `AAO.OPT` statistics: author-run full 81-month cross-file reconciliation reports 13,412,045 **settlement events**, 5,105,603 **provisional selected final non-intraday candidate** contract/date keys; the distinct published-study conditional target counts were 111,585 option-date rows on 189 dates. **Event count is not eligible forecast count.**

**Decision:** do **NOT repurchase** January 2020–September 2026 `AAO.OPT` `definition`/`statistics` simply to find settlement prices. Their schema and file archive already cover that problem.

## 2. Backup state investigated now

Repository listings at this branch show:

| Tracked research asset | Git state observed | What has NOT been verified |
| --- | --- | --- |
| `data/databento/wti_aao_bulk/raw/` | **162** monthly file entries: 81 `aao_definition__...` and 81 `aao_statistics__...`; Jan 2020–Sept 2026 | Independent **Git LFS server retrieval of all 162 complete binary objects** and hash verification on a separately restored machine |
| `data/databento/wti_aao_bulk/derived_private/aao_cross_month_PROVISIONAL_81_months.sqlite3` | Valid **Git LFS pointer** with claimed original size **539,226,112 bytes** and SHA-256 `6690d814289f1ced386ff12f0b3c67887ac786746b6cc5f8003295885f97ae7e` | That the full SQLite payload is presently retrievable from LFS remote and usable by SQLite |
| Other priced pilot/full `*.csv.gz` files | Multiple separate private LFS pointers under `derived_private/` | All remote binary payloads and derived license/redistribution entitlement |
| `results/analysis/wti_aao_history_feasibility/reacquisition_20261026/bulk_acquisition_manifest.json` | **162** completed chunks, with SHA-256, byte sizes, source date windows | Independent full binary download after upload |
| `results/analysis/wti_aao_history_feasibility/integrity/combined_manifest_audit.json` | Prior offline output claims 162/162 SHA-256 verified | It belongs to an older combined manifest run; not sufficient evidence of *remote* Git LFS object retrieval |

**Important false alarm resolved:** the older `bulk/` + `bulk_feb2021/` original-acquisition ledgers sometimes have **different byte sizes and SHA-256** from the current Git pointers. The correct comparison for present files is the **`reacquisition_20261026`** ledger. Six manually selected Git LFS pointers spanning 2020, 2021, 2023, 2025 and 2026 were independently inspected against **that newer ledger**; **6/6 matched SHA-256 and byte size exactly**. This is sampled Git **pointer** integrity only—not 162/162 full remote payload retrieval.

**Created [repeatable read-only pointer-check script](../scripts/audit_aao_git_lfs_pointers.py):** compare **all 162 tracked pointer objects** from Git history against the current reacquisition ledger. Its Python implementation **has not been executed in the Git checkout in this interaction**, so a full 162/162 pointer result is not claimed. It does not issue provider requests or re-download LFS objects.

### Backup-verification commands (safe; from correct repository branch)

```powershell
# Offline, metadata-only; outputs how many of the 162 pointers match the 2026-10-26 ledger:
python -m scripts.audit_aao_git_lfs_pointers --write-report

# Offline, local data bytes; DO NOT use old manifests for reacquired objects:
python -m scripts.audit_aao_manifests --manifest results/analysis/wti_aao_history_feasibility/reacquisition_20261026/bulk_acquisition_manifest.json

# Read-only local Git LFS integrity and pointer listing:
git lfs ls-files
git lfs fsck
```

**Note:** To independently assert complete **remote backup**, conduct a separate authenticated restore from remote LFS to **another non-destructive temporary directory**, then verify each restored payload's SHA-256 against the reacquisition ledger and open SQLite. This may transfer substantial binary data / incur LFS bandwidth cost. Do not destroy sparse checkouts, delete local data, force checkout/reset/clean, claim off-machine backup solely from a 132-byte pointer or silently overwrite the old acquisition ledgers. Do not put provider API keys in Git.

The optional `--write-report` creates only a derived JSON report; the user must commit/push it under the project handoff rules. **No binary files were transferred or re-saved by this review.**

## 3. Do we need to purchase anything else?

**Historical 2020–2026 AAO settlements:** **NO**. Already purchased and documented as `statistics`.

**Ongoing AAO final settlements after Sept 2026 (for prospective shadow experiment):** **POTENTIALLY YES**, but need confirmed authorized access, official settlement timetable, exact expected charges, and a prospective feed; a historical purchase **after** future outcomes occur cannot be treated as an independently sealed live forecast. [Databento Live](https://databento.com/docs/api-reference-live/client/live) offers streaming for `GLBX.MDP3` on entitled accounts; actual eligibility and charges depend on live licensing. It should be investigated first for an **existing** entitlement and `AAO.OPT` statistics coverage. A supplementary `definition` feed/source is needed to map instrument IDs; preferably CL futures settlement state from the previous completed day is also needed.

**If specific AAO strikes lack MDP3 settlement events:** Databento's official CME source documentation states that some instruments with no volume or open interest do not receive MDP settlement events. For **complete official daily EOD settlements**, [CME DataMine](https://www.cmegroup.com/datamine.html) sells **End of Market Summary / Settlements** and related products subject to entitlement. [CME's settlement FAQ](https://www.cmegroup.com/articles/faqs/access-to-cme-group-settlement-data-faq.html) differentiates real-time/distributed market feed from the paid DataMine settlement files and their fees. A CME DataMine purchase is appropriate only if the research needs fuller or separately validated settlement coverage than the already bought MDP3 `statistics`.

**For executable-price forecasting:** official settlement records cannot establish this; the separate dataset would be time-stamped trades (`trades`/`tbbo`) or quote/bid-ask messages (`mbp-1`/`bbo-1s`), plus exchange-specific liquidity/market hours. Buy only after a contract-volume/quote-availability probe; many WTI AAO strike-date marks have zero recorded volume.

### Cost and permission gate

Neither CME nor Databento accounts/payment credentials are connected as purchasing tools in this chat. **No order has been submitted; no license was agreed; no money was charged**. There is no verified per-user live-license quote or authorized budget. Do not manufacture a price or treat a general vendor website starting price as a firm AAO entitlement quote. The existing historical paid acquisition was quoted **USD 17.49357489** across 162 reacquired files; this is not a new purchase or confirmed charged amount. An October 2026 incremental request would need an **independent new quote** and a separate timestamped manifest; NEVER rerun the Jan-2020–Sep-2026 downloader unchanged.

**Purchase sequence when available:** (1) check current vendor Databento rights/access and October AAO `statistics` coverage at the exact desired product/period, (2) query actual price without downloading; for live feeds request the actual licensing terms, (3) check whether the missing records are absence of MDP publications versus schema lookup error, (4) buy **only missing data** after account holder has approved price/terms and a recoverable licensed-storage destination, (5) update the **new** incremental manifest and upload permitted binary objects with tested Git LFS push; independently verify restoration.

## 4. Relationship to prospective trial

Update the [prospective shadow protocol](PROSPECTIVE_WTI_AAO_SHADOW_FORECAST_PROTOCOL_2026-10-27.md) before issuing a live prediction:
- Preserve a sealed, **before-target** forecast and proof of model/CL inputs, **separately** from the later `statistics stat_type=3` outcome.
- Respect `ts_event`/`ts_recv` of actual statistics updates, not solely date-only `ts_ref`; avoid seeing settlement event revisions before forecast.
- The prospectively *retrieved* outcome can be purchased later; that is acceptable if the **forecast itself** was independently committed before outcome was known.
- Existing 2020–September 2026 historical `statistics` can develop/test the model, **not** serve as prospectively precommitted October–December 2026 forecasts.
- If missing-statistic symbols produce sparse outcome evaluation, retain denominator/attrition and do not substitute later theoretical marks without preregistering that source and definition.

**Decision:** Use our **already purchased** historical AAO settlement statistics. Get a narrow prospective **entitlement and cost quote** for any *future* flow or missing CME EOD fields; do not repeat costly history acquisition without evidence it is necessary. Validate remote recovery before declaring all 162 binaries safely backed up.
