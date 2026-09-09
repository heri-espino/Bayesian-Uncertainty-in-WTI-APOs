---
id: "rombouts_2009_bayesian-option-pricing-mixed-normal-models"
source_pdf: "../pdf/rombouts_2009_bayesian-option-pricing-mixed-normal-models.pdf"
source_filename: "rombouts_2009_bayesian-option-pricing-mixed-normal-models.pdf"
format: "academic-paper"
extraction_profile: "token-efficient-high-fidelity"
extraction_mode: "hybrid"
extraction_quality: "excellent"
extraction_score: 108.0
formula_enrichment: "codeformulav2"
table_structure: "accurate"
tables_png: 9
figures_png: 5
assets_dir: "../assets/rombouts_2009_bayesian-option-pricing-mixed-normal-models"
references_file: "../references/rombouts_2009_bayesian-option-pricing-mixed-normal-models.references.md"
---

<!-- p:1 -->

Centre Interuniversitaire sur le Risque, les Politiques Économiques et l'Emploi

Cahier de recherche/Working Paper 09-26

### Bayesian  Option  Pricing  Using  Mixed  Normal  Heteroskedasticity Models

Jeroen V.K. Rombouts Lars Stentoft

Août/August  2009

Rombouts: Institute of Applied Economics at HEC Montréal, CIRANO, CIRPÉE, Université Catholique de Louvain (CORE),  3000  Côte  Sainte-Catherine,  Montréal  (QC)  Canada    H3T  2A7 ;  phone :  +1 514 340-6466 ;  fax : +1 514 340-6469

jeroen.rombouts@hec.ca

Stentoft: Department of Finance at HEC Montréal, CIRANO, CREATES, CREF

The authors thank Eric Renault, Kris Jacobs, as well as seminar participants at Center (Tilburg University), CORE (Catholic  University  of  Louvain),  CREATES  (University  of  Aarhus),  and  the  Economics  Department  at  Boston University for comments. The first author thanks IFM2 for financial support. The second author thanks CREATES (Center for Research in Econometric Analysis of Time Series, funded by the Danish National Research Foundation) for financial support.


<!-- p:2 -->


##### Abstract:

While stochastic volatility models improve on the option pricing error when compared to the  Black-Scholes-Merton  model,  mispricings  remain.  This  paper  uses  mixed  normal heteroskedasticity  models  to  price  options.  Our  model  allows  for  significant  negative skewness  and  time  varying  higher  order  moments  of  the  risk  neutral  distribution. Parameter inference using Gibbs sampling is explained and we detail how to compute risk  neutral  predictive  densities  taking  into  account  parameter  uncertainty.  When forecasting out-of-sample options on the S&amp;P 500 index, substantial improvements are found compared to a benchmark model in terms of dollar losses and the ability to explain the smirk in implied volatilities.

Keywords: Bayesian  inference,  option  pricing,  finite  mixture  models,  out-of-sample prediction, GARCH models

##### JEL Classification: C11, C15, C22, G13


<!-- p:3 -->


While the Black-Scholes-Merton (BSM) model of Black and Scholes (1973) and Merton (1973) remains a standard tool for practitioners, when it comes to option pricing many attempts have been made on extending the model to obtain a better fit to actually observed prices. In particular, several studies have shown that the BSM model, which assumes constant volatility and Gaussian returns, severely underprices out of the money put options, particularly those with short maturity. In terms of implied volatilities, this leads to the well-known smile or smirk across moneyness, which is found to be particularly pronounced for index options. Intuitively, such findings can be the result of either non constant volatility or non Gaussian returns, or a combination of the two. Thus, extensions to the BSM model have been developed focusing on relaxing these assumptions. This paper uses mixed normal heteroskedasticity models which allow for time varying volatility and can generate skewness and excess kurtosis in the distribution. Using this model, we find substantial improvements compared to a benchmark model in terms of dollar losses and the ability to explain the smirk in implied volatilities.

Several studies have examined models which allow for more flexible specifications of the volatility process compared to the BSM model. In particular, the stochastic volatility (SV) models have successfully been applied, see Hull and White (1987), Johnson and Shanno (1987), Scott (1987), Stein and Stein (1991), Wiggins (1987), Amin and Ng (1993), and Heston (1993). When comparing these models to the BSM model, empirically support is found for the stochastic volatility specification. This is documented in Bakshi, Cao, and Chen (1997), Bates (2000), and Nandi (1996) when considering options on the S&amp;P 500 index or the index futures. In addition to the SV models, the generalized autoregressive conditional heteroskedasticity (GARCH) framework has been used for option pricing using the model of Duan (1995). This model has also been used with success for empirical option pricing by, among others, Christoffersen and Jacobs (2004), Heston and Nandi (2000), and Hsieh and Ritchken (2005). A recent contribution is Christoffersen, Jacobs, Ornthanalai, and Wang (2008) where the volatility is allowed to have both short and long run components. These studies have all analyzed options on the S&amp;P 500 index and found that the GARCH models diminish the mispricings found when using the constant volatility BSM model. Stentoft (2005) documents the same using a sample individual stock options and options on the S&amp;P


<!-- p:4 -->


100 index.

However, while the improvements in option pricing performance of SV and GARCH models are important, mispricings still exist when comparing these models to actual option data as documented by Nandi (1996). This has led to the development of option pricing models which rely on alternative conditional distributions in addition to having non constant volatility. In the SV literature, jumps have been introduced in the return and volatility processes. Classical references are, among others, Bakshi, Cao, and Chen (1997), Bakshi, Cao, and Chen (2000), Bates (1991), Bates (2000), Pan (2002), and Eraker (2004). When examining the empirical performance of these models, most of the above papers find support for the existence of jumps again when looking at S&amp;P 500 index options. One exception is Bakshi, Cao, and Chen (2000) which, however, analyzes long term options and finds only small gains of allowing for jumps. In addition to the jump-diffusion processes, models based on infinite activity L ́ evy processes have been proposed in Barndorff-Nielsen and Shephard (2001) and Carr, Geman, Madan, and Yor (2003), and on time changed L ́ evy processes in Carr and Wu (2004) with applications to currency options in Carr and Wu (2007) and Bakshi, Carr, and Wu (2008).

Within the GARCH literature extensions include the use of distributions which are either skewed or leptokurtic, or both, as is done in Duan (1999) and Christoffersen, Elkamhi, Feunou, and Jacobs (2008). For empirical applications of this framework, see Christoffersen, Heston, and Jacobs (2006), Christoffersen, Jacobs, Dorion, and Wang (2008) and Stentoft (2008). Although Christoffersen, Jacobs, Dorion, and Wang (2008) find little improvement for the non-normal models Christoffersen, Heston, and Jacobs (2006) observe that allowing for non-normal innovations is important when pricing out of the money put options on the S&amp;P 500 index. Moreover, Stentoft (2008) documents improvements for both call and put options in terms of fitting the smile across moneyness for a sample of individual stock options as well as for options on the S&amp;P 100 index. In addition to models with non Gaussian innovations, GARCH models with jumps have been developed by Duan, Ritchken, and Sun (2006) and Christoffersen, Jacobs, and Ornthanalai (2008). The latter of these papers also examines the empirical performance and shows that jumps are important empirically when pricing S&amp;P 500 index options.


<!-- p:5 -->


The discussion above documents that important advances have been made in the empirical option pricing literature when it comes to extending the BSM model. However, it is also clear that there is still much room for improvements as discussed in the reviews by Bates (2003) and Garcia, Gysels, and Renault (2009). In particular, the existing research has shown that there are large differences between the conditional distribution of the underlying asset and the distribution implied from option pricing. One difference is that the volatility implied by at the money options is significantly different from that observed over the life of the option. However, much more importantly is the finding that the implied volatility curve, that is the implied volatility plotted against moneyness, is not only asymmetric but also changes through time. The first of these findings requires substantial negative skewness, more than is often found in the underlying process, whereas the latter indicates that moments of higher order are time varying.

In the present paper, we price options using mixed normal heteroskedasticity models, and we show that our proposed model can address the above points. In particular, the type of finite mixture model we use is flexible enough to approximate arbitrarily well any kind of conditional distribution, for example highly skewed and leptokurtic, and to allow for stochastic volatility of the returns on the underlying asset of the option contract. We suggest a feasible way for option pricing within this general framework and we derive the appropriate risk neutral dynamics. In our application, we find pronounced differences between the risk neutral distribution and the conditional distribution of the underlying asset given the significant risk premium. We show that our model allows for significant negative skewness and time varying higher order moments.

Finite mixture models, which are convex combinations of densities, are becoming a standard tool in financial econometrics. They are attractive because of the parsimonious flexibility they provide in the specification of the distribution of the underlying random variable, which gives them a semiparametric flavor. In this framework, each distribution in the mixture can have its own mean and conditional variance process. Moreover, if required by the data, some conditional variance processes may even be weakly nonstationary, for example to capture turbulent periods, while the overall conditional variance remains weakly stationary. Finite mixture textbooks are for example McLachlan and Peel (2000) and Fr ̈ uhwirth-Schnatter


<!-- p:6 -->


(2006). Early applications are Kon (1982) and Kim and Kon (1994) who investigate the statistical properties of stock returns using mixture models. Boothe and Glassman (1987), Tucker and Pond (1988), and Pan, Chan, and Fok (1995) use mixtures of normals to model exchange rates. Recent examples are Wong and Li (2000) and Wong and Li (2001) who model the conditional return distribution, extended by Haas, Mittnik, and Paolella (2004) with an application of value at risk prediction, and Bauwens and Rombouts (2007a) for the clustering of financial time series. Durham (2007) investigates the power of finite mixtures of normal densities with stochastic volatility to model the return of the S&amp;P 500 index. Using statistical criteria such as QQ-plots, goodness-of-fit tests and information criteria he finds that the finite mixture does a good job of capturing the salient features of the data. We extend his work by analyzing the performance of finite mixtures in out-of-sample option pricing. Hence, we focus mostly on the financial properties of the finite mixture instead of its statistical properties. In doing so, we examine both the physical and risk neutral measures, which are shown to be very different.

The main advantages of the Bayesian approach are twofold. Firstly, we avoid the maximization of the involved likelihood function of the mixture model. Instead, we compute posterior moments of the model parameters by sampling from the posterior density. This is possible thanks to data augmentation, a technique that includes latent variables in the parameter space, so that they also can be drawn using the Bayesian sampler. Secondly, the predictive price densities, we compute for evaluating the option prices, are easily obtained as a by-product of the Bayesian sampler and take into account parameter uncertainty, because we integrate over the entire parameter space. This is unlike classical inference that almost always conditions on maximum likelihood estimates. Another interesting advantage of the Bayesian approach is that our procedure can be applied directly to the raw returns instead of percentage returns without running into problems of numerically stability. This is particularly convenient when pricing options since the riskneutralization procedure involves nonlinear transformations of the model parameters and the data. We note that Bayesian inference combines data information and prior information. However, the priors we use in this paper are diffusive, so that we give most of the weight to the data to learn about the model parameters.


<!-- p:7 -->


Our results show that the added flexibility of the finite mixture model in terms of both skewness and excess kurtosis provides important improvements in terms of predicted option prices. We use our model to forecast out-of-sample prices of 8,637 call and put options on the S&amp;P 500 index in 2006 and compute dollar losses and implied standard deviation losses. Using dollar losses the results are quite similar for call options, but for put options the losses are approximately 16% or $0.34 smaller. Moreover, improvements are found for most categories of moneyness and maturity. The largest improvement in dollar terms is $1.92 for the deep out of the money call options with very long maturity, and $1.71 for the deep in the money put options also with very long maturity. In percentage of the mean option prices, the improvement is largest for the shorter term options which are out of the money. For the call options it is as high as 37% for options which are deep out of the money with short maturity. Finally, using implied volatility losses, we also show that the mixed normal heteroskedasticity model performs significantly better for options far away from being at the money. Moreover, when the losses are considered across moneyness for various maturity categories, it is observed that our model does a much better job than the GARCH model in explaining the smirk found in our sample of options. The improvements are particularly pronounced for the short term options.

