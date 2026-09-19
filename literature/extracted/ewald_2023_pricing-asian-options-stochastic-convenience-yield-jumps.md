---
id: "ewald_2023_pricing-asian-options-stochastic-convenience-yield-jumps"
source_pdf: "../pdf/ewald_2023_pricing-asian-options-stochastic-convenience-yield-jumps.pdf"
source_filename: "ewald_2023_pricing-asian-options-stochastic-convenience-yield-jumps.pdf"
format: "academic-paper"
extraction_profile: "text-math-tables-high-fidelity"
extraction_mode: "hybrid"
extraction_quality: "excellent"
extraction_score: 100.0
visual_assets: "disabled"
references_file: "../references/ewald_2023_pricing-asian-options-stochastic-convenience-yield-jumps.references.md"
---

<!-- p:1 -->

University

of Glasgow

Ewald, C.-O., Wu, Y. and Zhang, A. (2023) Pricing Asian options with stochastic convenience yield and jumps. Quantitative Finance, 23(4), pp. 677-692.

This is the author final version of the work. There may be differences between this version and the published version. You are advised to consult the publisher's version if you wish to cite from it.

https://doi.org/10.1080/14697688.2022.2160799

https://eprints.gla.ac.uk/290021/

Deposited on: 26 April 2023

Enlighten - Research publications by members of the University of Glasgow https://eprints.gla.ac.uk


<!-- p:2 -->


## Pricing Asian Options with Stochastic Convenience Yield and Jumps

Christian-Oliver Ewald ∗ , Yuexiang Wu † , Aihua Zhang ‡§ April 25, 2023

###### Abstract

We price Asian options on commodity futures contracts in the presence of stochastic convenience yield, stochastic interest rates and jumps in the commodity spot price. In the case of no jumps, we obtain a closed-form solution for a geometric average Asian option. This analytic result enables us to employ this option as a suitable control variate when pricing the corresponding arithmetic average Asian option. Discussion of further applications and comparative statics are presented. To cover the case with jumps, we condition on the jump times first and then average over the sequences of jump times.

Keywords: Asian Options, Stochastic Convenience Yield, Jump Diffusion, Derivatives

JEL Classification:

G13, G11, D52, C63

Disclosure Statement:

None of the authors have anything to declare.

∗ Inland Norway University of Applied Sciences - Business School, 2624 Lillehammer, Norway and Adam Smith Business School - Economics, University of Glasgow, Glasgow, G12 8QQ, United Kingdom. e-mail: christian.ewald@glasgow.ac.uk

† Kingston Rayliant (Rayliant Global Advisors), 2705, East Tower, Raffles City, Dongdamin Road, Hongkou District, Shanghai, China. e-mail: yuexiang\_wu@hotmail.com

‡ Guangdong Provincial Key Laboratory of Interdisciplinary Research and Application for Data Science, BNU-HKBU United International College, China. e-mail: evaahzhang@uic.edu.cn

§ Aihua Zhang acknowledges financial support from the Department of Education of Guangdong Province under project code [2021ZDZX1059]; Start-up Research Fund from UIC [UICR0700015-22]; and Guangdong Provincial Key Laboratory of Interdisciplinary Research and Application for Data Science [2022B1212010006].


<!-- p:3 -->


### 1 Introduction

#### 1.1 General Background

In commodity markets, the so called convenience yield plays a fundamental role in interpreting the dynamics of futures and spot prices. According to Casassus and Dufresne (2005) the convenience yield can be identified as the difference between the risk neutral rate and the returns of the spot price under the risk-neutral pricing measure. In this way the convenience yield can be considered as an implicit dividend yield that takes account of the cost of storage, inventory, liquidity etc. Indeed it has been prominently featured in a long list of literature aiming to reveal its true nature. To name a few, Fama and French (1987) find statistical evidence to support the theory of storage. Heinkel et al. (1990) find a negative relationship between the level of aggregate inventory and convenience yield, and further identify two additional determinants of convenience yield, namely, marginal production costs, and spot prices of the commodity. Routledge et al. (2000) finds a positive relationship between convenience yield and spot prices, as well as a time-varying correlation between them. Schwartz (1997) shows that a stochastic convenience yield can generate mean reversion in spot prices, a feature that is crucial in many commodities.

We conduct our study following a specific avenue of research, where convenience yield is seen as having the characteristics of a dividend stream associated to a stock, modeled by a stochastic process (as in Gibson and Schwartz (1990); Schwartz (1997); Miltersen and Schwartz (1998)). We base our model largely on Schwartz (1997), where three stochastic factors are embedded, including the spot price, the convenience yield, and the interest rate. Convenience yield and interest rate are assumed to follow mean-reverting stochastic processes, similar as in the study of Gibson and Schwartz (1990) and Vasicek (1977). The Schwartz (1997) two- and three- factor models have proven themselves as benchmarks and are able to produce realistic term structures for forward and futures prices as well as mean reversion in spot prices.

Miltersen and Schwartz (1998) as well as Hilliard and Reis (1998) have looked into the pricing of European options in the context of the Schwartz (1997) model, but not Asian options. In this paper, we consider the pricing of Asian options, which have not previously been priced within the Schwartz (1997) framework. Asian options are commonly traded in commodity markets. Particular examples include average options on Aluminum futures traded at the London Metal Exchange. The distinctive feature of Asian options is the use of the average of the underlying prices over a specified period instead of the spot or futures prices at maturity only. This provides some distinct advantages over plain vanilla options, particularly the prevention of short-term manipulation of spot prices close to maturity date in order to drive up the option price. On the other hand, from a technical point of view, it is much more challenging to price Asian options than to price the corresponding European options. For arithmetic average Asian options, even the restrictive assumptions of the Black-Scholes model do not allow for a closed form solution. Basic qualitative features of Asian option, such as the dependence on volatility and time to maturity, have only recently been uncovered, see Ewald and Yor (2015) and Ewald and Yor (2018). Kemna and Vorst (1990) suggest geometric average Asian options, that adopt the geometric average instead of the arithmetic average, to be used in the process of calculating the arithmetic average option's price. In the Black-Scholes framework, the former can be priced in closed form through a suitable modification of the Black-Scholes formula. As Kemna and Vorst (1990) demonstrate, the geometric average version can then be used as an effective control variate in reducing simulation error and yield more accurate results when pricing arithmetic average Asian options in the Black-Scholes model by Monte Carlo simulation. This is possible because the geometric average of the spot price remains log-normal distributed.


<!-- p:4 -->


#### 1.2 Contribution

In this paper we extend the ideas of Kemna and Vorst (1990) to the case of a Schwartz (1997) type model which features a stochastic convenience yield, stochastic interest rates and the possibility of stochastic jumps in the spot price. We derive an analytic formula for the geometric average Asian option and then employ it as a control variate to price an arithmetic average Asian option using Monte Carlo simulation, at least for the case with no jumps. Our results show significant improvements in accuracy and reduced standard errors (by a factor of about 20), in comparison with standard Monte Carlo simulation without variance reduction methods as well as antithetic variate methods. We refer to Boyle et al. (1997) for an overview of variance reduction methods in Monte Carlo simulation, including the antithetic and control variate methods. Variation of the parameters of the model in appropriate pairs provides us with some intuition and insights as to how option prices change when the parameters change. This is very useful for risk management and control of this type of options. We then consider the case of stochastic jumps in the spot price. A jump can also be interpreted as a spike in the price movement. It is usually triggered by a sudden arrival of news or supply and demand shocks, which can have an immediate and profound effect on the underlying price. In the context of commodities this is particularly relevant for electricity. Merton (1976) was arguably the first to introduce jumps into option pricing. He derived a closed-form solution for plain vanilla European options, using a Black-Scholes dynamic with added jumps. Hilliard and Reis (1998) added jumps to the spot price dynamics in the Schwartz (1997) model, and also obtained closed form solutions for European options. In both of these models, the jump component is governed by two random sources. The first one determines the occurrence of jumps and follows a Poisson process. The second one determines the size of the jump. We apply the model proposed by Hilliard and Reis (1998) including three stochastic factors and jumps in the spot price in order to price Asian options. In difference to the previous case there now is no closed-form solution, even for the geometric average Asian option. This fact obviously hinges on the path-dependency. In fact, the price of plain vanilla options only depends on the accumulated size of the jumps, but not on the individual jump sizes and in particular not on the time of each jump's occurrence. In Asian options the exact time of each jump matters. When the average of the spot prices is calculated in order to obtain the underlying of an Asian option, a jump that occurs at the beginning of an option's lifetime obviously affects the price differently than if it occurs toward the end. Provided with this challenge, we argue that conditional on knowing when each jump occurs during the option's lifetime, we are able to extend our previous methodology in order to derive a closed form solution for a geometric average Asian option. The intuition is that if the timing of each jump is assumed to be known, then the only unknown random variable of the jump process is the jump size, which is assumed to follow a log-normal distribution as in Hilliard and Reis (1998), and so are the spot price and the geometric average of it. Therefore, conditional on the sequence of jump times, a closed-form solution is achievable for a geometric average Asian option. As we show, this will still be extremely useful for variance reduction purposes. Our strategy is based on the idea to compute the expectation that determines the price of the arithmetic average Asian option in two steps by using the tower property of the conditional expectation. The first expectation is conditional on the sequence of jumps and facilitates the geometric average Asian option as a control variate, and in the second step we average over jump sequences only. We compare this method with the standard Monte Carlo method without variance reduction and with antithetic variates. The results show a significant improvement in terms of simulation accuracy.


<!-- p:5 -->


#### 1.3 Relevance to recent literature on Asian options

Recent important contributions to the thematic of pricing Asian options with special emphasis on commodities include Kyriakou et al. (2016), Ballotta et al. (2017), Tong and Allen (2018) and Fusai and Meuci (2008) who consider pricing and hedging in exponential Lévy and/or stochastic volatility models. While all four papers make important contributions to account for jump activity and stochastic changes in volatility, they do not consider stochastic convenience yield and hence their models fail to produce important features such as mean reversion in spot price and realistic term structures in forward and futures prices. Other recent results such as Cai et al. (2015), Fusai and Kyriakou (2016) and Novikov and Kordzakhia (2014) are in theory applicable to a more general modelling framework, but in practice applicability hinges on the complexity of the specific model discussed. Adaptation of the latter results to the case of the Schwartz (1997) two- and three-factor models create a number of difficulties. In fact we believe that the latter approaches would indeed be infeasible due to the corresponding issues of dimensionality and complexity. The work of Cai et. al. (2015) in fact only considers one dimensional models and while Novikov and Kordzakhia (2014) in principle allow for a multivariate distribution of the underlying, the optimization problems that lead to their price bounds could not be solved analytically. The work of Fusai and Kyriakou (2016) applies to affine stochastic volatility models, but not to models which feature additional stochastic factors that affect the drift term of the underlying. Further, all three papers indeed present price bounds rather than actual prices. Hence there is a natural discrepancy between these results and the true prices. Further, these price bounds can not always be computed explicitly and require themselves sophisticated numerical computation. Chen and Ewald (2017) have shown that price bounds, at least for the case of Albrecher et al's (2005) co-monotonicity approach, can sometimes diverge significantly from the true prices for complex models such as the Schwartz (1997) two- or three-factor model. Having said that, given that the geometric average is always smaller than the corresponding arithmetic average, it is worthwhile to mention that the closed form solution for the geometric average Asian option, which we derive, always presents a lower bound for the price of the corresponding arithmetic average Asian option.

Our results directly connect to the approach of Dockner et. al. (2015) and Hochradl and Rammerstorfer (2012) to approximate the convenience yield of a commodity as the difference between two suitably designed geometric Asian options. Their approach in turn is based on Heaney's (2002) and Longstaff's (1995) option based approach to uncover the convenience yield. While Hochradl and Rammerstorfer (2012) use a geometric Brownian motion as underlying, Dockner et al. (2015) include the element of mean-reversion by using a Cox-Ingersoll-Ross type of process. Both models are one dimensional. In contrast, our model is multi-dimensional and implements a stochastic convenience yield and the possibility of jumps. The application of our results to extend those of Dockner et. al. (2015) and Hochradl and Rammerstorfer (2012) is left for future research.


<!-- p:6 -->


The remainder of the paper is organized as follows. Section 2 introduces the Schwartz (1997) multi-factor models which we adopt in the first part of this paper. We derive closed form solutions for geometric average Asian options and demonstrate how these can effectively be used as control variates in order to price arithmetic average Asian options using Monte Carlo simulation. In Section 3, we investigate how sensitive Asian option prices are with regard to changes in the parameters of the model. We add jumps to the spot price dynamics in section 4 and extend our methodology to this case. Again, the effectiveness of the method is demonstrated with specific examples. We conclude the paper with a summary of our main results in Section 5.

