#!/usr/bin/env python3
"""Compile the current REMEF Paper A into a local, preview-only LaTeX PDF.

Uses the REMEF-specific scientific sections, saved vector figures and the two
bibliographies. No Word conversion, Pandoc, Inkscape, simulations, data
downloads, or journal-style certification are performed.

From the repository root:
    python paper/remef/build_pdf.py
    python paper/remef/build_pdf.py --check

Requires a local XeLaTeX and BibTeX installation (e.g. MiKTeX on Windows).
Unlike latexmk, this command does not require Perl.
"""
from __future__ import annotations

import argparse
import shutil
import subprocess
from pathlib import Path

from build import BUILD, FIGURES, REFERENCES, ROOT, make_latex, validate

STAGE = BUILD / "latex_preview"
OUTPUT = BUILD / "remef_latex_preview.pdf"
PDF_FIGURES = (
    FIGURES / "ten_million" / "fig01_mechanism_map.pdf",
    FIGURES / "fig02_historical_vs_apo_implied_volatility.pdf",
    FIGURES / "fig03_forward_q_cluster_bootstrap.pdf",
    FIGURES / "fig04_numerical_identification.pdf",
)
PREAMBLE = r"""
\documentclass[11pt,letterpaper]{article}
\usepackage[margin=2.5cm]{geometry}
\usepackage{fontspec}
\IfFontExistsTF{Times New Roman}{\setmainfont{Times New Roman}}{\setmainfont{Latin Modern Roman}}
\usepackage{amsmath,amssymb,graphicx,booktabs}
\usepackage[round,authoryear]{natbib}
\usepackage[hidelinks]{hyperref}
\setlength{\parskip}{0.4em}
\setlength{\parindent}{1.2em}
\emergencystretch=3em
\begin{document}
"""
ENDING = r"""
\bibliographystyle{plainnat}
\bibliography{references_main,references_remef}
\end{document}
"""


def compose_preview() -> tuple[str, tuple[Path, ...]]:
    """Use the same REMEF text as the Word builder, with original vector PDFs."""
    validate()
    body = make_latex(with_author=False, for_pdf=True)
    used: list[Path] = []
    for source in PDF_FIGURES:
        pdf_reference = source.relative_to(ROOT).as_posix()
        if pdf_reference in body:
            body = body.replace(pdf_reference, f"preview_figures/{source.name}")
            used.append(source)
    if len(used) < 2:
        raise ValueError("Expected at least two REMEF figure references.")
    if "vector_figures/" in body or ".svg" in body:
        raise ValueError("Unexpected Word-only SVG reference in PDF preview.")
    if r"\begin{equation}" not in body or r"\label{eq:short_returns}" not in body:
        raise ValueError("Native LaTeX equation environments and labels are missing.")
    # Keep long Word table blocks within the PDF text width.
    body = body.replace(
        r"\begin{tabular}", r"\resizebox{\linewidth}{!}{\begin{tabular}"
    ).replace(r"\end{tabular}", r"\end{tabular}}")
    if r"\citep{" not in body or r"\section{Results}" not in body:
        raise ValueError("REMEF source content is incomplete.")
    return PREAMBLE + body + "\n" + ENDING, tuple(used)


def prepare_stage(source: str, figures: tuple[Path, ...]) -> Path:
    """Keep the full generated TeX and local bibliography beside the build logs."""
    STAGE.mkdir(parents=True, exist_ok=True)
    target = STAGE / "preview.tex"
    target.write_text(source, encoding="utf-8")
    figure_dir = STAGE / "preview_figures"
    figure_dir.mkdir(exist_ok=True)
    for figure in figures:
        shutil.copy2(figure, figure_dir / figure.name)
    for bibliography, name in zip(
        REFERENCES, ("references_main.bib", "references_remef.bib"), strict=True
    ):
        shutil.copy2(bibliography, STAGE / name)
    return target


def compile_preview() -> Path:
    """Run XeLaTeX/BibTeX directly: works even without latexmk or Perl."""
    xelatex, bibtex = shutil.which("xelatex"), shutil.which("bibtex")
    if not xelatex or not bibtex:
        raise SystemExit(
            "MiKTeX/TeX Live must provide xelatex and bibtex on PATH. "
            "Install or update MiKTeX first; Perl and Pandoc are not needed "
            "for this REMEF PDF preview."
        )
    tex, figures = compose_preview()
    prepare_stage(tex, figures)
    commands = (
        [xelatex, "-interaction=nonstopmode", "-halt-on-error",
         "-file-line-error", "preview.tex"],
        [bibtex, "preview"],
        [xelatex, "-interaction=nonstopmode", "-halt-on-error",
         "-file-line-error", "preview.tex"],
        [xelatex, "-interaction=nonstopmode", "-halt-on-error",
         "-file-line-error", "preview.tex"],
    )
    for command in commands:
        print("+", " ".join(command), flush=True)
        subprocess.run(command, cwd=STAGE, check=True)
    staged_pdf = STAGE / "preview.pdf"
    if not staged_pdf.is_file():
        raise SystemExit("XeLaTeX completed without generating preview.pdf")
    shutil.copy2(staged_pdf, OUTPUT)
    print("Built", OUTPUT.relative_to(ROOT))
    print("PREVIEW ONLY: REMEF scientific text and figures, not Word submission QA.")
    return OUTPUT


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true",
                        help="check source and preview references without compiling")
    args = parser.parse_args()
    if args.check:
        source, figures = compose_preview()
        assert r"\bibliography{references_main,references_remef}" in source
        print(f"REMEF PDF preview source passed ({len(source)} chars, "
              f"{len(figures)} figures).")
        return
    compile_preview()


if __name__ == "__main__":
    main()
