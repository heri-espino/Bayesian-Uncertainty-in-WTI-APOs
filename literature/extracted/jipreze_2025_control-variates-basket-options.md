---
id: "jipreze_2025_control-variates-basket-options"
source_pdf: "../pdf/jipreze_2025_control-variates-basket-options.pdf"
source_filename: "jipreze_2025_control-variates-basket-options.pdf"
format: "academic-paper"
extraction_profile: "token-efficient-high-fidelity"
extraction_mode: "hybrid"
extraction_quality: "excellent"
extraction_score: 108.0
formula_enrichment: "codeformulav2"
table_structure: "accurate"
tables_png: 9
figures_png: 0
assets_dir: "../assets/jipreze_2025_control-variates-basket-options"
references_file: "../references/jipreze_2025_control-variates-basket-options.references.md"
---

<!-- p:1 -->

IMA Journal of Management Mathematics (2025) 36 , 111-133 https://doi.org/10.1093/imaman/dpae023 Advance Access publication on 10 October 2024

## New control variates for pricing basket options

KAM JIPREZE AND PARESH DATE † Department of Mathematics, Brunel University London, UK † Corresponding author: paresh.date@brunel.ac.uk

[Received on 1 March 2023; accepted on 11 October 2024]

Accepted by: Giorgio Consigli

Accurate pricing of basket options, which are financial derivatives on multiple underlying assets, is a challenging and practically important task for financial institutions. We propose several new control variates for accurate, fast and efficient pricing of basket options. The first approach to deriving new control variates is the use of Hermite polynomial approximation of appropriate function of the underlying asset prices, which leads to a Black-Scholes-like analytic solution. This approach is new in the option pricing context and opens up new possibilities in derivative pricing. Further control variates are analytically derived using Jensen's inequality in one case, and distributional properties of multivariate Wiener processes in other cases. All the newly proposed control variates are shown to lead to excellent variance reduction in numerical experiments based on realistic data. The proposed methods are novel, computationally simple and have a strong potential to replace more conventional methods, such as the geometric lower bound in simulation-based pricing of basket options and similar products used in financial risk management.

Keywords :

finance; simulation; stochastic processes.

### 1. Introduction

A basket option is an option whose underlying is a group of assets and whose payoff depends on the weighted average of these assets at the maturity date. Basket options are popular over-thecounter financial instruments for cost-effective hedging of multiple underlying positions. Pricing baskets accurately can be challenging since the weighted average of the assets do not follow a closed-form distribution in general, even when the individual prices have a closed-form (e.g. lognormal) distribution. There is a significant amount of research over the past few decades on deriving approximate closedform prices for baskets. Kemna &amp; Vorst (1990) and Curran (1994) approximated the price of a basket option using the geometric mean of the prices of assets in the basket. Besides being a lower bound on the arithmetic mean, the geometric mean of lognormal random variables is also lognormal and leads to a closed-form estimate of basket option price. However, Gentle (1993) found that using a superposition of the strike and the expected difference of the average value of the basket and its geometric average yielded better approximations of the basket option price. In a different approach, Milevsky &amp; Posner (1998) obtained closed-form estimates for the basket option price, by approximating the distribution of the sum of the lognormal distribution by reciprocal gamma distribution. The only drawback is it was found to under-price out-of-the-money call options when compared with the Monte Carlo prices. Other closed-form approximations are based on moment matching and numerical approximations.

Methods of moment matching were used by Brigo et al. (2001) and Henriksen (2008) to approximate the price of a basket option. This approach generally involves using a lognormal random variable and matching its first and second moments with those of the basket. Ju (2002) used Taylor series expansion to price basket and Asian options.


<!-- p:2 -->


Despite several analytical approximations to pricing a basket option, Monte Carlo simulation remains the most accurate way of valuing such options. The biggest downsides of this approach are a high variance of the resulting estimates and a high computational cost. This has led to the use of various variance reduction methods, including antithetic variates and control variates based on closed-form bounds or approximations. De Luigi &amp; Maire (2010) used adaptive numerical techniques to price lowdimensional basket options and found that this technique served as good control variates in pricing highdimensional baskets. Dingeç&amp; Hörmann (2013) used a conditional Monte Carlo method along with geometric average as control variate to price basket options. Korn &amp; Zeytun (2013) proposed the use of a limiting approximation of the arithmetic mean by the geometric mean, to obtain closed-form estimates as well as low variance Monte Carlo estimates for the basket option price. Lai et al. (2015) used control variate to price basket option under jump diffusion models. This was extended to stochastic volatility models with jumps using relevant asymptotic expansions as control variates (Shiraya &amp; Takahashi, 2017). This method of asymptotic expansion was also previously used by Xu &amp; Zheng (2010) with Forward Partial Integro-Differential Equation to approximate the basket option price.

Dingeç (2019) also proposed new control variate models using time-changed Brownian motions for pricing and sensitivity analysis of Basket options. Shiraya et al. (2020) proposed a class of control variates for pricing basket options driven by Lévy processes with the use of subordinated Wiener processes. Zhang et al. (2019) extended this to exponential subordinated Wiener processes. Kreckel et al. (2004) provide a systematic numerical comparison of different basket option pricing methods. In the context of the existing work described above, the contribution of the paper can be summarized as follows:

1. For a basket of assets (which includes a practically important class of spread options), we introduce a new control variate for pricing basket options. This is done using a first-order Hermite polynomial approximation on the logarithm of a derived lower bound of the value of the basket, which is lognormally distributed. This leads to closed-form option price on the lower bound with modified strike, which is the logarithm of the strike of the basket.
2. We suggest the use of a new closed-form upper bound in terms of the Jensen's inequality as a control variate. To our knowledge, the use of this bound has not been explored in published literature. Using a fictitious basket option with volatilities and correlations of real-world indices, we demonstrate that the use of this bound as a control variate dramatically improves the variance of a Monte Carlo estimate.
3. We also propose two new distributional closed-form bounds on the basket option price: a lower bound using the minimum of Brownian motions and an upper bound using the maximum of Brownian motions provided certain integrability conditions are imposed. These bounds are new and contribute to the literature on stochastics. We demonstrate that these bounds can be used for variance reduction, with the distributional lower bound giving excellent variance reduction.

All our numerical experiments are benchmarked against a standard control variate, viz the geometric mean approximation as a lower bound on basket option price.

Note that the focus of this paper is variance reduction using novel control variates, which perform better than the benchmark method and lead to explicit analytic expressions. They also havethe potential to be useful for other multivariate Monte Carlo applications related to financial derivative pricing. Other variance reduction methods, such as importance sampling, hybrid methods (Sun &amp; Chenglong, 2018) and quasi-Monte Carlo methods are important in their own right, but are beyond the scope of this paper.


<!-- p:3 -->


The rest of the paper is organized as follows. Section 2 covers the modelling of the problem. Section 3 comprises numerical experiments which compare our new algorithms with the benchmark algorithms on realistic data sets. Section 4 concludes the paper.

### 2. Modelling approach

We model the economy with a filtered probability space (Ω , F , F t , Q ) , where Ω represents the sample space, { F t } t ≥ 0 represents the filtration generated by n independent Brownian motions W 1 ( t ) , ..., Wn ( t ) and Q is the risk neutral measure. We assume that the asset prices S i ( t ) are F t -measurable and follow a geometric Brownian motion (GBM) model given by

$$\text {each $S_{i}(t) \satisfies the stochastic differential equation,} & & \varnothing & & \varnothing & & \varnothing \\ S _ { i } ( t ) & = S _ { i } ( 0 ) \exp \left [ \left ( r - \frac { 1 } { 2 } \sigma _ { i } ^ { 2 } \right ) t + \sum _ { j = 1 } ^ { n } \sigma _ { i j } W _ { j } ( t ) \right ] , \, \forall i = 1 , \dots , n , & & \varnothing & & \varnothing & & \varnothing \\ \intertext { a c h S _ { i } ( r ) \satisfies the stochastic differential equation, }$$

i.e. each S i ( t ) satisfies the stochastic differential equation,

$$\frac { d S _ { i } ( t ) } { S _ { i } ( t ) } = r d t + \sum _ { j = 1 } ^ { n } \sigma _ { i j } d W _ { j } ( t ) . \quad & & ( 2 ) \\$$

Here r is the risk-free rate and σ is the volatility of the asset i such that σ 2 n σ 2 .

The value of a basket of n assets at a time t which satisfies (1)-(2) is given by

i i = ∑ j = 1 ij

where ω i ≥ 0 such that ∑ n i = 1 ω i = 1.

$$S ( t ) = \sum _ { i = 1 } ^ { n } \omega _ { i } S _ { i } ( t ) , & & \stackrel { \stackrel { \stackrel { \rightarrow } { \searrow } } { \rightarrow } } { \stackrel { \stackrel { \rightarrow } { \rightarrow } } { \rightarrow } } & & ( 3 ) & & \stackrel { \stackrel { \rightarrow } { \rightarrow } } { \rightarrow } & & \stackrel { \stackrel { \rightarrow } { \rightarrow } } { \rightarrow } & & \stackrel { \stackrel { \rightarrow } { \rightarrow } } { \rightarrow } & & \stackrel { \stackrel { \rightarrow } { \rightarrow } } { \rightarrow } & & \stackrel { \stackrel { \rightarrow } { \rightarrow } } { \rightarrow } & & \stackrel { \stackrel { \rightarrow } { \rightarrow } } { \rightarrow }$$

The price C ( 0, T , K ) of a basket call option at a time 0, with a strike K and maturing at time T , is

$$C ( 0 , T , K ) = e ^ { - r T } \mathbb { E } ^ { \mathbb { Q } } \left [ ( S ( T ) - K ) ^ { + } \right ] , \\ \text {tes the expectation under risk-neutral measure. In the subsequence, we } & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \infty & & \in$$

where E Q [ - ] denotes the expectation under risk-neutral measure. In the subsequent subsections, we derive the first-order Hermite polynomial control variate for pricing a basket option, which will later be used in Sections 3 and 4.

### 2.1. Lognormal approach using first-order hermite polynomials

