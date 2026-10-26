# Maintainer and agent guide

> **Current agent handoff (2026-10-26):** Read `HANDOFF.md`,
> `research/PAPER_COMPLETION_MASTER_PLAN_2026-10-26.md`,
> `research/AAO_EVIDENCE_LEDGER_2026-10-26.md`,
> `research/AAO_EXPERIMENT_REGISTER_2026-10-26.md`,
> and `research/AAO_AGENT_VERIFICATION_PROTOCOL_2026-10-26.md`.
> Do not merge another agent's PR, buy more data, or change sparse checkout without authorization.

The root `AGENTS.md` is the authoritative operational contract. This page explains how to
apply it while working with the documented API.

**Current research handoff (2026-10-25):** read `research/CHECKPOINT_2026-10-25_AAO_EXPANSION.md`, `research/AAO_AGENT_TASKS.md` and `docs/journal_strategy.md` before working on the newly acquired Databento AAO history. The 160 reported monthly chunks are local-only; the offline inventory, quality audit and new-date validation have not yet been completed. Do not rerun a billable download or silently change the manuscript target.


## Before changing code

1. Read {doc}`architecture`, {doc}`repository_layout`, and {doc}`development`.
2. Search {doc}`api/index` before implementing a function.
3. Check `research/` for scientific assumptions.
4. Install with `python -m pip install -e ".[dev,docs,market]"`.
5. Put reusable logic under `bayesian_asian_options/src/bayesian_asian_options/`; keep `experiments/` as orchestration.
6. Preserve deterministic seeds, manifests, and checkpoint semantics.
7. Start new work from current `main`; do not revive an already merged feature branch.

## Public-function standard

Every public package function/class must document the scientific object, P/Q
interpretation where relevant, parameters/units, return meaning, assumptions, validation
conditions, and whether it is intended for estimation, diagnostics, or figures. Add type
hints, tests, and the module to `docs/api/index.md` in the same change.

Private helpers begin with `_`. Avoid silent interface changes; update all callers,
examples, tests, and Sphinx references together.

## Branch and PR hygiene

`main` is the only long-lived branch. Use one short-lived branch for one coherent change,
merge through a pull request, then delete the feature branch. Superseded work should be
closed explicitly and the branch deleted once its useful content is preserved by another
PR or under `archive/`.

Do not use branch names as a provenance system. Git history, closed/merged PRs, manifests,
and `archive/` provide provenance without leaving obsolete development lines active.

## Required checks

```bash
python -m scripts.check_repo_structure
python paper/build.py --check
python -m pytest -q
python -m sphinx -W --keep-going -b html docs docs/_build/html
```

CI runs the same structural, test, documentation, and research smoke checks. Do not bypass
a failing structural check by adding path hacks or duplicate modules.

## Data and scientific guardrails

Preserve source-file/folder provenance, do not equate zero-volume `Latest` marks with
transactions, and verify redistribution rights before publishing third-party raw data. The
P/Q separation, WTI first-nearby payoff mechanics, external market benchmark, non-circular
Bayesian comparison, time-varying moneyness, and `richest`-versus-liquidity distinction are
scientific invariants unless a separately named alternative model is introduced.

For the current empirical pilot, Barchart CL histories under `data/csv/CL` define the
valuation-date futures curve, while Yahoo `CL=F` is only a labelled physical-return proxy.
These roles must remain distinct.
