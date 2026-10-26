# Complete Databento-only WTI APO paper runbook — 26 October 2026

## Scope

The author requested to finish the **Elsevier CAS manuscript from Databento
AAO source data alone**, with no Barchart option comparisons. This runbook
contains the code for the historical-volatility benchmarks, Bayesian
posterior-integration experiment, paired-date uncertainty, genuine
performance figures, and an independent Databento-only CAS manuscript.
The user will execute the heavy results and then the manuscript will
be revised to incorporate **the actual outputs**.

**Scientific caveat:** The purchased `AAO.OPT` definition and
statistics files cannot reconstruct the CME first-nearby CL futures
fixings or the CL futures curve. Under NYMEX rulebook Chapter 341,
the actual APO payoff averages these **first-nearby CL settlements**.
The new exercise uses a *reduced-form model of the terminal average*,
not the earlier canonical physical-CL-to-risk-neutral-Asian GBM model.
It is not an ex-ante forecast built without current-date option
information.

## Step 0: Data files must actually exist

The 162 source DBNs and earlier private SQLite went missing after an
unsafe sparse-checkout operation. The repo is now configured for
**Git LFS** and the replacement procedure is
`research/AAO_RECOVERY_AND_LFS_BACKUP_2026-10-26.md`.
Do not attempt the new economic experiment until:

1. All 162 recovered AAO DBNs are present and SHA256 verified.
2. The 162 files have been **committed and successfully pushed to the
   PRIVATE GitHub repo using Git LFS**.
3. The offline `python -m experiments.wti_aao_cross_month --all`
   has regenerated
   `data/databento/wti_aao_bulk/derived_private/aao_cross_month_PROVISIONAL_81_months.sqlite3`.
4. The reconstructed SQLite is also committed and pushed via LFS.

The full-history dataset contains **settlement marks**, not independently
confirmed trades. The prior run had 5,105,603 candidate marks on 1,700
reference dates. Newly re-downloaded data can contain vendor revisions,
so these are *historical comparison figures*, not assertions about the
new archive before it has been processed.

## Study design

1. **Target panel:** reconstructed latest final nonintraday exchange
   AAO marks, with native publisher+symbol and month-specific contract
   metadata (right, strike and expiry). Require price and strike
   sanity checks. The file-level latest state is retrospective; market
   availability and corrections are not fully point-in-time reconstructed.
2. **Pre-fixing only:** evaluate reference dates *before* the first
   calendar day of the option's averaging month. For partially fixed
   contracts, actual CL fixing prices would be necessary and are
   intentionally unavailable in this AAO-only study.
3. **Same-day parity anchors:** reserve seven matched actual-flagged
   call/put strikes per expiry/reference date. Fit
   `C(K)-P(K)=a-b K`, hence `D=b` and
   `E_Q[A]=a/b`. Require at least four anchors, a sufficiently wide
   strike range, plausible discount/forward and low residuals.
   **Exclude both call and put at all anchor strikes from the
   evaluation.** This avoids directly fitting any evaluation target.
   It does not eliminate contemporaneous information in other strikes.
4. **Price model:** Black-style lognormal terminal-average
   approximation, **NOT** exact Asian first-nearby pricing.
   Separate Q volatility of that approximate average from physical
   futures volatility, which cannot be measured from these source files.
5. **Historical proxy:** only earlier dates' log changes in matched
   same-expiry parity-implied average forwards. Prior mean variance is
   inverse-gamma with `alpha0=3, beta0=.16`; posterior draws=128
   by default. The P-proxy here is not first-nearby CL realized volatility.
6. **Methods on exactly the same contracts:** posterior integrated
   (PI), posterior-mean plug-in (PM), rolling 21 and rolling 63
   observation volatility, EWMA half-life=63, and previously available
   same-family AAO implied volatility. Prior IV is inverted on
   *earlier* dates from non-anchor near-ATM calls and puts.
7. **Uncertainty:** bias, MAE, RMSE on pooled matched contract dates
   and paired mean daily MAE improvement against PM, with a 95%
   valuation-day-cluster bootstrap. Distinguish actual-flagged and
   theoretical-flagged settlements. Do NOT use raw option-row count
   as an independent sample size.
8. **Period:** build lagged volatility history from 2021 onward,
   evaluate from 2023 onward and take every fifth eligible source
   reference date by default. The exact eligible source dates are
   determined by the archival records; `--date-stride 1` processes
   every eligible day.

## Execution: first inspect, then run

From Windows PowerShell at the root of the repository:

```powershell
git switch main
git pull --ff-only origin main
conda activate asian-options

python -m pytest tests/test_aao_databento_only.py -q
python paper/jcm/build_databento.py --check

# Dry run (does not access raw DBNs)
python -m experiments.wti_aao_databento_only

# Quick local pilot AFTER the 81-month SQLite and source DBNs exist:
python -m experiments.wti_aao_databento_only --execute --source-start 2022-01-01 --eval-start 2023-01-01 --date-stride 15 --max-contracts 40

# Full comparison (this is heavy but offline, no paid requests):
python -m experiments.wti_aao_databento_only --execute --source-start 2021-01-01 --eval-start 2023-01-01 --date-stride 5 --max-contracts 80

# Publication figures from actual completed outputs:
python -m scripts.plot_aao_databento_only

# Manual isolated Elsevier manuscript build (does not run experiments):
python paper/jcm/build_databento.py
```

If the pilot produces zero eligible observations, that is a
scientific exclusion report; **do not substitute synthetic results or
quietly include used anchor strikes**. Check available paired-strike
coverage, Databento strike scaling and historical parity forward
history. A summary count from the original 5.1m observations is not
enough to infer the eligible sample.

### Files generated

Public-safe aggregate outputs:

- `results/analysis/wti_aao_databento_only/method_metrics.csv`
- `results/analysis/wti_aao_databento_only/daily_metrics.csv`
- `results/analysis/wti_aao_databento_only/cluster_intervals.csv`
- `results/analysis/wti_aao_databento_only/experiment_manifest.json`
- `figures/aao_databento_only/fig06_databento_benchmark_mae.{pdf,png,svg}`
- `figures/aao_databento_only/fig07_databento_date_cluster_intervals.{pdf,png,svg}`
- `figures/aao_databento_only/fig08_databento_mae_time_series.{pdf,png,svg}`

Reproducible price-level, privately Git LFS-backed output:

- `data/databento/wti_aao_bulk/derived_private/AAO_DATABENTO_REDUCED_FORM_CONTRACT_PRICING.csv.gz`

Journal files:

- `paper/jcm/databento_main.tex`: complete CAS manuscript draft,
  but empirical results section intentionally pending actual numbers.
- `paper/jcm/build_databento.py`: compiles to
  `paper/jcm/build/databento/jcm_databento_working_draft.pdf`
  using the owner's Elsevier template; it never copies or overwrites
  the old Wiley/JFM and Barchart papers.

**Do not publish the old Barchart rankings in the new Databento-only
paper.** Once the author's log and summary files are available,
update the methods/sample counts, benchmark result table, clustered
intervals, interpretation, abstract and conclusion, and reconcile any
sample exclusion surprises. The answer on which method wins must
come from the execution, not an expectation.

Official methodological references: CME NYMEX Rulebook Chapter 341
and Databento's GLBX.MDP3 statistics documentation; see cited sources
in the manuscript's bibliography and the old paper's source notes.
