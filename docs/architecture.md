# Architecture

The repository is an installed research library plus reproducible experiment entry points.
Reusable scientific logic lives in `bayesian_asian_options/src/bayesian_asian_options/`.
`experiments/` orchestrates data, parameter grids, checkpoints, and outputs without
duplicating model implementations.

## Core layers

### Physical-measure inference

`bayesian_asian_options.bayesian_gbm`
: GBM returns under $\mathbb P$, posterior evaluation in `(mu, log_sigma)`, Random-Walk Metropolis, and GBM MLEs.

`bayesian_asian_options.wti_yahoo`
: Yahoo `CL=F` continuous/front-month proxy utilities used by the current empirical pilot for historical-return inference. This is explicitly a proxy, not a contract-reconstructed first-nearby series.

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

`bayesian_asian_options.barchart_cl`
: Barchart individual WTI futures `Daily Prices` ingestion, source hashes/manifests, exact-date futures-curve extraction, and explicit CL expiry-table loading.

`bayesian_asian_options.wti_yahoo_futures`
: Optional individual-Yahoo-contract utilities retained for validation and auxiliary work. They are not required by the canonical pilot because Yahoo can remove old delisted symbols.

### CME WTI APO mechanics

`bayesian_asian_options.wti_first_nearby`
: First-nearby CL mapping from explicit last-trade dates, exact-date reconstruction of already realized first-nearby fixings, and mapping of remaining fixing dates to the contemporaneous futures curve.

`bayesian_asian_options.wti_apo_pricing`
: CME-style calls/puts from realized fixings plus the futures term structure for remaining fixings.

`bayesian_asian_options.volatility_regimes`
: Rolling realized volatility and data-driven low/medium/high regimes.

### Discounting

`bayesian_asian_options.rates`
: U.S. Treasury daily par-yield ingestion and dated discount-factor construction under the explicitly documented pilot approximation.

## Current empirical data flow

```text
Yahoo CL=F history ---------------------------> P-measure sigma inference

Barchart APO histories ----------------------> observed option benchmark
Barchart individual CL histories + expiries -> realized first-nearby fixings
                                           \-> remaining fixing curve at valuation date
U.S. Treasury dated par curve ---------------> discount factor
                                                   |
                                                   v
                                      risk-neutral APO pricing
                                                   |
                                                   v
                                      model-vs-market comparison
```

The source objects are deliberately separate. A continuous ticker is not substituted for
the contractual futures term structure entering the APO payoff.

## Empirical orchestration

`experiments/wti_apo_empirical.py` is the **single canonical one-date driver**. It owns the
source-role separation, historical inference, realized/remaining fixing-state reconstruction,
dated discounting, pricing grid, market comparison, and reproducibility manifest. Before the
averaging month the realized set is empty; inside the averaging month, exact first-nearby
contract/date observations through the end-of-day valuation timestamp are fixed and only the
remaining dates are stochastic. Do not fork this logic into source-specific or `hybrid`
experiment drivers.

`experiments/wti_apo_date_panel.py` is orchestration only. It audits candidate dates,
requires both the realized fixing history and the date-specific CL curve needed by remaining
fixings, invokes the canonical one-date driver once per eligible date, and aggregates the
resulting contract/error/posterior tables. It does not reimplement pricing or inference logic.

Run manifests use repository-relative paths for repository inputs and redact external
workstation directory prefixes. They capture the Git commit/dirty-tree state and runtime
versions needed for reproduction while deliberately omitting hostnames and user names.

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
3. The empirical WTI APO payoff uses calendar-month first-nearby CL levels, not one fixed futures contract or Yahoo `CL=F`.
4. Realized first-nearby fixings are exact mapped contract/date observations; missing realized observations are not forward-filled.
5. Historical market marks are external benchmarks; posterior-generated prices cannot define truth.
6. Data completeness, liquidity, figure ranking, and estimation-sample inclusion are separate concepts.
7. Long runs remain reproducible/restartable through explicit seeds, manifests, hashes, and checkpoints.
8. Source fields retain their provenance: Barchart `Latest` is a settlement proxy unless separately validated as an official CME settlement.

See `AGENTS.md` for the mandatory maintenance policy and {doc}`development` for the branch/PR lifecycle.