For n = 1, we know that S ( t ) is lognormal and C ( 0, T , K ) is available in closed-form in terms of Black-Scholes formula. The main idea is to derive some lognormal random variable whose behaviour mimics that of the basket and which has a closed-form solution. If we can approximate the summation ∑ n i = 1 ω i S i ( t ) by a lognormal random variable with a known finite variance in closed-form, we can obtain a Black-Scholes-type approximate solution for the price of the basket option. Instead of trying to approximate S ( t ) directly e.g. using moments as in Leccadito et al. (2016), we construct a linear approximation of y ( t ) : = ln ( S ( t )) in terms of ln ( S i ( t )) , using a multivariate Hermite polynomial basis. As each ln ( S i ( t )) is normal, so is our approximation to y ( t ) . Consequently, e y ( t ) is lognormal and this allows us to use Black-Scholes-like formula for the basket option price, in terms of the parameters of our linear approximation. Evaluating the option price under GBM assumption always involves an accurate evaluation of integrals with respect to the Gaussian measure, which motivates our choice of Hermite polynomials as a basis for linear approximation. Given the function φ , which is the log of the terminal value of the basket, we can rewrite φ as a function of standard normal variables such that


<!-- p:4 -->


$$of the b a s k e t , we can rewrite \varphi as a function of standard normal variables such that \\ \varphi = \ln \left ( S ( T ) \right ) , \\ \\ = \ln \left ( \sum _ { i = 1 } ^ { n } \omega _ { i } S _ { i } ( 0 ) \exp \left ( \left ( r - \frac { 1 } { 2 } \sigma _ { i } ^ { 2 } \right ) T + \sum _ { i = 1 } ^ { n } \sigma _ { i j } W _ { j } ( T ) \right ) \right ) , \\ \\ = \ln \left ( \sum _ { i = 1 } ^ { n } \omega _ { i } S _ { i } ( 0 ) \exp \left ( \left ( r - \frac { 1 } { 2 } \sigma _ { i } ^ { 2 } \right ) T + \sqrt { T } \sum _ { j = 1 } ^ { n } \sigma _ { i j } u _ { j } \right ) \right ) , \\ \\ u _ { j } \sim \mathcal { N } ( 0 , 1 ) \ \forall j . \\ \text {non-linear function of Gaussian random variables can be approximated by a linear combination of} \\$$

Anon-linear function of Gaussian random variables can be approximated by a linear combination of standard normally distributed random variables using Hermite polynomial basis as follows. Consider a class of functions Y such that

$$\mathcal { Y } = \left \{ \varphi ( u ) \colon \int _ { - \infty } ^ { \infty } \phi ( u ; 0 , I ) \Phi ^ { 2 } ( u ) d u < \infty , \forall j \right \} ,$$

where φ( u ; 0, I ) is the density of a standard normal vector u = ( u 1 , ..., u n ) with covariance matrix I . We define the first-order Hermite polynomials { h ( 1 ) j ( u ) } n j = 1 as

$$h _ { j } ^ { ( 1 ) } ( u ) = ( - 1 ) \frac { \partial \phi ( u ; 0 , I ) } { \partial u _ { j } } \phi ^ { - 1 } ( u ; 0 , I ) , \\$$

where h ( 0 ) j ( u ) = 1 ∀ j . These polynomials satisfy the orthogonality condition with respect to the Gaussian density:

$$\int _ { - \infty } ^ { \infty } h _ { j } ^ { ( 1 ) } ( u ) h _ { k } ^ { ( 1 ) } ( u ) \phi ( u ; 0 , I ) d u = \delta _ { j k } ,$$

Since φ ∈ Y , we can approximate φ( u ) as

$$\varphi ( u ) & \approx \hat { \varphi } ( u ) = \sum _ { j = 0 } ^ { n } b _ { j } h _ { j } ^ { ( 1 ) } ( u ) , \\ & = b _ { 0 } + \sum _ { j = 1 } ^ { n } b _ { j } u _ { j } .$$

where u j ∼ N ( 0, 1 ) ∀ j .

where δ jk = { 1, if j = k 0, otherwise.


<!-- p:5 -->


The coefficients of the orthogonal expansion are obtained as

$$b _ { 0 } & = \int _ { - \infty } ^ { \infty } \varphi ( u ) \phi ( u ) d u \quad \text {and} , \\ b _ { 0 } & = \int _ { - \infty } ^ { \infty } \varphi ( u ) \phi ( u ) d u \quad \text {and} ,$$

$$- \int _ { - \infty } ^ { + \infty } \int _ { 0 } ^ { + \infty } \varphi ( u ) \phi ( u ) d u , \, 1 \leq j \leq n . \\ b _ { j } = \int _ { - \infty } ^ { \infty } u _ { j } \varphi ( u ) \phi ( u ) d u , \, 1 \leq j \leq n .$$

We can now approximate the basket option price under the assumption that the basket of assets in lognormally distributed.

PROPOSITION 1. The approximate price ˆ C ( 0, T , K ) of a basket option at a time 0 at an earlier time T with non-negative strike K is given by

$$\hat { C } ( 0 , T , K ) = e ^ { - r T } \left [ \exp \left ( \frac { 1 } { 2 } \left ( V + 2 b _ { 0 } \right ) \right ) \Phi \left ( \frac { b _ { 0 } + V - \ln K } { \sqrt { V } } \right ) - K \Phi \left ( \frac { b _ { 0 } - \ln K } { \sqrt { V } } \right ) \right ] , \quad ( 1 1 ) \\ \intertext { w h o r } \psi _ { V } = \sum _ { V } ^ { n } b _ { 2 } ^ { 2 }$$

Proof.

where V = ∑ n j = 1 b 2 j .

$$\hat { C } ( 0 , T , K ) = e ^ { - r T } \mathbb { E } ^ { \mathbb { Q } } \left [ \left ( e ^ { \hat { \phi } ( u ) } - K \right ) ^ { + } \right ] . \\ ( 1 2 ) \\ \hat { C } ( 0 , T , K ) = e ^ { - r T } \mathbb { E } ^ { \mathbb { Q } } \left [ \left ( e ^ { \hat { \phi } ( u ) } - K \right ) ^ { + } \right ] . \\ ( 1 2 ) \\ \hat { C } ( 0 , T , K ) = 0 .$$

We define the density ρ Φ ( y ) of ˆ Φ( u ) as

$$\rho _ { \phi } ( y ) = \frac { 1 } { \sqrt { V } } \phi \left ( \frac { y - b _ { 0 } } { \sqrt { V } } \right ) .$$

The approximate terminal payoff is given by

$$\mathbb { E } ^ { \mathbb { Q } } \left [ ( e ^ { \hat { \phi } ( u ) } - K ) ^ { + } \right ] & = \int _ { - \infty } ^ { \infty } \left ( e ^ { y } - K \right ) ^ { + } \rho _ { \Phi } ( y ) d y , \\ & = \exp \left ( \frac { 1 } { 2 y } \left [ ( b _ { 0 } + V ) ^ { 2 } - b _ { 0 } ^ { 2 } \right ] \right ) \Phi \left ( \frac { b _ { 0 } + V - \ln K } { \sqrt { V } } \right ) - K \Phi \left ( \frac { b _ { 0 } - \ln K } { \sqrt { V } } \right ) .$$

The approximated price ˆ C ( 0, T , K ) of the basket option, using a linear Hermite polynomial approximation, is thus given by

$$\hat { C } ( 0 , T , K ) = e ^ { - r T } \left [ \exp \left ( \frac { 1 } { 2 } \left ( V + 2 b _ { 0 } \right ) \right ) \Phi \left ( \frac { b _ { 0 } + V - \ln K } { \sqrt { V } } \right ) - K \Phi \left ( \frac { b _ { 0 } - \ln K } { \sqrt { V } } \right ) \right ] , \quad ( 1 5 ) \\ \intertext { w i h c o n t l e s the p r o f } \Phi \left ( 0 , T , K \right ) = e ^ { - r T } \left [ \exp \left ( \frac { 1 } { 2 } \left ( V + 2 b _ { 0 } \right ) \right ) \Phi \left ( \frac { b _ { 0 } + V - \ln K } { \sqrt { V } } \right ) - K \Phi \left ( \frac { b _ { 0 } - \ln K } { \sqrt { V } } \right ) \right ] , \quad ( 1 5 ) \\ \intertext { w i h c o n t l e s the p r o f } \prod _ { \substack { 0 } } \Phi$$

which completes the proof.

□

The closed-form approximation in equation (15) for a basket option price is analogous to BlackScholes representation for the price of a single asset.


<!-- p:6 -->


In practice, we estimate b j 's using a third-order Taylor series expansion of Φ about zero in equations (9) and (10), which leads to the integral in question being approximated by a simple linear function of moments of a Gaussian variable. Details are straightforward and are omitted for brevity. An alternative would be to use Gaussian quadrature to evaluate the said one-dimensional integrals. Also, this closed-form estimate can be used as a control variate for pricing basket options. However, the computational complexity of calculating the basket option price increases as the number of assets in the basket increases. To overcome this, we suggest an adaptation to the previously mentioned method to allow for its use as a control variate for pricing basket options with sufficiently large assets in the basket.

In general,

$$\ln ( 1 + \overline { S _ { i } ( T ) } ) \leq \overline { S _ { i } ( T ) } ,$$

where S i ( T ) = ω i S i ( T ) . Taking sums of (16) over i , we can deduce the following inequality:

$$\ln \left ( \prod _ { i = 1 } ^ { n } \overline { S _ { i } ( T ) } \right ) < \sum _ { i = 1 } ^ { n } \ln \left ( 1 + \overline { S _ { i } ( T ) } \right ) < \sum _ { i = 1 } ^ { n } \overline { S _ { i } ( T ) } = S ( T ) .$$

We can simplify the weighted products of assets as

$$\prod _ { i = 1 } ^ { n } \overline { S _ { i } ( T ) } = \left ( \prod _ { i = 1 } ^ { n } \overline { S _ { i } ( 0 ) } \right ) \exp \left [ \left ( n r - \frac { 1 } { 2 } \sum _ { i = 1 } ^ { n } \sigma _ { i } ^ { 2 } \right ) T \right ] \exp \left ( \sum _ { i = 1 } ^ { n } \sum _ { j = 1 } ^ { n } \sigma _ { i j } W _ { j } ( T ) \right ) , \quad ( 1 8 ) ^ { ( 1 8 ) } \stackrel { ( 1 8 ) } { \sim } \stackrel { ( 1 8 ) } { \geq } \stackrel { ( 1 8 ) } { \sim } \stackrel { ( 1 8 ) } { \geq } \stackrel { ( 1 8 ) } { \sim } \stackrel { ( 1 8 ) } { \geq } \stackrel { ( 1 8 ) } { \sim } \stackrel { ( 1 8 ) } { N } \stackrel { ( 1 8 ) } { \sim } \stackrel { ( 1 8 ) } { \sim } \stackrel { ( 1 8 ) } { \sim } \stackrel { ( 1 8 ) } { N } \stackrel { ( 1 8 ) } { \sim } \stackrel { ( 1 8 ) } { \sim } \stackrel { ( 1 8 ) } { N }$$

and its logarithm becomes

$$\ln \left ( \prod _ { i = 1 } ^ { n } \overline { S _ { i } ( T ) } \right ) = \ln \left ( \prod _ { i = 1 } ^ { n } \overline { S _ { i } ( 0 ) } \right ) + \left ( n r - \frac { 1 } { 2 } \sum _ { i = 1 } ^ { n } \sigma _ { i } ^ { 2 } \right ) T + \sum _ { i = 1 } ^ { n } \sum _ { j = 1 } ^ { d } \sigma _ { i j } W _ { j } ( T ) , \quad \\$$

$$= \gamma + \sum _ { i = 1 } ^ { n } \sum _ { j = 1 } ^ { n } \sigma _ { i j } W _ { j } ( T ) ,$$

where γ = ln ( ∏ n i = 1 S i ( 0 ) ) + ( nr - 1 2 n ∑ i = 1 σ 2 i ) T .


<!-- p:7 -->


We define a new function φ ′ by simply replacing S ( T ) in (5) with the logarithm of (20) and the strike of the basket with ln K to obtain

where u j ∼ Φ( 0, 1 ) ∀ j .

$$\begin{array} { l l } \text {function $\varphi$ by simply replacing $S(T)$ in $(5)$ with the logarithm of $(20)$ and the strike} \\ K \text { to obtain} \\ \\ & \varphi ^ { \prime } = \ln \left ( \ln \left ( \prod _ { i = 1 } ^ { n } S ( T ) \right ) \right ) , \\ \\ & = \ln \left ( \gamma + \sum _ { i = 1 } ^ { n } \sum _ { j = 1 } ^ { n } \sigma _ { i j } W _ { j } ( T ) \right ) , \\ \\ & = \ln \left ( \gamma + \sqrt { T } \sum _ { i = 1 } ^ { n } \sum _ { j = 1 } ^ { n } \sigma _ { i j } u _ { j } \right ) , \\ \\ \forall j . \\ \text { can approximate $\varphi^{\prime}(u)$ as} & \quad \stackrel { \circledast } { \leq } & \stackrel { \circledast } { \geq } & \stackrel { \circledast } { \geq } \\ & = \ln \left ( \gamma + \sqrt { T } \sum _ { i = 1 } ^ { n } \sum _ { j = 1 } ^ { n } \sigma _ { i j } u _ { j } \right ) , \\ \\ \forall j . \\ \text { can approximate $\varphi^{\prime}(u)$ as} & \quad \stackrel { \circledast } { \leq } & \stackrel { \circledast } { \geq } & \stackrel { \circledast } { \geq } \end{array}$$

Since φ ′ ∈ Y , we can approximate φ ′ ( u ) as

$$\varphi ^ { \prime } ( u ) = b _ { 0 } ^ { \prime } + \sum _ { j = 1 } ^ { n } b _ { j } ^ { \prime } u _ { j } , & & ( 2 3 ) ^ { \frac { 1 } { 2 0 } } & & \stackrel { \stackrel { \stackrel { \circledast } { 0 } } { 0 } } { \stackrel { \stackrel { \circledast } { 1 } } { 0 } } \\$$

where the parameters b ′ j 's are estimated as b j 's in (9) and (10) but are estimated by replacing φ with φ ′ for all 0 ≤ j ≤ n .

We can estimate the parameters of b ′ j 's in (23) using a third-order Taylor series approximation of φ ′ of u j 's about 0 given by

$$\dot { s } \text { about 0 given by} & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & &$$

Thus, the coefficients of the parameters of Φ ′ are

$$b _ { 0 } ^ { \prime } & = \ln \gamma - \frac { 1 } { 2 } \frac { T } { \rho ^ { 2 } } \sum _ { j = 1 } ^ { n } \sum _ { k = 1 } ^ { n } \sum _ { i = 1 } ^ { n } \sigma _ { i j } \sigma _ { k j } , \\ & = \ln \gamma - \frac { 1 } { 2 } \frac { T } { \rho ^ { 2 } } \sum _ { k = 1 } ^ { n } \sum _ { i = 1 } ^ { n } A _ { i k } ,$$

$$1 ^ { n } i = 1 ^ { n } k =
 e \sum _ { k = 1 } ^ { n } \sum _ { i = 1 } ^ { n } A$$

where A is the volatility matrix, ρ = γ + √ T n ∑ i = 1 n ∑ j = 1 σ ij u j and

$$b _ { j } ^ { \prime } = \frac { \sqrt { T } } { \gamma } \sum _ { i = 1 } ^ { n } \sigma _ { i j } + \left ( \frac { \sqrt { T } } { \gamma } \right ) ^ { 3 } \sum _ { i = 1 } ^ { n } \sum _ { l = 1 } ^ { n } \sum _ { m = 1 } ^ { n } \sigma _ { i j } \sigma _ { l j } \sigma _ { m j } + \left ( \frac { \sqrt { T } } { \gamma } \right ) ^ { 3 } \sum _ { k = 1 } ^ { n } \sum _ { i = 1 } ^ { n } \sum _ { l = 1 } ^ { n } \sum _ { m = 1 } ^ { n } \sigma _ { i j } \sigma _ { m k } \sigma _ { l j k } ,$$

for all 1 ≤ j ≤ n .


<!-- p:8 -->


We denote the price at time 0 of an option on the logarithm of the product of weighted assets in the basket with a strike ln K , maturing at time T as C ′ ( 0, T , ln K ) is given by

$$C ^ { \prime } ( 0 , T , \ln K ) = e ^ { - r T } \mathbb { E } ^ { \mathbb { Q } } \left [ \left ( \ln \left ( \prod _ { i = 1 } ^ { n } S ( T ) \right ) - \ln K \right ) ^ { + } \right ] .$$

Using the lognormal approximation for ln ( ∏ n i = 1 S ( T ) ) in (23), we can obtain the option price C ′ ( 0, T , ln K ) in a lognormal framework. Thus, the option price C ′ ( 0, T , ln K ) is given by

$$C ^ { \prime } ( 0 , T , \ln K ) = e ^ { - r T } \left [ \exp \left ( \frac { 1 } { 2 } \left ( \bar { V } + 2 b _ { 0 } ^ { \prime } \right ) \right ) \Phi \left ( \frac { b _ { 0 } ^ { \prime } + V - \ln \bar { K } } { \sqrt { \bar { V } } } \right ) - \bar { K } \Phi \left ( \frac { b _ { 0 } ^ { \prime } - \ln \bar { K } } { \sqrt { \bar { V } } } \right ) \right ] , \quad ( 2 9 ) \\ \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } = \bar { \ } =$$

