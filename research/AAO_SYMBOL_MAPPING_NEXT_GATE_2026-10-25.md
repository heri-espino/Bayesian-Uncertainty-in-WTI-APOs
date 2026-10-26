# AAO instrument identity: daily snapshot joins versus DBN symbology — 2026-10-25

## Verified local observations

The author's two-month `wti_aao_mapping_comparison` output tested three
daily-definition matching conventions and reported the following **final
settlement event** counts:

| Diagnostic | 2021-02 | 2026-06 |
|---|---:|---:|
| Final settlement events | **55,326** | **118,094** |
| CME reference-day definition match | 264 | 653 |
| Publication UTC-day definition match | 30,496 | 46,673 |
| Preceding-publication UTC-day definition match | 12 | 22,162 |
| At least one daily convention matched | **30,508 (55.1%)** | **68,835 (58.3%)** |
| Not matched by any three conventions | **24,818 (44.9%)** | **49,259 (41.7%)** |
| Conflicting contract fingerprints *among matching alternatives* | 0 | 0 |
| Publication and CME `ts_ref` day differ | 55,074 | 46,430 |

**None of these counts is a deduplicated option price panel or an independent
backtesting sample.** Matching a daily definition on a particular UTC date
can fail because CME `ts_ref` is a trading session date, whereas
`ts_event` records when the statistics publish. Databento's
[instrument-definition documentation](https://databento.com/docs/schemas/instrument-definitions)
explains its point-in-time definitions and daily snapshots (at UTC midnight
Monday–Friday under the stated feed conditions); its
[CME feed guide](https://databento.com/docs/knowledge-base/datasets/glbx-mdp3)
distinguishes settlement reference dates from publishing times.

Furthermore, **instrument IDs are only guaranteed unique within one day**,
and some instrument symbols can be reused. Databento documents both facts in
[common fields](https://databento.com/docs/conventions/common-fields-enums-types)
and [symbology](https://databento.com/docs/conventions/symbology).
Thus, simply allowing an arbitrary earlier definition, or taking the union
of date-shifted mappings, would introduce lookahead/incorrect contracts.
Zero observed conflicts among *matched* alternatives does **not** mean
unmatched cases can be safely filled.

## New next experiment: audit embedded DBN mapped symbols (offline)

Databento's [`DBNStore.to_df` API](https://databento.com/docs/api-reference-historical/helpers/dbn-store-to-df)
defaults to `map_symbols=True`, which can use embedded symbology metadata to
map numeric record IDs to their publisher-native symbols. The statistics
DataFrames from the author's earlier probes already list a `symbol` column.
This is an important **alternative hypothesis**: the source DBN symbology
mapping may recover candidate contract identities even when the exact
definition snapshot UTC-day matching misses that event.

The new `experiments/wti_aao_symbol_mapping.py` tests this without making
requests to Databento. It reads one month of the saved `definition` and
`statistics` DBNs with `map_symbols=True`. Its report measures:

- fraction of final settlements with a mapped, nonblank native `symbol`;
- within-month coverage against `definition.raw_symbol`, also requiring
  the matching Databento `publisher_id`;
- truly unambiguous `AAO` single-leg `C`/`P` identity matches using
  strike, expiry, class, underlying and exchange;
- symbols with conflicting contract fingerprints and strategy-only symbols;
- tentative unique publisher+symbol+`ts_ref` pairs, before any correction
  or publication-time handling.

Only **aggregate numbers** are printed and written locally; raw symbols,
options, strikes, prices and licensed records are never emitted. The
`symbol` field cannot be assumed valid in all DBN files, and a mapped
symbol is not yet a verified multiyear stable contract key or a clean final
settlement price. Correct for the same-symbol temporal reuse and
definition revisions before constructing prices.

### Run on author's Windows VM

```powershell
git switch main
git pull --ff-only origin main
conda activate asian-options
python -m pytest tests/test_wti_aao_symbol_mapping.py -q
python -m experiments.wti_aao_symbol_mapping --months 2021-02 2026-06
```

Reports go to
`results/analysis/wti_aao_history_feasibility/symbol_mapping/`.

**Decision after results:** If embedded symbol mapping has high validated
identity coverage and relatively few conflicts, build a tested
revision-aware, stable `publisher + symbol + class + expiry + strike +
underlying` contract master, checking exchange/strike scale, timestamp and
final `statistics.update_action`. Then deduplicate final settlement prices
per stable contract/CME reference day; preserve theoretical/actual and
liquidity distinctions; independently reconcile overlapping Barchart
settlements and contract/fixing conventions. If coverage is poor, determine
whether it is a missing in-file mapping or cross-month definition availability
problem before considering other solutions.

No new purchase, model-price experiment, updated inference or JCM paper
performance claim is justified by this diagnostic alone. The actual
81-month inventory contains **1,701 distinct final CME reference dates**,
not 1,701 valid strict-forward test dates.
