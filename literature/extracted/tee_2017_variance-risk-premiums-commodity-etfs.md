---
id: "tee_2017_variance-risk-premiums-commodity-etfs"
source_pdf: "../pdf/tee_2017_variance-risk-premiums-commodity-etfs.pdf"
source_filename: "tee_2017_variance-risk-premiums-commodity-etfs.pdf"
format: "academic-paper"
extraction_profile: "text-math-tables-high-fidelity"
extraction_mode: "hybrid"
extraction_quality: "excellent"
extraction_score: 108.0
visual_assets: "disabled"
references_file: "../references/tee_2017_variance-risk-premiums-commodity-etfs.references.md"
---

<!-- p:1 -->

### Variance Risk Premiums of Commodity ETFs

Chyng Wen Tee ∗† , Christopher Ting ∗

###### Abstract

Investments in commodities have grown over the years despite volatile market conditions. We formulate a model-free method to construct volatility indexes to facilitate trading and hedging of volatility risk. A key contribution of this paper is in using a model-independent method (based solely on no-arbitrage principle) to account for the early exercise premiums in American options on non-dividend paying stocks. We find that our estimates of early exercise premium are generally larger than the estimates by the binomial tree model and the Barone-Adesi and Whaley (1987) approximation. Applying our method to American options on the ETFs of gold, silver, natural gas, and crude oil, we find strong empirical evidence of variance risk premiums for these four important commodities, over a volatility term structure up to 18 months. Furthermore, we show that volatility indexes constructed by using existing methods tend to overestimate the risk-neutral variance, and consequently the magnitude of variance risk premium.

Keywords: variance risk, risk premiums, commodity markets, ETF, model-free volatility

∗

Lee Kong Chian School of Business, Singapore Management University, 50 Stamford Road #05-01, Singapore

178899.

† Corresponding author, email: cwtee@smu.edu.sg . Tel: +65 6828 0819


<!-- p:2 -->


## 1 Introduction

Volatility is a widely-used gauge in the financial market to convey information about the extent of fluctuation in the asset return. Even when the underlying asset prices remain largely unchanged, option prices can increase whenever market participants perceive future volatility to rise, and vice versa. In this sense, option traders are short-term volatility forecasters, supplying the market with their views on the expected volatility for the period from the current business day up to the option expiry date. Volatility can also be viewed as a market risk indicator, since stock return and the return's volatility are known to be negatively correlated (see Black 1976). In addition, investors' and traders' fear of a market crash is reflected in their willingness to insure against volatility risk, which in turn is manifested in the observed variance risk premiums (see Aït-Sahalia, Karaman and Mancini 2013).

A significant development in volatility estimation is the model-free approach. Instead of explicitly using an option pricing formula, the model-free method pioneered by Carr and Madan (1998), Derman et al. (1999), and Bakshi and Madan (2000) does not require an option pricing model to be explicitly specified. Different approaches to the derivation of the model-free method and its application in the equity market have been further expounded by Britten-Jones and Neuberger (2000), Carr and Wu (2006), Carr and Wu (2009), and Andersen and Bondarenko (2007), to name a few. The main advantage of the model-free method is that it is unaffected by model risks, since it relies solely on the general principle of no risk-free arbitrage profit opportunity. Jiang and Tian (2005) show that the model-free volatility subsumes all information contained in the Black-Scholes implied volatility.

With the creation of the CBOE VIX index (see CBOE (2009)) and the subsequent successful introductions of volatility derivatives, taking a direct exposure in volatility as an asset class has become more prevalent. This is an important development, as Szado (2009) has shown that although a long position in volatility may result in negative returns in the long term, it may nevertheless provide significant protection during downturns. In a similar vein, Black (2006) and Dash and Moran (2005) argue that due to the negative correlation between VIX and S&amp;P 500


<!-- p:3 -->


index, adding a small VIX position to an investment portfolio can significantly reduce portfolio volatility.

The 2007-2009 crisis has highlighted the need for market indicators to measure the risk aversion of market participants across different asset classes. It has also become increasingly clear that changes in risk appetites are an important determinant of asset prices. Indeed, the model-free volatility methodology has been applied to commodities. For instance, the presence of variance risk premiums in commodity markets has been studied for crude oil and natural gas (see Trolle and Schwartz (2010)), and corn (see Wang, Fausti and Qasmi (2011)). Pan and Kang (2011) analyze the variance risk premium and related issues in the energy market. Kang and Pan (2015) use a mean-variance model with stochastic variance in commodity market to show the negative relationship between the variance risk premium and expected commodity futures return.

Notably, Prokopczuk and Wese Simen (2013) perform an empirical analysis on the variance risk premiums for 21 commodities over more than two decades, demonstrating that a portfolio of short commodity variance swaps significantly outperforms that of long commodity futures. In Prokopczuk and Wese Simen (2014), the model-free volatility methodology is the main tool used to analyze the variance risk premium in the commodity market. They find compelling evidence that the model-free method outperforms other models in terms of minimizing bias. An important observation is that accounting for the variance risk premium results in superior volatility forecasting performance.

