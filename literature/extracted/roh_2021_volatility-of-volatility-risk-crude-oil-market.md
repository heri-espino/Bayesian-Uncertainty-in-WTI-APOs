---
id: "roh_2021_volatility-of-volatility-risk-crude-oil-market"
source_pdf: "../pdf/roh_2021_volatility-of-volatility-risk-crude-oil-market.pdf"
source_filename: "roh_2021_volatility-of-volatility-risk-crude-oil-market.pdf"
format: "academic-paper"
extraction_profile: "text-math-tables-high-fidelity"
extraction_mode: "hybrid"
extraction_quality: "excellent"
extraction_score: 100.0
visual_assets: "disabled"
references_file: "../references/roh_2021_volatility-of-volatility-risk-crude-oil-market.references.md"
---

<!-- p:1 -->

## Volatility-of-volatility risk in the crude oil market

Tai-Yong Roh 1 , Alireza Tourani-Rad 2 , Yahua Xu* ,3 , and Yang Zhao 4

#### Abstract

This paper examines the role of oil volatility-of-volatility (VOV) risk under a stochastic VOV framework. We show that oil VOV is a significant pricing factor  in the cross-sectional deltahedged gains constructed from oil options, and oil VOV also has predictive power for near-term delta-hedged option gains. Moreover, we show that the information contained in oil VOV is highly specific  compared  to  its  equity  counterpart  and  other  volatility-related  measures,  from  the perspective  of  its  predictability  of  future  economic  conditions.  Our  findings  are  robust  to alternative VOV risk measures and forecasting horizons.

Keywords : Crude oil market; Delta-hedged gains; Jump risk; Pricing implications; Stochastic volatility-of-volatility risk

1  Assistant professor, Li Anmin Institute of Finance and Economics, Liaoning University, No. 66 Chongshan Middle Road, Huanggu District, 110036 Shenyang, Liaoning Province, China.

2  Professor, Faculty of Business, Economics and Law, Auckland University of Technology, 42 Wakefield Street, 1010 Auckland, New Zealand.

3  Corresponding author: Assistant professor, China Economics and Management Academy, Central University of Finance  and  Economics,  No.  39  South  College  Road,  Haidian  District,  100081  Beijing,  China.  Phone:  +86  10

62888376. Fax: +86 10 62888376. Email: yahua.xu@cufe.edu.cn.

4  Assistant professor, Chinese Academy of Finance and Development, Central University of Finance and Economics, No. 39 South College Road, Haidian District, 100081 Beijing, China.


<!-- p:2 -->


#### JEL Classification : C1; G1; Q4

Acknowledgments: We are especially grateful to Robert Webb (editor) and to an anonymous referee for insightful comments that have significantly improved the paper. Alireza Tourani-Rad acknowledges the support of Czech Science Foundation (Project No. GA 20-00178S). Yang Zhao specially acknowledges the financial support from the National Natural Science Foundation of China  (Grant  No.  71801117,  71973162)  and  Program  for  Innovation  Research  in  Central University of Finance and Economics (Grant No. 20190092). All errors are those of the authors.


<!-- p:3 -->


### 1. Introduction

Despite the well-established strand of literature on the impact of stochastic volatility in financial asset pricing, from both theoretical and empirical perspectives (e.g., Ang et al., 2006; Campbell et al., 2018; Cao and Han, 2013; Heston, 1993; Hull and White, 1987), much less is known about the role of the uncertainty of volatility risk in asset pricing and investing decisions. In general, uncertainty of volatility that characterizes the distribution of time-varying volatility is empirically  measured  as  the  volatility-of-volatility  (VOV).  Intuitively,  VOV  also  carries important information about the investment opportunity set, as shocks to the economy cause sudden increases  in  VOV of the  market  portfolio,  which  eventually  affects  investors'  asset allocation  decisions.  This  argument  has  also  been  theoretically  supported  by  the  dynamic pricing framework of asset returns proposed by Huang et al. (2019), which incorporates both time-varying volatility as well as  the VOV risks. The analysis of VOV risk, however, is an underexplored topic, while being of great importance for researchers and practitioners.

Crude oil is used as a major input for production; fluctuations in the oil market have substantial impacts on the real economy (e.g., Ferderer, 1996; Elder and Serletis, 2010; Hamdi et  al.,  2019;  Herrera  et  al.,  2019).  It  is  further  widely  acknowledged  that  oil  volatility  has significant effects on financial markets, such as the stock market (e.g., Feng et al., 2017), the bond market (e.g., Kang et al., 2014), and the credit market (e.g., Bouri et al., 2018). The crosssectional analysis of Christoffersen and Pan (2018) finds that stocks with higher exposure to oil volatility  risk  earn  lower  average  returns,  and  vice  versa.  These  studies  highlight  the fundamental  significance  of  the  crude  oil  market,  and  thus  the  uncertainty  of  oil  market volatility, measured as oil VOV, can also be an important risk factor affecting consumption and production decisions. In this paper, we aim to analyze whether aggregate VOV risk in the crude oil market is priced by the delta-hedged gains of United States Oil Fund (USO) options and whether oil VOV contains information that is distinct from that of its equity counterpart. 5


<!-- p:4 -->


Our research is related to the growing body of asset pricing literature on VOV risk, whose economic implications have been less frequently examined until recently. Bollerslev et al. (2009) incorporate stochastic VOV risk into the long-run risk model of Bansal and Yaron (2004)  and  they    show  that  VOV  risk  drives  the  time-varying  variance  risk  premium  and contributes to the prediction of future equity index market returns. More recently, Chen et al. (2017) confirm the important role of VOV as a state variable that is significantly priced in the cross section of stock returns by developing a macroeconomic model that incorporates VOV risk as a pricing factor. In addition, several empirical papers have recently explored the crosssectional implications of VOV risk in various settings, such as individual stocks (e.g., Baltussen et al., 2018), the equity index (e.g., Hollstein and Prokopczuk, 2018), and hedge funds (e.g., Agarwal et al., 2017). More recently, a few studies have examined the relation between VOV risk and options. Huang et al. (2019) extend the analysis of VOV as a risk factor to the Standard &amp; Poor's (S&amp;P) 500 and Chicago Board Options Exchange (CBOE) Volatility Index (VIX) option markets. Cao et al. (2018) investigate the cross-sectional effects of VOV risk in future delta-hedged equity index option returns. Ruan (2020) focuses on the significantly negative relation between VOV risk and the cross section of equity option returns. However, so far, the role of VOV in the crude oil market remains unknown.

5  The USO is one of the largest and most liquid crude oil exchange-traded funds (ETFs).


<!-- p:5 -->


Our analysis extends the earlier discussions to the crude oil market by incorporating its VOV, while most previous work is confined to stochastic volatility. For instance, Chiang et al. (2015)  show  that  a  latent  stochastic  volatility  factor  is  significantly  related  to  key  macro variables and is thus a significant pricing factor. Prokopczuk et al. (2017) observe a negative oil  volatility  risk  premium  by  looking  at  the  average  of  a  synthetic  variance  swap  rate constructed from oil futures options. Even though recent studies have identified the important role of VOV risk in the equity markets, the question of whether VOV risk retains the same significance in the crude oil market has not yet been explored.

To test  our  hypothesis, we  first  construct  the  VOV  measure  using  the  exponentially weighted moving average (EWMA) model with the CBOE Crude Oil Volatility Index (OVX). 6 Next, we compare our findings with equity index volatility and VOV risks. The equity market volatility index and VOV index are proxied by VIX and VVIX, respectively. 7 The correlation is  much  lower  between  the  oil  and  equity  index  VOV  than  between  oil  and  equity  market volatility,  indicating  that  oil  and  equity  VOV  risks  contain  distinct  information  than  their volatility counterparts.

Our research is the first  attempt  to  investigate  whether  uncertainty  about  oil  market volatility is priced in the cross section of oil option returns. Bakshi et al. (2003) conduct a similar study on whether volatility risk is cross-sectionally priced in delta-hedged gains of S&amp;P 500 options.  Huang et al. (2019) analyze the equity market VOV and option returns associated with the S&amp;P 500 and VIX, and they also provide a testable model in which the expected deltahedged gains can be expressed as a sum of the market price of risk and compensations for volatility  and  VOV risks.  Hollstein  and  Prokopczuk  (2018)  also  confirm  that  the  aggregate VOV risk is priced in the cross section of equity returns and has negative predictive power for the future volatility and VOV. We adopt the methodology of Huang et al. (2019) to test whether oil volatility and VOV risks are cross-sectionally priced in delta-hedged USO option returns. 8

6 The OVX, or 'oil VIX,' measures the volatility of the crude oil market over the next one month.

7 The VIX is a forward measure of the stock market's expected volatility over the next month. The VVIX represents the expected volatility in the one-month-ahead price of the VIX.


<!-- p:6 -->


We further investigate the predictive power of VOV risk in the crude oil market. To do so, we run a set of time-series regressions controlling for various jump measures. We find that both oil market volatility and VOV risks significantly and negatively predict the one-monthahead delta-hedged gains of USO options, consistent with previous studies of equity index and VIX markets (e.g., Huang et al., 2019). We also conduct several robustness tests by adopting a different construction method for VOV risk and considering a one-week forecasting horizon by using weekly USO options.

We further identify the specific information content on oil VOV from the perspective of its predictability for future economic. More specifically, we find that higher oil VOV leads to lower personal consumption and higher financial stress level by investigating forecasting ability of oil VOV on one-month-ahead growth rate of real personal consumption expenditure (RPCE) and  Kansas  City  Financial  Stress  Index  (KCFSI),  respectively.    In  sum,  oil  VOV  contains unique market information that cannot be covered by its equity counterpart and other volatilityrelated measures.

8  Because ETFs and equity have a similar structure, USO options can provide equity option-like features, which are simpler than options on West Texas Intermediate (WTI) crude oil futures.


<!-- p:7 -->


Our paper contributes to the literature in several  respects. First, we construct the oil market's VOV measure using the EWMA model with the OVX index. Second, we examine how oil VOV risk is priced in delta-hedged option gains. Studies related to our analysis include Baltussen et al. (2018) and Agarwal et al. (2017) who find that VOV is an important factor in explaining cross-sectional returns of stocks and hedge funds, respectively. Third, we find that oil  VOV negatively predicts future delta-hedged gains of USO options,  consistent with the findings of Huang et al. (2019) in the equity index market. Fourth, the specific information content of oil VOV can be demonstrated by its predictability for future economic conditions. To the best of our knowledge, our work represents the first effort to comprehensively examine the VOV risk in the crude oil market by providing both cross-sectional and time-series evidence.

The remainder of this paper proceeds as follows. Section 2 describes the data and key variables. Section 3 describes the empirical analysis, including the results of testing the market price of oil VOV risk and its specific information content. Section 4 reports a set of robustness tests in which we consider jump risks, alternative measure of oil VOV, and one-week USO delta-hedged gains. Finally, Section 5 concludes the paper.

### 2. Data and Key Variables

#### 2.1. Data Information


<!-- p:8 -->


