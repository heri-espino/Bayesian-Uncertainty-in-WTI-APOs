---
id: "curran_1994_valuing-asian-and-portfolio-options"
source_pdf: "../pdf/curran_1994_valuing-asian-and-portfolio-options.pdf"
source_filename: "curran_1994_valuing-asian-and-portfolio-options.pdf"
format: "academic-paper"
extraction_profile: "token-efficient-high-fidelity"
extraction_mode: "hybrid"
extraction_quality: "excellent"
extraction_score: 98.0
formula_enrichment: "codeformulav2"
table_structure: "accurate"
tables_png: 2
figures_png: 0
assets_dir: "../assets/curran_1994_valuing-asian-and-portfolio-options"
---

<!-- p:1 -->

####### Valuing Asian and portfolio options by conditioning on the g Curran, Michael

Management Science; Dec 1994; 40, 12; Alumni - ABI/INFORM Global

pg. 1705

## Vl suo ng ne sns Vnn Conditioning on the Geometric Mean Price

Michael Curran

Salomon Bros., 7 World Trade Center, 40th Floor, New York, New York 10048

The valuation of Asian, or average price, options and of European options on portfolios in a "Black-Scholes" environment has given researchers trouble. The difficulty with these problems is that the probability distribution of the variable which determines the option payoff at expiration, a sum of correlated lognormal random variables, has no closed-form representation. For the Asian case the approach generally taken has been to approximate the distribution of the arithmetic average price, while for the portfolio option case, attempts have focused on discretizing the joint distribution of the terminal prices of the assets comprising the portfolio swep  s    d  -    he are not entirely satisfactory. The distribution-approximating procedures for Asian options are not very accurate for some cases, while the computational requirements for obtaining a reasonably accurate estimate using the discretizing or multinomial approaches for portfolio options become excessive as the number of assets rises above four or five, because the computation time is exponential in the number of assets. This paper presents a method based on conditioning on the geometric mean price which results in a far more efficient technique for valuing these options.

(Option Pricing; Conditioning; Exotic Options; Asian Options)

## 1. Introduction

The pricing of Asian, or average price, options and the -in, n s  oos tog rn oos c Scholes" environment has given researchers trouble. (The Asian call option payoff is the excess, if any, of the arithmetic average price experienced by the asset at evenly spaced points in time minus the strike price.) The difficulty with these problems is that the probability distribution of the variable which determines the option payoff at expiration, a sum of correlated lognormal random variables, has no closed-form representation. For the Asian case, an approximation of the distribution of the arithmetic mean price has been employed (see Ritchken et al. 1991, Turnbull and Wakeman 1991). In the literature covering the pricing of options on portfolios, the approach usually taken involves discretizing the risk-adjusted joint distribution of the prices of the assets in the portfolio (see Boyle et al. 1988, de Munnik 1990, and Rubinstein 1991). In this paper an alternative

0025-1909/94/4012/1705$01.25 Copyright © 1994, The Institute of Management Sciences approach is described. This method computes the expected option payoff conditional on the geometric mean of the relevant prices (we will use the phrase "relevant price" to refer to the asset prices at fixed points in time for the Asian case and terminal asset prices of the various assets in the portfolio case) and integrates with respect to the (known) distribution of the geometric mean price. That is, we utilize the fact that the price of an Asian option or a European call option on a portfolio can be expressed as

$$C = \exp ( - r T ) \tilde { E } \{ \tilde { E } [ \max ( A - K , 0 ) | G ] \} , \quad ( 1 )$$

where C is the price of the call option, r is the risk-free interest rate, T is the time to expiration,  denotes a riskadjusted expectation, A is the arithmetic mean of the relevant prices,

$$A = ( 1 / W ) \sum _ { i = 1 } ^ { n } w _ { i } S _ { i } ,$$


<!-- p:2 -->


K is the strike price, and G is the geometric mean price given by

$$G = \left \{ \prod _ { i = 1 } ^ { n } S _ { i } ^ { w _ { i } } \right \} ^ { 1 / W } ,$$

where, w &gt; 0 is the weighting of the ith relevant price, S; is the ith relevant price, n is the number of prices to be averaged, and