The ability to transact financial products based on volatility indexes will enable investors to not only manage volatility risk but also trade volatility spreads, as discussed in Bakshi and Madan (2006), and also in Carr and Lee (2009). Whaley (1993) argues that volatility derivatives are useful in providing a simple, cost-effective means to hedge the volatility of portfolios that contain options or securities with option-like features for any type of asset class.

The rapid expansion in the commodity market, along with the increased participation by hedge funds, has drastically increased volatility in this asset class (see, for instance, Brooks, Prokopczuk and Wu (2015)). Heightened risks in the gold and crude oil markets put the spotlight on the need for more effective tools to manage volatilities, or to seize the alpha-generating opportunities presented by those big swings. Following the research papers reviewed earlier, we formulate a model-free approach to construct the volatility indexes for the commodity ETFs, as the current studies of variance risk premiums in commodity markets tend to use futures on options for empirical analysis.


<!-- p:4 -->


A key problem that impedes the direct application of the model-free approach is the need to adjust for the early exercise premiums in the American options, since the method is only applicable to European options. This adjustment is typically performed by applying an option pricing model, which inevitably introduces model dependency and risk to an otherwise model-free approach. For instance, commonly used methods to adjust for early exercise premiums include the binomial tree model (see Cox, Ross and Rubinstein (1979)) and an analytical approximation method (see Barone-Adesi and Whaley (1987)), both of which are related to or based on the Black-Scholes option pricing model (Black and Scholes (1973)).

One may wonder whether the early exercise premium matters at all, since the options needed for the calculation are mostly out of the money. In dollar terms, the early exercise premium of out-of-the-money options should be small, as these option prices themselves are small. A follow-up question is that even if the early exercise premium does matter, will the different methods used to account for early exercise premiums introduce statistically and economically significant bias in the computation of model-free volatility? If the answers to both questions are affirmative, it follows as a consequence that the estimation of variance risk premium will be biased as well.

Motivated by these considerations, we propose a model-independent adjustment method to construct the volatility indexes for four commodity ETFs from their respective American options. The method only relies on the put-call parity to account for the early excise premium. A main finding is that early exercise premium does matter. More importantly, compared to the same benchmark, we find that two model-dependent adjustment methods, which are commonly applied in the industry and in academic research, tend to produce a model-free volatility larger than that with our proposed model-independent adjustment method. Moreover, the upward bias is especially pronounced for long-dated portion of the volatility term structure. This finding has a direct impact on the magnitude of variance risk premium.


<!-- p:5 -->


The paper is organized as follows: Section 2 provides a brief overview of the data used in this work, while Section 3 describes the model-free formulation and how early exercise premiums are handled. Empirical analyses are presented in Section 4, including the profit and loss (P&amp;L) of hypothetical variance swaps. Finally, conclusions are drawn in Section 5.

## 2 Data

The option and security data sets we use are obtained from OptionMetrics' Ivy DB, a database widely used by researchers. Historical daily data for U.S. listed equities and all U.S. listed index and equity options from January 1996 onward are in the database. Included also are the historical zero-coupon interest rate curves, as well as adjustment factors for stock splits and other distributions.

The average option volume, the average number of put and call strike prices per maturity and the average open interest tabulated in Table I are indicative of the option liquidity. Although the start date of option trading differs from one ETF to the other, the sample period for our empirical analysis ends on August 30, 2013, due to data availability.

Commodity ETFs contain important information about the volatility of this asset class (see Padungsaksawasdi and Daigler (2014)). The gold and silver ETFs with ticker symbols GLD and SLV, respectively, are physically backed by gold bullion and silver bars. On the other hand, the crude oil and natural gas ETFs (USO and UNG, respectively), are based on the futures contracts on the respective spot commodities. The United States Oil Fund is an exchange-traded security designed to track changes in crude oil prices. By holding near-term futures contracts and cash, the performance of the USO Fund is intended to reflect the spot price of West Texas Intermediate light sweet crude oil as closely as possible, less the fund expenses. Under the same ETF investment company, the United States Natural Gas Fund (UNG) is designed to track the performance of the spot natural gas delivered at the Henry Hub through its short-term futures, after fund expenses.


<!-- p:6 -->


The market capitalization at the end of the sample period (i.e., August 30, 2013) for SPDR Gold ETF is about 41 billion dollars, and for iShares Silver ETF, it is about 8 billion dollars. For non-physical, leveraged United States Natural Gas and Oil ETFs, their market capitalizations are less than one billion dollars.

Finally, a remark on the sample periods of our data is in order. Compared to options on commodity futures, options on commodity ETFs have a much shorter history. Nevertheless, given the rising popularity of ETFs in general and CBOE's volatility indexes based on commodity ETFs in particular, there are reasons to believe that it is also important to look into the variance risk premiums in commodity ETFs.

## 3 Model-Free Framework