### 2 The Model

We follow Schwartz (1997) to construct two-factor and three-factor models featuring stochastic convenience yield and interest rates. The ability of these models to produce realistic commodity term structures for forward and futures prices is well established.

#### 2.1 Two-Factor Model

In the two-factor model, the underlying spot price and instantaneous convenience yield are driven by the following two stochastic processes, namely,

$$d S _ { t } \ = \ ( \mu - \delta _ { t } ) S _ { t } d t + \sigma _ { 1 } S _ { t } d Z _ { 1 , t } \ ,$$

$$d \delta _ { t } \ = \ \kappa ( \alpha - \delta _ { t } ) d t + \sigma _ { 2 } d Z _ { 2 , t } \ ,$$

$$d Z _ { 1 , t } d Z _ { 2 , t } \ = \ \rho d t \ .$$

Equation (1) represents the stochastic process for the underlying spot price, where the drift term indicates a negative effect of the instantaneous convenience yield, δ , on its long-term growth rate, μ . This is consistent with the role that convenience yield plays in the theory of storage. The instantaneous convenience yield follows an Ornstein-Uhlenbeck stochastic process as shown in equation (2), which is in line with Gibson and Schwartz (1990). The coefficients κ and α denote the speed of adjustment and the long-term mean of the convenience yield, respectively, while σ 2 1 and σ 2 2 represent the variances of the underlying prices and the convenience yield. Both dZ 1 ,t and dZ 2 ,t are increments of standard Brownian motions, with ρ ∈ [ - 1 , 1] being the correlation coefficient.


<!-- p:7 -->


Within the two-factor model, we assume a constant interest rate, r . This assumption is relaxed in the three-factor model in section 2.3. It is worth noting that the convenience yield is not a tradable asset and therefore carries a market price of risk λ , which we assume to be constant. Under the pricing measure Q ∗ , i.e. the risk-neutral measure adopted by the market, the dynamics can be expressed as

$$d S _ { t } \ = \ ( r - \delta _ { t } ) S _ { t } d t + \sigma _ { 1 } S _ { t } d Z _ { 1 , t } ^ { * } \ ,$$

$$d \delta _ { t } \ = \ \kappa ( \hat { \alpha } - \delta _ { t } ) d t + \sigma _ { 2 } d Z _ { 2 , t } ^ { * } \ ,$$

$$d Z _ { 1 , t } ^ { * } d Z _ { 2 , t } ^ { * } \ = \ \rho d t \ ,$$

where ˆ α = α - λ κ .

The change in the drift term of the spot price process under the pricing measure is clearly visible, μ has been replaced by the risk-free rate, r . The effect of λ on the long term mean of the instantaneous convenience yield, α , has been absorbed through the risk-adjusted long term mean, ˆ α , taking the place of α .

By constructing a risk-less portfolio including two futures contracts with different maturities as well as a bond, Schwartz (1997) shows that the futures prices, F ( S, δ, τ ) , with time till maturity τ = T - t and given state variables S and δ , must follow the partial differential equation

$$\frac { 1 } { 2 } \sigma _ { 1 } ^ { 2 } S ^ { 2 } F _ { S S } + \sigma _ { 1 } \sigma _ { 2 } \rho S F _ { S \delta } + \frac { 1 } { 2 } \sigma _ { 2 } ^ { 2 } F _ { \delta \delta } + ( r - \delta ) S F _ { S } + ( \kappa ( \hat { \alpha } - \delta ) ) F _ { \delta } - F _ { \tau } = 0 \ ,$$

subject to the boundary condition F ( S, δ, 0) = S . The solution to the above equations is given as

$$F ( S , \delta , \tau ) = S \cdot \exp ( A ( \tau ) ) ,$$

where

$$A ( \tau ) = - \frac { \delta } { \kappa } ( 1 - e ^ { - \kappa \tau } ) + \left ( r - \hat { \alpha } + \frac { \sigma _ { 2 } ^ { 2 } } { 2 \kappa ^ { 2 } } - \frac { \sigma _ { 1 } \sigma _ { 2 } \rho } { \kappa } \right ) \tau \\ + \frac { \sigma _ { 2 } ^ { 2 } ( 1 - e ^ { - 2 \kappa \tau } ) } { 4 \kappa ^ { 3 } } + \left ( \hat { \alpha } \kappa + \sigma _ { 1 } \sigma _ { 2 } \rho - \frac { \sigma _ { 2 } ^ { 2 } } { \kappa } \right ) \frac { 1 - e ^ { - \kappa \tau } } { \kappa ^ { 2 } } \ .$$

This solution was derived independently by Jamshidian and Fein (1990) and Bjerksund (1991).


<!-- p:8 -->


##### 2.1.1 Closed Form Solution for the Continuously Sampled Case

We now turn to the pricing of Asian options written on futures contracts. It is well known that under most circumstances, arithmetic average Asian options do not admit closed-form solutions, because the arithmetic average of the log-normal underlying does not follow a log-normal distribution. The situation is different for geometric average Asian options, where the geometric average of a log-normal underlying remains log-normal. We conclude from equation (8) that the price of a futures contract follows a log-normal distribution, and so is the geometric average of the futures price. Hence, the derivation of a closed-form solution for a geometric average Asian option in the Schwartz (1997) two-factor model is feasible. In consequence, we can follow Kemna and Vorst's (1990) suggestion to price arithmetic average Asian options using Monte Carlo simulation, with the closed form solution for the geometric average Asian option acting as a control variate for variance reduction purposes. The simulation however requires a discretization, which produces a small bias. On the other hand, Asian options in reality are always discretely sampled. Applying solution methods that are tailored to the case of continuously sampled Asian option therefore create a systematic bias, and this bias can sometimes be large. We can avoid this problem by using the analogue formula for discretely sampled geometric Asian options, which is derived in the next subsection. In either way, the method is extremely effective, as the functional similarity of the two types of Asian options guarantees a high covariance between their payoffs and thus significantly reduces the variance of the simulated price.

Accordingly, we are looking for a closed form solution for the price of a geometric average Asian option written on a futures contracts, under the assumptions of the two-factor Schwartz (1997) model, equations (1) and (2). The price of the geometric average Asian option with maturity T written on a futures contracts with maturity time ˆ T at time t can be represented as follows

$$G A ( t , T , \hat { T } ) = e ^ { - r ( T - t ) } \mathbb { E } _ { t } ^ { * } \left [ \max ( G ( t , T , \hat { T } ) - K , 0 ) \right ] \ ,$$

where

$$G ( t , T , \hat { T } ) = \exp \left ( \frac { 1 } { T } \int _ { 0 } ^ { T } \ln F ( S _ { u } , \delta _ { u } , \hat { T } - u ) \ d u \right ) \ ,$$

where E ∗ t denotes the conditional expectation under Q ∗ with respect to the information available at t . It is assumed that 0 ≤ t ≤ T ≤ ˆ T , which means that the underlying futures contract cannot expire before the Asian option does. The variable t in equation (10) is redundant in the way that the expression on the right hand side does not explicitly depend on t . However in order to understand the dynamics of the option price it is useful to separate the underlying into what is known at time t and what is still unknown. Under the assumption that t &gt; 0 , equation (10) can be decomposed into two parts,


<!-- p:9 -->


$$G ( t , T , \hat { T } ) = & \exp \left \{ \frac { 1 } { T } \left [ \int _ { 0 } ^ { t } \ln F ( S _ { u } , \delta _ { u } , \hat { T } - u ) \ d u \\ & + \int _ { t } ^ { T } \ln F ( S _ { v } , \delta _ { v } , \hat { T } - v ) \ d v \right ] \right \} \, . \ \ ( 1 1 ) \\ \intertext { W h e n p r i cing the o t i n t a t i m e t s }$$

When pricing the option at time t , the first part will essentially be an adjustment to the strike price, K , and the discount factor in equation (9) will change its value correspondingly, whereas the main problem remains in computing the conditional expectation of the second part of equation (11), which is equivalent to the problem of computing the option price at time t = 0 . For notational simplicity, we therefore assume that the current time, t , coincides with the starting point of the Asian option, i.e. t = 0 , as the extension to any t &gt; 0 is fairly straightforward.

Given that futures prices in our model are log-normal and the interest rate is fixed, applying the methodology of Kemna and Vorst (1990) to equation (9) leads to

$$G A ( 0 , T , \hat { T } ) = e ^ { - r T } \left [ e ^ { E + \frac { 1 } { 2 } V } \mathcal { N } \left ( \frac { E - \ln ( K ) + V } { \sqrt { V } } \right ) - K \mathcal { N } \left ( \frac { E - \ln ( K ) } { \sqrt { V } } \right ) \right ] , \\ \\ F _ { \ } E = e ^ { - r T } \left [ e ^ { E + \frac { 1 } { 2 } V } \mathcal { N } \left ( \frac { E - \ln ( K ) + V } { \sqrt { V } } \right ) - K \mathcal { N } \left ( \frac { E - \ln ( K ) } { \sqrt { V } } \right ) \right ] ,$$

where E and V denote the expectation and variance of the average from equation (11), and N represents the cumulative distribution function of the standard normal distribution. 1 The expressions for E and V are given below with the sub-index indicating the model that these expressions relate to. We will later also derive the corresponding expressions for the three-factor model.

$$\text {will later also derive the corresponding expressions for the three-factor model.} \\ E _ { 2 - f a c t o r } = \ln ( S _ { 0 } ) - \frac { \delta _ { 0 } } { \kappa } + \frac { 1 } { 2 } \left ( r - \frac { \sigma _ { 1 } ^ { 2 } } { 2 } - \hat { \alpha } \right ) T + \left ( \delta _ { 0 } T - \hat { \alpha } T - \frac { \hat { \alpha } } { \kappa } \right ) \frac { e ^ { - \kappa \hat { T } } } { \kappa T } \\ + \hat { \alpha } \frac { e ^ { - \kappa ( \hat { T } - T ) } } { \kappa ^ { 2 } T } + \left ( r - \hat { \alpha } + \frac { \sigma _ { 2 } ^ { 2 } } { 2 \kappa ^ { 2 } } - \frac { \sigma _ { 1 } \sigma _ { 2 } \rho } { \kappa } \right ) \left ( \hat { T } - \frac { T } { 2 } \right ) \\ + \frac { \sigma _ { 2 } ^ { 2 } } { 4 \kappa ^ { 3 } T } \left ( T - \frac { e ^ { - 2 \kappa ( T - T ) } - e ^ { - 2 \kappa T } } { 2 \kappa } \right ) \\ + \frac { \hat { \alpha } \kappa + \sigma _ { 1 } \sigma _ { 2 } \rho - \frac { \sigma _ { 2 } ^ { 2 } } { \kappa } } { \kappa ^ { 2 } T } \left ( T - \frac { e ^ { - \kappa ( \hat { T } - T ) } - e ^ { - \kappa \hat { T } } } { \kappa } \right ) \, , \\ \frac { 1 } { \L } \text {Note that the variance of the average is strictly positive and hence the expression in}$$

1 Note that the variance of the average is strictly positive and hence the expression in equation (12) is well defined. This expression is in adaptation of the classical Black and Scholes formula. It can in principle be derived for any log-normal underlying.


<!-- p:10 -->


$$V _ { 2 - f a c l o r } = \frac { 1 } { T ^ { 2 } } \left ( \frac { 1 } { 3 } \sigma _ { 1 } ^ { 2 } T ^ { 3 } + \frac { \sigma _ { 2 } ^ { 2 } } { \kappa ^ { 2 } } \left ( \frac { 1 } { 4 \kappa ^ { 3 } } e ^ { - 2 \kappa ( \tilde { T } - T ) } - \frac { 4 } { \kappa ^ { 3 } } e ^ { - \kappa ( \tilde { T } - T ) } \\ - \left ( \frac { T ^ { 2 } } { 2 \kappa } + \frac { T } { 2 \kappa ^ { 2 } } + \frac { 1 } { 4 \kappa ^ { 3 } } \right ) e ^ { - 2 \kappa \tilde { T } } + \left ( 2 \frac { T ^ { 2 } } { \kappa } + 4 \frac { T } { \kappa ^ { 2 } } + \frac { 4 } { \kappa ^ { 3 } } \right ) e ^ { - \kappa \tilde { T } } + \frac { T ^ { 3 } } { 3 } \right ) \\ + \frac { 2 \sigma _ { 1 } \sigma _ { 2 } \rho _ { 1 } } { \kappa } \left ( \frac { 2 } { \kappa ^ { 3 } } e ^ { - \kappa ( \hat { T } - T ) } - \left ( \frac { T ^ { 2 } } { \kappa } + \frac { 2 T } { \kappa ^ { 2 } } + \frac { 2 } { \kappa ^ { 3 } } \right ) e ^ { - \kappa \hat { T } } - \frac { T ^ { 3 } } { 3 } \right ) \right ) \, , \\ \quad \\ \text {where } S _ { 0 } \text { and } \delta _ { 0 } \text { denote the spot price and the instantaneous convenience}$$

