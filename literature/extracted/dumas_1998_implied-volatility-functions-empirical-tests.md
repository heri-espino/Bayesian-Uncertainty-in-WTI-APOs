---
id: "dumas_1998_implied-volatility-functions-empirical-tests"
source_pdf: "../pdf/dumas_1998_implied-volatility-functions-empirical-tests.pdf"
source_filename: "dumas_1998_implied-volatility-functions-empirical-tests.pdf"
format: "academic-paper"
extraction_profile: "text-math-tables-high-fidelity"
extraction_mode: "hybrid"
extraction_quality: "excellent"
extraction_score: 106.0
visual_assets: "disabled"
references_file: "../references/dumas_1998_implied-volatility-functions-empirical-tests.references.md"
---

<!-- p:1 -->

##### NBER WORKING PAPER SERIES

##### IMPLIED VOLATILITY FUNCTIONS: EMPIRICAL TESTS

Bernard Dumas Jeff Fleming Robert E. Whaley

Working Paper 5500

####### NATIONAL BUREAU OF ECONOMIC RESEARCH 1050 Massachusetts Avenue Cambridge, MA 02138 March 1996

This research was supported by the Futures and Options Research Center at the Fuqua School of Business, Duke University. We gratefully acknowledge discussions with Jens Jackwerth and Mark Rubinstein and comments and suggestions by Blaise Allaz, Denis Alexandre, Suleyman Basak, David Bates, Greg Bauer, Peter Bossaerts. Peter Carr, Gilles Demonsant, Jin-Chuan Duan, Bruno Dupire, Gary Gorton, Sanford Grossman, Bruce Grundy, Philippe Henrotte, John Hull, Eric Jacquier, Jean-Paul Laurent, Hayne Leland, Angelo Melino, Krishna Ramaswamy, Ehud Ronn, Denis Talay, Alan White and the participants at the HEC Finance workshop in March 1995, the Isaac Newton Institute, Cambridge University, in April 1995, the Chicago Board of Trade's Nineteenth Annual Spring Research Symposium in May 1995, the Wharton School Finance workshop in September 1995, the University of New Mexico workshop in October 1995, the University of Toronto finance workshop in November 1995, the Sixth Annual Conference on Financial Economics and Accounting at the University of Maryland in November 1995 and the semiannual meeting of the Inquire Europe group in Barcelona in November 1995. This paper is part of NBER's research program in Asset Pricing. Any opinions expressed are those of the authors and not those of the National Bureau of Economic Research.

© 1996 by Bernard Dumas, Jeff Fleming and Robert E. Whaley. All rights reserved. Short sections of text, not to exceed two paragraphs, may be quoted without explicit permission provided that full credit, including © notice, is given to the source.


<!-- p:2 -->


##### IMPLIED VOLATILITY FUNCTIONS: EMPIRICAL TESTS

### ABSTRACT

Black and Scholes (1973) implied volatilities tend to be systematically related to the option's exercise price and time to expiration. Derman and Kani (1994), Dupire (1994), and Rubinstein (1994) attribute this behavior to the fact that the Black-Scholes constant volatility assumption is violated in practice. These authors hypothesize that the volatility of the underlying asset's return is a deterministic function of the asset price and time and develop the deterministic volatility function (DVF) option valuation model, which has the potential of fitting the observed cross-section of option prices exactly. Using a sample of S&amp;P 500 index options during the period June 1988 through December 1993, we evaluate the economic significance of the implied deterministic volatility function by examining the predictive and hedging performance of the DV option valuation model. We find that its performance is worse than that of an ad hoc BlackScholes model with variable implied volatilities.

Bernard Dumas H.E.C. School of Management 78351 Jouy-en-Josas Cedex FRANCE and NBER

Robert E. Whaley Fuqua School of Business Duke University Durham, NC 27708-0120

Jeff Fleming Jones Graduate School of Graduate Administration Rice University PO Box 1892 Houston, TX 77251


<!-- p:3 -->


##### IMPLIED VOLATILITY FUNCTIONS: EMPIRICAL TESTS

Claims that the Black and Scholes (1973) valuation formula no longer holds in financial markets are appearing with increasing frequency. When the Black/Scholes formula is inverted to imply volatilities from reported option prices, the volatility estimates differ across exercise prices and times to expiration.1 For S&amp;P 500 index option prices prior to the October 1987 market crash, for example, the implied volatilities form a "smile" pat y hny t--n  t-- d e  te tned volatilities than at-the-money options. After the crash, a "sneer"2 appears—implied volatilities of S&amp;P 500 options decrease monotonically as the option exercise price rises relative to the current index level, with the rate of decrease increasing for options with shorter time to expiration.

The failure of the Black/Scholes model to describe the structure of reported option prices is thought to arise from its constant variance assumption.3 Casual empiricism suggests that when stock prices go up volatility goes down, and vice versa. Accounting for nonconstant volatility within an option valuation framework, however, is no easy task. With stochastic volatility, option valuation generally requires a market price of risk parameter, which, among other things, is difficult to estimate. An exception occurs where the volatility of the underlying asset's return is a deterministic function of asset price and/or time. In this case, option valuation based on the Black/Scholes partial differential equation remains possible although not by means of the Black/Scholes formula itself.

