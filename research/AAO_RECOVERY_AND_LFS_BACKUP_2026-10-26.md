# AAO data-loss incident, full replacement, and private Git LFS backup

**Priority: restore and BACK UP the purchased history; only then rebuild
the science.** The author explicitly wants original DBN files and the
reconstructed private SQLite committed to the **private GitHub repo**
`heri-espino/Bayesian-Uncertainty-in-WTI-APOs`, via Git LFS.

## Incident record — do not repeat

On October 26, 2026, after successful offline processing of the
81-month Databento `AAO.OPT` dataset, an assistant instructed the
author to run `git sparse-checkout add data/csv` in the local Windows
checkout. At that time, `data/databento/` was omitted from the sparse
checkout, and the DBN files and private SQLite database were ignored
by Git and had **never been pushed** to GitHub. The author subsequently
found **the entire `data/databento` folder missing**. The Recycle Bin
was empty, no `winfr` program was installed, and only `C:` was
available. The timing is consistent with an unsafe sparse-checkout
change removing ignored local files, but no definitive deleted-file
forensics exist. The assistant's instruction failed to protect the
data and was unsafe.

**Nonnegotiable safety rule:** Never alter sparse checkout, reset,
clean, prune, reclone, change branches destructively, or automatically
delete ignored directories if there are locally purchased/generated
data files that have not already been verified as pushed to Git LFS.
`git status` does not protect ignored files.

Confirmed **before disappearance**: 162 SHA256-verified compressed
DBNs (81 continuous months; two schemas), with **USD 17.49357489
quoted** across original acquisition ledgers. Offline analyses had
already built a `5,105,603`-candidate cross-month SQLite state and
reported 1,700 selected CME reference dates. The missing date
2024-01-26 had 7,868 latest preliminary keys. Prior research outputs
and reports do **not** replace the raw data or SQLite database.

## What is versioned now

The repository's `.gitattributes` tracks:
- `data/databento/wti_aao_bulk/raw/*.dbn.zst`
- `data/databento/wti_aao_bulk/derived_private/*.sqlite3`
- `data/databento/wti_aao_bulk/derived_private/*.csv.gz`

via **Git LFS**, and `.gitignore` explicitly allows the named
81-month source DBNs and full-history database. Mutable `.sqlite3-wal`
and `.sqlite3-shm` are not committed. The tracked
`data/databento/wti_aao_bulk/README.md` is a permanent
sparse-checkout anchor. The repository's GitHub API confirms it is
**private**. However, **tracking configuration is not a backup**:
the 162 DBNs and reconstructed SQLite are not yet recovered or pushed.

GitHub LFS storage quotas and per-file limits depend on the account.
A rejected LFS push means no remote backup. Do not claim success until
the upload completes and LFS pointers/objects are confirmed.

## Step 1 — Prepare the worktree **before any replacement download**

In the user's Windows PowerShell and `asian-options` environment:

```powershell
git switch main
git pull --ff-only origin main
git lfs install

# Crucial: INCLUDE the future paid-data directory BEFORE it exists locally.
git sparse-checkout add data/databento/wti_aao_bulk

# Verify Git LFS, sparse-checkout anchor and ignore exceptions.
python -m scripts.aao_lfs_preflight
```

Expected `ready: true`, `source_files_currently_present: 0`,
`expected_source_files: 162`. The **0** is expected before
reacquisition. If not ready, stop. No paid requests may proceed.

Once data returns, **do not run any sparse-checkout commands again**
until the full Git LFS push succeeds. Do not move raw data to a
temporary untracked/ignored path inside the repository.

## Step 2 — Quote first, then download all 81 months

The existing source `experiments.wti_databento_aao_bulk` uses
`GLBX.MDP3`, parent symbol `AAO.OPT`, schemas
`definition` and `statistics`, January 2020 through September
2026 inclusive. It performs cost/record metadata checks in quote mode,
and downloads/resumes source files in download mode.

**IMPORTANT: use a NEW recovery report directory.** The old
`bulk` and `bulk_feb2021` ledgers describe the now-missing
original files. Reusing either old report directory makes the
downloader refuse to continue rather than double-charge or silently
overwrite the prior audit history.

```powershell
$recovery = 'results/analysis/wti_aao_history_feasibility/reacquisition_20261026'

# This step makes metadata requests only; no provider timeseries download.
python -m experiments.wti_databento_aao_bulk --mode quote --report-dir $recovery --max-budget-usd 40
```

