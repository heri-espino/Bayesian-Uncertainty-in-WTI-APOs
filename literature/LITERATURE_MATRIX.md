# Literature matrix: Bayesian parameter uncertainty in WTI Average Price Option valuation

This document records the role of the eight papers added in September 2026 and places them
against the existing core literature already in the repository. It is intended to be the source
for the manuscript rewrite in issue #34.

The paper's contribution should **not** be framed as "using Bayesian inference to price an
Asian option" or "using MCMC for option pricing." Prior literature already covers Bayesian
learning, Bayesian predictive option pricing, parameter uncertainty, Asian-option numerical
methods, stochastic-volatility commodity models, and option-implied volatility. The defensible
contribution is the combination of a mechanism, a controlled map of where posterior integration
matters, and a contract-consistent WTI APO application that directly compares the incremental
effect of posterior integration with the much larger volatility-specification margin.

## Matrix for the eight newly added papers

| Paper | Question / setting | Model and data | P/Q and uncertainty treatment | Main result | Role in this paper | Novelty boundary |
|---|---|---|---|---|---|---|
| **Bakshi, Cao & Chen (1997), _Empirical Performance of Alternative Option Pricing Models_** | Which relaxations of Black--Scholes materially improve option pricing and hedging? | Black--Scholes, stochastic volatility, stochastic rates, jumps and combinations; 38,749 S&P 500 call prices, June 1988--May 1991. | Pricing dynamics are specified under a risk-neutral measure; implied parameters are compared with time-series properties as a misspecification diagnostic. No Bayesian integration over parameter uncertainty. | Stochastic volatility provides the first-order pricing improvement; jumps matter especially for short-dated options; richer specifications do not improve every performance criterion. All considered models remain misspecified to some degree. | Establishes that **model specification error is a distinct and potentially first-order margin**. Supports treating the one-factor GBM as an intentionally controlled benchmark rather than a realistic complete model. | Does not study Asian/APO payoffs, WTI, posterior parameter uncertainty, or PI-versus-plug-in pricing. |
| **Cummins & Esposito (2025), _Appraising Model Complexity in Option Pricing_** | Is incremental model complexity justified by incremental performance? | Large suite of affine/nonaffine stochastic-volatility jump-diffusion index-option models; formal Model Confidence Set comparison across pricing, hedging and volatility criteria. | Explicitly treats differences between cross-sectional option-implied and time-series parameters as evidence relevant to misspecification. Focus is model selection, not posterior propagation. | Some complexity pays, but not all: certain price-jump and parsimonious nonlinear specifications help, whereas other added components are redundant or detrimental. | Strong justification for the manuscript's design principle: **complexity must earn its place empirically**. Directly motivates separating "parameter integration within a map" from "changing the map." | Does not study Bayesian price integration, Asian options, commodity futures, or WTI APOs. |
| **Dumas, Fleming & Whaley (1998), _Implied Volatility Functions: Empirical Tests_** | Are flexible implied-volatility functions stable enough to improve future option valuation? | Deterministic volatility functions and ad hoc Black--Scholes implied-volatility rules; S&P 500 options, June 1988--December 1993. | Cross-sectional option prices generate implied-volatility functions; performance is evaluated one week out of sample. Not Bayesian. | More flexible functions fit in-sample better but can perform worse one week later; time-dependent flexibility is particularly vulnerable to overfitting. | Provides the closest methodological precedent for our **strict forward-in-time smile validation**. It supports using lagged surfaces rather than contemporaneous fit as the relevant empirical test. | Does not study WTI, average-price options, Bayesian parameter uncertainty, or historical-vs-posterior integration. |
| **Ewald, Wu & Zhang (2023), _Pricing Asian Options with Stochastic Convenience Yield and Jumps_** | How can commodity Asian options be priced under richer commodity dynamics? | Schwartz-type two/three-factor commodity model with stochastic convenience yield, stochastic rates and spot jumps; geometric Asian controls for arithmetic Asian Monte Carlo. | Risk-neutral commodity pricing model; no posterior parameter uncertainty. | Closed-form geometric controls produce large variance-reduction gains; jumps make path dependence materially more complicated because jump timing matters. | Defines a credible **richer-model alternative** to our parsimonious futures GBM and supports the limitations/future-work discussion. | Does not ask whether Bayesian posterior integration matters, does not use WTI APO settlement data, and does not compare parameter uncertainty with volatility specification. |
| **Gilder & Tsiaras (2020), _Volatility Forecasts Embedded in the Prices of Crude-Oil Options_** | Which option-implied volatility measure best forecasts future crude-oil realized volatility? | WTI futures options and high-frequency futures prices, January 1996--April 2016; compares ATM IV, model-free IV, OVX, corridor IV and realized-volatility forecasts. | Option-implied measures are forward-looking risk-neutral objects used to forecast realized volatility; the paper explicitly notes volatility-risk-premium contamination. | Narrow-range corridor implied volatility consistently outperforms the main option-implied and realized-volatility alternatives; OVX performs poorly in their comparisons. | Direct support for the idea that **option prices contain forward-looking volatility information absent from historical returns**, while also warning that the exact extraction method matters. | Forecasts realized volatility rather than APO prices; no Bayesian posterior integration and no path-dependent WTI APO valuation. |
| **Roh, Tourani-Rad, Xu & Zhao (2021), _Volatility-of-Volatility Risk in the Crude Oil Market_** | Is crude-oil volatility-of-volatility a priced and predictive risk factor? | USO options, July 2010--June 2018, plus OVX and high-frequency USO data; delta-hedged option gains and VOV measures. | Combines option-implied volatility information with realized jump measures; focuses on risk pricing and predictability rather than a single diffusion coefficient. | Oil VOV is significantly priced in delta-hedged gains and contains information distinct from ordinary oil volatility and equity VOV. | Supports interpreting our scalar \(\sigma_Q\) as an **effective/model-equivalent state** that may absorb omitted volatility dynamics and higher-order volatility risk. | Does not price WTI APOs and does not study Bayesian parameter uncertainty. Its underlying is USO rather than CL futures. |
| **Schwartz (1997), _The Stochastic Behavior of Commodity Prices: Implications for Valuation and Hedging_** | Which tractable stochastic structures describe commodity futures curves and their valuation implications? | One-, two-, and three-factor commodity models with mean reversion, convenience yield and stochastic rates; weekly oil, copper and gold futures; Kalman-filter estimation. | Structural commodity models estimated from futures term structures; not a Bayesian option-pricing exercise. | Commercial commodities show strong mean reversion; convenience yield and additional factors materially affect term structures, long-horizon valuation and hedging. | Establishes the canonical structural alternative to our one-factor futures GBM and explains why convenience yield/futures-curve dynamics are legitimate omitted-state concerns. | Does not study Asian-option posterior integration, WTI APO settlements, or option-implied volatility surfaces. |
| **Tee & Ting (2017), _Variance Risk Premiums of Commodity ETFs_** | How should risk-neutral variance and variance risk premia be extracted from American commodity ETF options? | Model-free volatility construction for gold, silver, natural-gas and crude-oil ETFs; OptionMetrics data through August 2013. | Explicit distinction between option-implied risk-neutral variance and realized/physical variance; studies model dependence in early-exercise adjustment. | Finds strong commodity variance risk premia and shows that common model-dependent early-exercise adjustments can overstate risk-neutral variance. | Supports the manuscript's **P-versus-Q interpretation**: historical and option-implied volatility need not coincide, and the method used to extract a Q-volatility object is itself a source of specification risk. | Uses ETFs rather than CL futures/APOs and does not propagate a posterior over pricing parameters. |

