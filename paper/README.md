> **2026-10-28 current target:** Paper A now prioritizes an **ambitious JFM submission**, with the existing REMEF document left unchanged as the fallback. The JFM source is the concise `paper/manuscript/main_short.tex`, compiled by `python paper/build.py` using the frozen Wiley vendor class. `main.tex` is an older, noncanonical full-length draft. A bounded synthetic experiment is implemented but has **no claims or final results yet**; read [JFM revision and oracle pilot](manuscript/JFM_REVISION_AND_ORACLE_PILOT_2026-10-28.md) before running it. JFM-specific figure output is isolated under `figures/jfm/` and the REMEF artifact paths are untouched. This target change does **not** complete the distinct future JCM Paper B.

# Internal Wiley/JFM manuscript — retained while the journal target is reassessed

> **2026-10-27 publication decision:** The author plans TWO distinct studies: **Paper A** (Bayesian posterior integration and volatility information) is prioritized for REMEF after evidence/rights/editorial audit; **Paper B** (new path-dependent CL fixing and futures-curve WTI AAO valuation/hedging) is a research proposal for possible future JCM submission. See [two-paper scope/overlap ledger](../docs/two_paper_publication_strategy_2026-10-27.md), [REMEF revision plan](remef/SCIENTIFIC_REVISION_AND_SUBMISSION_GATE_2026-10-27.md), and [JCM feasibility plan](../research/STRUCTURAL_WTI_AAO_PAPER_FEASIBILITY_PLAN_2026-10-27.md). The current Wiley/JFM and CAS builds **reuse old Paper A text**, and are not evidence of an already written Paper B manuscript. The October 25 single-manuscript JCM/REMEF ranking described below is superseded.

> **New global paper handoff:** [complete research plan](../research/PAPER_COMPLETION_MASTER_PLAN_2026-10-26.md)
> and [evidence ledger](../research/AAO_EVIDENCE_LEDGER_2026-10-26.md).
> Keep Wiley/JFM, REMEF and JCM sources intact; the long-history model study is not complete.

> **2026-10-25 update:** The provisional ambitious future journal target is *Journal of
> Commodity Markets* **only if the new 2020–2026 AAO dataset yields substantially
> stronger verified independent-date evidence**. The ready REMEF Word draft is the
> fallback; the existing Wiley/JFM LaTeX source below is intentionally preserved,
> not automatically the next journal for submission. See [journal strategy](../docs/journal_strategy.md).
> **Previous October 2026 adaptation:** The REMEF manuscript is
> maintained separately under [`paper/remef/`](remef/README.md), with its own
> introduction, bilingual metadata, Word builder, source bibliography supplement,
> scientific-audit checklist, and manual-only GitHub Actions workflow.
> The JFM full and concise Wiley manuscripts remain intact for a later
> alternative submission, **never simultaneous** with REMEF or JCM.


## Elsevier working-draft adaptation

The author's new `paper/els-cas-templates/` CAS v2.4 bundle is now wired
into a separate provisional double-column working source in
[paper/jcm/](jcm/README.md). Use `python paper/jcm/build.py --check` or
a manual compile; the builder copies the earlier validated concise
sections and existing figures to an isolated staging directory. These
old numbers **do not** represent the new 81-month AAO dataset, which
must pass the scientific gates in
`research/AAO_81_MONTH_EXECUTION_PLAN.md` before manuscript revision.
The original frozen Wiley source and REMEF Word version remain intact.

## Language and literature terminology

Use [the manuscript wording dictionary](WORDING_DICTIONARY.md) and its
[source-by-source literature evidence map](../literature/TERMINOLOGY_EVIDENCE.md)
when editing the prose. Prefer established option-pricing terminology, direct
sentences, and explicit information cutoffs. Distinguish the PI--PM difference
from the posterior distribution of model prices. The concise manuscript (`manuscript/main_short.tex`) is the preferred editorial candidate
for submission. The fuller manuscript (`manuscript/main.tex`) remains available for
comparison; this preference does not replace the source selected for the full-paper build.



`paper/` contains the preserved internal Wiley/JFM manuscript source. Do not reformat it for JCM absent a dedicated author-approved manuscript PR.
The old REMEF-oriented drafts are preserved under `archive/paper_remef/` and are not active
manuscript sources.

## Canonical layout

```text
paper/
├── build.py
├── espino_2026_bayess-on-wti.pdf  # generated final PDF; gitignored
├── manuscript/
│   ├── main.tex
│   ├── references.bib
│   └── sections/
├── supplement/
│   └── online_supplement.md        # detailed design/robustness evidence moved from main text
├── vendor/
│   └── wiley_njd_v5/
└── build/                 # generated intermediate files; gitignored
```

