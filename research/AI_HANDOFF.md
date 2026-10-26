## Latest author decision: prepare Databento-only journal study (2026-10-26)

> **Canonical continuation:** [HANDOFF](../HANDOFF.md), [master plan](PAPER_COMPLETION_MASTER_PLAN_2026-10-26.md), [evidence ledger](AAO_EVIDENCE_LEDGER_2026-10-26.md), [experiment register](AAO_EXPERIMENT_REGISTER_2026-10-26.md), and [agent verification](AAO_AGENT_VERIFICATION_PROTOCOL_2026-10-26.md). The current user-selected paper is **Databento-only PR #110**, not Barchart/LO comparisons; the original DBNs/SQLite have not been verified reuploaded.

The author explicitly abandoned the Barchart-based option-price
comparisons for the **new Elsevier CAS manuscript** and requests
Bayesian PI/PM, historical-volatility and lagged AAO IV benchmarking
using the owned Databento AAO source data alone. The assistant prepared
`bayesian_asian_options.aao_databento_only`,
`experiments.wti_aao_databento_only`,
`scripts.plot_aao_databento_only`,
`paper/jcm/databento_main.tex` and
`paper/jcm/build_databento.py`, with synthetic tests and runbook
`research/AAO_DATABENTO_ONLY_PAPER_RUNBOOK_2026-10-26.md`.

**Scientific constraint:** AAO definitions+statistics do NOT contain
the original CL first-nearby futures returns, fixings or current
CL forward curve. This new study deliberately uses **reduced-form
terminal-average Black valuation**, inferred expected average and
discount from same-day AAO parity emph{at reserved strikes}, and
strictly lagged volatility inputs. Anchors never become evaluated
target strikes. Historical proxy changes in parity-implied forwards
are NOT independent observed P-measure CL returns. Do not relabel
this as the old structural Asian Monte Carlo or as fully ex-ante
forecast accuracy. Actual/theoretical exchange marks are reported
separately; inference resamples dates, not option rows.

The source files and SQLite were lost during prior unsafe sparse
checkout and remain unavailable until the author performs the paid
replacement and **LFS-push** procedure already in PR #109/main.
No Databento-only model results or publication charts have been
computed yet. After user runs the experiment, inspect its manifest,
`method_metrics.csv`, `cluster_intervals.csv`, and three
generated figures, then **update the new CAS manuscript with the
actual validated results**, not anticipated rankings.

# AI handoff

## URGENT: recovered data must be backed up via Git LFS (26 October 2026)

The user's original **162 Databento AAO DBN files and the 5.1m-key private
SQLite database disappeared** immediately after the assistant recommended a
sparse-checkout addition that excluded `data/databento`. The Recycle Bin
did not contain the files. This was an unsafe assistant instruction.
No reacquisition or upload has yet occurred. The author explicitly
directed that **the entire 81-month dataset, AND the rebuilt SQLite,
be stored in their VERIFIED PRIVATE GitHub repository using Git LFS**.

Do not fall back to the previous instruction "keep licensed DBNs only
on VM". It was the cause of the unrecoverable single-copy failure.
`.gitattributes` now marks DBNs/SQLite for LFS, `.gitignore`
un-ignores these exact files, and a tracked data README makes the
sparse-checkout path visible. The existing quote-first manual downloader
should write to `data/databento/wti_aao_bulk/raw` and use a **fresh
reacquisition_20261026 acquisition ledger** to avoid the older manifests
which reference missing source files.

**Read and follow every gate in**
`research/AAO_RECOVERY_AND_LFS_BACKUP_2026-10-26.md`.
The new `scripts.aao_lfs_preflight` must pass **before a paid retrieval**.
After obtaining **162 verified files**, **Git LFS commit and push them**
before any expensive replay or sparse-checkout operation. Then run
`scripts.aao_replay_offline --execute` (all 11 previous diagnostics)
and upload the rebuilt SQLite via LFS. CI must never acquire billable
data or generate heavy scientific figures automatically.
The historical results recorded below document past successful VM runs;
they do **not** mean the lost binary files are still available.


