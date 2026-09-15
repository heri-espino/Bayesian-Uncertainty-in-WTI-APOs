# Architecture

The repository is organized as a research library plus reproducible experiment entry points. Code under `src/` should contain reusable scientific logic. Code under `experiments/` should orchestrate datasets, parameter grids, checkpoints, and outputs without duplicating model implementations.

## Core layers

### Physical-measure inference

`src.bayesian_gbm`
: Simulates GBM log returns under $\mathbb P$, evaluates the posterior in `(mu, log_sigma)`, runs Random-Walk Metropolis, and computes GBM MLEs.

The important interface boundary is that this layer estimates historical parameters but does not price derivatives.

### Generic Asian-option pricing

`src.asian_pricing`
: Reference risk-neutral pricer for discretely monitored arithmetic Asian calls, including a closed-form geometric Asian control variate and posterior-volatility propagation.

`src.accelerated_pricing`
: Bounded-memory NumPy/CuPy implementations used for large pricing grids and workstation-scale experiments.

`src.asian_futures_pricing`
: Convenience wrappers for lognormal futures dynamics under $\mathbb Q$, implemented by setting the spot-style drift to zero while retaining discounting.

### Synthetic validation

`src.synthetic_validation`
: Reusable theoretical, deterministic, and stochastic validation utilities.

Experiment entry points in `experiments/` build on these functions to generate publication tables and restartable large-scale simulations.

### WTI market-data ingestion

`src.barchart_apo`
: Parses individual Barchart WTI Average Price Option histories, decodes contract metadata, standardizes the daily panel, audits folder/expiry mismatches, adds effective moneyness, and separates data-quality diagnostics from estimation filters.

`src.wti_yahoo`
: Handles the Yahoo `CL=F` continuous/front-month proxy used for historical-volatility inference and auxiliary empirical work. It must not be described as an exact reconstructed first-nearby series.

### CME WTI APO contract mechanics

`src.wti_first_nearby`
: Maps each APO fixing date to the first CL futures contract that is still trading, using explicit exchange last-trade dates supplied as data.

`src.wti_apo_pricing`
: Prices CME-style WTI arithmetic-average calls and puts from realized fixings plus the futures term structure for remaining first-nearby fixings.

`src.volatility_regimes`
: Constructs rolling realized-volatility measures and data-driven low/medium/high volatility regimes.

## Dependency direction

Keep dependencies moving from experiment orchestration toward reusable library code:

```text
experiments/  --->  src/
                    |
                    +--> NumPy / pandas / SciPy
```

Avoid importing an `experiments.*` module from `src.*`. A function that becomes useful to more than one experiment should be moved into `src/` and documented in the API reference.

## Scientific invariants

Changes should preserve these invariants unless the research design is explicitly revised and documented:

1. `mu` belongs to inference under $\mathbb P$ and does not enter the baseline Black--Scholes pricing dynamics under $\mathbb Q$.
2. Posterior uncertainty is propagated through parameters that matter for pricing, principally `sigma` in the current baseline.
3. The empirical WTI APO payoff is based on calendar-month averages of first-nearby CL settlements, not on one fixed futures contract.
4. Historical market settlements are external benchmarks; posterior-generated prices must not be reused as the definition of truth.
5. Raw-data completeness, liquidity, representative-figure ranking, and estimation-sample inclusion are different concepts and must remain separate in code and analysis.
6. Long-running experiments must remain reproducible and restartable through explicit seeds, manifests, hashes, and checkpoints.
