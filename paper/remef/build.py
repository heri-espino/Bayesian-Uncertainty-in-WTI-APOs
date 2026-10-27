#!/usr/bin/env python3
"""Assemble an editable Word *review draft* for REMEF from the concise source.

Requirements: pandoc (in PATH) and python-docx. No simulations are run.
Usage:
  python paper/remef/build.py             # anonymized reviewer draft
  python paper/remef/build.py --author-version
  python paper/remef/build.py --check     # validate inputs, no Word conversion

This script intentionally does NOT replace the independent Wiley/JFM builders.
"""
from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import tempfile
from pathlib import Path
from xml.etree import ElementTree as ET

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
SHORT = ROOT / "paper" / "manuscript" / "sections_short"
FIGURES = ROOT / "figures" / "publication"
BUILD = HERE / "build"
SVG_DIR = BUILD / "vector_figures"
# REMEF-specific scientific sections; Wiley/JFM sources stay frozen.
REMEF_SECTIONS = HERE / "sections"
BODY_SECTIONS = [
    REMEF_SECTIONS / "02_posterior_pricing.tex",
    REMEF_SECTIONS / "03_data_design.tex",
    REMEF_SECTIONS / "04_results.tex",
    REMEF_SECTIONS / "05_robustness.tex",
    REMEF_SECTIONS / "06_conclusion.tex",
]
REFERENCES = [
    ROOT / "paper" / "manuscript" / "references.bib",
    HERE / "references.bib",
]
LABEL_RE = re.compile(r"\\label\{([^}]+)\}")
ENV_RE = re.compile(r"\\begin\{(equation|figure\*?|table\*?)\}(?:\[[^\]]*\])?", re.DOTALL)
FIG_RE = re.compile(r"\\begin\{figure\*?\}(?:\[[^\]]*\])?(.*?)\\end\{figure\*?\}", re.DOTALL)
TAB_RE = re.compile(r"\\begin\{table\*?\}(?:\[[^\]]*\])?(.*?)\\end\{table\*?\}", re.DOTALL)
CAPTION_RE = re.compile(r"\\caption\{((?:[^{}]|\{[^{}]*\})*)\}", re.DOTALL)


def validate() -> None:
    paths = [HERE / "frontmatter.tex", HERE / "introduction.tex", HERE / "apa.csl", HERE / "postprocess.py", *BODY_SECTIONS, *REFERENCES]
    paths.extend(FIGURES / name for name in [
        "ten_million/fig01_mechanism_map.pdf",
        "fig02_historical_vs_apo_implied_volatility.pdf",
        "fig03_forward_q_cluster_bootstrap.pdf",
        "fig04_numerical_identification.pdf",
    ])
    missing = [str(p.relative_to(ROOT)) for p in paths if not p.is_file()]
    if missing:
        raise SystemExit("Missing REMEF build inputs:\n- " + "\n- ".join(missing))


def authorship() -> str:
    """Author-identifying metadata, NEVER included in blinded review output.

    REMEF requests a correspondence footnote on the first page. The author has
    supplied a name, academic email, ORCID, professional pages, campus
    mailing address, and university telephone number.
    """
    return r"""
\begin{center}
\textbf{Heriberto Espino-Montelongo}\footnote{Corresponding author: Heriberto Espino-Montelongo; email: heriberto.espinomo@udlap.mx. Institutional postal address: Ex Hacienda Santa Catarina M\'artir s/n, San Andr\'es Cholula, Puebla, C.P. 72810, M\'exico. Telephone: +52 222 810 1202.}\\
Universidad de las Américas Puebla, Mexico\\
ORCID: https://orcid.org/0009-0009-1230-2931
\end{center}
\noindent\textbf{Professional website:} https://heri-espino.github.io\\
\noindent\textbf{LinkedIn:} https://www.linkedin.com/in/heri-espino/
"""


