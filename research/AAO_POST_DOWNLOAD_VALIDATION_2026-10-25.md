# AAO post-download checks and publication-time settlement gate — 2026-10-25

## Completed on author's VM, not reproduced on GitHub

**Verified local data integrity:** `python -m scripts.audit_aao_manifests` returned `success=true`, `files_verified=162`, `month_count=81`, `sha256_verified=true`, no issues, and **USD 17.49357489 quoted** across two acquisition manifests. The quoted amount is **not** provider-verified billing.

**Updated 81-month inventory source exists locally:** `scripts.plot_aao_history_coverage` accepted a full **81-month** event inventory with SHA256
`4ec3893c8b5b216a5f450ffa40d0a910012bf6b66910b5eb8ad5f0c7f8950c13`, and generated `fig05_aao_final_settlement_event_coverage.{pdf,png,svg}`. These are **diagnostic event-frequency graphics**, not prices or forecast-performance results. The **new total** number of final events and distinct reference dates from the 81-month inventory was not included in the author's console output; **do not re-use the earlier 80-month 5,843,770 and 1,682 totals** as current 81-month values.

**Exploratory same-month identity probes passed** for 2021-02 and 2026-06:

| Month | 2021-02 | 2026-06 |
|---|---:|---:|
| Definition events | 140,790 | 206,136 |
| Definition C / P / T events | 70,394 / 70,394 / 2 | 102,978 / 102,978 / 180 |
| Settlement statistic events | 127,958 | 248,275 |
| Final settlement events | **55,326** | **118,094** |
| Final actual-flagged events | **37,998** | **53,377** |
| Final theoretical-flagged events | **17,328** | **64,717** |
| Unique outright publisher-ID pairs observed | 6,252 | 8,082 |
| Final events with same-month matching outright publisher-ID | 55,326 | 118,094 |
| Final events without same-month matching ID | 0 | 0 |
| Tentative unique instrument-ID × `ts_ref` date pairs | **48,730** | **101,397** |
| Repeated final events beyond those tentative pairs | **6,596** | **16,697** |
| Distinct final reference dates | 19 | 23 |

The old identity probe joins definitions *anywhere in the same month* to statistics, without respecting the order of instrument definitions, changes, and settlement publication. Its **100% matched** outcome does **not** prove a causal as-of match, valid prices, or stable symbols across dates. Databento [explicitly states that instrument IDs are guaranteed unique only within a given day](https://databento.com/docs/conventions/common-fields-enums-types). Definition events are point-in-time records; CME statistics can be amended or deleted. See [definitions](https://databento.com/docs/schemas/instrument-definitions) and [statistics](https://databento.com/docs/schemas/statistics).

**CAS check:** `python paper/jcm/build.py --check` passed. The Elsevier manuscript is a working draft still using **prior validated 2026 Barchart/LO results**, not the extended 81-month pricing data. The author has not supplied a verified PDF build.

## New strictly offline diagnostic: publication-time-aware settlement gate

The follow-up script `experiments/wti_aao_settlement_gate.py` conservatively matches each settlement event to the latest definition **at or before the event time, and within the same UTC event calendar day**, using `publisher_id + instrument_id`. It does not carry potentially reused publisher IDs over days. The implementation intentionally *fails closed* on missing fields, unknown security/stat update codes, ambiguous tied settlement updates and invalid timestamps; it excludes strategy `T` / legged records, inactive definitions, non-final or deleted latest settlement updates.

It **only prints counts**: event-time definition matches and unmatched events, excluded strategy/inactive records, tentative reference-day ID keys, selected final + active rows, actual/theoretical flags, and differing `ts_event` UTC dates versus `ts_ref` trading reference dates. A same-day definition may be unavailable on weekends or some sessions, so unmatched rates are a diagnostic, **not evidence of absent valid market prices**. Its keys are still day-scoped temporary IDs and **are not stable across-month contract IDs**. It does **not** export price fields or a commercially restricted row-level panel.

Run locally, after updating the branch:

```powershell
conda activate asian-options
python -m pytest tests/test_wti_aao_settlement_gate.py -q
python -m experiments.wti_aao_settlement_gate --months 2021-02 2026-06
```

If the schema action codes are represented differently by Databento's pandas conversion, the script will reject them. Inspect the local representation and write regression fixtures; **do not bypass the check by guessing that an unknown action means New**.

## Scientific next steps (must precede new option-price experiments)

1. Examine whether the as-of join is usable in the two test months; quantify cases without same-day active definitions and those with `ts_ref` before publication time. Reconcile these by a documented calendar/venue mapping rather than silent forward-fill.
2. Define a stable outright **contract identity** with `raw_symbol`, instrument class, expiration, strike, exchange and underlying; verify these against `Barchart.Latest` contract-date marks and CME contract specs. Track definition updates and any raw-symbol changes. Do not equate an instrument ID with a multiyear contract.
3. Implement tested, *locally stored* final settlement corrections and unique **contract × CME reference date** prices. Preserve publication timestamps as the information-availability cutoff and distinguish actual/theoretical, final/preliminary, liquidity and source data quality.
4. Build the long-form dated CL first-nearby/fixing/rates and historical-return inputs. Strictly lag APO smile and independent LO-IV inputs; measure attrition in **eligible forward test dates**.
5. Only then rerun historical PI/PM, expanding/rolling/EWMA/GARCH/lagged-IV benchmarks on frozen chronological splits and common support. Report MAE/RMSE/bias with date/time-block uncertainty, liquidity, regime, expiry, fixing-progress and theoretical-settlement analyses.
6. Generate **new** empirical performance figures from those experiments, then revise the CAS JCM working manuscript, abstracts, tables and supplements. The paper remains **provisionally targeted to JCM**, conditional on its real scientific contribution, with REMEF/JFM alternatives intact.

No further Databento download or monetary authorization is needed for the current diagnostics.
