# JCM Paper B — novelty matrix and independent study design

**Started:** 2026-10-27. **Status:** research design and source audit, **no new pricing or hedging results**. **Candidate journal:** *Journal of Commodity Markets* (JCM), not an accepted or submitted paper. **Work branch:** `paper/jcm-independent-research-track`; source base: `results/aao-databento-pilot-2023h1-20261026`. Keep the REMEF Paper A and Experiments 003–005 untouched. Never merge into another agent's branch without explicit authorization.

## 1. Working question and distinct primary contribution

**Working title, subject to revision:** *The Value of Correct Fixing Paths and Information Timing in WTI Average Price Option Valuation and Hedging*.

**Question:** When valuing NYMEX WTI Average Price Options (AAOs), how much economic/pricing/hedging error is attributable to (a) correct already-realized first-nearby CL daily fixings, (b) the actual contract roll and valuation-date CL futures term structure, (c) volatility/process assumptions, and (d) lagged and reliable information vintages? Are simpler benchmarks competitive when evaluated against independently observed executable prices or hedges?

This is a **proposal**, not a novel empirical discovery. The research only becomes an independent paper if we provide *new*, independently validated economic evidence, beyond the REMEF Paper A comparison between posterior-integration and volatility-input choices.

**Schematic option payoff (per contract):**

`1000 × max(eta × (A - K), 0)`, where `eta=+1` call, `eta=-1` put, and `A = [sum_{i in R(t)} observed_CL_fix_i + sum_{i in U(t)} future_first_nearby_CL_fix_i] / N`.

The actual fixing schedule, last trading day, first-nearby contract identity, dollar/barrel scaling and historically available settlement timestamp must be verified against the relevant CME rule revision. This is an accounting identity for a fixed-strike cash-settled Asian payoff, **not** by itself a new model. Rule 341 identifies first-nearby CL average, USD/barrel minimum increment $0.01, contract multiplier 1,000 barrels, last business day expiry, and European cash settlement: https://www.cmegroup.com/rulebook/NYMEX/3/341.pdf .

## 2. Prior-art matrix — what we MUST NOT claim as original

| Source / verified bibliographic entry | Established contribution | Consequence for our JCM originality |
| --- | --- | --- |
| **Kemna & Vorst (1990)**, *A Pricing Method for Options Based on Average Asset Values*, *Journal of Banking & Finance*. Supplied in project literature. | Asian average-value options; Monte Carlo pricing and variance reduction using geometric average. | Monte Carlo or a geometric control variate for an arithmetic Asian payoff is NOT novel. |
| **Curran (1994)**, *Valuing Asian and Portfolio Options by Conditioning on the Geometric Mean Price*, *Management Science* 40(12). Project source. | Conditioning on geometric means for efficient Asian/basket approximation. | Curran is an **established approximation baseline**, not a new discovery or claim of exact exchange-engine reproduction. |
| **Kahalé (2018)**, *General Multilevel Monte Carlo Methods for Pricing Discretely Monitored Asian Options*. Project source. | Efficient MLMC schemes for discretely monitored averages under a range of stochastic models. | Faster brute-force Monte Carlo alone is unlikely to establish algorithmic novelty; benchmark complexity claims against MLMC literature. |
| **Kyriakou, Pouliasis & Papapostolou (2016)**, *Jumps and stochastic volatility in crude oil prices and advances in average option pricing*, *Quantitative Finance* 16(12), 1859–1873, DOI 10.1080/14697688.2016.1211798. | Calibrates WTI vanilla options, prices arithmetic Asian options under jumps/stochastic volatility; reports price sensitivity to jump risk. | **Stochastic volatility + jumps + WTI Asian valuation has already been done.** Merely fitting such a model does NOT establish novelty. https://doi.org/10.1080/14697688.2016.1211798 |
| **Kyriakou, Nomikos, Pouliasis & Papapostolou (2016)**, *Affine-Structure Models and the Pricing of Energy Commodity Derivatives*, *European Financial Management* 22(5), 853–881, DOI 10.1111/eufm.12071. | Petroleum futures, discrete arithmetic Asian option pricing **and hedging** under affine seasonal mean reversion/jumps/stochastic volatility. | **Asian pricing and hedging for WTI with complex processes already exists.** We need a new question/data design/empirical result, not "first to hedge Asian options." https://doi.org/10.1111/eufm.12071 |
| Existing repository **Paper A** WTI APO code: `wti_apo_pricing.py`, `wti_first_nearby.py`, `asian_futures_pricing.py`, `experiments/wti_curran_benchmark.py`; experiment outputs. | Implements partly fixed realized CL values, dated futures fixings, Curran-style approximation, one-factor Q Monte Carlo, Barchart/Databento diagnostics. | **Even our repository already has a structural component**: new JCM work must go beyond its 2026 Barchart/LO simulations and the retrospective parity-anchored Experiments 003–005. |

This is a **preliminary** related-work matrix, not a comprehensive systematic search. Before a JCM abstract, check 2017–2026 JCM and *Energy Economics* studies and recently published options-hedging literature for closely overlapping empirical tests.

## 3. Stronger falsifiable claims worth TESTING (not asserting)

