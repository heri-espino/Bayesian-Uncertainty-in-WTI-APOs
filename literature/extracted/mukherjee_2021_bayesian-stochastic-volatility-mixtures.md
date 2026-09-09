---
id: "mukherjee_2021_bayesian-stochastic-volatility-mixtures"
source_pdf: "../pdf/mukherjee_2021_bayesian-stochastic-volatility-mixtures.pdf"
source_filename: "mukherjee_2021_bayesian-stochastic-volatility-mixtures.pdf"
format: "academic-paper"
extraction_profile: "token-efficient-high-fidelity"
extraction_mode: "full-page-ocr"
extraction_quality: "excellent"
extraction_score: 108.0
formula_enrichment: "codeformulav2"
table_structure: "accurate"
tables_png: 2
figures_png: 3
assets_dir: "../assets/mukherjee_2021_bayesian-stochastic-volatility-mixtures"
references_file: "../references/mukherjee_2021_bayesian-stochastic-volatility-mixtures.references.md"
---

<!-- p:1 -->

## Bayesian Analysis of Stochastic Volatility Model using Finite Gaussian Mixtures with Unknown Number of Components

Soham Mukherjee

School of Mathematics and Statistics, University of Hyderabad

October 26, 2021

###### Abstract

Financial studies require volatility based models which provides useful insights on risks related to investments. Stochastic volatility models are one of the most popular approaches to model volatility in such studies. The asset returns under study may come in multiple clusters which are not captured well assuming standard distributions. Mixture distributions are more appropriate in such situations. In this work, an algorithm is demonstrated which is capable of studying finite mixtures but with unknown number of components. This algorithm uses a Birth-Death process to adjust the number of components in the mixture distribution and the weights are assigned accordingly. This mixture distribution specification is then used for asset returns and a semi-parametric stochastic volatility model is fitted in a Bayesian framework. A specific case of Gaussian mixtures is studied. Using appropriate prior specification, Gibbs sampling method is used to generate posterior chains and assess model convergence. A case study of stock return data for State Bank of India is used to illustrate the methodology.

Keywords: Birth-Death process, Gaussian mixtures, Semi-parametric, Stochastic volatility, Point process, Gibbs sampler, Markov Chain Monte Carlo.

MSC2020-Mathematics Subject Classifications 62F15

## 1Introduction

The analysis of stock market has always been a topic of constant interest in the world of financial researchers. Assessment of risk before investing in a stock is a necessity. The most popular way involving statistical approach is using the time series data of stock returns and model the volatility.

I wish to express my sincere gratitude to Prof. Diganta Mukherjee for providing the NSE-Nifty data on State Bank of India, insightful reviews and continued support.


<!-- p:2 -->


Using such models, the underlying volatility are studied to assess the risk involved in a particular stock to make an informed decision. One of the popular models involve the evolution of volatility dy .()   ()         l alternative approach involve modelling the volatility probabilistically through a state-space model where the logarithm of the squared volatility or the latent states, follow an AR (1) process. This specification is known as Stochastic Volatility model first developed by Taylor (1982). Further works on similar model specifications include Hull and White (1987), Chesney and Scott (1989), Taylor (1986, 1994), Jacquier et al. (1994) and Shepherd (1996). Parametric and semi-parametric estimation methods of SV models include works of Harvey et al. (1994), Carter and Kohn (1994), Kim et al. (1998), and Omori et al. (2007). Except the first, all three specify and demonstrate SV models using a Gaussian mixture approximation. To implement mixture models, the number of components need to be specified. Use of infinite component DPMs are popular since they represent the most general case of mixtures but comes at a cost of enhanced analytical complexity. A good balance is to assume that the mixture components are finite but unknown. The most important works like Richardson and Green (1997), Stephens (2000a) and Frühwirth-Schnatter (2006) demonstrate how to adjust and optimize the number of components for model specifications. Majority of these works involve some sort of Bayesian computation and simulation. Kim, Shepherd and Chib (1998) briefly mentioned how semiparametric SV models could be implemented using ReversibleJump MCMC developed by Richardson and Green (1997). Later, Asai (2009) demonstrated use of mixture SV models for return volatility modeling by fixing a 2 component mixture. The Markov Chain Monte Carlo methods of inferences used were discussed in Gelfand and Smith (1990), Chib and Greenberg (1996) and Gilks, Richardson and Spiegelhalter (1996).

