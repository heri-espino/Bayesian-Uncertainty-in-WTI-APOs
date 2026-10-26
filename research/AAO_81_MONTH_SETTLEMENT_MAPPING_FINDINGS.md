# All-81-month AAO inventory and daily-definition mapping anomaly — 2026-10-25

## Evidence from author-run Windows VM commands

**Source:** Author's local logs from `experiments.wti_aao_settlement_gate`, full `aao_inventory_summary.json` and verified 162-file Databento acquisition. Raw vendor data remain on the author's VM; the author shared only aggregate outputs.

The complete 81-month offline inventory reports:

| Measure | All 81 months (2020-01 through 2026-09) |
|---|---:|
| `months_processed` | **81** |
| `records` (statistics only) | **70,154,064** |
| `settlement_events` | **13,412,045** |
| `final_events` | **5,899,096** |
| `final_actual_events` | **4,027,696** |
| `final_theoretical_events` | **1,871,400** |
| `distinct_final_reference_dates` | **1,701** |
| Positive cleared-volume statistic events | **99,878** |
| Positive open-interest statistic events | **5,781,953** |

The previous 80-month inventory found 1,682 distinct final reference dates, so adding February 2021 adds **19 distinct reference dates**. These are distinct CME trading-reference dates containing *final settlement events*, not independently eligible forward model test dates. The 5.9 million events are not distinct option contract/day marks. The download integrity checker separately verified all **162 DBN files by SHA256**, with no issues.

## Time-aware same-UTC-day diagnostic (not a final join)

```powershell
python -m experiments.wti_aao_settlement_gate --months 2021-02 2026-06
```

| Report | Feb 2021 | Jun 2026 |
|---|---:|---:|
| Settlement statistic events | 127,958 | 248,275 |
| Without a **same-UTC-event-day, earlier** definition | **97,438 (76.1%)** | **201,293 (81.1%)** |
| With such a definition | 30,520 | 46,982 |
| Tentative ID/day/reference keys | 23,912 | 32,258 |
| Selected final active tentative keys | 23,900 | 32,258 |
| Selected actual-flagged | 6,584 | 8,255 |
| Selected theoretical-flagged | 17,316 | 24,003 |
| Selected keys whose publication UTC day differs from CME reference day | 23,660 | 31,902 |
| Distinct selected reference dates | 17 | 15 |

**Interpretation:** The old `wti_aao_identity_probe` matched every final event to some outright definition ID *somewhere in the same month*; the follow-up `wti_aao_settlement_gate` requires a preceding definition on the *same event UTC day*. The much lower match rate is **not proof of missing market data or a liquidity crisis**. In fact, nearly all selected keys have a publication UTC date that differs from their `ts_ref` reference date.

Databento's official [GLBX.MDP3 guide](https://databento.com/docs/datasets/glbx-mdp3) explains that `ts_ref` is the CME `TradingReferenceDate`, with date precision, and settlement publication times need not coincide with that session date. Databento's [instrument-definition documentation](https://databento.com/docs/schemas/instrument-definitions) describes point-in-time definitions and UTC-midnight snapshots on weekdays. **Reference trading date, publication UTC day and the preceding UTC day are distinct concepts.**

**Do not** use the strict same-day selected counts as a final sample, deduce that 76–81% of prices are unusable, claim that 1,701 dates are valid chronological tests, or alter paper pricing figures on that basis.

## Next implemented diagnostic: compare three daily snapshot conventions

```powershell
git switch main
git pull --ff-only origin main
conda activate asian-options
python -m pytest tests/test_wti_aao_mapping_comparison.py -q
python -m experiments.wti_aao_mapping_comparison --months 2021-02 2026-06
```

This **offline, no-charge** script compares candidate definition snapshots dated to (1) CME `ts_ref` date, (2) `ts_event` publication UTC day, and (3) the previous UTC day. It reads each month separately and **only emits aggregate counts** in `results/analysis/wti_aao_history_feasibility/mapping_comparison/`, including ambiguous within-day instrument identities, missing candidate definitions, future-only snapshots, non-outright/strategy records, and cases in which the alternative mappings associate **different contract fingerprints** with the same statistic. It rejects unknown definition actions. No raw symbols, settlement prices or licensed rows are exported.

**These methods are hypotheses, not authorized alternative final joins.** A union of their matches can include false positives from instrument-ID reuse. Even agreement on contract identity between candidate snapshots is not yet a fully historical, revision-aware stable-contract validation. The experiment must inform a separately tested rule for contract normalization that respects instrument-ID scope, CME session boundaries and price-publication information cutoffs.

## Next scientific gates

1. Evaluate two-month candidate mapping rates and **identity disagreement**. On each matched event, preserve a defensible definition before settlement publication; investigate weekend and cross-month snapshots. Verify definition `security_update_action` and statistical `update_action`, including corrections/deletions and intraday settlement flags, against authoritative documentation.
2. Build **stable outright option contract identity** from actual raw symbol, call/put, expiry, strike, underlying, exchange and effective definition record. Do not use `instrument_id` as a multiyear key. Inspect any conflicting within-day identities and data-quality dates.
3. Select the latest admissible final official settlement per stable contract × CME reference date; distinguish theoretical vs actual marks, volume/OI and timestamp availability. Cross-check matching Barchart `Latest` prices. Do not publish raw licensed prices.
4. Produce chronological, prior-information-supported eligibility funnel for CL first-nearby fixings, valuation-day futures curve, dated rates, earlier APO smiles and independent LO IV. Distinguish eligible test **dates** from contract-date **rows**.
5. Reuse canonical PI/PM and benchmark pricing code on frozen chronological splits and common support, with date/time-block inference. Only then regenerate **new** economic performance figures and rewrite the Elsevier CAS journal manuscript. The conditional Journal of Commodity Markets strategy and REMEF/JFM alternatives remain unchanged.

**No additional Databento purchases are necessary for these diagnostics.**