The Wiley vendor directory is a frozen copy of the NJDv5 bundle supplied for manuscript
preparation. Do not edit it as part of ordinary paper revisions. The active manuscript uses
exactly the selected journal simulation options:

```tex
\documentclass[HARVARD,Utopia2COL]{WileyNJDv5}
```

This preserves Harvard references, Utopia, and the two-column layout selected for the
Journal of Futures Markets internal draft. Wiley's own guideline recommends XeLaTeX for
the bundled NJD fonts.

## Build

From any directory in the repository:

```bash
python paper/build.py
```

The builder creates an isolated staging tree under `paper/build/`, combines the manuscript
with the frozen Wiley bundle, and compiles with XeLaTeX. If `latexmk` is available it is
preferred; otherwise the script falls back to XeLaTeX + BibTeX passes. After compilation,
the builder moves the final local PDF to:

```text
paper/espino_2026_bayess-on-wti.pdf
```

Generated LaTeX products and the exported PDF must not be committed.

The submission-oriented concise manuscript keeps the main argument and essential evidence.
Detailed experimental settings and supporting diagnostics are preserved in
`paper/supplement/online_supplement.md` for later conversion to journal supplementary material.

Useful maintenance commands:

```bash
python paper/build.py --check
python paper/build.py --clean
python -m scripts.check_repo_structure
```

`--check` validates paths and the selected Wiley class options without requiring a TeX
installation, so it is suitable for CI.


## GitHub Actions build

The repository includes `.github/workflows/build-paper.yml` for a fully reproducible
remote build. It installs the Linux TeX toolchain, prepares the vendored
Utopia + PSNFSS + mathastext stack, rebuilds the four publication figures, requires
`font_mode: wiley-utopia-vendored`, compiles the Wiley manuscript, and uploads the
result as a GitHub Actions artifact.

The workflow is intentionally **manual-only** via `workflow_dispatch`; heavy figure/PDF builds
must not run on ordinary pushes or pull requests. Launch it from **Actions -> build-paper ->
Run workflow** when a compiled artifact is actually needed.

The artifact contains:

```text
paper/espino_2026_bayess-on-wti.pdf
figures/publication/*.pdf
figures/publication/*.png
figures/publication/figure_manifest.json
```

This is the preferred build path on machines where installing a local TeX distribution
is inconvenient or restricted.

## Draft status

The current manuscript is an internal working draft. It may contain explicitly identified
pending empirical analyses. Do not replace those placeholders with inferred or fabricated
results. Empirical claims are added only after the corresponding versioned experiment has
run and its outputs can be traced to data, configuration, seed, and code commit.

## Argument map for the concise submission candidate

Each main-text section has one primary purpose:

1. **Introduction:** identify the research question and the distinction between posterior integration and volatility-input choice; no derivation
2. **Posterior pricing:** define PI and PM, derive the curvature--variance approximation, and specify the synthetic experiment
3. **Data and design:** define the contract, information cutoffs, volatility benchmarks, and external LO comparison
4. **Results:** present synthetic mechanism, October PI--PM comparison, out-of-sample volatility benchmarks, and cross-instrument evidence, with no separate mini-conclusion
5. **Robustness:** report only checks that alter the strength or interpretation of the findings; retain technical details in the supplement
6. **Conclusion:** state what the comparisons establish and their limits without repeating tables or the introduction

The introductory PI--PM equations now appear only in the pricing section. The posterior-RMS
plug-in sensitivity is preserved in Supplement S2. Main-text tables and publication figures
are retained as core evidence, not removed merely to reduce length.

## Concise manuscript rewrite

The repository now keeps a from-scratch concise manuscript in `manuscript/main_short.tex`, with its six sections under `manuscript/sections_short/`. It uses the same final empirical results, bibliography, Wiley class, and publication figures as the full manuscript, but organizes the paper around three findings: the curvature--posterior-variance mechanism, the distinction between the PI--PM point-price effect and posterior price uncertainty, and the out-of-sample historical-versus-option-implied volatility comparison including the external vanilla-WTI validation.

The fuller manuscript in `manuscript/main.tex` is retained as a separate comparison draft.
Neither manuscript is yet claimed to be submission-ready; LaTeX compilation and author
metadata still require checking.


### Build the concise rewrite

The concise manuscript has an independent build so it never overwrites the full-paper PDF:

\`\`\`bash
python paper/build_short.py --check
python paper/build_short.py
\`\`\`

If the publication figures have already been generated, skip rebuilding them:

\`\`\`bash
python paper/build_short.py --skip-figures
\`\`\`

The exported PDF is:

\`\`\`text
paper/espino_2026_bayess-on-wti_short.pdf
\`\`\`

Cleaning the concise build removes only \`paper/build_short/\` and the concise exported PDF:

\`\`\`bash
python paper/build_short.py --clean
\`\`\`
