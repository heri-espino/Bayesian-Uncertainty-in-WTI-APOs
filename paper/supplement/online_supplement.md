# Online Supplement — Detailed Design and Robustness Evidence

This supplement contains the evidence intentionally omitted from the compact main manuscript.
Sections S1--S4 are the stable locations cited by the paper. The original detailed LaTeX source
from the longer manuscript is preserved afterward as an audit archive.

## S1. Complete historical-volatility benchmarks

Table S1 gives the complete pooled comparison on the same 2,381 out-of-sample APO
contract-date observations and 15 target dates. The rolling-window and EWMA choices were fixed
before inspecting their pricing errors. MAE and RMSE are in U.S. dollars per barrel.

**Table S1. Historical-volatility and prior option-implied volatility benchmarks.**

| Volatility input | N | Dates | MAE | RMSE |
| --- | ---: | ---: | ---: | ---: |
| Long-window historical PI | 2,381 | 15 | 2.6187 | 3.4090 |
| Rolling 252 returns | 2,381 | 15 | 5.2183 | 6.3933 |
| Rolling 126 returns | 2,381 | 15 | 8.3419 | 9.7846 |
| Rolling 63 returns | 2,381 | 15 | 4.5201 | 5.6465 |
| EWMA, half-life 63 days | 2,381 | 15 | 5.6616 | 6.8824 |
| Horizon-matched GARCH(1,1) | 2,381 | 15 | 2.6730 | 3.4441 |
| Earlier-date APO expanding smile | 2,381 | 15 | 0.1088 | 0.1725 |
| Previous-day APO smile | 2,381 | 15 | 0.1075 | 0.1594 |

The GARCH fit is estimated from earlier returns. The target-date return updates only the
end-of-day conditional variance state; parameters are not re-estimated with that return.
Forecast conditional variances are accumulated over each remaining fixing horizon and mapped
to the maintained common-factor constant-volatility APO representation.

## S2. Numerical accuracy and posterior calibration

The empirical PI--PM differences are small, so the numerical audit compares high-precision
pseudo-random Monte Carlo, independently scrambled Sobol pricing, and Curran conditioning.
Across the difficult targets, differences among the three PI--PM estimates are on the order of
micro-dollars, well below the empirical gaps near (10^{-3}) dollars per barrel.

**Table S2. Numerical identification and simulation-based calibration.**

**Panel A. Representative PI--PM differences (U.S. dollars per barrel).**

| Target | Pseudo-MC | Curran | Scrambled Sobol |
| --- | ---: | ---: | ---: |
| 2026-08-27, October call, K=98 | 0.0013683 | 0.0013690 | 0.0013717 |
| 2026-08-28, October call, K=98 | 0.0013394 | 0.0013402 | 0.0013393 |

**Panel B. Simulation-based calibration of the Gaussian volatility posterior.**

| Historical observations n | Mean posterior rank | KS p-value | Empirical 95% coverage |
| ---: | ---: | ---: | ---: |
| 21 | 0.5000 | 0.861 | 0.9500 |
| 63 | 0.4993 | 0.348 | 0.9505 |
| 252 | 0.4978 | 0.210 | 0.9483 |
| 1,260 | 0.5027 | 0.106 | 0.9505 |

The numerical comparison establishes practical resolution of the PI--PM difference; it does not
imply that Curran and Monte Carlo produce identical absolute option prices. The calibration
experiment uses 200,000 prior-predictive datasets in total, with 50,000 replications at each
sample size.

## S3. Liquidity and valuation-date dependence

Contracts observed on the same valuation date share the futures curve, historical posterior,
and market environment. Error differences are therefore resampled by valuation-date cluster.
The qualitative ranking also persists under transaction-activity and open-interest restrictions.

**Table S3. Positive-volume out-of-sample comparison.**

| Volatility input | N | Target-date clusters | MAE | RMSE |
| --- | ---: | ---: | ---: | ---: |
| Historical PI | 62 | 13 | 1.6340 | 2.3391 |
| Earlier-date APO expanding smile | 62 | 13 | 0.1003 | 0.1358 |
| Previous-day APO smile | 62 | 13 | 0.1084 | 0.1333 |

The same direction is preserved at open-interest thresholds of 10, 100, and 500 contracts.
At open interest of at least 100, the option-implied MAEs are approximately 0.106--0.107
versus 1.990 for the historical benchmark. Long-dated positive-volume observations remain
sparse within individual expiries, so maturity-specific transaction-price interpretation is
more limited than the pooled comparison.

## S4. Vanilla-WTI transfer and CRR refinement

The external LO validation uses a fixing-count weighted RMS mapping as its primary transfer from
maturity-specific vanilla-WTI implied volatilities to the scalar volatility required by the
maintained APO pricing model. A second mapping chooses the scalar volatility that matches the
variance of the unresolved arithmetic-average component under the same common-factor
representation.

