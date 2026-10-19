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
    assert "Ex Hacienda Santa Catarina" in private
    assert "San Andrés" not in reviewer
    assert "+52 222 810 1202" in private
    assert "+52 222 810 1202" not in reviewer
    assert "[author to supply" not in private


def test_actual_pandoc_heading_text_is_supported(tmp_path):
    """Regression: Pandoc creates unnumbered headings in Word (run #39158592891).

    Exercise actual python-docx postprocessing on minimal Pandoc-shaped source,
    including moves between sections, so this bug fails lightweight pytest CI.
    """
    from docx import Document
    spec = importlib.util.spec_from_file_location(
        "_remef_postprocess", ROOT / "paper" / "remef" / "postprocess.py"
    )
    assert spec is not None and spec.loader is not None
    processor = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(processor)

    doc = Document()
    doc.add_paragraph("Posterior Integration and Volatility Inputs in WTI Asian Options")
    doc.add_paragraph("Integración posterior y volatilidad en opciones asiáticas WTI")
    doc.add_paragraph("Abstract", style="Heading 1")
    doc.add_paragraph("Keywords: Bayesian option pricing")
    doc.add_paragraph("Resumen", style="Heading 1")
    doc.add_paragraph("JEL: C11; C15; C58; G13; G17; Q40.")
    doc.add_paragraph("Introduction", style="Heading 1")
    doc.add_paragraph("Volatility is not observed directly")
    doc.add_paragraph("Asian options depend on a price average")
    doc.add_paragraph("WTI APOs provide a different test setting")
    doc.add_paragraph("The distinction between historical and option-implied information")
    doc.add_paragraph("Posterior uncertainty and Asian-option pricing", style="Heading 1")
    for title in (
        "Physical inference and risk-neutral valuation",
        "Posterior integration and price uncertainty",
        "Synthetic mechanism experiment",
    ):
        doc.add_paragraph(title, style="Heading 2")
        doc.add_paragraph("A reproducible scientific calculation.")
    doc.add_paragraph("Data and empirical design", style="Heading 1")
    for title in (
        "WTI Average Price Options",
        "Out-of-sample volatility comparisons",
        "Cross-instrument validation",
        "AI-assisted manuscript preparation",
    ):
        doc.add_paragraph(title, style="Heading 2")
        doc.add_paragraph("Data and analysis use earlier observations.")
    doc.add_paragraph("Results", style="Heading 1")
    doc.add_paragraph("When does posterior integration matter?", style="Heading 2")
    doc.add_paragraph("Robustness and interpretation", style="Heading 1")
    doc.add_paragraph("Conclusion", style="Heading 1")
    doc.add_paragraph("Data availability", style="Heading 1")
    doc.add_paragraph("External data subject to licensing.")
    doc.add_paragraph("Funding", style="Heading 1")
    doc.add_paragraph("This research received no external funding.")
    doc.add_paragraph("Conflicts of interest", style="Heading 1")
    doc.add_paragraph("The author declares no conflicts of interest.")
    doc.add_paragraph("References", style="Heading 1")
    for rows, cols in ((5, 3), (5, 5), (4, 5), (4, 3)):
        tab = doc.add_table(rows=rows, cols=cols)
        for cell in tab.rows[0].cells:
            cell.text = "Value"
    source = tmp_path / "pandoc_unumbered.docx"
    doc.save(source)
    processor.prepare_docx(source)
    result = Document(source)
    headings = [p.text for p in result.paragraphs if p.style.name.startswith("Heading")]
    for required in (
        "1. Introduction", "2. Literature review", "3. Methodology",
        "3.7 Computational implementation", "3.8 AI-assisted manuscript preparation",
        "4. Results and discussion", "4.5 Robustness, interpretation and limitations",
        "5. Conclusions and recommendations",
    ):
        assert required in headings
    assert "Data and empirical design" not in headings
    assert len(result.tables) == 4
    assert result.tables[0].cell(0, 1).text == "N"
    assert any("The REMEF studies examine" in p.text for p in result.paragraphs)
    assert any("no external funding" in p.text for p in result.paragraphs)
    # Reference-PDF title alignment and REMEF pagination are deterministic.
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    titles = [
        "Posterior Integration and Volatility Inputs in WTI Asian Options",
        "Integración posterior y volatilidad en opciones asiáticas WTI",
    ]
    for title in titles:
        para = next(p for p in result.paragraphs if p.text.strip() == title)
        assert para.alignment == WD_ALIGN_PARAGRAPH.LEFT
    assert result.sections[0].footer._element.xpath(".//w:fldSimple")
    assert "PAGE" in result.sections[0].footer._element.xml



def test_remef_manual_workflow_produces_math_reference_not_broken_lo_pdf():
    """Guard against regressing to LibreOffice-only rendering of Word OMML."""
    path = ROOT / ".github" / "workflows" / "build-remef.yml"
    workflow = path.read_text(encoding="utf-8")
    assert "workflow_dispatch:" in workflow
    assert "on:\\n  push:" not in workflow
    assert "ubuntu-24.04" in workflow
    for action in ("actions/checkout@v5", "actions/setup-python@v6",
                   "actions/upload-artifact@v6"):
        assert action in workflow
    assert "--from=docx --to=pdf --pdf-engine=xelatex" in workflow
    assert "remef_math_reference.pdf" in workflow
    assert "unicodedata.normalize(" in workflow
    assert "lo_layout" in workflow
    assert "Greek math symbols are absent from PDF preview" not in workflow
    assert "            paper/remef/build/remef_blinded_draft.pdf" not in workflow
