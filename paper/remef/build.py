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

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
SHORT = ROOT / "paper" / "manuscript" / "sections_short"
FIGURES = ROOT / "figures" / "publication"
BUILD = HERE / "build"
BODY_SECTIONS = [
    SHORT / "02_posterior_pricing.tex",
    SHORT / "03_data_design.tex",
    SHORT / "04_results.tex",
    SHORT / "05_robustness.tex",
    SHORT / "06_conclusion.tex",
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
        "fig01_mechanism_map.png",
        "fig03_forward_q_cluster_bootstrap.png",
    ])
    missing = [str(p.relative_to(ROOT)) for p in paths if not p.is_file()]
    if missing:
        raise SystemExit("Missing REMEF build inputs:\n- " + "\n- ".join(missing))


def authorship() -> str:
    """Author-identifying metadata, NEVER included in blinded review output.

    REMEF requests a correspondence footnote on the first page. The author has
    supplied a name, academic email, ORCID and professional pages but has not
    supplied a mailing address or telephone. Do not fabricate either.
    """
    return r"""
\begin{center}
\textbf{Heriberto Espino-Montelongo}\footnote{Corresponding author: Heriberto Espino-Montelongo; email: heriberto.espinomo@udlap.mx. Postal correspondence address and telephone: [author to supply before submission].}\\
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
        img = source.with_suffix(".png")
        if not (ROOT / img).is_file():
            raise ValueError(f"Missing 300-dpi PNG version of {source}")
        n = labels[ids[0]]
        cap = caption.group(1)
        return (r"\begin{center}" + "\n" +
                r"\includegraphics[width=0.94\linewidth]{" + img.as_posix() + "}\n" +
                r"\end{center}" + "\n" +
                r"\noindent\textbf{Figure " + n + ".} " + cap + "\n" +
                r"\noindent\textit{Source: Authors' calculations from the recorded experiment outputs.}" + "\n")
    return FIG_RE.sub(convert, tex)


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
        "OpenAI ChatGPT was used for language editing, literature organization, "
        "and manuscript restructuring and conversion. It was not the source of "
        "the reported data or computed results. The author is responsible for "
        "verifying the scientific content and disclosure before submission.\n"
    )
    sections[3] += "\n" + disclosure
    if with_author:
        sections[0] = authorship() + "\n" + sections[0]
    # The reviewer version must not publish identifying repo URLs or affiliations.
    statements = (
        r"\section*{Data availability}" + "\n"
        "The original market data are subject to the vendors' redistribution "
        "conditions. Derived summaries, provenance records and source code "
        "are available from the corresponding author subject to a licensing "
        "and double-blind-review check.\n"
        r"\section*{Code and results availability}" + "\n"
        "Reproducible experiment code and recorded derived summaries have "
        "been prepared in a version-controlled research repository. "
        "A non-identifying access route is to be established before submission.\n"
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