where  ̄ K = ln K and  ̄ V = ∑ n j = 1 b ′ j 2 . Given that we have the price of the option C ′ ( 0, T , ln K ) in closed-form, we have all the essential ingredients necessary to use this method for pricing basket options, using the first-order Hermite polynomial as a control variate for a large number of underlying assets.

### 2.2. Direct upper bound

As a second control variate, we look at an upper bound on the option price. As mentioned earlier, a lot of analytical work was done in estimating bounds on its price (Rogers &amp; Shi (1995), Xu &amp; Zheng (2010)). However, we can obtain an easy and direct upper bound on the price of a basket option by a direct application of the Jensen's inequality due to the convexity of the payoff function of the basket. To our knowledge, this bound has not been used in the published literature and can be explained as follows.

$$\mathbb { E } \left ( S ( T ) - K \right ) ^ { + } = \mathbb { E } \left ( \sum _ { i = 1 } ^ { n } \omega _ { i } S _ { i } ( T ) - K \right ) ^ { + } \leq \sum _ { i = 1 } ^ { n } \omega _ { i } \mathbb { E } \left ( S _ { i } ( T ) - K \right ) ^ { + } . \\$$

So that,

$$e ^ { - r T } \mathbb { E } \left ( S ( T ) - K \right ) ^ { + } & \leq e ^ { - r T } \sum _ { i = 1 } ^ { n } \omega _ { i } \mathbb { E } \left ( S _ { i } ( T ) - K \right ) ^ { + } = \colon U _ { B } . \\$$

The upper bound UB on the price of a basket option can be seen as the same as holding n options of different assets with the same strike K . The price UB of such a fictitious portfolio is given by

$$U _ { B } = e ^ { - r T } \sum _ { i = 1 } ^ { n } \left [ S _ { i } ( 0 ) e ^ { r T } \Phi ( h _ { i } ^ { + } ) - K \Phi ( h _ { i } ^ { - } ) \right ] ,$$

where h i ± = ln ( Si ( 0 ) e rT K ) ± 1 2 σ 2 i T σ i √ T .


<!-- p:9 -->


While an upper bound similar to the one presented in this paper has also been discussed in Yu et al. (2022), there is a conceptual difference in how the bound is arrived at: we average over individual options with the same strike, whereas Yu et al. (2022) average over the geometric mean of the basket.

### 2.3. Distributional bounds

Some of the research into finding suitable bounds on the price of a basket option involve using the properties of its payoff function such as in the Rogers-Shi lower bound (Rogers &amp; Shi, 1995). In this section, we derive new upper and lower bounds on a basket of assets and their corresponding option price using the distributional properties of Brownian motions.

2.3.1. Lower and upper distributional bounds of a basket option. We can obtain an upper bound on the basket of assets in (3) and the price of a basket option in (4) by replacing the independent Wiener processes with their joint maximum. Similarly, we can also obtain lower bounds on the basket and its corresponding option price by replacing the independent Wiener processes with their joint minimum.

PROPOSITION 2. The value S ( t ) of the basket of assets at any time t is bounded above by

$$S _ { u } ( t ) = \sum _ { i = 1 } ^ { n } \omega _ { i } S _ { i } ( 0 ) \exp \left ( ( r - \frac { 1 } { 2 } \sigma _ { i } ^ { 2 } ) t \right ) \exp \left ( M _ { n } ( t ) \sum _ { j = 1 } ^ { n } \sigma _ { i j } \right ) , \quad ( 3 3 ) \sum _ { \substack { 1 \div 2 \\ \frac { 1 0 } { 2 } \\ \frac { 1 0 } { 2 } } } ^ { \frac { 1 } { 2 } }$$

and bounded below by

$$S _ { l } ( t ) = \sum _ { i = 1 } ^ { n } \omega _ { i } S _ { i } ( 0 ) \exp \left ( ( r - \frac { 1 } { 2 } \sigma _ { i } ^ { 2 } ) t \right ) \exp \left ( m _ { n } ( t ) \sum _ { j = 1 } ^ { n } \sigma _ { i j } \right ) , \quad ( 3 4 ) \sum _ { \substack { 1 \div 2 \\ \div \frac { 1 } { 2 } \div 1 } } ^ { \frac { 1 } { 2 } } \sigma _ { i j } \right ) ,$$