The case study data for NSE-Nifty State Bank of India stocks had observations coming from clusters of Gaussian population which is represented using finite Gaussian mixtures in this work. The data posed some typical challenges that are usually related to Bayesian inference for mixture distribution. Along with significant computational resource and time, there were issues of label switching for posterior means. Label switching is common for Bayesian mixture analysis where the swapping of component parameters due to permutations while simulation result in multiple posterior maxima. Since, the standard Bayesian method is to estimate parameters from marginal posterior means, swapping of mixture component parameter causes serious identification issues. Richardson and Green (1997) used ordering of posterior means as a constraint to deal with label switching. In Stephens (2000b), it is shown that these constraints in general fails to solve the problem and relabelling algorithms need to be implemented. Further, according to Diebolt and Rou ut t   oet o o t ort , (ut oud mean a divergent posterior chain and unusable estimates. So proper informative priors specified by previous works had to be used. Although using finite mixture distributions of stock returns and modelling their volatility is a popular approach, the method of dealing with finite unknown components and their optimization is usually done using RJMCMC method of Richardson and Green (1997). In this work, the alternate approach Birth-death MCMC developed by Stephens (2000a) is used which is both easy to implement and label switching invariant by construction. Further, a modified 3 dimensional point process for the Gaussian mixtures is used with varying e  (a s          eom with few adjustments in order to incorporate the Bayesian SV model via Gibbs sampling steps and priors used by Kim, Shepherd and Chib (1998). This approach brings a new outlook in the field of Bayesian semi-parametric SV model which is illustrated.


<!-- p:3 -->


In this paper, the SV model as well as its finite Gaussian mixture specification is demonstrated in the section 2.1. In section 2.2, the algorithm along with the adjustments for finite Gaussian mixtures with unknown number of components are determined and discussed in detail. The prior specifications and the Gibbs sampling steps for the Bayesian SV model is demonstrated in section 2.3. Using these, the case study is used for illustration purpose in section 3 to demonstrate model fitting and performance followed by a discussion in section 4.

## 2 Methodology

The methodology section is divided into three parts. Section 2.1 describes the SV model that is used in this paper alongside the finite mixture specifications. 2.2 demonstrates the setup and algorithm to determine the number of components of the mixture distribution which is achieved by using a Birth-Death MCMC process. Finally, 2.3 explores the implementation of the determined number of components and its usage to obtain the posterior of the required parameters to fit a stochastic volatility model.

### 2.1 Model

The simple or canonical stochastic volatility model is considered for this work.

$$y _ { t } = \epsilon _ { t } \exp ( h _ { t } / 2 )$$

$$h _ { t } = c + \phi ( h _ { t - 1 } - c ) + \eta _ { t }$$


<!-- p:4 -->


where |φ| &lt; 1 and yt is asset return at t. exp(ht/2) is volatility, so ht is log of squared volatility. et ∼ iid with E(et) = μet and Var(et) = σet2, ηt ∼ iidN(0, σ2). et and ηs are assumed to be mutually independent ∀t, s. €t is used to model yt. This form of the model has been used by Taylor (1986, 1994), Hull and White (1987), Chesney and Scott (1989), Shepherd (1996), Ghysels, Harvey and Renault (1986), Jacquier, Polson and Rossi (1994), Kim, Shephard and Chib (1998). These above cited works discusses its basic econometric properties as well as estimation procedures of SV models. The same form is also used by Asai (2009) where author discusses its extension using two-component gaussian mixtures. In this work, €t in the canonical model is assumed to follow mixture distribution with k components (where k is unknown). It is denoted by the usual form of a mixture distribution

$$p ( \epsilon _ { t } | \pi , \mu , \sigma ) = \pi _ { 1 } f ( \epsilon _ { t } ; \mu _ { 1 } , \sigma _ { 1 } ) + \dots + \pi _ { k } f ( \epsilon _ { t } ; \mu _ { k } , \sigma _ { k } )$$

Literature on this form of mixtures have been discussed in the works of Frühwirth-Schnatter (2006). It is further assumed that et is a finite mixture of univariate normals based on the discussions provided by Fama (1965) with adjustments made in the form of varying means in this case. So, f(et; μi, σi) is N(μi, σ2) in the above notation.

### 2.2 Determining the number of components

To address the unknown components and weights, the Birth-Death MCMC by Stephens (2000a) is followed. Using the notations of a point process, et is written in terms of (πi, μi, σi) in the form et = {(π1, μ1, σ1), ..., (πk, μk, σk)} which belongs to parameter space Ωk. The author denotes the Births and Deaths as follows. When a birth occurs at (π, μ, σ), then the process jumps to

$$\epsilon _ { t } \cup ( \pi , \mu , \sigma ) = \{ ( \pi _ { 1 } ( 1 - \pi ) , \mu _ { 1 } , \sigma _ { 1 } ) , \dots , ( \pi _ { k } ( 1 - \pi ) , \mu _ { k } , \sigma _ { k } ) , ( \pi , \mu , \sigma ) \} \in \Omega _ { k + 1 }$$

In case of a death at (πi, μi, σi) ∈ ∈t, the process jumps to

$$\epsilon _ { t } \, \vee \, ( \pi _ { i } , \mu _ { i } , \sigma _ { i } ) = \{ ( \pi _ { 1 } / ( 1 - \pi _ { i } ) , \mu _ { 1 } , \sigma _ { 1 } ) , \dots , ( \pi _ { i - 1 } / ( 1 - \pi _ { i } ) , \mu _ { i - 1 } , \sigma _ { i - 1 } ) , \\ ( \pi _ { i + 1 } / ( 1 - \pi _ { i } ) , \mu _ { i + 1 } , \sigma _ { i + 1 } ) , \dots , ( \pi _ { k } / ( 1 - \pi _ { i } ) , \mu _ { k } , \sigma _ { k } ) \} \in \Omega _ { k - 1 } \quad ( 5 )$$

A birth increases number of components by one and a death decreases number of components by one. The entire setup is defined in a way that births and deaths are inverse mechanisms and the weights sum up to unity. When the process is at et ∈ Ωk, births and deaths occur as independent Poisson process. Births occur at overall rate β(€t) which is chosen with density b(€t; (π, μ, σ)). On the other hand, a point dies independently of others as a Poisson process with rasΩ (),  = ()  (l  I( ( ((,  ) :(,  ) \ )) = (), (tns the specific hierarchical prior on the parameters (k, π, μ, σ) used in Stephens (2000a) along with a density r(k, π, μ, σ) the mixture specification becomes invariant under relabeling of components which will eventually result in a more practical posterior. It is worthwhile to note that due to this specification, no additional conditioning on the parameters, for example, ordering of means which was used in Richardson and Green (1997) is unnecessary. Assuming π and σ are a priori independent and identically distributed from a distribution with density p(μ, σ), then


<!-- p:5 -->


$$r ( k , \pi , \mu , \sigma ) = p ( k ) \tilde { p } ( \mu _ { 1 } , \sigma _ { 1 } ) \dots \tilde { p } ( \mu _ { k } , \sigma _ { k } )$$

A special case of Diebolt and Robert (1994), Richardson and Green (1997) and Stephens (2000a) is to use mixtures of univariate normals. The likelihood is specified as follows.

$$L ( k , \pi , \mu , \sigma ) = p ( y _ { t } | k , \pi , \mu , \sigma ) = \prod _ { j = 1 } ^ { n } [ \pi _ { 1 } f ( \epsilon _ { t j } ; \mu _ { 1 } , \sigma _ { 1 } ) + \dots + \pi _ { k } f ( \epsilon _ { t j } ; \mu _ { k } , \sigma _ { k } ) ]$$

As per the construct, this is invariant under permutations of component labels. In case of financial studies with asset returns, yt is the asset return data. Using the theorem proposed by Stephens (2000a), the posterior

$$p ( k , \pi , \mu , \sigma | y _ { t } ) \subset L ( k , \pi , \mu , \sigma ) r ( k , \pi , \mu , \sigma )$$

has stationary distribution provided b and d satisfy

$$( k + 1 ) d ( \epsilon _ { t } ; ( \pi , \mu , \sigma ) ) r ( \epsilon _ { t } \cup ( \pi , \mu , \sigma ) ) L ( \epsilon _ { t } \cup ( \pi , \mu , \sigma ) ) k ( 1 - \pi ) ^ { k - 1 } = \beta ( \epsilon _ { t } ) b ( \epsilon _ { t } ; ( \pi , \mu , \sigma ) ) r ( \epsilon _ { t } ) L ( \epsilon _ { t } )$$

As with any other Bayesian implementation, prior specification is one of the most important aspect of a methodology. In this paper, the priors for the special case by Richardson and Green (1997) and Stephens (2000a) is used. A truncated Poisson prior is assumed for number of components k.

$$p ( k ) \, \infty \, \frac { \lambda ^ { k } } { K ! } ; ( k = 1 ( 1 ) 1 0 , s a y )$$

where λ is a constant. For the rest of the parameters, the following prior specifications are considered.

$$\beta \sim \Gamma ( 2 l , ( 2 m ) ^ { - 1 } )$$

$$\pi \sim \mathcal { D } ( \gamma )$$


<!-- p:6 -->


$$\mu _ { i } \sim N ( \zeta , \tau ^ { - 1 } )$$

$$\sigma _ { i } ^ { - 1 } | \beta \sim \Gamma ( 2 \alpha , ( 2 \beta ) ^ { - 1 } )$$

where β is a hyperparameter; D(μ) denotes the symmetric Dirichlet distribution with density

$$\frac { \Gamma ( k \gamma ) } { \Gamma ( \gamma ) ^ { k } } \pi _ { 1 } ^ { \gamma - 1 } \dots \pi _ { k - 1 } ^ { \gamma - 1 } ( 1 - \pi _ { 1 } - \dots - \pi _ { k - 1 } ) ^ { \gamma - 1 }$$

ζ is the midpoint of the observed interval of variation in the data, R is the length of the interval, R2, α = 2, l = 0.2, m = 1 , γ = 1. Using these, a Markov chain with suitable station100l ary distribution is simulated. The generalized algorithm is implemented starting with the initial specification of et = {(π1, μ1, σ1), ..., (πk, μk, σk)} ∈ Ωk. Using the priors, the following steps are performed.

1. The birth rate β(€t) = λb is specified by the researcher
2. Using the birth rate and (9) the death rate is calculated for each component as

$$\delta _ { j } ( \epsilon _ { t } ) = \lambda _ { b } \frac { ( L ( \epsilon _ { t } \wedge ( \pi _ { j } , \mu _ { j } , \sigma _ { j } ) ) } { L ( \epsilon _ { t } ) } \frac { p ( k - 1 ) } { k p ( k ) }$$

3. The total death rate is calculated as δ(et) = Σj δj(et)
4. The time to next jump is simulated from exponential distribution with mean 1/(β(€t) + δ(€t))
5. The birth and death probabilities are computed as β(∈t) and δ(€t) respectively. β(∈t)+δ(et) (7)g+(t)g
6. €t is adjusted according to birth or death as defined in (5) and (6). Birth for the point (π, μ, σ) is obtained using b(y; (π, μ, σ)) = k(1 − π)k−1p(μ, σ) by simulating π from k(1 − π)k−1 and (μ, σ) from p(μ, σ) independently. Death for a component is obtained from (πi, μi, σi) ∈ ∈t selected with probability δj(∈t)/δ(et)
7. Steps 2 to 6 are repeated until convergence or max iterations

Alternatively, the Step (7) could be skipped, that is the above steps are performed only once in order to obtain an updated initial value of (k, π, μ, σ) denoted by (k(j), π(j), μ(j), σ(j)). Using Gibbs sampler,

1. Sample μ(j+1) from p(μ|k(j+1), π(j), σ(j), yt)
2. Sample σ(j+1) from p(σ|k(j+1), μ(j+1), π(j), yt)


<!-- p:7 -->


3. Sample π(j+1) from p(π|k(j+1), μ(j+1), σ(j+1), yt)

Repeating this until model convergence would provide the required posterior sample of (k, π, μ, σ) which would then be presented alongside the posteriors of SV model parameters demonstrated in the following section 2.3.

### 2.3 Fitting the stochastic volatility model

Having simulated the number of components and the weights, all that is left is simulating the latent volatility model. Following the works of Kim et al. (1998) and Asai (2009), the priors for (c, φ, σ2) follows c ∼ N(0, 10), (φ + 1)/2 ∼ Beta(φ2, φ1), σ2 ∼ IG(σr/2, Sσ/2) where IG denotes inverse gamma distribution; φ1 = 20, φ2 = 1.5, σr = 5, Sσ = 0.01σr. The prior distribution of h0 is set to be the unconditional distribution of ht that is h0 ∼ N(c, σ2/(1 − φ2)). The Gibbs sampler is used to generate samples using the parameters (c, φ, σ2) and log-squared volatility ht given the data yt. The following steps are followed.

1. Initialize h and (c, φ, σ2)
2. Sample ht from ht|h\t, , φ, σ2, yt,t = 1(1)n
3. Sample σ2|y, ht, φ, c
4. Sample φ|ht, c, σ 2 η
5. Sample c|ht, φ, σ 2
6. Re-iterate step 2

The Gibbs sampler will be required to repeat steps through 2 to 5 many thousand times or even higher to generate samples from c, φ, σ2, ht|yt. This should provide an appropriate posterior sample for the Stochastic Volatility Mixture Gaussian model.

## 3 Illustration

The algorithm is implemented in the case study of NSE-Nifty covering 6 working days of September 2017 stocks of State Bank of India which contains about 409 observations in 10 minute time intervals. The various exploratory plots for the return data are The plots show the range of return values for the case study. Additionally the data is free of outliers. The density plots provide indication of presence of mixtures and the QQplot indicates that the returns are leptokurtic. The leptokurtic nature of asset returns in financial studies are recognized since Mandelbrot (1963) and Fama (1965). Fama (1965) further specifies a possible explanation of heavy tailed nature could be a mixture of normal distributions with same mean and different variances. The density plot here however shows distinct modal peaks. So, it will be adequate to consider different means as well.


<!-- p:8 -->


Figure 1: Summary Plots

A: Time series plot

B: Boxplot

65


0


Y

-0-

-0.5

-1.0


0

100

200

300

400

Time

C: Density plot

D: QQplot

8

Sample Quantiles

65

Density

0.0

40

-0.5

0

-1.0


-0.5

0.0

0.5

1.0

-3

-2

-1

0

1

2

3

N = 409 Bandwidth = 0.1083

Theoretical Quantiles

Performing the algorithm in 2.2 once to obtain a set of initial values, a Gibbs sampling is implemented to obtain a posterior sample of number of components k. The simulation is run for 1000 iterations with 100 burn-in. An easy-to-use R package bmixture by Mohammadi (2021) will provide similar and necessary implementation for the initial step. The number of components are determined to be

$$( 2 , 1 , 2 , 1 , \dots , 8 , 9 , 8 , 7 , 6 )$$

The number of components is considered k = 6 and the initial values of the mixture components generated by the Birth-Death MCMC algorithm is given as


<!-- p:9 -->


```
&i = (0.0604687, 0.1310388, 0.1116203, 0.3106168, 0.2236884, 0.1625669)
                &i = ( -0.80323887, -0.4422737, -0.2452619, -0.1486318, 0.2454454, 0.4692405)
                &i = (0.004225127, 0.002882527, 0.0006002868, 0.101062441, 0.01168029, 0.018423264)
```

Using the Gibbs sampling steps in 2.3, the SV model is fitted using JAGS in R. The posterior values of the parameters are obtained and recorded when a convergent model is observed. The GelmanRubin statistic developed by Gelman and Rubin (1992) is used to assess model convergence. The maximum value for Gelman-Rubin statistic for the obtained model is 1.063 which is acceptable for a Bayesian model assessment as a numerical convergence indication. The posterior means are recorded which can be used to specify the SV model. A comparison with a non-mixture specified Bayesian SV model with similarly tuned Gibbs sampler as well as same prior specifications is shown.

Table 1: SV and Mixture SV comparison

| Parameters   | SV       | SV    | Mixture SV   | Mixture SV   |
|--------------|----------|-------|--------------|--------------|
|              | Mean     | Rhat  | Mean         | Rhat         |
| c            | -0.343   | 1.193 | -0.136       | 1.028        |
| φ            | 0.949    | 1.128 | 0.983        | 1.051        |
| σ η t        | 0.007    | 1.022 | 0.215        | 1.063        |
| deviance     | 1143.911 | 1.060 | -798.982     | 1.009        |

This table shows comparison between the posterior means of SV parameters for the two models. Without the mixture specification that is by considering the data is not comprised of a cluster of observations, the numerical convergence of the model is not achieved which is indicated by the Gelman-Rubin statistic value of &gt; 1.1 for some parameters. Even the deviance posterior mean value is much lower for the Mixture SV model. This provides the insight that mixture specification was indeed necessary. The complete summary table along with diagnostics for Mixture SV model is provided in the Appendix (Table 2) of this paper. The posterior means of mixture component parameters are observed. Specifically, it is interesting to see the variance of each of the components is very close. This indicates that the components are similarly dispersed. In the summary table, the inverse of variance is provided and its small values indicate somewhat large variance. The means of the components are very close to zero which captures and represents the asset return data successfully. The weights assigned to the clusters add up to unity satisfying the mixture specification conditions. The weight assigned to the first component which is N(-0.008, 17.2413) is the largest among the six components. The fitted SV model is given as in (1) and (2) with c = −0.136, φ = 0.983 and ηt ∼ iidN(0, 0.215). For visual proof of convergence, trace plots are obtained for the posterior samples of model parameters. The trace plots are provided in the Appendix (Figure 2). Couple of parameters show less amount of mixing of two posterior chains compared to others. A natural solution is to simulate model for more iterations. That would provide more posterior samples, which will in turn show better quality trace plots with converged chains and better mixing but it would also take much longer time as well has more computation power and resources. Since, numerical convergence is achieved, more simulations are not performed. The density plots provided in the Appendix (Figure 3) for the posterior sample show some deviation from the prior specifications. The visual difference is not very large which means the prior specifications are appropriate. The slight deviations also speak about the quality of the data since the data had enough information to influence the prior choices.


<!-- p:10 -->


## 4 Discussion

This paper demonstrates a Bayesian semi-parametric SV model for situations where target variable nn n    mn  g is o   o nn number of components without any hard evidence does not really reflect a realistic scenario. The usage of finite mixtures by introducing a flexibility in number of components provides a practical approach although the computation becomes comparatively resource intensive. In this work the Birth-Death MCMC is used instead of the more popular RJMCMC due to the ease of implementation and intuitiveness. Further, the algorithm being label switching invariant makes the posterior means more reliable without having to introduce additional parameter constraints. The number of components essentially comes from the appropriate choice of priors as well as a user specified birth rate. This setup results in death rate greater than birth rate most of the time. This means that the number of components will die faster than their birth. To compensate this, an appropriate starting value for the number of components is specified for the case study using the crude estimate of distinct modes in the density graph of the stock returns. The algorithm demonstrated holds for more general distributions (non-Gaussian) with more parameters. The point process specification will need to be adjusted to reflect a higher dimension and the algorithms can be modified accordingly along with appropriate priors. The mixture components posterior estimates show Gaussian means close to zero along with very close variance. The dispersion of the clusters of asset returns can be claimed similar. The SV model obtained in the case study shows model convergence and the fitted model parameters satisfy all model constraints like sum of mixture weights to unity and φ &lt; 1. These results make the fitted SV model for the case study a practical and usable model. The sample size of 409 is used due to computational resource limitations, however satisfactory results o  o o o us o os  o o s u  ore an exact competitive model was difficult to find in existing literature. The non-mixture specified model is compared and the limitations are highlighted in the previous section. Models from other Bayesian samplers are not compared due to the compatibility issues for the specific Bayesian packages in R. Due to this, such complex models from different samplers are very difficult to compare and so it is kept outside the scope of this paper. Potential extensions could include a more robust mixture component optimization which would be less sensitive to starting point of k. This may be explored by modifying user specified birth rates and replacing it with data dependent birth rates. Although the algorithm has provisions for non-Gaussian distributions, only the specific case of univariate mixture normals is studied. Other potential distributions may be explored but that would also require different prior specification through rigorous prior elicitation methods which are beyond the scope of this paper.


<!-- p:11 -->

## Appendix

Table 2: Summary Diagnostic Table

| Parameter                                                                                                          | mu.vect                                                                                                                                      | sd.vect                                                                                                                             | 2.50%                                                                                                                                        | 25%                                                                                                                                        | 50%                                                                                                                                          | 75%                                                                                                                                 | 97.50%                                                                                                                               | Rhat                                                                                                                                |
|--------------------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------|
| c μ 1 μ 2 μ 3 μ 4 μ 5 μ 6 φ π 1 π 2 π 3 π 4 π 5 π 6 σ η t σ - 1 1 σ - 1 2 σ - 1 3 σ - 1 4 σ - 1 5 σ - 1 6 deviance | -0.136 -0.008 -0.001 -0.001 -0.009 -0.005 -0.001 0.983 0.201 0.175 0.144 0.188 0.16 0.132 0.215 0.058 0.057 0.058 0.058 0.057 0.058 -798.982 | 0.308 0.063 0.066 0.072 0.064 0.068 0.068 0.012 0.294 0.286 0.244 0.297 0.26 0.242 0.031 0.056 0.052 0.055 0.056 0.058 0.057 64.238 | -0.736 -0.116 -0.119 -0.123 -0.115 -0.125 -0.132 0.942 0.001 0.001 0.001 0.001 0.001 0.001 0.159 0.01 0.009 0.008 0.008 0.008 0.007 -928.981 | -0.352 -0.049 -0.046 -0.047 -0.049 -0.05 -0.048 0.983 0.011 0.01 0.01 0.011 0.012 0.009 0.192 0.023 0.024 0.024 0.024 0.024 0.023 -839.455 | -0.145 -0.029 -0.023 -0.024 -0.028 -0.027 -0.018 0.986 0.034 0.029 0.025 0.031 0.031 0.026 0.212 0.041 0.042 0.041 0.041 0.04 0.039 -799.588 | 0.07 0.043 0.052 0.049 0.042 0.043 0.05 0.989 0.29 0.168 0.142 0.208 0.187 0.082 0.235 0.073 0.073 0.071 0.069 0.071 0.068 -758.839 | 0.485 0.108 0.115 0.139 0.112 0.12 0.12 0.994 0.912 0.907 0.846 0.922 0.907 0.899 0.282 0.216 0.199 0.217 0.212 0.195 0.221 -670.416 | 1.028 1.003 1.001 1.010 1.001 1.001 1.005 1.051 1.004 1.000 1.033 1.008 1.006 1.008 1.063 1.005 1.005 1.012 1.004 1.011 1.012 1.009 |


<!-- p:14 -->


Figure 2: Trace Plots

250000


[]n

150000

[9]n

150000

pi[5]

150000


50000

5000


0.0 0.1 0.2

-0.2

t0

-0.1

€0-

80

0.4

00

0.4

0.2

00

250000


150000

[]n

150000

pi[4]

150000


5000


50000

0255

0.15

0.3

t0

-0.1

€0-

80

40

00

0.3

0.0 0.1 0.2

250000


150000

mu[4]

150000

[ε]!d

5000

150000

50000


5000


0.93 ,0.95 0.97 0.99

0

00

-0.2

80

40

00

0.3

0.2

0.1

250000


deviance

150000

m]3

150000


sinv[1]

150000

[in]l]

150000

50000

5000


50000

-7000

006-

0.1

-0.1

€0-

80

0.4

00

0.4

0.2

00

0.4

0.2

0.0

250000


150000

2]

150000

pi[1]

150000

pi[6]

150000

[innnl5]

150000

50000

5000


-1.0 -0.5 0.0 0.5

0.1

-0.1

€0-

80

40

0.0

80

0.4

0.0

9.0

0.4

0.2

0.0


<!-- p:15 -->


Figure 3: Posterior density plots

2

0

0.5

0.8

01

0.4

[]n

[9]n

0.0

[]!d]

0.6

sinv[4]

0.3

-0.1

2

-0.1

-0.2

10

-02

-0.3

0


12

8

9

10

15

10

5

0

15

10

0

0.35

03

22

0.8

0.30

03

01

90

025

[]n

pi[4]

sinv[3]

2

0.20

-0.1

01

0.15

-0.2

0.2

-0.3

0

0.0

12

8

9

10

20

15

10

9

0

15

10

9

0

1.00

0.4

22

0.8

860

01

9.0

mu[4]

0.0

[ε]!d

Sihnl2]

2

-0.1

0

0.94

0.2

01

-0.2

092

-0.3

0


80

09

40

20

12

8

9

25

20

15

10

9

15

10

9

0

500

0.5


-700

009-

02

01

0.8

0.4

deviance

008-

0.0

90

sinv[1]

0.3

sinv[6]

-0.1

2

02

006-

-0.2

0.2

10

01

-1000

-0.3

0


9000

00003

0.000

15

10

5

20

15

10

5

0

15

10

15

10

02

0.6

55

0.8

8.0

0.5

0.0

96

0.6

0.4

0

2]

pi[1]

pi[6]

[innl5]

-0.1

0.4

-.0

02

-0.2

0.2

02

-1.0

-0.3

0


1.2

80

0.4

00

10

8

2

0

15

10

9

0

20

15

10

15

10

0