It should be noted that we use only historical data on the underlying asset to obtain the parameters to be used for option valuation. However, it is very likely that historical option prices themselves contain important information on the model parameters. Therefore, an alternative approach is to infer these parameters either from historical option data alone or by using both returns and options data, by calibrating the option pricing model to existing option data, as detailed in Chernov and Ghysels (2000). This is for example the procedure used in Jacquier and Jarrow (2000), who incorporates parameter uncertainty and model error in the BSM model, and in Eraker (2004), who develops an option pricing model allowing for stochastic volatility with jumps in both the return and the volatility processes. In both of these papers, option pricing models within the affine class are considered, a choice which is motivated by the existence of closed or semiclosed form pricing formulas. However, this class of models could be considered as restrictive since many of the well known specifications within for example the GARCH framework are non-affine. An important exception is Heston and Nandi (2000). Moreover, research has shown that in terms of option pricing, non-affine models often perform better than affine models, see for example Hsieh and Ritchken (2005) and Christoffersen, Jacobs, Dorion, and Wang (2008). In the framework of the mixed normal heteroskedasticity model considered here, closed or semiclosed form solutions for option prices do not exist. Thus, using option data for estimation purposes along the lines above becomes extremely cumbersome if at all possible.


<!-- p:8 -->


The rest of the paper is organized as follows: Section 1 presents the mixed normal heteroskedasticity model. In Section 2 we discuss the risk neutral dynamics, and in Section 3 we explain how options can be priced using the mixed normal heteroskedasticity model. Section 4, explains how to conduct Bayesian inference and compute predictive price densities taking into account parameter uncertainty. Section 5, reports the results on the empirical application to options on the S&amp;P 500 index. Finally, Section 6 contains the conclusion.

## 1 Mixed normal heteroskedasticity

Building on the finite mixtures with autoregressive means and variances of Wong and Li (2000) and Wong and Li (2001), Haas, Mittnik, and Paolella (2004) develop a mixture of normals coupled with the GARCH specification to capture, for example, conditional kurtosis and skewness. They define a mixture model on a demeaned series ε t = y t - E ( y t |F t - 1 ) where F t - 1 is the information set up to time t and the conditional mean does not depend on the mixture. The conditional distribution of ε t is a combination of K densities

$$F ( \varepsilon _ { t } | \mathcal { F } _ { t - 1 } ) \ = \ \sum _ { k = 1 } ^ { K } \pi _ { k } \Phi \left ( \frac { \varepsilon _ { t } - \mu _ { k } } { \sigma _ { k , t } } \right ) ,$$

$$\sigma _ { k , t } ^ { 2 } \ = \ \omega _ { k } + \alpha _ { k } \varepsilon _ { t - 1 } ^ { 2 } + \beta _ { k } \sigma _ { k , t - 1 } ^ { 2 } ,$$

and Φ( · ) is the standard Gaussian distribution. We denote this the mixed normal heteroskedasticity (MNGARCH) model. For each t in this finite mixture framework, ε t is drawn from one of the K conditional distributions with probabilities π 1 , . . . , π K . Consequently, the parameter π k is restricted to be positive for all k and ∑ K k =1 π k = 1, which is imposed by

where setting π K = 1 - ∑ K - 1 k =1 π k . The zero mean assumption on ε t is ensured by the restriction


<!-- p:9 -->


$$\mu _ { K } \ = \ - \sum _ { k = 1 } ^ { K - 1 } \frac { \pi _ { k } \mu _ { k } } { \pi _ { K } } . \\ \\ n \ r o t r i o n \ d o s \ n o t \ i n v { p } _ { \ } s y m m o t r i o \ d i t r i o n \ T h o l t o r$$

Note that this zero mean restriction does not imply a symmetric distribution. The latter would only happen if all μ K 's are zero, something that can be tested. Indeed, the fact that our model is able to generate substantial skewness is an important advantage as documented also in Durham (2007).

Conditional moments of ε t for the MNGARCH model are combinations of the K distribution moments in (1). The conditional variance of ε t is given by

$$\sigma _ { t } ^ { 2 } \, = \, \sum _ { k = 1 } ^ { K } \left ( \pi _ { k } \mu _ { k } ^ { 2 } + \pi _ { k } \sigma _ { k , t } ^ { 2 } \right ) . \\ \intertext { d m o m e n t is g i v e n b y }$$

The conditional third moment is given by

$$E _ { t - 1 } ( \varepsilon _ { t } ^ { 3 } ) = \sum _ { k = 1 } ^ { K } \left ( \pi _ { k } \mu _ { k } ^ { 3 } + 3 \pi _ { k } \sigma _ { k , t } ^ { 2 } \mu _ { k } \right ) , \\ \\ \text {al} \text { fourth moment is given by}$$

and the conditional fourth moment is given by

$$E _ { t - 1 } ( \varepsilon _ { t } ^ { 4 } ) \, = \, \sum _ { k = 1 } ^ { K } \left ( \pi _ { k } \mu _ { k } ^ { 4 } + 6 \pi _ { k } \mu _ { k } ^ { 2 } \sigma _ { k , t } ^ { 2 } + 3 \pi _ { k } \sigma _ { k , t } ^ { 4 } \right ) , \\ \\ ( \cdot ) \, \text {means the expectation conditional on } \mathcal { F } _ { t } \, \text { .} \, \text { These formulas illustrate that}$$

where E t - 1 ( · ) means the expectation conditional on F t - 1 . These formulas illustrate that we can have flexible dynamics compared to the classical GARCH model which arises when K = 1. For example, the skewness of the conditional distribution of returns would be forced to zero in the latter case.

The MNGARCH model defined here is substantially different from the component volatility models introduced by Ding and Granger (1996) and Engle and Lee (1999). The component volatility model incorporates in a convenient way long range dependence in volatility. Each component allows the variance innovations to decay at a different rate, however there is only one conditional variance process. It can easily be shown that the component volatility model is a GARCH model with more lags in the squared innovations and the conditional variances than the conventional GARCH(1,1) model. For example, in Engle and Lee (1999), one component captures the long run movements in volatility while a second component accounts for the short run volatility movements. Skewness in the conditional return distribution is only possible when the innovation distribution is skewed. However, it is possible to have skewness in the unconditional return distribution if there is a time varying conditional mean in the model, see He, Silvennoinen, and Terasvirta (2008) for more details.


<!-- p:10 -->


What makes the mixture model attractive from an econometric point of view is the common innovation term ε t that feeds in the K conditional variance equations. Therefore, evaluation of the likelihood function is possible since there is no path dependence problem as would be the case in a Markov switching GARCH model. Note that to have an overall variance process that is weakly stationary, only one of the conditional variance processes is required to be weakly stationary. The other K - 1 conditional variance processes are allowed to be explosive ( α k + β k &gt; 1) as long as their combined probability is not too high. More formally, the weak stationarity condition for the model is

$$\left [ \sum _ { k = 1 } ^ { K } \frac { \pi _ { k } } { ( 1 - \beta _ { k } ) } \left ( 1 - \alpha _ { k } - \beta _ { k } \right ) \right ] \prod _ { k = 1 } ^ { K } ( 1 - \beta _ { k } ) \ > \ 0 .$$

More details on the unconditional moments of the mixed normal heteroskedasticity model can be found in Haas, Mittnik, and Paolella (2004).

The parameters of the mixture model are not identified as such because of the label switching problem which leaves the model likelihood unchanged when we change the order of the distributions in the finite mixture. This is not a problem if the objects of interest are label invariant, an example would be the predictive density of future returns. However, if we want to give a financial interpretation of the parameters, like in this paper, we add an identification restriction like π 1 ≥ π 2 ≥ . . . &gt; π K . Other restrictions, for example on the mean of the distributions, are possible as explained in Hamilton, Zha, and Waggoner (2007).

Finally, we note that the mixture model can incorporate extreme events by having a distribution with very low probability and with a large mean and a small constant variance for example. Moreover, the model can be made even more general by considering other conditional variance models than the GARCH model of Bollerslev (1986) used here. Examples include, but are not restricted to, the NGARCH model of Engle and Ng (1993), the GJR-GARCH model of Glosten, Jagannathan, and Runkle (1993), or the EGARCH model of Nelson (1991) all of which allow for asymmetries in the volatility process. Furthermore, other distributions than the normal can be considered in the finite mixture like the exponential power distribution proposed by Bouaddi and Rombouts (2009).


<!-- p:11 -->


### 1.1 Asset return dynamics with mixed normal heteroskedasticity

In this paper, we use the dynamics above as the driving innovation for asset returns. To be specific, we assume that the underlying return process R t ≡ ln ( S t /S t - 1 ) can be characterized by

$$R _ { t } \ = \ \mu _ { t } - \Psi _ { t } \left ( - 1 \right ) + \varepsilon _ { t } ,$$

where S t is the index level on day t and where ε t follows (1). In (8), the term Ψ t ( · ) denotes the conditional cumulant generating function which corresponds to the logarithm of the conditional moment generating function. The conditional moment generating function (also called the conditional Laplace transform) of ε t in (1) is given by

$$E _ { t - 1 } \exp ( - u \varepsilon _ { t } ) \ = \ \sum _ { k = 1 } ^ { K } \pi _ { i } \exp \left ( - u \mu _ { k } + \frac { u ^ { 2 } \sigma _ { k , t } ^ { 2 } } { 2 } \right ) .$$

In fact, this is just a convex combination of Gaussian moment generating functions and thus very easy to calculate. For option pricing purposes, the logarithm of this function will be used extensively, and the fact that it may easily be calculated is therefore convenient.

Using (9), the conditional cumulant generating function evaluated at u = - 1 is now simply given by

$$\ln \left ( E _ { t - 1 } \left [ \exp \left ( \varepsilon _ { t } \right ) \right ] \right ) \ = \ \Psi _ { t } \left ( - 1 \right ) .$$

Substituting this into (8), we see that

$$E _ { t - 1 } \left [ S _ { t } / S _ { t - 1 } \right ] & \ = \ E _ { t - 1 } \left [ \exp \left ( \mu _ { t } - \Psi _ { t } \left ( - 1 \right ) + \varepsilon _ { t } \right ) \right ] \\ & = \ \exp \left ( \mu _ { t } \right ) .$$

It makes indeed sense to define the return process as above since with this particular specification, since μ t can be interpreted as the expected gross rate of return.


<!-- p:12 -->


## 2 Risk neutral dynamics

Once the conditional distribution of R t is specified, the proposed system can be taken to the data. However, when the ultimate goal is that of option pricing some further work is needed. In particular, for option pricing to proceed an equivalent martingale measure (EMM) is needed. While technically complicated, intuitively what we are looking for is a 'transformation' to the distribution of ε t . This transformation, however, has to be special in the sense that the two measures, the original and the transformed one, have the same null sets, i.e. they are equivalent. Furthermore, under the transformed measure, the expected gross rate of returns should equal the risk free rate, i.e. discounted returns are martingales. The new conditional distribution is distinguished from the original density F by adding a superscript Q . We will refer to this as either the distribution under Q , the distribution under the risk neutral measure, or simply as the risk neutral distribution.

In this paper, we follow the approach of Christoffersen, Elkamhi, Feunou, and Jacobs (2008) which involves the specification of a candidate EMM through a specification of a Radon-Nikodym derivative. A similar method, which would provide an equal set of conditions, specifies a candidate stochastic discount factor directly as is done in Gourieroux and Monfort (2007). For a discussion of the relationship between the two probability measures F and Q and the corresponding stochastic discount factor see Bertholon, Monfort, and Pegoraro (2008). Note that an alternative method is to work within a general equilibrium setup as is done in Duan (1999). While this method also yields the dynamics to be used for option pricing, the specification is generally less explicit and an actual application of the method computationally complex (see e.g. Stentoft (2008)). Thus, this approach appears to be more restrictive.

Once a candidate EMM is obtained, European options may be priced as the expected value, under the EMM, of future cash flows discounted using the risk free interest rate. For example, the price of a European call option at time T with maturity T ∗ and strike price K can be computed as

$$\text {an be computed as} \\ C _ { T } ( S , T ^ { * } , K ) \ = \ e ^ { - r ( T ^ { * } - T ) } \int _ { 0 } ^ { \infty } \max ( S _ { T ^ { * } } - K , 0 ) f ^ { Q } ( S _ { T ^ { * } } ) d S _ { T ^ { * } } \\ \intertext { w h o r } \ \text {bzero} \ f ^ { Q } ( S _ { - } ) \text { is the density of the undorling aspect of a) orientation under the} \text {ho} .$$

where f Q ( S T ∗ ) is the density of the underlying asset price at expiration under the EMM, i.e.


<!-- p:13 -->


the risk neutral density.

### 2.1 Specification of a candidate EMM