where S 0 and δ 0 denote the spot price and the instantaneous convenience yield at the start of the Asian option, i.e. when t = 0 . 23

##### 2.1.2 Closed Form Solution for the Discretely Sampled Case

As indicated above, we also present a closed form solution for a geometric Asian option in the Schwartz (1997) model for the case when the averaging occurs over discretely sampled values of the underlying. This case is indeed much closer to the real world and also necessary when using the result as a control variate in order to avoid discretization bias.

We adjust the previous notation slightly in order to take account of the discretized sampling. To be more specific, the current time will be marked as t 0 , the maturity time of the future contract as ˆ T , and the maturity time of the Asian option as t N , where N indicates the total number of samples taken over the option's lifetime. It is assumed that t 0 ≤ t N ≤ ˆ T , in other words the underlying future contract cannot expire before the Asian option does. As a result, the price of the geometric average Asian option with maturity time t N written on a future contract with maturity time ˆ T at time t 0 under the risk-neutral measure can be represented similar as before by the following equation

$$G A ( t _ { 0 } , t _ { N } , \hat { T } ) = e ^ { - r ( t _ { N } - t _ { 0 } ) } \mathbb { E } ^ { * } \left [ \max ( G ( t _ { 0 } , t _ { N } , \hat { T } ) - K , 0 ) \right ] \, ,$$

where

$$G ( t _ { 0 } , t _ { N } , \hat { T } ) = \exp \left ( \frac { 1 } { N + 1 } \sum _ { i = 0 } ^ { N } \ln F ( S ( t _ { i } ) , \delta ( t _ { i } ) , \hat { T } - t _ { i } ) \right ) \, .$$

2 The derivation of the expectation and variance term follows basic principles of computations with normal and log-normal random variables. However it is tedious and lengthy and is therefore omitted. Nevertheless, the computations are compiled in an online appendix which is available from the authors on request.

3 For κ → 0 the expression for V 2 - factor in equation (14) converges to 1 30 T ( 10 σ 2 1 + σ 2 2 ( T 2 - 5 ˆ TT +10 ˆ T 2 ) +5 ρσ 2 σ 1 ( T - 4 ˆ T )) .


<!-- p:11 -->


As in the continuously sampled case, we have

$$G A ( t _ { 0 } , t _ { N } , \hat { T } ) & = e ^ { - r ( t _ { N } - t _ { 0 } ) } \left [ e ^ { E + \frac { 1 } { 2 } V } \mathcal { N } \left ( \frac { E - \ln ( K ) + V } { \sqrt { V } } \right ) - K \mathcal { N } \left ( \frac { E - \ln ( K ) } { \sqrt { V } } \right ) \right ] , \\ \\ \intertext { g A ( t _ { 0 } , t _ { N } , \hat { T } ) = e ^ { - r ( t _ { N } - t _ { 0 } ) } \left [ e ^ { E + \frac { 1 } { 2 } V } \mathcal { N } \left ( \frac { E - \ln ( K ) + V } { \sqrt { V } } \right ) - K \mathcal { N } \left ( \frac { E - \ln ( K ) } { \sqrt { V } } \right ) \right ] , } \\$$

where E and V denote the expectation and variance of the average in equation (16), and N represents the standard normal distribution function. The corresponding expressions for E and V are now determined through

$$\text { corresponding expressions for } E \text { and } V \text { are now determined through } \\ E _ { 2 } - & \text { factor} = \ln S ( t _ { 0 } ) + \left ( \frac { \hat { \alpha } - \delta _ { 0 } } { \kappa } \right ) \, \left ( 1 - e ^ { - \kappa \hat { T } } \right ) - \frac { 3 \sigma _ { 2 } ^ { 2 } } { 4 \kappa ^ { 3 } } \\ & + \left ( r - \hat { \alpha } + \frac { \sigma _ { 2 } ^ { 2 } } { 2 \kappa ^ { 2 } } \right ) \, \hat { T } + \sigma _ { 1 } \sigma _ { 2 } \rho \, \left ( \frac { 1 - \kappa \hat { T } } { \kappa ^ { 2 } } \right ) \\ & + \frac { 1 } { N + 1 } \, \left [ - \left ( \frac { 1 } { 2 } \sigma _ { 1 } ^ { 2 } + \frac { \sigma _ { 2 } ^ { 2 } } { 2 \kappa ^ { 2 } } - \frac { \sigma _ { 1 } \sigma _ { 2 } \rho } { \kappa } \right ) \frac { ( t _ { 0 } + t _ { N } ) ( N + 1 ) } { 2 } \right ] \\ & + \frac { \frac { \sigma _ { 2 } ^ { 2 } } { \kappa } - \sigma _ { 1 } \sigma _ { 2 } \rho } { \kappa ^ { 2 } } \, \frac { e ^ { - \kappa ( \hat { \Gamma } - t _ { 0 } ) ( 1 - e ^ { \kappa \Delta t ( N + 1 ) } ) } } { 1 - e ^ { \kappa \Delta t } } \\ & - \frac { \sigma _ { 2 } ^ { 2 } } { 4 \kappa ^ { 3 } } \, \frac { e ^ { - 2 \kappa ( \hat { T } - t _ { 0 } ) ( 1 - e ^ { 2 \kappa \Delta t ( N + 1 ) } ) } } { 1 - e ^ { 2 \kappa \Delta t } } \right ] \, ,$$

$$V _ { 2 - } & \text {factor} = \frac { 1 } { ( N + 1 ) ^ { 2 } } \ \left \{ \sigma _ { 1 } ^ { 2 } \ \sum _ { i = 1 } ^ { N } ( N - i + 1 ) ^ { 2 } \ \Delta t \\ & \quad + \frac { 2 \sigma _ { 1 } \sigma _ { 2 } \rho } { \kappa } \ \sum _ { i = 1 } ^ { N } ( N - i + 1 ) ^ { 2 } \ \left [ \frac { e ^ { - \kappa \hat { T } } } { \kappa } \left ( e ^ { \kappa t _ { i } } - e ^ { \kappa t _ { i - 1 } } \right ) - \Delta t \right ] \\ & \quad + \frac { \sigma _ { 2 } ^ { 2 } } { \kappa ^ { 2 } } \ \sum _ { i = 1 } ^ { N } ( N - i + 1 ) ^ { 2 } \ \left [ \frac { e ^ { - 2 \kappa T } } { 2 \kappa } \left ( e ^ { 2 \kappa t _ { i } } - e ^ { 2 \kappa t _ { i - 1 } } \right ) \\ & \quad - \frac { 2 e ^ { - \kappa \hat { T } } } { \kappa } \ \left ( e ^ { \kappa t _ { i } } - e ^ { \kappa t _ { i - 1 } } \right ) + \Delta t \right ] \right \} \ , \\ \intertext { w h e r $ \Delta t = t _ { i } - t _ { i - 1 } \, . $ }$$

where ∆ t = t i - t i - 1 .

#### 2.2 Performance of the Control Variate

As indicated previously, the closed form solution for the discretely sampled geometric average Asian option will provide us with a control variate to help


<!-- p:12 -->


Table 1 Comparison of Monte Carlo Simulation Results ∗ (Two-Factor Model)

|     |      |   Standard |            | Antithetic Control Variate   |          |            |
|-----|------|------------|------------|------------------------------|----------|------------|
| α   | 0.05 |   4.110549 | (0.033477) | 4.128904 (0.013402)          | 4.116849 | (0.001369) |
|     | 0.08 |   2.914107 | (0.028617) | 2.929277 (0.014071)          | 2.923942 | (0.001322) |
|     | 0.11 |   1.969123 | (0.023647) | 1.981864 (0.013493)          | 1.980276 | (0.001274) |
|     | 0.14 |   1.265132 | (0.018844) | 1.274750 (0.011713)          | 1.273519 | (0.001215) |
| κ   |    1 |   3.892199 | (0.033824) | 3.909979 (0.014647)          | 3.885797 | (0.001419) |
|     |  1.4 |   2.775324 | (0.027609) | 2.792632 (0.013756)          | 2.767709 | (0.001257) |
|     |  1.8 |   2.269386 | (0.025421) | 2.288177 (0.013929)          | 2.267750 | (0.001301) |
|     |  2.2 |   2.032357 | (0.024848) | 2.051099 (0.014323)          | 2.038149 | (0.001418) |
| σ 1 |  0.1 |   4.582455 | (0.029467) | 4.558615 (0.008343)          | 4.551479 | (0.000765) |
|     |  0.4 |   2.278707 | (0.025392) | 2.280277 (0.013890)          | 2.268571 | (0.001311) |
|     |  0.7 |   2.872786 | (0.045544) | 2.877244 (0.028680)          | 2.849718 | (0.006124) |
|     |    1 |   3.724552 | (0.072571) | 3.723735 (0.047413)          | 3.693217 | (0.016387) |

∗ The basic setting is as follows, unless indicated otherwise: S 0 = 40 , K = 40 , δ 0 = 0 . 2 ,

κ = 1 . 8 , α = 0 . 1 , λ 1 = 0 . 3 , ρ = 0 . 8 , σ 1 = 0 . 4 , σ 2 = 0 . 5 . The interest rate is fixed at 5%.

20,000 paths are simulated. Standard deviations are in brackets.

reduce the error in the appropriate Monte Carlo simulation, when pricing an arithmetic average Asian option. To demonstrate its effectiveness, we compare the results for pricing an arithmetic average Asian option by standard Monte Carlo simulation without any variance reduction method, with variance reduction achieved through using antithetic variates, and with variance reduction using our newly derived control variate.

The results from the three Monte Carlo approaches are shown in Table 1, where parameters are given with different values as indicated in the first two columns. Columns 3 to 5 present option prices and the standard deviation incurred within the simulation (listed in the brackets) using different Monte Carlo methods. It is apparent to see that the control variate method consistently yields much smaller standard deviations. Given 20,000 simulations in our experiment, for an Asian option contract worth around $1 to $4, the standard errors incurred by standard Monte Carlo simulation could be as large as 2 to 7 cents, or 1% - 2% to the price. In the case of the antithetic variate method, they tend to shrink to as low as 0 . 2% - 1% . However, using our control variate, the standard errors are usually around 0.1 to 1.6 cents, or 0 . 01% - 0 . 4% . On average, the standard errors obtained within the simulations when using our control variate are more than 7 times smaller than those obtained from the standard Monte Carlo simulation, and 8 times smaller than those obtained from the antithetic variate method.


<!-- p:13 -->


#### 2.3 Three-Factor Model

The assumption of constant interest rates is relaxed in the three-factor model, where we adopt an Ornstein-Uhlenbeck process to model the instantaneous interest rate. This is inspired by Vasicek (1977), where the mean-reverting feature of the interest rate was first captured in a continuous time model. Under the risk-neutral measure, Q ∗ , the stochastic processes for the underlying spot price, the instantaneous convenience yield and the instantaneous interest rate can then be represented as follows,

$$d S _ { t } \ = \ ( r - \delta _ { t } ) S _ { t } d t + \sigma _ { 1 } S _ { t } d Z _ { 1 , t } ^ { * } \ ,$$

$$d \delta _ { t } \ = \ \kappa ( \hat { \alpha } - \delta _ { t } ) d t + \sigma _ { 2 } d Z _ { 2 , t } ^ { * } \ ,$$

$$d r _ { t } \ = \ a ( \hat { m } - r _ { t } ) d t + \sigma _ { 3 } d Z _ { 3 , t } ^ { * } \ ,$$

$$d Z _ { 1 , t } ^ { * } d Z _ { 2 , t } ^ { * } = \rho _ { 1 } d t \ , \quad d Z _ { 2 , t } ^ { * } d Z _ { 3 , t } ^ { * } = \rho _ { 2 } d t \ , \quad d Z _ { 1 , t } ^ { * } d Z _ { 3 , t } ^ { * } = \rho _ { 3 } d t \ ,$$

where ˆ α = α - λ 1 κ and ˆ m = m - λ 2 a .

Here, a and ˆ m denote the speed of adjustment and the risk-adjusted long term mean of the interest rate, respectively. The parameters λ 1 and λ 2 represent the market price of convenience yield risk and interest rate risk. The three-factor model can account for short term fluctuations in the spot interest rate. This is of particular interest when certain commodities are empirically linked to or heavily influenced by monetary policy change, see Frankel (2006).

