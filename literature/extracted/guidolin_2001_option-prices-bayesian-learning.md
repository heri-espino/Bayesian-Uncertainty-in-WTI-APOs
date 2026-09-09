---
id: "guidolin_2001_option-prices-bayesian-learning"
source_pdf: "../pdf/guidolin_2001_option-prices-bayesian-learning.pdf"
source_filename: "guidolin_2001_option-prices-bayesian-learning.pdf"
format: "academic-paper"
extraction_profile: "token-efficient-high-fidelity"
extraction_mode: "full-page-ocr"
extraction_quality: "excellent"
extraction_score: 108.0
formula_enrichment: "codeformulav2"
table_structure: "accurate"
tables_png: 11
figures_png: 32
assets_dir: "../assets/guidolin_2001_option-prices-bayesian-learning"
references_file: "../references/guidolin_2001_option-prices-bayesian-learning.references.md"
---

<!-- p:1 -->

Option Prices under Bayesian Learning: Implied Volatility Dynamics and Predictive Densities By

Massimo Guidolin and Allan Timmermann

DISCUSSION PAPER 397

November 2001

### FINANCIAL MARKETS GROUP

AN ESRC RESEARCH CENTRE

LONDON SCHOOL OF ECONOMICS

E·S·R·C

ECONOMIC

RESEARCH

COUNCIL

Any opinions expressed are those of the author and not necessarily those of the Financial Markets Group.

ISSN 0956-8549-397


<!-- p:2 -->


## Option Prices under Bayesian Learning: Implied Volatility Dynamics and Predictive Densities*

Massimo Guidolin† Allan Timmermann University of Virginia University of California, San Diego

JEL codes: G12, D83.

#### Abstract

This paper shows that many of the empirical biases of the Black and Scholes option pricing model can be explained by Bayesian learning effects. In the context of an equilibrium model where dividend news evolve on a binomial lattice with unknown but recursively updated probabilities we derive closed-form pricing formulas for European options. Learning is found to generate asymmetric skews in the implied volatility surface and systematic patterns in the term structure of option prices. Data on S&amp;P 500 index option prices is used to back out the parameters of the underlying learning process and to predict the evolution in the cross-section of option prices. The proposed model leads to lower out-ofsample forecast errors and smaller hedging errors than a variety of alternative option pricing models, including Black-Scholes and a GARCH model.

*We wish to thank four anonymous referees for their extensive and thoughtful comments that greatly improved

the paper. We also thank Alexander David, José Campa, Bernard Dumas, Wake Epps, Stewart Hodges, Claudio Michelacci, Enrique Sentana and seminar participants at Bocconi University, CEMFI, University of Copenhagen, Econometric Society World Congress in Seattle, August 2000, the North American Summer meetings of the Econometric Society in College Park, June 2001, the European Finance Association meetings in Barcelona, Au      st  stt     l  sty of Virginia for discussions and helpful comments.

†Correspondence to: Massimo Guidolin, Department of Economics, University of Virginia, Charlottesville -

114 Rouss Hall, Charlottesville, VA 22903. Tel: (434) 924-7654; Fax: (434) 982-2904; e-mail: mg8g@virginia.edu


<!-- p:3 -->


### 1. Introduction

Although Black and Scholes' (1973) formula remains the most commonly used option pricing model in financial markets, a large literature has documented its strong empirical biases. Most commonly, such biases are associated with the appearance of systematic patterns (smiles or skews) in the implied volatility surface produced by inverting market prices and solving for the unknown volatility parameter (e.g. Rubinstein (1985, 1994) and Dumas, Fleming and Whaley (1998)). Implied volatility also appears to be systematically related to the term structure of option contracts (Das and Sundaram (1999)).