$$W = \sum _ { i = 1 } ^ { n } w _ { i } \, .$$

In the portfolio case we consider the weighted average asset value at expiration instead of the total portfolio value for notational convenience, with no loss of generality. Using benchmark values from Levy and Turnbull (1992) and Boyle et al. (1988) (hereafter LT and BEG), it is shown that this approach yields excellent estimates with a minimum of computation.

## 2. Computational Approach

### 2.1. Decomposing the Calculation

The expression for the price of the portfolio option given in (1) can be expanded to

$$C & = \exp ( - r T ) \left \{ \int _ { 0 } ^ { \kappa } \widetilde { E } | \max ( A - K , 0 ) | G | _ { g } ( G ) d G \\ & \quad + \int _ { K } ^ { \infty } \widetilde { E } | \max ( A - K , 0 ) | G | _ { g } ( G ) d G \right \} , \quad ( 2 ) \\$$

where &amp; is the density function of G. Let the terms inside the braces on the right-hand side of (2) be denoted by C1 and C2 so that

$$C = \exp ( - r T ) [ C _ { 1 } + C _ { 2 } ] .$$

For the more numerically demanding portfolio case (or when extreme accuracy is desired for the Asian case) a more refined approximation is derived. The general portfolio case is more difficult because the correlations among the relevant prices are arbitrary, while in the Asian case they are all positive and average about onehalf. In particular for the Asian case, the correlation between the price at time t and time s &gt; t is Vt /s (see Cryer 1986, p. 12). When the relevant prices have large correlations, A and G are generally closer than when the correlations are smaller. This reduces the contribution of C1 to C, thereby improving the overall accuracy.

### 2.2. Calculation of C2

If X, = ln[S ], then the risk-neutral terminal distribution of X is normal, consistent with the Black-Scholes assumptions. Let the mean of X, be denoted by μ and its variance by σ, where the μ and σ are determined by the nature of the option pricing problem. Now if we define X = ln(G), then

$$= \ln ( G ) , \, then \\ X & = \ln \{ \prod _ { i = 1 } ^ { n } S _ { i } ^ { w _ { i } } \} ^ { 1 / W } \\ & = ( 1 / W ) \sum _ { i = 1 } ^ { n } w _ { i } \ln ( S _ { i } ) \\ & = ( 1 / W ) \sum _ { i = 1 } ^ { n } w _ { i } X _ { i } .$$

$$i = 1$$

Therefore, X is also normally distributed with mean

$$\mu = ( 1 / W ) \sum _ { i = 1 } ^ { n } w _ { i } \mu _ { i } .$$

The variance of X is

Since, A ≥ G for all possible terminal asset values, the second term in the braces above is equal to

$$C _ { 2 } = \int _ { K } ^ { \infty } \left [ \tilde { E } [ A | G ] - K \right ] g ( G ) d G . \quad ( 3 ) \quad \text {where} \quad \begin{matrix} 3 \end{matrix} \quad \text {and} \quad$$

While C2 can be computed exactly, C1 is more difficult. Given that the geometric mean price is below the strike, , m , myy n m  m mo , Therefore, we must settle for an approximation of C1. For the Asian case a naive approximation which avoids the need for numerical integration is shown to suffice.

1706

$$\sigma ^ { 2 } = ( 1 / W ^ { 2 } ) \sum _ { i = 1 } ^ { n } \sum _ { j = 1 } ^ { n } w _ { i } w _ { j } \sigma _ { i } \sigma _ { j } \rho _ { i j } ,$$

where ρij is the correlation between returns of the ith and jth relevant price. The covariance of X and X is

$$\sigma _ { X i } = ( \sigma _ { i } / W ) \sum _ { j = 1 } ^ { n } w _ { j } \sigma _ { j } \rho _ { i j } .$$

Note that in the Asian case these summations collapse due to the special covariance structure. The expectation in (3) can be computed by noting that X and X; have

MANAGEMENT SCIENCE/ E/Vol. .. 40, No. 12, , December 1994


<!-- p:3 -->


a bivariate normal distribution for any i, since they are both linear combinations of the same set of normal random variables. Therefore (see Johnson and Wichern, p. 135–136), the conditional distribution of X, is

