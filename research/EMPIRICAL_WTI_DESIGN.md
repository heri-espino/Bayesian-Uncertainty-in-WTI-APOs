# Empirical WTI Average Price Option design

## Role of the real-data application

The CME WTI application complements rather than replaces the controlled synthetic
experiment. Simulation retains known true parameters and therefore supports
bias/RMSE/coverage. The empirical application asks whether Bayesian parameter
uncertainty is economically material for observed WTI Average Price Options (APOs).

## Contract mechanics

CME WTI APOs settle on the arithmetic average of daily settlement prices of the
**first-nearby Light Sweet Crude Oil (CL) futures contract during the calendar month**.
The real contract must therefore be modeled with the first-nearby roll and observed futures
term structure; a single fixed spot/futures GBM is only a hypothetical benchmark.

## Maturities, strikes, and panel layers

The downloaded maturity set spans Sep-2026, Oct-2026, Nov-2026, Mar-2027, Sep-2027,
Mar-2028, Sep-2028, and Jun-2029. All downloaded near-the-money calls and puts are retained
in the raw panel. A fixed strike can move from OTM to ATM to ITM over its life, so status on
the final download date never defines the historical estimation sample.

`richest_option_series.csv` is an information/data-richness diagnostic based on session
count, calendar span, and field completeness. It is not a liquidity or economic-interest
score. Raw data, main-sample filters, and representative-contract rankings remain separate.

## Historical CL source and roll-safe returns

The automated empirical pipeline uses **individual** Yahoo Finance NYMEX WTI contracts such
as `CLV26.NYM`, `CLX26.NYM`, and `CLZ26.NYM`. Yahoo `CL=F` remains useful as an exploratory
front-month proxy but is not treated as the contractual first-nearby series.

For physical-measure inference, the first-nearby history is reconstructed from the
individual contracts. If the active contract changes between adjacent observations, the
corresponding log return is excluded. The difference between two contracts at the roll can
reflect contango or backwardation and must not be interpreted as a one-day WTI diffusion
shock.

Yahoo daily `Close` is retained as an end-of-day **settlement proxy**. The pipeline supports
a local validation table so selected closes can be compared with CME/Barchart reference
observations without requiring proprietary source data to be committed.

## Effective moneyness

For an APO, current front-month WTI alone is not the right state variable. Define

\[
\widehat A_{t,T}^{Q}=\frac{
\sum_{j\in R_t}F_j^{\mathrm{fix}}+
\sum_{j\in U_t}E_t^Q[F_j^{\mathrm{fix}}]
}{N},
\]

where realized and remaining fixing dates are each mapped to the applicable first-nearby CL
contract. Then

\[
m_{t,K,T}=\log(K/\widehat A_{t,T}^{Q}).
\]

ATM/moderate/deep buckets are descriptive reporting conventions, not acquisition filters.

## Pricing baseline

For remaining fixing date `j`, use the current futures level associated with the
first-nearby contract, `F_j(0)`, and the transparent one-factor Q baseline

\[
F_j(t_j)=F_j(0)\exp[-\tfrac12\sigma^2t_j+\sigma W_{t_j}^{Q}].
\]

The observed term structure and roll enter through `F_j(0)`. Posterior uncertainty is
propagated through `sigma`. Richer term-structure or stochastic-volatility models are
robustness extensions rather than hidden changes to the baseline.

## Date-specific discounting

A single constant discount rate is not used for the empirical panel. The baseline source is
the official U.S. Treasury Daily Treasury Par Yield Curve Rates. The first pilot makes one
approximation explicit: interpolate the dated Treasury **par** curve in maturity and treat
that interpolated yield as a continuously compounded zero-rate proxy,

\[
D(t,T)\approx \exp[-y^{par}_{t}(T-t)(T-t)].
\]

This is a transparent pilot approximation, not a claim that Treasury par yields are
zero-coupon rates. A later robustness specification should replace it with a proper
bootstrapped zero curve or SOFR/OIS discounting while leaving the rest of the APO pipeline
unchanged.

## Volatility regimes

The baseline classification uses 21-day annualized realized volatility and sample quantiles
to define low, medium, and high volatility regimes. Political/geopolitical developments can
be discussed as context only after the quantitative regime classification is fixed.

The main empirical quantity is

\[
\Delta_{FB-PM}=C_{FB}-C_{PM},
\]

studied as a function of effective moneyness, maturity, posterior dispersion in sigma,
volatility regime, option type, partial-fixing status, and liquidity diagnostics.

## First real-market pilot

The first implemented pricing experiment is the October-2026 APO cross-section observed on
2026-09-04. The experiment reconstructs the first-nearby CL history, removes roll-switch
returns, runs multiple Metropolis chains using only information available by the valuation
date, reconstructs the October first-nearby curve from exact-date individual Yahoo closes,
uses a date-specific Treasury discount factor, and prices the observed calls/puts over a
common sigma grid with common random numbers.

It reports Full Bayes, posterior-mean, marginal-sigma-mode, and MLE model prices against the
Barchart market marks. The sigma mode is explicitly a marginal posterior mode, not a joint
MAP estimate. No empirical method-ranking claim enters the manuscript until the run and its
source validation have completed successfully.

The October-2026 pilot currently uses a weekday fixing schedule because the selected month
has no full-day CME energy closure. General production-panel work must replace this pilot
fallback with an explicit exchange settlement calendar.

## Data audit

`experiments/build_wti_apo_panel.py` recursively scans `data/csv`, decodes expiry from each
JAO symbol rather than trusting the folder name, de-duplicates repeated downloads, and
writes a folder/expiry mismatch report. The known `JAOU8` Sep-2028 file located under the
`jun2029` folder remains a useful integrity check.