We specify a candidate EMM from the following Radon-Nikodym derivative

$$\text {candidate EMM from the following Radon-Nikodym derivative} \\ \frac { d Q } { d F } \Big | \mathcal { F } _ { t } \ = \ \exp \left ( - \sum _ { i = 1 } ^ { t } \left ( \nu _ { i } \varepsilon _ { i } + \Psi _ { i } ( \nu _ { i } ) \right ) \right ) , \\ \intertext { s i t h e t d i o n a l c u m u l a n t g e r a n t i g n o u f i n c t i o n s e f i d e a b o v e . I t i s i m m e d i }$$

where Ψ t ( u ) is the conditional cumulant generating function specified above. It is immediately observed that by using a Radon-Nikodym of this type we are guaranteed that the two measures are equivalent as they have the same null sets. To ensure that discounted asset prices are martingales under the risk neutral measure it can be shown that the sequence ν t has to satisfy the following equation

$$0 \ = \ \Psi _ { t } \left ( \nu _ { t } - 1 \right ) - \Psi _ { t } \left ( \nu _ { t } \right ) - \Psi _ { t } \left ( - 1 \right ) + \mu _ { t } - r _ { t } .$$

Moreover, we have that under the risk neutral measure the conditional cumulant generating function of ε t is given by

$$\Psi _ { t } ^ { Q } \left ( u \right ) \ = \ \Psi _ { t } \left ( \nu _ { t } + u \right ) - \Psi _ { t } \left ( \nu _ { t } \right ) .$$

Using the Inversion Theorem (see for example Billingsley (1995, Theorem 26.2) or Davidson (1997, Theorem 11.12)) this can be used to obtain (15) the distribution under Q .

The two above equations completely characterize the risk neutral process and hence this is, in fact, all that is needed for option pricing purposes. In particular, equation (15) characterizes the risk neutral distribution in terms of the sequence ν and equation (14) provides the link between this sequence and the properties under the original measure F . In order to apply the method for pricing, however, all that is left is to derive these dynamics explicitly. To do this, we simply use (14) and (15) in the mean equation in (8). Doing so, we obtain the following specification of the risk neutral dynamics

$$R _ { t } ^ { Q } \ = \ r _ { t } - \Psi _ { t } ^ { Q } \left ( - 1 \right ) + \varepsilon _ { t } ^ { Q } ,$$

where the superscript Q indicates that the variables are considered under the risk neutral distribution. Using this specification, we can calculate the gross rate of return on assets under Q as


<!-- p:14 -->


$$E _ { t - 1 } ^ { Q } \left [ S _ { t } / S _ { t - 1 } \right ] & \ = \ E _ { t - 1 } ^ { Q } \left [ \exp \left ( r _ { t } - \Psi _ { t } ^ { Q } \left ( - 1 \right ) + \varepsilon _ { t } \right ) \right ] \\ & = \ \exp \left ( r _ { t } \right ) .$$

Thus, it equals the risk free interest rate as required.

As it was noted in Christoffersen, Elkamhi, Feunou, and Jacobs (2008), the above method is only one of several ways to derive the risk neutral dynamics to be used for option pricing. In fact, in the present setting markets are incomplete and hence in general no unique EMM exists as is the case in for example the constant volatility BSM model. However, in this setup the obtained option prices are in fact unique conditional on the choice of Radon-Nikodym derivative.

### 2.2 A strategy for riskneutralization

Based on the above, the strategy to follow for option pricing is clear and consists of the following three steps:

- First, a sequence ν t which satisfy (14) has to be specified. If possible, this can be done directly by inverting the conditional cumulant generating function. Below, we propose an alternative and somewhat indirect way of specifying this sequence which can be used in general.
- Secondly, given the sequence for ν t the conditional cumulant generating function for ε t under the risk neutral density can be obtained from (15). With this the distribution of ε t under the Q measure can be obtained.
- Finally, the return process under the risk neutral measure can be obtained from (16) and this then specifies the dynamics to be used for option pricing purposes. Note that if the conditional variance depends on the innovations, as it is the case in for example the GARCH specification, it is the innovations from this distribution which should be used.


<!-- p:15 -->


It is immediately seen, that the procedure we use riskneutralizes by changing the distribution of the innovations. This is in line with the procedure used in the BSM model and in most of the SV literature. It also corresponds to the method used in Duan (1999), although the obtained distribution is given somewhat implicitly in this framework as mentioned above. However, the method differs from the procedure used in Barone-Adesi, Engle, and Mancini (2008), where it is the actual parameters of the mean and variance process, that are changed under Q .

#### 2.2.1 The Gaussian special case

We now consider the Gaussian special case for illustrative purposes. In this case, the conditional cumulant generating function of ε t is given by

$$\Psi _ { t } \left ( u \right ) \ = \ \frac { 1 } { 2 } \sigma _ { t } ^ { 2 } u ^ { 2 } .$$

We now proceed with the three steps outlined above for risk neutralization:

- Substituting the conditional cumulant generating function into (14), we can rewrite the EMM restriction as

$$0 & \ = \ \frac { 1 } { 2 } \sigma _ { t } ^ { 2 } ( \nu _ { t } - 1 ) ^ { 2 } - \frac { 1 } { 2 } \sigma _ { t } ^ { 2 } \left ( \nu _ { t } \right ) ^ { 2 } - \frac { 1 } { 2 } \sigma _ { t } ^ { 2 } \left ( - 1 \right ) ^ { 2 } + \mu _ { t } - r _ { t } \\ & = \ - \sigma _ { t } ^ { 2 } \nu _ { t } + \mu _ { t } - r _ { t } .$$

Thus, in this case, there is an exact and analytically tractable mapping between μ t and the required ν t . In particular, for any choice of μ t , the corresponding ν t process is given by

$$\nu _ { t } \ = \ \frac { \mu _ { t } - r _ { t } } { \sigma _ { t } ^ { 2 } } .$$

- Substituting (20) into (15) and using the specification of the cumulant generating function, we obtain

$$\Psi _ { t } ^ { Q } \left ( u \right ) & = \frac { 1 } { 2 } \sigma _ { t } ^ { 2 } \left ( \frac { \mu _ { t } - r _ { t } } { \sigma _ { t } ^ { 2 } } + u \right ) ^ { 2 } - \frac { 1 } { 2 } \sigma _ { t } ^ { 2 } \left ( \frac { \mu _ { t } - r _ { t } } { \sigma _ { t } ^ { 2 } } \right ) ^ { 2 } \\ & = \left ( \mu _ { t } - r _ { t } \right ) u + \frac { 1 } { 2 } \sigma _ { t } ^ { 2 } u ^ { 2 } .$$


<!-- p:16 -->


This, however, is recognized as the cumulant generating function of a Gaussian variable with mean equal to - ( μ t - r t ) and variance equal to σ 2 t . Thus, it follows that ε t is distributed as N ( r t - μ t , σ 2 t ) under Q .

- The risk neutral dynamics may now be obtained as

$$R _ { t } ^ { Q } \ & = \ r _ { t } - \Psi _ { t } ^ { Q } \left ( - 1 \right ) + \varepsilon _ { t } ^ { Q } \\ & = \ \mu _ { t } - \frac { 1 } { 2 } \sigma _ { t } ^ { 2 } + \varepsilon _ { t } ^ { Q } .$$

To be even more specific, we take as an example the particular choice of mean specification used in Duan (1995) where μ t = r t + λσ t . Substituting this into (22), the risk neutral dynamics are obtained as

$$R _ { t } ^ { Q } \ = \ r _ { t } + \lambda \sigma _ { t } - \frac { 1 } { 2 } \sigma _ { t } ^ { 2 } + \varepsilon _ { t } ^ { Q } .$$

Moreover, assume that the conditional variance is of the GARCH type given by

$$\sigma _ { t } ^ { 2 } \ = \ \omega + \alpha \varepsilon _ { t - 1 } ^ { 2 } + \beta \sigma _ { t - 1 } ^ { 2 } .$$

Then, under the risk neutral dynamics the conditional variance is given by

$$\sigma _ { t } ^ { 2 } \ = \ \omega + \alpha ( \varepsilon _ { t - 1 } ^ { Q } ) ^ { 2 } + \beta \sigma _ { t - 1 } ^ { 2 } .$$

## 3 Option pricing under general assumptions

In the previous section, we outlined a strategy for riskneutralization and we provided an example on how this can be implemented in the Gaussian special case. In this section, we show how this can be done under more general assumptions and we interpret the effect of riskneutralization on the model parameters. We first provide a general method for obtaining a solution to the restriction in equation (14) used in the first step. We then derive the risk neutral distribution in the mixed normal heteroskedasticity model from the conditional cumulant generating function obtained in the second step from (15).


<!-- p:17 -->


### 3.1 Feasible option pricing

As mentioned above, we effectively choose the appropriate EMM by solving (14) for ν t given μ t and the assumed distribution of ε t . However, this is potentially complicated due to the nonlinearity of this relationship and an analytical expression for ν t may therefore not be available in general. In particular, this is the case with the mixed normal heteroskedasticity model used here, and it may thus seem to be impossible to derive the EMM given μ t for this model.

However, (14) may equally well be solved for μ t given ν t and the assumed distribution of ε t as

$$\mu _ { t } \ = \ r _ { t } - \Psi _ { t } \left ( \nu _ { t } - 1 \right ) + \Psi _ { t } \left ( \nu _ { t } \right ) + \Psi _ { t } \left ( - 1 \right ) .$$

From this, we note that for any choice of ν t a closed form expression exist for μ t given that the cumulant generating function exists. Substituting this into the return equation in (8) we obtain

$$R _ { t } \ = \ r _ { t } - \Psi _ { t } \left ( \nu _ { t } - 1 \right ) + \Psi _ { t } \left ( \nu _ { t } \right ) + \varepsilon _ { t } ,$$

which can be used for estimation directly. This way of implying μ t , given a particular specification of ν t , is used in Stentoft (2008) in the Normal Inverse Gaussian framework using the option pricing model of Duan (1999). However, it is equally applicable here.

It should be noted that, depending on the specification of ν t and the assumed distribution of ε t , we may interpret the specification in (27) differently. We next illustrate this for the Gaussian case and then for the general case.

#### 3.1.1 Interpreting ν t in the Gaussian special case

With the Gaussian distribution, we obtain the following in (27) above

$$R _ { t } & \ = \ r _ { t } - \Psi _ { t } \left ( \nu _ { t } - 1 \right ) + \Psi _ { t } \left ( \nu _ { t } \right ) + \varepsilon _ { t } \\ & = \ r _ { t } - \frac { 1 } { 2 } \sigma _ { t } ^ { 2 } \left ( v _ { t } - 1 \right ) ^ { 2 } + \frac { 1 } { 2 } \sigma _ { t } ^ { 2 } \left ( v _ { t } \right ) ^ { 2 } + \varepsilon _ { t } \\ & = \ r _ { t } - \frac { 1 } { 2 } \sigma _ { t } ^ { 2 } + \nu _ { t } \sigma _ { t } ^ { 2 } + \varepsilon _ { t } .$$


<!-- p:18 -->


Hence, we see that ν t is related to the assumption of the unit risk premium. In particular, if we were to specify ν t = ν , that is as a constant, the implied mean specification corresponds to assuming a unit risk premium proportional to the level of the variance. Alternatively, if ν t = ν/σ t , the unit risk premium becomes proportional to the level of the standard deviation, and finally with ν t = ν/σ 2 t a constant unit risk premium independent of the level of the variance is obtained. Thus, while it may appear that we, by implying the mean, are constraining the potential mean specification in an unreasonably way from an econometric point of view, this is in fact not the case.

#### 3.1.2 Interpreting ν t in the general case

In the Gaussian case, the sequence ν t was immediately interpreted as determining the unit risk premium. In the mixed normal heteroskedasticity model this is less obvious. However, we may analyze the effect of ν t using a Taylor series expansion in (27). To do this, we first note that the two terms involving the log moment generating functions may be approximated by

$$\Psi _ { t } ( \nu _ { t } - 1 ) \ & \approx \ \Psi _ { t } ( 0 ) + \Psi _ { t } ^ { \prime } ( 0 ) \left ( \nu _ { t } - 1 \right ) + \frac { 1 } { 2 } \Psi _ { t } ^ { \prime \prime } ( 0 ) \left ( \nu _ { t } - 1 \right ) ^ { 2 } \\ & + \frac { 1 } { 6 } \Psi _ { t } ^ { \prime \prime \prime } ( 0 ) \left ( \nu _ { t } - 1 \right ) ^ { 3 } + \frac { 1 } { 2 4 } \Psi _ { t } ^ { \prime \prime \prime \prime } ( 0 ) \left ( \nu _ { t } - 1 \right ) ^ { 4 }$$