where M n ( t ) = max 1 ≤ j ≤ n Wj ( t ) , mn ( t ) = min 1 ≤ j ≤ n Wj ( t ) and provided n ∑ j = 1 σ ij is non-negative for 1 ≤ i ≤ n .

Proof. Given that the assets in the basket follow a GBM model, we set up the following inequalities:

$$m _ { n } ( t ) \sum _ { j = 1 } ^ { n } \sigma _ { i j } \leq \sum _ { j = 1 } ^ { n } \sigma _ { i j } W _ { j } ( t ) \leq M _ { n } ( t ) \sum _ { j = 1 } ^ { n } \sigma _ { i j } , \quad \\$$

where Mn ( t ) = max 1 ≤ j ≤ n Wj ( t )) and mn ( t ) = min 1 ≤ j ≤ n Wj ( t ) ,

so that the price of the basket at time t is bounded by

$$S _ { l } ( t ) = \sum _ { i = 1 } ^ { n } Y _ { i } \exp \left ( m ( t ) \sigma _ { i } ^ { * } \right ) \leq S ( t ) \leq \sum _ { i = 1 } ^ { n } Y _ { i } \exp \left ( M ( t ) \sigma _ { i } ^ { * } \right ) = S _ { u } ( t ) ,$$

These bounds on the value of the basket given by S u ( t ) and S l ( t ) are analytically intractible and are of a similar problem-type as the the basket of assets. To this end, we can estimate options on S u ( t ) and

$$where \sigma _ { i } ^ { * } & = \sum _ { j = 1 } ^ { n } \sigma _ { i j } , \sigma _ { i } ^ { 2 } = \sum _ { j = 1 } ^ { n } \sigma _ { i j } ^ { 2 } \text { and } Y _ { i } = \omega _ { i } S _ { i } ( 0 ) \exp \left [ \left ( r - \frac { 1 } { 2 } \sigma _ { i } ^ { 2 } \right ) T \right ] . \\ & \text { These bounds on the value of the basket given by } S _ { i } ( r ) \text { and } S _ { i } ( r ) \text { are analytically intractable and are } \\$$


<!-- p:10 -->


S l ( t ) using their respective geometric means as suggested by Gentle (1993). Given the representations of the distributional upper and lower bound on the value of a basket of n assets at a time T given by S u ( T ) and S l ( T ) , respectively, in proposition 2. Let Gu ( T ) denote the geometric mean of (33), which has the following representation:

$$G _ { u } ( T ) = \prod _ { i = 1 } ^ { n } \left [ S _ { i } ( 0 ) \exp \left [ \left ( r - \frac { 1 } { 2 } \sigma _ { i } ^ { 2 } \right ) T \right ] \exp \left ( M _ { n } ( T ) \sum _ { j = 1 } ^ { n } \sigma _ { i j } \right ) \right ] ^ { \frac { 1 } { n } } . \\ \intertext { c h e n s } \text {when this representation of } G _ { u } ( T ) , \text { we can use it to estimate the price of an option on } S _ { u } ( T ) , \text { which is } \sum _ { \substack { i = 1 \\ i \geq 0 \\ 0 \stackrel { \circledast } { \geq } 0 } } ^ { n } \sigma _ { i j } .$$

Given this representation of Gu ( T ) , we can use it to estimate the price of an option on S u ( T ) , which is an the upper bound on the basket option price with the same strike.

PROPOSITION 3. The price C Gu ( 0, T ) at time 0 of an option on the geometric mean Gu ( T ) , maturing at time T with non-negative strike K , is given by

$$C _ { G _ { u } } \left ( 0 , T \right ) = \alpha _ { 1 } \beta _ { 1 } e ^ { - r T } \int _ { \tilde { K } } ^ { \infty } e ^ { \gamma _ { 1 } y } \frac { n } { \sqrt { T } } \phi \left ( \frac { y } { \sqrt { T } } \right ) \left ( \Phi \left ( \frac { y } { \sqrt { T } } \right ) \right ) ^ { n - 1 } d y - K e ^ { - r T } \left [ 1 - \left ( \Phi \left ( \frac { \tilde { K } } { \sqrt { T } } \right ) \right ) ^ { n } \right ] ,$$

where α 1 = ∏ n i = 1 S i ( 0 ) 1 n , β 1 = exp [( r - 1 2 ∑ n i = 1 σ 2 i n ) T ] , γ 1 = 1 n ∑ n i = 1 ∑ n j = 1 σ ij and  ̃ K = 1 γ 1 ln ( K α 1 β 1 ) .

Proof. We can simplify the expression for Gu ( T ) in (37) to become

$$G _ { u } ( T ) = & \left ( \prod _ { i = 1 } ^ { n } \left ( S _ { i } ( 0 ) \right ) ^ { \frac { 1 } { n } } \right ) \exp \left [ \left ( r - \frac { 1 } { 2 } \sum _ { i = 1 } ^ { n } \frac { \sigma _ { i } ^ { 2 } } { n } T \right ) \right ] \exp \left ( M _ { n } ( T ) \frac { 1 } { n } \sum _ { i = 1 } ^ { n } \sum _ { j = 1 } ^ { n } \sigma _ { i j } \right ) . \\ \intertext { The price C _ { G } \ ( 0 , T ) \ of the option on G _ { ( T ) } at a time 0 is given by }$$

The price C Gu ( 0, T ) of the option on Gu ( T ) at a time 0 is given by

$$The price \, C _ { G _ { u } } ( 0 , T ) \, of \, the \, \text {option on } G _ { u } ( T ) \, \text { at a time } 0 \, \text { is given by} \\ & \quad C _ { G _ { u } } ( 0 , T ) = e ^ { - r T } \mathbb { E } \left [ ( G _ { u } ( T ) - K ) ^ { + } \right ] , \\ & = e ^ { - r T } \int _ { \tilde { K } } ^ { \infty } \left ( \alpha _ { 1 } \beta _ { 1 } e ^ { \gamma y _ { 1 } } - K \right ) \frac { n } { \sqrt { T } } \phi \left ( \frac { y } { \sqrt { T } } \right ) \left ( \Phi \left ( \frac { y } { \sqrt { T } } \right ) \right ) ^ { n - 1 } d y , \\ & = \alpha _ { 1 } \beta _ { 1 } e ^ { - r T } \int _ { \tilde { K } } ^ { \infty } e ^ { y y _ { 1 } } \frac { n } { \sqrt { T } } \phi \left ( \frac { y } { \sqrt { T } } \right ) \left ( \Phi \left ( \frac { y } { \sqrt { T } } \right ) \right ) ^ { n - 1 } d y \\ & \quad - K e ^ { - r T } \left [ 1 - \left ( \Phi \left ( \frac { \tilde { K } } { \sqrt { T } } \right ) \right ) ^ { n } \right ] . \\$$

This completes the proof.

□


<!-- p:11 -->


Similarly, given the geometric mean of S l ( T ) in (34), we can also derive the price of an option on it with the same strike K . We can define the geometric mean Gl ( T ) of S l ( T ) as

$$G _ { l } ( T ) = \prod _ { i = 1 } ^ { n } \left [ S _ { i } ( 0 ) \exp \left [ \left ( r - \frac { 1 } { 2 } \sigma _ { i } ^ { 2 } \right ) T \right ] \exp \left ( m _ { n } ( T ) \sum _ { j = 1 } ^ { n } \sigma _ { i j } \right ) \right ] ^ { \frac { 1 } { n } } .$$

PROPOSITION 4. The price C Gl ( 0, T ) of an option on Gl ( T ) , maturing at T at a time 0 with non-negative strike K , is given by

$$C _ { G _ { I } } ( 0 , T ) = e ^ { - r T } \int _ { \tilde { K } } ^ { \infty } e ^ { \gamma _ { 1 } y } \frac { n } { \sqrt { T } } \phi \left ( \frac { y } { \sqrt { T } } \right ) \left ( \Phi \left ( - \frac { y } { \sqrt { T } } \right ) \right ) ^ { n - 1 } d y + K e ^ { - r T } \left ( \Phi \left ( - \frac { \tilde { K } } { T } \right ) \right ) ^ { n } ,$$

where α 1 = ∏ n i = 1 S i ( 0 ) 1 n , β 1 = exp [( r - 1 2 ∑ n i = 1 σ 2 i n ) T ] , γ 1 = 1 n ∑ n i = 1 ∑ n j = 1 σ ij and  ̃ K = 1 γ 1 ln ( K α 1 β 1 ) .

Hence, we are able to use the bounds (33) and (34) on the value of the basket to obtain closedform bounds on the price of a basket option using their respective geometric means. Alternatively, we can obtain more accurate distributional bounds on the price of a basket option. This can be achieved by conditioning the option price of the distributional bounds on the value of the basket with the same strike K on its geometric mean as suggested by Curran (1994). We demonstrate this in the next two propositions.

PROPOSITION 5. The estimated option price C u B ( 0, T ) on S u ( T ) with strike K , at a time 0 prior to its maturity T using Curran's conditioning arguments, is given by

$$C _ { B } ^ { u } ( 0 , T ) = e ^ { - r T } \mathbb { E } \left [ S _ { u } ( T ) \mathbb { 1 } \{ G _ { u } ( T ) \geq K \} \right ] + K e ^ { - r T } \left [ \left ( \Phi \left ( \frac { 1 } { \gamma _ { 1 } } \ln \left ( \frac { K } { \alpha _ { 1 } \beta _ { 1 } } \right ) \right ) \right ) ^ { \prime \prime } - 1 \right ] , \quad ( 4 3 )$$

[( ) ]

where S u ( T ) is as defined is (33), α 1 = ∏ n i = 1 S i ( 0 ) 1 n , β 1 = exp r - 1 2 ∑ n i = 1 σ 2 i n T , γ 1 = 1 n ∑ n i = 1 ∑ n j = 1 σ ij .


<!-- p:12 -->


Proof. The price at time 0 an option on S u ( T ) prior to the maturity T is given by