$$( X _ { i } \, | \, X = x ) \sim N \{ \, \mu _ { i } + ( \sigma _ { X i } / \sigma ^ { 2 } ) [ x - \mu ] , \, \sigma _ { i } ^ { 2 } - \sigma _ { X i } ^ { 2 } / \sigma ^ { 2 } \, \} \, .$$

As a result, the conditional distribution of S; is lognormal, and since the mean of a lognormal random variable with parameters β and γ2 is exp(β + γ2 /2),

$$with \text {parameters} \beta \text { and } \gamma ^ { ^ { * } } \text { is exp} ( \beta + \gamma ^ { ^ { * } } / 2 ) , \\ \tilde { E } [ A | G = e ^ { x } ] & = \tilde { E } [ A | X = x ] \\ & = \sum _ { i = 1 } ^ { n } \exp \{ \mu _ { i } + ( \sigma _ { x i } / \sigma ^ { 2 } ) [ x - \mu ] \\ & + ( \sigma _ { i } ^ { 2 } - \sigma _ { x i } ^ { 2 } / \sigma ^ { 2 } ) / 2 \} . \quad ( 4 ) \\ \text {We can now calculate the expectation in } ( 3 ) \colon$$

We can now calculate the expectation in (3):

$$C _ { 2 } = \int _ { \ln K } ^ { \infty } \left \{ \tilde { E } [ A | X = x ] - K \right \} f ( x ) d x ,$$

where f is a normal density with parameters μ and σ2, and we have made a change of variable using X = ln(G). From the definition of A,

$$= & \ln ( G ) . \text { From the definition of A ,} \\ & C _ { 2 } = \int _ { \ln \kappa } ^ { \infty } \left \{ \sum _ { i = 1 } ^ { n } \left ( 1 / W \right ) \tilde { E } [ w _ { i } S _ { i } | X = x ] - K \right \} f ( x ) d x \\ & = \left \{ ( 1 / W ) \int _ { \ln \kappa } ^ { \infty } \sum _ { i = 1 } ^ { n } w _ { i } \tilde { E } [ S _ { i } | X = x ] \right \} ( x ) d x \\ & \quad - \int _ { \ln \kappa } ^ { \infty } K f ( x ) d x \right \} . \\ & \text {We will treat the two terms on the right-hand side of}$$

We will treat the two terms on the right-hand side of the equation above separately. Let

$$C _ { 2 } \equiv \{ I _ { 1 } - I _ { 2 } \} .$$

The first integral is equal to

$$The first integral is equal to \\ I _ { 1 } = ( 1 / W ) \int _ { \ln K } ^ { \alpha } \sum _ { i = 1 } ^ { n } w _ { i } \tilde { E } [ S _ { i } | X = x ] f ( x ) d x \\ = ( 1 / W ) \sum _ { i = 1 } ^ { n } w _ { i } \int _ { \ln K } ^ { \alpha } \tilde { E } [ S _ { i } | X = x ] f ( x ) d x \\ = ( 1 / W ) \sum _ { i = 1 } ^ { n } w _ { i } \int _ { \ln K } ^ { \alpha } \exp \{ \mu _ { i } + ( \sigma _ { x i } / \sigma ^ { 2 } ) [ x - \mu ] \\ + ( \sigma _ { i } ^ { 2 } - \sigma _ { X i } ^ { 2 } / \sigma ^ { 2 } ) / 2 \} f ( x ) d x .$$

MANAGEMENT SCIENCE/Vol. 40, No. 12, December 1994

After factoring out constants, substituting z = (x − μ)/ σ, and integrating, we get

$$I _ { 1 } = ( 1 / W ) \sum _ { i = 1 } ^ { n } w _ { i } \exp ( \mu _ { i } + \sigma _ { i } ^ { 2 } / 2 ) \\ \times \Phi ( ( \mu - \ln K ) / \sigma + \sigma _ { X i } / \sigma ) ,$$

where Φ(·) is the standard normal distribution function. Using similar techniques we get

$$I _ { 2 } = K \Phi ( ( \mu - \ln K ) / \sigma ) .$$

This completes the derivation of C2.

### 2.3. Calculation of C1