**Table S4. LO scalar-transfer and tree-refinement diagnostics.**

**Panel A. Alternative LO scalar mapping on the 253-observation common-support sample.**

| Specification | MAE | RMSE |
| --- | ---: | ---: |
| Previous-day LO, primary weighted-RMS mapping | 0.1559 | 0.2599 |
| Previous-day LO, variance-matched mapping | 0.1562 | 0.2612 |
| Expanding LO, primary weighted-RMS mapping | 0.1604 | 0.2858 |
| Expanding LO, variance-matched mapping | 0.1611 | 0.2869 |

**Panel B. Absolute LO implied-volatility changes under CRR refinement.**

| Refinement | Mean | Median | 95th percentile | Maximum |
| --- | ---: | ---: | ---: | ---: |
| 80 to 160 steps | 0.000820 | — | — | — |
| 160 to 320 steps | 0.000402 | 0.000284 | 0.001089 | 0.001810 |

The refinement audit contains 156 stratified LO contract-dates. It establishes practical
stability of the production 160-step inversion at the precision relevant for the external
comparison; it is not a proof of an exact infinite-tree limit. A separate strictly-prior
surface-shape audit contains 144 diagnostics over 12 dates, with no nonpositive or nonfinite
fitted volatilities inside observed prior support and at most one direction change in the fitted
curves.

---

## Archive A. Preserved detailed research-design source

