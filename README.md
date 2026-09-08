# Bayesian parameter uncertainty for Asian options

This repository studies Bayesian inference for a geometric Brownian motion (GBM) and the propagation of parameter uncertainty into arithmetic-average Asian option valuation.

> **Research status:** active methodological refactor. The original notebook/report are preserved as the historical baseline; the `publication-reframe-risk-neutral` branch introduces the pricing convention needed for a publishable version.

## Core distinction: physical inference vs. risk-neutral pricing

Historical returns are modeled under the physical measure \(\mathbb P\):

\[
dS_t = \mu S_t\,dt + \sigma S_t\,dW_t^{\mathbb P}.
\]

Bayesian inference may therefore target

\[
p(\mu,\sigma\mid \mathcal D).
\]

However, in the Black-Scholes complete-market model, the no-arbitrage price of a traded contingent claim is computed under the risk-neutral measure \(\mathbb Q\):

\[
dS_t = (r-q)S_t\,dt + \sigma S_t\,dW_t^{\mathbb Q}.
\]

Hence the historical drift \(\mu\) must **not** be inserted into the Monte Carlo pricing dynamics. Conditional on \(\sigma\), an arithmetic Asian call is

\[
C(\sigma)=e^{-rT}\,\mathbb E^{\mathbb Q}\!\left[(\bar S-K)^+\mid\sigma\right].
\]

Parameter uncertainty can still generate a posterior distribution of arbitrage-free model prices, but in the basic Black-Scholes setting it enters through the posterior of \(\sigma\):

\[
p(C\mid\mathcal D)
=\int \delta_{C(\sigma)}\,p(\sigma\mid\mathcal D)\,d\sigma.
\]

The legacy notebook propagates posterior draws of both \(\mu\) and \(\sigma\) directly through discounted physical-measure simulations. Those outputs are useful as a record of the initial experiment, but they should not be interpreted as Black-Scholes no-arbitrage option prices.

## New pricing module

`src/asian_pricing.py` implements:

- risk-neutral Monte Carlo for a discretely monitored arithmetic-average Asian call;
- antithetic sampling;
- a geometric-Asian control variate with a closed-form benchmark;
- mapping posterior draws of \(\sigma\) into a posterior distribution of risk-neutral option prices using common random numbers.

The physical drift `mu` is intentionally absent from the pricing API.

## Publication-oriented research question

A defensible research question is not whether Metropolis-Hastings can price an Asian option. Rather:

> **How does Bayesian parameter uncertainty in the physical model propagate into risk-neutral prices of path-dependent options, and when does full posterior integration materially differ from plug-in pricing?**

The main empirical design should compare estimators against a known risk-neutral benchmark across repeated datasets, rather than evaluating the posterior mean against the same posterior sample under squared loss (where the mean is optimal by construction).

See [`research/REFRAMING.md`](research/REFRAMING.md) for the proposed paper design.

## Repository map

- `notebook.ipynb`, `notebook.py`: original exploratory analysis.
- `reporte/`: original course report and LaTeX source.
- `results/`, `figures/`: outputs from the original experiment.
- `src/`: corrected risk-neutral pricing utilities.
- `tests/`: regression tests for the pricing convention and numerical implementation.
- `research/REFRAMING.md`: publication roadmap and methodological corrections.

## Reproducibility target

The publication version should ultimately contain a deterministic environment specification, multiple-chain MCMC diagnostics, simulation seeds, Monte Carlo error reporting, benchmark validation, and a single script/notebook capable of regenerating every table and figure.