The main constraint of the model-free approach is its applicability to European style options only. Incidentally, options on the underlying equity indexes such as the S&amp;P 500 index, Nasdaq100 index, Euro STOXX 50 index, and Nikkei 225 index, just to name a few, happen to be European style. However, the vast majority (if not all) of the exchange-traded equity and ETF options are American style. For instance, the 'Oil VIX' (OVX), the 'Gold VIX' (GVZ), and the 'Sliver VIX' (VXSLV) are calculated from the American option quotes of the underlying commodity ETFs.

In principle, the early exercise premiums in the American options will bring about an upward bias to the model-free volatility. This bias is undesirable, as overpricing the volatility indexes could hinder the development of a liquid market for the derivatives on commodity volatilities. Therefore, before computing the model-free volatility from American options, it is crucial to adjust for the early exercise premiums. In the following, we propose a put-call parity method to account for the early exercise premiums of American options on non-dividend paying stocks without using an option pricing model.


<!-- p:7 -->


### 3.1 Put-Call Parity and Early Exercise Premiums

Suppose the underlying asset does not pay a dividend from time 0 to time T . Then it is never optimal to exercise American calls C ( X,T ) early. Consequently, the early exercise premiums for American calls are all zero, and C ( X,T ) = c ( X,T ) , where c ( X,T ) is the European call price. For American puts, it is sometimes optimal to exercise early when they are sufficiently in the money, and hence, early exercise premiums are never zero.

By definition, the early exercise premium E ( X,T ) is the difference in price between an American put option P ( X,T ) and an otherwise identical European put option p ( X,T ) . In other words, p ( X,T ) = P ( X,T ) - E ( X,T ) . Given the spot price S 0 and the risk-free interest rate r of tenor T at time 0 , the put-call parity is expressed as

$$c ( X , T ) - \left [ P ( X , T ) - E ( X , T ) \right ] = S _ { 0 } - X e ^ { - r T } .$$

Since the only unknown in this equation is the early exercise premium E ( X,T ) , we can express it as

$$E ( X , T ) = S _ { 0 } - X e ^ { - r T } - [ c ( X , T ) - P ( X , T ) ] \, .$$

In this way, a simple rearrangement of the put-call parity allows us to back out the early exercise premium. Since the put-call parity is derived from the principle of no risk-free arbitrage profit, the early exercise premium in Equation (1) has no dependence on any option pricing model. Commonly used valuation models of American options such as Cox, Ross and Rubinstein (1979), Johnson (1983), Geske and Roll (1984), Barone-Adesi and Whaley (1987), Detemple and Tian (2002), and Nunes (2009), to name a few, are not involved at all.

The put-call parity approach has been explored by Brenner and Galai (1986) and Zivney (1991) to estimate, respectively, the implied interest rate and the implied early exercise premium.


<!-- p:8 -->


Brenner and Galai (1986) find that, in general, the implied interest rate tracks the trends in market rate, despite the possibility that early exercise premiums could cause the implied interest rate to deviate from the observed rate. Zivney (1991) uses the implied interest rates of Brenner and Galai (1986) to estimate the net value of early exercise for a pair of put and call options. Zivney (1991) concludes that the exercise premiums in options on S&amp;P 100 index are more substantial than what existing literature has suggested. Interestingly, in the setting of modelfree volatility, the empirical results documented in the subsequent sections are qualitatively consistent with Zivney (1991)'s conclusion. Nonetheless, a difference of Equation (1) from these two works is that the notion of implied interest rate is not needed.

Notice that the inputs to the early exercise premium in Equation (1) are all observable prices in the stock market, interest rate market, and the option market. Hence, it is a modelindependent formula, which is a departure from Carr and Wu (2009), Driessen, Maenhout and Vilkov (2009), Trolle and Schwartz (2010), and Prokopczuk and Wese Simen (2013), among others. In these papers, early exercise premium is adjusted by essentially the Black-Scholes option pricing model, either implemented as an analytical approximation ( Barone-Adesi and Whaley (1987) ) , or using the binomial tree method ( Cox, Ross and Rubinstein (1979) ) . The drawback, however, is that Equation (1) becomes inapplicable whenever the dividend ex-date t ex is before the option expiry date T , i.e., 0 &lt; t ex &lt; T . This is not an issue for non-dividend paying stocks, which is the case for the four ETFs examined in this paper.

### 3.2 Model-Free Volatility Index

An implied volatility method is truly model-free if, at every stage of the calculation, models for pricing options are not required at all. In the model-free approach, the implied model-free volatility σ MF is directly computed from the continuum of European options of the same underlying asset and time to maturity T . However, if any interpolation is performed on the Black-Scholes implied volatility, model dependence could still be inadvertently introduced. Furthermore, direct interpolation in the implied volatility space is not guaranteed to be arbitrage-free. In this section, we outline a model-free approach that interpolates directly in the price space with no-arbitrage conditions.


<!-- p:9 -->


Given the observed option prices, the model-free formula for computing the implied variance σ 2 MF T is the sum of two integrals over the strike price X :