The  empirical  analysis  spans  from  July  2010  to  June  2018.  We  use  the  USO  option  data obtained from the Thomson Reuters Tick History of Eikon to construct the delta-hedged gains. 9 Before  our  calculation,  we  filter  out  option  data  with  incomplete  or  incorrect  information. Specifically, we remove options with a zero close bid, a close ask greater than the close bid, prices  violating  the  standard  no-arbitrage  condition,  or  a  Black-Scholes-implied  volatility greater than 100% or less than 1%. The following analysis mainly focuses on delta-hedged gains obtained from one-month options. Weekly USO options were launched in July 2010, and we also construct delta-hedged gains using weekly options for a robustness check to compare with their one-month results. Moreover, we use the five-minute intraday prices of the USO exchangetraded funds (ETFs) obtained from Thomson Reuters DataScope Select to calculate the modelfree jump measures proposed by Barndorff-Nielsen et al. (2004) and Barndorff-Nielsen and Shephard  (2006).  The  risk-free  rates  are  proxied  by  the  London  Interbank  Offered  Rate, obtained from Federal Reserve Economic Data (FRED) offered by the Federal Reserve Bank of St. Louis. 10

#### 2.2. Key Variable Definitions

##### 2.2.1. Volatility-of-Volatility (VOV) Measures

9  Compared to options written on crude oil futures, ETF option data have the advantage of an equity option-like structure, which is much simpler.

10 https://www.stlouisfed.org.


<!-- p:9 -->


We adopt the OVX as a proxy for crude oil market volatility, which measures the 30-day-ahead volatility of the market. 11 We then construct the oil VOV measure, denoted by vovt 2 , by using the EWMA model with the OVX index: 12

$$\ v o v _ { t } ^ { 2 } = \lambda v o v _ { t - 1 } ^ { 2 } + ( 1 - \lambda ) u _ { t - 1 } ^ { 2 } ,$$

where ut is  the  logarithm  of  the  gross  return  of  the  OVX  (i.e., ln ( OVXt OVXt-1 ) ), vovt is  the conditional volatility of the gross OVX return, and λ is the degree of the weighting decrease, which is set at 0.94 here.

##### 2.2.2. Delta-Hedged Option Gains

A  delta-hedged  option  portfolio  consists  of  longing  an  option  and  shorting  delta  units,  as implied by the option, of its underlying stock, with net income invested at the risk-free rate. It is worthwhile to note that the gains of such a portfolio are thus insensitive to changes in the prices of the underlying stock.

Let C(t, τ, K) denote the price at time t of a call option with time to maturity τ and strike price K and  let  the  corresponding  option  delta  be  represented  by Δ(t, τ, K) (i.e., Δ(t, τ, K) ≡ ∂C(t,τ,K) ∂St ). Then, the delta-hedged gains, denoted by πt,t+τ , can be expressed as

$$\pi _ { t , t + \tau } = C _ { t + \tau } - C _ { t } - \int _ { t } ^ { t + \tau } \Delta _ { u } d S _ { u } - \int _ { t } ^ { t + \tau } r _ { u } ( C _ { u } - \Delta _ { u } S _ { u } ) d u \, ,$$

11  The OVX is the oil VIX. The construction method of the OVX is similar to that for the VIX.

12 The EWMA model is widely used in practice because of its simplicity and less restrictive data requirements.


<!-- p:10 -->


where St denotes the price at time t of the underlying stock and r t denotes the risk-free rate at time t . For compactness, we denote C(t, τ, K) and Δ(t, τ, K) as Ct and Δt , respectively.

#### 2.3. Summary Statistics

##### 2.3.1. Volatility-Related Variables

Table 1 reports the descriptive statistics for crude oil market volatility ( vol ), crude oil market VOV ( vov ),  equity market volatility (VIX), and equity market VOV (VVIX). 13 Notably, vov exhibits much greater skewness and kurtosis than the other variables, suggesting that oil VOV is highly asymmetric.

##### [Insert Table 1 here]

Table 2 reports the cross-sectional correlations between the variables. The correlation between  oil  market  volatility  ( vol )  and  VOV  ( vov )  is  0.250,  suggesting  that  limited  comovement  between  volatility  and  VOV  exists  in  the  crude  oil  market.  This  result  is  also consistent with the time-series plots of vol and vov , as depicted in Figure 1. Interestingly, the spikes exhibited by vol and vov reveal markedly different patterns. Moreover, the correlation between oil market volatility ( vol ) and equity market volatility (VIX) is 0.493, much higher than the correlation between oil market VOV ( vov ) and equity market VOV (VVIX), which is around 0.169. This result highlights the fact that volatility and VOV risks in the crude oil and equity markets contain distinct information.

13 We also incorporate equity market volatility and VOV risks here for comparison with their crude oil market counterparts.


<!-- p:11 -->


[ Insert Table 2 here ]

[ Insert Figure 1 here ]

##### 2.3.2. Statistical Properties of Delta-Hedged Gains

We next consider the discrete-time counterpart of Equation (2), with daily rebalancing:

$$\pi _ { t , t + \tau } = C _ { t + \tau } - C _ { t } - \sum _ { n = 0 } ^ { N - 1 } \Delta _ { t _ { n } } ( S _ { t _ { n + 1 } } - S _ { t _ { n } } ) - \sum _ { n = 0 } ^ { N - 1 } r _ { t _ { n } } ^ { f } ( C _ { t } - \Delta _ { t _ { n } } S _ { t _ { n } } ) \frac { \tau } { N } ,$$

where Δtn is the option delta on day tn , implied by the model of Black and Scholes (1973), and N is the total number of trading days from time t to t + τ .

Table 3 reports the descriptive statistics for unscaled delta-hedged gains (i.e., π t,t+τ ) and scaled  delta-hedged  gains  (i.e., πt,t+τ St ) constructed  on  one-month  USO  call  and  put  options, grouped by moneyness (i.e., St e r τ K ). On average, both unscaled and scaled delta-hedged gains are significantly negative over all ranges of moneyness, suggesting that the strategies lose money, which is consistent with previous findings for the equity markets (e.g., Bakshi and Kapadia, 2003; Cao and Han, 2013; Carr and Wu, 2009).

[ Insert Table 3 here ]


<!-- p:12 -->


We observe that, in most cases, the magnitudes of the delta-hedged gains decrease when going deeper in or out of the money. Considering put options with moneyness m ∈ [0 . 900 , 0 . 925] versus put options with moneyness m ∈ [0 . 975 , 1 . 000], we can observe that the averages of the unscaled delta-hedged gains are -$0.068 versus -$0.071, and the averages of the scaled deltahedged gains are -0.19% versus -0.21%. The curve for vega (i.e., ∂Ct ∂σt ) is concave, that is, it peaks for  at-the-money  (ATM)  strikes  and  tends  to  decrease  for  away-from-the-money  strikes,  as depicted in Figure 2. This suggests that the impact of volatility risk decreases for away-from-themoney options. However, we also observe that the unscaled delta-hedged gains for put options with moneyness m ∈ [0 . 925 , 0 . 950] are -$0.076, and the scaled delta-hedged gains are -0.20%, on average, where the former is greater than and the latter is similar to their ATM counterparts. This result is inconsistent with the decreasing magnitude of vega for away-from-the-money options. The curve of volga (i.e., ∂ 2 Ct ∂σ t 2 ) is convex around the near-the-money range, as presented by Figure 2, which reaches its lowest point for ATM strikes, and tends to increase when moving away from moneyness equal to one. This result suggests increasing VOV risk for away-from-the-money

options.

##### [ Insert Figure 2 here ]

We further find that the losses of delta-hedged portfolios increase with extended hedging horizons. This is easily observed from the delta-hedged gains constructed on one-week USO options,  reported  in  Table  4.  For  example,  for  the  call  option  groups  with  moneyness m ∈ [0 . 975 , 1 . 000], the average of unscaled delta-hedged gains (i.e., πt,t+τ ) is -$0.031 for the oneweek and -$0.056 for one-month options, respectively. We observe similar patterns for options in  other  moneyness  groups.  Thus,  delta-hedged  gains  tend  to  increase  with  longer  hedging horizons.


<!-- p:13 -->


[ Insert Table 4 here ]

Overall, the delta-hedged gains are negative for all options in the crude oil market, and the non-monotonic changes of the delta-hedged gains with respect to moneyness indicate the possible impacts of both volatility and VOV risks in the crude oil market.

### 3. Empirical Analysis

Previous studies find that returns of the delta-hedged strategy in the equity markets are negative (e.g., Bakshi and Kapadia, 2003; Carr and Wu, 2009). Bakshi and Kapadia (2003) confirm the significant impact of volatility risk on negative delta-hedged gains in the equity index market. Recent work by Huang et al. (2019) shows that in the equity index market VOV risk also plays a significant role in pricing delta-hedged gains. However, the question of how the delta-hedged strategy performs in the crude oil market and whether the corresponding volatility and VOV risks significantly affect the portfolio gains remains unexplored.

#### 3.1. Delta-Hedged Gains and Stochastic Volatility-of-Volatility Risk

##### 3.1.1. Stochastic Volatility-of-Volatility Model

Following the framework of Huang et al. (2019), which incorporates time-varying volatility and VOV risks, the dynamics of the underlying price St under the physical measure P is such that

$$\frac { d S _ { t } } { S _ { t } } = \mu ( S _ { t } , v _ { t } , \eta _ { t } ) d t + \sqrt { v _ { t } } d \omega _ { t } ^ { 1 } ,$$


<!-- p:14 -->


$$d v _ { t } = \theta ( v _ { t } ) d t + \sqrt { \eta _ { t } } d \omega _ { t } ^ { 2 } ,$$

$$d \eta _ { t } = \gamma ( \eta _ { t } ) d t + \phi \sqrt { \eta _ { t } } d \omega _ { t } ^ { 3 } ,$$

where (ωt 1 , ω t 2 , ω t 3 ) t≥0 is a three-dimensional Brownian motion with the correlation coefficient corr(dωt i , dω t j ) = ρij , for all i  ≠ j , vt denotes the stochastic variance of immediate returns, and ηt denotes  the  variance  of  innovation  in vt ,  which  follows  an  autonomous  stochastic process.

Based  on  this  framework,  the  expected  value  of  the  delta-hedged  gain  (i.e., πt,t+τ ) depends on the risk premiums of volatility and VOV risks, as shown by

$$E _ { t } [ \pi _ { t , t + \tau } ] = \int _ { t } ^ { t + \tau } E _ { t } \left [ \lambda _ { u } ^ { \nu } \frac { \partial C _ { u } } { \partial v _ { u } } \right ] d u + \int _ { t } ^ { t + \tau } E _ { t } \left [ \lambda _ { u } ^ { \eta } \frac { \partial C _ { u } } { \partial \eta _ { u } } \right ] d u \, ,$$

η denote the compensation for stochastic volatility and VOV risks, respectively.

Moreover, ∂vu ∂ηu

where λt v and λ t ∂Cu and ∂Cu represent the vega and volga of the call option, respectively.

Furthermore, assuming that the risk premiums (i.e., λt v and λ t η ) have a linear structure, the scaled expected delta-hedged gain is linear with respect to the fundamental factors:

$$\frac { E _ { t } [ \pi _ { t , t + \tau } ] } { S _ { t } } = \lambda ^ { v } \beta _ { t } ^ { v } v _ { t } + \lambda ^ { \eta } \beta _ { t } ^ { \eta } \eta _ { t } ,$$


<!-- p:15 -->


where βt v and β t η represent the options' exposure to volatility risk and VOV risk, respectively. For more details about the expressions βt v and β t η and corresponding derivations, see Appendix A.1.

Overall, under the stochastic volatility and VOV pricing framework proposed by Huang et al. (2019), the expected value of the delta-hedged gains compensates for both volatility and VOV risks. Moreover, if restrictions in the linear structure are placed on the risk premiums, the scaled delta-hedged gains are also linear with respect to volatility and VOV risks. We conduct corresponding empirical analysis in the following section.

##### 3.1.2. Cross-Sectional Analysis

The stochastic VOV model implies that options with higher exposure to volatility and VOV risks should have a higher negative payoff. To empirically verify this justification, we follow the extant literature (e.g., Bakshi and Kapadia, 2003; Huang et al., 2018) and employ the option greeks (i.e., vega and volga) implied by the model of Black and Scholes (1973) to proxy for option volatility and VOV risk betas. Then, we adopt the following econometric specification to check the cross-sectional implications of delta-hedged option gains on volatility and VOV risks:

$$G a i n s _ { t , t + \tau } ^ { i } = \Phi _ { 1 } V e g a _ { t } ^ { i } + \Phi _ { 2 } V o l g a _ { t } ^ { i } + \gamma _ { t } + \epsilon _ { t , t + \tau } ^ { i } ,$$

where we define scaled delta-hedged gains as Gainst,t+τ i ≡ πt,t+τ i St .  We also denote the option vega and volga implied by Black and Scholes (1973) as Vegat i and Volgat i , respectively. Let i


<!-- p:16 -->


represent  the  moneyness  range  ( i = 1,2, ... , I )  corresponding  to  the  option  groups  shown  in Table 3. We use γt to denote the time-fixed effects.

Table 5 reports the cross-sectional evidence from the regressions of the average scaled delta-hedged  gains  (i.e., Gains i )  on  option  volatility  and  VOV  risk  betas.  The  univariate estimate for vega is significantly negative, with a value of -0.058 and a t-statistic of -4.80. The negative  volatility  premiums  in  the  crude  oil  market  are  consistent  with  those  in  previous findings (e.g., Bakshi and Kapadia, 2003; Bardgett et al., 2019; Bollerslev et al., 2011). The second  row  shows  the  univariate  estimate  for  volga,  which  is  insignificant.  The  third  row presents the multivariate regression including both vega and volga. Both estimates are negative and statistically significant at the 1% level; the slope of vega is -0.119, and the corresponding t -statistic is -7.22; the slope of volga is -0.020, and the corresponding t -statistic is -5.38. 14  The negative price of VOV risk in the crude oil market is consistent with that in the equity index market as reported by Huang et al. (2019). In sum, the cross-sectional evidence indicates that both volatility and VOV risks are negatively and significantly priced in the crude oil market.

[ Insert Table 5 here ]

##### 3.1.3. Time-Series Analysis

Under the stochastic VOV model, we can see that time variations in the expected delta-hedged gains  are  driven  by  time-varying  volatility  and  VOV  risks.  Thus,  we  adopt  the  following econometric specification to examine the impacts of both risks on the time variations in scaled delta-hedged gains:

14 We scale both slopes by 1,000 here.


<!-- p:17 -->


$$G a i n s _ { t , t + \tau } ^ { i } = \Phi _ { 0 } + \Phi _ { 1 } v o l _ { t } ^ { 2 } + \Phi _ { 2 } v o v _ { t } ^ { 2 } + G a i n s _ { t - \tau , t } ^ { i } + u ^ { i } + \epsilon _ { t + \tau } ^ { i } ,$$

where we include the moneyness group fixed effects u i to  account  for  heterogeneity  in  the sensitivity of options in various moneyness bins to the underlying volatility and VOV risks. volt represents  oil  market  volatility, vovt represents  oil  market  VOV,  and Gainst-τ,t i represents one-month-lagged delta-hedged gains, with i as the moneyness ranges of the USO options.

[ Insert Table 6 here ]

The results are reported in Table 6. The first column shows the results for the case in which vovt 2 is a single predictor. It significantly predicts one-period-ahead delta-hedged gains, with a negative coefficient of -0 . 894 and a t -statistic of -7.83, consistent with the results of cross-sectional analysis. The second column of Table 6 is a joint prediction model incorporating both volt 2 and vovt 2 ,  and  it  shows  that  the  coefficients  of  both  are  negative  and  highly significant. The findings for the crude oil market are very similar to those for the equity index market, as demonstrated by Bakshi and Kapadia (2003) and Huang et al. (2019). Overall, the time-series  evidence  also  indicates  that  both  volatility  and  VOV  risks  are  negatively  and significantly priced in the crude oil market.

#### 3.2. The Information Contained in Oil Volatility-of-Volatility Risk


<!-- p:18 -->


So far, we have confirmed that both oil volatility and VOV risks are significantly and negatively priced in the USO option market, and this section builds on previous research by Huang et al. (2019)  that  focuses  on  the  relationship  between  equity  volatility  and  VOV  risks  and  deltahedged S&amp;P 500 option gains. Uncertainty about oil volatility could also affect financial market conditions and the real economy because economic decisions in a state with high oil market volatility are largely different from those in a state with low oil market volatility. In this section, we further explore whether the information content of oil VOV is distinct from its equity market counterpart  and  oil  volatility,  from  the  perspective  of  its  predictability  for  future  economic conditions. 15

##### 3.2.1. Economic Conditions: Consumption Growth and Financial Stress Level

Oil  prices  have  significant  impacts  on  the  U.S.  economy.  Intuitively,  oil  prices  influence production  and  manufacturing  costs,  which  ultimately  affects  business  and  consumption. Meanwhile, because of the rapid development of new technology allowing extraction of oil and natural gas from shale deposits, the U.S. has become a major oil-producing economy, therefore, fluctuations in oil prices also affect banking and finance based on the changing financial needs of oil companies. In sum, oil prices affect the U.S. economy in two ways: the rapid development of the oil industry has positive impacts on banking and finance and lowers consumption and business costs. We thus analyze the predictive relationships between oil market VOV and future economic conditions, such as the growth rate of RPCE and the financial stress level proxied by KCFSI. 16 Specifically, we run the following predictive regression:

15  It has been shown that the volatility risk of the oil and equity markets differ, and both are important pricing factors (e.g., Christoffersen and Pan, 2018; Gao et al., 2018).


<!-- p:19 -->


$$y _ { t + 1 } = \alpha + \beta _ { h } ^ { 1 } v o v _ { t } ^ { 2 } + \beta _ { h } ^ { 2 } v o l _ { t } ^ { 2 } + \beta _ { h } ^ { 3 } V V I X _ { t } ^ { 2 } + \beta _ { h } ^ { 4 } y _ { t } + \gamma _ { h } ^ { \prime } x _ { t } + \epsilon _ { t } ,$$

where y stands for the economic variables of interest (i.e., RPCE and KCFSI), vov represents the oil market VOV, vol is the oil market volatility, VVIX is the equity market VOV, and x is the  vector  of  fundamental  economic  variables,  including  the  term  spread  (TS),  the  default spread (DS), and the log dividend-price ratio (DP).

The results are reported in Table 7. Oil VOV ( vov ) negatively forecasts the growth rate of consumption,  indicating  that  it  contains  different  information  from  other  volatility-related variables, such as oil volatility ( vol ) and equity VOV ( VVIX ). These results imply that oil VOV could be closely related to the real economy, and fluctuations in oil volatility have a negative and significant effect on consumption growth. One possible reason for this is that higher fluctuations in oil volatility may lower consumption of durable goods (Elder and Serletis, 2010). Moreover, higher uncertainty in oil volatility may affect consumer spending because it raises uncertainty about employment, and thus people increase their precautionary savings (Edelstein and Kilian, 2009).  Additionally,  the  influence  of  commodity  markets  on  the  global  financial  market  has increased because of the financialization of commodity futures markets starting in 2004-2005. These motivate us to investigate the predictive power of oil VOV on the financial market stress level. 17 We find that both oil and equity VOV significantly and positively predict one-monthahead  KCFSI  with  corresponding  t-statistics  of  2.58  and  4.06,  respectively.  Our  finding  is consistent with that of Nazlioglu et al. (2015), that downturns in the oil market tend to depress economic  activity,  which  negatively  affects  banking  and  finance  and  subsequently  increases financial stress. In fact, previous research such as Nazlioglu et al. (2015) has provided mixed evidence on the relationship between the oil market and the financial market, and our findings contribute to this strand of the literature.

16  The Kansas City Financial Stress Index (KCFSI) is a monthly measure of stress in the U.S. financial system based on 11 financial market variables and can be obtained from Federal Reserve Economic Data (FRED).


<!-- p:20 -->


Overall, oil VOV contains specific predictive information on economic conditions, in that higher oil VOV can significantly predict a lower growth rate in personal consumption and higher financial stress in the near term.

[ Insert Table 7 here ]

### 4. Robustness

#### 4.1. Robustness Check: Control for Jump Risks

Under the stochastic VOV model, as specified by Equations (4)-(6), jump risk is not considered; however, as demonstrated in previous research, adding jumps can improve the performance of pricing models (e.g., Bakshi et al., 1997; Bates, 1996; Duffie et al., 2000). In this section, we introduce  jump  risk  to  the  model,  which  considers  the  impacts  of  stochastic  volatility  risk, stochastic VOV risk, and jump risk. We can thus further investigate whether the pricing role of oil VOV is affected by jumps.

17  For further discussion about the effects of the financialization of commodity futures markets, see Tang and Xiong (2012) .


<!-- p:21 -->


##### 4.1.1. Stochastic Volatility-of-Volatility Model with Jumps

As shown by Huang et al. (2019), if jump risk is considered, the dynamics of underlying price St under the physical measure P is

$$\frac { d S _ { t } } { S _ { t } } = \mu ( S _ { t } , v _ { t } , \eta _ { t } ) d t + \sqrt { v _ { t } } d \omega _ { t } ^ { 1 } + ( e ^ { x } - 1 ) d q _ { t } - \mu _ { J } \Lambda _ { J } \sqrt { v _ { t } } d t ,$$

$$d v _ { t } = \theta ( v _ { t } ) d t + \sqrt { \eta _ { t } } d \omega _ { t } ^ { 2 } ,$$

$$d \eta _ { t } = \gamma ( \eta _ { t } ) d t + \phi \sqrt { \eta _ { t } } d \omega _ { t } ^ { 3 } .$$

The jump term follows a Poisson process with volatility-independent intensity ΛJ√vt . We use x to  denote  the  jump  size  and q to  represent  its  corresponding  physical  density.  We  further assume that the mean of e x -1 is μJ , so the compensator is μJΛJ√vtdt .

Therefore,  the  expected  delta-hedged  gain  (i.e., πt,t+τ )  under  physical  measure P compensates for stochastic volatility, VOV, and jump risks, as shown by

