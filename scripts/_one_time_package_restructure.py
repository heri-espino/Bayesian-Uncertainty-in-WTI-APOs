"""One-time repository migration to the editable-install package layout.

This file is executed by the temporary refactor workflow and deletes itself before
committing the migrated tree. It intentionally uses only the Python standard library.
"""
from __future__ import annotations

from pathlib import Path
import re
import shutil

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = "bayesian_asian_options"
PACKAGE_ROOT = ROOT / PACKAGE
PACKAGE_SRC = PACKAGE_ROOT / "src" / PACKAGE


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.rstrip() + "\n", encoding="utf-8")


def move(src: str, dst: str) -> None:
    source = ROOT / src
    target = ROOT / dst
    if not source.exists():
        return
    target.parent.mkdir(parents=True, exist_ok=True)
    if target.exists():
        raise RuntimeError(f"target already exists: {target}")
    shutil.move(str(source), str(target))


def migrate_python_imports() -> None:
    roots = [PACKAGE_SRC, ROOT / "experiments", ROOT / "tests", ROOT / "scripts"]
    for base in roots:
        if not base.exists():
            continue
        for path in base.rglob("*.py"):
            text = path.read_text(encoding="utf-8")
            text = text.replace("from src.", f"from {PACKAGE}.")
            text = text.replace("import src.", f"import {PACKAGE}.")
            text = text.replace("``src.", f"``{PACKAGE}.")
            path.write_text(text, encoding="utf-8")


def migrate_active_text_paths() -> None:
    roots = [ROOT / "docs", ROOT / "research", ROOT / "paper"]
    files = [ROOT / "README.md"]
    for base in roots:
        if base.exists():
            files.extend(
                path
                for path in base.rglob("*")
                if path.is_file() and path.suffix.lower() in {".md", ".tex", ".txt"}
            )
    for path in files:
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8", errors="strict")
        text = text.replace("from src.", f"from {PACKAGE}.")
        text = text.replace("`src.", f"`{PACKAGE}.")
        text = text.replace("``src.", f"``{PACKAGE}.")
        text = text.replace("src/", f"{PACKAGE}/src/{PACKAGE}/")
        text = text.replace("reporte/", "paper/")
        path.write_text(text, encoding="utf-8")