$$\sigma _ { M F } ^ { 2 } T = 2 e ^ { r T } \left ( \int _ { 0 } ^ { F _ { 0 } } \frac { p ( X , T ) } { X ^ { 2 } } \ d X + \int _ { F _ { 0 } } ^ { \infty } \frac { c ( X , T ) } { X ^ { 2 } } \ d X \right ) .$$

Here, F 0 is the forward price of the underlying asset valued at time 0 . For commodity ETFs that do not pay dividends and other benefits, the forward price is simply F 0 = S 0 e rT .

Equation (2) is generic and assumes only the existence of a unique risk-neutral probability measure when taking the expectation of the option payoff on the expiration date. It is riskneutral in the sense that market makers can afford to be indifferent to the risk accompanying a plain vanilla option because its payoff can be replicated and hedged whenever the option is fairly valued under the risk-neutral framework where there is no risk-free arbitrage opportunity.

It is important to note that evaluating the integrals in Equation (2) is a non-trivial task, given that in theory we need the full continuum of option prices spanning all positive real numbers. Yet, the market provides firm quotes for a small number of options at discrete strikes. To ensure that no option pricing model is utilized at all stages of the construction process, we follow Lim and Ting (2013) to interpolate the discrete strike prices into a continuum, in such a way that no risk-free arbitrage opportunities will arise. More details of the interpolation algorithm based on cubic spline in the price space can be found in Appendix A.

As an example, Figure 1 shows the results of spline fitting the end-of-day mid-quotes of options on UNG ETF, chosen because their liquidity is the lowest among the four commodity option contracts to demonstrate the robustness of the interpolation procedures. The left panel contains options maturing in 22 days' time from August 30, 2013, which is the last day of our sample period. The right panel shows the spline fitting results for UNG ETF's options with 50 days to maturity. Notice that the generated price curves do not pass through the observed midquotes exactly, because they must satisfy the three specific conditions required by the principle of no risk-free arbitrage opportunities.


<!-- p:10 -->


### 3.3 Commodity Volatility Indexes

To obtain the annualized volatility index σ for a fixed time horizon or constant maturity T , we interpolate the model-free variances σ 2 a T a and σ 2 b T b with T a &lt; T &lt; T b , where T a is strictly smaller than T b . At time 0, following the standard practice (see CBOE (2009)), the model-free volatility index σ is obtained by linear interpolation as follows:

$$\sigma ^ { 2 } T = \sigma _ { a } ^ { 2 } T _ { a } \frac { T _ { b } - T } { T _ { b } - T _ { a } } + \sigma _ { b } ^ { 2 } T _ { b } \frac { T - T _ { a } } { T _ { b } - T _ { a } } .$$

The Actual/365 day-count convention is used to annualize the variance, since the expiration of the American option is based on the calendar date, which includes Saturday and Sunday.

As an illustration, based on the UNG ETF example in Figure 1, we have T a = 22 / 365 and T b = 50 / 365 . We obtain from Equation (A.1) that σ a = 20 . 81% and σ b = 24 . 20% . For 30-day constant maturity, i.e., T = 30 / 365 , applying Equation (3) results in a model-free natural gas volatility index of 22.49% for August 30, 2013.

Figure 2 plots eight time series of ETF's prices and the constructed volatility index values for 30-day constant maturity. Note that each volatility index tends to move in the direction opposite to its underlying ETF's price movement. This anti-correlation is a standard characteristic of volatility indexes. For instance, it is commonly observed that whenever the market is in crisis, VIX tends to register abnormally high values. The reference to VIX as a 'fear gauge' has become a common practice among analysts and journalists.

Our commodity volatility indexes also exhibit this feature. For example, when the UNG ETF price is at its peak, the natural gas volatility index is in the valley. In particular, after the UNG ETF hit the historical high of (reverse stock split adjusted) $507.84 per share on July 1, 2008, a sharp decline ensued. Meanwhile, the UNG volatility index experienced a rapid incline upward from the level of about 30 to 40 percentage points to the range of 60 to 70 percentage points. When the UNG ETF sank below $75 per share for the very first time on September 3, 2009, the UNG volatility index reached the record high of about 85%.


<!-- p:11 -->


The negative correlation between the volatility indexes and the underlying ETFs quantifies the degree of predictability in their co- or counter-movements. The correlations estimated from daily returns are tabulated in Table II. These estimates are statistically different from zero at the 5% level of significance. As a reference, the correlation between the daily return on VIX and that on the S&amp;P 500 index is - 76 . 15% over our sample period (May 9, 2007 through August 30, 2013). Although the correlation estimates are not as negative compared to VIX's correlation with the S&amp;P 500 index, our four commodity volatility indexes nonetheless exhibit the 'fear gauge' feature, particularly during the 2008-2009 recession.

## 4 Empirical Analyses

Using the options on four commodity ETFs from OptionMetrics (see Section 2), we perform adjustments of early exercise premiums, compute model-free volatilities, and estimate the variance risk premiums.

