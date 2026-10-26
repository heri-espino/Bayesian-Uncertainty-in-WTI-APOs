# WTI Average Price Options — canonical project-completion plan

**Status date:** 2026-10-26. **Repository:** `heri-espino/Bayesian-Uncertainty-in-WTI-APOs` (private). **Purpose:** finish a scientifically defensible article on Bayesian volatility uncertainty in WTI Average Price Options (APOs), using both the original Barchart history and the planned restoration of the extended Databento AAO archive. This is the canonical current handoff. Historical checkpoints must remain intact, but must not supersede this document.

**Companion files:** [Numerical evidence ledger](AAO_EVIDENCE_LEDGER_2026-10-26.md), [sequential experiment register](AAO_EXPERIMENT_REGISTER_2026-10-26.md), [independent-agent verification protocol](AAO_AGENT_VERIFICATION_PROTOCOL_2026-10-26.md), [recovery and LFS procedure](AAO_RECOVERY_AND_LFS_BACKUP_2026-10-26.md), [agent rules](../AGENTS.md).

## 1. Research mission and motivation

**Central question:** When does integrating uncertainty about volatility into risk-neutral WTI Asian-option prices materially change model values, and when does the *volatility input* matter much more?

The original paper tested Bayesian posterior integration versus a posterior-mean volatility plug-in and the economic importance of historical versus earlier-date option-implied volatility. Synthetic simulations characterized the theoretical effect. The original market study contained **2,381 option/valuation-date holdouts on 15 distinct dates** (seven expiries), plus **253 independent-LO-based comparisons on 10 dates**. These are correlated contracts within dates, NOT thousands of independent temporal experiments.

The author therefore acquired more historical data in order to test robustness across **many additional distinct forward-eligible dates, strikes, expiry months, fixing states and regimes** rather than inflating the cross-sectional row count. This is the potential new contribution for a commodity-derivatives journal.

Instruments and sources must remain distinct:
- **AAO** (CME Globex) / **AO** (clearing): WTI Average Price Options. These are the **pricing targets**. Target payoff depends on the arithmetic average of daily settlements of first-nearby **CL** WTI futures during the specified calendar month, with exact contract schedule and partial fixings.
- **CL**: WTI futures underlying, daily past fixings and dated forward curve; correct first-nearby roll is essential.
- **LO**: ordinary WTI futures options. They provide an *independent earlier-date implied-volatility information source*, not more AAO target marks.
- **Barchart**: original JAO/APO contract-date histories, earlier benchmark data and a cross-vendor validation source.
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

## 5. Required steps to complete the project

**Gate 0 — Reacquire and preserve (absolute prerequisite).** Follow `research/AAO_RECOVERY_AND_LFS_BACKUP_2026-10-26.md`, not stale dated download snippets. On the Windows VM, ensure tracked data path is included in sparse checkout *before* fetching; verify `python -m scripts.aao_lfs_preflight`; request a fresh 81/81-month quote with `experiments.wti_databento_aao_bulk` and the new `reacquisition_20261026` report directory; manually authorize cost; download exactly 81 x 2 chunks; hash-audit and count all 162 against the NEW ledger; commit/push originals and ledger to the private GitHub remote via LFS; verify upload actually exists. Never touch sparse checkout, reset or clean while the only copy remains local. **Do not store Databento API key/DPAPI data in Git.** Rebuild and push SQLite with LFS after replay. A budget guard is an estimated quote, not a provider-enforced cost ceiling.

**Gate 1 — Reproduce historical diagnostics.** Review `python -m scripts.aao_replay_offline` (dry-run), then manually run `--execute` only after originals are remotely backed up. It calls the 11 existing diagnostic steps: manifest hash audit, full inventory, coverage figure, sampled ID probes, settlement as-of-day diagnostics, alternative date mappings, native symbol mapping, monthly candidate normalization, all-month correction-aware reconciliation, and quality / Barchart *date-only* overlap. Preserve outputs, configurations, counts, hashes, code commit and discrepancies; if Databento data changed since original delivery, document a *vintage difference* rather than forcing identical results. A `fig05` coverage figure is NOT evidence of model pricing performance.

**Gate 2 — Contract/time/price validation.** Build an unambiguous key: exchange/publisher, native symbol, call/put, expiry and maturity, underlying, strike with verified price scaling, multiplier/currency. As-of match definitions, settlement `ts_ref` vs UTC publication timestamp, update-action, final/theoretical and deletion/correction state. Compare Databento with Barchart ONLY after matching **same contract, same reference date, compatible timestamp and normalized USD/barrel amount**. Record overlap and unmatched/ambiguous rejection reasons, mismatch tolerance and price-difference distribution. Date-only Barchart intersection is not enough.