def _numbered_labels(tex: str) -> dict[str, str]:
    counts = {"equation": 0, "figure": 0, "table": 0}
    labels: dict[str, str] = {}
    for match in ENV_RE.finditer(tex):
        category = match.group(1).rstrip("*")
        counts[category] += 1
        close = re.search(
            r"\\end\{" + re.escape(match.group(1)) + r"\}", tex[match.end():],
        )
        if close is None:
            raise ValueError(f"Unclosed {category} environment")
        content = tex[match.end():match.end() + close.start()]
        for label in LABEL_RE.findall(content):
            labels[label] = str(counts[category])
    return labels


def _rewrite_figures(tex: str, labels: dict[str, str]) -> str:
    def convert(match: re.Match[str]) -> str:
        body = match.group(1)
        caption = CAPTION_RE.search(body)
        path_match = re.search(r"\\includegraphics(?:\[[^\]]*\])?\{([^}]+)\}", body)
        ids = LABEL_RE.findall(body)
        if caption is None or path_match is None or not ids:
            raise ValueError("Figure without caption, image path, or label")
        source = Path(path_match.group(1))
        pdf = ROOT / source
        if source.suffix.lower() != ".pdf" or not pdf.is_file():
            raise ValueError(f"Missing vector PDF source: {source}")
        img = SVG_DIR / (source.stem + ".svg")
        n = labels[ids[0]]
        cap = caption.group(1)
        return (r"\begin{center}" + "\n" +
                r"\includegraphics[width=0.94\linewidth]{" + img.relative_to(ROOT).as_posix() + "}\n" +
                r"\end{center}" + "\n" +
                r"\noindent\textbf{Figure " + n + ".} " + cap + "\n" +
                r"\noindent\textit{Source: Authors' calculations from the recorded experiment outputs.}" + "\n")
    return FIG_RE.sub(convert, tex)



def _sanitize_and_repair_svg(path: Path, *, repair_figure_3: bool = False) -> None:
    """Remove inherited PDF metadata; repair Figure 3's clipped top heading.

    Conversion from the committed vector PDF retains paths, text outlines,
    axes and hybrid raster artists. A white band replaces the originally
    cropped Figure 3 heading, and clean centered SVG text is drawn below the
    top edge. No numerical data or plotting coordinates are changed.
    """
    ns = "http://www.w3.org/2000/svg"
    ET.register_namespace("", ns)
    ET.register_namespace("xlink", "http://www.w3.org/1999/xlink")
    tree = ET.parse(path)
    root = tree.getroot()
    for parent in root.iter():
        for child in list(parent):
            if child.tag.split("}")[-1].lower() in {"metadata", "desc"}:
                parent.remove(child)
    if repair_figure_3:
        box = root.attrib.get("viewBox")
        if not box:
            raise ValueError(f"SVG lacks viewBox for title correction: {path}")
        x, y, width, height = [float(part) for part in box.split()]
        # The original PDF clipped its title above the top page edge.
        # The upper 12% is white space preceding both chart panels.
        ET.SubElement(root, f"{{{ns}}}rect", {
            "x": str(x), "y": str(y),
            "width": str(width), "height": str(0.12 * height),
            "fill": "#ffffff",
        })
        title = ET.SubElement(root, f"{{{ns}}}text", {
            "x": str(x + width / 2), "y": str(y + 0.072 * height),
            "text-anchor": "middle",
            "font-family": "Times New Roman",
            "font-size": "10.5",
            "fill": "#111111",
        })
        title.text = "Forward-in-time volatility comparisons across expiries"
    tree.write(path, encoding="utf-8", xml_declaration=True)
    # The blinded copy must not receive the source PDF's Author metadata.
    data = path.read_text(encoding="utf-8")
    if any(token in data.lower() for token in (
        "heriberto", "espino-montelongo", "@udlap.mx",
    )):
        raise ValueError(f"Author-identifying metadata in reviewer SVG: {path}")


