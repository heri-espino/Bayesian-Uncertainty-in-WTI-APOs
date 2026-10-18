"""Lightweight source checks for the journal-specific REMEF Word draft."""
from __future__ import annotations

import importlib.util
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "paper" / "remef" / "build.py"


def _build_module():
    spec = importlib.util.spec_from_file_location("_remef_build", SOURCE)
    assert spec is not None and spec.loader is not None
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_rem_e_f_inputs_and_blinding():
    b = _build_module()
    b.validate()
    tex = b.make_latex(with_author=False)
    assert "Heriberto Espino-Montelongo" not in tex
    assert "github.com/heri-espino" not in tex
    assert r"\citet{matiasgonzalez2019}" in tex
    assert r"\citet{ortizjimenez2026}" in tex
    assert r"\citet{gildertsiaras2020}" in tex
    assert r"\section{Results}" in tex
    assert r"\section{Conclusion}" in tex
    assert r"\begin{tabular}" in tex
    assert tex.count(r"\includegraphics") >= 2
    assert r"\begin{table*}" not in tex
    assert r"\begin{figure*}" not in tex
    assert r"\eqref{" not in tex
    assert r"\ref{" not in tex
    assert r"\label{" not in tex


def test_rem_e_f_author_and_bilingual_abstract_limits():
    b = _build_module()
    author = b.make_latex(with_author=True)
    assert "Heriberto Espino-Montelongo" in author
    fm = (ROOT / "paper" / "remef" / "frontmatter.tex").read_text(encoding="utf-8")
    for start, end in (
        (r"\section*{Abstract}", r"\textbf{Keywords:}"),
        (r"\section*{Resumen}", r"\textbf{Palabras clave:}"),
    ):
        segment = fm.split(start, 1)[1].split(end, 1)[0]
        segment = re.sub(r"\\textbf\{([^}]*)\}", r"\1", segment)
        words = segment.split()
        assert len(words) <= 180, (start, len(words))
    assert len("Posterior Integration and Volatility Inputs in WTI Asian Options".split()) <= 10
    assert len("Integración posterior y volatilidad en opciones asiáticas WTI".split()) <= 10


def test_rem_e_f_sources_distinct_from_original_wiley():
    b = _build_module()
    tex = b.make_latex(with_author=False)
    assert "Posterior Integration and Volatility Inputs in WTI Asian Options" in tex
    assert r"\documentclass[HARVARD,Utopia2COL]" not in tex
    assert r"\subsection{AI-assisted manuscript preparation}" in tex
    assert r"\noindent\textbf{Table " in tex
    assert r"\noindent\textbf{Figure " in tex

def test_remef_apa_and_required_section_postprocessor_exist():
    """Keep APA and REMEF section structure explicit in the reproducible build."""
    style = ROOT / "paper" / "remef" / "apa.csl"
    post = ROOT / "paper" / "remef" / "postprocess.py"
    builder = SOURCE.read_text(encoding="utf-8")
    assert style.is_file()
    assert "American Psychological Association" in style.read_text(encoding="utf-8") or "APA" in style.read_text(encoding="utf-8")
    assert post.is_file()
    content = post.read_text(encoding="utf-8")
    for heading in ("Literature review", "Methodology", "Results and discussion", "Conclusions and recommendations"):
        assert heading in content
    assert '"--csl=" + str(HERE / "apa.csl")' in builder
    assert "prepare_docx(path)" in builder

def test_confirmed_funding_and_coi_in_both_versions():
    b = _build_module()
    private = b.make_latex(with_author=True)
    reviewer = b.make_latex(with_author=False)
    for content in (private, reviewer):
        assert "This research received no external funding." in content
        assert "The author declares no conflicts of interest." in content
        assert "To be completed and verified" not in content
    for sensitive in (
        "Heriberto Espino-Montelongo",
        "heriberto.espinomo@udlap.mx",
        "0009-0009-1230-2931",
        "heri-espino.github.io",
        "linkedin.com/in/heri-espino",
    ):
        assert sensitive in private
        assert sensitive not in reviewer
    assert r"\footnote{" in private
    assert "Postal correspondence address and telephone: [author to supply before submission]" in private