Schwartz (1997) shows that futures prices under the three-factor model, F ( S, δ, r, τ ) , must satisfy the following partial differential equation,

$$\frac { 1 } { 2 } \sigma _ { 1 } ^ { 2 } S ^ { 2 } F _ { S S } + \frac { 1 } { 2 } \sigma _ { 2 } ^ { 2 } F _ { \delta \delta } + \frac { 1 } { 2 } \sigma _ { 3 } ^ { 2 } F _ { r r } + \sigma _ { 1 } \sigma _ { 2 } \rho _ { 1 } S F _ { S \delta } + \sigma _ { 2 } \sigma _ { 3 } \rho _ { 2 } F _ { \delta r } + \sigma _ { 1 } \sigma _ { 3 } \rho _ { 3 } S F _ { S r } \\ + ( r - \delta ) S F _ { S } + \kappa ( \hat { \alpha } - \delta ) F _ { \delta } + a ( \hat { m } - r ) F _ { r } - F _ { \tau } = 0 \ ,$$

subject to the boundary condition F ( S, δ, r, 0) = S . The solution to the above equation can be identified in the form

$$F ( S , \delta , r , \tau ) = S \exp ( A ( \tau ) + B ( \tau ) + C ( \tau ) ) \ ,$$


<!-- p:14 -->


where,

$$where , \\ A ( \tau ) = \, - \, \frac { \delta ( 1 - e ^ { - \kappa \tau } ) } { \kappa } , \\ B ( \tau ) = \frac { r ( 1 - e ^ { - a \tau } ) } { a } , \\ C ( \tau ) = \frac { ( \kappa \hat { \alpha } + \sigma _ { 1 } \sigma _ { 2 } \rho _ { 1 } ) ( ( 1 - e ^ { - \kappa \tau } ) - \kappa \tau ) } { \kappa ^ { 2 } } \\ - \, \frac { \sigma _ { 2 } ^ { 2 } ( 4 ( 1 - e ^ { - \kappa \tau } ) - ( 1 - e ^ { - 2 \kappa \tau } ) - 2 \kappa \tau ) } { 4 \kappa ^ { 3 } } \\ - \, \frac { ( a \hat { m } + \sigma _ { 2 } \sigma _ { 3 } \rho _ { 3 } ) ( ( 1 - e ^ { - a \tau } ) - a \tau ) - a \tau } { a ^ { 2 } } \\ - \, \frac { \sigma _ { 3 } ^ { 2 } ( 4 ( 1 - e ^ { - a \tau } ) - ( 1 - e ^ { - 2 a \tau } ) - 2 a \tau ) } { 4 \kappa ^ { 3 } } \\ + \sigma _ { 2 } \sigma _ { 3 } \rho _ { 2 } \left ( \frac { ( 1 - e ^ { - \kappa \tau } ) + ( 1 - e ^ { - a \tau } ) - ( 1 - e ^ { - ( \kappa + a ) \tau } ) } { \kappa ^ { a } a ^ { ( \kappa + a ) } } \right ) \\ + \frac { \kappa ^ { 2 } ( 1 - e ^ { - a \tau } ) + a ^ { 2 } ( 1 - e ^ { - \kappa \tau } ) - \kappa a ^ { 2 } \tau - a \kappa ^ { 2 } \tau } { \kappa ^ { a ^ { 2 } } ( \kappa + a ) } \right ) \, . \\ \intertext { t h e r $ p o r $ of a (continuously sampled ) geometric average $ A $ian option } \, at t i m t $ w h a t u r i g $ T $ w i t e n $ o a f u tures $ c o r t $ w i t h u r i t $ \hat { T } $ i s$$

The price of a (continuously sampled) geometric average Asian option at time t with maturity T written on a futures contract with maturity ˆ T is given by the following equation,

$$G A ( t , T , \hat { T } ) = \mathbb { E } _ { t } ^ { * } \, \left [ e ^ { - r ( T - t ) } \max ( G ( t , T , \hat { T } ) - K , 0 ) \right ] ,$$

where

$$G ( t , T , \hat { T } ) = \exp \left ( \frac { 1 } { T } \int _ { 0 } ^ { T } \ln F ( S _ { u } , \delta _ { u } , r _ { u } , \hat { T } - u ) \ d u \right ) \ . \\$$

In order to price options under stochastic interest rates, a technique using the so called forward measure has been developed, see for example Bjoerk (2004). This method effectively deals with the problem of correlation between the underlying and the discount factor, when taking expectations to price the option. We denote the T -forward measure by Q T . This measure represents a martingale measure when using a zero-coupon bond with maturity T as the numeraire (the process of the transformation is provided in Appendix A.1). Applied to the Asian option case, the price of the geometric average Asian option in the three-factor model can then be computed via

$$G A ( 0 , T , \hat { T } ) & = P ( 0 , T ) \mathbb { E } ^ { \mathbb { T } } \max ( G ( 0 , T , \hat { T } ) - K , 0 ) \\ & = P ( 0 , T ) \left [ e ^ { E + \frac { 1 } { 2 } V } \mathcal { N } \left ( \frac { E - \ln ( K ) + V } { \sqrt { V } } \right ) - K \mathcal { N } \left ( \frac { E - \ln ( K ) } { \sqrt { V } } \right ) \right ] \, ,$$


<!-- p:15 -->


where P (0 , T ) , the price of the zero-coupon bond with maturity T at time t = 0 , is given as follows:

$$P ( 0 , T ) = A ( 0 , T ) e ^ { - r _ { 0 } B ( 0 , T ) } \ ,$$

with

$$B ( 0 , T ) & = \frac { 1 - e ^ { - a T } } { a } \\ A ( 0 , T ) & = \exp \left [ \left ( \hat { m } - \frac { \sigma _ { 3 } ^ { 2 } } { 2 a ^ { 2 } } \right ) ( B ( 0 , T ) - T ) - \frac { \sigma _ { 3 } ^ { 2 } } { 4 a } B ^ { 2 } ( 0 , T ) \right ] ,$$

and the expectation, E , and variance, V , in equation (28), are respectively

$$and the expectation, E , \, \text { and variance, } V , \, \text { in equation (28)} , \, \text { are respectively} \\ E _ { 3 - } \text { factor} = \frac { 1 } { T } \left \{ \left [ \ln ( S _ { 0 } ) + \frac { \ r _ { 0 } } { a } \right ] T - \frac { 1 } { 2 } \left ( \frac { 1 } { 2 } \sigma _ { 1 } ^ { 2 } - \hat { m } + \hat { \alpha } \right ) T ^ { 2 } \\ + \frac { \delta _ { 0 } - \hat { \alpha } } { \kappa } T e ^ { - \kappa \hat { T } } + \frac { \hat { \alpha } } { \kappa ^ { 2 } } e ^ { - \kappa \hat { T } } ( e ^ { T } - 1 ) - \frac { \ r _ { 0 } - \hat { m } } { a } T e ^ { - a \hat { T } } - \frac { \hat { m } } { a ^ { 2 } } e ^ { - a \hat { T } } e - 1 ) \\ + \frac { \kappa \hat { \alpha } + \sigma _ { 1 } \sigma _ { 2 } \rho _ { 1 } } { \kappa ^ { 2 } } \left ( l _ { 1 } - \kappa T \hat { T } + \frac { 1 } { 2 } \kappa T ^ { 2 } \right ) - \frac { \sigma _ { 2 } ^ { 2 } } { 4 k ^ { 3 } } ( 4 l _ { 1 } - l _ { 3 } - 2 \kappa T \hat { T } + \kappa T ^ { 2 } ) \\ - \frac { a \hat { m } + \sigma _ { 1 } \sigma _ { 3 } \rho _ { 3 } } { a ^ { 2 } } \left ( l _ { 2 } - a T \hat { T } + \frac { 1 } { 2 } a T ^ { 2 } \right ) - \frac { \sigma _ { 3 } ^ { 2 } } { 4 a ^ { 3 } } ( 4 l _ { 2 } - l _ { 4 } - 2 a T \hat { T } + a T ^ { 2 } ) \\ + \frac { \sigma _ { 2 } \sigma _ { 3 } \rho _ { 2 } } { \kappa ( a + a ) } ( l _ { 1 } + l _ { 2 } - l _ { 5 } ) + \frac { \sigma _ { 2 } \sigma _ { 3 } \rho _ { 2 } } { \kappa ^ { 2 } a ^ { 2 } ( \kappa + a ) } \left [ \kappa ^ { 2 } l _ { 2 } + a ^ { 2 } l _ { 1 } - a \kappa T \left ( \hat { T } - \frac { 1 } { 2 } T \right ) ( a + \kappa ) \right ] \\ - \frac { \sigma _ { 1 } \sigma _ { 3 } \gamma _ { 1 } } { a } \left [ \frac { T ^ { 2 } } { 2 } - \frac { 1 } { a ^ { 2 } } + ( \frac { T } { a } + \frac { 1 } { a ^ { 2 } } ) e ^ { - a T } \right ] - \frac { \sigma _ { 2 } \sigma _ { 3 } \gamma _ { 2 } } { \kappa a } \left [ e ^ { - \kappa T } \left ( - \frac { T } { \kappa } + \frac { e ^ { \kappa T } } { \kappa ^ { 2 } } \right ) \right ] \\ - e ^ { - \kappa T } \hat { T } - \left ( - \frac { T } { \kappa } + \frac { e ^ { \kappa T } + T - 1 } { ( \kappa + a ) ^ { 2 } } \right ) - \frac { T ^ { 2 } } { 2 } + \frac { 1 } { a ^ { 2 } } - \frac { T } { a } e ^ { - a T } \right ] \\ + \frac { \sigma _ { 2 } ^ { \gamma _ { 3 } } } { a ^ { 3 } } \left [ e ^ { - a \hat { T } } \left ( - \frac { T } { a } + \frac { e ^ { T } - 1 } { a ^ { 2 } } \right ) - e ^ { - a ^ { ( \hat { T } + T ) } } \left ( - \frac { T } { 2 a } + \frac { e ^ { 2 T } - 1 } { 4 a ^ { 2 } } \right ) \\ - \frac { T ^ { 2 } } { 2 } + \frac { 1 } { a ^ { 2 } } - \frac { T } { a } e ^ { - a T } - \frac { e ^ { - a T } } { a ^ { 2 } } \right ] \right ] \, , \\ \text {where} \\ \quad l _ { 2 } - \frac { e ^ { - \kappa T } } { T } ( e ^ { \kappa T } - 1 ) \, \quad l _ { 1 } - T = \frac { e ^ { - a T } } { 2 } ( e ^ { a T } - 1 ) \, \quad l _ { 2 } = T - \frac { e ^ { - 2 \kappa T } } { a ^ { 2 } T } ( e ^ { 2 \kappa T } - 1 )$$

where

$$l _ { 1 } & = T - \frac { e ^ { - \kappa \hat { T } } } { \kappa } ( e ^ { \kappa T } - 1 ) , \quad l _ { 2 } = T - \frac { e ^ { - \alpha \hat { T } } } { a } ( e ^ { a T } - 1 ) , \quad l _ { 3 } = T - \frac { e ^ { - 2 \kappa \hat { T } } } { 2 \kappa } ( e ^ { 2 \kappa T } - 1 ) , \\ l _ { 4 } & = T - \frac { e ^ { - 2 \alpha \hat { T } } } { 2 a } ( e ^ { 2 a T } - 1 ) , \quad l _ { 5 } = T - \frac { e ^ { - ( \kappa + a ) \hat { T } } } { ( \kappa + a ) } ( e ^ { ( \kappa + a ) T } - 1 ) \ ,$$


<!-- p:16 -->


and

