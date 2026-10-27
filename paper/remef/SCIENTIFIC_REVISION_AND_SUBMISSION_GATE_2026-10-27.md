# Paper A (REMEF): scientific revision and submission gate

> **2026-10-27 arithmetic audit update:** Direct recomputation now confirms the older 310-row October-expiry PI/PM price errors, 2,381-row historical PI and first-nearby robustness, and 253-row LO external validation; 10M run metadata also agrees with the paper. See [scientific audit findings](SCIENTIFIC_AUDIT_FINDINGS_2026-10-27.md) and the updated [presubmission checklist](PRESUBMISSION_AUDIT.md). **Not submission-ready:** old 2,381 prior-smile prediction rows, 2,366 same-contract IV, source-vintage/rights checks, original LO inputs and Word/editorial gates remain unresolved. The old and Databento pricing designs must not be pooled.

**Recorded:** 2026-10-27. **Working title:** Posterior Integration and Volatility Information in WTI Asian Option Pricing. **Status:** existing bilingual Word candidate and manuscript material, with significant evidence/audit issues still open. **NOT submitted, NOT submission-ready**. This is the **first-priority paper**, distinct from the NEW structural pricing/hedging JCM project.

Primary two-paper publication decision and overlap ledger:
[Two-paper strategy](../../docs/two_paper_publication_strategy_2026-10-27.md).
Original presubmission blockers:
[REMEF scientific/editorial audit](PRESUBMISSION_AUDIT.md).

## Core contribution

Ask how much Bayesian posterior integration of parameter uncertainty changes WTI Asian-option prices relative to (a) the plug-in posterior-mean price and (b) differences arising from volatility information sources. Evaluate what the experiments do and do not establish under each maintained pricing model. Aim for an interpretable economic finding rather than a catalogue of new priors.

**Critical interpretation:** A small posterior integration vs plug-in change does not mean posterior model-price uncertainty is zero; a large difference between option-implied and historical proxy volatility does not prove the magnitude of a P/Q variance risk premium. Conventional market-IV persistence may itself explain much of the pricing gap. Results use option settlements that can be exchange model-generated; quote and trade evidence require independent verification.

## Frozen research evidence — DO NOT MIX DESIGNS WITHOUT RECONCILIATION

| Evidence | Existing design and result | Appropriate Paper A status |
| --- | --- | --- |
| 10-million synthetic-history study and curvature/Taylor approximation | Existing concise manuscript and publication figures; mechanism correlation ~0.9995 in the reported experiment | Theoretical/mechanism evidence; independently verify source numerics and Monte Carlo convergence |
| Original Barchart/LO forward panel | 2,381 contract-date rows, **15 valuation dates**; historical PI MAE 2.6187 versus prior AAO-IV smile MAE 0.1075 | Existing main-text empirical design; verify row-level inputs, source rights and timestamps; keep results tied to the original Curran/one-factor settings |
| Original October and cross-instrument checks | 310 October sample, 253-row vanilla-WTI/LO comparison, as stated in original concise draft | Supporting old model checks; original reproducibility audit remains open |
| Databento Experiment 003, full 2023–Sep2026 | 111,585 contract-dates on 189 dates (97,341 actual-flagged); lagged IV MAE 0.21842 vs historical-proxy PI 0.80404 | **Different** reduced-form terminal-average model, with contemporaneous disjoint AAO parity anchors. Could be supplementary comparison; not the same structural/independent pricing evaluation as older dataset |
| Databento Experiment 004 | 2025–Sep2026 actual-mark holdout: unchanged lagged IV 0.208924 MAE vs Bayesian market-IV PI 0.209830; paired month-block CI covers zero | Empirical **null** incremental-value result, with inspected holdout; cannot claim Bayes IV integration wins |
| Databento Experiment 005 | Bayesian NIG residual-price intervals vs rolling residual quantiles; early-2026 observed 90% coverage collapse (~59% Mar, ~56.9% Apr) | Optional **conditional settlement-mark residual calibration diagnostic**, **not** implied volatility posterior price dispersion or an Asian payoff-interval model |

