# Bayesian parameter uncertainty for Asian options

## February 2021 gap resolved (2026-10-25)

The author successfully recovered the formerly omitted February 2021 month in a separate Databento acquisition: **two additional `AAO.OPT` files, USD 0.15870165 quoted**. Together, the two local manifests now report **162 compressed definition/statistics files for all 81 months (January 2020–September 2026), USD 17.49357489 combined quoted** (not verified actual charges). The original February omission was a transient HTTP 504 price-metadata failure. The previous 80-month inventory's **1,682** final reference days and **5,843,770** final settlement events are **not yet updated** to include February.

Next VM command (no paid data): `python -m experiments.wti_databento_aao_inventory --all`. Keep both ledgers and all licensed source files local. See [inventory results](research/AAO_INVENTORY_RESULTS_2026-10-25.md) and [agent tasks](research/AAO_AGENT_TASKS.md).


Research library, reproducible experiments, data pipeline, and manuscript for Bayesian parameter uncertainty in arithmetic Asian-option valuation, with an empirical application to CME WTI Average Price Options. The **conditional next ambitious journal target is the Journal of Commodity Markets** after verification of the expanded empirical sample; the ready REMEF candidate is retained as a publication-focused fallback, and the Wiley/Journal of Futures Markets manuscript remains available as an alternative. See [journal strategy](docs/journal_strategy.md).

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
paper/manuscript/                                    preserved Wiley/JFM LaTeX manuscripts
paper/remef/                                         REMEF Word-format alternative and audit
paper/vendor/wiley_njd_v5/                           frozen Wiley NJDv5 vendor bundle
paper/build.py                                       canonical manuscript builder
research/                                            methodological design notes
figures/                                             study figures
literature/                                          literature corpus/index
archive/                                             superseded papers/notebooks/presentations
```

`main` is the only long-lived development branch. New work should use short-lived feature branches that are deleted after merge or explicit supersession. See `CONTRIBUTING.md` and `docs/development.md` for the branch/PR lifecycle and the read-only branch audit utility.

The root `AGENTS.md` is mandatory reading for coding agents and maintainers. It defines the package and manuscript contracts and the scientific guardrails that must be preserved.

## Publication strategy after the new historical dataset

The prospective higher-ambition subject-fit target is the **Journal of Commodity Markets**, **conditional on** verified improvements in distinct forward-eligible dates, settlement-quality checks, temporal robustness and originality. It is **not yet a journal chosen for actual submission**. The prepared [REMEF Word draft](paper/remef/README.md) and [presubmission audit](paper/remef/PRESUBMISSION_AUDIT.md) remain the realistic fallback; the preserved Wiley/JFM LaTeX sources are a demanding alternative. The same paper cannot be considered by two journals simultaneously. See [journal strategy](docs/journal_strategy.md).

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

## Databento 2020–2026 AAO acquisition: completed transfer, pending scientific validation

**New inventory evidence (2026-10-25):** All 80 downloaded months decoded
without errors, with **1,682 distinct reference dates containing final settlement events**,
**5,843,770 final settlement events** (3,989,698 actual-flagged and 1,854,072
theoretical-flagged). `AAO` asset confirmed in monthly definition summaries.
**February 2021** is the absent month, pending metadata diagnosis.
These are *not* 1,682 eligible forward-validation dates or 5.8 million
independent contract-price observations. See
[offline inventory findings](research/AAO_INVENTORY_RESULTS_2026-10-25.md)
and [next agent tasks](research/AAO_AGENT_TASKS.md). No model result or
publication target has been revised on this basis alone.


**The author reported a successful local historical download:** 160 compressed `AAO.OPT`
definition/statistics files across **80 eligible monthly windows** from January 2020 to
September 2026, quoted at **USD 17.33487324** (not verified actual billing).
The one excluded month, checksum parity, contract identities, unique final settlements,
theoretical/actual status, Barchart agreement and new independent forward-test dates have
**not** yet been audited. The earlier 2,381 holdouts across 15 dates and 253 external-LO
matches across 10 dates remain the only validated comparisons until new results exist.

**Start here:** [2026-10-25 checkpoint](research/CHECKPOINT_2026-10-25_AAO_EXPANSION.md),
[agent execution tasks](research/AAO_AGENT_TASKS.md),
[bulk acquisition guide](research/DATABENTO_AAO_BULK_ACQUISITION.md), and
[tracking Issue #90](https://github.com/heri-espino/Bayesian-Uncertainty-in-WTI-APOs/issues/90).
The raw DBN payloads are on the author's VM, not in GitHub. No re-download is needed.

```powershell
git switch main
git pull --ff-only origin main
conda activate asian-options
python -m pytest tests/test_wti_databento_aao_inventory.py -q
python -m experiments.wti_databento_aao_inventory --months 2023-06 2025-06 2026-06
# Inspect sample report and data fields, then:
python -m experiments.wti_databento_aao_inventory --all
```

Do **not** run another `--mode download` by default; charges may recur. Keep licensed raw
market data gitignored and publish only permitted aggregate results. Heavy builds and
experiments remain manual-only.

## New completed verification (2026-10-25)

The author's local integrity audit confirmed **all 162 downloaded DBN
files by SHA256**, with no issues. The full 81-month coverage figure
was generated (PDF/PNG/SVG) from a refreshed local inventory. In
2021-02 and 2026-06, all final settlement events found a same-month
outright instrument ID, but repeated events and predominantly
theoretical June 2026 marks require detailed normalization.

See `research/AAO_POST_DOWNLOAD_VALIDATION_2026-10-25.md` for exact
counts and the next experiment:
`python -m experiments.wti_aao_settlement_gate --months 2021-02 2026-06`.
This does not yet establish valid multiyear contract-day option prices,
independent holdout dates, fresh performance figures or a finished
Journal of Commodity Markets manuscript.

## 81-month research execution and provisional Elsevier paper

The completed AAO acquisitions cover **all 81 months (2020-01 through
2026-09)**, with **162 local DBN chunks** and a combined **USD 17.49357489
quoted cost**; those quotes are not confirmed provider charges. The previous
**80-month** inventory's 1,682 reference dates and 5,843,770 final settlement
*events* are not valid expanded-paper holdout counts. The next steps require
contract-specific price validation and chronological cross-vendor backtests.

The new [execution plan](research/AAO_81_MONTH_EXECUTION_PLAN.md) documents
the evidence and stage gates. The repo now includes:

- `python -m scripts.audit_aao_manifests` to validate both acquisition ledgers
  and 162 source file SHA256 hashes, entirely offline.
- `python -m scripts.plot_aao_history_coverage` to create a *diagnostic*
  AAO event-coverage figure from a complete 81-month inventory, refusing
  obsolete/incomplete reports.
- [paper/jcm/](paper/jcm/README.md), an **Elsevier CAS double-column
  working draft**, staged from the old validated concise research; it is
  not a finished expanded empirical manuscript.

Both the old Wiley/JFM and the REMEF alternatives are preserved. No
Databento purchases, backtest numerical claims or new pricing result
tables are implied by the CAS manuscript or coverage figure.

## Research roadmap

The active research roadmap is tracked through GitHub Issues and the project wiki in the documentation:

- `docs/project_wiki.md` — current scientific thesis and navigation;
- `docs/research_roadmap.md` — milestones M1–M5, issue map, and Project-board design;
- `docs/literature_strategy.md` — literature screening and novelty workflow;
- `docs/journal_strategy.md` — conditional JCM/REMEF/JFM strategy and evidence gates;
- `docs/submission_checklist.md` — journal-neutral readiness gate plus preserved JFM package.

Milestone tracker Issues are #43–#47, with concrete research tasks in #33–#42.

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

A live test showed that Yahoo may remove older delisted individual CL symbols, so the canonical pilot does **not** require individual Yahoo contract downloads. In the Barchart histories used by this project, `Latest` is the CME settlement field. The raw field name is retained for provenance and is not interpreted as an intraday last trade.

There is one canonical real-market driver:

```bash
python -m experiments.wti_apo_empirical \
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

Run manifests use repository-relative paths for repository inputs, redact external directory prefixes, and record the Git commit, dirty-tree status, Python/platform information, and NumPy/pandas/SciPy versions. Hostnames and user names are intentionally not recorded.

The Treasury pilot uses an explicit approximation: the maturity-interpolated **par yield** is treated as a continuously compounded zero-rate proxy. It is not described as a bootstrapped zero/OIS curve.

All downloaded APO strikes are retained in the raw panel. Liquidity/sample filters and representative-contract rankings are separate operations. In particular, `richest_option_series.csv` is a data-completeness diagnostic, not a liquidity ranking. See `docs/empirical_wti.md` and `research/EMPIRICAL_WTI_DESIGN.md`.