```tex
\section{Research design}\label{sec:design}

\subsection{Synthetic repeated-sampling benchmark}

The simulation study first asks a question that cannot be answered cleanly with market prices alone: when the data-generating volatility is known, how much is lost by collapsing posterior uncertainty before pricing? Historical return samples are generated under $\mathbb P$ and option values are evaluated under $\mathbb Q$, preserving the measure separation in Section~\ref{sec:methodology}. The original production grid varies historical sample size, volatility, moneyness, and maturity and evaluates posterior-integrated, posterior-mean, posterior-mode, and MLE pricing against the external target
\begin{equation}
 C_0=C^Q(\sigma_0).
 \label{eq:synthetic_target}
\end{equation}
The target is not a posterior draw and is not constructed from any estimator being compared.

For method $M\in\{PI,PM,Mode,MLE\}$ and $R$ independent histories, the main statistics are
\begin{align}
 \operatorname{Bias}_M
 &=R^{-1}\sum_{j=1}^{R}(\widehat C_{M,j}-C_0),\\
 \operatorname{MAE}_M
 &=R^{-1}\sum_{j=1}^{R}|\widehat C_{M,j}-C_0|,\\
 \operatorname{RMSE}_M
 &=\left[R^{-1}\sum_{j=1}^{R}(\widehat C_{M,j}-C_0)^2\right]^{1/2}.
 \label{eq:metrics}
\end{align}

\subsection{Massive mechanism map}

The large mechanism experiment is designed around Equation~\eqref{eq:taylor_gap}. It uses
\begin{align}
 n&\in\{21,42,63,126,252,504,1260\},\\
 \sigma_0&\in\{0.10,0.20,0.35,0.50,0.80\},
\end{align}
with 5,000 independently generated histories in each $(n,\sigma_0)$ cell, for 175,000 synthetic datasets. The contract layer crosses four maturities (21, 63, 126, and 252 days), seven moneyness values from 0.60 to 1.50, and six partial-fixing states from zero to nearly the full averaging window.

Because the Gaussian prior on $\mu$ is conjugate to the likelihood conditional on $\sigma$, $\mu$ is integrated analytically. The remaining posterior in $\sigma$ is evaluated on a dense deterministic grid. This removes random-walk Metropolis error from the mechanism map while retaining exactly the baseline Gaussian statistical model. For each history and contract state the experiment computes $\Delta_{PI,PM}$, posterior variance of $\sigma$, local price curvature, and the Taylor approximation in Equation~\eqref{eq:taylor_gap}. The purpose is not merely to show that a gap can be made large, but to characterize the state variables that make posterior integration economically relevant.

\subsection{Empirical option panel}

The raw empirical sample contains every downloaded WTI APO history rather than a hand-selected set of strikes. The unit of observation is option $i$ on trading date $t$, identified by option type, strike, expiry month, and symbol. The raw panel contains 213 unique contracts and 11,179 option-date observations. The sample is intentionally unbalanced because strike availability and liquidity decline at longer maturities.

Three data layers remain separate. The \emph{raw panel} preserves all parsed observations. The \emph{main empirical panel} applies transparent data-quality and pricing-availability rules. The \emph{representative-contract set} is used only for figures and economic discussion. The October-2026 baseline contains 310 retained contract-date observations across 12 eligible valuation dates. Five dates contain at least one option with positive reported volume, and six individual contract-date observations report positive daily volume themselves.

\subsection{Reconstructing first-nearby fixings and moneyness}

Each option-date observation is linked to the information set required by the APO payoff. The pipeline reconstructs: (i) realized first-nearby settlements for fixing dates already elapsed, (ii) the relevant CL futures contracts for remaining fixing dates, and (iii) the contemporaneous futures term structure used to initialize those remaining fixings. This mapping produces $\widehat A^Q_{t,T}$ in Equation~\eqref{eq:expected_average} and the observation-specific moneyness measure in Equation~\eqref{eq:moneyness}.

The baseline physical-measure inference uses Yahoo \texttt{CL=F} as a labelled continuous/front-month return proxy; it is not used as a contractual substitute for the first-nearby sequence that determines the APO payoff. A dedicated source-robustness experiment reconstructs the historical first-nearby return series contract by contract from official final CL settlements. Each trading date is assigned to the earliest contract whose last-trade date has not passed. Returns spanning a contract switch are excluded so that contango or backwardation is not treated as a one-day diffusion shock. Four isolated mapped settlement gaps are retained in the audit trail but not imputed; any one-day return depending on a missing price is also excluded. The resulting 2024--2026 reconstruction contains 632 usable daily returns and 33 mapped roll switches, compared with 676 usable Yahoo returns over the same inference window.

Valuation uses committed Barchart individual CL histories with explicit last-trade dates. In the Barchart histories used here, \texttt{Latest} is the CME settlement field; the source-field name is retained for provenance and is not interpreted as an intraday last trade.

\subsection{Rolling physical-measure uncertainty}

Let $\mathcal D_t$ denote the historical information set available at date $t$. For an expanding sample beginning in January 2024, the posterior
\begin{equation}
 p(\sigma\mid\mathcal D_t)
\end{equation}
is estimated without using future returns. Each option-date observation is then priced using posterior integration, posterior-mean volatility, the marginal posterior mode, and the historical MLE. This rolling construction prevents later returns from contaminating earlier valuation dates.

The principal pricing errors are
\begin{equation}
 e^M_{i,t}=P^{M}_{i,t}-P^{mkt}_{i,t},
\end{equation}
where $P^{mkt}_{i,t}$ is the Barchart end-of-day settlement field and $M$ indexes the pricing rule. Mean error, MAE, and RMSE are reported overall and within liquidity-restricted samples.

To separate information source from information recency, a pre-specified recent-history benchmark reuses the exact strict-forward holdouts and target-date information cutoffs. It evaluates annualized realized volatility from the most recent 63, 126, and 252 usable daily returns, plus an exponentially weighted estimate with a 63-business-day half-life. These choices are fixed before inspecting their pricing errors. Each scalar estimate is mapped through the same Curran APO pricing engine used for the prior-date smile predictions. The purpose is not to optimize a historical window ex post, but to ask whether a reasonable recent historical benchmark materially narrows the option-informed advantage.

A stronger historical forecast benchmark uses a Gaussian GARCH(1,1), a standard class in crude-oil volatility forecasting \cite{gildertsiaras2020}. For each target date, parameters are estimated only from usable returns dated strictly before that date,
\begin{equation}
 h_{t+1}=\omega+\alpha\varepsilon_t^2+\beta h_t,
 \qquad \alpha+\beta<1.
 \label{eq:garch11}
\end{equation}
The observed target-date return is then used only to update the end-of-day conditional variance state, not to re-estimate parameters. Expected daily variances are forecast over the remaining business-day horizon and accumulated to each unresolved fixing date. Those cumulative variances define the common-factor covariance of the remaining futures fixings. Finally, a single annualized $\sigma_{GARCH}$ is chosen so that the constant-volatility pricing representation matches the arithmetic-average variance implied by the GARCH forecast path. The resulting horizon-matched scalar is evaluated on the same 2,381 strict-forward holdouts.

A second scalar sensitivity uses Equation~\eqref{eq:sigma_rms}. Because every empirical run already stores the posterior mean and standard deviation of $\sigma$, the posterior-RMS comparator can be evaluated on the same holdouts without rerunning MCMC.

\subsection{APO-implied volatility and cross-sectional validation}

The initial September and October panels provide 402 contract-date observations for implied-volatility analysis. Contract-level implied volatilities are obtained by inverting Equation~\eqref{eq:apo_iv}. A date-level common $\sigma_Q$ is then calibrated by minimizing cross-sectional settlement squared error. Two deliberately harder checks avoid evaluating a contract on information extracted from that same contract: leave-one-contract-out calibration excludes the target option, and cross-option-type transfer estimates from calls and evaluates puts or vice versa.

These exercises remain cross-sectional. The primary predictive robustness design is therefore strictly forward in time. For each target date and expiry, the volatility smile is estimated using only APO implied-volatility observations from dates strictly earlier than the target. Two schemes are considered: a \emph{previous-day smile} using the latest earlier completed date and an \emph{expanding smile} using all earlier dates with exponential recency weights. Same-day implied volatility is retained only as an ex-post diagnostic and never enters the target-date fit.

A persistence benchmark asks whether the fitted previous-day smile adds information beyond simply carrying forward the same contract's latest strictly prior APO implied volatility. The carried volatility is repriced using the target-date futures curve, realized-fixing state, discount factor, and remaining fixing schedule. Thus the benchmark preserves a transparent current-state adjustment while excluding same-day APO information. A committed-data coverage audit requires at least six main-sample contracts on a date before an expiry is admitted to the smile experiment. Seven expiries pass that screen---September, October, and November 2026; March and September 2027; and March and September 2028---while June 2029 does not. The extended evaluation contains 2,381 option-date holdouts over 15 distinct target dates, with results reported both pooled and separately by expiry.

\subsection{Independent vanilla-WTI forward validation}\label{sec:external_lo_design}

The APO prior-date smile establishes that option-market volatility information is forward-relevant, but it does not by itself rule out a within-family explanation. The independent validation therefore constructs a risk-neutral state from standard monthly WTI futures options (LO) and uses it to predict October-2026 APO settlements. Raw vendor records are kept local; only reproducible query metadata, diagnostics, and derived results are versioned.

The acquisition window is August 24 through September 10, 2026, with CME trading reference date used for temporal ordering. The final strike range is 70--120 on the two CL futures contracts required by the October APO fixing schedule, CLX6 and CLZ6. Final official LO settlements are paired with official CL futures settlements and inverted using Equation~\eqref{eq:lo_iv}. The resulting panel contains 5,220 successful contract-date implied-volatility inversions over 13 reference dates. Of these settlements, 5,214 are flagged actual and six theoretical.

For each target APO date $t$, every LO observation used to fit the external surface satisfies $s<t$. The \emph{previous-day} surface uses only the latest completed LO reference date; the \emph{expanding} surface uses all earlier reference dates with a five-calendar-day exponential half-life. The primary specification evaluates the fitted surface separately for CLX6 and CLZ6 at each APO strike and combines the component volatilities with the fixing-count RMS rule in Equation~\eqref{eq:lo_effective_sigma}. A pre-specified sensitivity instead chooses the scalar volatility that matches the variance of the unresolved arithmetic-average component under the maintained common-factor representation, using target-date futures levels and fixing times. Same-day APO prices are never used to estimate the external state.

The final October comparison is matched at the contract-date level. Across the 280 observations shared by the historical baseline, the two external LO specifications, and the two prior-date APO smiles, 253 contract-dates lie inside the observed prior LO moneyness support for both external surface specifications. This 90.4\% no-clipping subset spans all 10 matched valuation dates and is the primary external-validation sample. Error differences are resampled by valuation-date cluster with 100,000 bootstrap replications so that contracts sharing one market date are not treated as independent observations.

\subsection{Heavy-tail robustness under the physical measure}

To test whether the Gaussian historical likelihood drives the pricing hierarchy, the physical-measure innovation is replaced by a standardized Student-$t$ variable,
\begin{equation}
 R_i=
 \left(\mu-\frac12\sigma^2\right)\Delta t
 +\sigma\sqrt{\Delta t}\,\varepsilon_i,
 \qquad
 \operatorname{Var}(\varepsilon_i)=1,
\end{equation}
with degrees of freedom inferred jointly with $\mu$ and $\sigma$. The $Q$ pricing dynamics, realized fixings, futures curve, and pricing map are otherwise unchanged. The production robustness run uses eight chains of 100,000 iterations per unique valuation date and covers 402 option-date observations across the September and October expiries.

\subsection{Numerical accuracy and posterior calibration}

Small values of $\Delta_{PI,PM}$ are scientifically useful only if they are larger than pricing noise. Eighteen empirically difficult contracts are therefore repriced over a dense volatility grid with independent high-precision pseudo-random Monte Carlo runs. Eight common difficult targets are also evaluated with independently scrambled Sobol sequences, and Curran conditioning is evaluated on the same volatility grids. The budgets are chosen so that direct Monte Carlo uncertainty in the PI--PM gap is typically of order $10^{-6}$, well below the observed empirical gaps near $10^{-3}$.

Posterior implementation is checked separately by simulation-based calibration. Two hundred thousand datasets are drawn from the prior predictive distribution, with 50,000 replications at each of $n=21,63,252,1260$. Calibration is assessed through posterior-CDF ranks and 50\%, 80\%, and 95\% credible-interval coverage.

\subsection{Liquidity dependence and clustered uncertainty}

Contracts observed on the same valuation date share the futures curve, historical posterior, and market shock, so treating option rows as independent would overstate precision. Error comparisons are therefore bootstrapped by valuation-date cluster rather than by individual contract. The production robustness analysis uses 100,000 cluster resamples for the full sample, the positive-volume subset, and open-interest thresholds of 1, 10, 100, and 500 contracts. The bootstrap reports percentile intervals and the probability that a candidate specification improves MAE or RMSE relative to the historical-volatility posterior-integrated baseline.

```