$$E _ { t } [ \pi _ { t , t + \tau } ] = \int _ { t } ^ { t + \tau } E _ { t } \left [ \lambda _ { u } ^ { v } \frac { \partial C _ { u } } { \partial \nu _ { u } } \right ] d u + \int _ { t } ^ { t + \tau } E _ { t } \left [ \lambda _ { u } ^ { \eta } \frac { \partial C _ { u } } { \partial \eta _ { u } } \right ] d u + \mu _ { J } ^ { * } \Lambda _ { J } \int _ { t } ^ { t + \tau } E _ { t } \left [ \sqrt { \nu _ { u } } S _ { u } \frac { \partial C _ { u } } { \partial S _ { u } } \right ] d u$$

$$- \Lambda _ { J } \int _ { t } ^ { t + \tau } \sqrt { v _ { u } } \left [ \int _ { - \infty } ^ { \infty } C ( S _ { u } e ^ { x } ) q ( x ) ^ { * } d x - \int _ { - \infty } ^ { \infty } C ( S _ { u } e ^ { x } ) q ( x ) d x \right ] d u .$$


<!-- p:22 -->


In sum, if stochastic volatility, VOV, and jump risks are considered in the dynamics of underlying asset St , the expected delta-hedged gains compensate for all three risks. For more details about the derivation, see Appendix A.2.

##### 4.1.2. Jump Risk Measures

If  jump  risk  is  considered,  as  shown  in  Equation  (16),  the  delta-hedged  gain  could  also  be attributed to the large, discontinuous jumps in the underlying prices, apart from compensation for the VOV risk. To address concerns about whether the effect of VOV risk is robust to the presence of jump risk, we adopt two measures of jump risk.

The first jump measure is risk-neutral skewness and kurtosis, because jump risk can be proxied by the skewness and kurtosis of the underlying return distribution (e.g., Bakshi et al., 2003; Bates, 2000; Jackwerth and Rubinstein, 1996), in which the former is closely related to jump size, and the latter is closely related to jump intensity. We construct risk-neutral skewness and kurtosis using the model-free approach of Bakshi et al. (2003). Specifically, the higherorder risk-neutral moments can be spanned by a set of out-of-money calls and puts,

$$\ s k e w _ { t , t + \tau } = \frac { e ^ { r \tau } W _ { t , t + \tau } - 3 \mu _ { t , t + \tau } e ^ { r \tau } V _ { t , t + \tau } + 2 \mu _ { t , t + \tau } ^ { 3 } } { \left [ e ^ { r \tau } V _ { t , t + \tau } - \mu _ { t , t + \tau } ^ { 2 } \right ] ^ { 3 / 2 } } ,$$

$$k u r t _ { t , t + \tau } = \frac { e ^ { r \tau } X _ { t , t + \tau } - 4 \mu _ { t , t + \tau } e ^ { r \tau } W _ { t , t + \tau } + 6 e \mu _ { t , t + \tau } ^ { 2 } V _ { t , t + \tau } - 3 \mu _ { t , t + \tau } ^ { 4 } } { \left [ e ^ { r \tau } V _ { t , t + \tau } - \mu _ { t , t + \tau } ^ { 2 } \right ] ^ { 2 } } ,$$

where Vt,t + τ , Wt,t + τ , and Xt,t + τ are based on the prices of volatility and cubic and quartic contracts, respectively, and μt,t + τ is a function of them. Detailed expressions are in Appendix Section A.3.

The second jump measure is constructed by applying the model-free methodology of Barndorff-Nielsen et al. (2004) and Barndorff-Nielsen and Shephard (2006) to high-frequency USO prices. According to Barndorff-Nielsen et al. (2004), the realized variance, the sum of squared intraday returns, is a consistent estimator for integrated volatility when there are no jumps:


<!-- p:23 -->


$$R V _ { t } = \sum _ { i = 1 } ^ { M _ { t } } r _ { t , i } ^ { 2 } \, ,$$

where Mt is the total number of observations, and rt,i is the i th five-minute return on trading day t .  Barndorff-Nielsen  et  al.  (2004),  Barndorff-Nielsen  and  Shephard  (2006),  and  Huang  and Tauchen (2005) further show that the bipower variation, the sum of the products of adjacent absolute intraday returns, is a consistent estimator of integrated volatility, even in the presence of jumps:

$$B V _ { t } = \frac { \pi } { 2 } \frac { M } { M - 1 } \sum _ { i = 2 } ^ { M } | r _ { t , i } | r _ { t , i - 1 } | \, .$$

Therefore,  the  jump  measure  can  be  constructed  based  on  the  realized  variance  and bipower variation:

$$J _ { t } = s i g n ( r _ { t } ) \times \sqrt { ( R V _ { t } - B V _ { t } ) \times I ( Z J _ { t } \geq \Phi _ { \alpha } ^ { - 1 } ) } ,$$

where Φα -1 denotes  the  inverse  cumulative  distribution  function  of  the  standard  normal distribution. We set α = 99 . 9%, and I(∙) is an indicator function. The specific expression for ZJt is in Appendix Section A.4.

Furthermore, the model-free jump risk measure ( J ) can be grouped into positive and negative jumps, based on the sign of the market return on the day:

$$J _ { t } ^ { + } = I ( r _ { t } \geq 0 ) J _ { t } ,$$

$$J _ { t } ^ { - } = I ( r _ { t } < 0 ) J _ { t } ,$$


<!-- p:24 -->


where rt denotes the daily return on day t .

##### 4.1.3. Empirical Analysis

So far, we have identified the effects of oil volatility and VOV risks on the delta-hedged payoff of USO options. The losses on the delta-hedged portfolios can also be attributed to the fear of market crashes, namely, jump risk, as demonstrated in the model of stochastic VOV with jumps in Section 4.1.1. In this section, we empirically verify the joint effects of volatility, VOV, and jump risks on scaled delta-hedged gains by including the jump risk measures. Specifically, we consider two sets of jump measures, described in Section 4.1.2.

The first set of jump measures considered is risk-neutral skewness and kurtosis extracted from the cross section of USO option prices, using the model-free approach of Bakshi et al. (2003). The econometric specification is as follows:

$$G a i n s _ { t , t + \tau } ^ { i } = \Phi _ { 0 } + \Phi _ { 1 } v o l _ { t } + \Phi _ { 2 } v o v _ { t } + \Phi _ { 3 } s k e w _ { t } + \Phi _ { 4 } k u r t _ { t } + G a i n s _ { t - \tau , t } ^ { i } + u ^ { i } + \epsilon _ { t + \tau } ^ { i } ,$$

where skewt and kurtt denote risk-neutral skewness and kurtosis, respectively, on trading day t .

Columns  (3)  to  (5)  in  Table  6  display  the  results  after  controlling  for  risk-neutral skewness ( skew ) and kurtosis ( kurt ). The predictive power of oil volatility ( vol ) and VOV ( vov ) risks is not affected by the risk-neutral jump measures, and the corresponding slopes Φ1 and Φ2 remain unchanged. Moreover, regarding the predictability of risk-neutral jumps, greater jump fear  risk  predicts  more  negative  delta-hedged  gains  in  the  future: kurt significantly  and negatively  predicts  future  gains,  whether  alone  or  combined  with skew .  This  finding  is consistent with similar studies on the equity index market (e.g., Bakshi et al., 2003; Huang et al., 2018).


<!-- p:25 -->


The second set of jump measures is constructed from the five-minute intraday USO data, based  on  Equation  (21).  We  further  divide  the  jump  measure  into  positive  and  negative components based on market direction, as shown in Equations (22) and (23). Thus, we consider the following two sets of regressions:

$$G a i n s _ { t , t + \tau } ^ { i } = \Phi _ { 0 } + \Phi _ { 1 } v o l _ { t } + \Phi _ { 2 } v o v _ { t } + \Phi _ { 3 } J _ { t } + \Phi _ { 4 } G a i n s _ { t - \tau , t } ^ { i } + u ^ { i } + \epsilon _ { t + \tau } ^ { i } ,$$

$$G a i n s _ { t , t + \tau } ^ { i } = \Phi _ { 0 } + \Phi _ { 1 } v o l _ { t } + \Phi _ { 2 } v o v _ { t } + \Phi _ { 3 } J _ { t } ^ { + } + \Phi _ { 4 } J _ { t } ^ { - } + \Phi _ { 5 } G a i n s _ { t - \tau , t } ^ { i } + u ^ { i } + \epsilon _ { t + \tau } ^ { i } ,$$

where Jt represents the jump measure for trading day t , and Jt + and Jt - stand for positive and negative jumps, respectively.

We control for the realized jump measures, both decomposed and undecomposed, and obtain the results reported in Columns (6) and (7) in Table 6. The variables vol and vov still strongly and negatively predict future delta-hedged option gains, even after the control variables are included. As when the risk-neutral jumps are controlled for, the coefficients of realized jump measures (i.e., J , J + , and J - ) are highly significant. Overall, the predictability of oil VOV risk is robust after controlling for jump risk measures.

#### 4.2. Robustness Check: Alternative Volatility-of-Volatility Measure

We construct a second measure of oil VOV following Baltussen et al. (2018). Specifically, we scale the standard deviation of oil market volatility, which is still proxied by OVX, with the average volatility over the past month, as follows:


<!-- p:26 -->


$$v o v _ { t } ^ { B } = \frac { \sqrt { \frac { 1 } { 2 2 } \sum _ { j = t - 2 1 } ^ { t } ( v o l _ { t } - \overline { v o l _ { t } } ) ^ { 2 } } } { \overline { v o l _ { t } } } \, , \\$$

where vov B is the alternative measure of oil VOV, vol is oil volatility, and volt = ∑ vol j t j=t-21 .

[ Insert Table 8 here ]

The  results  are  displayed  in  Table  8.  As  in  our  previous  findings,  the  univariate regression of delta-hedged USO option gains on oil VOV ( vov B ) generates a highly significant and negative coefficient. Moreover, in the multivariate regressions that add oil volatility and jump measures as control variables, we find that vov B remains highly significant and negative. This  result  suggests  that  oil  VOV  is  significantly  priced  in  the  delta-hedged  gains  of  USO options even with an alternative measure.

#### 4.3. Impacts of Maturities: Weekly Options

Weekly options, or 'weeklies,' were first introduced by the CBOE in October 2005. They have an expiration of about one week, whereas traditional options normally have an expiration of months or years.  The  addition  of  weekly  options  produces  benefits  such  as  greater  trading flexibility and more precise timing; the trading in weeklies has grown rapidly. 18  USO weekly options were introduced in July 2010. Therefore, we also construct delta-hedged gains using weekly USO options. We then conduct an analysis similar to that for one-month delta-hedged gains to investigate the impacts on them of volatility, VOV, and jump risks.

18  For example, according to Andersen et al. (2017), the trading share of S&amp;P 500 weeklies has reached 40% of the total trading volume of S&amp;P 500 options.


<!-- p:27 -->


Using USO weeklies has two main advantages. First, as Andersen et al. (2017) state, the pricing of short-dated ATM options depends mainly on its diffusive component, whereas deep OTM options mainly reflect the characteristics of the risk-neutral jump process. The use of weekly ATM options can be an effective way to control for the effects of jump risk and to focus primarily on diffusive risks. Second, the use of weekly options can increase the sample size and complement our main results based on the use of monthly options.

