# AAO source recovery — updated status after Windows restart (2026-10-26)

**Recovery milestone achieved; integration and full-science experiments remain pending.**

## Verified user-run local evidence

- `python -m scripts.aao_lfs_preflight --require-complete`: `ready=true`, **162 expected / 162 present**, LFS available, tracked data-directory anchor present, zero issues.
- `python -m scripts.audit_aao_manifests --manifest results/analysis/wti_aao_history_feasibility/reacquisition_20261026/bulk_acquisition_manifest.json`: `success=true`, `sha256_verified=true`, **162 of 162 files verified**, **81 of 81 months**, zero issues, historical **quoted** USD 17.49357489. This is a quote, not confirmed final invoice.
- Local commits: `8c37e35` (81-month AAO DBN sources) and `ff4db91` (reconstructed cross-month SQLite). Source files were staged and tracked with LFS.
- Backup push succeeded: user's `git log --oneline --left-right origin/main...main` showed `origin/backup/aao-recovery-20261026` on local tip `ff4db91`. Main branch push was rejected because `origin/main` separately advanced to PR #110. **No data-loss indication in this rejection**.

## Independently verified from the private GitHub remote

- Remote branch `backup/aao-recovery-20261026` resolves to commit `ff4db919c5c3074f60eda656d05d0fb93dda69cb`.
- Its Git tree has exactly **162** `data/databento/wti_aao_bulk/raw/*.dbn.zst` paths as LFS pointers and **one** `data/databento/wti_aao_bulk/derived_private/aao_cross_month_PROVISIONAL_81_months.sqlite3` LFS pointer (`size 539226112`).
- It also holds `results/analysis/wti_aao_history_feasibility/reacquisition_20261026/bulk_acquisition_manifest.json` (60,361-byte normal Git blob).
- The GitHub API verified the LFS **pointer references**, not independent download of every LFS **object body**. For complete remote-backup assurance, verify an authenticated LFS fetch from the remote and the restored hashes; the successful user's LFS push and visible pointer entries are encouraging but not equivalent to independently reading all binaries.
- Remote `main` was still commit `acf6251` with merged PR #110's separate Databento-only Bayesian experimental implementation. **Data are on the backup branch, not yet main.**

## Integration

- [PR #112](https://github.com/heri-espino/Bayesian-Uncertainty-in-WTI-APOs/pull/112) proposes to merge the recovery commits into `main`. It was checked as **mergeable**. It must be independently reviewed and **not merged without the author's authorization**.
- [PR #111](https://github.com/heri-espino/Bayesian-Uncertainty-in-WTI-APOs/pull/111) is the comprehensive research handoff and remains open. This latest addendum supersedes all earlier phrases in that PR saying the backup files do not exist **anywhere on GitHub**. They are on the backup branch, but **not** on the default branch.
- Avoid `git pull --rebase`, force pushes, resets, clean or sparse-checkout changes while local artifacts might be unpublished. Preserve the reported modified `results/analysis/wti_aao_history_feasibility/integrity/combined_manifest_audit.json` and untracked `results/analysis/massive_mechanism_map/6e23d5aabc519982/checkpoints/` before switching or cleaning branches.

## Still incomplete — paper

- 162 sources and the SQLite are backed up by GitHub LFS **pointers on the backup branch**. The source authenticity SHA256 audit passed **locally**. An independent remote LFS object download check remains desirable.
- GitHub `main` does **not** yet include these 163 data paths until PR #112 is integrated.
- The 11-step source/reconciliation replay and Databento-only reduced-form **six-benchmark pilot/full pricing experiments** are NOT proven rerun after the machine restart from these logs.
- The new Databento-only CAS manuscript `paper/jcm/databento_main.tex` has not been populated with verified new MAE/RMSE/valuation-date clustered results and figures.
- Next: merge/reconcile PR #112 with permission, verify remote LFS actual objects, check no local uncommitted result loss, run the offline replay/pilot/full six-method experiments, publish outputs and update the independent paper evidence ledger.

**Status rule:** documentation is evidence of the above **reported and remote-verified** state; do not present source recovery as equivalent to a completed 2020–2026 pricing paper.
