---
id: "kemna_1990_pricing-average-asset-value-options"
source_pdf: "../pdf/kemna_1990_pricing-average-asset-value-options.pdf"
source_filename: "kemna_1990_pricing-average-asset-value-options.pdf"
format: "academic-paper"
extraction_profile: "token-efficient-high-fidelity"
extraction_mode: "hybrid"
extraction_quality: "excellent"
extraction_score: 108.0
formula_enrichment: "codeformulav2"
table_structure: "accurate"
tables_png: 1
figures_png: 0
assets_dir: "../assets/kemna_1990_pricing-average-asset-value-options"
references_file: "../references/kemna_1990_pricing-average-asset-value-options.references.md"
---

<!-- p:1 -->

##### A PRICING METHOD FOR OPTIONS BASED ON AVERAGE ASSET VALUES

A.G.Z. KEMNA and A.C.F. VORST*

Erasmus University Rotterdam, 3000 DR Rotterdam, The Netherlands

Received May 1988, final version received January 1989

In this paper, we present a new strategy for pricing average value options, i.e. options whose payoff depends on the average price of the underlying asset over a fixed period leading up to the maturity date. Such options are of particular interest and importance for thinly-traded assets (e.g. crude oil), since price manipulation is inhibited, and both the investor and issuer enjoy a welcome degree of protection from the vagaries of the market. These options are often implicit in a bond contract, although they also appear in a straightforward form. Our results suggest that the price of an average-value option will always be lower than that of a standard European option. Óur pricing strategy involves Monte Carlo simulation with variance reduction elements and offers an enhanced pricing method to both arbitragers and hedgers, as well as to the issuers of such bonds.

### 1. Introduction

Since their introduction in the late seventies, commodity-linked bond contracts with an average-value settlement price have intrigued investors and bond issuers alike. These contracts entitle the investors to the average value of the underlying commodity over a certain time interval or the nominal value of the bond, which ever is higher. Hence the investors are offered a straightforward bond plus an option on the average value of the commodity, where the exercise price is equal to the nominal value of the bond.1 There is an instinctive awareness that such average-value options reduce the risk of price manipulation of the underlying asset at the maturity date.

*We gratefully acknowledge the helpful comments of two referees and of participants in seminars at Brussels, Jouy-en-Josas, Madrid and Rotterdam, where earlier versions of this paper were presented.

'Examples include:

(ii) Mexican Petrobonds (1977) featuring redemption at 25-day interval averages;

(i) Oranje Nassau (Netherlands) (May 1985) bonds in local currency backed by crude oil, where the settlement price was defined as the average Brent Blend oil price over the last year of the contract. The redeemer receives face value plus the difference between face value and settlement price – for which he forfeits 1% of the coupon rate;

(iii) Delaware Gold indexed bond, based on the average gold price over 10 trading days;

(v) BT Gold Notes Limited notes (1988) based on monthly averages.

(iv) Petrolewis oil indexed notes based on 3-month averages [see Budd (1983) for an overview of these contracts];

0378–4266/90/$3.50 ©1990, Elsevier Science Publishers B.V. (North-Holland)


<!-- p:2 -->


Actors in commodity-linked bond markets are also aware that averagevalue options (AV-options) enable the investor to share in the general prosperity of the firm in which he or she has invested, while the issuer of the bond is not confronted by an atypically high maturity-date value after weeks or months of low prices.

Average-value options not only appear as an implicit part of commodityns  s u  ur o ea n suo  u interest rate contracts.2

Our paper is specifically concerned with European AV-options on assets.3 We do not propose to consider the American options, since they can be redeemed as early as the start of the final period, and are therefore vulnerable to price manipulation at or near the effective exercise date. Bergman (1981) studied average-value options with an exercise price equal to zero, which over simplifies the pricing problem. In fact none of the options mentioned in footnotes 1 and 2 are American in character, i.e. they cannot be exercised before maturity. Neither do they have an exercise price equal to zero.

Section 2 of this paper presents a dynamic hedging strategy from which the value of the AV-option can be derived, using arbitrage arguments. We hereby explain why it is impossible to derive an explicit formula for an AVoption. In section 3, we present an exposition of some of the peculiar characteristics of an AV-option. We find, for example, that the price of an AV-option is always less (or equal to) the price of a standard European option. In section 4, we demonstrate that Monte Carlo simulation can be used to determine the price of an AV-option, and we show that an out-ofthe-money standard option can be expected to be significantly more expensive than an AV-option. In order to reduce the standard deviation's 95% confidence interval to one or two cents, a geometric average (GA) is deployed rather than an arithmetic average (AV) option. An analytical value for this GA-option is found, which then serves as a lower bound for the AVoption and as a control variable in the variance reduction technique which is applied to the Monte Carlo simulation. In appendices A and B, some formal mathematical proofs are given.

### 2. A valuation model for an average value option

We assume a perfect security market which is open continuously, offers a constant riskless interest rate r to all borrowers and lenders and in which no transaction costs and/or taxes are incurred. In this paper we further assume that the underlying asset on which the option is based is equal to a stock with price S(t). Our first equation expresses this S(t) in the usual stochastic differential manner:

