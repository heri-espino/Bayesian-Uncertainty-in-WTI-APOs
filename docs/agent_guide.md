# Maintainer and agent guide

The root `AGENTS.md` is the authoritative operational contract. This page explains how to
apply it while working with the documented API.

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
