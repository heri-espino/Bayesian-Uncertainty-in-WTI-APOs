---
id: "kahale_2018_multilevel-monte-carlo-asian-options"
source_pdf: "../pdf/kahale_2018_multilevel-monte-carlo-asian-options.pdf"
source_filename: "kahale_2018_multilevel-monte-carlo-asian-options.pdf"
format: "academic-paper"
extraction_profile: "token-efficient-high-fidelity"
extraction_mode: "hybrid"
extraction_quality: "good"
extraction_score: 90.0
formula_enrichment: "codeformulav2"
table_structure: "accurate"
tables_png: 10
figures_png: 0
assets_dir: "../assets/kahale_2018_multilevel-monte-carlo-asian-options"
references_file: "../references/kahale_2018_multilevel-monte-carlo-asian-options.references.md"
---

<!-- p:1 -->

## General multilevel Monte Carlo methods for pricing discretely monitored Asian options

Nabil Kahal ́ e ∗

October 1, 2018

##### Abstract

We describe general multilevel Monte Carlo methods that estimate the price of an Asian option monitored at m fi xed dates. Our approach yields unbiased estimators with standard deviation O ( ǫ ) in O ( m + ǫ - 2 ) expected time for a variety of processes including the BlackScholes model, Merton's jump-diffusion model, the Square-Root diffusion model, Kou's double exponential jump-diffusion model, the variance gamma and NIG exponential Levy processes and, via the Milstein scheme, processes driven by scalar stochastic differential equations. Using the Euler scheme, our approach estimates the Asian option price with root mean square error O ( ǫ ) in O ( m + (ln( ǫ )) 2 ǫ - 2 ) expected time for processes driven by multidimensional stochastic differential equations. Numerical experiments confirm that our approach outperforms the conventional Monte Carlo method by a factor of order m .

Keywords: discretely monitored Asian option, multilevel Monte Carlo method, option pricing, variance reduction

## 1 Introduction

Asian options are financial derivatives whose payoff depends on the arithmetic average of an underlying during a specific time-period. Asian options are useful to corporations which are exposed to average exchange rates or commodity prices over a certain period of time. Pricing Asian options has been the subject of many studies. Under the Black-Scholes model, the price of a continuously sampled Asian option can be expressed as an infinite series (Linetsky 2004). Transform based methods have been used to value Asian options under Markov processes (Cai, Song and Kou 2015, Cui, Lee and Liu 2018). A convex programming method that computes optimal model-independent bounds on Asian option prices is described in (Kahal ́ e 2017). Monte Carlo methods can price Asian options under various models, but conventional Monte Carlo algorithms have a high computational cost, which motivates the need to improve the efficiency of such methods. Control variate techniques for pricing Asian options with Monte Carlo simulation are given in (Kemna and Vorst 1990, Dinge ̧ c and H ̈ ormann 2012, Shiraya and Takahashi 2017). An importance sampling algorithm for pricing Asian options is derived in (Glasserman, Heidelberger and Shahabuddin 1999). When the underlying follows a stochastic differential equation (SDE) satisfying certain regularity conditions, the multilevel Monte Carlo method (MLMC) described in (Giles 2008b) estimates the price of a continuously monitored Asian option with mean square error ǫ 2 in O ((ln( ǫ )) 2 ǫ - 2 ) time using the Euler discretization. This computational cost has been reduced to O ( ǫ - 2 ) time using the Milstein scheme for scalar SDEs (Giles 2008a, Giles, Debrabant and R ̈ oßler 2013) and multi-dimensional SDEs (Giles, Szpruch et al. 2014). For a broad class of pure-jump exponential Levy processes, the MLMC method described in (Giles and Xia 2017) estimates the price of a continuously monitored Asian option with mean square error ǫ 2 in O ( ǫ - 2 ) time. Randomized multilevel Monte Carlo methods (RMLMC) that produce efficient and unbiased estimators of expectations of functionals arising in SDEs are given in (Rhee and Glynn 2015, Vihola 2018). Exact simulation algorithms, which exist for several financial models (see (Glasserman 2004, § 3)), also yield unbiased estimators for prices of derivatives. More recent exact simulation methods have been developed for Heston's stochastic volatility model (Broadie and Kaya 2006, Glasserman and Kim 2011), jump-diffusion processes (Giesecke and Smelov 2013), and the SABR model (Cai, Song and Chen 2017).

∗ Europe, Labex ReFi and Big data research center, 75011 Paris, France; e-mail: nkahale@escpeurope.eu.


<!-- p:2 -->


Consider now an Asian option with a given maturity monitored at m fi xed dates. Even in the Black-Scholes model, the time required to estimate the option price with variance O ( ǫ 2 ) is Θ( mǫ - 2 ) under the conventional Monte Carlo method, assuming the payoff variance is upper and lower bounded by constants independent of m . This is because the simulation of the underlying prices at the m dates takes Θ( m ) time.

This paper describes a general multilevel framework to price an Asian option monitored at m dates. The basic idea behind our approach is to (approximately) simulate the forward prices at only a subset of the m dates at a given iteration. The forward prices at the remaining dates are then approximated by the average of surrounding forward prices. Our approach does not make any assumptions on the nature of the stochastic process driving the underlying. It however assumes the existence of a linear relationship between the underlying and forward prices, that the underlying price is square-integrable, and makes certain assumptions on the running time required to simulate the underlying on a discrete time grid with a given precision. The latter condition is satisfied in any model where the forward price process can be simulated exactly at m ′ fixed dates in O ( m ′ ) expected time. Using the Milstein scheme, it is also satisfied by processes driven by scalar SDEs. Our approach yields unbiased estimators with variance O ( ǫ 2 ) for the Asian option price in O ( m + ǫ - 2 ) expected time for a variety of processes including the Black-Scholes model, Merton's jump-diffusion model, the Square-Root model, Kou's double exponential jump-diffusion model, the variance gamma and NIG exponential Levy processes and, using the Milstein scheme, processes driven by scalar SDEs. Our method is also applicable with the same performance guarantees if the underlying is the average of assets that follow a multi-dimensional geometric Brownian motion. Using the Euler scheme, our approach estimates the Asian option price with mean square error O ( ǫ 2 ) in O ( m +(ln( ǫ )) 2 ǫ - 2 ) expected time for processes driven by one-dimensional or multidimensional SDEs. We are not aware of any previous Monte Carlo, MLMC or RMLMC method that provably achieves such tradeoffs between the running time and target accuracy, even under the Black-Scholes model. Giles, Debrabant and R ̈ oßler (2013) and Giles, Szpruch et al. (2014) mention that their methods can be used to price Asian options monitored at m dates, but do not analyse the performance of their algorithms in terms of m . Our paper makes three main contributions:

1. Our approach prices Asian options monitored at m dates and achieves a target accuracy O ( ǫ ) in O ( m + ǫ - 2 ) or O ( m +(ln( ǫ )) 2 ǫ - 2 ) expected time, depending on the assumptions satisfied by the diffusion process. It applies to a wide range of processes, including processes with jumps.
2. When the forward price process can be simulated exactly at m ′ fixed dates in O ( m ′ ) expected time, we give explicit upper-bounds on the variance of our estimators in terms of the underlying variance at T . Certain processes such as the Square-Root diffusion satisfy this condition even though they have no known discretization schemes with positive strong order of convergence, and so multilevel methods based on the Euler or Milstein schemes are inapplicable to such processes.
3. We do not make any assumptions on the dates at which the option is monitored. We assume that the sum of the absolute values of the weights associated with the monitoring dates is upper-bounded by a constant independent of m , but make no assumptions on the


<!-- p:3 -->


sign or order of magnitude of these weights. Our approach thus applies to average price and average strike options.

The rest of the paper is organized as follows. § 2 describes the modelling framework and recalls the MLMC and RMLMC methods. § 3 presents our algorithms for Asian options pricing. Examples are described in § 4. Numerical simulations are given in § 5. We provide concluding remarks in § 6. Omitted proofs are in the appendix, which also contains additional numerical results.

## 2 Preliminaries

### 2.1 The modelling framework

Assume that interest rates are deterministic. Let T be a fixed maturity and m a positive integer. Denote by F ( t ) the forward price of an underlying calculated at time t for maturity T . For 0 ≤ j ≤ m , let F j = F ( t j ), where t 0 &lt; · · · &lt; t m , with t 0 = 0 and t m = T . Note that F m is the underlying price at T . Let A = ∑ m j =1 w j F j be a linear combination of the forward prices, where the w j 's are non-zero signed weights whose absolute values sum up to 1. Consider an Asian option with payoff f ( A ) at maturity T , where f is a κ -Lipschitz real-valued function of one variable. Such a payoff can model Asian options that arise in a broad range of situations. For instance, the payoff of an average price call with strike K and maturity T on futures prices maturing at T is equal to f ( A ), with f ( x ) = max( x - K, 0) and w 1 = · · · = w m = 1 /m . This is because forward prices are equal to futures prices when interest rates are deterministic. Similarly, the payoff of an average strike call with maturity T on futures prices maturing at T is equal to f ( A ), where f ( x ) = 2max( x, 0) and w 1 = · · · = w m - 1 = - ( m - 1) - 1 / 2, with w m = 1 / 2. In the same vein, average price and average strike options have a payoff equal to f ( A ) for a suitable choice of f and of the weights w j 's if the underlying is a stock that pays deterministic dividends, or an index with a deterministic and continuous dividend rate, or an exchange rate. This is due to the existence of a deterministic linear relationship between the forward price and the underlying price (see (Hull 2014, Chap. 5)).

We assume the existence of a risk-neutral probability Q such that the sequence ( F j ), 0 ≤ j ≤ m , is a martingale under Q , and the price of the option at time 0 is e - rT E ( f ( A )), where r is the risk-free rate at time 0 for maturity T . The existence of Q can be shown under no-arbitrage conditions (see (Glasserman 2004, § 1.2.2)). All expectations in this paper are taken with respect to Q . We assume that F m is square-integrable. By (Revuz and Yor 1999, Corollary 1.6, p. 53), this implies that F j is square-integrable for 1 ≤ j ≤ m . We also assume that κ is upper-bounded by a constant independent of m .

### 2.2 The MLMC method

The MLMC method described in (Giles 2008b) efficiently estimates the expectation of a random variable Y L that is approximated with increasing accuracy by random variables Y l , 0 ≤ l ≤ L - 1, for some integer L . For 0 ≤ l ≤ L , denote by C l the expected cost of computing Y l - Y l - 1 , with Y - 1 := 0. Assume that Y l , 0 ≤ l ≤ L , are square-integrable. For 0 ≤ l ≤ L , let  ̄ Y l be the average of n l independent copies of Y l - Y l - 1 , where n l is a positive integer to be specified later. Assume that the estimators  ̄ Y 0 , . . . ,  ̄ Y L are independent. Following the analysis in (Giles 2008b),  ̄ Y = ∑ L l =0  ̄ Y l is an unbiased estimator of E ( Y L ), and

$$V a r ( \bar { Y } ) = \sum _ { l = 0 } ^ { L } \frac { \mu _ { l } } { n _ { l } } ,$$

