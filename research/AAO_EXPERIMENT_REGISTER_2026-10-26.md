# Sequential experiments and reproducibility contract for the extended WTI APO paper

**As of 2026-10-26**. These are the **next experiments to run**, not claims of completed Databento pricing-model research. Number them sequentially (`experiment001`, `experiment002`, ...), preserving historical named scripts under `experiments/` without rebranding earlier findings. Read the [master plan](PAPER_COMPLETION_MASTER_PLAN_2026-10-26.md) and [evidence ledger](AAO_EVIDENCE_LEDGER_2026-10-26.md).

## Common data and execution contract

For each experiment create a durable note under `research/experiments/experimentNNN/README.md` (or equivalent repository-consistent directory) containing:
- title, objective, statistical hypothesis, what is done, **why**, assumptions, units, methodological choices, git commit, executable command, conda environment/seed, source manifests+SHA256 and predeclared sample/split;
- input/output schema; target dates, contract identity, P/Q measure and information cutoff; input provenance; stage-by-stage sample attrition and failure reasons;
- numerical results (including **null results and failures**), risk flags, figures/tables with generating scripts and machine-readable aggregates, date-cluster uncertainty, computation cost;
- comparisons against frozen old baseline on **identical rows**, if feasible;
- precise interpretation and next step, unresolved issues and handoff for another agent;
- upload binary source/raw/reconstructed snapshots to private Git via LFS as appropriate; preserve generated numeric outputs and figure source in Git. Do not leave the **only** copy in ephemeral VM storage.

Use one active branch and PR per task where feasible; preserve others' concurrent work and do not merge without authorization. CI only for light tests/lint/provenance; heavy analyses and PDF/figures are manual-only. Never commit Databento API credentials or confidential DPAPI secrets.

**Baseline vs new:** Previous 2,381-row/15-date Barchart and 253-row/10-date LO study is **preserved for historical context, not used in the selected Databento-only new manuscript**. All new real-data Databento-only 81-month economic results remain unexecuted pending re-acquisition; the new experimental code was implemented by PR #110. No model-performance statistics are currently warranted for the expanded sample.

## Pre-experiment: RECOVERY (blocking, not a pricing experiment)

- **Goal:** reacquire 81 monthly windows * 2 schemas and back up everything in private GitHub.
- **Inputs:** `GLBX.MDP3` / `AAO.OPT` metadata, local `DATABENTO_API_KEY`, `scripts.aao_lfs_preflight`, quote-first `experiments.wti_databento_aao_bulk`.
- **Actions:** explicit safe cost quote; confirm 81/81 eligible; manual download with `--report-dir results/analysis/wti_aao_history_feasibility/reacquisition_20261026`, manual budget confirmation (current quote unknown); SHA256 162/162; commit/push 162 raw DBNs, manifest and later rebuilt SQLite using Git LFS. Verify remote push and LFS objects independently.
- **Exit:** persisted 162 valid DBNs, source-inventory manifest, remote LFS verification and no secrets or pending data lost to sparse checkout. **No subsequent experiment is authorized to claim source completeness before this exit.**
- **Reference:** `research/AAO_RECOVERY_AND_LFS_BACKUP_2026-10-26.md`. **Current status: NOT DONE.**

## experiment001 — 81-month source integrity and historical replay

**Question:** Does the replacement archive reproduce the historical AAO inventory and settlement-state counts? What changed by data vintage?

**Method:** manually inspect `python -m scripts.aao_replay_offline` (dry run), then `python -m scripts.aao_replay_offline --execute` after remote source backup. Existing steps perform SHA256 manifest audit, full inventory, historical coverage figure, February 2021 and June 2026 definition/stat probes, same-day as-of and alternative snapshot-date comparisons, native-symbol mapping, monthly candidate normalization, full 81-month cross-file latest-action reconciliation, raw-final-day diagnosis and Barchart *date-only* overlap. Use existing scripts, not a rewritten parallel engine.

**Required outputs:** provenance JSON (new DBN SHA256 and manifest), every test status, 81-month counts, 2019-12-31 observation status, 2024-01-26 latest-state status, diagnostic coverage figure, differences versus old 5,105,603/1,700 and 70,154,064/1,701 historic numbers; explain differences if exchange vendor revised source. Close SQLite and upload to Git LFS; aggregate JSONs and scripts committed. The coverage plot **is not new option-model accuracy**.