2AB Svensk Exportkredit offered currency options (January 1988) based on daily-average Yen aoudt at t t t-t  aat r t r ds r tt on based on the average interest rate over a fixed time interval have been traded on the Paris market for some time.

3Other papers on options with special features are Fisher (1978), Margrabe (1978) and Stulz (1982).


<!-- p:3 -->


$$d S ( t ) = \alpha S ( t ) \, d t + \sigma S ( t ) \, d W ( t )$$

in which W(t) is a Wiener process and α and σ are constants.

For To≤t≤T we introduce the variable A(t) as:

$$A ( t ) = \frac { 1 } { T - T _ { 0 } } \, \int _ { \ r _ { 0 } } ^ { t } S ( \tau ) \, d \tau , \quad \text {where}$$

T is the maturity date and

[To, T] is the final time interval over which the average value of the stock is calculated.

Note that A(t) is an average only where t=T. For T0≤t&lt; T, A(t) is defined as the part of the final average up to time t, and is a monotonically increasing function of t.4 The payoff on the option can be expressed as max(A(T)- K, 0), where K is the exercise price of the AV-option.

We now see that where To≤t≤T, the price of the option Č will depend upon t, S(t) and A(t). Where t &lt; T0 the value of A(t) will not be relevant. In order to determine the value of the option at t=0, we first calculate the value of the option in the time interval [To, T] and use the value found for To to calculate the value in the interval [0, To]. Since in the time interval [0, To] the value of the option is determined by t and S(t) alone, the standard partial differential equation for the option price can be derived in ng   IIn (n ns n Ilng I) extension:

$$\tilde { C } _ { t } + \frac { 1 } { 2 } \sigma ^ { 2 } S ^ { 2 } \tilde { C } _ { s s } + r ( S \tilde { C } _ { s } - \tilde { C } ) = 0 ,$$

where Č, Č, are first order partial derivatives with respect to t and S and Čss a second order partial derivative with respect to S. The boundary conditions for a standard call option which expires at To (i.e., a 'non-averaged' option) can be expressed as:

4If our model was applied to American options, A(t) would have to be expressed as an average up to time t. In fact, we have ignored American options since their early exercise features make price manipulation possible at the start of the final period, the average would thus be a one day average.


<!-- p:4 -->


$$C ( S ( T _ { 0 } ) , T _ { o } ) = \max \left ( S ( T _ { 0 } ) - K , 0 \right )$$

$$C ( 0 , t ) = 0$$

$$C _ { s } ( \infty , t ) = 1 .$$

For an AV-option, however, the boundary condition at time To implies that the value of the option is equal to Č(S(To), To). We recall that before this value can be calculated, the AV-option has to be valued over the time interval [To, T], and that Č in that case depends on t, S(t) and A(t).

We need a partial differential equation for Č(S(t), A(t), t), To ≤t≤T, and our first step is to note that our eq. (2) yields the equation:

$$d A ( t ) & = \beta S ( t ) \, d t , \quad \text {where} \\ \beta \text { is } 1 / ( T - T _ { 0 } ) .$$

If Č(S(t), A(t), t) is the value of the option at time t ∈ [To, T], we are able to apply Ito's formula [see, Arnold (1974, pp. 90–91)], as follows:

$$\mathbf d \widetilde { C } ( t ) = ( \widetilde { C } _ { t } + \frac { 1 } { 2 } \sigma ^ { 2 } S ^ { 2 } \widetilde { C } _ { s s } + \alpha S \widetilde { C } _ { s } + \beta S \widetilde { C } _ { s } ) \, \mathbf d t + \sigma S \widetilde { C } _ { s } \mathbf d W ( t )$$

where Č is the first order partial derivative with respect to A.

Thus a continuously-adjusted portfolio consisting of Č, stocks which is partially financed by a loan (ČsS—Č), bears an identical instantaneous risk, i.e. σSČ,dW(t) to the AV-option, and costs an identical Č in initial payments. Arbitrage arguments imply that the expected instantaneous return on the portfolio and on the option must be identical. We can therefore derive the following partial differential equation for the option price:

$$\tilde { C } _ { \tau } + \frac { 1 } { 2 } \sigma ^ { 2 } S ^ { 2 } \tilde { C } _ { s s } + \beta S \tilde { C } _ { \lambda } + r ( S \tilde { C } _ { s } - \tilde { C } ) = 0 ,$$

which holds in the domain

$$D ^ { * } = \{ ( S , A , t ) | S \geqq 0 , \, A \geqq 0 , \, T _ { 0 } \leqq t \leqq T \} .$$

Eq. (9) is in fact eq. (3) into which the factor βSČ has been incorporated. As Cox, Ingersoll and Ross (1985) have pointed out, the value of Č at this juncture depends on the boundary conditions which apply in Č(S, A,t). The very nature of an AV-option contract means that we can write the following three conditions:

$$\tilde { C } ( S ( T ) , A ( T ) , T ) = \max \left ( A ( T ) - K , 0 \right )$$


<!-- p:5 -->


$$\tilde { C } ( 0 , A ( t ) , t ) = \max \left ( e ^ { - r ( T - t ) } ( A ( t ) - K ) , 0 \right ) \\$$

