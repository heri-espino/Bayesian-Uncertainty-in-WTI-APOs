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

## Market-data source architecture

The current empirical design separates physical-measure inference from the contract-specific
curve used for valuation.

- **APO market marks:** committed Barchart option histories under `data/csv`.
- **Historical volatility inference:** Yahoo `CL=F`, explicitly labelled as a continuous/front-month proxy.
- **Valuation-date CL curve:** committed Barchart `Daily Prices` histories under `data/csv/CL`.
- **CL last-trade dates:** explicit versioned study table `data/csv/CL/contract_expiries.csv`.
- **Discounting:** U.S. Treasury Daily Treasury Par Yield Curve Rates.
- **Independent Q-state validation:** Databento CME/NYMEX standard monthly WTI options (`LO`) and official statistics, stored only as local proprietary inputs.

A live workstation run showed that Yahoo may return 404 / `YFTzMissingError` for older
delisted monthly CL symbols. The canonical pilot therefore does not require Yahoo individual
contract histories. Yahoo `CL=F` is not used as the APO fixing curve.

Barchart `Latest` is retained as an end-of-day **settlement proxy**. It is not asserted to be
an official CME settlement without separate validation.

## Physical-measure return sample

The current pilot estimates the GBM volatility posterior from Yahoo `CL=F` returns using only
information available through the valuation date. This is an explicit measurement
compromise: Yahoo does not document the historical `CL=F` roll convention precisely enough
to call the series a self-reconstructed CME first-nearby history.

If a later source provides a complete monthly CL history, the preferred robustness
specification is to reconstruct first-nearby returns contract by contract and exclude every
return spanning a roll. The difference between two contracts at a roll can reflect contango
or backwardation and must not be interpreted as a one-day diffusion shock.

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

For remaining fixing date `j`, use the valuation-date Barchart CL level associated with the
first-nearby contract, `F_j(0)`, and the transparent one-factor Q baseline

\[
F_j(t_j)=F_j(0)\exp[-\tfrac12\sigma^2t_j+\sigma W_{t_j}^{Q}].
\]

The observed term structure and roll enter through `F_j(0)`. Posterior uncertainty is
propagated through `sigma`. Richer term-structure or stochastic-volatility models are
robustness extensions rather than hidden changes to the baseline.

For an averaging month `M`, the current-month CL contract has terminated before the averaging
month begins. First-nearby fixings therefore use the `M+1` delivery contract until its
last-trade date and the `M+2` delivery contract thereafter. The 14 committed Barchart CL
files cover the two contracts required by each observed APO maturity.

## Date-specific discounting

A single constant discount rate is not used for the empirical panel. The baseline source is
the official U.S. Treasury Daily Treasury Par Yield Curve Rates. The first pilot makes one
approximation explicit: interpolate the dated Treasury **par** curve in maturity and treat
that interpolated yield as a continuously compounded zero-rate proxy,