and

$$\Psi _ { t } ( \nu _ { t } ) \ \approx \ \Psi _ { t } ( 0 ) + \Psi _ { t } ^ { \prime } ( 0 ) \nu _ { t } + \frac { 1 } { 2 } \Psi _ { t } ^ { \prime \prime } ( 0 ) \nu _ { t } ^ { 2 } + \frac { 1 } { 6 } \Psi _ { t } ^ { \prime \prime \prime } ( 0 ) \nu _ { t } ^ { 3 } + \frac { 1 } { 2 4 } \Psi _ { t } ^ { \prime \prime \prime \prime } ( 0 ) \nu _ { t } ^ { 4 } ,$$

respectively. Furthermore, by the definition of ε t as a zero mean random variable with conditional variance σ 2 t we have that Ψ ′ t (0) = 0 and Ψ ′′ t (0) = σ 2 t . Moreover, by the definition of Ψ t ( u ), we have that Ψ ′′′ t (0) = - skew t σ 3 t and Ψ ′′′′ t (0) = exkurt t σ 4 t , where skew t and exkurt t denotes the conditional skewness and excess kurtosis at time t respectively.

With the above expressions, (27) may be rewritten as

$$R _ { t } \approx r _ { t } - \Psi _ { t } ( - 1 ) + \nu _ { t } \sigma _ { t } ^ { 2 } + \frac { ( 3 \nu _ { t } ^ { 2 } - 3 \nu _ { t } ) } { 6 } ( - s k e w _ { t } ) \sigma _ { t } ^ { 3 } + \frac { ( 4 \nu _ { t } ^ { 3 } - 6 \nu _ { t } ^ { 2 } + 4 \nu _ { t } ) } { 2 4 } e x k u r t _ { t } \sigma _ { t } ^ { 4 } + \varepsilon _ { t } ,$$

where we have collected all the terms which do not involve ν t in Ψ t ( - 1). Equation (31) shows that even in the more general setting it makes sense to interpret ν t as the unit risk This figure plots the coefficients of the variance term, the skewness term, and the excess kurtosis term in (31) as a function of ν t in panels (a) through (c). Panel (d) plots the combined effect.


<!-- p:19 -->


Figure 1: Unit risk premium effects

premium. In particular, it may be observed that for reasonable values of ν t , say larger than 1, the coefficients above are all positive. In Figure 3.1.2, we plot in panels (a) through (c) the coefficients of the variance term, the skewness term, and the excess kurtosis term as a function of ν t . Thus, in a general setting, the premium is increasing in the variance, decreasing in the skewness, and increasing in the excess kurtosis.

In the case of our model for the S&amp;P 500 index, for which we obtain negative skewness and significantly excess kurtosis, equation (31) shows that the higher the value of ν t the larger the premium required by investors for holding this particular risky asset. Panel (d) of Figure 3.1.2 plots the combined effect of the three terms with a solid line. Note also, that if we were to neglect these higher order moment properties of the return process and assume them equal to zero, then to compensate for this a higher value of ν t would be required to generate the same overall level of compensation for risk. This is clear from the dotted line in Panel (d) of Figure 3.1.2 which shows the effect without the higher order terms.


<!-- p:20 -->


### 3.2 Risk neutral distribution in the mixed normal heteroskedasticity model

Once a sequence ν t has been obtained, in the second step in the riskneutralization strategy, the risk neutral distribution are obtained from (15). For this, we need the conditional cumulant generating function for the mixed normal heteroskedastic model which from equation (9), becomes

$$\Psi _ { t } ( u ) \ = \ \ln \left ( \sum _ { k = 1 } ^ { K } \pi _ { i } \exp \left ( - u \mu _ { k } + \frac { u ^ { 2 } \sigma _ { k , t } ^ { 2 } } { 2 } \right ) \right ) . \\ \intertext { t h e c t i o n a l c u m u l a n g r e p a t i o n f o r } \$$

Using this, the conditional cumulant generation function of ε t under the risk neutral measure Q is easily obtained as

$$\text {as} \, \text {only} \, \text { obtained as} \, \\ \Psi _ { t } ^ { Q } ( u ) \ = \ \Psi _ { t } ( \nu _ { t } + u ) - \Psi _ { t } ( \nu _ { t } ) \\ \equiv \ \ln \left ( \frac { \sum _ { k = 1 } ^ { K } \pi _ { i } \exp \left ( - ( \nu _ { t } + u ) \mu _ { k } + \frac { ( \nu _ { t } + u ) ^ { 2 } \sigma _ { k , t } ^ { 2 } } { 2 } \right ) } { \sum _ { k = 1 } ^ { K } \pi _ { i } \exp \left ( - \nu _ { t } \mu _ { k } + \frac { \nu _ { t } ^ { 2 } \sigma _ { k , t } ^ { 2 } } { 2 } \right ) } \right ) \\ \equiv \ \ln \left ( \sum _ { k = 1 } ^ { K } \pi _ { i } ^ { * } \exp \left ( - u \mu _ { k } ^ { * } + \frac { u ^ { 2 } \sigma _ { k , t } ^ { 2 } } { 2 } \right ) \right ) , \\$$

where

and

$$\mu _ { k , t } ^ { * } \ = \ \mu _ { k } - \nu _ { t } \sigma _ { k , t } ^ { 2 } ,$$

$$\pi _ { k , t } \ = \ \frac { \pi _ { k } \exp \left ( - \nu _ { t } \mu _ { k } + \frac { \nu _ { t } ^ { 2 } \sigma _ { k , t } ^ { 2 } } { 2 } \right ) } { \sum _ { k = 1 } ^ { K } \pi _ { k } \exp \left ( - \nu _ { t } \mu _ { k } + \frac { \nu _ { t } ^ { 2 } \sigma _ { k , t } ^ { 2 } } { 2 } \right ) } , \\ . \text { Thus, the risk neutral distribution of } \varepsilon _ { t } \text { remains within the family of normal}$$

for k = 1 , .., K . Thus, the risk neutral distribution of ε t remains within the family of normal mixtures. In fact, in the special case with no unit risk premium, the above equations show that the risk neutral distribution correspond to the original distribution. In general, however, under Q the distribution of ε t will have changed means and probabilities.


<!-- p:21 -->


We remark that for the risk neutral distribution, the weak stationarity condition in (7) is not appropriate anymore, since the finite mixture under Q has time varying distribution probabilities π ∗ t . Therefore, it can in principle occur, that the physical distribution is weakly stationary, but the risk neutral distribution is not.

#### 3.2.1 Interpreting the impact of riskneutralization

For simplicity, we now consider the special case where K = 2. With respect to the risk neutral means from (34), it is immediately seen that the correction is very similar to what is obtained with the Gaussian model, where the mean of ε t under Q is equal to r t - μ t = - ν t σ 2 t . The intuition behind this is the following: If volatility risk carries a positive premium, then in the risk neutral world the mean of the innovations is shifted downwards to compensate for this.

With respect to the risk neutralized probabilities, the relationship is somewhat less straightforward. However, when K = 2 (35) simplifies to

$$\text {traightforward.} \text { However, when } K = 2 \left ( 3 5 \right ) \text { simplifies to } \\ \pi \exp \left ( - \nu _ { t } \mu _ { 1 } + \frac { \nu _ { t } ^ { 2 } \sigma _ { 1 , t } ^ { 2 } } { 2 } \right ) \\ \pi _ { t } ^ { * } \ = \ \frac { \pi } { \pi \exp \left ( - \nu _ { t } \mu _ { 1 } + \frac { \nu _ { t } ^ { 2 } \sigma _ { 1 , t } ^ { 2 } } { 2 } \right ) + ( 1 - \pi ) \exp \left ( - \nu _ { t } \mu _ { 2 } + \frac { \nu _ { t } ^ { 2 } \sigma _ { 2 , t } ^ { 2 } } { 2 } \right ) } . \\ \text {Moreover, by dividing through with exp \left ( - \nu _ { t } \mu _ { 1 } + \frac { \nu _ { t } ^ { 2 } \sigma _ { 1 , t } ^ { 2 } } { 2 } \right ) , it is seen that }$$

$$\pi _ { t } ^ { * } \equiv \pi \text { if } \exp \left ( - \nu _ { t } \mu _ { 1 } + \frac { \nu _ { t } ^ { 2 } \sigma _ { 1 , t } ^ { 2 } } { 2 } \right ) \geqslant \exp \left ( - \nu _ { t } \mu _ { 2 } + \frac { \nu _ { t } ^ { 2 } \sigma _ { 2 , t } ^ { 2 } } { 2 } \right ) .$$

Moreover, by dividing through with exp ( - ν t μ 1 + ν 2 t σ 2 1 ,t 2 ) , it is seen that

Thus, if we further assume that the variance term ν 2 t σ 2 k,t 2 is negligible compared to the mean term - ν t μ k , for k = 1 , 2, this restriction simplifies to

$$\pi _ { t } ^ { * } \geqq \pi \text { if } \nu _ { t } \mu _ { 2 } \geqq \nu _ { t } \mu _ { 1 } .$$

However, by construction μ 2 &lt; μ 1 and hence the effect on the probabilities depends entirely on the sign of the unit risk premium. Since we expect this premium to be positive, it follows that we will in general have that π ∗ t &lt; π . The intuition behind this result is the following: If volatility risk carries a positive premium then the probability attributed to the explosive part, that is 1 - π ∗ t , is increased in the risk neutral world to compensate appropriately for this.


<!-- p:22 -->


## 4 Bayesian Inference

Bayesian inference is an approach to statistics that describes the model parameters as well as the data by probability distributions. It has become of widespread use in economics since Zellner (1971), van Dijk and Kloek (1978) and Geweke (1989a). Recent introductions to Bayesian inference are Koop (2003) and Geweke (2005), whereas the last chapter of Tsay (2005) treats inference for some particular models often used in financial econometrics. Polson and Johannes (2009) explain how to estimate equity price models, driven for example by stochastic volatility and jumps, using Markov Chain Monte Carlo (MCMC) methods.

In order to learn about the model parameters of the mixed normal heteroskedasticity model and to forecast out-of-sample option prices, we need to draw from the posterior density. Unfortunately, the posterior density is too involved to sample from directly because it is nonstandard. We implement a MCMC procedure known as Gibbs sampling which is an iterative procedure to sample sequentially from the posterior distribution, see Gelfand and Smith (1990). Each iteration in the Gibbs sampler produces a draw from a Markov chain. Under regularity conditions, see for example Robert and Casella (2004), the simulated distribution converges to the posterior distribution. The Markov chain is generated by drawing iteratively from lower dimensional distributions, called blocks or complete conditional distributions, of this joint target distribution. These complete conditional distributions are easier to sample from because either they are known in closed form or approximated by a lower dimensional additional sampler.

In the next section, we explain the Gibbs sampler and its blocks to perform inference on the parameters of the mixed normal heteroskedasticity model. Then we explain how to compute predictive densities and to price options.

### 4.1 Gibbs sampling

The mixture model is defined in (1) for the innovations ε t only to leave the specification of the conditional mean for option pricing. As required by (27), the model for the returns is defined as


<!-- p:23 -->


$$R _ { t } & \ = \ r _ { t } - \Psi _ { t } \left ( \nu _ { t } - 1 \right ) + \Psi _ { t } \left ( \nu _ { t } \right ) + \varepsilon _ { t } \\ & = \ \rho _ { t } ( \nu ) + \varepsilon _ { t } .$$

That is, we consider ν t as constant although this can be specified otherwise if desired by the econometrician. Note that a constant ν does not imply a constant risk premia as (31) shows. The likelihood of the model for T observations is given by

$$\mathcal { L } ( \xi \, | \, R ) \ = \ \prod _ { t = 1 } ^ { T } \sum _ { k = 1 } ^ { K } \pi _ { k } \phi ( R _ { t } | \mu _ { k } + \rho _ { t } ( \nu ) , \theta _ { k } ) , \\ \intertext { h e v e r g r o u p i n g t h e r $ t $ a n d $ \mu _ { k } $ a n d $ \theta _ { k } $ a n d $ \theta _ { k } $ f o r $ k = 1 }$$

