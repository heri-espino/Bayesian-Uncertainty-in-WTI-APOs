# Empirical WTI APO workflow

This page describes the implemented research pipeline for the CME WTI Average Price Option application. It is an implementation map, not a substitute for `research/EMPIRICAL_WTI_DESIGN.md`.

## Data-source contract

The empirical application deliberately uses different sources for different objects:

- **WTI APO market marks:** committed Barchart contract histories already present under `data/csv`;
- **physical-measure volatility inference:** Yahoo Finance `CL=F`, explicitly labelled as a continuous/front-month proxy;
- **valuation-date CL term structure and APO fixing contracts:** Yahoo Finance individual contract symbols such as `CLV26.NYM`, `CLX26.NYM`, and `CLZ26.NYM`;
- **CL contract settlement/expiration metadata:** Yahoo quote metadata when available, with a named pilot fallback for the October-2026 case and exchange/Barchart validation required for production work;
- **USD discounting:** U.S. Treasury Daily Treasury Par Yield Curve Rates;
- **validation:** small external reference tables can be supplied locally and are never required to be committed.

Yahoo `Close` is treated as a **daily settlement proxy**, not silently renamed an official CME settlement.

A live university-workstation test showed that Yahoo can return 404 / `YFTzMissingError` for older delisted individual contracts such as `CLG24.NYM`. Consequently, the project does **not** assume that Yahoo provides a complete historical strip of monthly CL contracts indefinitely.

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

## 3. Build the physical-measure inference sample

The current pilot uses Yahoo `CL=F` only for historical-return inference:

```python
from bayesian_asian_options.wti_yahoo import (
    download_yahoo_wti,
    prepare_wti_model_sample,
)

history, metadata = download_yahoo_wti(
    ticker="CL=F",
    start="2024-01-01",
    end="2026-09-05",
)
sample = prepare_wti_model_sample(
    history,
    start="2024-01-01",
    end="2026-09-05",
)
returns = sample.log_returns
```

This is an explicit measurement compromise, not a contractual claim. Yahoo does not document the historical `CL=F` roll convention precisely enough to call this series a self-reconstructed CME first-nearby series. The experiment manifest records that limitation.

If a later source provides complete contract-specific historical data, the preferred robustness specification is to reconstruct the first-nearby series contract by contract and exclude every return that spans a roll.

## 4. Download only the individual CL contracts needed for APO valuation

The APO payoff still requires contract-specific futures levels. For one averaging month we therefore download only a short local strip around that month. The October-2026 pilot uses:

```text
CLV26.NYM
CLX26.NYM
CLZ26.NYM
```

The October delivery contract has already expired by the averaging month, the November contract is first-nearby for the early October fixings, and the December contract becomes first-nearby after the November contract terminates.

These snapshots are cached under `data/wti_yahoo_contracts/` and are gitignored. This avoids making the experiment depend on Yahoo retaining dozens of old delisted contract pages.

## 5. Reconstruct the remaining APO fixing curve

For every remaining fixing date, map to the earliest CL contract that has not passed its settlement/expiration date:

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

Yahoo expiry metadata is preferred. If metadata is missing for an active contract, the October-2026 pilot can fall back to a named weekend-only implementation of the standard CL three-business-day termination rule. Production-panel dates affected by exchange holidays require a validated CME calendar rather than this pilot fallback.

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

The canonical first pilot is the October-2026 APO cross-section observed on 2026-09-04.

Direct command:

```bash
python -m experiments.wti_apo_empirical_hybrid \
    --valuation-date 2026-09-04 \
    --apo-expiry 2026-10 \
    --download-treasury
```

The experiment writes a versioned run directory containing the continuous-proxy inference series, inference-return audit, MCMC diagnostics, posterior summary/draws, APO fixing state, pricing grid, contract-level prices/errors, source metadata, and a JSON manifest.

The current pilot uses a weekday fixing schedule because October 2026 has no full-day CME energy closure. General production-panel work must replace this fallback with an explicit exchange settlement calendar before results are treated as final.

## 11. University-PC launcher

After editable installation:

```bash
python -m scripts.run_university_wti_apo --check-only
python -m scripts.run_university_wti_apo --quick
python -m scripts.run_university_wti_apo
```

`--quick` is for an end-to-end smoke run. The default command uses the higher-precision MCMC/pricing settings. The launcher now routes through the hybrid experiment: one `CL=F` inference history, only the individual CL contracts needed for the valuation curve, and Treasury data only when the local Treasury directory is empty.

## 12. Source validation

If a small Barchart/CME reference table is available locally, pass:

```bash
python -m scripts.run_university_wti_apo \
    --quick \
    --futures-reference-csv path/to/reference.csv
```

The reference schema is `trade_date,contract,close`. The validation report contains Yahoo close, reference price, difference, and absolute difference. Do not commit newly acquired proprietary reference data unless redistribution rights are clear.
