# WTI APO — start here (2026-10-26)

**RECOVERY STATUS UPDATE (later on 2026-10-26):** The 162 DBNs, new 81-month acquisition manifest, and SQLite are **now verified present on remote backup branch** `backup/aao-recovery-20261026` (Git LFS pointers); the author's 162/162 SHA256 audit passed. They are **not yet merged into `main`**. [PR #112](https://github.com/heri-espino/Bayesian-Uncertainty-in-WTI-APOs/pull/112) is open for safe integration. Independent remote LFS blob retrieval and the new six-method actual pricing tests remain pending. Read [the latest checkpoint](research/AAO_RECOVERY_CONFIRMED_BACKUP_BRANCH_2026-10-26.md). Earlier statements below describing files as absent reflect the pre-recovery checkpoint.

**The paper is NOT finished.** Previous Bayesian WTI Barchart/LO research and manuscript results are stored in this repository; the 81-month Databento AAO extension has only historical source/instrument/settlement diagnostics, **not a validated extended forward pricing study**.

The original 162 AAO DBN files and private historical SQLite disappeared from the Windows VM after an unsafe sparse-checkout instruction. Private Git LFS tracking is configured, but **no 162 replacement files nor rebuilt 81-month SQLite have been verified as pushed to GitHub**.

**Author's explicit objective:** re-acquire all 81 months, back up all 162 DBNs and the new closed SQLite to the private repository through Git LFS, and finish the **Databento-only reduced-form AAO Bayesian paper** prepared by merged PR #110. The implemented comparison uses PI, PM, rolling21, rolling63, EWMA63 and strictly prior-date AAO implied volatility on **non-anchor** options, with same-day disjoint put/call parity anchors and a lognormal terminal-average approximation. **Barchart, LO and CL futures comparisons belong to the earlier separate paper/optional extension; they are not inputs to the selected new article.** **Conditional ambitious journal:** Journal of Commodity Markets (JCM). Preserve REMEF fallback and Wiley/JFM sources.

Read this order:

1. [AGENTS.md](AGENTS.md)
2. [Master completion plan](research/PAPER_COMPLETION_MASTER_PLAN_2026-10-26.md)
3. [Evidence ledger with all known results and qualifications](research/AAO_EVIDENCE_LEDGER_2026-10-26.md)
4. [Sequential experiments001–008](research/AAO_EXPERIMENT_REGISTER_2026-10-26.md)
5. [Independent agent verification protocol](research/AAO_AGENT_VERIFICATION_PROTOCOL_2026-10-26.md)
6. [Full data replacement and LFS backup](research/AAO_RECOVERY_AND_LFS_BACKUP_2026-10-26.md)
7. [Current Databento-only experiment and manuscript runbook](research/AAO_DATABENTO_ONLY_PAPER_RUNBOOK_2026-10-26.md)
8. [Historical agent handoff](research/AI_HANDOFF.md) and [Issue #90](https://github.com/heri-espino/Bayesian-Uncertainty-in-WTI-APOs/issues/90).

**5,105,603** is the historical count of provisional final nonintraday *contract/reference-date keys*, not independently forward-eligible pricing observations. A reported Barchart overlap value `available:false` was from **before** Barchart CSVs were restored to the worktree; a subsequent audit failed because the Databento SQLite was already missing. No successful post-restoration cross-vendor parity experiment exists; **such parity is not required for the Databento-only reduced-form paper.**

For every experiment, preserve the raw/processed source, code, environment/seed, machine-readable outputs, charts, interpretations, failures and next actions under an independent Git branch/PR. Never merge without explicit author authorization. Do not leave essential data only on the VM, use unsafe sparse-checkout cleanup, or commit API credentials.