$$P o f . \ \ The price at time 0 \an option on S _ { u } ( T ) \ prior to the matracity T \ is given by \\ & C _ { B } ^ { u } ( 0 , T ) = e ^ { - r T } \mathbb { E } \left [ ( S _ { u } ( T ) - K ) ^ { + } \right ] , \\ & = e ^ { - r T } \mathbb { E } \left [ \mathbb { E } \left [ ( S _ { u } ( T ) - K ) ^ { + } \left | G _ { u } ( T ) = y \right ] \right ] , \\ & = e ^ { - r T } \int _ { 0 } ^ { K } \mathbb { E } \left [ ( S _ { u } ( T ) - K ) ^ { + } \left | G _ { u } ( T ) = y \right ] \mathbb { Q } \left ( G _ { u } ( T ) \in d y \right ) , \\ & + e ^ { - r T } \int _ { K } ^ { \infty } \mathbb { E } \left [ ( S _ { u } ( T ) - K ) ^ { + } \left | G _ { u } ( T ) = y \right ] \mathbb { Q } \left ( G _ { u } ( T ) \in d y \right ) . \\ \intertext { W e u s e the f a t h } & \int _ { K } ^ { K } \mathbb { E } \left [ ( S _ { u } ( T ) - K ) ^ { + } \left | C _ { u } ( T ) = y \right ] \mathbb { Q } \left ( G _ { u } ( T ) \in d y \right ) .$$

We use the fact that

$$\int _ { 0 } ^ { K } \mathbb { E } \left [ ( S _ { u } ( T ) - K ) ^ { + } \left | G _ { u } ( T ) = y \right ] \mathbb { Q } \left ( G _ { u } ( T ) \in d y \right ) \approx 0 . \\ \int ( 4 ) \, \text {in} \, ( 4 6 ) \, \text {to obtain}$$

Substituting (47) in (46) to obtain

$$C _ { B } ^ { u } ( 0 , T ) & = e ^ { - r T } \int _ { K } ^ { \infty } \mathbb { E } \left [ \left ( S _ { u } ( T ) - K \right ) ^ { + } \left | G _ { u } ( T ) = y \right ] \mathbb { Q } \left ( G _ { u } ( T ) \in d y \right ) , \\ & = e ^ { - r T } \int _ { K } ^ { \infty } \mathbb { E } \left [ S _ { u } ( T ) - K \left | G _ { u } ( T ) = y \right ] \mathbb { Q } \left ( G _ { u } ( T ) \in d y \right ) ,$$

=

$$J K \\ & = e ^ { - r T } \int _ { K } ^ { \infty } \mathbb { E } \left [ S _ { u } ( T ) - K \left | G _ { u } ( T ) = y \right ] \mathbb { Q } \left ( G _ { u } ( T ) \in d y \right ) , \\ & = e ^ { - r T } \mathbb { E } \left [ S _ { u } ( T ) \mathbb { 1 } \{ G _ { u } ( T ) \geq K \} \right ] - K e ^ { - r T } \mathbb { Q } \left ( G _ { u } ( T ) \geq K \right ) ,$$

e

-

rT

E

S u

(

T

)

1

{

Gu

(

T

)

≥

K

}

-

Ke

-

rT

Q

Gu

(

T

)

≥

K

,

(50)

$$= e ^ { - r T } \mathbb { E } \left [ S _ { u } ( T ) \mathbb { I } \{ G _ { u } ( T ) \geq K \} \right ] - K e ^ { - r T } \left [ 1 - \left ( \Phi \left ( \frac { 1 } { \gamma _ { 1 } } \ln \left ( \frac { K } { \alpha _ { 1 } \beta _ { 1 } } \right ) \right ) ^ { n } \right ) \right ] . \\ \text {Thus, we are able to obtain the required results}$$

[

]

Thus, we are able to obtain the required results.

□

The option price given by C u B ( 0, T ) is an upper bound on the basket option price in (4). Next, we shall proceed to work out the lower bound on the basket option price using similar conditioning arguments.

PROPOSITION 6. The estimated option price C l B ( 0, T ) on S l ( T ) , with strike K at a time 0 prior to its maturity T using Curran's conditioning arguments, is given by

$$C _ { B } ^ { l } ( 0 , T ) = e ^ { - r T } \mathbb { E } \left [ S _ { l } ( T ) \mathbb { 1 } \{ G _ { l } ( T ) \geq K \} \right ] + K e ^ { - r T } \left [ \left ( \Phi \left ( - \frac { 1 } { \gamma _ { 1 } } \ln \left ( \frac { K } { \alpha _ { 1 } \beta _ { 1 } } \right ) \right ) \right ) \right ) ^ { n } \right ] , \quad ( 5 2 ) \\$$

$$\frac { 1 } { n } \sum _ { i = 1 } ^ { n } \sum _ { j = 1 } ^ { n } \sigma _ { i j } .$$

where S l ( T ) is as defined is (34), α 1 = ∏ n i = 1 S i ( 0 ) 1 n , β 1 = exp [( r - 1 2 ∑ n i = 1 σ 2 i n ) T ] , γ 1 =

(

)


<!-- p:13 -->


Proof. The price at time 0 an option on S l ( T ) prior to the maturity T is given by

$$P o f . \ \ The price at time 0 \an option on S _ { l } ( T ) \ prior to the matURITY T \ is given by \\ C _ { B } ^ { l } ( 0 , T ) = e ^ { - r T } \mathbb { E } \left [ ( s _ { l } ( T ) - K ) ^ { + } \right ] , \\ = e ^ { - r T } \mathbb { E } \left [ \mathbb { E } \left [ ( S _ { l } ( T ) - K ) ^ { + } \left | G _ { l } ( T ) = y \right ] \right ] , \\ = e ^ { - r T } \int _ { 0 } ^ { K } \mathbb { E } \left [ ( s _ { l } ( T ) - K ) ^ { + } \left | G _ { l } ( T ) = y \right ] \mathbb { Q } \left ( G _ { l } ( T ) \in d y \right ) , \\ + e ^ { - r T } \int _ { K } ^ { \infty } \mathbb { E } \left [ ( S _ { l } ( T ) - K ) ^ { + } \left | G _ { l } ( T ) = y \right ] \mathbb { Q } \left ( G _ { l } ( T ) \in d y \right ) . \\ \intertext { w e s u t h e f a t h } \int _ { K } ^ { K } \mathbb { E } \left [ ( s _ { l } ( T ) - K ) ^ { + } \left | G _ { l } ( T ) = y \right ] \mathbb { Q } \left ( G _ { l } ( T ) \in d y \right ) . \\ \intertext { w e s u t h e f a t h } \int _ { K } ^ { K } \mathbb { E } \left [ ( s _ { l } ( T ) - K ) ^ { + } \left | G _ { l } ( T ) = y \right ] \mathbb { Q } \left ( G _ { l } ( T ) \in d y \right ) .$$

We use the fact that

$$\int _ { 0 } ^ { K } \mathbb { E } \left [ ( S _ { l } ( T ) - K ) ^ { + } \left | G _ { l } ( T ) = y \right ] \mathbb { Q } \left ( G _ { l } ( T ) \in d y \right ) \approx 0 . \\ \int ( 5 6 ) \, \text {in} \, ( 5 5 ) \, \text {to obtain}$$

Substituting (56) in (55) to obtain

$$Substituting \, ( 5 ) \, in \, ( 5 5 ) \, to \, \text {obtain} & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & &$$

Thus, we are able to obtain the required results.

□

Given the analytic intractibility of the bounds S l ( t ) and S u ( t ) on the value of the basket at any time t , we can impose integrability conditions on the the volatility parameters, allowing for closed-form evaluation of options on these bounds. These integrability conditions lead to bounds on the value of the basket given by

$$\bar { S } _ { l } ( t ) = \sum _ { i = 1 } ^ { n } Y _ { i } \exp \left ( m _ { n } ( t ) \sigma _ { m } \right ) \leq S ( t ) \leq \sum _ { i = 1 } ^ { n } Y _ { i } \exp \left ( M _ { n } ( t ) \sigma _ { M } \right ) = \bar { S } _ { u } ( t ) , \quad \\$$

PROPOSITION 7. Given the lower bound  ̄ S l ( t ) on the value of a basket S ( t ) at a time t , its density and distribution

$$& \text {where } \sigma _ { i } ^ { 2 } = \sum _ { j = 1 } ^ { n } \sigma _ { i j } ^ { 2 } , \sigma _ { M } = \max _ { 1 \leq i \leq n } \sigma _ { i } ^ { * } \text { and } \sigma _ { m } = \min _ { 1 \leq i \leq n } \sigma _ { i } ^ { * } \text { and } Y _ { i } = \omega _ { i } S _ { i } ( 0 ) \exp \left [ \left ( r - \frac { 1 } { 2 } \sigma _ { i } ^ { 2 } \right ) T \right ] . \\ & \text {Proposition } 7 . \text { Given the lower bound } \bar { S } _ { l } ( t ) \text { on the value of } a \text { basket } S ( t ) \text { at } t \text { time } t , \text { its density } \text { and }$$

$$\mathbb { Q } \left ( \bar { S } _ { l } ( t ) \in d y \right ) = \frac { 1 } { y } \frac { 1 } { \sigma _ { m } \sqrt { T } } n \phi \left ( \frac { 1 } { \sigma _ { m } \sqrt { T } } \ln \left ( \frac { y } { \vartheta } \right ) \right ) \left [ 1 - \Phi \left ( \frac { 1 } { \sigma _ { m } \sqrt { T } } \ln \left ( \frac { y } { \vartheta } \right ) \right ) \right ] ^ { n - 1 } d y ,$$


<!-- p:14 -->


are given by the following and

$$\mathbb { Q } \left ( \bar { S } _ { l } ( t ) \leq y \right ) = 1 - \left [ 1 - \Phi \left ( \frac { 1 } { \sigma _ { m } \sqrt { T } } \ln \left ( \frac { y } { \vartheta } \right ) \right ) \right ] ^ { n } ,$$

respectively, where θ = ∑ n i = 1 ω i S i ( 0 ) exp [ ( r - 1 2 σ 2 i ) T ] .

PROPOSITION 8. Given the upper bound  ̄ S u ( t ) on the value of a basket S u ( t ) , its density and distribution

$$\mathbb { Q } \left ( \bar { S } _ { u } ( t ) \in d y \right ) = \frac { 1 } { y } \frac { 1 } { \sigma _ { M } \sqrt { T } } n \phi \left ( \frac { 1 } { \sigma _ { M } \sqrt { T } } \ln \left ( \frac { y } { \vartheta } \right ) \right ) \left ( \Phi \left ( \frac { 1 } { \sigma _ { M } \sqrt { T } } \ln \left ( \frac { y } { \alpha } \right ) \right ) \right ) ^ { n - 1 } d y , \quad ( 6 4 ) \\$$

are given by the following and

