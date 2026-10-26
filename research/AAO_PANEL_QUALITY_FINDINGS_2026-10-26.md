# AAO full-history settlement quality — VM results, 26 October 2026

## Follow-up: latest status and GitHub source verification (2026-10-26)

**The missing reference date is explained at the latest-key status level.**
On `2024-01-26`, the user's read-only `--explain-date` query found
**7,868** latest publisher+symbol+reference-day keys, **all 7,868
preliminary**, and **zero** deleted, intraday, invalid, conflicting
or selected final keys. The earlier raw DBN scan had detected **two
final settlement statistic events** that day. These are consistent
with final messages being superseded by later nonfinal latest states;
however the aggregate output does not prove the precise update
sequence of those two event records. Thus **1,700** reference dates
in the selected provisional panel versus **1,701** dates containing
at least one original final event is a known consequence of the
latest-update selection rule, **not a missing Databento file**. Preserve
this difference as a data-quality and vintage-selection result; do
not force preliminary marks into a final-price sample.

**Barchart source files exist on GitHub `main`:** a live repository
lookup confirmed `data/csv/sep2026/jaou6_10000c_price-history-09-12-2026.csv`
and additional `jao*.csv` histories in `data/csv/sep2026` and
other expiry folders. The user's Windows VM reports
`Test-Path ...jaou6_10000c... = False`, and
`root_exists: false` for `data/csv`. Its
`git ls-files 'data/csv/*' | Select-Object -First 10` output
listed **CL contracts** only; because of `-First 10`, it does not
establish whether the JAOs are tracked in that local commit.
Check current `main`, sparse checkout, tracked missing paths and
local status before recovering anything. **Do not use `git reset
--hard`, `git clean` or any blanket restore that might overwrite
local work.**

~~~powershell
git switch main
git pull --ff-only origin main
git status --short -- data/csv
git ls-files --error-unmatch -- 'data/csv/sep2026/jaou6_10000c_price-history-09-12-2026.csv'
git sparse-checkout list
git ls-files -v -- 'data/csv/sep2026/jaou6_10000c_price-history-09-12-2026.csv'
~~~

If sparse checkout is enabled and omits these files, extend it
without resetting local changes:

~~~powershell
git sparse-checkout add data/csv
~~~

If sparse checkout is **disabled** and the file is tracked on local
`HEAD` but absent in the worktree, first confirm that this path
has no **wanted** local edits, then restore just that file:

~~~powershell
git restore --source=HEAD --worktree -- 'data/csv/sep2026/jaou6_10000c_price-history-09-12-2026.csv'
~~~

Other Barchart folders must also exist before calling
`python -m experiments.wti_aao_panel_quality` with the default
root. Do not restore entire folders until local changes are checked;
the root cause may alternatively be a stale or partial checkout.
For Barchart CSVs stored elsewhere use the already-supported
`--barchart-root`. This audit establishes file availability
and **date-only** overlap, not matching identical contracts, settlement
units or causal IV calibration.

---


## Completed offline data-quality scan

The author executed
`python -m experiments.wti_aao_panel_quality --scan-final-dates`
and shared the aggregate output. The query read the private SQLite
and all 81 existing raw DBN statistics files; **no vendor API request**.

- **5,105,603** provisional final nonintraday
  publisher/native-symbol/`ts_ref` candidates remain after
  cross-month update reconciliation.
- **1,700** distinct final-candidate reference dates, compared with
  **1,701** reference dates with at least one raw final settlement event.
- **The sole lost reference date is 2024-01-26**, containing just
  **two raw final settlement events**. This does **not** yet prove why
  no candidate survived. Query the latest private SQLite status for
  that date before assigning a cause.
- The candidate date set includes **2019-12-31** (4,706 candidate
  keys) even though the retrieved source-file windows start
  **2020-01-01**. A historical CME settlement reference date
  can precede its publication/file month. The 1,700 selected
  dates include this pre-2020 date: **1,699 selected reference
  dates fall in 2020 or later**. These are **not** 1,699
  leakage-free, strictly forward-test dates.
