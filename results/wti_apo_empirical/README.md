# WTI APO empirical results

This directory contains versioned outputs from the real-market WTI Average Price Option workflow. Each run lives under `<valuation-date>_<expiry-month>` and must be interpreted together with its `manifest.json` and source audits.

## Completed pilot

The first completed full-precision run is:

```text
2026-09-04_202610/
```

It prices the October-2026 APO cross-section observed on 2026-09-04 using:

- Yahoo `CL=F` as the labelled physical-measure historical-return proxy;
- Barchart `CLX26 = 88.57` and `CLZ26 = 85.46` as the valuation-date contract-specific curve;
- the explicit CL last-trade-date table under `data/csv/CL/contract_expiries.csv`;
- a dated U.S. Treasury discount-factor proxy;
- four MCMC chains, 20,000 iterations per chain, 4,000 burn-in iterations, 100,000 Monte Carlo paths per sigma-grid point, and 41 sigma-grid points.

The run contains 673 usable historical returns and 29 option observations after the configured filters. Posterior volatility summary:

```text
sigma MLE             0.414888
posterior mean sigma  0.415259
posterior SD sigma    0.011385
95% interval          [0.393623, 0.438053]
sigma R-hat           1.000109
mu R-hat              1.000889
```

Model-vs-market error summary:

| Method | MAE | RMSE |
| --- | ---: | ---: |
| Full Bayes | 0.248330 | 0.299866 |
| Posterior mean plug-in | 0.249114 | 0.300588 |
| Sigma posterior-mode plug-in | 0.267895 | 0.317528 |
| MLE plug-in | 0.251462 | 0.302679 |

These are **pilot results**, not a method ranking or a final publication table. In this cross-section the Full-Bayes and posterior-mean prices are extremely close relative to the overall model-vs-market discrepancy. The observed option records on this valuation date have zero reported daily volume but positive open interest, so the Barchart values are treated as end-of-day market marks rather than same-day transaction prices.

## Files in each run

- `manifest.json`: source roles, seeds, settings, curve values, discounting, and runtime provenance;
- `posterior_summary.csv`: MLE/posterior volatility summary and R-hat diagnostics;
- `mcmc_diagnostics.csv`: chain-level acceptance rates and parameter means;
- `posterior_draws.npz`: pooled posterior sigma draws;
- `valuation_cl_curve.csv`: contract-specific valuation-date futures curve;
- `cl_expiry_table.csv`: last-trade dates used by the fixing map;
- `apo_fixing_state.csv`: fixing-date-to-CL-contract mapping and levels;
- `pricing_grid.csv`: conditional model prices over the sigma grid;
- `contract_pricing.csv`: market marks and Full-Bayes/plugin prices by option contract;
- `error_summary.csv`: aggregate model-vs-market error statistics;
- `barchart_cl_manifest.csv`: source-file hashes and observation ranges;
- `inference_proxy_series.csv` and `inference_return_audit.csv`: the historical inference proxy and return audit.

Future runs should be produced with the canonical driver `python -m experiments.wti_apo_empirical`. Manifest schema version 2 records repository-relative/redacted paths, the Git commit and dirty-tree flag, and package/runtime versions without storing workstation user names or hostnames.