$$\text {and} \\ V _ { 3 - f \text {actor} } = \frac { 1 } { T ^ { 2 } } \left \{ \frac { 1 } { 3 } T ^ { 3 } \sigma _ { 1 } ( \alpha _ { 1 } ^ { 2 } + \beta _ { 1 } ^ { 2 } + \gamma _ { 1 } ^ { 2 } ) \\ + \frac { \sigma _ { 2 } ^ { 2 } ( \beta _ { 2 } ^ { 2 } + \gamma _ { 2 } ^ { 2 } ) } { \kappa ^ { 2 } } \left ( \frac { T ^ { 3 } } { 3 } + \frac { 1 } { 4 \kappa ^ { 3 } } e ^ { - 2 \kappa ( \hat { T } - T ) } - \frac { 4 } { \kappa ^ { 3 } } e ^ { - \kappa ( \hat { T } - T ) } - m _ { 1 } + m _ { 2 } \right ) \\ + \frac { \sigma _ { 3 } ^ { 2 } \gamma _ { 2 } ^ { 2 } } { a ^ { 3 } } \left ( \frac { T ^ { 3 } } { 3 } + \frac { 1 } { 4 a ^ { 3 } } e ^ { - 2 a ( \hat { T } - T ) } - \frac { 4 } { a ^ { 3 } } e ^ { - a ( \hat { T } - T ) } - m _ { 3 } + m _ { 4 } \right ) \\ + \frac { 2 \sigma _ { 1 } \sigma _ { 2 } ( \beta _ { 1 } \beta _ { 2 } + \gamma _ { 1 } \gamma _ { 2 } ) } { \kappa } \left ( \frac { 2 } { \kappa ^ { 3 } } e ^ { - \kappa ^ { ( \hat { T } - T ) } } - \frac { 1 } { 2 } m _ { 2 } - \frac { T ^ { 3 } } { 3 } \right ) \\ - \frac { 2 \sigma _ { 1 } \sigma _ { 3 } \gamma _ { 1 } \gamma _ { 3 } } { a } \left ( \frac { 2 } { a ^ { 3 } } e ^ { - a ( \hat { T } - T ) } - \frac { 1 } { 2 } m _ { 4 } - \frac { T ^ { 3 } } { 3 } \right ) \\ - \frac { 2 \sigma _ { 2 } \sigma _ { 3 } \gamma _ { 2 } \gamma _ { 3 } } { \kappa a } \left [ \left ( \frac { 2 } { ( \kappa + a ) ^ { 3 } } e ^ { - ( \kappa + a ) ( \hat { T } - T ) } - m _ { 5 } - \frac { T ^ { 3 } } { 3 } \right ) \\ - \left ( \frac { 2 } { \kappa ^ { 3 } } e ^ { - \kappa ^ { ( \hat { T } - T ) } } - \frac { 1 } { 2 } m _ { 2 } - \frac { T ^ { 3 } } { 3 } \right ) - \left ( \frac { 2 } { a ^ { 3 } } e ^ { - a ( \hat { T } - T ) } - \frac { 1 } { 2 } m _ { 4 } - \frac { T ^ { 3 } } { 3 } \right ) \right ] \right \} \, , \\ \text {where} \\ m _ { 2 } - \frac { 1 } { \kappa } \left ( T ^ { 2 } + \frac { T } { T } + \frac { 1 } { 2 } \right ) e ^ { - 2 \kappa \hat { T } } \, \cdot \, m _ { 3 } - \frac { 2 } { 2 } \left ( T ^ { 2 } + \frac { 2 T } { 2 } + \frac { 2 } { 2 } \right ) e ^ { - \kappa \hat { T } }$$

where

$$\text {where} \\ m _ { 1 } = \frac { 1 } { 2 \kappa } \left ( T ^ { 2 } + \frac { T } { \kappa } + \frac { 1 } { 2 \kappa ^ { 2 } } \right ) e ^ { - 2 \kappa \hat { T } } , \quad m _ { 2 } = \frac { 2 } { \kappa } \left ( T ^ { 2 } + \frac { 2 T } { \kappa } + \frac { 2 } { \kappa ^ { 2 } } \right ) e ^ { - \kappa \hat { T } } , \\ m _ { 3 } = \frac { 1 } { 2 a } \left ( T ^ { 2 } + \frac { T } { a } + \frac { 1 } { 2 a ^ { 2 } } \right ) e ^ { - 2 a \hat { T } } , \quad m _ { 4 } = \frac { 2 } { a } \left ( T ^ { 2 } + \frac { 2 T } { a } + \frac { 2 } { a ^ { 2 } } \right ) e ^ { - a \hat { T } } , \\ m _ { 5 } = \frac { 1 } { \kappa + a } \left ( T ^ { 2 } + \frac { 2 T } { \kappa + a } + \frac { 2 } { ( \kappa + a ) ^ { 2 } } \right ) e ^ { - ( \kappa + a ) \hat { T } } \, . \\ \text {The analog formula for a discretely sampled geometrician option}$$

The analogue formula for a discretely sampled geometric Asian option in the Schwartz (1997) three factor model is presented in Appendix A.2. In analogy with the two-factor model, we use this closed-form solution as a control variate to price the corresponding arithmetic average Asian option. Table 2 shows a comparison of the results from the standard Monte Carlo simulation without variance reduction, the antithetic variates method and the control variate method. The results resemble those observed for the two-factor model: the control variate technique gives the most accurate performance, followed by the antithetic variate method. Most of the option prices lie in the range of $2 to $4. The standard deviations from standard Monte Carlo, antithetic variate method and control variate method are in the order of 2 . 5 cents, 1 . 5 cents and 0 . 1 cents, or in relative terms 1% , 0 . 5% and 0 . 05% of the price. On average, the control variate method leads to standard errors being about 18 times smaller than the standard errors produced by Monte Carlo method without variance reduction, and 10 times smaller than those produced when using the antithetic variate method instead.


<!-- p:17 -->


Table 2 Comparison of Monte Carlo Simulation Results ∗ (Three-Factor Model)

|     |              | Standard            | Antithetic          | Control Variate     |
|-----|--------------|---------------------|---------------------|---------------------|
| a   | 0.6 1.985803 | (0.023735) 1.992815 | (0.013454)          | 2.000054 (0.001268) |
| a   | 1.2          | 2.053695 (0.024133) | 2.060524 (0.013546) | 2.066573 (0.001272) |
| a   | 2            | 2.108031 (0.024444) | 2.114748 (0.013612) | 2.120103 (0.001275) |
| a   | 3            | 2.146772 (0.024662) | 2.153468 (0.013653) | 2.158484 (0.001277) |
| λ 2 | 0.005        | 2.184034 (0.024843) | 2.165446 (0.013726) | 2.165895 (0.00131)  |
| λ 2 | 0.01         | 2.084817 (0.024298) | 2.066784 (0.013620) | 2.067767 (0.001305) |
| λ 2 | 0.015        | 1.988568 (0.023752) | 1.971061 (0.013496) | 1.972593 (0.001301) |
| λ 2 | 0.02         | 1.895321 (0.023208) | 1.878254 (0.013355) | 1.880513 (0.001297) |
| σ 3 | 0.01         | 2.068057 (0.024337) | 2.086242 (0.013803) | 2.067671 (0.001333) |
| σ 3 | 0.1          | 2.171346 (0.025135) | 2.191243 (0.014131) | 2.168322 (0.001393) |
| σ 3 | 0.3          | 3.015526 (0.032013) | 3.043007 (0.016943) | 3.019851 (0.002007) |
| σ 3 | 0.5          | 4.514536 (0.043350) | 4.550951 (0.020866) | 4.533627 (0.003310) |

### 3 Comparative Statics of Options Prices

#### 3.1 Two-Factor Model

Option prices change in response to changes in the parameters of the model. A good understanding of these so called 'sensitivities' is relevant for risk management and control. In this section we will show how and to what extent the prices of Asian options in the context of the Schwartz (1997) twofactor model change with the various parameters of the model. Here, the price of the underlying asset and convenience yield follow equations (1) and (2) (or (4) and (5) within the risk neutral setting) respectively. We vary the parameters in pairs so as to see how they jointly influence the price of an arithmetic average Asian option with one year to maturity, written on a futures contract of two years to maturity. The valuation is carried out by Monte Carlo simulation, with the analytical solution of the corresponding geometric average Asian option taken as a control variate for variance reduction purpose. We generate 20,000 paths for each pair of parameters. The interest rate is fixed at 5%. The basic setting of the values for all the parameters are exactly the same as in Table 1 and Table 2, except the particular variables which are varied.


<!-- p:18 -->


Figure 1: Price of Asian option depending on key parameters (twofactor model)

Figure 1 illustrates the results. Some interesting patterns can be identified here. For example, the first graph shows that the Asian option price seems to be rather sensitive to changes of either σ 1 or κ , when these parameter are relatively low. However, when either of them carries higher values, we can hardly see any price movement when we manipulate the value of the other. The upper left graph in Figure 1 also suggests that given a relatively low speed of adjustment for the convenience yield, κ , a more volatile market reduces the price of the Asian option. This is particular interesting in light of the results of Ewald and Yor (2015,2018). In addition a higher κ given a low level of σ 1 reduces the price of the Asian option, implying that a more stable inventory level for the commodity leads to a lower option price. Note the relationship between the convenience yield and inventory level, see Fama and French (1988). Similar patterns can be observed in the upper right graph in Figure 1. When σ 2 is low, the option price fluctuates to a larger extent subject to the change of α . Also, higher volatility of the convenience yield brings the Asian options price down. The joint influence of the two volatility parameters, σ 1 and σ 2 , on the Asian option price can be observed in the lower left graph, which reveals a convex shape when varying both parameters. In the lower right graph in Figure 1, we can also observe a convex shape when varying λ 1 , while the option price monotonically increases with σ 1 .


<!-- p:19 -->


#### 3.2 Three-Factor Model

Within the Schwartz (1997) three-factor model, Asian option prices change with varying parameter values in a slightly different way. Here, the price of the underlying asset, convenience yield and interest rate follow equations (20) to (22). Figure 2 shows how the prices change in response to the change of key parameters. In the upper left graph, α and m , the long-term mean of convenience yield and interest rate respectively (unadjusted by market price of risk) are varied. It is easy to notice that when m is larger than 5%, the price becomes very sensitive to changes in m irrespective of the value of α . On the other hand, the option price rises monotonically with the increase of α , given a relatively low level of interest rate over the option period. This is obviously different from the results obtained for the two-factor model in Figure 1, where the option price forms a convex shape with changes in α . Hence, the inclusion of stochastic interest rates apparently alters the way Asian options prices react to changes in the long-term mean of convenience yield.

The upper right graph in Figure 2 shows how options prices move depending on the different values for the speed of adjustment for both convenience yield, κ , and interest rate, a , respectively. It can be seen clearly that higher values of κ and lower values of a result in higher option prices. This is another subtle difference to our results for the two-factor model. While in the two factor model the option price rises dramatically with decreasing κ given a low value of σ 1 , the influence of κ on the option price seems to be the opposite, given a relatively large σ 1 , see upper left in Figure 1. In Figure 2, upper right, the option price appears to increase monotonically with κ , and drops monotonically with a .

The middle left and right and lower left graphs in Figure 2 are dedicated to highlight the relationship between the Asian option price and the volatilities


<!-- p:20 -->

σ2

Figure 2: Price of Asian option depending on key parameters (threefactor model)

of the underlying spot price, σ 1 , the convenience yield, σ 2 , and the interest rate, σ 3 . The third graph clearly shows that the option price forms a convex shape in response to the changes of σ 1 and σ 2 . This is similar to the results from the two-factor model in Figure 1. It is also possible to see from the middle right and lower left graphs that the option price form a convex shape when the volatility of interest rate, σ 3 , varies. However, in neither of the two graphs could we identify any observable changes in the option prices when the volatility of the underlying spot, σ 1 , and convenience yield, σ 2 , vary, given a fixed σ 3 . The lower right graph in Figure 2 demonstrates the response of the option price to changes in the market prices of both convenience yield risk, λ 1 , and interest rate risk, λ 2 . Option payoffs drop with λ 1 , but rise with λ 2 .


<!-- p:21 -->


### 4 Jump Diffusion

In this section, a jump component is added to the stochastic process representing the spot price. The idea of introducing jumps into continuous time models in financial asset pricing originated from Merton (1976). While the Black-Scholes model assumes that the dynamics of spot prices is log-normally distributed, there is strong evidence suggesting fat-tails in the distribution of real world asset prices. In other words, extraordinarily large movements of the underlying spot price do happen in real markets, and such movements are best accounted for by adding a jump component to the spot price dynamic. In reality such jumps correspond to demand or supply shocks, or the sudden arrival of important news, leading to a sudden and profound effect on the underlying spot price.

In the context of the Schwartz (1997) model with stochastic convenience yield, jumps could be added to the spot price as well as the convenience yield. Due to the convenience yield entering the drift term of the spot price, jumps in the convenience yield would lead to a less dramatic effect and less fat tails than the explicit inclusion of a jump component in the spot price. This is the main reason why we decided to go for the latter. We further opt for the threefactor model instead of the two-factor model, as we are mainly interested in longer term horizons, where the possibility of a large price movement, i.e. jump, is much more prominent than within short term horizons. In the former case, commodity futures are also much more sensitive to interest rate risk. Schwartz (1997), has provided specific evidence that the three factor model seems to outperform the two-factor model when the corresponding futures contracts carry longer maturities.

Including a jump component in the spot price, the stochastic process representing the underlying spot price satisfies the following equation under the T -forward measure, Q T ,

