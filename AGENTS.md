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

The preserved **Wiley/JFM internal manuscript source** belongs under `paper/manuscript/`; historical drafts belong under `archive/`. **Current journal planning is conditional**: first consider the *Journal of Commodity Markets* only if the 2020–2026 Databento AAO expansion yields defensible new independent-date evidence; the prepared REMEF Word manuscript is the realistic fallback, with JFM a demanding alternative. See `docs/journal_strategy.md`. Do not change manuscript format or claim a final journal decision without author approval. The Wiley NJDv5
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
- in the Barchart histories used by this project, `Latest` is the CME settlement field; preserve the raw source-field name and provenance, and do not reinterpret it as an intraday last trade;
- the current physical-measure inference pilot uses Yahoo `CL=F` only as an explicitly labelled continuous/front-month proxy, with its undocumented historical roll convention recorded as a limitation;
- if a later data source permits contract-reconstructed physical returns, every return spanning a contract switch must be excluded from the volatility likelihood rather than treating contango/backwardation as a one-day WTI return;
- CL last-trade dates used by the fixing map come from the explicit versioned reference table `data/csv/CL/contract_expiries.csv`; do not replace it with a hidden approximate roll rule;
- Yahoo individual-contract pages are optional validation/fallback material only and are not required by the canonical pilot because delisted symbols can disappear;
- discounting is date-specific. The current pilot uses the U.S. Treasury daily par curve and explicitly labels the interpolated-par-yield zero-rate approximation; do not call it a bootstrapped zero/OIS curve;
- `experiments/wti_apo_empirical.py` is the single canonical one-date empirical driver. Multi-date orchestration may delegate to it, but do not recreate parallel `hybrid`/source-specific pricing drivers;
- panel samples must be namespaced by their actual selection rule. In particular, a positive-volume-date sample (all contracts on an active date) is not the same object as a positive-volume-contract sample (only observations with own volume > 0), and one sample must never overwrite another;
- error summaries for a filtered panel must be recomputed from the contract rows retained by that filter; never reuse an MAE/RMSE table calculated on a broader sample;
- run manifests must use repository-relative paths for repository inputs and redact external directory prefixes. Record Git/runtime versions needed for reproducibility without storing workstation user names or hostnames.

Alternative models may relax an invariant only when the alternative is clearly named and
the research design, tests, and API documentation are updated together.

## Data and licensing

The author explicitly requires **backup of the reconstructed AAO source dataset and
reconstructed SQLite state in this VERIFIED PRIVATE GitHub repository using Git LFS**.
For `data/databento/wti_aao_bulk/`, raw `*.dbn.zst` and completed
`derived_private/*.sqlite3` are intentionally Git LFS-tracked. Do not
re-ignore, silently exclude, delete or prevent backing up those files.
Do not store API keys, passwords, user profile secrets or personal credentials in Git.

The author has committed the Barchart CL source histories under `data/csv/CL` for the current
private research workflow. Before making the repository or those raw files public, verify
Barchart redistribution terms. Yahoo continuous-proxy snapshots under `data/wti_yahoo/` and
local Treasury CSVs under `data/rates/treasury/` are workstation caches/source inputs and are
gitignored by default. Their README files, parsers, query metadata, hashes, and derived
scientific outputs remain versioned.

## Critical incident and data backup policy (2026-10-26)

Previously, a sparse-checkout instruction was given while 162 licensed AAO
DBN files and a derived SQLite state were ignored and not uploaded. After the
checkout change, the entire `data/databento` tree disappeared from the user's
Windows VM. This assistant-caused incident must be considered before any future
Git advice. The original data are currently **not available** and have **not**
been re-downloaded or pushed.

**Required:** Include `data/databento/wti_aao_bulk` in sparse checkout
**before reacquisition**, verify `scripts.aao_lfs_preflight`, quote and
explicitly authorize a paid retrieval, reacquire into the tracked raw folder,
verify all 162 original-like DBNs via a NEW acquisition manifest, commit
and push as Git LFS, then rerun analyses and commit the resulting SQLite.
No tool/agent may run sparse-checkout modifications, reset/clean, or prune a
repository that contains *any* as-yet unpushed local research data.
Before saying "backed up", confirm the Git LFS push actually succeeded.
Recovery guide: `research/AAO_RECOVERY_AND_LFS_BACKUP_2026-10-26.md`.
CI must remain lightweight. Paid downloads and heavy experimental steps are
manual-only.

