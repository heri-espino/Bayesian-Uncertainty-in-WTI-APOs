# Research checkpoint — 2026-09-23

## Purpose

This file is the durable handoff for the current scientific state of the project before starting the historical first-nearby reconstruction in Issue #38.

The active manuscript is:

`paper/manuscript/main.tex`

Current target journal:

**Journal of Futures Markets**

The current manuscript title remains:

> **When Does Bayesian Parameter Uncertainty Matter? Evidence from WTI Average Price Options**

The latest major empirical extension was merged to `main` through PR #56:

- PR #56: independent vanilla-WTI external-Q validation;
- merge commit: `279b0bc17bd8e4f2beefa9d3df51b6d524ba585a`;
- Issue #36 is scientifically complete and closed.

Do not restart the project from the original “Bayesian pricing beats plug-in pricing” framing. The evidence has changed the paper's scientific interpretation.

---

## Current scientific question

The paper now asks two different questions.

### 1. Conditional on a pricing model, when does Bayesian posterior integration matter?

For a conditional risk-neutral price (C^Q(\sigma)),

\[
C_{PI}
=
E[C^Q(\sigma)\mid D],
\qquad
C_{PM}
=
C^Q(E[\sigma\mid D]).
\]

The second-order mechanism is

\[
C_{PI}-C_{PM}
\approx
\frac12 C^{Q\prime\prime}(\bar\sigma)
\operatorname{Var}(\sigma\mid D).
\]

The synthetic results support this mechanism strongly: posterior integration becomes important when posterior dispersion and pricing curvature are simultaneously large.

### 2. In observed WTI APOs, which empirical margin matters more?

The observed data show that the much larger pricing margin is not PI versus PM. It is the volatility state supplied to the pricing model.

The current empirical hierarchy is:

\[
\boxed{
\text{posterior-integration refinement}
\ll
\text{historical-}P\text{ versus option-informed risk-neutral volatility}
}
\]

This statement is now supported in two distinct ways:

1. a strict forward-in-time APO-implied volatility experiment;
2. an independent cross-instrument vanilla-WTI LO experiment.

The second experiment is important because it weakens the objection that the improvement is merely circular calibration within the APO family.

---

# Completed evidence

## A. Synthetic mechanism map

The large mechanism experiment is complete.

Key design:

- 175,000 independently simulated historical return datasets;
- historical sample sizes from 21 to 1,260;
- true volatility from 0.10 to 0.80;
- multiple maturities;
- moneyness from 0.60 to 1.50;
- multiple partial-fixing states;
- dense posterior quadrature rather than MCMC for this experiment.

Key result:

- largest observed absolute PI-PM gap: **0.1384**;
- largest gaps occur with:
  - short historical samples;
  - high volatility;
  - long remaining horizon;
  - extreme moneyness;
  - little realized fixing.

The Taylor mechanism tracks the observed gap very closely in the adverse states.

Interpretation:

> Bayesian posterior integration is not generically negligible. It becomes economically relevant when posterior uncertainty interacts with strong curvature of the pricing map.

This is the controlled mechanism result and should remain the first scientific contribution.

---

## B. Contract-consistent October-2026 WTI APO baseline

The production October-2026 panel contains:

- 310 retained option-date observations;
- 12 valuation dates;
- six individual positive-volume contract-date observations.

Main result:

| Method | RMSE |
|---|---:|
| Posterior-integrated | 0.5177 |
| Posterior-mean plug-in | 0.5183 |

Positive-volume contracts:

| Method | RMSE |
|---|---:|
| Posterior-integrated | 0.1864 |
| Posterior-mean plug-in | 0.1869 |

The PI-PM differences are approximately (10^{-3}), and the high-precision numerical experiments show that these differences are real rather than Monte Carlo noise.

Independent numerical checks include:

- high-budget pseudo-random Monte Carlo;
- randomized Sobol;
- Curran conditioning.

Conclusion:

> In the observed October WTI states, posterior integration is a second-order point-price correction.

---

## C. Extended strict forward APO-implied-Q validation

Issue #35 is complete.

The experiment spans seven expiries:

- Sep-2026;
- Oct-2026;
- Nov-2026;
- Mar-2027;
- Sep-2027;
- Mar-2028;
- Sep-2028.

Total strict-forward holdouts:

**2,381 option-date observations**

No same-day target APO implied volatility enters the fitted prior-date surface.

Pooled result:

| Method | MAE | RMSE |
|---|---:|---:|
| Historical-volatility PI | 2.6187 | 3.4090 |
| Expanding prior-date APO smile | 0.1088 | 0.1725 |
| Previous-day APO smile | 0.1075 | 0.1594 |

The result appears in every admitted expiry and survives:

- valuation-date cluster resampling;
- positive-volume subsets;
- open-interest thresholds.

The effective APO-implied volatility term structure is materially different from the long-window historical posterior near 0.416.

Approximate effective date-level (Q) levels:

- Sep-2026: 0.448;
- Oct-2026: 0.457;
- Nov-2026: 0.444;
- Mar-2027: 0.361;
- Sep-2027: 0.300;
- Mar-2028: 0.265;
- Sep-2028: 0.242.

These are **effective/model-equivalent risk-neutral volatility states under the maintained one-factor pricing map**, not claims about a unique structural diffusion coefficient.

---

## D. Independent vanilla-WTI LO validation

Issue #36 is complete and merged.

### Why this experiment exists

The prior-date APO smile could still be criticized because the volatility information comes from the same option family that is later priced.

The independent experiment instead uses:

\[
\text{prior-date LO vanilla information}
\rightarrow
\widehat\sigma_Q^{LO}
\rightarrow
\widehat C^{APO}.
\]

No APO price is used to construct the external LO state.

### Data

Source:

- Databento;
- dataset `GLBX.MDP3`;
- CME standard monthly WTI option parent `LO.OPT`.

Required underlyings for the October APO fixing structure:

- `CLX6`;
- `CLZ6`.

Final acquired strike range:

**70 to 120**

Strict-forward acquisition window:

- start: 2026-08-24;
- end-exclusive: 2026-09-11.

Raw Databento vendor records remain local and gitignored.

### Vanilla IV inversion

Databento GLBX.MDP3 does not directly publish settlement implied volatility for this use.

The project therefore uses:

- official LO option settlements;
- official CL futures settlements;
- option definitions;
- Treasury rate proxy;
- American CRR futures-option IV inversion.

Expanded IV panel:

- **5,220 / 5,220 successful IV inversions**;
- 13 trading reference dates;
- two underlyings;
- 5,214 option settlements flagged actual;
- six flagged theoretical;
- median implied volatility approximately 0.4814;
- range approximately 0.4090 to 0.6574.

### External surface mapping

For each required underlying, a prior-date quadratic log-moneyness smile is fitted with call/put interaction terms.

For a target APO strike (K),

\[
\widehat\sigma_{Q,t}^{LO,eff}(K)
=
\left[
\sum_u
w_u
\left\{
\widehat\sigma_{Q,u,t-1}^{LO}(K)
\right\}^2
\right]^{1/2}.
\]

The (w_u) values come from the actual APO fixing map.

For the October pre-averaging schedule, the fixing structure corresponds to:

- 14 CLX26 fixings;
- 8 CLZ26 fixings.

The code derives the weights from `apo_fixing_state.csv`; they are not hardcoded.

### Expanded common-support result

The original narrow LO strike pilot had only 60/280 matched contract-dates inside genuine interpolation support.

After expanding the acquired LO strikes to 70–120:

- matched sample: 280 contract-dates / 10 valuation dates;
- exact no-clipping common-support sample: **253/280 = 90.4%**;
- all 10 matched dates remain represented;
- only **50/620 = 8.1%** external surface rows require support clipping.

Exact 253-row comparison:

| Method | MAE | RMSE |
|---|---:|---:|
| Historical PI | 0.44636 | 0.55617 |
| External LO surface, previous day | 0.15588 | 0.25989 |
| External LO surface, expanding | 0.16040 | 0.28578 |
| Prior-date APO smile, previous day | 0.16763 | 0.26860 |
| Prior-date APO smile, expanding | 0.16122 | 0.29124 |

### Paired valuation-date cluster bootstrap

100,000 date-cluster resamples.

External previous-day LO vs historical PI:

- delta MAE = -0.29048;
- 95% CI [-0.34391, -0.23325];
- delta RMSE = -0.29627;
- 95% CI [-0.35029, -0.25798].