Several pricing models have been proposed to overcome these problems. These include stochastic volatility (Hull and White (1987), Wiggins (1987), Melino and Turnbull (1990), Heston (1993)) and GARCH models (Duan (1995), Heston and Nandi (2000)); models with jumps in the underlying price process (Merton (1976)); jump-diffusion models (Ball and Torous 1a  (() )  os ds s  :(  (a) and Chen (1997) summarize the empirical performance of these models. Most option pricing models fail to improve significantly on the empirical fit of the Black-Scholes (BS) model and, by modifying the stochastic process followed by the underlying asset price, do not provide a direct economic explanation for the systematic shortcomings of BS. Nevertheless, this literature has contributed significantly to our understanding of the requirements of an option pricing model that can fit observed data.

In this paper we relax the key assumption underlying the BS model of full information about the stochastic process that drives fundamentals. More specifically, we assume that fundamentals evolve on a binomial lattice with up' and down' probabilities that are unknown to investors who update their probability estimates using Bayes' rule. The underlying asset price process is determined by embedding the learning mechanism in an equilibrium model. In equilibrium, asset prices reflect all possible future probability distributions of the parameter estimates and there are no expected gains from implementing trading strategies based on the unfolding of estimation uncertainty.

While there are now many papers studying the asset pricing effects of learning,1 the only other studies that explicitly consider its derivative pricing implications appear to be David and Veronesi (1999) and Yan (2000). In an important contribution, David and Veronesi (1999) have investors facing a filtering problem which leads them to update the probability of which of two states fundamentals are currently in. In their model, shocks to fundamentals are drawn from a non-Gaussian mixture distribution and hence the BS model is not obtained in the limit even when there is full information about the state. In contrast, we assume that fundamentals follow a binomial process, whose limit is Gaussian. This allows us to isolate the effect of investors' recursive estimation of parameter values in a model that converges asymptotically to BS. Another difference is that we study the ability of the learning model to predict out-ofsample the evolution in the entire cross-section of option prices and to generate lower hedging errors than BS. The importance of such exercises for evaluating different option pricing models has recently been emphasized by Dumas et al. (1998). In Yan (2000) the unobservable rate of growth of dividends follows a mean-reverting diffusion process. Again shocks to fundamentals are drawn from a non-Gaussian mixture distribution, so that BS does not obtain under full information,2 which makes it more difficult to extract the effects of recursive learning on option prices. Yan presents calibrations which indicate that the model can generate a wide variety of implied volatility surfaces but presents no empirical estimates of the model's fit and does not explore the possibility of implying beliefs from observed asset prices.

1E.g., Bossaerts (1995, 1999) and Timmermann (1993).


<!-- p:4 -->


Our approach is also related to a large literature that infers the market's probability beliefs from asset prices (Rubinstein (1994), Jackwerth and Rubinstein (1996), Ait-Sahalia and Lo (1998)) although our results explicitly incorporate the effect of investors' beliefs on equilibrium prices. The assumption that the market updates its beliefs through Bayes rule adds a new aspect to this exercise and provides an understanding of the time-series dynamics of implied volatility surfaces.

Simply replacing the assumption in the BS model of known 'up' and 'down' probabilities with Bayesian learning is found to generate biases similar to those observed in option prices. Consistent with recent empirical evidence (Ait-Sahalia and Lo (1998)), learning alters the shape of the state price density perceived by investors by adding to tail probabilities. Furthermore, learning effects can generate implied volatility smiles as well as a variety of non-constant term structures of implied volatility.3 By inverting the resulting model, we can infer the dynamics of the parameters of the Bayesian learning scheme from data on S&amp;P 500 index option prices. Independently of the time period over which theoretical option prices are matched with observed prices, we find that estimated parameters are remarkably stable over time and that our model provides a good in-sample fit, and especially an excellent out-of-sample performance in addition to generating smaller out-of-sample hedging errors than the BS model and various alternatives proposed in the literature (Dumas et al.'s (1998) ad hoc strawman and Heston and Nandi's (2000) option NGARCH).

The outline of the paper is as follows. Section 2 introduces the data set and briefly describes systematic biases in the BS option pricing model. Section 3 presents the binomial lattice model under full information and Bayesian learning is introduced in Section 4 which also derives explicit formulae for European option prices. Section 5 characterizes the equilibrium effect of learning on option prices and calibrates the option pricing model under learning so it can be compared to the data from Section 2. The parameters characterizing the maintained recursive learning process are inferred from option prices in Section 6 and used to predict option prices out-of-sample. Section 7 concludes.

2However Yan (2000, p. 22) shows that under log-utility a special version of BS that incorporates stochastic interest rates and volatility obtains.

3Das and Sundaram (1999) show that the most popular alternatives to BS — jump-diffusion and stochastic volatility models — fail to simultaneously generate implied volatility smiles and term structures that match the complex features of the data.


<!-- p:5 -->


### 2. Biases in the Black-Scholes Model

This section briefly outlines the systematic pricing biases in the BS option pricing model and thus serves as a benchmark for the empirical analysis. Our data set of option prices from the CBOE consists of weekly S&amp;P 500 index option prices4 covering a five and a half year period from June 1988 through December 1993 (a total of 30,461 observations) and is identical to the one used in Dumas et al. (1998).5 We explicitly take into account that the index pays out daily dividends and adjust the reported index level by subtracting the present value of the cash dividends to be paid during the life of the option. We follow the same procedures for filtering the data as in Ait-Sahalia and Lo (1998) and thus differ slightly from Dumas et al. (1998) in the application of some exclusion criteria. First, we eliminate options with fewer than 6 and more than 200 days to expiration.6 Second, since it is well known that in-the-money options are thinly traded, their prices are notoriously unreliable and are thus discarded from the data Sue ey e o , oe e n ---n pn n---e ns put-call parity. All information contained in liquid put option prices has thus been extracted and converted into call prices. The remaining put options are discarded from the data set without loss of information. The application of these criteria reduces the size of the sample to a total of 9,679 observations.7

#### 2.1. Implied Volatility Surfaces

Initially we confirm the existence of a systematic skew in the relationship between BS implied volatility and moneyness. Figure 1 plots the implied volatility surface against moneyness for the six December maturities represented in our data sample.8 For most days in the sample period, the curve relating BS implied volatilities to the strike price is skewed. This is of course inconsistent with the maintained assumption of a constant diffusion in the BS model.

4As stressed by Rubinstein (1994), the market for S&amp;P 500 index options on the CBOE provides a case study where the conditions required by BS seem to be well approximated in terms of volumes, continuity of the trading process and hedging opportunities.

5We thank Bernard Dumas for making this data set available to us. Data are sampled on Wednesdays and only options with bid/ask price quotes between 2:45 and 3:15 p.m. (CST) are used. Wednesdays are chosen in order to minimize the incidence of the number of holidays. Option prices correspond to bid/ask midpoints. The risk-free rate is proxied by the average of bid and ask discounts reported in the Wall Street Journal. Daily cash dividends are collected from the S&amp;P 500 Information Bulletin.

6Dumas et al. (1998) exclude all contracts with more than 100 days to expiration.

7One observation had to be excluded since it violated the lower bound condition and led to a negative implied volatility.


<!-- p:6 -->


#### 2.2. Term Structure of Implied Volatility

The data also reveals a systematic term structure in implied volatilities. Using three alternative values of moneyness over the period Jan. 18, 1993 to Jan. 25, 1993, Figure 2 shows that the implied volatilities of at-the-money options and options with moneyness less than one increase with time to expiration. For in-the-money options the pattern is somewhat weaker: some days implied volatility is an increasing and convex function of time to expiration; other days implied volatility is a concave function of moneyness and occasionally the pattern is constant or even declining.

#### 2.3. State Price Densities

Recently Rubinstein (1994) and Jackwerth and Rubinstein (1996) proposed to extract state o romr  oe e e    oe (  e demonstrating biases in the BS model whose assumption is that the state price density is lognormal. Figure 3 shows the SPD inferred from option contracts with at least 7 calendar days to expiration and averaged across calendar days and maturities (a total of 765 estimated SPDs). To ensure that SPDs on different days are comparable, all plots use standardized logarithmic returns. Particularly important in economic terms is the tail behavior of the SPD since this may provide information about the jump risk expected by markets, cf. Bates (1991). Therefore we plot in the bottom of Figure 3 the estimated tail behavior of the average SPD.

Compared to the lognormal benchmark, the SPD is clearly leptokurtic. Market participants assign high value to future extreme' outcomes that under a lognormal SPD would receive a much smaller state price. To demonstrate this point, Table 1 compares the no-arbitrage prices of a state-contingent asset paying off one dollar when the S&amp;P 500 returns exceed (in absolute value) a certain number of standard deviations of returns under the estimated SPDs versus under a lognormal benchmark. Higher prices for tail-contingent securities reflect the fact that under the estimated SPDs the market assigns a much higher risk-neutral price to a dollar paid out in either crash or strongly bullish states of the world.

8The finding of skews in implied volatility is generic and holds across different maturities.


<!-- p:7 -->


### 3. Asset Prices under Full Information

The empirical findings reported in Section 2 confirm the presence of systematic biases in the BS model and suggest that a more general option pricing model is required. This section characterizes option prices in a full information equilibrium model which has the BS model as a limiting case and sets up a benchmark from which to evaluate option pricing biases. Learning is introduced in Section 4.

#### 3.1. Fundamentals on a Binomial Lattice

Our starting point is a version of the infinite horizon, representative agent endowment economy studied by Lucas (1978). There are three assets: A one-period default-free, zero-coupon bond in zero net supply trading at a price of Pt and earning interest of rt = (1/Pt − 1); a stock traded at a price of St whose net supply is normalized at 1; and a European call option written on the stock with τ ≡ T − t periods to expiration, strike price K and current price Ct.

and are consumed in the period when they are received. Dividend growth rates, gt+k = Dt+k Dt+k−1 1, follow a Bernoulli process that is subject to change m times in each unit interval. Within the interval [t, t + τ] dividends thus follow a v = τm-step binomial process. For each interval the dividend growth rate is gh with probability π or gl with probability 1 − π:

$$g _ { t + k + 1 } = \begin{cases} \ g _ { h } & w i t h \ p r o b . \ \pi \\ \ g _ { l } & w i t h \ p r o b . \ 1 - \pi \end{cases} \quad \forall k \geq 0 , \quad \pi \in ( 0 , 1 )$$

Without loss of generality we assume that gh &gt; gl &gt; -1 so that dividends are non-negative provided Dt &gt; 0. This gives a standard recombining binomial tree similar to the one adopted by Cox, Ross and Rubinstein (1979) for the underlying asset price process. We follow the literature in normalizing the parameters by the incremental time unit: 1 + gh = eσ√ x , 1 + gl = (1 + gh)−1, dt =  e 十 1μ dt . As dt → 0, the distribution of dividends converges weakly to a geometric 2 2σ√ v v Brownian motion with constant drift and diffusion (μ, σ).

To price assets we assume a perfect capital market. There are unlimited short sales possibilities, perfect liquidity, no taxes, no transaction costs or borrowing and lending constraints and markets are open at all the nodes of the binomial lattice where news on dividends are generated.

9Dividends in our model really refer to all information on (cash and non cash) earnings produced by companies in the stock index. David and Veronesi (2000) compare beliefs implicit in observed option prices and beliefs filtered on n  s  n e y     o  s   nt a sign that a much more complex notion of fundamentals than earnings or dividends is likely to be used by investors.


<!-- p:8 -->


The representative investor has power utility

$$u ( Z _ { t } ) = \begin{cases} \frac { Z _ { t } ^ { 1 - \gamma } - 1 } { 1 - \gamma } & \gamma < 1 \\ \ln Z _ { t } & \gamma = 1 \end{cases}$$

where Zt is real consumption at time t. We focus on the case where γ ≤ 1; models with γ &gt; 1 have the counter-intuitive property that stock prices decline when the probability of high growth of the fundamentals increases, see Abel (1988).10 The representative agent chooses bond, stock, and call option holdings to maximize the discounted value of expected future utilities derived from consumption subject to a budget constraint:

$$\max _ { \{ Z _ { t + k } , w _ { t + k } ^ { s } , w _ { t + k } ^ { b } \} _ { k = 0 } ^ { \infty } } E _ { t } \left [ \sum _ { k = 0 } ^ { \infty } \beta ^ { k } u ( Z _ { t + k } ) \right ] \\ Z _ { t + k } , \, S _ { C } \, , \, \max _ { \{ Z _ { t + k } , w _ { t + k } ^ { s } \} _ { k = 0 } ^ { \infty } } E _ { t } \left [ \sum _ { k = 0 } ^ { \infty } \beta ^ { k } u ( Z _ { t + k } ) \right ]$$

where β = 1 , represent the number of stocks and bonds in the agent's portfolio as of period t + k.11

Standard dynamic programming methods yield the following Euler equations for stock and bond prices:

$$S _ { t } & \ = \ E _ { t } \left [ Q _ { t + 1 } ( S _ { t + 1 } + D _ { t + 1 } ) \right ] \\ P _ { t } & \ = \ E _ { t } \left [ Q _ { t + 1 } \right ]$$

=β (Zt+1 -γ is the pricing kernel defined as the product of the discount u′(Zt) Zt factor and the intertemporal marginal rate of substitution in consumption.

Guidolin and Timmermann (2001) price the underlying stock and risk-free bond in this setting subject to a transversality condition.12 For convenience, we state asset prices using the

10The restriction γ ≤ 1 is not as implausible as it might appear in the light of the voluminous literature that has either estimated or used values of γ well above 1 in order to match known stylized facts concerning asset prices and returns. The existing literature has in general performed these empirical exercises under the assumption of full information rational expectations. Guidolin and Timmermann (2000) show that on a Bayesian learning path, many stylized facts concerning asset prices (such as high volatility and serial correlation) can easily be rationalized for γ ≤ 1. A referee also pointed out that in the framework of Abel (1999), an economy with leverage can be well approximated by our endowment economy with the coefficient of relative risk aversion replaced by the ratio between γ and the leverage index.

12The transversality condition is:

11Since the call is a redundant asset which does not expand the set of attainable consumption patterns, option holdings do not enter into the program and the equilibrium stock and bond prices can be determined independently of the option price.

$$\lim _ { T \to \infty } E _ { t } \left [ \left ( \prod _ { k = 1 } ^ { T } Q _ { t + k } \right ) S _ { t + T } \right ] = 0 .$$


<!-- p:9 -->


transformed parameters gt = (1 + gl)1−γ − 1 and gh = (1 + gh)1−γ − 1.

Proposition 1 (Guidolin and Timmermann (2001)) The full information rational expectations stock price is given by

$$S _ { t } = \frac { 1 + g _ { l } ^ { * } + \pi ( g _ { h } ^ { * } - g _ { l } ^ { * } ) } { \rho - g _ { l } ^ { * } - \pi ( g _ { h } ^ { * } - g _ { l } ^ { * } ) } D _ { t } , \\$$

while the full information bond price is

$$P _ { t } = \frac { ( 1 + g _ { l } ) ^ { - \gamma } + \pi \left [ ( 1 + g _ { h } ) ^ { - \gamma } - ( 1 + g _ { l } ) ^ { - \gamma } \right ] } { 1 + \rho } . \\$$

A property of the solution is that the stock price is homogeneous of first order in dividends and that the ex-dividend stock price follows the same binomial lattice {gh, gl, π, m} as dividends.13 This means that dividends and stock prices follow a stationary Markov chain.

#### 3.2. Option Prices under Full Information

Pricing European calls and establishing the link to Black-Scholes is straightforward under full information. This follows from noting that in our model (i) arbitrage opportunities are ruled out; (ii) markets are complete; (iii) ex-dividend stock prices inherit the binomial lattice structure {gh, gl, π, m} from dividends; (iv) although the underlying asset pays out cash dividends, the option is European and early exercise is not possible. Therefore we can draw on the result of Cox et al. (1979) that the price of a European option converges to the BS value provided the parameters are suitably adjusted as the number of increments to the lattice per unit of calendar time goes to infinity. Let r be the risk-free rate, δ the dividend yield, and μ and σ respectively the (annual) mean and volatility of the dividend growth rate, while dt is an interval of fixed calendar time (typically τ/252, supposing there are 252 trading days). The following proposition restates this result and shows the mapping between the deep parameters of our model and the BS inputs.

Proposition 2 Suppose that the parameters have been scaled as follows:

$$\text {Proposition } 2 \text { Suppose that the parameters have been scaled as follows} \colon \\ g _ { h } ^ { ( m ) } & = e ^ { \sigma \sqrt { d t / v } } - 1 , 1 + g _ { l } ^ { ( m ) } = \left ( 1 + g _ { h } ^ { ( m ) } \right ) ^ { - 1 } , \pi ^ { ( m ) } = \frac { 1 } { 2 } + \frac { 1 } { 2 } \frac { \mu } { \sigma } \sqrt { \frac { d t } { v } } \\ \rho ^ { ( m ) } & = ( 1 + \frac { \frac { d t } { v } } { v } \left \{ ( 1 + g _ { l } ^ { ( m ) } ) ^ { - \gamma } + \pi ^ { ( m ) } \left [ ( 1 + g _ { h } ^ { ( m ) } ) ^ { - \gamma } - ( 1 + g _ { l } ^ { ( m ) } ) ^ { - \gamma } \right ] \right \} - 1 > 0 \\ \delta ^ { ( m ) } & = \frac { ( 1 + r ) \left \{ ( 1 + g _ { l } ^ { ( m ) } ) ^ { - \gamma } + \pi ^ { ( m ) } \left [ ( 1 + g _ { h } ^ { ( m ) } ) ^ { - \gamma } - ( 1 + g _ { l } ^ { ( m ) } ) ^ { - \gamma } \right ] \right \} } { \left \{ ( 1 + g _ { l } ) ^ { 1 - \gamma } + \pi ^ { ( m ) } \left [ ( 1 + g _ { h } ^ { ( m ) } ) ^ { 1 - \gamma } - ( 1 + g _ { l } ^ { ( m ) } ) ^ { 1 - \gamma } \right ] \right \} } - 1 . \\ \frac { 1 3 \text {When combined with the result in Pliska} ( 1997) that a multiperiod security markets model is complete if and}$$

13When combined with the result in Pliska (1997) that a multiperiod security markets model is complete if and only if all possible sequences of single period models obtained by decomposing the binomial lattice are formed by complete models, it follows that the asset market in our model is complete and the call option is a redundant asset, as conjectured.


<!-- p:10 -->


Then as m → ∞, the price of the European call converges to its BS value:

$$C _ { t } ^ { B S } \ = \ S _ { t } \Phi ( d _ { 1 } ) e ^ { - \delta ^ { ( m ) } d t } - e ^ { - r d t } K \Phi \left ( d _ { 2 } \right ) \\ \ln \left ( \frac { S _ { t } } { K } \right ) + \left ( r - \delta ^ { ( m ) } \right ) v + \frac { 1 } { 2 } v \left [ \ln ( 1 + g _ { h } ^ { ( m ) } ) \right ] ^ { 2 } \\ \frac { d _ { 1 } } { d _ { 2 } } \ = \ \frac { \sqrt { v } \ln ( 1 + g _ { h } ^ { ( m ) } ) } { d _ { 1 } - \sqrt { v } \ln \left ( 1 + g _ { h } \right ) }$$

where v = τm and Φ(·) is the c.d.f. of the standard normal distribution.

Proof. See Appendix A.

As m → ∞, dt goes to zero, and the binomial lattice converges weakly to a geometric Browv nian motion with parameters (μ, σ), the distributional assumption required by BS in continuous time.14 This proposition shows that the results of Cox et al. fully extend to our framework where dividends rather than stock prices are assumed to follow a binomial lattice. Notice, however, that while Cox et al. take the process for the underlying price as exogenous, we derive the underlying stock price in an equilibrium model in which preferences matter. This result can also be related to Stapleton and Subrahmanyam (1984) who value options in a general equilibrium model when markets are incomplete and the stock price evolves on a binomial lattice. In contrast to Stapleton and Subrahmanyam, our model assumes that markets are complete, but the exogenous binomial lattice process applies to dividends. Obviously in both cases preferences affect the equilibrium price of stocks as well as options. Since the BS option price is obtained in the limit under full information, this model is ideally suited to discuss the origin of BS pricing biases.

### 4. Option Prices on a Learning Path

It is common in the option pricing literature to assume a given process for the underlying asset price and then price the option as a redundant asset whose payoffs can be replicated in a dynamic hedging strategy invested in the risky asset and a riskfree bond. The standard setup assumes that the asset price process is stationary and hence that there are no learning effects. Once learning is introduced, an equilibrium model for the underlying asset price is required.

Suppose that the proportion of times dividends move up on the binomial lattice, π, is unknown to investors who recursively estimate it through the simple maximum likelihood esti-

14This point can also be shown by noting that as m, v → ∞ the discrete state price density converges to a transformation of the lognormal:

$$\widetilde { f } ( S _ { t + T } ) = e ^ { - r \tau } \frac { 1 } { \sqrt { 2 \pi } \sigma \sqrt { \tau } } \frac { 1 } { S _ { t + T } } \exp \left \{ - \frac { \left [ \ln \left ( S _ { t } \right ) - \left ( r - \delta + \frac { 1 } { 2 } \left [ \ln ( 1 + g _ { h } ) \right ] ^ { 2 } \right ) v \right ] ^ { 2 } } { 2 v \left [ \ln ( 1 + g _ { h } ) \right ] ^ { 2 } } \right \} .$$


<!-- p:11 -->


mator:

$$\widehat { \pi } _ { t + k , j } = \frac { \sum _ { i = 1 } ^ { m ( t + k ) + j } I _ { \{ m ( t + k ) + i = g _ { h } \} } } { m ( t + k ) + j } = \frac { m _ { m ( t + k ) + j } } { N _ { m ( t + k ) + j } } \quad j = 0 , 1 , \dots , m - 1$$

where I{m(t+k)+i=gh} is an indicator function which is one when at the m(t + k) + i−th step of the lattice dividend growth is high, and is zero otherwise. ni denotes the number of high growth states recorded up to node i, while Ni is the total number of nodes since time t. The indices m(t + k) + j (j = 0, 1, ..., m − 1) take into account that learning happens on the binomial tree and not over calendar time. Investors are assumed to start out with prior beliefs {no, No} and update these through Bayes rule.

Despite the presence of learning effects, the same features that simplified the solution of asset prices under full information are still in place: (i) consumption and dividends must coincide in general equilibrium; (ii) if markets are complete, investors form portfolio choices based only on the stock index and the bond; (iii) being redundant assets, options can be priced by noarbitrage, using the unique risk neutral probability measure. This can be used to prove the following result:

Proposition 3 Suppose that the stock price is homogeneous of degree one in the level of real dividends, that a transversality condition holds, and that ρ &gt; gh. Then the stock price under Bayesian learning (BL) is

$$S _ { t } ^ { B L } \ & = \ D _ { t } v \to \infty \ell i m \left \{ \sum _ { i = 1 } ^ { v } \beta ^ { i } \sum _ { j = 0 } ^ { i } ( 1 + g _ { h } ^ { * } ) ^ { j } ( 1 + g _ { l } ^ { * } ) ^ { i - j } \Pr _ { t } ^ { B L } \left ( D _ { t + i } ^ { j } | n _ { t } , N _ { t } \right ) \right \} \\ & \equiv \ D _ { t } \Psi _ { t } ^ { B L } ( n _ { t } , N _ { t } )$$

where the posterior distribution Pr BL hq uəab s? (,N (u|(A t−?(1b + I),(u6 + I) = }+ta)

$$\Pr _ { t } ^ { B L } \left \{ D _ { t + i } ^ { j } | n _ { t } , N _ { t } \right \} = \binom { i } { j } \frac { \prod _ { k = 0 } ^ { j - 1 } ( n _ { t } + k ) \prod _ { k = 0 } ^ { i - j - 1 } ( N _ { t } - n _ { t } + k ) } { \prod _ { k = 0 } ^ { i - 1 } ( N _ { t } + k ) } .$$

The bond price under Bayesian learning is

$$P _ { t } ^ { B L } ( \widehat { \pi } _ { t } ) = \widehat { E } _ { t } \left [ \beta ( 1 + g _ { t + 1 } ) ^ { - \gamma } \right ] = \frac { ( 1 + g _ { l } ) ^ { - \gamma } + \widehat { \pi } _ { t } \left [ ( 1 + g _ { h } ) ^ { - \gamma } - ( 1 + g _ { l } ) ^ { - \gamma } \right ] } { 1 + \rho } .$$

Proof. See Appendix A.

Proposition 3 has several implications. First, the price-dividend ratio is no longer constant and depends (through nt and Nt) on the current estimate πt. Dividend changes acquire a selfenforcing nature: Positive dividend shocks lead to an increase in the stock price not only through the standard proportional effect, but also through the revision of the dividend multiplier.


<!-- p:12 -->


Although dividend yields are now time-varying, in principle binomial methods could still be used to obtain the no-arbitrage price of European options on flexible trees (see, e.g., Chriss (1997)). However, risk-free rates in our equilibrium model are not only time-varying, but also a function of the state variable πt+k. Furthermore, the interest rate process cannot be characterized as a recombining lattice. The value today of one dollar in the future depends not only on the number of high and low growth states occurring between today and the future, but also uep-t d ste s ee hnt sn   e s t n Since risk-free rates show up in the general risk-neutral valuation formula proved by Harrison and Kreps (1979), the induced lattice for the call option also becomes non-recombining. 16

This path dependence means that no-arbitrage methods are more complicated in an equilibrium model with learning. Nevertheless, European call options on a stock index can still be priced by employing a change of measure based on the perceived probabilities:

Proposition 4 On a Bayesian learning path, the no-arbitrage price of a European call with time-to-expiration τ and strike price K is

$$C _ { t } ^ { B L } ( K , T , S _ { t } ^ { B L } ) = \sum _ { j = 0 } ^ { v } \max \left \{ 0 , S _ { t + v } ^ { B L , j } - K \right \} \widetilde { P } _ { t } ^ { B L } \left \{ S _ { t + v } ^ { j } | n _ { t } , N _ { t } \right \}$$

where v = τm, St+v BL,j = (1 + gh)j(1 + gl)ν−jSBL = (1 + gh)j(1 + gl)v−j ΨBL ltLv(nt + j, Nt + v) Dt,

15This can most easily be seen by comparing the value as of period t + 1 of one dollar in period t + 3 when both the high and low dividend growth rates occur. When high growth is followed by low growth we have

$$& \quad \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \$$

where πt+2 = nt+1 = πt+2. du Nt+2

When the sequence is reversed and low growth is followed by high growth, we get

$$\text {when the sequence is reversed and row $g$-flow on row $G$} \\ \left [ 1 + r _ { t + 1 } ^ { B L } ( \widehat { \pi } _ { t + 1 } ) \right ] ^ { - 1 } \left [ 1 + r _ { t + 2 } ^ { B L } ( \widehat { \pi } _ { t + 2 } ) \right ] ^ { - 1 } & = \\ = \frac { 1 + \rho } { ( 1 + g _ { l } ) ^ { - \gamma } + \frac { n _ { l } } { N _ { t + 1 } } \left [ ( 1 + g _ { h } ) ^ { - \gamma } - ( 1 + g _ { l } ) ^ { - \gamma } \right ] } \times \frac { 1 + \rho } { ( 1 + g _ { l } ) ^ { - \gamma } + \frac { n _ { l } + 1 } { N _ { t + 2 } } \left [ ( 1 + g _ { h } ) ^ { - \gamma } - ( 1 + g _ { l } ) ^ { - \gamma } \right ] } .$$

Taking the ratio of these two expressions and letting G ≡ [(1 + gh)−γ − (1 + gl)−γ], we have

$$\frac { ( 1 + g _ { l } ) ^ { - 2 \gamma } + \frac { n _ { t } ( n _ { t } + 1 ) } { ( N _ { t + 1 } ) ( N _ { t + 2 } ) } G ^ { 2 } + \frac { n _ { t } ( N _ { t } + 2 ) + ( n _ { t } + 1 ) ( N _ { t } + 1 ) } { ( N _ { t + 1 } ) ( N _ { t + 2 } ) } ( 1 + g _ { l } ) ^ { - \gamma } G } { ( 1 + g _ { l } ) ^ { - 2 \gamma } + \frac { ( n _ { t } + 1 ) ^ { 2 } } { ( N _ { t + 1 } ) ( N _ { t + 2 } ) } G ^ { 2 } + \frac { ( n _ { t } + 1 ) ( 2 N _ { t } + 3 ) } { ( N _ { t + 1 } ) ( N _ { t + 2 } ) } ( 1 + g _ { l } ) ^ { - \gamma } G }$$

which in general differs from unity. For discounting purposes, the exact sequence of dividend realizations matters. 16This is another important difference between our model and that of David and Veronesi (2000) which assumes multiple states for dividends. In a Lucas-type general equilibrim model this will result in a state-dependent consumption and risk-free rate process. However, David and Veronesi assume that the interest rate is fixed, suggesting that their results are of a partial equilibrium nature.


<!-- p:13 -->


$$D _ { t + v } ^ { j } = ( 1 + g _ { h } ) ^ { j } ( 1 + g _ { l } ) ^ { v - j } D _ { t } \, \left ( j = 0 , 1 , \dots , v \right ) , \, a n d \\ \widetilde { P } _ { t } ^ { B L } \left \{ S _ { t + v } ^ { j } | n _ { t } , N _ { t } \right \} \ = \ \widetilde { P } \left \{ D _ { t + v } ^ { j } | n _ { t } , N _ { t } \right \} & = \beta ^ { v } \left ( \frac { D _ { t + v } ^ { j } } { D _ { t } } \right ) ^ { - \gamma } \times \\ & \times \left ( \begin{matrix} v \\ j \end{matrix} \right ) \frac { \prod _ { k = 0 } ^ { j - 1 } ( n _ { t } + k ) \prod _ { k = 0 } ^ { v - j - 1 } ( N _ { t } - n _ { t } + k ) } { \prod _ { k = 0 } ^ { v - 1 } ( N _ { t } + k ) } \\ \text {Proof. See Appendix A.}$$

Proof. See Appendix A.

Under learning stock prices and beliefs no longer follow a stationary Markov chain, since both the possible rates of change of the stock index and the (perceived) probabilities of these changes follow heterogenous Markov chains. The time-varying transition matrix that determines how the risk-neutral distribution is updated is given by

$$\text {how the risk-neural distribution is updated is given by} \\ \left [ \widehat { R } ^ { B L } \{ X _ { t + k + 1 } = n _ { t } + j | X _ { t + k } = n _ { t } + i \} \right ] & = \widetilde { M } _ { t + k } ( i + 1 , j + 1 ) \\ = & \beta \left [ \begin{array} { c c c } R ^ { l } _ { t + k } ( 1 + g _ { l } ) ^ { - \gamma } \frac { N _ { t + k } - n _ { t } } { N _ { t + k } } & R ^ { h } _ { t + k } ( 1 + g _ { h } ) ^ { - \gamma } \frac { N _ { t + k } } { N _ { t + k } } & \frac { 0 } { N _ { t + k } } & \dots & 0 \\ 0 & R ^ { l } _ { t + k } ( 1 + g _ { l } ) ^ { - \gamma } \frac { N _ { t + k } - n _ { t - 1 } } { N _ { t + k } } & R ^ { h } _ { t + k } ( 1 + g _ { h } ) ^ { - \gamma } \frac { N _ { t + k } } { N _ { t + k } } & \dots & 0 \\ \dots & \dots & \dots & \vdots \\ 0 & 0 & 0 & \dots & 1 \end{array} \right ]$$

where Rt+k ≡ 1+rt+ rt+k is the gross interest rate factor that applies to the low growth state at t+k etc. Computation of the risk neutral probabilities now requires keeping track of the risk-free rate as we move along the dividend tree, reflecting the path-dependence in this variable.

### 5. BS anomalies and learning effects

To better understand the sense in which Bayesian learning can explain the biases in the BS model we establish conditions under which learning systematically affects option prices. Estimation uncertainty reduces the underlying asset price when investors are risk averse, but also increases the asset price through the positive covariance between future asset payoffs and beliefs (πt). When risk aversion is not 'too high'(γ &lt; 1) the second effect dominates. A similar ranking across asset prices can be established by comparing option prices under learning to BS option prices:

Proposition 5 If the mean dividend growth rate is nonnegative and investors have optimistic beliefs (πt ≥ π) then

$$C _ { t } ^ { B L } ( K ) \geq C _ { t } ^ { B S } ( K ) \ \forall K .$$


<!-- p:14 -->


Proof. See Appendix A.

One can show that the difference between the call option price under Bayesian learning and under full information is positive for a zero strike price, increases over some interval of strike prices and then decreases towards zero. Figure 4 provides an example. Optimistic beliefs (πt &gt; π) are suffcient for the difference between option prices CBL(K)–CBS(K) to be monotonically increasing for low strike prices. For unrestricted beliefs πt, there will be intervals for the strike price over which CBL(K) ≥ CBs(K) and others over which this inequality is reversed. For instance, pessimism makes it more likely that out of the money calls be underpriced under BL relative to BS; however, the mean preserving spread caused by the presence of learning effects keeps assigning positive valuation to deep out of the money calls that otherwise receive near-zero prices under BS. Furthermore, although optimistic beliefs are sufficient, they are not a necessary condition for learning to systematically affect option prices. Numerical results confirm that even when πt ≤ π, provided that π − πt is not too large, it is possible to obtain CBL(K) ≥ CBs(K) for many configurations of the remaining parameters.

Guidolin and Timmermann (2001) show that in this setup the price-dividend ratio is a monotonically increasing and convex function of beliefs, πt. The intuition is that the presence of learning effects shifts risk-neutral probability mass towards the tails relative to the lognormal benchmark underlying BS. In general, this could either depress or increase the equilibrium price of a call option. However, optimistic beliefs are sufficient to guarantee that the mass shifted towards the right tail dominates the mass shifted towards the left tail. Also, because of the selfenforcing effects of dividend changes, learning in a lattice framework widens (in both directions) the support of the perceived risk-neutral distribution of time t + τ stock prices relative to the lognormal case. Convexity of the pricing kernel guarantees that this effect increases the equilibrium option price.

Effectively the cross-section of option prices allows us to infer the market's perception of fundamentals once the model is tested on option data. For instance, market prices for European calls systematically above BS predictions and a 'smiling' implied volatility shape would suggest strong learning effects and that investors are somewhat optimistic.

Ultimately an analysis must consider whether the Bayesian option pricing model can replicate the data in Section 2. To investigate this, we set the parameters of the dividend process and the risk-free rate at plausible levels. Dividends are assumed to be paid out daily (m = 1). For a wide market index such as the S&amp;P 500 this provides a fairly good approximation. The annual dividend growth rate (μ) is set to 3%, to match the average dividend growth rate around r s %  s  (  .( o -     h ally.17 Finally the annualized risk-free rate (r) is set to 4%, while the dividend yield is fixed at Figures 5 and 6 plot implied volatilities as a function of moneyness for the April 1993 maturity. These are representative of what we have found in other sub-periods of our sample. Comparing the left and right windows, the resemblance between the implied volatility under learning and observed market values is striking. The lattice model under Bayesian learning appears to price options far more accurately than the BS model.


<!-- p:15 -->


To further underline this point, Figure 7 compares observed option prices on February 22, 1993 and BL prices assuming nt = 43, Nt = 80 (πt = 0.538). The fit is even more striking than in Figure 6 and is indicative of the ability of the model to fit implied volatility skews. Assuming that the markets really were on a Bayesian learning path on that day, the estimate πt = 0.538 with a precision of Nt = 80 seems to accurately characterize investors' beliefs.

#### 5.2. State Price Densities

Systematic differences between BS and BL European option prices must reflect differences in the underlying equivalent martingale measures employed by the market under the two alternative models or, equivalently, in the SPDs (cf. Harrison and Kreps (1979)). Learning affects state price densities in two distinct ways: (i) the SPD perceived by investors changes; (ii) the support of the set of time t+T equilibrium stock prices is widened. If the initial beliefs on π are unbiased, extreme events drawn from either end of the tail are perceived as more likely on a Bayesian learning path than under a lognormal distribution. Likewise, a wider support for the SPD also means that more extreme events now become possible.

When πt decreases towards π from above, BL continues to inflate the tails of the SPD perceived by the investors relative to the lognormal benchmark thus creating an implied volatility skew. This matches the stylized facts of the S&amp;P 500 option data that densities are located more to the right than the lognormal benchmark but also attach positive probability mass to some crash events. Figure 8 shows that, consistent with the data in Section 2, Bayesian learning produces SPDs that are skewed to the right and have fatter tails than a lognormal.

#### 5.3. Term Structure of Implied Volatilities

Next we vary the time to maturity (τ) from 10 to 150 days in steps of 10 days to study the implied volatility term structure resulting from Bayesian learning. Figure 9 shows the outcome of this exercise for three sets of strike prices: K = 420 (moneyness 1.04), K = 435 (moneyness 1), and K = 455 (moneyness of 0.96). Bayesian learning generates an upward sloping term structure for at-the-money and out-of-the money call options, while the term structure at first decreases and then increases for in-the-money call options. These patterns are broadly consistent with what was found in the data, cf. Figure 2. The increase of about 2 percentage points in implied volatility between close-to-expiration options and long-term options is also plausible.20 Figure 10 presents both dimensions of the implied volatility surface under BL. Skews dominate at all maturities, with exception of very short term options, for which an asymmetric smile obtains. While for OTM and ATM contracts the term structure is upward sloping, a richer variety of shapes obtains for ITM contracts.


<!-- p:16 -->


#### 5.4. Vanishing learning effects

In our setup investors use a consistent estimator of π, and as Nt → ∞, πt → π and learning effects vanish. To study the consequence of this, we double the precision of investors' beliefs with respect to the experiments performed in section 5, keeping the mean constant, i.e. nt = 182 and Nt = 350. The representative agent now brings experience of over 16 months of trading and dividend realizations. Figure 11 shows the resulting option prices.

When learning effects are weak and investors have a more accurate estimate of π, BL option prices converge to BS prices. This is not surprising since learning is the only source of nonstationarity in our model. The first panel of Figure 11 shows that differences previously of the order of 1-2 dollars, now decline to a quarter of that range. Panels two and three show that BL implied volatilities continue to display a systematic pattern over moneyness, although the implied volatility surface is flatter than the one exhibited in Figure 6. As Nt → ∞ and πt → π (from above) a smile is obtained instead of the smirk in figure 6. This indicates that at times when option markets are characterized by smiles, learning effects are weak in the sense that investors attach high precision to their initial beliefs. Smirks, on the other hand, are indicative of markets with strong learning effects and uncertain beliefs. Finally, the fourth panel shows that the SPD converges to the log-normal distribution.21

To ensure that learning effects do not disappear asymptotically, one can simplify the learning model to assume that the markets use a rolling window of the data to estimate π. This guarantees that the markets will not obtain an infinite precision of the fundamentals parameters as the sample grows. This is also consistent with widespread market practice and is a way of robustifying the estimate of π with respect to slowly moving non-stationarities in the fundamentals process. An additional benefit from this assumption is that we can deduce from the options price data the effective memory (or window length, Nt) applied by the market, which is of separate interest. In practice, the use of a rolling window of observations has two oned omu o  n  s   :s  so o ver

20See Campa and Chang (1995).

21We omit the discussion of the impact of a large Nt on the volatility term structure. Though the patterns are unchanged, the implied volatility curves get flatter and their level moves down towards the BS value. Nevertheless, a precision, Nt, in excess of 16 months of observations implies effects that are still close to those observed in the data.


<!-- p:17 -->


π based only on the most recent R observations, where R is the length of the rolling window, ∑j=t-R+1 R πt {9t+j=9h} (assuming R &lt; t). There is a second and subtler implication: R R When agents form perceptions of the probability distribution of future dividend levels on the binomial lattice, they have to integrate over all the possible future perceptions of πR, accounting for the fact that moving into the future they will have to keep rolling the window of observations used in the estimation, replacing past observations with future realizations. The resulting formula to calculate the perceived probability distribution over future dividend levels is:

$$\text {for} \quad & \text {calculate the perceived probability distribution over future derived levels is:} \\ & \quad \Pr _ { t } R ^ { W } \left \{ D _ { t + i | n } ^ { j } R , R \right \} = \frac { 1 } { R ^ { i } } \sum _ { l = 1 } ^ { ( i ) } \left \{ \left [ I _ { \{ g _ { l + 1 } = g _ { n } \} } ^ { j } n _ { t } ^ { R } + \left ( 1 - I _ { \{ g _ { l + 1 } = g _ { h } \} } \right ) ( R - n _ { t } ^ { R } ) \right ] \times \\ & \quad i \sum _ { k = 2 } ^ { i } I _ { \{ g _ { t + k } = g _ { h } \} } \left ( n _ { t } ^ { R } + \sum _ { s = 1 } ^ { k - 1 } I _ { \{ g _ { t + s } = g _ { h } \} } ^ { R } - f _ { k } \right ) + \left ( 1 - I _ { \{ g _ { t + k } = g _ { h } \} } \right ) \left ( R - n _ { t } ^ { R } - \sum _ { s = 1 } ^ { k - 1 } I _ { \{ g _ { t + s } = g _ { h } \} } + f _ { k } \right ) \right ] \right \} \\ & \quad \exp ( 1 - \sum _ { k = 2 } ^ { k - 2 } I _ { \{ g _ { t } = 0 \} } ) .$$

Σs=0 I{gt-N+s=9h} is a forget factor' that counts the number of times in which dividends grew at a high rate between t − R and t − R + k − 1. Notice that the summation (j) iterates over all of the independent paths leading to the same final dividend level Dt t+i, 0 ≤ j ≤ i, with l indexing each of these paths. Indeed, the simple binomial coefficient (j) in (j) Proposition 3 is now replaced by Σ=1 . However, although its theoretical limiting properties are interestingly different, as long as the rolling window is not too small, the Bayesian model described in Section 4 will provide a good approximation to an exact solution which explicitly incorporates investors' use of a rolling window.22

### 6. Option price dynamics and learning effects

Thus far we have studied the ability of the BL model to match typical cross-sections of option prices at a point in time. However, the Bayesian updating algorithm implies a set of dynamic restrictions on how implied volatility surfaces and term structures evolve over time as investors update πt. Such testable restrictions do not have a counterpart in the BS model which does not consider the effect of changing probability beliefs. By tracking option prices on several consecutive days, not only do we get insights into how investors change their beliefs but we also get a more precise estimate of the initial beliefs.

Estimating the dynamics of beliefs from observed option prices is a new exercise that needs to be put in perspective. When asset markets are (dynamically) complete, equilibrium asset prices contain information about preferences and beliefs. Rubinstein (1985) observes that any pair of the following implies the third: (1) the preferences of a representative agent; (2) agents' beliefs; and (3) the state-price density (SPD). A vast literature has attempted to use the observed prices of risky assets to infer preferences, the stochastic process of prices, or both. For instance, Bick (1990) and He and Leland (1993) impose parametric restrictions on the generating process of asset prices and infer the preferences of a representative agent. Rosenberg and Engle (1997) develop a nonparametric estimator of the empirical pricing kernel which is based on the ratio of the estimated state prices and the estimated physical (objective) probability beliefs defined on a discrete grid of possible future returns. They use their pricing kernel estimates to document time-variation in the risk attitudes of the market. Furthermore, Bates (1991), Jackwerth and Rubinstein (1996), and Ait-Sahalia and Lo (1998) back out the perceived risk neutral stochastic process of asset prices from observed option prices.

22Simulation experiments (approximating rolling window option prices with Monte Carlo techniques) confirmed that for the values of Nt typically encountered in our sample, namely around 300 observations, the Bayesian price under an expanding and a rolling window were quite similar.


<!-- p:18 -->


Bayesian learning provides an as far unexplored possibility to expand Rubinstein's list to a fourth and separate item: the dynamics of the learning process followed by a representative agent in an equilibrium model. As in Rubinstein (1994) and Jackwerth and Rubinstein (1996), we fix preferences and infer a vector of unknown parameters from observed option prices. Since the dynamics of beliefs on a learning path determine the evolution in the SPD and therefore also option prices, the parameters on the entire learning path can be backed out from the following general program23

$$\text {eral program} ^ { 2 3 } \\ \min _ { \{ \pi _ { t } \} _ { 1 } ^ { T } = 1 , N , m } \sum _ { t = 1 } ^ { T } \sum _ { \tau = \underline { \tau } _ { t } } \sum _ { K _ { \tau , t } = \underline { K } _ { t } } ^ { \overline { K } _ { \tau } } g \left ( C ^ { B L } ( f _ { t } , \pi _ { t } , N , m ; \gamma , \beta ) , C ( f _ { t } ) \right ) \\ s . t . \quad \frac { \pi _ { t } N } { N + m } \leq \pi _ { t + 1 } \leq \frac { \pi _ { t } N + m } { N + m } \\ 0 \leq \pi _ { t } \leq 1 \quad t = 1 , \dots , T \\ N > 0 , \quad m > 0 \\$$

where ft = [t Kτt St rt]' denotes the option contract features and the underlying asset price, St, which we condition on, CBL(ft, N, m; γ, β) is the theoretical price of the call option on s             (f r   t expiring in τt days. The indexes appended to τt and Kτt reflect the fact that maturities and strike prices change over time, following the dynamics of the underlying price and the financial cycle. The first constraint arises from the fact that when dividends change m times in a unit interval, πt can be updated to any value between πtN (when dividends grow m times at the N+m rate gl) and πtN+m (when dividends grow m times at the rate gh). Finally, g(·) is a function N+m that measures the distance between the observed and theoretical option price. For instance, we might minimize the sum of squared pricing errors across days, strikes or maturities.

23Our approach is similar to Bates (1991), who imposes CRRA preferences to estimate by NLS the parameters os  s    u se re ro


<!-- p:19 -->


Again we assume that the annual volatility of the fundamentals, σ, is 5%. Given σ, gh and gl can be determined from Proposition 3. We set γ = 0.9 and β = 1 ≈ 0.98 on an annual 1.02 basis. These choices are based either on the features of our data on the S&amp;P 500 index and index options, or on what seems a priori plausible.

The estimation procedure provides an estimate  which represents how much precision the market assigns to its initial beliefs, an estimate î of the frequency with which these beliefs are updated over the sample period,24 and a T × 1 vector π whose dynamics is constrained by Bayes rule. /m can also be interpreted as an estimate of the length of the time window investors use to form their beliefs about fundamentals. For instance, if news on fundamentals arrive every three days (m = ) and  = 300, this implies that agents are using a data window of 900 days.

#### 6.1. Inferring learning from daily cross-sections

The objective of our first exercise is to infer from option prices the belief, πt, its precision level, Nt, and the frequency with which beliefs are updated and new information arrives, mt, for each week in the sample:

$$\min _ { \pi _ { t } , N _ { t } , m _ { t } } \sum _ { \tau = \underline { \tau } _ { t } , \, K _ { \tau _ { t } } = \underline { K } _ { \tau _ { t } } } \sum _ { \tau = \underline { K } _ { t } , \, K _ { \tau _ { t } } = \underline { K } _ { \tau _ { t } } } \left [ C ^ { B L } ( f _ { t } , \pi _ { t } , m _ { t } , N _ { t } ) - C ( f _ { t } ) \right ] ^ { 2 }$$

for t = 1, 2, ..., T. This amounts to minimizing the in-sample squared pricing errors produced by the model for each weekly cross-section of option prices. πt, Ñt, and mt can be viewed as non-standard NLS estimates.25 The problem is solved by a combination of grid search and a polytope method, details of which are provided in Appendix B.

This exercise ignores the intertemporal restrictions imposed by our model on the updating of investors' beliefs and therefore does not provide the strongest possible test. We do not rule out large changes across days in the estimated belief πt or unbounded variation in the estimated precision level Ñt. On the other hand, the exercise is quite simple, requiring the estimation of only three parameters on a data set with a cross-sectional size equal to the number of traded contracts on week t. Furthermore, this setup is fully consistent with the presence of infrequent and unpredictable structural breaks in the distribution of the fundamentals (cf. Section 5.4). Ît then represents an estimate of the size of the window used by the market at time t to form its estimate of πt. When structural breaks are assessed to occur more frequently, the optimal reaction is to shorten the time window of observations used for estimation purposes, and vice versa. This is also our rationale for allowing sizeable jumps' in πt, since changing the size of the observation window can have quite a strong impact on the resulting estimate of π, especially when beliefs on the frequency of breaks are drastically revised.

24The perceived frequency of dividend news, m, is another structural parameter that agents are unlikely to know. In reality investors will probably use an estimate of its most likely value, î. Also, we refer to m as a number of the form m = d, d ∈ N, i.e. a rational number and not necessarily an integer. m &lt; 1 (d &gt; 1) would then imply that news are perceived to hit the market every d periods, on average. For instance î = 1 implies that news on fundamentals are perceived to arrive every two days.

25The problem is nonstandard both because of the presence of constraints on the parameters and because Nt is a positive integer while mt has structure à, where d ∈ N. As far as the metric g(·) is concerned, we tried to estimate the six competing models listed below by minimizing instead the sum of squared implied volatility errors, i.e. deviation of theoretical implied volatilities from the empirical implied volatilities underlying observed prices. We obtain in-sample results roughly similar to the one presented below.


<!-- p:20 -->


To better gauge the plausibility of the learning path implied by S&amp;P 500 option prices, our empirical tests compare the relative performance of the BL model to the following alternatives:

$$( i ) \ B S \colon \ C ^ { B S } ( f _ { t } ; \hat { \sigma } _ { t } ) ,$$

where ôt is the implied volatility that minimizes the sum of the squared deviations

$$\sum _ { \tau _ { t } = \mathcal { I } _ { t } } ^ { \bar { \tau } _ { t } } \sum _ { K _ { \tau _ { t } } = \underline { K } _ { \tau _ { t } } } ^ { \overline { \overline { K } } _ { \tau _ { t } } } \left [ C ^ { B S } ( f _ { t } ; \hat { \sigma } _ { t } ) - C ( f _ { t } ) \right ] ^ { 2 } \quad s . t . \ \hat { \sigma } _ { t } > 0 , \ t = 1 , \dots , T$$

ôt is the implied volatility estimated from the cross-section of option prices at t.

The second model is Black-Scholes generalized to allow the volatility input to depend on the moneyness of the priced option, that is, a BS with a step-wise modification to accommodate the 'smile' bias along moneyness:

$$( i i ) \ B S ( m ) \colon C ^ { B S } ( f _ { t } ; \hat { \sigma } _ { K _ { \tau _ { t } } } )$$

where ôKτt = {KIT,  KATM, KOTM is a volatility index function of moneyness.26We allow Tt Tt ôK to take three separate values depending on the moneyness of the option. A contract is ITM if moneyness is above +2%, it is ATM is moneyness is between -2 and +2%, and it is OTM if moneyness is below -2%. The three volatility indices are chosen to minimize the sum of squared deviations

$$\sum _ { \tau _ { t } = \underline { \mathcal { I } } _ { t } , \, K _ { \tau _ { t } } = \underline { K } _ { t } } \sum _ { \sigma _ { t } } ^ { \overline { \tau } _ { t } } \left [ C ^ { B S } ( f _ { t } ; \hat { \sigma } _ { K _ { \overline { t } } ^ { M o n } } ) - C ( f _ { t } ) \right ] ^ { 2 } \quad s . t . \ \hat { \sigma } _ { K _ { t } ^ { M o n } } > 0 \\ \hat { \sigma } _ { K _ { t } ^ { M o n } } = \left \{ \hat { \sigma } _ { K _ { \overline { t } } ^ { T M } } , \hat { \sigma } _ { K _ { \overline { t } } ^ { A T M } } , \hat { \sigma } _ { K _ { \overline { t } } ^ { T M } } \right \} .$$

26Moneyness is defined as 100 Ft.T -1 ) , where K is the strike price and Ft,τ is the price of a futures contract K expiring at τ.


<!-- p:21 -->


The third model is a Black-Scholes formula generalized to allow the volatility input to depend on the time-to-maturity of the priced option:

$$( i i i ) \ B S ( \tau ) \colon C ^ { B S } ( f _ { t } ; \hat { \sigma } _ { \tau _ { t } ^ { M a t } } ) ,$$

where ôτMat = ô is a volatility index function of time-to-maturity which reflects whether the option is close-to-expiration (less than 40 calendar days to expiration), medium term (between 40 and 70 days to maturity), or has a long (more than 70 days to expiration) time-to-expiration. The parameters are chosen to minimize the sum of squared deviations

$$\sum _ { \tau _ { t } = \tau _ { t } } \sum _ { K _ { \tau _ { t } } = K _ { \tau _ { t } } } \frac { \overline { K } _ { \tau _ { t } } } { \sum _ { \tau _ { t } = \tau _ { t } } } \left [ C ^ { B S } ( f _ { t } ; \hat { \sigma } _ { \tau _ { t } } M a t ) - C ( f _ { t } ) \right ] ^ { 2 } \quad s . t . \ \hat { \sigma } _ { \tau _ { t } } M a t > 0 \\ \hat { \sigma } _ { \tau _ { t } } M a t = \left \{ \hat { \sigma } _ { \tau _ { t } } ^ { \ } s h o r t , \hat { \sigma } _ { \tau _ { t } } ^ { \ } m e d , \hat { \sigma } _ { \tau _ { t } } ^ { \ } l o n g \right \} .$$

The fourth model we consider is a deterministic volatility BS model modified to allow σ to be quadratic in strikes (to obtain smile shapes) and linear in time-to-maturity:27

$$( i v ) \ B S { - s p l i n e } \colon \ C ^ { s p l i n e } ( f _ { t } ) = C ^ { B S } ( f _ { t } ; \sigma ^ { s p l i n e } ( \tau _ { t } , K _ { \tau } ) ) \\ \sigma ^ { s p l i n e } ( \tau _ { t } , K _ { \tau _ { t } } ) = \max \left \{ . 0 1 , \alpha _ { 0 } + \alpha _ { 1 } K _ { \tau _ { t } } + \alpha _ { 2 } K _ { \tau _ { t } } ^ { 2 } + \alpha _ { 3 } \tau _ { t } + \alpha _ { 4 } K _ { \tau _ { t } } ^ { 2 } \tau _ { t } \right \}$$

For each sample day we fit a model for the volatility surface σspline(τt, Kτt) by solving:

$$\min _ { \alpha _ { t } } S S R ( \alpha _ { t } ) \equiv \sum _ { \tau _ { t } = \mathcal { T } _ { t } } ^ { \overline { \tau } _ { t } } \sum _ { K _ { \tau _ { t } } = \underline { K } _ { \tau _ { t } } } ^ { \overline { K } _ { \tau _ { t } } } \left [ \sigma ^ { s p l i n e } ( f _ { t } ; \alpha _ { t } ) - \sigma _ { I } ( f _ { t } ) \right ] ^ { 2 }$$

where σ1 denotes observed market implied volatilities (calculated by inverting the BS formula). We then plug the estimated t into BS to obtain option prices. Notice that although similar in spirit, (13) differs from models two and three because it is fitted to the implied volatility surface and not to observed option prices.

Finally, we estimate Heston and Nandi's (2000) NGARCH(1,1) model on the sequence of weekly cross sections of option prices. Assume that the continuously compounded returns on the underlying asset follow a nonlinear asymmetric GARCH (1,1)-in-mean process over time steps of fixed length equal to one day:

$$r ( t ) \ = \ r ^ { f } + \lambda h ( t ) + \sqrt { h ( t ) } z ( t )$$

$$h ( t ) \ = \ \omega + \alpha \left [ z ( t - 1 ) - \xi \sqrt { h ( t - 1 ) } \right ] ^ { 2 } + \phi h ( t - 1 ) ,$$

27This echoes the "ad hoc strawman" model of Dumas et al. (1998, pp. 2085-2087) who argue that market makers simply smooth the implied volatility surface using polynomials and predict option prices by using a BS in which σ is a function of the strike and maturity.


<!-- p:22 -->


where r(t) ≡ ln S(t) − ln S(t − ∆), rf is the continuously compounded and constant risk-free interest rate, z(t) ∼ N(0, 1), and h(t) is the volatility of the underlying daily returns for the time interval [t − 1, t) conditional on the information available at time t — 1. Let

$$z ^ { * } ( t ) = z ( t ) + \left ( \lambda + \frac { 1 } { 2 } \right ) \sqrt { h ( t ) } \quad \text {and} \quad \xi ^ { * } = \xi + \lambda + \frac { 1 } { 2 } .$$

Substituting these definitions into (15) - (16) we obtain:

$$r ( t ) \ = \ r ^ { f } - \frac { 1 } { 2 } \sqrt { h ( t ) } + \sqrt { h ( t ) } z ^ { * } ( t )$$

$$h ( t ) \ = \ \omega + \alpha \left [ z ^ { * } ( t - 1 ) - \xi ^ { * } \sqrt { h ( t - 1 ) } \right ] ^ { 2 } + \phi h ( t - 1 ) .$$

variance ht. Under assumptions ensuring that a call option with one period to expiration satisfies the Black-Scholes formula (see, e.g., Duan (1995)), Heston and Nandi (2000) show that a local risk neutral probability measure Q exists, that it is unique and that it is characterized by another NGARCH (1,1) process with EQ [rt|Φt−1] = rf − ψht. They also show how to solve for the conditional generating function ft(φ) of the final spot price ST under the process in (15) - (16) using the method of undetermined coefficients.28 The current equilibrium price of a call option with strike K and τ periods to maturity can be calculated by inverting the risk neutral conditional characteristic function ft (iφ) according to the formula:

$$P _ { K } ^ { * } = F ^ { * } ( \ln K ) = \frac { 1 } { 2 } + \frac { 1 } { \pi } \int _ { 0 } ^ { \infty } R e \left [ \frac { e ^ { - i \phi \ln K } f _ { t } ^ { * } ( i \phi ) } { i \phi } \right ] d \phi ,$$

We can therefore write our final benchmark model as follows:

$$( v ) \ N G A R C H ( 1 , 1 ) \colon C \left ( S _ { t } , \tau , K ; \omega , \alpha , \phi , \xi , \theta \right ) = S _ { t } P _ { S } ^ { * } - e ^ { - r ^ { f } \tau } K P _ { K } ^ { * }$$

where 1

$$w h e r e \ P _ { S } ^ { * } = \frac { 1 } { 2 } + \frac { 1 } { \pi } \int _ { 0 } ^ { \infty } R e \left [ \frac { e ^ { - i \phi \ln K } f _ { t } ^ { * } ( i \phi + 1 ) } { i \phi f _ { t } ^ { * } ( 1 ) } \right ] d \phi .$$

28 ft(φ) is log-linear with coefficients that depend on the parameters θ, ω, α, φ, and ξ. These coefficients can be calculated in a recursive fashion starting from the terminal conditions where all of the coefficients must equal

29Our implementation follows the same procedures detailed in the paper by Heston and Nandi. We (i) use ( +     ( using the time series of index returns over the previous 252 days.


<!-- p:23 -->


#### 6.2. Goodness-of-fit Measures

To measure the fit of any given option pricing model, Î(ft), we adopt four indicators. The first is the average root mean squared valuation error (RMSVE),

$$& \text {is the average root mean squared validation error} \left ( R M S V E \right ) , \\ & \quad R M S V E \ = \ T ^ { - 1 } \sum _ { t = 1 } ^ { T } \left \{ W _ { t } ^ { - 1 } \sum _ { \pi _ { t } = K _ { t } } ^ { \overline { \tau } _ { t } } \left [ \widehat { C } ( f _ { t } ) - C ( f _ { t } ) \right ] ^ { 2 } \right \} \\ & = \ T ^ { - 1 } \sum _ { t = 1 } ^ { T } \left \{ W _ { t } ^ { - 1 } S \widehat { S } R _ { t } ^ { M } \right \} ^ { 1 / 2 } \\ \intertext { w h e r $ W _ { t } \, \text { measures the total number of contracts for which prices were available as of week $ t$} }$$

where Wt measures the total number of contracts for which prices were available as of week t.

Likewise, we consider the average mean absolute valuation error (MAVE),

$$M A V E = T ^ { - 1 } \sum _ { t = 1 } ^ { T } W _ { t } ^ { - 1 } \sum _ { \tau _ { t } = \overline { \tau } _ { t } } ^ { \overline { \tau } _ { t } } \sum _ { K _ { \tau } = \overline { K } _ { \tau } } ^ { \bar { K } _ { \tau } } \left | \widehat { C } ( f _ { t } ) - C ( f _ { t } ) \right | .$$

To assess the potential for overfitting, we report Akaike's information criterion (AIC),30

$$A I C = T ^ { - 1 } \sum _ { t = 1 } ^ { T } \left [ - 2 \ln L ( \hat { \theta } _ { t } ) + 2 p \right ] ,$$

where p is the number of parameters estimated for a given model and L(θt) is its likelihood. This criterion trades off fit, as measured by L(t), against parsimony.

Finally, we follow Dumas et al. (1998) and calculate the mean absolute error outside the bid-ask spread (MOE):31

$$M O E = \max \left \{ \max [ \widehat { C } ( f _ { t } ) - C ^ { a } ( f _ { t } ) , 0 ] , \max [ C ^ { b } ( f _ { t } ) - \widehat { C } ( f _ { t } ) , 0 ] , 0 \right \} .$$

According to this definition, MOE &gt; 0 if and only if either the theoretical option price exceeds the ask price (Ca(ft)) or the theoretical option price is below the bid quote (Cb(ft)).

To compare the results across models, we also report the proportion of weeks in the sample for which a given model displays the lowest value of a particular performance measure. This is also done to avoid situations where a certain model dominates most of the time, although its average performance is very poor as a result of a few days with extreme performance.

30For simplicity, we call θ the vector of parameters to be estimated with reference to any possible pricing model

M. For instance, in the case of model 4, θ = α, for the BL model θ = [πt Nt mt]′, and for the variants on the BS model θ collects the contract-specific volatility parameters.

31Our definition differs from that in Dumas et al. (1998, p. 2072) since our MOE ≥ 0, while their measure can be either positive or negative. We want MOE to be able to detect all situations where the theoretical option price falls outside the bid-ask spread and thus do not distinguish between cases where the price is too low and cases where it is too high.


<!-- p:24 -->


Table 2 contains the in-sample averages of RMSVE, AIC, and MAVE across the 292 weeks during the period June 1988 - December 1993. On average, and across the different measures of goodness-of-fit, the BS - spline model seems to outperform all alternatives, followed by the NGARCH model and the BL model.32 Although the average distance between the BL model and BS-spline is not excessive (less than 10 cents when measured by the RMSVE), the AIC estimates suggest that the larger number of parameters of the BS-spline model does not completely explain its superior performance. At the same time, our weekly implementation of the BL model leads to an improvement of 78 cents over Black-Scholes. Though far from being the best fitting model in-sample, the BL approach provides quite precise estimates of option prices, often inside the bid-ask spread. Indeed the MOE of the BL model (35 cents on average) is quite close to the BS-spline minimum of 30 cents and better than any of the other competing models.

Following Dumas et al. (1998), these performance indicators are broken down according to both moneyness and the time-to-expiration of each traded contract. Interesting information can be extracted when the goodness-of-fit indicators are decomposed according to either moneyness or time-to-maturity (Panels B and C). The BL model fits as well as the BS-spline for ATM contracts. For these contracts, BL has a much lower MOE than BS-spline, signalling that the latter — although surely superior on average — can also lead to gross mispricings outside the bid-ask spread for these options. While the NGARCH model is particularly effective at pricing ITM contracts, BS and its variants BS(τ) and BS(m) only provide good in-sample fits for short-term options.

Table 3 presents summary statistics for the parameter estimates obtained for the five models. While BS and BS(m) are characterized by estimated volatilities that are quite stable over time, the same cannot be said for the estimates under BS(τ) and BS — spline. For the latter two models the SPD implied by the estimates also shows significant instability. In the case of the BL model, while the πt and Nt estimates are quite stable, there is more variation in the estimate of the rate of information arrival mt.

To get a better impression of parameter stability for the different models, Figure 12 shows the time series of the estimated parameters for BS, BS - spline, and BL. The constant volatility assumption underlying BS is clearly rejected as volatility varies systematically over time. On some days ôt changes by several percentage points. Likewise, the intercept and coefficients associated with K and K2 in the BS - spline model fluctuate widely from one week to the next. The case of highest instability concerns the NGARCH model, as already reported by Heston and Nandi (2000, p. 605). In particular, the estimates of ξ and φ oscillate dramatically: while  is frequently observed to approach extreme values such as 0 and 1, ξ even switches sign, thus implying the occasional presence of a negative leverage effect that could be associated with atypical shapes of the implied volatility surface. This instability must be carefully considered when evaluating the out-of-sample performance of the NGARCH model. In all cases, such sharp revisions in the parameter estimates suggest significant instability in the implied volatility surface. The BL model generates relatively stable parameter estimates, with πt steadily in the range of [.52, .65], t normally around 300 observations, and ît most of the time in the narrow interval [.3, .5]. The speed of flow of information seems to peak in the first months of 1991 in correspondence with the recovery of the US economy from the recession of 1990.33 In general option markets display weak optimism (πt ≥ 1). The stability of the parameter estimates suggests a relatively smooth evolution in the market's learning.

32This finding differs slightly from Heston and Nandi's (2000) result that the NGARCH(1,1) model outperforms tit      t  i  i  -e  ie   -p dta selection procedures.


<!-- p:25 -->


#### 6.3. Out-of-sample predictions

The true economic and statistical value of a good option pricing model depends not on its insample fit, which will uniformly improve as more parameters are introduced, but on the precision with which the model predicts future option prices out-of-sample. Moreover, despite the superior in-sample fit of the BS-spline and NGARCH models uncovered in the previous subsection, we also found some results that are potentially problematic for their empirical performance, such as the instability of the parameter estimates and the large MOEs. We therefore extend the previous analysis and report statistical measures of out-of-sample prediction performance. Subsequently we report the hedging performance to measure the economic tracking errors of the models.

For each week t in the sample we estimate the relevant vector of parameters t in the manner described above and then use this to forecast the cross-section of option prices on the following trading week.34

Table 4 provides summary statistics for the one-step-ahead prediction errors. Unsurprisingly, these are somewhat larger than the errors in Table 2. Out-of-sample, the BL model outperforms the proposed alternatives in the aggregate (Panel A), albeit only marginally in the case of the BS-spline model. The root mean squared prediction error of the BL model is 1 dollar against 1.68 dollar for Black-Scholes and 1.06 dollars or higher for the empirical modifications to BS. The NGARCH does relatively poorly, outperforming Black-Scholes (by 42 cents) but also predicting with average errors 16 cents larger than BL. In relative RMSPE terms, BL is the best model out-of-sample in 35% of the sample weeks. The superior forecasting performance of the BL model suggests that this model does not provide an accurate fit purely as a result of weekly variation in the learning parameters. On the other hand, it is natural to attribute the relatively weaker predictive performance of the BS-spline and NGARCH models to their parameter instability. When the forecast indicators are decomposed according to either moneyness or time-to-maturity (Panels B and C), we get a better picture of the relative strengths of the BL model: It outperforms the other benchmarks for OTM contracts and always compares closely with the best performing alternative models across moneyness and maturity levels.

33Since m is on average around 0.3,  = 300 corresponds to about 1000 trading days, i.e. 4 years. t and mt also have a high positive correlation (0.55) so the actual size of the data window implied by the estimates displays low volatility and for most of the sample period lies between 800 and 1,100 observations.

34When forecasting option prices one-step ahead, we follow Dumas et al. (1998) and condition on the stock index level and the risk-free rate at close of the following week. This way we test the predictive properties of the option pricing models independently of the ability to predict the future stock price.


<!-- p:26 -->


#### 6.4. Hedging performance

A common economic measure of the precision of an option pricing model is its ability to assist in setting up a hedge against changes in the value of the underlying asset. Such a delta hedge is attained by selling short an amount (ft; θt) of the stock index, where ∆ measures the sensitivity of the option price to the value of the underlying asset. (ft; t) is model dependent and an option pricing model performs well if it allows accurate calculation of △(ft; θt) over time. Allowing for possible misspecification in the option model, the dollar return on the delta neutral position in excess of the risk-free rate can be shown to be:

$$\eta _ { t + 1 } ( \hat { \theta } _ { t } ) = \Delta C _ { t + 1 } - \widehat { \Delta } C _ { t + 1 } ( \hat { \theta } _ { t } )$$

which is the difference between the change in the actual price of the call minus the change predicted by the model based on the estimated vector of parameters t. A good model should reduce the excess returns from hedging to zero since ηt(θt) ≠ 0 can result from misspecification. This is the same concept of error from a delta-hedging strategy used by Dumas et al. (1998, 2088-2089).

Table 5 reports statistics on hedging errors. Results are quite similar to the out-of-sample prediction experiments, in the sense that the BL model still outperforms all the proposed and (ii) the risk-free interest rate (from proposition 3). Figure 13 reports the two time series. Overall, the implied path for these variables is quite plausible and consistent with an economy moving through a slow learning path.


<!-- p:27 -->


The expected rate of growth of fundamentals is 5% per annum on average. This is higher than the average rate of growth of real dividends (2.2%) reported by Shiller (2000) for the period 1988-1993. However the dynamics over time of the implied expected fundamental growth fits the NBER business cycles dates quite well. For instance, the average expected growth rate is 7.4% for the period June 1988 - July 1990 and then declines to a modest 3.5% for the period August 1990 - December 1993, which contains the last recorded recession of 1990-1991.35 Moreover, the high average might be related to the high growth rates observed by agents on a learning path over the expansion period 1983-1989 (3.9%), in the sense that agents' beliefs might have adjusted slowly to the incipient recession and the exogenous uncertainty related to the Gulf War. Although the expected growth rate implied by the BL model is never negative, consistent with beliefs that the US economy is growing in real terms, annualized growth rates of real dividends as high as 9% appear in Shiller's data.

Another implied series that gives positive indications on the robustness of the BL model is the riskfree interest rate. Its average is 6.4% vs. a sample value of 5.6% for the 1988-1993 period. The implied interest rate appears to decline over time, consistent with the evidence and with the evolution in the US business cycle during our sample. The model also produces a time-series standard deviation of the risk-free rate (2.3%) that fits well with the sample value of 2.1%.

#### 6.6. Learning dynamics with an expanding window

The empirical exercise of the previous subsections ignores the intertemporal restrictions imposed by our model on the updating of investors' beliefs and therefore does not provide the strongest possible test. Therefore we try next to infer the dynamics of learning from observed option prices by imposing these restrictions on πt. The model in section 4 assumes that beliefs evolve as follows:

$$\widehat { \pi } _ { m ( t + k ) + j } = \widehat { \pi } _ { m ( t + k ) + j - 1 } + \frac { I _ { \{ m ( t + k ) + j = g _ { h } \} } - \widehat { \pi } _ { m ( t + k ) + j - 1 } } { N _ { m ( t + k ) + j } } .$$

If only one piece of news arrives every period, this intertemporal structure rules out large revisions in the belief parameters.

We impose these restrictions on blocks of time each of which lasts for two months, and thus consider a panel of option prices comprising July and August 1988, followed by a panel of the September and October 1988 prices, and so on, up to December 1993. For each block we solve the program:

35Of course, the identification of fundamentals with real dividends is problematic at best.


<!-- p:28 -->


$$\log \text {lam} . \\ \min _ { \{ \pi _ { t } \} _ { t = 1 } ^ { T } , N } \sum _ { t = 1 } ^ { T } \sum _ { \tau = \tau _ { t } } ^ { \bar { \tau } _ { t } } \sum _ { K _ { \tau _ { t } = \underline { K } _ { \tau _ { t } } } } ^ { \overline { K } _ { \tau _ { t } } } \left [ C ^ { B L } ( f _ { t } , \pi _ { t } , N ; \gamma , \beta ) - C ( f _ { t } ) \right ] ^ { 2 } \\ s . t . \quad \frac { \pi _ { t } N } { N + 1 } \leq \pi _ { t + 1 } \leq \frac { \pi _ { t } N + 1 } { N + 1 } \\ 0 \leq \pi _ { t } \leq 1 \quad t = 1 , \dots , T - 1 \quad N > 0 \\$$

The program is limited to blocks of 8-9 weeks to avoid the curse of dimensionality implicit in this tends to infinity which makes a solution practically impossible. Limiting ourselves to a bimonthly period means estimating a vector with 9-10 parameters to fit a sample of well over 300 observations on average. This setup therefore imposes much stronger restrictions on our model than in the previous sub-section and narrowly constrains the temporal dynamics of investors' beliefs with regard to the probability of good states. We make the same assumptions on preferences as in Section 6.3 and to simplify the estimation task also impose m = 1/7, i.e. fundamentals change at weekly frequency.

Figure 14 reports results over the period July 1988 - June 1991. We limit ourselves to this interval of time for computational reasons. The figure suggests that the estimated sequence 0.7]. We notice the same phenomena that were identified above: During 1990 agents drastically revised downwards their average beliefs on the likelihood of a high growth rate. This is consistent with a rational reaction to an incipient recession as well as to the additional uncertainty created by the Gulf War. While other even more restrictive tests can be designed, we consider these findings prima facie evidence that the BL model is indeed capable of extracting measures of agents' beliefs that are economically meaningful.

### 7. Conclusion

This paper has proposed a simple stylized equilibrium model for asset prices under Bayesian learning and investigated its ability to explain a variety of empirical biases in the Black-Scholes option pricing model.

Despite its simplicity, the model with Bayesian learning proved to be able to match both skews in implied volatilities and a non-constant term-structure in implied volatility. Thus the model offers a new economic explanation of BS biases. This is important because standard models in the literature that incorporate jump-diffusion and stochastic volatility effects, have been found by Das and Sundaram (1999) to be unable to correctly fit both stylized facts for plausible parameters values.


<!-- p:29 -->


The parameters of the learning process implied by the cross-section of option prices appear reasonably stable over time. Episodes of sharp revisions in the beliefs implied by options prices are rare and tend to involve the precision of these beliefs rather than their level, which we find plausible. When we impose the intertemporal restrictions built in through our maintained Bayesian learning scheme, we find again that the estimated parameters are stable across time and do not deviate much from the results obtained through the daily cross-sections. This stability means that the model performs well in out-of-sample prediction and delta hedging experiments. It also provides a very different learning model than that recently proposed by David and Veronesi (1999). In their filtering algorithm the updated state probabilities have frequent discrete jumps from near zero to near one. Our results suggest that a smoother learning process may be well suited for out-of-sample predictions of the evolution in the cross-section of option prices.

## Appendix B

#### Estimating learning parameters using the polytope method

Suppose we are interested in minimizing the sum of squared pricing errors computed across strikes, Kτt, and maturities, τt:

$$1 . 2 5 ^ { x } \times \frac { 1 0 } { 4 } = 1 0
 x ^ { + } = 0 . 2 x + x ^ { + }
 \frac { 1 } { 2 } x ^ { + } -
 5 0 0 ^ { \circ }
 0 . 1$$

Here the pricing error is defined as

$$\begin{matrix} 0 . 9 5 & 1 & 1 . 0 5 & 1 . 1 & 1 . 1 5 & 1 . 2 \\ & & & & & 0 . 8 & 0 . 8 5 & 0 . 9 & 0 . 9 5 & 1 & 1 . 0 5 & 1 . 1 & 1 . 1 5 \end{matrix}$$

We accomplish this by a combination of the polytope method and a grid search over a restricted region of the parameter space:

$$^ { \prime \prime }$$

The polytope method is a multidimensional comparison method that first constructs a simplex in Rn(in our case n = 3,the dimension of θt).37 The simplex comprises four vertices {θa θb θc θd } ...8 The initial simplex is composed of four vectors that lie on a three-dimensional plane. At each iteration the vertex that gives the highest value of the objective function is replaced with a new vertex that is likely to give a lower value.

37A more complete treatment of polytope methods can be found in Judd (1998) and Walters et al. (1991).

38We choose {θa θb θc θd } such that:

θa = [(πt−1 − .05) (t−1 − 50) (mt−1 + 0.3)]′

θc = [(πt−1 + .05) (t−1 − 50) (−t−1 + 0.3)]′

θb = [(πt−1 − .05) (t−1 + 50) (mt−1 − 0.3)]′

θd = [(πt−1 + .05) (t−1 + 50) (^t−1 − 0.3)]′


<!-- p:39 -->


A reason for the adoption of this comparison method is that one of the parameters, Nt, can only take positive, integer values. Furthermore, the layered objective function has systematic flats and kinks since the total number of forward steps vτ on the lattice is given by the integer part of τm. Gradient methods are not useful since there exists an infinite number of points in the parameter space where the objective function is not differentiable. Polytope methods do not impose smoothness conditions on the objective function and can handle simple discontinuities.

Two additional tests are conducted to see if the polytope search uncovers a local as opposed to a global minimum of the objective function. First, each day the polytope is started from a different initial simplex which is not a function of the estimation results from day t — 1and is chosen to be particularly wide.39 Second, we supplement the combined polytope and grid search with a rough grid search and require that the minimum sum of squared residuals over the grid exceeds the polytope solution.

If any of these conditions is not met, we resort to extensive grid search in order to obtain an optimal estimate of the parameters. Specifically, we implement a two-stage, three-layer grid search over the following wide region of the parameter space:

$$\hat { Y }$$

We limit ourselves to values of πin the interval [.4, .6]since we found that πtnever falls outside this region. N ≥ 250corresponds more or less to a constant volatility Black-Scholes model so we concentrate on cases where N &lt; 250. N &lt; 100,on the other hand, results in too strong skews and such values are therefore not considered. The first stage of the grid search involves 825 grid points, from which the three best estimates are selected prior to a more extensive neighborhood search around θ(1) :

$$\frac { \ M a t u n t y } { \neg - 1 8 / 1 - \neg 1 9 / 1 - \neg 2 0 / 1 - \neg 2 1 / 1 - \neg 2 5 / 1 - \neg 2 2 / 1 }$$

In the second stage each search involves 3,225 grid points. This procedure thus searches over more than 10,000 distinct points in the parameter space. Up to this point we have performed two polytope optimizations (from two alternative starting simplices), and two grid searches (the second in two steps and two layers), so we have considerable confidence in the results.

39We use the following values for {θa θb θc θd }:

θa = [.40 20 1]′, θb = [.40 300 .50]′

θc = [.60 20 1]′, and θd = [.60 300 0.50]'.


<!-- p:40 -->


#### Figure 1

#### Implied Volatility Surface vs. Moneyness

Implied volatility as a function of moneyness for S&amp;P 500 index options maturing in December of each year covered by our data set (1988 fi 1993). Each symbol in the plots corresponds to a particular day in the sample where a given maturity was traded. Moneyness is defined as the ratio between the level of the S&amp;P 500 index (less the dividends paid by the index up to maturity of the option contract) and the strike price.

December 1988

0.25

0.2

implied volatility

求

0.15

0.1

0.05

0.8

0.85

0.9

0.95

1

1.05

1.1

1.15

1.2

Moneyness

December 1989

0.3

0.25

implied volatility

▲

0.2

×

米

0.15

0.1

0.05

0.8

0.85

0.9

0.95

1

1.05

1.1

1.15

1.2

Moneyness

December 1990

0.3

0.25

■

implied volatility

□

▲

米

X

o+

0.2

0.15

口X

0.1

0.05

0.8

0.85

0.9

0.95

1

1.05

1.1

1.15

1.2

Moneyness

December 1991

0.3

0.25

implied volatility

0.2

米

0.15

米

A

米

0.1

●

0.05

0.8

0.85

0.9

0.95

1

1.05

1.1

1.15

1.2

Moneyness

December1992

0.3

0.25

implied vola tility

0.2

0.15

0.1

0.05

0.8

0.85

0.9

0.95

1

1.05

1.1

1.15

1.2

Moneyness

December 1993

0.3

0.25

implied volatility

0.2

0.15

0.1

0.05

米

0.8

0.85

0.9

0.95

1

1.05

1.1

1.15

1.2

Moneyness


<!-- p:41 -->


#### Figure 2

#### Implied Volatility Surface vs. Term Structure

The three graphs plot implied volatility as a function of maturity for S&amp;P 500 index options over the period Jan. 18 - Jan. 25, 1993. Three different moneyness levels are used: 0.96 (in the money), 1 (at the money), and 1.04 (out of the money). Moneyness is defined as the ratio between the level of the S&amp;P 500 index (less the dividends paid by the index up to maturity of the option contract) in the moment of the trade and the strike price.

Term structure of implied volatilities for out-of

the-money (call) options - moneyness= 1.04

0.09

implied volatility

0.08

米

0.07

米

0.06

Jan-93

Feb-93

Mar-93

Apr-93

Maturity

1/21/1/11/01/1/81

Term structure of implied volatilities for

ATM options

0.11

implied volatility

0.1

0.09

0.08

0.07

Jan-93

Feb-93

Mar-93

Apr-93

Maturity

-18/119/120/1→21/1→25/122/1

Term structure of implied volatilities for in-the-

money (call) options - moneyness= 1.04

0.12

中

■

implied volatility

0.11

米

*

米

0.1

0.09

Jan-93

Feb-93

Mar-93

Apr-93

Maturity

18/119/120/1→×21/1→25/1→22/1


<!-- p:42 -->


#### Figure 3

#### State Price Density Implied by S&amp;P 500 Index Options

The three graphs plot the average state-price density estimated from S&amp;P 500 index options and the S&amp;P 500 cash index over the period June 1988 fi December 1993 compared to a lognormal SPD. The estimated SPD is the average of 765 SPDs obtained from options data with more than 6 calendar days to expiration using the nonparametric, implied binomial trees method of Rubinstein (1994) and Jackwerth and Rubinstein (1996). The objective function is the maximum smoothness function:

$$t i o n s \, \text {exploring in April 1993} .$$

For every week in the sample and for each cross section of contracts, we minimize the objective function subject to martingale constraints on the option prices and the underlying index. The constraints are imposed by a penalty method that progressively raises the penalty parameter over various steps of the numerical optimization (see Judd (1998, 123-125)).

Lognormal vs. Average SPD Estimated from

S&amp;P500 Index Option Prices

0.18

0.16

0.14

State price

0.12

0.1

0.08

0.06

0.04

0.02

0

-10

-8

-6

-4

-2

0

2

4

6

8

10

Standardized logarithmic returns

lognormal  estimated

Lognormal vs. Average SPD Estimated from

S&amp;P500 Index Options - Left Tail

0.0009

0.0008

0.0007

0.0006

State price

0.0005

0.0004

0.0003

0.0002

0.0001

0

-10

-8

-6

-4

-2

Standardized logarithmic returns

- lognormal  estimated

Lognormal vs. Average SPD Estimated from

S&amp;P500 Index Options - Left Tail

0.0006

0.0005

0.0004

State price

0.0003

0.0002

0.0001

0

2

4

6

8

10

Standardized logarithmic returns

- lognormal

estimated


<!-- p:43 -->


#### Figure 4

#### Option Prices under Full Information and Bayesian Learning

Difference between the price of a European call with 50 days to expiration (τ= 50) calculated under full information and Bayesian learning. The assumed parameters are: m= 1, gh=0.00315, gl= -0.00314, π= 0.519, ρ= 0.02 (annual), γ= 0.999. For BL prices, we take n= 42 and N= 80, implying a marginally biased initial belief π, = 0.525. The current price of the S&amp;P 500 is assumed to be $436.38, the closing price on Feb. 22, 1993.

Figure 5 The Implied Volatility Surface under Full Information

Dollar Difference between BS and BL

call prices

2.5

2

dollars

1.5

1

0.5

0


200

400

600

800

Strike price

Implied Black-Scholes volatilities as a function of moneyness for a European call with 50 days to expiration (τ= 50) calculated under full information. The parameters are set as follows: m= 1, gh= 0.00315, gl= -0.00314, π= 0.519, ρ= 0.02 (annual), and γ= 0.999. The price of the S&amp;P 500 is assumed to be $436.38, the closing price on Feb. 22, 1993. For comparison, the left panel reports implied volatilities as a function of moneyness for options expiring in April 1993.

Implied Volatilities - April 1993 Maturity

0.25

A

0.2

implied vola tility

■

0.15

0.1

文

0.05

0

0.85 0.89 0.93 0.97 1.01 1.05 1.09

1.131.17

Moneyness

Volatilities implied by BS call prices

0.25

0.2

annual volatility

0.15

0.1

0.05

0

0.85 0.89 0.93 0.97 1.01 1.05 1.09 1.13 1.17

Moneyness (stock index/strike)


<!-- p:44 -->


Figure 6 The Implied Volatility Surface under Bayesian Learning

Implied Black-Scholes volatilities as a function of moneyness for a European call with 50 days to expiration (τ= 50) cCal = 0 = - =  00 =  = :   s   ,  s   0 0) àt        =         =       (s assumed to be $436.38, the closing price on Feb. 22, 1993. For comparison, the left panel reports implied volatilities as a function of moneyness for options expiring in April 1993.

Figure 7 The Implied Volatility Surface under Bayesian Learning

Implied Volatilities - April 1993 Maturity

0.25

&lt;

0.2

implied volatility

0.15

0.1

0.05

0

0.85 0.89 0.93 0.97 1.01 1.05 1.09 1.13 1.17

Moneyness

Volatilities implied by BL call prices

0.25

0.2

annual volatility

0.15

0.1

0.05

0

0.85

0.89

0.93

0.97

1.01

1.05

1.09

1.13

1.17

Moneyness

Implied Black-Scholes volatilities as a function of moneyness for a European call with 50 days to expiration (τ= 50) calculated on a Bayesian learning path and using actual market data on February 22, 1993. The parameters are: m=1, gh= 0.00315, g= -0.00314, π= 0.519, ρ= 0.02 (annual), γ= 0.999, nt= 43, and Nt= 80, implying an initial belief π t = 0.538.

Market vs. BL implied volatilities on Feb. 22,

1993 (April 1993 maturity)

0.25

annual volatility

0.2

0.15

1

0.1

HHHA

0.05

0

0.88

0.92

0.96

1

1.04

1.08

Moneyness

-Market implied volatilities

Implied volatilities under BL


<!-- p:45 -->


#### Figure 8

#### State-Price Densities under Full Information and Bayesian Learning

State-price densities for the 50 days ahead (τ= 50) values of the S&amp;P 500 index derived from a BS vs. a Bayesian learning model on Feb. 22, 1993. The parameters are set as follows: m = 1, gh= 0.00315, gl= -0.00314, π = 0.519, ρ = 0.02 (annual), γ = 0.999, n= 42, and N= 80, implying an initial belief πt = 0.525. The price of the S&amp;P 500 is $436.38, the closing price on Feb. 22, 1993. The third panel compares the BS with the BL state price density adjusting for differences in their respective supports. For comparison, the fourth panel plots the average empirical SPD estimated in Section 2 when the index takes a value of $436.38.

BS state price density for 50 days-ahead values

of the S&amp;P 500

0.12

0.1

price

0.08

0.06

state

0.04

0.02

0

360

385

410

435

460

485

510

Index

Bayesian learning state price density for 50 days-

ahead values of the S&amp;P 500

0.12

0.1

state price

0.08

0.06

0.04

0.02

0+

360

385

410

435

460

485

510

Index

Comparing BS and BL state-price density for

50 days-ahead values of the S&amp;P 500

0.12

0.1

state price

0.08

0.06

0.04

0.02

0

360

385

410

435

460

485

510

Index

Bayesian learning

BS/lognormal

Average SPD Estimated from S&amp;P500 Index

Option Prices Centered on the level of the

index on Feb. 22, 1993

0.18

0.16

0.14

0.12

State price

0.1

0.08

0.06

0.04

0.02

0

360

380

400

420

440

460

480

500

520

540

Index


<!-- p:46 -->


#### Figure 9

#### Implied Volatility Term Structure Under Full Information and Bayesian Learning

We assume m= 1 while the other 'deep' parameters (gh, g, π, ρ, and γ) are adjusted according to Proposition 2 to ensure that the BS option price is an approximation to the Black-Scholes value with an annual risk-free rate of 4% and a dividend yield of 3%. In the BL case, we take n=42 and Nt=80, implying an initial belief π, = 0.525. The current price of the S&amp;P 500 is assumed to be $436.38, the closing price on Feb. 22, 1993. The first panel sets K=455, the second K=435, and the third K=420.

Implied volatility term structure under BS and

BL for an out-of-the-money European call

0.12

pli

im

0.1

ed

0.08

vol

0.06

aitl

ity

0.04

0.02

0


50

100

150

time to expiration

Implied volatility term structure under BS and

BL for an at-the-money European call

0.12

implied volaitlity

0.1

0.08

0.06

0.04

0.02

0


50

100

150

time to expiration

Implied volatility term structure under BS and

BL for an in-the-money European call

0.12

implied volaitlity

0.1

0.08

0.06

0.04

0.02

0


50

100

150

time to expiration


<!-- p:47 -->


#### Figure 10

#### Implied Volatility Surface under Bayesian Learning

We plot the annualized implied volatilities as a function of both the strike price and time to maturity when the economy is on a Bayesian learning path. We assume n=42 and Nt=80, implying an initial belief π, = 0.525. The current price of the S&amp;P 500 is assumed to be $436.38, the closing price on Feb. 22, 1993.

(Annual) implied volatility

0.08 0.12 0.16 0.20

390

Time to maturity

60

80

430

Strike

470


<!-- p:48 -->


#### Figure 11

#### Weak Learning Effects

We plot the differences between call prices, implied volatilities as a function of the strike price, and 50-day-ahead stateprice densities for the S&amp;P 500 index on Feb. 22,1993 for the FIRE and BL asset pricing models. The first three graphs reln t   bs s s  ut      s     t der full information rational expectations and with diamond the SPD calculated under Bayesian learning. The parameters are set as follows: m= 1, gh= 0.00315, g=-0.00314, π=0.519, ρ=0.02 (annual), γ= 0.999, nt= 182, and Nt= 350, implying an initial unbiased belief π, =0.52 ≈ π. The current price of the S&amp;P 500 is assumed to be $436.38 dollars, the closing price on Feb. 22, 1993.

Difference between BS and BL call prices

(in dollars)

0.7

0.6

0.5

dollars

0.4

0.3

0.2

0.1

0


200

400

600

800

Strike price

Volatilities implied by BS call prices

0.25

0.2

volatility

0.15

annual

0.1

0.05

0

0.89

0.93

0.97

1.01

1.05

1.09

1.13

Moneyness (stock index/strike)

Volatilities implied by BL call prices

0.25

annual volatility

0.2

0.15

0.1

0.05

0

0.85 0.89 0.93 0.97 1.011.051.091.131.17

Moneyness (stock index/ strike)

Comparing BS and BL state-price density for

50 days-ahead values of the S&amp;P 500

0.12

0.1

8

state-price

0.08

日

口

0.06

口

0.04

0.02

0

360

385

410

435

460

485 510

Index


<!-- p:49 -->


#### Figure 12

#### Estimated Parameter Plots

The graphs plot weekly parameter estimates obtained by fitting to the cross section of S&amp;P 500 index option prices each day Black-Scholes (BS), BS with three maturity parameters (BS(τ)), BS with three moneyness parameters (BS(m)), a BSspline model (BS-spline) with five parameters, Heston and Nandi,s (2000) NGARCH(1,1) model, and a Bayesian learning model (BL) obtained by setting ρ = 0.02 and γ = 0.9. The sample consists of the weekly data for the period June 1988 fi December 1993. In the case of the ,ad hoc,,strawman of Dumas et al. (1993), only the estimates of the coefficients α0, α1, and α2 are reported; for the NGARCH (1,1) only the estimates of α, ξ, and φ are plotted.

Estimated weekly BS implied volatility

BS(tau), estimated implied volatility

BS(m), estimated implied volatilities

023

0.25

0.3

0.23

0.21

(Annual) implied volatility

0.21

(Annual) implied volatility

0.25

(Annual) implied volatility

61'0

0.19

0.2

0.17


0.15


0.13

0.11

0.13

0.11

0.1

600

60'0

0.07

0.05

007

0.05


61

81

101

121

141

161 181 201 221 241 261 281

21

41

61

81

101

121

141

161

181 201 221 241 261 281

21

81

101

121

141

161 181 201 221 241 261 281

Week


&lt; 40 days

- between 40 and 70 days - - - - &gt; 70 days

ITM volatility

ATM volatility

OTM volatility

NGARCH(1,1), estimated alpha

NGARCH(1,1), estimated phi

NGARCH(1,1), estimated csi

0.00025

6000

5000

0.0002

0.8

4000

0.00015

0.6

300

2000

0.0001

0.4

100

0.00005

0.2

-1000

81

101 121 141 161 181 201 221 241 261 281

21

41

61

81

101 121 141 161 181 201 221 241 261 281

21

41

61

81

101

121

141

161

181 201 221 241 261 281

Week


BS-spline, a0

BS-spline, a1

BS-spline, a2

0.02

0.0000800

0.0000700

6

0.01

0.0000600

0.0000500

0.0000400

3

-0.01

0.0000300

2

0.0000200

-0.02

0.0000100

0.0000000

0

-0.03

-0.0000100

-0.0000200

-2

-0.04

-0.0000300

21

41

81

101

181

201

221

241 261 281

21

41

61

81 101 121 141 161 181 201 221 241 261 281

21

41

61

81

101

121

141

161 181 201 221 241 261 281

Week


BL model, estimated pi (rho= 2%, CRRA= 0.9)

BL model, estimated N (rho= 2%, CRRA= 0.9)

BL model, estimated m (rho= 2%, CRRA=0.9)

0.7

400

0.65

0.8

360

0.6


320

0.55

0.4

0.5

280

02

M

0+45

240

21

41

61

81

101

121

161

181 201 221 241 261 281

81

101 121 141 161 181 201 221 241 261 281

21

41

61

81

101 121 141 161 181 201 221 241 261 281

Week


<!-- p:50 -->


#### Figure 14

#### Learning Dynamics on an Expanding Window

x      ( t       id  d s t  d dex option prices during the period June 1988 fi June 1991. We also report the precision of these beliefs (the number of T are estimated by solving the program:

$$\text {polynomial in K (the strike price) and } \tau \text { (time-to-maturity) to the implied volatility} \\ \text {the fitted volatility levels. NGARCH is the option pricing GARCH model prop} \\ \text {s a Bayesian learning model (assuming a fundamental volatility of 5% per year) re-} \\ \text {the coefficient} \quad \text {Mean} \quad \text {Median} \quad \text {St}$$

i.e. by minimizing the (cross-sectional) sum of the squared pricing errors implied by the model under BL on blocks of 2 months length. The exercise assumes ρ =0.02 (annually), CRRA-power preferences with constant relative risk aversion γ= 0.9, and a volatility of fundamental news σ=5% (annualized).

Bayesian learning with expanding window -

estimated pi

0.8

0.7

0.6

0.5

0.4

0.3

0.2

1 10 19 28 37 46 55 64 73 82 91 100 109 118 127 136 145 154

Week


<!-- p:51 -->


#### Table 1 Implied State Price Densities

The table reports the price of a state-contingent claim that pays out 1 dollar when (demeaned) S&amp;P 500 returns fall below or above X standard deviations, calculated using the SPD estimated from option contracts with at least 7 calendar days to maturity. As a benchmark the table also reports the price of the same contingent claims based on a lognormal SPD. The SPDs have been demeaned and divided by σ√τ . The price of the contingent claims are calculated according to the

formula:

$$s , \, \text {on which a particular model has a lower daily RMSPE than any other.} \, \% \, \text {best-} \, \\ \text {allogoussly. BS is the Black-Scholes model, BS( \tau) is a BS model that allows volatile volatility to be a function of moneyness, 'BS sp $ } \\ \text {, BS(m) is a BS model that allows volatile volatility to be a function of moneyness, 'BS sp $ } \\ K \, ( \text {the strike price} ) \, \text {and } \, \tau \, ( \text {time-to-maturity} ) \, \text {to the implied volatility surface and} \\ \text {tilitility levels. NGARCH is the option pricing GARCH model proposed by Hestor} \\ \text {learning model (assuming either $\rho = 0.1$ or $\rho = 0.05$ and $\gamma = 0.9$) re-estimated} \\ \text {and as 100\times(F/K-1), where F is the futures price with maturity identical to the option} \\ \text {, } \, \text {Panel A: Aggregate Results} \\$$

where the λ;s are the state-prices, I is the standard indicator function,

$$\frac { \text {Model} } { \text {BS} } \left ( \begin{array} { c c c c c } \text {Model} & & \text {RMSPE} & \text {MAPE} & \text {MOE-P} & \text {RMSPE} & \text {MAPE} & \text {MOE-P} \\ & & & & & \text {RMSPE} & \text {MAPE} & \text {MOE-P} \\ & & & & & & \text {RMSPE} & \text {MAPE} & \text {MOE-P} \\ & & & & & & & \text {MOE-P} \\ & & & & & & & \text {RMSPE} \\ & & & & & & & \text {BS (T)} \\ & & & & & & & \text {BS (T)} \end{array} \right )$$

and Prob{ Sjt+v uidv-j S is a risk-neutral probability, based either on the normal density or implied by the options data. The estimated SPDs are either average or median state-price densities estimated from S&amp;P 500 index options and the S&amp;P 500 cash index over the period June 1988 fi December 1993 using the nonparametric, implied binomial tree method of Rubinstein (1994) and Jackwerth and Rubinstein (1996). The objective is the maximum smoothness function:

$$\begin{array} { c } \text {Panel B: Results by Moneyness} \\ \text {Moneyness (%} ) \\ \text {ss than -2% of (OTM)} & - 2 \% \text { to } + 2 \% \text { (ATM)} \end{array}$$

| X       | Average price   | Average price   | Median price   | Median price   |
|---------|-----------------|-----------------|----------------|----------------|
|         | Lognormal SPD   | Estimated SPD   | Lognormal SPD  | Estimated SPD  |
| -7<     | 1.42E-05        | 0.00069         | 3.81E-13       | 1.71E-10       |
| -6<     | 2.01E-05        | 0.00079         | 7.35E-10       | 7.37E-10       |
| -5<     | 2.08E-05        | 0.00089         | 3.33E-07       | 1.83E-09       |
| - Q -4< | 6.17E-05        | 0.00128         | 4.34E-05       | 3.59E-09       |
| -3<     | 0.00176         | 0.00188         | 0.00186        | 6.97E-09       |
| -2<     | 0.02720         | 0.00446         | 0.02932        | 2.06E-08       |
| -1<     | 0.17622         | 0.06631         | 0.18695        | 4.78E-05       |
| >1      | 0.13626         | 0.05123         | 0.12875        | 0.04078        |
| >2      | 0.01852         | 0.00831         | 0.01629        | 0.00239        |
| >3      | 0.00110         | 0.00262         | 0.00080        | 0.00022        |
| + Q >4  | 7.94E-05        | 0.00136         | 1.37E-05       | 5.22E-05       |
| >5      | 4.83E-05        | 0.00061         | 7.23E-08       | 1.20E-05       |
| >6      | 4.02E-05        | 0.00043         | 9.71E-11       | 4.44E-06       |
| >7      | 3.20E-05        | 0.00028         | 2.46E-14       | 2.00E-06       |


<!-- p:52 -->


#### Table 2

#### Average Dollar Valuation Errors Using the Bayesian Learning Model and Different Versions of Black-Scholes.

RMSVE is the root mean squared dollar valuation error averaged across all days and all traded contracts over the sample period June 1988 - December 1993. MAVE is the average of the mean absolute dollar evaluation error. AIC is the average of the Akaike Information Criterion. MOE is the average pricing error outside the bid/ask spread. '% best-RMSVE' is the frequency of days, expressed as a ratio of the total number of days, on which a particular model has a lower daily RMSVE than any other. '% best-MAVE', '% best-AIC', and '% best-MOE' are defined analogously. BS is the Black-Scholes model, BS(τ) is a BS model that allows volatility to be a function of time-to-expiration, BS(m) is a BS model that allows volatility to be a function of moneyness, 'BS spline' fits a function of a polynomial in K (the strike price) and τ (time-to-maturity) to the implied volatility surface and then prices options using the fitted volatility levels. NGARCH is the option pricing GARCH model proposed by Heston and Nandi (2000). BL is a Bayesian learning model (assuming ρ = 0.02 and γ = 0.9) re-estimated on a weekly basis. All the models are estimated by minimizing the sum of squared pricing errors. Moneyness is defined as 100×(F/K-1), where F is the futures price for maturity identical to the option contract.

| Panel A: Aggregate Results   | Panel A: Aggregate Results   | Panel A: Aggregate Results   | Panel A: Aggregate Results   | Panel A: Aggregate Results   | Panel A: Aggregate Results   | Panel A: Aggregate Results   | Panel A: Aggregate Results   | Panel A: Aggregate Results   |
|------------------------------|------------------------------|------------------------------|------------------------------|------------------------------|------------------------------|------------------------------|------------------------------|------------------------------|
| Model                        | RMSVE                        | MAVE                         | AIC                          | MOE                          | % best- RMSVE                | % best- MAVE                 | % best- AIC                  | % best- MOE                  |
| BS                           | 1.5048                       | 1.2634                       | 0.7829                       | 1.1098                       | 0%                           | 0%                           | 0.34%                        | 0%                           |
| BS ( τ )                     | 1.4508                       | 1.1916                       | 0.8259                       | 1.0401                       | 0%                           | 0%                           | 0.34%                        | 0%                           |
| BS(m)                        | 0.7846                       | 0.5756                       | -0.3847                      | 0.4364                       | 11.30%                       | 14.04%                       | 19.52%                       | 14.73%                       |
| BS spline                    | 0.6240                       | 0.4391                       | -0.7822                      | 0.3015                       | 53.77%                       | 63.70%                       | 52.06%                       | 55.67%                       |
| NGARCH                       | 0.6999                       | 0.5396                       | -0.5105                      | 0.7141                       | 13.36%                       | 8.56%                        | 10.96%                       | 0%                           |
| BL                           | 0.7190                       | 0.5612                       | -0.5361                      | 0.3512                       | 21.58%                       | 13.70%                       | 17.47%                       | 29.59%                       |

#### Panel B: Results by Moneyness

|           | Moneyness (%)       | Moneyness (%)       | Moneyness (%)       | Moneyness (%)    | Moneyness (%)    | Moneyness (%)    | Moneyness (%)      | Moneyness (%)      | Moneyness (%)      |
|-----------|---------------------|---------------------|---------------------|------------------|------------------|------------------|--------------------|--------------------|--------------------|
|           | Less than -2% (OTM) | Less than -2% (OTM) | Less than -2% (OTM) | -2% to +2% (ATM) | -2% to +2% (ATM) | -2% to +2% (ATM) | More than 2% (ITM) | More than 2% (ITM) | More than 2% (ITM) |
| Model     | RMSVE               | MAVE                | MOE                 | RMSVE            | MAVE             | MOE              | RMSVE              | MAVE               | MOE                |
| BS        | 2.155               | 1.352               | 1.203               | 1.494            | 0.990            | 0.797            | 1.184              | 1.452              | 1.321              |
| BS ( τ )  | 1.481               | 1.271               | 1.124               | 1.078            | 0.833            | 0.646            | 1.638              | 1.426              | 1.295              |
| BS(m)     | 0.422               | 0.348               | 0.348               | 1.087            | 0.929            | 0.929            | 0.685              | 0.523              | 0.523              |
| BS spline | 0.553               | 0.407               | 0.278               | 0.855            | 0.709            | 0.518            | 0.435              | 0.313              | 0.204              |
| NGARCH    | 0.795               | 0.664               | 0.829               | 0.876            | 0.757            | 0.979            | 0.469              | 0.417              | 0.562              |
| BL        | 0.640               | 0.484               | 0.288               | 0.853            | 0.665            | 0.394            | 0.689              | 0.548              | 0.348              |

#### Panel C: Results by Time-to-Maturity

#### Days to Expiration

|           | Less than 40   | Less than 40   | Less than 40   | 40 to 70   | 40 to 70   | 40 to 70   | More than 70   | More than 70   | More than 70   |
|-----------|----------------|----------------|----------------|------------|------------|------------|----------------|----------------|----------------|
| Model     | RMSVE          | MAVE           | MOE            | RMSVE      | MAVE       | MOE        | RMSVE          | MAVE           | MOE            |
| BS        | 0.477          | 0.623          | 0.450          | 0.871      | 0.886      | 0.645      | 2.078          | 1.358          | 0.999          |
| BS ( τ )  | 0.482          | 0.422          | 0.334          | 0.749      | 0.636      | 0.523      | 1.299          | 1.068          | 0.925          |
| BS(m)     | 0.536          | 0.418          | 0.330          | 0.648      | 0.493      | 0.382      | 0.767          | 0.565          | 0.431          |
| BS spline | 0.273          | 0.211          | 0.129          | 0.344      | 0.260      | 0.158      | 0.565          | 0.404          | 0.273          |
| NGARCH    | 0.450          | 0.431          | 0.505          | 0.520      | 0.504      | 0.542      | 0.684          | 0.825          | 0.758          |
| BL        | 0.439          | 0.359          | 0.219          | 0.507      | 0.405      | 0.237      | 0.695          | 0.577          | 0.358          |


<!-- p:53 -->


#### Table 3

#### Summary Statistics for Parameter Estimates.

The table reports summary statistics from fitting five different models to the cross-section of S&amp;P 500 index option prices over the period Jan. 4 - Dec. 31, 1993. BS is the Black-Scholes model, BS (τ) is a BS model that allows volatility to be a function of time-to-expiration, BS(m) is a BS model that allows volatility to be a function of moneyness, 'BS spline' that fits a function of a polynomial in K (the strike price) and τ (time-to-maturity) to the implied volatility surface and then prices options using the fitted volatility levels. NGARCH is the option pricing GARCH model proposed by Heston and Nandi (2000). BL is a Bayesian learning model (assuming a fundamental volatility of 5% per year) re-estimated on a daily basis.

| Model             | Coefficient estimate   |      Mean |   Median |   Standard Dev. |
|-------------------|------------------------|-----------|----------|-----------------|
| BS                | σ                      |    0.1314 |   0.1283 |          0.0274 |
| BS( m )           | σ OTM                  |    0.1126 |   0.1090 |          0.0241 |
| BS( m )           | σ ATM                  |    0.1381 |   0.1343 |          0.0335 |
| BS( m )           | σ ITM                  |    0.1681 |   0.1620 |          0.0371 |
| BS( τ )           | σ short                |    0.1221 |   0.1185 |          0.0333 |
| BS( τ )           | σ medium               |    0.0997 |   0.1130 |          0.0532 |
| BS( τ )           | σ long                 |    0.1329 |   0.1310 |          0.0279 |
| BS-spline         | α 0                    |    1.4299 |   1.2683 |          1.1750 |
| BS-spline         | α 1                    |   -0.0053 |  -0.0045 |          0.0066 |
| BS-spline         | α 2                    |  4.80E-06 | 3.80E-06 |        10.0E-06 |
| BS-spline         | α 3                    |   -0.0019 |  -0.0014 |          0.0022 |
| BS-spline         | α 4                    |  5.29E-06 | 4.33E-06 |        5.67E-06 |
| NGARCH            | ω                      | -7.44E-06 | 4.53E-07 |       26.06E-06 |
| NGARCH            | α                      | 14.16E-06 | 2.29E-06 |       28.80E-06 |
| NGARCH            | β                      |    0.6560 |   0.7003 |          0.2757 |
| NGARCH            | γ                      |  373.4480 | 261.1294 |        651.4054 |
| NGARCH            | λ                      |    0.6698 |   0.6768 |          1.2937 |
| Bayesian learning | π t                    |    0.5589 |   0.5776 |          0.0315 |
| Bayesian learning | N t                    |    315.52 |   317.00 |           18.96 |
| Bayesian learning | m t                    |    0.2839 |   0.2676 |          0.0913 |


<!-- p:54 -->


#### Table 4

#### Average Dollar Prediction Errors Using the Bayesian Learning Model and Different Versions of Black-Scholes formula.

ms   s a  s  s  oe od a  a   s ape period January 4, 1993 - December 31, 1993. MAPE is the average of the mean absolute dollar prediction error. MOE is the average pricing error outside the bid/ask spread. '% best-RMSPE' is the frequency of days, expressed as a ratio of the total number of days, on which a particular model has a lower daily RMSPE than any other. '% best-MAPE' and '% bestMOE' are defined analogously. BS is the Black-Scholes model, BS(τ) is a BS model that allows volatility to be a function of time-to-expiration, BS(m) is a BS model that allows volatility to be a function of moneyness, 'BS spline' fits a function of a polynomial in K (the strike price) and τ (time-to-maturity) to the implied volatility surface and then prices options using the fitted volatility levels. NGARCH is the option pricing GARCH model proposed by Heston and Nandi (2000). BL is a Bayesian learning model (assuming either ρ = 0.1 or ρ = 0.05 and γ = 0.9) re-estimated on a weekly basis. Moneyness is defined as 100×(F/K-1), where F is the futures price with maturity identical to the option contract.

| Panel A: Aggregate Results   | Panel A: Aggregate Results   | Panel A: Aggregate Results   | Panel A: Aggregate Results   | Panel A: Aggregate Results   | Panel A: Aggregate Results   | Panel A: Aggregate Results   |
|------------------------------|------------------------------|------------------------------|------------------------------|------------------------------|------------------------------|------------------------------|
| Model                        | RMSPE                        | MAPE                         | MOE-P                        | % best- RMSPE                | % best- MAPE                 | % best- MOE-P                |
| BS                           | 1.6767                       | 1.3630                       | 1.1079                       | 0%                           | 0%                           | 0%                           |
| BS ( τ )                     | 1.8873                       | 1.4886                       | 1.0380                       | 0.34%                        | 0%                           | 0%                           |
| BS(m)                        | 1.0713                       | 0.7888                       | 0.4367                       | 15.12%                       | 18.56%                       | 17.18%                       |
| BS spline                    | 1.0614                       | 0.7321                       | 0.3009                       | 42.61%                       | 48.45%                       | 58.35%                       |
| NGARCH                       | 1.1602                       | 0.9010                       | 0.7546                       | 7.22%                        | 5.84%                        | 0.69%                        |
| BL                           | 0.9990                       | 0.7704                       | 0.3532                       | 34.71%                       | 27.15%                       | 23.78%                       |

Moneyness (%)

#### Panel B: Results by Moneyness

|           | Moneyness (%)       | Moneyness (%)       | Moneyness (%)       | Moneyness (%)    | Moneyness (%)    | Moneyness (%)    | Moneyness (%)      | Moneyness (%)      | Moneyness (%)      |
|-----------|---------------------|---------------------|---------------------|------------------|------------------|------------------|--------------------|--------------------|--------------------|
|           | Less than -2% (OTM) | Less than -2% (OTM) | Less than -2% (OTM) | -2% to +2% (ATM) | -2% to +2% (ATM) | -2% to +2% (ATM) | More than 2% (ITM) | More than 2% (ITM) | More than 2% (ITM) |
| Model     | RMSPE               | MAPE                | MOE-P               | RMSPE            | MAPE             | MOE-P            | RMSPE              | MAPE               | MOE-P              |
| BS        | 1.606               | 1.452               | 1.201               | 1.422            | 1.162            | 0.796            | 1.729              | 1.472              | 1.320              |
| BS ( τ )  | 1.766               | 1.522               | 1.122               | 1.816            | 1.402            | 0.644            | 1.821              | 1.559              | 1.294              |
| BS(m)     | 0.771               | 0.619               | 0.228               | 1.399            | 1.169            | 0.739            | 0.878              | 0.680              | 0.403              |
| BS spline | 1.003               | 0.756               | 0.277               | 1.129            | 0.909            | 0.516            | 0.820              | 0.596              | 0.203              |
| NGARCH    | 1.166               | 1.030               | 0.891               | 1.195            | 1.056            | 0.863            | 0.896              | 0.805              | 0.680              |
| BL        | 0.897               | 0.698               | 0.398               | 1.158            | 0.910            | 0.512            | 0.899              | 0.718              | 0.423              |

|           | Days to Expiration   | Days to Expiration   | Days to Expiration   | Days to Expiration   | Days to Expiration   | Days to Expiration   | Days to Expiration   | Days to Expiration   | Days to Expiration   |
|-----------|----------------------|----------------------|----------------------|----------------------|----------------------|----------------------|----------------------|----------------------|----------------------|
|           | Less than 40         | Less than 40         | Less than 40         | 40 to 70             | 40 to 70             | 40 to 70             | More than 70         | More than 70         | More than 70         |
| Model     | RMSPE                | MAPE                 | MOE-P                | RMSPE                | MAPE                 | MOE-P                | RMSPE                | MAPE                 | MOE-P                |
| BS        | 0.602                | 0.580                | 0.451                | 1.053                | 0.800                | 0.646                | 2.543                | 1.219                | 0.997                |
| BS ( τ )  | 0.635                | 0.542                | 0.334                | 1.376                | 1.064                | 0.523                | 1.682                | 1.322                | 0.923                |
| BS(m)     | 0.626                | 0.500                | 0.329                | 0.770                | 0.600                | 0.382                | 0.989                | 0.736                | 0.432                |
| BS spline | 0.416                | 0.347                | 0.129                | 0.504                | 0.408                | 0.158                | 1.000                | 0.635                | 0.273                |
| NGARCH    | 0.659                | 0.644                | 0.554                | 0.778                | 0.763                | 0.610                | 1.027                | 0.908                | 0.834                |
| BL        | 0.553                | 0.460                | 0.454                | 0.659                | 0.526                | 0.297                | 0.925                | 0.734                | 0.405                |

#### Panel C: Results by Time-to-Maturity


<!-- p:55 -->


#### Table 5

#### Average Dollar Hedging Errors Using the Bayesian Learning Model and Different Versions of Black-Scholes.

RMSHE is the root mean squared dollar hedging error averaged across all days and all traded contracts in the sample period January 4, 1993 - December 31, 1993. MAHE is the average of the mean absolute dollar hedging error. '% bestRMSHE'is the frequency of days, expressed as a ratio of the total number of days, on which a particular model has a lower daily RMSHE than any other model. '% best-MAHE' is defined analogously. BS is the Black-Scholes model, BS (τ) is a BS model that allows volatility to be a function of time-to-expiration, BS(m) is a BS model that allows volatility to be a function of moneyness, 'BS spline' fits a function of a polynomial in K (the strike price) and τ (time-to-maturity) to the implied volatility surface and then prices options using the fitted volatility levels. NGARCH is the option pricing GARCH model proposed by Heston and Nandi (2000). BL is a Bayesian learning model (assuming either ρ = 0.1 or ρ = 0.05 and γ = 0.9) re-estimated on a weekly basis. Moneyness is defined as 100×(F/K-1), where F is the futures price with maturity identical to the option contract.

| Panel A: Aggregate Results   | Panel A: Aggregate Results   | Panel A: Aggregate Results   | Panel A: Aggregate Results   | Panel A: Aggregate Results   |
|------------------------------|------------------------------|------------------------------|------------------------------|------------------------------|
| Model                        | RMSHE                        | MAHE                         | % best-RMSHE                 | % best-MAHE                  |
| BS                           | 0.9399                       | 0.6804                       | 2.06%                        | 5.84%                        |
| BS ( τ )                     | 0.9414                       | 0.6647                       | 6.53%                        | 8.94%                        |
| BS(m)                        | 0.9327                       | 0.6586                       | 13.75%                       | 12.72%                       |
| BS spline                    | 0.7556                       | 0.5233                       | 28.87%                       | 29.90%                       |
| NGARCH                       | 0.8126                       | 0.6082                       | 21.99%                       | 17.87%                       |
| BL                           | 0.7441                       | 0.5404                       | 26.80%                       | 24.74%                       |

Moneyness (%)

#### Panel B: Results by Moneyness

|           | Less than -2% (OTM)   | Less than -2% (OTM)   | -2% to +2% (ATM)   | -2% to +2% (ATM)   | More than 2% (ITM)   | More than 2% (ITM)   |
|-----------|-----------------------|-----------------------|--------------------|--------------------|----------------------|----------------------|
|           | RM SHE                | MAH E                 | RM SHE             | MAVE               | RM SHE               | MAH E                |
| Model BS  | 0.792                 | 0.652                 | 1.177              | 0.919              | 0.552                | 0.461                |
| BS ( τ )  | 0.815                 | 0.649                 | 1.148              | 0.870              | 0.579                | 0.476                |
| BS(m)     | 0.615                 | 0.496                 | 1.184              | 0.945              | 0.680                | 0.513                |
| BS spline | 0.664                 | 0.522                 | 0.938              | 0.718              | 0.449                | 0.353                |
| NGARCH    | 0.713                 | 0.646                 | 0.931              | 0.774              | 0.479                | 0.443                |
| BL        | 0.716                 | 0.574                 | 0.994              | 0.756              | 0.592                | 0.493                |

#### Panel C: Results by Time-to-Maturity

#### Days to Expiration

|           | Less than 40   | Less than 40   | 40 to 70   | 40 to 70   | More than 70   | More than 70   |
|-----------|----------------|----------------|------------|------------|----------------|----------------|
| Model     | RM SHE         | MAH E          | RM SHE     | MAVE       | RM SHE         | MAH E          |
| BS        | 0.575          | 0.479          | 0.659      | 0.513      | 0.903          | 0.650          |
| BS ( τ )  | 0.575          | 0.381          | 0.696      | 0.454      | 1.037          | 0.633          |
| BS(m)     | 0.638          | 0.510          | 0.736      | 0.546      | 0.953          | 0.672          |
| BS spline | 0.415          | 0.337          | 0.482      | 0.354      | 0.881          | 0.657          |
| NGARCH    | 0.598          | 0.583          | 0.615      | 0.511      | 0.802          | 0.600          |
| BL        | 0.537          | 0.432          | 0.600      | 0.455      | 0.789          | 0.560          |