## Current WTI AAO checkpoint and agent handoff (2026-10-25)

Before touching the historical market data or WTI empirical study, read:
`research/CHECKPOINT_2026-10-25_AAO_EXPANSION.md`, `research/AAO_AGENT_TASKS.md`,
`research/AI_HANDOFF.md`, and `docs/journal_strategy.md`. These update the acquisition-status
portion of earlier 2026 planning notes, without invalidating earlier published or validated numerical experiments.

- The author's local VM reported a **completed** compressed Databento `AAO.OPT` acquisition:
  **160 chunks = 80 eligible months × `definition`/`statistics`**, 2020-01 through 2026-09,
  quoted **USD 17.33487324**. The amount actually billed and the 81st missing month are unverified.
  [Historical note] Those original files were not hosted on GitHub and were later lost
  during an unsafe sparse-checkout change. This no longer describes the desired state.
- The next step is **offline inventory**, then instrument-identity, final/theoretical settlement,
  liquidity, degraded-date and Barchart reconciliation. The number of newly eligible pricing
  dates and all expanded-study results are **unknown**.
- Do **not rerun** `experiments.wti_databento_aao_bulk --mode download` by default, nor
  purchase more LO/CL/history without explicit new authorization. Databento's USD 32
  safety threshold is a *quote-based* guard, not a provider-enforced bill cap.
- When filtering `statistics`, verify the actual DBN/DataFrame `stat_type` representation
  before comparing with integer 3; `stat_flags & 1` denotes final settlement and
  `stat_flags & 2` denotes actual (not theoretical), per CME/Databento for GLBX.MDP3.
  These flags do **not** establish an exchange trade or an independent market price.
- Use `ts_ref` as the CME reference trading date; join source instrument definitions
  and normalize actual contract identities rather than using event count or file month.
  Contract-linked settlement is model-derived in some cases (Curran settlement valuation);
  separate actual/theoretical sources and all existing Barchart `Latest` marks.
- Treat 2,381 option rows / 15 previous target dates and 253 external-LO rows / 10 dates
  as prior evidence, not as expanded-history results. Do not mix samples, infer new
  significance from record volume, or use future/same-day IV inputs to fit a forecast.
- Preserve all previously validated results, source files, packages, experiments and
  manuscript formats. Use short-lived isolated PRs for inventory, reconciliation,
  eligible dates, extended forward runs and editorial work, in that order.
- Licensed files, locally stored DPAPI credentials, personal Windows paths, raw
  symbol-level holdings and unapproved data dumps must not be committed or exposed.
  Only license-permitted aggregate diagnostics, redacted manifests, hashes and code.
- Heavy data/paper/figure workflows must be **manual-only**. Light automatic CI is fine.

## New 81-month AAO figure and Elsevier manuscript safeguards

Read `research/AAO_81_MONTH_EXECUTION_PLAN.md`. The acquisition report
now covers **162 locally stored definition/statistics chunks over 81 months**,
with two separate manifests and quoted USD 17.49357489, not verified billing.
The prior 80-month event inventory **must not** be presented as updated
81-month results. Use `scripts.audit_aao_manifests` to verify both ledgers
with SHA256 on the author's VM. `scripts.plot_aao_history_coverage` creates
only a **diagnostic event-coverage figure**, never evidence of unique option
price or out-of-sample pricing performance.

The author's new Elsevier template is under `paper/els-cas-templates/`;
the `paper/jcm/` builder is an isolated manual pre-submission working
draft that reuses earlier verified concise sections. Do not claim the
expanded paper is written, overwrite old JFM/REMEF source, repurpose
old figures as the new sample, or select final journal formatting absent
the contract/date/fixing/IV/backtest/inference gates. Licensed raw data,
local figures and heavy manuscript builds are never automatically
committed or triggered on pushes.

## Enforcement

Run both commands before opening a PR:

```bash
python -m scripts.check_repo_structure
python paper/build.py --check
```

CI also runs these checks, pytest, the empirical panel audit, synthetic validation smoke
tests, and Sphinx with warnings as errors. Structural CI failures must be fixed rather than
bypassed.