External expanding LO vs historical PI:

- delta MAE = -0.28596;
- 95% CI [-0.33025, -0.23415];
- delta RMSE = -0.27039;
- 95% CI [-0.33738, -0.24072].

External previous-day LO vs prior-date APO previous-day:

- delta MAE = -0.01175;
- 95% CI [-0.02506, -0.00008];
- delta RMSE = -0.00871;
- 95% CI [-0.01490, 0.00024].

External expanding LO vs prior-date APO expanding:

- delta MAE = -0.00082;
- 95% CI [-0.00973, 0.00931];
- delta RMSE = -0.00546;
- 95% CI [-0.01493, 0.00292].

### Correct interpretation

The result supports:

> Independent vanilla-WTI risk-neutral information robustly improves strict-forward APO pricing relative to the historical physical-volatility state.

It also supports:

> Over the broad common-support sample, the external LO surface and the prior-date APO surface are empirically comparable.

Do **not** claim:

- LO is globally superior to APO;
- the LO surface identifies the unique structural (Q) diffusion;
- all common WTI market dependence/endogeneity has disappeared;
- the empirical surface transfer is a no-arbitrage equality between vanilla and APO volatility.

The experiment reduces the important **family-specific circularity** concern.

---

# Current manuscript state

PR #56 also rewrote the active JFM manuscript.

The current paper now presents the evidence in this order:

1. synthetic PI-PM mechanism;
2. contract-consistent observed WTI PI-PM comparison;
3. extended strict-forward APO-implied volatility experiment;
4. independent vanilla-WTI LO validation.

The external LO experiment is now a **main result**, not future work.

Files materially updated include:

- `paper/manuscript/main.tex`;
- `paper/manuscript/sections/01_introduction.tex`;
- `paper/manuscript/sections/02_contract_market.tex`;
- `paper/manuscript/sections/03_methodology.tex`;
- `paper/manuscript/sections/04_research_design.tex`;
- `paper/manuscript/sections/05_results.tex`;
- `paper/manuscript/sections/06_robustness.tex`;
- `paper/manuscript/sections/07_conclusion.tex`.

The title was intentionally retained.

---

# Data-source conventions and corrections

## Barchart APO / CL field

**Important correction from the author/source workflow:**

For the Barchart histories used in this project, the `Latest` field is the **CME settlement** field.

Earlier repository wording was intentionally over-cautious and called it a settlement proxy pending reconciliation. Do not continue treating this as a scientific uncertainty in the project.

Consequences:

- Issue #37 is **not a scientific blocker** for submission;
- no large observation-by-observation CME reconciliation is required merely to establish that the target field is a settlement;
- remaining provenance work, if retained, is documentation/field-mapping cleanup;
- manuscript/research docs that still say “settlement proxy” or “not independently verified official CME settlement” should be updated in the next provenance cleanup;
- `AGENTS.md` must no longer instruct future agents to treat the field only as a proxy.

Do not reinterpret `Latest` as an intraday last trade.

## Historical physical-measure source

The current (P)-measure volatility inference still uses:

`Yahoo CL=F`

as an explicitly labelled continuous/front-month proxy.

This is now the **main unresolved scientific data issue**.

The historical roll convention of Yahoo `CL=F` is not sufficiently transparent for the paper's final empirical conclusion.

## Databento

Raw proprietary Databento data:

- remain local;
- remain gitignored;
- must not be committed unless redistribution rights are verified.

Versioned artifacts may contain:

- query metadata;
- hashes;
- diagnostics;
- code;
- permitted derived summaries/results.

No additional Databento purchase is currently needed for Issue #36.

---

# Next scientific task: Issue #38

## Objective

Replace or benchmark the Yahoo `CL=F` physical-volatility proxy with a contract-reconstructed historical first-nearby CL return series.

This is the next task **before declaring the paper scientifically submission-ready**.

## Why it matters

The paper's main empirical conclusion is now that the volatility state matters much more than posterior integration.

A referee could reasonably ask whether the poor historical-(P) baseline is partly caused by the construction of the continuous/front-month Yahoo series.

The project therefore needs to determine whether:

\[
\sigma_P^{\text{reconstructed first-nearby}}
\]

materially differs from the current Yahoo-based posterior and whether replacing the source changes the pricing hierarchy.

