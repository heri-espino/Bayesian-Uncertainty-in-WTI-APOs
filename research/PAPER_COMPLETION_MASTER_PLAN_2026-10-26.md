# WTI Average Price Options — canonical project-completion plan

**Status date:** 2026-10-26. **Repository:** `heri-espino/Bayesian-Uncertainty-in-WTI-APOs` (private). **Purpose:** finish the **user-selected Databento-only** Bayesian WTI AAO article using the restored 81-month exchange settlement archive. Preserve the earlier Barchart/LO structural work separately; it is NOT required as a pricing input or empirical comparison in the new article. This is the canonical current handoff. Historical checkpoints must remain intact, but must not supersede this document.

**Companion files:** [Numerical evidence ledger](AAO_EVIDENCE_LEDGER_2026-10-26.md), [sequential experiment register](AAO_EXPERIMENT_REGISTER_2026-10-26.md), [independent-agent verification protocol](AAO_AGENT_VERIFICATION_PROTOCOL_2026-10-26.md), [recovery and LFS procedure](AAO_RECOVERY_AND_LFS_BACKUP_2026-10-26.md), [agent rules](../AGENTS.md).

## 1. Research mission and motivation

**Central question:** When does integrating uncertainty about volatility into risk-neutral WTI Asian-option prices materially change model values, and when does the *volatility input* matter much more?

The original paper tested Bayesian posterior integration versus a posterior-mean volatility plug-in and the economic importance of historical versus earlier-date option-implied volatility. Synthetic simulations characterized the theoretical effect. The original market study contained **2,381 option/valuation-date holdouts on 15 distinct dates** (seven expiries), plus **253 independent-LO-based comparisons on 10 dates**. These are correlated contracts within dates, NOT thousands of independent temporal experiments.

The author therefore acquired historical AAO data to test stability across **many reference dates, strikes and expiry months** rather than inflating the correlated cross-sectional row count. The NEW manuscript is explicitly a **Databento-only reduced-form, pre-fixing, same-day parity-anchored evaluation**, not a fully independent forward CL-price forecasting study. This is the potential new contribution for a commodity-derivatives journal.

Instruments and sources must remain distinct:
- **AAO** (CME Globex) / **AO** (clearing): WTI Average Price Options. These are the **pricing targets**. Target payoff depends on the arithmetic average of daily settlements of first-nearby **CL** WTI futures during the specified calendar month, with exact contract schedule and partial fixings.
- **CL**: WTI underlying futures, essential for the **old structural pricing model**, but **not contained in purchased AAO-only files** and **not used in the new reduced-form experiment**. Do not claim the new model reconstructs exact CL fixings/rolls.
- **LO**: ordinary WTI futures options used by the **old independent external validation**; **not used in the selected new AAO-only benchmark**.
- **Barchart**: original JAO/APO history and prior paper benchmarks, **NOT used for targets, inputs, comparison tables or figures of the selected new Databento-only paper**. Cross-vendor parity remains optional separate research.
- **Databento**: GLBX.MDP3 CME AAO definitions and statistics, historically 2020-01-01 to 2026-10-01 exclusive (81 months). Different providers require explicit contract/date/scale matching.

## 2. Mathematics and scientific interpretation

Let d denote valuation cutoff, K strike, T maturity, A the correct average of contract-specific CL daily settlements, and D(d,T) a dated discount factor. Under a stated risk-neutral measure Q and volatility parameter sigma:

    C_Q(sigma; d,K,T) = D(d,T) E^Q[(A-K)^+ | F_d, sigma].

Let p(sigma | D_<d) be a posterior estimated from permitted historical information strictly before the volatility-estimation cutoff. The **posterior-integrated** price is PI = E_post[C_Q(sigma)] and the **posterior-mean volatility plug-in** price is PM = C_Q(E_post[sigma]). For a concentrated posterior and regular conditional pricing function,

    PI - PM ~= (1/2) C_Q''(mean sigma) Var_post(sigma).

