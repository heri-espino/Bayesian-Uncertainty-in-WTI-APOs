# Quickstart

## Environment

The scientific environment remains Conda-first:

```bash
conda env create -f environment.yml
conda activate asian-options
python -m pip install -e ".[dev,docs,market]"
```

Documentation dependencies are intentionally separate from the scientific runtime:

```bash
python -m pip install -r docs/requirements.txt
```

## 1. Simulate historical GBM returns and infer volatility

```python
import numpy as np

from bayesian_asian_options.bayesian_gbm import (
    gbm_log_returns,
    gbm_mle,
    random_walk_metropolis_gbm,
)

returns = gbm_log_returns(
    mu=0.08,
    sigma=0.25,
    dt=1 / 252,
    n_obs=252,
    seed=123,
)

mu_mle, sigma_mle = gbm_mle(returns, dt=1 / 252)
posterior = random_walk_metropolis_gbm(
    returns,
    dt=1 / 252,
    n_iter=20_000,
    burn_in=4_000,
    theta_init=(mu_mle, np.log(sigma_mle)),
    seed=123,
)

print(posterior.acceptance_rate)
print(posterior.sigma.mean())
```

`posterior.mu` and `posterior.sigma` are posterior draws under the physical-measure GBM model. Only the volatility draws are propagated into the Black--Scholes pricing layer.

## 2. Price an arithmetic Asian call under $\mathbb Q$

```python
from bayesian_asian_options.asian_pricing import asian_arithmetic_call_mc

estimate = asian_arithmetic_call_mc(
    S0=100.0,
    K=100.0,
    r=0.03,
    sigma=0.25,
    T=1.0,
    q=0.0,
    n_steps=252,
    n_paths=100_000,
    seed=123,
)

print(estimate.price)
print(estimate.standard_error)
```

The pricing function deliberately has no `mu` argument. Its simulated drift is the risk-neutral drift `r - q`.

## 3. Propagate posterior volatility into Asian prices

```python
from bayesian_asian_options.asian_pricing import posterior_price_samples

price_draws = posterior_price_samples(
    posterior.sigma,
    S0=100.0,
    K=100.0,
    r=0.03,
    T=1.0,
    q=0.0,
    n_steps=252,
    n_paths=20_000,
    seed=12345,
)

full_bayes_price = price_draws.mean()
```

The function resets the same pseudo-random seed for each volatility draw. This common-random-numbers design reduces Monte Carlo noise when comparing prices across posterior values of $\sigma$.

## 4. Build the Barchart WTI APO panel

The committed market-data histories are stored as one CSV per option contract. Build the standardized panel with:

```bash
python -m experiments.build_wti_apo_panel \
  --input-dir data/csv \
  --output-dir results/wti_apo_panel
```

The ingestion utilities are also usable directly:

```python
from bayesian_asian_options.barchart_apo import (
    discover_barchart_histories,
    build_apo_panel,
    summarize_contracts,
)

paths = discover_barchart_histories("data/csv")
panel = build_apo_panel(paths)
quality = summarize_contracts(panel)
```

Do not use `richest_option_series.csv` as a liquidity filter. Its score describes data completeness and time-span coverage, not economic importance.

## 5. Price a CME-style WTI Average Price Option

```python
import numpy as np

from bayesian_asian_options.wti_apo_pricing import wti_average_price_option_mc

estimate = wti_average_price_option_mc(
    realized_fixings=np.array([91.2, 92.0, 91.7]),
    forward_fixings=np.array([93.0, 93.4, 94.1]),
    fixing_times=np.array([1 / 252, 2 / 252, 3 / 252]),
    strike=92.5,
    sigma=0.35,
    rate=0.04,
    time_to_expiry=3 / 252,
    option_type="call",
    n_paths=100_000,
    seed=123,
)

print(estimate.price)
print(estimate.expected_average)
```

For the empirical application, `forward_fixings` should come from the observed CL futures curve after mapping each remaining fixing date to the correct first-nearby contract. See {doc}`empirical_wti`.
