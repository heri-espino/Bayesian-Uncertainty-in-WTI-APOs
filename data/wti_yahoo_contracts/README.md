# Local Yahoo CL contract cache

This directory is the default cache for individual NYMEX WTI futures histories downloaded by `bayesian_asian_options.wti_yahoo_futures`.

Generated files such as `CLV26.csv` and `CLV26.json` are gitignored. The CSV stores normalized daily Yahoo Finance OHLCV history; the JSON stores source metadata, SHA-256, and the Yahoo futures settlement/expiration date when available.

Yahoo `Close` is treated as an end-of-day **settlement proxy**. It is not renamed an official CME settlement. Publication runs should retain source-validation reports against permitted CME/Barchart reference observations.

Recreate the cache with:

```bash
python -m scripts.run_university_wti_apo --quick
```

Use `--refresh-futures` only when a fresh Yahoo snapshot is intentionally required.