def prepare_vector_figures() -> list[Path]:
    """Generate genuine SVG drawings from the four committed vector PDFs.

    Pandoc 3 embeds them with DrawingML asvg:svgBlip. A raster compatibility
    fallback may be included for older Word versions, but SVG is the main
    rendering source. Requires Inkscape, not Monte Carlo or proprietary data.
    """
    inkscape = shutil.which("inkscape")
    if not inkscape:
        raise SystemExit(
            "Inkscape is required for native SVG Word figures. "
            "Install it before building the REMEF Word manuscript."
        )
    sources = (
        FIGURES / "ten_million" / "fig01_mechanism_map.pdf",
        FIGURES / "fig02_historical_vs_apo_implied_volatility.pdf",
        FIGURES / "fig03_forward_q_cluster_bootstrap.pdf",
        FIGURES / "fig04_numerical_identification.pdf",
    )
    SVG_DIR.mkdir(parents=True, exist_ok=True)
    paths = []
    for source in sources:
        if not source.is_file():
            raise FileNotFoundError(f"Missing committed vector PDF: {source}")
        dest = SVG_DIR / (source.stem + ".svg")
        subprocess.run(
            [inkscape, str(source), "--export-plain-svg",
             "--export-filename=" + str(dest)],
            check=True, capture_output=True, text=True,
        )
        if not dest.is_file() or dest.stat().st_size < 512:
            raise ValueError(f"Vector figure conversion failed: {dest}")
        _sanitize_and_repair_svg(
            dest, repair_figure_3=(source.stem == "fig03_forward_q_cluster_bootstrap")
        )
        paths.append(dest)
    return paths


def _rewrite_tables(tex: str, labels: dict[str, str]) -> str:
    def convert(match: re.Match[str]) -> str:
        body = match.group(1)
        caption = CAPTION_RE.search(body)
        ids = LABEL_RE.findall(body)
        if caption is None or not ids:
            raise ValueError("Table without caption or label")
        n = labels[ids[0]]
        result = CAPTION_RE.sub("", body, count=1)
        result = LABEL_RE.sub("", result)
        result = result.replace(r"\centering", "").replace(r"\vspace{5pt}", "")
        # Pandoc represents each tabular as a real, editable Word table.
        return (r"\noindent\textbf{Table " + n + ".} " + caption.group(1) + "\n" +
                result.strip() + "\n" +
                r"\noindent\textit{Source: Authors' calculations from the recorded experiment outputs.}" + "\n")
    return TAB_RE.sub(convert, tex)


