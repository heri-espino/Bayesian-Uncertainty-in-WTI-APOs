# U.S. Treasury daily par-yield files

Place official **Daily Treasury Par Yield Curve Rates** CSV files in this directory. The empirical driver discovers every `*.csv` file here and selects the latest curve available on or before each valuation date.

The user-provided working files currently cover 2024, 2025, and 2026. They are source data rather than generated results and are kept local by default; the runner can also download a missing valuation year from the official Treasury CSV endpoint:

```bash
python -m scripts.run_university_wti_apo --quick
```

The current pilot uses a clearly labeled approximation: maturity-interpolate the Treasury **par yield** and treat it as a continuously compounded zero-rate proxy. This is not described as a bootstrapped zero curve. A later robustness specification should use a proper zero/OIS curve without changing the rest of the pricing pipeline.