## Newest resolution: January 26 latest preliminary, Barchart checkout incomplete

The user's `--explain-date 2024-01-26` query found **7,868/7,868**
latest contract/date keys **preliminary** and **no** selected final
keys (no deleted, invalid, intraday or rank-conflicted keys). Two
historical raw final *events* on that reference date were reported
earlier; event-level revision attribution has not been independently
traced. The 1,701 raw-final versus 1,700 selected-final date
difference is therefore **explained at the final-status level**,
not attributable to an incomplete Databento purchase.

Local Barchart CSV discovery returned `root_exists:false` and
`Test-Path ...sep2026/jaou6_10000c... = False` on the Windows VM.
Direct GitHub `main` inspection confirms the JAO histories **are
tracked upstream** in `data/csv/sep2026/`. The user's
`git ls-files ... | Select-Object -First 10` shows only the first
ten CL paths, not a complete JAO existence test. First inspect
the exact JAO path via `git ls-files --error-unmatch -- <path>`,
`git sparse-checkout list` and `git status --short -- data/csv`.
Restore individual missing tracked files only when safe or extend
sparse checkout, **without resetting uncommitted work**.

Full evidence and recovery procedure:
`research/AAO_PANEL_QUALITY_FINDINGS_2026-10-26.md`.
No new pricing results, Barchart date overlaps or manuscript changes
are established.

## Most recent source-quality result (2026-10-26)

The full 81-month cross-file reconciliation contains **5,105,603**
provisional final nonintraday AAO candidate settlement keys on 1,700
CME reference dates; the count includes **2019-12-31** (4,706 keys).
Therefore the January 2020–September 2026 date-range subset has
**1,699 distinct selected reference dates**, not an established
forward-backtest date count.

The author ran the raw-final-date scan: exactly **2024-01-26** was
lost, with **two raw final events** and no selected candidate.
Investigate the latest private SQLite status on that reference date
with the new `python -m experiments.wti_aao_panel_quality
--explain-date 2024-01-26`; do not repeat the expensive raw scan.
Barchart `available: false` is a missing **local file-discovery**
diagnostic, not no source overlap: GitHub main does track Barchart
APO history CSVs under `data/csv`. New optional
`--barchart-root` and path diagnostics help restore discovery.

Read `research/AAO_PANEL_QUALITY_FINDINGS_2026-10-26.md`
before changing code, pricing figures or Elsevier CAS manuscript.
No new vendor API calls or price/contract-level uploads.


## Latest handoff: full historical backfill complete (2026-10-25)

The author completed the February 2021 `AAO.OPT` recovery: **two files** for February at **USD 0.15870165 quoted**, saved with a *separate* February acquisition manifest. Combined with the earlier 160 file / USD 17.33487324 acquisition, there are now **162 reported DBN files covering 81 months**, with **USD 17.49357489 total quoted** (not necessarily billed). Earlier notes below saying “February missing” and “80 months” describe the prior 80-month inventory; they must not be treated as current acquisition status.

**Next agent action:** run *offline* `python -m experiments.wti_databento_aao_inventory --all` on the VM to refresh the old 80-month report, then check all 162 file hashes against both manifests and proceed to definitive contract/settlement-day identity. Do not rerun any billable download. Until that inventory is supplied, **1,682 final reference dates is an old 80-month figure**, not the full history. Journal planning remains conditional JCM / ready REMEF fallback / preserved JFM manuscript.


## New experiment/figure/manuscript working stage (2026-10-25)

The author added the Elsevier CAS template in `paper/els-cas-templates/`.
A separate `paper/jcm/` **CAS double-column working draft** preserves the
validated earlier concise paper and is explicitly **not** a new 81-month
pricing study. Source files, research workstreams and instructions are in
`research/AAO_81_MONTH_EXECUTION_PLAN.md`.

Offline executable gates:
`python -m scripts.audit_aao_manifests` checks all 162 source files
against both ledgers (including 2021-02);
`python -m experiments.wti_databento_aao_inventory --all` refreshes
the event counts if needed;
`python -m scripts.plot_aao_history_coverage` produces an intentionally
**diagnostic-only** new coverage figure and requires an 81-month report;
`python paper/jcm/build.py --check` validates the CAS working source.

