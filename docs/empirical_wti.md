# Empirical WTI APO workflow

This page describes the implemented research pipeline for the CME WTI Average Price Option application. It is an implementation map, not a substitute for `research/EMPIRICAL_WTI_DESIGN.md`.

## Data-source contract

The empirical application deliberately uses different sources for different objects:

- **WTI APO market marks:** committed Barchart option histories under `data/csv`;
- **physical-measure volatility inference:** Yahoo Finance `CL=F`, explicitly labelled as a continuous/front-month proxy;
- **valuation-date CL term structure and APO fixing contracts:** committed Barchart `Daily Prices` histories under `data/csv/CL`;
- **CL last-trade dates:** the explicit versioned table `data/csv/CL/contract_expiries.csv`;
- **USD discounting:** U.S. Treasury Daily Treasury Par Yield Curve Rates;
- **optional validation:** a small external reference table can be supplied locally.

Barchart `Latest` is used as the futures end-of-day price / settlement proxy. It is not silently renamed an official CME settlement.

A live workstation test showed that Yahoo can return 404 / `YFTzMissingError` for older delisted individual contracts such as `CLG24.NYM`. Individual Yahoo CL pages are therefore no longer required by the canonical pilot.

## 1. Ingest the option histories

Use all downloaded APO contracts in the raw panel. Do not select strikes according to the final observed WTI level.

```python
from bayesian_asian_options.barchart_apo import discover_barchart_histories, build_apo_panel

paths = discover_barchart_histories("data/csv")
raw_panel = build_apo_panel(paths, deduplicate_contracts=True)
```

The APO discovery function ignores the separate `data/csv/CL` futures files because they do not match the JAO option filename convention.

## 2. Keep data richness separate from liquidity

`data/csv/richest_option_series.csv` is a historical-coverage diagnostic, not a liquidity ranking. Use `summarize_contracts` for diagnostics and `apply_main_sample_filters` for transparent sample rules.

## 3. Build the physical-measure inference sample

The current pilot uses Yahoo `CL=F` only for historical-return inference:

```python
from bayesian_asian_options.wti_yahoo import download_yahoo_wti, prepare_wti_model_sample

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

This is an explicit measurement compromise, not a contractual claim. Yahoo does not document the historical `CL=F` roll convention precisely enough to call the series a self-reconstructed CME first-nearby series. The experiment manifest records that limitation.

If a later source provides a complete historical monthly CL strip, the preferred robustness specification is to reconstruct the first-nearby series contract by contract and exclude every return that spans a roll.

## 4. Load the Barchart CL term structure

The committed futures files live under:

```text
data/csv/CL/
├── CLV26.csv
├── CLX26.csv
├── CLZ26.csv
├── ...
├── CLN29.csv
├── CLQ29.csv
└── contract_expiries.csv
```

Load only the contracts needed for a particular APO averaging month:

```python
from bayesian_asian_options.barchart_cl import load_barchart_cl_strip

panel, manifest = load_barchart_cl_strip(
    "data/csv/CL",
    contracts=["CLX26", "CLZ26"],
)
```

For an averaging month `M`, daily first-nearby fixings use the `M+1` delivery contract until its last-trade date and then the `M+2` delivery contract. Thus the October-2026 pilot requires `CLX26` and `CLZ26`, not a historical strip of old Yahoo contracts.

On the 2026-09-04 valuation date the committed files contain `CLX26 = 88.57` and `CLZ26 = 85.46` in the Barchart `Latest` field. These values are preserved in the run-level valuation-curve audit.

## 5. Reconstruct the APO fixing curve

Last-trade dates are read from the explicit study table rather than inferred through an undocumented roll heuristic:

```python
from bayesian_asian_options.barchart_cl import (
    barchart_cl_curve_on_date,
    load_cl_expiry_table,
)
from bayesian_asian_options.wti_first_nearby import build_forward_fixing_curve

expiries = load_cl_expiry_table(
    "data/csv/CL/contract_expiries.csv",
    contracts=["CLX26", "CLZ26"],
)
curve_t = barchart_cl_curve_on_date(
    panel,
    "2026-09-04",
    contracts=["CLX26", "CLZ26"],
)
forward_fixings = build_forward_fixing_curve(
    fixing_dates=remaining_fixing_dates,
    contract_expiries=expiries,
    futures_curve=curve_t,
)
```

The current October-2026 pilot still uses a weekday fixing schedule. General production-panel work must replace that fallback with an explicit CME energy settlement calendar before final publication tables are produced.

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

Place official Treasury CSVs under `data/rates/treasury/`, or let the workstation runner download the required year when the directory is empty.

```python
from bayesian_asian_options.rates import load_treasury_par_yields, treasury_curve_on_or_before

