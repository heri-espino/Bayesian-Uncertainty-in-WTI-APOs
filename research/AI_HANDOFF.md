# AI handoff

Read this file before continuing research work.

## Canonical current checkpoint

The current scientific state, completed experiments, exact numerical results, milestone status, and submission blockers are documented in:

`research/CHECKPOINT_2026-09-29.md`

That checkpoint supersedes older planning notes where they conflict.

## Scientific status

Issue #38 is complete in production.

The contract-reconstructed first-nearby physical-volatility robustness gives:

- posterior mean sigma 0.41824 versus 0.41651 for Yahoo `CL=F`;
- annualized realized volatility 0.41834 versus 0.41670;
- 2,381 exact pricing holdouts in both runs;
- historical PI MAE/RMSE 2.6468/3.4451 under first-nearby versus 2.6187/3.4090 under Yahoo;
- external previous-day LO MAE/RMSE 0.1559/0.2599 on the 253-row common-support sample versus reconstructed historical PI 0.4362/0.5466.

Therefore the paper's empirical hierarchy survives the physical-return source change.

Do not restart #38 or propose another first-nearby experiment.

## Current main scientific result

The paper supports:

[
	ext{posterior-integration refinement}
ll
	ext{historical-}P	ext{ versus option-informed }Q
]

in the observed WTI APO data, while the synthetic mechanism map shows that posterior integration can become material under weak information and high price curvature.

The option-informed conclusion is supported by both:

1. strict prior-date APO-implied smiles;
2. independent prior-date standard WTI vanilla-option (LO) information.

## Immediate next work

Do not add a richer pricing model by default.

The current sequence is:

1. finish manuscript integration of the first-nearby robustness;
2. resolve proprietary-data tracking/licensing consistency before freeze;
3. finish figures/tables and wording cleanup;
4. reproducibility freeze;
5. compile and inspect the Wiley submission PDF;
6. complete JFM submission materials.

## Important source conventions

- In the Barchart histories used here, `Latest` is the CME settlement field.
- The reconstructed physical return series excludes all roll-crossing returns.
- Four isolated mapped CL settlement gaps are not imputed; all affected one-day returns are excluded.
- Option-implied volatility is an effective/model-equivalent state under the maintained pricing map, not a unique structural diffusion coefficient.
- Do not claim universal LO superiority over APO information.

## Repository hygiene warning

The project policy is that proprietary raw Databento inputs should not be redistributed without verified rights. The current tree contains LFS-tracked paths under `data/databento/**/raw/` after recent data commits. Resolve this before the reproducibility freeze and keep the manuscript data-availability statement consistent with the actual repository state.
