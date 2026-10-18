"""Journal-specific, non-destructive layout adaptation of Pandoc Word output.

Keeps native OMML equations editable. Do not imitate publisher-produced DOI/logo headers.
Source: REMEF author instructions and a published article supplied for layout reference.
"""
from __future__ import annotations

from pathlib import Path
from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.shared import Cm, Pt, RGBColor


def find(doc, prefix):
    for p in doc.paragraphs:
        if p.text.strip().startswith(prefix):
            return p
    raise ValueError("Expected REMEF paragraph not found: " + prefix)


def insert_before(anchor, text, style=None):
    p = anchor.insert_paragraph_before(text)
    if style:
        other = next(x for x in anchor._parent.paragraphs if x.style.name == style)
        p.style = other.style
    return p


def remove(p):
    element = p._element
    element.getparent().remove(element)


def adapt_sections(doc):
    """Five REMEF-style scientific sections; preserve scientific paragraphs and formulas."""
    intro = find(doc, "1 Introduction")
    intro.text = "1. Introduction"
    original = find(doc, "2 Posterior uncertainty")
    insert_before(original, "2. Literature review", "Heading 1")
    for prefix in (
        "Asian options depend on a price average",
        "WTI APOs provide a different test setting",
        "The distinction between historical and option-implied information",
    ):
        original._p.addprevious(find(doc, prefix)._p)
    insert_before(
        original,
        "The REMEF studies examine Asian-option valuation with stochastic-control or "
        "mean-reverting volatility specifications; the crude-oil option study addresses "
        "forecasts of subsequent realized volatility. They are complementary but do not "
        "directly test our question. Here the pricing dynamics are held fixed while we "
        "separate the posterior-integration correction, the dispersion of conditional "
        "model values, and the contribution of previously available volatility inputs "
        "to out-of-sample APO pricing errors.",
    )
    new = {
        "2 Posterior uncertainty and Asian-option pricing": "3. Methodology",
        "2.1 Physical inference and risk-neutral valuation": "3.1 Physical-measure inference and risk-neutral valuation",
        "2.2 Posterior integration and price uncertainty": "3.2 Posterior integration and price uncertainty",
        "2.3 Synthetic mechanism experiment": "3.3 Synthetic experiment",
        "3.1 WTI Average Price Options": "3.4 WTI Average Price Options and market data",
        "3.2 Out-of-sample volatility comparisons": "3.5 Forward-in-time volatility comparisons",
        "3.3 Cross-instrument validation": "3.6 Cross-instrument validation",
        "3.4 AI-assisted manuscript preparation": "3.8 AI-assisted manuscript preparation",
        "4 Results": "4. Results and discussion",
        "5 Robustness and interpretation": "4.5 Robustness, interpretation and limitations",
        "6 Conclusion": "5. Conclusions and recommendations",
    }
    for p in doc.paragraphs:
        key = p.text.strip()
        if key in new:
            p.text = new[key]
            if key == "5 Robustness and interpretation":
                p.style = find(doc, "3.1 Physical-measure").style
    remove(find(doc, "3 Data and empirical design"))
    ai = find(doc, "3.8 AI-assisted manuscript preparation")
    insert_before(ai, "3.7 Computational implementation", "Heading 2")
    insert_before(
        ai,
        "The computations are implemented in Python using NumPy, SciPy and pandas "
        "for inference, simulation and market data processing, and Matplotlib for "
        "figures. The research repository records the experiment scripts, "
        "configurations, seeds, saved derived results and provenance manifests. "
        "The synthetic calculation integrates physical drift analytically "
        "conditional on volatility. For empirical validation, estimated volatility "
        "inputs obey the documented time cutoffs, and errors are resampled by "
        "valuation date to retain within-date contract dependence.",
    )
    conclusion = find(doc, "5. Conclusions and recommendations")
    insert_before(
        conclusion,
        "Compared with the related Asian-option valuation studies, these results do "
        "not establish that constant volatility is the best structural pricing "
        "model. They show how posterior integration and the choice of volatility "
        "input contribute differently to the pricing errors of one fixed benchmark.",
    )
    insert_before(
        find(doc, "Data availability"),
        "For valuation practice, the results support benchmarking historical "
        "volatility against earlier option-implied information and reporting "
        "posterior model-price dispersion separately from the PI–PM correction. "
        "Future work should expand the number of valuation dates and liquid "
        "contracts and examine stochastic-volatility and multifactor alternatives.",
    )


