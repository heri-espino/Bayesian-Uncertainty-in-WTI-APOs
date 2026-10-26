# WTI APO — start here (2026-10-26)

**The paper is NOT finished.** Previous Bayesian WTI Barchart/LO research and manuscript results are stored in this repository; the 81-month Databento AAO extension has only historical source/instrument/settlement diagnostics, **not a validated extended forward pricing study**.

The original 162 AAO DBN files and private historical SQLite disappeared from the Windows VM after an unsafe sparse-checkout instruction. Private Git LFS tracking is configured, but **no 162 replacement files nor rebuilt 81-month SQLite have been verified as pushed to GitHub**.

**Author's explicit objective:** re-acquire all 81 months, back up all 162 DBNs and new closed SQLite to the private repository through Git LFS, validate contract-specific Barchart-versus-Databento settlement prices and first-nearby CL fixing calendars, compare strictly previous-date APO and independent LO IV with historical volatility baselines and posterior integration, generate uncertainty-aware experiments/figures, and finish the paper. **Conditional ambitious journal:** Journal of Commodity Markets (JCM). Preserve REMEF fallback and Wiley/JFM sources.

Read this order:

1. [AGENTS.md](AGENTS.md)
2. [Master completion plan](research/PAPER_COMPLETION_MASTER_PLAN_2026-10-26.md)
3. [Evidence ledger with all known results and qualifications](research/AAO_EVIDENCE_LEDGER_2026-10-26.md)
4. [Sequential experiments001–008](research/AAO_EXPERIMENT_REGISTER_2026-10-26.md)
5. [Independent agent verification protocol](research/AAO_AGENT_VERIFICATION_PROTOCOL_2026-10-26.md)
6. [Full data replacement and LFS backup](research/AAO_RECOVERY_AND_LFS_BACKUP_2026-10-26.md)
7. [Historical agent handoff](research/AI_HANDOFF.md) and [Issue #90](https://github.com/heri-espino/Bayesian-Uncertainty-in-WTI-APOs/issues/90).

**5,105,603** is the historical count of provisional final nonintraday *contract/reference-date keys*, not independently forward-eligible pricing observations. A reported Barchart overlap value `available:false` was from **before** Barchart CSVs were restored to the worktree; a subsequent audit failed because the Databento SQLite was already missing. No successful post-restoration cross-vendor parity experiment exists.

For every experiment, preserve the raw/processed source, code, environment/seed, machine-readable outputs, charts, interpretations, failures and next actions under an independent Git branch/PR. Never merge without explicit author authorization. Do not leave essential data only on the VM, use unsafe sparse-checkout cleanup, or commit API credentials.