**Do not** replace published-draft figures/tables with an event-count graph.
Priority is time-aware historical contract mapping, unique final contract-day
mark normalization, Barchart/CL and strictly lagged-IV eligibility, and then
reproducible chronological backtests before replacing empirical claims.
All heavy output generation remains manual-only and local to licensed data.

## Latest VM validation results and next agent action — 2026-10-25

The author reports **all 162 SHA256 checks passed**, with 81/81 monthly
windows, combined quoted USD 17.49357489 and no missing files. The
81-month coverage diagnostic generated all three formats from an
81-month inventory with SHA256
`4ec3893c8b5b216a5f450ffa40d0a910012bf6b66910b5eb8ad5f0c7f8950c13`.
The two existing identity probes both matched 100% of **final events to
some outright ID in the same month**, but that is **not** an event-time
as-of join: February 2021 has 55,326 final events versus 48,730 tentative
unique day/ID keys; June 2026 has 118,094 versus 101,397, and more
theoretical-flagged than actual-flagged final events in June.

**New first task:** run
`python -m experiments.wti_aao_settlement_gate --months 2021-02 2026-06`
on the author's VM (offline). It tests strict same-UTC-day definition
as-of matches, deletions, last updates and differing settlement
reference/publication days. It prints **aggregate counts only**, not a
contract/day pricing panel. See `research/AAO_POST_DOWNLOAD_VALIDATION_2026-10-25.md`.
Scientific pricing experiments, model figures and JCM numerical
manuscript updates are **not yet completed**. No repeat paid download.

## Latest 81-month inventory and timestamp-mapping investigation (2026-10-25)

**Author's refreshed 81-month inventory:** 70,154,064 statistics events,
13,412,045 settlement events, **5,899,096 final** (4,027,696 actual-flagged,
1,871,400 theoretical-flagged), and **1,701 distinct final CME `ts_ref`
reference dates**. These are not deduplicated option prices or eligible
out-of-sample dates. All 162 raw files passed the author's SHA256 check.

The conservative `wti_aao_settlement_gate` excluded **76.1%** of February
2021 and **81.1%** of June 2026 settlement events from a *same-publication-
UTC-day, preceding-definition* match. This should **not** be treated as
market-data attrition: many CME settlement reference dates differ from
the UTC publication day, and venue definition snapshots are time-dependent.
Latest actionable checkpoint:
`research/AAO_81_MONTH_SETTLEMENT_MAPPING_FINDINGS.md`.

**Next offline command:** `python -m experiments.wti_aao_mapping_comparison
--months 2021-02 2026-06`. It tests daily definition mappings against
reference, publication and preceding publication dates, including
conflicting contract-fingerprint indicators. It is a *diagnostic*, not a
validated priced option-date panel or a basis to change the paper yet.

## Newer instrument-mapping experiment and status (2026-10-25)

The latest author's full local outputs are recorded in
`research/AAO_SYMBOL_MAPPING_NEXT_GATE_2026-10-25.md`.
Only **55.1%** of February 2021 and **58.3%** of June 2026 final
settlement events matched one or more tried *definition-snapshot-day*
conventions. No conflicting contract identities were observed among
matched alternatives. Missing snapshots do **not** establish missing
market prices.

The next action is **offline**:
`python -m experiments.wti_aao_symbol_mapping --months 2021-02 2026-06`.
Databento's `DBNStore.to_df(map_symbols=True)` can map numeric IDs to
native symbols using local DBN metadata; the `statistics` tables already
show a `symbol` field. Verify its completeness and unique outright
contract fingerprints before implementing the stable contract/day
price panel. Do not use numeric `instrument_id` alone across dates;
do not run further paid downloads. Model results and paper figures
are not yet updated.

## Native-symbol breakthrough and candidate-panel implementation (2026-10-26)