### 4.1 Comparison of Methods to Account for Early Exercise Premiums

As discussed in the previous section, applications of the model-free volatility methodology to underlying assets where the options traded are American style need to first address the issue of how early exercise premiums are to be adjusted. Carr and Wu (2009), Driessen, Maenhout and Vilkov (2009), Trolle and Schwartz (2010), and Prokopczuk and Wese Simen (2013) take this into consideration using either the binomial tree model of Cox, Ross and Rubinstein (1979) 1 or the approximation of Barone-Adesi and Whaley (1987). The binomial tree is essentially a finite-time discretization of the Black and Scholes (1973) model, while the Barone-Adesi and Whaley (BAW) method is an analytical approximation relying on the pricing formulas of Black and Scholes (1973). In contrast, a salient feature of our put-call parity method (Equation (1)) is zero dependence on any option pricing model. This feature preserves the model-free quality of Equation (2).

1 The binomial tree model is also used by OptionMetrics.


<!-- p:12 -->


To examine the sensitivity and impact of early exercise premium on the model-free volatility, we need to have a common benchmark for the three early exercise premium adjustment methods on the same basis for meaningful comparison. To this end, we first calculate the model-free volatility indexes by treating the American options as European, ignoring the need to subtract the early exercise premiums. We then recalculate the model-free volatility indexes using each of the following methods to account for the early exercise premium:

1. put-call parity method proposed in this paper
2. binomial tree model
3. Barone-Adesi and Whaley (BAW) approximation

The objective of this analysis is to determine whether the early exercise premium adjustment yields statistically and economically significant differences in the volatility indexes. If the early exercise premium does play a vital role, the model-free volatility computed without adjustment for the early exercise premium should be economically larger. Apart from the early exercise premium adjustment methods, all the model-free volatility calculations are based on the same methodology described in this paper, so that any numerical differences are attributed solely to the difference in the treatment of early exercise premiums. We carry out this analysis across maturity to identify potential variation along the term structure of volatilities.

For each commodity ETF and for each option maturity T , we compute the difference of annualized volatilities in percentage points:

$$D ( T ) = \sigma _ { 0 } ( T ) - \sigma _ { a } ( T ) .$$

Here, σ 0 ( T ) is the model-free volatility without adjustment for the early exercise premium, which serves as the benchmark for comparing the three methods that account for the early exercise premium. The model-free volatility with adjustment is denoted by σ a ( T ) , where a is either the put-call parity method, the binomial tree model, or the Barone-Adesi and Whaley approximation.


<!-- p:13 -->


The implied volatility is the parameter of the binomial tree that will match the market price of the American option. The early exercise premium can be readily quantified once the matching implied volatility is obtained. Likewise, the BAW approximation uses the implied volatility as a parameter to iteratively search for a value such that the option price generated matches the American option price observed in the market. By contrast, the put-call parity method is a straightforward calculation, which does not involve an iterative search with an option pricing model.

It is important to point out that when using the binomial tree model, occasionally the implied volatility required to match the observed option price cannot be calculated. This could happen for instance when the midpoint of the bid and ask prices falls below the intrinsic value, or when the iterative implied volatility search procedure fails to converge. The BAW approximation method may also experience no convergence at times. When either the binomial tree or the BAW approximation does not attain convergence, D ( T ) calculated for the model-free variance based on the put-call-parity method is omitted in the comparison. Otherwise, there will be more D ( T ) values for the put-call-parity method, and the comparison with the binomial tree and the BAW approximation cannot be performed on an equal footing.

Given the restrictions from the binomial tree and the BAW approximation, we group D ( T ) by maturity of 7 ≤ T ≤ 30 , 30 &lt; T ≤ 60 , 60 &lt; T ≤ 90 , . . . , 510 &lt; T ≤ 540 , and then compute the average difference. We limit T to be less than 540 days to maturity. This is due to the fact that options of maturities longer than one and a half years do not have sufficient sample size for obtaining a reliable average. Moreover, liquidity for options of long maturities is typically low and the spread between bid and ask prices is large.

The summary statistics for the volatility differences are presented in Table III. For each grouped maturity, the null hypothesis is that D ( T ) = 0 and the alternative hypothesis is that D ( T ) &gt; 0 . The comparison results for gold (Panel A: GLD), silver (Panel B: SLV), natural gas (Panel C: UNG), and crude oil (Panel D: USO) are presented. Overall we find that the volatility differences are statistically significant for these four commodity ETFs. Given that the null hypothesis is not valid, we have evidence to suggest that early exercise premium adjustment plays an important role in the calculation of model-free volatility when the options are American style. Without accounting for it, an upward bias will be present in the calculation of model-free volatilities.


<!-- p:14 -->