In order to obtain an estimate of C1 we introduce some matrix notation. (Vectors will be underscored and matrices will be in bold.) First, let the (n + 1) × n matrix W be given by

$$W = \begin{bmatrix} \underline { I } \\ \underline { w ^ { T } } \end{bmatrix}$$

where I is an n × n identity matrix and

$$\underline { w } ^ { T } = ( w _ { 1 } / W , w _ { 2 } / W , w _ { 3 } / W \cdot \cdot \cdot w _ { n } / W ) .$$

Now if we let

$$\underline { X } ^ { T } = ( X _ { 1 } , X _ { 2 } , X _ { 3 } \cdots X _ { n } ) \quad \text {and} \\ \underline { X } _ { + } = \left [ \frac { X } { X } \right ] ,$$

then we can express X+ as

$$\underline { X } _ { + } = W \underline { X } _ { \cdot } .$$

If we denote the covariance matrix of X by C then C has elements Cij = σiσjρij. It follows that X+ has a covariance matrix given by

$$w ^ { T } C W = \left [ \begin{matrix} C & \overset { ! } { w } \\ \underline { w } ^ { T } C ^ { T } & \overset { ! } { w } ^ { T } C \underline { w } \end{matrix} \right ] .$$

Note that the ith element of the vector (Cω) is σxi and that w Cω = σ2. From a result in multivariate statistics

1707


<!-- p:4 -->


(see Johnson and Wichern 1982, p. 135–136), the distribution of X conditional upon X is multivariate normal with covariance matrix

$$\hat { C } = C - \frac { C _ { \underline { w } } w ^ { T } C ^ { T } } { \underline { w } ^ { T } C _ { \underline { w } } } \, .$$

(This is the conditional covariance matrix irrespective of the value of X.) Then the mean of A conditional on X = ln(K) (i.e., the geometric mean is equal to the strike price) is equal to

$$\hat { \mu } _ { A } = ( 1 / W ) \sum _ { i = 1 } ^ { n } w _ { i } \exp [ \hat { \mu } _ { i } + ( 1 / 2 ) \hat { C } _ { i i } ] ,$$

where the caret indicates that we are conditioning on uaX

$$\hat { \mu } _ { i } = \mu _ { i } + ( \sigma _ { X i } / \sigma ^ { 2 } ) [ \ln ( K ) - \mu ] .$$

We can now compute the conditional variance of A as

$$\hat { \sigma } _ { A } ^ { 2 } = ( 1 / W ^ { 2 } ) \ V a r \left \{ \sum _ { i = 1 } ^ { n } w _ { i } \, \exp ( X _ { i } | X = \ln ( K ) ) \right \} ,$$

where, again, the caret indicates that we are conditioning on the value of X. Expanding gives

$$where , \text { again, the caret indicates that we are condition-
ing on the value of X. Expanding gives} \\ \hat { \sigma } _ { A } ^ { 2 } = ( 1 / W ^ { 2 } ) \sum _ { i = 1 } ^ { n } \sum _ { j = 1 } ^ { n } w _ { i } w _ { j } \\ \times \text { Cov} ( \exp ( X _ { i } ) , \exp ( X _ { j } ) | X = \ln ( K ) ) \\ = ( 1 / W ^ { 2 } ) \sum _ { i = 1 } ^ { n } \sum _ { j = 1 } ^ { n } w _ { i } w _ { j } \{ \hat { E } [ \exp ( X _ { i } ) \exp ( X _ { j } ) ] \\ - \hat { E } [ \exp ( X _ { i } ) ] \hat { E } [ \exp ( X _ { j } ) ] \} \\ = ( 1 / W ^ { 2 } ) \sum _ { i = 1 } ^ { n } \sum _ { j = 1 } ^ { n } w _ { i } w _ { j } \{ \hat { E } [ \exp ( X _ { i } + X _ { j } ) ] \\ - \hat { E } [ \exp ( X _ { i } ) ] \hat { E } [ \exp ( X _ { j } ) ] \} . \\ \text {The random variables } \exp ( X _ { i } | X = \ln ( K ) ) , \, \exp ( X _ { j } | X } \\ = \ln ( K ) , \, \text {and} \exp ( X _ { i } + X _ { j } | X = \ln ( K ) ) \text { are all lognormal} .$$

