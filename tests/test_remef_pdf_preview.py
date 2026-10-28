"""Regression tests for the local, preview-only REMEF LaTeX PDF route."""
from __future__ import annotations

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REMEF = ROOT / "paper" / "remef"


def _builder(monkeypatch):
    monkeypatch.syspath_prepend(str(REMEF))
    spec = importlib.util.spec_from_file_location(
        "_remef_pdf_preview", REMEF / "build_pdf.py"
    )
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_pdf_preview_uses_remef_sources_not_wiley_or_word(monkeypatch):
    builder = _builder(monkeypatch)
    tex, figures = builder.compose_preview()
    assert r"\documentclass[11pt,letterpaper]{article}" in tex
    assert "Posterior Integration and Volatility Inputs in WTI Asian Options" in tex
    assert r"\section{Results}" in tex
    assert r"\section{Conclusion}" in tex
    assert r"\citep{" in tex
    assert r"\bibliography{references_main,references_remef}" in tex
    assert r"\resizebox{\linewidth}{!}{\begin{tabular}" in tex
    assert r"\usepackage{amsmath,amssymb,graphicx,booktabs}" in tex
    assert r"\begin{equation}" in tex
    assert r"\end{equation}" in tex
    assert r"\label{eq:short_returns}" in tex
    assert r"\eqref{eq:short_average}" in tex
    assert r"\begin{figure*}" in tex
    assert r"\caption{" in tex
    assert len(figures) == 2
    for name in ("fig01_mechanism_map.pdf", "fig03_forward_q_cluster_bootstrap.pdf"):
        assert f"preview_figures/{name}" in tex
    assert ".svg" not in tex
    assert "Heriberto Espino-Montelongo" not in tex
    assert "WileyNJDv5" not in tex



def test_pdf_does_not_strip_labels_into_empty_math_paragraphs(monkeypatch):
    """Regression for MiKTeX 'Missing $ inserted' at preview.tex:177."""
    builder = _builder(monkeypatch)
    pdf, _ = builder.compose_preview()
    word_source = builder.make_latex(with_author=False)
    native = builder.make_latex(with_author=False, for_pdf=True)
    assert r"\label{eq:short_returns}" in native
    assert r"\begin{equation}" in native
    assert r"\label{eq:short_returns}" not in word_source
    assert r"\begin{equation}" not in word_source
    assert r"\begin{equation}" in pdf
    assert r"\label{eq:short_returns}" in pdf




def test_pdf_preview_staging_preserves_source_and_bibliography(monkeypatch, tmp_path):
    builder = _builder(monkeypatch)
    monkeypatch.setattr(builder, "STAGE", tmp_path / "latex_preview")
    tex, figures = builder.compose_preview()
    source = builder.prepare_stage(tex, figures)
    assert source.read_text(encoding="utf-8") == tex
    assert (builder.STAGE / "references_main.bib").is_file()
    assert (builder.STAGE / "references_remef.bib").is_file()
    assert all(
        (builder.STAGE / "preview_figures" / figure.name).is_file()
        for figure in figures
    )


def test_wiley_builders_do_not_require_broken_latexmk(monkeypatch):
    for name in ("build.py", "build_short.py"):
        source = (ROOT / "paper" / name).read_text(encoding="utf-8")
        assert 'if latexmk and xelatex and compiler("perl"):' in source
        assert "elif xelatex and bibtex:" in source


def test_perl_declared_in_conda_environment():
    environment = (ROOT / "environment.yml").read_text(encoding="utf-8")
    assert "\n  - perl\n" in environment