The statistics in Table III for the binomial tree model and for the Barone-Adesi and Whaley approximation are very close to each other by comparison. This finding should be intuitive, since these two option pricing methods are based on or related to the Black-Scholes model. Interestingly, with the exception of gold ETF, D ( T ) tends to be larger for short maturities than for long maturities when these two methods are applied to account for the early exercise premiums. By contrast, the average volatility difference for the put-call parity approach is fairly constant across maturities. The differences are not only statistically more significant (larger t statistics), but also economically significant. As an example, for the GLD volatility index calculated using the put-call parity approach, the overall average difference is about 0.55 percentage points. By contrast, the corresponding averages for the binomial tree and the BAW model are only 0.07 percentage points, which are not economically significant. The former is about 2.41% of the average model-free volatility of 22.90 percentage points, while the latter is a mere 0.30% of the average model-free volatility of 23.45 percentage points.

It is also worth highlighting that the mean volatility difference is higher for the put-callparity method, as shown in the last row of each panel. In addition to the case of gold ETF discussed earlier, the mean volatility difference of 2.31 percentage points for the crude oil ETF is also much higher than the 0.49 percentage points for the binomial tree (and also for the BAW method). To summarize, all the three methods are able to adjust for the early exercise risk premium. Nevertheless, the put-call parity approach is different from the other two methods at longer maturities up to 540 days.


<!-- p:15 -->


The consistently larger D ( T ) for the put-call parity method suggests that in the setting of model-free volatility, the early exercise premium accounted for is larger than what the two commonly used methods have yielded. This result is qualitatively consistent with the findings in Zivney (1991). Consequently, the model-free volatility calculated after the early exercise premium adjustment tends to be smaller than that using the other two adjustment methods.

### 4.2 Model-Free Variance and Variance Swap

Variance swaps are liquid across major equity indexes and large cap stocks, and are becoming increasingly popular across emerging market indexes and other asset classes (see Allen, Einchcomb and Granger (2006) and also Carr and Wu (2009)). The most liquid variance swaps are on stock indexes with maturities ranging approximately from 3 months to 2 years. Ample liquidity is also observed at the front end (e.g. 3 months) for short-dated index variance. In this contract, the model-free variance is the variance swap rate for the fixed leg, which constitutes a direct application of the model-free variance.

The variance swap on the S&amp;P 500 index is traded over the counter (OTC). Market quotes of index variance swaps are obtainable from broker-dealers. Recent papers that utilize brokerdealers' variance swap quotes include Egloff, Leippold and Wu (2010) and Aït-Sahalia, Karaman and Mancini (2013). The volatility index of a commodity ETF can be thought of as a synthetic but useful benchmark for pricing a commodity variance swap, in much the same way that VIX is synthetic yet employed as a reference rate to price an S&amp;P 500 index variance swap.

More specifically, the model-free variance is the risk-neutral expectation of future variance integrated over an infinitesimal time interval dt , from today ( t = 0) to expiration time ( t = T ) . Expressed mathematically, it is

$$\sigma _ { M F } ^ { 2 } T = \mathbb { E } _ { 0 } ^ { \mathbb { Q } } \left [ \int _ { 0 } ^ { T } \sigma _ { t } ^ { 2 } \ d t \right ] .$$

Under the risk-neutral measure, the model-free variance σ 2 MF is the variance swap rate.


<!-- p:16 -->


The floating leg of the m -day variance swap is computed using the spot prices from calendar day 0 up to calendar day m when the variance swap matures. Let N m be the number of trading days in these two calendar dates. Denoting the end-of-day ETF price by S k , the annualized realized variance is defined as the average of the squared logarithmic returns:

$$V = \frac { 2 5 2 } { N _ { m } } \sum _ { k = 1 } ^ { N _ { m } } \left [ \ln \left ( \frac { S _ { k } } { S _ { k - 1 } } \right ) \right ] ^ { 2 } .$$

Here, the subscript k in the daily ETF price S k refers to the number of trading days from today, and 252 is the conventional constant to annualize the realized variance. Equation (6) is the definition used in practice for variance swap transactions (see Allen, Einchcomb and Granger (2006)).

As can be seen from Figure 2, the variance or volatility itself is also stochastic. Therefore, investors are exposed to two sources of market risk, namely, the risk about the return as captured by the return variance (volatility), and the risk about the return variance itself (volatility of volatility). In this context, variance swaps offer a straightforward means to manage the uncertainty in volatility of an underlying asset. Moreover, investors can use variance swaps to take a direct volatility exposure without the cost and complexity of managing and hedging a basket of vanilla options.

Let G denote the cash flow that a variance swap buyer receives at maturity T , i.e.,

$$G = N o t i o n a l \ A m o u n t \ \times ( V - \sigma _ { M F } ^ { 2 } ) .$$

Buyer pays the fixed rate agreed upon at time 0 and receives the floating V , which is the realized variance defined in Equation (6) (See for example, Bekaert and Hoerova (2014)). At time 0, the underlying asset price S k for k &gt; 1 is unknown. By time T , all the asset prices are observed, and V can be computed. It follows that there is no ambiguity in determining the profit and loss.

