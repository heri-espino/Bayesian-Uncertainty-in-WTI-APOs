# Maintainer and agent guide

This page is the short operational contract for future contributors and coding agents.

## Before changing code

1. Read {doc}`architecture` to identify the correct layer.
2. Search {doc}`api/index` for an existing function before implementing a duplicate.
3. Check `research/` for methodological assumptions that the code is expected to preserve.
4. Treat `experiments/` as orchestration and `src/` as the reusable library layer.
5. Preserve deterministic seeds, manifests, and checkpoint semantics in publication experiments.

## Public-function documentation standard

Every public function or class added under `src/` should have a docstring that states, as applicable:

- what scientific object it computes;
- the probability measure or modeling interpretation (`P` versus `Q`);
- parameter meaning and units when not obvious;
- return type and the meaning of returned fields;
- important assumptions or approximations;
- validation or failure conditions;
- whether it is intended for production estimation, diagnostics, or figures only.

Private helpers should begin with `_`. If a helper becomes part of the intended public interface, rename/document it and ensure it appears in the Sphinx API reference.

## Adding a new module

When adding a reusable module under `src/`:

1. Give the module a top-level docstring describing its scientific role.
2. Add type hints to public functions.
3. Add unit tests under `tests/`.
4. Add the module to `docs/api/index.md`.
5. Add a short architecture entry if it introduces a new conceptual layer.
6. Add a usage example to the relevant guide when the interface is not self-evident.
7. Run the documentation build locally with warnings as errors.

## Documentation build

```bash
python -m pip install -r docs/requirements.txt
python -m sphinx -W --keep-going -b html docs docs/_build/html
```

The same build runs in CI. A documentation warning should be treated as a code-quality failure, not ignored.

## API stability

This repository is research software, so the API can evolve. Nevertheless, avoid silent interface changes. When renaming/removing a public function:

- update all internal callers in the same PR;
- update examples and Sphinx references;
- note the change in the PR description;
- preserve a compatibility wrapper when an old result/checkpoint depends on the previous name and the wrapper is inexpensive.

## Data handling

Do not infer economic metadata from folder names when it is encoded in the contract symbol. Keep source-file and source-folder provenance in processed panels so anomalies remain auditable.

Do not interpret `Latest` as a transaction price when volume is zero. In the empirical study it is treated as an EOD market settlement/mark only after validation against an independent CME settlement where available.

Do not commit newly acquired proprietary/raw market data unless redistribution rights have been checked. Code, schemas, hashes, diagnostics, and permitted derived summaries are safer public artifacts.

## Scientific guardrails

The following are not implementation details and should not be changed casually:

- historical `mu` must not be inserted into the baseline risk-neutral pricing dynamics;
- the WTI APO average uses first-nearby CL fixings across the calendar month;
- the empirical market settlement is an external benchmark;
- full-Bayes-versus-plug-in comparisons must not use a circular loss whose target is generated from the same posterior draws;
- strike relevance is time-varying, so contracts are not permanently labeled ATM based on a single date;
- `richest` means data completeness, not liquidity.

If a new model deliberately relaxes one of these guardrails, implement it as a clearly named alternative specification and document the change in both the research design and the API.
