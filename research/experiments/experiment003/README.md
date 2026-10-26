# First real Databento-only AAO experiment — manual pilot

**Start:** after the user-approved integration of data PR #112 and documentation PR #111, both of which passed their CI. The 162 DBN LFS pointers, 81-month source manifest and reconstructed SQLite are now on `main`. The user's SHA256 audit verified all 162 sources locally. This is **not** proof that the six-method pricing model has produced real-data results yet.

## Model

The current study is `experiments/wti_aao_databento_only.py`, the **reduced-form Databento-only** Black lognormal terminal-average approximation with same-date disjoint AAO put/call parity anchors. It uses prior reference-date volatility estimates (Bayesian PI, PM, rolling21, rolling63, EWMA63 and lagged AAO IV). No Barchart, LO, CL, rate-curve data, provider API or true first-nearby CL fixing path is used. Thus the valuation error is **conditional cross-sectional**, not a fully independent ex-ante futures-price forecast.

## Pilot, proposed predeclared design

- Source information starts 2022-01-01.
- Eligible pricing dates start 2023-01-01, with inclusive end 2023-06-30.
- Every 15th candidate source date, up to 40 non-anchor option contracts per expiry; 99 date-level bootstrap resamples.
- **Dates before 2023 are deliberately retained** in the volatility training history. The new `--eval-end` bounds the pilot without using a misleading `--max-dates` that could exclude every evaluation date.
- `--execute` only, explicitly requested by the author; dry run is default otherwise.

## Preferred run: manually dispatch GitHub Actions

Only the **manual** workflow `.github/workflows/aao-databento-only-manual.yml` can trigger the heavy job (`workflow_dispatch`, **no push or PR trigger**). After its PR is merged into `main`, visit **Actions → aao-databento-only-manual-study → Run workflow**. Choose branch `main`, `scope=pilot`. This executes from the exact selected Git ref and checks out LFS binaries in an ephemeral runner. The job first requires 162 local files and a passing SHA256 manifest audit, then executes the synthetic tests and the pilot, then uploads **only specified aggregates and figures** as a 30-day GitHub Actions artifact with the commit SHA in its name. **No automatic commit, push or vendor purchase.**

A failed pilot will attempt to upload `eligibility_failure.json` with aggregate reasons. Do not weaken filters merely to fabricate performance.

## Alternative: Windows PowerShell

The user's worktree previously had a modified `combined_manifest_audit.json` and untracked synthetic checkpoints: **do not reset/clean or change sparse checkout**. Preserve local work. Once remote backup and code have been verified and a clean safe pull can occur:

```powershell
conda activate asian-options
git fetch origin
git pull --ff-only origin main
python -m scripts.aao_lfs_preflight --require-complete
python -m scripts.audit_aao_manifests --manifest results/analysis/wti_aao_history_feasibility/reacquisition_20261026/bulk_acquisition_manifest.json
python -m pytest tests/test_aao_databento_only.py tests/test_aao_databento_paper.py -q
python -m experiments.wti_aao_databento_only --execute --source-start 2022-01-01 --eval-start 2023-01-01 --eval-end 2023-06-30 --date-stride 15 --max-contracts 40 --bootstrap 99
```

**Git is source of truth:** If run on Windows VM, create a task branch and commit/push relevant aggregate outputs and (if complete) private price-level data under `data/databento/wti_aao_bulk/derived_private/` with LFS. Never overwrite the only raw source, never commit credentials and do not auto-commit from CI. On GitHub Actions, download the 30-day artifact and integrate its machine-readable results through a reviewed PR; a GitHub Actions artifact is temporary storage, **not** the final durable research record.

## Exit requirements

1. `n_priced_dates > 0`; quote and anchor eligibility documented; if none, preserve failure report and investigate instrument strike scale/expiry.
2. All six methods evaluated on the same non-anchor option rows.
3. `method_metrics.csv`, `daily_metrics.csv`, `cluster_intervals.csv`, `experiment_manifest.json` captured with commit SHA.
4. Uncertainties calculated by paired valuation-day clustering, not 5.1m independent marks; actual/theoretical flags distinguished.
5. The full heavy comparison is permitted only after reviewing pilot results, then `scope=full` manually generates both numerical results and fig06/fig07/fig08 under a separate artifact.
6. Finish `paper/jcm/databento_main.tex` **only after** actual results; preserve original Barchart/LO/JFM and REMEF manuscripts.

**As of creating this workflow, no real market pilot was dispatched or executed by the assistant.** Never state that it passed until a real workflow run and artifacts confirm it.
