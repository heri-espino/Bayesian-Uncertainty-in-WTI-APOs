# Bayesian parameter uncertainty for Asian options

> **2026-10-27 TWO-PAPER STRATEGY:** We will aim to finish **Paper A** (Bayesian posterior integration versus volatility-information inputs; REMEF candidate, NOT submission-ready) and independently investigate **Paper B** (genuine first-nearby CL fixing-path, futures-curve WTI AAO pricing/hedging; possible future JCM paper, NOT yet data-validated). The latter must not duplicate Paper A's synthetic results and conditional mark comparisons. See [two-paper strategy, evidence boundaries and overlap ledger](docs/two_paper_publication_strategy_2026-10-27.md), [REMEF revision gate](paper/remef/SCIENTIFIC_REVISION_AND_SUBMISSION_GATE_2026-10-27.md), and [structural research/data feasibility protocol](research/STRUCTURAL_WTI_AAO_PAPER_FEASIBILITY_PLAN_2026-10-27.md). Existing experiments, original source data and preserved manuscript sources remain intact; the previously separate results and REMEF work have been reconciled for integration into main.

> **CURRENT COMPLETED AAO-ONLY RESULTS (2026-10-27; the integrated research branch):** The locally executed six-method Databento-only benchmark has **111,585 evaluated AAO contract-date targets across 189 pricing dates** (97,341 actual-flagged), plus 1,689-group retrospective implied-volatility diagnostic and corrected actual-only monthly-block uncertainty. **Lagged AAO IV MAE 0.2184 vs Bayesian PI MAE 0.8040 USD/bbl** on actual-flagged marks; this is reduced-form conditional cross-sectional settlement pricing, not structural/ex-ante valuation. Read the **[authoritative empirical report](research/AAO_DATABENTO_ONLY_EMPIRICAL_REPORT_2026-10-27.md)** and **[proposed next experiment protocol](research/AAO_DATABENTO_ONLY_MARKET_INFORMED_BAYES_PROTOCOL_2026-10-27.md)**. Earlier acquisition-loss and "no pricing study yet" text below is historical and superseded. **The 2026-10-27 branch was separately audited before integration; do not reset/change sparse-checkout.** All heavy work remains manual on the author's PC; never dispatch GitHub Actions.


> **Authoritative current handoff:** [HANDOFF.md](HANDOFF.md), [master plan](research/PAPER_COMPLETION_MASTER_PLAN_2026-10-26.md), [evidence ledger](research/AAO_EVIDENCE_LEDGER_2026-10-26.md), [experiments](research/AAO_EXPERIMENT_REGISTER_2026-10-26.md), [independent verification](research/AAO_AGENT_VERIFICATION_PROTOCOL_2026-10-26.md). The earlier 2026-10-26 Databento-only build-only status below is superseded by the 2026-10-27 committed empirical report. Git LFS pointers exist for the recovered source, but remote binary retrieval must still be verified.

## Historical 2026-10-26 research priority (superseded by 2026-10-27 experiments)

The author chose a **Databento-only** exchange settlement study, with
NO Barchart option-price comparison. The final new study uses
`experiments/wti_aao_databento_only.py` and
`bayesian_asian_options.aao_databento_only` to compare posterior
integration (PI), posterior-mean pricing (PM), rolling-21, rolling-63,
EWMA and strictly lagged AAO-implied volatility on a common set of
non-anchor option contracts; it makes **no paid provider calls**.
The input is the 81-month AAO source DBNs and rebuilt private SQLite.

**Methodological boundary:** The downloaded AAO definitions and
statistics do not contain CL first-nearby futures curves or daily
settlement fixings, so the new model is a **reduced-form lognormal
terminal-average approximation**. It derives the expected average
and discount factor from separate same-day matched AAO call/put
parity anchors, excluded from pricing targets. Volatility features
are strictly lagged; forward-average proxy changes are NOT actual
WTI P-measure CL returns. The evaluation is conditionally
cross-sectional, not fully independent ex-ante structural Asian pricing.