The goal is not to force the current conclusion to survive.

If the reconstructed series materially closes the (P)-versus-option-informed gap, the manuscript must be revised accordingly.

## Required design

1. **Specify the roll rule explicitly.**
   - Use a documented first-nearby rule consistent with the APO/futures conventions.
   - Reuse the explicit contract-expiry information where appropriate.
   - Do not hide an approximate roll heuristic.

2. **Reconstruct daily first-nearby CL settlement levels contract by contract.**
   - Inspect existing source coverage first.
   - If additional market data are required, quote cost before purchasing.
   - Preserve licensing constraints.

3. **Exclude every return that spans a contract switch.**
   - A jump from one delivery contract to another can reflect contango/backwardation.
   - It must not be treated as a one-day diffusion return.

4. **Compare reconstructed returns with Yahoo `CL=F`.**
   Report at least:
   - number of observations;
   - date coverage;
   - excluded roll returns;
   - mean/std of returns;
   - annualized realized volatility;
   - major return discrepancies;
   - rolling volatility comparison.

5. **Re-estimate the physical posterior.**
   Compare:
   - posterior mean/median/mode of sigma;
   - posterior standard deviation;
   - credible interval;
   - sensitivity to the return-source change.

6. **Re-run the key historical-volatility pricing baselines on identical holdouts.**
   The important comparison is not merely the posterior sigma.
   Recompute the historical-(P) prices/errors against the same strict-forward target observations used by the option-informed models.

7. **Test the scientific hierarchy.**

   The question is:

   \[
   \text{Does reconstructed }P
   \text{ remain much worse than prior-date }Q\text{ information?}
   \]

8. **Update the manuscript only from versioned results.**
   No number enters the paper without a saved experiment/config/result.

## Exit criterion for #38

Issue #38 is complete when:

- the first-nearby roll rule is versioned;
- the reconstructed physical return panel exists;
- roll-crossing returns are explicitly excluded;
- the reconstructed and Yahoo physical posteriors are compared;
- key historical pricing results are rerun;
- the manuscript states whether the central hierarchy survives.

---

# What not to do next

Do not expand scope before #38 is resolved.

Specifically:

- do not buy more LO data;
- do not expand the independent LO strike range further;
- do not run same-day APO calibration as evidence for the external claim;
- do not start Heston merely because it is more realistic;
- do not add a multi-factor model before checking the physical-return construction;
- do not make the paper about LO outperforming APO;
- do not commit proprietary raw Databento files.

---

# Milestone status

The repository tracks publication work through Issues #43–#47.

## M1 — Literature & positioning (#43)

Status: **scientifically complete, archival cleanup remains**.

Completed:

- #33 literature matrix;
- #34 manuscript positioning rewrite.

Remaining:

- #49 archival acquisition/extraction of direct-precedent PDFs.

#49 is not currently a scientific blocker because the critical direct precedents have already been verified and incorporated into the manuscript positioning.

## M2 — Empirical validation (#44)

Status: **almost complete; #38 is the remaining scientific blocker**.

Completed:

- #35 extended strict-forward APO validation;
- #36 independent vanilla-WTI LO validation.

Reclassified:

- #37 Barchart settlement provenance is not a scientific blocker because `Latest` in the project histories is the CME settlement field. Remaining work is documentation cleanup.

Next:

- #38 historical first-nearby CL reconstruction.

M2 exits after #38 and the associated manuscript/data-source cleanup are complete.

## M3 — Model robustness & paper integration (#45)

Tracked issues:

- #39 richer commodity-volatility robustness;
- #40 final figures/tables integration.

Current recommendation:

- #40 is required for submission polish;
- #39 should be treated as **optional targeted robustness**, not an automatic prerequisite, unless #38 reveals that the central hierarchy is unstable or a referee-facing gap remains.

Avoid scope creep into a second modeling paper.

## M4 — Reproducibility freeze (#46)

Not started.

After scientific results are frozen:

- rebuild tables/figures;
- ensure tests are green;
- compile the Wiley manuscript;
- create final version tag;
- archive the exact scientific snapshot.

## M5 — JFM submission (#47)

Not started.

Final package still needs the work tracked in #42, including:

- remove internal-draft marker;
- fill corresponding-author metadata;
- complete acknowledgments as applicable;
- final bibliography/data/code checks;
- assemble supplement;
- cover letter;
- final JFM guideline pass.

