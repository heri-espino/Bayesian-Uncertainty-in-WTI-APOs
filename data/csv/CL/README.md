# Barchart CL futures histories

This directory contains the author-supplied Barchart `Daily Prices` CSVs for the individual NYMEX WTI (CL) contracts needed by the observed APO maturities.

The 14 contract files are:

```text
CLV26  CLX26  CLZ26  CLF27
CLJ27  CLK27  CLV27  CLX27
CLJ28  CLK28  CLV28  CLX28
CLN29  CLQ29
```

They cover the two first-nearby delivery contracts required during each APO averaging month already present in the empirical option dataset.

The source schema is:

```text
Time, Open, High, Low, Latest, Change, %Change, Volume, Open Int
```

`Latest` is retained as the Barchart source field. In the histories used by this project it is the CME settlement field; it is not interpreted as an intraday last trade.

The Barchart UI was queried with a two-year history setting, but the downloaded CSVs contain only the observations Barchart actually returned for each listed contract. Several longer-dated contracts currently have only roughly August--September 2026 observations. The source manifest records each file's first/last date and row count. Therefore these files are sufficient for the 2026-09-04 pilot and nearby valuation dates, but they do not by themselves reconstruct the entire 2025--2026 historical futures curve panel.

`contract_expiries.csv` is a versioned study reference table with the CL last-trade dates required by the first-nearby fixing map. Pricing code reads that table explicitly rather than applying a hidden roll rule.

The canonical loader is:

```python
from bayesian_asian_options.barchart_cl import load_barchart_cl_strip

panel, manifest = load_barchart_cl_strip(
    "data/csv/CL",
    contracts=["CLX26", "CLZ26"],
)
```

The October-2026 pilot valued on 2026-09-04 uses `CLX26` and `CLZ26` for its future first-nearby fixings. The original historical-volatility baseline uses Yahoo `CL=F`; Issue #38 provides a separate official-settlement first-nearby reconstruction for robustness rather than trying to extend these short committed Barchart files backward.

Before making the repository or raw files public, verify Barchart redistribution/licensing terms. The scientific code, hashes, schemas, manifests and derived results should remain reproducible even if raw source files later need to be distributed separately.