**Exit:** every input file verified, no silent skipped months, as-of snapshots fail closed on ambiguous identity, note complete with costs and full replay logs.

## experiment002 — Databento-only parity-anchor feasibility (pre-fixing)

**Question:** Can one identify an unambiguous set of *pre-fixing* AAO contracts and stable same-day call/put parity anchors from the archived settlement marks? This is NOT a first-nearby CL structural pricing exercise.

**Already implemented code (PR #110):** `bayesian_asian_options/src/bayesian_asian_options/aao_databento_only.py` and the runner `experiments/wti_aao_databento_only.py`, with synthetic tests `tests/test_aao_databento_only.py`. No claimed actual 81-month pricing results.

**Method:** use AAO contract definitions and latest selected settlement values, validate expiry, call/put and strike units, exclude dates on/after start of averaging month. On each same-day expiry/reference cross-section reserve preferred seven, minimum four, matched *actual-flagged* parity anchor strikes. Fit `C(K)-P(K)=a-bK`, discount D=b and expected Q terminal average `a/b`. Require positive plausible values, sufficient K span and low parity residual; exclude **both call and put** on all anchor strikes from target evaluations.

**Exit:** a documented source/contract and anchor attrition funnel, leakage check showing target strikes disjoint from anchor strikes and source-vintage/price-scale cautions. Same-day anchors imply conditional cross-sectional evaluation, **not ex-ante prediction or full CL fixing reconstruction**. Report true unique reference-day eligibility counts, or zero eligible observations if appropriate.

## experiment003 — AAO-only manual pilot with lagged volatility

**Question:** Does the existing six-model reduced-form pipeline produce scientifically valid non-anchor held-out AAO evaluations on real data?

**Runbook command (after backed-up DBNs + SQLite):**

    python -m experiments.wti_aao_databento_only --execute --source-start 2022-01-01 --eval-start 2023-01-01 --date-stride 15 --max-contracts 40

**Method:** pre-fixing only; same-day parity anchoring as experiment002; volatility from earlier reference-date changes of **parity-implied expected terminal average** (NOT P-measure CL realized volatility), inverse-gamma variance prior alpha0=3/beta0=0.16 with default 128 draws, rolling 21/63, EWMA half-life 63 and prior-date same-family AAO implied volatility. Predict **non-anchor** option values only.

**Exit:** actual run log, frozen config/git commit, dates, contract counts, benchmark feasibility, diagnostics for empty sample, bad strike scale, expiry mismatch or anchor failure; commit sufficient private and aggregate outputs. No synthetic substitution for empty/missing panels; no purchases needed.

## experiment004 — Full Databento-only six-method benchmark

**Question:** On the same eligible archive-mark subset, how do PI, PM, rolling21, rolling63, EWMA63 and `lagged_IV` compare, after accounting for volatility posterior uncertainty and date dependence?

**Runbook command (heavy, manual):**

    python -m experiments.wti_aao_databento_only --execute --source-start 2021-01-01 --eval-start 2023-01-01 --date-stride 5 --max-contracts 80

**Method:** the new `AAO.OPT` definitions and statistics only; no Barchart options, LO standard options, CL futures or Treasury external curve. Black-style **lognormal terminal-average** approximation, discount/forward from excluded current-date AAO parity anchors; no actual path-dependent first-nearby futures state. Prior volatility estimators strictly lagged. Compare on identical non-anchor rows. Keep the user-defined default every fifth eligible day, assess alternative stride 1 as sensitivity if resources permit.

**Outputs expected, NOT YET GENERATED:** `results/analysis/wti_aao_databento_only/method_metrics.csv`, `daily_metrics.csv`, `cluster_intervals.csv`, `experiment_manifest.json`, and LFS-backed `data/databento/wti_aao_bulk/derived_private/AAO_DATABENTO_REDUCED_FORM_CONTRACT_PRICING.csv.gz`.

**Exit:** number of unique eligible valuation days, row/expiry counts, actual vs theoretical split, paired bias/MAE/RMSE, paired mean daily MAE improvements, 95% valuation-day-cluster bootstrap intervals, complete source lineage and long-run logs. No claim of independent ex-ante trading forecast.

## experiment005 — Databento-only diagnostic and robustness review

**Question:** Are six-method rankings stable under actual vs theoretical settlements, zero/nonzero volume, anchor fit quality, number of strikes, near-term maturity and temporal dependence?

**Method:** predeclare slices before inspecting winners. Probe sensitivity to strike-span and anchor-count thresholds, correction-vintage ambiguity, date stride and unique-day support, posterior variance prior/horizon and 128-draw Monte Carlo error. Calculate paired metrics and bootstrap intervals with dates as units, consider serial dependence; keep only common support. The engine's `C(K)-P(K)` anchor is **same-day** option information even though tested target strike is disjoint, so language must remain conditional cross-sectional.

**Exit:** reproducible tests, exclusion funnel, actual/theoretical and liquid subsets, paired date-level error uncertainty and honest uncertainty about archive-vintage availability and zero-volume marks.

## experiment006 — Databento-only figures and CAS results

**Question:** Do the *executed* full metrics support the proposed paper conclusion and is every graphical number reproducible?

**Existing scripts:** `python -m scripts.plot_aao_databento_only`; `python paper/jcm/build_databento.py --check`; `python paper/jcm/build_databento.py` (manual). Do not run plots/build as an apparent substitute for the unfinished economic experiment.

**Planned figures:** `figures/aao_databento_only/fig06_databento_benchmark_mae`, `fig07_databento_date_cluster_intervals`, `fig08_databento_mae_time_series`, each in PDF/PNG/SVG with figure manifest.

**Manuscript:** `paper/jcm/databento_main.tex` is a separate manuscript already authored with **results deliberately pending**, not the Barchart-based adaptation `paper/jcm/main.tex`. Fill sample counts, tables, intervals, discussion, abstract, conclusion and limitations using the executed manifest only; preserve all previous JFM/REMEF/Barchart artifacts. Clearly identify terminal-average Black approximation and same-date anchoring, not the exact CME first-nearby-CL structural payoff model.

**Exit:** accurate independently cross-checked manuscript and figure/table source map, compiled CAS working draft, with no unrun results or transferred old Barchart rankings.

## experiment007 — Optional independent Barchart/LO/CL research extension (NOT required)

**Scope:** the earlier Barchart APO/CL and LO IV structural research survives in the repository, and deeper cross-vendor or structural work may be valuable **as a separate branch/project or future study**. It is **not required to finish the user-selected Databento-only JCM manuscript** and must not be quietly inserted into it.

If explicitly pursued: align Databento/Barchart native contract/right/strike/expiry/reference date/vintage/currency and settlement price units; reconstruct true first-nearby CL fixings and forward curves, date-specific rates and earlier-date independent LO IV; run full ex-ante structure as a **separate estimand**. Record independent eligibility dates, liquidity and robustness. Do not falsely compare the old structural pricing losses directly with the new AAO-only reduced-form errors as if instruments, inputs and targets were identical.

**Exit:** clearly separated external validation/research report if requested; not a paper blocker.

## experiment008 — Final scientific review and author submission decision

**Tests:** verify source/derived LFS completeness and model-output hashes; document all required contracts, source/revision times, good/bad parity, every actual/theoretical and unique-day denominator, previous-date volatility cutoffs, matched benchmark support and cluster bootstrap; reproduce every figure/table; inspect JCM actual guidelines; ensure no unsubstantiated originality, arbitrage or forecasting claims. Compare against the independent [verification protocol](AAO_AGENT_VERIFICATION_PROTOCOL_2026-10-26.md).

**Decision:** send the *Databento-only* JCM article only if the actual results are substantive, correctly presented and author approved; retain REMEF and Wiley/JFM alternatives and all historical data. Never submit identical work simultaneously.

**Exit:** complete paper/source/figures/reproducibility packet and author signoff. **Currently NOT complete.**

## Execution ordering and handoff

**Primary user-selected path:**

    recovery + private LFS source backup
      -> experiment001 source replay
      -> experiment002 parity-anchor feasibility
      -> experiment003 smaller AAO-only pilot
      -> experiment004 full 6-way reduced-form comparison
      -> experiment005 actual/theoretical, vintage and time-uncertainty robustness
      -> experiment006 new figures and Databento-only JCM manuscript
      -> experiment008 independent verification + author's submission decision

**experiment007** is optional earlier Barchart/LO/CL cross-provider *separate research*, **not a prerequisite or source in the Databento-only manuscript**. All new heavy experiments remain unexecuted as of this handoff; PR #110 implemented the source code, synthetic tests and manuscript template. Read `research/AAO_DATABENTO_ONLY_PAPER_RUNBOOK_2026-10-26.md` for exact existing commands and outputs. Do not claim a result based solely on existing code.