## How these papers change the manuscript argument

### 1. Parameter uncertainty and model specification must be separated

Bakshi et al. (1997) and Cummins & Esposito (2025) make it unsafe to frame a large pricing
error under the constant-volatility benchmark as evidence that Bayesian integration is failing.
A model can be internally coherent and still be misspecified. Our empirical decomposition should
therefore remain:

1. **within-model parameter integration:** PI versus PM under the same pricing map; and
2. **between-specification/state discrepancy:** historical volatility versus the effective
   volatility state required by option prices.

This separation is one of the manuscript's strongest conceptual features.

### 2. The forward-smile experiment is more important than contemporaneous fit

Dumas et al. (1998) show why an implied-volatility function that fits the contemporaneous
cross-section is not automatically useful: flexibility can overfit and deteriorate out of sample.
Accordingly, the manuscript should emphasize the strict prior-date experiments before discussing
same-date or leave-one-contract-out calibration results. The forward experiment is the appropriate
test of whether the option surface contains transferable pricing information.

### 3. Option-implied volatility is informative, but it is not a structural diffusion coefficient

Gilder & Tsiaras (2020), Tee & Ting (2017), and Roh et al. (2021) jointly support a cautious
interpretation of option-implied volatility. Crude-oil option prices contain forward-looking
information, but risk premia, strike selection, higher-order volatility risk, and extraction choices
all matter. The manuscript should therefore retain the phrase **effective risk-neutral/model-
equivalent volatility** and avoid describing the inferred APO scalar as "the true Q volatility."

