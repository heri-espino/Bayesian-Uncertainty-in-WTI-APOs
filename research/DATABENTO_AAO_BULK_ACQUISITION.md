# Budgeted WTI APO (AAO) historical-data acquisition

**Scope:** GLBX.MDP3, parent `AAO.OPT`, `definition` + `statistics` only.
**Budget:** Author permits up to **USD 40 of Databento credits** (reported balance USD 120).
**Safety rule:** Price **all eligible monthly chunks first**, then require an
explicit download command. The code limits *total quoted amount* to **USD 32**
(80% of the authorized USD 40). This is a safety margin, not a guaranteed
provider-side billing limit: actual charges depend on transferred bytes.

## Why we are doing this

The manuscript's narrowest limitation is its **15 distinct forward-test APO
valuation dates**, not just its 2,381 option-level comparisons. Four separate
2023–2026 dates returned positive metadata counts for `AAO.OPT`, while
`symbology.resolve` returned empty mapping lists even for the known working
`LO.OPT` control. These counts indicate promising coverage, but **do not yet
verify that the payload consists of the target product, final settlements,
traded prices, or suitable eligible dates**.

This workflow broadens coverage back to 2020 as an initial target, and can be
extended earlier if actual metadata prices, contracts, and quality support it.

## Manual Windows / PowerShell procedure

Use the already-created Conda environment and the private API key set in
the user's PowerShell session. **Never paste the key in an issue or commit it.**

```powershell
git switch main
git pull --ff-only
git switch feature/aao-bulk-budgeted-history-20261023

conda activate asian-options
python -m pytest tests/test_wti_databento_aao_bulk.py -q

# FREE QUOTE ONLY — first check broad history, costs, and metadata coverage.
python -m experiments.wti_databento_aao_bulk --mode quote --start 2020-01-01 --end 2026-10-01 --max-budget-usd 40

# Inspect the plan before allowing any charge:
$plan = Get-Content "results/analysis/wti_aao_history_feasibility/bulk/bulk_quote_plan.json" -Raw | ConvertFrom-Json
$plan | Select-Object start,end,eligible_months,total_months,eligible_quote_usd,safety_ceiling_usd
$plan.requests | Where-Object { $_.status -eq 'error' } |
    Select-Object schema,start,end,error
```

Only if the plan has an acceptable price and useful quoted coverage, run this
**billable manual command**:

```powershell
python -m experiments.wti_databento_aao_bulk --mode download --start 2020-01-01 --end 2026-10-01 --max-budget-usd 40 --confirm-budget-usd 40
```

The downloader refuses a request whose cumulative metadata quotes exceed USD
32. If exceeded, **shorten the date range and re-quote** (e.g. start in 2023).
Do not raise the budget beyond USD 40. The price estimate is **not** an exact
billing guarantee; check the Databento billing/credits page while downloading.

## Output and reproducibility

- Local proprietary source files: `data/databento/wti_aao_bulk/raw/aao_<schema>__<start>__<end>.dbn.zst`. These are gitignored.
- Full monthly metadata plan:
  `results/analysis/wti_aao_history_feasibility/bulk/bulk_quote_plan.json`.
- Persistent acquisition ledger:
  `results/analysis/wti_aao_history_feasibility/bulk/bulk_acquisition_manifest.json`.
  Each completed chunk includes source query, quoted amount, raw DBN SHA256,
  file size and estimated record count.
- Files are compressed DBN rather than giant in-memory DataFrames. Existing
  SHA-matched completed files are not re-downloaded. Unknown or partially
  downloaded files halt execution for manual recovery.

**No heavy download is triggered by GitHub Actions**, commits, or metadata
quotes. No manuscript numerical claims are changed by this PR.

## Critical research validation before expanding LO/CL downloads

Inspect the raw definitions and statistics to verify: option family/contract
specifications, calls vs puts, strikes, expiries, delivery underlyings, trading
reference date `ts_ref`, settlement `stat_type=3`, final vs preliminary
`stat_flags`, actual vs theoretical settlements, volume `stat_type=6`,
open interest `stat_type=9`, and overlap with existing Barchart APO marks.

**Do not equate thousands of quote records with independent observations**.
Only after the AAO feed is confirmed should we expand LO volatility data,
CL futures fixing inputs, then create the extended strict-forward panel with
date-cluster/serial-dependence inference.

Databento docs: https://databento.com/docs/api-historical/timeseries/timeseries-get-range?lang=python
and https://databento.com/docs/faqs/usage-pricing-and-data-credits .


## After acquisition: audit the 160 local DBN files

The user-side download report completed 160 chunks from 80 of 81 months in
2020-01 through 2026-09, with total **quoted** USD 17.33487324. The amount
actually charged should be checked in Databento billing. Several daily data
conditions were flagged degraded. The missing month must be read from
`bulk_quote_plan.json`, not guessed.

First run a small **strictly offline** inventory:

```powershell
git pull --ff-only origin feature/aao-bulk-budgeted-history-20261023
conda activate asian-options
python -m pytest tests/test_wti_databento_aao_inventory.py -q
python -m experiments.wti_databento_aao_inventory --months 2023-06 2025-06 2026-06
```

The inventory reads only downloaded `.dbn.zst` files and never uses
`db.Historical()`, `get_range`, or any paid service. Output:
`results/analysis/wti_aao_history_feasibility/inventory/aao_inventory_summary.json`.

If sample identity and fields are correct, audit all downloaded months:

```powershell
python -m experiments.wti_databento_aao_inventory --all
```

The report summarizes definition asset, instrument class, expiry, raw-symbol
count and settlement `stat_type=3`; final flag bit 0, actual flag bit 1;
trading reference dates via `ts_ref`; and volume/open-interest event counts.
The flags follow Databento's CME Globex conventions:
https://databento.com/docs/knowledge-base/datasets/glbx-mdp3 .

**Scope limits:** these are event/reference-date counts only. They do NOT
establish executable transactions, active markets, unique contract IDs across
rollovers, independent forward-validation dates, correct fixing schedules or
the accuracy of derived option prices. No licensed raw market data should be
committed; report only permissible derived aggregate summaries.

Before final scientific conclusions, verify the instrument identities and
`ts_ref` dates against overlapping Barchart data, identify degraded dates,
deduplicate preliminary/final updates by trading date and contract, and
implement a strict earlier-date volatility calibration.
