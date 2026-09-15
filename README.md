# Bayesian parameter uncertainty for Asian options

Research library, reproducible experiments, data pipeline, and manuscript for Bayesian
parameter uncertainty in arithmetic Asian-option valuation, with an empirical application
to CME WTI Average Price Options. The publication strategy targets the **Journal of Futures
Markets** first.

## Scientific boundary: P versus Q

Historical returns are modeled under the physical measure $\mathbb P$,

$$
dS_t = \mu S_t\,dt + \sigma S_t\,dW_t^{\mathbb P},
$$

while derivative valuation is performed under $\mathbb Q$,

$$
dS_t = (r-q)S_t\,dt + \sigma S_t\,dW_t^{\mathbb Q}.
$$

The physical drift $\mu$ is therefore not inserted into the baseline no-arbitrage pricing
dynamics. Posterior uncertainty in parameters relevant to pricing, principally $\sigma$ in
the current baseline, is propagated into the option value.

## Install the research library

```bash
conda env create -f environment.yml
conda activate asian-options
python -m pip install -e ".[dev,docs,market]"
```

Representative imports:

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
docs/                                                Sphinx/MyST API and methodology docs
experiments/                                         reproducible experiment drivers
tests/                                               automated tests
scripts/                                             repository/reproducibility utilities
data/                                                source data and provenance
results/                                             experiment outputs and checkpoints
paper/manuscript/                                    active JFM LaTeX manuscript
paper/vendor/wiley_njd_v5/                           frozen Wiley NJDv5 vendor bundle
paper/build.py                                       canonical manuscript builder
research/                                            methodological design notes
figures/                                             study figures
literature/                                          literature corpus/index
archive/                                             superseded papers/notebooks/presentations
```

The root `AGENTS.md` is mandatory reading for coding agents and maintainers. It defines the
package and manuscript contracts and the scientific guardrails that must be preserved.

## JFM manuscript

The internal manuscript preserves the selected Wiley layout:

```tex
\documentclass[HARVARD,Utopia2COL]{WileyNJDv5}
```

Build it with XeLaTeX through the repository wrapper rather than compiling source files in
place:

```bash
python paper/build.py
```

The generated PDF and all intermediate files remain under the gitignored `paper/build/`.
A compiler-free structural check is available for CI and agents:

```bash
python paper/build.py --check
```

See `paper/README.md` for the manuscript directory contract. The older REMEF-oriented draft
is retained intact under `archive/paper_remef/` for provenance.

## Documentation and API discovery

After editable installation:

```bash
python -m sphinx -W --keep-going -b html docs docs/_build/html
```

Start at `docs/index.md`. `docs/api/index.md` is the canonical function/class inventory.
New reusable modules must be documented there.

## Reproducible validation

```bash
python -m scripts.check_repo_structure
python paper/build.py --check
python -m experiments.synthetic_validation --quick
python -m experiments.build_wti_apo_panel --input-dir data/csv --output-dir results/wti_apo
```

Long-running experiments remain checkpointed and resumable. See `research/COMPUTE.md` and
the experiment modules for presets, seeds, configuration fingerprints, and hardware
manifests.

## WTI empirical application

The CME WTI Average Price Option application does not treat one fixed futures contract as
the Asian underlying. The pipeline reconstructs calendar-month first-nearby CL fixings,
separates realized and remaining fixings, uses the observed term structure for remaining
expectations, defines moneyness observation by observation relative to the expected final
average, and compares Full Bayes / posterior-mean / MAP / MLE prices with observed market
settlements.

All downloaded strikes are retained in the raw panel. Liquidity/sample filters and
representative-contract rankings are separate operations. In particular,
`richest_option_series.csv` is a data-completeness diagnostic, not a liquidity ranking.
See `docs/empirical_wti.md` and `research/EMPIRICAL_WTI_DESIGN.md`.
