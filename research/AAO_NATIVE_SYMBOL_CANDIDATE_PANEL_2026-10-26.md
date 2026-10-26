# AAO native symbol mapping solved; correction-aware contract-day candidate stage

## New author-run identity evidence (2026-10-26)

The author's `python -m experiments.wti_aao_symbol_mapping --months 2021-02 2026-06` returned complete native DBN mapping for **both sampled months**:

| Diagnostic | Feb 2021 | Jun 2026 |
|---|---:|---:|
| Final settlement events | **55,326** | **118,094** |
| Final events with nonempty `statistics.symbol` | **55,326 (100%)** | **118,094 (100%)** |
| Final events matched to `definition.raw_symbol` with same publisher | **55,326 (100%)** | **118,094 (100%)** |
| Matched to unambiguous outright AAO call/put fingerprint | **55,326 (100%)** | **118,094 (100%)** |
| Symbol groups with multiple fingerprints within sampled month | **0** | **0** |
| Tentative publisher+symbol+reference-day keys | **48,730** | **101,397** |
| Distinct final reference dates | 19 | 23 |
| Final actual-flagged events | 37,998 | 53,377 |
| Final theoretical-flagged events | 17,328 | 64,717 |

This **resolves the immediate same-month contract-identity lookup problem**.
The earlier 55.1%/58.3% calendar-snapshot match rates were artifacts of
trying to align daily numeric IDs and snapshots with UTC publication dates.
Databento embeds mapping intervals and native symbols in the DBN files:
[official symbology documentation](https://databento.com/docs/conventions/symbology).

**Not yet established:** Stable identity through different file months;
symbol reuse across dates; corrections/deletions and preliminary versus final
settlement state; cross-month late publication; currency/tick/value scaling;
overlap with Barchart prices; sufficiently supported forward test dates. The
1,701 historical final-reference dates still do **not** mean 1,701 eligible
out-of-sample pricing dates.

## Implemented offline next stage

`experiments/wti_aao_contract_day_candidates.py` consumes already downloaded
monthly DBNs with native mapped symbols and produces **conservative within-file-
month candidate rows**. It compares the full outright call/put fingerprint,
rejects ambiguous symbols, groups statistics by publisher+native symbol+CME
`ts_ref` reference date, and applies update chronology:

- `stat_type=3` is the settlement statistic.
- `update_action=1` adds; `2` deletes. The **last reported action** for
  that key governs, not the last *final-only* action.
- `stat_flags & 1` is final, `stat_flags & 2` is actual (not theoretical),
  `stat_flags & 8` means intraday. Select the latest **final**, active,
  non-intraday, nonnegative finite-priced candidate within that file month.
- Equal-rank conflicting updates or inconsistent symbol definitions are
  rejected, not resolved by arbitrary CSV order.
- Source DBNs are never modified, printed or transmitted. Price-level
  candidate output is optional and PRIVATE, protected by `.gitignore`.

These choices follow the official [statistics schema](https://databento.com/docs/schemas/statistics)
and [CME dataset guide](https://databento.com/docs/datasets/glbx-mdp3).
**Important:** This is a per-file-month staging candidate, not a validated
unique contract/reference-day dataset, because the *same CME reference day*
may have later updates published in another source month.

## Run on the VM — first only two representative months

```powershell
git switch main
git pull --ff-only origin main
conda activate asian-options

python -m pytest tests/test_wti_aao_contract_day_candidates.py -q
python -m experiments.wti_aao_contract_day_candidates --months 2021-02 2026-06
```

This prints only aggregate counts and saves report JSON under
`results/analysis/wti_aao_history_feasibility/contract_day_candidates/`.
If the results pass basic face-value checks, the following remains local
and should be run only after deciding on available disk capacity:

```powershell
# Explicitly opt in to local row-level licensed data; NEVER git-add this folder.
python -m experiments.wti_aao_contract_day_candidates --months 2021-02 2026-06 --export-private
# Later, once sample and performance are validated:
python -m experiments.wti_aao_contract_day_candidates --all --export-private
```

Candidate CSV.gz files are written to
`data/databento/wti_aao_bulk/derived_private/` and contain native
symbols and candidate option settlement values. They must not be
committed or shared with agents via public GitHub issues. Public-eligible
outputs should be limited to permissible aggregates and code.

## Scientific gates before any new paper figure

1. Verify the candidate counts and deletion/amendment/intraday distribution.
2. Build a separate **cross-month identity and final-update reconciler**.
   A symbol's month-level fingerprint must match across all overlapping
   months, or the shared-key candidate is quarantined. A deletion published
   the next month for the previous reference day must supersede the prior
   candidate. Use original source event records for this, not only already-
   filtered candidate rows.
3. Audit price scale, option contract specs, expiry, positive-OI/volume
   alignment, source publish timestamps, degraded-data warnings and matching
   Barchart settlements. Do not call model-generated theoretical settlement
   marks traded prices.
4. Construct dated CL/first-nearby/discount/earlier-IV eligible-market
   sample, freeze chronological holdout windows and run existing PI/PM
   Bayesian and historical/IV model comparisons on common rows.
5. Regenerate the **economic performance figures** and the provisional
   Elsevier CAS manuscript only from verified expanded-data analysis.

No further Databento purchase is required. The current JCM target remains
conditional; REMEF and JFM manuscripts remain preserved.
