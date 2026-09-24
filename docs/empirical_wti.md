# Empirical WTI APO workflow

This page describes the implemented research pipeline for the CME WTI Average Price Option application. It is an implementation map, not a substitute for `research/EMPIRICAL_WTI_DESIGN.md`.

## Data-source contract

The empirical application deliberately uses different sources for different objects:

- **WTI APO market marks:** committed Barchart option histories under `data/csv`;
- **physical-measure volatility inference:** baseline Yahoo Finance `CL=F` continuous/front-month proxy, with an implemented robustness route using a contract-reconstructed first-nearby CL settlement series from official Databento statistics;
- **realized first-nearby fixings and valuation-date CL term structure:** committed Barchart `Daily Prices` histories under `data/csv/CL`;
- **CL last-trade dates:** the explicit versioned table `data/csv/CL/contract_expiries.csv`;
- **USD discounting:** U.S. Treasury Daily Treasury Par Yield Curve Rates;
- **independent risk-neutral validation:** local Databento CME/NYMEX `LO` option definitions and official `statistics`, acquired through a cost-capped workflow and not committed as raw vendor data;
- **optional validation:** a small external reference table can be supplied locally.

In the Barchart histories used by this project, `Latest` is the CME settlement field. The parser preserves the source-field name and does not reinterpret it as an intraday last trade.

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

The original empirical baseline uses Yahoo `CL=F` as an explicitly labelled continuous/front-month proxy. Issue #38 adds a contract-reconstructed alternative from official final CL settlements so the paper can test whether its historical-`P` baseline depends on Yahoo's undocumented roll construction.

The reconstruction is deliberately cost-gated. Quote first:

```powershell
python -m experiments.wti_databento_first_nearby --mode quote
```

Only if the quote is acceptable:

```powershell
python -m experiments.wti_databento_first_nearby --mode download
python -m experiments.wti_first_nearby_reconstruction
```

The reconstruction maps every trading date to the earliest CL contract whose observed final-settlement last-trade date has not passed. A return is admitted to the physical-volatility likelihood only when the current and previous settlements belong to the same contract. The first return after every contract switch is therefore excluded rather than treating contango or backwardation as a one-day diffusion shock.

The reconstruction experiment compares the roll-clean return series against Yahoo `CL=F` over the same calendar information window and fits the paper's same Gaussian-GBM posterior to both. Raw vendor snapshots remain local; derived roll boundaries, posterior comparisons, diagnostics, and the report are versioned.

The canonical pricing driver can then use the reconstructed source without creating a second valuation engine:

```powershell
python -m experiments.wti_apo_empirical --valuation-date 2026-09-04 --apo-expiry 2026-10 --physical-inference-source first-nearby --download-treasury
```

For the complete publication robustness rerun, use the one-command production runner:

```powershell
python -m scripts.run_first_nearby_robustness
```

It reconstructs the return panel, runs the same seven-expiry strict-forward suite under the first-nearby physical posterior, reruns the independent vanilla-WTI comparison and its date-cluster bootstrap, and finally checks Yahoo versus first-nearby historical-P errors on exact matching holdouts. These runs are automatically namespaced under `*_first_nearby` output roots and do not overwrite the original Yahoo-based production results.

## 4. Load the Barchart CL histories

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

For an averaging month `M`, daily first-nearby fixings use the `M+1` delivery contract until its last-trade date and then the `M+2` delivery contract. Thus the October-2026 APO requires `CLX26` and `CLZ26`. The September-2026 APO uses `CLV26` and `CLX26`.

On the 2026-09-04 valuation date the committed files contain `CLX26 = 88.57` and `CLZ26 = 85.46` in the Barchart `Latest` field. These values are preserved in the run-level valuation-curve audit.

## 5. Reconstruct realized and remaining APO fixings

Last-trade dates are read from the explicit study table rather than inferred through an undocumented roll heuristic. The same contract mapping is used for both already realized fixings and remaining fixings.