def main() -> None:
    if not (ROOT / "src").is_dir():
        raise RuntimeError("expected legacy src/ directory")

    # 1. Promote reusable scientific code into a conventional src-layout package.
    PACKAGE_SRC.parent.mkdir(parents=True, exist_ok=True)
    shutil.move(str(ROOT / "src"), str(PACKAGE_SRC))
    write(
        PACKAGE_SRC / "__init__.py",
        '''"""Bayesian parameter-uncertainty and Asian-option research library.

Reusable scientific code lives in this package. Experiment orchestration belongs in
``experiments/`` and must depend on the package rather than the reverse.
"""

__version__ = "0.1.0"
''',
    )
    migrate_python_imports()

    # 2. Move active manuscript sources and legacy top-level artifacts out of root.
    move("reporte", "paper")
    move("notebook.ipynb", "archive/notebooks/notebook.ipynb")
    move("notebook.py", "archive/notebooks/notebook.py")
    move("old_notebook.ipynb", "archive/notebooks/old_notebook.ipynb")
    move("presentacion", "archive/presentation")
    move("Valuación Bayesiana de Opciones Asiáticas.pdf", "archive/legacy_outputs/Valuación Bayesiana de Opciones Asiáticas.pdf")
    move("14.2", "archive/misc/14.2")
    if (ROOT / ".DS_Store").exists():
        (ROOT / ".DS_Store").unlink()

    # Requirements are centralized in pyproject.toml. Keep only the platform-specific
    # CuPy hint in a dedicated requirements directory.
    write(
        ROOT / "requirements" / "gpu-cuda12.txt",
        '''# Optional NVIDIA/CUDA acceleration for bayesian_asian_options.accelerated_pricing.
# Verify the workstation driver with nvidia-smi first. If the workstation uses a
# different CUDA major version, install the matching CuPy distribution instead.
cupy-cuda12x
''',
    )
    for old in ("requirements-gpu.txt", "requirements-publication.txt"):
        path = ROOT / old
        if path.exists():
            path.unlink()

    migrate_active_text_paths()

    # 3. Packaging metadata: editable install from repository root.
    write(
        ROOT / "pyproject.toml",
        '''[build-system]
requires = ["setuptools>=75", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "bayesian-asian-options"
version = "0.1.0"
description = "Research library for Bayesian parameter uncertainty and risk-neutral Asian-option pricing."
readme = "README.md"
requires-python = ">=3.11"
authors = [{name = "Heriberto Espino Montelongo"}]
dependencies = [
  "numpy>=2.0",
  "pandas>=2.2",
  "scipy>=1.13",
]

[project.optional-dependencies]
market = ["yfinance>=1.4"]
dev = [
  "pytest>=8.0",
  "psutil>=6.0",
  "matplotlib>=3.9",
]
docs = [
  "sphinx>=8.0",
  "myst-parser>=4.0",
  "furo>=2024.8.6",
]

[tool.setuptools]
package-dir = {"" = "bayesian_asian_options/src"}
include-package-data = false

[tool.setuptools.packages.find]
where = ["bayesian_asian_options/src"]
include = ["bayesian_asian_options*"]

[tool.pytest.ini_options]
testpaths = ["tests"]
addopts = "-ra"
''',
    )
    write(
        PACKAGE_ROOT / "README.md",
        '''# Python library boundary

All reusable scientific logic belongs in `src/bayesian_asian_options/`.

Install the repository from its root with:

```bash
python -m pip install -e .
```

Experiment drivers, manuscript code, one-off data conversions, and generated results do
not belong in this package. See the root `AGENTS.md` and `docs/architecture.md` before
adding modules.
''',
    )

    # 4. Make the structural contract explicit for future coding agents.
    write(
        ROOT / "AGENTS.md",
        '''# Repository contract for coding agents and maintainers

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
''',
    )

    write(
        ROOT / "scripts" / "check_repo_structure.py",
        '''"""Validate the repository/package architecture expected by maintainers and agents."""
from __future__ import annotations

from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
PACKAGE_DIR = ROOT / "bayesian_asian_options" / "src" / "bayesian_asian_options"
API_DOC = ROOT / "docs" / "api" / "index.md"

REQUIRED = [
    ROOT / "AGENTS.md",
    ROOT / "pyproject.toml",
    ROOT / "docs" / "index.md",
    ROOT / "docs" / "architecture.md",
    PACKAGE_DIR / "__init__.py",
]
FORBIDDEN_ROOT = [
    "src",
    "reporte",
    "presentacion",
    "notebook.ipynb",
    "notebook.py",
    "old_notebook.ipynb",
    ".DS_Store",
]
LEGACY_IMPORT = re.compile(r"(^|\\n)\\s*(?:from|import)\\s+src(?:\\.|\\s|$)")


def main() -> None:
    errors: list[str] = []
    for path in REQUIRED:
        if not path.exists():
            errors.append(f"missing required path: {path.relative_to(ROOT)}")
    for name in FORBIDDEN_ROOT:
        if (ROOT / name).exists():
            errors.append(f"forbidden root-level path returned: {name}")

    scan_roots = [PACKAGE_DIR, ROOT / "experiments", ROOT / "tests", ROOT / "scripts"]
    for base in scan_roots:
        if not base.exists():
            continue
        for path in base.rglob("*.py"):
            text = path.read_text(encoding="utf-8")
            if LEGACY_IMPORT.search(text):
                errors.append(f"legacy 'src' import in {path.relative_to(ROOT)}")

    if PACKAGE_DIR.exists() and API_DOC.exists():
        api = API_DOC.read_text(encoding="utf-8")
        modules = sorted(
            path.stem for path in PACKAGE_DIR.glob("*.py") if path.name != "__init__.py"
        )
        for module in modules:
            dotted = f"bayesian_asian_options.{module}"
            if dotted not in api:
                errors.append(f"public module missing from Sphinx API reference: {dotted}")

    if errors:
        raise SystemExit("Repository structure check failed:\n- " + "\n- ".join(errors))
    print("Repository structure check passed")


if __name__ == "__main__":
    main()
''',
    )

    # 5. Documentation now describes the installed package, not a generic src namespace.
    write(
        ROOT / "docs" / "index.md",
        '''# Bayesian Asian Options Research Library

This documentation is the operational reference for the reusable Python package and the
research workflows built on top of it. It is intended for researchers, maintainers, and
future coding agents who need to discover existing functionality without reading the
entire source tree.

The canonical Python namespace is `bayesian_asian_options`. The repository uses a
standard editable-install source layout:

```text
bayesian_asian_options/src/bayesian_asian_options/
```

Install from the repository root before running experiments or building documentation:

```bash
python -m pip install -e ".[dev,docs,market]"
```

## Design principles

- Historical inference is performed under the physical measure $\\mathbb P$.
- Derivative valuation is performed under the risk-neutral measure $\\mathbb Q$.
- The physical drift $\\mu$ is not propagated into Black--Scholes no-arbitrage prices.
- Synthetic validation and the empirical CME WTI Average Price Option application are separate experimental layers.
- Raw market-data provenance and data-quality diagnostics remain distinct from economic sample-selection rules.
- Representative contracts are selected only for figures/case studies; they do not define the estimation sample.

## Documentation map

```{toctree}
:maxdepth: 2
:caption: User guide

quickstart
architecture
repository_layout
empirical_wti
agent_guide
api/index
```

## Build the documentation

```bash
python -m sphinx -W --keep-going -b html docs docs/_build/html
```

The package must already be installed editable. CI builds the documentation with warnings
as errors, so broken API references fail before merge.
''',
    )
    write(
        ROOT / "docs" / "repository_layout.md",
        '''# Repository layout

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
''',
    )
    write(
        ROOT / "docs" / "architecture.md",
        '''# Architecture

The repository is an installed research library plus reproducible experiment entry
points. Reusable scientific logic lives in
`bayesian_asian_options/src/bayesian_asian_options/`. `experiments/` orchestrates data,
parameter grids, checkpoints, and outputs without duplicating model implementations.

## Core layers

### Physical-measure inference

`bayesian_asian_options.bayesian_gbm`
: GBM returns under $\\mathbb P$, posterior evaluation in `(mu, log_sigma)`, Random-Walk Metropolis, and GBM MLEs.

### Generic Asian-option pricing

`bayesian_asian_options.asian_pricing`
: Reference risk-neutral arithmetic-Asian pricing, geometric control variate, and posterior-volatility propagation.

`bayesian_asian_options.accelerated_pricing`
: Bounded-memory NumPy/CuPy pricing used for large grids.

`bayesian_asian_options.asian_futures_pricing`
: Lognormal futures-price Asian wrappers under $\\mathbb Q$.

### Synthetic validation

`bayesian_asian_options.synthetic_validation`
: Reusable deterministic, theoretical, and stochastic checks. Publication-scale orchestration remains in `experiments/`.

### WTI market-data ingestion

`bayesian_asian_options.barchart_apo`
: Barchart WTI APO filename decoding, tidy histories, quality audits, effective moneyness, filters, and representative-contract ranking.

`bayesian_asian_options.wti_yahoo`
: Yahoo `CL=F` continuous/front-month proxy utilities. The proxy is not described as an exact reconstructed first-nearby series.

### CME WTI APO mechanics

`bayesian_asian_options.wti_first_nearby`
: First-nearby CL mapping from explicit exchange last-trade dates.

`bayesian_asian_options.wti_apo_pricing`
: CME-style calls/puts from realized fixings plus the futures term structure for remaining fixings.

`bayesian_asian_options.volatility_regimes`
: Rolling realized volatility and data-driven low/medium/high regimes.

## Dependency direction

```text
experiments/  --->  bayesian_asian_options
                         |
                         +--> NumPy / pandas / SciPy
```

The package must never import `experiments.*`. A function reused by more than one
experiment belongs in the package and must be added to the API documentation and tests.

## Scientific invariants

1. `mu` belongs to inference under $\\mathbb P$ and does not enter baseline pricing under $\\mathbb Q$.
2. Posterior uncertainty is propagated only through parameters that matter for the pricing model, principally `sigma` in the baseline.
3. The empirical WTI APO payoff uses calendar-month first-nearby CL settlements, not one fixed futures contract.
4. Historical market settlements are external benchmarks; posterior-generated prices cannot define truth.
5. Data completeness, liquidity, figure ranking, and estimation-sample inclusion are separate concepts.
6. Long runs remain reproducible/restartable through explicit seeds, manifests, hashes, and checkpoints.

See `AGENTS.md` for the mandatory maintenance policy.
''',
    )
    write(
        ROOT / "docs" / "agent_guide.md",
        '''# Maintainer and agent guide

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
''',
    )

    # Existing user guides only need canonical import names and paths after migration.
    for path in [ROOT / "docs" / "quickstart.md", ROOT / "docs" / "empirical_wti.md"]:
        text = path.read_text(encoding="utf-8")
        text = text.replace("from src.", f"from {PACKAGE}.")
        text = text.replace("`src.", f"`{PACKAGE}.")
        text = text.replace("src/", f"{PACKAGE}/src/{PACKAGE}/")
        if path.name == "quickstart.md":
            text = text.replace(
                "conda activate asian-options\n```",
                "conda activate asian-options\npython -m pip install -e \".[dev,docs,market]\"\n```",
            )
        path.write_text(text, encoding="utf-8")

    api_sections = [
        ("Bayesian GBM inference", "bayesian_gbm"),
        ("Generic Asian pricing", "asian_pricing"),
        ("Accelerated pricing", "accelerated_pricing"),
        ("Futures-style Asian pricing", "asian_futures_pricing"),
        ("Synthetic validation utilities", "synthetic_validation"),
        ("Barchart WTI APO ingestion", "barchart_apo"),
        ("WTI first-nearby mapping", "wti_first_nearby"),
        ("CME-style WTI APO pricing", "wti_apo_pricing"),
        ("Volatility regimes", "volatility_regimes"),
        ("Yahoo WTI auxiliary data utilities", "wti_yahoo"),
    ]
    api = [
        "# API reference",
        "",
        "This is the canonical inventory of reusable public functions/classes. It is generated from package docstrings at Sphinx build time.",
        "",
    ]
    for title, module in api_sections:
        api.extend(
            [
                f"## {title}",
                "",
                f"```{{automodule}} {PACKAGE}.{module}",
                ":members:",
                ":show-inheritance:",
                "```",
                "",
            ]
        )
    write(ROOT / "docs" / "api" / "index.md", "\n".join(api))

    write(
        ROOT / "docs" / "conf.py",
        '''from __future__ import annotations

project = "Bayesian Asian Options Research Library"
author = "Heriberto Espino Montelongo"
copyright = "2026, Heriberto Espino Montelongo"

extensions = [
    "myst_parser",
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "sphinx.ext.intersphinx",
]

autosummary_generate = True
autodoc_member_order = "bysource"
autodoc_typehints = "description"
autodoc_preserve_defaults = True
napoleon_google_docstring = True
napoleon_numpy_docstring = True
napoleon_use_param = True
napoleon_use_rtype = True

myst_enable_extensions = ["colon_fence", "deflist", "dollarmath", "fieldlist"]
source_suffix = {".rst": "restructuredtext", ".md": "markdown"}
master_doc = "index"
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

html_theme = "furo"
html_title = project
html_static_path: list[str] = []

intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "numpy": ("https://numpy.org/doc/stable/", None),
    "pandas": ("https://pandas.pydata.org/docs/", None),
}
''',
    )

    # 6. Conda remains useful for workstation provisioning; pip editable install is the
    # canonical project installation step.
    write(
        ROOT / "environment.yml",
        '''name: asian-options
channels:
  - conda-forge
dependencies:
  - python=3.11
  - pip
  - numpy>=2.0
  - pandas>=2.2
  - scipy>=1.13
  - matplotlib>=3.9
  - pytest>=8.0
  - psutil>=6.0
  - yfinance>=1.4
''',
    )

    # 7. Modern root README: entry point, installation, architecture, reproducibility.
    write(
        ROOT / "README.md",
        '''# Bayesian parameter uncertainty for Asian options

Research code and manuscript for Bayesian parameter uncertainty in arithmetic Asian-option
valuation, with a real-market CME WTI Average Price Option application. The publication
strategy currently targets the **Journal of Futures Markets** first.

## Scientific boundary: P versus Q

Historical returns are modeled under the physical measure $\\mathbb P$,

$$
dS_t = \\mu S_t\\,dt + \\sigma S_t\\,dW_t^{\\mathbb P},
$$

while derivative valuation is performed under $\\mathbb Q$,

$$
dS_t = (r-q)S_t\\,dt + \\sigma S_t\\,dW_t^{\\mathbb Q}.
$$

The physical drift $\\mu$ is therefore not inserted into the baseline no-arbitrage pricing
dynamics. Posterior uncertainty in parameters relevant to pricing, principally $\\sigma$ in
the current baseline, is propagated into the option value.

## Install the research library

The reusable code is a proper editable-install package rather than a generic root `src`
namespace:

```bash
conda env create -f environment.yml
conda activate asian-options
python -m pip install -e ".[dev,docs,market]"
```

Then import directly:

```python
from bayesian_asian_options.bayesian_gbm import random_walk_metropolis_gbm
from bayesian_asian_options.asian_pricing import asian_arithmetic_call_mc
from bayesian_asian_options.wti_apo_pricing import wti_average_price_option_mc
```

CuPy is optional and platform-specific. For a CUDA-12 workstation, see
`requirements/gpu-cuda12.txt` after checking `nvidia-smi`.

## Repository map

```text
bayesian_asian_options/src/bayesian_asian_options/  reusable scientific library
docs/                                                Sphinx/MyST documentation
experiments/                                         reproducible experiment drivers
tests/                                               automated tests
scripts/                                             reproducibility/repository utilities
data/                                                source data and provenance
results/                                             generated/checkpointed outputs
paper/                                               current manuscript sources
research/                                            methodological design notes
figures/                                             study figures
literature/                                          literature corpus/index
archive/                                             legacy notebooks/presentation/output
```

The root `AGENTS.md` is mandatory reading for coding agents and maintainers. It defines
where new code belongs and the scientific guardrails that must be preserved.

## Documentation and API discovery

Build the documentation after editable installation:

```bash
python -m sphinx -W --keep-going -b html docs docs/_build/html
```

Start at `docs/index.md`. `docs/api/index.md` is generated from package docstrings and is
the canonical function/class inventory. New reusable modules must be documented there.

## Reproducible validation

Quick synthetic smoke validation:

```bash
python -m experiments.synthetic_validation --quick
```

Build/audit the committed WTI APO panel:

```bash
python -m experiments.build_wti_apo_panel --input-dir data/csv --output-dir results/wti_apo
```

Run the repository architecture check:

```bash
python -m scripts.check_repo_structure
```

Long-running synthetic experiments remain checkpointed and resumable. See
`research/COMPUTE.md` and the experiment modules for presets, seeds, configuration
fingerprints, and hardware manifests.

## WTI empirical application

The CME WTI Average Price Option application does not treat one fixed futures contract as
the Asian underlying. The empirical pipeline reconstructs calendar-month first-nearby CL
fixings, separates realized and remaining fixings, uses the observed term structure for
remaining expectations, defines moneyness observation by observation relative to the
expected final average, and compares Full Bayes / posterior-mean / MAP / MLE prices with
observed market settlements.

All downloaded strikes are retained in the raw panel. Liquidity/sample filters and
representative-contract rankings are separate operations. In particular,
`richest_option_series.csv` is a data-completeness diagnostic, not a liquidity ranking.
See `docs/empirical_wti.md` and `research/EMPIRICAL_WTI_DESIGN.md`.

## Manuscript and legacy material

Active manuscript sources live in `paper/`. Legacy exploratory notebooks, the prior
presentation, and superseded output artifacts live under `archive/` so they remain
traceable without cluttering the active project root.
''',
    )

    # 8. CI installs the package exactly as researchers do and enforces the layout.
    write(
        ROOT / ".github" / "workflows" / "tests.yml",
        '''name: tests

on:
  push:
    branches: [main]
  pull_request:

jobs:
  pytest:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"
      - name: Install editable research package
        run: |
          python -m pip install --upgrade pip
          python -m pip install -e ".[dev,docs,market]"
      - name: Enforce repository architecture
        run: python -m scripts.check_repo_structure
      - name: Smoke-test installed package namespace
        run: python -c "import bayesian_asian_options as bao; print(bao.__version__)"
      - name: Compile library, experiments, and scripts
        run: >-
          python -m compileall -q
          bayesian_asian_options/src/bayesian_asian_options
          experiments
          scripts
      - name: Run tests
        run: python -m pytest -q
      - name: Build Sphinx API documentation
        run: python -m sphinx -W --keep-going -b html docs /tmp/sphinx-html
      - name: Audit committed WTI APO histories
        run: >-
          python -m experiments.build_wti_apo_panel
          --input-dir data/csv
          --output-dir /tmp/wti_apo
      - name: Run system probe without requiring NVIDIA/CuPy
        run: python -m scripts.system_probe --output-dir /tmp/system_probe
      - name: Run reproducible synthetic validation smoke test
        run: >-
          python -m experiments.synthetic_validation
          --quick
          --parameter-replications 5
          --posterior-replications 1
          --output-dir /tmp/synthetic_validation
      - name: Analyze committed extreme experiment
        run: >-
          python -m experiments.analyze_extreme_results
          --output /tmp/extreme_analysis.json
''',
    )

    # 9. Ignore package/LaTeX build products.
    gitignore = (ROOT / ".gitignore").read_text(encoding="utf-8")
    additions = '''\n# Python package build products\nbuild/\ndist/\n\n# LaTeX build products\n*.aux\n*.bbl\n*.bcf\n*.blg\n*.fdb_latexmk\n*.fls\n*.log\n*.out\n*.run.xml\n*.synctex.gz\n'''
    if "# Python package build products" not in gitignore:
        (ROOT / ".gitignore").write_text(gitignore.rstrip() + additions + "\n", encoding="utf-8")

    # 10. A canonical-import regression test makes editable packaging part of the test suite.
    write(
        ROOT / "tests" / "test_package_imports.py",
        '''import bayesian_asian_options as bao
from bayesian_asian_options import (
    accelerated_pricing,
    asian_futures_pricing,
    asian_pricing,
    barchart_apo,
    bayesian_gbm,
    synthetic_validation,
    volatility_regimes,
    wti_apo_pricing,
    wti_first_nearby,
    wti_yahoo,
)


def test_canonical_package_namespace_is_importable() -> None:
    assert bao.__version__ == "0.1.0"
    assert callable(bayesian_gbm.random_walk_metropolis_gbm)
    assert callable(asian_pricing.asian_arithmetic_call_mc)
    assert callable(accelerated_pricing.asian_arithmetic_call_mc_chunked)
    assert callable(asian_futures_pricing.asian_futures_arithmetic_call_mc)
    assert callable(barchart_apo.build_apo_panel)
    assert callable(wti_first_nearby.assign_first_nearby_contract)
    assert callable(wti_apo_pricing.wti_average_price_option_mc)
    assert callable(volatility_regimes.realized_volatility)
    assert callable(wti_yahoo.prepare_wti_model_sample)
    assert callable(synthetic_validation.risk_neutral_martingale_check)
''',
    )

    # Remove temporary migration machinery from the final tree.
    temp_workflow = ROOT / ".github" / "workflows" / "package-refactor-once.yml"
    if temp_workflow.exists():
        temp_workflow.unlink()
    Path(__file__).unlink()


if __name__ == "__main__":
    main()
