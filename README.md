# Bayesian parameter uncertainty for Asian options

This repository studies Bayesian inference for a geometric Brownian motion (GBM) and the propagation of parameter uncertainty into arithmetic-average Asian option valuation.

> **Research status:** publication-oriented refactor. The legacy notebook is preserved for traceability, while this branch contains a rewritten manuscript, a physical-measure inference module, risk-neutral pricing engines, a non-circular repeated-sampling experiment, and an empirical WTI Average Price Option (APO) workflow.

## Core distinction: physical inference vs. risk-neutral pricing

Historical returns are modeled under the physical measure \(\mathbb P\):

\[
dS_t = \mu S_t\,dt + \sigma S_t\,dW_t^{\mathbb P}.
\]

Bayesian inference targets \(p(\mu,\sigma\mid\mathcal D)\). In the Black-Scholes complete-market model, however, a traded contingent claim is priced under \(\mathbb Q\):

\[
dS_t = (r-q)S_t\,dt + \sigma S_t\,dW_t^{\mathbb Q}.
\]

The historical drift \(\mu\) therefore does **not** enter the pricing dynamics. Conditional on \(\sigma\), a discretely monitored arithmetic Asian call is

\[
C^{\mathbb Q}(\sigma)=e^{-rT}\,\mathbb E^{\mathbb Q}\!\left[(\bar S-K)^+\mid\sigma\right].
\]

Posterior parameter uncertainty is propagated through

\[
p(C\mid\mathcal D)=\int \delta_{C^{\mathbb Q}(\sigma)}\,p(\sigma\mid\mathcal D)\,d\sigma.
\]

The legacy notebook propagated posterior draws of both \(\mu\) and \(\sigma\) through discounted physical-measure simulations. Those outputs remain as a record of the initial experiment but are not interpreted as Black-Scholes no-arbitrage prices.

## Publication manuscript

`reporte/reporte.tex` has been rewritten around the corrected research question and is structured for an applied finance/economics journal submission:

- bilingual title, abstract, keywords, and JEL codes;
- explicit state-of-the-art section;
- inference under \(\mathbb P\) separated from pricing under \(\mathbb Q\);
- Metropolis-Hastings in \((\mu,\log\sigma)\), including the change-of-variable Jacobian;
- risk-neutral Asian-option pricing with variance reduction;
- comparison of full Bayes, posterior-mean plug-in, MAP plug-in, and MLE;
- repeated-sampling bias, MAE, RMSE, and posterior-interval coverage;
- limitations, reproducibility statement, and transparent AI-use disclosure.

The current synthetic pilot uses 80 independent replications at \(n\in\{63,252,1260\}\). The main result is deliberately modest: full posterior integration and the posterior-mean plug-in are nearly indistinguishable in this Black-Scholes experiment, while the physical drift uncertainty does not enter the no-arbitrage price.

## Empirical WTI Average Price Option application

The real-data extension uses CME WTI Average Price Options. CME Rulebook Chapter 341 defines the payoff using the arithmetic average of the daily settlement price of the **first-nearby CL futures contract during the calendar month**. The empirical pricer therefore cannot treat the contract as an Asian option on one fixed spot process or one fixed futures maturity.

The initial maturity panel deliberately spans the curve:

\[
\text{Sep-2026, Oct-2026, Nov-2026, Mar-2027, Sep-2027, Mar-2028, Sep-2028, Jun-2029}.
\]

All downloaded near-the-money calls and puts are retained in the raw panel. Strikes are not selected using only their moneyness on the final download date because the WTI level moved sharply during the sample. Instead, each option-date will be classified using effective moneyness relative to the expected terminal contract average.

The empirical workflow distinguishes:

- **raw panel:** every downloaded option-date and every available Barchart field;
- **main estimation panel:** objective quality filters such as positive open interest and sensitivity to minimum-tick observations;
- **representative contracts:** a ranking used only for figures, favoring long histories, informative prices, persistent open interest, near-ATM observations, and contracts that cross moneyness states.

