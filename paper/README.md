# Journal of Futures Markets manuscript

## Language and literature terminology

Use [the manuscript wording dictionary](WORDING_DICTIONARY.md) and its
[source-by-source literature evidence map](../literature/TERMINOLOGY_EVIDENCE.md)
when editing the prose. Prefer established option-pricing terminology, direct
sentences, and explicit information cutoffs. Distinguish the PI--PM difference
from the posterior distribution of model prices. The concise manuscript (`manuscript/main_short.tex`) is the preferred editorial candidate
for submission. The fuller manuscript (`manuscript/main.tex`) remains available for
comparison; this preference does not replace the source selected for the full-paper build.



`paper/` contains the active internal manuscript for the Journal of Futures Markets target.
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