Deurtt  (D   ( n (   ns of the deterministic volatility function (DVF) option valuation model. Rather than positing n eo   us sur es n fuo   u no

1 Rubinstein (1994) examines the S&amp;P 500 index option market. Similar investigations have also been performed for the Philadelphia Exchange's foreign currency option market (e.g., Taylor and Xu (1993)), and for stock options traded at the LIFFE (e.g., Duque and Paxson (1993)) and the European Options Exchange (e.g., Heynen (1993)).

3 Putting it succinctly, Black (1976, p. 177) says that "... if the volatility of a stock changes over time, the

Jo ste      osda a     a     l en one corner of the upper lip."

option formulas that assume a constant volatility are wrong."

1


<!-- p:4 -->


trinomial lattice that achieves an exact cross-sectional fit of reported option prices. Rubinstein, for example, uses an "implied binomial tree" whose branches at each node are designed (either by choice of up-and-down increment sizes or probabilities) to reflect the time-variation of volatility. An exact fit is ensured since there are as many degrees of freedom in their approaches as there are reported option prices.

With so much freedom in parameter selection, the chance of overfitting reported puui uin n uin i  Dui in  e u ui ud procedures for estimating (implicitly) the volatility function in-sample, none of the studies go out-of-sample to determine the stability of the function through time. If the estimated volatility function is stable, the DVF option valuation model offers an important new way for setting hedge ratios and valuing exotic options. On the other hand, if the estimated function is not stable, valuation and risk management using the DVF methodology will be unreliable, and other explanations for the Black/Scholes implied volatility patterns must be sought.

The purpose of this paper is to assess the stability of the implied deterministic volatility function for the S&amp;P 500 index. Since valuation and risk management are measured in dollars and cents, we evaluate the stability of the estimated volatility function by examining how well it predicts future option prices. We estimate the volatility function based on the cross-section of reported option prices one week, and then we examine the price deviations from theoretical values one week later. An alternative, albeit inferior, approach would be to examine whether the coefficients of the volatility function change significantly through time.4

The paper is organized as follows. In Section I, we outline our empirical procedure and review option valuation under deterministic volatility. In Section II, we describe our sample of S&amp;P 500 index option prices and document typical Black/Scholes implied volatility patterns. In Section III, we estimate the implied volatility functions using the DVF option valuation model and a cross-section of reported index option prices, and describe the model's goodness-of-fit. In Sections IV and V, we assess the stability of the implied volatility functions for the S&amp;P 500 index. The tests in Section IV examine how well the volatility function estimated at time t predicts option prices one week later, and tasns Sas es  Dnc s es sn  ss ts ss ne. The study concludes in Section VI with a summary of the main results and some suggestions for future research.

4 In Section IV-B, we discuss the weakness of evaluating the DVF methodology by examining the volatility function coefficients directly.


<!-- p:5 -->


## I. Empirical Procedure and Option Valuation Under Deterministic Volatility

The procedure used in this study to evaluate the economic significance of the deterministic volatility option valuation model has two steps. The first step, called estimation," involves fitting the deterministic volatility option valuation model (using different specifications for the local volatility rate) by minimizing the sum of squared deviations of theoretical option values from reported option prices.s The volatility functions are sufficiently descriptive so as to fit the cross-section of reported option prices almost exactly. The second step, called "prediction," involves moving forward one week in time and evaluating the model's prediction errors, defined as the difference between the theoretical DVF option values computed using the previous week's estimated volatility function and reported option prices.6 In this section, we outline our procedure for valuing options under deterministic volatility and describe our assumed volatility function specifications.

### A. Option valuation under deterministic volatility

Option valuation under deterministic volatility is relatively straightforward. Assuming that the local volatility rate of the underlying asset is a deterministic function of asset price and time, the partial differential equation describing the option price dynamics is the familiar Black/Scholes (1973) equation,

5 The algorithm used for the minimization is "AMOEBA" from Press, Teukolsky, Vetterling, and Flannery (1992). The routine is based on the downhill simplex method of Nelder and Mead (1965).

6 The direct evaluation of the DVF model's prediction errors is more efficient statistically than is the alternative procedure of testing the estimated volatility function on subsequent asset price behavior. To estimate the stochastic process directly requires a time series of observations during which the process functional specification remains unchanged. Our approach requires only a cross-section of option prices.


<!-- p:6 -->


$$- \frac { 1 } { 2 } \sigma ^ { 2 } ( F , t ) F ^ { 2 } \frac { \partial c } { \partial F ^ { 2 } } = \frac { \hat { x } } { \hat { a } } ,$$

where F is the asset price for forward delivery on the expiration date of the option, c is the forward option price, σ(F,t) is the local volatility of the price F, and t is current time.7 Forward prices, rather than spot prices, for the option and its underlying asset to avoid the issue of randomly fluctuating interest rates.

Equation (1) applies to the valuation of both calls and puts and both Europeanand American-style options. What distinguishes the valuation problems are the boundary conditions. For a European-style call option, for example, the boundary condition, c(F,T)= max(F– X,0), is applied at the option's expiration. In the special case where the volatility rate is constant (i.e., σ(F,t)= σ), the value of a European-style call can be obtained analytically, with the resulting formula being known as the "Black/Scholes formula." For more complex volatility functions, analytical formulas are generally not possible although option valuation remains possible using numerical procedures. Rubinstein (1994), for example, uses a binomial lattice approach, while Dupire (1994) uses a trinomial lattice.

Equation (1) is called the backward equation of the Black/Scholes model (expressed in terms of forward prices). The call option value is a function of F and t for a fixed exercise price X and date of expiration T. At time 1 when F is known, however, the cross-section of option prices (with different exercise prices and dates of expiration) can also be considered to be functionally related to X and T. For European-style options, Dupire (1994) shows that the forward option value, c(X, T), must be a solution of the forward partial differential equation,8

<!-- p:7 -->


with the associated initial condition, c(X,0)= max(F– X,0). In equation (2), the same local volatility function, σ(·,·), appears as in equation (1). The arguments, F and t, however, are replaced by the arguments X and T because equation (1) uses the local volatility that prevails at the present time when the calendar date is t and the index level is F, while equation (2) uses the future local volatility that will prevail on the expiration date, T, assuming that the underlying index is then at level X.

The advantage of using the forward equation to value European-style options (like those listed on the S&amp;P 500 index) is that all option series with a common time to expiration can be valued simultaneously-—a considerable computational cost saving when using numerical procedures.9 To infer volatility functions from American-style option prices, however, would require solving the backward equation (2) for each option series.

### B. Specifying the volatility function

To estimate the volatility function σ(X, T), the DVF option valuation model is fitted to the reported option prices at time t. Since σ(X, 7) is an arbitrary function, we posit a number of different structural forms including:10

Model 0: σ = a\_0

Model 1: σ =a +a1X +a2X2 (3)

Model 2: σ = a。+a,X +a2X2 +a3T+asXT

Model 3: σ=a。+a1X+a2X2+a3T+a4T2+a5XT

Model 0 is the volatility function of the Black/Scholes constant volatility model. Model 1 attempts to capture variation in volatility attributable to asset price, and Models 2 and 3 capture additional variation attributable to time.

In using parsimonious volatility structures such as Models 1 through 3, our approach does not guarantee that the fitted theoretical values match the reported option prices, as did the lattice approaches of Derman and Kani (1994), Dupire (1994) and Rubinstein (1994). Among other reasons, we choose to specify the functional form of the local volatility rate directly to avoid the problems of using the tree-based approaches to predict option values. Had we built a binomial tree at date t, the likelihood that the actual S&amp;P500 index level falling on a node of the tree one week later is remote. Indeed, the future index level is virtually certain to fall between nodes or outside the span of the tree entirely, in which case interpolation or extrapolation techniques must be applied. By estimating an approximate quadratic function at time t, we can proceed to value options at the prediction stage without further complication. In addition, while our restricted functional forms do not deliver an absolutely perfect fit of the cross-section of reported option prices, models as parsimonious as Model 3 achieve an "almost" perfect fit. Consequently, using more elaborate models such as those embedded in the lattice-based approaches presents a significant danger of overfitting reported prices and deteriorating the quality of prediction.

9 We solve equation (2) using the Crank-Nicholson finite-difference method.

10 If, in the course of the estimation, the value of σ becomes negative, it is replaced by a small positive number (i.e., one percent annually). Typically, this occurs only for extremely high index levels.


<!-- p:8 -->


Finally, we choose quadratic forms to model the local volatility rate. This decision is based, in part, on the casual empiricism that Black-Scholes implied volatility patterns for S&amp;P 500 index options have a parabolic shape. (See, for example, Section I-B below.) The volatility function could also be estimated using more flexible nonparametric methods such as kernel regressions" or splines. As noted above, however, we wish to avoid overparametrization of the volatility function.

## II. S&amp;P 500 Option Prices and Implied Volatility Smiles

S s sis sae s  ss  se s si o e i dhis section, we describe the data used in our analyses and document the commonly-observed pattern in Black/Scholes implied volatilities.

### A. Data Selection

Our sample contains reported prices of S&amp;P 500 index options traded on the Chicago Board Options Exchange (CBOE) during the period June 1988 through December 1993.12 S&amp;P 500 index options are European-style and expire on the third Friday of the contract month. Originally, S&amp;P 500 options traded at the CBOE expired only at the close of trading on the expiration day and were enoted by the ticker symbol SPX. When the Chicago Mercantile Exchange (CME) changed the expiration of their S&amp;P 500 futures contract from the close to the open in June 1987, the CBOE introduced a second set of S&amp;P 500 options with the ticker symbol NSX that expired at the open along with the futures. At the outset, the trading volume of the S&amp;P 500 "open-expiry" option series was considerably lower than the "close-expiry" options. Over time, however, the trading volume grew and eventually exceeded that of the close-expiry options. On August 24, 1992, the CBOE reversed the ticker symbols of the two sets of options. Our sample contains SPX options throughout: close-expiry options until August 24, 1992 and openexpiry options thereafter. During the first subperiod, the option's time to expiration is measured as the number of calendar days between the trade date and the expiration date; during the second, the number of days to expiration is the number of calendar days remaining less one.

11 See Ait-Sahalia and Lo (661)0


<!-- p:9 -->


During the sample period, we estimate each of the volatility functions once each week (as was noted earlier). Wednesdays are used because fewer holidays fall on Wednesday than any other trading day. Where a Wednesday was a holiday during the sample period, the trading day immediately preceding Wednesday was used.

In order to estimate the volatility functions, the S&amp;P 500 index level and S&amp;P 500 index option prices are expressed as forward prices. Constructing a forward price for the S&amp;P 500 index requires both the term structure of default-free interest rates as well as the daily cash dividends for the S&amp;P 500 portfolio over the life of the option. To proxy for riskless interest rates, we use the T-bill rates implied by the average of the bid and ask discounts. The history of these discounts was collected from the Wall Street Journal. The entire term structure was collected for each day. The riskless rate corresponding to a given future dividend payment date or option maturity date is the rate obtained by interpolating the rates of the two T-bills whose maturities straddle the date in question. The daily cash dividends for the S&amp;P 500 index portfolio were collected from the S&amp;P 500 Information Bulletin. To compute the present value of the dividends paid during the option's life, PVD, the daily dividends are discounted at the rates corresponding to the ex-dividend dates and summed over the life of the option, that is,

n sd e s n e  i t      e s es a an reporting daily cash dividends for the S&amp;P 500 index portfolio. See Harvey and Whaley (1992b) regarding the importance of incorporating discrete daily cash dividends in index option valuation.


<!-- p:10 -->


$$P V D = \sum _ { n = 1 } ^ { n } D _ { i } e ^ { - \eta _ { n } }$$

where D, is the i-th cash dividend payment, t, is the time to ex-dividend from the current date, r, is the interest rate corresponding to the time to ex-dividend (interpolated from the current term structure of interest rates), and n is the number of dividend payments during the option's life.13 The implied forward price of the S&amp;P 500 index is therefore

$$F = ( S - P V D ) e ^ { \pi } ,$$

where S is the reported index level and T is the time to expiration of the option. To create a forward option price, we multiply the average of the option's bid and ask price quotesl4 btr s tor    s  stn t on

Three exclusionary criteria are applied to the data. First, options with less than six and with more than one hundred days to expiration are eliminated. Options with less than six days to expiration have relatively small time premia, hence the estimation of volatility is extremely sensitive to nonsynchronous option prices and other possible measurement errors. Options with more than a hundred days to expiration, on the other hand, are unnecessary since our objective is only to determine whether the volatility function remains valid over a span of one week. Including longer-term options would only serve to deteriorate the cross-sectional fit.

13 The convention introduces an inconsistency, with small consequences, between option prices of different maturities. The inconsistency takes two forms. First, in constructing the forward version of the S&amp;P 500 index level, one assumes that the dividends to be paid during the option's life are certain which means that, during that time, the value of the equity cannot fall below the promised amount of dividends. But that barrier is set differently for different horizon points. Secondly, the volatility function that we are estimating is truly a volatility of the forward price to the maturity date of the option. To be rigorous, we should be estimating a different volatility function for each maturity.

14 Using bid/ask midpoints rather than trade prices reduces noise in the cross-sectional estimation of the volatility function.


<!-- p:11 -->


$$\text {Second, options whose absolute ``moneyness``,} ^ { \dagger } \left | \frac { X } { F } - 1 \right | , \text { is greater than ten percent}$$

are eliminated. Like in the case of extremely short-term options, deep in- and out-of-themoney options have little time premia and hence contain little information about the volatility function. In addition, these options have little trading activity and price quotes are generally not supported by actual trades.

Finally, only options with bid/ask price quotes during the last half hour of trading (i.e., 2:45 to 3:15 PM (CST)) are used. Fearing imperfect synchronization between the option market and other markets,'5 we use neither the reported S&amp;P index nor the S&amp;P 500 futures price from the CME16 in the estimation procedure. Instead, we infer the current index level simultaneously, together with the parameters of the volatility function, from the cross-section of option prices. In this way, our empirical procedure relies only on observations from a single market, and no auxiliary assumption of market integration is necessary.17 Using this procedure, however, requires that the option prices are reasonably synchronous—hence the need for a tight time window. The cost of imposing this criterion is that we reduce the number of available option quotes. The cost is not too onerous, however, since we find quotes for an average of 44 option series during the last half-hour each Wednesday.18 Seventeen of the 292 Wednesday cross-sections had only one contract expiration available; 141 had two; 129 had three; and five had four.

### B. Black/Scholes implied volatility patterns

To illustrate a typical pattern of Black/Scholes implied volatilities, we use bid and ask price quotes for call options19 during the 2:45-3:15 PM window on April 1, 1992 (a typical day) and compute implied volatilities20 based on the Black/Scholes call option valuation formula,

15 See Fleming, Ostdiek and Whaley (1995).

17 This is not quite true since we use Treasury bill rates in computing forward prices.

16 For a detailed description of the problems of using a reported index level in computing implied volatility, see Whaley (1994, Appendix).

18 To assess the reasonableness of using the 2:45-3:15 PM window for estimation, we computed the mean absolute return and the standard deviation of return of the nearby S&amp;P 500 futures (with at least six days to expiration) by fifteen-minute interval throughout the trading day across the days of the sample period.

The results indicated that the lowest mean absolute return and standard deviation of return occur just prior

to noon. The end-of-day window is only slightly higher, while the beginning-of-day window is nearly double. We chose to stay with the end-of-day window for ease in interpretation of the results.

reported index is always stale, we use only call options. While a stale index causes the implied volatilities

19 For this exercise only, we use the reported stock index level in the estimation of volatility. Since the


<!-- p:12 -->


$$c = F N ( d _ { 1 } ) - X N \left ( d _ { 2 } \right ) ,$$

where d, =[ln(F/ X)+.5σ2(T−t)]/σ√T-t, d2 =d1−σ√T-t, and N(.) is the cumulative normal density function. The pattern of implied volatilities is displayed in Figure 1. Note that these are the Black/Scholes implied volatilities and not a graph of the local volatility rates from the DVF option valuation model. The fact that the Black/Scholes implied volatilities do not fall on an horizontal line is "the evidence" that the Black/Scholes formula does not hold.

Several features in Figure 1 deserve comment. First, observe that implied volatilities corresponding to bid and ask quoted prices are closest together for at-themoney options. The divergence between bid and ask implied volatilities increases as moneyness moves away from 0, particularly to the left of the figure where the call options are deep in the money. This pattern arises for two reasons. First, although spreads are competitively determined, they tend to vary systematically with option moneyness. In part, this may be caused by the CBOE's rules governing the maximum spreads for options with different premia. The rules state that the maximum bid/ask spread is (a) 1/4 for options whose bid price is less than $2, (b) 3/8 for bid prices between $2 and $5, (c) 1/2 for bid prices between $5 and $10, (d) 3/4 for bid prices between $10 and $20, and (e) 1 for bid prices above $20.21 Second, the sensitivity of option price to the volatility parameter is highest for at-the-money options, with in-the-money and out-of-the-money having much lower sensitivity. This means that, for a given spread between the bid and ask price quotes, the range of Black/Scholes implied volatilities will be lowest for at-the-money we  e ne oe ae e  e e e e  e e szr Seco     ,   a  sa , -  ose prior to the October 1987 market crash when, in general, the Black/Scholes implied volatilities were symmetric around zero moneyness, with in-the-money and out-of-themoney options having higher implied volatilities than at-the-money options. The sneer pattern displayed in Figure 1, however, is more indicative of the pattern that has existed since the market crash, with call (put) option implied volatilities decreasing monotonically as the call (put) goes deeper out of the money (in the money).

of the calls to be biased downward or upward depending on whether the reported index is above or below its true level, the bias for all calls will be in the same direction. With puts, the bias is opposite.

21 See Obligations of Market-Makers, Rule 8.7 in Chicago Board Options Exchange (1995, pp. 2123-4).

20 For this illustration only, we do not enforce the moneyness criterion.

22To illustrate, consider the Black/Scholes implied volatilities of 30-day call options with different exercise prices, where all calls have a bid/ask spread of 1/4. Assume the index level is 400, the volatility rate of the index returns is 20 percent, and the interest rate is 5 percent. The spread between the implied volatilities based on bid and ask prices is 319 basis points for a call that is 10 percent in-the-money, 55

basis points for an at-the-money call, and 210 basis points for a call that is 10 percent out-of-the-money.


<!-- p:13 -->


Third, the sneer gets worse as the option's time to expiration grows small. For the calls with 45 and 80 days to expiration, the implied volatilities range between 10 and 22 percent. The 17-day calls, on the other hand, range up to nearly 30 percent. Indeed, this behavior provides the motivation for considering local volatility functions that are a function of time, particularly Models 2 and 3 in which time interacts with the level of asset price.

## III. Estimation Results

Using the S&amp;P 500 index option data described in the previous section, the four volatility functions specified in (3) are estimated. As noted earlier, Model 0 is the Black/Scholes constant volatility model. Model 1 allows the volatility rate to vary with index level but not with time. Models 2 and 3 attempt to capture additional variation due to time. A fifth volatility function, denoted Model S, is also estimated. Model S switches between the volatility functions given by Models 1, 2 and 3, depending on whether the number of different option expirations in a given cross-section is one, two, or three, respectively. Model S is introduced because a few cross-sections have little or no time-toexpiration variation, undermining our ability to estimate precisely the relation between the local volatility rate and time.

This section focuses on identifying the "best" volatility function given the structure of S&amp;P 500 index option prices. First, each local volatility function is estimated by mMmg   s oe es   sr s  us s t model values. Summary statistics on the goodness-of-fit are provided. Next, we examine the surface implied by the best-fitting volatility function and the implied probability functions for options of different times to expiration.


<!-- p:14 -->


### A. Goodness-of-fit

To assess the quality of the fitted models, two measurements are made each week. The root mean squared valuation error (RMSVE) is the square root of the average squared deviations of the reported option prices from the model's theoretical values. The average error (AVERR) is the average error outside the bid/ask spread. If the theoretical value is below (exceeds) the option's bid (ask) price, the error is defined as the difference between the theoretical value and the bid (ask) price, and, if the theoretical value is within the spread, the error is set equal to zero. A positive value of AVERR, therefore, means that the model value is too high on average, and a negative value means the model value is toolow.

Table 1 contains the average RMSVE's and average AVERR's across the 292 days (one day each week) during the sample period June 1988 through December 1993. Also reported is the frequency with which the specified model has a lower RMSVE than Model S (FREQ). The average RMSVE results indicate that there is a strong relation between the local volatility rate and the asset price. Where the volatility rate is a quadratic function asset price (Model 1), the average RMSVE of the DVF model is less than half of that of the Black/Scholes constant volatility model (Model 0), .301 vs. .650, for all options in the sample. Time variation also appears important. In moving from Model 1 to Model 2, the average RMSVE in the full sample is reduced further (i.e., from .301 to .230), albeit not as dramatically. The addition of the time variable to the volatility function appears to , of sdt nt xe ats t  nns t  o the cross-product term, XT.23 Adding a quadratic time to expiration term (Model 3) reduces the average RMSVE to its lowest level of the assumed specifications, .226. Model S's RMSVE is virtually the same. The average AVERR measurement criterion leads to the same conclusions for the overall sample.

23 Model 2 was also estimated without the time variable with little difference in explanatory power.


<!-- p:15 -->


The AVERR values reported for the Black/Scholes model (Model 0) show that the theoretical value exceeds the ask price on average for call options and is below the bid price for put options. This behavior arises from the character of our sample (i.e., the number of calls versus the number of puts, and the number of in-the-money options versus the number of out-of-the-money options). When the options are stratified by option type and moneyness, the Black/Scholes model value appears to be too low (relative to the bid price) for in-the-money calls and for out-of-the-money puts. This is consistent with the implied volatility sneer shown in Figure 1. With all options forced to have the same volatility in the estimation of Model O, the variation in implied volatility translates into valuation errors. Options with Black/Scholes implied volatilities higher (lower) than average are valued too low (high).

Figure 2 shows the valuation errors (i.e., model values less bid/ask midpoints) of Model 0 for call options with 40 to 70 days to expiration. Also shown are normalized bid/ask spreads (i.e., the bid/ask prices less the bid/ask midpoint). Note first that the bid/ask spreads are as high as one dollar for deep in-the-money calls on the left of the figure. As we move right along the horizontal axis, the maximum bid/ask spread stays at a dollar until the moneyness variable is about -2.5 percent, and then the maximum spread begins to decrease as the calls move further out-of-the-money. This spread behavior is consistent with the CBOE's maximum spread rules described earlier. The average bid/ask spread across all option series used in our estimation is approximately 47 cents.

Figure 3 shows the valuation errors of Model 3 for calls with 40 to 70 days to expiration. The DVF model improves the cross-sectional fit. Where the valuation errors are outside the bid/ask spread, they appear randomly, with a slight tendency for the DVF option valuation model to undervalue deep in-the-money and deep out-of-the-money calls and to overvalue at-the-money calls. Overall, however, Model 3's fit appears quite good. The AVERR across the moneyness categories is -.026 across all of the calls in this category, in contrast to an AVERR of more than .250 for the Black/Scholes model.

M t vln lt  l  l t svelld tn t ltn option's days to expiration. For the Black/Scholes model, the valuation errors generally increase with days to expiration. For deep in-the-money calls with less than 40 days to expiration, for example, the RMSVE is .313; .644 for calls between 40 and 70 days to expiration; and 1.051 for calls with more than 70 days to expiration. For the same call options, the RMSVE's for Model 3 are .259, .223 and .220, respectively.


<!-- p:16 -->


All in all, the evidence reported in Table 1 supports the notion that the more complex is the volatility function the better the DVF option valuation model fits the crosssection of reported option prices. Of the functions considered, Model 3 and Model S appear to be the "best"fitting.24

### B. Average parameter estimates and the implied local volatility surface

The average parameters estimated for each of the volatility function are also interesting. Model 0 is, of course, the constant volatility model of Black/Scholes. When this model was fitted each week during our 292-week sample period, the mean estimated coefficient, 0, was 15.72 percent. Figure 4 shows the level of the Black/Scholes implied volatility on a week-by-week basis. Over the sample period, implied market volatility fell from above 20 percent to below 10 percent. Volatility reached a maximum of 27.16 percent on January 16, 1991, the height of the Gulf War. The minimum implied volatility, 9.43 percent, occurred on December 29, 1993, the last date of the sample period.

Model 3 has six parameters in total, and the averages (standard deviations) of the model's six parameter estimates across the 292 cross-sections are as follows:

| ā = 131.824     | 1 = −.352941   |
|-----------------|----------------|
| (69.5)          | (.447)         |
| a2 =.0000861056 | á3 = −.226000  |
| (.000768)       | (1.94)         |
| ā = −.000166645 | ā =.0527528    |
| (.00237)        | (.0593)        |

The average implied index level over the period was about 370. To illustrate what these average values imply in terms of a volatility surface, we plot in Figure 5 the estimated function for a range of index levels and days to expiration. For a given number of days to expiration, the local volatility rate displays the sneer-like pattern that appeared for the Black/Scholes implied volatilities in Figure 1. As the index level rises, the volatility rate falls. With few days to expiration and high index levels, the volatility rate appears to reach its constrained minimum level of one percent. For a given index level, on the other hand, the local volatility rate increases slowly and linearly with days to expiration. At an index level of 320, for example, the local volatility rate rises from about 28 percent to 32 percent over the 100 day interval. The time variation, however, pales by comparison to the variation attributable to the index level.

24 To test if the estimation results were driven by the presence of outliers, we examined the valuation errors of the various models. We identified usually large errors in three days during the sample period. When we eliminated these days from the summary results, the magnitudes of the average errors reported in Table 1 were reduced, but the ordering of the average errors was the same. Consequently, we report the results for the full sample.


<!-- p:17 -->


The standard deviation of the parameter estimates indicates that there is con ie  s k  vatse ni  s ot tsaps that the volatility function is not stable through time. On the other hand, if the parameter estimates are highly correlated, the errors affecting them may cancel out when looking at option prices. To check this possibility, we computed the correlation among the parameter estimates across the 292 weeks in the sample period and report them below. As the values

|    |     â2 |        |     â4 |     âs |
|----|--------|--------|--------|--------|
| â  | -0.969 |  0.596 | -0.811 | -0.291 |
| â2 |        | -0.589 |  0.853 |  0.182 |
| â3 |        |        | -0.114 | -0.232 |
| â  |        |        |        |  0.093 |

show, the correlations are generally quite large. The correlation between the linear and quadratic terms in Model 3, for example, is -.969, indicating that in weeks where â, is high â2 is low and vice versa. What this evidence implies is that the economic significance of the DVF model should be measured in terms of valuation prediction errors, which is exactly the procedure applied in Section IV.


<!-- p:18 -->


### C. Implied probability distribution

The estimated coefficients of the volatility functions can also be used to deduce the shape of the risk-neutral probability distribution at the end of the options' lives.2s To illustrate, we first use the estimated coefficients of Model 3 on April 1, 1992. On April 1, 1992, the S&amp;P 500 options had three different expiration months, April, May, and June 1992, with 17, 45 and 80 days to expiration, respectively. Based upon these expirations, the estimated volatility function implies the three probability distributions shown in Figure 6. All distributions are skewed to the left, exactly the opposite of the right-skewness that one normally associates with the Black/Scholes assumption of lognormally-distributed asset prices. The wider variances for the May and then June expirations merely reflects the fact that the longer is the option's time to expiration, the greater is the probability of large asset price moves. Our implied distributions do not exhibit the bimodality that appeared in Rubinstein (1994). This likely results from the fact that our volatility functions are more parsimonious than that implicitly used within his binomial lattice framework.

## IV. Prediction Results

The estimation results reported in the last section indicate that as more parameters are added to the volatility function the DVF model explains more of the variation in the cross-section of reported S&amp;P 500 index option prices. Indeed, with as many parameters as cross-sectional option prices, the DVF model could describe the reported structure of option prices exactly. A critical assumption of the model, however, is that the volatility function is stable through time. In this section, we evaluate how well the volatility function estimated one week values the same options one week later.

### A. Goodness-of-fit

Table 2 provides the summary statistics of the prediction errors across all days in the sample. The RMSVE and AVERR values shown in the table are computed in the same manner as in the previous section. The prediction errors are generally quite large, at least relative to the estimation errors reported in Table 1. The average RMSVE is about 56 cents out-of-sample across all days for all DVF models except Model 0, while the insample error for these models is about 23 cents. The magnitude of the prediction error should not be surprising, however, in the sense that new market information presumably induces a shift in the level of overall market volatility from week to week.

25 The identification of state price densities from option prices has been the goal of much of David Bates' work: see Bates (1995a, b). See also Ait-Sahalia and Lo (1995).


<!-- p:19 -->


The prediction errors for calls and puts are about the same size. Like in the case of the estimation errors, the average AVERR for Model 0 is positive for calls and negative for puts. As noted earlier, this arises from the character of the sample. When the options are stratified by option type and moneyness, we see that the Black/Scholes model value is too low (relative to the bid price) for in-the-money calls and out-of-the-money puts and is too high (relative to the ask price) for out-of-the-money calls and in-the-money puts. This pattern is particularly clear in Figure 7, which is the analogue at the prediction stage, of Figure 2 at the estimation stage.

Interestingly, the average AVERR is smaller for Model 1 than for Models 2, 3, and S. This means that the time variable in the more elaborate volatility functions is unnecessary. Apparently, the time variable serves only to overfit the data at the estimation stage. The fact that the valuation prediction errors for the models that include the time variable are more negative than those of Model 1 indicates that the implied volatility functions predict more of a decrease in volatility over the week than actually transpires.

At-the-money options have the largest valuation prediction errors for all times to expiration. This arises because at-the-money options are the most sensitive to volatility (where time premium is highest). For a given error in the estimated volatility rate, the dollar valuation error is larger for at-the-money options than for either in-the-money or out-of-the-money options. Figure 8, which is the analogue of Figure 3, makes it plain that the prediction pricing errors of Model 3 do not display the characteristic patterns across the spectrum of moneyness that we identified above for Model 0.

### B. An "ad hoc"strawman

What is most troubling about the analysis thus far is that, although the RMSVE's seem large for all practical purposes, we have no real means for evaluating what size of pe s sre roer  o e   t,   s  oeod measure them against a benchmark. To account for the sneer patterns in Black/Scholes implied volatilities, many market makers simply smooth the implied volatility relation across exercise prices (and days to expiration) and value options using the smoothed relation. To operationalize this practice, we fit the Black/Scholes model to the reported structure of option prices each week using Model S to describe Black/Scholes implied volatility. Obviously, applying the Black/Scholes formula in this context is internally inconsistent since the Black/Scholes formula is based on an assumption of constant volatility. Nonetheless, the procedure is used in practice as a mean of predicting option prices.26 The DVF option valuation model, which is based on an internally consistent specification, should dominate this "ad hoc" approach.


<!-- p:20 -->


To create our strawman, we use a two-step procedure similar to the one we used for the DVF models. On day t, we fit Model S to the Black/Scholes implied volatilities, and then, on day t+7, we apply the Black/Scholes formula using the volatility levels from estimated regression. The valuation prediction errors computed in this fashion are also summarized in Table 2. As the table shows, the errors using the Ad Hoc Model are almost uniformly smaller than those of the DVF approach. The average RMSVE across the entire sample period is 49 cents for the ad hoc Black/Scholes procedure, where it is nearly 56 cents for the DVF (Model 1) option valuation model. In viewing the various option cattn -  n t rt ens an arns s ns whs     r s      s  ic volatility approach does not appear to be an improvement over the ad hoc, albeit theoretically inconsistent, procedure used in practice.

### V. Hedging Results

A key motivation for developing the DVF option valuation model is to provide better risk management. If volatility is a deterministic function of asset price and time, setting hedge ratios based on the DVF option valuation model should present an improvement over the constant volatility model. In this section, we evaluate hedging performance. To focus exclusively on valuation, we assume that the hedge portfolio is continuously rebalanced through time.27 The hedge portfolio is formed on day t and then unwound one week later.

26 The Black/Scholes procedure could not serve to predict American or exotic option prices from

European option prices, which is the major benefit claimed for the implied volatility tree approach.


<!-- p:21 -->


Under the continuous-rebalancing assumption, the hedging error is defined as:28

$$\varepsilon _ { t } = \Delta c _ { r o p o r t , t } - \Delta c _ { m o l , t } ,$$

where ∆creponed, is the change in the reported option price from day t until day t+7 and ∆cmode, is the change in the model's theoretical value. The proof is straightforward. The hedging error that results from the continuous rebalancing using the wrong model for the hedge ratio, h, is:

$$\Delta c _ { r o p a r t , t } - \overset { t + 7 } { \int } h ( S _ { \tau } , u ) d S _ { \tau } \, .$$

If we had the correct model, the two quantities in (8) would be equal to one another, not as a real number equality, but with probability one or at the very least in the sense that their difference would have an expected value of zero and zero variance. Therefore, it must be the case that the integral term equals ∆cmoda, . In other words, when the hedge is continuously rebalanced, the hedging error is simply equal to the time increment in the valuation error.

Table 3 contains a summary of the hedging error results. Across the overall sample period, Model 0—-the Black-Scholes constant-volatility model—performs best of all the deterministic volatility function specifications! Its average root mean squared hedging error (RMSHE) is .455, compared with .489, .506, .506, and .505 for Models 1 through 3 and Model S, respectively. The results indicate that, the more parsimonious is the volatility function, the better the hedging performance.

27 Here, we are not interested in the issues raised by discrete-time hedges.

28 Recall that c refers to option premium payable at maturity. When terminal currency units are used, as is the case here, we need not incorporate interest earnings on the riskless asset.


<!-- p:22 -->


The ad hoc Black/Scholes procedure described in the last section also performs well from a hedging standpoint. The average RMSHE is only .449. Consistent with the prediction results reported in Table 2, the DVF option valuation model does not appear to be an improvement. Better risk management results can be obtained using the ad hoc procedure.

## VI. Summary and Conclusions

Claims that the Black and Scholes (1973) valuation formula no longer holds in financial markets are appearing with increasing frequency. When the Black/Scholes formula is used to imply volatilities from reported option prices, the volatility estimates vary systematically across exercise prices and times to expiration. Derman and Kani (1994), Dupire (1994), and Rubinstein (1994) argue that this systematic behavior is driven by the fact that the volatility rate of asset return varies with the level of asset price and time. They hypothesize that volatility is a deterministic function of asset price and volatility and provide appropriate binomial or trinomial option valuation procedures.

In this paper, we apply the deterministic volatility option valuation approach to S&amp;P 500 index option prices during the period June 1988 through December 1993 and reach the following conclusions. First, the more flexible is the volatility function's specification, the better the DVF model fits in-sample. Indeed, because of the unlimited flexibility in specifying the volatility function, it is always possible to describe the reported structure of option prices exactly. Second, when the fitted volatility function is used to value options one week later, the DVF model's prediction errors grow larger as the volatility function specification becomes less parsimonious. In particular, specifications that include a time parameter do worst of all, indicating that the time variable is an important cause of the overfitting at the estimation stage. Third, hedge ratios determined by the Black/Scholes model appear more reliable than those obtained from the DVF option valuation model. In sum, "simpler is better."

Overall, our results suggest at least three possible lines for future investigation. First, the deterministic volatility framework could be generalized. The volatility surface, for example, may be related to past changes in the index level. Such a generalized volatility surface is probably the last candidate model that can be considered before resorting to fully stochastic volatility processes—processes which are difficult to estimate and do not permit option valuation by the absence of arbitrage.


<!-- p:23 -->


Second, the "smile" problem may not be a deficiency of the Black/Scholes model. After the October 1987 crash, portfolio insurers began buying exchange-traded index options to replace dynamic portfolio insurance schemes. Buying out-of-the-money index puts will surely drive Black/Scholes implied volatilities higher if no one is actively arbitraging according to the Black/Scholes model. With institutional buying pressure on out-of-the-money puts and no naturally offsetting selling pressure, index put prices rise to a level where market makers are eventually willing to step in and accept the bet that the index level will not fall below the exercise price before the option's expiration (i.e., they sell naked puts). So, even if the Black/Scholes model is correct, trading costs combined with option series clienteles may induce patterns in implied volatilities, with these patterns implying little in terms of the distributional properties of the underlying index.

Finally, thought should be given to appropriate statistical test designs for competing volatility structures. The "null hypothesis" being investigated is that volatility is an exact function of asset price and time, so that options can be valued exactly by the noarbitrage condition. Any deviation from such a strict theory, no matter how small, should cause a test statistic to reject it.29 If a source of error had been introduced, some restriction on the sampling distribution of the error could be deduced and could provide a basis for a testing procedure.30

29 The same difficulty arises in any empirical verification of an exact theory. See MacBeth and Merville (1979), Whaley (1982) and Rubinstein (1985).

3o Jacquier and Jarrow (1995) introduce two kinds of errors in the Black/Scholes model: model error and market error, which they distinguish by assuming that market errors occur rarely. Other approaches to the problem include Lo (1986) who introduces parameter uncertainty, Clément, Gouriéroux and Montfort (1993) who randomize the martingale pricing measure to account for an incomplete market and Bossaerts and Hillion (1994) whose error is due to discreteness in hedging.


<!-- p:24 -->

#### Valuation error

<!-- p:31 -->


Figure 3: Valuation estimation errors in dollars of Deterministic Volatility Function Model 3 for S&amp;P 500 call options with between 40 and 70 days to expiration during the period June 1988 through December 1993. The solid square dots correspond to normalized bid/ask price quotes (i.e., the bid and ask prices less the average of the bid and ask prices). The circle dots correspond to valuation errors (i.e., the theoretical option value less the bid/ask midpoint). Moneyness is defined as X / F – 1.

#### Valuation error

<!-- p:32 -->


Figure 4: Black/Scholes implied volatility estimated each week during the period June 1, 1988 through December 29, 1993 using S&amp;P 500 index option price quotes. Implied volatility is computed by minimizing the sum of squared errors between the reported bid/ask midpoints and theoretical option values.

## Volatility (%)

Time


<!-- p:33 -->


Figure 5: Volatility surface implied by the average of the coefficent estimates of Deterministic Volatility Function Model 3 during the sample period June 1988 through December 1993. Surface displays the local volatility rate for different index levels and different days to expiration.

<!-- p:34 -->


Figure 6: Risk-neutral probability density functions for April, May and June 1992 S&amp;P 500 option expirations on April 1, 1992. The probability distributions are based on the parameter estimates of Deterministic Volatility Function Model 3.

#### Probability

<!-- p:35 -->


Figure 7: Valuation prediction errors in dollars of Deterministic Volatility Function Model 0 (i.e., the Black/Scholes model) for S&amp;P 500 call options with between 40 and 70 days to expiration during the period June 1988 through December 1993. The theoretical values are based on the implied volatility function from the previous week. The solid square dots correspond to normalized bid/ask price quotes (i.e., the bid and ask prices less the average of the bid and ask prices). The circles correspond to valuation errors (i.e., the theoretical option value less the bid/ask midpoint). Moneyness is defined as X / F – 1.

#### Valuation error

<!-- p:36 -->


Figure 8: Valuation prediction errors in dollars of Deterministic Volatility Function Model 3 for S&amp;P 500 call options with between 40 and 70 days to expiration during the period June 1988 through December 1993The theoretical values are based on the implied volatility function from the previous week. The solid square dots correspond to normalized bid/ask price quotes (i.e., the bid and ask prices less the average of the bid and ask prices). The circles correspond to valuation errors (i.e., the theoretical option value less the bid/ask midpoint). Moneyness is defined as X / F – 1.

#### Valuation error