The pricing baseline maps every remaining fixing date to the first-nearby CL contract and uses the observed futures term structure. Posterior uncertainty is then propagated through \(\sigma\), while 21-day realized volatility is used to classify low/medium/high volatility regimes. Geopolitical episodes may motivate the economic discussion, but regime labels are defined from market data rather than assigned causally by hand.

See [`research/EMPIRICAL_WTI_DESIGN.md`](research/EMPIRICAL_WTI_DESIGN.md) for the detailed design.

## Reproducible code

- `src/bayesian_gbm.py`: physical-measure GBM likelihood, priors, transformed M-H sampler, and MLE.
- `src/asian_pricing.py`: risk-neutral arithmetic Asian-call Monte Carlo, antithetic sampling, and geometric control variate for the controlled synthetic experiment.
- `src/barchart_apo.py`: parser for per-contract Barchart APO histories, tidy-panel construction, effective moneyness joins, objective filtering, and representative-contract ranking.
- `src/wti_first_nearby.py`: mapping from fixing dates to the first-nearby CL contract using explicit exchange last-trade dates.
- `src/wti_apo_pricing.py`: risk-neutral WTI APO Monte Carlo with realized fixings, remaining first-nearby forward fixings, term structure, and contract roll.
- `src/volatility_regimes.py`: 21-day realized-volatility construction and data-driven low/medium/high regime classification.
- `experiments/publication_experiment.py`: outer repeated-sampling experiment evaluated against the external benchmark \(C^{\mathbb Q}(\sigma_0)\).
- `experiments/build_wti_apo_panel.py`: converts locally stored Barchart CSV histories into a research panel and representative-contract ranking.
- `results/publication_experiment_summary.csv`: synthetic pilot summary reported in the manuscript.
- `requirements-publication.txt`: dependencies for the publication experiments.
- `tests/`: regression tests for the \(\mathbb P/\mathbb Q\) separation, Barchart parsing, first-nearby roll mapping, WTI APO pricing, and volatility regimes.

Run the synthetic publication experiment from the repository root:

```bash
python -m pip install -r requirements-publication.txt
python experiments/publication_experiment.py
```

Build the empirical option panel from a local directory of licensed Barchart downloads:

```bash
python experiments/build_wti_apo_panel.py \
  --input-dir data/raw/barchart_apo \
  --output data/processed/wti_apo_panel.csv \
  --ranking results/wti_apo_representative_contracts.csv
```

Raw Barchart downloads are intentionally excluded from version control until redistribution rights are confirmed.

## Publication-oriented research question

> **How does Bayesian parameter uncertainty in the physical model propagate into risk-neutral prices of path-dependent options, and when does full posterior integration materially differ from plug-in pricing?**

The synthetic estimators are evaluated against a known risk-neutral benchmark across independent datasets. This avoids the previous circular comparison in which the posterior mean was evaluated under squared loss against the same posterior draws and therefore minimized the criterion by construction. The WTI application complements that controlled experiment by testing whether the same mechanism is economically material in real average-price-option data across moneyness, maturity, and volatility regimes.

See [`research/REFRAMING.md`](research/REFRAMING.md) and [`research/EMPIRICAL_WTI_DESIGN.md`](research/EMPIRICAL_WTI_DESIGN.md) for the methodological roadmap.

## Repository map

- `notebook.ipynb`, `notebook.py`: legacy exploratory analysis.
- `reporte/reporte.tex`: rewritten publication-oriented manuscript.
- `src/`: corrected inference, synthetic pricing, WTI empirical-data, roll-mapping, and APO-pricing modules.
- `experiments/`: repeated-sampling publication experiment and empirical panel builder.
- `results/`: legacy outputs plus corrected synthetic pilot summary and locally generated empirical summaries.
- `tests/`: automated regression tests.
- `research/REFRAMING.md`: publication roadmap and methodological notes.
- `research/EMPIRICAL_WTI_DESIGN.md`: real-data WTI APO methodology.
