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

**Baseline vs new:** Previous 2,381-row/15-date Barchart and 253-row/10-date LO study is established, but **all 81-month Databento new-market experiments here are unexecuted pending re-acquisition**. No model-performance statistics are currently warranted for the expanded sample.

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

## experiment002 — contract-level Databento/Barchart settlement parity

**Question:** Can AAO options from the two vendors be identified and compared on the same contract and settlement reference date, with verified units and publication vintage?

**Method:** read `bayesian_asian_options.barchart_apo`, `aao_settlements.py` and `aao_cross_month.py` before coding; normalize publisher/exchange, native symbol, class (C/P), underlying, expiry/maturity, strike-price factor and tick units, contract multiplier and currency; recover as-of definitions and sequence/correction states. Distinguish CME `ts_ref`, publication UTC, local session date and Barchart `Time` conventions; set a time tolerance *before* looking at mismatches. Join on all dimensions, not just date. Examine examples across early 2020, 2021-02, 2024-01-26, September 2026; exclude unmatched, false symbols and later-updated vintages.

**Metrics:** source and matched date count, matched unique contracts, unique contract-dates, rejected ambiguous keys, price difference (raw and normalized), MAE/RMSE of vendor disagreement, distribution of zero/actual/theoretical and volume/OI, mismatch causes, suspect units and as-of cutoffs. Validate known older Barchart records without changing them.

**Exit:** source-level price units and exact key verified; documented consistent prices or clearly bounded differences; **date-only overlap is explicitly insufficient**. If price parity fails, stop further paper-model comparisons until corrected.

## experiment003 — causal historical pricing eligibility panel

**Question:** On which independent valuation dates do we possess all inputs available by the cutoff to price an AAO without look-ahead?

**Method:** reconstruct CME APO daily fixing calendar and the **first-nearby** CL reference futures path, realized portion of average, remaining fixings and dated forward curve; discounting curve; prior CL returns, prior-date APO IV, prior-date independent LO IV (including support/interpolation). Use strictly timestamped data availability. Preserve both a retrospective-final-target variant and a publication-vintage-eligible version; NEVER train on later settlement amendments. Use stable contracts and unique `(cutoff date, target contract)` keys. Freeze chronological fit/selection/test windows before benchmarking.

**Outputs:** canonical panel schema and column dictionary; per-year and per-expiry count funnel (raw events -> preliminary/final valid -> unique contracts -> price-scale parity -> available futures curve, rates, fixings, volatility support -> **independent eligible pricing dates**); excluded rows with reason codes; leakage checks and cutoff reproducibility tests; no unsupported use of option marks as contemporaneously tradable quotes.

**Exit:** a model-independent frozen eligible-date panel and versioned data manifest; no invented eligibility counts.

## experiment004 — reproduce and align original Barchart baseline

**Question:** What is the original 2,381-row / 15-date result on the exact Barchart panels, and what subset has direct Databento parity?

**Method:** reuse `experiments.wti_apo_empirical`, `experiments.wti_apo_date_panel`, `experiments.wti_apo_implied_volatility`, `scripts/run_extended_forward_validation` and existing checkpoints to recreate the old baseline on its original dates. Compare the replacement Databento values for **same matched contract-dates** without changing the old Barchart CSV or figure. Predeclare whether price target is retrospective vendor settlement or as-of published quote and assess dates not supported by both.

**Outputs:** old-vs-rerun Barchart metrics, vendor matched-support metrics, strict-cutoff audit, matched and unmatched date counts, dataset differences, error table and hashes. Preserve previous paper results, don't overwrite them.

**Exit:** a reproducible bridge between historical small-sample and new long-sample evidence. A different source convention must not be misdescribed as model improvement.

## experiment005 — full fixed-support pricing-method comparison

**Question:** PI vs PM versus volatility-information choice: which matters more under a frozen common Q pricing engine, and with what uncertainty?

**Predeclare estimators:** posterior-integrated historical PI, posterior-mean PM (possibly posterior-RMS sensitivity), expanding-history, rolling 63-return history, EWMA, horizon-matched GARCH(1,1), previous-date APO smile IV, and genuinely independent previous-date LO IV. All option-price predictions for a *given paired comparison* must target exactly identical option/valuation-date rows and use consistent contract/curve/discount conventions. Label Monte Carlo and Curran pricing separately; use high-precision/numerical convergence to disentangle pricing-engine error from volatility-input effects.