table = load_treasury_par_yields(["data/rates/treasury/2026.csv"])
curve = treasury_curve_on_or_before(table, "2026-09-04")
discount = curve.proxy_discount_factor(time_to_payoff_years)
```

The current pilot interpolates the Treasury **par** curve and treats that yield as a continuously compounded zero-rate proxy. It is not described as a bootstrapped zero/OIS curve. A proper zero/OIS discounting robustness specification can replace this component later without changing the rest of the pipeline.

## 8. Estimate historical volatility uncertainty

Historical returns are modeled under $\mathbb P$. The physical drift `mu` remains an inferred forecasting parameter but does not enter the risk-neutral APO pricing dynamics.

The real-market driver runs multiple Metropolis chains and records chain-level acceptance rates plus Gelman-Rubin $\hat R$ for `mu` and `sigma`.

## 9. Price the observed cross-section under Q

`wti_apo_cross_section_mc` simulates the arithmetic average once for a shared expiry/fixing state and reuses it across all call/put strikes. Nearby sigma values use common random numbers.

The reported pricing rules are Full Bayes, posterior-mean plug-in, marginal-sigma-mode plug-in, and historical MLE plug-in. The external benchmark is the observed Barchart end-of-day APO mark.

## 10. Canonical real-market experiment

There is one canonical driver for the Barchart-CL/Yahoo-CL=F/Treasury workflow:

```bash
python -m experiments.wti_apo_empirical \
    --valuation-date 2026-09-04 \
    --apo-expiry 2026-10 \
    --cl-data-dir data/csv/CL \
    --download-treasury
```

The run directory contains the continuous-proxy inference series, inference-return audit, MCMC diagnostics, posterior draws/summary, valuation-date CL curve, explicit expiry table, APO fixing state, pricing grid, contract-level prices/errors, Barchart CL source manifest, and the JSON reproducibility manifest.

The manifest schema stores repository inputs as repository-relative paths. External paths are reduced to an `<external>/filename` form so workstation/user directories are not exposed. It also records the Git commit and dirty-tree state plus Python, platform, NumPy, pandas, and SciPy versions; hostnames and user names are deliberately omitted.

## 11. University-PC launcher

After editable installation:

```bash
python -m scripts.run_university_wti_apo --check-only
python -m scripts.run_university_wti_apo --quick
python -m scripts.run_university_wti_apo
```

`--quick` is the end-to-end smoke run. A fresh run now requires network access only for Yahoo `CL=F` and, when no local Treasury CSV exists, the U.S. Treasury download. Individual CL curve contracts are read locally from `data/csv/CL`.

## 12. Multi-date panel

The date-panel orchestrator discovers valuation dates for which both the APO cross-section and the two required Barchart CL contracts are available. It never replaces the single-date driver; it invokes that driver once per date and aggregates the resulting outputs.

Inspect candidate dates first:

```bash
python -m experiments.wti_apo_date_panel --apo-expiry 2026-10 --list-dates
```

Run a lower-cost panel smoke test:

```bash
python -m experiments.wti_apo_date_panel --apo-expiry 2026-10 --quick
```

To focus on valuation dates with at least one positive-volume option observation:

```bash
python -m experiments.wti_apo_date_panel \
    --apo-expiry 2026-10 \
    --quick \
    --require-positive-volume
```

Panel outputs are written under `results/wti_apo_empirical/panel_<YYYYMM>/` and include `panel_date_audit.csv`, `panel_contract_pricing.csv`, `panel_error_summary.csv`, and `panel_posterior_summary.csv`. The date audit reports raw/main-sample option counts, positive-volume counts, total reported volume, and whether both required CL curve contracts exist on each date.

## 13. Source validation

An optional external table with schema `trade_date,contract,close` can be passed with:

```bash
python -m scripts.run_university_wti_apo \
    --quick \
    --futures-reference-csv path/to/reference.csv
```

The resulting report compares the external price with Barchart `Latest`. Keep licensing and redistribution restrictions in mind before publishing raw market-data files.