- **H1 (fixing progress):** The incremental model error from misidentifying already-realized fixings varies systematically with the fraction fixed `m/N` and roll transitions. Test with date-, option-, strike- and expiry-matched contrasts at the same predeclared timestamp.
- **H2 (information timing):** Valuation accuracy deteriorates when contemporaneous futures-curve or official settlement revisions are incorrectly treated as available before publication. Test replay using publication timestamps and an alternative archive-end vintage; never call retrospective data strictly ex-ante without proof.
- **H3 (pricing vs hedging):** A richer path-dependent model may change delta hedge risk even when its contract-level MAE benefit is small. Evaluate executable futures hedges, rebalancing, transaction costs and tail risks; **do not** present this as novel merely because it includes hedging.
- **H4 (independent vs model-generated targets):** Rankings based on exchange settlement marks may differ from rankings based on contemporaneous AAO trades or bid/ask. **Cannot test until independent market targets are actually found**.

A failure of H1–H4 is still a research result if the experiment is clean; journal-level publishability remains conditional on contribution strength.

## 4. Pre-existing CL sources and immediate blocker

Read `research/JCM_CL_FUTURES_FEASIBILITY_AUDIT_2026-10-27.md` first. Important discovery: the repository ALREADY HAS a separately purchased CL futures-history LFS file covering source-query Jan 2024–Sep 2026, a 673-day first-nearby reconstruction (632 clean returns), and 14 short Barchart 2026 CL strip CSVs. The 81-month AAO raw DBNs are options, not 81 months of CL underlyings.

**Integrity blocker:** the declared raw CL SHA256 in `results/analysis/wti_first_nearby/acquisition_manifest.json` (**f52ec758ace7bb7f924c69009e686bfdb09196cdbfdb09e1b505822626e57204**) differs from the Git LFS pointer OID (**bbc5356c7fc5e41b898bdf316cc3dcc8e918e3b0d8be351fbbabfa3dff7c3602**). This suggests a version/provenance discrepancy, NOT proven data corruption. Existing `scripts/audit_jcm_cl_feasibility.py` already performs a metadata audit and optionally computes the local file SHA256. **Do not create a redundant scanner, pay the vendor, override the manifest, or silently proceed with this history.**

Local owner must first run read-only validation (no GitHub Actions, provider calls, or changes to sparse checkout):

```powershell
conda activate asian-options
python -m scripts.audit_jcm_cl_feasibility --verify-large-raw-sha256
```

Use the report's printout to reconcile the version, and save a *new* versioned discrepancy/replay report. Hashing can take time; it only reads the pre-existing ~312 MB file. **Do not overwrite earlier logs or manifests.** The exact binary hash can only be trusted once the local LFS payload is verified. The metadata scanner itself may encounter a missing file if sparse-checkout excludes that path.

## 5. Experiments and separation from Paper A

**Experiment001 (proposed first new JCM experiment; NOT RUN):** *Path construction and settlement-vintage integrity*. Target: mechanically reconstruct 2024–2026 monthly AAO first-nearby CL fixes from verified existing sources for selected dates without provider calls. Implement tests for roll day, no/partial/all fixed, missing settlement, NaN/price unit failures, update availability, and exact payoff multiplier. Reuse existing modules and scripts; only add missing capability in the library with docstrings/tests/API docs. Calculate traceable discrepancy counts, no contract price extracts in public files. **Do not call this a pricing-accuracy backtest.**

**Experiment002 (only after Experiment001 is validated):** *Futures-curve conditional path-pricing attribution*. Evaluate the existing one-factor Q MC and Curran-style approximation with the **same verified** fixing calendar and curve; vary a *single* assumption at a time to attribute model/measurement errors. Track numerical errors, market-price errors and distinct calibration timing. Do not use target AAO premium to infer its own volatility.

**Experiment003 (only if data permit):** *Independent AAO market quotes or execution/hedge outcomes*. Compare model rankings under independent, timestamp-valid targets; include appropriate bid/ask and costs. If no quotes exist, narrow the research question and **do not fabricate an independent market exercise**.

Sequential experiment names are deliberate; each needs its own `README.md`, run metadata, exact reproducibility commands, source hashes, results/figures, conclusions, failures and handoff, all pushed to Git. Heavy computation must remain **manual local**, not automatic GitHub Actions.

## 6. Publication evidence gate and collaboration instructions

- **Data gate:** verified SHA/provenance; fixing calendar, CL contract roll, forward curve, rates, target settlement/quotes, publication timestamps; explicit missingness/attrition.
- **Economic gate:** validate model price units ($/bbl vs contract USD), 1-cent tick and 1000-barrel multiplier; value of model improvements relative to costs and numerical MC standard errors.
- **Independence gate:** Paper A REMEF studies historical vs lagged market-IV and Bayesian PI–PM effects, including Experiments 003–005; JCM needs **distinct** primary figures, payoff/hedge interpretation and genuinely new information. Declare shared raw data and cite Paper A as appropriate.
- **Publication gate:** no submission until result-level novelty and exact empirical soundness are demonstrated; JCM title remains provisional.
- **Collaboration:** work in new branch/PR; never merge without user instruction, reset/clean/force-push, delete LFS files or alter main/REMEF manuscripts. Agent handoff: `paper/jcm/INDEPENDENT_STUDY_HANDOFF.md`.

**Immediate next action for local data owner:** run the existing CL hash audit, share/push machine-readable verification, and use that to decide whether Experiment001 can ingest the 2024–2026 CL material safely. **No new Databento purchase is needed for that step.**
