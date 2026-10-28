# Second terminology and academic-style review — REMEF Paper A

**Date:** 28 October 2026  
**Scope:** Editorial copyedit of the REMEF-only bilingual abstract, introduction, methods, empirical design, results, figure and table captions, limitations, conclusion and Word postprocessor. **No new experiments, estimates, simulations, figures, source-data changes or reference substitutions.** Existing numerical results and caveats are intentionally preserved.

## Editorial aim

Use ordinary academic finance language without losing the distinctions between (i) posterior-integrated versus posterior-mean plug-in **point prices**, (ii) posterior distributions of **model prices**, and (iii) empirical **settlement-price errors** and their coverage intervals. The Barchart/LO/Curran and Databento/terminal-average analyses must remain separate.

## Literature comparison

- Curran (1994), *Valuing Asian and Portfolio Options by Conditioning on the Geometric Mean Price*, uses the established language of arithmetic-average Asian options and conditioning approximations: https://doi.org/10.1287/mnsc.40.12.1705
- Sagor, Boone and Ghanam (2026), *Bayesian Joint Estimation of the Hurst Parameter and Volatility with Applications to Fractional Option Pricing*, discusses posterior distributions of option prices and posterior price uncertainty: https://doi.org/10.3390/risks14080173
- Pirjol and Zhu (2021), *What is the Volatility of an Asian Option?*, uses the conventional terms volatility smile, Asian-option prices and adjusted/constant volatility: https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3875929

These sources are **terminological reference points only**; this pass does not add a novelty claim or introduce a new citation to the paper.

## Specific improvements

| Previously awkward / ambiguous wording | Revised approach |
|---|---|
| “actual-flagged targets” | “observations classified as actual settlements” (provider classification is retained) |
| “historical parity-forward-change volatility proxy” | “historical volatility estimate based on earlier changes in the average inferred from put--call parity” |
| “same-date disjoint parity anchors” | “put--call parity estimates from other same-date strikes” |
| “out-of-sample pricing-error differences” | “date-ordered conditional pricing-error differences” (not a confirmed real-time forecast) |
| “market-IV innovations” | “changes in log implied volatility for each expiry” |
| “Bayesian market-IV PI” | “Bayesian modeling of earlier implied volatility” or explicit posterior-integration method name |
| “residual-interval undercoverage” | “coverage of pricing-error intervals falls below its stated level” |
| “posterior curvature corrections” | explain the role of option-price curvature and posterior volatility variance |
| “first-publication vintages” | “when records were originally published or subsequently revised” |
| “originally stored-row arithmetic reconciled” | “stored estimates and date ordering independently checked” |
| “vanilla-WTI” in a heading | “WTI futures options” |

Standard finance/statistics terms retained where they have precise meanings: **implied volatility, volatility smile, moneyness, risk-neutral valuation, Curran conditioning approximation, posterior integration, posterior mean, GARCH(1,1), Cox–Ross–Rubinstein, date-cluster bootstrap, MAE, RMSE, model-price distribution and interval coverage**.

## Accuracy boundaries preserved

1. The original 2,381 option-date observations cover **15 dates**, with **2,319 zero-volume rows**. They are date-ordered **conditional repricing** comparisons using information on each valuation date, not confirmed fully prospective forecasts.
2. The separate Databento study has **97,341 provider-classified actual settlements** across **189 dates**, conditions on *other same-date* option prices through put--call parity, and uses a different reduced-form terminal-average pricing model.
3. Vendor publication times, record revisions, market-data redistribution rights and external replay checks remain unresolved. We do not claim trade execution, identifiable volatility risk premium, causal validation or out-of-sample predictive superiority.
4. Original numerical values, sample sizes, bootstrap intervals and scientific figures have not been changed.
5. Section titles in the Word postprocessor and its synthetic tests were revised along with the LaTeX source. The old committed Word/PDF review files remain **pre-edit snapshots**. Rebuild and visually inspect both drafts and PDF before submission.

## Copyediting decisions

Use direct active sentences; introduce “implied volatility” before “IV”; describe what the sample or statistic measures before listing model details; separate the two data sources in the narrative. Avoid adding promotional adjectives or self-defensive statements (“we do not claim … is new”) where a focused contribution statement is clearer. A negative result remains publishable only if presented within its original evaluation setting.

This editorial pass **does not clear** outstanding scientific, licensing, submission or blind-metadata checks. Follow `SUBMISSION_HANDOFF_2026-10-28.md` and `EDITORIAL_READABILITY_REVIEW_2026-10-28.md` before submitting.
