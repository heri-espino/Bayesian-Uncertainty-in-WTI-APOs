# AAO historical archive — Git LFS-backed private repository

**This directory is intentionally tracked in the private Git repository.**

- `raw/aao_definition__YYYY-MM-DD__YYYY-MM-DD.dbn.zst`
  and `raw/aao_statistics__YYYY-MM-DD__YYYY-MM-DD.dbn.zst` are **162
  expected compressed source files** (81 source months × 2 schemas).
- `derived_private/aao_cross_month_PROVISIONAL_81_months.sqlite3` and
  optional `derived_private/AAO_CANDIDATES_NOT_VALIDATED_*.csv.gz`
  hold generated local contract-level research data.
- Binary files use **Git LFS**; `.gitattributes` and `.gitignore`
  explicitly allow the approved paths.

**Important — prior data-loss incident:** The 162 source files and
private SQLite disappeared after a sparse-checkout change while the
files were Git-ignored and not uploaded. Never run `git sparse-checkout
set`, `git sparse-checkout disable`, `git clean` or `git reset --hard`
before verifying all source data have been committed AND pushed as
Git LFS objects. `git status` alone does not list ignored files.

This tracked README keeps the directory in versioned Git and provides a
visible sparse-checkout anchor even before the reacquired files are
uploaded. When using sparse checkout, first **include**
`data/databento/wti_aao_bulk`, before any paid download.

**Do not infer that any binary files have been backed up simply because
this README is present.** Confirm `git lfs ls-files`, successful
`git push` and remote LFS storage verification.

See `research/AAO_RECOVERY_AND_LFS_BACKUP_2026-10-26.md` for the
approved quote-first reacquisition, audit, Git LFS push, and offline
experiment replay procedure.
