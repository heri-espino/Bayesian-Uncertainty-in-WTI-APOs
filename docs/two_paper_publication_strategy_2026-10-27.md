# Two-paper publication strategy — WTI Average Price Options

> **2026-10-27 audit progress:** [Paper A REMEF arithmetic audit](../paper/remef/SCIENTIFIC_AUDIT_FINDINGS_2026-10-27.md) now independently recalculates the core 310/2,381/253 observation price-error claims and corroborates the 10M run metadata; **original input-vintage/rights, other predictor-row and editorial gates remain open**. [Paper B CL feasibility audit](../research/JCM_CL_FUTURES_FEASIBILITY_AUDIT_2026-10-27.md) identifies partial existing Databento first-nearby CL history, plus a serious *unexplained hash mismatch* between the CL LFS object and its acquisition manifest. Neither paper is submission-ready; no new experiment was run.

**Decision recorded:** 2026-10-27. **Status:** author-approved research/publication direction; neither paper has been submitted, accepted or cleared for submission. **Scope:** two substantially different manuscripts, not simultaneous submissions of the same paper. This document supersedes the older single-manuscript "JCM first, REMEF fallback" *target allocation*, not prior scientific results.

**Decision:** prioritize completing the existing Bayesian volatility-information manuscript for the Revista Mexicana de Economía y Finanzas (REMEF); in parallel, develop an **independent** structural/hedging study for potential submission to the Journal of Commodity Markets (JCM). The Journal of Futures Markets (JFM) Wiley source remains an archived alternative form of the first manuscript, not an additional third publication.

## 1. The two distinct research contributions

| Dimension | Paper A — REMEF (priority to complete) | Paper B — JCM (new research) |
| --- | --- | --- |
| Working title (provisional) | Posterior Integration and Volatility Information in WTI Asian Option Pricing | Pricing and Hedging WTI Average Price Options under Futures-Curve Uncertainty |
| Central question | How consequential is Bayesian posterior price integration relative to the choice of volatility information? | How accurately can a path-dependent WTI AAO payoff be priced/hedged using an observed fixing schedule, futures curve and independent market signals? |
| Primary analysis | Posterior-integrated versus plug-in pricing, synthetic price curvature, historical- versus prior market-implied volatility information, comparative conditional mark errors | Contract-exact partly fixed monthly Asian payoff; explicitly reconstructed first-nearby CL settlement fixings; futures-curve and risk-neutral modeling; independent quote/trade validation and/or implementable hedging |
| Contribution type | Statistical/computational comparison and bounded empirical finding about input choice versus posterior integration | New *structural* commodity-derivatives empirical valuation/risk evidence beyond the reduced-form terminal-average Black proxy |
| Existing empirical assets | Original Barchart/LO study, ten-million-path synthetic study, Databento Experiments 003–005 with caveats | Potential historical AAO source overlap only; **new independent CL futures fixing/curve and market/hedging measurements needed** |
| Journal target | REMEF (subject to original scientific/editorial audit) | JCM (conditional on feasibility, originality and independent validation) |
| Current readiness | Manuscript/Word builder exists; **NOT submission-ready** pending harmonized evidence and audits | Research proposal only; not a second finished manuscript or validated structural pricing system |

These are **working titles**, not claims that the projects have earned these respective journal placements or acceptance prospects.

### Paper A: permitted core argument

One-factor Bayesian option-pricing analysis, showing under maintained modeling assumptions that the volatility *information source* is far more consequential to option-mark pricing error than price averaging over posterior volatility draws. Posterior uncertainty can affect price distributions while having little effect on posterior-integrated versus plug-in *mean* prices. Preserve the quantitative distinction between predictive interval **coverage**, price posterior dispersion, and tiny PI−PM price corrections.

The original REMEF draft is adapted from the Wiley/JFM concise manuscript and reports an older Barchart/LO empirical design (e.g. 2,381-option-date benchmark over 15 dates, separate 253-row LO comparison, 310-observation October design). Those are **NOT interchangeable** with the 81-month Databento reduced-form study. The latter has 111,585 target contract-date observations over 189 dates (97,341 actual-flagged) with contemporaneous disjoint parity-derived forwards/discounts: conditional cross-sectional settlement-mark valuation, not a structural CL fixing-path model or an independent fully ex-ante forecast. New Experiment 004/005 regressions have already used the 2025–26 retrospective period; report this, not an untouched holdout.

Paper A may selectively incorporate Experiments 003–005 as **clearly separately identified datasets/designs**, robustness or limitations if reconciled. Do not concatenate sample counts, methods, or estimated effects from non-equivalent pricing engines into one claimed common experiment. Avoid claiming that the 2026 residual interval failure validates structural Asian option payoff intervals. The manuscript must have one coherent question and test design; do not automatically insert all findings to increase length.

### Paper B: distinct contribution required

