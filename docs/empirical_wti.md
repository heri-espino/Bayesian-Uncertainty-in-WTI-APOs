# Empirical WTI APO workflow

This page describes the intended research pipeline for the CME WTI Average Price Option application. It is an implementation map, not a substitute for the methodological discussion in `research/EMPIRICAL_WTI_DESIGN.md`.

## 1. Ingest all downloaded option histories

Use all downloaded near-the-money contracts in the raw panel. Do not select strikes according to the final observed WTI level.

```python
from bayesian_asian_options.barchart_apo import discover_barchart_histories, build_apo_panel

paths = discover_barchart_histories("data/csv")
raw_panel = build_apo_panel(paths, deduplicate_contracts=True)
```

The filename parser is the authoritative source for expiry, strike, and call/put metadata. Folder names are audited rather than blindly trusted because a contract can be stored in the wrong directory.

## 2. Keep data richness separate from liquidity

`data/csv/richest_option_series.csv` was created from a score based on session count, calendar span, and numerical-field completeness. It is useful for auditing historical coverage but must not define the main empirical sample.

Use `bayesian_asian_options.barchart_apo.summarize_contracts` for diagnostics and `bayesian_asian_options.barchart_apo.apply_main_sample_filters` for an explicit baseline sample rule. Sensitivity analysis can then vary open-interest thresholds or minimum-tick exclusions without changing the raw panel.

## 3. Reconstruct the first-nearby fixing schedule

A WTI APO is not an Asian option on one fixed CL maturity. For every remaining fixing date, map to the earliest CL contract that has not passed its exchange last-trade date:

```python
from bayesian_asian_options.wti_first_nearby import build_forward_fixing_curve

forward_curve = build_forward_fixing_curve(
    fixing_dates=remaining_fixing_dates,
    contract_expiries=cl_expiry_table,
    futures_curve=current_cl_curve,
)
```

The `contract_expiries` table must contain explicit exchange last-trade dates. Do not substitute an approximate roll convention inside the scientific code.

## 4. Construct the expected final average

At valuation date $t$, define

$$
\widehat A_{t,T}^{Q}
=
\frac{
\sum_{j\in R_t} F_j^{\mathrm{realized}}
+
\sum_{j\in U_t} F_j(t)
}{N},
$$

where `R_t` denotes already fixed business days and `U_t` remaining fixing dates. Under the current baseline, each current futures quote is the $\mathbb Q$ expectation of its own future settlement.

Use `bayesian_asian_options.wti_apo_pricing.expected_average_level` for the corresponding numerical quantity.

## 5. Define moneyness observation by observation

Do not assign a permanent ATM/ITM/OTM label to a strike. The same contract can move through different states during its life.

The empirical panel uses

$$
m_{t,K,T}=\log\left(\frac{K}{\widehat A_{t,T}^{Q}}\right).
$$

`bayesian_asian_options.barchart_apo.add_effective_moneyness` currently classifies absolute log-moneyness into ATM (`<= 0.05`), moderate (`0.05` to `0.15`), and deep (`> 0.15`) buckets. These thresholds are analysis conventions and should be reported when used.

## 6. Estimate historical volatility uncertainty

Historical WTI returns generate a posterior for `sigma` under the physical measure. The current baseline uses the GBM inference routines in `bayesian_asian_options.bayesian_gbm`. The posterior should be estimated with information available at the valuation date when conducting a genuinely out-of-sample exercise.

The physical drift `mu` is retained as an inferred quantity but is not passed into the risk-neutral APO pricer.

## 7. Propagate posterior volatility through the CME-style pricer

```python
from bayesian_asian_options.wti_apo_pricing import posterior_wti_apo_prices

posterior_prices = posterior_wti_apo_prices(
    sigma_samples,
    realized_fixings=realized_fixings,
    forward_fixings=forward_fixings,
    fixing_times=fixing_times,
    strike=strike,
    rate=rate,
    time_to_expiry=time_to_expiry,
    option_type=option_type,
)
```

The principal estimators are then obtained from the same conditional pricing function:

- Full Bayes: posterior mean of conditional prices.
- Posterior-mean plug-in: price evaluated at the posterior mean of `sigma`.
- MAP plug-in: price evaluated at the posterior mode of `sigma`.
- MLE plug-in: price evaluated at the historical maximum-likelihood volatility.

Compare these quantities against the observed market settlement, not against posterior-generated price draws.

## 8. Volatility regimes

Use realized volatility to define low, medium, and high-volatility regimes from the data rather than manually labeling geopolitical events. Geopolitical developments can be discussed as market context after the statistical regime definition is fixed.

The relevant utilities live in `bayesian_asian_options.volatility_regimes`.

## 9. Representative contracts

Use `bayesian_asian_options.barchart_apo.rank_representative_contracts` only to identify informative examples for plots or case studies. A representative score can reward long histories, non-minimum-tick observations, open interest, ATM days, and moneyness crossings without changing the main estimation sample.
