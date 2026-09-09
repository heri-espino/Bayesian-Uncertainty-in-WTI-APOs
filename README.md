# Bayesian parameter uncertainty for Asian options

This repository studies Bayesian inference for a geometric Brownian motion (GBM) and the propagation of parameter uncertainty into arithmetic-average Asian option valuation.

> **Research status:** publication-oriented refactor on `main`. The legacy notebook is preserved for traceability, while the current codebase contains a rewritten manuscript, a physical-measure inference module, a risk-neutral pricing engine, reproducible synthetic validation, and non-circular repeated-sampling experiments.

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

`reporte/reporte.tex` contains the corrected publication-oriented manuscript, while `reporte/draft_v1.tex` is the first full draft developed from the literature corpus in `literature/`.

The manuscript includes:

- bilingual title, abstract, keywords, and JEL codes;
- explicit state-of-the-art section;
- inference under \(\mathbb P\) separated from pricing under \(\mathbb Q\);
- Metropolis-Hastings in \((\mu,\log\sigma)\), including the change-of-variable Jacobian;
- risk-neutral Asian-option pricing with variance reduction;
- comparison of full Bayes, posterior-mean plug-in, MAP plug-in, and MLE;
- repeated-sampling bias, MAE, RMSE, and posterior-interval coverage;
- limitations, reproducibility statement, and transparent AI-use disclosure.

The current pilot uses 80 independent replications at \(n\in\{63,252,1260\}\). The main preliminary result is deliberately modest: full posterior integration and the posterior-mean plug-in are nearly indistinguishable in this Black-Scholes experiment, while physical-drift uncertainty does not enter the no-arbitrage price.

## Reproducible code

- `src/bayesian_gbm.py`: physical-measure GBM likelihood, priors, transformed M-H sampler, and MLE.
- `src/asian_pricing.py`: risk-neutral arithmetic Asian-call Monte Carlo, antithetic sampling, and geometric control variate.
- `src/synthetic_validation.py`: reusable deterministic, stochastic, and theoretical validation utilities.
- `experiments/synthetic_validation.py`: reproducible validation suite with explicit seed scheme and manifest.
- `experiments/publication_experiment.py`: outer repeated-sampling pricing experiment evaluated against \(C^{\mathbb Q}(\sigma_0)\).
- `results/publication_experiment_summary.csv`: pilot summary reported in the manuscript.
- `requirements-publication.txt`: dependencies for the publication experiment.
- `tests/`: regression tests that enforce the \(\mathbb P/\mathbb Q\) separation and numerical/theoretical behavior.

Install the publication dependencies from the repository root:

```bash
python -m pip install -r requirements-publication.txt
```

### Synthetic/stochastic/theoretical validation

Run a lightweight deterministic smoke validation:

```bash
python experiments/synthetic_validation.py --quick
```

Run the publication-oriented validation suite:

```bash
python experiments/synthetic_validation.py
```

The default output directory is `results/synthetic_validation/`. Each run writes:

- `parameter_recovery_raw.csv`: every synthetic GBM dataset and its MLE estimates;
- `parameter_recovery_summary.csv`: bias and RMSE of \(\mu\) and \(\sigma\) by sample size;
- `posterior_recovery_raw.csv`: posterior means, credible intervals, coverage, seeds, and acceptance rates;
- `posterior_recovery_summary.csv`: repeated-sampling posterior coverage and average estimates;
- `theoretical_checks.csv`: risk-neutral martingale, geometric closed-form, zero-volatility limit, variance reduction, monotonicity, and physical-drift-irrelevance checks;
- `manifest.json`: full configuration, root seed, seed-generation scheme, Python/NumPy versions, Git commit, and SHA-256 hash of every output CSV.

The default reproducibility seed is `20260909`. It can be overridden explicitly:

```bash
python experiments/synthetic_validation.py \
  --seed 20260909 \
  --output-dir results/synthetic_validation
```

Seeds for individual datasets and MCMC chains are generated with NumPy `SeedSequence` from integer identifiers rather than Python string hashes, so runs do not depend on process-level hash randomization. The raw output tables also store the actual data and chain seeds used in each replication.

The continuous-integration workflow runs the unit tests and a reduced `--quick` synthetic validation on every push to `main`. Full simulations remain explicit research runs rather than mandatory CI jobs.

### Pricing experiment

Run the current repeated-sampling pricing experiment with:

```bash
python experiments/publication_experiment.py
```

## Publication-oriented research question

> **How does Bayesian parameter uncertainty in the physical model propagate into risk-neutral prices of path-dependent options, and when does full posterior integration materially differ from plug-in pricing?**

The estimators are evaluated against a known risk-neutral benchmark across independent datasets. This avoids the previous circular comparison in which the posterior mean was evaluated under squared loss against the same posterior draws and therefore minimized the criterion by construction.

See [`research/REFRAMING.md`](research/REFRAMING.md) for the methodological roadmap and remaining extensions before submission.

## Repository map

- `notebook.ipynb`, `notebook.py`: legacy exploratory analysis.
- `reporte/reporte.tex`: corrected publication-oriented manuscript.
- `reporte/draft_v1.tex`: first full literature-informed draft.
- `literature/`: local literature corpus with extracted text, PDFs, and references.
- `src/`: inference, pricing, and validation modules.
- `experiments/`: reproducible synthetic validation and repeated-sampling pricing experiments.
- `results/`: legacy outputs, pilot pricing summary, and generated validation outputs.
- `tests/`: automated regression and theoretical tests.
- `research/REFRAMING.md`: publication roadmap and methodological notes.