def format_tables(doc):
    # All table cells remain native and editable.
    for idx, table in enumerate(doc.tables):
        table.autofit = False
        if idx < 3:
            table.cell(0, 1).text = "N"
        if idx == 0:
            table.cell(3, 0).text = "Mean |PI − PM|"
        widths = (
            [Cm(8.3), Cm(2.5), Cm(4.6)] if idx == 0 else
            [Cm(6.8), Cm(1.8), Cm(2), Cm(2), Cm(2.4)] if idx in (1, 2) else
            [Cm(8.0), Cm(3.8), Cm(3.8)]
        )
        for col, width in zip(table.columns, widths):
            col.width = width
        for i, row in enumerate(table.rows):
            props = row._tr.get_or_add_trPr()
            props.append(OxmlElement("w:cantSplit"))
            if i == 0:
                props.append(OxmlElement("w:tblHeader"))
            for cell, width in zip(row.cells, widths):
                cell.width = width
                for p in cell.paragraphs:
                    p.paragraph_format.space_after = Pt(0)
                    p.paragraph_format.keep_with_next = (i < len(table.rows) - 1)
                    for run in p.runs:
                        run.font.name = "Times New Roman"
                        run.font.size = Pt(10)


def format_layout(doc):
    # Margins and fonts are from REMEF author instructions, not from the typeset PDF.
    for sec in doc.sections:
        sec.page_width, sec.page_height = Cm(21.59), Cm(27.94)
        sec.top_margin = sec.bottom_margin = Cm(2.5)
        sec.left_margin = sec.right_margin = Cm(3)
    styles = {p.style.name: p.style for p in doc.paragraphs}
    for name in ("Normal", "Body Text", "First Paragraph", "Bibliography",
                 "Heading 1", "Heading 2", "Heading 3"):
        if name not in styles:
            continue
        style = styles[name]
        style.font.name = "Times New Roman"
        style.font.size = Pt(12)
        style.font.color.rgb = RGBColor(0, 0, 0)
        style.paragraph_format.line_spacing = 1
        style.paragraph_format.space_after = Pt(3)
        if name.startswith("Heading"):
            style.font.bold = True
            style.paragraph_format.space_before = Pt(9)
            style.paragraph_format.space_after = Pt(5)
            style.paragraph_format.keep_with_next = True

    for p in doc.paragraphs:
        if p.style.name in ("Body Text", "Normal", "First Paragraph"):
            p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        for run in p.runs:
            run.font.color.rgb = RGBColor(0, 0, 0)
            if p.style.name.startswith("Heading"):
                run.font.name = "Times New Roman"
                run.font.size = Pt(12)
                run.font.bold = True

    for p in doc.paragraphs[:2]:
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_after = Pt(7)
        for run in p.runs:
            run.font.size = Pt(12)
            run.font.bold = True

    # JEL codes explicitly labelled in both languages.
    english = find(doc, "Keywords:")
    spanish = find(doc, "JEL: C11;")
    insert = english.insert_paragraph_before("JEL classification: C11; C15; C58; G13; G17; Q40.")
    english._p.addnext(insert._p)
    spanish.text = "Clasificación JEL: C11; C15; C58; G13; G17; Q40."

    for p in list(doc.paragraphs):
        if p.text.startswith(("Figure ", "Table ")):
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            p.paragraph_format.keep_with_next = True
            p.paragraph_format.keep_together = True
            p.paragraph_format.space_before = Pt(4)
            if p.text.startswith("Figure ") and "Source:" in p.text:
                cap, source = p.text.split("Source:", 1)
                p.text = cap.strip()
                extra = p.insert_paragraph_before()
                p._p.addnext(extra._p)
                extra.text = "Source: " + source.strip()
                for run in extra.runs:
                    run.italic = True
                    run.font.size = Pt(10)
            if p.text.startswith("Table 2.") and " Panel A: main out-of-sample comparison" in p.text:
                p.text = p.text.replace(" Panel A: main out-of-sample comparison", "")
                panel = p.insert_paragraph_before("Panel A: Main out-of-sample comparison")
                p._p.addnext(panel._p)
                panel.alignment = WD_ALIGN_PARAGRAPH.LEFT
                panel.paragraph_format.keep_with_next = True
                for run in panel.runs:
                    run.font.bold = True
                    run.font.size = Pt(10)
            for run in p.runs:
                run.font.name = "Times New Roman"
                run.font.size = Pt(10)
        if p.text.startswith("Panel B:"):
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            p.paragraph_format.keep_with_next = True
            for run in p.runs:
                run.font.size = Pt(10)
                run.font.bold = True
        if p.text.startswith("Source:"):
            for run in p.runs:
                run.font.size = Pt(10)
                run.italic = True
        if p.style.name == "Bibliography":
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            p.paragraph_format.left_indent = Cm(0.6)
            p.paragraph_format.first_line_indent = Cm(-0.6)
            for run in p.runs:
                run.font.name = "Times New Roman"
                run.font.size = Pt(12)

    # The author's funding and acknowledgments are not yet confirmed.
    # Omit the optional unfinished placeholder rather than print it as final text.
    remove(find(doc, "Acknowledgments and funding"))
    remove(find(doc, "To be completed and verified by the author"))
    doc.core_properties.author = ""
    doc.core_properties.last_modified_by = ""
    doc.core_properties.comments = ""


def prepare_docx(path: Path) -> None:
    doc = Document(path)
    adapt_sections(doc)
    format_layout(doc)
    format_tables(doc)
    doc.save(path)


if __name__ == "__main__":
    import sys
    prepare_docx(Path(sys.argv[1]))