$$\mathbb { Q } \left ( \bar { S } _ { u } ( t ) \leq y \right ) = \left ( \Phi \left ( \frac { 1 } { \sigma _ { M } \sqrt { T } } \ln \left ( \frac { y } { \vartheta } \right ) \right ) \right ) ^ { n } , \\$$

respectively, where θ = ∑ n i = 1 ω i S i ( 0 ) exp [ ( r - 1 2 σ 2 i ) T ] .

PROPOSITION 9. Given a basket of assets, which has the lower and upper bounds  ̄ S l ( t ) and  ̄ S u ( t ) , respectively, as specified in (61), such a basket has the following bounds on the price of the basket option with maturity T and strike K at a time 0 given by

$$U B _ { 1 } ^ { n } = n e ^ { - r T } \frac { \sum _ { 1 } ^ { n } Y _ { 1 } } { \sqrt { T } } \int _ { \xi } ^ { \infty } e ^ { \sigma _ { M Y } } \phi \left ( \frac { y } { \sqrt { T } } \right ) \left ( \Phi \left ( \frac { y } { \sqrt { T } } \right ) \right ) ^ { n - 1 } d y - K e ^ { - r T } \left [ 1 - \left ( \Phi \left ( \frac { \xi } { \sqrt { T } } \right ) \right ) ^ { n } \right ] , \quad ( 6 6 ) \\$$

and

$$L B _ { 1 } ^ { n } = n e ^ { - r T } \frac { \sum _ { i = 1 } ^ { n } Y _ { i } } { \sqrt { T } } \int _ { \tau } ^ { \infty } e ^ { \sigma _ { m } y } \phi \left ( \frac { y } { \sqrt { T } } \right ) \left ( 1 - \Phi \left ( \frac { y } { \sqrt { T } } \right ) \right ) ^ { n - 1 } d y + K e ^ { - r T } \left [ 1 - \Phi \left ( \frac { \tau } { \sqrt { T } } \right ) \right ] ^ { n } ,$$

where Y i = ω i S i ( 0 ) exp [( r - 1 2 σ 2 i ) T ] , ξ = 1 σ M ln K ∑ n i = 1 Y i and τ = 1 σ m ln K ∑ n i = 1 Y i . UB n 1 and LB n 1 denote the respective option price of S u ( t ) and S l ( t ) .

The integral expressions for UB n 1 and LB n 1 are difficult to solve analytically and can be simplified using suitable approximations.


<!-- p:15 -->


PROPOSITION 10. The upper bound UB n 1 on the basket option price of, as defined in equation (66), can be bounded from above and below as follows:

UB n 1 ∈ ( LUB n 1 , UUB n 1 ) , where

$$U B _ { 1 } ^ { n } \in ( L U B _ { 1 } ^ { - } , U O B _ { 1 } ^ { - } ) , \text { where } \\ L U B _ { 1 } ^ { n } = n e ^ { - r T } \left [ \alpha e ^ { \frac { 1 } { 2 } \sigma _ { M } ^ { 2 } T } \Phi \left ( \eta \right ) - K \Phi \left ( - \frac { \xi } { \sqrt { T } } \right ) \right ] \\$$

and

$$U U B _ { 1 } ^ { n } = n \alpha e ^ { - r T } e ^ { \frac { 1 } { 2 } \sigma _ { M } ^ { 2 } T } \int _ { \xi } ^ { \infty } \phi \left ( \frac { y - \sigma _ { M } T } { \sqrt { T } } \right ) \Phi \left ( \frac { y } { \sqrt { T } } \right ) d y - \frac { n K e ^ { - r T } } { 2 } \left [ 1 - \Phi ^ { 2 } \left ( \frac { \xi } { \sqrt { T } } \right ) \right ] .$$

$$where , \sigma _ { M } & = \max _ { 1 \leq i \leq n } \sum _ { j = 1 } ^ { n } \sigma _ { i j } \text { as before, } \alpha \, = \, \sum _ { i = 1 } ^ { n } i _ { i } \omega _ { i } S _ { i } ( 0 ) \exp \left [ \left ( r - \frac { 1 } { 2 } \sigma _ { i } ^ { 2 } \right ) T \right ] , \, \xi \, = \, \frac { 1 } { \sigma _ { M } } \ln \left ( \frac { K } { \alpha } \right ) , \quad \, \hat { \otimes } \, , \\ \phi ( z ) & = \frac { 1 } { \sqrt { 2 \pi } } e ^ { - \frac { 1 } { 2 } z ^ { 2 } } \, \text { and } \eta = \frac { \xi - \sigma _ { M } T } { \sqrt { T } } .$$

Proof. The proof is available as online-only material and omitted from the text for brevity.

□

PROPOSITION 11. The lower bound LB n 1 on the basket option price of n assets, as defined in (67), can be bounded from above and below as follows:

LB n 1 ∈ ( LLB n 1 , ULB n 1 ) where

$$\text { and } \ U L B _ { 1 } ^ { n } = n e ^ { - r T } \left [ \alpha e ^ { \frac { 1 } { 2 } \sigma _ { m } ^ { 2 } T } \Phi \left ( \frac { \sigma _ { m } T - \zeta } { \sqrt { T } } \right ) - K \Phi \left ( - \frac { \zeta } { \sqrt { T } } \right ) \right ] , \\$$

$$L L B _ { 1 } ^ { n } & = n e ^ { - r T } \left ( \Phi \left ( - \frac { | \zeta | } { \sqrt { T } } \right ) \right ) ^ { n - 1 } \left [ \alpha e ^ { \frac { 1 } { 2 } \sigma _ { m } ^ { 2 } T } \Phi \left ( - \mu \right ) - K \Phi \left ( - \frac { \zeta } { \sqrt { T } } \right ) \right ] , \\ & \quad \ \ [ \tau _ { 1 } + \tau _ { 2 } ] ( \tau _ { 1 } - \tau _ { 2 } ) \zeta$$

where ζ m = 1 σ m ln ( K α ) , σ m = min 1 ≤ i ≤ n ∑ n j = 1 σ ij and μ = ζ - σ m T √ T . α and φ( z ) are as defined in proposition 10.

Proof. The proof is available as online-only material and omitted from the text for brevity.

□

In the discussion on control variates in subsequent sections, we will use a numerical approximation of UB n 1 and LB n 1 as control variates. Furthermore, the bounds derived and the analysis presented in this section are new and may have wider applications beyond the ones in this paper.

### 2.4. Control variates

The control variate approach is a method of variance reduction for Monte Carlo estimates. While this method is standard, we outline it here for completeness and to establish the notation which we will use. Consider a random variable Y which is a function h ( X ) whose distribution is not known, but the distribution of X is known. We can estimate the value of Y using a random variable Z = h ∗ ( X ) whose distribution is known using the random variable Ψ such that


<!-- p:16 -->


$$\Psi = Y - \lambda ( Z - \mathbb { E } ( Z ) ) ,$$

where the optimal value of the parameter λ which minimizes the variance of Ψ is given by

$$\lambda = \frac { C o v ( Y , Z ) } { V a r ( Z ) } .$$

This shows that Ψ is an estimator of Y . The algorithm (1) in the appendix shows the implementation of the control variate methodology.

For the purpose of this research we have used λ = 1 for the direct upper bound and geometric lower bound control variates, because their empirical values for λ are close to one, which was also observed by Dingeç &amp; Hörmann (2013).

### 3. Numerical implementation and findings

To conduct the numerical experiments for the control variate analysis, we estimated the sample covariance matrix using 522 observations of daily prices from 1 January 2018 to 31 December 2019, for five market indices namely FTSE 100, FTSE 250, S &amp; P 500, NIKKEI 225 and IMOEX (from Thomson Reuters Datastream), using log return of the prices. 1 The prices of two-asset and five-asset baskets were simulated using these covariance estimates. The control variates used for this experiment are the geometric lower bound of the basket option price, the modified geometric lower bound, the direct upper bound, the distributional upper and lower bound on the basket option price. For the distributional upper and lower bounds we use (69) and (70), respectively, as the closed-form estimates for the respective control variates. The modified geometric lower bound is simply using an option on the geometric lower bound on the final value of the basket with a modified strike ˆ K . This strike ˆ K is obtained by equating the expected differences of the final value of the basket from the strike K , and that of the geometric estimate of the basket's final value from the modified strike ˆ K as suggested by Gentle (1993). This relation can be simplified to obtain

$$\hat { K } = K + \mathbb { E } [ G ( 0 , T ) ] - F ( 0 , T ) , \\$$

where F ( 0, T ) = S ( 0 ) e rT and G ( 0, T ) is the geometric average of the final value of the basket. We will use the geometric lower bound as well as the modified geometric lower bound as benchmark control variates in our numerical experiments.

### 3.1. Control variate analysis of basket option price

In this section, we simulate the price of two- and five-asset basket option using 10 6 simulations, with initial value of the assets in the basket being S i ( 0 ) = 80 and weightings ω i = 1 n , for i = 1, 2, ... n . Also, the simulations are carried out for a variety of strikes K = 60, 80, 100 and for different maturities, T = 0.5, 1, 2. We assume a constant risk-free rate r of 1%. For the two-asset case, the simulation are carried out using only the volatility estimates from FTSE 100 and FTSE 250, while for the five-asset case we use volatility estimates from FTSE 100, FTSE 250, S &amp; P 500, NIKKEI 225 AND IMOEX. Table 2 shows the estimated prices of a two-asset basket option using first-order Hermite polynomial approximation and the corresponding error (E), which is given by

1 Data availability: the results described in this paper are fully reproducible based on the covariance matrix presented and do not need any external data. The data were used simply to produce a realistic enough covariance matrix.


<!-- p:17 -->


TABLE 1 Daily covariance estimates of market indices ( × 10 - 5 )

|            |   FTSE 100 |   FTSE 250 |   S&P 500 |   NIKKEI 225 |   IMOEX |
|------------|------------|------------|-----------|--------------|---------|
| FTSE 100   |       7.18 |       6.90 |      3.48 |         1.86 |    4.40 |
| FTSE 250   |       6.90 |       9.29 |      3.67 |         2.58 |    3.75 |
| S&P 500    |       3.48 |       3.67 |      8.60 |         7.00 |    3.89 |
| NIKKEI 225 |       1.86 |       2.58 |      7.00 |         9.57 |    1.57 |
| IMOEX      |       4.40 |       3.75 |      3.89 |         1.57 |   16.31 |

TABLE 2 Hermite polynomial approximation for a two-asset basket option