$$d S = ( r - \delta - \theta \gamma _ { 1 } - \lambda _ { J } ^ { T } \bar { \kappa } _ { J } ^ { T } ) S d t + \alpha _ { 1 } S d W _ { 1 } ^ { T } + \beta _ { 1 } S d W _ { 2 } ^ { T } + \gamma _ { 1 } S d W _ { 3 } ^ { T } + \kappa _ { J } ^ { T } d q ^ { T } \, .$$

Here θ , α 1 , β 1 , γ 1 have the same interpretation as in equation (A6) and equation (A2) in the Appendix. The expression κ T J dq T represents the jump component, which is governed by two random sources. The first random source, q T represents a Poisson process with intensity λ T J . Hence, the probability that a jump occurs in an infinitesimal unit of time dt is λ T J , i.e. Prob ( dq T = 1) = λ T J dt and Prob ( dq T = 0) = 1 - λ T J dt . The second random source, κ T J , denotes the percentage jump size of the underlying spot price, conditional upon the occurrence of a jump. As in Merton (1976) we assume that κ T J +1 follows a log-normal distribution, or ln( κ T J +1) ∼ N ( ln( ̄ κ T J +1) - 1 2 v 2 J , v 2 J ) . In conclusion, for most of the time when no jump occurs, dq ∗ = 0 and the stochastic process for the underlying spot price behaves in analogy to the Schwartz (1997) three-factor model. When a jump does occur, the underlying price moves abruptly by a random percentage. It is assumed that the two random sources dq T and κ T J are pairwise uncorrelated with each other, and uncorrelated with the Brownian motions driving spot price, convenience yield and interest rate.


<!-- p:22 -->


Within the three-factor model with jumps, the stochastic process of the futures price under Q T follows

$$d F = - ( \lambda _ { J } ^ { T } \bar { \kappa } _ { J } ^ { T } - h _ { 4 } h _ { 3 } ) F d t + h _ { 1 } F d W _ { 1 } ^ { T } + h _ { 2 } F d W _ { 2 } ^ { T } + h _ { 3 } F d W _ { 3 } ^ { T } + \kappa _ { J } ^ { T } d q ^ { T } , \ ( 3 3 )$$

where

$$h _ { 1 } & = \sigma _ { 1 } \alpha _ { 1 } , \ h _ { 2 } = \sigma _ { 1 } \beta _ { 1 } - \frac { \sigma _ { 2 } \beta _ { 2 } } { \kappa } ( 1 - e ^ { - \kappa ( \hat { T } - t ) } ) , \\ h _ { 3 } & = \sigma _ { 1 } \gamma _ { 1 } - \frac { \sigma _ { 2 } \gamma _ { 2 } } { \kappa } ( 1 - e ^ { - \kappa ( \hat { T } - t ) } ) + \frac { \sigma _ { 3 } \gamma _ { 3 } } { a } ( 1 - e ^ { - a ( \hat { T } - t ) } ) , \ h _ { 4 } = - \frac { \sigma _ { 3 } } { a } ( 1 - e ^ { - a ( T - t ) } ) \ .$$

The introduction of jumps adds certain complication to the pricing of Asian options. In difference to Merton (1976) who attempts to price a European option, the exact timing of when the jumps occur matters for the path dependent Asian option. More precisely, the payoff of a European option only depends on the total size of the accumulated jumps, for an Asian option and its payoff it makes a profound difference whether a jump occurs early or late in the lifetime of the option. Since the time between two jumps is Poisson distributed, the geometric average of the underlying spot price will be no longer log-normal. In consequence, there is no closed-form solutions for either arithmetic average or geometric average Asian options.

Nevertheless, we show that it is still possible to use the geometric average Asian option as a suitable control variate in computing arithmetic average Asian option prices via Monte Carlo simulation. The trick here is to undertake the Monte Carlo simulation in two steps. The tower property of the conditional expectation implies that we can compute the option price by first taking an expectation conditional on the sequence of jump times generated by the Poisson process dq T and in a second step average over all possible such sequences. In undertaking the first step, we assume that a sequence of jump times is given and are left with only one additional random variable in comparison to the standard Schwartz (1997) three-factor model, the percentage jump size. The latter is log-normally distributed, and so is its product with the futures price. Hence, the geometric average of the futures prices given the sequence of jump times also follows a log-normal distribution. For this case, a closed form solution for the geometric average Asian option can be computed and used as a control variate to price the corresponding arithmetic average Asian option given the same sequence of jump times by Monte Carlo simulation. We only discuss the case of a discretely sampled geometric average Asian option here, as this is most relevant for the numerical implementation. Nevertheless, the continuously sampled case can be derived in complete analogy.


<!-- p:23 -->


To do so, we follow the same approach as in the three-factor model discussed earlier but take account of the given sequence of jump times. We find the mean and variance of the geometric average of the futures prices over the option period, namely E Jump and V Jump , respectively, under the T -forward measure. We use N J and { T J i } where i runs through { 1 , 2 , ..., N J } to denote the total number of jumps and the exact sequence of jump-times, respectively. These are both assumed to be known when carrying out the first step, and will be averaged over in the second step. The closed-form solutions to the geometric average Asian option at time 0 conditioned on the assumed scenario of jumps can then be presented as in the following equation

$$G A ( t _ { 0 } , t _ { N } , \hat { T } | N _ { J } , \{ T _ { J } , \} ) & = \mathbb { E } [ e ^ { - r } T ^ { \max } ( G ( t _ { 0 } , t _ { N } , \hat { T } ) - K , 0 ) \ | \ N _ { J } , \{ T _ { J } , \} ] \ , \\ & = P ( t _ { 0 } , t _ { N } ) \mathbb { E } ^ { T } \max ( G ( t _ { 0 } , t _ { N } , \hat { T } ) - K , 0 \ | \ N _ { J } , \{ T _ { J } , \} ) \\ & = P ( t _ { 0 } , t _ { N } ) \left [ e ^ { E _ { J } + \frac { 1 } { 2 } V _ { J } } \mathcal { N } \left ( \frac { E _ { J } - \ln ( K ) + V _ { J } } { \sqrt { V _ { J } } } \right ) \right ] \ ( 3 5 ) \\ & - \ K \mathcal { N } \left ( \frac { E _ { J } - \ln ( K ) } { \sqrt { V _ { J } } } \right ) \right ] \ ,$$

where G ( t 0 , t N , ˆ T ) follows equation (A0) in Appendix A.2. The solution to the expectation, E J , and variance, V J , are given as follows,

$$E _ { J } = \frac { 1 } { T } ( E _ { 1 } + E _ { 2 } ) \ , \quad V _ { J } = \frac { 1 } { T ^ { 2 } } ( V _ { 1 } + V _ { 2 } ) ,$$


<!-- p:24 -->


where both E 2 and V 2 are related to and conditional on the jumps.

$$where both E _ { 2 } \text { and } V _ { 2 } \text { are related to and conditional on the jumps} . \\ E _ { 1 } & = ( N + 1 ) \, \ln F ( 0 ) \\ & + m _ { 1 } \left [ - \lambda _ { \bar { \kappa } } \bar { \kappa } _ { J } ^ { T } - \frac { \sigma _ { 3 } } { a } \left ( \sigma _ { 1 } \gamma _ { 1 } - \frac { \sigma _ { 2 } \gamma _ { 2 } } { \kappa } + \frac { \sigma _ { 3 } \gamma _ { 3 } } { a } \right ) \\ & - \frac { 1 } { 2 } \sigma _ { 1 } ^ { 2 } ( \alpha _ { 1 } ^ { 2 } + \beta _ { 1 } ^ { 2 } + \gamma _ { 1 } ^ { 2 } ) - \frac { 1 } { 2 } \left ( \frac { \sigma _ { 2 } ^ { 2 } \beta _ { 2 } ^ { 2 } } { \kappa ^ { 2 } } + \frac { \sigma _ { 2 } ^ { 2 } \gamma _ { 2 } ^ { 2 } } { \kappa ^ { 2 } } + \frac { \sigma _ { 3 } ^ { 2 } \gamma _ { 3 } ^ { 2 } } { a ^ { 2 } } \right ) \\ & + \frac { \sigma _ { 1 } \sigma _ { 2 } } { \kappa } ( \beta _ { 1 } \beta _ { 2 } + \gamma _ { 1 } \gamma _ { 2 } ) - \frac { \sigma _ { 3 } \gamma _ { 3 } } { a } \left ( \sigma _ { 1 } \gamma _ { 1 } - \frac { \sigma _ { 2 } \gamma _ { 2 } } { \kappa } \right ) \right ] \\ & + m _ { 2 } \left [ - \frac { \sigma _ { 2 } \sigma _ { 3 } \gamma _ { 2 } } { \kappa a } ( 1 + \gamma _ { 3 } ) + \frac { \sigma _ { 2 } ^ { 2 } } { \kappa ^ { 2 } } ( \beta _ { 2 } ^ { 2 } + \gamma _ { 2 } ^ { 2 } ) - \frac { \sigma _ { 1 } \sigma _ { 2 } } { \kappa } ( \beta _ { 1 } \beta _ { 2 } + \gamma _ { 1 } \gamma _ { 2 } ) \right ] \\ & + m _ { 3 } \left [ \frac { \sigma _ { 3 } ^ { 2 } \gamma _ { 3 } } { a ^ { 2 } } ( 1 + \gamma _ { 3 } ) + \frac { \sigma _ { 3 } \gamma _ { 3 } } { a } \left ( \sigma _ { 1 } \gamma _ { 1 } - \frac { \sigma _ { 2 } \gamma _ { 2 } } { \kappa } \right ) \right ] \\ & + m _ { 4 } \left ( \frac { \sigma _ { 1 } \sigma _ { 3 } \gamma _ { 1 } } { a } - \frac { \sigma _ { 2 } \sigma _ { 3 } \gamma _ { 2 } } { \kappa a } + \frac { \sigma _ { 3 } ^ { 2 } \gamma _ { 3 } } { a ^ { 2 } } \right ) - m _ { 5 } \frac { \sigma _ { 2 } ^ { 2 } } { 2 \kappa ^ { 2 } } ( \beta _ { 2 } ^ { 2 } + \gamma _ { 2 } ^ { 2 } ) \\ & - m _ { 6 } \frac { \sigma _ { 2 } ^ { 2 } \gamma _ { 3 } } { 2 a ^ { 2 } } + m _ { 7 } \frac { \sigma _ { 2 } \sigma _ { 3 } \gamma _ { 2 } } { \kappa a } - m _ { 8 } \frac { \sigma _ { 2 } ^ { 2 } \gamma _ { 3 } } { a ^ { 2 } } + m _ { 9 } \frac { \sigma _ { 2 } \sigma _ { 3 } \gamma _ { 2 } \gamma _ { 3 } } { \kappa a } \ , \\ \intertext { where } & ( t _ { 1 } + t _ { 2 } ) ( N _ { 1 } + 1 )$$

where

