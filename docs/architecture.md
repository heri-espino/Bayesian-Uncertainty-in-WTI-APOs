# Architecture

The repository is an installed research library plus reproducible experiment entry
points. Reusable scientific logic lives in
`bayesian_asian_options/src/bayesian_asian_options/`. `experiments/` orchestrates data,
parameter grids, checkpoints, and outputs without duplicating model implementations.

## Core layers

### Physical-measure inference

`bayesian_asian_options.bayesian_gbm`
: GBM returns under $\mathbb P$, posterior evaluation in `(mu, log_sigma)`, Random-Walk Metropolis, and GBM MLEs.

### Generic Asian-option pricing

`bayesian_asian_options.asian_pricing`
: Reference risk-neutral arithmetic-Asian pricing, geometric control variate, and posterior-volatility propagation.

`bayesian_asian_options.accelerated_pricing`
: Bounded-memory NumPy/CuPy pricing used for large grids.

`bayesian_asian_options.asian_futures_pricing`
: Lognormal futures-price Asian wrappers under $\mathbb Q$.

### Synthetic validation

`bayesian_asian_options.synthetic_validation`
: Reusable deterministic, theoretical, and stochastic checks. Publication-scale orchestration remains in `experiments/`.

### WTI market-data ingestion

`bayesian_asian_options.barchart_apo`
: Barchart WTI APO filename decoding, tidy histories, quality audits, effective moneyness, filters, and representative-contract ranking.

`bayesian_asian_options.wti_yahoo`
: Yahoo `CL=F` continuous/front-month proxy utilities. The proxy is not described as an exact reconstructed first-nearby series.

### CME WTI APO mechanics

`bayesian_asian_options.wti_first_nearby`
: First-nearby CL mapping from explicit exchange last-trade dates.

`bayesian_asian_options.wti_apo_pricing`
: CME-style calls/puts from realized fixings plus the futures term structure for remaining fixings.

`bayesian_asian_options.volatility_regimes`
: Rolling realized volatility and data-driven low/medium/high regimes.

## Dependency direction

```text
experiments/  --->  bayesian_asian_options
                         |
                         +--> NumPy / pandas / SciPy
```

The package must never import `experiments.*`. A function reused by more than one
experiment belongs in the package and must be added to the API documentation and tests.

## Scientific invariants

1. `mu` belongs to inference under $\mathbb P$ and does not enter baseline pricing under $\mathbb Q$.
2. Posterior uncertainty is propagated only through parameters that matter for the pricing model, principally `sigma` in the baseline.
3. The empirical WTI APO payoff uses calendar-month first-nearby CL settlements, not one fixed futures contract.
4. Historical market settlements are external benchmarks; posterior-generated prices cannot define truth.
5. Data completeness, liquidity, figure ranking, and estimation-sample inclusion are separate concepts.
6. Long runs remain reproducible/restartable through explicit seeds, manifests, hashes, and checkpoints.

See `AGENTS.md` for the mandatory maintenance policy.