The random variables exp(X|X = In(K)), exp(X,|X = In(K)), and exp(Xi + X,|X = ln(K)) are all lognormal. Therefore, the conditional variance of A is equal to

$$\text {Here, the conditional variance of A is equal to} \\ \hat { \sigma } _ { A } ^ { 2 } = ( 1 / W ^ { 2 } ) \sum _ { i = 1 } ^ { n } \sum _ { j = 1 } ^ { n } w _ { i } w _ { j } \\ \times \{ \exp [ \hat { \mu } _ { i } + \hat { \mu } _ { j } + ( 1 / 2 ) ( \hat { C } _ { i i } + \hat { C } _ { i j } + 2 \hat { C } _ { i j } ) ] & & \text {where} \\ - \exp [ \hat { \mu } _ { i } + ( 1 / 2 ) \hat { C } _ { i i } ] \exp [ \hat { \mu } _ { j } + ( 1 / 2 ) \hat { C } _ { j j } ] \} . & & \text {with} \\$$

1708

We approximate the distribution of ε ≡ (A − G|G) as lognormal with constant mean and variance, in order to use a Black-Scholes-like formula to estimate the value of the portfolio option conditional upon the geometric mean. Ritchken et al. (1991) give evidence indicating that the lognormal is a good approximation for the distribution of a (unconditional) sum of correlated (as in the Asian case) lognormal random variables. We will assume that the same is true of the sum of correlated lognormal random variables conditional on the geometric mean. Numerical results which follow support this assumption. We will also assume that the mean and variance of ε are constant and equal to their values for G = K. The rationale behind this assumption is that the majority of the contribution to the value of the portfolio option when the geometric mean price is below the strike will come from instances when the geometric mean price is close to the strike price. Therefore, the mean and variance of ε in these cases will be very nearly equal to their values when G = K (or, equivalently, X = In(K)). The mean and variance of a lognormal random variable with parameters β and γ2 are, respectively,

$$\exp ( \beta + \gamma ^ { 2 } / 2 ) \ \text { and } \ [ \exp ( \gamma ^ { 2 } ) - 1 ] \exp ( 2 \beta + \gamma ^ { 2 } ) .$$

Therefore, given our approximations of the mean and variance of ε, μ = βA − K and σ2 = ôλ, respectively, we can easily infer the values of β and γ under the lognormal assumption with

$$\gamma ^ { 2 } = \ln [ \hat { \sigma } _ { \epsilon } ^ { 2 } / \hat { \mu } _ { \epsilon } ^ { 2 } + 1 ] ,$$

and and

$$\beta = \ln ( \hat { \mu } _ { \epsilon } ) - \gamma ^ { 2 } / 2 .$$

Utilizing these parameters we employ a modified Black-Scholes formula to estimate the expected riskneutral payoff of the portfolio option conditional upon the geometric mean taking on a particular value less than the strike. We then get an estimate of C1 by imposing a mesh on the geometric mean and numerically integrating

$$C _ { 1 } ^ { \epsilon } = h \sum _ { i = 0 } ^ { m } B S ^ { \epsilon } ( i h ) g ( K - i h ) ,$$

where h is the interval width, g(·) is a lognormal density with parameters μ and σ2, and option values for 'strikes" greater than mh are assumed to be negligible.

MANAGEMENT SCIENCE/ E/Vol. 40, No. 12, December 1994


<!-- p:5 -->


Note that more sophisticated quadrature techniques may be used. The intent is to convey the essence of the computation. Here, BS'(k) is an estimate of the conditional value of the option

$$B S ^ { \epsilon } ( k ) & = \{ \exp ( \beta + \gamma ^ { 2 } / 2 ) & & \text {is the} & \text {and} \\ & \times N ( ( \beta - \ln k ) / \gamma + \gamma ) - k N ( ( \beta - \ln k ) / \gamma ) \} . & & \text {atity} &$$

We will refer to this approximation of C1 as the "sophisticated" approximation. A simpler, but less accurate, approximation of C, can be obtained by exchanging the expectation and the Maximum function in the integrand

