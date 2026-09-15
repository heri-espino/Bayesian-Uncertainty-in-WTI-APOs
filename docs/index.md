# Bayesian Asian Options Research Library

This documentation is the operational reference for the code used in the Bayesian Asian-option research project. It is written for researchers, maintainers, and future coding agents who need to understand what modules exist, which functions are public, and how the pieces fit together without reading every source file.

The current Python import namespace is `src`. The repository is still a research codebase rather than a separately published PyPI package, so examples use imports such as `from src.bayesian_gbm import ...`.

## Design principles

The codebase enforces several distinctions that are central to the paper:

- Historical inference is performed under the physical measure $\mathbb P$.
- Derivative valuation is performed under the risk-neutral measure $\mathbb Q$.
- The physical drift $\mu$ is not propagated into Black--Scholes no-arbitrage prices.
- Synthetic validation and the empirical CME WTI Average Price Option application are separate experimental layers.
- Raw market-data provenance and data-quality diagnostics are kept distinct from economic sample-selection rules.
- Representative contracts are selected only for figures and case studies; they do not define the estimation sample.

## Documentation map

```{toctree}
:maxdepth: 2
:caption: User guide

quickstart
architecture
empirical_wti
agent_guide
api/index
```

## Build the documentation

From the repository root:

```bash
python -m pip install -r docs/requirements.txt
python -m sphinx -W --keep-going -b html docs docs/_build/html
```

Open `docs/_build/html/index.html` after a successful build.

The CI workflow builds the documentation with warnings treated as errors. Broken API references or invalid Sphinx markup should therefore fail a pull request before merge.
