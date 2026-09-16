# Repository layout

The root is intentionally small and domain-oriented:

```text
.
├── AGENTS.md
├── CONTRIBUTING.md
├── README.md
├── pyproject.toml
├── environment.yml
├── bayesian_asian_options/
│   └── src/bayesian_asian_options/   # reusable scientific library
├── docs/                              # Sphinx/MyST documentation
├── experiments/                       # reproducible experiment entry points
├── tests/                             # unit/regression/theoretical tests
├── scripts/                           # repository and reproducibility utilities
├── data/                              # source data and auditable provenance
│   └── csv/CL/                        # Barchart individual CL histories + expiries
├── results/                           # generated/checkpointed experiment results
├── paper/                             # active JFM manuscript + frozen vendor template
├── research/                          # methodological design notes
├── figures/                           # figure artifacts used by the study
├── literature/                        # literature corpus/index
├── requirements/                      # platform-specific optional requirements
└── archive/                           # superseded notebooks/manuscripts/presentations
```

Do not add miscellaneous files to root. Reusable model/data/pricing logic goes into the
installed package; experiment-specific orchestration stays in `experiments/`; historical
or superseded artifacts go under `archive/`.

## Active versus historical material

`main` is the authoritative current state. Historical development is preserved through the
Git commit/PR history and through `archive/` when a file itself remains useful for provenance.
Feature branches are not an archive and should be deleted after merge or explicit
supersession.

The active manuscript is only `paper/manuscript/`. Older manuscript versions live under
`archive/`. The frozen Wiley template lives under `paper/vendor/` and should not be copied
back to the repository root.

The active reusable Python namespace is only `bayesian_asian_options`. Do not recreate the
old top-level `src/` layout or duplicate reusable modules inside `experiments/`.

## Data boundaries

The empirical data tree intentionally contains different objects:

- `data/csv/<maturity folders>/`: Barchart APO histories;
- `data/csv/CL/`: Barchart individual CL futures histories and `contract_expiries.csv`;
- `data/wti_yahoo/`: local/gitignored Yahoo `CL=F` inference cache;
- `data/rates/treasury/`: local/gitignored Treasury source files.

Do not feed the CL futures CSVs through the APO parser; the two filename/schema families are
handled by separate library modules.

The structural policy is enforced by `scripts/check_repo_structure.py` and CI. The
normative instructions for coding agents are in the root `AGENTS.md`; branch and pull-request
workflow is documented in {doc}`development`.