The author ran `wti_aao_symbol_mapping` locally on 2021-02 and 2026-06:
**100% of final AAO settlement events in both samples** have nonempty
native mapped symbols and match one unambiguous publisher-scoped outright
C/P option fingerprint; **zero** same-symbol conflicting fingerprints in
either month. There are 48,730 and 101,397 *tentative* unique symbol +
CME reference-date keys, respectively. This makes native-symbol matching
a much better starting point than arbitrary daily instrument-ID joins.

The new offline
`experiments.wti_aao_contract_day_candidates --months 2021-02 2026-06`
constructs *within-file-month* candidate settlement records using latest
correction/deletion, final/non-intraday flags, and unambiguous outright
identities. It prints aggregate reports by default; row-level
`--export-private` writes only to a **gitignored** local folder, never
GitHub. See `research/AAO_NATIVE_SYMBOL_CANDIDATE_PANEL_2026-10-26.md`.

**These are not yet validated exchange prices or a chronological test
panel.** After reviewing candidates, implement cross-month late-update
reconciliation, contract-spec/price-scale audit, CL/fixing/rates/lagged-IV
eligibility, and only then actual new Bayesian backtests, performance
figures and manuscript updates. Never rerun paid Databento downloads.

## Cross-month settlement reconciliation ready to run (2026-10-26)

The user successfully ran `wti_aao_contract_day_candidates`
on 2021-02 and 2026-06: **48,730** and **101,397**
final nonintraday native-symbol/reference-day candidates, with
**101** and **190** latest preliminary keys, respectively. They
found no ambiguous last updates, deletions, intraday candidate flags
or invalid prices in the sampled months. These are *within-source-file-
month candidates* and cannot yet be the study's unique observed prices.

The next **strictly offline** tool
`experiments.wti_aao_cross_month` uses a two-pass global contract
identity audit and on-disk SQLite replay across source months to
account for late corrections and symbol reuse. Run four sampled source
months before `--all`. The complete procedure, privacy rules and
further pricing gates are documented in
`research/AAO_CROSS_MONTH_SETTLEMENT_RECONCILIATION_2026-10-26.md`.
No Databento charges, new model-performance claims or manuscript
reformatting are warranted now.

## Latest checkpoint: full 81-month cross-file reconciliation (2026-10-26)

The user's **four-month** and **full 81-month** offline SQLite
reconciliation commands succeeded. Full results: **5,157,894** tentative
publisher/symbol/reference-day keys; 71,145 seen in more than one
file month; 52,290 latest preliminary, **1** latest invalid price,
and **5,105,603 selected final nonintraday candidates**, split into
3,299,087 actual-flagged and 1,806,516 theoretical-flagged.
There are **1,700 selected CME reference dates**, not the raw-event
inventory's **1,701**. No tied latest updates, deletions or
cross-month symbol-fingerprint conflicts appeared in these logs.

The next task is an **offline quality/date-gap/source overlap audit**:
`python -m experiments.wti_aao_panel_quality`, then
`python -m experiments.wti_aao_panel_quality --scan-final-dates`
if the date discrepancy remains. See
`research/AAO_FULL_HISTORY_RECONCILIATION_2026-10-26.md`.
Do NOT treat millions of correlated candidates as 1,700 independent
backtests or revise Bayesian comparison figures yet. Then establish
actual contract/price-unit Barchart parity, CL/rates/prior-IV inputs
and frozen chronological holdouts.

Read this file before continuing research work.

## Canonical current checkpoint

**Latest operational checkpoint for the historical AAO expansion:** `research/CHECKPOINT_2026-10-25_AAO_EXPANSION.md`; coordinated agent tasks: `research/AAO_AGENT_TASKS.md`; conditional editorial strategy: `docs/journal_strategy.md`.

The earlier scientifically validated results, exact numbers and 2026 experimental status are preserved in `research/CHECKPOINT_2026-09-29.md`. The **October 25 checkpoint supersedes earlier statements that historical AAO acquisition is merely proposed**. The author's VM reports 160 completed DBN chunks (80 months, `AAO.OPT` definitions/statistics) at USD 17.33487324 *quoted*. Actual billing, file contents, valid final settlements and extended market tests are not yet verified. **No automatic redownload, new charges, or new manuscript numerical claims.**

## Current local-data validation update — 2026-10-25

