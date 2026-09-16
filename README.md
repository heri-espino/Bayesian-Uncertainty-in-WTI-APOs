# Bayesian parameter uncertainty for Asian options

Research library, reproducible experiments, data pipeline, and manuscript for Bayesian parameter uncertainty in arithmetic Asian-option valuation, with an empirical application to CME WTI Average Price Options. The publication strategy targets the **Journal of Futures Markets** first.

## Scientific boundary: P versus Q

Historical returns are modeled under the physical measure $\mathbb P$, while derivative valuation is performed under $\mathbb Q$. The physical drift `mu` is therefore not inserted into the baseline no-arbitrage pricing dynamics. Posterior uncertainty in parameters relevant to pricing, principally `sigma` in the current baseline, is propagated into the option value.

## Install the research library

```bash
conda env create -f environment.yml
conda activate asian-options
python -m pip install -e ".[dev,docs,market]"
```

Representative imports:

```python
from bayesian_asian_options.bayesian_gbm import random_walk_metropolis_gbm
from bayesian_asian_options.barchart_cl import load_barchart_cl_strip
from bayesian_asian_options.rates import treasury_curve_on_or_before
from bayesian_asian_options.wti_apo_pricing import wti_apo_cross_section_mc
```

CuPy is optional and platform-specific. For a CUDA-12 workstation, see `requirements/gpu-cuda12.txt` after checking `nvidia-smi`.

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

`main` is the only long-lived development branch. New work should use short-lived feature branches that are deleted after merge or explicit supersession. See `CONTRIBUTING.md` and `docs/development.md` for the branch/PR lifecycle and the read-only branch audit utility.

The root `AGENTS.md` is mandatory reading for coding agents and maintainers. It defines the package and manuscript contracts and the scientific guardrails that must be preserved.

## JFM manuscript

The internal manuscript preserves the selected Wiley layout:

```tex
\documentclass[HARVARD,Utopia2COL]{WileyNJDv5}
```

Build it with:

```bash
python paper/build.py
```

Generated TeX intermediates remain under the gitignored `paper/build/`; the final generated PDF is `paper/espino_2026_bayess-on-wti.pdf` and is also gitignored. A compiler-free structural check is available for CI and agents:

```bash
python paper/build.py --check
```

See `paper/README.md` for the manuscript directory contract. The older REMEF-oriented draft is retained under `archive/paper_remef/` for provenance.

## Documentation and API discovery

After editable installation:

```bash
python -m sphinx -W --keep-going -b html docs docs/_build/html
```

Start at `docs/index.md`. `docs/api/index.md` is the canonical function/class inventory. New reusable modules must be documented there.

## Reproducible validation

```bash
python -m scripts.check_repo_structure
python paper/build.py --check
python -m pytest -q
python -m experiments.synthetic_validation --quick
python -m experiments.build_wti_apo_panel --input-dir data/csv --output-dir results/wti_apo
```

Long-running experiments remain checkpointed and resumable. See `research/COMPUTE.md` and the experiment modules for presets, seeds, configuration fingerprints, and hardware manifests.

## WTI empirical application

The CME WTI Average Price Option application separates the data object used for physical volatility inference from the contract-specific futures curve used for risk-neutral APO valuation. The current real-market pilot uses:

- committed Barchart WTI APO histories as the external option-price benchmark;
- Yahoo Finance `CL=F` only as an explicitly labelled continuous/front-month proxy for historical returns under the physical measure;
- committed Barchart individual CL `Daily Prices` histories under `data/csv/CL` for the valuation-date futures term structure and future first-nearby fixings;
- `data/csv/CL/contract_expiries.csv` as the explicit CL last-trade-date reference;
- date-specific U.S. Treasury par-yield data for discounting.

A live test showed that Yahoo may remove older delisted individual CL symbols, so the canonical pilot does **not** require individual Yahoo contract downloads. Barchart `Latest` is retained as the source field and used as an end-of-day settlement proxy; it is not presented as an official CME settlement without separate validation.

The first real-market driver is:

```bash
python -m experiments.wti_apo_empirical_hybrid \
    --valuation-date 2026-09-04 \
    --apo-expiry 2026-10 \
    --cl-data-dir data/csv/CL \
    --download-treasury
```

For the university workstation, use:

```bash
python -m scripts.run_university_wti_apo --check-only
python -m scripts.run_university_wti_apo --quick
python -m scripts.run_university_wti_apo
```

The October-2026 pilot uses `CLX26` and `CLZ26`; the committed 2026-09-04 Barchart `Latest` values are 88.57 and 85.46 respectively. The workstation runner therefore needs network access only for Yahoo `CL=F` and, if no local rate file is present, the U.S. Treasury.

The Treasury pilot uses an explicit approximation: the maturity-interpolated **par yield** is treated as a continuously compounded zero-rate proxy. It is not described as a bootstrapped zero/OIS curve.

All downloaded APO strikes are retained in the raw panel. Liquidity/sample filters and representative-contract rankings are separate operations. In particular, `richest_option_series.csv` is a data-completeness diagnostic, not a liquidity ranking. See `docs/empirical_wti.md` and `research/EMPIRICAL_WTI_DESIGN.md`.
