# Databento WTI APO history expansion — feasibility-first research plan

**Status:** Proposed, not executed. **Tracking:** [Issue #90](https://github.com/heri-espino/Bayesian-Uncertainty-in-WTI-APOs/issues/90).
**Decision:** Investigate longer-dated and longer-history CME WTI Average Price Option data *before* finalizing the REMEF submission; keep the completed paper intact as a fallback. Neither AAO availability nor costs are confirmed.

## Why this is worth considering

The existing empirical results are technically complete but limited in their independent **valuation dates**, not merely their row counts:

| Existing scientific object | Recorded coverage | Source |
| --- | --- | --- |
| Raw Barchart WTI APO history | 213 contracts, 11,179 contract-date observations (not an eligible pricing sample) | `paper/manuscript/sections_short/03_data_design.tex` |
| Strict forward APO volatility comparison | **2,381 held-out option-date observations**, **15 target dates**, **7 expiries** | `results/analysis/wti_extended_forward/README.md` |
| LO-to-APO independent external-volatility check | **253 matched APO contract-dates**, **10 target dates** | `paper/manuscript/sections_short/04_results.tex` |
| Existing Databento LO/CL acquisition | `GLBX.MDP3`, LO option definitions/statistics for Aug–Sep 2026, 404 selected options | `results/analysis/wti_databento_external_q/acquisition_manifest.json` |

Adding more LO observations alone **does not create new APO valuation dates**. The primary objective is to increase independent eligible APO *dates and market regimes*, while using additional LO and CL information for source-independent validation.

### Two independent paths (keep distinct)

1. **Priority: APO outcome panel.** Check whether Databento actually supplies usable historical **WTI APO** contract definitions and final settlements. CME product labels `AAO` (Globex) / `AO` (clearing) are **search candidates**, not verified Databento raw-symbol or parent-schema names and not evidence of historical feed coverage. Confirm actual identifiers from metadata and definitions.
2. **Secondary: LO/CL volatility and fixing inputs.** Expand the already implemented Databento **LO** (standard WTI options) and **CL** futures histories for the same eligible valuation dates, with prior-date LO volatility and compatible futures contracts. If APO history is unavailable, LO-only expansion can improve *coverage of existing APO dates* and sensitivity checks, but must be described as such.

Keep the completed 10-million-history synthetic experiment unchanged. Additional simulation is not a substitute for more distinct target dates.

## Phase 0 — Audit existing panel attrition **before purchases**

Reconstruct a date-by-expiry waterfall from the currently committed Barchart APO archive:

1. Raw record counts and unique `valuation_date × expiry × strike × option_type` keys; duplicate and timestamp treatment.
2. Available matched daily APO settlements and contract metadata; positive-volume and open-interest counts separate from eligibility.
3. Exact first-nearby CL fixing and target-date term-structure support, required CL maturity/roll table, dated rates, CME settlement calendar and holidays.
4. Baseline posterior availability at each cutoff; number of contracts for fitting the existing six-parameter prior APO smile.
5. Chronologically valid smile calibration and at least one **strictly earlier** observation date for each test; any additional same-contract prior-IV coverage.
6. Different denominators for complete-price, liquid-contract, positive-volume-*date*, positive-volume-*contract*, external-LO and common-support samples.

Output proposed `results/analysis/wti_aao_history_feasibility/existing_sample_attrition.csv` plus a human-readable summary. **Do not overwrite** the existing `results/analysis/wti_extended_forward/` outputs. Reuse the logic in `experiments/wti_expiry_coverage_audit.py`, `experiments/wti_apo_date_panel.py`, and `scripts/run_extended_forward_validation.py`; improve eligibility rules rather than inventing a second pricing driver.

If the apparent 15-date limit is primarily an avoidable selection/calibration limitation rather than raw-data availability, address that first.

## Phase 1 — Free metadata and strictly cost-capped quotes (AAO availability is unknown)

Databento source candidate: `GLBX.MDP3`, subject to actual dataset entitlements and historical coverage. Reuse the proven `experiments/wti_databento_external_q.py` quote/discovery patterns, but **do not** mislabel its LO-only `--mode quote` as an AAO quote.

- Confirm whether the CME APO product is disseminated in the accessible instrument-definition data, its true `raw_symbol`, `parent`, exchange, contract size, option type, strike representation, underlying and expiry; confirm whether the feed spans the historical years sought. `AAO`/`AO` are discovery labels, not guaranteed Databento `stype_in=parent` symbols.
- Probe a few **separate historical windows** (illustrative: 2023, 2024, 2025, 2026), subject to actual dataset start and entitlement, to prevent misleading extrapolation from one day.
- First request metadata and price estimates (`get_cost`/availability checks where offered); **do not** download full definition or statistics history just to learn prices. If a minimal billable snapshot is required, request explicit approval and enforce a hard USD cap before the request.
- For available options, test official `statistics` records: settlement `stat_type=3`, cleared volume `6`, open interest `9`; distinguish final/preliminary, actual/theoretical as represented by `stat_flags`. Use the **CME trading reference date** (e.g. `ts_ref` where available), not the download timestamp or publication timestamp. Observe missing exchange settlement dates.
- Record quote basis, requested interval (end exclusive), symbol count, returned definitions/statistics, selected contracts and entitlements, proposed total acquisition costs, and versioned **aggregate** coverage—never the API key. Never extrapolate the old small LO cost quote to a multiyear AAO download.

Proposed command **to implement in the next coding PR**, not an existing command:
`python -m experiments.wti_databento_aao_feasibility --mode quote --years 2023 2024 2025 2026 --max-quote-usd 5`.

Deliverables: `results/analysis/wti_aao_history_feasibility/metadata_coverage.csv`, `cost_quotes.json`, `feasibility_report.md` and redacted manifest, with no licensed records committed.

### Feasibility stop conditions

Stop and report **NO-GO** before purchasing large datasets if any of the following applies: no Databento AAO feed/entitlement; no reliable historical official settlements; inadequate exact-date CL or option-definition joins; restricted contract coverage; data cost disproportionate to genuinely new *dates*; or incompatible settlement semantics. Do **not** substitute LO prices for APO prices or quietly manufacture missing APO marks.

## Phase 2 — Small approved pilot and cross-vendor reconciliation

**Only after feasible coverage + explicit spend authorization**, acquire a small AAO option + required CL + LO bundle for a few overlapping Barchart dates and separate older nonoverlapping dates. Acquisition must be restartable and cost-capped, not a speculative bulk request.

- Match `valuation_date, APO expiry, option_type, strike`, contract multiplier, fixing schedule, settlement conventions, final flags and Barchart `Latest` (known here to be a CME settlement field). Verify option chain identity before comparing price levels.
- Compare matched official option marks, unmatched rows, stale/zero-volume vs traded records, preliminary/final updates, holidays and late-reported corrections. Report discrepancies and sample rules; do not cherry-pick clean matches.
- Validate the first-nearby CL roll rule and delivery contracts over the added years using observed last-trade calendars—not approximated `CL=F` roll dates. Preserve physical-`P` versus risk-neutral-`Q` source roles and date-specific rates.
- Assess prior-date LO implied-volatility surface availability and common strike support on the exact eligible target dates.

Save source metadata and SHA256/file inventories locally with redacted paths; never commit raw Databento payloads, account secrets or licensed historical quote records. Derived aggregates only if license permits.

## Phase 3 — Predeclared expansion and evaluation design

If the pilot works, **freeze** the sample eligibility and model choices before examining new holdout outcomes:

- Extend the existing canonical `experiments/wti_apo_empirical.py` / `experiments/wti_apo_date_panel.py` ingestion and rerun the production `scripts/run_extended_forward_validation.py` orchestration. Any new source adapters belong in reusable library modules with public API docs/tests; no parallel AAO valuation engine.
- Hold out a later chronological block (and report earlier/next-year regimes separately) while fitting all volatility surfaces only on dates *strictly before* each target date. Ensure price marks on the target date never leak into volatility input estimation.
- Compare on **identical eligible contract-date rows**: posterior integration (PI), posterior-mean plug-in (PM), historical rolling/EWMA/GARCH, lagged APO IV smile, lagged same-contract IV, and separate prior LO-derived IV using its own accessible support.
- Primary outcomes: independent valuation-date and expiry counts, MAE, RMSE, bias, dispersion of `PI-PM` and posterior-model-price intervals; report spread across year/regime, pre-/partial fixing, volume and OI, and expiry. Preserve date-cluster dependence; consider time-block bootstrap or other sensitivity when clusters are serially dependent. Do not treat thousands of contracts per date as thousands of independent dates.
- Show attrition and liquidity checks alongside headline results, including a fully matched sample for comparisons. Keep separate all-mark, own-volume-positive and date-volume-positive universes.
- Retain the 2026 research outputs unchanged until a named `extended_history` result family passes numerical parity on overlapping dates; audit identical row keys and source-specific differences.

Proposed new experiment/orchestration names for **future** PRs only (not currently implemented): `experiments/wti_databento_aao_feasibility.py` for metadata/cost, and an optional source adapter in `bayesian_asian_options.databento_wti`. Build tests with stored **synthetic** fixtures and query stubs so CI does not contact Databento.

## Gate for scaling up and changing journal target

Before spending more, prepare one decision sheet with:
- New **distinct, independently eligible valuation dates** vs the existing 15 main / 10 external, and how many separated market regimes/years;
- number of expiries with sufficient *prior-date* IV cross-sections, complete CL fixing maps, contemporaneous rates and real settlement observations;
- expected USD charge and author's explicitly approved budget ceiling;
- whether greater temporal coverage changes the conclusion or uncertainty, not only statistical significance.

A useful working aspiration is **dozens of extra distinct dates spanning multiple market conditions**; targets like 100–250 dates are planning scenarios, **not confirmed Databento coverage or a requirement for acceptance**. If AAO cannot add credible dates or the cost is too high, keep the current manuscript and proceed with its best-fitting submission route rather than postponing indefinitely.

**Journal decision occurs after the feasibility/pilot gates.** REMEF remains the prepared candidate. A longer history may justify reconsidering commodity-market journals, but no acceptance prediction is implied. Do not update the paper's numerical results, figures, conclusion or archived software DOI to describe proposed data as acquired.

## Execution and research integrity rules

- Do not spend money or initiate data downloads in this planning PR.
- Use `DATABENTO_API_KEY` only from the local environment. Raw vendor files are local/gitignored; provenance and permitted aggregate diagnostics are versioned.
- Heavy acquisitions, pricing runs, figure builds and manuscript builds are local or manual-only `workflow_dispatch`; lightweight tests/documentation can run on PRs.
- Retain source-specific files, definition-to-symbol mapping, CME reference-date semantics, cost quotes, SHA256s, exact historical cutoffs, selected/failed dates and source-code commit in every run manifest.
- The user reviews the Stage 1/2 report and **approves actual spending and expansion** before large downloads.

## Implemented first gate (2026-10-21; results not yet executed on VM)

**Both diagnostic commands are now implemented**, with synthetic local
tests and **no data download function** in the AAO probe:

```powershell
git switch main
git pull --ff-only origin main
conda run --no-capture-output -n asian-options python -m pytest tests/test_wti_aao_history_feasibility.py -q
conda run --no-capture-output -n asian-options python -m experiments.wti_aao_existing_attrition
# Set DATABENTO_API_KEY in your local session, then:
conda run --no-capture-output -n asian-options python -m experiments.wti_databento_aao_feasibility --mode quote --years 2023 2024 2025 2026 --parents AAO.OPT AO.OPT --max-quote-usd 5
```

Output directory:
`results/analysis/wti_aao_history_feasibility/`.

- `existing_sample_attrition.csv`: market row/key/date decomposition, liquidity
  counts, source-specific CL eligibility, the necessary earlier-smile date
  condition and recorded exact forward holdouts (if the saved file exists).
- `existing_sample_attrition.json`: totals, by-expiry counts and failure flags.
- `aao_metadata_quotes.json`: dataset/schema availability, candidate
  AAO/AO parent resolution *counts* on June's second Wednesday in each requested year,
  one-day **USD quotes** for definition/statistics where supported,
  redacted API errors, and `historical_aao_settlements_confirmed=false`.

No historical AAO price or final settlement download is performed or
asserted. A price quote is not a purchase, and `--max-quote-usd` only
highlights estimates that exceed the proposed pilot limit; it does not
authorize any spending. Databento's `symbology.resolve` or `get_cost`
may reject candidates and that negative/error result must be reported,
not replaced by guessed symbols or a different contract family.

**Live-probe correction (2026-10-22):** The first user-side metadata
run successfully listed `GLBX.MDP3` (including available historical
`definition` and `statistics` schema ranges) but **all 8 parent
resolution probes failed before any quotes**: Databento requires
`[ROOT].OPT` under `stype_in=parent`. We now use `AAO.OPT` and
`AO.OPT` as candidates, normalize bare aliases, and probe on the
second Wednesday of June to avoid the former Saturday anchor for
2023. This does not yet establish APO contract presence or any
historical final settlements. No paid acquisition took place.

**Next action:** run these two scripts on the VM; inspect the returned
reports and decide whether a separately approved small paid acquisition
is scientifically and economically justified. No Databento cost or new
empirical result is claimed by the current coding PR.
