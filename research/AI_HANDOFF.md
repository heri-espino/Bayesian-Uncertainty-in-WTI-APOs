# AI handoff

Read this file before continuing research work.

## Canonical current checkpoint

The current scientific state, completed experiments, exact numerical results, milestone status, submission blockers, and next task are documented in:

`research/CHECKPOINT_2026-09-23.md`

That checkpoint supersedes older planning notes where they conflict.

## Immediate next task

Issue #38:

> Reconstruct historical first-nearby CL returns instead of relying only on Yahoo `CL=F`.

The purpose is to test whether the paper's current central empirical hierarchy survives when the physical-measure volatility posterior is estimated from a transparently reconstructed first-nearby settlement series.

Do not start a richer volatility model, buy more LO data, or reopen the completed external-Q experiment before resolving #38.

## Important source correction

In the Barchart histories used by this project, `Latest` is the CME settlement field. Do not continue describing it as merely a settlement proxy or as an intraday last trade.

## Current main scientific result

Independent prior-date vanilla-WTI LO volatility information materially improves APO pricing relative to historical physical volatility and is broadly comparable to the prior-date APO-implied surface on a 253/280 no-clipping common-support matched sample.

PR #56 is merged; Issue #36 is complete.

See the canonical checkpoint for all exact numbers and interpretation boundaries.
