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