|   T |   K |   Price |   Error |
|-----|-----|---------|---------|
| 0.5 |  60 |  22.285 |   1.927 |
|     |  80 |   7.534 |   2.901 |
|     | 100 |   1.560 |   1.243 |
|   1 |  60 |  21.743 |   0.742 |
|     |  80 |   7.230 |   0.533 |
|     | 100 |  1.4681 |   0.209 |
|   2 |  60 |  20.685 |  -1.795 |
|     |  80 |   6.652 |  -2.954 |
|     | 100 |   1.298 |  -1.987 |

$$E = H P P r i c e - M C P r i c e , & & ( 7 5 ) & \stackrel { \frac { \overline { \Phi } } { \overline { n } } } { \stackrel { \stackrel { \circ } { \circ } } { \circ } } & \stackrel { ( 7 5 ) } { \stackrel { \stackrel { \circ } { \circ } } { \circ } } & \stackrel { ( 7 5 ) } { \stackrel { \stackrel { \circ } { \circ } } { \circ } }$$

where HPPrice is the first-order Hermite polynomial approximation of basket option price calculated in (15) and MCPrice is the standard Monte Carlo price of the basket option.

The results show a good approximation for the two-asset basket option price, when the strike price K of the basket is 60 and 80, but is significantly different when the basket is out-of-the money. This observation is consistent with findings in Milevsky &amp; Posner (1998): that lognormal models tend to over-value out-of-the-money call option prices.

For control variate analysis, we simulate Monte Carlo option price with control variates using 10 6 simulations, for the two-asset and five-asset basket, for different maturities and a variety of strikes 2 . We use a 95% confidence interval for our results and the general idea is that, for the same number of simulations, we can obtain tighter confidence intervals with faster times (given that standard Monte Carlo needs significantly more simulations to obtain better confidence intervals).

2 The implementation of these control variates is reproducible using the control variate algorithm and implementation chart given in the appendix.


<!-- p:18 -->


TABLE 3 Basket option prices for a two-asset basket, T = 0.5

|   K | Method   |   Price |   Variance |   CI Lower |   CI Upper |   Time |
|-----|----------|---------|------------|------------|------------|--------|
|  60 | MC       | 20.3633 |     1.0000 |    20.3415 |    20.3850 | 0.0567 |
|     | LB       | 20.3615 |     0.0001 |    20.3612 |    20.3617 | 0.2320 |
|     | MLB      | 20.3616 |     0.0001 |    20.3613 |    20.3618 | 0.1548 |
|     | UB       | 20.3618 |     0.0002 |    20.3614 |    20.3620 | 0.0733 |
|     | HP       | 20.3609 |     0.0225 |    20.3586 |    20.3631 | 0.0068 |
|     | UBM      | 20.3581 |     0.4601 |    20.3435 |    20.3626 | 0.4486 |
|     | LBM      | 20.3094 |     0.0596 |    20.3042 |    20.3147 | 0.0469 |
|  80 | MC       |  4.6431 |     1.0000 |     4.6285 |     4.6567 | 0.0152 |
|     | LB       |  4.6387 |     0.0001 |     4.6385 |     4.6389 | 0.2362 |
|     | MLB      |  4.6387 |     0.0002 |     4.6381 |     4.6396 | 0.1497 |
|     | UB       |  4.6392 |     0.0047 |     4.6382 |     4.6402 | 0.0769 |
|     | HP       |  4.6392 |     0.0285 |     4.6373 |     4.6409 | 0.0869 |
|     | UBM      |  4.6374 |     0.4327 |     4.6289 |     4.6403 | 0.2613 |
|     | LBM      |  4.6464 |     0.0784 |     4.6424 |     4.6504 | 0.0865 |
| 100 | MC       |  0.3122 |     1.0000 |     0.3085 |     0.3159 | 0.0541 |
|     | LB       |  0.3145 |     0.0004 |     0.3144 |     0.3146 | 0.2355 |
|     | MLB      |  0.3142 |     0.0007 |     0.3139 |     0.3149 | 0.1889 |
|     | UB       |  0.3147 |     0.0454 |     0.3139 |     0.3155 | 0.0782 |
|     | HP       |  0.3144 |     0.1912 |     0.3127 |     0.3161 | 0.0875 |
|     | UBM      |  0.3138 |     0.5194 |     0.3111 |     0.3154 | 0.2853 |
|     | LBM      |  0.3127 |     0.1781 |     0.3112 |     0.3142 | 0.0867 |

In Tables 3- 8, we compare the price, (normalized) variance and confidence intervals of our Monte Carlo estimates for a two- and five-asset basket option with those obtained using different control variates, for different maturities and strikes. The normalized variances are simply the estimated variances, normalized with respect to the Monte Carlo variance for a fixed maturity and strike. The Monte Carlo, first-order Hermite polynomial, geometric lower bound, modified geometric lower bound, direct upper bound, distributional upper bound and distributional lower bounds are abbreviated as MC, HP, LB, MLB, UB, UBM and LBM, respectively, in all of the tables. Furthermore, CI Lower and CI Upper are the respective lower and upper confidence intervals of our estimates. Our numerical experiments show that for the same number of simulations, we obtain significant variance reduction, and tighter confidence intervals compared with standard Monte Carlo results for both the two-asset and fiveasset case. In Tables 3- 5, we find that our control variates (with the exception of the UBM) for the two-asset basket option have over 80% variance reduction, but were on average outperformed by the reference control variate. In terms of computation times, we find that LBM and HP control variate outperforms other control variates, while the UBM recorded the slowest computation times. The results for the five-asset basket option are presented in Tables 6- 8. The results show significant variance reduction for all control variates, with the UB and LB having the highest variance reduction. The computation times are found to be largely similar for all the control variates besides the LBM.


<!-- p:19 -->


TABLE 4 Basket option prices for a two-asset basket, T = 1

|   K | Method   |   Price |   Variance |   CI Lower |   CI Upper |   Time |
|-----|----------|---------|------------|------------|------------|--------|
|  60 | MC       | 20.9871 |     1.0000 |    20.9569 |    21.0179 | 0.0335 |
|     | LB       | 20.9849 |     0.0002 |    20.9845 |    20.9853 | 0.2036 |
|     | MLB      | 20.9845 |     0.0002 |    20.9840 |    20.9852 | 0.1505 |
|     | UB       | 20.9844 |     0.0005 |    20.9837 |    20.9852 | 0.0341 |
|     | HP       | 20.9847 |     0.0194 |    20.9813 |    20.9881 | 0.0435 |
|     | UBM      | 20.9844 |     0.4363 |    20.9701 |    20.9997 | 0.2325 |
|     | LBM      | 20.9791 |     0.0607 |    20.9716 |    20.9865 | 0.0495 |
|  80 | MC       |  6.6758 |     1.0000 |     6.6549 |     6.6966 | 0.0501 |
|     | LB       |  6.6595 |     0.0003 |     6.6592 |     6.6599 | 0.2364 |
|     | MLB      |  6.6595 |     0.0003 |     6.6580 |     6.6612 | 0.1511 |
|     | UB       |  6.6599 |     0.0007 |     6.6585 |     6.6613 | 0.0751 |
|     | HP       |  6.6609 |     0.0185 |     6.6581 |     6.6637 | 0.0857 |
|     | UBM      |  6.6631 |     0.4791 |     6.6501 |     6.6771 | 0.2541 |
|     | LBM      |  6.6174 |     0.0771 |     6.6115 |     6.6233 | 0.0872 |
| 100 | MC       |  1.2449 |     1.0000 |     1.2356 |     1.2542 | 0.0500 |
|     | LB       |  1.2487 |     0.0006 |     1.2484 |     1.2489 | 0.2356 |
|     | MLB      |  1.2487 |     0.0007 |     1.2484 |     1.2497 | 0.1505 |
|     | UB       |  1.2483 |     0.0221 |     1.2469 |     1.2497 | 0.0771 |
|     | HP       |  1.2486 |     0.0361 |     1.2469 |     1.2500 | 0.0868 |
|     | UBM      |  1.2322 |     0.5101 |     1.2256 |     1.2338 | 0.2620 |
|     | LBM      |  1.2359 |     0.1186 |     1.2325 |     1.2391 | 0.0869 |

TABLE 5 Basket option prices for a two-asset basket, T = 2

|   K | Method   |   Price |   Variance |   CI Lower |   CI Upper |   Time |
|-----|----------|---------|------------|------------|------------|--------|
|  60 | MC       | 22.4924 |     1.0000 |    22.4509 |    22.5238 | 0.0545 |
|     | LB       | 22.4834 |     0.0004 |    20.4819 |    22.4845 | 0.2401 |
|     | MLB      | 22.4836 |     0.0004 |    20.4816 |    22.4850 | 0.1555 |
|     | UB       | 22.4832 |     0.0009 |    22.4819 |    22.4845 | 0.0810 |
|     | HP       | 22.4839 |     0.0311 |    22.4770 |    22.4883 | 0.0906 |
|     | UBM      | 22.2479 |     0.5278 |    22.2210 |    22.2747 | 0.3034 |
|     | LBM      | 22.2396 |     0.0645 |    22.2291 |    22.2502 | 0.0965 |
|  80 | MC       |  9.5914 |     1.0000 |     9.5601 |     9.6226 | 0.0574 |
|     | LB       |  9.6002 |     0.0006 |     9.5994 |     9.6009 | 0.2423 |
|     | MLB      |  9.6002 |     0.0009 |     9.5974 |     9.6003 | 0.1582 |
|     | UB       |  9.6019 |     0.0037 |     9.5596 |     9.6039 | 0.0814 |
|     | HP       |  9.5974 |     0.0421 |     9.5930 |     9.6017 | 0.0928 |
|     | UBM      |  9.4249 |     0.4424 |     9.4044 |     9.4374 | 0.1918 |
|     | LBM      |  9.4150 |     0.0777 |     9.4062 |     9.4238 | 0.0566 |
| 100 | MC       |  3.3437 |     1.0000 |     3.3242 |     3.3632 | 0.0375 |
|     | LB       |  3.3377 |     0.0008 |     3.3371 |     3.3383 | 0.2108 |
|     | MLB      |  3.3479 |     0.0011 |     3.3456 |     3.3493 | 0.1564 |
|     | UB       |  3.3467 |     0.0119 |     3.3445 |     3.3488 | 0.0396 |
|     | HP       |  3.3531 |     0.0718 |     3.3479 |     3.3583 | 0.0525 |
|     | UBM      |  3.3406 |     0.4914 |     3.3374 |     3.3563 | 0.2172 |
|     | LBM      |  3.2906 |     0.1152 |     3.2841 |     3.2971 | 0.0601 |


<!-- p:20 -->


