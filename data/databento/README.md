# Databento WTI external-Q inputs

This directory is reserved for the independent vanilla-WTI option experiment in Issue #36.

Raw Databento market data are **local inputs only** and must not be committed. The acquisition
driver stores them under `data/databento/wti_external_q/raw/`, which is gitignored. Versioned
artifacts should be limited to code, query metadata, hashes, diagnostics, and derived summaries
whose redistribution is permitted.

The acquisition workflow is deliberately cost-capped:

```powershell
$env:DATABENTO_API_KEY = "<your local key>"
python -m experiments.wti_databento_external_q --mode quote
python -m experiments.wti_databento_external_q --mode discover
python -m experiments.wti_databento_external_q --mode download
```

The default request targets CME Globex `GLBX.MDP3`, standard WTI monthly options
`LO.OPT`, underlyings `CLX6` and `CLZ6`, strikes 85.0--94.5, and the strict-forward
window 2026-08-24 through 2026-09-10. The end date passed to Databento is 2026-09-11
because API ranges are end-exclusive.

The default hard cap is **USD 5.00**. `quote` is metadata-only. `discover` may purchase
only the one-day option-definition snapshot after checking its quote, then stops after
quoting the exact statistics request. `download` fetches the selected statistics only
when the estimated additional cost remains below the cap.

Do not use `--force` casually: repeated streaming requests can be billed again.
