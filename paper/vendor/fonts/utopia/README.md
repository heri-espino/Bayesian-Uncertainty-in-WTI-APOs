# Vendored Adobe Utopia support

This directory keeps the upstream CTAN archives required to reproduce the text typeface used by the active Wiley manuscript class:

```tex
\documentclass[HARVARD,Utopia2COL]{WileyNJDv5}
```

The Wiley class loads `utopia` for text and `mathastext` for text-matched mathematics. The latter is vendored separately under `../mathastext/`.

## Upstream archives

- `upstream/utopia.zip` — CTAN `/fonts/utopia`, Adobe Utopia Type 1 PFB/AFM files. The archive contains `LICENSE-utopia.txt` and the upstream README. CTAN package version: 2006-11-17.
- `upstream/psnfss.zip` — CTAN `/macros/latex/required/psnfss`, PSNFSS 9.3. It provides the LaTeX interface, Utopia font map/encoding support, and the nested `freenfss.zip` metrics/font-definition tree. PSNFSS is distributed under the LPPL.

The archives are preserved byte-for-byte as uploaded rather than expanding hundreds of generated/support files into Git.

## Local preparation

Run:

```powershell
python -m scripts.vendor_utopia_fonts
```

The helper combines these archives with the vendored `mathastext.dtx`, expands everything into the ignored `paper/build/vendor_fonts/utopia/` cache, creates a local TDS-style tree, extracts `utopia.sty` and `mathastext.sty` when needed, and prepends the local tree to kpathsea search paths. It does not modify the system TeX installation.

The publication-figure builder invokes this automatically and prefers the vendored tree:

```powershell
python -m scripts.build_publication_figures --formats pdf
```

The resulting `figure_manifest.json` records `font_mode` as either:

- `wiley-utopia-vendored`
- `wiley-utopia-system`
- `stix-fallback`

## Sources

- https://ctan.org/pkg/utopia
- https://ctan.org/pkg/psnfss
- https://ctan.org/pkg/mathastext