$$where \\ m _ { 1 } = \frac { ( t _ { 0 } + t _ { N } ) ( N + 1 ) } { 2 } , \\ m _ { 2 } = \frac { e ^ { - \kappa \hat { T } } } { \kappa } \left ( \frac { e ^ { \kappa t _ { 0 } } ( 1 - e ^ { \kappa \Delta t ( N + 1 ) } } { 1 - e ^ { \kappa \Delta t } } - ( N + 1 ) \right ) , \\ m _ { 3 } = \frac { e ^ { - a \hat { T } } } { a } \left ( \frac { e ^ { a t _ { 0 } } ( 1 - e ^ { a \Delta t ( N + 1 ) } } { 1 - e ^ { a \Delta t } } - ( N + 1 ) \right ) , \\ m _ { 4 } = \frac { e ^ { - a t _ { N } } } { a } \left ( \frac { e ^ { a t _ { 0 } } ( 1 - e ^ { a \Delta t ( N + 1 ) } } { 1 - e ^ { a \Delta t } } - ( N + 1 ) \right ) , \\ m _ { 5 } = \frac { e ^ { - 2 \kappa \hat { T } } } { 2 \kappa } \left ( \frac { e ^ { 2 \kappa t _ { 0 } } ( 1 - e ^ { 2 \kappa \Delta t ( N + 1 ) } } { 1 - e ^ { 2 \kappa \Delta t } } - ( N + 1 ) \right ) , \\ m _ { 6 } = \frac { e ^ { - 2 a \hat { T } } } { 2 a } \left ( \frac { e ^ { 2 a t _ { 0 } } ( 1 - e ^ { 2 a \Delta t ( N + 1 ) } } { 1 - e ^ { 2 a \Delta t } } - ( N + 1 ) \right ) , \\ m _ { 7 } = \frac { e ^ { - \kappa \hat { T } - a t _ { N } } } { \kappa + a } \left ( \frac { e ^ { ( \kappa + a ) t _ { 0 } } ( 1 - e ^ { ( \kappa + a ) \Delta t ( N + 1 ) } } { 1 - e ^ { ( \kappa + a ) \Delta t } } - ( N + 1 ) \right ) , \\ m _ { 8 } = \frac { e ^ { - a ( \hat { T } - t _ { N } ) } } { 2 a } \left ( \frac { e ^ { 2 a t _ { 0 } } ( 1 - e ^ { 2 a \Delta t ( N + 1 ) } } { 1 - e ^ { 2 a \Delta t } } - ( N + 1 ) \right ) , \\ m _ { 9 } = \frac { e ^ { - ( \kappa + a ) \hat { T } } } { \kappa + a } \left ( \frac { e ^ { ( \kappa + a ) t _ { 0 } } ( 1 - e ^ { ( \kappa + a ) \Delta t ( N + 1 ) } } { 1 - e ^ { ( \kappa + a ) \Delta t } } - ( N + 1 ) \right ) , \\$$


<!-- p:25 -->


and

$$E _ { 2 } = \sum _ { i = 1 } ^ { N } N _ { J } ^ { i } ( N - i + 1 ) \left [ \ln ( \bar { \kappa } _ { J } ^ { T } + 1 ) - \frac { 1 } { 2 } v _ { J } ^ { 2 } \right ] \ ,$$

where N i J indicates the number of jumps that occurred during time t i - 1 and t i . As for the variance,

$$t _ { i } \, \text { As for the variance,} \\ V _ { 1 } = \sigma _ { 1 } ^ { 2 } \alpha _ { 1 } ^ { 2 } \sum _ { i = 1 } ^ { N } ( N - i + 1 ) ^ { 2 } \Delta t \\ + \sum _ { i = 1 } ^ { N } ( N - i + 1 ) ^ { 2 } \left [ \left ( \sigma _ { 1 } \beta _ { 1 } - \frac { \sigma _ { 2 } \beta _ { 2 } } { \kappa } \right ) ^ { 2 } \Delta t + 2 n _ { 1 } \left ( \sigma _ { 1 } \beta _ { 1 } - \frac { \sigma _ { 2 } \beta _ { 2 } } { \kappa } \right ) \frac { \sigma _ { 2 } \beta _ { 2 } } { \kappa } + n _ { 3 } \frac { \sigma _ { 2 } ^ { 2 } \beta _ { 2 } } { \kappa ^ { 2 } } \right ] \\ + \sum _ { i = 1 } ^ { N } ( N - i + 1 ) ^ { 2 } \left [ \left ( \sigma _ { 1 } \gamma _ { 1 } - \frac { \sigma _ { 2 } \gamma _ { 2 } } { \kappa } + \frac { \sigma _ { 3 } \gamma _ { 3 } } { a } \right ) ^ { 2 } \Delta t + n _ { 3 } \left ( \frac { \sigma _ { 2 } \gamma _ { 2 } } { \kappa } \right ) ^ { 2 } + n _ { 4 } \left ( \frac { \sigma _ { 3 } \gamma _ { 3 } } { a } \right ) ^ { 2 } \\ + 2 \left ( \sigma _ { 1 } \gamma _ { 1 } - \frac { \sigma _ { 2 } \gamma _ { 2 } } { \kappa } + \frac { \sigma _ { 3 } \gamma _ { 3 } } { a } \right ) \left ( n _ { 1 } \frac { \sigma _ { 2 } \gamma _ { 2 } } { \kappa } - n _ { 2 } \frac { \sigma _ { 3 } \gamma _ { 3 } } { a } \right ) - 2 n _ { 5 } \frac { \sigma _ { 2 } \sigma _ { 3 } \gamma _ { 2 } / 2 \gamma _ { 3 } } { \kappa a } \right ] , \\ \text {where}$$

where

$$n _ { 1 } & = \frac { e ^ { - \kappa \hat { T } } } { \kappa } ( e ^ { \kappa t _ { i } } - e ^ { \kappa t _ { i - 1 } } ) , \ n _ { 2 } = \frac { e ^ { - a \hat { T } } } { a } ( e ^ { a t _ { i } } - e ^ { a t _ { i - 1 } } ) , \ n _ { 3 } = \frac { e ^ { - 2 \kappa \hat { T } } } { 2 \kappa } ( e ^ { 2 \kappa t _ { i } } - e ^ { 2 \kappa t _ { i - 1 } } ) , \\ n _ { 4 } & = \frac { e ^ { - 2 a \hat { T } } } { 2 a } ( e ^ { 2 a t _ { i } } - e ^ { 2 a t _ { i - 1 } } ) , \ n _ { 5 } = \frac { e ^ { - ( \kappa + a ) \hat { T } } } { \kappa + a } ( e ^ { ( \kappa + a ) t _ { i } } - e ^ { ( \kappa + a ) t _ { i - 1 } } ) ,$$

and

$$V _ { 2 } = \sum _ { i = 1 } ^ { N } N _ { J } ^ { i } ( N - i + 1 ) ^ { 2 } \ v _ { J } ^ { 2 } \ .$$

As indicated before, the expressions above only contribute one step toward the final option price. The next step is to simulate a large number of different sequences of jump times, each providing a unique scenario of jumps and a corresponding analytic option pricing formula via (35), which is to be used as a control variate. This leads to a numerical solution for the arithmetic average Asian option, by averaging over all simulated sequences of jump times.

Table 3 lists the results from the Monte Carlo simulation. By comparing the results and standard deviations from the different methods, it can be clearly seen that the control variate method outperforms the standard Monte Carlo simulation and antithetic variate methods. This is consistent with our previous results where jumps had not been permitted. It is also observable that the antithetic variate method hardly improves the simulation accuracy, since the standard errors are very close to those with standard Monte Carlo.


<!-- p:26 -->


Table 3 Comparison of Monte Carlo Simulation Results ∗ (Three-Factor Model with Jump Diffusion)

|     |     | Standard             | Antithetic           | Control Variate      |
|-----|-----|----------------------|----------------------|----------------------|
| λ J |  20 | 4.545479 (0.047045)  | 4.506676 (0.045807)  | 4.538718 (0.020298)  |
|     |  40 | 6.301796 (0.069681)  | 6.261815 (0.068924)  | 6.258641 (0.027347)  |
|     |  60 | 7.795545 (0.089468)  | 7.776528 (0.088991)  | 7.702643 (0.037032)  |
|     |  80 | 9.249594 (0.115987)  | 9.211714 (0.115242)  | 9.031631 (0.049664)  |
|     | 125 | 11.136526 (0.161701) | 11.127934 (0.161418) | 10.905373 (0.070040) |
|     | 175 | 13.188179 (0.207702) | 13.173379 (0.207424) | 12.978395 (0.097738) |
|     | 250 | 14.972683 (0.318225) | 14.975528 (0.319073) | 14.917575 (0.169395) |

Nevertheless, a comparison between Table 3 and Table 2 shows that the control variate method can improve the simulation accuracy in both cases, but to a more limited extent in the presence of jumps. This is mainly due to the fact that in the three-factor model without jumps, only a single closedform solution to the geometric average Asian option is generated and used as a control variate. However, in the three-factor model with jumps, for every specific series of jumping times, one corresponding solution is used as a control variate. As a result, the control variate method is effective and outperforms the standard Monte Carlo and the antithetic method, but not with the same overwhelming success as in the three-factor model without jumps.

### 5 Conclusions

The pricing of Asian options is a central problem within the context of commodity derivatives. It is therefore surprising, that the pricing of Asian options in what many would refer to as the most important benchmark model for commodity pricing, the Schwartz (1997) multi-factor model, has only been given very little attention. In fact, except Ewald and Chen (2017) who use Albrecher et. al. 's (2005) co-monotonicity approach to derive price bounds, there is no literature addressing this important topic. In this paper we derive closed form solutions for the case of a geometric average Asian option for the two- and three-factor models. We show how these solutions can be used to provide suitable control variates in order to price the more complicated arithmetic average Asian options in these two models. The comparison of the numerical results derived from standard Monte Carlo simulation without variance reduction, the antithetic variate method and using the geometric Asian option as a control variate, shows very significant improvements (up to a factor of 20 times) when the control variate method is implemented. Next, we vary the parameters of the model to see how option prices behave qualitatively. The results show that option prices react to changes of parameters very differently when comparing two- and three-factor models. This is important for the risk-management and control of such options. Further, we extend the classical Schwartz (1997) framework by adding a stochastic jump component to the spot price process. Due to the path dependence of the pay-offs, the consequences of this are far more complex than for European options, which have been discussed in Hilliard and Reis (1998). In consequence, there appears to be no analytical solutions for either the arithmetic average or the geometric average Asian option case. However, we find that conditional upon knowing the sequence of jump times over the option period, a closed form solution for the geometric average Asian option can be derived. This solution is then used as a control variate to price the corresponding arithmetic average Asian option conditional on the same sequence of jump times numerically with Monte Carlo simulation using the geometric Asian option as a control variate. The result is intermediate, because it is conditional on a specific sequence of jumping times over the option period. In a second step we then simulate a large number of different sequences of jump times and repeat the previous step. This finally leads to an unbiased estimate of the true option price by taking the average of all intermediate results over all sequences of jump times. In comparison to standard Monte Carlo and antithetic variates, our methods shows a clearly visible improvement in terms of accuracy.


<!-- p:27 -->


## Appendix

###### A.1

Recall that the price of the geometric average Asian option at time t with maturity T written on a future contract with maturity ˆ T under the riskneutral measure, Q ∗ , can be represented

$$G A ( t , T , \hat { T } ) = \mathbb { E } ^ { * } \max [ e ^ { - r ( T - t ) } ( G ( t , T , \hat { T } ) - K , 0 ) ] \ .$$


<!-- p:28 -->


Since the interest rate is a stochastic process that appears in both the discount factor and the underlying price, solving equation (A0) requires a change of numeraire, where we transform the risk-neutral measure to the T -forward measure, Q T , i.e. the zero-coupon bond is used as the new numeraire. Accordingly, equation (A0) is equivalent to equation (28).

We first attempt to decompose the three correlated Brownian motions in equation (20) to (22) into three independent Brownian motions, namely dW ∗ 1 , dW ∗ 2 , dW ∗ 3 under Q ∗ . The result is shown as follows,

$$d Z _ { 1 } ^ { * } & = \alpha _ { 1 } d W _ { 1 } ^ { * } + \beta _ { 1 } d W _ { 2 } ^ { * } + \gamma _ { 1 } d W _ { 3 } ^ { * } \\ d Z _ { 2 } ^ { * } & = \beta _ { 2 } d W _ { 2 } ^ { * } + \gamma _ { 2 } d W _ { 3 } ^ { * } \\ d Z _ { 3 } ^ { * } & = \gamma _ { 3 } d W _ { 3 } ^ { * } \ ,$$

where

$$\alpha _ { 1 } & = \sqrt { 1 - \rho _ { 3 } ^ { 2 } - ( \frac { \rho _ { 1 } - \rho _ { 2 } \rho _ { 3 } } { \sqrt { 1 - \rho _ { 2 } ^ { 2 } } } ) ^ { 2 } } , \ \beta _ { 1 } = \frac { \rho _ { 1 } - \rho _ { 2 } \rho _ { 3 } } { \sqrt { 1 - \rho _ { 2 } ^ { 2 } } } , \ \beta _ { 2 } = \sqrt { 1 - \rho _ { 2 } ^ { 2 } } , \\ \gamma _ { 1 } & = \rho _ { 3 } , \ \gamma _ { 2 } = \rho _ { 2 } , \ \gamma _ { 3 } = 1 .$$

We then attempt to derive the corresponding Brownian motion under the T -forward measure Q T . In our model where the stochastic interest rate process is governed by equation (22), the price of the zero-coupon bond at time t with maturity T , P ( t, T ) , satisfies the following stochastic process under Q ∗ ,

$$d P ( t , T ) = r ( t ) P ( t , T ) d t - \sigma _ { 3 } B ( t , T ) P ( t , T ) d Z _ { 3 } ^ { * } \ ,$$

where

$$B ( t , T ) = \frac { 1 - e ^ { - a ( T - t ) } } { a } \ . \\$$

We define the discount factor D ( t ) at time t , then the discounted price of the zero-coupon bond can be represented by the following stochastic equation,

$$d ( D ( t ) P ( t , T ) ) = \theta D ( t ) P ( t , T ) d Z _ { 3 } ^ { * } \ ,$$

$$\theta = - \sigma _ { 3 } B ( t , T ) \ .$$

Hence, according to the rules of changing numeraires, the following process,

$$d W _ { 3 } ^ { T } = \theta d t + d W _ { 3 } ^ { * } \ ,$$

is a Brownian motion under Q T , and so are dW ∗ 1 , dW ∗ 2 , as they are independent of dW ∗ 3 and the interest rate process. Nevertheless, we will denote these

where as dW T 2 , dW T 3 in the following context. Hence, the three stochastic processes in our model can now be identified as follows,


<!-- p:29 -->


$$d S = ( r - \delta - \theta \gamma _ { 1 } ) S d t + \alpha _ { 1 } S d W _ { 1 } ^ { T } + \beta _ { 1 } S d W _ { 2 } ^ { T } + \gamma _ { 1 } S d W _ { 3 } ^ { T } \ ,$$

$$d \delta = [ \kappa ( \hat { \alpha } - \delta ) - \theta \gamma _ { 2 } ] d t + \beta _ { 2 } d W _ { 2 } ^ { T } + \gamma _ { 2 } d W _ { 3 } ^ { T } \ ,$$

$$d r = [ a ( \hat { n } - r ) - \theta \gamma _ { 3 } ] d t + \gamma _ { 3 } d W _ { 3 } ^ { T } \ ,$$

$$\hat { \alpha } = \alpha - \frac { \lambda _ { 1 } } { \kappa } \ , \quad \hat { m } = m - \frac { \lambda _ { 2 } } { a } \ . \\$$

where

Under the T-forward measure, equations (A8) to (A10) will then be used to calculate the price of the geometric average Asian option, represented by equation (28).

###### A.2

In this appendix we present the analogue derivation for the discretely sampled geometric average Asian option in the Schwartz (1997) three factor model. Here

$$G A ( t _ { 0 } , t _ { N } , \hat { T } ) = \mathbb { E } ^ { * } \left [ e ^ { - r ( t _ { N } - t _ { 0 } ) } \max ( G ( t _ { 0 } , t _ { N } , \hat { T } ) - K , 0 ) \right ] ,$$

where

$$G ( t _ { 0 } , t _ { N } , \hat { T } ) = \exp \left ( \frac { 1 } { N + 1 } \sum _ { i = 0 } ^ { i = N } \ln F ( S ( t _ { i } ) , \delta ( t _ { i } ) , r ( t _ { i } ) , \hat { T } - t _ { i } ) \right ) \, . \quad ( A 1 2 )$$

The solution to the Asian option price at time t = 0 is given by the following equations,

$$G A ( t _ { 0 } , t _ { N } , \hat { T } ) & = P ( t _ { 0 } , t _ { N } ) \mathbb { E } ^ { \mathbb { T } } \max ( G ( t _ { 0 } , t _ { N } , \hat { T } ) - K , 0 ) \\ & = P ( t _ { 0 } , t _ { N } ) \left [ e ^ { E + \frac { 1 } { 2 } V } \mathcal { N } \left ( \frac { E - \ln ( K ) + V } { \sqrt { V } } \right ) - K \mathcal { N } \left ( \frac { E - \ln ( K ) } { \sqrt { V } } \right ) \right ] ,$$

where P ( t, T ) , the price of the zero-coupon bond with maturity T at time t , is provided by the following equation,

$$P ( t _ { 0 } , t _ { N } ) = A ( t _ { 0 } , t _ { N } ) e ^ { - r _ { 0 } B ( t _ { 0 } , t _ { N } ) } ,$$

where

$$B ( t _ { 0 } , t _ { N } ) & = \frac { 1 - e ^ { - a ( t _ { N } - t _ { 0 } ) } } { a } , \\ A ( t _ { 0 } , t _ { N } ) & = \exp \left [ \left ( \hat { m } - \frac { \sigma _ { 3 } ^ { 2 } } { 2 a ^ { 2 } } \right ) ( B ( t _ { 0 } , t _ { N } ) - ( t _ { N } - t _ { 0 } ) ) - \frac { \sigma _ { 3 } ^ { 2 } } { 4 a } B ^ { 2 } ( t _ { 0 } , t _ { N } ) \right ] ,$$


<!-- p:30 -->


and the expectation, E , and variance, V above are respectively given as

$$and the expectation, E , and variance, V \, \text {above are respectively given as} \\ E _ { 3 - \text {factor} } = \ln S ( t _ { 0 } ) - \frac { \delta ( t _ { 0 } ) } { \kappa } ( 1 - e ^ { - \kappa \hat { T } } ) - \frac { \hat { \alpha } } { \kappa } e ^ { - \kappa \hat { T } } + \frac { r ( t _ { 0 } ) } { a } ( 1 - e ^ { - a \hat { T } } ) + \frac { \hat { m } } { a } e ^ { - a \hat { T } } \\ + \frac { \kappa \hat { \alpha } + \sigma _ { 1 } \sigma _ { 2 } \rho _ { 1 } } { \kappa ^ { 2 } } - \frac { a \hat { m } + \sigma _ { 1 } \sigma _ { 3 } \rho _ { 3 } } { a ^ { 2 } } - \frac { 3 } { 4 } \left ( \frac { \sigma _ { 2 } ^ { 2 } } { \kappa ^ { 3 } } + \frac { \sigma _ { 3 } ^ { 2 } } { a ^ { 3 } } \right ) - \frac { \sigma _ { 1 } \sigma _ { 3 } \gamma _ { 1 } } { a ^ { 2 } } e ^ { - a \hat { T } } \\ + \frac { \sigma _ { 2 } \sigma _ { 3 } \rho _ { 2 } } { \kappa a ( \kappa + a ) } \left ( 1 + \frac { \kappa ^ { 2 } + a ^ { 2 } } { \kappa a } \right ) + \frac { \sigma _ { 2 } \sigma _ { 3 } \gamma _ { 2 } } { \kappa a } \left ( \frac { e ^ { - a \hat { T } } } { a } + \frac { e ^ { - \kappa \hat { T } } } { \kappa } - \frac { e ^ { - \kappa \hat { T } } a } { \kappa + a } \right ) \\ - \frac { \sigma _ { 3 } ^ { 2 } \gamma _ { 3 } } { a ^ { 2 } } \left ( \frac { e ^ { - a \hat { T } } } { a } + \frac { e ^ { - a \hat { T } } } { a } - \frac { e ^ { - a ( \hat { T } + T ) } } { 2 a } \right ) \\ + \frac { 1 } { N + 1 } \left \{ f _ { 1 } \left [ - \left ( \hat { \alpha } - \hat { m } + \frac { 1 } { 2 } \sigma _ { 1 } ^ { 2 } \right ) - \frac { \sigma _ { 3 } } { a } \left ( \sigma _ { 1 } \gamma _ { 1 } - \frac { \sigma _ { 2 } \gamma _ { 2 } } { \kappa } + \frac { \sigma _ { 3 } \gamma _ { 3 } } { a } \right ) \right ] \right \} \\ + f _ { 2 } \left [ - \frac { \kappa \hat { \alpha } + \sigma _ { 1 } \sigma _ { 2 } \rho _ { 1 } } { \kappa } + \frac { \sigma _ { 2 } ^ { 2 } } { 2 \kappa ^ { 2 } } + \frac { a \hat { m } + \sigma _ { 1 } \sigma _ { 3 } \rho _ { 3 } } { a } + \frac { \sigma _ { 3 } ^ { 2 } } { 2 a ^ { 2 } } - \frac { \sigma _ { 2 } \sigma _ { 3 } \rho _ { 2 } } { \kappa a } \right ] \\ + f _ { 3 } \left [ \frac { \hat { \alpha } - \kappa \hat { \alpha } + \sigma _ { 1 } \sigma _ { 2 } \rho _ { 1 } } { \kappa } + \frac { \sigma _ { 2 } ^ { 2 } } { \kappa ^ { 2 } } - \frac { \sigma _ { 2 } \sigma _ { 3 } \rho _ { 2 } } { \kappa ( \kappa + a ) } \left ( \frac { 1 } { a } + \frac { 1 } { \kappa } \right ) - \frac { \sigma _ { 2 } \sigma _ { 3 } \gamma _ { 2 } } { \kappa ^ { 2 } a } \right ] \\ f _ { 4 } \left [ - \frac { \hat { m } } { a } + \frac { a \hat { m } + \sigma _ { 1 } \sigma _ { 3 } \rho _ { 3 } } { a ^ { 2 } } + \frac { \sigma _ { 3 } ^ { 2 } } { a ^ { 3 } } - \frac { \sigma _ { 2 } \sigma _ { 3 } \rho _ { 2 } } { a ( \kappa + a ) } \left ( \frac { 1 } { a } + \frac { 1 } { \kappa } \right ) \\ + \sigma _ { 3 } ^ { 2 } \frac { \sigma _ { 2 } - a ( T - T ) } { a ^ { 2 } } \left ( \sigma _ { 1 } \gamma _ { 1 } - \frac { \sigma _ { 2 } \gamma _ { 2 } } { \kappa ^ { 2 } } + \frac { \sigma _ { 3 } \gamma _ { 3 } } { a } \right ) + \frac { \sigma _ { 3 } ^ { 2 } \gamma _ { 3 } } { a ^ { 3 } } \right ] \\ - f _ { 5 } \frac { \sigma _ { 2 } ^ { 2 } } { 4 \kappa ^ { 3 } } - f _ { 6 } \frac { \sigma _ { 3 } ^ { 2 } } { 2 a ^ { 3 } } \left ( \frac { 1 } { 2 } + \gamma _ { 3 } e ^ { - a ( T - \hat { T } ) } \right ) + f _ { 7 } \frac { \sigma _ { 2 } \sigma _ { 3 } } { \kappa a ( \kappa + a ) } \left ( \gamma _ { 2 } e ^ { - a ( T - \hat { T } ) } + \rho _ { 2 } \right ) \right \} , \\ \intertext { w h } f _ { 1 } = \frac { ( t _ { 0 } + t _ { N } ) ( N + 1 ) } { 2 } , \ f _ { 2 } = ( N + 1 ) \hat { T } - \frac { ( t _ { 0 } + t _ { N } ) ( N + 1 ) } { 2 } ,$$

with

$$with & & f _ { 1 } = \frac { ( t _ { 0 } + t _ { N } ) ( N + 1 ) } { 2 } , & f _ { 2 } = ( N + 1 ) \hat { T } - \frac { ( t _ { 0 } + t _ { N } ) ( N + 1 ) } { 2 } , \\ & f _ { 3 } = e ^ { - \kappa ( \hat { T } - t _ { 0 } ) } \frac { 1 - e ^ { \kappa \Delta t ( N + 1 ) } } { 1 - e ^ { \kappa \Delta t } } , & f _ { 4 } = e ^ { - a ( \hat { T } - t _ { 0 } ) } \frac { 1 - e ^ { a \Delta t ( N + 1 ) } } { 1 - e ^ { a \Delta t } } , \\ & f _ { 5 } = e ^ { - 2 \kappa ( \hat { T } - t _ { 0 } ) } \frac { 1 - e ^ { 2 \kappa \Delta t ( N + 1 ) } } { 1 - e ^ { 2 \kappa \Delta t } } , & f _ { 6 } = e ^ { - 2 a ( \hat { T } - t _ { 0 } ) } \frac { 1 - e ^ { 2 a \Delta t ( N + 1 ) } } { 1 - e ^ { 2 a \Delta t } } , \\ & f _ { 7 } = e ^ { - ( \kappa + a ) ( \hat { T } - t _ { 0 } ) } \frac { 1 - e ^ { ( \kappa + a ) \Delta t ( N + 1 ) } } { 1 - e ^ { ( \kappa + a ) \Delta t } } ,$$


<!-- p:31 -->


and

with

$$g _ { 1 } & = \frac { e ^ { - \kappa \hat { T } } } { \kappa } ( e ^ { \kappa t _ { i } } - e ^ { \kappa t _ { i - 1 } } ) , \ g _ { 2 } = \frac { e ^ { - a \hat { T } } } { a } ( e ^ { a t _ { i } } - e ^ { a t _ { i - 1 } } ) , \ g _ { 3 } = \frac { e ^ { - 2 \kappa \hat { T } } } { 2 \kappa } ( e ^ { 2 \kappa t _ { i } } - e ^ { 2 \kappa t _ { i - 1 } } ) , \\ g _ { 4 } & = \frac { e ^ { - 2 a \hat { T } } } { 2 a } ( e ^ { 2 a t _ { i } } - e ^ { 2 a t _ { i - 1 } } ) , \ g _ { 5 } = \frac { e ^ { - ( \kappa + a ) \hat { T } } } { \kappa + a } ( e ^ { ( \kappa + a ) t _ { i } } - e ^ { ( \kappa + a ) t _ { i - 1 } } ) .$$