### 4. The commodity benchmark is intentionally parsimonious

Schwartz (1997) and Ewald et al. (2023) show that commodity pricing can explicitly model mean
reversion, convenience yield, stochastic rates, correlated factors, and jumps. Their existence is
not a reason to hide the simple GBM benchmark; it is a reason to state its purpose precisely.
The baseline isolates one statistical question—posterior integration of volatility—before adding
additional uncertain state variables. A richer model is a robustness layer, not the paper's
starting claim.

## Relation to the existing core literature already in the repository

The eight new papers must be read together with four existing anchors:

- **Guidolin & Timmermann (2001):** Bayesian learning itself can alter option-price dynamics,
  implied-volatility skews and out-of-sample forecasts. Therefore, this paper is not the first to
  connect Bayesian learning and option prices.
- **Rombouts & Stentoft (working-paper version in the corpus):** computes risk-neutral predictive
  densities while taking parameter uncertainty into account and uses them for out-of-sample option
  pricing. Therefore, "integrating parameter uncertainty in option pricing" is not by itself the
  novelty claim.
- **Kemna & Vorst (1990):** establishes the geometric-average control-variate tradition for
  arithmetic average options.
- **Curran (1994):** supplies the geometric-conditioning approximation that is both a natural Asian
  pricing benchmark and directly relevant to the exchange's later use of Curran-style valuation.

These papers move the novelty away from the estimator/algorithm and toward the **mechanism and
empirical decomposition**.

## Defensible novelty statement after the literature review

A conservative version of the novelty claim is:

> The paper does not propose Bayesian option pricing or Asian-option pricing as new ideas.
> Instead, it isolates the incremental point-price effect of integrating posterior volatility
> uncertainty, shows that the effect is approximately governed by posterior dispersion times
> pricing curvature, maps the regimes in which this correction becomes economically material,
> and compares that within-model correction with the empirically much larger volatility-
> specification margin in a contract-consistent WTI Average Price Option application.

The empirical contribution has four pieces that should appear together:

1. a 175,000-history mechanism map varying information, volatility, moneyness, maturity and fixing;
2. direct PI-versus-PM comparison on actual WTI APO states;
3. independent numerical identification of sub-cent PI--PM gaps using Curran, high-precision
   pseudo-Monte Carlo and randomized Sobol; and
4. strict forward-in-time testing showing that prior-date option-implied volatility information
   changes pricing errors far more than posterior integration in the observed sample.

The claim should remain **conditional**: posterior integration can matter materially in weak-
information/high-curvature states, but it is not the dominant empirical margin in the observed
WTI APO sample.

## Citation deployment in the manuscript

| Manuscript location | Papers to deploy | Claim they should support |
|---|---|---|
| Introduction: why specification matters | Bakshi et al. (1997); Cummins & Esposito (2025) | Richer pricing models can improve some dimensions of performance, but added complexity is not automatically valuable. |
| Introduction: P versus option-implied Q information | Gilder & Tsiaras (2020); Tee & Ting (2017) | Option prices contain forward-looking volatility information and commodity variance risk premia make historical and option-implied volatility economically distinct objects. |
| Introduction / related work: Bayesian option pricing | Guidolin & Timmermann; Rombouts & Stentoft | Bayesian learning and parameter uncertainty in option pricing precede this paper. |
| Contract/methodology: Asian numerical literature | Kemna & Vorst; Curran | Arithmetic-average pricing requires approximation/simulation; geometric quantities provide useful controls/conditioning. |
| Methodology/limitations: commodity dynamics | Schwartz (1997); Ewald et al. (2023) | Convenience yield, mean reversion, stochastic rates and jumps are credible omitted dynamics in commodity Asian pricing. |
| Research design: why forward validation | Dumas et al. (1998) | Contemporaneous implied-volatility flexibility can overfit; out-of-sample transfer is the relevant test. |
| Robustness/interpretation of effective \(\sigma_Q\) | Roh et al. (2021); Tee & Ting (2017); Gilder & Tsiaras (2020) | A scalar implied volatility can absorb volatility risk premia, VOV, skew and other omitted risk-neutral features. |
| Conclusion: complexity trade-off | Cummins & Esposito (2025) | Additional model complexity should be judged by incremental empirical performance. |