```python
from bayesian_asian_options.barchart_cl import (
    barchart_cl_curve_on_date,
    load_cl_expiry_table,
)
from bayesian_asian_options.wti_first_nearby import (
    build_forward_fixing_curve,
    build_realized_fixing_curve,
)

expiries = load_cl_expiry_table(
    "data/csv/CL/contract_expiries.csv",
    contracts=["CLV26", "CLX26"],
)

realized = build_realized_fixing_curve(
    realized_fixing_dates,
    expiries,
    panel,
)

curve_t = barchart_cl_curve_on_date(
    panel,
    valuation_date,
    contracts=remaining_contracts,
)
remaining = build_forward_fixing_curve(
    remaining_fixing_dates,
    expiries,
    curve_t,
)
```

The canonical one-date driver uses an **end-of-day convention**: a fixing dated on the valuation date is known for that same end-of-day option mark. Dates strictly later than the valuation date remain stochastic. Missing realized contract/date observations raise an error and are never forward-filled.

The current implementation still uses a weekday fixing schedule. This is intentionally fail-closed for partial fixing: if that provisional calendar includes a market holiday with no actual CL settlement, the panel audit marks the date unavailable instead of fabricating a fixing. An explicit CME energy settlement calendar remains required before final publication-scale cross-maturity tables.

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

The contract-level outputs additionally record

$$
\phi_t = \frac{|R_t|}{N},
$$

as `fraction_fixed`, together with `n_realized_fixings` and `n_remaining_fixings`. A strike is not permanently ATM/ITM/OTM.

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

The same driver now supports partial fixing. For example, a September-2026 end-of-day valuation inside the September averaging month can be run with:

```bash
python -m experiments.wti_apo_empirical \
    --valuation-date 2026-09-04 \
    --apo-expiry 2026-09 \
    --cl-data-dir data/csv/CL \
    --download-treasury
```

The run directory contains the continuous-proxy inference series, inference-return audit, MCMC diagnostics, posterior draws/summary, valuation-date CL curve for remaining fixings, explicit expiry table, combined realized/remaining `apo_fixing_state.csv`, pricing grid, contract-level prices/errors, Barchart CL source manifest, and the JSON reproducibility manifest.

Manifest schema version 3 records the realized/remaining fixing counts, `fraction_fixed`, the end-of-day timing convention, and the fail-on-missing-realized-fixing policy. Repository inputs use repository-relative paths. External paths are reduced to an `<external>/filename` form so workstation/user directories are not exposed. The manifest also records the Git commit and dirty-tree state plus Python, platform, NumPy, pandas, and SciPy versions; hostnames and user names are deliberately omitted.

## 11. University-PC launcher

After editable installation:

```bash
python -m scripts.run_university_wti_apo --check-only
python -m scripts.run_university_wti_apo --quick
python -m scripts.run_university_wti_apo
```

`--quick` is the end-to-end smoke run. A fresh run now requires network access only for Yahoo `CL=F` and, when no local Treasury CSV exists, the U.S. Treasury download. Individual CL curve contracts are read locally from `data/csv/CL`.

## 12. Multi-date panel and liquidity samples

The date-panel orchestrator now admits both pre-averaging and partial-fixing dates. For each candidate date it independently verifies:

1. an eligible APO cross-section exists;
2. every realized first-nearby fixing through the end-of-day valuation timestamp exists at the exact mapped CL contract/date;
3. the valuation-date CL curve contains every contract needed by the remaining fixing dates.

Inspect candidate dates first:

```bash
python -m experiments.wti_apo_date_panel --apo-expiry 2026-10 --list-dates
```

For the first partial-fixing experiment, inspect the already committed September data:

```bash
python -m experiments.wti_apo_date_panel \
    --apo-expiry 2026-09 \
    --start-date 2026-09-01 \
    --end-date 2026-09-04 \
    --list-dates
```

Run a lower-cost panel smoke test with the same date range by replacing `--list-dates` with `--quick`. A production run omits both flags.

A normal all-date run writes three separate samples so a liquidity robustness run cannot overwrite the baseline aggregation:

```text
results/wti_apo_empirical/panel_202609/
├── panel_date_audit.csv
├── all_dates/
│   ├── panel_contract_pricing.csv
│   ├── panel_error_summary.csv
│   ├── panel_overall_error_summary.csv
│   ├── panel_posterior_summary.csv
│   └── sample_manifest.json
├── positive_volume_dates/
│   └── ...
└── positive_volume_contracts/
    └── ...
```

The sample definitions are deliberately different:

