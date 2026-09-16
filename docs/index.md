# Bayesian Asian Options Research Library

This documentation is the operational reference for the reusable Python package and the
research workflows built on top of it. It is intended for researchers, maintainers, and
future coding agents who need to discover existing functionality without reading the
entire source tree.

The canonical Python namespace is `bayesian_asian_options`. The repository uses a
standard editable-install source layout:

```text
bayesian_asian_options/src/bayesian_asian_options/
```

Install from the repository root before running experiments or building documentation:

```bash
python -m pip install -e ".[dev,docs,market]"
```

## Design principles

- Historical inference is performed under the physical measure $\mathbb P$.
- Derivative valuation is performed under the risk-neutral measure $\mathbb Q$.
- The physical drift $\mu$ is not propagated into Black--Scholes no-arbitrage prices.
- Synthetic validation and the empirical CME WTI Average Price Option application are separate experimental layers.
- Raw market-data provenance and data-quality diagnostics remain distinct from economic sample-selection rules.
- Representative contracts are selected only for figures/case studies; they do not define the estimation sample.
- `main` is the only long-lived development branch; merged or superseded feature branches should be deleted.

## Documentation map

```{toctree}
:maxdepth: 2
:caption: User guide

quickstart
architecture
repository_layout
development
empirical_wti
agent_guide
api/index
```

## Build the documentation

```bash
python -m sphinx -W --keep-going -b html docs docs/_build/html
```

The package must already be installed editable. CI builds the documentation with warnings
as errors, so broken API references fail before merge.
