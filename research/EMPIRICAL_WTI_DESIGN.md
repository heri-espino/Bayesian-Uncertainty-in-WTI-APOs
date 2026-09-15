# Empirical WTI Average Price Option design

## Role of the real-data application

The CME WTI application complements rather than replaces the controlled synthetic
experiment.  Simulation retains known true parameters and therefore supports
bias/RMSE/coverage.  The empirical application asks whether Bayesian parameter
uncertainty is economically material for observed WTI Average Price Options (APOs).

## Contract mechanics

CME WTI APOs settle on the arithmetic average of daily settlement prices of the
**first-nearby Light Sweet Crude Oil (CL) futures contract during the calendar
month**.  The real contract must therefore be modeled with the first-nearby roll
and the observed futures term structure; a single fixed spot/futures GBM is only
a hypothetical benchmark.

## Maturities and strikes

The downloaded maturity set intentionally spans the curve:

- Sep-2026, Oct-2026, Nov-2026;
- Mar-2027, Sep-2027;
- Mar-2028, Sep-2028;
- Jun-2029.

All downloaded near-the-money calls and puts are retained in the raw panel.  WTI
moved sharply during the sample, so a fixed strike can move from OTM to ATM to
ITM over its life.  Selecting contracts only from their status on the final
download date would create avoidable selection bias.

## What `richest_option_series.csv` means

The existing `data/build_option_series_properties.py` file defines an
**information/data-richness** score:

- 45% session count;
- 30% calendar span;
- 25% numerical-field completeness.

That score is useful for finding long and complete histories, but it is **not a
liquidity score and not an economic-interest score**.  A series can be labelled
`rich` even with zero trading volume and low open interest.  The empirical design
therefore keeps data richness as one diagnostic rather than using
`richest_option_series.csv` to choose the estimation sample.

## Three data layers

1. **Raw panel.** Keep every downloaded contract/date observation and preserve
   raw Barchart fields. Zero-volume days are not automatically deleted because
   an exchange end-of-day mark can still be economically informative.
2. **Main empirical panel.** Apply transparent quality filters only after the
   raw panel is built. Baseline candidates are positive open interest, a usable
   market price, and a sensitivity analysis that includes/excludes minimum-tick
   observations.
3. **Representative contracts.** Choose a small number only for figures and
   discussion. Rank them using history length, non-minimum-tick prices, open
   interest, ATM days, and moneyness crossings. This ranking must not determine
   which observations enter the main error calculations.

## Effective moneyness

For an APO, current front-month WTI alone is not the right state variable,
especially after the averaging month begins. Define

\[
\widehat A_{t,T}^{Q}=\frac{
\sum_{j\in R_t}F_j^{\mathrm{fix}}+
\sum_{j\in U_t}E_t^Q[F_j^{\mathrm{fix}}]
}{N},
\]

where `R_t` are already-realized fixings and `U_t` are remaining fixing dates,
each mapped to the appropriate first-nearby CL contract. Then

\[
m_{t,K,T}=\log(K/\widehat A_{t,T}^{Q}).
\]

Descriptive buckets are initially `|m| <= 0.05` (ATM), `0.05 < |m| <= 0.15`
(moderate), and `|m| > 0.15` (deep). These are reporting buckets, not sample
selection rules.

## Pricing baseline

For remaining fixing date `j`, use the current futures level associated with the
first-nearby contract, `F_j(0)`, and the transparent one-factor Q baseline

\[
F_j(t_j)=F_j(0)\exp[-\tfrac12\sigma^2t_j+\sigma W_{t_j}^{Q}].
\]

The observed term structure and roll enter through `F_j(0)`. Posterior uncertainty
is propagated through `sigma`. A richer term-structure or stochastic-volatility
model is a robustness extension rather than something to hide inside the first
empirical specification.

## Volatility regimes

The recent WTI episode provides useful high-volatility variation, but geopolitical
labels should not be assigned causally by hand. The baseline classification uses
21-day annualized realized volatility and sample quantiles to define low, medium,
and high volatility regimes. Political/geopolitical events can be discussed as
context after the quantitative regime classification.

The main empirical quantity is

\[
\Delta_{FB-PM}=C_{FB}-C_{PM},
\]

studied as a function of effective moneyness, maturity, posterior dispersion in
sigma, volatility regime, call/put status, and liquidity diagnostics.

## Data audit

`experiments/build_wti_apo_panel.py` recursively scans `data/csv`, decodes expiry
from each JAO symbol rather than trusting the folder name, de-duplicates repeated
contract downloads, and writes a folder/expiry mismatch report. This is important
because the current repository already contains at least one apparent folder/root
mismatch (a `JAOU8` Sep-2028 contract inside the `jun2029` folder).