##### [ Insert Table 9 here ]

Columns (1) to (3) in Table 9 show our results based on one-week delta-hedge option gains. The variables vol and vov remain significant and have negative predictive power for oneweek-ahead delta-hedged option gains. Specifically, the t -statistic for the coefficient of vov is - 5.01 for predicting one-week option gains, whereas the corresponding t -statistic is  -3.26 for predicting  one-month  option  gains.  We  also  consider  model  specifications  with  jump  risk proxies. Even after controlling for jump risk, we find that the coefficient of vov is still negative and  significant;  however,  the  coefficient  of vol is  no  longer  significant.  Consistent  with Andersen et al. (2017), where the effect of jump risk is lower for weekly ATM options, the predictive power of jump risk proxies is weaker than that associated with one-month deltahedged  option  returns.  Specifically,  the  coefficients  of  risk-neutral  skewness  ( skew ),  riskneutral kurtosis ( kurt ), and downside realized jump risk ( J - ) are not significant, whereas those associated with realized jumps ( J ) and upside realized jumps ( J + ) are statistically significant.


<!-- p:28 -->


### 5. Conclusion

Based on the theoretical framework featuring stochastic VOV risk proposed by Huang et al. (2019), we provide a detailed empirical analysis on oil VOV risk. We demonstrate that oil VOV is  a  risk  factor  significantly  priced  in  the  cross  section  of  USO  option  delta-hedged  gains, beyond oil volatility risk. This finding is consistent with the descriptive statistics indicating: (1) the  negative  value  of  average  delta-hedged  USO  option  gains  and  their  nonlinear  pattern (average delta-hedged USO option gains) across moneyness suggest that investors need to be compensated for oil volatility and VOV risks, and (2) the low correlation between oil volatility and  oil  VOV,  with  a  value  of  0.250,  indicates  that  the  two  risk  factors  contain  different information.

We further explore the specific information content of oil VOV, in comparison with its equity counterpart and other volatility-related measures. First, we investigate the relationship between oil VOV and U.S. economic conditions, given  the U.S. has recently become an oil economy, By focusing on the predictability of oil VOV on the one-month-ahead consumption growth rate and financial stress level, we find that oil VOV negatively predicts the personal consumption growth rate and positively predicts the financial stress level in the near term.

The predictive power of oil VOV remains significant after several robustness tests are performed. First, jump risk measures, such as risk-neutral skewness, risk-neutral kurtosis, and realized jumps extracted from high-frequency USO data, are incorporated into our analysis. Second, we adopt the alternative methodology proposed by Baltussen et al. (2018) and construct an oil VOV risk measure; we find that the new measure remains significant in predicting oneperiod-ahead delta-hedged gains. Finally, we change the forecasting horizon to one week by using USO weekly option delta-hedged gains, and it complements our main findings which are based on monthly options.


<!-- p:29 -->


### DATA AVAILABILITY STATEMENT

