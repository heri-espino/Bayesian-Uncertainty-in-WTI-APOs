# Independent JCM paper track — agent handoff

**Current handoff:** October 27, 2026. **Research status:** pre-experimental. This is the new, separate Paper B, not the old JCM CAS reformatting of Paper A. **No new JCM pricing/hedging experiment has been executed**. Full description: [novelty and study design](../../research/JCM_PAPER_B_NOVELTY_MATRIX_AND_STUDY_DESIGN_2026-10-27.md).

## Ownership and boundaries

The user assigned this ChatGPT research track the JCM development work **in parallel with another REMEF-focused agent**. Work in `paper/jcm-independent-research-track`, based on `results/aao-databento-pilot-2023h1-20261026`, using draft PR review. **No merge, no main changes, no editing REMEF manuscript/figures or completed Experiments 003–005 without express request**.

This document is the durable cross-agent state; agents must never rely on chat to reconstruct intended work or previous findings. All future JCM analyses must be preserved in Git commits, including experiments, configs, data provenance, raw/aggregate metric integrity, logs, synthetic tests, numerical results, failures, interpretation, figures and next steps. Large approved private market data use Git LFS; never store credentials.

## Read these before any JCM research

1. Repository `AGENTS.md`, `README.md`, `research/AI_HANDOFF.md`, `docs/architecture.md`, `docs/api/index.md`.
2. [Two-paper strategy and overlap ledger](../../docs/two_paper_publication_strategy_2026-10-27.md).
3. [New structural AAO feasibility plan](../../research/STRUCTURAL_WTI_AAO_PAPER_FEASIBILITY_PLAN_2026-10-27.md).
4. [CL feasibility audit and SHA discrepancy](../../research/JCM_CL_FUTURES_FEASIBILITY_AUDIT_2026-10-27.md).
5. [Novelty matrix, hypotheses, staged experiments](../../research/JCM_PAPER_B_NOVELTY_MATRIX_AND_STUDY_DESIGN_2026-10-27.md).
6. Existing pricing library modules: `wti_apo_pricing`, `wti_first_nearby`, `asian_futures_pricing`; existing Curran benchmark `experiments/wti_curran_benchmark.py`. Do not reimplement these under new names without evidence they are insufficient.

## Current established facts, not JCM results

- AAO option raw histories: 81 months, 162 LFS DBNs (2020–Sep2026), prior acquisition/manifests. No proof this includes historical CL futures prices or AAO order-book trades.
- A *different* Databento CL history (33 contracts; reported 2,223,975 rows) was previously acquired for Jan2024–Sep2026. A 673-date first-nearby series with 632 usable returns and four missing dates is **already** in the repo. Narrow 2026 Barchart contract strip also exists.
- **Blocker:** CL raw file's LFS OID `bbc5356c7fc5e41b898bdf316cc3dcc8e918e3b0d8be351fbbabfa3dff7c3602` does not match original acquisition ledger SHA `f52ec758ace7bb7f924c69009e686bfdb09196cdbfdb09e1b505822626e57204`. This means source *version* provenance needs investigation, not that either source is necessarily corrupt. Remote GitHub metadata cannot establish byte-level equivalence without retrieving the LFS payload.
- The original one-factor partly fixed Asian pricing, Curran approximation and first-nearby contract mapping **already exist**, so claiming their first invention for JCM would be incorrect.
- There is established WTI Asian option stochastic-volatility and jumps research (Kyriakou, Pouliasis, Papapostolou 2016) AND petroleum Asian option **hedging** research (Kyriakou et al. 2016). Our originality must be a new, distinct empirical question and validated data design.

## Operational sequence

**Step 1 — local hash check, no provider calls.** The owner of the real LFS payload runs:

```powershell
conda activate asian-options
python -m scripts.audit_jcm_cl_feasibility --verify-large-raw-sha256
```

Inspect and commit an independent result report; do not rewrite the old acquisition manifest to suppress the mismatch. If the Git LFS object is absent locally, report missing materialization without sparse-checkout changes or repurchase. Do not claim `--write-json` is safe when an output file already exists; it refuses to overwrite.

**Step 2 — `experiment001`, strictly first.** Build a read-only reproducible verification of first-nearby fixing paths, roll mapping, publication/vintage checks, source-level prices and data attrition for a *small* predeclared 2024–26 sample. Synthetic tests first; no paid API and no source mutation. Do not refer to this as an independent pricing backtest.

**Step 3 — `experiment002` conditional on Step 2.** The path-dependent Q MC and Curran numerical comparison using the exact same verified fixings and forward curve. Distinguish Monte Carlo numerical SE, historical model error, and price-vintage mismatch.

**Step 4 — `experiment003` conditional on market data.** Independent quote/trade or implementable hedge performance with explicit bid/ask and transaction-cost assumptions; do not use exchange theoretical settlements as if they were executed trades.

**Step 5 — manuscript only after result gates.** A new JCM title, abstract, source/figures and quantitative conclusions **must not reuse** Paper A's lead PI–PM historical-vs-IV comparison or call 189 retrospective parity-anchored dates a true untouched live holdout. The old `paper/jcm/main.tex` is a repackaged Paper A CAS source; do not silently relabel it as Paper B.

## Research decision and stop conditions

No material new model/quote/hedging results yet, hence the proposed JCM manuscript is **not ready**. Reevaluate once exact underlying futures fixings and curve, timestamps, rates and independent evaluation marks have been demonstrated. If independent AAO quotes are unavailable, narrow the empirical contribution; if a genuinely distinct economic result is absent, do not force a second publication.

**Next needed human-side input:** the real local CL LFS payload SHA check. Until that is recorded, proceed only with theoretical and synthetic/documentary work. No more data purchases are authorized. No background experiments or automatic heavy Actions are scheduled.
