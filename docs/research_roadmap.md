# Research roadmap and project management

This page is the operational roadmap for the WTI Average Price Option paper. It should
be kept aligned with open GitHub Issues and the manuscript's actual scientific state.

## Project objective

Prepare a defensible submission to *Journal of Futures Markets* around the question:

> When does Bayesian parameter uncertainty materially affect WTI Average Price Option
> valuation, and when does volatility/model specification dominate instead?

The project is considered submission-ready only when the empirical evidence, literature
positioning, manuscript, reproducibility layer, and journal package all pass their
respective exit criteria.

## Milestone map

| Milestone | Goal | Issues | Exit criterion |
|---|---|---|---|
| [**M1 — Literature & positioning**](https://github.com/heri-espino/Metropolis-Hastings-for-Asian-Options-Using-Bayesian-Inference-and-Black-Scholes--Article-/issues/43) | Establish novelty and related-work positioning | [#33](https://github.com/heri-espino/Metropolis-Hastings-for-Asian-Options-Using-Bayesian-Inference-and-Black-Scholes--Article-/issues/33), [#34](https://github.com/heri-espino/Metropolis-Hastings-for-Asian-Options-Using-Bayesian-Inference-and-Black-Scholes--Article-/issues/34) | Literature matrix complete; introduction states a defensible contribution relative to Bayesian pricing, crude-oil IV, Asian-option, and model-complexity literatures |
| [**M2 — Empirical validation**](https://github.com/heri-espino/Metropolis-Hastings-for-Asian-Options-Using-Bayesian-Inference-and-Black-Scholes--Article-/issues/44) | Strengthen external validity and data provenance | [#35](https://github.com/heri-espino/Metropolis-Hastings-for-Asian-Options-Using-Bayesian-Inference-and-Black-Scholes--Article-/issues/35), [#36](https://github.com/heri-espino/Metropolis-Hastings-for-Asian-Options-Using-Bayesian-Inference-and-Black-Scholes--Article-/issues/36), [#37](https://github.com/heri-espino/Metropolis-Hastings-for-Asian-Options-Using-Bayesian-Inference-and-Black-Scholes--Article-/issues/37), [#38](https://github.com/heri-espino/Metropolis-Hastings-for-Asian-Options-Using-Bayesian-Inference-and-Black-Scholes--Article-/issues/38) | Forward validation broadened where feasible; settlement/data provenance strengthened; independent-Q-volatility route either implemented or explicitly documented as unavailable |
| [**M3 — Model robustness & paper integration**](https://github.com/heri-espino/Metropolis-Hastings-for-Asian-Options-Using-Bayesian-Inference-and-Black-Scholes--Article-/issues/45) | Test the central hierarchy and integrate final evidence | [#39](https://github.com/heri-espino/Metropolis-Hastings-for-Asian-Options-Using-Bayesian-Inference-and-Black-Scholes--Article-/issues/39), [#40](https://github.com/heri-espino/Metropolis-Hastings-for-Asian-Options-Using-Bayesian-Inference-and-Black-Scholes--Article-/issues/40) | One targeted richer-model robustness decision completed; final figures/tables are embedded in the manuscript and support the narrative |
| [**M4 — Reproducibility freeze**](https://github.com/heri-espino/Metropolis-Hastings-for-Asian-Options-Using-Bayesian-Inference-and-Black-Scholes--Article-/issues/46) | Make the submitted result exactly rebuildable | [#41](https://github.com/heri-espino/Metropolis-Hastings-for-Asian-Options-Using-Bayesian-Inference-and-Black-Scholes--Article-/issues/41) | Tests and build-paper workflow green; figures use vendored Wiley typography; submission tag/archive created |
| [**M5 — JFM submission**](https://github.com/heri-espino/Metropolis-Hastings-for-Asian-Options-Using-Bayesian-Inference-and-Black-Scholes--Article-/issues/47) | Produce the upload-ready journal package | [#42](https://github.com/heri-espino/Metropolis-Hastings-for-Asian-Options-Using-Bayesian-Inference-and-Black-Scholes--Article-/issues/42) | Main paper, supplement, cover letter, metadata, data/code statements, bibliography, and journal-specific checks completed |

## Workstreams

### Literature and novelty

The literature review must distinguish four related but non-identical questions:

1. Bayesian learning and parameter uncertainty in option pricing.
2. Asian/average-price option valuation and numerical methods.
3. Crude-oil option-implied volatility and volatility risk premia.
4. Model complexity and specification error in commodity option pricing.

The main novelty statement should not rely on MCMC as the contribution. The core result
is the conditional mechanism
[
C_{PI}-C_{PM}
approx
rac{1}{2}C^{Q\prime\prime}(\bar\sigma)
\operatorname{Var}(\sigma\mid\mathcal D),
]
combined with an empirical comparison against the much larger volatility-specification
margin observed in WTI APOs.

### Empirical validation

The current strongest empirical result is the strict forward-in-time volatility
validation. Future empirical work must preserve the following rules:

- no same-day APO settlement may enter a fitted surface used for that date;
- option rows from a valuation date are treated as clustered;
- broad-sample results and liquidity-filtered results are reported separately;
- sparse positive-volume evidence is described as such;
- APO-implied volatility remains labelled endogenous to the option family unless an
  independent vanilla CL surface is used.

### Modeling and robustness

The baseline one-factor constant-volatility model is a controlled benchmark, not a claim
that WTI follows GBM exactly. A richer model is useful only if it answers a concrete
robustness question without obscuring the paper's primary identification problem.

Completed robustness layers already include:

- prior/window sensitivity;
- Student-t physical-measure returns;
- high-precision pseudo-Monte Carlo;
- randomized Sobol QMC;
- Curran conditioning;
- simulation-based calibration;
- liquidity/open-interest filters;
- valuation-date cluster bootstrap.

### Reproducibility

The canonical remote build is GitHub Actions `build-paper`. A submission snapshot should
be reproducible from committed derived results without access to proprietary raw Barchart
files.

Required invariants:

- tests pass;
- documentation builds;
- `build-paper` passes;
- `figure_manifest.json` reports `wiley-utopia-vendored`;
- manuscript PDF is produced with the Wiley `Utopia2COL` template;
- all data-license constraints remain explicit.

## Recommended GitHub Project layout

When the repository Project is enabled, use these columns:

1. **Backlog**
2. **Ready**
3. **In progress**
4. **Blocked**
5. **Review**
6. **Done**

Recommended Project views:

- **Roadmap** — grouped by milestone M1–M5.
- **Workstream** — grouped by Literature, Data, Empirical, Robustness, Manuscript, Reproducibility, Submission.
- **Submission critical** — only issues required before JFM upload.
- **Optional extensions** — richer-model and external-data tasks that are useful but not allowed to block submission unless they reveal a material problem.

## Decision rule for new work

A new task should become an Issue if it changes at least one of:

- a scientific claim;
- an empirical result;
- a robustness conclusion;
- a table or figure;
- the reproducibility of the paper;
- the submission package.

Exploratory ideas that do not yet meet this threshold belong in research notes, not in the
main roadmap.