where μ l ≜ Var( Y l - Y l - 1 ) for 0 ≤ l ≤ L . Let  ̄ C = ∑ L l =0 n l C l be the expected cost of computing  ̄ Y . It is observed in (Giles 2008b) that the work-normalized variance  ̄ C Var(  ̄ Y ) is minimized when n l is proportional to √ μ l /C l , ignoring integrality constraints. The work-normalized variance of an unbiased estimator is defined as the product of the variance and expected running time. Glynn and Whitt (1992) show that the efficiency of an unbiased estimator is inversely proportional to the work-normalized variance.


<!-- p:4 -->


### 2.3 The RMLMC method

We now recall a RMLMC method of Rhee and Glynn (2015) that efficiently estimates the expectation of a random variable Y that is approximated by random variables Y l , l ≥ 0. As in § 2.2, denote by C l the expected cost of computing Y l - Y l - 1 , for l ≥ 0, with Y - 1 := 0. Assume that Y and Y l , l ≥ 0, are square-integrable. Let ( p l ), l ≥ 0, be a probability distribution such that p l &gt; 0 for l ≥ 0. Let N ∈ N be an integral random variable independent of ( Y l : l ≥ 0) such that Pr( N = l ) = p l for l ≥ 0. Set Z = ( Y N - Y N - 1 ) /p N , with Y - 1 := 0. For a square-integrable random variable X , let || X || = √ E ( X 2 ). The following result is due to Rhee and Glynn (2015) (see also (Vihola 2018, Theorem 2)).

Theorem 2.1 ((Rhee and Glynn 2015)) . Assume that || Y l - Y || converges to 0 as l goes to infinity. If ∑ ∞ l =0 || Y l - Y l - 1 || 2 /p l is finite then Z is square-integrable, E ( Z ) = E ( Y ) , and

$$\| Z \| ^ { 2 } = \sum _ { l = 0 } ^ { \infty } \frac { \| Y _ { l } - Y _ { l - 1 } \| ^ { 2 } } { p _ { l } } .$$

Denote by C be the expected cost of computing Z . Propositions 2.1 and 2.2 below are in the same spirit as results previously obtained in (Giles 2008b, Theorem 3.1) and (Rhee and Glynn 2015). For completeness, we give their proof in the appendix. Proposition 2.1 shows that, under certain conditions on Y l and C l , the sequence ( p l ), l ≥ 0, can be chosen so that both || Z || and C are finite.

$$| | Y _ { l } - Y | | ^ { 2 } & \leq \nu 2 ^ { - \beta l } \\ \\$$

Proposition 2.1. Assume that || Y 0 || 2 ≤ ν and that, for l ≥ 0 ,

and C l ≤ c 2 l , where c , ν and β are positive constants, with β ∈ (1 , 2] . If, for l ≥ 0 ,

$$p _ { l } = ( 1 - 2 ^ { - ( \beta + 1 ) / 2 } ) 2 ^ { - ( \beta + 1 ) l / 2 } , \\ \\ U _ { \Gamma ( Z ) } = \Gamma ( Z ) \Gamma ( V )$$

then Z is square-integrable, E ( Z ) = E ( Y ) , and

Furthermore,

$$| | Z | | ^ { 2 } \leq \frac { 2 0 \nu } { 1 - 2 ^ { - ( \beta - 1 ) / 2 } } .$$

$$C & \leq \frac { c } { 1 - 2 ^ { - ( \beta - 1 ) / 2 } } . \\ \text {sition } 2 . 2 \text { shows how to construct a biased estimator } Z _ { L } \text { of } Y , \text { for}$$

If we relax (2.2), Proposition 2.2 shows how to construct a biased estimator Z L of Y , for any positive integer L , with expected cost and variance bounded by a linear function of L , and a bias that decreases geometrically with L .

Proposition 2.2. Assume that || Y 0 || 2 ≤ ν and that, for l ≥ 0 ,

and C l ≤ c 2 l , where ν and c are positive constants. Let p l = 2 - ( l +1) for l ≥ 0 . Fix a positive integer L and set Z L = ( Y N - Y N - 1 ) 1 N ≤ L /p N . Then Z L is square-integrable,

and

Furthermore, the expected cost of computing Z L is at most cL .

$$| | Y _ { l } - Y | | ^ { 2 } & \leq \nu 2 ^ { - l } & & ( 2 . 6 ) \\ & \ddots & & & \\$$

$$( E ( Z _ { L } - Y ) ) ^ { 2 } \leq \nu 2 ^ { - L } ,$$

$$| | Z _ { L } | | ^ { 2 } & \leq 1 2 \nu ( L + 1 ) . \\ \intertext { a l $ o f $ o f $ o m p u t $ i n $ a $ }$$


<!-- p:5 -->


More sophisticated versions of the RMLMC method can be found in (Rhee and Glynn 2015, Vihola 2018).

## 3 Multilevel algorithms for Asian options

We construct multilevel approximations of A in § 3.1 and use them in § 3.2 and § 3.3 to build estimators of the Asian option price. § 3.2 considers the case where forward prices can be simulated exactly, while § 3.3 treats the case where forward prices can be simulated approximately. Set a = f (( ∑ m j =1 w j ) F 0 ) and U = f ( A ) - a .

### 3.1 Multilevel approximations of A

Here we construct an increasing sequence of subsets of { 1 , . . . , m } and show that A is approximated, with increasing accuracy, by linear combinations of forward prices corresponding to these subsets. For integers i and j with 1 ≤ i ≤ m and 0 ≤ j ≤ m , let

$$W ( i , j ) = \sum _ { k = i } ^ { j } w _ { k } \text { and } W ^ { \prime } ( i , j ) = \sum _ { k = i } ^ { j } | w _ { k } | .$$

By convention, W ( i, j ) = W ′ ( i, j ) = 0 if j &lt; i . Define the subsets J l of { 1 , . . . , m } , for l ≥ 0, as follows. Set L = ⌈ log 2 m ⌉ and J l = { 1 , . . . , m } for l ≥ L . For 0 ≤ l ≤ L - 1, let

$$J _ { l } = \{ j \in \{ 1 , \dots , m \} \colon 2 ^ { l } W ^ { \prime } ( 1 , j - 1 ) < \lfloor 2 ^ { l } W ^ { \prime } ( 1 , j ) \rfloor \} .$$

Note that J 0 = { m } . Roughly speaking, J l consists of the indices j where the sequence W ′ (1 , j ) 'jumps' over a multiple of 2 - l . It is therefore reasonable to expect that the sequence ( J l ), l ≥ 0, is increasing and that the size of J l is at most 2 l +1.

Proposition 3.1. For l ≥ 0 ,

and

$$| J _ { l } | \leq 2 ^ { l } + 1$$

$$J _ { l } \subseteq J _ { l + 1 } .$$

Proposition 3.1 implies that, for 0 ≤ l ≤ L - 1,

$$J _ { l } = \{ j \in J _ { l + 1 } \colon 2 ^ { l } W ^ { \prime } ( 1 , j - 1 ) < \lfloor 2 ^ { l } W ^ { \prime } ( 1 , j ) \rfloor \} .$$

For l ≥ 0, define the following trapezoidal approximation of A :

$$A _ { l } = \sum _ { j \in J _ { l } } w _ { j } F _ { j } + \frac { 1 } { 2 } \sum _ { ( i , k ) \in \mathcal { P } _ { l } } W ( i + 1 , k - 1 ) ( F _ { i } + F _ { k } ) ,$$

where P l is the set of pairs of consecutive of elements of the set { 0 } ∪ J l . Thus A l is obtained from A by replacing each F j with ( F i + F k ) / 2 for each pair ( i, k ) ∈ P l and each integer j with i &lt; j &lt; k . By construction, A l is a deterministic linear function of ( F j ), j ∈ J l . Note that A l = A for l ≥ L . Theorem 3.1 below gives a bound on the L 2 -distance between A 0 and W (1 , m ) F 0 on one hand, and between A l and A on the other hand.

Theorem 3.1. || A 0 - W (1 , m ) F 0 || 2 ≤ Var( F m ) and, for l ≥ 0 ,

$$| | A _ { l } - A | | ^ { 2 } \leq 2 ^ { - 2 l } \text {Var} ( F _ { m } ) .$$

Algorithm M below calculates the coefficients W ( i +1 , k - 1) in (3.5), for 0 ≤ l ≤ L - 1 and ( i, k ) ∈ P l , in O ( m ) total time, using the following steps.


<!-- p:6 -->


1. Calculate recursively W (1 , j ) and W ′ (1 , j ) for 1 ≤ j ≤ m .
2. Construct by backward induction the subsets J l , for 0 ≤ l ≤ L , using (3.4). This takes O ( m ) total time since | J l +1 | ≤ 1+2 l +1 for l ∈ { 0 , . . . , L - 1 } , and so J l can be constructed in O (2 l ) time.
3. For l ∈ { 0 , . . . , L - 1 } and each pair ( i, k ) ∈ P l , calculate W ( i +1 , k - 1) via the relation W ( i + 1 , k - 1) = W (1 , k - 1) - W (1 , i ). For each level l , this takes O (2 l ) time, and so this step takes O ( m ) total time.

### 3.2 The exact simulation case

Assumption 1 (A1). There is a constant c independent of m such that, for any subset J of { 1 , . . . , m } , the expectation of the time required to simulate the vector ( F j ), j ∈ J , is at most c | J | .

A1 holds if the expectation of the time to simulate the forward price process on a discrete time grid of size n is O ( n ). Examples where A1 holds are given in § 4. Theorem 3.2 below shows how to construct an unbiased estimator of the Asian option price under A1 using the RMLMC method.

Theorem 3.2. Suppose A1 holds. Let N ∈ N be an integral random variable independent of ( F j : 1 ≤ j ≤ m ) such that Pr( N = l ) = p l for non-negative integer l , where p l = (1 - 2 - 3 / 2 )2 - 3 l/ 2 . Set V = ( U N - U N - 1 ) /p N , where U l = f ( A l ) - a for l ≥ 0 and U - 1 = 0 . Then V is square-integrable,

$$E ( f ( A ) ) = E ( V ) + a ,$$

$$\text {Var} ( V ) \leq 7 0 \kappa ^ { 2 } \text {Var} ( F _ { m } ) . \\ \quad \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \$$

Furthermore, the expectation of the time required to simulate V is upper-bounded by a constant independent of m .

Proof. Since | J l | ≤ 2 l +1, the expectation of the time to simulate the vector ( F j ), j ∈ J l , is at most c 2 l +1 . Together with (3.5), this implies the existence of a constant c ′ independent of m such that, for l ≥ 0, the expectation of the time to simulate U l - U l - 1 is at most c ′ 2 l . Since A L = A , we have U L = U . By (3.5), A l is square-integrable for l ≥ 0 and, since f is κ -Lipschitz, so are U l and U . As | U 0 | ≤ κ | A 0 - W (1 , m ) F 0 | , Theorem 3.1 implies that

$$| | U _ { 0 } | | ^ { 2 } \leq \kappa ^ { 2 } \text {Var} ( F _ { m } ) .$$

Similarly, as | U l - U | ≤ κ | A l - A | for l ≥ 0, by Theorem 3.1,

$$| | U _ { l } - U | | ^ { 2 } \leq \kappa ^ { 2 } 2 ^ { - 2 l } \text {Var} ( F _ { m } ) .$$

The conditions of Proposition 2.1 are thus met for Y = U and Y l = U l for l ≥ 0, with ν = κ 2 Var( F m ), β = 2 and c = c ′ . By (2.5), the expectation of the time required to simulate V is at most 4 c ′ . Furthermore, V is square-integrable with E ( V ) = E ( U ), which yields (3.7). Similarly, (3.8) follows from (2.4).

