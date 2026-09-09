# WTI empirical application from Yahoo Finance

## Scope

The empirical application uses Yahoo Finance ticker `CL=F` as a reproducible
continuous/front-month **proxy** for NYMEX WTI crude-oil futures. Yahoo exposes a
long daily OHLCV history for this symbol, but the project does not assume that
Yahoo's undocumented historical roll construction is identical to a first-nearby
series reconstructed contract by contract.

This application therefore has two purposes:

1. estimate the physical-measure GBM parameters from real WTI futures-proxy data;
2. propagate posterior uncertainty in volatility into a hypothetical arithmetic
   Asian call on a lognormal futures-price process under Q.

It is **not** a validation against an observed market price of a CME Asian option.

## Why the default modeling window starts in 2021

GBM log returns require strictly positive prices. The May 2020 NYMEX WTI contract
settled at a negative price on 20 April 2020, so a GBM specification cannot be
applied blindly across that event. The downloader may retrieve the full history,
but the default inference window begins on `2021-01-01`. The code raises an error
instead of silently deleting any non-positive close inside the requested model
window.

## Conda setup

For an existing environment:

```powershell
conda env update -n asian-options -f environment.yml --prune
```

Or create it from scratch:

```powershell
conda env create -f environment.yml
```

## Download and historical inference

```powershell
conda run -n asian-options python -m experiments.wti_yahoo_application
```

The default query asks yfinance for the maximum available daily history of `CL=F`.
The local raw snapshot is written under:

```text
data/wti_yahoo/
```

These CSV files are intentionally ignored by Git. The experiment records their
SHA-256 digest and the exact first/last observations in the manifest.

Scientific outputs are written under:

```text
results/wti_yahoo/
    manifest.json
    posterior_summary.csv
    posterior_draws.npz        # local / ignored by Git
```

The inference model uses daily log returns with `dt = 1/252` and the same
Metropolis-Hastings implementation used by the synthetic experiment.

## Optional hypothetical Asian futures valuation

A futures price is modeled under Q as

```text
dF_t = sigma F_t dW_t^Q,
```

which has zero futures drift. The option value is discounted at the supplied
risk-free rate. The physical drift estimated from historical data is not inserted
into Q pricing.

The risk-free rate is deliberately required rather than silently hard-coded:

```powershell
conda run -n asian-options python -m experiments.wti_yahoo_application `
  --price-asian `
  --risk-free-rate 0.04 `
  --backend cupy
```

Replace `0.04` by the rate selected for the empirical valuation date. The default
contract grid uses:

```text
K/F0 = {0.8, 1.0, 1.2}
T    = {0.5, 1.0, 2.0} years
```

and produces:

```text
results/wti_yahoo/asian_pricing_summary.csv
results/wti_yahoo/asian_pricing_grid.csv
```

The summary reports full posterior integration, posterior-mean plug-in, MAP,
MLE, and a 95% posterior price interval. These are model-implied hypothetical
prices, not observed Asian-option quotes.

## Reproducibility

The manifest records:

- Yahoo ticker and query parameters;
- yfinance version;
- first and last downloaded observations;
- local raw snapshot path and SHA-256;
- exact inference window and number of log returns;
- MCMC seed, iterations, burn-in and acceptance rate;
- posterior and MLE summaries;
- all optional Asian-pricing assumptions.

The raw Yahoo snapshot should remain local unless redistribution rights have been
verified separately. Code, metadata, hashes, and derived scientific summaries may
be versioned independently.