where ξ is the vector regrouping the parameters ν and π k , μ k , and θ k for k = 1 , . . . , K , R denotes the vector of returns i.e. R = ( R 1 , R 2 , . . . , R T ) ′ , and φ ( ·| μ k + ρ t ( ν ) , θ k ) denotes a normal density with mean μ k + ρ t ( ν ) and variance σ 2 k,t that depends on θ k = ( ω k , α k , β k ).

A direct evaluation of the likelihood function is difficult because it consists of a product of sums. It is this function that is maximized in the classical inference framework. To alleviate this evaluation, in the Bayesian framework, we introduce for each observation a state variable G t ∈ { 1 , 2 , . . . , K } that takes the value k if the observation R t belongs to distribution k . The vector G T contains the state variables for the T observations. We assume that the state variables are independent given the distribution probabilities. Then, the probability that G t is equal to k is equal to π k which can be written as

$$\varphi ( G ^ { T } | \pi ) = \prod _ { t = 1 } ^ { T } \varphi ( G _ { t } | \pi ) \, = \, \prod _ { t = 1 } ^ { T } \pi _ { G _ { t } } , \\ \pi _ { t } \, \Omega _ { t } = \pi _ { t } \Omega \, \text { given } G ^ { T } \text { and } B \text { the likelihood function is}$$

where π = ( π 1 , π 2 , . . . , π K ). Given G T and R , the likelihood function is

$$\mathcal { L } ( \xi \, | \, G ^ { T } , R ) \ = \ \prod _ { t = 1 } ^ { T } \pi _ { G _ { t } } \phi ( R _ { t } | \mu _ { G _ { t } } + \rho _ { t } ( \nu ) , \theta _ { G _ { t } } ) , \\ \text {asier to evaluate than } ( 4 0 ) \text { since the sum has disconnected $Since G^{T}$ is not observed}$$

which is easier to evaluate than (40) since the sum has disappeared. Since G T is not observed, we treat it as an extra parameter of the model. This technique is called data augmentation, see Tanner and Wong (1987) and Albert and Chib (1993) for more details, and Jacquier, Polson, and Rossi (1994) for a well known application in stochastic volatility modeling. Although the augmented model contains more parameters, the initial parameters plus the states, inference becomes easier by making use of MCMC methods as we will see next.


<!-- p:24 -->


Since the posterior density of the mixed normal heteroskedasticity model is too involved to sample from directly, we implement a hybrid Gibbs sampling algorithm that allows to sample from the posterior distribution by sampling from its conditional posterior densities, see also Bauwens and Rombouts (2007b) for more details. The blocks of the Gibbs sampler, and the prior densities are explained next using the parameter vectors G T = ( G 1 , . . . , G T ) ′ , π = ( π 1 , π 2 , . . . , π K ), μ = ( μ 1 , μ 2 , . . . , μ K ), θ = ( θ 1 , θ 2 , . . . , θ K ) and the parameter ν . The joint posterior distribution is given by

$$\varphi ( G ^ { T } , \nu , \mu , \theta , \pi | R ) \ \underset { t = 1 } { \ \ \ \ } \alpha \ \varphi ( \nu ) \, \varphi ( \mu ) \, \varphi ( \theta ) \, \varphi ( \pi ) \prod _ { t = 1 } ^ { T } \pi _ { G _ { t } } \phi ( R _ { t } | \mu _ { G _ { t } } + \rho _ { t } ( \nu ) , \theta _ { G _ { t } } ) , \\ \\ \intertext { w h e r } \ m a t h s c r { G } ^ { T } , \nu , \mu , \theta , \pi | R ) \ \underset { t = 1 } { \ \ \ } \alpha \ \varphi ( \nu ) \, \varphi ( \mu ) \, \varphi ( \theta ) \, \varphi ( \pi ) \prod _ { t = 1 } ^ { T } \pi _ { G _ { t } } \phi ( R _ { t } | \mu _ { G _ { t } } + \rho _ { t } ( \nu ) , \theta _ { G _ { t } } ) , \\$$

where φ ( ν ), φ ( μ ), φ ( θ ), φ ( π ) are the corresponding prior densities. Thus, we assume prior independence between ν , π , μ , and θ . This makes the construction of the Gibbs sampler easier. It does, however, not imply posterior independence between the parameters.

· φ ( G T | ν, μ, θ, π, R )

Given ν, μ, θ, π and y , the posterior density of G T is proportional to L ( ξ | G T , R ). Since the G t 's are mutually independent, we can write the relevant conditional posterior density as

$$\varphi ( G ^ { T } | \nu , \mu , \theta , \pi , R ) \ = \ \prod _ { t = 1 } ^ { T } \varphi ( G _ { t } | \nu , \mu , \theta , \pi , R ) . \\ \\ ( G ) T \ \colon \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \qu$$

As the sequence { G t } T t =1 is equivalent to a multinomial process, we simply have to sample from a discrete distribution where the K probabilities are given by

$$P ( G _ { t } = k | \nu , \mu , \theta , \pi , R ) \ = \ \frac { \pi _ { k } \phi ( R _ { t } | \mu _ { k } + \rho _ { t } ( \nu ) , \theta _ { k } ) } { \sum _ { j = 1 } ^ { K } \pi _ { j } \phi ( R _ { t } | \mu _ { j } + \rho _ { t } ( \nu ) , \theta _ { j } ) } , \ ( k = 1 , \dots , K ) . \quad ( 4 5 ) \\ \intertext { T o s m a p l e G _ { t } , w e d r a w e o n s e r v a t i o n f r o m a u f i m o r d i b u t i o n on [ 0 , 1 ] a n d c i d e }$$

To sample G t , we draw one observation from a uniform distribution on [0 , 1] and decide which group k to take according to (45).

- φ ( π | G T , ν, μ, θ, R )

The full conditional posterior density of π depends only on G T and is given by

$$\varphi ( \pi | G ^ { T } ) = \alpha \ \varphi ( \pi ) \prod _ { k = 1 } ^ { K } \pi _ { k } ^ { x _ { k } } ,$$


<!-- p:25 -->


where x k is the number of times that G t = k . The prior φ ( π ) is chosen to be a Dirichlet distribution, Di ( a 10 , a 20 · · · a K 0 ) with parameter vector a 0 = ( a 10 , a 20 · · · a K 0 ) ′ . As a consequence, φ ( π | G T ) is also a Dirichlet distribution, Di ( a 1 , a 2 · · · a K ) with a k = a k 0 + x k , k = 1 , 2 , . . . , K .

- φ ( μ | G T , ν, π, θ, R )

The conditional distribution of  ̃ μ = ( μ 1 , μ 2 , . . . , μ K - 1 ) ′ is Gaussian with mean - A - 1 b and covariance matrix A - 1 where

and

$$\text {and covariance matrix } A ^ { - 1 } \text { where} \\ A \ = \ \text {diag} \left ( \sum _ { ( 1 ) } \frac { 1 } { \sigma _ { 1 , t } ^ { 2 } } , \dots , \sum _ { ( K - 1 ) } \frac { 1 } { \sigma _ { K - 1 , t } ^ { 2 } } \right ) + \frac { \tilde { \pi } \tilde { \pi } ^ { \prime } } { \pi _ { K } ^ { 2 } } \sum _ { ( K ) } \frac { 1 } { \sigma _ { K , t } ^ { 2 } } , \\$$

$$b \ = \ \left [ \begin{array} { c c } \frac { \pi _ { 1 } } { \pi _ { K } } \sum _ { ( K ) } \frac { \varepsilon _ { t } } { \sigma _ { K , t } ^ { 2 } } - \sum _ { ( 1 ) } \frac { \varepsilon _ { t } } { \sigma _ { 1 , t } ^ { 2 } } \\ \vdots \\ \frac { \pi _ { K - 1 } } { \pi _ { K } } \sum _ { ( K ) } \frac { \varepsilon _ { t } } { \sigma _ { K , t } ^ { 2 } } - \sum _ { ( K - 1 ) } \frac { \varepsilon _ { t } } { \sigma _ { K - 1 , t } ^ { 2 } } \right ] , \\ \\ ( \pi _ { 1 } , \dots , \pi _ { K - 1 } ) \text { and } \sum _ { ( k ) } \text { means summation over all } t \text { for which } G _ { t } = k ,$$

where  ̃ π = ( π 1 , . . . , π K - 1 ) and ∑ ( k ) means summation over all t for which G t = k , Once  ̃ μ has been drawn, the last mean μ K is obtained from (3).

- φ ( θ | G T , ν, μ, π, R )

By assuming prior independence between the θ k 's, that is φ ( θ ) = ∏ K k =1 φ ( θ k ), it follows that

$$\varphi ( \theta | G ^ { T } , \nu , \mu , \pi , R ) \ & = \ \varphi ( \theta | G ^ { T } , \nu , \mu , R ) \\ & = \ \varphi ( \theta _ { 1 } | \nu , \mu _ { 1 } , \widetilde { R } ^ { 1 } ) \varphi ( \theta _ { 2 } | \nu , \mu _ { 2 } , \widetilde { R } ^ { 2 } ) \cdots \varphi ( \theta _ { K } | \nu , \mu _ { K } , \widetilde { R } ^ { K } ) \\ \text {where } \widetilde { R } ^ { k } = \{ R _ { t } | G _ { t } = k \} \text { and }$$

$$\varphi ( \theta _ { k } | \nu , \mu _ { k } , \widetilde { R } ^ { k } ) & \ \ \ \alpha \quad \varphi ( \theta _ { k } ) \ \prod _ { t \in G _ { t } = k } \ \phi ( R _ { t } | \mu _ { k } + \rho _ { t } ( \nu ) , \theta _ { k } ) . \\ \intertext { w e c d i t i o n o r t h e s t a r i v a b i l e s , w e c a n s i m u late e a c h b l o c k \theta _ { k } \ s e p a r a t i y . \ W e }$$

where  ̃ R k = { R t | G t = k } and

Since we condition on the state variables, we can simulate each block θ k separately. We do this with the griddy-Gibbs sampler (for further details, see Bauwens, Lubrano, and Richard (1999)). We take bounded uniform supports for ω k , α k and β k . The choice of these bounds are finely tuned in order to cover the relevant posterior parameter support. Doing so, we only impose diffuse priors.


<!-- p:26 -->


- φ ( ν | G T , μ, π, θ, R )

The conditional posterior distribution for this block does not belong to a known family of distributions. Since ν is a scalar, we can sample directly numerically by drawing one observation from a uniform distribution on [0 , 1] and finding the corresponding quantile of the conditional posterior distribution of ν . We use a diffuse prior for ν .

Convergence of the Gibbs sampler is checked with CUMSUM plots of the parameter draws as explained for example in Bauwens, Lubrano, and Richard (1999). To ensure a good precision of posterior moments in this paper, we take N = 20 , 000 and a warm up of 5 , 000 draws to ensure convergence to the target joint posterior distribution and to eliminate the impact of the starting values on the final results. All of the posterior results and the option prices in this paper are obtained within hours on a standard desktop computer.

### 4.2 Predictive densities and option prices

To compute option prices, we first need to have predictive return densities under the Q measure. The predictive density of R T +1 under the risk neutral measure Q is given by

$$f ^ { Q } ( R _ { T + 1 } | \ R ) \ = \ \int f ^ { Q } ( R _ { T + 1 } | \ \xi , R ) \, \varphi ( \xi \, | \, R ) \, d \xi \\$$

where f Q ( R T +1 | ξ, R ) = ∑ K k =1 π ∗ k φ ( R T +1 | μ ∗ k + ρ T +1 ( ν ) , θ k ) as implied by the finite mixture distribution defined in (1). Unlike prediction in the classical framework, note that predictive densities take into account parameter uncertainty by construction while integrating the predictive likelihood over the parameter space. An analytical solution to (51) is unavailable but extending the algorithm of Geweke (1989b), it can be approximated by

$$\text { but extending the algorithm of Geweke (1969b), it can be applied proximated by} \\ \widehat { f ^ { Q } } ( R _ { T + 1 } | R ) \ = \ \frac { 1 } { N } \sum _ { j = 1 } ^ { N } \left ( \sum _ { k = 1 } ^ { K } \pi _ { k } ^ { * ( j ) } \phi \left ( R _ { T + 1 } | \mu _ { k } ^ { * ( j ) } + \rho _ { T + 1 } ( \nu ) , \theta _ { k } ^ { ( j ) } , R \right ) \right ) \\ \\ \text {where the superscript (j) indexes the draws generated with the Gibbs sampler and N is the}$$

