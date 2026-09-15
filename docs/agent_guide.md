# Maintainer and agent guide

The root `AGENTS.md` is the authoritative operational contract. This page explains how to
apply it while working with the documented API.

## Before changing code

1. Read {doc}`architecture` and {doc}`repository_layout`.
2. Search {doc}`api/index` before implementing a function.
3. Check `research/` for scientific assumptions.
4. Install with `python -m pip install -e ".[dev,docs,market]"`.
5. Put reusable logic under `bayesian_asian_options/src/bayesian_asian_options/`; keep `experiments/` as orchestration.
6. Preserve deterministic seeds, manifests, and checkpoint semantics.

## Public-function standard

Every public package function/class must document the scientific object, P/Q
interpretation where relevant, parameters/units, return meaning, assumptions, validation
conditions, and whether it is intended for estimation, diagnostics, or figures. Add type
hints, tests, and the module to `docs/api/index.md` in the same change.

Private helpers begin with `_`. Avoid silent interface changes; update all callers,
examples, tests, and Sphinx references together.

## Required checks

```bash
python -m scripts.check_repo_structure
python -m pytest -q
python -m sphinx -W --keep-going -b html docs docs/_build/html
```

CI runs the same structural, test, documentation, and research smoke checks. Do not bypass
a failing structural check by adding path hacks or duplicate modules.

## Data and scientific guardrails

Preserve source-file/folder provenance, do not equate zero-volume `Latest` marks with
transactions, and do not commit proprietary data without redistribution rights. The P/Q
separation, WTI first-nearby payoff mechanics, external market benchmark, non-circular
Bayesian comparison, time-varying moneyness, and `richest`-versus-liquidity distinction
are scientific invariants unless a separately named alternative model is introduced.
