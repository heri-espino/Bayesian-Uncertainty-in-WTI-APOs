# Bayesian parameter uncertainty for Asian options

This repository studies Bayesian inference for a geometric Brownian motion (GBM) and the propagation of parameter uncertainty into arithmetic-average Asian option valuation.

> **Research status:** publication-oriented refactor. The legacy notebook is preserved for traceability, while this branch contains a rewritten manuscript, a physical-measure inference module, a risk-neutral pricing engine, and a non-circular repeated-sampling experiment.

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

The current pilot uses 80 independent replications at \(n\in\{63,252,1260\}\). The main result is deliberately modest: full posterior integration and the posterior-mean plug-in are nearly indistinguishable in this Black-Scholes experiment, while the physical drift uncertainty does not enter the no-arbitrage price.

## Reproducible code

- `src/bayesian_gbm.py`: physical-measure GBM likelihood, priors, transformed M-H sampler, and MLE.
- `src/asian_pricing.py`: risk-neutral arithmetic Asian-call Monte Carlo, antithetic sampling, and geometric control variate.
- `experiments/publication_experiment.py`: outer repeated-sampling experiment evaluated against the external benchmark \(C^{\mathbb Q}(\sigma_0)\).
- `results/publication_experiment_summary.csv`: pilot summary reported in the manuscript.
- `requirements-publication.txt`: dependencies for the publication experiment.
- `tests/`: regression tests that enforce the \(\mathbb P/\mathbb Q\) separation and basic numerical behavior.

Run the publication experiment from the repository root:

```bash
python -m pip install -r requirements-publication.txt
python experiments/publication_experiment.py
```

## Publication-oriented research question

> **How does Bayesian parameter uncertainty in the physical model propagate into risk-neutral prices of path-dependent options, and when does full posterior integration materially differ from plug-in pricing?**

The estimators are evaluated against a known risk-neutral benchmark across independent datasets. This avoids the previous circular comparison in which the posterior mean was evaluated under squared loss against the same posterior draws and therefore minimized the criterion by construction.

See [`research/REFRAMING.md`](research/REFRAMING.md) for the methodological roadmap and remaining extensions before submission.

## Repository map

- `notebook.ipynb`, `notebook.py`: legacy exploratory analysis.
- `reporte/reporte.tex`: rewritten publication-oriented manuscript.
- `src/`: corrected inference and pricing modules.
- `experiments/`: repeated-sampling publication experiment.
- `results/`: legacy outputs plus corrected pilot summary.
- `tests/`: automated regression tests.
- `research/REFRAMING.md`: publication roadmap and methodological notes.
