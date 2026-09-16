# Yahoo WTI individual-contract cache

This directory is the local cache for contract-specific NYMEX WTI futures histories downloaded through `yfinance`, using symbols such as `CLV26.NYM`, `CLX26.NYM`, and `CLZ26.NYM`.

The current empirical pilot uses these individual contracts only where the actual APO mechanics require them: the valuation-date futures curve and the first-nearby contracts associated with the averaging-month fixing dates. A live workstation test showed that Yahoo may return 404 / `YFTzMissingError` for older delisted symbols such as `CLG24.NYM`; therefore the project must not assume that a complete historical strip of individual Yahoo contracts is available indefinitely.

Physical-measure volatility inference in the current pilot uses the separate Yahoo `CL=F` continuous/front-month proxy under `data/wti_yahoo/`. That series is explicitly labelled a proxy because Yahoo does not document its historical roll convention precisely enough to call it a reconstructed contractual first-nearby series.

Yahoo daily `Close` for individual contracts remains a settlement proxy until cross-validated against CME/Barchart observations. CSV and JSON cache files in this directory are gitignored; source code, hashes, manifests, diagnostics, and permitted derived summaries remain versioned.

Recreate the cache with:

```bash
python -m scripts.run_university_wti_apo --quick
```

Use `--refresh-futures` only when a fresh Yahoo snapshot is intentionally required.