- `all_dates`: every eligible date and every main-sample contract on those dates;
- `positive_volume_dates`: every contract on dates where at least one main-sample contract reports positive daily volume;
- `positive_volume_contracts`: only contract-date observations whose own reported daily volume is strictly positive.

The contract-level sample recomputes MAE/RMSE after filtering; it never reuses an error summary calculated from zero-volume contracts.

If the expensive single-date runs already exist, rebuild all three aggregate views without rerunning MCMC or Monte Carlo:

```bash
python -m experiments.wti_apo_date_panel \
    --apo-expiry 2026-10 \
    --aggregate-only
```

`--require-positive-volume` remains available when computation should be restricted to dates with at least one positive-volume observation. Those outputs are written only to `positive_volume_dates/` and `positive_volume_contracts/`, so they do not overwrite `all_dates/`.

The root `panel_date_audit.csv` reports raw/main-sample option counts, liquidity, realized and remaining fixing counts, `fraction_fixed`, realized-fixing availability, remaining-curve availability, eligibility, and any availability failure message.

## 13. Source validation

An optional external table with schema `trade_date,contract,close` can be passed with:

```bash
python -m scripts.run_university_wti_apo \
    --quick \
    --futures-reference-csv path/to/reference.csv
```

The resulting report compares the external price with Barchart `Latest`. Keep licensing and redistribution restrictions in mind before publishing raw market-data files.


## 14. Independent vanilla-WTI Q state via Databento

Issue #36 tests whether an independently observed vanilla-WTI risk-neutral state predicts APO
marks without calibrating on the APO family itself. The Barchart vanilla histories currently
available begin after the strict October-2026 target window, so they are retained as parser/audit
fixtures rather than used as forward evidence.

The replacement source is Databento's CME Globex `GLBX.MDP3` dataset. Standard monthly WTI
options are selected through parent symbol `LO.OPT`. A one-day definition snapshot provides
the option `raw_symbol`, `underlying`, `strike_price`, `expiration`, and option class.
The first pilot filters to options on `CLX6` and `CLZ6`, strikes 85.0--94.5, then requests
only the low-volume `statistics` schema for 2026-08-24 through 2026-09-10.

Acquisition is local and fail-closed on cost:

```powershell
$env:DATABENTO_API_KEY = "<your local key>"
python -m experiments.wti_databento_external_q --mode quote
python -m experiments.wti_databento_external_q --mode discover
python -m experiments.wti_databento_external_q --mode download
```

The default hard cap is USD 5.00. Raw Databento records live under the gitignored
`data/databento/wti_external_q/raw/`; the versioned acquisition manifest records only query
metadata, quotes, selected instrument counts, hashes, and row counts. Repeated downloads are
blocked by default because duplicate streaming requests can incur repeated charges.

For `GLBX.MDP3`, the primary market objects are official settlement (`stat_type=3`), cleared
volume (`6`), and open interest (`9`). Databento's current statistics-availability table does not
list settlement-implied volatility (`14`) for CME Globex. The independent Q state is therefore
inferred from official LO option and CL futures settlements with an American-style futures-option
model; Black-76 remains only a labelled near-ATM robustness approximation. Before inversion, run
`python -m experiments.wti_databento_external_q_audit` to verify date/instrument coverage and
final-settlement flags.


### Databento vanilla-IV inversion

After the acquisition coverage audit reports `strict_forward_data_ready=true`, build the
contract-level vanilla WTI implied-volatility panel with:

```powershell
python -m experiments.wti_databento_external_q_iv --download-treasury
```

The driver selects the latest final, non-intraday CME settlement for each option and
underlying futures contract on each `ts_ref` date. It uses the later of the option/futures
settlement publication timestamps as the information-availability timestamp, reads the
option expiration from the Databento definition, interpolates the dated Treasury par-yield
curve under the paper's existing zero-rate-proxy approximation, and inverts volatility with
the American CRR futures-option model.

The output `vanilla_iv_panel.csv` remains contract-level and records strike, underlying,
settlement flags, moneyness, maturity, rate, inversion status, and implied volatility.
`daily_vanilla_iv_summary.csv` is diagnostic only; it does not yet define the final
strike/maturity aggregation used to predict APO settlements. Cleared volume and open
interest are retained as ex-post diagnostics and do not enter the volatility inversion.
