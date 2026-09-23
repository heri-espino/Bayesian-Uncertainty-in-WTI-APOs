# Vanilla CL external-Q data audit

## Current download

The committed `data/csv/CLX26/` folder contains 40 Barchart-style vanilla-option histories:

- 20 strikes from **85.0 to 94.5** in 0.5 increments;
- both a call and put at every strike;
- underlying futures month: **CLX26 (November 2026 WTI future)**.

This is a good strike grid for an external-`Q` pilot.

## Temporal limitation

The inspected histories currently contain observations only from roughly **14/15 September 2026
through 22/23 September 2026**. The October-2026 APO baseline used in the manuscript has target
valuation dates ending **10 September 2026**.

Therefore the current files have **no temporal overlap** with the strict experiment

[
\text{vanilla CL information at }t-1
\rightarrow \sigma_Q^{\text{vanilla}}
\rightarrow \text{APO settlement at }t.
]

They must not be used to claim independent forward validation for the existing October baseline.

## Correct series

For the standard monthly WTI option on the November-2026 WTI future, Barchart reports option
expiration **2026-10-15**. The underlying future is CLX26. The option expiry must be retained
explicitly because implied-volatility inversion requires time to expiry.

The present CSV schema does not itself store the option expiry, so the external-Q pipeline should
carry it as contract metadata rather than infer it from the filename.

## Next data requirement

Before running the pricing experiment, obtain histories for the same standard monthly CLX26
option series that include at least **2026-08-24 through 2026-09-10**. A second CLZ26 monthly
surface is desirable for a contract-matched two-futures mapping, but CLX26 alone is sufficient for
a first scalar-`Q` pilot under the paper's maintained one-factor constant-volatility pricing map.

The first test after any re-download should be the lightweight audit:

```powershell
python -m experiments.wti_vanilla_cl_audit
```

Only after `strict_forward_ready=true` should the IV inversion and APO pricing stage run.

## Modeling note

Standard WTI monthly options are American-style. A plain Black-76 inversion is therefore an
approximation, especially away from the money. The production external-Q experiment should either
use an American futures-option valuation routine or restrict a Black-style robustness calculation
to sufficiently near-the-money observations and label that approximation explicitly.


## Databento replacement route

Barchart no longer exposes the pre-11-September history needed for this strict-forward test.
Issue #36 therefore uses Databento CME Globex `GLBX.MDP3` as the replacement acquisition
route. The parent option symbol is `LO.OPT`; instrument definitions are filtered to the
November- and December-2026 WTI futures (`CLX6`, `CLZ6`) and strikes 85.0--94.5.

The acquisition driver is deliberately cost-capped:

```powershell
$env:DATABENTO_API_KEY = "<your local key>"
python -m experiments.wti_databento_external_q --mode quote
python -m experiments.wti_databento_external_q --mode discover
python -m experiments.wti_databento_external_q --mode download
```

The default hard cap is USD 5.00. `quote` performs no billable time-series request.
`discover` buys only the one-day definition snapshot after checking its quote and then
quotes the exact selected `statistics` request. `download` proceeds only if the estimated
new cost remains below the cap. Existing local files are reused unless `--force` is given.

For `GLBX.MDP3`, the downloaded `statistics` records provide official settlement (`stat_type=3`),
cleared volume (`6`), and open interest (`9`). Databento's current per-dataset table does not list
settlement-implied volatility (`14`) for CME Globex, so the first analysis step is a coverage audit
of LO and CL settlements; IV is then inverted from those official settlements with an American
futures-option model.