---

## Archive B. Preserved robustness and numerical-diagnostics source

```tex
\section{Robustness and extensions}\label{sec:robustness}

The completed robustness analysis asks whether the paper's main hierarchy survives changes in statistical assumptions, numerical pricing engines, posterior calibration checks, and liquidity weighting. The purpose is not to search for a specification that mechanically minimizes in-sample error, but to determine which conclusions are stable and which remain sample-dependent.

\subsection{Prior and estimation-window sensitivity}

The inverse-gamma prior in Equation~\eqref{eq:priors} is not treated as uniquely correct. A dedicated sensitivity experiment compares the baseline prior with two alternatives centered near 0.40 and estimation windows of 63, 126, 252, 504, and 673 daily returns. Four chains of 20,000 iterations are used for each specification, with maximum observed $\hat R_\sigma$ of 1.0007.

The main distinction is between prior sensitivity and window sensitivity. With 673 returns, posterior mean volatility is 0.4151 under the baseline prior, 0.4153 under a broad WTI-centered prior, and 0.4153 under a more concentrated WTI-centered prior. The corresponding Curran posterior-integrated prices are 0.6419, 0.6430, and 0.6428. Thus reasonable prior changes are negligible once the likelihood is informative. With only 63 observations, prior effects become visible at the cent level, while the PI--PM gap itself reaches approximately 0.0146. Changes in the historical window are materially larger because the windows span different realized volatility regimes.

This experiment prices one representative difficult contract and therefore diagnoses sensitivity of the posterior-integration mechanism; it is not the same as a comprehensive forward comparison on all 2,381 holdouts. The exact-holdout historical benchmarks in Section~\ref{sec:design} address that distinct question without selecting the historical window after seeing pricing errors.

\subsection{Dynamic historical-volatility forecasting}

A horizon-matched Gaussian GARCH(1,1) provides a stronger historical benchmark than rolling or exponentially weighted realized volatility because it explicitly forecasts conditional variance over the remaining APO fixing horizon. Parameters are fitted strictly before each target date; the target-date return updates only the conditional variance state. The forecast variance path is then collapsed to the constant-volatility pricing representation by matching the unresolved arithmetic-average variance.

All target-date fits converge. Estimated persistence $\alpha+\beta$ ranges from 0.9787 to 0.9820, while the implied long-run annualized volatility ranges from 0.4050 to 0.4167. The target-date updated one-day annualized state varies more substantially, from 0.3619 to 0.4908, and the resulting horizon-matched effective APO volatility ranges from 0.3617 to 0.4818 across date-expiry states. The benchmark therefore does react to recent conditions and remaining maturity rather than reproducing a fixed long-window scalar.

Those additional dynamics do not materially improve pooled pricing relative to the long-window historical baseline reported in Table~\ref{tab:recent_history_persistence}. GARCH improves RMSE modestly for October 2026 and September 2028, but is worse than the long-window historical baseline in the other five expiries and remains far above the previous-day APO-smile RMSE in every expiry. The historical-versus-option-informed comparison therefore does not hinge on treating historical volatility as static.

\subsection{Heavy-tailed physical-measure returns}

WTI returns are not especially well described by Gaussian innovations. Replacing the Gaussian likelihood under $\mathbb P$ with standardized Student-$t$ innovations produces posterior mean degrees of freedom around 3.8 across valuation dates, with posterior medians near 3.74--3.77. The data therefore support substantially heavier tails than the Gaussian benchmark.

The change does not overturn the main pricing hierarchy. Across 402 September--October contract-date observations, Student-$t$ posterior-integrated pricing has MAE 0.3263 and RMSE 0.4418, compared with 0.3444 and 0.4616 for the Gaussian posterior-integrated baseline. The improvement is approximately 5\% in MAE and 4\% in RMSE. Among nine positive-volume observations, MAE falls from 0.1249 to 0.1125 and RMSE from 0.1572 to 0.1413. Heavy tails therefore improve the physical-measure volatility estimate modestly, but the remaining error is still far larger than the within-model PI--PM correction.

The Student-$t$ volatility posterior is also wider: posterior standard deviations are roughly 0.027 rather than approximately 0.011 in the Gaussian long-window baseline. Even with that additional uncertainty, posterior-integrated and posterior-mean Student-$t$ prices remain close. This provides a direct robustness check on the claim that the observed pricing map is locally smooth relative to posterior dispersion.

\subsection{Contract-reconstructed physical volatility}

The baseline physical-measure analysis uses Yahoo \texttt{CL=F} as a reproducible continuous/front-month proxy, so a natural concern is that its undocumented roll construction may distort the historical volatility benchmark. A dedicated robustness experiment reconstructs the first-nearby settlement history contract by contract from official final CL settlements over the same January 2024--September 2026 inference window. The mapping contains 33 contract switches. Every return spanning a switch is excluded, and four isolated mapped settlement gaps are left missing rather than imputed; any one-day return that depends on a missing settlement is excluded as well.

The reconstructed series contains 632 usable daily returns, versus 676 for Yahoo. Its annualized realized volatility is 0.4183, compared with 0.4167 for Yahoo. Under the same Gaussian likelihood and prior, the posterior mean of $\sigma$ is 0.4182 with posterior standard deviation 0.0117, versus 0.4165 and 0.0112 under Yahoo. After normalizing Yahoo timestamps to trading dates, the 632 overlapping usable returns have correlation 0.9935 and mean absolute return difference 0.00051. Thus the two physical-volatility inputs are empirically very similar away from the deliberately excluded roll transitions.

The pricing result is equally stable. On exactly the same 2,381 strict-forward holdouts, replacing Yahoo with the reconstructed first-nearby history changes the historical posterior-integrated MAE/RMSE from 2.6187/3.4090 to 2.6468/3.4451. The expanding and previous-day option-informed errors remain 0.1088/0.1725 and 0.1075/0.1594 because their risk-neutral states are unchanged. On the 253-observation external-LO common-support sample, the reconstructed historical baseline has MAE 0.4362 and RMSE 0.5466, while the external previous-day LO surface remains at 0.1559 and 0.2599. The valuation-date cluster bootstrap still separates external LO from reconstructed historical volatility: the MAE difference is $-0.2804$ with a 95\% interval of $[-0.3329,-0.2243]$, and the RMSE difference is $-0.2867$ with interval $[-0.3399,-0.2490]$.

This check addresses the specific concern that the comparison between the long-window historical benchmark and option-informed inputs is an artifact of Yahoo's continuous-contract construction. It is not: the physical posterior barely moves and the pricing comparison is essentially unchanged.

\subsection{Scalar-volatility and external-LO sensitivities}

The posterior-RMS plug-in provides a direct scalar sensitivity to the posterior-mean choice. Across the 2,381 strict-forward holdouts,
\[
\sigma_{RMS}=\sqrt{\mathbb E[\sigma^2\mid\mathcal D]}
\]
exceeds the posterior mean by only 0.000153 on average. Repricing at \(\sigma_{RMS}\) changes the model value by 0.00325 on average in absolute terms, with a maximum absolute change of 0.00558. For this sensitivity only, both scalar summaries are repriced under the same deterministic Curran engine: pooled MAE/RMSE are 2.6185/3.3955 for the posterior-mean plug-in and 2.6211/3.3989 for the posterior-RMS plug-in. These values are not alternative estimates of the main historical PI benchmark in Table~\ref{tab:forward_q}, whose RMSE 3.4090 comes from the canonical Monte Carlo posterior-integrated specification. The common-engine comparison isolates the choice of scalar posterior summary, which is negligible relative to the volatility-input differences documented in Section~\ref{sec:results}.

The LO-to-APO transfer is similarly insensitive to replacing the fixing-count RMS rule with a variance-matched scalar based on the unresolved arithmetic-average component. On the exact 253-observation common-support sample, the moment-matched previous-day LO surface has MAE 0.1562 and RMSE 0.2612, compared with 0.1559 and 0.2599 under the primary weighted-RMS transfer. The expanding surface changes from 0.1604/0.2858 to 0.1611/0.2869. Thus the external-option conclusion is not driven by treating fixing-count-weighted RMS volatility as an exact variance identity.

The American-option inversion is also stable to tree refinement at the precision relevant here. A deterministic stratified audit of 156 LO contract-dates spanning reference date, underlying, option type, and low/ATM/high moneyness re-inverts volatility with 80, 160, and 320 CRR steps. The mean absolute IV difference falls from 0.000820 between 80 and 160 steps to 0.000402 between 160 and 320; for the latter comparison the median, 95th percentile, and maximum absolute differences are 0.000284, 0.001089, and 0.001810. This refinement pattern does not establish an exact infinite-tree limit, but it shows that the production 160-step inversion is numerically stable relative to the scale of the fitted LO surface.

Finally, a strictly-prior LO surface-shape audit produces 144 diagnostics over 12 target dates. No fitted volatility inside observed prior support is nonpositive or nonfinite, the fitted curves have at most one direction change, and the mean fitted call--put IV gap on overlapping support is 0.00099, with maximum 0.00634. These diagnostics are sanity checks on the quadratic surface representation rather than a claim of a fully arbitrage-free volatility surface.

\subsection{Numerical robustness: Monte Carlo, Sobol, and Curran}\label{sec:numerical_robustness}

The empirical PI--PM gaps are sufficiently small that numerical error is a first-order methodological concern. The high-precision benchmark therefore recomputes difficult contracts using three distinct engines. Pseudo-random Monte Carlo uses antithetic paths and an arithmetic-average control variate with known $Q$ expectation. Randomized Sobol uses independently scrambled low-discrepancy sequences without that control variate. Curran conditioning supplies a deterministic approximation under the same one-factor futures dynamics.

Across the difficult targets, the three engines agree on PI--PM to within a few micro-dollars. Direct seed-to-seed Monte Carlo uncertainty for the PI--PM gap is generally of order $10^{-6}$, compared with empirical gaps near $10^{-3}$; randomized-Sobol scramble uncertainty is of similarly smaller order. The conclusion that posterior integration adds little to the October point-price mean is therefore numerically identified rather than an artifact of insufficient simulation.

For representative October calls, the August 27, 2026 $K=98$ contract has a pseudo-Monte Carlo PI--PM gap of 0.0013683, a Curran gap of 0.0013690, and a randomized-Sobol gap of 0.0013717. The August 28 $K=98$ call gives 0.0013394, 0.0013402, and 0.0013393, respectively. Figure~\ref{fig:numerical_identification} shows all eight difficult empirical targets common to the three engines.

\begin{figure*}[t]
\centering
\includegraphics[width=\textwidth]{figures/publication/fig04_numerical_identification.pdf}
\caption{Numerical identification of the posterior-integration effect on eight difficult WTI APO targets. Panel A compares the PI--PM price difference from high-precision pseudo-random Monte Carlo, Curran conditioning, and independently randomized Sobol pricing; error bars show 95\% Monte Carlo or scramble-based intervals where applicable. Panel B reports deviations of the stochastic estimates from the deterministic Curran gap in units of $10^{-6}$ price units. Agreement at this scale shows that the observed sub-cent PI--PM differences are resolved well above numerical noise, even though the three engines need not produce identical absolute option prices.}
\label{fig:numerical_identification}
\end{figure*}

Curran prices can differ from Monte Carlo point prices by small amounts that are larger than the PI--PM correction itself. This is another useful distinction: pricing-engine approximation is a separate model/numerical margin from posterior integration. Importantly, Curran, Monte Carlo, and Sobol still produce almost the same \emph{difference} between PI and PM, so the integration conclusion does not depend on the chosen engine.

\subsection{Simulation-based calibration}

The Gaussian posterior implementation is validated with 200,000 prior-predictive datasets. After constructing the posterior CDF consistently with the trapezoidal quadrature density, posterior ranks are close to Uniform$(0,1)$ at every sample size.

For $n=21,63,252,$ and $1260$, rank means are 0.5000, 0.4993, 0.4978, and 0.5027, respectively; the target is 0.5. Rank variances are all close to $1/12$. Kolmogorov--Smirnov $p$-values are 0.861, 0.348, 0.210, and 0.106, so the experiment does not detect systematic rank non-uniformity. Empirical 95\% coverage is 0.9500, 0.9505, 0.9483, and 0.9505, with similarly accurate 50\% and 80\% coverage. Mean posterior bias in $\sigma$ is near zero. The calibration experiment therefore supports the statistical implementation used by the mechanism map and baseline posterior calculations.

\subsection{Liquidity and valuation-date dependence}

Option rows from the same date are not independent because they share the futures curve, historical posterior, and market environment. The robustness analysis therefore resamples valuation-date clusters rather than individual option contracts. In the extended forward experiment, the pooled sample contains 2,381 option-date observations over 15 distinct valuation-date clusters and seven expiries.

For the expanding prior-date smile, the pooled MAE difference relative to the historical-volatility posterior-integrated baseline is $-2.5099$, with a 95\% valuation-date cluster-bootstrap interval of $[-2.8297,-2.3000]$; the RMSE difference is $-3.2365$, with interval $[-3.5345,-3.0342]$. The previous-day smile produces corresponding differences of $-2.5112$ and $-3.2496$. Every resampled date-cluster draw in the reported bootstrap has lower error for these comparisons. This is a resampling result conditional on the observed dates, not a probability statement about all future market histories. The same direction survives open-interest thresholds of 10, 100, and 500.

The transaction-active pool is now materially larger than in the original September--October experiment. Across 62 positive-volume holdouts over 13 valuation-date clusters, the expanding smile lowers MAE by 1.5337 with a 95\% interval of $[-1.9039,-1.0401]$ and lowers RMSE by 2.2034 with interval $[-2.7027,-1.4213]$. The previous-day specification gives nearly identical conclusions. Thus the pooled positive-volume evidence now supports the same direction as the broader cross section. This does not eliminate the liquidity caveat: positive-volume observations remain sparse within individual long-dated expiries, especially in 2028, so maturity-specific inference is better supported by the denser open-interest-filtered panels than by transaction counts alone.

The expiry-level bootstrap reinforces that the pooled result is not generated by one maturity. For the expanding smile, the MAE improvement interval excludes zero for every expiry from September 2026 through September 2028. The absolute improvement grows with maturity because the historical volatility near 0.416 increasingly exceeds the lower effective APO volatility embedded in the 2027--2028 cross sections. This maturity pattern is economically informative but should not be read as a structural estimate of a long-run risk-neutral diffusion coefficient: stale marks, term-structure effects, smile dynamics, and model misspecification can all be absorbed by the one-factor implied-volatility state.

Cross-sectional calibration still reveals an important limitation. Leave-one-contract-out APO calibration strongly improves the broad September--October sample, while some narrow transaction-active and cross-option-type subsets are less stable. Those reversals are consistent with a non-flat implied-volatility surface and with calls and puts occupying different moneyness regions. They remain evidence against interpreting one common $\sigma_Q$ as a complete structural model of the APO cross-section.

\subsection{Interpretation of option-informed risk-neutral volatility}

The APO-implied exercise is intentionally endogenous to the option market being studied, so by itself it cannot show that the forward improvement survives outside the target family. The independent LO experiment supplies that missing check. It constructs the risk-neutral state from standard monthly WTI options and matching CL futures settlements, uses only dates strictly earlier than each APO target date, and then transfers the resulting surface to the APO fixing horizon. This design mirrors the market-calibration logic of \cite{shirayatakahashi2011} at a deliberately simpler model level: vanilla WTI options supply risk-neutral information before the average option is valued.

The external result strengthens the interpretation of the forward-smile evidence. On the 253 no-clipping common-support contract-dates, the previous-day LO surface has RMSE 0.2599 versus 0.5562 for historical PI and 0.2686 for the previous-day APO smile. The expanding LO and APO surfaces are similarly close. Valuation-date cluster bootstraps separate either option-informed specification from the long-window historical baseline, while most LO-versus-APO differences are small. The empirical conclusion is therefore not that one option family supplies a universally superior volatility estimate, nor that the experiment isolates a pure structural $\mathbb P$--$\mathbb Q$ wedge. It shows that the pricing advantage of recent option-informed volatility survives a cross-instrument construction.

Strike dependence remains important. The initial LO pilot covered only strikes 85--94.5 and placed just 60 of 280 matched contract-dates inside genuine prior moneyness support. Expanding the observed strike range to 70--120 raises common support to 253 observations, or 90.4\% of the matched sample, and reduces clipped external-surface rows to 50 of 620. This progression shows why a scalar or narrowly supported volatility comparison is insufficient. The result should still not be reduced to a claim that risk-neutral volatility is simply higher than physical volatility: the APO maturity structure changes sign relative to the historical level, and both the LO and APO cross sections contain smile information. The relevant object is an effective volatility surface under the maintained pricing map, not a unique structural diffusion coefficient.

\subsection{Remaining model and data limitations}

Several limitations remain relevant to the scope of the conclusions. The main historical tables retain Yahoo \texttt{CL=F} as the baseline return source for comparability, although the contract-reconstructed first-nearby robustness above shows that the empirical hierarchy is insensitive to that choice. The four isolated missing settlements in the reconstructed series are not imputed and all affected one-day returns are excluded. In the Barchart histories used here, \texttt{Latest} is the CME settlement field. Discounting uses an interpolated Treasury par-yield approximation rather than a bootstrapped OIS curve.

The pricing dynamics remain one-factor and constant-volatility. A correlated multi-factor futures curve, stochastic volatility, jumps, or mean reversion could improve absolute fit and would introduce additional uncertain parameters. Such models are natural extensions, but they should be evaluated separately from the narrower question answered here: conditional on a specified pricing map, how much does posterior integration add beyond a point estimate?

Finally, the forward-validation panel spans seven expiries from September 2026 through September 2028 but only 15 distinct target dates, while the independent vanilla experiment is concentrated on the October-2026 fixing structure and 10 matched APO valuation dates. Date-cluster resampling preserves within-date dependence but does not by itself remove serial dependence across adjacent dates. Liquidity also remains uneven: positive daily volume is sparse in the longest-dated APO expiries even when open interest is nonzero. The long-maturity evidence should therefore be interpreted as validation against available end-of-day market marks rather than as a dense transaction-price study. In the LO inversion panel, 5,214 of 5,220 settlements are flagged actual and six theoretical; this distinction is retained as a data-quality diagnostic rather than hidden. Broader cross-expiry vanilla validation would further strengthen external validity.

```
