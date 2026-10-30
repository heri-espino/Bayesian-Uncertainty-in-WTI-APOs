# WTI APO price-provenance gate for JFM (2026-10-29)

**Status: partially checked; the core Barchart settlement-mark provenance remains unresolved.**

This is a record-by-record source audit, not an assertion that vendor price vintages are authentic or that the observed marks were traded.

## Author confirmation (2026-10-30)

The author confirmed that they personally assembled the Barchart research
sample and accepts its recorded observations as the data source for Paper A.
This author acceptance allows the paper to proceed as a **conditional,
retrospective valuation comparison**, provided its existing provenance,
settlement-proxy, trading-volume, and timing disclosures stay explicit.
It is **not** independent certification of historical vendor release times,
revision vintages, execution prices, or exchange settlement status.
No external claim of an independently prospective trading experiment is made.

## What the repository establishes

1. `results/analysis/wti_extended_forward/forward_q_validation/forward_q_report.json` records 4,762 method-specific forward predictions on 15 target valuation dates across seven expiries. Its guardrail is strictly earlier-date APO implied-volatility fitting; it explicitly does not use same-day APO implied volatilities to fit or price that target. **This is an auditable source-date ordering rule, not independently verified source *publication-time* ordering.**
2. `results/analysis/wti_extended_forward/README.md` reports 2,381 option-date holdouts (15 target-date clusters), with a positive-volume restricted set of 62 observations on 13 dates. Of the 2,381 observations, 2,319 report zero volume (97.4%). Those prices are not demonstrated executed trades.
3. The external cross-instrument LO control is better sourced: `results/analysis/wti_databento_external_q/acquisition_manifest.json` records Databento `GLBX.MDP3` LO/CL source filenames and checksums. `results/analysis/wti_databento_external_q/coverage_audit.json` reports final settlement observations for 404 selected **LO** options, 13 expected valid session dates, and exclusion of 2026-09-07. It uses CME `ts_ref` and distinguishes preliminary/final and actual/theoretical via `stat_flags`. These checks establish **external LO input coverage**, not independent validation of the Barchart AAO target marks.
4. `results/analysis/wti_aao_history_feasibility/settlement_gate/gate_2026-06.json` concerns a **different future AAO/Databento feasibility project**. It excludes 201,293 unmatched records, distinguishes actual and theoretical flags, and explicitly warns it is not a stable price-level or forward-eligible panel. Do not silently substitute those unvalidated AAO observations for this Paper A dataset.
5. CME Clearing Advisory 20-198 (dated **May 15, 2020**) specifies changing the model used for WTI Average Price Option end-of-day valuation to **Curran**, effective **May 18, 2020**:
   https://www.cmegroup.com/notices/clearing/2020/05/Chadv20-198.pdf
   This source establishes potential dependence between Curran-based repricing and CME model-settlement marks. It does **not** establish that every Barchart `Latest` record was the corresponding final CME settlement.

## Still not verified

- Source-by-source original UTC publication timestamps and subsequent correction history of historical **Barchart AAO** observations.
- Mapping from each Barchart `Latest` value to final CME settlement versus theoretical/preliminary vendor mark.
- Whether selected **AAO** cross-sections have sufficient actual trading activity for an independent trade-price experiment.
- Market-data licenses covering distribution of raw records, derived rows, and source-linked reconstruction.
- A true prospective test that fixes *all* inputs (not only volatility) before the target-date quote or settlement.
- The impact of model-based exchange marks on the size of the implied-volatility pricing advantage.

## Editorial interpretation

The supported statement is **date-ordered conditional repricing against vendor end-of-day price proxies**, with a separately sourced prior-date LO implied-volatility input. It is not a verified real-time, transaction-backed forecast and cannot establish structural physical/risk-neutral volatility or risk premium differences.

For a stronger market-validation claim, obtain original provider publication-vintage metadata and final AAO settlement flags/actual transaction prices for a new independently dated sample. The existing manuscript is defensibly cautious only if these missing facts remain explicitly disclosed. Do not claim that this provenance gate is closed just because the PDF compiles.
