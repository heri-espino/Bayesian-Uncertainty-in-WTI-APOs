# Repository contract for coding agents and maintainers

This file is normative. Future coding agents and maintainers must preserve the repository
architecture unless a deliberate migration is documented and completed atomically.

## Read before editing

Before writing code, read `docs/index.md`, `docs/architecture.md`, `docs/api/index.md`,
`docs/agent_guide.md`, and the relevant files under `research/`. Search the Sphinx API
reference before implementing a new function.

## Required structure

Reusable scientific code lives only under:

```text
bayesian_asian_options/
└── src/
    └── bayesian_asian_options/
```

The package is installed from the repository root with `python -m pip install -e .`.
Use imports such as `from bayesian_asian_options.bayesian_gbm import ...`. Do not create
a new top-level `src/`, do not use `sys.path` hacks, and do not introduce the generic
`src` import namespace.

`experiments/` contains reproducible orchestration only. If code becomes reusable across
experiments, move it into the library, add tests, and document it. The library must never
import from `experiments/`.

## Public API rule

Every new public library function/class/module must ship in the same change with:

1. a scientific docstring and type hints;
2. tests under `tests/`;
3. an entry in `docs/api/index.md`;
4. architecture or usage documentation when the interface/model is not obvious;
5. a passing Sphinx build with warnings treated as errors.

Private helpers begin with `_`. Do not silently rename or remove public APIs; update all
callers, tests, examples, and docs in the same change.

## Root-directory hygiene

Do not drop notebooks, ad-hoc scripts, PDFs, temporary outputs, or downloaded files in the
repository root. Use the existing domain directories: `archive/`, `data/`, `docs/`,
`experiments/`, `figures/`, `literature/`, `paper/`, `research/`, `results/`, `scripts/`,
and `tests/`. Generated caches/build products must remain ignored.

## Scientific invariants

Do not change these silently:

- historical inference is under P and derivative valuation is under Q;
- physical drift `mu` does not enter the baseline risk-neutral Black--Scholes pricing dynamics;
- CME WTI APO pricing uses calendar-month first-nearby CL fixings, including realized fixings and the remaining term structure;
- observed market settlements are external empirical benchmarks;
- Full-Bayes/plugin comparisons must not use circular posterior-generated targets;
- moneyness is observation-specific, not permanently assigned from one market date;
- `richest` means data completeness, not liquidity or economic importance;
- deterministic seeds, manifests, hashes, and restartable checkpoints are part of the reproducibility contract.

Alternative models may relax an invariant only when the alternative is clearly named and
the research design, tests, and API documentation are updated together.

## Data and licensing

Do not commit newly acquired proprietary market data until redistribution rights have been
verified. Preserve source provenance and prefer code, schemas, hashes, diagnostics, and
permitted derived summaries.

## Enforcement

Run `python -m scripts.check_repo_structure` before opening a PR. CI also runs this check,
pytest, the empirical panel audit, synthetic validation smoke tests, and Sphinx with
warnings as errors. Structural CI failures must be fixed rather than bypassed.