The new standalone Elsevier source `paper/jcm/databento_main.tex`,
CAS builder `paper/jcm/build_databento.py`, 3 figures in
`scripts/plot_aao_databento_only.py` and full execution commands
are in
[Databento-only paper runbook](research/AAO_DATABENTO_ONLY_PAPER_RUNBOOK_2026-10-26.md).
**No new experimental numerical performance claims are available
until the author runs the code.** This preserves the old Barchart/Wiley
papers separately. Re-acquire and Git LFS-back-up the missing source
data BEFORE running the new experiment.

## URGENT — Databento raw history recovery and Git LFS backup (2026-10-26)

The previous **162 compressed AAO DBN files and reconstructed SQLite
settlement database were lost** on the author's Windows VM following an
unsafe sparse-checkout instruction. The author explicitly requires
re-downloading and **backing up the 81-month AAO dataset and rebuilt
SQLite into this PRIVATE GitHub repo via Git LFS**. The 81-month data
are **NOT presently in GitHub** merely because `.gitattributes`
tracks the patterns. Earlier acquisition/analysis paragraphs below
describe historical results, not currently available local source files.

**Start here:** [AAO replacement, integrity audit, LFS upload and
full experimental replay](research/AAO_RECOVERY_AND_LFS_BACKUP_2026-10-26.md).

Commands include `git sparse-checkout add data/databento/wti_aao_bulk`
**before reacquisition**, `python -m scripts.aao_lfs_preflight`,
quote-first and explicitly budget-confirmed Databento download with a
**fresh report directory**, SHA256 verification, Git LFS backup of
the 162 sources, and a manual-only replay of all 11 historical data
diagnostics. Then push the derived full-history SQLite via Git LFS.
Do not alter sparse checkout again before confirming remote LFS uploads.

## Latest source diagnosis (26 October 2026)

For the CME reference date **2024-01-26**, all **7,868** latest
publisher/symbol/day keys are preliminary; there are **zero**
selected final marks. This explains why the retained set has
**1,700** reference dates versus the raw final-event inventory's
**1,701**, while the two original raw final events' exact update
sequence has not been traced.

The local VM does **not** have the default Barchart CSV root
populated, but direct GitHub `main` inspection confirms
JAO option-history CSVs are versioned under `data/csv/sep2026/`.
Do not infer zero overlap or purchase missing data. Check the
local exact tracked path, sparse-checkout settings, and local work
before restoring any files. See the
[AAO quality checkpoint](research/AAO_PANEL_QUALITY_FINDINGS_2026-10-26.md).
Contract-specific price-parity and chronological Bayesian
backtesting remain open.

## New source quality checkpoint (26 October 2026)

The verified 81-month AAO data reconciler yielded 5,105,603
provisional final nonintraday candidates on 1,700 reference dates,
including 2019-12-31 (therefore 1,699 from 2020 onward).
Two raw final settlement events on 2024-01-26 produced no selected
candidate; the reason still needs inspection. The local Barchart
option-history discovery returned unavailable, although source CSVs
are tracked in this repository. Investigate checkout and paths
before treating this as zero market overlap. See
[latest diagnostic instructions](research/AAO_PANEL_QUALITY_FINDINGS_2026-10-26.md).
Neither the option-price parity nor the full forward backtest is
established; prior journal results remain unchanged.

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

## Result of daily definition mapping and new native-symbol audit

The author's three-rule daily-definition mapping only accounted for
**30,508/55,326 (55.1%)** February 2021 final settlement events and
**68,835/118,094 (58.3%)** June 2026 events. Remaining unmatched events
may have valid instrument identities; these counts do **not** establish
missing settlement prices. The matched candidate methods showed no
conflicting identities, but cannot validate unmatched records.

Next offline task: use Databento's locally embedded native `symbol`
mapping, not further arbitrary date shifts:

```powershell
python -m experiments.wti_aao_symbol_mapping --months 2021-02 2026-06
```

The [symbol-mapping checkpoint](research/AAO_SYMBOL_MAPPING_NEXT_GATE_2026-10-25.md)
records the observed counts, why numeric IDs and trading-session dates
need special treatment, and safe steps toward a contract/day panel. The
journal draft and pricing-performance figures still use the earlier
scientifically validated sample.

## Cross-month correction reconciliation implemented (2026-10-26)