$$C _ { 1 } \approx \int _ { 0 } ^ { K } \max \{ \tilde { E } ( A | G ) - K , 0 \} | _ { G } ( G ) d G .$$

Since Max(y, 0) is a convex function of y, Jensen's inequality implies that this approximation will be a lower bound on C1. We will refer to this approximation as the "naive" approximation.

## 3. Numerical Results

The method described in this paper was applied to Asian call options by using the naive approximation for the

Table 1 Call Option Values

|      |     | Call Option Values 20 Weeks Prior to Averaging Period n = 53, S0 = 100, r = 0.09/year ∆t = 1 week, d = 0, tn = 72 weeks   | Call Option Values 20 Weeks Prior to Averaging Period n = 53, S0 = 100, r = 0.09/year ∆t = 1 week, d = 0, tn = 72 weeks   | Call Option Values 20 Weeks Prior to Averaging Period n = 53, S0 = 100, r = 0.09/year ∆t = 1 week, d = 0, tn = 72 weeks   | Call Option Values at Averaging Period n = 53, S0 = 100, r = 0.09/year ∆t = 1 week, d = 0, tn = 1 year   | Call Option Values at Averaging Period n = 53, S0 = 100, r = 0.09/year ∆t = 1 week, d = 0, tn = 1 year   | Call Option Values at Averaging Period n = 53, S0 = 100, r = 0.09/year ∆t = 1 week, d = 0, tn = 1 year   | Call Option Values 20 Weeks into Averaging Period n = 53, S20 = 100, A20 = 100. r = 0.09/year ∆t = 1 week, d = 0, tn = 32 weeks   | Call Option Values 20 Weeks into Averaging Period n = 53, S20 = 100, A20 = 100. r = 0.09/year ∆t = 1 week, d = 0, tn = 32 weeks   | Call Option Values 20 Weeks into Averaging Period n = 53, S20 = 100, A20 = 100. r = 0.09/year ∆t = 1 week, d = 0, tn = 32 weeks   |
|------|-----|---------------------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------|
| σ    | K   | MC (Std Err)                                                                                                              | DA                                                                                                                        | GC                                                                                                                        | MC (Std Err)                                                                                             | DA                                                                                                       | GC                                                                                                       | MC (Std Err)                                                                                                                      | DA                                                                                                                                | GC                                                                                                                                |
|      | 95  | 11.76 (0.00)                                                                                                              | 11.76                                                                                                                     | 11.76                                                                                                                     | 8.81 (0.00)                                                                                              | 8.81                                                                                                     | 8.81                                                                                                     | 6.39 (0.00)                                                                                                                       | 6.39                                                                                                                              | 6.39                                                                                                                              |
| 0.05 | 100 | 7.39 (0.00)                                                                                                               | 7.39                                                                                                                      | 7.39                                                                                                                      | 4.31 (0.00)                                                                                              | 4.31                                                                                                     | 4.31                                                                                                     | 1.73 (0.00)                                                                                                                       | 1.73                                                                                                                              | 1.73                                                                                                                              |
|      | 105 | 3.48 (0.00)                                                                                                               | 3.47                                                                                                                      | 3.47                                                                                                                      | 0.95 (0.00)                                                                                              | 0.95                                                                                                     | 0.95                                                                                                     | 0.01 (0.00)                                                                                                                       | 0.01                                                                                                                              | 0.01                                                                                                                              |
|      | 95  | 11.96 (0.00)                                                                                                              | 11.96                                                                                                                     | 11.96                                                                                                                     | 8.91 (0.00)                                                                                              | 8.91                                                                                                     | 8.91                                                                                                     | 6.40 (0.00)                                                                                                                       | 6.40                                                                                                                              | 6.40                                                                                                                              |
| 0.10 | 100 | 8.07 (0.00)                                                                                                               | 8.07                                                                                                                      | 8.07                                                                                                                      | 4.91 (0.00)                                                                                              | 4.91                                                                                                     | 4.91                                                                                                     | 2.11 (0.00)                                                                                                                       | 2.10                                                                                                                              | 2.11                                                                                                                              |
|      | 105 | 4.87 (0.00)                                                                                                               | 4.87                                                                                                                      | 4.87                                                                                                                      | 2.06 (0.00)                                                                                              | 2.06                                                                                                     | 2.06                                                                                                     | 0.20 (0.00)                                                                                                                       | 0.20                                                                                                                              | 0.20                                                                                                                              |
|      | 90  | 19.17 (0.01)                                                                                                              | 19.16                                                                                                                     | 19.17                                                                                                                     | 14.96 (0.01)                                                                                             | 15.00                                                                                                    | 14.96                                                                                                    | 11.32 (0.01)                                                                                                                      | 11.32                                                                                                                             | 11.32                                                                                                                             |
| 0.30 | 100 | 13.42 (0.01)                                                                                                              | 13.43                                                                                                                     | 13.43                                                                                                                     | 8.81 (0.01)                                                                                              | 8.84                                                                                                     | 8.80                                                                                                     | 4.12 (0.01)                                                                                                                       | 4.12                                                                                                                              | 4.12                                                                                                                              |
|      | 110 | 9.06 (0.01)                                                                                                               | 9.06                                                                                                                      | 9.05                                                                                                                      | 4.68 (0.01)                                                                                              | 4.69                                                                                                     | 4.67                                                                                                     | 0.91 (0.01)                                                                                                                       | 0.93                                                                                                                              | 0.92                                                                                                                              |
|      | 90  | 24.17 (0.03)                                                                                                              | 24.02                                                                                                                     | 24.10                                                                                                                     | 18.14 (0.03)                                                                                             | 18.13                                                                                                    | 18.14                                                                                                    | 12.30 (0.02)                                                                                                                      | 12.29                                                                                                                             | 12.29                                                                                                                             |
| 0.50 | 100 | 19.38 (0.03)                                                                                                              | 19.35                                                                                                                     | 19.37                                                                                                                     | 12.98 (0.03)                                                                                             | 13.00                                                                                                    | 12.98                                                                                                    | 6.23 (0.02)                                                                                                                       | 6.24                                                                                                                              | 6.23                                                                                                                              |
|      | 110 | 15.44 (0.03)                                                                                                              | 15.49                                                                                                                     | 15.47                                                                                                                     | 9.10 (0.03)                                                                                              | 9.12                                                                                                     | 9.07                                                                                                     | 2.73 (0.02)                                                                                                                       | 2.79                                                                                                                              | 2.77                                                                                                                              |