\[
D(t,T)\approx \exp[-y^{par}_{t}(\tau)\tau],\qquad \tau=T-t.
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
2026-09-04. Physical-measure inference uses Yahoo `CL=F`; the valuation curve uses the
committed Barchart `CLX26` and `CLZ26` histories. On 2026-09-04 their Barchart `Latest`
values are 88.57 and 85.46, respectively. The fixing map uses the explicit last-trade-date
reference table, a date-specific Treasury discount factor, and a common sigma grid with
common random numbers.

The experiment reports Full Bayes, posterior-mean, marginal-sigma-mode, and MLE model prices
against the Barchart APO market marks. The sigma mode is explicitly a marginal posterior
mode, not a joint MAP estimate.

The completed full-precision pilot used 673 historical returns, four MCMC chains with 20,000
iterations per chain and 4,000 burn-in iterations, 100,000 pricing paths per sigma-grid
point, and 41 sigma-grid points. The posterior mean volatility was 0.415259 with posterior
standard deviation 0.011385 and a 95% interval of [0.393623, 0.438053]. The sigma R-hat was
1.000109 and the mu R-hat was 1.000889.

For the 29 option observations retained on that date, Full Bayes produced MAE 0.248330 and
RMSE 0.299866; the posterior-mean plug-in produced MAE 0.249114 and RMSE 0.300588. The sigma
posterior-mode plug-in and MLE plug-in had RMSE 0.317528 and 0.302679, respectively. These
numbers are treated as pilot evidence, not as a method ranking or final publication table.
The Full-Bayes/posterior-mean difference is small relative to the overall model-vs-market
pricing discrepancy in this cross-section.

All 29 retained option observations on 2026-09-04 have zero reported daily volume but
positive open interest. Their Barchart prices are therefore treated as end-of-day market
marks, not same-day transaction prices. A multi-date analysis must report positive-volume
and zero-volume observations separately rather than interpreting the pilot RMSE as a clean
transaction-price benchmark.

The October-2026 pilot currently uses a weekday fixing schedule because the selected month
has no full-day CME energy closure. General production-panel work must replace this pilot
fallback with an explicit exchange settlement calendar.

## Multi-date panel extension

`experiments/wti_apo_date_panel.py` operationalizes the next empirical step without
duplicating the single-date pricing implementation. It first constructs a date audit for one
APO expiry and keeps only dates for which both the option cross-section and the required two
Barchart CL curve contracts are available. The audit records raw and main-sample option
counts, the number of positive-volume observations, total reported volume, and curve
availability.

The panel runner invokes the canonical `experiments.wti_apo_empirical` driver once per
selected date and aggregates contract-level prices and posterior summaries. The aggregation
layer then creates three explicitly different empirical samples:

1. `all_dates`: every eligible date and every main-sample contract on those dates;
2. `positive_volume_dates`: every contract on dates where at least one main-sample contract
   has positive reported daily volume;
3. `positive_volume_contracts`: only contract-date observations whose own reported daily
   volume is strictly positive.

These objects answer different questions and are never allowed to overwrite one another.
The first is the broad market-mark panel, the second conditions on dates with some observed
trading activity, and the third is the narrowest transaction-activity robustness sample.
Error summaries for the third sample are recomputed after the contract-level filter rather
than reusing statistics from all contracts on the same dates.

For the currently committed October-2026 date audit, 12 pre-averaging dates are eligible.
Five dates contain at least one positive-volume main-sample option, but only six
contract-date observations across those dates have positive reported daily volume. This
thin transaction-activity sample is reported as a robustness layer rather than silently
substituted for the broader market-mark panel.

Derived panel aggregations live in separate subdirectories under
`results/wti_apo_empirical/panel_<YYYYMM>/`. They can be rebuilt from the canonical
single-date folders with `--aggregate-only`, so changing a sample definition does not
require rerunning MCMC or Monte Carlo pricing.

## Reproducibility metadata

The canonical driver writes manifest schema version 2. Repository inputs are stored as
repository-relative paths; external paths are reduced to `<external>/filename` so workstation
user directories are not exposed. The manifest records the Git commit, dirty-tree state,
Python/platform information, and NumPy/pandas/SciPy versions. Hostnames and user names are
intentionally omitted.

The first committed pilot predates this schema. Its workstation-specific expiry-reference
path was normalized after the run without changing any numerical output; the legacy manifest
records that metadata-only normalization explicitly.

## Data audit

`experiments/build_wti_apo_panel.py` recursively scans `data/csv`, decodes expiry from each
JAO symbol rather than trusting the folder name, de-duplicates repeated downloads, and
writes a folder/expiry mismatch report. The CL futures directory is ignored by APO discovery
because its filenames do not match the JAO option convention.

The committed Barchart CL source files are separately parsed by
`bayesian_asian_options.barchart_cl`. Run-level manifests record source file names, SHA-256
hashes, observation ranges, and the exact valuation-date CL curve used for pricing.


## Independent vanilla-option Q validation

Issue #36 is designed to break the endogeneity of estimating the risk-neutral volatility state
from the same APO family used as the target. The strict object is

\[
\mathcal I^{LO}_{t-1}
\longrightarrow \widehat\sigma^{LO}_{Q,t-1}
\longrightarrow \widehat C^{APO}_{t},
\]

where no APO mark dated \(t\) enters the vanilla-state estimate. The available Barchart
vanilla histories begin after the current October-2026 target window and therefore cannot
identify this experiment.

The replacement acquisition route is Databento `GLBX.MDP3`. The pilot uses the standard
WTI monthly-option parent `LO.OPT`, filters instrument definitions to underlyings `CLX6`
and `CLZ6` and strikes 85.0--94.5, and requests only the `statistics` schema over
2026-08-24 through 2026-09-10. The acquisition driver quotes every request before purchase and
enforces a default USD 5 hard cap. Raw vendor data remain local and gitignored.

For `GLBX.MDP3`, the observed fields used by this study are official settlement price
(`stat_type=3`), cleared volume (`6`), and open interest (`9`). Databento's current
statistics-availability table does not list settlement-implied volatility (`14`) for CME
Globex. The independent Q-state is therefore derived from official vanilla-option and futures
settlements using an American futures-option model because standard WTI monthly options are
American-style. Black-76 may be reported only as a near-ATM robustness approximation.

No empirical result from this route enters the manuscript until the acquisition manifest,
coverage audit, time ordering, and licensing treatment are versioned.


### Vanilla settlement inversion

The first independent-Q implementation derives a contract-level surface before any
aggregation to the APO horizon. For each final CME LO settlement on trading reference date
(t), the matching CL futures settlement is joined through the Databento underlying
instrument mapping. Let (F_t) be that futures settlement, (K) the option strike,
(	au) time to the Databento-reported option expiration, and (r_t(	au)) the dated
Treasury par-yield proxy already used elsewhere in the paper.

The standard LO contract is American style, so the primary inversion uses a
Cox--Ross--Rubinstein American futures-option tree. Under deterministic rates and the
maintained lognormal one-factor futures model,

[
u=e^{sigmasqrt{Delta t}},qquad d=u^{-1},qquad
p=rac{1-d}{u-d}.
]

At every node the option value is the maximum of immediate exercise and discounted
continuation. Brent root finding then solves the settlement-pricing equation for
(widehatsigma^{LO}_{Q,t,K}). Black--76 remains a European near-ATM robustness object,
not the production inversion.

The empirical surface is kept contract-level through this stage. Actual versus theoretical
CME settlement flags, volume, open interest, inversion failures, smile shape, and tree-step
convergence must be inspected before defining the scalar or maturity-interpolated Q state
used for strict (t-1) APO prediction.