$$\tilde { C } _ { s } ( \infty , A ( t ) , t ) = \beta ( T - t ) e ^ { - r ( T - t ) } .$$

We note that if S(t)=0, eq. (1) tells us that S(τ) is also equal to zero for τ ∈[t, T] and A(T) is thus equal to A(t).

Because we have an extra partial derivative in the p.d.e. (namely: ČA), we are obliged to find an extra boundary condition. In order to do so, we employ the following argument:

where A(t) ≥ K, the final payoff on the option is certain to be positive.

At time t, this payoff can be expressed as:

$$( A ( t ) - K ) + \beta \int _ { t } ^ { T } S ( t ) \, d \tau .$$

It is easy to show that this payoff can also be obtained by using the self-financing duplicating portfolio strategy described below.

Assume that an investor commits (A(t)-K)e-r(T-o into riskless bonds in order to secure the return promised by the first part of eq. (14) i.e., (A(t)- K) at time T. If the investor is to be certain of accruing the return promised by the second part of eq. (14), he is obliged to transfer a certain portion of stock ( +        s   (     t) eiapses. Overall this strategy requires a sum equal to (A(t)— K)e-r(T-t) plus the portion of a stock which can be expressed as follows:

$$\sum _ { t } ^ { T } \beta e ^ { - r ( T - t ) } d \tau = & \frac { \beta } { r } ( 1 - e ^ { - r ( T - t ) } ) .$$

If the no arbitrage condition is applied, we find that the price of the option when A(t)≥K must be equal to:5

$$\tilde { C } ( S ( t ) , A ( t ) , t ) = ( A ( t ) - K ) e ^ { - r ( T - t ) } + \frac { \beta } { r } ( 1 - e ^ { - r ( T - t ) } ) S ( t ) .$$

Ilor is   se  o  r t t r st ta a s u eq. (9). The next step is thus the process of finding a solution for eq. (9) in the following domain:

Bergman (1981) arrived at a similar looking result in his 'general method for pricing pathdependent European options'. In that method, however, he only lets the exercise price (K) equal zero, which has the merit of simplifying the mathematics, but the demerit of compromising the usefulness of his pricing model, as explained in the introduction.


<!-- p:6 -->


$$D = \{ ( S , A , t ) \in D ^ { * } | A \leq K \} .$$

The boundary condition for A(t)=K can be directly derived from our eq. (16):

$$\tilde { C } ( S ( t ) , K , t ) = & \frac { \beta } { r } ( 1 - e ^ { - r ( \tau - t ) } ) S ( t ) .$$

If we now use the boundary conditions [expressed in eqs. (11), (12), (13) and (18)] to solve our eq. (9), we shall find the price of the AV-option in the final time period.

We can use Kolmogorov's backward equation6 to give the following expression for the value of the AV-option.

$$\tilde { C } ( S ( t ) , A ( t ) , t ) = e ^ { - r ( T - t ) } E ^ { S ( t ) , \, A ( t ) , t } \max \left \{ A ( T ) - K , 0 \right \}$$

A(t) and t. S(t) is now given by: where ES('*A(L)*f expresses the conditional expectation with respect to S(t),

$$d S ( t ) = r S ( t ) \, d t + \sigma S ( t ) \, d W ( t ) .$$

The value of Č which we have found in our eq. (19) could also have been arrived at using a hedging approach and the risk-neutrality argument described by Cox and Ross (1976). The combined process (S(t), A(t)) is not Gaussian in character, which implies that it is impossible to find an explicit formula for the value of Č in (19).7 This suggests that if we want to find a value for Č(S(t), A(t),t) where A(t)&lt; K, we are obliged to use numerical computations.

### 3. Special characteristics of the AV-options

Before presenting our numerical computations for the value of AV-options we would like to discuss some of their characteristics in more detail. A bond issuer might prefer AV-options to standard European options for several reasons. The most significant reason is probably the protection against price manipulation which an AV-option affords. This is of special importance where thinly-traded assets, like crude oil are concerned, since they are vulnerable to such manipulation when they are traded as standard European options.

6Kolmogorov's backward equation is explained for example in Friedman (1975) and Øksendahl (1985).

7See, for example, Arnold (1974) for a discussion on this point.


<!-- p:7 -->


The AV-options as included in a bond contract also enhances the ability of bondholders to share in the profits of a firm when those profits depend on the price level of an underlying asset. If, for example, a standard European call option is based on an asset which remains low in price during a large part of the final time period and rises significantly at maturity, the firm would not have been able to generate sufficient revenues to pay the high premium to the option holders.

Now that we have reached the conclusion that no explicit formula for the value of an AV-option can be found, and have decided to use numerical procedures, we need to express the time variable t in discrete periods. We may thus approximate A(T) in our eq. (2) as follows:

$$A ( T ) = \frac { 1 } { n + 1 } \sum _ { i = 0 } ^ { n } S ( T _ { i } )$$

where Ti= T0 +i(T— To)/n. If n is large enough this formula is a satisfactory approximation of (2). We can therefore substitute the expression for A(T) in o    l l  (l    (1on the value of an AV-option at time To:

$$\left \{ \cdot \quad ( 2 2 )$$

Remind that in this formula S(t) is given by (20). Our equation enables comparison of the value of an AV-option with that of a standard European option. The latter can be expressed in similar terms; viz.

$$\max \left ( \sum _ { i = 0 } ^ { n } \frac { S ( T ) } { n + 1 } - K , 0 \right ) \right \} .$$

where S(t) is again expressed in terms of our eq. (20). We can prove that (23) is an adequate formula for the value of an option by substituting the following expression (24) into (23).

$$\sum _ { i = 0 } ^ { n } \frac { S ( T ) } { n + 1 } = S ( T ) .$$

If we now compare eqs. (22) and (23), we can derive the following lemma:

Lemma 1. If r≥0, then


<!-- p:8 -->


$$E ^ { S ( T _ { 0 } ) , T _ { 0 } } \{ \max \left ( \sum _ { i = 0 } ^ { n } \frac { S ( T _ { i } ) } { n + 1 } - K , 0 \right ) \} \leq & E ^ { S ( T _ { 0 } ) , T _ { 0 } } \{ \max \left ( \sum _ { i = 0 } ^ { n } \frac { S ( T ) } { n + 1 } - K , 0 \right ) \} \\$$

and strict inequality holds if r&gt;0 or σ&gt;0.

Although we offer a formal proof of this lemma in appendix A, we would here like to show that it is intuitively plausible in order to shed light on the nature of an AV-option.

We    (t     tt t t t ter than the expectation of S(T)/(n+ 1). One might argue, using the hedging argument that expected changes in the value of the stock are not relevant, that is until one realizes that in this case we are obliged to compare two expectations at different points in time.

The (  a  a t  e   s t(l( is less than the variance of S(T)/(n+ 1). We finally note that although the values of S(T)/(n + 1) for different points in time are correlated, they do not correlate as perfectly as the S(T)/(n+ 1). It is clearly the case that a higher degree of correlation results in a higher total variance and thus in a higher total value of the option.

Ww t  t(   t       s wer variance and less perfect correlation of the S(T) for i= 1,...,n are characteristics which combine to ensure that the price of an AV-option is always lower than a comparable standard European option.

Although we have only established that our eq. (25) holds for discrete processes, it can, in fact, describe a continuous process if we let n go to infinity. We can thus infer that at t= To, an AV-option has a lower value than a comparable European option, and it therefore follows that the value of the AV-option is also lower during the time interval [0, T0]. It is the case h a n n a     s u Gn evaluated in terms of our eq. (3), and their respective values where 0≤t≤ To can thus be expressed as follows, using Kolmogorov's backward equation:

$$\tilde { C } ( S , t ) = e ^ { - r ( T _ { o } - t ) } E ^ { S ( t ) , t } \tilde { C } ( S ( T _ { o } ) , 0 , T _ { o } )$$

$$C ( S , t ) = e ^ { - r ( T _ { o } - t ) } E ^ { S ( t ) , t } C ( S ( T _ { 0 } ) , T _ { 0 } ) .$$

Since Č(S(To), O, T0)≤C(S(To), T0) as our Lemma 1 claims, it follows that Č(S,t)≤C(S,t), i.e. that the value of a European call option will always be greater than, or equal to, the value of an AV-option.


<!-- p:9 -->


### 4. Numerical computations

Our eq. (9) has three variables, which implies that its solution cannot readily be found using a finite difference approach. We therefore propose to use a Monte Carlo simulation approach in finding a value for Č, which we intend to calculate at the inception of the final time interval. This point in time is chosen for expositional convenience, but does not effect the validity of the end results as we later explain.

For the Monte Carlo simulation we use eq. (22) where log(S(Ti)/S(T-1)) is normally distributed with mean (r-σ2)(T- To)/n and variance σ2(T-To)/n. The random sequence S(T1),...,S(T) can be generated as follows:

$$\log S ( T _ { i } ) = \log S ( T _ { i - 1 } ) + ( r - \frac { 1 } { 2 } \sigma ^ { 2 } ) \left ( T - T _ { 0 } \right ) / n + \sigma \sqrt { ( T - T _ { 0 } ) / n x _ { i } } \quad ( 2 8 )$$

where x1,...,x is a sequence of independent drawings from the standard normal distribution. Our Monte Carlo simulation relies on a total of 10,000 series, and for each series the value of a single realization Y(T) was calculated as:

$$Y ( T ) = e ^ { - \kappa T - T _ { 0 } } \max \left \{ A ( T ) - K , 0 \right \} .$$

Since Č represents the expected value of Y(T), the Monte Carlo estimate of the value of Č is equal to the average value found for (29) in the 10,000 simulation series.

To compare the AV-option with the standard European option we used a range of values for the interest rate r, the volatility σ, the exercise price K and the stock price S(To) as given in Cox and Rubinstein (1985, p. 216). We let n+1 =88 since we chose the time to maturity equal to four months and there are approximately 88 trading days in such a period.

Table 1 sets out our results. The left-hand column 'C' is for standard European option results, while column Č' shows the values of an AV-option with the respective standard deviations in brackets. The table shows that thue      sue  ue  ues t s eean option, especially where out-of-the-money options are concerned. Column Č' also shows that the standard deviations remain large in spite of our 10,000 simulation series, and are especially large in the case of out-of-the-money options. In fact, for all options at an exercise price of 35, the 95% confidence t s  st t st  t  s  s   ets s tte standard deviation of a Monte Carlo estimate apparently widens not only when the volatility of the stock is more pronounced, but also where the gap between the stock price and the exercise price increases.

It is clearly desirable to shrink the 95% confidence interval to some 1 or 2 cents, but this would imply a tremendous increase in the number of simulations series (approx. one million) and make the method unsuitable for on-line use. We therefore propose to employ a variance reduction technique which can reduce the Monte Carlo simulations' confidence intervals to satisfactory proportions.8 In order to apply such a technique, we are


<!-- p:10 -->


Table 1 Monte Carlo simulation results.

| IJ      | K       | C'        | P                     | c red. varsE         |
|---------|---------|-----------|-----------------------|----------------------|
| r= 1.03 | r= 1.03 | r= 1.03   | r= 1.03               | r= 1.03              |
|         | 35      | 5.564171  | 5.13204 1 (0.02592S)  | 5.162534 (0.000395)  |
| 0.2     | 40      | 2.035335  | 1.130741 (0.016595)   | 1.156578 (O.OQO393)  |
|         | 45      | 0.458753  | O.OS6056 (0.~3671)    | 0.055610 (0.~305)    |
|         | 35      | 6.079410  | 5.293287 (0.037757)   | 5.280812 (O.OfWI7)   |
| 0.3     | 40      | 2.947493  | 1.725343 (0.025949)   | 1.686469 (0.000968)  |
|         | 45      | 1.185225  | 0.282336 (0.010629)   | 0.283505 (0.000833)  |
|         | 35      | 6.739822  | 5481946 (0.048061)    | 5.513017 (0.001621)  |
| 0.4     | 40      | 3.858478  | 2.167185 (0.033897)   | 2.208228 (0.0016541  |
|         | 45      | 2.02 1782 | 0.651712 (0.019268)   | 0.641400 (0.001654j  |
| r= 1.05 | r= 1.05 | r= 1.05   | r= 1.05               | r= 1.05              |
|         | 3s      | 5.760638  | 5.242711 (0.026092)   | 5.254582 (0.000407)  |
| 0.2     | 40      | 2.167464  | 1.255169 (0.017604)   | 1.222033 (0.000448)  |
|         | 45      | 0.506410  | 0.056861(0.003620j    | 0.061814 (0.000311)  |
|         |         | 6.251320  | 5.450449 (0.038 1 SO) | 5.365896 (0.000922)  |
| 0.3     | 2       | 3.072905  | 1.740240 (0.025701)   | 1.743938 (0.0@0955)  |
|         | 45      | 1.254903  | 0.301295 (0.011014)   | 0.302174 (0.~14)     |
|         | 3.5     | 6.894444  | 5.519462 (0.048166)   | 5.590104 (0.001646)  |
| 0.4     | 40      | 3.979016  | 2.223067 (0.0347$4)   | 2.266583 (0.001762)  |
|         | 45      | 2.102843  | 0.619928 (0.018468)   | 0.662447 (0.001624)  |
| r= 1.07 | r= 1.07 | r= 1.07   | r= 1.07               | r= 1.07              |
|         | 3s      | 5.954377  | 5.362746 (0.025763)   | 5.344459 (0.~396)    |
| 0.2     | 40      | 2.301672  | 1.248346 (0.017388~   | 1.284268 (0.~ 1)     |
|         | 45      | 0.556796  | 0.067794 (0.003822j   | 0.069112 (0.000321)  |
|         | 3s      | 6.421252  | 5.373735 (0.037328)   | 5.446790 (O.OQO905)  |
| 0.3     | 40      | 3.198780  | 1.768012 (0.025760)   | 1.802526 (0.000969)  |
|         | 4s      | 1.326070  | 0.336724 (0.011952)   | 0.3 19448 (0.000924) |
|         | 35      | 7.047242  | 5.66473 1 (0.048268)  | 5.665121 (0.001671)  |
| 0.4     | 40      | 4.099354  | 2.273241 (0.034954)   | 2.321506 (0.001768)  |
|         | 4s      | 2.184482  | 0.655245 (0.019~1~    | 0.486804 (0.~1610)   |

sSee Boyle (1977) for the use of such a technique in calculating the prices of European call options on dividend paying stocks. See also Hammersley and Handscomb (1964) for an excellent exposition of the variance reduction technique.


<!-- p:11 -->


( o   (  i    n and is a sound approximating expression for Y(T) and amenable to an analytic expression of the expectation EW(T).

Provided that W(T) is a satisfactory approximation of Y(T), we shall thus have reduced the standard deviation considerably.

We chose our random variable as:

$$W ( T ) = e ^ { - r ( T - T _ { \circ } ) } \max \left \{ G ( T ) - K , 0 \right \} , \quad \text {where}$$

$$G ( T ) = \left ( \prod _ { i = 0 } ^ { \mathfrak { N } } S ( T _ { i } ) \right ) ^ { 1 / ( n + 1 ) }$$

We have thus proceeded to substitute a geometric average G(T) for the arithmetic average A(T). Since a geometric average is always lower than an arithmetic average [Beckenbach and Bellman (1971, p. 4)], W(T) provides a lower bound for Y(T).

In the continuous case eq. (31) can be written as:

$$G ( T ) = \exp \left ( \beta \int _ { T _ { 0 } } ^ { T } \log ( S ( \tau ) ) d \tau$$

In both continuous and discrete cases, the variable G(T) is lognormally distributed so that its expectation and variance values may be calculated expr   o   (    p  dsult is:

$$\log ( G ( T ) ) = n ( \frac { 1 } { 2 } ( r - \frac { 1 } { 2 } \sigma ^ { 2 } ) \left ( T - T _ { 0 } \right ) + \log ( S ( T _ { 0 } ) ) ; \, \frac { 1 } { 3 } \sigma ^ { 2 } ( T - T _ { 0 } ) \right )$$

where n(a; b) represents a normal distribution with mean a and variance b. Having established this we can proceed to evaluate the geometric average option (GA-option) value as follows [see Jarrow and Rudd (1983, pp. 92-95)]:

$$E \max \left \{ G ( T ) - K , 0 \right \} & = E \{ G ( T ) | G ( T ) \geqq K \} - K \, . \, \text {prob} \left \{ G ( T ) \geqq K \right \} \\ & = e ^ { d } S ( T _ { 0 } ) N ( d ) - K N ( d - \sigma \sqrt { \frac { 1 } { 3 } ( T - T _ { 0 } ) } ) ,$$

where N is the cumulative standard normal distribution function and d* and d can be written as:

$$d ^ { * } = \frac { 1 } { 2 } ( r - \frac { 1 } { 6 } \sigma ^ { 2 } ) \left ( T - T _ { 0 } \right )$$


<!-- p:12 -->


$$d = \frac { \log ( S ( T _ { 0 } ) / K ) + \frac { 1 } { 2 } ( r + \frac { 1 } { 6 } \sigma ^ { 2 } ) \left ( T - T _ { 0 } \right ) } { \sigma \sqrt { \frac { 1 } { 3 } ( T - T _ { 0 } ) } } .$$

We have thus arrived at an analytic expression for EW(T) which satisfies our requirements, and we can proceed to find a new Monte Carlo estimate of the AV-option price by adding EW(T) to our Monte Carlo estimate of the value of E(Y(T) − W(T)).

Table 1 records the results of this process in the column marked Č red. var.'. We again used 10,000 series, and found the standard deviations shown in brackets. In all cases the standard deviation has been reduced by at least %act  n  s nr s  satr ar  nr  5s confidence interval has shrunk to about 0.85 cents at the most. The 'Č red. var.' column in table 1 also shows that the size of the difference between the stock price and the exercise price has no effect on the standard deviation. In fact, the standard deviation only grows significantly larger when the volatility of the stock price increases. This effect is to be expected, since an increase in uncertainty about stock prices would tend to undermine the pu i ro  pe  pri   osr strategy of incorporating a geometric average has thus proved extremely successful in reducing the variance which marred our original (arithmetic average) Monte Carlo simulation estimates of the price of an AV-option.

In the interests of clarity, all of our Monte Carlo simulations took a time t which is exactly equal to the inception date of the final time interval [To, T]. The procedure described above would nevertheless readily lend itself to simulations where t &lt; T0 if we first simulate a value for S(To). Where t&gt; To, the factor A(t) has to be taken into account, so that our variance reduction technique can only be applied after modification of our eqs. (33) through (36). The necessary modification, which is quite straightforward, can be found in appendix B.

### 5. Conclusions

Our attempts to find a method for pricing averaged value options have produced some interesting results. We have shown that the use of an arithmetic average for the value of an underlying asset of such an option cannot result in an analytic expression for the value of an option before and during the final time interval. However, we were able to prove that the value ol     s n    s n d n s od European option. We have shown that the use of a geometric average in our calculations enables us to find an analytic expression for the value both in the final time interval, and over the total time period from issue date to maturity.


<!-- p:13 -->


We calculated the price of an average-value option based on an arithmetic average by Monte Carlo simulation techniques. Our first set of simulations proved that the AV-option value is considerably lower than the value of a similar standard European call option. The standard deviation results, however, were rather disconcertingly extreme, with a 95% confidence interval of some 10 to 20 cents.

We therefore applied a variance reduction technique to the Monte Carlo approach whereby a geometric average was used instead of the previously used arithmetic average. This improved the standard deviation results to provide a 95% confidence interval of some 90 cents.

Iu-    cd      c ded assets like oil, or on interest rates or currencies we anticipate that this pricing method will make a significant contribution.

## Appendix A

Proof of Lemma 1. If we define Ri=S(Ti)/S(Ti-1) and R0 = S(To), it is clear that S(Ti)= R0R1,..., R. From eq. (20) it follows that each R, is lognormally distributed with:

$$E ( R _ { i } , \dots , R _ { j } ) = \exp \left \{ r ( T - T _ { 0 } ) \left ( j - i + 1 \right ) / n \right \} \geq 1 .$$

Hence, we have to prove that:

$$E \max \left \{ \frac { R _ { 0 } + R _ { 0 } R _ { 1 } + \cdots + R _ { 0 } R _ { 1 } , \dots , R _ { n } } { n + 1 } - K , 0 \right \} \\ \leq E \max \left \{ R _ { 0 } R _ { 1 } , \dots , R _ { n } - K , 0 \right \} .$$

We will use the following:

Lemma 2. If U is a random variable with EU≥1 then for every m∈N and K&gt;0 we have

$$E \max \left ( \frac { 1 } { m } + \frac { m - 1 } { m } \, U - K , 0 \right ) \leq E \max \left ( U - K , 0 \right ) .$$

We will first demonstrate how (A.2) follows from this lemma. It is enough to show that


<!-- p:14 -->


$$E \max \left \{ \frac { 1 } { n + 1 } + \frac { n } { n + 1 } \, \frac { R _ { 1 } + \cdots + R _ { 1 } , \dots , R _ { n } } { n } - K ^ { \prime } , 0 \right \}$$

$$\leqq E \max \left \{ R _ { 1 } , \dots , R _ { n } - K ^ { \prime } , 0 \right \}$$

for each R0 with K'= K/Ro.

$$& + \frac { n } { n + 1 } \, \frac { R _ { 1 } + \cdots + R _ { 1 } , \dots , R _ { n } } { n } - K ^ { \prime , 0 } \} \\ & \{ R _ { 1 } , \dots , R _ { n } - K ^ { \prime } , 0 \}$$

Since (E(R++ R1,..,R)/n)≥1 by virtue of (A.1) we can apply Lemma 2 and hence

$$E \max \left \{ \frac { 1 } { n + 1 } + \frac { n } { n + 1 } \frac { R _ { 1 } + \cdots + R _ { 1 } , \dots , R _ { n } } { n } - K ^ { \prime } , 0 \right \} \\ \leq E \max \left \{ \frac { R _ { 1 } + \cdots + R _ { 1 } , \dots , R _ { n } } { n } - K ^ { \prime } , 0 \right \} \leq E \max \{ R _ { 1 } , \dots , R _ { n } - K ^ { \prime } , 0 \}$$

$$( A . 5 )$$

where the last inequality follows from induction on the number of random variables. (The induction can be started at n =0 in which (A.2) is a triviality.)

Proof of Lemma 2. Let p(U) be the density function of U≥0.

$$\frac { 1 } { m } + \frac { m - 1 } { m } \, U - K \geqslant 0 \text { if } U \geqslant K _ { 0 } = \frac { m K - 1 } { m - 1 } \, .$$

We distinguish two cases, namely K0≥1 and K0&lt; 1.

If K0≥1 then

$$E \max ( U - K , 0 ) = \sum _ { \kappa } ^ { \infty } \left ( U - K \right ) p ( U ) \, d U \geq \sum _ { \kappa _ { 0 } } ^ { \infty } \left ( U - K \right ) p ( U ) \, d U$$

$$\geq & \, \stackrel { \infty } { \int } \left ( \frac { 1 } { m } + \frac { m - 1 } { m } \ U - K \right ) p ( U ) \, \mathrm d U = E \max \left ( \frac { 1 } { m } + \frac { m - 1 } { m } \ U - K , 0 \right ) . \, ( A . 6 )$$

If K0 &lt; 1 then

$$E \max ( U - K , 0 ) = \sum _ { K } ^ { \infty } \left ( U - K \right ) p ( U ) \, d U \geq \sum _ { K _ { 0 } } ^ { \infty } \left ( U - K \right ) p ( U ) \, d U$$


<!-- p:15 -->


$$A . G . Z . \, K e m n a n d \, A . C . F . \, V o r s , \, P r i c i n g \, m e t h o d i t i o n s & & 1 2 7 \\ = E ( U - K ) - \int _ { 0 } ^ { K _ { 0 } } ( U - K ) p ( U ) \, d U \geqslant E \left ( \frac { 1 } { m } + \frac { m - 1 } { m } \ U - K \right ) \\ & \\ & - \int _ { K _ { 0 } } ^ { \infty } ( U - K ) p ( U ) \, d U \\ & \\ \geqslant E \left ( \frac { 1 } { m } + \frac { m - 1 } { M } \ U - K ) - \int _ { 0 } ^ { K _ { 0 } } \left ( \frac { 1 } { m } + \frac { m - 1 } { m } \ U - K \right ) p ( U ) \, d U \\ & \\ = E \max \left ( \frac { 1 } { m } + \frac { m - 1 } { m } \ U - K , 0 \right ) & & ( A . 7 ) \\ \intertext { w h e r e } \text {where the last inequarity follows because } U \leqslant K _ { 0 } \leqslant 1 .$$

where the last inequality follows because U≤K0≤1.

This completes the proof of Lemma 2. It is clear that if r&gt;0 or σ&gt;0 at least one of the above inequalities is a strict inequality which in fact establishes the second part of Lemma 1.

## Appendix B

In this appendix, we show that log {G(T)/G(To)}, with G(T) given by eq. (32), is normally distributed and we prove formulas (33)–(36). We will use the following notation:

$$V ( t ) = \log S ( t ) \quad \text {and} \quad Z ( t ) = \log G ( t ) .$$

Frrll   ss  (  (  ll s tol  n system of stochastic differential equations

$$d \begin{pmatrix} V ( t ) \\ Z ( t ) \end{pmatrix} = \left [ \begin{pmatrix} 0 & 0 \\ \beta & 0 \end{pmatrix} \begin{pmatrix} V ( t ) \\ Z ( t ) \end{pmatrix} + \begin{pmatrix} r - \frac { 1 } { 2 } \sigma ^ { 2 } \\ 0 \end{pmatrix} \right ] d t + \left [ \begin{pmatrix} \sigma \\ 0 \end{pmatrix} \right ] d W ( t ) .$$

Since, to use Arnold's terminology (1974, sec. 2), (B.2) is a linear stochastic differential equation in the narrow sense, we see that (V(t)Z(t))' must be a Gaussian process. This means that (V(t)Z(t))' is binormally distributed. Hence, log {G(T)/G(To)} is normally distributed. Furthermore, it follows from the same reference that

$$d \begin{pmatrix} E V ( t ) \\ E Z ( t ) \end{pmatrix} = \left [ \begin{pmatrix} 0 & 0 \\ 0 & 0 \end{pmatrix} \begin{pmatrix} E V ( t ) \\ E Z ( t ) \end{pmatrix} + \begin{pmatrix} r - \frac { 1 } { 2 } \sigma ^ { 2 } \\ 0 \end{pmatrix} \right ] d t .$$


<!-- p:16 -->


The covariance matrix of (V(t)Z(t))' as defined by

$$K ( t ) = \begin{pmatrix} K _ { 1 1 } ( t ) & K _ { 1 2 } ( t ) \\ K _ { 2 1 } ( t ) & K _ { 2 2 } ( t ) \end{pmatrix}$$

is the unique symmetric non-negative definite solution of the following matrix differential equation:

$$d \begin{pmatrix} K _ { 1 1 } ( t ) & K _ { 1 2 } ( t ) \\ K _ { 2 1 } ( t ) & K _ { 2 2 } ( t ) \end{pmatrix} = & \begin{bmatrix} 0 & 0 \\ \beta & 0 \end{bmatrix} \begin{pmatrix} K _ { 1 1 } ( t ) & K _ { 1 2 } ( t ) \\ K _ { 2 1 } ( t ) & K _ { 2 2 } ( t ) \end{pmatrix} \\ & + \begin{pmatrix} K _ { 1 1 } ( t ) & K _ { 1 2 } ( t ) \\ K _ { 2 1 } ( t ) & K _ { 2 2 } ( t ) \end{pmatrix} \begin{pmatrix} 0 & \beta \\ 0 & 0 \end{pmatrix} + \begin{pmatrix} \sigma & 0 \\ 0 & 0 \end{pmatrix} \sigma \\ & \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\$$

It is quite straightforward to solve (B.3) and (B.5) and thus find:

$$\begin{pmatrix} E ( V ( t ) - V ( t _ { 0 } ) ) \\ E ( Z ( t ) - Z ( t _ { 0 } ) ) \end{pmatrix} = \begin{pmatrix} ( r - \frac { 1 } { 2 } \sigma ^ { 2 } ) \left ( \varepsilon - T _ { 0 } \right ) \\ \frac { 1 } { 2 } \beta ( r - \frac { 1 } { 2 } \sigma ^ { 2 } ) \left ( t - T _ { 0 } \right ) ^ { 2 } + \beta V ( t _ { 0 } ) \left ( t - T _ { 0 } \right ) \end{pmatrix} \quad$$

$$\begin{pmatrix} K _ { 1 1 } ( t ) & K _ { 1 2 } ( t ) \\ K _ { 2 1 } ( t ) & K _ { 2 2 } ( t ) \end{pmatrix} = \begin{pmatrix} \sigma ^ { 2 } ( t - T _ { 0 } ) & \frac { 1 } { 2 } \beta \sigma ^ { 2 } ( t - T _ { 0 } ) ^ { 2 } \\ \frac { 1 } { 2 } \beta \sigma ^ { 2 } ( t - T _ { 0 } ) ^ { 2 } & \frac { 1 } { 3 } \beta ^ { 2 } \sigma ^ { 2 } ( t - T _ { 0 } ) ^ { 3 } \end{pmatrix} .$$

Combining (B.1), (B.6) and (B.7) immediately gives us formula (33). In order to prove (34)–(36) we remark that in cases in which A is a random variable, such that log A is normally distributed with mean E and variance V, and K &gt;0 is a real number, then:

$$E \max ( A - K , 0 ) = e ^ { E + \tilde { \nu } } N \left ( \frac { E - \log ( K ) + V } { \sqrt { V } } \right ) - K N \left ( \frac { E - \log ( K ) } { \sqrt { V } } \right ) ( B . 8 )$$

where N is the cumulative standard normal distribution function. This is merely an exercise in probability theory [the essential features of this formula were derived in Jarrow and Rudd (1983, pp. 92–95)]. By combining (33) and (B.8) we arrive at formulas (33)–(36).
