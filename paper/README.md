# Journal of Futures Markets manuscript

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

The workflow runs automatically when manuscript, figure-builder, or committed analysis
outputs change, and it can also be launched manually from **Actions -> build-paper ->
Run workflow**.

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