The older manuscript's numerical comparisons must not be silently replaced with the Databento figures: the data vendors, price-generating mechanisms, selected dates, volatility proxies, available CL underlying information, and degrees of ex-ante independence differ. **No pooling across these studies without an explicitly justified common design.** The supplemental candidate should emphasize these distinctions and produce a detailed sample/information-set comparison table.

## Editing order for the scientific manuscript

1. **Define one claim-driven abstract/introduction.** The Paper A topic is Bayesian posterior integration and volatility information. Avoid hedging P&L or full CL fixing reconstruction as promised results: they belong to the separate JCM proposal.
2. **Build a claim-to-evidence ledger.** For every reported sample size, pricing metric, CI, volatility source, source model, figure and posterior interval, identify exact committed CSV/JSON, raw-vendor provenance, generation code, sample dates, method support, clustering unit, and manuscript sentence. Remove/qualify any number without an audit trail.
3. **Resolve the empirical section's primary cohort.** Keep the original Barchart/LO study as the core only if its original audit passes; otherwise consider an explicitly narrower REMEF claim based on the Databento reduced-form conditional study. If using both, each has its own separately labelled study and methodology. Do not describe the new Databento setup as a first-nearby CL pathwise Asian pricing simulation.
4. **Read actual and theoretical settlement flags separately.** Report actual-flagged sample and date cluster counts first; disclose theoretical marks, zero volume, implied-volatility persistence and current-date disjoint parity assumptions. Review how exchange settlement models affect independence of the target.
5. **Report honest statistical inference.** Use date/month-block paired intervals and assess economic magnitude versus minimum tick and bid/ask. Don't treat tens of thousands of strike/expiry observations as independent replicates.
6. **Preserve the negative findings.** PI−PM differences may be tiny, lagged market-IV Bayesian variants may not improve MAE, and conditional residual calibration may fail markedly under nonstationarity. A negative result can be informative but requires a clear, novel research contribution.
7. **Literature/novelty test:** distinguish existing commodity Asian-option valuation approximations, Bayesian calibration, REMEF Asian-option precedents, Gilder–Tsiaras volatility-predictability study, and known prior-IV advantages. Establish exactly what this manuscript adds.
8. **Rights and editorial gate:** confirm data redistribution permissions, both source-vendor licenses, cited data availability, method/AI-use disclosure, funding/COI accuracy, signed author documents, bilingual formatting, APA references, editable Word equations/tables, ≤25-page limit and blind/anonymized review output. Recheck live REMEF requirements before submission.
9. **Submission gate:** generate and inspect final Word and supplement **only after** audit. Author reviews, approves and submits; nothing is automatically submitted or scheduled. Do not submit substantially equivalent drafts simultaneously to JCM/JFM.

## Output handoff requirements

- Scientific manuscript remains in the existing paper/remef infrastructure, which currently adapts the concise Wiley source; do not overwrite its source until choosing and validating the evidence changes. Work on isolated sections/PRs for significant rewrites.
- Update paper/remef/PRESUBMISSION_AUDIT.md checkboxes **only when evidence is actually verified**, not when a task is merely proposed.
- Create a new manuscript-evidence manifest (claim, code version, data source, run ID, table/figure ID, validation status); compile clean blinded and author Word only after the intended text is fixed.
- Record both successful and unsuccessful audit results, reasons for excluding records, material data-rights concerns and exact next steps.
- Keep separate structural/JCM feasibility work in [research structural plan](../../research/STRUCTURAL_WTI_AAO_PAPER_FEASIBILITY_PLAN_2026-10-27.md), with independent hypotheses and outcome tables.

## Decision rule

**Ready for REMEF consideration** means that the old and/or new empirical claim set is internally consistent and reproducible, novelty is adequately articulated, exchange-derived settlement dependence is disclosed, data rights are resolved, all existing audit blockers are closed, and the author approves the blinded Word and supporting materials.

**Not ready** if old 15-day original results cannot be reproduced, vendor permissions are unknown, multiple models' effects are casually pooled, or novelty rests solely on 10 million simulations and a foreseeable lagged-IV advantage.

**Paper B remains separate:** no new JCM manuscript is asserted ready or even feasible until actual CL fixings/curves and independent price/hedge outcome data are audited.