Note: Estimates three standard errors or more from Monte Carlo estimate in bold.

MANAGEMENT SCIENCE/Vol. 40, No. 12, December 1994

value of C1. Table 1 demonstrates that even using this naive approximation gives excellent results for the Asian case. Here, n is the number of averaging points, S0 is the initial asset price, r is the riskless rate of interest, ∆t is the time between averaging points, d is the dividend yield, t is the final averaging point, and vol is the volatility of the asset. The columns labelled MC are the result of Monte Carlo simulations, and the columns labelled DA result from the most refined version of the class of Distribution Approximating models (due to Levy and Turnbull). These results have been copied from LT. The columns labelled GC (Geometric Conditioning) give the results of using the model presented in this paper. Observe that in almost all cases the GC column provides values that are most consistent with the results of the Monte Carlo simulations.

Table 2 gives the results of valuing one-year options on the three-asset portfolios estimated in BEG. In each case the risk-free rate of interest is 10%, the dividend yield on each asset is 0%, K = 100, and the assets are equally weighted with an initial value of 100. The volatilities are assumed to be equal, and all the pairwise correlations are fixed at 0.5. Since the BEG method discretizes the joint distribution of the assets, the result depends on the number of steps used in the discretization process. The results are displayed below where the more sophisticated approximation for C1, Ci has been used.


<!-- p:6 -->


Table 2

|              | Volatility     | Volatility    | Volatility    |
|--------------|----------------|---------------|---------------|
| No. of Steps | 2%0% BEG value | 25% BEG value | 30% BEG value |
| 20           | 12.060         | 13.405        | 14.815        |
| 40           | 12.072         | 13.411        | 14.816        |
| 60           | 12.076         | 13.413        | 14.816        |
| 80           | 12.078         | 13.413        | 14.816        |
| GC value     | 12.083         | 13.415        | 14.815        |