**Gate 3 — Chronological pricing eligibility.** For each target-date price observation reconstruct daily already fixed CL settlements and their exact first-nearby rolls, remaining future fixings, current futures curve, rates/discount factors and compatible prior CL return histories. Fit historical volatility strictly with allowed cutoff. For APO/LO implied volatility, use **prior-date** option information (no same-target future leak), with explicit support/moneyness/expiry interpolation rules and no hidden test-target calibration. Produce auditable staged attrition funnel of rows / contract-date keys / contract-expiry dates / distinct unique valuation dates, reject reasons and year/regime coverage. Chronological train/validation/test partitions must be predeclared and frozen before evaluating forecasts.

**Gate 4 — Actual model comparison.** Reuse the existing Q pricing engine; do NOT fork new divergent economics. Compare posterior integration (PI) against posterior-mean (PM), historical long expanding/rolling 63/EWMA/horizon-matched GARCH volatility inputs and strictly prior APO IV and independent LO IV on **identical eligible rows**. Specify where Monte Carlo PI vs deterministic Curran pricing is used. Evaluate MAE, RMSE, bias, distribution of errors and **paired date-block** differences/uncertainty. Stratify by date/year/regime, expiry, moneyness, fixing progress, put/call, settlement actual/theoretical, positive volume and OI. Include older Barchart matched date subset for vendor-robustness. A statistically/financially unconvincing new result is a legitimate finding; do not claim material improvement a priori.

**Gate 5 — Diagnostics and publication science.** Examine whether PI–PM is negligible or material across states, whether posterior *price dispersion* is distinguishable from mean-price correction, and whether option-based IV superiority survives many dates/regimes, recent history/GARCH and genuine/liquid marks. Avoid pseudo-replication: option rows sharing dates are correlated; adjacent dates can be serially dependent. Report confidence intervals reflecting that structure; quantify support and missingness. Include negative outcomes and sensitivity to settlement-vintage eligibility.

**Gate 6 — Paper and reproducibility.** Regenerate new result tables and graphics from committed experimental artifacts; annotate every figure/table with producing script, frozen config, git commit, input SHA256 and eligible observation count. Replace old numbers in `paper/jcm/` ONLY once new empirical results pass all checks. Preserve old `figures/publication/fig01` through `fig04`, ten-million-path synthetic figures, REMEF and Wiley/JFM source, old output reports. Make new data diagnostics separate from new **pricing-performance** figures. Verify the JCM author guide and journal constraints before final build. The manuscript must be concise and use established derivatives vocabulary. A journal submission requires the author's final authorization; none has occurred.

## 6. Proposed manuscript argument, not a preordained result

Hypothesis H1: posterior mean-price integration adjustment is governed locally by posterior variance and Q-price curvature (sign unrestricted).

Hypothesis H2: economically relevant posterior model-price uncertainty may be much larger than its associated PI–PM point correction.

Hypothesis H3: option-informed strictly prior volatility can outperform historical alternatives on matched forward-eligible AAO marks, but the size and robustness can vary by source, time regime, liquidity and volatility estimator.

Hypothesis H4: improved sample depth allows meaningful inference across more **independent dates**, not because 5.1 million option marks provide 5.1 million independent errors.

New empirical evidence should be distinguished from numerical mechanism proof, econometric model identification, and market executability. Reject/rewrite any hypothesis the data do not support.

## 7. Figures and table contract

**Existing paper figures (keep as prior-sample evidence):**
`figures/publication/fig01_mechanism_map`, `fig02_historical_vs_apo_implied_volatility`, `fig03_forward_q_cluster_bootstrap`, `fig04_numerical_identification`; the ten-million-path versions live in `figures/publication/ten_million/`. `paper/jcm/build.py --check` checks a template, NOT new pricing evidence.

**Planned (not yet produced) expanded 2020–2026 outputs:** monthly final settlement/instrument/actual/theoretical/volume coverage and `ts_ref`/publication-funnel diagnostics; Databento-vs-Barchart contract-level matched price parity graph; eligible valuation-date calendar and attrition table; multi-date same-support pricing-error panels (PI/PM, historical, APO prior IV, LO prior IV); date-block pairwise differences; year/expiry/regime/fixing progress/moneyness/liquidity heterogeneity; posterior price interval vs PI–PM correction figure; source/contract/maturity/price-scale robustness; experimental reproducibility manifest. Only move plots and results into the article after accepted source/Q/temporal checks.

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