Theorem 3.2 shows that e - rT ( V + a ) is an unbiased estimator of the Asian option price that can be simulated in constant time with variance bounded by a constant independent of m . Simulating ⌈ ǫ - 2 ⌉ independent copies of V yields an unbiased estimator of the option price with variance O ( ǫ 2 ) in O ( m + ǫ - 2 ) expected time, including the O ( m ) preprocessing cost of Algorithm M.

Theorem 3.3 below shows how to construct another unbiased estimator of the Asian option price under A1 using the MLMC method.

and Theorem 3.3. Suppose A1 holds. Define U l , l ≥ - 1 , as in Theorem 3.2 and, for 0 ≤ l ≤ L , let μ l = Var( U l - U l - 1 ) and For 0 ≤ l ≤ L , let  ̄ U l be the average of n l independent copies of U l - U l - 1 . Assume that the estimators  ̄ U 0 , . . . ,  ̄ U L are independent. Set  ̄ U = ∑ L l =0  ̄ U l . Then and Furthermore, the expectation of the time required to simulate  ̄ U is O ( m ) .


<!-- p:7 -->


$$n _ { l } = \left \lfloor 1 + \frac { m \sqrt { \mu _ { l } / J _ { l } } } { \sum _ { l ^ { \prime } = 0 } ^ { L } \sqrt { \mu _ { l ^ { \prime } } | J _ { l ^ { \prime } } } } \right \rfloor . \\ \intertext { b e t h e a v e r a g e o f $ n _ { l } $ i n d e p e n d e n t c o p i e s o f $ U _ { l } - U _ { l - 1 } . $ A s s u m e t h a t h e }$$

$$E ( f ( A ) ) = E ( \bar { U } ) + a ,$$