These results suggest that the GC method is extremely accurate. The computational complexity of this method results from the calculation of covariances. This computation is o(n2) with a small constant. Therefore, this method is fast for any practical number of assets.

## 4. Summary

We have presented a method of estimating the value of Asian options and European options on portfolios. A fast and relatively simple formula was given for valuing Asian options, which is more accurate than previous approaches. A more sophisticated approximation was presented which appears accurate for the more difficult portfolio option case. The method is much faster than previous multinomial methods that have been applied to this problem. The valuation of Asian and portfolio-put options can be obtained through putcall parity. The form of this relationship for Asian options is given in LT.

The computation of hedge parameters is similar to price estimation in that differentiating C2 is straightforward, but the contributions to the hedge parameters corresponding to C1 would need to be obtained numerically.

The approach detailed in this paper may be generalized in various ways. For large portfolios a parsimonious parametric specification of the covariance structure of asset returns, as is commonly used for multifactor models for portfolio selection, would be advisable. Using similar methods to those described it is fairly straightforward to price Asian options on portfolios. Such an option would address the hedging needs of a buyer or seller of several assets, where the purchases or sales occur periodically through time.

Options on spreads can also be priced using the method described in this paper. To see how this may be accomplished, consider the payoffs for calls and puts on spreads:

$$C \text { Call Payoff} & = \max [ 0 , ( S _ { l } - S _ { s } ) - K ] , \\ \text {Put Payoff} & = \max \{ 0 , K - ( S _ { l } - S _ { s } ) ] ,$$

where S, and S, are the prices of the assets held long and short. If K ≥ 0, then in the put payoff we can make S, the numeraire:

$$\text {Put Payoff} = S _ { i } \, \text {Max} [ 0 , K / S _ { i } + S _ { s } / S _ { i } - 1 ) ] .$$

Since the ratio of two lognormal random variables is lognormal, this payoff is in the same form as that of an option on a portfolio. Put-call parity can then be used to obtain the price of the call. If K &lt; 0, we begin with the call payoff and use S, as the numeraire.

The GC method can also be applied to pricing options on coupon bonds when forward interest rates follow Gaussian processes, because in this case discount bond prices are distributed lognormally. While Jamshidian (1989) has developed an efficient algorithm for onefactor Gaussian models, his approach cannot be applied to multifactor models, while the GC method can handle these cases.1

1 This research was completed while the author was a member of the Derivative Products and New Ventures group of Kidder, Peabody, &amp; Co., Inc.

####### References

Boyle, P. P., J. Evnine, and S. Gibbs, "Valuation of Options on Several Underlying Assets," Working Paper, University of Waterloo, Waterloo, Ontario, Canada, 1988.

Cryer, J. D., Time Series Analysis, Duxbury Press, Boston, MA, 1986. de Munnik, J., "Options on Several Assets: A Multinomial Approach,"

1710

MANAGEMENT SCIENCE/Vol. 40, No. 12, December 1994


<!-- p:7 -->


##### CURRAN

- He, H., "Convergence from Discrete to Continuous Time Financial Models," Working Paper No. 190, Haas School of Business, University of California at Berkeley, Berkeley, CA.
- Levy, Edmond and Stuart Turnbull, "Average Intelligence," Risk, (February 1992).
- Jamshidian, Farshid, "An Exact Bond Option Formula," J. Finance (1989).
- Johnson, R. A. and D. W. Wichern, Applied Multivariate Statistical Analysis, Prentice-Hall, Inc., NJ, 1982.
- Kemna, A. G. Z. and A. C. F. Vorst, "A Pricing Method for Options Based on Average Asset Values," J. Banking and Finance, 14 (1990).
- Ritchken, P., L. Sankarasubramanian, and A. M. Vijh, "The Valuation of Path Dependent Contracts on the Average," Working Paper, Weatherhead School of Management, Case Western Reserve University, Cleveland, OH, 1991.
- Rubinstein, Mark, "Exotic Options," Unpublished Manuscript, 1991.
- Turnbull, Stuart, and Lee Wakeman, "A Quick Algorithm for Pricing European Average Options,"J. Financial and Quantitative Analysis, 26, 3 (1991).

Accepted by Robert Heinkel; received September 1992.
