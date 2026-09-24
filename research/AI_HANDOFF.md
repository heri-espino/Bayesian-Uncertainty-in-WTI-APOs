# AI handoff

Read this file before continuing research work.

## Canonical current checkpoint

The current scientific state, completed experiments, exact numerical results, milestone status, submission blockers, and next task are documented in:

`research/CHECKPOINT_2026-09-23.md`

That checkpoint supersedes older planning notes where they conflict.

## Immediate next task

Issue #38 is now implemented in code but still awaits the production data run.

The next local command after PR #58 is merged is:

```powershell
python -m experiments.wti_databento_first_nearby --mode quote
```

If the quote is acceptable, download the historical CL statistics and run:

```powershell
python -m experiments.wti_databento_first_nearby --mode download
python -m scripts.run_first_nearby_robustness
```

The purpose remains to test whether the paper's current central empirical hierarchy survives when the physical-measure volatility posterior is estimated from a transparently reconstructed first-nearby settlement series. Do not treat implementation as a scientific result until those outputs are inspected.

Do not start a richer volatility model, buy more LO option data, or reopen the completed external-Q experiment before resolving #38.

## Important source correction

In the Barchart histories used by this project, `Latest` is the CME settlement field. Do not continue describing it as merely a settlement proxy or as an intraday last trade.

## Current main scientific result

Independent prior-date vanilla-WTI LO volatility information materially improves APO pricing relative to historical physical volatility and is broadly comparable to the prior-date APO-implied surface on a 253/280 no-clipping common-support matched sample.

PR #56 is merged; Issue #36 is complete.

See the canonical checkpoint for all exact numbers and interpretation boundaries.