The variance swap buyer pays the variance swap rate known at time 0 to hedge or insure against a rise in volatility from time 0 to time T . If the P&amp;L is negative most of the time so that G is on average negative for the variance swap buyer, it can be said that the buyer pays a premium to insure against the variance risk.


<!-- p:17 -->


Suppose a hypothetical variance swap deal is done each day in our sample period for every commodity ETF. The notional amount is set at $100. In Table IV, we present the statistics for G , which is the P&amp;L of the variance swap buyer. To examine its statistical significance, a t statistic is computed with the Newey and West (1987) adjustment for serial correlations for each commodity ETF. We further apply the recommendation in Newey and West (1994) to select the number of lags with the Bartlett kernel. Based on the Newey-West t statistics at the 5% significance level, we infer that G , in general, is negative and statistically significant. These t test results constitute resounding evidence of variance risk premiums for our commodity ETFs 2 .

Table IV also compares the three different adjustment methods against the benchmark, which is the model-free variance computed without adjustment (None) for early exercise premiums. In the previous subsection, we have shown that with the put-call parity (PCP) adjustment method, evidence is compelling that the early exercise premium is larger than previously thought when either the binomial tree pricing model (BT) or the Barone-Adesi and Whaley approximation (BAW) is used as the adjustment method. It follows that the P&amp;L for the PCP method of a long position in the variance swap should be less negative, since the resulting variance swap rate, i.e., model-free variance, is comparatively smaller. Indeed, the results tabulated in Table IV are consistent in that, with a few exceptions, the average P&amp;L for the PCP method is comparatively smaller in magnitude.

Turning to the 50-th percentile (i.e., the median), we find that they are negative as well. Moreover, the median values are more negative than the average values. At the 75-th percentile, the P&amp;L starts to turn positive. In other words, approximately 75% of the time, the P&amp;L is negative, which means that variance swap buyers stand to lose more often than gain. Taken together, our results are comparable to the empirical findings for equity market indexes such as VIX, where the option-implied variance for stock indexes tends to be larger than the realized variance, suggesting that it is favorable to sellers of stock index variance swaps. As alluded to earlier, the persistence of a negative P&amp;L for the variance swap buyer is interpreted as the variance risk premium that investors pay to hedge against the drastic fluctuation of volatility.

2 There are a few exceptions: gold ETF for 30- up to 90-day constant maturities and crude oil for 90- up to 330-day constant maturities when put-call parity method is applied to adjust for early exercise premiums. The Newey-West t statistics for these cases are not statistically significant.


<!-- p:18 -->


## 5 Conclusions

Applications of the model-free method to construct volatility indexes from American options have hitherto been impeded by the lack of a model-independent way to handle early exercise premiums. While the binomial tree model and the Barone-Adesi and Whaley approximation are popular methods for the adjustment of early exercise premiums, it is difficult to consider the values obtained as truly model-independent.

Furthermore, when integrating across the continuum of strikes to obtain the risk-neutral variance, interpolation is typically performed in the Black-Scholes implied volatility space, without checking whether the no-arbitrage conditions are satisfied. These two shortcomings inevitably introduce model dependence to the otherwise model-free formulation.

This paper fills the gap by formulating a totally model-free framework to construct volatility indexes using the market quotes of American options on four important commodity ETFs. A salient feature of our proposed approach is the complete absence of model dependence. Early exercise premium is accounted for using only the put-call parity, which is predicated solely on the principle of no risk-free arbitrage. The caveat, however, is that the proposed method is only applicable to American options on non-dividend paying assets. Another feature of our method is that interpolation across strike prices is performed directly in the option price space, with no-arbitrage conditions incorporated into the cubic spline algorithm.

Our empirical analysis suggests that the early exercise premiums estimated using either the binomial tree pricing model or the Barone-Adesi and Whaley approximation tend to be relatively smaller than those estimated by the put-call parity method. Accordingly, volatility indexes calculated after using the put-call parity method to adjust for early exercise premiums are lower in comparison. Despite being lower, we still find strong empirical evidence of variance risk premiums. In other words, using model-dependent methods to adjust for early exercise premiums could potentially overestimate the magnitude of variance risk premiums. In summary, we have proposed a theoretically and computationally sound methodology to construct volatility indexes, with the distinctive feature of complete independence from any option pricing model, even in the interpolation of strike prices and the adjustment for early exercise premiums. Our research also provides evidence for the presence of variance risk premiums in four commodity ETFs that are important to fund managers. Finally, an upward bias is likely to be introduced by current numerical schemes widely used for extracting the early exercise premiums. This finding has important implications for traders and investors in the commodity market.


<!-- p:19 -->


## Appendices

## A Interpolation Methodology

The model-free formula (Equation (2)) requires the strike price X to span the full continuum of positive real numbers. In practice, the strike price of an option chain never extends from zero to infinity. For every maturity series, call options of strike prices larger than the highest strike price H and put options of strike prices smaller than the lowest strike price L of the option chain is effectively zero. Consequently, Equation (2) becomes