**Metrics:** matched N rows, N unique valuation dates, N expiry-date groups, bias/MAE/RMSE/USD per barrel, medians/quantiles, paired price differences, date-cluster plus moving/blocked-time-bootstrap confidence intervals and sensitivity to block choice. The main report must show a frozen chronological test and not retune on the test sample.

**Exit:** versioned per-date errors or sufficient secure internal research outputs plus aggregate tables, exact pricing functions, posterior diagnostics, computational seeds/config and source manifest, reproducible model comparison. **No new price-error number is known yet.**

## experiment006 — realistic liquidity, regime and settlement robustness

**Question:** Do main effects survive difficult states or rely on stale theoretical marks?

**Slices:** liquid actual-flagged and positive-volume marks, positive open interest, theoretical-flagged and zero-volume separately; 2020 turbulence, 2022 market volatility and other predeclared year bands; call/put, expiry, moneyness and IV support, already fixed percentage, near and long horizon, option with zero quoted settlement, extreme strikes and missingness. Never assume annual regime label itself proves exogenous differences.

**Tests:** paired differences on common support; groupwise N unique dates, not only option rows; stable results across exclusion thresholds and block bootstrap; diagnostic sensitivity to published settlement revision-vintage availability.

**Exit:** all exclusions justified with counts, confidence intervals and limitations; robust or explicitly nonrobust conclusions.

## experiment007 — interpretation, mechanisms and numerical stability

**Question:** Do posterior variance/conditional price curvature explain observed PI–PM, and how large is model-price posterior uncertainty? Is numerical noise adequately controlled?

**Method:** use the established synthetic mechanisms and old ten-million-path study as references; do not rerun massive simulations without a concrete diagnostic need. Audit PI–PM against curvature approximation, posterior model-price interval, Monte Carlo standard error, randomized QMC/Curran crosschecks and calibration methods. Quantify estimator/engine cross-effects and stress-test high volatility, partial fixings and unusual strike/expiry states.

**Exit:** a succinct, theoretically coherent mechanism assessment with identifiable error budgets. Avoid incorrectly treating a high correlation as methodological novelty.

## experiment008 — submission-ready JCM results and full paper audit

**Question:** Is there sufficient robust, *new* independent-date empirical evidence for JCM, and is every sentence/figure reproducible?

**Deliverables:** data-funnel table, vendor contract-specific parity, eligible-day calendar, main paired results, uncertainty/regime panels, actual/theoretical/liquidity sensitivity, numerical PI-vs-PM magnitude and intervals, reproducible figure source/manifest, expanded manuscript abstract/introduction/methods/results/limitations/discussion, clean supplement, consistent references and proper Elsevier CAS build and author guideline check. Preserve `paper/remef`, `paper/manuscript` and historical figures as fallback. JCM is **conditional**: if novelty/generalizability tests fail, retain honest science and decide if REMEF or a shorter Applied Economics Letters form is better. No simultaneous submissions.

**Exit:** finished JCM candidate PDF/source and reproducibility package with auditor signoff; author approves final submission. **Not yet done.**

## Execution ordering and handoff

The dependency path is:

    recovery -> experiment001 -> experiment002 -> experiment003
                         |-> experiment004 -> experiment005
                                           -> experiment006
                                           -> experiment007
                                           -> experiment008 -> author submission decision

The timing and exact script interfaces of **new experiments002–008** are **design requirements, not code already implemented**. Use fresh modules under `experiments/` only after inspecting pre-existing interfaces and tests, and then record actual commands/artifacts under each numbered experiment. Do not claim a result based solely on an outline. A new agent should complete the next unverified gate and push a branch/PR with full reproducibility data, updating the evidence ledger before moving on.

**Known blocker today:** original 162 AAO DBNs and full 81-month SQLite are not present in the GitHub tree. The replacement invoice, hashes, files and full out-of-sample study remain unverified. Do not run tests that assume private data are materialized until the replacement Git LFS upload is proven complete.