TABLE 6 Basket option prices for a five-asset basket, T = 0.5

|   K | Method   |   Price |   Variance |   CI Lower |   CI Upper |   Time |
|-----|----------|---------|------------|------------|------------|--------|
|  60 | MC       | 20.3111 |     1.0000 |    20.2937 |    20.3285 | 0.1401 |
|     | LB       | 20.3107 |     0.0021 |    20.3099 |    20.3107 | 0.3675 |
|     | MLB      | 20.3108 |     0.0023 |    20.3101 |    20.3108 | 0.3674 |
|     | UB       | 20.3082 |     0.0035 |    20.3072 |    20.3092 | 0.2131 |
|     | HP       | 20.3109 |     0.3406 |    20.3007 |    20.3186 | 0.2016 |
|     | UBM      | 20.3027 |     0.5521 |    20.2897 |    20.3157 | 0.4189 |
|     | LBM      | 20.3107 |     0.2322 |    20.3024 |    20.3190 | 1.6879 |
|  80 | MC       |  3.7339 |     1.0000 |     3.7228 |     3.7451 | 0.1352 |
|     | LB       |  3.7341 |     0.0051 |     3.7334 |     3.7342 | 0.3754 |
|     | MLB      |  3.7340 |     0.0051 |    20.3097 |     3.7341 | 0.3672 |
|     | UB       |  3.7237 |     0.0635 |     3.7208 |     3.7265 | 0.2188 |
|     | HP       |  3.7371 |     0.3438 |     3.7284 |     3.7404 | 0.2018 |
|     | UBM      |  3.7371 |     0.5701 |     3.7297 |     3.7414 | 0.3795 |
|     | LBM      |  3.7371 |     0.2844 |     3.7312 |     3.7431 | 1.6751 |
| 100 | MC       |  0.0931 |     1.0000 |     0.0914 |     0.0948 | 0.1446 |
|     | LB       |  0.0941 |     0.0227 |     0.0939 |     0.0941 | 0.3624 |
|     | MLB      |  0.0940 |     0.0227 |     0.0938 |     0.0941 | 0.3625 |
|     | UB       |  0.0909 |     1.4135 |     0.0892 |     0.0917 | 0.2145 |
|     | HP       |  0.0945 |     0.3987 |     0.0929 |     0.0948 | 0.1972 |
|     | UBM      |  0.0945 |     0.6239 |     0.0931 |     0.0949 | 0.3864 |
|     | LBM      |  0.0946 |     0.3917 |     0.0934 |     0.0948 | 1.6667 |

TABLE 7 Basket option prices for five-asset basket, T = 1

|   K | Method   |   Price |   Variance |   CI Lower |   CI Upper |   Time |
|-----|----------|---------|------------|------------|------------|--------|
|  60 | MC       | 20.7163 |     1.0000 |    20.6920 |    20.7407 | 0.1546 |
|     | LB       | 20.7216 |     0.0047 |    20.7199 |    20.7216 | 0.3869 |
|     | MLB      | 20.7219 |     0.0047 |    20.7202 |    20.7219 | 0.3871 |
|     | UB       | 20.7114 |     0.0086 |    20.7096 |    20.7136 | 0.2363 |
|     | HP       | 20.7188 |     0.3712 |    20.7051 |    20.7291 | 0.2222 |
|     | UBM      | 20.7141 |     0.5647 |    20.7057 |    20.7221 | 0.4474 |
|     | LBM      | 20.7217 |     0.2357 |    20.7101 |    20.7291 | 1.7071 |
|  80 | MC       |  5.3851 |     1.0000 |     5.3688 |     5.4015 | 0.1434 |
|     | LB       |  5.3925 |     0.0103 |     5.3908 |     5.3925 | 0.3682 |
|     | MLB      |  5.3920 |     0.0104 |     5.3902 |     5.3921 | 0.3681 |
|     | UB       |  5.3764 |     0.0585 |     5.3724 |     5.3804 | 0.2163 |
|     | HP       |  5.3941 |     0.3191 |     5.3834 |     5.3991 | 0.2019 |
|     | UBM      |  5.3853 |     0.5441 |     5.3734 |     5.3911 | 0.3795 |
|     | LBM      |  5.3902 |     0.2764 |     5.3814 |     5.3963 | 1.7035 |
| 100 | MC       |  0.5749 |     1.0000 |     0.5694 |     0.5893 | 0.1673 |
|     | LB       |  0.5698 |     0.0309 |     0.5689 |     0.5699 | 0.3891 |
|     | MLB      |  0.5695 |     0.0306 |     0.5686 |     0.5696 | 0.3893 |
|     | UB       |  0.5612 |     0.5094 |     0.5572 |     0.5651 | 0.6194 |
|     | HP       |  0.5656 |     0.4133 |     0.5609 |     0.5704 | 0.2286 |
|     | UBM      |  0.5654 |     0.7069 |       5609 |     0.5698 | 0.6194 |
|     | LBM      |  0.5669 |     0.3771 |     0.5635 |     0.5701 | 1.7383 |


<!-- p:21 -->


TABLE 8 Basket option price for a five-asset basket, T = 2

|   K | Method   |   Price |   Variance |   CI Lower |   CI Upper |   Time |
|-----|----------|---------|------------|------------|------------|--------|
|  60 | MC       | 22.7791 |     1.0000 |    21.7453 |    21.8128 | 0.1579 |
|     | LB       | 21.7702 |     0.0103 |    21.7667 |    21.7702 | 0.3845 |
|     | MLB      | 21.7707 |     0.0103 |    21.7673 |    21.7708 | 0.3845 |
|     | UB       | 21.7462 |     0.0126 |    21.7424 |    21.7501 | 0.2341 |
|     | HP       | 21.7692 |     0.2846 |    21.7505 |    21.7723 | 0.2189 |
|     | UBM      | 21.7814 |     0.5704 |    21.7907 |    22.0133 | 0.2948 |
|     | LBM      | 21.7698 |     0.2427 |    21.7532 |    21.7764 | 1.7223 |
|  80 | MC       |  7.8575 |     1.0000 |     7.8320 |     7.8879 | 0.1574 |
|     | LB       |  7.8367 |     0.0212 |     7.8333 |     7.8367 | 0.3814 |
|     | MLB      |  7.8385 |     0.0215 |     7.8316 |     7.8351 | 0.3814 |
|     | UB       |  7.8232 |     0.0529 |     7.8177 |     7.8288 | 0.2303 |
|     | HP       |  7.8402 |     0.3803 |     7.8296 |     7.8504 | 0.2166 |
|     | UBM      |  7.8424 |     0.5132 |     7.8269 |     7.8593 | 0.3953 |
|     | LBM      |  7.8402 |     0.2925 |     7.8338 |     7.8596 | 1.7361 |
| 100 | MC       |  1.9530 |     1.0000 |     1.9659 |     1.9560 | 0.0129 |
|     | LB       |  1.9419 |     0.0428 |     1.9393 |     1.9419 | 0.3791 |
|     | MLB      |  1.9421 |     0.0429 |     1.9398 |     1.9422 | 0.3793 |
|     | UB       |  1.9294 |     0.3107 |     1.9231 |     1.9357 | 0.2309 |
|     | HP       |  1.9454 |     0.4719 |     1.9351 |     1.9508 | 0.2153 |
|     | UBM      |  1.9394 |     0.6037 |     1.9293 |     1.9421 | 0.4001 |
|     | LBM      |  1.9454 |     0.3255 |     1.9351 |     1.9511 | 1.7026 |

All the computations in this paper have been carried out using an Apple M1 Pro MacBook Pro 2021 with 16GB of unified memory and 8-core CPU (with six performance cores and two efficiency cores). The matlab version used is MatlabR2022a.

### 4. Conclusion

In this paper, we have proposed several new control variate for efficient simulation-based pricing of basket options. The first method is a lognormal approximation of the basket (or logarithm of the product of weighted assets in the basket) using first-order Hermite polynomials.

The second control variate is a direct upper bound on the payoff of the basket option obtained by a direct application of the Jensen's inequality.

The third and fourth control variates are the distributional upper and lower bounds, which involve obtaining bounds on the price of a basket option, whose randomness is driven by the maximum or minimum of independent Brownian motions.

Our numerical results show that all our control variates achieve significant variance reduction compared with standard Monte Carlo. Also, the variance reductions obtained from the use of the distributional lower bound and first-order Hermite polynomial approximation control variates are comparable with the benchmark control variates (geometric lower bound without and with modified strike), but have significantly faster computation times.

Since basket options are commonly used by financial institutions for cost-effective hedging of multiple underlying positions, new methods to price them efficiently and accurately is a useful contribution in risk management. Further, the lower distributional bound derived in this paper is believed to be new, as is the derivation of Hermite polynomial-based approximation. Both these approaches will have applications beyond basket option pricing and beyond GBM set-up. Adaptation of these control variates to the pricing of Asian options and basket options under stochastic volatility are topics of current research.


<!-- p:22 -->


### Acknowledgements

The authors thank the peer reviewers for their valuable feedback and contributions.

### Data availability

The data underlying this article will be shared on reasonable request to the corresponding author.

### A. Appendix

#### A.1. Control Variate Algorithm

##### Algorithm 1 Algorithm for control variates

1. Pick a large number N for number of simulations.
2. Set k = 1.
3. For each k, generate Y ( k ) and Z ( k ) and evaluate the mean of Z in closed-form.
4. Calculate Ψ ( k ) given in (72) such that

$$\Psi ^ { ( k ) } = Y ^ { ( k ) } - \lambda ( Z ^ { ( k ) } - \mathbb { E } ( Z ) ) ,$$

where λ is of the form given in (73).

5. Set k = k+1.
6. If k &lt; N , go to step 3. Else, compute

#### A.2. Algorithm Implementation Table

Table 9 gives pointers to computation of Z k and E ( Z ) in the algorithm above, for each control variate.

TABLE 9 Algorithm implementation chart for control variates

| Method   | Eqn for E ( Z )   | Z ( k )                                  |
|----------|-------------------|------------------------------------------|
| UB       | ( 32 )            | e - rT ∑ n i = 1 ω i ( S i ( T ) - K ) + |
| HP       | ( 15 )            | e - rT e Φ( u ) - K +                    |
| UBM      | ( 69 )            | ( ) e - rT  ̄ S u ( T ) - K +             |
| LBM      | ( 70 )            | ( ) e rT S l ( T ) K +                   |

$$\widehat { \Psi } = \frac { 1 } { N } \sum _ { k = 1 } ^ { N } \Psi ^ { ( k ) } .$$

(

 ̄

-

)