The data that support the findings of this study are available from six different sources: Thomson Reuters  Tick  History  of  Eikon,  Thomson  Reuters  DataScope  Select,  Thomson  Reuters Datastream, Federal Reserve Economic Data (FRED), CBOE website (https://www.cboe.com), and Amit Goyal's website (http://www.hec.unil.ch/agoyal). Restrictions apply to the availability of data from Thomson Reuters Tick History of Eikon, Thomson Reuters DataScope Select, and Thomson Reuters Datastream, which were used under license for this study.


<!-- p:30 -->

## Appendix

###### A.1. Stochastic Volatility-of-Volatility Model

The pricing framework of Huang et al. (2019) features the dynamics of underlying returns by incorporating time-varying volatility and VOV risks. First, we assume that, under the physical measure P, the dynamics of the underlying price St are such that

$$\frac { d S _ { t } } { S _ { t } } = \mu ( S _ { t } , v _ { t } , \eta _ { t } ) d t + \sqrt { v _ { t } } d \omega _ { t } ^ { 1 } ,$$

$$d v _ { t } = \theta ( v _ { t } ) d t + \sqrt { \eta _ { t } } d \omega _ { t } ^ { 2 } ,$$

$$d \eta _ { t } = \gamma ( \eta _ { t } ) d t + \phi \sqrt { \eta _ { t } } d \omega _ { t } ^ { 3 } ,$$

where (ωt 1 , ω t 2 , ω t 3 ) t≥0 is  a  three-dimensional  Brownian  motion  with  correlation  coefficient corr(dωt i , dω t j ) = ρij , for all i  ≠ j . vt denotes the stochastic variance in immediate returns, and ηt denotes the variance of innovation in vt .

Correspondingly,  under  the  risk-neutral  probability  measure Q ,  the  dynamics  of  the underlying price St are

$$\frac { d S _ { t } } { S _ { t } } = r d t + \sqrt { v _ { t } } d \widetilde { \omega } _ { t } ^ { 1 } ,$$

$$d v _ { t } = ( \theta ( v _ { t } ) - \lambda _ { t } ^ { v } ) d t + \sqrt { \eta _ { t } } d \widetilde { \omega } _ { t } ^ { 2 } ,$$

$$d \eta _ { t } = \left ( \gamma ( \eta _ { t } ) - \lambda _ { t } ^ { \eta } \right ) d t + \phi \sqrt { \eta _ { t } } d \widetilde { \omega } _ { t } ^ { 3 } ,$$


<!-- p:36 -->


where (ωt 1 ̃ , ω t 2 ̃ , ω t 3 ̃ ) t≥0 represents  the  corresponding  three-dimensional  Brownian  motion under  the  risk-neutral  probability  measure Q .  Moreover, λt v represents  compensation  for stochastic variance and λ t η represents compensation for the stochastic variance in the variance.

Consider a call option written on the underlying asset St . By Itˆo's lemma, its price at time t + τ can be expressed as

$$C _ { t + \tau } = C _ { t } + \int _ { t } ^ { t + \tau } \frac { \partial C _ { u } } { \partial S _ { u } } d S _ { u } + \int _ { t } ^ { t + \tau } \frac { \partial C _ { u } } { \partial v _ { u } } d v _ { u } + \int _ { t } ^ { t + \tau } \frac { \partial C _ { u } } { \partial \eta _ { u } } d \eta _ { u } + \int _ { t } ^ { t + \tau } b _ { u } d u \, ,$$

where bt is defined as

$$b _ { t } = \frac { \partial C _ { t } } { \partial t } + \frac { 1 } { 2 } v _ { t } S _ { t } ^ { 2 } \frac { \partial ^ { 2 } C _ { t } } { \partial S _ { t } ^ { 2 } } + \frac { 1 } { 2 } \eta _ { t } \frac { \partial ^ { 2 } C _ { t } } { \partial v _ { t } ^ { 2 } } + \frac { 1 } { 2 } \phi ^ { 2 } \eta _ { t } \frac { \partial ^ { 2 } C _ { t } } { \partial \eta _ { t } ^ { 2 } } + \rho _ { 1 2 } \sqrt { v _ { t } } \sqrt { \eta _ { t } } S _ { t } \frac { \partial ^ { 2 } C _ { t } } { \partial S _ { t } \partial v _ { t } } \\ + \rho _ { 1 3 } \phi \sqrt { v _ { t } } \sqrt { \eta _ { t } } S _ { t } \frac { \partial ^ { 2 } C _ { t } } { \partial S _ { t } \partial \eta _ { t } } + \rho _ { 2 3 } \phi \eta _ { t } \frac { \partial ^ { 2 } C _ { t } } { \partial v _ { t } \partial \eta _ { t } } .$$

Meanwhile, the valuation equation that determines the price of the call option Ct is

$$r S _ { t } \frac { \partial C _ { t } } { \partial S _ { t } } + ( \theta ( v _ { t } ) - \lambda _ { t } ^ { v } ) \frac { \partial C _ { t } } { \partial v _ { t } } + \left ( \gamma ( \eta _ { t } ) - \lambda _ { t } ^ { \eta } \right ) \frac { \partial C _ { t } } { \partial \eta _ { t } } + b _ { t } - r C _ { t } = 0 .$$

Rearranging Equation ( A1.8 ), we obtain

$$b _ { t } = r \left ( C _ { t } - S _ { t } \frac { \partial C _ { t } } { \partial S _ { t } } \right ) - ( \theta ( v _ { t } ) - \lambda _ { t } ^ { v } ) \frac { \partial C _ { t } } { \partial v _ { t } } - ( \gamma ( \eta _ { t } ) - \lambda _ { t } ^ { \eta } ) \frac { \partial C _ { t } } { \partial \eta _ { t } } .$$

Considering that the dynamics of vt and ηt are defined by Equations ( A1.2 ) and ( A1.3 ), respectively, these can be simplified by substituting bt in Equation ( A1.10 ) into Equation ( A1.7 ), as follows:


<!-- p:37 -->


$$\pi _ { t , t + \tau } = \int _ { t } ^ { t + \tau } \lambda _ { u } ^ { v } \frac { \partial C _ { u } } { \partial v _ { u } } d u + \int _ { t } ^ { t + \tau } \lambda _ { u } ^ { \eta } \frac { \partial C _ { u } } { \partial \eta _ { u } } d u + \int _ { t } ^ { t + \tau } \sqrt { \eta _ { u } } \frac { \partial C _ { u } } { \partial v _ { u } } d \omega _ { u } ^ { 2 } + \int _ { t } ^ { t + \tau } \phi \sqrt { \eta _ { u } } \frac { \partial C _ { u } } { \partial \eta _ { u } } d \omega _ { u } ^ { 3 } .$$

Therefore,  the  expected  value  of  the  delta-hedged  gain  (i.e., πt,t+τ )  under  physical measure P is given by considering the martingale property of Ito ̂′s integral:

$$E _ { t } [ \pi _ { t , t + \tau } ] = \int _ { t } ^ { t + \tau } E _ { t } \left [ \lambda _ { u } ^ { v } \frac { \partial C _ { u } } { \partial v _ { u } } \right ] d u + \int _ { t } ^ { t + \tau } E _ { t } \left [ \lambda _ { u } ^ { \eta } \frac { \partial C _ { u } } { \partial \eta _ { u } } \right ] d u \, ,$$

where λt v and λ t η denote  compensation  for  stochastic  volatility  and  VOV  risks,  respectively. Moreover, ∂Cu ∂vu and ∂Cu ∂ηu represent  the  vega  and  volga  of  the  call  option,  respectively.  Equation (A1.12) shows that the expected delta-hedged gains depend on the risk premiums of volatility and VOV.

For tractability, Huang et al. (2019) assume that the risk premiums have a linear structure:

$$\lambda _ { t } ^ { v } = \lambda ^ { v } v _ { t } , \quad \lambda _ { t } ^ { \eta } = \lambda ^ { \eta } \eta _ { t } ,$$

where λt v and λ t η represent constant market prices of volatility and VOV risks, respectively.

The scaled expected delta-hedged gain is linear with respect to the fundamental factors by applying Ito ̂′s Taylor expansions to Equation ( A1.11 ):

$$\frac { E _ { t } [ \pi _ { t , t + \tau } ] } { S _ { t } } = \lambda ^ { v } \beta _ { t } ^ { v } v _ { t } + \lambda ^ { \eta } \beta _ { t } ^ { \eta } \eta _ { t } ,$$

where βt v and β t η represent the options' exposure to volatility risk and VOV risk, respectively. Specifically, βt v and β t η are expressed as


<!-- p:38 -->


$$\beta _ { t } ^ { \nu } = \sum _ { n = 0 } ^ { \infty } \frac { \tau ^ { 1 + n } } { ( 1 + n ) ! } \Phi _ { t , n } ^ { \nu } > 0 ,$$

$$\beta _ { t } ^ { \eta } = \sum _ { n = 0 } ^ { \infty } \frac { \tau ^ { 1 + n } } { ( 1 + n ) ! } \Phi _ { t , n } ^ { \eta } > 0 ,$$

where Φ v ( ∙ ) and Φ η ( ∙ ) are positive functions depending on option moneyness, vega, and volga

(i.e., m , ∂Cu ∂vu and ∂Cu ∂ηu , respectively).

###### A.2. Stochastic Volatility-of-Volatility Model with a Jump

Under the physical measure P , we assume that the dynamics of the underlying price St can be expressed as:

$$\frac { d S _ { t } } { S _ { t } } = \mu ( S _ { t } , v _ { t } , \eta _ { t } ) d t + \sqrt { v _ { t } } d \omega _ { t } ^ { 1 } + ( e ^ { x } - 1 ) d q _ { t } - \mu _ { J } \Lambda _ { J } \sqrt { v _ { t } } d t ,$$

$$d v _ { t } = \theta ( v _ { t } ) d t + \sqrt { \eta _ { t } } d \omega _ { t } ^ { 2 } ,$$

$$d \eta _ { t } = \gamma ( \eta _ { t } ) d t + \phi \sqrt { \eta _ { t } } d \omega _ { t } ^ { 3 } .$$

This framework allows random jumps, along with stochastic volatility and VOV, to play a role in pricing the underlying St .  The jump term follows a Poisson process with volatilityindependent intensity ΛJ vt . We use x to denote the jump size and q to represent its corresponding physical density. We further assume that the mean of e x  - 1 is μJ , and then the compensation is μJΛJ√vtdt .


<!-- p:39 -->


Assume that, under the risk-neutral probability measure Q , the density of the jump size (i.e., x ) is q , and the mean of e x - 1 is μ ∗ J . Then, we can write the dynamics of the underlying St as

$$\frac { d S _ { t } } { S _ { t } } = r d t + \sqrt { v _ { t } } d \widetilde { \omega } _ { t } ^ { 1 } + ( e ^ { x } - 1 ) d q _ { t } ^ { * } - \mu _ { J } ^ { * } \Lambda _ { J } \sqrt { v _ { t } } d t ,$$

$$d v _ { t } = ( \theta ( v _ { t } ) - \lambda _ { t } ^ { v } ) d t + \sqrt { \eta _ { t } } d \widetilde { \omega } _ { t } ^ { 2 } ,$$

$$d \eta _ { t } = ( \gamma ( \eta _ { t } ) - \lambda _ { t } ^ { \eta } ) d t + \phi \sqrt { \eta _ { t } } d \widetilde { \omega } _ { t } ^ { 3 } .$$

By Ito ̂′s lemma , we can write the call option price at time t + τ as

$$C _ { t + \tau } & = C _ { t } + \int _ { t } ^ { t + \tau } \frac { \partial C _ { u } } { \partial S _ { u } } d S _ { u } + \int _ { t } ^ { t + \tau } \frac { \partial C _ { u } } { \partial v _ { u } } d v _ { u } + \int _ { t } ^ { t + \tau } \frac { \partial C _ { u } } { \partial \eta _ { u } } d \eta _ { u } \\ + \Lambda _ { J } \int _ { t } ^ { t + \tau } \sqrt { v _ { u } } \int _ { - \infty } ^ { \infty } [ C ( S _ { t } e ^ { x } ) - C ( S _ { t } ) ] q ( x ) d x \, d u + \int _ { t } ^ { t + \tau } b _ { u } d u \, , \\$$

where bt is defined as in Equation (A1.2). Moreover, the valuation equation is given by

$$\left ( r - \mu _ { J } ^ { * } \Lambda _ { J } \sqrt { v _ { t } } \right ) S _ { t } \frac { \partial C _ { t } } { \partial S _ { t } } + ( \theta ( v _ { t } ) - \lambda _ { t } ^ { v } ) \, \frac { \partial C _ { t } } { \partial v _ { t } } + \left ( \gamma ( \eta _ { t } ) - \lambda _ { t } ^ { \eta } \right ) \frac { \partial C _ { t } } { \partial \eta _ { t } }$$

$$+ \Lambda _ { J } \sqrt { v _ { t } } \int ^ { \infty } [ C ( S _ { t } e ^ { x } ) - C ( S _ { t } ) ] q ( x ) ^ { * } d x + b _ { t } - r C _ { t } = 0 .$$

$$\Lambda _ { J } \sqrt { v _ { t } } \int _ { - \infty } ^ { \infty } [ C ( S _ { t } e ^ { x } ) - C ( S _ { t } ) ] q ( x ) ^ { * } d x + b _ { t } - r C _ { t } = 0 .$$

Rearranging Equation ( A2.8 ), we obtain

$$b _ { t } & = r \left ( C _ { t } - S _ { t } \frac { \partial C _ { t } } { \partial S _ { t } } \right ) - ( \theta ( v _ { t } ) - \lambda _ { t } ^ { v } ) \, \frac { \partial C _ { t } } { \partial v _ { t } } - \left ( \gamma ( \eta _ { t } ) - \lambda _ { t } ^ { \eta } \right ) \frac { \partial C _ { t } } { \partial \eta _ { t } } \\ & + \mu _ { J } ^ { * } \Lambda _ { J } \sqrt { v _ { t } } S _ { t } \frac { \partial C _ { t } } { \partial S _ { t } } - \Lambda _ { J } \sqrt { v _ { t } } \int _ { - \infty } ^ { \infty } [ C ( S _ { t } e ^ { x } ) - C ( S _ { t } ) ] q ( x ) ^ { * } d x \, .$$

Therefore, the delta-hedged gain (i.e., πt,t+τ ) under physical measure P is


<!-- p:40 -->


$$E _ { t } [ \pi _ { t , t + \tau } ] = \int _ { t } ^ { t + \tau } E _ { t } \left [ \lambda u \frac { \partial C _ { u } } { \partial \nu _ { u } } \right ] d u + \int _ { t } ^ { t + \tau } E _ { t } \left [ \lambda _ { u } ^ { \eta } \frac { \partial C _ { u } } { \partial \eta _ { u } } \right ] d u + \mu _ { \jmath } ^ { * } A _ { J } \int _ { t } ^ { t + \tau } E _ { t } \left [ \sqrt { \nu _ { u } } S _ { u } \frac { \partial C _ { u } } { \partial S _ { u } } \right ] d u \\ - A _ { J } \int _ { t } ^ { t + \tau } \sqrt { \nu _ { u } } \left [ \int _ { - \infty } ^ { \infty } C ( S _ { u } e ^ { x } ) q ( x ) ^ { * } d x - \int _ { - \infty } ^ { \infty } C ( S _ { u } e ^ { x } ) q ( x ) d x \right ] d u . \\ \text { Unlike the expected delta-hedged gain under stochastic volatility framework in}$$

Unlike  the  expected  delta-hedged  gain  under  stochastic  volatility  framework  in Equations ( A1.1 )- (A1.3 ), if jump fears are considered, Equation ( A2.10 ) indicates that the deltahedged gain is also affected by jump risk.

###### A.3. Construction of Risk-Neutral Moments

According to Bakshi et al. (2003), the prices of the volatility and cubic and quartic contracts can be expressed by option prices, respectively, as follows:

$$C ( t , \tau ) = \int _ { S _ { t } } ^ { \infty } \frac { 2 \left ( 1 - \ln \left ( \frac { K } { S _ { t } } \right ) \right ) } { K ^ { 2 } } C ( t , \tau , K ) d K + \int _ { 0 } ^ { s _ { t } } \frac { 2 \left ( 1 + \ln \left ( \frac { S _ { t } } { t } \right ) \right ) } { K ^ { 2 } } P ( t , \tau , K ) d K , \\ W _ { t , t + \tau } = \int _ { S _ { t } } ^ { \infty } \frac { \int _ { \frac { K } { S _ { t } } } \left ( \frac { K } { t } \right ) - 3 \left ( \ln \left ( \frac { K } { S _ { t } } \right ) \right ) ^ { 2 } } { K ^ { 2 } } C ( t , \tau , K ) d K - \int _ { 0 } ^ { s _ { t } } \frac { \int _ { \frac { K } { t } } ^ { 6 \ln \left ( \frac { S _ { t } } { t } \right ) + 3 \left ( \ln \frac { S _ { t } } { K } \right ) \right ) ^ { 2 } } { K ^ { 2 } } P ( t , \tau , K ) d K , \\ X _ { t , t + \tau } = \int _ { S _ { t } } ^ { \infty } \frac { 1 2 \left ( \ln \left ( \frac { K } { S _ { t } } \right ) \right ) ^ { 2 } - 4 \left ( \ln \left ( \frac { K } { S _ { t } } \right ) \right ) ^ { 3 } } { K ^ { 2 } } C ( t , \tau , K ) d K + \int _ { 0 } ^ { s _ { t } } \frac { 1 2 \left ( \ln \left ( \frac { S _ { t } } { K } \right ) \right ) ^ { 2 } + 4 \left ( \ln \left ( \frac { S _ { t } } { K } \right ) \right ) ^ { 3 } } { K ^ { 2 } } P ( t , \tau , K ) d K , \\ \text {where } C ( t , \tau , K ) \text { stands for the price of a call option with time to maturity } \tau \text { and strike price } K \text { at }$$

where C ( t, τ, K ) stands for the price of a call option with time to maturity τ and strike price K at time t .  Note  that,  in  practice,  we  discretized  the  integrals  in  these  equations  by  defining  the increment ∆ K as

$$\Delta I ( K _ { i } ) = \begin{cases} \frac { K _ { i + 1 } - K _ { i - 1 } } { 2 } , 0 \leq i \leq N & ( \text {with} \, K _ { - 1 } = 2 K _ { 0 } - K _ { 1 } , K _ { N + 1 } = 2 K _ { N } - K _ { N - 1 } ) \, , \\ & 0 , \quad o t h e r w i s e . \end{cases}$$


<!-- p:41 -->


###### A.4. Expressions in the Model-Free Jump Measure

The detailed expression for ZJ in the model-free jump measure (i.e., J ) shown in Equation (21), is

$$Z J _ { t } = \frac { \frac { R V _ { t } - B V _ { t } } { R V _ { t } } } { \sqrt { [ \pi / 2 ) ^ { 2 } + \pi - 5 ] / m \times m a x ( 1 , T P _ { t } / B V _ { t } ^ { 2 } ) } } ,$$