Make the payoff explicitly depend on the month of CL first-nearby futures fixes, including already observed partial fixings and modelled future fixing dates. Obtain or verify independently sourced dated CL settlements/futures curves/discount inputs and, if possible, independently observed AAO quotes, bid/ask or trades (not solely exchange theoretical settlements). Compare path-dependent pricing numerical methods (including an appropriate Curran benchmark and simulation), then evaluate hedging/risk performance **if verifiable executable hedges and timestamps exist**. If the original dataset does not permit those analyses, first document the missing data and feasibility rather than imply the results exist.

Paper B must deliver **new** structural model results, an independent pricing/hedging question and distinct primary figures/tables. Its key results cannot merely repeat Paper A's PI vs PM or historical-versus-IV accuracy tables with a cosmetic model change. Prior-paper estimators can appear as **cited comparators**, but their earlier evidence cannot be presented as a second independent main finding. A credible JCM novelty argument requires showing what the existing commodity Asian-option, stochastic-volatility, Curran/Monte-Carlo, and hedging literature has not answered.

## 2. Independence, overlap and publication ethics

**Permissible:** reuse clearly identified historical raw AAO data where licensing allows; refer to common contract specifications and foundational mathematical identities; cite and accurately explain the first paper as related work (including a preprint or submission when a citable version exists); use previously published models as baselines with transparent attribution.

**Not permissible:** duplicate or substantially recycle the same introduction/results text, tables, figures, hypotheses or conclusions; submit two versions of materially the **same paper** to different journals at once; represent the same contract-date dataset as independent validation across the two papers; conceal overlap, preregistration after result inspection, or already-presented related manuscript material.

**Operational overlap ledger** (keep updated before either submission):

| Item | Paper A status | Paper B treatment |
| --- | --- | --- |
| Commodity AAO payoff and exchange specifications | General background; explicit assumptions | More precise calendar contract definition; cite original/standard sources and Paper A where relevant |
| Ten-million-path PI−PM simulation/mechanism | Primary evidence in Paper A | Do not reproduce as a new contribution |
| Barchart/LO older pricing panel | Paper A evidence after original audit | Cite only if context; no second independent claim |
| Databento AAO option histories 2020–Sep 2026 | Reduced-form conditional evidence/robustness, carefully labelled | Data might overlap but independently collected CL fixing/curve/quote inputs, newly derived economic targets and distinct primary estimation needed; disclose reuse |
| Experiment 003 historical PI vs lagged AAO IV | Paper A supporting result | Do not rerun and present as new central result |
| Experiment 004 market-IV Bayesian PI/PM | Paper A supporting null result | Reference or cite, not central claim |
| Experiment 005 residual mark interval calibration | Paper A optional diagnostic/limitation | Do not use as untested structural payoff uncertainty result |
| New CL-path fixing/cash-flow reconstruction | Not Paper A's core claim | Potential Paper B foundational new method/data |
| External trade/quote comparisons or true hedge P&L | Only if already separately validated in Paper A; avoid duplicate main analysis | Intended NEW Paper B primary evidence, subject to feasibility |
| Historical information vintages, shared option price sources | Full acknowledgement | Re-evaluate independent timestamps and data availability; explicitly disclose sample overlap |

**Editors/rights:** Verify the current REMEF and Elsevier JCM ethics/related-manuscript instructions immediately before submission, and disclose the existence/status of the other related study if required. The initial strategy is **one manuscript submitted to REMEF while conducting separate research for JCM**, not a loophole to publish the same study twice. No simultaneous submission of substantially overlapping manuscripts. Any shared figures/tables require appropriate attribution and reuse permission. Explicitly check data-provider redistribution/licensing rights, including commit history of formerly public files.

## 3. Completion gates — Paper A (REMEF)

1. **Scientific identity:** select which numerical claims belong to the authoritative Paper A model. Existing REMEF draft is based on a different data/pricing pipeline than Experiments 003–005. Create an evidence-to-manuscript map (claim, source file/commit, sample, date cutoffs, model and limitations) and freeze one coherent narrative.
2. **Independent audit:** close the existing open result-to-source, same-contract prior IV/LO timing, sample-provenance, posterior-integration numerical precision, actual vs theoretical marks, date/time dependence, transaction/settlement caveats and vendor-rights checks in paper/remef/PRESUBMISSION_AUDIT.md.
3. **Honest result framing:** Market option-implied signals decisively outperform the particular historical AAO-forward-change proxy in the Databento setup; market-IV Bayesian adjustments fail to reliably beat unchanged lagged IV; experimental residual intervals fail during early 2026. Do not claim generic Bayesian superiority, economically meaningful penny-fraction gains, independent ex-ante pricing, or structural P-vs-Q effects.
4. **Novelty:** critically compare REMEF's Asian-option papers, vanilla crude-oil IV literature, existing Bayesian and simulation approaches; make clear precisely what the paper adds beyond well-known IV persistence and Jensen/Taylor curvature arguments.
5. **Editorial checks:** word count/length, bilingual English/Spanish abstracts/titles, APA references, blinded/author versions, native Word equations/tables, rendered pages, funding/ethics/AI-use disclosures, author approval, and any signed forms. Verify fresh REMEF policies.
6. **Submit only after gate completion.** REMEF is a working target, **not yet submitted or accepted**. A rejection can lead to a subsequent exclusive submission elsewhere after the first editorial process ends.