**The correction can have either sign**; do not confuse this often small *posterior mean-price correction* with the (potentially much larger) **posterior dispersion of model prices**. A high synthetic simulation count does not establish a new theory.

Historical drift fitted under the physical measure P must NOT be inserted into Q option prices. Price under Q, specify the maintained one-factor common Brownian futures assumption, discounting, CL curve and volatility mapping. Do not interpret superior earlier-option-IV pricing as identified Q structural dynamics, variance risk premiums, an executable hedging strategy, or arbitrage profits. Foundational documents: `research/REFRAMING.md`, `research/EMPIRICAL_WTI_DESIGN.md`, `research/REVIEWER_REVISION_2026-09-29.md`, `paper/manuscript/sections_short/02_posterior_pricing.tex`.

## 3. Timeline: completed historical work vs what exists NOW

1. **Before October 2026:** Built Bayesian/MH inference, Q Asian option pricing engine, Curran and Monte Carlo numerical benchmarks, synthetic mechanism study, first-nearby CL reconstruction, Barchart market panel, strict-forward APO IV and independent LO IV tests, liquidity/partial-fixing/expiry robustness, publication figures and prior manuscript. These survive in the repository and should be preserved.
2. **Journal reconsideration:** Wiley/JFM long and concise sources preserved in `paper/manuscript/`. REMEF bilingual Word draft preserved in `paper/remef/`. New Elsevier CAS v2.4 provisional draft created at `paper/jcm/`. **Conditional ambitious target:** *Journal of Commodity Markets*, not a submitted article. REMEF is fallback; Applied Economics Letters could require a substantially shorter paper. Read `docs/journal_strategy.md`.
3. **2026-10-20–25 Databento availability:** A parent-only `symbology.resolve` check was inconclusive. A corrected metadata record-count/cost check found AAO data. Original transfer completed 80 of 81 months, then separately acquired February 2021 after a metadata gateway 504. Total **162 compressed DBN chunks** (`definition` + `statistics` for 81 months), with **USD 17.49357489 combined historical *quote*, not proven invoice**. Successful VM SHA256 verification of 162 files was reported.
4. **2026-10-25–26 historical offline diagnostic execution:** Full 81-month inventory, native symbol identity, alternative event-day vs CME-reference-day matching, within-month latest action, cross-month replay, and annual price-bin diagnostics were run on the user's VM. Main candidate counts are in the evidence ledger. **These analyses are NOT the expanded forward-test pricing experiments.**
5. **2026-10-26 Barchart checkout problem:** Original CSV option history under `data/csv/` was initially absent from the Windows sparse checkout; `git sparse-checkout add data/csv` restored it and the user verified the exact JAO CSV with `Test-Path = True`. An ensuing date-overlap audit was blocked by the missing SQLite; the earlier report saying `available: false` was STALE. **No up-to-date numerical Barchart-AAO overlap or price-parity result exists.**
6. **2026-10-26 critical data-loss incident:** The entire **ignored, unbacked-up** `data/databento/` directory was missing after an unsafe earlier assistant-recommended sparse-checkout operation. Original source DBNs and derived 81-month SQLite are no longer present in the user's observed Windows repo; Recycle Bin empty. Timing is consistent with sparse-checkout cleanup but exact file-deletion mechanism is **not forensically proven**. The assistant should have protected the data before suggesting Git changes. The user's explicit decision is **back up all replacement DBNs AND rebuilt SQLite in PRIVATE GitHub via LFS**. PR #109 created the Git LFS allowlist, backup instructions, preflight and offline replay scripts. **No replacement source files, replacement invoice, complete new manifest, or uploaded 81-month SQLite have yet been verified**.
7. **This handoff:** Documents goals, achieved empirical evidence, current loss/recovery state and experiment acceptance gates. **Documentation is not proof that an experiment has run.**

## 4. Dataset state and strict interpretations

**Original historical inventory (author-provided VM result):** 81 months, 70,154,064 combined raw records, 13,412,045 settlement events, 5,899,096 raw final settlement events (4,027,696 flagged actual, 1,871,400 theoretical), 1,701 distinct CME reference dates on which at least one raw final event existed.