where the superscript ( j ) indexes the draws generated with the Gibbs sampler and N is the number of draws. Therefore, simultaneously with the Gibbs sampler where we simulate N times ξ ( j ) ∼ φ ( ξ | R ), we simulate R ( j ) T +1 ∼ f Q ( R T +1 | ξ ( j ) , R ). A similar algorithm is used by Bauwens and Lubrano (2002). Extending the idea used for R T +1 , the predictive density for R T + s under the Q measure may be written as


<!-- p:27 -->


$$\text {for } R _ { T + s } \text { under the } Q \text { measure may be written as } \\ f ^ { Q } ( R _ { T + s } | \ R ) \ = \ \int \left [ \iint \dots \int f ^ { Q } ( R _ { T + s } | \ R _ { T + s - 1 } , \dots , R _ { T + 1 } , R , \xi ) \times \\ f ^ { Q } ( R _ { T + s - 1 } | \ R _ { T + s - 2 } , \dots , R _ { T + 1 } , R , \xi ) \times \\ \dots \times \\ f ^ { Q } ( R _ { T + 1 } | \ R , \xi ) d R _ { T + s - 1 } d R _ { T + s - 2 } d R _ { T + 1 } \right ] \varphi ( \xi \ | \ R ) \ d \xi , \\ \intertext { \text {for which draws can be obtained by extending the above algorithm to a } ( s + 1 ) \text {-step algorithm} }$$

for which draws can be obtained by extending the above algorithm to a (s+1)-step algorithm. The draw of R T +1 serves as conditioning information to draw R T +2 , both realizations serve to draw R T +3 , etc. These draws are generated from the finite mixture of normal densities with adjusted parameters to sample under the Q measure. A non Bayesian procedure typically proceeds by conditioning on a point estimate of ξ , which ignores the estimation uncertainty.

The predictive densities described until here are return densities. To obtain predictive option prices, we need price densities at the maturity date of the option contract. This predictive price density is obtained by aggregating the predicted returns until maturity for each of the N draws. For the European option example in (12), we obtain

$$\text {cuh} \, \exp \left ( 1 + \text {draw} \cdot \text {R} \right ) \, \exp \left ( 1 + \text {exp} \right ) \, \exp \left ( 1 + \exp \right ) \, \exp \left ( 1 + \exp \right ) \, , \\ C _ { T } ( S , T ^ { * } , K ) \, \approx \, e ^ { - r ( T ^ { * } - T ) } \frac { 1 } { N } \, \sum _ { j = 1 } ^ { N } \max \left ( S _ { T } \exp \left ( \sum _ { i = T } ^ { T ^ { * } } R _ { i } ^ { ( j ) } \right ) - K , 0 \right ) , \\ \\ \ m b { i } { h } _ { \ } s o n \, b e \, e x u l t e d \, \text {nonduly} \, U \, \text {ing} \, \text {the} \, \text {Poeccion} \, \text {infor nonce} \, \text {app} \, \text {schn} \, \text {b, we have} \, \text {the} \, \text {complete} \,$$

which can be evaluated rapidly. Using the Bayesian inference approach, we have the complete predictive price density at maturity. In fact, once we have the N draws from the predictive densities until maturity T ∗ , we can price any contract defined on the underlying S until that maturity.

## 5 Pricing S&amp;P 500 options

We now take our model to the data and evaluate its out-of-sample forecast performance by pricing a large sample of options. We compare the performance to a benchmark Gaussian GARCH model, which is a special case of our MNGARCH model with K = 1. This benchmark model has been used extensively in the literature, and it has been shown to improve significantly on the performance of the constant volatility BSM model for example. Note that the constant volatility mixture model, which allows for non zero skewness and excess kurtosis, also performs worse than this benchmark. We therefore refrain from reporting results on these two unconditional models.


<!-- p:28 -->


Until now, we have considered the general formulation of the MNGARCH model without fixing K , the number of distributions in the finite mixture. However, when applying the model empirically a choice has to made about K , and this is the first issue we investigate. It turns out that for our sample, there is no evidence for adding a third distribution. In fact, we find that the probability to be in the last distribution is found to be indistinguishable from zero for K = 3. Therefore, K = 2 is considered as optimal, and in the following we report results for this case only.

In the next section, we describe the option data as well as the data we use for inference purposes in detail. We then proceed to report detailed results for the parameter estimates for the first week for which option data is available. The last section contains the overall pricing results using the full sample of 8 , 637 option contracts on the S&amp;P 500 index in 2006.

### 5.1 Data

In the present paper, we use option data from the CBOE provided by Market Data Express, return and dividend data for the S&amp;P 500 index from Datastream, and interest data from the H.15 Federal Reserve Statistical Release, all of which we now describe in detail.

#### 5.1.1 Option data

The option data set contains one daily observation for each option contract on the S&amp;P 500 index traded at the CBOE. We work with option data for 2006 for which approximately 180 , 000 observations are available. Thus, for this to be manageable we impose the following restrictions. First, we consider weekly data and choose the options traded on Wednesdays. This choice is made to balance the tradeoff between having a long time period against the computational complexity. We choose Wednesdays as these options are least affected by weekend effects. Secondly, we choose to work only with those contracts which had a daily volume of trades larger than or equal to 5. Thirdly, we exclude options which have a midquote Mean price in USD, mean ISD, and number of contracts in the cells of this table. The maturity (columns) and moneyness (lines) are defined in the text.


<!-- p:29 -->


Table I: Properties of the S&amp;P 500 index options data set (Calls)

|      | Time to maturity in days   | Time to maturity in days   | Time to maturity in days   | Time to maturity in days   | Time to maturity in days   | Time to maturity in days   |
|------|----------------------------|----------------------------|----------------------------|----------------------------|----------------------------|----------------------------|
|      | VST                        | ST                         | MT                         | LT                         | VLT                        | ALL                        |
| DOTM | -                          | $ 0.86                     | $ 1.76                     | $ 5.20                     | $ 12.33                    | $ 4.54                     |
| OTM  | - 0 $ 1.32 0.0898          | 0.0988 60 $ 2.84 0.0910    | 0.0946 135 $ 6.69 0.0969   | 0.1021 103 $ 17.86 0.1103  | 0.1090 68 $ 29.81 0.1181   | 0.1001 366 $ 7.50 0.0967   |
| ATM  | 107 $ 11.67 0.0969         | 350 $ 17.45 0.1041         | 229 $ 25.34                | 93 $ 39.30 0.1223          | 68 $ 51.13 0.1281          | 847 $ 21.70 0.1072         |
|      | 363 $ 42.87                | 450                        | 0.1120 360                 | 127                        | 68                         | 1368                       |
| ITM  | 0.1225                     | $ 45.81 0.1231             | $ 52.21 0.1253             | $ 63.11 0.1307             | $ 76.54 0.1370             | $ 52.40                    |
| DITM | 148 $ 117.41               | 144 $ 117.46               | 109 $ 135.02               | 65 $ 125.57                | 70                         | 0.1261 536                 |
|      | 0.1342 81                  | 0.1448 136                 | 0.1561 115                 | 0.1534 65                  | $ 122.61 0.1485 80         | $ 123.65 0.1475            |
| ALL  | $ 28.95                    | $ 27.60                    | $ 33.87                    | $ 42.94                    | $ 60.76                    | $ 24.95                    |
|      |                            |                            | 0.1128                     |                            |                            | 477                        |
|      | 0.1056                     |                            |                            | 0.1209                     | 0.1289                     | 0.1122                     |
|      |                            | 0.1070                     |                            |                            |                            |                            |
|      | 699                        | 1140                       | 948                        | 453                        | 354                        | 3594                       |

below half a dollar, and we use the midquote as the price. Finally, we eliminate options in the LEAPS series as the contract specifications for these options do not correspond to that of the standard options. In total, we end up with a sample of 8 , 637 options of which 3 , 594 are calls and 5 , 043 are puts.

In Table I, we provide descriptive statistics for the call option in terms of the number of options, the average prices as well as average implied standard deviations (ISD) from the BSM model. We tabulate data for various categories of maturity measured in trading days, T ∗ , and moneyness measured as M = S/ ( K exp ( - rT ∗ )), where S is the value of the underlying, K is the strike price, and r is the risk free interest rate. The maturity categories are divided into very short term (VST), with T ∗ &lt; 22, short term (ST), with 22 ≤ T ∗ &lt; 43, medium term (MT), with 43 ≤ T ∗ &lt; 85, long term (LT), with 85 ≤ T ∗ &lt; 169, and very long term (VLT), with T ∗ ≥ 169. For the call options, the moneyness categories are divided into deep out of the money (DOTM), with M &lt; 0 . 95, out of the money (OTM), with 0 . 95 ≤ M &lt; 0 . 98, at the money (ATM), with 0 . 98 ≤ M &lt; 1 . 02, in the money (ITM), with 1 . 02 ≤ M &lt; 1 . 05, and deep in the money (DITM), with M ≥ 1 . 05. Table II contains similar descriptive statistics for these categories for the put options. For the put options, the moneyness categories are inverted, for example the DOTM put options have M ≤ 1 . 05.


<!-- p:30 -->


Besides the overrepresentation of DOTM put options, Tables I and II show that our sample contains a diverse sample of traded options. First of all, in terms of the number of contracts even the VLT category contains a large number and so does the DITM category. Naturally, most of the options in our sample are ATM options with ST maturity. Next, in terms of option prices, the two tables show that the mean of these vary from $0.86 to $135.02 for the call options and from $1.20 to $142.04 for the put options thus spanning a very large interval. Finally and most importantly, we observe the well known volatility smirk which is present for both call and put options. To be specific, Table I shows that the mean ISD is higher for DITM options than for DOTM options and Table II shows that the mean ISD is higher for DOTM options than for DITM options.

#### 5.1.2 Return, dividend and interest rate data

As return data, we use a total return index (Datastream data type RI), which is calculated under the assumption that dividends are re-invested. Figure 2 displays the sample path, the normal quantile plot, and the autocorrelation functions for returns and for squared returns. Panel (a) of this figure shows the well known pattern of time varying volatility with periods of high volatility levels followed by periods of low levels of volatility, which is often observed in financial data. Panel (b) clearly shows that returns are far from being Gaussian and instead have fat tails. Finally, Panel (c) provides evidence of the lack of persistency in raw returns, i.e. the first moment of the series, whereas Panel (d) provides evidence of the strong persistency in squared returns, i.e. a proxy of the second moment of the series.


<!-- p:31 -->


Table II: Properties of the S&amp;P 500 index options data set (Puts)

Mean price in USD, mean ISD and number of contracts in the cells of this table. The maturity (columns) and moneyness (lines) are defined in the text.

|      | Time to maturity in days   | Time to maturity in days   | Time to maturity in days   | Time to maturity in days   | Time to maturity in days   | Time to maturity in days   |
|------|----------------------------|----------------------------|----------------------------|----------------------------|----------------------------|----------------------------|
|      | VST                        | ST                         | MT                         | LT                         | VLT                        | ALL                        |
| DITM | $ 99.12 0.0999             | $ 123.69 0.0936            | $ 140.04 0.0839            | $ 132.87 0.0955            | $ 142.04 0.1020            | $ 127.23 0.0937            |
| ITM  | 24 $ 43.37 0.0746 87       | 24 $ 49.33 0.0966 82       | 32 $ 57.75 0.1054 45       | 20 $ 74.83 0.1104 31       | 16 $ 94.64 0.1111 12       | 116 $ 53.98 0.0931 257     |
| ATM  | $ 13.13 0.0985 352         | $ 20.21 0.1090             | $ 28.20 0.1170             | $ 49.07 0.1256 103         | $ 68.49 0.1282             | $ 24.22 0.1100             |
|      | $ 2.73                     | 398 $ 8.03                 | 306 $ 15.84                | $ 34.41                    | 39                         | 1198                       |
| OTM  | 0.1280 251                 | 0.1285 315                 | 0.1295 229                 | 0.1338 120                 | $ 50.37 0.1357 58          | $ 14.28 0.1297 973         |
| DOTM | $ 1.20                     | $ 2.52                     | $ 5.20                     | $ 11.42                    |                            |                            |
|      | 0.1775 267                 | 0.1711 715 $ 12.63         | 0.1713 637                 | 0.1745 521                 | $ 21.85 0.1663 359         | $ 7.69 0.1718 2499         |
| ALL  | $ 12.00                    |                            | $ 18.13                    | $ 25.29                    | $ 34.80                    | $ 18.00                    |
|      | 0.1255                     | 0.1410                     |                            |                            |                            | 0.1432                     |
|      |                            |                            | 0.1457                     | 0.1575                     | 0.1561                     |                            |
|      | 981                        | 1534                       | 1249                       | 795                        | 484                        | 5043                       |