The author **already completed** both offline inventory commands on the Windows VM:
`--months 2023-06 2025-06 2026-06` and `--all`. The latter read 80 months without errors, identifying asset `AAO`, 5,843,770 final settlement **events** (3,989,698 flagged actual, 1,854,072 flagged theoretical) and **1,682 distinct final reference dates**; **February 2021** is absent. These are *not* distinct verified option-day prices or eligible independent test dates. Full counts, warnings and remaining work:
`research/AAO_INVENTORY_RESULTS_2026-10-25.md`.

**Next:** checksum/manifest audit, investigate the excluded month, canonicalize outright definitions and stable instrument keys, deduplicate final settlement events, and Barchart/CL/rates/lagged-IV eligibility reconciliation. Do not rerun the completed inventory unless diagnosing a change; do **not** rerun the paid downloader.

## Scientific status

Issue #38 is complete in production.

The contract-reconstructed first-nearby physical-volatility robustness gives:

- posterior mean sigma 0.41824 versus 0.41651 for Yahoo `CL=F`;
- annualized realized volatility 0.41834 versus 0.41670;
- 2,381 exact pricing holdouts in both runs;
- historical PI MAE/RMSE 2.6468/3.4451 under first-nearby versus 2.6187/3.4090 under Yahoo;
- external previous-day LO MAE/RMSE 0.1559/0.2599 on the 253-row common-support sample versus reconstructed historical PI 0.4362/0.5466.

Therefore the paper's empirical hierarchy survives the physical-return source change.

Do not restart #38 or propose another first-nearby experiment.

## Current main scientific result

The paper supports:

[
	ext{posterior-integration refinement}
ll
	ext{historical-}P	ext{ versus option-informed }Q
]

in the observed WTI APO data, while the synthetic mechanism map shows that posterior integration can become material under weak information and high price curvature.

The option-informed conclusion is supported by both:

1. strict prior-date APO-implied smiles;
2. independent prior-date standard WTI vanilla-option (LO) information.

## Immediate next work — October 2026 historical-data phase

1. **Inventory already ran successfully.** Compare SHA256 with the manifest, investigate the missing February 2021 quote, check degraded dates and instrument master fields; do not access the paid Databento API by default.
2. Inspect option identity, `stat_type=3` final/theoretical flags, `ts_ref` dating, instrument revisions, expiries, strikes, sides and open interest/volume; generate only license-compliant derived aggregates.
3. Cross-match Databento and Barchart settlements and construct new unique, eligible valuation dates with proper CL first-nearby fixing schedule, dated Treasury rates and **strictly prior-date** APO/LO volatility information.
4. Only after that, run the canonical historical extension using `experiments/wti_apo_empirical.py` / `scripts/run_extended_forward_validation.py`; freeze chronological test blocks and compare models on common row support, reporting date-cluster/time-block uncertainty.
5. Reconsider *Journal of Commodity Markets* as a **conditional next target** if the independently verified new results warrant it. Preserve the prepared REMEF Word route and frozen Wiley/JFM manuscript until an author-approved reformat/submission decision. No parallel submissions.

Earlier first-nearby robustness (Issue #38) is done and must not be repeated.

## Important source conventions

- In the Barchart histories used here, `Latest` is the CME settlement field.
- The reconstructed physical return series excludes all roll-crossing returns.
- Four isolated mapped CL settlement gaps are not imputed; all affected one-day returns are excluded.
- Option-implied volatility is an effective/model-equivalent state under the maintained pricing map, not a unique structural diffusion coefficient.
- Do not claim universal LO superiority over APO information.

## Temporary data-retention decision

The current LFS-tracked raw/external data are being kept intentionally as a temporary continuity backup because the active experiments are running on an external machine whose local storage may be erased.

Do **not** delete, untrack, purge, or "clean up" these data unless the author explicitly authorizes it.

The intended workflow is:
1. keep the backup through manuscript submission;
2. once the paper has been sent and the scientific state is safely archived elsewhere, review licenses and remove/restructure raw vendor data as needed for the final public/reproducibility snapshot.

Temporary retention does not by itself establish redistribution rights.