**Historical cross-month latest-state reconciliation:** 5,157,894 tentative publisher/native-symbol/reference-date keys; 71,145 keys seen in more than one file month; 52,290 latest preliminary; 1 latest invalid-price key; no latest deleted/intraday-final/ambiguous-tie keys; **5,105,603 provisional final nonintraday candidate keys** (3,299,087 actual-flagged and 1,806,516 theoretical-flagged); **1,700** distinct reference dates. The selected dates include **2019-12-31** (4,706 candidates), so just **1,699** are within 2020–2026. This does NOT imply 1,699 independent eligible pricing dates. Some 190,064 latest updates occur in file months different from their reference months; these are not all proven exchange corrections.

**One-date discrepancy resolved at aggregate latest-state level:** 2024-01-26 appeared in raw final events (2 events), but all 7,868 latest candidate keys were preliminary, with zero surviving finals. Individual event revision lifecycles have not been traced. Retain an explicit two-definition denominator (raw final-event dates vs selected final latest-state dates), never force preliminary prices into the final target.

**Instrument identity:** the original sample monthly probes found native mapped symbols and plausible outright identities, but month-local `instrument_id` reuse, different UTC publication dates, `ts_ref`, exchange settlement vintages, put/call strikes, strike scaling, multiplier, contract lifecycle and as-of timing must still pass **contract-level** checks. A raw final settlement flag is NOT an executable trade or independent model validation.

**Remote GitHub today:** contains `data/databento/wti_aao_bulk/README.md`, `.gitattributes` and tooling, but not 162 raw `*.dbn.zst`, not the full derived SQLite, and not `results/analysis/wti_aao_history_feasibility/` manifests. These file paths were referred to in older documentation, but direct remote-tree inspection found them missing. Old manuscript and versioned results remain. New acquisition must create/push its **own** source manifest. Do not call a configured LFS pattern a completed backup.

## 5. User-selected Databento-only completion path (PR #110 already merged)

**Author decision and current main-code boundary:** `research/AAO_DATABENTO_ONLY_PAPER_RUNBOOK_2026-10-26.md` is the operational authority for the **primary new manuscript**. `experiments/wti_aao_databento_only.py`, `bayesian_asian_options/src/bayesian_asian_options/aao_databento_only.py`, `scripts/plot_aao_databento_only.py`, `paper/jcm/databento_main.tex`, and `paper/jcm/build_databento.py` already exist, with synthetic tests. They are **implemented but their heavy real-data results have not been run**. The previous `paper/jcm/main.tex` and Barchart/Wiley/REMEF versions remain separate; do not overwrite them.

**Gate 0 — Reacquire/backup (blocking):** follow `research/AAO_RECOVERY_AND_LFS_BACKUP_2026-10-26.md`; obtain fresh 81/81-month metadata quote; manually retrieve and SHA256 audit exactly 162 AAO DBNs, commit/push through private Git LFS, then reconstruct and push the closed SQLite. Prior VM counts are historical and cannot substitute for source re-verification. Never allow a destructive sparse-checkout or unchecked data deletion.

**Gate 1 — Replay 81-month AAO source identity:** manually execute the 11-step offline quality runner after LFS backup. Verify target option **put/call, strike, expiry, contract factor**, as-of definitions, settlement vintages and actual vs theoretical marks. Observe `ts_ref` vs publication dates. Do not confuse 5.1m candidate marks with forward-eligible model targets.

**Gate 2 — AAO-only reduced-form pilot:** the purchased AAO definition/statistics do **not** include first-nearby CL fixings or a true CL futures curve. The new experiment models the **terminal arithmetic average** as approximately lognormal (Black-style), a separate econometric estimand from the old structural CL Asian GBM. Restrict to dates **before the averaging month (pre-fixing)**. On each target reference date, reserve disjoint actual-flagged matched C/P strikes (seven preferred, minimum four) to estimate `C(K)-P(K)=a-bK`, `D=b`, and `E_Q[A]=a/b`. **Remove all anchor strikes, both calls and puts, from evaluation targets.** Same-day market parity information is used: do **not** call this strictly ex-ante forecasting or structurally exact Asian valuation. Check strike/expiry/discount scale and parity residuals, rejecting failures with reasons.