$$T P _ { t } = m \mu _ { 4 / 3 } ^ { - 3 } \frac { m } { m - 2 } \sum _ { i = 3 } ^ { m } | r _ { t , i - 2 } | ^ { 4 / 3 } | r _ { t , i - 1 } | ^ { 4 / 3 } | r _ { t , i } | ^ { 4 / 3 } \, ,$$

$$\mu _ { k } = 2 ^ { k / 2 } \frac { \Gamma [ ( k + 1 ) / 2 ] } { \Gamma [ 1 / 2 ] } , k > 0 ,$$

and Γ(∙) denotes the gamma function.

where Note: This table reports descriptive statistics such as the mean (Mean), standard deviation (Std. dev.), skewness (Skewness), kurtosis (Kurtosis), 25th percentile (Q1), median (Median), and 75th percentile (Q3) for the following key variables: crude oil market volatility ( vol ), crude oil market volatility-of-volatility ( vov ), the VIX (VIX), and the VIX volatility index (VVIX). The sample period is July 2010 to June 2018.


<!-- p:42 -->


Table 1. Descriptive statistics

|      | Mean     | Std. dev.   | Skewness   | Kurtosis   | Q1       | Median   | Q3       |
|------|----------|-------------|------------|------------|----------|----------|----------|
| vol  | 33 . 040 | 10 . 850    | 0 . 823    | 3 . 604    | 25 . 590 | 31 . 360 | 39 . 300 |
| vov  | 0 . 002  | 0 . 002     | 4 . 681    | 36 . 711   | 0 . 001  | 0 . 002  | 0 . 003  |
| VIX  | 16 . 560 | 5 . 559     | 1 . 872    | 7 . 604    | 12 . 900 | 15 . 200 | 18 . 510 |
| VVIX | 90 . 670 | 12 . 912    | 1 . 146    | 7 . 050    | 82 . 340 | 89 . 180 | 97 . 570 |


<!-- p:43 -->


Table 2. Correlations

|     | vol     | vov     | VIX     | VVIX    |
|-----|---------|---------|---------|---------|
| vol | 1 . 000 | 0 . 250 | 0 . 493 | 0 . 427 |
| vov |         | 1 . 000 | 0 . 424 | 0 . 169 |
| VIX |         |         | 1 . 000 | 0 . 529 |

Note: This table reports the correlations between the following key variables: crude oil market volatility ( vol ), crude oil market VOV ( vov ), the VIX (VIX), and the VIX volatility index (VVIX). The sample period is July 2010 to June 2018.


<!-- p:44 -->


Table 3. Delta-Hedged Gains for One-Month USO Options

| Moneyness    | π t,t+τ - Mean   | π t,t+τ - t -stat   | π t,t+τ - in $ % < 0   |   π t,t+τ - Std. | π t,t+τ - AR(1)   | π t,t+τ (in $) S t in % - Mean   | π t,t+τ (in $) S t in % - t -stat   |   π t,t+τ (in $) S t in % - Std. | π t,t+τ (in $) S t in % - AR(1)   |
|--------------|------------------|---------------------|------------------------|------------------|-------------------|----------------------------------|-------------------------------------|----------------------------------|-----------------------------------|
| Call options |                  |                     |                        |                  |                   |                                  |                                     |                                  |                                   |
| 0.900-0.925  | -0.050           | - 2 . 36            | 59%                    |             0.16 | 0.15              | - 0 . 13%                        | - 1 . 86                            |                             0.01 | 0.05                              |
| 0.925-0.950  | -0.059           | - 2 . 19            | 61%                    |             0.19 | 0.19              | - 0 . 17%                        | - 1 . 99                            |                             0.01 | 0.06                              |
| 0.950-0.975  | -0.058           | - 1 . 83            | 60%                    |             0.21 | 0.21              | - 0 . 19%                        | - 1 . 96                            |                             0.01 | 0.15                              |
| 0.975-1.000  | -0.056           | - 1 . 86            | 59%                    |             0.20 | 0.21              | - 0 . 17%                        | - 1 . 65                            |                             0.01 | 0.12                              |
| 1.000-1.025  | -0.065           | - 2 . 06            | 64%                    |             0.21 | 0.11              | - 0 . 18%                        | - 1 . 83                            |                             0.01 | - 0 . 03                          |
| 1.025-1.050  | -0.050           | - 2 . 06            | 63%                    |             0.21 | - 0 . 02          | - 0 . 15%                        | - 2 . 03                            |                             0.01 | - 0 . 10                          |
| 1.050-1.075  | -0.058           | - 2 . 39            | 68%                    |             0.20 | - 0 . 13          | - 0 . 17%                        | - 2 . 19                            |                             0.01 | - 0 . 13                          |
| 1.075-1.100  | -0.044           | - 2 . 79            | 69%                    |             0.13 | 0.01              | - 0 . 14%                        | - 2 . 84                            |                             0.00 | - 0 . 07                          |
| Put options  |                  |                     |                        |                  |                   |                                  |                                     |                                  |                                   |
| 0.900-0.925  | - 0 . 068        | - 2 . 90            | 68%                    |             0.18 | 0.13              | - 0 . 19%                        | - 2 . 37                            |                             0.01 | 0.11                              |
| 0.925-0.950  | - 0 . 076        | - 2 . 27            | 63%                    |             0.23 | 0.22              | - 0 . 20%                        | - 1 . 95                            |                             0.01 | 0.10                              |
| 0.950-0.975  | - 0 . 070        | - 2 . 07            | 60%                    |             0.23 | 0.13              | - 0 . 19%                        | - 1 . 97                            |                             0.01 | 0.00                              |
| 0.975-1.000  | - 0 . 071        | - 2 . 18            | 66%                    |             0.21 | 0.27              | - 0 . 21%                        | - 1 . 95                            |                             0.01 | 0.23                              |
| 1.000-1.025  | - 0 . 069        | - 2 . 01            | 64%                    |             0.23 | 0.17              | - 0 . 18%                        | - 1 . 78                            |                             0.01 | 0.03                              |
| 1.025-1.050  | - 0 . 060        | - 2 . 50            | 66%                    |             0.19 | 0.06              | - 0 . 16%                        | - 2 . 20                            |                             0.01 | - 0 . 07                          |
| 1.050-1.075  | - 0 . 084        | - 3 . 61            | 70%                    |             0.20 | - 0 . 13          | - 0 . 24%                        | - 3 . 07                            |                             0.01 | - 0 . 12                          |
| 1.075-1.100  | - 0 . 038        | - 1 . 85            | 68%                    |             0.20 | - 0 . 12          | - 0 . 11%                        | - 1 . 89                            |                             0.01 | - 0 . 15                          |

Note: The table reports the gains on a portfolio of a long position in a one-month USO option hedged by a short position in the underlying asset, such that the net investment earns the risk-free interest rate. The sample period is July 2010 to June 2018. The delta-hedged gains are rebalanced on a daily basis and calculated based on Equation (3). We report the unscaled delta-hedged gains ( Πt,t+τ ) and the delta-hedged gains scaled by the underlying ( πt,t+τ St ).

Both are averaged over the specified moneyness ranges, in which moneyness is defined as m ≡ Se rτ K . The t -statistic tests the null hypothesis that the delta-hedged gains equal zero. The % &lt; 0 column shows the percentage of negative delta-hedged gains within the corresponding moneyness range.


<!-- p:45 -->


Table 4. Delta-Hedged Gains for One-Week USO Options

| Moneyness    |   π t,t+τ - Mean |   π t,t+τ - t -stat | π t,t+τ - in $ % < 0   |   π t,t+τ - Std. |   π t,t+τ - AR(1) | π t,t+τ (in $) S t in % - Mean   |   π t,t+τ (in $) S t in % - t -stat |   π t,t+τ (in $) S t in % - Std. |   π t,t+τ (in $) S t in % - AR(1) |
|--------------|------------------|---------------------|------------------------|------------------|-------------------|----------------------------------|-------------------------------------|----------------------------------|-----------------------------------|
| Call options |                  |                     |                        |                  |                   |                                  |                                     |                                  |                                   |
| 0.900-0.925  |           -0.015 |               -2.99 | 65%                    |             0.06 |              0.01 | -0.05%                           |                               -2.21 |                             0.00 |                             -0.14 |
| 0.925-0.950  |           -0.018 |               -2.96 | 62%                    |             0.09 |             -0.05 | -0.05%                           |                               -2.15 |                             0.00 |                             -0.09 |
| 0.950-0.975  |           -0.028 |               -3.86 | 63%                    |             0.12 |             -0.02 | -0.09%                           |                               -3.84 |                             0.00 |                             -0.06 |
| 0.975-1.000  |           -0.031 |               -3.46 | 61%                    |             0.13 |              0.03 | -0.09%                           |                               -2.73 |                             0.01 |                              0.04 |
| 1.000-1.025  |           -0.024 |               -2.72 | 61%                    |             0.15 |             -0.07 | -0.06%                           |                               -1.91 |                             0.01 |                              0.00 |
| 1.025-1.050  |           -0.014 |               -1.30 | 68%                    |             0.17 |             -0.03 | -0.07%                           |                               -2.09 |                             0.01 |                             -0.07 |
| 1.050-1.075  |           -0.026 |               -3.09 | 61%                    |             0.11 |              0.04 | -0.08%                           |                               -2.97 |                             0.00 |                             -0.06 |
| 1.075-1.100  |           -0.015 |               -1.58 | 59%                    |             0.14 |              0.02 | -0.08%                           |                               -2.34 |                             0.00 |                              0.02 |
| Put options  |                  |                     |                        |                  |                   |                                  |                                     |                                  |                                   |
| 0.900-0.925  |           -0.012 |               -1.43 | 54%                    |             0.12 |              0.02 | 0.00%                            |                               -0.07 |                             0.01 |                              0.02 |
| 0.925-0.950  |           -0.033 |               -3.62 | 59%                    |             0.12 |              0.00 | -0.10%                           |                               -3.30 |                             0.00 |                             -0.07 |
| 0.950-0.975  |           -0.034 |               -3.77 | 60%                    |             0.12 |              0.10 | -0.10%                           |                               -3.48 |                             0.00 |                              0.02 |
| 0.975-1.000  |           -0.033 |               -3.60 | 62%                    |             0.13 |              0.02 | -0.10%                           |                               -3.05 |                             0.01 |                              0.02 |
| 1.000-1.025  |           -0.028 |               -3.34 | 63%                    |             0.14 |             -0.12 | -0.07%                           |                               -2.13 |                             0.01 |                              -003 |
| 1.025-1.050  |           -0.025 |               -3.23 | 68%                    |             0.12 |              0.00 | -0.09%                           |                               -3.33 |                             0.00 |                             -0.08 |
| 1.050-1.075  |           -0.023 |               -3.49 | 74%                    |             0.09 |              0.11 | -0.08%                           |                               -3.25 |                             0.00 |                              0.02 |
| 1.075-1.100  |           -0.007 |               -0.87 | 68%                    |             0.11 |             -0.02 | -0.03%                           |                               -1.06 |                             0.00 |                             -0.03 |