Table III provides the standard descriptive statistics for the S&amp;P 500 index return series. The numbers in this table show that the return data is slightly negatively skewed and very leptokurtic. The classical Jarque-Bera test rejects the null of normality at any level of significance due to the high level of kurtosis. However, the individual test for skewness results in a p-value of 1.15%.

For pricing purposes, we need an estimate of future dividend payments since options are written on the actual index value and not on the total return index. For this, we choose to use the Dividend Yield (Datastream data type DY). This series is calculated as a rolling This figure plots the sample path, QQ plot, ACF's of returns and squared returns using a sample period from September 11, 1990 to December 27, 2006 (4,252 observations) .


<!-- p:32 -->


Figure 2: Properties of the S&amp;P 500 returns

average of the daily yields for the previous year. Panel (a) of Figure 3 displays the sample paths for this series. From this, it is seen that while the dividend yield changes through time, for the last part of the period which is used for pricing, it is quite stable. Thus, in the pricing part, we simply set the future dividend equal to the historical dividend yield at the day of pricing.

Finally, in order to perform inference and forecast option prices, we need a series of interest rates. We use the series of one month Eurodollar deposit rates provided by the H.15 Federal Reserve Statistical Release. Panel (b) of Figure 3 displays the sample paths for the daily interest rates. While the plot clearly shows that this series changes over time, it may also be observed that during the last part of the sample, it remains relatively constant. Since this is the period over which we will be pricing options, we simply assume that the interest rate remains constant over the life of the option, and set it equal to the prevailing rate at This figure plots the sample paths of the dividend yields and interest rates using a sample period from September 11, 1990 to December 27, 2006 (4,252 observations) .


<!-- p:33 -->


Table III: Descriptive statistics for S&amp;P 500 index percentage returns Sample period: September 11, 1990 to December 27, 2006 (4,252 observations)

| Mean               |   0.042963 | Maximum   |   5.5754 |
|--------------------|------------|-----------|----------|
| Standard deviation |    0.97980 | Minimum   |  -7.1130 |
| Skewness           |  -0.094923 | Kurtosis  |   7.2501 |

Figure 3: Sample paths of the dividend yield and interest rate

the day of pricing.

### 5.2 Posterior results

Table IV displays posterior moments for the GARCH and MNGARCH models. The results are based on the data used for pricing of week one in the option pricing data. As it is often found in the literature, the posterior means of the GARCH model imply a highly persistent variance process since α 1 + β 1 = 0 . 995. For the MNGARCH model, we see that the second distribution has an explosive variance process since 0 . 237+0 . 869 &gt; 1. Given that the probability to be in this state is small, i.e. 1 - π = 0 . 246, the second order stationarity condition stated in equation (7) is still met. It is thanks to this distribution that we can accommodate for example the high kurtosis in the returns of the underlying.

Table V informally compares the moments of the data with the moments implied by the posterior mean parameters of the GARCH and MNGARCH models. From this table, we


<!-- p:34 -->


####### Table IV: Posterior means and standard deviations

Week 1. September 5, 1990 to January 3, 2006 (4,000 observations). A - symbol means that the parameter is set to 0. Posterior moments based on 20,000 draws from the Gibbs sampler defined in Section 4.

|     | GARCH   | GARCH              | MNGARCH   | MNGARCH            |
|-----|---------|--------------------|-----------|--------------------|
|     | mean    | standard deviation | mean      | standard deviation |
| ν   | 6.139   | (1.081)            | 4.534     | (1.348)            |
| μ   | -       | -                  | 0.001     | (0.0001)           |
| π   | -       | -                  | 0.754     | (0.082)            |
| ω 1 | 5.1E-7  | (9.9E-7)           | 6.8E-8    | (5.8E-8)           |
| α 1 | 0.054   | (0.007)            | 0.018     | (0.006)            |
| β 1 | 0.941   | (0.008)            | 0.970     | (0.008)            |
| ω 2 | -       | -                  | 4.3E-6    | (2.0E-6)           |
| α 2 | -       | -                  | 0.237     | (0.071)            |
| β 2 | -       | -                  | 0.869     | (0.031)            |

see that the GARCH model can match the variance but clearly not the kurtosis of the data. The MNGARCH model, on the other hand, matches both the standard deviation and the kurtosis nicely. With respect to the skewness, it should be noted that, given the size of the estimates, these are both insignificantly different from zero.

With respect to the unit risk premium parameter ν , Table IV shows that the posterior mean of ν is centered around 6 . 139 for the GARCH model and 4 . 534 for the MNGARCH model. Figure 4 plots the posterior marginals for ν and shows that they are symmetrically This figure plots the posterior marginal densities of the unit risk premium ν using 20,000 draws from the Gibbs sampler .

Table V: Empirical and implied moments of the returns (week 1) Simulated moments using 50,000 draws for the GARCH and MNGARCH models.

|           |   Standard deviation |   Skewness |   Kurtosis |
|-----------|----------------------|------------|------------|
| Empirical |               0.9984 |   -0.09517 |     7.1077 |
| GARCH     |               1.0316 |    0.06911 |     4.5840 |
| MNGARCH   |               1.0143 |    0.10518 |     7.4169 |


<!-- p:35 -->


Figure 4: Posterior marginal densities of ν

distributed away from zero. Comparing the size of the estimates, we note that while it may seem that the unit risk premium is larger for the GARCH model than for the MNGARCH model this, in fact, is to be expected as this model neglects the impact of higher order conditional moments. In particular, as it was mentioned above the higher order terms in (31) varies negatively with conditional skewness and positively with conditional excess kurtosis for a given level of ν . Hence, when these terms are neglected, a higher ν is required to compensate investors appropriately for the risk of the asset.

### 5.3 Option pricing results

For option pricing to proceed, we need the risk neutral dynamics, i.e. the dynamics under Q . As mentioned in the introduction, our method allows us to derive these using only historical data on returns and hence no calibration to historical option prices is needed. Figure 5 displays the term structure of the mean, variance, skewness and kurtosis of the predicted returns under Q until the highest maturity, i.e. 248 trading days, for week 1 for the GARCH and MNGARCH models.

While the first two moments are similar for the two models, this is clearly not the case for the skewness and the kurtosis. In particular, for the GARCH model skewness is zero as expected, whereas the risk neutral dynamics of the MNGARCH model has pronounced negative skewness. Likewise, for the kurtosis large differences are also observed as the level This figures plots the term structure of the first four moments of the predictive return densities under Q using 20,000 draws from the Gibbs sampler .


<!-- p:36 -->


Figure 5: Week 1 term structure under Q

<!-- p:37 -->


is much higher for the MNGARCH model than for the GARCH model. These features are related to the explosive volatility process in the second distribution of the finite mixture which in the risk neutral dynamics becomes even more important as π ∗ t &lt; π .

It is well known that skewness and excess kurtosis are important for option pricing purposes, and will potentially affect different categories of options. In particular, excess kurtosis increases the predicted value of both DITM and DOTM options and lowers predicted prices of ATM options. The large negative skewness will, everything else equal, contribute positively to OTM and DOTM put options and ITM and DITM call options. Table I and II show that both of these effects are relevant for our sample of options.

#### 5.3.1 Dollar losses

We now proceed to compare out-of-sample our MNGARCH model to the classical GARCH model in terms of actual prices. Since we price options for 52 weeks in 2006, we update the return data on a weekly basis to compute the predictive price densities. We could also update the posterior densities weekly, but given that our inference is based on the last 4,000 observations neither the parameters nor the predictive densities would change substantially when doing this. Table VI provides dollar losses for the calls, calculated as the observed price minus the predicted price, whereas Table VII provides dollar losses for the puts. The tables also report the root mean squared error (RMSE). In both tables, the top panels provide the results for the GARCH model whereas the results for the MNGARCH model are found in the bottom panels. In all tables and panels, we categorize the losses according to the maturity and moneyness as defined in Section 5.1.2.

Examining first the overall results, we see that there are pronounced differences between the performance of the two models. Using the dollar losses, it appears that the GARCH models performs the best for call options whereas the MNGARCH models perform the best for put options. For the call options, Table VI shows a clear pattern across both moneyness and maturity. In particular, when comparing the two panels, it is only for the ATM category that the GARCH model has the smallest losses. For the DOTM options with VLT maturity, the MNGARCH model improves on the GARCH model with an average $1.92. In percentage of the mean option prices, the improvement is as high as 37% for the DOTM options with OTM


<!-- p:38 -->


VST

####### Table VI: Dollar losses for Calls

In the cells of this table, the first number is the mean error and the second number is the root mean squared error both measured in USD. The maturity (columns) and moneyness (lines) are defined in Section 5.1.2.

|      | GARCH          | GARCH              | GARCH              | GARCH              | GARCH              | GARCH              |
|------|----------------|--------------------|--------------------|--------------------|--------------------|--------------------|
|      | VST            | ST                 | MT                 | LT                 | VLT                | ALL                |
| DOTM | -              | -1.532             | -2.477             | -4.772             | -6.836             | -3.778             |
| OTM  | - -1.443 1.768 | 1.866 -1.977 2.443 | 2.839 -2.580 3.185 | 5.205 -3.430 4.306 | 7.251 -4.520 5.320 | 4.576 -2.436 3.148 |
| ATM  | -0.756 1.632   | -0.454 2.157       | 0.421 2.756        | 0.355 3.145        | -0.593 3.525       | -0.236 2.402       |
| ITM  | 0.933          | 1.868              | 3.241              | 3.703              | 4.191              | 2.415              |
| DITM | 1.556          | 2.730 1.428        | 4.123              | 4.707              | 5.311              | 3.535              |
|      | 0.477          | 2.228              | 3.467              | 5.803              | 6.913              | 3.274              |
| ALL  | 1.385          |                    | 4.325              | 6.539              | 7.580              | 4.660              |
|      | -0.361         | -0.461             | -0.023             | -0.325             | 0.095              | -0.092             |
|      | 1.612          | 2.321              | 3.272              | 4.696              | 6.041              | 3.432              |

###### MNGARCH

ST

MT

LT

VLT

ALL

DOTM

-

-1.211

-2.015

-3.540

-4.915

-2.851

-

1.453

2.269

3.860

5.259

3.402

-1.260

-1.794

-2.261

-2.519

-2.896

-2.021

ATM

1.523

2.166

2.771

3.495

3.806

2.610

-0.860

-0.639

0.235

0.806

0.780

-0.263

ITM

1.639

2.087

2.668

3.158

3.311

2.343

0.621

1.361

2.495

3.402

4.731

2.075

DITM

1.493

2.361

3.365

4.299

5.551

3.268

0.417

1.200

2.971

5.481

6.748

3.008

ALL

1.368

2.150

3.882

6.245

7.216

4.395

-0.460

-0.552

-0.096

0.179

1.110

-0.158

1.562

2.128

2.902

4.116

5.297

3.001


<!-- p:39 -->


ITM

VST

####### Table VII: Dollar losses for Puts

In the cells of this table, the first number is the mean error and the second number is the root mean squared error both measured in USD. The maturity (columns) and moneyness (lines) are defined in Section 5.1.2.

|      | GARCH              | GARCH             | GARCH             | GARCH             | GARCH              | GARCH        |
|------|--------------------|-------------------|-------------------|-------------------|--------------------|--------------|
|      | VST                | ST                | MT                | LT                | VLT                | ALL          |
| DITM | -0.208             | -0.142            | -1.624            | -4.340            | -8.151             | -2.393       |
| ITM  | 1.262 -1.029       | 1.789 -1.612      | 2.517 -2.217      | 4.899 -2.744      | 8.601 -6.188       | 4.133 -1.871 |
| ATM  | 1.803 -0.562 1.584 | 2.708 0.122 2.138 | 3.288 1.126 2.852 | 3.454 0.274 3.247 | 6.627 -0.962 3.806 | 2.970 0.155  |
| OTM  | 1.036              | 2.400             |                   | 4.026             | 3.553 4.695        | 2.360        |
|      | 1.405              | 2.870             | 3.645 4.248       | 4.794             |                    | 2.610 3.402  |
| DOTM | 0.995              | 1.829             | 3.223             | 5.074             | 6.418              | 3.431        |
|      | 1.196              | 2.189             |                   |                   |                    |              |
|      |                    |                   | 3.771             | 5.752             | 7.202              | 4.416        |
| ALL  | 0.238              | 1.289             | 2.466             | 3.752             | 4.686              | 2.174        |
|      | 1.456              | 2.357             | 3.620             | 5.252             | 6.768              | 3.831        |