$$\sigma _ { M F } ^ { 2 } T = 2 e ^ { T } \left [ \int _ { L } ^ { F _ { 0 } } \frac { p ( X , T ) } { X ^ { 2 } } \ d X + \int _ { F _ { 0 } } ^ { H } \frac { c ( X , T ) } { X ^ { 2 } } \ d X \right ] .$$

Furthermore, in reality, X is discrete and the gap from one strike price to the next can be wide.

These two issues have been, among others, specifically addressed by Lim and Ting (2013). They apply the spline technique directly on option prices to perform polynomial interpolation across the strike price intervals while enforcing the no-arbitrage principle. In addition to being truly model-free, another advantage of the price-space approach is that one can directly incorporate the three no-arbitrage conditions of option price monotonicity, bounded gradient, and convexity with respect to the strike price. These three conditions must be satisfied by the option price curves to prevent risk-free arbitrage. Since the underlying stock price has zero probability to go beyond the minimum or maximum strike price of the option chain on any given trading day, which is satisfied ex-post, the smooth splines generate synthetic options that fill the strike price gaps.

Specifically, the strike price interval or gap is sliced into many sub-intervals. The synthetic European option price o k ( X,T ) over any small sub-interval ( X k , X k +1 ] is represented locally as a cubic polynomial function:

$$o ^ { k } ( X , T ) = s _ { 1 } ^ { k } X ^ { 3 } + s _ { 2 } ^ { k } X ^ { 2 } + s _ { 3 } ^ { k } X + s _ { 4 } ^ { k } .$$


<!-- p:20 -->


Every cubic spline is defined by its coefficients s k 1 to s k 4 . Notably, integration over each subinterval ( X k , X k +1 ] admits a closed form expression, which makes calculations of model-free variance exact :

$$\int _ { X _ { k } } ^ { X _ { k + 1 } } \frac { o ^ { k } ( X , T ) } { X ^ { 2 } } \ d X = s _ { 1 } ^ { k } \frac { X _ { k + 1 } ^ { 2 } - X _ { k } ^ { 2 } } { 2 } + s _ { 2 } ^ { k } ( X _ { k + 1 } - X _ { k } ) + s _ { 3 } ^ { k } \ln \left ( \frac { X _ { k + 1 } } { X _ { k } } \right ) - s _ { 4 } ^ { k } \left ( \frac { 1 } { X _ { k + 1 } } - \frac { 1 } { X _ { k } } \right ) .$$

Representation of a smooth curve locally by a polynomial function is a foundation of numerical analysis. It is a nonlinear generalization of the linear interpolation.

When the sub-interval size X k +1 - X k is made as small as $0.01 for each sub-interval k , the two integrals in Equation (A.1) can be obtained by applying Equation (A.3), which is an exact definite integral. In other words, the integration is performed exactly, as shown on the right hand side of Equation (A.3). The required continuum of strike prices is obtained after piecing together all the sub-intervals ( X k , X k +1 ] . More concretely, let X 1 = L , X I = F 0 , and X J = H . With p i 1 to p i 4 and c j 1 to c j 4 being the spline coefficients for puts and calls, respectively, we compute the two integrals in Equation (A.1) by adding up every sub-interval. Accordingly, we obtain

$$\int _ { L } ^ { F _ { 0 } } \frac { p ( X , T ) } { X ^ { 2 } } d X = \sum _ { i = 1 } ^ { I - 1 } \left [ p _ { 1 } ^ { X _ { i + 1 } ^ { 2 } - X _ { i } ^ { 2 } } + p _ { 2 } ^ { i } ( X _ { i + 1 } - X _ { i } ) + p _ { 3 } ^ { i } \ln \left ( \frac { X _ { i + 1 } } { X _ { i } } \right ) - p _ { 4 } ^ { i } \left ( \frac { 1 } { X _ { i + 1 } } - \frac { 1 } { X _ { i } } \right ) \right ]$$

and

$$\int _ { F _ { 0 } } ^ { H } \frac { c ( X , T ) } { X ^ { 2 } } d X = \sum _ { j = I } ^ { J - 1 } \left [ c _ { 1 } ^ { j } \frac { X _ { j + 1 } ^ { 2 } - X _ { j } ^ { 2 } } { 2 } + c _ { 2 } ^ { j } ( X _ { j + 1 } - X _ { j } ) + c _ { 3 } ^ { j } \ln \left ( \frac { X _ { j + 1 } } { X _ { j } } \right ) - c _ { 4 } ^ { j } \left ( \frac { 1 } { X _ { j + 1 } } - \frac { 1 } { X _ { j } } \right ) \right ] .$$

With these formulas, we can compute the model-free variance as accurately as possible by setting the sub-interval size as small as $0.01.

The combination of the put-call parity and the cubic spline methods, which are firmly grounded on the principle of no risk-free arbitrage opportunity, is consistent with the truly model-free approach of not using any option pricing models at all stages of computation, which is a big advantage. The simplicity and robustness of our proposed method also make it easier for practitioners to implement and adopt.


<!-- p:21 -->