- Private SQLite selected price-level scaling is **not verified**
  against CME units or Barchart. The script produced coarse
  price-magnitude bins, not a matched quote comparison.

### Selected provisional marks by reference year

| Year | Candidate marks | Distinct days | Actual-flagged | Theoretical-flagged | Zero-price marks |
|---|---:|---:|---:|---:|---:|
| 2019 (one day) | 4,706 | 1 | 4,614 | 92 | 92 |
| 2020 | 951,147 | 251 | 805,424 | 145,723 | 3,218 |
| 2021 | 678,637 | 253 | 439,655 | 238,982 | 3,316 |
| 2022 | 754,632 | 252 | 448,070 | 306,562 | 2,845 |
| 2023 | 689,570 | 251 | 412,639 | 276,931 | 582 |
| 2024 | 690,312 | 251 | 394,737 | 295,575 | 556 |
| 2025 | 707,400 | 252 | 418,150 | 289,250 | 1,666 |
| 2026 through September | 629,199 | 189 | 375,798 | 253,401 | 2,377 |
| **Total** | **5,105,603** | **1,700** | **3,299,087** | **1,806,516** | **14,652** |

A zero-price theoretical mark is not automatically wrong; investigate
quote definitions, unit conversion, deep-OTM contracts, and market
microstructure before filtering. Actual-flagged settlement types are
not independently observed transactions.

## Barchart local discovery is an environmental blocker

The author's report returned
`"barchart_date_only_overlap": {"available": false}`.

**This is not zero overlap.** The existing
`bayesian_asian_options.barchart_apo.discover_barchart_histories`
did not find a matching Barchart file under the VM's expected
`data/csv` directory. The GitHub repository's `main`
**does contain** `data/csv/sep2026/jaou6_10000c_price-history-09-12-2026.csv`
and other Barchart option CSVs. This therefore requires checking
the VM's file paths, checkout and sparse-checkout configuration.
Avoid starting pricing experiments against a silently absent source.

## New targeted diagnostics

After pulling the follow-up code, run:

```powershell
git switch main
git pull --ff-only origin main
conda activate asian-options
python -m pytest tests/test_wti_aao_panel_quality.py -q

# No DBN re-scan: inspect the latest private status of the missing day
python -m experiments.wti_aao_panel_quality --explain-date 2024-01-26

# Check local checkout of Barchart sources; do not assume empty dataset
Test-Path .\data\csv\sep2026\jaou6_10000c_price-history-09-12-2026.csv
git ls-files 'data/csv/*' | Select-Object -First 10
Get-ChildItem .\data\csv -Recurse -File -Filter 'jao*.csv' |
    Select-Object -First 10 FullName

# If the canonical directory is not where the CSVs are:
python -m experiments.wti_aao_panel_quality --barchart-root 'C:\your\local\Barchart\folder'
```

Do **not** pass `--scan-final-dates` again merely to identify the
missing date: it is already known to be `2024-01-26`. The
`--explain-date` query reports the newest candidate statuses
(preliminary, invalid, deleted, tied, selected) for that date using
the existing private database. It does not publish licensed price rows.

The Barchart CLI now describes why discovery fails (missing directory
versus existing CSVs with unexpected filenames) and supports a local
`--barchart-root` override. Merely recovering date overlap is
**not** instrument-specific price parity; settlement values still
need matching contract expiry, option side, strike and time reference.

## Publication gate

1. Investigate the two lost-date raw final events versus their
   newest private SQLite statuses; do not assume data is missing.
2. Confirm which Barchart option-history files are available locally.
3. Resolve Databento strike/settlement price scale, expiry/class
   identity and vendor alignment on overlapping contract/reference dates.
4. Construct dated CL term-structure/fixings, rates and strictly
   lagged risk-neutral volatility features. Count independently
   eligible forecast dates, not event rows.
5. Run chronological holdout PI/PM, historical-volatility and implied
   volatility benchmarks with block uncertainty. Only then update
   market-performance figures and the provisional Elsevier CAS paper.

Journal of Commodity Markets remains a conditional working target,
with REMEF and earlier Wiley/JFM manuscript sources preserved.
