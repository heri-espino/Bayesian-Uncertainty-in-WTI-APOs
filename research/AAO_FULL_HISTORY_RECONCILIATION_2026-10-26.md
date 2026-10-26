# AAO cross-month reconciliation: 81-month observed results (2026-10-26)

The author ran the four-month smoke test and the full local
`experiments.wti_aao_cross_month --all` with no API requests. These are
**provisional settlement candidate** counts, not trading prices or
independent pricing observations.

| Measure | Four months | All 81 months |
|---|---:|---:|
| Settlement events | 711,542 | 13,412,045 |
| Distinct tentative symbol/reference-date keys | 276,325 | 5,157,894 |
| Keys appearing in multiple source months | 0 | 71,145 |
| Latest preliminary keys | 2,636 | 52,290 |
| Latest invalid-price keys | 0 | 1 |
| Selected final nonintraday candidates | **273,689** | **5,105,603** |
| Actual-flagged | 156,945 | 3,299,087 |
| Theoretical-flagged | 116,744 | 1,806,516 |
| Reference dates with candidates | 85 | **1,700** |
| Registry publisher/symbol identities | 15,090 | 38,926 |
| Conflicting historical contract fingerprints | 0 | 0 |
| Registry groups not safe as outright | 20 | 296 |
| Latest update's source month differs from reference month | 300 | 190,064 |

There were **zero** latest deletions, intraday final marks and tied
ambiguous updates in the reported results. All settlement events had
a safe global symbol mapping. The selected count equals
5,157,894 - 52,290 - 1 = **5,105,603**.

**Important distinctions:** The 71,145 cross-file keys and the
190,064 source/reference-month differences measure different things.
Neither count alone identifies corrections. The 296 unsafe registry
groups need not contribute any settlement events. The **1,700**
selected reference dates differ from the raw-inventory **1,701**
final-event reference dates by one day. The reason remains unknown.

## Next offline diagnostic

`experiments/wti_aao_panel_quality.py` audits the existing local
SQLite settlement state. It summarizes candidate counts by year,
actual versus theoretical flags, zero-price share, coarse price-size
bins, and **date-only** overlap with the existing Barchart APO files.
It never publishes symbol-level or price-level records.

```powershell
git switch main
git pull --ff-only origin main
conda activate asian-options
python -m pytest tests/test_wti_aao_panel_quality.py -q

# Reads the existing private SQLite database and local Barchart files
python -m experiments.wti_aao_panel_quality

# Heavier: reads all 81 raw statistics DBNs to find the missing date
python -m experiments.wti_aao_panel_quality --scan-final-dates
```

The aggregate report is saved locally at
`results/analysis/wti_aao_history_feasibility/quality/cross_month_quality.json`.
No vendor purchase or network call is needed. The price-bearing
SQLite file stays locally gitignored.

## Research release gates

1. Validate USD/barrel price and strike scale, contract multiplier,
   actual option expiry and market settlement definition.
2. Match **specific options** (same valuation date, expiry,
   strike and call/put) to committed Barchart `Latest` marks;
   date-only overlaps are not such matches.
3. Account for revisions published after the CME reference date.
   Retrospective final marks cannot be used as earlier market
   calibration information.
4. Establish eligible forward dates with correct CL fixing calendar,
   contemporaneous futures term structure, rates, and strictly
   lagged APO/LO volatility estimates.
5. Run held-out Bayesian PI/PM and historical/IV comparisons with
   date-block uncertainty; then regenerate performance figures and
   revise the Elsevier CAS manuscript.

The manuscript's existing numerical results remain unchanged.
