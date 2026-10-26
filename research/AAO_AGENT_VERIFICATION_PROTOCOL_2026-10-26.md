# Independent-agent verification protocol — 2026-10-26

**CURRENT BACKUP REVIEW CORRECTION:** The 162 source DBNs and SQLite now have remote Git LFS pointer references on branch `backup/aao-recovery-20261026` with the manifest; the user passed SHA256 audit for all 162 locally. Verify this **backup branch**, not just `main`, and independently test remote object fetch before concluding end-to-end backup validation. [PR #112](https://github.com/heri-espino/Bayesian-Uncertainty-in-WTI-APOs/pull/112) is open, not merged. More detail: [new recovery checkpoint](AAO_RECOVERY_CONFIRMED_BACKUP_BRANCH_2026-10-26.md). The pre-recovery expected conclusions below are historical, not the current backup state.

An independent agent must verify this handoff **from the repository, not the previous conversation**. This is an audit, not authorization to merge, buy data, change sparse checkout or submit a paper.

## Read first

Read `AGENTS.md`, `README.md`, `research/PAPER_COMPLETION_MASTER_PLAN_2026-10-26.md`, `research/AAO_EVIDENCE_LEDGER_2026-10-26.md`, `research/AAO_EXPERIMENT_REGISTER_2026-10-26.md`, `research/AAO_RECOVERY_AND_LFS_BACKUP_2026-10-26.md`, `research/AI_HANDOFF.md`, `research/AAO_AGENT_TASKS.md`, `docs/journal_strategy.md`, `paper/jcm/README.md`, original JFM and REMEF manuscripts, numerical results and source code. Inspect the real code/test fixtures before trusting prose.

## Review matrix

| Area | Required independent observation | Present expectation |
| --- | --- | --- |
| Repository | Verify private visibility, target branch, active PRs | This is a private repository; current handoff is on a review branch |
| AAO source backup | Inspect remote Git/LFS for 162 compressed DBNs under `data/databento/wti_aao_bulk/raw/` | **Not uploaded at this checkpoint**; LFS configuration alone is not a backup |
| Derived data | Check remote 81-month SQLite and fresh acquisition manifest | Both absent at this checkpoint |
| Source completeness | Examine downloader and preflight | 81 windows * 2 schemas = 162, explicit quote-before-paid-download |
| Offline replay | Examine `scripts/aao_replay_offline.py` | 11 manual-only *diagnostic* stages, not new pricing comparisons |
| Old main comparison | Verify historical reports and short paper results | 2,381 option rows on 15 dates; seven expiries |
| Independent LO | Verify manuscript and reports | 253 APO rows on 10 dates, prior LO volatility |
| New historical inventory | Check evidence ledger provenance | 70,154,064 records; 13,412,045 settlements; 5,899,096 raw final events and 1,701 raw-final dates; previously run on VM only |
| Cross-month normalization | Check ledger arithmetic and implementation | 5,105,603 provisional final nonintraday keys over 1,700 dates, **not** eligible tests |
| Reference-date anomaly | Read quality note | 2024-01-26 has two raw final events but all 7,868 latest keys preliminary |
| Barchart source | Check tracked `data/csv/` and history of local restoration | CSVs tracked; post-recovery contract-level parity **not computed**; optional other study, not Databento-only paper input |
| Economic correctness | Check exact distinction: AAO-only reduced-form terminal average vs old structural CL Asian pricing | Same-day disjoint parity anchors, **pre-fixing only**, earlier-date volatility proxy/IV; no observed CL P-measure returns or first-nearby fixings; not fully ex-ante |
| JCM | Check both `paper/jcm/main.tex` and **new** `paper/jcm/databento_main.tex`, the separate `build_databento.py`, `research/AAO_DATABENTO_ONLY_PAPER_RUNBOOK_2026-10-26.md` | The Databento-only CAS article is authored with **results pending**. Old `main.tex` uses the earlier Barchart/LO results and must not be mistaken for the selected new article |
| Future plan | Compare master gates and experiment IDs | experiment001–008 **experiment task packages** are proposed; Databento-only engine/scripts and CAS draft are already implemented in PR #110, but heavy real-data pricing runs are unexecuted |

## Read-only / lightweight checks

Use `git ls-files` to locate source DBN and SQLite paths, `git lfs ls-files` to inspect tracking, repository metadata to verify actual remote LFS object presence, and existing README/manuscript/figure reports to verify numerical assertions. Git LFS pointer entries do not prove binary availability. Optional lightweight checks: `python -m scripts.aao_replay_offline` (dry run), `python paper/jcm/build.py --check`, and selected pytest modules including `tests/test_aao_lfs_preflight.py`, `tests/test_aao_manifests.py`, `tests/test_aao_cross_month.py`, `tests/test_wti_aao_panel_quality.py`.

Do NOT run the paid downloader, `--execute` heavy 81-month replay, destructive Git commands or snapshot-altering operations merely to audit a documentation change.

## Required reviewer deliverable

Write an independent report in a review branch/PR with: (1) checked Git revision; (2) files read; (3) commands actually executed; (4) **PASS/FAIL/BLOCKED/NOT CHECKED** for every source/science/paper gate; (5) verified evidence, contradictions and stale documents; (6) missing raw files or reports; (7) exact next safe work; (8) checks of date dependence, revisions, contract identities, price scaling, P vs Q, true forward information and uncertainty; (9) confirmation that no API key is exposed and that neither source files nor author work will be lost by sparse checkout; and (10) author-review questions.

Never report 81-month model pricing MAE/RMSE, validated vendor settlement parity, actual invoice amount, new JCM paper or completed remote LFS backup without independently versioned evidence. Preserve prior results and do not merge without authorization.

## Agent review instruction

Audit the WTI APO repository using the master completion plan, evidence ledger, experiment register, existing source, tests, result manifests and manuscript. Independently verify every recorded fact, identify stale documentation and scientifically invalid leaps, document blockers and propose minimal changes in a separate unmerged PR. The repository must be sufficient to complete source recovery, Databento-only pre-fixing parity-anchor validation, strictly prior volatility comparisons under the disclosed reduced-form model, new six-benchmark figures and the Databento-only JCM submission candidate without this conversation. Treat Barchart, LO and CL structural research as optional separate work, not a new-paper dependency.
