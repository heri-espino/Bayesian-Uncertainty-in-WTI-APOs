# WTI APO empirical results

This directory contains versioned outputs from the real-market WTI Average Price Option workflow. Each run lives under `<valuation-date>_<expiry-month>` and must be interpreted together with its `manifest.json` and source audits.

## Current committed October-2026 panel

The active single-date folders under `2026-08-25_202610/` through `2026-09-10_202610/` were regenerated at the production computational budget. Their manifests record:

- four MCMC chains;
- 20,000 iterations per chain;
- 4,000 burn-in iterations per chain;
- 100,000 Monte Carlo paths per sigma-grid point;
- 41 sigma-grid points.

These are the active production-budget baseline results for the current one-factor, constant-volatility specification. They replace the earlier lower-cost multi-date outputs in the same canonical single-date folders.

All current October runs use:

- Yahoo `CL=F` as the labelled physical-measure historical-return proxy;
- committed Barchart `CLX26` and `CLZ26` histories as the valuation-date contract-specific curve;
- the explicit CL last-trade-date table under `data/csv/CL/contract_expiries.csv`;
- a dated U.S. Treasury discount-factor proxy;
- common random numbers and antithetic pricing within each run.

The Barchart option values are treated as end-of-day market marks. Zero reported daily volume is not interpreted as evidence of a same-day transaction.

## Multi-date October-2026 panel

The date audit identifies 12 eligible pre-averaging valuation dates with both APO observations and the two required Barchart CL curve contracts. Five dates have at least one main-sample contract with positive reported daily volume: 2026-08-27, 2026-08-28, 2026-08-31, 2026-09-01, and 2026-09-02. Across those dates only six contract-date observations have positive reported daily volume, so date-level and contract-level liquidity filters must not be conflated.

Panel aggregations are derived from the canonical single-date folders and are namespaced:

```text
panel_202610/
├── panel_date_audit.csv
├── all_dates/
├── positive_volume_dates/
└── positive_volume_contracts/
```

Each sample directory contains:

- `panel_contract_pricing.csv`;
- `panel_error_summary.csv`, recomputed by valuation date from the contracts actually in that sample;
- `panel_overall_error_summary.csv`, pooled across contract-date observations in that sample;
- `panel_posterior_summary.csv` for the dates represented in the sample;
- `sample_manifest.json` with the exact sample definition and counts.

The three sample definitions are:

- `all_dates`: all eligible dates and all main-sample contracts;
- `positive_volume_dates`: all contracts on dates where at least one contract has positive reported volume;
- `positive_volume_contracts`: only contract-date observations whose own reported volume is strictly positive.

The current pooled production-budget results are:

| Sample | N | Full Bayes RMSE | Posterior-mean RMSE | Sigma-mode RMSE | MLE RMSE |
| --- | ---: | ---: | ---: | ---: | ---: |
| All eligible dates | 310 | 0.517741 | 0.518337 | 0.520002 | 0.519702 |
| Positive-volume dates | 136 | 0.430270 | 0.431045 | 0.441301 | 0.432399 |
| Positive-volume contracts | 6 | 0.186425 | 0.186902 | 0.202551 | 0.188180 |

The main qualitative result survives the increase in numerical precision: Full Bayes and posterior-mean plug-in prices remain very close relative to the larger model-to-market discrepancy. In the six positive-volume contract-date observations, mean absolute `|Delta_FB-PM|` is approximately 0.000591 and the maximum is approximately 0.001005, compared with Full-Bayes MAE 0.154266. The strict sample is too small for a strong general ranking of pricing rules.

The lower-cost multi-date pass previously produced Full-Bayes RMSE 0.508325 in the all-dates sample and 0.178282 in the strict positive-volume sample. The production rerun changes the absolute error levels but leaves the central Full-Bayes versus posterior-mean conclusion unchanged.

The older flat aggregate files directly under `panel_202610/` were removed because a second panel run could overwrite the first sample silently. Existing single-date run folders remain the provenance authority and contain all numerical results. Rebuild namespaced aggregates without rerunning MCMC or pricing with:

```bash
python -m experiments.wti_apo_date_panel \
    --apo-expiry 2026-10 \
    --aggregate-only
```

## Files in each single-date run

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
