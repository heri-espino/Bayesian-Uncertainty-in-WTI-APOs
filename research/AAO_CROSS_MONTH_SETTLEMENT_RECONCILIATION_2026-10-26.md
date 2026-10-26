# AAO cross-month settlement reconciliation — 26 October 2026

## Source evidence already observed on the author's VM

The native DBN symbol lookup matched all final settlement events to
unambiguous AAO outright call/put definitions in February 2021 and
June 2026. The latest **correction-aware, within-file-month** candidate run:

| Diagnostic | 2021-02 | 2026-06 |
|---|---:|---:|
| Settlement events | 127,958 | 248,275 |
| Last-update publisher/native-symbol/`ts_ref` keys | 48,831 | 101,587 |
| Latest key is nonfinal | 101 | 190 |
| Latest key deleted / intraday / invalid price / tied conflict | 0 | 0 |
| **Selected final nonintraday candidates** | **48,730** | **101,397** |
| Selected actual-flagged | 31,414 | 43,067 |
| Selected theoretical-flagged | 17,316 | 58,330 |
| Distinct reference dates with candidates | 19 | 23 |
| Earlier settlement events collapsed into latest monthly keys | 79,127 | 146,688 |

The last-update counts and final candidates are exactly consistent with
the earlier native-symbol probe's 48,730 and 101,397 tentative keys.
They are **not** yet final cross-month price observations or available
held-out valuation dates. The end-of-archive date is 2026-10-01
(exclusive); revisions released afterward cannot be detected by these
files.

## New implemented two-pass reconciler (offline)

`bayesian_asian_options.aao_cross_month` and
`experiments/wti_aao_cross_month.py` replace the provisional
within-month-only analysis with **all-source-month** reconciliation.

- **Pass 1: contract registry.** Read locally downloaded monthly
  `definition` files and require that each publisher+native raw symbol
  has one consistent AAO C/P outright fingerprint across the selected
  months (class, expiry, strike, underlying, exchange). Reject global
  collisions/symbol reuse or non-outright identities; do **not** interpret
  a temporary instrument ID as a stable cross-month key.
- **Pass 2: settlement action chronology.** Read monthly `statistics`
  files with embedded native symbol mapping and appropriately scaled
  prices (`DBNStore.to_df(price_type="float", map_symbols=True)`).
  Include **all** settlement add, delete, preliminary and final
  updates. First reduce each source month to its newest action for
  publisher+symbol+CME reference day. Merge these across months
  ordered by publication `ts_event` and venue sequence.
  A later delete or preliminary entry supersedes an earlier final
  candidate; rank-tied contradictory updates are quarantined.
- The **latest nondeleted, final, nonintraday, finite, nonnegative**
  candidates are reported by actual/theoretical flag and distinct
  reference day. A count of keys seen in more than one source month
  quantifies where a monthly-only panel might misstate final state.
- **Privacy:** all SQL state (including local licensed prices/symbols)
  is stored only in the gitignored
  `data/databento/wti_aao_bulk/derived_private/` tree. The main JSON
  report contains aggregated counts and no contract-level prices.
  No vendor API calls or paid orders are made.

This is still a **provisional** settlement panel: verify source
price units and tick conventions, exchange contract specs, final
correction availability, cross-vendor overlap, and settlement
theoretical/actual mix before running financial model tests.
CME `ts_ref` is the *reference trading date*, which can differ
from dissemination time. The API source also documents final, actual
and intraday bit flags. References:
[Databento statistics](https://databento.com/docs/schemas/statistics),
[CME GLBX.MDP3 guide](https://databento.com/docs/knowledge-base/datasets/glbx-mdp3),
[DBNStore conversion](https://databento.com/docs/api-historical/helpers/dbn-store-to-df?lang=python).

## Run locally, small smoke test first

```powershell
git switch main
git pull --ff-only origin main
conda activate asian-options

python -m pytest tests/test_aao_cross_month.py -q

# Four representative source months: two neighboring pairs
python -m experiments.wti_aao_cross_month --months 2021-02 2021-03 2026-06 2026-07
```

Only if the test/outputs pass and enough local free disk remains:

```powershell
# Reads 81 definition files, then 81 statistics files; PRIVATE local state.
python -m experiments.wti_aao_cross_month --all
```

Full output:
`results/analysis/wti_aao_history_feasibility/cross_month/cross_month_audit_81_months.json`.
Proprietary SQLite state:
`data/databento/wti_aao_bulk/derived_private/aao_cross_month_PROVISIONAL_81_months.sqlite3`.
Do not `git add -f` the latter or copy the vendor data into public issues,
PRs, assistants, PDFs, or shared reports. Neither execution requires
another Databento query.

## Next research gates

1. Inspect cross-month symbol conflicts, unseen corrections, invalid
   marks, missing contracts and number of distinct final settlement
   reference dates. Sample a few private rows locally to check
   Databento `price_type="float"` scale, strike display convention and
   CME units with documented source fields and Barchart overlap.
2. Validate that contract identities remain stable, that late
   corrections are applied to `ts_ref`, and that no future corrections
   are inadvertently used at earlier information cutoffs. Separate
   *latest reconstructed final settlement* targets from
   *point-in-time available* volatility inputs.
3. Implement rate/WTI CL first-nearby/fixing/calendar and
   strictly-prior APO/LO implied-volatility joins on the verified
   cross-vendor overlap. Measure eligible **test dates**, not merely
   settlement statistic rows.
4. Freeze chronological holdouts, compare Bayesian PI/PM and
   historical/IV baselines on common support with date-block inference,
   update genuine model-performance figures, and revise the provisional
   Elsevier CAS JCM manuscript **only after** reproducible runs.

JCM remains a conditional proposed submission target, with REMEF
and Wiley/JFM manuscript sources preserved. Existing validated
paper numbers remain unchanged.
