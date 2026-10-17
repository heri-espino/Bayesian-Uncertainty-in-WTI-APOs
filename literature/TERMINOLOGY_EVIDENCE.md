# Terminology evidence from the option-pricing literature

This document is an editorial source map for [the manuscript wording dictionary](../paper/WORDING_DICTIONARY.md). Its purpose is **not** to establish a corpus-wide frequency ranking. It records expressions visibly used in the relevant papers in `literature/extracted/`, with the appropriate limits on their meaning. The extracted text can contain OCR artifacts; use the source PDF to verify any consequential quotation or numerical claim. No substantive financial result is inferred from a term alone.

## Core source-to-term map

| Literature source | Language supported in the source | Appropriate use in the WTI APO paper | Important distinction |
|---|---|---|---|
| Kemna & Vorst (1990), `extracted/kemna_1990_pricing-average-asset-value-options.md` | average-value options, arithmetic average, geometric average, Monte Carlo, variance reduction | Identify the path-dependent contract and numerical pricing method | Generic average-value options are not automatically the exact CME WTI APO contract |
| Curran (1994), `extracted/curran_1994_valuing-asian-and-portfolio-options.md` | Asian (average-price) options, conditioning on the geometric mean, risk-neutral expectation | Describe the deterministic conditioning approximation | A numerical pricing approximation is not a separate observed market price |
| Kahalé (2018), `extracted/kahale_2018_multilevel-monte-carlo-asian-options.md` | discretely monitored Asian options, monitoring dates, multilevel Monte Carlo, control variates | Use *monitoring dates* for the generic payoff and *fixing dates* for the actual CME contract | A monitoring date in an abstract model need not match the contract-specific first-nearby futures fixing |
| Bakshi, Cao & Chen (1997), `extracted/bakshi_1997_empirical-performance-alternative-option-pricing-models.md` | empirical option-pricing performance, out-of-sample pricing, pricing errors, hedging errors, model misspecification, moneyness/maturity | State which empirical loss function and information cutoff is being evaluated | Pricing performance is not equivalent to hedging performance |
| Dumas, Fleming & Whaley (1998), `extracted/dumas_1998_implied-volatility-functions-empirical-tests.md` | implied-volatility functions, in-sample fit, out-of-sample pricing | Refer to previously estimated implied-volatility functions and test-date repricing | A contemporaneously fitted smile is not an out-of-sample forecast |
| Guidolin & Timmermann (2001 draft), `extracted/guidolin_2001_option-prices-bayesian-learning.md` | Bayesian learning, implied-volatility dynamics, predictive densities, out-of-sample forecast errors | Place Bayesian option pricing and prediction in context | An equilibrium learning model is not the same as the manuscript's posterior over a historical-volatility parameter |
| Rombouts & Stentoft (2009 working paper), `extracted/rombouts_2009_bayesian-option-pricing-mixed-normal-models.md` | parameter uncertainty, posterior moments, predictive densities, out-of-sample option prices, benchmark models | Refer to posterior inference and established empirical evaluation vocabulary | Their risk-neutral *predictive price densities* are not identical to the distribution obtained by transforming our parameter posterior through a fixed conditional-pricing function |
| Gilder & Tsiaras (2020), `extracted/gilder_2020_volatility-forecasts-crude-oil-options.md` | volatility forecasts, option-implied volatility, realized volatility, forecasting performance | Discuss volatility information in WTI options and historical-versus-option-based forecasts | Predicting realized volatility differs from predicting APO settlements |
| Schwartz (1997), `extracted/schwartz_1997_stochastic-behavior-commodity-prices.md` | term structure, commodity futures, convenience yield, stochastic factors | Describe omitted futures-curve dynamics | The maintained one-factor volatility model does not itself estimate convenience yield |
| Ewald, Wu & Zhang (2023), `extracted/ewald_2023_pricing-asian-options-stochastic-convenience-yield-jumps.md` | commodity Asian options, stochastic convenience yield, jumps, geometric-average control variates | Identify richer commodity-model alternatives | These are possible model extensions, not mechanisms established by our experiment |
| Cummins & Esposito (2025), `extracted/cummins_2025_appraising-model-complexity-option-pricing.md` | option-pricing performance, model complexity, competing specifications | Distinguish better out-of-sample fit from added model complexity | Do not infer that one model class is universally superior |

