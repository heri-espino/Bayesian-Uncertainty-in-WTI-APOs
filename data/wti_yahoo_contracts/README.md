# Yahoo WTI individual-contract cache

This directory is retained for optional Yahoo individual-contract validation experiments. It is **not required** by the canonical WTI APO pilot.

A live workstation test showed that Yahoo may return 404 / `YFTzMissingError` for older delisted symbols such as `CLG24.NYM`. The canonical valuation-date CL curve now comes from the committed Barchart `Daily Prices` files under `data/csv/CL`.

The current source split is:

- Yahoo `CL=F` under `data/wti_yahoo/`: physical-measure historical-return proxy;
- Barchart `data/csv/CL/*.csv`: contract-specific valuation-date CL curve and first-nearby fixing contracts;
- this directory: optional Yahoo individual-contract cross-checks only.

If an individual Yahoo contract is downloaded for validation, Yahoo daily `Close` remains a settlement proxy until compared with CME/Barchart observations. Generated CSV/JSON cache files in this directory remain gitignored.