$$\ m V a r ( \bar { U } ) & \leq 2 4 0 \kappa ^ { 2 } V a r ( F _ { m } ) . \\ \intertext { m V a r ( \bar { U } ) } \alpha \colon \intertext { \intertext { m V a r ( \bar { U } ) } \alpha \colon \intertext { \intertext { m V a r ( \bar { U } ) } } \alpha ^ { 2 } \intertext { \intertext { m V a r ( \bar { U } ) } } \alpha ^ { 2 } \intertext { \intertext { m V a r ( \bar { U } ) } } \alpha ^ { 2 } \intertext { \intertext { m V a r ( \bar { U } ) } } \alpha ^ { 2 } \intertext { \intertext { m V a r ( \bar { U } ) } } \alpha ^ { 2 } \intertext { \intertext { m V a r ( \bar { U } ) } } \alpha ^ { 2 } \intertext { \intertext { m V a r ( \bar { U } ) } } \alpha ^ { 2 } \intertext { \intertext { m V a r ( \bar { U } ) } } \alpha ^ { 2 } \intertext { \intertext { m V a r ( \bar { U } ) } } \alpha ^ { 2 } \intertext { \intertext { m V a r ( \bar { U } ) } } \alpha ^ { 2 } \intertext { \intertext { m V a r ( \bar { U } ) } } \alpha ^ { 2 } \intertext { \intertext { m V a r ( \bar { U } ) } } \alpha ^ { 2 } \intertext { \intertext { m V a r ( \bar { U } ) } } \alpha ^ { 2 } \intertext { \intertext { m V a r ( \bar { U } ) } } \alpha ^ { 2 } \intertext { \intertext { m V a r ( \bar { U } ) } } \alpha ^ { 2 } \intertext { \intertext { m V a r ( \bar { U } ) } } \alpha ^ { 2 } \intertext { \intertext { m V a r ( \bar { U } ) } } \alpha ^ { 2 } \intertext { \intertext { m V a r ( \bar { U } ) } } \alpha ^ { 2 } \intertext { \intertext { m V a r ( \bar { U } ) } } \alpha ^ { 2 } \intertext { \intertext { m V a r ( \bar { U } ) } } \alpha ^ { 2 } \intertext { \intertext { m V a r ( \bar { U } ) } } \alpha ^ { 2 } \intertext { \intertext { m V a r ( \bar { U } ) } } \alpha ^ { 2 } \intertext { \intertext { m V a r ( \bar { U } ) } } \alpha ^ { 2 } \intertext { \intertext { m V a r ( \bar { U } ) } } \alpha ^ { 2 } \intertext { \intertext { m V a r ( \bar { U } ) } } \alpha ^ { 2 } \intertext { \intertext { m V a r ( \bar { U } ) } } \alpha ^ { 2 } \intertext { \intertext { m V a r ( \bar { U } ) } } \alpha ^ { 2 } \intertext { \intertext { m V a r ( \bar { U } ) } } \alpha ^ { 2 } \intertext { \intertext { m V a r ( \bar { U } ) } } \alpha ^ { 2 } \intertext { \intertext { m V a r ( \bar { U } ) } } \alpha ^ { 2 } \intertext { \intertext { m V a r ( \bar { U } ) } } \alpha ^ { 2 } \intertext { \intertext { m V a r ( \bar { U } ) } } \alpha ^ { 2 } \intertext { \intertext { m V a r ( \bar { U } ) } } \alpha ^ { 2 } \intertext { \intertext { m V a r ( \bar { U } ) } } \alpha ^ { 2 } \intertext { \intertext { m V a r ( \bar { U } ) } } \alpha ^ { 2 } \intertext { \intertext { m V a r ( \bar { U } ) } } \alpha ^ { 2 } \intertext { \intertext { m V a r ( \bar { U } ) } } \alpha ^ { 2 } \intertext { \intertext { m V a r ( \bar { U } ) } } \alpha ^ { 2 } \intertext { \intertext { m V a r ( \bar { U } ) } } \alpha ^ { 2 } \intertext { \intertext { m V a r ( \bar { U } ) } } \alpha ^ { 2 } \intertext { \intertext { m V a r ( \bar { U } ) } } \alpha ^ { 2 } \intertext { \intertext { m V a r ( \bar { U } ) } } \alpha ^ { 2 } \intertext { \intertext { m V a r ( \bar { U } ) } } \alpha ^ { 2 } \intertext { \intertext { m V a r ( \bar { U } ) } } \alpha ^ { 2 } \intertext { \intertext { m V a r ( \bar { U } ) } } \alpha ^ { 2 } \intertext { \intertext { m V a r ( \bar { U } ) } } \alpha ^ { 2 } \intertext { \intertext { m V a r ( \bar { U } ) } } \alpha ^ { 2 } \intertext { \intertext { m V a r ( \bar { U } ) } } \alpha ^ { 2 } \intertext { \intertext { m V a r ( \bar { U } ) } } \alpha ^ { 2 } \intertext { \intertext { m V a r ( \bar { U } ) } } \alpha ^ { 2 } \intertext { \intertext { m V a r ( \bar { U } ) } } \alpha ^ { 2 } \intertext { \intertext { m V a r ( \bar { U } ) } } \alpha ^ { 2 } \intertext { \intertext { m V a r ( \bar { U } ) } } \alpha ^ { 2 } \intertext { \intertext { m V a r ( \bar { U } ) } } \alpha ^ { 2 } \intertext { \intertext { m V a r ( \bar { U } ) } } \alpha ^ { 2 } \intertext { \intertext { m V a r ( \bar { U } ) } } \alpha ^ { 2 } \intertext { \intertext { m V a r ( \bar { U } ) } } \alpha ^ { 2 } \intertext { \intertext { m V a r ( \bar { U } ) } } \alpha ^ { 2 } \intertext { \intertext { m V a r ( \bar { U } ) } } \alpha ^ { 2 } \intertext { \intertext { m V a r ( \bar { U } ) } } \alpha ^ { 2 } \intertext { \intertext { m V a r ( \bar { U } ) } } \alpha ^ { 2 } \intertext { \intertext { m V a r ( \bar { U } ) } } \alpha ^ { 2 } \intertext { \intertext { m V a r ( \bar { U } ) } } \alpha ^ { 2 } \intertext { \intertext { m V a r ( \bar { U } ) } } \alpha ^ { 2 } \intertext { \intertext { m V a r ( \bar { U } ) } } \alpha ^ { 2 } \intertext { \intertext { m V a r ( \bar { U } ) } } \alpha ^ { 2 } \intertext { \intertext { m V a r ( \bar { U } ) } } \alpha ^ { 2 } \intertext { \intertext { m V a r ( \bar { U } ) } } \alpha ^ { 2 } \intertext { \intertext { m V a r ( \bar { U } ) } } \alpha ^ { 2 } \intertext { \intertext { m V a r ( \bar { U }$$

Assuming the variances μ l , 0 ≤ l ≤ L , are known, Theorem 3.3 shows that e - rT (  ̄ U + a ) is an unbiased estimator of the Asian option price that can be simulated in O ( m ) time with variance O (1 /m ). Simulating ⌈ ǫ - 2 /m ⌉ independent copies of  ̄ U yields an unbiased estimator of the option price with variance O ( ǫ 2 ) in O ( m + ǫ - 2 ) expected time. The variances μ l can be estimated by Monte Carlo simulation.

### 3.3 The approximate simulation case

For J ⊆ { 1 , . . . , m } , let R J denote the set of vectors of dimension | J | , indexed by the elements of J .

Assumption 2 (A2). There are constants c 1 , c 2 and β ∈ [1 , 2] such that, for l ≥ 0 and J ⊆ { 1 , . . . , m } , there is a random vector ˆ F = ˆ F ( J, l ) ∈ R J such that || ˆ F j - F j || 2 ≤ c 2 2 - βl for any j ∈ J . For l ≥ 1 and J ′ ⊆ J ⊆ { 1 , . . . , m } , the expected time required to simulate the vector ( ˆ F ( J ′ , l - 1) , ˆ F ( J, l )) is at most c 1 ( | J | +2 l ).

The first condition in A2 says that, for l ≥ 0 and J ⊆ { 1 , . . . , m } , the forward price F j is approximated by ˆ F j with 'mean square error' at most c 2 2 - βl for any j ∈ J , where ˆ F = ˆ F ( J, l ). The second condition gives an upper bound on the expected time to jointly simulate ˆ F ( J ′ , l - 1) and ˆ F ( J, l ). It is shown in § I that A2 holds under certain regularity conditions when the Euler or Milstein schemes are used to approximately simulate forward prices.

Assume now that A2 holds. For l ≥ 0, let ˆ F l = ˆ F ( J l , l ) and

$$\hat { A } _ { l } = \sum _ { j \in J _ { l } } w _ { j } \hat { F } _ { j } ^ { l } + \frac { 1 } { 2 } \sum _ { ( i , k ) \in \mathcal { P } _ { l } } W ( i + 1 , k - 1 ) ( \hat { F } _ { i } ^ { l } + \hat { F } _ { k } ^ { l } ) .$$

Thus ˆ A l is obtained from A by replacing each F j with ˆ F l j if j ∈ J l and by ( ˆ F l i + ˆ F l k ) / 2 if ( i, k ) ∈ P l and i &lt; j &lt; k . Note that ˆ A l is a deterministic linear function of the vector ˆ F l . Proposition 3.2 below gives a bound on the L 2 -distance between ˆ A 0 and W (1 , m ) F 0 on one hand, and between ˆ A l and A on the other hand.

Proposition 3.2. If A2 holds then || ˆ A 0 - W (1 , m ) F 0 || 2 ≤ c 3 and || ˆ A l - A || 2 ≤ c 3 2 - βl for l ≥ 0 , where c 3 = 2( c 2 +Var( F m )) .

Theorem 3.4 below shows how to construct an unbiased estimator of the Asian option price under A2, with β &gt; 1. The case β = 1 will be considered in Theorem 3.5.


<!-- p:8 -->


Theorem 3.4. Suppose A2 holds with β &gt; 1 . Let N ∈ N be an integral random variable independent of ( ˆ F ( J l , l ) : l ≥ 0) such that Pr( N = l ) = p l for non-negative integer l , where p l is given by (2.3) . Let ˆ U l = f ( ˆ A l ) - a for l ≥ 0 , and let ˆ V = ( ˆ U N - ˆ U N - 1 ) /p N , where ˆ U - 1 := 0 . Then ˆ V is square-integrable and

$$E ( f ( A ) ) = E ( \hat { V } ) + a .$$

Furthermore, Var( ˆ V ) and the expectation of the time required to simulate ˆ V are upper-bounded by constants independent of m .

As per the discussion following Theorem 3.2, Theorem 3.4 shows that e - rT ( ˆ V + a ) is an unbiased estimator of the Asian option price that can be simulated in constant time and with variance bounded by a constant independent of m . Independent ⌈ ǫ - 2 ⌉ runs of this estimator yield an unbiased estimator of the Asian option price with variance O ( ǫ 2 ) in O ( m + ǫ - 2 ) expected time.

Theorem 3.5 below constructs an estimator of the option price with an arbitrarily small bias when A2 holds with β = 1.

Theorem 3.5. Suppose A2 holds with β = 1 . Fix ǫ ∈ (0 , 1 / 2) and set L = ⌈ 2log 2 (1 /ǫ ) ⌉ . Let N ∈ N be an integral random variable independent of ( ˆ F ( J l , l ) : l ≥ 0) such that Pr( N = l ) = 2 - ( l +1) for l ∈ N . Let ˆ U l = f ( ˆ A l ) - a for l ≥ 0 , and let

$$\hat { V } = \frac { \hat { U } _ { N } - \hat { U } _ { N - 1 } } { p _ { N } } 1 _ { N \leq L } ,$$

where ˆ U - 1 := 0 . Then ˆ V is square-integrable and

$$( E ( \hat { V } ) + a - E ( f ( A ) ) ) ^ { 2 } \leq c _ { 3 } \kappa ^ { 2 } \epsilon ^ { 2 } ,$$

where c 3 is defined as in Proposition 3.2. Furthermore, there are constants c 4 and c 5 independent of m and of ǫ such that Var( ˆ V ) ≤ c 4 ln(1 /ǫ ) and the expectation of the time required to simulate ˆ V is upper-bounded by c 5 ln(1 /ǫ ) .

Under the assumptions of Theorem 3.5, the Asian option price can be calculated with O ( ǫ 2 ) mean square error in O ( m + ǫ - 2 ln 2 (1 /ǫ )) expected time as follows. We simulate n independent copies of ˆ V , where n = ⌈ ln(1 /ǫ ) ǫ - 2 ⌉ , and take their average ˆ V n . Since Var( ˆ V n ) = Var( ˆ V ) /n , we have Var( ˆ V n ) ≤ c 4 ǫ 2 . Furthermore, as E ( ˆ V n ) = E ( ˆ V ), it follows from (3.16) that

$$( E ( \hat { V } _ { n } ) + a - E ( f ( A ) ) ) ^ { 2 } \leq c _ { 3 } \kappa ^ { 2 } \epsilon ^ { 2 } .$$

Since the mean square error is the sum of the variance and squared bias, we conclude that

$$| | \hat { V } _ { n } + a - E ( f ( A ) ) | | ^ { 2 } \leq ( c _ { 4 } + c _ { 3 } \kappa ^ { 2 } ) \epsilon ^ { 2 } .$$

Thus e - rT (  ̄ V + a ) is an estimate of the Asian option price e - rT E ( f ( A )) with mean square error O ( ǫ 2 ). The total expected time to simulate ˆ V n is O ( m +ln 2 ( ǫ ) ǫ - 2 ), including the cost of Algorithm M.

## 4 Examples

Below are examples where A1 holds.


<!-- p:9 -->


### 4.1 The Black-Scholes model

In this model, F ( t ) satisfies the SDE

$$d F ( t ) = \sigma F ( t ) d W$$

on [0 , T ], where σ is a constant volatility and W is a one-dimensional Brownian motion under Q . Given J ⊆ { 1 , . . . , m } , let n = | J | , and let 0 = τ 0 &lt; τ 1 &lt; · · · &lt; τ n be the elements of the time grid G = { 0 } ∪ { t j : j ∈ J } , sorted in increasing order. Let X 1 , . . . , X n be independent standard Gaussian random variables. We simulate the forward prices on G in O ( n ) time using the following recursive procedure (Glasserman 2004, § 3.2.1):

$$F ( \tau _ { k } ) = F ( \tau _ { k - 1 } ) \exp ( - \sigma ^ { 2 } \frac { \tau _ { k } - \tau _ { k - 1 } } { 2 } + \sigma \sqrt { \tau _ { k } - \tau _ { k - 1 } } X _ { k } ) , \\$$

1 ≤ k ≤ n . Then, for j ∈ J , we set F j = F ( τ k ). where k is the index such that τ k = t j . Thus A1 holds for the Black-Scholes model. Furthermore, it is well-known that the forward price is square-integrable at any fixed date in this model.

### 4.2 Merton's jump-diffusion model

The risk-neutral process for the forward price in this model (see (Merton 1976)) is:

$$\frac { d F ( t ) } { F ( t - ) } = - \lambda m d t + \sigma d W ( t ) + d J ( t )$$

on [0 , T ], where W is a Brownian motion, J ( t ) = ∑ N ( t ) j =1 ( Y j - 1), and N ( t ) is a Poisson process with rate λ . If a jump occurs at time τ j , then S ( τ j +) = S ( τ j - ) Y j , where ln( Y j ) is a Gaussian random variable with mean β and standard deviation γ . The model parameters satisfy the equation: m + 1 = exp( β + γ 2 / 2). We assume that W , N and the Y j 's are independent. An algorithm that simulates the forward price process on a discrete time grid of size n in O ( n ) expected time is given in (Glasserman 2004, § 3.5.1). Thus A1 holds for Merton's jump-diffusion model. A classical calculation based on (Glasserman 2004, § 3.5.1) shows that the forward price is square-integrable at any fixed date in this model.

### 4.3 The Square-Root diffusion model

Here we assume that F ( t ) satisfies the following SDE:

$$d F ( t ) = \sigma \sqrt { F ( t ) } d W ( t ) \\$$

on [0 , T ], where W is a Brownian motion under Q , and σ &gt; 0. The Square-Root diffusion model, introduced in (Cox and Ross 1976), is a special case of the CEV model. An algorithm that simulates the forward price process on a discrete time grid of size n in O ( n ) expected time is described in § J. Thus A1 holds for the Square-Root diffusion model. It is also shown in § J that F m is square-integrable.

It is well-known that the standard Euler scheme is not defined for Square-Root diffusions because it may produce negative forward prices. The related Cox-Ingersoll-Ross process has an implicit Euler scheme with a strong convergence of order 1 (see (Alfonsi 2015, § 3.2)) under certain assumptions on the model parameters, but we are not aware of discretization schemes with positive strong order of convergence for Square-Root diffusions.


<!-- p:10 -->


### 4.4 Other examples

It can be shown that A1 holds for a variety of other processes such as Kou's double exponential jump-diffusion model (see (Kou 2002)), and the variance gamma and NIG exponential Levy processes. Algorithms that simulate these processes on a discrete time-grid are described in (Glasserman 2004, § 3.5), and it is easy to prove that the underlying second moment is finite under certain conditions on the model parameters. A1 also holds if the underlying is the average of assets that follow a multi-dimensional geometric Brownian motion. An algorithm that jointly simulates such assets is given in (Glasserman 2004, § 3.2.3).

## 5 Numerical experiments

We have implemented the RMLMC method of Theorem 3.2, and the MLMC method of Theorem 3.3, but replaced m with 30 m in (3.11) in order to mitigate the rounding effect and achieve greater efficiency. The variances μ l were estimated by Monte Carlo simulation using 10 4 independent runs. The RMLMC method based on the Milstein scheme (RMLMC-Milstein) was implemented for the Black-Scholes model as described in Theorem 3.4, with β = 2, without solving explicitly (4.1). The codes were written in the C++ programming language. Our experiments assume that interest rates are constant and equal to r . In Tables 1 through 10, 'Price' is the estimated Asian option price obtained via n independent replications, and 'Std' is the estimated price standard error. The variable 'Cost' refers to the total number of simulated underlying prices throughout the n replications. Thus, Cost × Std 2 is an estimate of the worknormalized variance. In each table, the number of independent replications is chosen so that the variable 'Cost' has the same order of magnitude for the studied algorithms. As the variance of a single run of the standard Monte Carlo estimator is e - 2 rT Var( f ( A )), the variance reduction

factor VRF is defined as

where Var( f ( A )) is estimated via 10 5 independent samples of A . The payoff of an average price call with strike K is max( m - 1 ( ∑ m i =1 S i ) - K, 0), while the payoff of an average strike call is max( S m - ( m - 1) - 1 ( ∑ m - 1 i =1 S i ) , 0), where S i is the underlying price at t i = iT/m .

$$V R F = \frac { m e ^ { - 2 r T } V a r ( f ( A ) ) } { C o s t \times S t d ^ { 2 } } , \\ v i a \, 1 0 ^ { 5 } \, i n d e p e n d e n t \, s a m p l e s \, o f \, A .$$

### 5.1 The Black-Scholes model

In our experiments, the underlying is a stock S with no dividends, and the model parameters are S 0 = 2, σ = 50%, r = 5%, and T = 2. These values are taken from (Linetsky 2004). Table 1 gives our results for average price calls with K = 2 and selected values of m . The cost of a single replication, i.e. Cost /n , is roughly independent of m for the RMLMC and RMLMC-Milstein algorithms, and is roughly proportional to m for the MLMC algorithm. For the RMLMC, MLMC and RMLMC-Milstein algorithms, the products Cost × Std 2 are roughly independent of m , and the VRFs are roughly proportional to m . These results are consistent with Theorems 3.2, 3.3 and 3.4. Table 2 reports similar results for average strike calls. In Table 1, the RMLMC and MLMC methods have a similar performance, and slightly outperform the RMLMC-Milstein algorithm. In Table 2, the MLMC method slightly outperforms the RMLMC method. This can be explained by observing that the frequencies n l in Theorem 3.3 are nearoptimal, which is not always the case for the probabilities p l in Theorem 3.2. The RMLMC method outperforms the RMLMC-Milstein algorithm by about a factor of 2. In practice, the price of a continuously monitored Asian option can be approximated by using a very large value of m , as reported in Table 3. The price of the average price call produced by the RMLMC algorithm in Table 3 is very close to the price of the continuously monitored average price call given in (Linetsky 2004), which is 0 . 350095.


<!-- p:11 -->


### 5.2 Merton's jump-diffusion model

In our experiments, the underlying is an index with constant dividend yield q . The model parameter values used are S 0 = 2, σ = 17 . 65%, r = 5 . 59%, q = 1 . 14%, λ = 8 . 90%, β = - 88 . 98%, and γ = 45 . 05%. Except for the spot price, these values are taken from (Andersen and Andreasen 2000), where they were obtained by fitting option prices with maturities ranging from one month to ten years. We set T = 2. Tables 4 and 5 give prices of average price and average strike calls, respectively, using the RMLMC and MLMC algorithms. The estimated work-normalized variances of the RMLMC and MLMC methods are roughly independent of m , and the VRFs are roughly proportional to m . The RMLMC and MLMC methods have a similar performance for average price calls, but MLMC slightly outperforms RMLMC for average strike calls.

### 5.3 The Square-Root diffusion model

The model parameter values in our experiments are S 0 = 2, r = 5%, σ = 0 . 4, and T = 2. Tables 6 and 7 give prices of average price and average strike calls, respectively, using the RMLMC and MLMC algorithms. Our simulation results are similar in nature to those of the Black-Scholes model and Merton's jump-diffusion model.

## 6 Conclusion

We have described a general MLMC framework to estimate the price of an Asian option monitored at m dates. We assume the existence of a linear relation between the underlying and forward prices, and that the underlying price is square-integrable at maturity T . Our approach yields unbiased estimators with variance O ( ǫ 2 ) in O ( m + ǫ - 2 ) expected time for a variety of processes that can be simulated exactly and, via the Milstein scheme, processes driven by scalar SDEs. Using the Euler scheme, our approach estimates the Asian option price with mean square error O ( ǫ 2 ) in O ( m +(ln( ǫ )) 2 ǫ - 2 ) expected time for processes driven by multidimensional SDEs. Numerical experiments confirm that our approach outperforms the conventional Monte Carlo method by a factor of order m .

### Acknowledgments

This research has been presented at the 35th Spring International Conference of the French Finance Association, May 2018. The author thanks Aur ́ elien Alfonsi, Mike Giles, Benjamin Jourdain and conference participants for helpful conversations. This work was achieved through the Laboratory of Excellence on Financial Regulation (Labex ReFi) under the reference ANR10-LABX-0095. It benefitted from a French government support managed by the National Research Agency (ANR).

Table 1: Pricing average price calls in the Black-Scholes model with strike K = 2

|         |                | n        | Price     | Std            | Cost          | Cost × Std 2   | VRF   |
|---------|----------------|----------|-----------|----------------|---------------|----------------|-------|
| m = 125 | RMLMC          | 1 × 10 9 | 0 . 35239 | 4 . 6 × 10 - 5 | 2 . 1 × 10 9  | 4 . 5          | 12    |
|         | MLMC           | 8 × 10 5 | 0 . 35231 | 4 . 6 × 10 - 5 | 2 . 16 × 10 9 | 4 . 6          | 12    |
|         | RMLMC-Milstein | 1 × 10 9 | 0 . 35236 | 4 . 4 × 10 - 5 | 3 . 3 × 10 9  | 6 . 4          | 8 . 5 |
| m = 250 | RMLMC          | 1 × 10 9 | 0 . 35126 | 4 . 7 × 10 - 5 | 2 . 13 × 10 9 | 4 . 7          | 24    |
|         | MLMC           | 4 × 10 5 | 0 . 35128 | 4 . 7 × 10 - 5 | 2 . 21 × 10 9 | 4 . 8          | 23    |
|         | RMLMC-Milstein | 1 × 10 9 | 0 . 35127 | 4 . 5 × 10 - 5 | 3 . 33 × 10 9 | 6 . 6          | 17    |
| m = 500 | RMLMC          | 1 × 10 9 | 0 . 3507  | 4 . 7 × 10 - 5 | 2 . 15 × 10 9 | 4 . 8          | 45    |
|         | MLMC           | 2 × 10 5 | 0 . 35069 | 4 . 7 × 10 - 5 | 2 . 22 × 10 9 | 5              | 43    |
|         | RMLMC-Milstein | 1 × 10 9 | 0 . 35082 | 4 . 5 × 10 - 5 | 3 . 36 × 10 9 | 6 . 8          | 32    |


<!-- p:12 -->


Table 2: Pricing average strike calls in the Black-Scholes model

|         |                | n        | Price     | Std            | Cost          | Cost × Std 2   | VRF   |
|---------|----------------|----------|-----------|----------------|---------------|----------------|-------|
| m = 125 | RMLMC          | 1 × 10 9 | 0 . 36325 | 6 . 2 × 10 - 5 | 1 . 42 × 10 9 | 5 . 4          | 17    |
|         | MLMC           | 8 × 10 5 | 0 . 36327 | 4 . 3 × 10 - 5 | 2 . 11 × 10 9 | 3 . 9          | 23    |
|         | RMLMC-Milstein | 1 × 10 9 | 0 . 36332 | 6 . 2 × 10 - 5 | 2 . 62 × 10 9 | 10             | 8 . 9 |
| m = 250 | RMLMC          | 1 × 10 9 | 0 . 36284 | 6 . 3 × 10 - 5 | 1 . 42 × 10 9 | 5 . 6          | 34    |
|         | MLMC           | 4 × 10 5 | 0 . 36291 | 4 . 4 × 10 - 5 | 2 . 17 × 10 9 | 4 . 1          | 46    |
|         | RMLMC-Milstein | 1 × 10 9 | 0 . 36291 | 6 . 3 × 10 - 5 | 2 . 62 × 10 9 | 11             | 18    |
| m = 500 | RMLMC          | 1 × 10 9 | 0 . 3627  | 6 . 3 × 10 - 5 | 1 . 42 × 10 9 | 5 . 7          | 61    |
|         | MLMC           | 2 × 10 5 | 0 . 36275 | 4 . 4 × 10 - 5 | 2 . 13 × 10 9 | 4 . 2          | 83    |
|         | RMLMC-Milstein | 1 × 10 9 | 0 . 36276 | 6 . 4 × 10 - 5 | 2 . 63 × 10 9 | 11             | 32    |

Table 3: Randomized multilevel Monte Carlo pricing of Asian calls in the Black-Scholes model

2

|                | m    | n    | Price     | Std            | Cost          | Cost × Std   |
|----------------|------|------|-----------|----------------|---------------|--------------|
| Average price  | 10 7 | 10 9 | 0 . 35014 | 4 . 8 × 10 - 5 | 2 . 21 × 10 9 | 5 . 1        |
| Average strike | 10 7 | 10 9 | 0 . 36252 | 6 . 5 × 10 - 5 | 1 . 43 × 10 9 | 6            |

The strike of the average price call is K = 2.

Table 4: Pricing average price calls in Merton's jump-diffusion model with K = 2

|         |       | n        | Price     | Std            | Cost          | Cost × Std 2   |   VRF |
|---------|-------|----------|-----------|----------------|---------------|----------------|-------|
| m = 125 | RMLMC | 1 × 10 9 | 0 . 19306 | 1 . 6 × 10 - 5 | 2 . 1 × 10 9  | 0 . 53         |    13 |
|         | MLMC  | 8 × 10 5 | 0 . 19309 | 1 . 6 × 10 - 5 | 2 . 16 × 10 9 | 0 . 53         |    13 |
| m = 250 | RMLMC | 1 × 10 9 | 0 . 1924  | 1 . 6 × 10 - 5 | 2 . 13 × 10 9 | 0 . 55         |    26 |
|         | MLMC  | 4 × 10 5 | 0 . 19242 | 1 . 6 × 10 - 5 | 2 . 2 × 10 9  | 0 . 56         |    25 |
| m = 500 | RMLMC | 1 × 10 9 | 0 . 19206 | 1 . 6 × 10 - 5 | 2 . 15 × 10 9 | 0 . 56         |    50 |
|         | MLMC  | 2 × 10 5 | 0 . 19208 | 1 . 6 × 10 - 5 | 2 . 21 × 10 9 | 0 . 57         |    49 |

Table 5: Pricing average strike calls in Merton's jump-diffusion model

|         |       | n        | Price     | Std            | Cost          | Cost × Std 2   |   VRF |
|---------|-------|----------|-----------|----------------|---------------|----------------|-------|
| m = 125 | RMLMC | 1 × 10 9 | 0 . 20107 | 2 . 2 × 10 - 5 | 1 . 42 × 10 9 | 0 . 69         |    13 |
|         | MLMC  | 8 × 10 5 | 0 . 20109 | 1 . 5 × 10 - 5 | 2 . 14 × 10 9 | 0 . 49         |    19 |
| m = 250 | RMLMC | 1 × 10 9 | 0 . 20096 | 2 . 2 × 10 - 5 | 1 . 42 × 10 9 | 0 . 71         |    25 |
|         | MLMC  | 4 × 10 5 | 0 . 20097 | 1 . 5 × 10 - 5 | 2 . 18 × 10 9 | 0 . 51         |    35 |
| m = 500 | RMLMC | 1 × 10 9 | 0 . 20088 | 2 . 3 × 10 - 5 | 1 . 42 × 10 9 | 0 . 72         |    49 |
|         | MLMC  | 2 × 10 5 | 0 . 20087 | 1 . 6 × 10 - 5 | 2 . 13 × 10 9 | 0 . 51         |    69 |

Table 6: Pricing average price calls with strike K = 2 in the Square-Root diffusion model

|         |       | n        | Price     | Std            | Cost          | Cost × Std 2   |   VRF |
|---------|-------|----------|-----------|----------------|---------------|----------------|-------|
| m = 125 | RMLMC | 1 × 10 9 | 0 . 21837 | 2 . 0 × 10 - 5 | 2 . 1 × 10 9  | 0 . 82         |    13 |
|         | MLMC  | 8 × 10 5 | 0 . 21839 | 2 . 0 × 10 - 5 | 2 . 16 × 10 9 | 0 . 83         |    13 |
| m = 250 | RMLMC | 1 × 10 9 | 0 . 21762 | 2 . 0 × 10 - 5 | 2 . 13 × 10 9 | 0 . 85         |    26 |
|         | MLMC  | 4 × 10 5 | 0 . 21763 | 2 . 0 × 10 - 5 | 2 . 21 × 10 9 | 0 . 87         |    25 |
| m = 500 | RMLMC | 1 × 10 9 | 0 . 21726 | 2 . 0 × 10 - 5 | 2 . 15 × 10 9 | 0 . 87         |    50 |
|         | MLMC  | 2 × 10 5 | 0 . 21728 | 2 . 0 × 10 - 5 | 2 . 22 × 10 9 | 0 . 9          |    49 |

Table 7: Pricing average strike calls in the Square-Root diffusion model

|         |       | n        | Price     | Std            | Cost          | Cost × Std 2   |   VRF |
|---------|-------|----------|-----------|----------------|---------------|----------------|-------|
| m = 125 | RMLMC | 1 × 10 9 | 0 . 2251  | 2 . 9 × 10 - 5 | 1 . 42 × 10 9 | 1 . 2          |    11 |
|         | MLMC  | 8 × 10 5 | 0 . 22505 | 2 . 0 × 10 - 5 | 2 . 15 × 10 9 | 0 . 82         |    16 |
| m = 250 | RMLMC | 1 × 10 9 | 0 . 22495 | 2 . 9 × 10 - 5 | 1 . 42 × 10 9 | 1 . 2          |    21 |
|         | MLMC  | 4 × 10 5 | 0 . 22485 | 2 . 0 × 10 - 5 | 2 . 2 × 10 9  | 0 . 86         |    30 |
| m = 500 | RMLMC | 1 × 10 9 | 0 . 22484 | 3 . 0 × 10 - 5 | 1 . 42 × 10 9 | 1 . 3          |    40 |
|         | MLMC  | 2 × 10 5 | 0 . 22483 | 2 . 0 × 10 - 5 | 2 . 15 × 10 9 | 0 . 87         |    59 |


<!-- p:13 -->


## A Proof of Proposition 2.1

Since ( x + x ′ ) 2 ≤ 2( x 2 + x ′ 2 ) for any real numbers x and x ′ , if X and X ′ are square-integrable random variables,

$$| | X + X ^ { \prime } | | ^ { 2 } & \leq 2 ( | | X | | ^ { 2 } + | | X ^ { \prime } | | ^ { 2 } ) . & & ( A . 1 ) \\ ( A _ { 1 } ) _ { 2 } & \div ( A _ { 2 } - V _ { 2 } ) ( X ^ { \prime } - V _ { 2 } ) ( X ^ { \prime } - V _ { 2 } ) .$$

For l ≥ 1, by applying (A.1) with X = Y l - Y and X ′ = Y l - 1 - Y , it follows that

$$| | Y _ { l } - Y _ { l - 1 } | | ^ { 2 } \leq 2 ( | | Y _ { l } - Y | | ^ { 2 } + | | Y _ { l - 1 } - Y | | ^ { 2 } ) .$$

Since || Y l - 1 - Y || 2 ≤ 4 ν 2 - βl by (2.2), it follows that from (A.2) that

$$| | Y _ { l } - Y _ { l - 1 } | | ^ { 2 } \leq 1 0 \nu 2 ^ { - \beta l } .$$

As || Y 0 || 2 ≤ ν , (A.3) holds also for l = 0. Thus, as p l ≥ 2 - 1 - ( β +1) l/ 2 ,

$$\sum _ { l = 0 } ^ { \infty } \frac { | | Y _ { l } - Y _ { l - 1 } | | ^ { 2 } } { p _ { l } } & \ \leq \ 2 0 \nu \sum _ { l = 0 } ^ { \infty } 2 ^ { - ( \beta - 1 ) l / 2 } \\ & = \ \frac { 2 0 \nu } { 1 - 2 ^ { - ( \beta - 1 ) / 2 } } . \\ \intertext { c o n c l u d e t h a t $ Z $ i s s u r a g e - i n t e g r a b l e w i t h $ E ( Z ) = E $ }$$

By Theorem 2.1, we conclude that Z is square-integrable with E ( Z ) = E ( Y ), and that (2.4) holds.

We now prove (2.5). As observed in (Rhee and Glynn 2015), C = ∑ ∞ l =0 p l C l . Since p l ≤ 2 - ( β +1) l/ 2 ,

which concludes the proof.

## B Proof of Proposition 2.2

We apply Theorem 2.1 to the sequence ( Y min( l,L ) : l ≥ 0) and Y L . Thus Z = Z L , and so Z L is square-integrable, E ( Z L ) = E ( Y L ), and

$$\| Z _ { L } \| ^ { 2 } = \sum _ { l = 0 } ^ { L } \frac { | | Y _ { l } - Y _ { l - 1 } | | ^ { 2 } } { p _ { l } } .$$

$$\begin{array} { r c l } ( E ( Z _ { L } - Y ) ) ^ { 2 } & = & ( E ( Y _ { L } - Y ) ) ^ { 2 } \\ & & \leq & | | Y _ { L } - Y | | ^ { 2 } , \end{array}$$

which yields (2.7). On the other hand, for l ≥ 1, as || Y l - 1 - Y || 2 ≤ 2 ν 2 - l by (2.6), it follows from (A.2) that

$$| | Y _ { l } - Y _ { l - 1 } | | ^ { 2 } & \leq 6 \nu 2 ^ { - l } . \\ \\$$

Since || Y 0 || 2 ≤ ν , (B.1) also holds for l = 0. Hence,

$$\sum _ { l = 0 } ^ { L } \frac { | | Y _ { l } - Y _ { l - 1 } | | ^ { 2 } } { p _ { l } } \leq 1 2 \nu ( L + 1 ) ,$$

which implies (2.8). Finally, the expected cost of computing Z L is ∑ L l =0 p l C l , which is upperbounded by cL since p l C l ≤ c/ 2.

曰

$$C \leq c \sum _ { l = 0 } ^ { \infty } 2 ^ { - ( \beta - 1 ) l / 2 } ,$$

Hence


<!-- p:14 -->


## C Proof of Proposition 3.1

We first show (3.2). As this equation clearly holds for l ≥ L , we assume that 0 ≤ l ≤ L - 1. Let j and j ′ be two elements of J l , with j &lt; j ′ . As j ≤ j ′ - 1,

$$\begin{array} { r l } { \lfloor 2 ^ { l } W ^ { \prime } ( 1 , j ) \rfloor } & { \leq } & { \lfloor 2 ^ { l } W ^ { \prime } ( 1 , j ^ { \prime } - 1 ) \rfloor } \\ & { \leq } & { 2 ^ { l } W ^ { \prime } ( 1 , j ^ { \prime } - 1 ) } \\ & { < } & { \lfloor 2 ^ { l } W ^ { \prime } ( 1 , j ^ { \prime } ) \rfloor , } \end{array}$$

where the last equation follows from (3.1). Thus the map j ↦→⌊ 2 l W ′ (1 , j ) ⌋ from J l to { 0 , . . . , 2 l } is strictly increasing. This implies (3.2).

We now show (3.3). As this relation is obvious when l ≥ L - 1, assume that 0 ≤ l ≤ L - 2. Since 2 ⌊ x ⌋ ≤ ⌊ 2 x ⌋ for x ∈ R , for any an element j of J l ,

$$2 ^ { l + 1 } W ^ { \prime } ( 1 , j - 1 ) < 2 \lfloor 2 ^ { l } W ^ { \prime } ( 1 , j ) \rfloor \leq \lfloor 2 ^ { l + 1 } W ^ { \prime } ( 1 , j ) \rfloor ,$$

where the first equation follows from (3.1). Thus, j ∈ J l +1 . This implies (3.3).

## D Proof of Theorem 3.1

Proposition D.1 below proves standard properties of square-integrable martingales.

Proposition D.1. For 0 ≤ i ≤ j ≤ k ≤ m ,

$$E ( F _ { i } ( F _ { k } - F _ { j } ) ) = 0 ,$$

$$| | F _ { i } | | \leq | | F _ { j } | | .$$

$$| | F _ { j } - F _ { i } | | ^ { 2 } \leq | | F _ { k } | | ^ { 2 } - | | F _ { i } | | ^ { 2 } .$$

Proof. Let F = ( F i ), 0 ≤ i ≤ m , be the natural filtration of the random process ( F i ), 0 ≤ i ≤ m . By the tower law,

$$\begin{array} { r l r } { E ( F _ { i } ( F _ { k } - F _ { j } ) ) } & { = } & { E ( E ( F _ { i } ( F _ { k } - F _ { j } ) | \mathcal { F } _ { j } ) ) } \\ & { = } & { E ( F _ { i } E ( F _ { k } - F _ { j } | \mathcal { F } _ { j } ) ) } \\ & { = } & { 0 . } \end{array}$$

The last equation follows from the fact that ( F i ), 0 ≤ i ≤ m , is a martingale with respect to F . This implies (D.1). In particular, E ( F i ( F j - F i )) = 0. As F j = ( F j - F i ) + F i ,

$$| | F _ { j } | | ^ { 2 } = | | F _ { j } - F _ { i } | | ^ { 2 } + | | F _ { i } | | ^ { 2 } ,$$

which proves (D.2). The inequality || F j || ≤ || F k || then implies (D.3).

We next prove the following proposition.

Proposition D.2. For l ≥ 0 , if ( i, k ) ∈ P l then W ′ ( i +1 , k - 1) ≤ 2 - l .

Proof. The desired inequality clearly holds if k = i +1. Assume that k &gt; i +1. Thus l ≤ L - 1. For any integer j in [ i +1 , k - 1], since j / ∈ J l , we have 2 l W ′ (1 , j - 1) ≥ ⌊ 2 l W ′ (1 , j ) ⌋ , and so

$$\lfloor 2 ^ { l } W ^ { \prime } ( 1 , j - 1 ) \rfloor = \lfloor 2 ^ { l } W ^ { \prime } ( 1 , j ) \rfloor .$$

and

Moreover, Hence Rewriting (3.5) as and noting that it follows that


<!-- p:15 -->


$$2 ^ { l } W ^ { \prime } ( 1 , k - 1 ) - 1 & \ \leq \ \lfloor 2 ^ { l } W ^ { \prime } ( 1 , k - 1 ) \rfloor \\ & = \ \lfloor 2 ^ { l } W ^ { \prime } ( 1 , i ) \rfloor \\ & \leq \ 2 ^ { l } W ^ { \prime } ( 1 , i ) . \\$$

The second equation follows from (D.4). As W ′ ( i + 1 , k - 1) = W ′ (1 , k - 1) - W ′ (1 , i ), this completes the proof.

We now prove Theorem 3.1. By (3.5) and the relation J 0 = { m } ,

$$A _ { 0 } = w _ { m } F _ { m } + \frac { 1 } { 2 } W ( 1 , m - 1 ) ( F _ { 0 } + F _ { m } ) .$$

As W (1 , m ) = W (1 , m - 1) + w m , it follows that

$$A _ { 0 } - W ( 1 , m ) F _ { 0 } = ( \frac { 1 } { 2 } W ( 1 , m - 1 ) + w _ { m } ) ( F _ { m } - F _ { 0 } ) ,$$

and so || A 0 - W (1 , m ) F 0 || ≤ || F m - F 0 || . As E ( F m ) = F 0 , this implies the desired bound on || A 0 - W (1 , m ) F 0 || 2 .

Fix now l ≥ 0. For ( i, k ) ∈ P l , let

$$B _ { i } = \sum _ { j = i + 1 } ^ { k - 1 } w _ { j } ( F _ { j } - F _ { i } ) \text { and } B _ { i } ^ { \prime } = \sum _ { j = i + 1 } ^ { k - 1 } w _ { j } ( F _ { j } - F _ { k } ) .$$

$$A _ { l } = \sum _ { j \in J _ { l } } w _ { j } F _ { j } + \frac { 1 } { 2 } \sum _ { ( i , k ) \in \mathcal { P } _ { l } } \sum _ { j = i + 1 } ^ { k - 1 } w _ { j } ( F _ { i } + F _ { k } ) ,$$

$$A = \sum _ { j \in J _ { l } } w _ { j } F _ { j } + \sum _ { ( i , k ) \in \mathcal { P } _ { l } } \sum _ { j = i + 1 } ^ { k - 1 } w _ { j } F _ { j } ,$$

$$A - A _ { l } = \frac { 1 } { 2 } \sum _ { ( i , k ) \in \mathcal { P } _ { l } } ( B _ { i } + B _ { i } ^ { \prime } ) .$$

Hence, by the triangular inequality,

$$\| A - A _ { l } \| \leq \frac { 1 } { 2 } | | \sum _ { ( i , k ) \in \mathcal { P } _ { l } } B _ { i } | | + \frac { 1 } { 2 } | | \sum _ { ( i , k ) \in \mathcal { P } _ { l } } B _ { i } ^ { \prime } | | .$$

We bound each of the two terms in the RHS of (D.5) separately. First observe that if ( i, k ) and ( i ′ , k ′ ) are two distinct elements of P l with i &lt; i ′ , then

$$E ( B _ { i } B _ { i ^ { \prime } } ) \ & = \ \sum _ { j = i + 1 } ^ { k - 1 } \sum _ { j ^ { \prime } = i ^ { \prime } + 1 } ^ { k ^ { \prime } - 1 } w _ { j } w _ { j ^ { \prime } } E ( ( F _ { j } - F _ { i } ) ( F _ { j ^ { \prime } } - F _ { i ^ { \prime } } ) ) \\ & = \ 0 ,$$

where the second equation follows from (D.1). Thus

$$| | \sum _ { ( i , k ) \in \mathcal { P } _ { l } } B _ { i } | | ^ { 2 } = \sum _ { ( i , k ) \in \mathcal { P } _ { l } } | | B _ { i } | | ^ { 2 } ,$$


<!-- p:16 -->


On the other hand, for ( i, k ) ∈ P l , by the triangular inequality,

$$| | B _ { i } | | & \leq \sum _ { j = i + 1 } ^ { k - 1 } | w _ { j } | | | F _ { j } - F _ { i } | | \\ & \leq \ W ^ { \prime } ( i + 1 , k - 1 ) \sqrt { | | F _ { k } | | ^ { 2 } - | | F _ { i } | | ^ { 2 } } , \\ \text {equation follows from (D.3).} \ U \text {ing Propositition} \ D . 2 , \, i t \, f o l o l$$

where the second equation follows from (D.3). Using Proposition D.2, it follows that

$$\sum _ { ( i , k ) \in \mathcal { P } _ { l } } | | B _ { i } | | ^ { 2 } & \ \leq \ 2 ^ { - 2 l } \sum _ { ( i , k ) \in \mathcal { P } _ { l } } ( | | F _ { k } | | ^ { 2 } - | | F _ { i } | | ^ { 2 } ) \\ & = \ 2 ^ { - 2 l } ( | | F _ { m } | | ^ { 2 } - | | F _ { 0 } | | ^ { 2 } ) \\ & = \ 2 ^ { - 2 l } \text {Var} ( F _ { m } ) .$$

$$\| \sum _ { ( i , k ) \in \mathcal { P } _ { l } } B _ { i } \| \leq 2 ^ { - l } S t d ( F _ { m } ) .$$

The same upper bound on || ∑ ( i,k ) ∈P l B ′ i || can be shown in a similar way. Hence

This concludes the proof.

## E Proof of Theorem 3.3

The proof is similar to that of Theorem 3.2. As U L = U , the analysis of § 2.2, with Y l = U l for 0 ≤ l ≤ L , shows that E (  ̄ U ) = E ( U ) = E ( f ( A )) - a . This implies (3.12). Let

Since n l ≥  ̄ m √ μ l / | J l | for 0 ≤ l ≤ L , it follows from (2.1) that

$$\bar { m } = \frac { m } { \sum _ { l = 0 } ^ { L } \sqrt { \mu _ { l } | J _ { l } | } } .$$

$$V & ( \bar { U } ) \ \leq \ \bar { m } ^ { - 1 } ( \sum _ { l = 0 } ^ { L } \sqrt { \mu _ { l } | J _ { l } | } ) \\ & = \ \frac { ( \sum _ { l = 0 } ^ { L } \sqrt { \mu _ { l } | J _ { l } | } ) ^ { 2 } } { m } .$$

As μ 0 = Var( U 0 ), by (3.9), we have μ 0 ≤ κ 2 Var( F m ). By arguments similar to those leading to (A.2), for l ≥ 1,

Since || U l - 1 - U || 2 ≤ 4 κ 2 2 - 2 l Var( F m ) by (3.10),

$$| | U _ { l } - U _ { l - 1 } | | ^ { 2 } & \leq 2 ( | | U _ { l } - U | | ^ { 2 } + | | U _ { l - 1 } - U | | ^ { 2 } ) . \\ | | 2 \ < \ 0 \ 2 \sigma = 2 l _ { \Upsilon } \ \ ( \Gamma \ \, ) \, l \quad ( \sigma \, 1 0 )$$

$$| | U _ { l } - U _ { l - 1 } | | ^ { 2 } & \leq 1 0 \kappa ^ { 2 } 2 ^ { - 2 l } \text {Var} ( F _ { m } ) . \\$$

We conclude that μ l ≤ 10 κ 2 2 - 2 l Var( F m ) for 0 ≤ l ≤ L . Since | J l | ≤ 2 l +1 , it follows from (E.1) that

which implies (3.13).

$$\ m V a r ( \bar { U } ) \leq \frac { 2 0 \kappa ^ { 2 } V a r ( F _ { m } ) } { ( 1 - 2 ^ { - 1 / 2 } ) ^ { 2 } } ,$$

Denote by C l is the expectation of the time to simulate U l - U l - 1 , for 0 ≤ l ≤ L , and let  ̄ C = ∑ L l =0 n l C l be the expected cost of computing  ̄ Y . As in the proof of Theorem 3.2, it can

$$\| A - A _ { l } \| \leq 2 ^ { - l } S t d ( F _ { m } ) .$$

We conclude that

□


<!-- p:17 -->


be shown that there is a constant c ′ independent of m such that C l ≤ c ′ | J l | for 0 ≤ l ≤ L . As n l ≤ 1 +  ̄ m √ μ l / | J l | ,

$$\bar { C } \leq c ^ { \prime } \sum _ { l = 0 } ^ { L } | J _ { l } | + c ^ { \prime } \bar { m } \sum _ { l = 0 } ^ { L } \sqrt { \mu _ { l } | J _ { l } | } .$$

Since | J l | ≤ 2 l +1 for l ≥ 0, it follows that  ̄ C ≤ c ′ 2 L +2 + c ′ m ≤ 9 c ′ m .

## F Proof of Proposition 3.2

By (3.5) and (3.14),

$$\hat { A } _ { l } - A _ { l } = \sum _ { j \in J _ { l } } w _ { j } ( \hat { F } _ { j } ^ { l } - F _ { j } ) + \frac { 1 } { 2 } \sum _ { ( i , k ) \in \mathcal { P } _ { l } } W ( i + 1 , k - 1 ) ( ( \hat { F } _ { i } ^ { l } - F _ { i } ) + ( \hat { F } _ { k } ^ { l } - F _ { k } ) ) .$$

Hence

$$| | \hat { A } _ { l } - A _ { l } | | & \leq \sum _ { j \in J _ { l } } w _ { j } | | \hat { F } _ { j } ^ { l } - F _ { j } | | + \frac { 1 } { 2 } \sum _ { ( i , k ) \in \mathcal { P } _ { l } } W ( i + 1 , k - 1 ) ( | | \hat { F } _ { i } ^ { l } - F _ { i } | | + | | \hat { F } _ { k } ^ { l } - F _ { k } | | ) .$$

As || ˆ F l j - F j || ≤ √ c 2 2 - βl for j ∈ J l and

$$\sum _ { j \in J _ { l } } w _ { j } + \sum _ { ( i , k ) \in \mathcal { P } _ { l } } W ( i + 1 , k - 1 ) = 1 ,$$

it follows that || ˆ A l - A l || ≤ √ c 2 2 - βl . Together with (3.6) and (A.1), this shows that || ˆ A l - A || 2 ≤ c 3 2 - βl . Similarly, as || A 0 - W (1 , m ) F 0 || 2 ≤ Var( F m ), we have || ˆ A 0 - W (1 , m ) F 0 || 2 ≤ c 3 .

## G Proof of Theorem 3.4

The proof is similar to that of Theorem 3.2. By A2 and (3.2), the vector ( ˆ F l - 1 , ˆ F l ) can be simulated in O (2 l ) expected time for l ≥ 1. Hence, by (3.14), there is a constant c ′ independent of m such that, for l ≥ 0, the expectation of the time to simulate ˆ U l - ˆ U l - 1 is at most c ′ 2 l . As | ˆ U 0 | ≤ κ | ˆ A 0 - W (1 , m ) F 0 | , Proposition 3.2 implies that || ˆ U 0 || 2 ≤ c 3 κ 2 , where c 3 is defined as in Proposition 3.2. Similarly, for l ≥ 0, as | ˆ U l - U | ≤ κ | ˆ A l - A | , Proposition 3.2 shows that || ˆ U l - U || 2 ≤ c 3 κ 2 2 - βl . The conditions of Proposition 2.1 are thus met for Y = U and Y l = ˆ U l for l ≥ 0, with ν = c 3 κ 2 and c = c ′ . Thus, ˆ V is square-integrable with E ( ˆ V ) = E ( U ). This implies (3.15). By (2.4),

$$| | \hat { V } | | ^ { 2 } \leq \frac { 2 0 c _ { 3 } \kappa ^ { 2 } } { 1 - 2 ^ { - ( \beta - 1 ) / 2 } } , \\ \text {by a constant independent of}$$

and so Var( ˆ V ) is upper-bounded by a constant independent of m . By (2.5), the expectation of the time to simulate ˆ V is at most c ′ / (1 - 2 - ( β - 1) / 2 ). This completes the proof.

## H Proof of Theorem 3.5

By arguments similar to those used in the proof of Theorem 3.4, there is a constant c ′ independent of m and of ǫ such that the expected cost of computing ˆ U l - ˆ U l - 1 is at most c ′ 2 l for l ≥ 0. Also, || ˆ U 0 || 2 ≤ c 3 κ 2 and, for l ≥ 0,

$$| | \hat { U } _ { l } - U | | ^ { 2 } \leq c _ { 3 } \kappa ^ { 2 } 2 ^ { - l } .$$


<!-- p:18 -->


The conditions of Proposition 2.2 are thus met for Y = U and Y l = ˆ U l for l ≥ 0, with ν = c 3 κ 2 and c = c ′ . By (2.7), ˆ V is square-integrable and ( E ( ˆ V - U )) 2 ≤ c 3 κ 2 ǫ 2 . This implies (3.16). Similarly, (2.8) implies that

Furthermore, the expectation of the time required to simulate ˆ V is at most 4 c ′ log 2 (1 /ǫ ).

$$V a r ( \hat { V } ) & \leq 4 8 c _ { 3 } \kappa ^ { 2 } \log _ { 2 } ( 1 / \epsilon ) . \\ c _ { 1 } + \cdot \cdot \cdot & \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad \cdot \quad 1 + \cdot \quad \cdot \quad \hat { V }$$

## I The Euler and Milstein schemes

We show here that A2 holds when the forward price follows a continuous diffusion process satisfying certain regularity conditions. Assume that F ( t ) satisfies the SDE

$$d F ( t ) = b ( F ( t ) , t ) d W ,$$

where b is a real-valued function on R 2 and W is a one-dimensional Brownian motion under Q . For J ⊆ { 1 , . . . , m } , let 0 = τ 0 &lt; τ 1 &lt; · · · &lt; τ n be the elements of the time grid

$$G ( J , l ) = \{ t _ { j } \colon j \in J \} \cup \{ i 2 ^ { - l } T \colon 0 \leq i \leq 2 ^ { l } \} .$$

Note that n ≤ | J | +2 l and the maximum distance δ between two consecutive elements of G ( J, l ) is at most 2 - l T . Using the time grid G ( J, l ), the Euler scheme approximates the forward price path via the sequence  ̃ F =  ̃ F ( J, l ) defined recursively as follows:  ̃ F 0 = F 0 and, for 0 ≤ k ≤ n - 1,

$$\tilde { F } _ { k + 1 } = \tilde { F } _ { k } + b ( \tilde { F } _ { k } , \tau _ { k } ) ( \Delta W ) ,$$

where ∆ W = W ( τ k +1 ) - W ( τ k ). It follows from (Kloeden and Platen 1992, Theorem 10.6.3) that, under certain regularity conditions on b ,

$$E ( \max _ { 0 \leq k \leq n } ( \tilde { F } _ { k } - F ( \tau _ { k } ) ) ^ { 2 } ) \leq K _ { 1 } \delta ,$$

where K 1 is a constant that does not depend on δ . Define ˆ F = ˆ F ( J, l ) ∈ R J as follows. For j ∈ J , set ˆ F j =  ̃ F k . where k is the index such that τ k = t j . In other words, ˆ F is the 'restriction' of  ̃ F to the dates corresponding to J . It follows from (I.2) that || ˆ F j - F j || 2 ≤ K 1 2 - l T for j ∈ J . Furthermore, for l ≥ 1 and J ′ ⊆ J ⊆ { 1 , . . . , m } , the grid G ( J ′ , l - 1) is contained in G ( J, l ). The vector ( ˆ F ( J ′ , l - 1) , ˆ F ( J, l )) can thus be simulated in at most c 1 ( | J | +2 l ) time, where c 1 is a constant independent of m , by first simulating W on the elements of G ( J, l ) and then using the same W to calculate recursively  ̃ F ( J, l ) and  ̃ F ( J ′ , l - 1) via (I.1). Thus A2 holds for these processes with β = 1 for the Euler scheme.

Similarly, under regularity conditions on b , we can calculate ˆ F ( J, l ) by computing the sequence F ∗ = F ∗ ( J, l ) via the Milstein scheme

$$F _ { k + 1 } ^ { * } = F _ { k } ^ { * } + b ( F _ { k } ^ { * } , \tau _ { k } ) ( \Delta W ) + \frac { 1 } { 2 } b ( F _ { k } ^ { * } , \tau _ { k } ) b ^ { \prime } ( F _ { k } ^ { * } , \tau _ { k } ) ( ( \Delta W ) ^ { 2 } - ( \tau _ { k + 1 } - \tau _ { k } ) ) ,$$

where b ′ is the partial derivative of b with respect to its first argument. It follows from (Kloeden and Platen 1992, Theorem 10.6.3) that, under certain regularity conditions on b ,

$$E ( \max _ { 0 \leq k \leq n } ( F _ { k } ^ { * } - F ( \tau _ { k } ) ) ^ { 2 } ) \leq K _ { 2 } \delta ^ { 2 } ,$$

where K 2 does not depend on δ . By arguments similar to those used in the Euler scheme analysis, we conclude that A2 holds for the Milstein scheme with β = 2 for scalar continuous processes satisfying certain regularity conditions. A straightforward generalization of the preceding arguments shows that A2 holds for the Euler scheme with β = 1 for multi-dimensional continuous processes satisfying certain regularity conditions.


<!-- p:19 -->


## J Simulation of Square-Root diffusions

Proposition J.1 below shows how to sample F ( t ), for t ∈ [0 , T ]. Proposition J.1 and its proof are inspired from the analysis of the Cox-Ingersoll-Ross process in (Glasserman 2004, § 3.4.1).

Proposition J.1. Let N be a Poisson random variable with mean 2 F 0 / ( σ 2 t ) . For integer k ≥ 1 , let χ 2 k be a Chi-Square random variable with k degrees of freedom independent of N , and let χ 2 0 = 0 . Then F ( t ) has the same distribution as ( σ 2 t/ 4) χ 2 2 N . Furthermore, F ( t ) is square-integrable.

Proof. For t ∈ [0 , T ], let X ( t ) = 4 F ( t ) /σ 2 , and let x = X (0). Then

$$X ( t ) = x + 2 \int _ { 0 } ^ { t } \sqrt { X ( s ) } \, d W ( s ) . \\ \intertext { d } R a v e l _ { m a n g h s c r f i d i m u n i o n } \, 0 \, \ S h s c r { o } _ { m a n g h s c r f i d i m u n i o n } \, ( J o r k h s c r { l } ) .$$

Hence X is a squared Bessel process of dimension 0. Such a process is a martingale (Jeanblanc, Yor and Chesney 2009, p. 339), and so ∫ t 0 X ( s ) ds has finite expectation. By (J.1) and the isometry of stochastic integrals (Jeanblanc, Yor and Chesney 2009, § 1.5.1), it follows that X ( t ) is square-integrable. By (Jeanblanc, Yor and Chesney 2009, p. 344), for t &gt; 0, we have Pr( X ( t ) = 0) = e - x/ (2 t ) and X ( t ) has density

$$q _ { t } ( x , y ) & = \frac { 1 } { 2 t } \sqrt { \frac { x } { y } } \exp ( - \frac { x + y } { 2 t } ) I _ { 1 } ( \frac { \sqrt { x y } } { t } )$$

at y &gt; 0, where I 1 is the modified Bessel function with index 1 defined for z &gt; 0 by

$$I _ { 1 } ( z ) = \sum _ { k = 0 } ^ { \infty } \frac { ( z / 2 ) ^ { 2 k + 1 } } { k ! ( k + 1 ) ! } .$$

$$\Pr ( \chi _ { 2 k } ^ { 2 } \geq y ) = \frac { 1 } { 2 } \int _ { y } ^ { \infty } e ^ { - z / 2 } \frac { ( z / 2 ) ^ { k - 1 } } { ( k - 1 ) ! } \, d z .$$

$$\Pr ( t \chi _ { 2 k } ^ { 2 } \geq y ) & = \frac { 1 } { 2 t } \int _ { y } ^ { \infty } \exp ( - \frac { z } { 2 t } ) ( \frac { z } { 2 t } ) ^ { k - 1 } \frac { 1 } { ( k - 1 ) ! } \, d z . \\ = x / ( 2 t ) , \, \text {we have}$$

For y &gt; 0 and k ≥ 1,

Thus,

Since E ( N ) = x/ (2 t ), we have

$$\Pr ( N = k ) = \exp ( - \frac { x } { 2 t } ) ( \frac { x } { 2 t } ) ^ { k } \frac { 1 } { k ! } ,$$

and so

$$\text {and so} \\ \Pr ( t \chi _ { 2 N } ^ { 2 } \geq y ) \ & = \ \sum _ { k = 1 } ^ { \infty } \Pr ( N = k ) \Pr ( t \chi _ { 2 k } ^ { 2 } \geq y ) \\ & = \ \frac { 1 } { 2 t } \int _ { y } ^ { \infty } \exp ( - \frac { x + z } { 2 t } ) \sum _ { k = 1 } ^ { \infty } ( \frac { x } { 2 t } ) ^ { k } ( \frac { z } { 2 t } ) ^ { k - 1 } \frac { 1 } { ( k - 1 ) ^ { k } ! n ! } \, d z \\ & = \ \int _ { y } ^ { \infty } q _ { t } ( x , z ) \, d z \\ & = \ \Pr ( X ( t ) \geq y ) . \\ \text {Thus, } X ( t ) \, \text { has the same distribution as } t \chi _ { 2 N } ^ { 2 } \text { . This concluades the proof.}$$

Thus, X ( t ) has the same distribution as tχ 2 2 N . This concludes the proof.

Consider now a time grid G consisting of n +1 dates 0 = τ 0 &lt; τ 1 &lt; · · · &lt; τ n . We can use Proposition J.1 to recursively sample F ( τ k ) for 1 ≤ k ≤ n , and thereby simulate the forward price process on G in O ( n ) expected time. Algorithms that simulate in unit expected time Poisson and Chi-Square random variables are given in (Devroye 1986). In our experiments, though, we have used generators from the standard C++ library.


<!-- p:20 -->


Table 8: Variance reduction factors for average price calls in the Black-Scholes model

| K       |                | 1 . 6   | 1 . 8   | 2     | 2 . 2   |   2 . 4 |
|---------|----------------|---------|---------|-------|---------|---------|
| m = 125 | RMLMC          | 13      | 13      | 12    | 11      |      11 |
|         | MLMC           | 13      | 12      | 12    | 11      |      10 |
|         | RMLMC-Milstein | 8 . 9   | 8 . 7   | 8 . 4 | 8 . 2   |       8 |
| m = 250 | RMLMC          | 26      | 25      | 23    | 22      |      21 |
|         | MLMC           | 25      | 24      | 22    | 22      |      22 |
|         | RMLMC-Milstein | 17      | 17      | 17    | 16      |      16 |
| m = 500 | RMLMC          | 49      | 47      | 45    | 43      |      41 |
|         | MLMC           | 49      | 44      | 44    | 43      |      39 |
|         | RMLMC-Milstein | 34      | 33      | 32    | 31      |      30 |

n = 10 7 for the RMLMC and RMLMC-Milstein algorithms and n = 10 6 /m for the MLMC algorithm.

Table 9: Randomized Multilevel Monte Carlo pricing of Asian calls in Merton's jump-diffusion model

|                | Price     | Std            | Cost          | Cost × Std 2   |
|----------------|-----------|----------------|---------------|----------------|
| Average price  | 0 . 19173 | 1 . 6 × 10 - 5 | 2 . 21 × 10 9 | 0 . 6          |
| Average strike | 0 . 20082 | 2 . 3 × 10 - 5 | 1 . 42 × 10 9 | 0 . 75         |

m = 10 7 and n = 10 9 . The strike of the average price call is K = 2.

## K Further numerical experiments

We report here additional numerical experiments for the Black-Scholes model, Merton's jumpdiffusion model, and the Square-Root diffusion model, using the same model parameters as in § 5.

### K.1 The Black-Scholes model

Table 8 gives VRFs for average price calls with different strikes for the RMLMC, MLMC and RMLMC-Milstein algorithms, with S 0 = 2, σ = 50%, r = 5%, and T = 2. For each strike, the VRFs are proportional to m for the three algorithms. The RMLMC and MLMC methods have a similar performance, and slightly outperform the RMLMC-Milstein algorithm.

### K.2 Merton's jump-diffusion model

Table 9 gives prices of average price and average strike calls when m = 10 7 using the RMLMC algorithm, with S 0 = 2, σ = 17 . 65%, r = 5 . 59%, q = 1 . 14%, λ = 8 . 90%, β = - 88 . 98%, γ = 45 . 05%, and T = 2.

### K.3 The Square-Root diffusion model

Table 10 gives prices of average price and average strike calls when m = 10 7 using the RMLMC algorithm, with S 0 = 2, r = 5%, σ = 0 . 4, and T = 2.

Table 10: Randomized multilevel Monte Carlo pricing of Asian calls in the Square-Root diffusion model

|                | Price     | Std            | Cost          | Cost × Std 2   |
|----------------|-----------|----------------|---------------|----------------|
| Average price  | 0 . 21693 | 2 . 0 × 10 - 5 | 2 . 21 × 10 9 | 0 . 92         |
| Average strike | 0 . 22474 | 3 . 1 × 10 - 5 | 1 . 43 × 10 9 | 1 . 3          |

m = 10 7 and n = 10 9 . The strike of the average price call is K = 2.


<!-- p:21 -->
