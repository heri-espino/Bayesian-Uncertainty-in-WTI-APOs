# Vendored Adobe Utopia support

This directory keeps the upstream CTAN archives required to reproduce the typeface used by the active Wiley manuscript class:

```tex
\documentclass[HARVARD,Utopia2COL]{WileyNJDv5}
```

The Wiley class loads `utopia` for text and `mathastext` for text-matched mathematics.

## Upstream archives

- `upstream/utopia.zip` — CTAN `/fonts/utopia`, Adobe Utopia Type 1 PFB/AFM files. The archive contains `LICENSE-utopia.txt` and the upstream README. CTAN package version: 2006-11-17.
- `upstream/psnfss.zip` — CTAN `/macros/latex/required/psnfss`, PSNFSS 9.3. It provides the LaTeX interface, Utopia font map/encoding support, and the nested `freenfss.zip` metrics/font-definition tree. PSNFSS is distributed under the LPPL.

The archives are preserved byte-for-byte as uploaded rather than expanding hundreds of generated/support files into Git.

## Local preparation

Run:

```powershell
python -m scripts.vendor_utopia_fonts
```

The helper expands the archives into the ignored `paper/build/vendor_fonts/utopia/` cache, creates a local TDS-style tree, generates `utopia.sty` from the PSNFSS DocStrip source when needed, and prepends the local tree to kpathsea search paths. It does not modify the system TeX installation.

The publication-figure builder invokes this automatically and prefers the vendored tree:

```powershell
python -m scripts.build_publication_figures --formats pdf
```

The resulting `figure_manifest.json` records `font_mode` as either:

- `wiley-utopia-vendored`
- `wiley-utopia-system`
- `stix-fallback`

## Remaining dependency

`mathastext` is not supplied by either of these two upstream archives. It remains a normal TeX-distribution dependency because `WileyNJDv5.cls` loads it independently. If the manuscript already compiles under `Utopia2COL`, this dependency is normally already present.

## Sources

- https://ctan.org/pkg/utopia
- https://ctan.org/pkg/psnfss
- https://ctan.org/pkg/mathastext