###### MNGARCH

ST

MT

LT

VLT

ALL

DITM

-0.318

-0.166

-1.117

-2.797

-6.441

-1.778

1.228

1.929

2.131

3.646

6.972

3.366

-0.925

-1.308

-1.729

-1.830

-4.590

-1.468

ATM

1.703

2.549

2.974

3.067

4.885

2.617

-0.699

-0.118

-0.916

1.137

0.589

0.106

OTM

1.563

2.051

2.731

3.081

3.402

2.283

0.724

1.828

2.951

3.973

4.055

2.205

DOTM

1.203

2.441

3.628

4.601

4.853

3.069

0.868

1.554

2.728

4.508

5.901

3.021

ALL

1.084

1.938

3.271

5.184

6.565

3.965

0.081

0.997

2.066

3.559

4.584

1.831

1.364

2.114

3.183

4.768

6.158

3.384


<!-- p:40 -->


ST maturity.

For the put options, the MNGARCH model outperforms the GARCH model and as Table VII shows the losses are approximately 16% or $0.34 smaller. This holds true along both dimensions of the data indicating clearly that the flexible dynamics accommodated by this model are important for the pricing of put options. The largest average improvement in dollar losses is $1.71 for the DITM options with VLT maturity. In percentage of the mean option prices, the improvement is largest for the shorter term options which are out of the money. For several of these categories, this improvement exceeds 10% to 15%.

While the ranking of the models in terms of dollar losses are ambiguous for the call options, the ranking of the models in terms of RMSE is clear. In particular, using this metric the MNGARCH model is the best for both calls and puts. This holds not only overall but also along both moneyness and maturity dimensions. Moreover, the improvements of the MNGARCH model are in several cases of a significant size. Consider, as an example, the DOTM category where the GARCH RMSE equals 4 . 576 and the MNGARCH RMSE equals 3 . 402. This corresponds to a reduction of approximately 25%.

#### 5.3.2 Implied standard deviation losses

Whereas the section above considered actual dollar losses, another often used metric for comparing the performance of alternative option pricing models is losses in ISD's. Tables VIII and IX provide these losses for the call and put options, respectively. In both tables, the losses are calculated as the difference between the ISD of the market price and the ISD of the predicted price. Thus, when comparing these numbers across all the options we may firstly gauge whether or not the models generate a sufficiently high level of volatility under the risk neutral measure Q in general. Secondly, if a particular model can explain the smile or smirk, which is documented in Tables I and II for our option sample, losses should be constant across moneyness for the various maturity.

Although the overall losses are not exactly equal to zero, they are in fact quite close to zero. This is so especially for the call options. For the put options, the overall losses are slightly positive and somewhat larger for the GARCH model. This indicates that this model fails to produce a high enough level of volatility under Q , a feature which is well known in In the cells of this table, the first number is the mean error and the second number is the root mean squared error both measured in ISD's. The maturity (columns) and moneyness (lines) are defined in Section 5.1.2.


<!-- p:41 -->


Table VIII: Implied volatility losses for Calls

|      | GARCH                   | GARCH        | GARCH               | GARCH        | GARCH               | GARCH        |
|------|-------------------------|--------------|---------------------|--------------|---------------------|--------------|
|      | VST                     | ST           | MT                  | LT           | VLT                 | ALL          |
| DOTM | -                       | -0.024       | -0.026              | -0.027       | -0.023              | -0.025       |
|      | -                       | 0.027        | 0.028               | 0.030        | 0.024               | 0.028        |
| OTM  | -0.023                  | -0.020 0.023 | -0.016              | -0.011 0.014 | -0.011 0.012        | -0.017       |
|      | 0.026                   |              | 0.020               |              |                     | 0.021        |
| ATM  | -0.007 0.016            | -0.003 0.013 | 0.002 0.012         | 0.001 0.009  | -0.001 0.008        | -0.003 0.013 |
| ITM  | 0.017 0.036 0.018 0.085 | 0.015 0.022  | 0.016 0.020         | 0.010 0.014  | 0.009 0.012         | 0.014 0.028  |
| DITM | -0.002 0.037            | 0.034 0.076  | 0.048 0.073         | 0.029 0.035  | 0.021               | 0.032 0.067  |
| ALL  |                         | -0.003 0.032 | 0.031               | -0.003       | 0.031               |              |
|      | VST                     |              | 0.001               | 0.022        | 0.001               | -0.001       |
|      |                         |              | MNGARCH             | LT           | 0.020               | 0.031        |
|      | -                       | ST -0.020    | MT                  | -0.021       | VLT                 | ALL          |
| DOTM | - -0.020                | 0.022        | -0.022 0.024 -0.014 | 0.023 -0.009 | -0.017 0.018 -0.007 | -0.020 0.022 |
| OTM  | 0.023                   | -0.018 0.019 | 0.017 0.001         | 0.012 0.002  | 0.009               | -0.015 0.019 |
| ATM  | -0.008                  | -0.004       | 0.012               |              | 0.001               | -0.003       |
| ITM  | 0.010                   | 0.013 0.010  | 0.012               | 0.009        | 0.007               | 0.013        |
|      | 0.015                   |              |                     | 0.009        |                     |              |
|      |                         |              |                     |              | 0.010               |              |
|      |                         |              |                     |              |                     | 0.010        |
|      | 0.034                   | 0.018        | 0.016               | 0.012        | 0.012               |              |
|      |                         |              |                     |              |                     | 0.022        |
| DITM | 0.012                   | 0.029        | 0.039               | 0.026        | 0.018               | 0.027        |
|      | 0.090                   | 0.059        | 0.073               | 0.036        | 0.021               | 0.069        |
| ALL  | -0.004                  | -0.003       | 0.000               | -0.001       | 0.002               | -0.002       |
|      | 0.037                   | 0.033        | 0.018               | 0.019        | 0.015               | 0.030        |


<!-- p:42 -->


Table IX: Implied volatility losses for Puts

In the cells of this table, the first number is the mean error and the second number is the root mean squared error both measured in ISD's. The maturity (columns) and moneyness (lines) are defined in Section 5.1.2.

|         | GARCH               | GARCH             | GARCH         | GARCH        | GARCH               | GARCH               |
|---------|---------------------|-------------------|---------------|--------------|---------------------|---------------------|
|         | VST                 | ST                | MT            | LT           | VLT                 | ALL                 |
| DITM    | 0.011               | -0.026            | -0.041        | -0.034       | -0.028              | -0.025              |
|         | 0.115               | 0.076             | 0.069         | 0.049        | 0.031               | 0.076               |
| ITM     | -0.037              | -0.018            | -0.013        | -0.009       | -0.015              | -0.022              |
|         | 0.059               | 0.031             | 0.019         | 0.011        | 0.016               | 0.040               |
| ATM     | -0.006 0.017        | 0.001 0.013       | 0.005 0.012   | 0.001 0.009  | -0.002 0.008        | -0.000 0.0137       |
| OTM     | 0.021 0.025 0.057   | 0.020 0.023 0.053 | 0.018 0.021   | 0.012 0.014  | 0.008 0.011         | 0.018 0.022         |
| DOTM    | 0.063 0.016 0.045   | 0.058             | 0.052 0.058   | 0.043 0.048  | 0.031               | 0.048 0.054         |
| ALL     |                     | 0.028 0.043       | 0.029         | 0.029 0.040  | 0.035               | 0.025               |
|         | VST                 |                   | 0.044 MNGARCH |              | 0.022 0.031         | 0.042               |
|         |                     |                   | MT            | LT           |                     |                     |
| DITM    | -0.007              | ST -0.032         | -0.037        | -0.027 0.043 | VLT                 | ALL                 |
|         | 0.121 -0.036        | 0.090 -0.016      | 0.061 -0.010  | -0.006       | -0.023 0.025 -0.011 | -0.026 0.078 -0.020 |
| ITM ATM | 0.059 -0.007 -0.001 | 0.031             | 0.014 0.004   | 0.010 0.009  | 0.011               | 0.040               |
| OTM     |                     | 0.013             | 0.011         | 0.003        | 0.001               | -0.001              |
|         | 0.013               |                   | 0.015         |              | 0.007               | 0.013               |
|         | 0.016               | 0.014             |               | 0.011        | 0.009               | 0.014               |
|         | 0.019               |                   | 0.018         | 0.013        | 0.011               |                     |
|         |                     | 0.019             |               |              |                     | 0.018               |
| DOTM    | 0.041               | 0.038             | 0.038         | 0.034        | 0.026               | 0.036               |
|         | 0.047               | 0.043             | 0.042         | 0.037        | 0.028               | 0.040               |
| ALL     | 0.009               | 0.019             | 0.021         | 0.024        | 0.019               | 0.019               |
|         | 0.038               | 0.034             | 0.033         | 0.032        | 0.025               | 0.033               |


<!-- p:43 -->


empirical option pricing as highlighted in the introduction. The MNGARCH model, on the other hand, is able to generate a higher volatility under Q than the GARCH model, which reduces the ISD loss with 24%. The conclusions are the same when considering the RMSE's which are 21% smaller for the MNGARCH model than for the GARCH model for the put options.

Inspecting the individual cells in Tables VIII and IX, we see that in most cases the losses are smaller for the MNGARCH model than for the GARCH model. In fact, this is so for 41 of the 49 categories for which options are available. Moreover, this is so for all the DOTM categories and for all but one of the DITM categories (the ST put options). The improvement is larger than 28% for DOTM put options with less than MT maturity. Taken together, the evidence in the two tables indicates that the MNGARCH model is capable of explaining a larger fraction of the smile in ISD's than the GARCH model.

## 6 Conclusion

In this paper, we perform option pricing using mixed normal heteroscedasticity models. We provide details on how to obtain the appropriate risk neutral dynamics and we suggest a feasible way for option pricing within this general framework. Moreover, we perform inference in a Bayesian framework which allows us to compute easily predictive price densities that take into account parameter uncertainty. We compare our option pricing model to a benchmark model and find substantial improvements in terms of both dollar losses and implied standard deviation losses for a large sample of options on the S&amp;P 500 index.

In terms of the risk neutralization, we show that the risk neutral dynamics stay within the class of mixed normal heteroscedasticity models, although the parameters of the distribution are changed. These risk neutral parameters are easily interpreted as providing investors with compensation for specific distributional features like for example the distribution with an explosive variance process found in our data. Moreover, when comparing the properties of the risk neutral distribution these differ in a pronounced way from the properties under the original measure used for inference.

We document significant difference between our model and the benchmark in terms of the risk neutral dynamics used for option pricing. In particular, our model is capable of generating negative skewness and significant amounts of excess kurtosis. In terms of pricing performance, our results confirm the importance of both of these features for our sample of index options. Our model performs best for options which are deep out of the money and deep in the money. In terms of explaining the smirk in implied volatilities, improvements are found for all maturities, and this is particularly pronounced when considering the shorter maturities.


<!-- p:44 -->


There are several interesting extensions for further research. The most obvious will be to extend our data to include the recent period of financial turmoil as data becomes available. We conjecture that this may require additional distributions in the mixture, i.e. increasing K , which is easily accommodated in our framework. With this new data it would be interesting to consider alternative benchmarks which could include discrete jumps in returns and volatility as suggested by Christoffersen, Jacobs, and Ornthanalai (2008). Another extension would be to consider Markov switching models in which returns can have a high or low mean and variance, and switches between these states are determined by a Markov process. Within this framework, it is possible to allow for state dependent unit risk premiums that further drive a wedge between the physical and risk neutral dynamics. Lastly, this paper does not use option prices for inference on the model parameters. We explained in the introduction how complicated this is for our model which is non-affine. However, it would nevertheless be interesting to investigate how the information contained in past option prices can be included in the inference procedure of this paper.