## 4. Feasibility gates — Paper B (new JCM project)

1. **Data inventory without purchases:** check existing Git LFS and manifests, AAO product/expiry/fixing conventions, first-nearby CL daily settlement coverage, forward-curve tenors, rates, option quote/trade fields, their timestamps and historical availability. Explicitly label any missing dataset. No automatic data purchases or provider queries.
2. **Economic object:** implement the actual exchange AAO payoff for months with 0, partial and complete fixing progress. Validate exact effective first-nearby convention and holiday/roll calendar against original exchange documents before writing pricing code.
3. **Risk-neutral structure:** baseline conditional Curran approximation where applicable, path simulation with curve-consistent dynamics and correct discount; then optional models for stochastic volatility, multiple curve factors or jumps. Compare numerical consistency and convergence.
4. **Independent empirical target:** define tradable independent quotes/trades where available, or declare exchange settlement-mark replication as a narrower target. Preserve observation timestamps, bid/ask bounds, marked volume and date availability; avoid current target contamination.
5. **Economic metric:** preferably hedge P&L, hedging turnover/cost, tail loss and drawdown with implementability assumptions, or rigorously selected independent market-price accuracy if hedging infeasible. Do not add unnecessary complexity merely for novelty.
6. **Design/inference:** predeclare leakage-free splits and independent new test dates. 2020–Sep 2026 datasets and 2025–26 episodes have been inspected by the team for older questions; reusing them for model development is **exploratory**, not a fresh untouched confirmatory test. Consider future >Sep 2026 genuinely uninspected evaluation data only when lawfully available.
7. **No guarantee:** if independent quotes/CL curves are missing or new results add no clear novelty, defer JCM and do not fabricate a structural/hedging claim. Paper B is a research project, not an automatic second publication.

See the standalone [structural data feasibility and research protocol](../research/STRUCTURAL_WTI_AAO_PAPER_FEASIBILITY_PLAN_2026-10-27.md).

## 5. Repo ownership, handoff and operating sequence

- **Paper A current candidate:** [paper/remef/README.md](../paper/remef/README.md); [REMEF presubmission blockers](../paper/remef/PRESUBMISSION_AUDIT.md); original author-maintained Wiley/JFM sources remain intact at paper/manuscript/.
- **Paper B workspace:** [paper/jcm/README.md](../paper/jcm/README.md) currently has an **old-source CAS staging draft**, not the structural Paper B. Do not mistake a successful compile for scientific readiness; new Paper B paper source should be separate and created only after research design is validated.
- **Experiment 003 handoff:** [reduced-form full historical evidence](../research/experiments/experiment003/DATABENTO_AAO_EMPIRICAL_RESULTS_AND_HANDOFF_2026-10-27.md).
- **Experiment 004 handoff:** [market IV Bayesian holdout results](../research/experiments/experiment004/FULL_RESULTS_AND_HOLDOUT_REVIEW_2026-10-27.md).
- **Experiment 005 handoff:** [price-residual interval results](../research/experiments/experiment005/FULL_RESULTS_AND_CALIBRATION_REVIEW_2026-10-27.md).
- **Separate Paper B feasibility plan:** [research/STRUCTURAL_WTI_AAO_PAPER_FEASIBILITY_PLAN_2026-10-27.md](../research/STRUCTURAL_WTI_AAO_PAPER_FEASIBILITY_PLAN_2026-10-27.md).
- **Journal strategy index:** [docs/journal_strategy.md](journal_strategy.md).

**Sequence:** (A) finish and audit Paper A; submit to REMEF only after author approval and required checks; (B) in parallel perform Paper B no-spend data-feasibility audit; (C) implement structural pricing/independent validation only if feasible; (D) develop and eventually submit a distinct JCM manuscript if a genuinely new contribution emerges. No fixed deadline or promise of acceptance.

**Version-control policy:** Work only on the existing results branch unless author requests another branch/PR. Do not merge into main automatically, reset/clean/force-push, alter historical manifests, overwrite private data, or change sparse checkout unexpectedly. Full source truth is GitHub: persist reproducible code/configs, independent result files, protocols, limitations, diagnostics, failures, charts and next steps. Heavy compute runs are manual on the author's PC. Lightweight CI may remain automatic; do not create/run automatic heavy GitHub Actions.