**Gate 3 — Volatility and comparison:** fit posterior volatility to **strictly earlier** reference dates' parity-implied average-forward changes (NOT physical CL return volatility). Prior is inverse-gamma alpha0=3, beta0=0.16; default posterior draws=128. Compare **PI, PM, rolling21, rolling63, EWMA63 and prior-date AAO implied volatility (`lagged_IV`)** on exactly the same held-out **non-anchor** contract marks. No Barchart, CL, Treasury or LO inputs. Volatility inputs are lagged, but the same-day forward/discount anchor means this remains a **conditional cross-sectional** price evaluation, not fully independent prior-market-state price prediction.

**Gate 4 — Full Databento-only run and inference:** the runbook proposes historical source data from 2021 onward, evaluation from 2023 onward, every fifth eligible reference day by default. First run the predeclared smaller pilot; if no eligible rows, retain failure/attrition output instead of silently relaxing rules. Then manually run full dataset (`--execute`); report paired biases, MAE/RMSE, **daily paired mean MAE improvement over PM**, 95% valuation-date-cluster bootstrap, actual-flagged vs theoretical-flagged settlement distinction and explicit unique evaluation day counts. Findings depend on real execution: **no new MAE/RMSE is known**.

**Gate 5 — Figures and standalone manuscript:** only after metrics exist, run `scripts.plot_aao_databento_only` to generate `fig06_databento_benchmark_mae`, `fig07_databento_date_cluster_intervals`, and `fig08_databento_mae_time_series` plus a source manifest. Fill the deliberately pending result section of `paper/jcm/databento_main.tex` using `results/analysis/wti_aao_databento_only/{method_metrics.csv,daily_metrics.csv,cluster_intervals.csv,experiment_manifest.json}`. Build using `python paper/jcm/build_databento.py --check` then manual build. Keep original `paper/jcm/main.tex`, all Wiley/JFM, REMEF and old figures untouched. This Databento-only paper's main empirical interpretation MUST disclose same-date parity anchoring, archived latest-mark revisions and lack of structural first-nearby CL input.

**Optional separate research, NOT blockers to new paper:** contract-level Databento-vs-Barchart parity, external LO volatility transfer, first-nearby CL structural Q pricing, liquidity and full ex-ante forward validation. These can support a future structural extension or alternative paper; never insert their older Barchart results into the new Databento-only CAS manuscript or claim they are part of its implemented six-way benchmark.

**Exact commands and restrictions** appear in `research/AAO_DATABENTO_ONLY_PAPER_RUNBOOK_2026-10-26.md`; the sequential execution and evidence protocol appear in the experiment register. Heavy runs manual-only, no new paid requests in the benchmark suite, no invented paper numbers.

## 6. Proposed manuscript argument, not a preordained result

Hypothesis H1: posterior mean-price integration adjustment is governed locally by posterior variance and Q-price curvature (sign unrestricted).

Hypothesis H2: economically relevant posterior model-price uncertainty may be much larger than its associated PI–PM point correction.

Hypothesis H3: option-informed strictly prior volatility can outperform historical alternatives on matched forward-eligible AAO marks, but the size and robustness can vary by source, time regime, liquidity and volatility estimator.

Hypothesis H4: improved sample depth allows meaningful inference across more **independent dates**, not because 5.1 million option marks provide 5.1 million independent errors.

New empirical evidence should be distinguished from numerical mechanism proof, econometric model identification, and market executability. Reject/rewrite any hypothesis the data do not support.

## 7. Databento-only paper and preserved earlier figures

**Selected new article:** `paper/jcm/databento_main.tex`, not the earlier Barchart CAS adaptation `paper/jcm/main.tex`. The Databento-only draft and `paper/jcm/build_databento.py` exist, but its **new empirical result section is intentionally pending** until the heavy AAO-only run is completed.