**Inspect `estimated_cost_usd` and `eligible_months` before the
billable operation**. The old quoted amount US$17.49 is an historical
estimate, not a new price or entitlement. The original downloader's
safety gate enforces `max_budget_usd <= 40` and
`estimated total <= 80% of that ceiling` (US$32 at a US$40 max).
It will refuse to buy if the quote exceeds the gate or eligibility
is incomplete. The author has requested full replacement, but the
actual Databento cost must still be displayed before proceeding.
A billable download is never triggered by push, CI, or any
automatic workflow:

```powershell
# Billable command — run only after inspecting the quotation above:
python -m experiments.wti_databento_aao_bulk --mode download --report-dir $recovery --max-budget-usd 40 --confirm-budget-usd 40
```

The downloader reuses already acquired chunks if interrupted,
verifies their hashes and errors on untracked/partial files. If a
download aborts, **do not delete any partial data blindly**; inspect
its error and resume safely. No automated paid commands run in CI.

## Step 3 — Verify all 162 files, then upload the originals to GitHub

```powershell
$manifest = 'results/analysis/wti_aao_history_feasibility/reacquisition_20261026/bulk_acquisition_manifest.json'

python -m scripts.aao_lfs_preflight --require-complete
python -m scripts.audit_aao_manifests --manifest $manifest

# Stage the compressed source files using Git LFS; do NOT stage secrets.
git add -- data/databento/wti_aao_bulk/raw
git add -- $manifest
git diff --cached --stat

# Confirm that the staged source files are LFS entries.
git lfs ls-files

git commit -m "Back up 81 months of Databento AAO source data using LFS"
git push origin main
```

**The push is a required outcome**, not a best-effort extra. Git LFS
uploads the original file bodies as LFS objects and stores pointers in
normal Git. If authentication, quota, or file-size policy prevents
the push, **stop**; do not change sparse checkout or consider the
originals safely backed up. Verify at least 162 LFS DBN objects, the
Git remote origin, and a clean status. If large, the push may incur
GitHub LFS storage/bandwidth charges.

## Step 4 — Rebuild every previously run offline diagnostic

The manual-only runner is **dry-run by default** and contains the
prior historical check list: SHA256 file audit, full inventory,
coverage figure, two sample-month native ID probes,
event/publication-date comparison, daily snapshot comparison,
native symbol matching, correction-aware sample-month candidate
selection, full 81-month cross-file SQLite reconciliation, and the
final reference-date/Barchart-date quality audit.

```powershell
python -m scripts.aao_replay_offline
python -m scripts.aao_replay_offline --execute
```

The second command is **heavy local computation**, not a paid market
download. It rebuilds
`data/databento/wti_aao_bulk/derived_private/aao_cross_month_PROVISIONAL_81_months.sqlite3`
and the aggregate reports. Old data counts may differ because the
new acquisition may include vendor updates; document any discrepancy
rather than forcing historical counts to match.

## Step 5 — Git LFS-back up the SQLite analysis state too

Ensure the SQLite processing finished and closed the database; do
not stage a live SQLite write-ahead log. Then:

```powershell
git add -- data/databento/wti_aao_bulk/derived_private/aao_cross_month_PROVISIONAL_81_months.sqlite3
git add -- results/analysis/wti_aao_history_feasibility
git lfs ls-files
git diff --cached --stat
git commit -m "Back up AAO cross-month research panel and diagnostics"
git push origin main
```

If no new files were produced, `git commit` may report a clean
working tree; that is not an error. **Never call the data backed up
until the Git LFS push has succeeded.**

## Step 6 — Resume actual scientific comparisons

All the above diagnostics investigate data identity and correctness,
**not** Bayesian price-prediction skill. Only after the raw/derived
datasets have been backed up:

1. Match Barchart `Latest` quotes and Databento AAO final marks by
   **reference date, contract expiry, strike and call/put**; check
   price display scale, units and settlement definitions.
2. Link eligible CL forward/fixing prices, discounting and
   *strictly lagged* APO/LO IV inputs, with a frozen chronological
   test-date eligibility funnel.
3. Run prior-date PI/PM and historical volatility benchmarks on
   identical eligible rows; keep actual and theoretical settlements
   separate and use date-block uncertainty.
4. Generate the performance figures and amend the Elsevier CAS JCM
   paper only after numerical experiments are finished.

**Do not rerun paid downloads for repeated data diagnostics.** No
automated push-triggered heavy figure/paper jobs are needed.
