"""Local JFM adapter for AwesomeFigures PGF raster sidecars.

The pinned AwesomeFigures exact PDF compiler inputs an absolute .pgf from
a different TeX working directory. Matplotlib may write additional files
such as fig01-img0.png beside that PGF (for imshow or heatmaps), but the TeX
input retains relative image names. This adapter adds a TeX graphicspath
to the true PGF directory and otherwise uses the original compiler and
the unmodified Wiley preamble. It never substitutes Matplotlib PDF fonts.
Remove after upstream AwesomeFigures handles these sidecars itself.
"""
from __future__ import annotations

from contextlib import contextmanager
from pathlib import Path
import tempfile



def _add_pgf_graphicspath(original: str, pgf: Path) -> str:
    """Extend the preamble without modifying its class, fonts or body."""
    marker = r"\begin{document}"
    if marker not in original:
        raise ValueError("Missing LaTeX document boundary")
    folder = pgf.parent.resolve().as_posix().rstrip("/") + "/"
    # Forward slashes work in XeLaTeX on both Windows and Unix.
    extension = (
        r"\usepackage{graphicx}" + "\n"
        + r"\graphicspath{{" + folder + "}}\n"
    )
    return original.replace(marker, extension + marker, 1)


@contextmanager
def jfm_pgf_sidecar_support():
    """Temporarily add the PGF output folder to exact-TeX asset lookup.

    Reuse AwesomeFigures' own compiler, audit and font checks. The generated
    temporary TeX file stays in the original Wiley stage folder so relative
    class and style imports continue to resolve normally.
    """
    from awesomefigures import auto_publication

    compile_original = auto_publication._compile_exact_pdf

    def compile_with_assets(pgf, pdf, manuscript, engine, timeout):
        pgf = Path(pgf)
        source = Path(manuscript)
        amended = _add_pgf_graphicspath(
            source.read_text(encoding="utf-8-sig"), pgf
        )
        temporary = None
        try:
            with tempfile.NamedTemporaryFile(
                prefix="_jfm_figures_", suffix=".tex", dir=source.parent,
                mode="w", encoding="utf-8", delete=False,
            ) as handle:
                handle.write(amended)
                temporary = Path(handle.name)
            return compile_original(pgf, pdf, temporary, engine, timeout)
        finally:
            if temporary is not None:
                temporary.unlink(missing_ok=True)

    auto_publication._compile_exact_pdf = compile_with_assets
    try:
        yield
    finally:
        auto_publication._compile_exact_pdf = compile_original