**Planned figure artifacts from actual model outputs only:** `figures/aao_databento_only/fig06_databento_benchmark_mae.{pdf,png,svg}`, `fig07_databento_date_cluster_intervals.{pdf,png,svg}`, `fig08_databento_mae_time_series.{pdf,png,svg}`, with manifest. New tables: actual/theoretical-flagged evaluation funnel, source date and expiry counts, same-support PI/PM/rolling21/rolling63/EWMA63/lagged_IV bias MAE RMSE, valuation-day clustered paired intervals and sensitivity to archive revisions or anchor quality. Do not produce pretend figures when the data/model have not run.

**Old separate papers and figures retained:** `figures/publication/fig01_mechanism_map`, `fig02_historical_vs_apo_implied_volatility`, `fig03_forward_q_cluster_bootstrap`, `fig04_numerical_identification`, and the `ten_million/` variants. They describe a different Barchart/CL/LO empirical design and are **not** figures of the new Databento-only manuscript.

## 8. Canonical repo entry points and agent collaboration

| Purpose | Canonical path |
| --- | --- |
| Autonomous agent rules | `AGENTS.md`; `research/AI_HANDOFF.md` |
| Current scientific state | **This file** plus `research/AAO_EVIDENCE_LEDGER_2026-10-26.md` |
| Sequential next experiments | `research/AAO_EXPERIMENT_REGISTER_2026-10-26.md` |
| Independent verification | `research/AAO_AGENT_VERIFICATION_PROTOCOL_2026-10-26.md` |
| Incident, full recovery, Git LFS | `research/AAO_RECOVERY_AND_LFS_BACKUP_2026-10-26.md`; `scripts/aao_lfs_preflight.py` |
| Manual acquisition | `experiments/wti_databento_aao_bulk.py`; `experiments/wti_databento_aao_feasibility.py` |
| Source integrity/audits | `scripts/audit_aao_manifests.py`; `scripts/aao_replay_offline.py`; `experiments/wti_aao_*.py` |
| Native identity and cross-month engine | `bayesian_asian_options/src/bayesian_asian_options/aao_cross_month.py`; `aao_settlements.py` |
| Barchart reader / originals | `bayesian_asian_options/src/bayesian_asian_options/barchart_apo.py`; `data/csv/` |
| Existing forward pricing/evaluation | `experiments/wti_apo_empirical.py`; `wti_apo_date_panel.py`; `wti_apo_implied_volatility.py`; `scripts/run_extended_forward_validation.py` |
| Historical empirical and synthetic results | `results/analysis/wti_extended_forward/`; `results/analysis/wti_forward_q_validation/`; `figures/publication/`; `results/publication_experiment_summary.csv` |
| New AAO output target (missing remotely now) | `results/analysis/wti_aao_history_feasibility/` |
| Manuscripts | `paper/jcm/` (conditional JCM); `paper/remef/`; `paper/manuscript/` |
| Journal decision | `docs/journal_strategy.md` |
| Team tracking | [GitHub Issue #90](https://github.com/heri-espino/Bayesian-Uncertainty-in-WTI-APOs/issues/90) |

Do not create additional market-data purchases or new model claims by following old dated screenshots blindly. Current work must be recorded in **sequential** `experiment001`, `experiment002`, etc. logs as described in the register, including why, execution, inputs, raw/derived artifacts, results, failures and next steps. Preserve tests and figures and push important artifacts to the appropriate repository branch; use LFS for large binary data; no secrets. Active concurrent agents work on separate branches/PRs. **Never merge without explicit authorization.**

## 9. Exact completion test

This project is complete only when: (a) new AAO source data and closed SQLite are verified as backed up to the private remote, (b) a revision-aware contract-specific matched target panel and reproducible strictly causal CL/LO/APO historical input panel exist, (c) paired chronological pricing experiments and date-aware inference are reproduced from versioned data, (d) all plots/tables/paper claims are traceable to their hashes/commits, (e) one submission candidate passes research and journal checks, and (f) the author authorizes the submission. The working manuscript and Git configuration are currently **not** these deliverables.
