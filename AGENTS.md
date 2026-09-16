# Repository contract for coding agents and maintainers

This file is normative. Future coding agents and maintainers must preserve the repository
architecture unless a deliberate migration is documented and completed atomically.

## Read before editing

Before writing code, read `docs/index.md`, `docs/architecture.md`, `docs/api/index.md`,
`docs/agent_guide.md`, `docs/development.md`, `paper/README.md`, and the relevant files under
`research/`. Search the Sphinx API reference before implementing a new function.

## Required package structure

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

## Branch and pull-request lifecycle

`main` is the only long-lived development branch. New work starts from current `main` in a
short-lived, narrowly scoped feature branch. Do not revive or reuse a branch after its PR
has been merged.

After a PR is merged, delete its remote branch. If work is explicitly superseded, close the
old PR, confirm that its useful changes are preserved elsewhere, and delete that branch as
well. Git history, closed/merged PRs, manifests, and `archive/` are the provenance record;
obsolete branches are not an archival mechanism.

Prefer branch names with a clear role such as `feature/`, `fix/`, `paper/`, `data/`, or
`chore/`. Keep one coherent scientific or infrastructure change per PR.

## Manuscript structure is also normative

The active paper targets the **Journal of Futures Markets**. Manuscript source belongs only
under `paper/manuscript/`; historical paper drafts belong under `archive/`. The Wiley NJDv5
bundle supplied by the author is frozen under `paper/vendor/wiley_njd_v5/` and must not be
edited during ordinary manuscript work.

The internal manuscript must preserve the selected Wiley simulation unless the author
explicitly requests a format change:

```tex
\documentclass[HARVARD,Utopia2COL]{WileyNJDv5}
```

This means Harvard references, Utopia, and two columns. The canonical build command is:

```bash
python paper/build.py
```

Do not add an alternative ad-hoc LaTeX build script or compile into the source directory.
Generated TeX intermediates belong under the gitignored `paper/build/`; the canonical
builder moves the final, gitignored PDF to `paper/espino_2026_bayess-on-wti.pdf`. CI uses
`python paper/build.py --check` to detect format or layout drift without requiring a full
TeX installation.

When editing the manuscript, never invent empirical results to fill a narrative gap. An
empirical number enters the paper only when it can be traced to a versioned experiment,
configuration, data provenance, seed where relevant, and code commit. Explicit TODO or
working-draft language is preferable to an unsupported result.

## Root-directory hygiene

Do not drop vendor bundles, notebooks, ad-hoc scripts, PDFs, temporary outputs, or downloaded
files in the repository root. Use the existing domain directories: `archive/`, `data/`,
`docs/`, `experiments/`, `figures/`, `literature/`, `paper/`, `research/`, `results/`,
`scripts/`, and `tests/`. Third-party manuscript templates belong below `paper/vendor/`.
Generated caches/build products must remain ignored.

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

For the empirical WTI pipeline, additionally preserve these source/measurement rules:

- the canonical valuation-date CL curve comes from the committed Barchart individual-contract `Daily Prices` histories under `data/csv/CL`; do not silently substitute Yahoo `CL=F` for that contractual term structure;
- Barchart `Latest` is retained as the source field and may be used as an end-of-day settlement proxy, but it must not be called an official CME settlement without separate validation;
- the current physical-measure inference pilot uses Yahoo `CL=F` only as an explicitly labelled continuous/front-month proxy, with its undocumented historical roll convention recorded as a limitation;
- if a later data source permits contract-reconstructed physical returns, every return spanning a contract switch must be excluded from the volatility likelihood rather than treating contango/backwardation as a one-day WTI return;
- CL last-trade dates used by the fixing map come from the explicit versioned reference table `data/csv/CL/contract_expiries.csv`; do not replace it with a hidden approximate roll rule;
- Yahoo individual-contract pages are optional validation/fallback material only and are not required by the canonical pilot because delisted symbols can disappear;
- discounting is date-specific. The current pilot uses the U.S. Treasury daily par curve and explicitly labels the interpolated-par-yield zero-rate approximation; do not call it a bootstrapped zero/OIS curve;
- `experiments/wti_apo_empirical.py` is the single canonical one-date empirical driver. Multi-date orchestration may delegate to it, but do not recreate parallel `hybrid`/source-specific pricing drivers;
- run manifests must use repository-relative paths for repository inputs and redact external directory prefixes. Record Git/runtime versions needed for reproducibility without storing workstation user names or hostnames.

Alternative models may relax an invariant only when the alternative is clearly named and
the research design, tests, and API documentation are updated together.

## Data and licensing

Do not commit newly acquired proprietary market data until redistribution rights have been
verified. Preserve source provenance and prefer code, schemas, hashes, diagnostics, and
permitted derived summaries.

The author has committed the Barchart CL source histories under `data/csv/CL` for the current
private research workflow. Before making the repository or those raw files public, verify
Barchart redistribution terms. Yahoo continuous-proxy snapshots under `data/wti_yahoo/` and
local Treasury CSVs under `data/rates/treasury/` are workstation caches/source inputs and are
gitignored by default. Their README files, parsers, query metadata, hashes, and derived
scientific outputs remain versioned.

## Enforcement

Run both commands before opening a PR:

```bash
python -m scripts.check_repo_structure
python paper/build.py --check
```

CI also runs these checks, pytest, the empirical panel audit, synthetic validation smoke
tests, and Sphinx with warnings as errors. Structural CI failures must be fixed rather than
bypassed.