## Direct-overlap precedents discovered during synthesis

The eight-paper acquisition is complete. The synthesis surfaced a smaller set of **more directly overlapping** papers. Their bibliographic roles and legal/free sources are now verified in `DIRECT_PRECEDENTS_SOURCES.md`; the final PDFs/extractions should still be added to the local corpus for archival completeness.

### Critical

1. **Shiraya & Takahashi (2011), "Pricing Average Options on Commodities," _Journal of Futures Markets_, 31(5), 407--439, DOI 10.1002/fut.20481.**
   - Directly studies average commodity options under Heston and extended \(\lambda\)-SABR.
   - The working-paper version explicitly discusses calibrating stochastic-volatility models to
     American vanilla WTI futures options and using those parameters to value WTI average options.
   - This is the closest precedent for the "independent vanilla WTI Q state -> average option"
     extension and is mandatory for a JFM submission.

2. **Gupta & Reisinger (2014), "Robust Calibration of Financial Models Using Bayesian Estimators," _Journal of Computational Finance_, 17(4), 3--36, DOI 10.21314/JCF.2014.285.**
   - Builds posterior distributions for calibrated model parameters and propagates them to exotic-
     option prices.
   - This is a direct prior for Bayesian parameter uncertainty in exotic pricing and must be used
     to narrow the Bayesian novelty claim.

3. **Gan, Wang & Yang (2020), "Machine Learning Solutions to Challenges in Finance: An Application to the Pricing of Financial Products," _Technological Forecasting and Social Change_, 153, 119928, DOI 10.1016/j.techfore.2020.119928.**
   - Uses real WTI Average Price Option data (from Barchart) in an empirical Asian-option pricing
     application.
   - It is methodologically very different—model-free/deep-learning rather than Bayesian
     structural pricing—but it is a direct empirical WTI-APO precedent and should be cited.

### Secondary but useful

4. **Guillaume & Schoutens (2015), "Bid-Ask Spread for Exotic Options under Conic Finance," DOI 10.1007/978-3-319-09114-3_4.**
   - Studies model/calibration/parameter uncertainty for path-dependent exotics, explicitly
     including arithmetic Asian options.
   - It is not the same Bayesian posterior-integration problem, but it is useful evidence that
     parameter/calibration uncertainty can be magnified by path dependence.

A targeted search did **not** surface a paper combining all of the following in one design:
Bayesian posterior integration of historically inferred volatility, a mechanism based on pricing
curvature and posterior dispersion, and empirical WTI APO validation. This is a search result,
not proof of absence, so the manuscript should use "to our knowledge" only after the three
critical papers above have been read and their reference lists checked.


### Refined novelty boundary after the direct-precedent check

The direct-precedent search eliminates three possible novelty claims:

- **not first WTI APO pricing study:** Shiraya & Takahashi already model WTI average-price contract mechanics under stochastic-volatility dynamics and calibrate to vanilla WTI options;
- **not first Bayesian propagation to exotic prices:** Gupta & Reisinger explicitly map a posterior over calibrated model parameters into exotic-option prices;
- **not first empirical use of Barchart WTI APO data:** Gan, Wang & Yang use real Barchart WTI Average Price Option observations in a deep-learning pricing application.

The manuscript should therefore claim novelty only at the intersection that remains unsupported by those antecedents: a controlled mechanism for the PI--PM correction, large-scale mapping of that mechanism over information and contract states, and an empirical decomposition of posterior integration versus volatility specification in a contract-consistent WTI APO setting.

## What is no longer a literature gap

After the eight-paper addition, the following areas are sufficiently anchored for the current
draft:

- general option-pricing model misspecification and complexity;
- deterministic/implied-volatility surface validation;
- crude-oil option-implied volatility forecasting;
- commodity variance/VOV risk;
- structural commodity futures dynamics;
- richer stochastic-volatility/jump Asian-option pricing.

The remaining work is now **precision of positioning**, not bibliography volume.
