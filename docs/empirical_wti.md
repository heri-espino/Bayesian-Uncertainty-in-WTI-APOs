# Empirical WTI APO workflow

This page describes the implemented research pipeline for the CME WTI Average Price Option application. It is an implementation map, not a substitute for `research/EMPIRICAL_WTI_DESIGN.md`.

## Data-source contract

The empirical application deliberately uses different sources for different objects:

- **WTI APO market marks:** committed Barchart contract histories already present under `data/csv`;
- **individual CL futures histories and historical curve points:** Yahoo Finance contract symbols such as `CLV26.NYM`, `CLX26.NYM`, and `CLZ26.NYM`, downloaded through `yfinance`;
- **CL contract settlement/expiration metadata:** Yahoo quote metadata in the automated pilot, with exchange/Barchart cross-validation required for publication tables;
- **USD discounting:** U.S. Treasury Daily Treasury Par Yield Curve Rates;
- **validation:** small external reference tables can be supplied locally and are never required to be committed.

Yahoo `Close` is treated as a **daily settlement proxy**, not silently renamed an official CME settlement.

## 1. Ingest all downloaded option histories

Use all downloaded contracts in the raw panel. Do not select strikes according to the final observed WTI level.

```python
from bayesian_asian_options.barchart_apo import discover_barchart_histories, build_apo_panel

paths = discover_barchart_histories("data/csv")
raw_panel = build_apo_panel(paths, deduplicate_contracts=True)
```

The filename parser is the authoritative source for expiry, strike, and call/put metadata. Folder names are audited rather than blindly trusted.

## 2. Keep data richness separate from liquidity

`data/csv/richest_option_series.csv` is a historical-coverage diagnostic, not a liquidity ranking. Use `summarize_contracts` for diagnostics and `apply_main_sample_filters` for transparent sample rules.

## 3. Download individual Yahoo CL contracts

Do not use `CL=F` as the contractual first-nearby series. Build the monthly strip explicitly:

```python
from bayesian_asian_options.wti_yahoo_futures import (
    cl_contract_strip,
    download_or_load_yahoo_cl_strip,
)

contracts = cl_contract_strip("2024-01-01", "2026-10-31", lead_months=2)
panel, metadata = download_or_load_yahoo_cl_strip(
    contracts,
    directory="data/wti_yahoo_contracts",
)
```

The cache is local and gitignored. Metadata contains hashes, source labels, and the Yahoo expiration/settlement date when available.

## 4. Reconstruct first-nearby history without fake roll returns

A futures roll is not a daily WTI innovation. The reconstructed physical-measure series therefore sets the log return to missing whenever the active contract changes:

```python
from bayesian_asian_options.wti_yahoo_futures import (
    expiry_table_from_yahoo_metadata,
    reconstruct_first_nearby_history,
)

expiries = expiry_table_from_yahoo_metadata(metadata)
first_nearby = reconstruct_first_nearby_history(
    panel,
    expiries,
    start="2024-01-01",
    end="2026-09-04",
)
returns = first_nearby.loc[
    first_nearby["usable_inference_return"], "log_return"
]
```

This prevents contango/backwardation at the roll from being interpreted as one-day diffusion noise.

## 5. Reconstruct the remaining APO fixing curve

For every remaining fixing date, map to the earliest CL contract that has not passed its explicit settlement/expiration date:

```python
from bayesian_asian_options.wti_first_nearby import build_forward_fixing_curve
from bayesian_asian_options.wti_yahoo_futures import futures_curve_on_date

curve_t = futures_curve_on_date(panel, "2026-09-04")
forward_fixings = build_forward_fixing_curve(
    fixing_dates=remaining_fixing_dates,
    contract_expiries=expiries,
    futures_curve=curve_t,
)
```

The scientific code does not infer a hidden roll rule from a continuous ticker.

## 6. Construct expected final average and moneyness

At valuation date $t$,

$$
\widehat A_{t,T}^{Q}
=
\frac{
\sum_{j\in R_t} F_j^{\mathrm{realized}}
+
\sum_{j\in U_t} F_j(t)
}{N},
$$

and observation-specific moneyness is

$$
m_{t,K,T}=\log\left(\frac{K}{\widehat A_{t,T}^{Q}}\right).
$$

A strike is not permanently ATM/ITM/OTM.

## 7. Use a date-specific Treasury curve

Place the official Treasury CSV files under:

```text
data/rates/treasury/
```

or let the workstation runner download the required year when the directory is empty.

```python
from bayesian_asian_options.rates import (
    load_treasury_par_yields,
    treasury_curve_on_or_before,
)

table = load_treasury_par_yields(["data/rates/treasury/2026.csv"])
curve = treasury_curve_on_or_before(table, "2026-09-04")
discount = curve.proxy_discount_factor(time_to_payoff_years)
```

The current pilot is explicit about its approximation: it interpolates the Treasury **par** curve and treats that yield as a continuously compounded zero-rate proxy. It is not called a bootstrapped zero/OIS curve. A proper zero/OIS discounting robustness specification can replace this component later without changing the rest of the pipeline.

## 8. Estimate historical volatility uncertainty

Historical returns are modeled under $\mathbb P$. The physical drift `mu` remains an inferred forecasting parameter but does not enter the risk-neutral APO pricing dynamics.

The first real-market driver runs multiple Metropolis chains and records chain-level acceptance rates plus Gelman-Rubin $\hat R$ for `mu` and `sigma`.

## 9. Price the observed cross-section under Q

`wti_apo_cross_section_mc` simulates the arithmetic average once for a shared expiry/fixing state and reuses it across all call/put strikes. Nearby sigma values use the same random seed, providing common random numbers.

The reported pricing rules are:

- Full Bayes: posterior mean of conditional prices;
- posterior-mean plug-in;
- marginal-sigma-mode plug-in;
- historical MLE plug-in.

The external benchmark is the observed Barchart end-of-day option mark.

## 10. First real experiment

The first implemented pilot is the October-2026 APO cross-section observed on 2026-09-04.

Direct command:

```bash
python -m experiments.wti_apo_empirical \
    --valuation-date 2026-09-04 \
    --apo-expiry 2026-10 \
    --download-treasury
```

The experiment writes a versioned run directory containing the first-nearby reconstruction, roll-return audit, MCMC diagnostics, posterior summary/draws, APO fixing state, pricing grid, contract-level prices/errors, source metadata, and a JSON manifest.

The current pilot uses a weekday fixing schedule because October 2026 has no full-day CME energy closure. General production-panel work must replace this fallback with an explicit exchange settlement calendar before results are treated as final.

## 11. University-PC launcher

After editable installation:

```bash
python -m scripts.run_university_wti_apo --check-only
python -m scripts.run_university_wti_apo --quick
python -m scripts.run_university_wti_apo
```

`--quick` is for an end-to-end smoke run. The default command uses the higher-precision MCMC/pricing settings. Yahoo futures downloads and Treasury CSVs are cached locally.

## 12. Source validation

If a small Barchart/CME reference table is available locally, pass:

```bash
python -m scripts.run_university_wti_apo \
    --quick \
    --futures-reference-csv path/to/reference.csv
```

The reference schema is `trade_date,contract,close`. The validation report contains Yahoo close, reference price, difference, and absolute difference. Do not commit newly acquired proprietary reference data unless redistribution rights are clear.