The author's within-month AAO candidate normalizer produced **48,730**
final nonintraday publisher+symbol+reference-day candidates for
February 2021 and **101,397** for June 2026 (31,414/43,067
actual-flagged and 17,316/58,330 theoretical-flagged, respectively).
The two months had **101** and **190** latest preliminary keys; no
reported deletions, intraday final marks, nonfinite prices or conflicts.
These figures are **not** full-history usable option prices.

The [cross-month reconciliation instructions](research/AAO_CROSS_MONTH_SETTLEMENT_RECONCILIATION_2026-10-26.md)
introduce `python -m experiments.wti_aao_cross_month --months
2021-02 2021-03 2026-06 2026-07` and, after a sample check, `--all`.
This offline module creates a complete-history native-symbol identity
registry, replays settlement latest actions across monthly file
boundaries and keeps licensed state in a local gitignored SQLite file.
The counts and the selected candidate statuses for **all 81 months**
remain unknown until the author executes the local job. Prices,
performance figures and the provisional Elsevier manuscript are
**unchanged** pending further scientific validation.

## Full 81-month provisional settlement reconciliation (2026-10-26)

The author's offline full-history run processed **13,412,045 settlement
events** and produced **5,105,603 final nonintraday provisional
publisher/symbol/reference-date candidates** (3,299,087 actual-flagged,
1,806,516 theoretical-flagged) on **1,700 CME reference dates**. It
identified 71,145 keys in multiple source months and 52,290 latest
preliminary keys; there were no historical symbol-fingerprint conflicts.
These are **not** valid out-of-sample test dates or transaction prices.

The older raw inventory had 1,701 final reference dates. One date
disappeared after candidate selection; its cause is not yet determined.
See [full history findings](research/AAO_FULL_HISTORY_RECONCILIATION_2026-10-26.md).
Next entirely offline diagnostic:
`python -m experiments.wti_aao_panel_quality`, optionally followed
by `--scan-final-dates` to identify that date. The output provides
annual aggregate price bins and **date-only** Barchart overlap, not
instrument-level pricing validation. The journal figures and results
remain unchanged until genuine chronological experiments are run.

## Native AAO contract symbology confirmed; candidate-price stage (2026-10-26)

The local DBN native-symbol audit confirmed **100% of final settlement
events in February 2021 (55,326)** and **June 2026 (118,094)** map to
unambiguous outright AAO C/P contract definitions by publisher+symbol,
with **zero** within-month fingerprint conflicts. The daily numeric
instrument-ID matching issue no longer blocks local preliminary
contract identification.

The [candidate normalization checkpoint](research/AAO_NATIVE_SYMBOL_CANDIDATE_PANEL_2026-10-26.md)
and new offline `python -m experiments.wti_aao_contract_day_candidates
--months 2021-02 2026-06` implement correction-aware,
final/non-intraday filtering, with licensed price-level output only
in an opt-in gitignored local directory. Selected records remain
**within-month candidates**, not validated cross-month settlement
prices, actual transactions or eligible chronological option-pricing
test dates. Existing paper figures and numerical conclusions are
unchanged until source parity and new out-of-sample experiments pass.

## 81-month AAO inventory totals and timestamp-mapping gate (2026-10-25)

The locally verified historical archive contains **81 months**,
70,154,064 statistics events, **5,899,096 final settlement events**,
and **1,701 distinct final CME reference dates**. Of final events,
4,027,696 are actual-flagged and 1,871,400 theoretical-flagged.
These are *not yet* distinct contract-day option prices or the number of
strictly forward-eligible backtesting dates.

A strict same-UTC-day, preceding-definition diagnostic missed 76.1%
of February 2021 and 81.1% of June 2026 settlement events. Since CME's
settlement reference date can differ from its publication date,
this is a **diagnostic-rule mismatch**, not a demonstrated data gap.
See the [settlement mapping checkpoint](research/AAO_81_MONTH_SETTLEMENT_MAPPING_FINDINGS.md).

Next entirely offline test:
`python -m experiments.wti_aao_mapping_comparison --months 2021-02 2026-06`.
It compares reference-day/publication-day/preceding-day instrument
definition mappings and flags contract-identity conflicts. It does not
produce usable price records, performance figures or new paper results.

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