def make_latex(*, with_author: bool) -> str:
    sources = [HERE / "frontmatter.tex", HERE / "introduction.tex", *BODY_SECTIONS]
    sections = [p.read_text(encoding="utf-8") for p in sources]
    # Place the required disclosure in Methods, not outside the research design.
    disclosure = (
        r"\subsection{AI-assisted manuscript preparation}" + "\n"
        "OpenAI ChatGPT assisted with research software development, literature "
        "organization, language editing, and drafting and revision of the manuscript. "
        "The author remains responsible for the methods, numerical calculations, "
        "independent checking and interpretation of the results."
        + (" The corresponding research software is archived on Zenodo.\n"
           if with_author else "\n")
    )
    sections[3] += "\n" + disclosure
    if with_author:
        sections[0] = authorship() + "\n" + sections[0]
    data_note = (
        r"\section*{Data availability}" + "\n"
        "The primary empirical study draws on Barchart WTI Average Price "
        "Option end-of-day fields (which can serve as settlement proxies), "
        "CL futures contract histories, and Databento standard WTI/LO "
        "option data. A distinct longer-date conditional benchmark uses "
        "Databento AAO option definitions and settlement statistics; "
        "its option forward-average and discount inputs are estimated from "
        "other same-date AAO strikes by put--call parity. These inputs are "
        "not equivalent to direct contemporaneous CL fixing histories. "
        "Vendor/exchange original data and private contract-level results "
        "are subject to licensing and are not redistributed publicly. "
        "Replication requires independently licensed observations, "
        "source-vintage verification and the computational workflow "
        "specified in the supporting research records.\n"
    )
    if with_author:
        code_note = (
            "The source-only research software accompanying this study is "
            "archived as version 0.1.0 on Zenodo "
            "\\citep{espino2026software}: "
            "https://doi.org/10.5281/zenodo.23468649. "
            "Its public source repository is "
            "https://github.com/heri-espino/WTI-Asian-Option-Pricing. "
            "It includes pricing and Bayesian-inference code, synthetic "
            "demonstrations, numerical tests, and scripts for empirical "
            "WTI Average Price Option comparisons. The synthetic examples "
            "do not require proprietary inputs; reproducing empirical "
            "results requires independently licensed market observations, "
            "which are neither redistributed nor deposited in Zenodo.\n"
        )
    else:
        code_note = (
            "The source-only companion software contains pricing and Bayesian-"
            "inference code, synthetic demonstrations, numerical tests, and "
            "scripts for the empirical analyses. Its identifying repository "
            "location is omitted here to preserve double-blind review and may "
            "be provided confidentially to the editor. Re-executing empirical "
            "experiments requires separately licensed vendor observations.\n"
        )
    statements = (
        data_note +
        r"\section*{Code and results availability}" + "\n" + code_note +
        r"\section*{Funding}" + "\n"
        "This research received no external funding.\n"
        r"\section*{Conflicts of interest}" + "\n"
        "The author declares no conflicts of interest.\n"
    )
    combined = "\n\n".join(sections) + "\n" + statements
    labels = _numbered_labels(combined)
    combined = _rewrite_figures(combined, labels)
    combined = _rewrite_tables(combined, labels)
    combined = re.sub(r"\\eqref\{([^}]+)\}", lambda m: "(" + labels[m.group(1)] + ")", combined)
    combined = re.sub(r"\\ref\{([^}]+)\}", lambda m: labels[m.group(1)], combined)
    combined = LABEL_RE.sub("", combined)
    combined = re.sub(r"\\begin\{equation\}", r"\\[", combined)
    combined = re.sub(r"\\end\{equation\}", r"\\]", combined)
    # Avoid leaving Wiley-only LaTeX commands in the Word source.
    combined = combined.replace(r"\toprule", r"\hline")
    combined = combined.replace(r"\midrule", r"\hline")
    combined = combined.replace(r"\bottomrule", r"\hline")
    return combined


def format_docx(path: Path) -> None:
    from postprocess import prepare_docx
    prepare_docx(path)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="validate source only")
    parser.add_argument("--author-version", action="store_true",
                        help="include author page metadata placeholders")
    args = parser.parse_args()
    validate()
    latex = make_latex(with_author=args.author_version)
    if args.check:
        print(f"REMEF source check passed ({len(latex)} generated LaTeX chars).")
        return
    if not shutil.which("pandoc"):
        raise SystemExit("Install pandoc for native Word tables and editable OMML equations.")
    BUILD.mkdir(parents=True, exist_ok=True)
    vector_paths = prepare_vector_figures()
    print(f"Prepared {len(vector_paths)} native SVG figures for Word.")
    target = BUILD / ("remef_author_draft.docx" if args.author_version else "remef_blinded_draft.docx")
    with tempfile.TemporaryDirectory(prefix="remef-") as td:
        tex = Path(td) / "manuscript.tex"
        tex.write_text(latex, encoding="utf-8")
        command = [
            "pandoc", "--from=latex", "--to=docx", "--standalone", "--citeproc",
            "--metadata=reference-section-title:References",
            "--csl=" + str(HERE / "apa.csl"),
            "--resource-path=" + str(ROOT),
            "--bibliography=" + str(REFERENCES[0]),
            "--bibliography=" + str(REFERENCES[1]),
            "-o", str(target), str(tex),
        ]
        subprocess.run(command, check=True, cwd=ROOT)
    format_docx(target)
    print(f"Built {target.relative_to(ROOT)}")
    print("DRAFT ONLY: render/inspect all pages; verify 25-page cap, figures, captions, ")
    print("math editability, references, proprietary data and author declarations.")


if __name__ == "__main__":
    main()
