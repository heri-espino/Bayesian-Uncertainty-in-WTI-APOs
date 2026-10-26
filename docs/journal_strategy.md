# Journal strategy — October 2026 post-Databento expansion


> **Current scope and author decision (2026-10-26):** JCM remains a conditional stretch target,
> not a submitted or completed 2020–2026 study. REMEF and earlier Wiley/JFM source are preserved.
> See `research/PAPER_COMPLETION_MASTER_PLAN_2026-10-26.md`
> and `research/AAO_EVIDENCE_LEDGER_2026-10-26.md`.
> Expanded Databento pricing model comparisons and JCM figure revisions are still unexecuted.

**Planning status, not submission approval.** The author has asked us to reconsider the journal after expanding historical WTI Average Price Option data. The **working ambitious target is *Journal of Commodity Markets* (JCM), conditional on strong *verified* new market evidence**. The prepared realistic fallback is *Revista Mexicana de Economía y Finanzas* (REMEF); *Journal of Futures Markets* (JFM) remains a demanding alternative and the Wiley LaTeX source remains intact. The author has not confirmed a final journal submission or author-approved journal reformatting. **Do not send multiple journals the same paper simultaneously.**

## Why JCM is a reasonable next target (subject to evidence)

The official [Journal of Commodity Markets description](https://shop.elsevier.com/journals/journal-of-commodity-markets/2405-8513) explicitly covers empirical/theoretical commodity economics and finance, including **pricing, hedging, and risk analysis of commodity derivatives**, energy markets, and econometric/statistical analysis. Our application to exchange-traded WTI Asian options falls within this remit. The scope also emphasizes **originality, quality and clear presentation**: acquiring more records alone does not demonstrate a novel contribution.

The [Journal of Futures Markets scope](https://onlinelibrary.wiley.com/page/journal/10969934/homepage/productinformation.html) covers derivatives and risk management broadly; it is a plausible but competitive alternative for a genuinely stronger inference/generalizability claim. Its [author guidelines](https://onlinelibrary.wiley.com/page/journal/10969934/homepage/forauthors.html) currently offer **free-format submission**, so a source template cannot itself define the research target. We maintain the frozen Wiley NJDv5 source for continuity, not as a claim that Wiley submission is already approved.

[REMEF's official instructions](https://remef.org.mx/index.php/remef/about/submissions) cover energy markets, commodities, financial engineering, derivatives and risk management, and prohibit simultaneous submission. Its [journal policy](https://remef.org.mx/index.php/remef/about) states it charges no submission or article-processing fees. A separate REMEF Word manuscript already exists under `paper/remef/` with bilingual abstracts and a presubmission audit. Preserve this route in case new evidence is incomplete or not sufficiently novel for JCM/JFM.

## Core research contribution to test

**Question:** How important is posterior integration (PI) compared with the choice of volatility information in real-market pricing of WTI average-price options? The synthetic experiment isolates the posterior-dispersion × price-curvature mechanism. The old WTI empirical comparison suggests volatility-input selection is substantially more consequential than PI-versus-posterior-mean (PM) differences, **under its maintained one-factor pricing model and small date sample**.

A successful new paper would add:
- many more distinct, properly supported, forward-eligible valuation **dates** and expiries, not merely thousands of correlated contract rows;
- independent cross-vendor settlement validation and accurate timing of price marks;
- actual versus theoretical CME settlement diagnostics; CME's use of the Curran settlement model (effective May 2020) complicates interpreting comparison against model-generated prices as transaction-price prediction;
- year/regime/expiry/fixing-progress/volume sensitivities and defensible date/time-block uncertainty;
- truly prior-date APO-IV/same-contract/LO-IV versus historical P-volatility comparisons on exactly matched rows;
- a precise economic interpretation of PI, PM, volatility information and model misspecification, with a clearly bounded novelty claim.

**Novelty traps:** MCMC itself, 10 million simulations, the 0.9995 simulation correlation, WTI APO pricing, use of Barchart WTI options, and propagation of Bayesian uncertainty into exotic prices are not by themselves new. Test against Shiraya & Takahashi (2011), Gupta & Reisinger (2014), Gan, Wang & Yang (2020), Gilder & Tsiaras (2020), and the existing literature matrix. Do not turn an empirically foreseeable IV advantage into a universal option-market theorem.

## Decision gates

1. **Acquisition (done only at file-transfer level):** The author's CLI reported 160 compressed AAO definition/statistics chunks spanning 80 of 81 month windows, 2020-Jan through 2026-Sep, USD 17.33487324 *quoted*; actual billing, missing month, file integrity and final APO settlements still require verification. See `research/CHECKPOINT_2026-10-25_AAO_EXPANSION.md`.
2. **Contract/measurement gate (OPEN):** confirm target product, unique outright contracts, final settlements, `ts_ref`, theoretical/actual mix, liquidity, exact source agreement and missingness.
3. **Eligible-date gate (OPEN):** compute independently eligible chronological holdout dates, with ex-ante CL fixings/rates, no IV leakage, and meaningful support across market regimes.
4. **Inference/robustness gate (OPEN):** rerun canonical models on strict common support, report date and expiry counts, uncertainty, source splits and robustness to theoretical marks.
5. **Editorial gate (OPEN):** if the contribution is more generalizable and genuinely differentiable from prior commodity-derivative work, **JCM becomes the first choice to prepare for**. If empirical coverage/novelty remains modest, prioritize existing **REMEF draft**; consider JFM only if evidence and presentation plausibly satisfy its stronger originality hurdle. No invented acceptance probabilities.
6. **Author approval and current guidelines (OPEN):** confirm the target, article type, formatting, length, data/source code sharing conditions, open-access fees/options and related-work obligations before modifying journal formatting or submitting. No simultaneous submissions.

## Manuscript and repo contract

- Existing `paper/manuscript/main.tex`, `main_short.tex` and `paper/build.py` remain **the internal JFM/Wiley implementation**. The existing fixed two-column Utopia format is a *source preservation rule*, not a restriction on discussing another journal.
- `paper/remef/` remains the separately prepared REMEF Word-format fallback. Its published numerical claims remain the earlier validated results until a new experiment passes full parity and audit.
- No JCM-specific journal template has yet been selected, added or built. Add a new output mode or manuscript adaptation only in a dedicated author-approved PR, without overwriting or changing frozen vendor code.
- Keep the scientific paper, online supplement, results, citations, methods and claims mutually consistent; do not quietly transfer previous-sample results to the expanded sample.
- The real target decision should follow `research/AAO_AGENT_TASKS.md`, `research/CHECKPOINT_2026-10-25_AAO_EXPANSION.md`, and `paper/remef/PRESUBMISSION_AUDIT.md`.

## Author-guideline verification links (checked 2026-10-25)

- JCM official journal scope: https://shop.elsevier.com/journals/journal-of-commodity-markets/2405-8513
- JFM official scope: https://onlinelibrary.wiley.com/page/journal/10969934/homepage/productinformation.html
- JFM official author guidance: https://onlinelibrary.wiley.com/page/journal/10969934/homepage/forauthors.html
- REMEF submission instructions: https://remef.org.mx/index.php/remef/about/submissions
- REMEF publication charges: https://remef.org.mx/index.php/remef/about

Recheck all journal policies when an actual submission is planned; this is a research target strategy, not a journal acceptance or compliance certificate.
