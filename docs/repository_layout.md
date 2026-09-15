# Repository layout

The root is intentionally small and domain-oriented:

```text
.
├── AGENTS.md
├── README.md
├── pyproject.toml
├── environment.yml
├── bayesian_asian_options/
│   └── src/bayesian_asian_options/   # reusable scientific library
├── docs/                              # Sphinx/MyST documentation
├── experiments/                       # reproducible experiment entry points
├── tests/                             # unit/regression/theoretical tests
├── scripts/                           # repository and reproducibility utilities
├── data/                              # source data and auditable data provenance
├── results/                           # generated/checkpointed experiment results
├── paper/                             # manuscript sources and current paper build
├── research/                          # methodological design notes
├── figures/                           # figure artifacts used by the study
├── literature/                        # literature corpus/index
├── requirements/                      # platform-specific optional requirements
└── archive/                           # legacy notebooks/presentation/output artifacts
```

Do not add miscellaneous files to root. Reusable model/data/pricing logic goes into the
installed package; experiment-specific orchestration stays in `experiments/`; historical
or superseded artifacts go under `archive/`.

The structural policy is enforced by `scripts/check_repo_structure.py` and CI. The
normative instructions for coding agents are in the root `AGENTS.md`.