Note: The table reports the gains on a portfolio of a long position in a one-week USO option hedged by a short position in the underlying asset, such that the net investment earns the risk-free interest rate. The sample period is July 2010 to June 2018. The delta-hedged gains are rebalanced on a daily basis and calculated based on Equation (3). We report the unscaled delta-hedged gains ( Πt,t+τ ) and the delta-hedged gains scaled by the underlying ( πt,t+τ St ).

Both are averaged over the specified moneyness ranges, in which moneyness is defined as m ≡ Se rτ K . The t -statistic tests  the  null  hypothesis  that  the  delta-hedged  gains  equal zero.  The  % &lt; 0 column shows the percentage of negative delta-hedged gains within the corresponding moneyness range.


<!-- p:46 -->


Table 5. Delta-Hedged Gains from Volatility and Volatility-of-Volatility Risks

|             | Vega - Slope   | Vega - t -stat   | Volga - Slope   | Volga - t -stat   |
|-------------|----------------|------------------|-----------------|-------------------|
| Gains t,t+τ | -0.058 ∗∗∗     | (-4.80)          |                 |                   |
|             |                |                  | -0.002          | (-0.61)           |
|             | -0.119 ∗∗∗     | (-7.22)          | -0.020 ∗∗∗      | (-5.38)           |

Note: This table reports the cross-sectional regressions of one-month USO option gains on the vega ( ∂Ct ∂σt ) and volga ( ∂ 2 Ct ∂ 2 σ t 2 ) of the options, taking into account time-fixed effects. All the slopes are scaled by 1,000. The option greeks are implied by Black and Scholes (1973). The sample period is July 2010 to June 2018. The values in parentheses are Newey and West (1987) robust t -statistics (with lag 3), significant at the 1%, 5%, and 10% levels, denoted respectively by ∗∗∗ , ∗∗ , and ∗ .


<!-- p:47 -->


Table 6. Delta-Hedged Gains from Volatility and Volatility-of-Volatility Risks

|         | π t,t+τ - (1)      | π t,t+τ - (2)          | π t,t+τ - (3)          | π t,t+τ - (4)          | π t,t+τ - (5)          | π t,t+τ - (6)           | π t,t+τ - (7)                     |
|---------|--------------------|------------------------|------------------------|------------------------|------------------------|-------------------------|-----------------------------------|
| vov 2   |                    | -2.450e-06 ∗∗∗ (-7.19) | -2.310e-06 ∗∗∗ (-6.58) | -2.450e-06 ∗∗∗ (-7.25) | -2.550e-06 ∗∗∗ (-7.26) | -5.090e-06 ∗∗∗ (-12.48) | -5.640e-06 ∗∗∗ (-13.40)           |
| vol 2   | -0.894 ∗∗∗ (-7.83) | -0.610 ∗∗∗ (-5.17)     | -0.553 ∗∗∗ (-4.83)     | -0.548 ∗∗∗ (-4.65)     | -0.578 ∗∗∗ (-4.77)     | -0.410 ∗∗∗ (-3.64)      | -0.313 ∗∗∗ (-2.76)                |
| skew    |                    |                        | 3.201e-04 ∗ (1.87)     |                        | -2.28E-04 (-1.08)      |                         |                                   |
| kurt    |                    |                        |                        | -2.751e-05 ∗∗∗ (-4.58) | -3.237e-05 ∗∗∗ (-4.31) |                         |                                   |
| J       |                    |                        |                        |                        |                        | 1.037 ∗∗∗ (10.48)       |                                   |
| J + J - |                    |                        |                        |                        |                        |                         | 0.623*** (4.36) 1.390 ∗∗∗ (11.24) |
| π t-τ,t | 0.06               | 0.031                  | 0.033                  | 0.047                  | 0.047                  | 0.070 ∗∗                | 0.049                             |
|         | (1.87)             | (0.96)                 | (1.01)                 | (1.47)                 | (1.45)                 | (2.31)                  | (1.63)                            |

Note: This table shows the predictability of one-month-ahead delta-hedged gains from volatility ( vol ), VOV ( vov ), and jump (i.e., skew , kurt , J , J + , and J - ) risks. The sample period is July 2010 to June 2018. The values in parentheses are Newey and West (1987) robust t -statistics (with lag 3), significant at the 1%, 5%, and 10% levels, denoted respectively by ∗∗∗ , ∗∗ , and ∗ .


<!-- p:48 -->


Table 7. Information content of oil volatility-of-volatility on macro variables

| Macro Variables   | vov 2      | vol 2       | VVIX 2        | AR1       | TS      | DS        | DP      |   Adj. R 2 (%) |
|-------------------|------------|-------------|---------------|-----------|---------|-----------|---------|----------------|
| ∆ ln RPCE         | -0.107 ∗∗  | 5.766e-07 ∗ | -8.290e-08    | -0.226 ∗∗ | -0.020  | -0.251 ∗∗ | -0.001  |           5.96 |
|                   | (-2.11)    | (1.92)      | (-0.80)       | (-2.51)   | (-1.50) | (-2.27)   | (-0.33) |                |
| KCFSI             | 20.337 ∗∗∗ | 7.421e-05   | 3.155e-05 ∗∗∗ | 0.564 ∗∗∗ | 2.135   | 19.195    | 0.195   |          69.78 |
|                   | (2.58)     | (1.53)      | (4.06)        | (4.24)    | (1.24)  | (0.75)    | (0.54)  |                |

Note: This table reports the one-month ahead predictability of oil VOV ( vov ) on the monthly growth rate of real personal consumption ( ∆ ln RPCE) and Kansas City Financial Stress Index (KCFSI), controlling for oil volatility (vol), equity VOV (VVIX), the term spread (TS), the default spread (DS), and the log dividendprice ratio (DP) and its lag term (AR1). The sample period is July 2010 to June 2018. The values in parentheses are Newey and West (1987) robust t -statistics (with lag 3), significant at the 1%, 5%, and 10% levels, denoted respectively by ∗∗∗ , ∗∗ , and ∗ .


<!-- p:49 -->


Table 8. Robustness check: Another volatility-of-volatility measure

|         | π t,t+τ - (1)      | π t,t+τ - (2)      | π t,t+τ - (3)      | π t,t+τ - (4)      | π t,t+τ - (5)          | π t,t+τ - (6)       | π t,t+τ - (7)              |
|---------|--------------------|--------------------|--------------------|--------------------|------------------------|---------------------|----------------------------|
| vov 2   |                    | -2.770 ∗∗∗ (-8.31) | -2.570 ∗∗∗ (-7.41) | -2.740 ∗∗∗ (-8.28) | -2.550e-06 ∗∗∗ (-7.26) | -5.380 ∗∗∗ (-13.70) | -5.830 ∗∗∗ (-14.64)        |
| vol 2   | -0.122 ∗∗∗ (-5.25) | -0.075 ∗∗∗ (-3.26) | -0.061 ∗∗ (-2.55)  | -0.066 ∗∗∗ (-2.86) | -0.578 ∗∗∗ (-4.77)     | -0.056 ∗∗∗ (-2.60)  | -0.060 ∗∗∗ (-2.80)         |
| skew    |                    |                    | 41.404 ∗∗ (2.41)   |                    | -2.28E-04 (-1.08)      |                     |                            |
| kurt    |                    |                    |                    | -2.948 ∗∗∗ (-4.89) | -3.237e-05 ∗∗∗ (-4.31) |                     |                            |
| J       |                    |                    |                    |                    |                        | 1.077 ∗∗∗ (10.98)   |                            |
| J + J - |                    |                    |                    |                    |                        |                     | 0.581 ∗∗∗ (4.05) 1.458 ∗∗∗ |
| π t-τ,t | 0.095 ∗∗∗ (2.76)   | 0.048 (1.41)       | 0.047 (1.38)       | 0.063 ∗ (1.87)     | 0.064 ∗ (1.89)         | 0.086 ∗∗ (2.70)     | (12.16) 0.067 ∗∗∗ (2.13)   |

Note: This table shows the predictability of one-month-ahead delta-hedged gains from volatility ( vol ), volatility of-volatility ( vov B ), and jump (i.e., skew , kurt , J , J + , and J - ) risks. The sample period is July 2010 to June 2018. The values in parentheses are Newey and West (1987) robust t -statistics (with lag 3), significant at the 1%, 5%, and 10% levels, denoted respectively by ∗∗∗ , ∗∗ , and ∗ .


<!-- p:50 -->


Table 9. Robustness check: Predictability of one-week delta-hedge gains

πt,t+τ

|         | (1)                | (2)                    | (3)                    | t,t+τ (4)              | (5)                    | (6)                | (7)                           |
|---------|--------------------|------------------------|------------------------|------------------------|------------------------|--------------------|-------------------------------|
| vov 2   |                    | -8.817e-07 ∗∗∗ (-7.43) | -9.915e-07 ∗∗∗ (-8.01) | -9.921e-07 ∗∗∗ (-8.04) | -1.030e-06 ∗∗∗ (-8.26) | -1.09e-07 (-0.26)  | -7.01e-08 (-0.17)             |
| vol 2   | -0.218 ∗∗∗ (-5.36) | -0.109 ∗∗ (-2.53)      | -0.077 (-1.60)         | -0.081 ∗ (-1.68)       | -0.083 ∗ (-1.72)       | -0.403 ∗∗∗ (-4.82) | -0.401 ∗∗∗ (-4.86)            |
| skew    |                    |                        | -1.38E-04 (-0.93)      |                        | -3.523e-04 ∗∗ (-1.99)  |                    |                               |
| kurt    |                    |                        |                        | -2.12E-05 (-1.37)      | -4.117e-05 ∗∗ (-2.23)  |                    |                               |
| J       |                    |                        |                        |                        |                        | 0.337 ∗∗∗ (4.00)   |                               |
| J + J - |                    |                        |                        |                        |                        |                    | 0.596 ∗∗∗ (5.60) 0.129 (1.25) |
| π t-τ,t | -0.024             | 0.025                  | 0.024                  | -0.026                 | -0.025                 | -0.026 ∗           | -0.037                        |
|         | (-1.25)            | (-1.31)                | (-1.12)                | (-1.32)                | (-1.27)                | (-0.63)            | (-0.88)                       |

Note: This table shows the predictability of one-week-ahead delta-hedged gains from volatility ( vol ), volatility of-volatility ( vov ), and jump (i.e., skew , kurt , J , J + , and J - ) risks. The sample period is July 2010 to June 2018. The values in parentheses are Newey and West (1987) robust t -statistics (with lag 3), significant at the 1%, 5%, and 10% levels, denoted respectively by ∗∗∗ , ∗∗ , and ∗ .


<!-- p:51 -->


Figure 1: Oil market volatility (OVX) and volatility-of-volatility (VOV)

oil volatility Note: This figure plots the Black-Scholes-implied vega (i.e., ∂Ct ∂σt , upper panel) and volga (i.e., ∂ 2 Ct ∂ 2 σ t 2 , lower panel) for USO call options on September 18, 2015, with time to maturity of one month with respect to their moneyness (i.e., m = Se rτ /K ).

Note: This figure shows the time series of OVX (upper panel) and oil VOV (lower panel). The sample period is July 2010 to June 2018.

<!-- p:52 -->


Figure 2: Call vega and volga