Do not start the submission freeze before #38 is resolved.

---

# Current blocker hierarchy

### Scientific blocker

1. **#38 — reconstructed historical first-nearby CL returns**

### Documentation / paper integration

2. update stale “Barchart settlement proxy” wording;
3. final figures/tables integration (#40).

### Reproducibility / submission

4. #41 reproducibility freeze;
5. #42 submission package.

### Optional, not automatically required

- #39 richer model robustness;
- #49 archival literature-file cleanup.

---

# Scientific claim to preserve unless #38 changes it

The current paper should be summarized as:

> Bayesian posterior integration has a predictable state-dependent effect governed by posterior dispersion and pricing curvature. It can become economically material in weak-information, high-curvature regimes. In the observed WTI APO application, however, posterior integration of historical volatility is a second-order refinement. Option-informed risk-neutral volatility states provide a much larger strict-forward pricing improvement, and that conclusion survives when the volatility state is constructed independently from standard vanilla WTI options rather than from the APO family itself.

This claim is conditional on the maintained pricing map and must be revisited after the reconstructed first-nearby physical-volatility experiment.

---

## Issue #38 implementation status

The code path for the historical first-nearby robustness is implemented in PR #58 on branch `data/reconstruct-first-nearby-returns`.

Implemented:

- cost-capped Databento acquisition of official monthly CL final-settlement statistics for the 2024-01-01 through 2026-09-10 physical-inference window;
- exact first-nearby reconstruction from contract/date settlements;
- empirical roll boundaries derived from each contract's last final-settlement reference date;
- mandatory exclusion of the first return after every contract switch;
- same-model posterior comparison against Yahoo `CL=F`;
- `--physical-inference-source first-nearby` in the canonical WTI APO pricing driver;
- source propagation through date-panel and seven-expiry forward-validation runners;
- separate `*_first_nearby` namespaces so original production outputs are preserved;
- rerun of the independent vanilla-WTI LO validation against the reconstructed historical baseline;
- exact-holdout Yahoo-versus-first-nearby pricing comparison;
- a one-command production runner: `python -m scripts.run_first_nearby_robustness`.

**No production first-nearby result has yet been accepted into the manuscript.**

The immediate local data gate after PR #58 is merged is:

```powershell
python -m experiments.wti_databento_first_nearby --mode quote
```

Only after inspecting and accepting that quote should the raw historical CL statistics be downloaded. The raw Databento file remains local/gitignored.

After download:

```powershell
python -m scripts.run_first_nearby_robustness
```

Do not close #38 or update manuscript numbers until the reconstruction report, posterior comparison, identical-holdout baseline comparison, external-LO rerun, and date-cluster bootstrap have been inspected.

---

# Reproducibility / branch rules

Before new work:

```bash
git switch main
git pull --ff-only
```

Start Issue #38 from current `main` on a new short-lived branch, for example:

```bash
git switch -c data/reconstruct-first-nearby-returns
```

Do not revive `empirical/vanilla-cl-data-audit`; PR #56 has already been merged.

Before opening the #38 PR:

```bash
python -m scripts.check_repo_structure
python paper/build.py --check
python -m pytest -q
```

Heavy derived-output workflows remain manual-only through `workflow_dispatch`. Lightweight CI may remain automatic.

---

# Handoff to the next agent

Read this checkpoint first, then:

1. read Issue #38;
2. inspect the existing monthly CL data coverage and expiry table;
3. inspect the current Yahoo `CL=F` inference implementation;
4. design the first-nearby reconstruction before writing a parallel pricing pipeline;
5. keep reusable return/roll logic in `bayesian_asian_options/src/bayesian_asian_options/`;
6. keep experiment orchestration in `experiments/`;
7. reuse the existing canonical WTI pricing drivers rather than creating a new source-specific valuation engine;
8. save comparison outputs under a clearly namespaced analysis directory;
9. document the checkpoint/result before moving to submission polishing.

The immediate question is no longer whether external (Q) information works. That has been answered.

The immediate question is:

> **Does the central P-versus-option-informed-Q hierarchy survive when the physical volatility is estimated from a transparently reconstructed first-nearby CL settlement series rather than Yahoo `CL=F`?**
