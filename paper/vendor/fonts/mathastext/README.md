# Vendored mathastext support

This directory contains the upstream source used by WileyNJDv5 when `Utopia2COL` is selected.

## Upstream files

`upstream/` contains the files uploaded from the mathastext distribution:

- `mathastext.dtx` — package source, version 1.4e (2024-10-26), LPPL 1.3c.
- `mathastext.pdf` — upstream package documentation.
- `README.md` — upstream README/license notice extracted from the package source.

The upstream files are kept unchanged. The repository does not commit a generated `mathastext.sty`; instead, `scripts/vendor_utopia_fonts.py` runs the package's own DocStrip extraction into the ignored build cache.

The source itself specifies that running TeX/e-TeX on `mathastext.dtx` extracts `mathastext.sty`. The bootstrap follows that installation path and places the result in the local TDS tree used by the figure builder.

This makes the figure typography reproducible without requiring a global installation of mathastext.