The first, third, fourth, fifth, sixth and seventh rows are particularly useful when normalizing prose. The full literature matrix is in [LITERATURE_MATRIX.md](LITERATURE_MATRIX.md).

## Required distinctions in the manuscript

| Quantity or comparison | Preferred expression | Do not replace it with |
|---|---|---|
| `E[C^Q(sigma) ∣ D]` | posterior-integrated price (PI) | predictive market price density |
| `C^Q(E[sigma ∣ D])` | posterior-mean plug-in price (PM) | posterior mean price |
| `PI-PM` | PI--PM difference, *not* a necessary bias correction | integration correction without a stated convention |
| `{C^Q(sigma): sigma ~ p(sigma ∣ D)}` | posterior distribution of conditional model prices | future distribution of traded option prices |
| `Var(sigma ∣ D)` | posterior variance of volatility | volatility of volatility, realized variance |
| `C^{Q\prime\prime}(sigma)` | curvature of the option price with respect to volatility | volatility curvature without definition |
| IV inverted from APO market settlements | APO-implied volatility | observed physical volatility |
| IV inverted from monthly vanilla LO option prices | vanilla-WTI implied volatility | independent structural risk-neutral volatility |
| Estimation using only earlier option dates, followed by repricing at current futures/fixings/rates | out-of-sample pricing using earlier-date option information | forecast made with exclusively previous-day market inputs |
| Select rows whose *own* contract volume is positive | contract-date observations with positive trading volume | transaction prices |
| Select all rows on a date with some volume elsewhere | observations from positive-volume dates | observations with positive contract volume |
| 80/160/320 CRR comparison | check of the number of tree steps / tree-refinement check | convergence proof |
| Matching unresolved arithmetic-average variance to one scalar | variance-matched constant volatility | the true risk-neutral diffusion volatility |

**Information timing:** The experiment uses **earlier-date options to estimate implied volatility** but **the valuation-date futures curve, realized fixings, and discount factor to reprice**. State both parts whenever describing the forecast design. This prevents an imprecise claim that *all* inputs were lagged.

**Posterior price intervals:** These intervals measure parameter uncertainty *conditional on the maintained pricing model*. They do not include market-price innovations, uncertainty in the model specification, bid-ask spreads, or unspecified future volatility dynamics.

## Sentence-level editorial tests

1. Prefer a subject with a specific action: “We estimate GARCH parameters from earlier returns.” Not “A dynamic volatility state is operationalized.”
2. Write estimation, updating, forecasting, mapping, and repricing as separate steps where they are separate operations.
3. Replace abstract labels with measured comparisons: “MAE falls from X to Y on N observations.”
4. Define PI and PM once and subsequently say “PI--PM difference”; avoid calling it a “correction” unless deriving a mathematical expansion with a defined sign.
5. Keep *curvature*, *moneyness*, *risk-neutral measure*, *posterior variance*, *delta method*, *EWMA*, *GARCH(1,1)*, and *valuation-date cluster bootstrap*: they are concise and technically appropriate.
6. Avoid “weak-information states” when the actual manipulated variable is sample size: say “short historical samples” or “few historical observations.”
7. Do not use “independent validation” to imply statistically independent dates. “Cross-instrument validation” means a different option *family* supplied the implied volatility; it does not remove dependence across dates or products.
8. State the limits of evidence once, clearly, rather than repeating nearly identical caveats in every section.

## Editing boundaries

A terminology edit must not change equations, labels, table numbers, empirical counts, sample restrictions, code/data provenance, citation keys, or the physical/risk-neutral measure distinction. Factual inconsistency is an issue for a *separate scientific revision*, not a silent language edit. The fuller and concise manuscript versions must remain distinct until the author chooses the submission version.
