# AI handoff

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
