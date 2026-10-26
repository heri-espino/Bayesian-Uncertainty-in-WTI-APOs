"""Manual staged Elsevier CAS working-draft builder; never runs experiments.

Usage: python paper/jcm/build.py --check | --clean | (build)
The build copies existing validated concise sections/figures into isolated
paper/jcm/build/stage/ without modifying frozen CAS or Wiley source files.
"""
from __future__ import annotations

import argparse
from pathlib import Path
import shutil
import subprocess

ROOT = Path(__file__).resolve().parents[2]
PAPER = ROOT / "paper"
HERE = PAPER / "jcm"
CAS = PAPER / "els-cas-templates"
MANUSCRIPT = PAPER / "manuscript"
FIGURES = ROOT / "figures" / "publication"
BUILD = HERE / "build"
STAGE = BUILD / "stage"
PDF = BUILD / "jcm_working_draft.pdf"

SECTIONS = (
    "01_introduction", "02_posterior_pricing", "03_data_design",
    "04_results", "05_robustness", "06_conclusion",
)


def validate_layout() -> None:
    required = [
        HERE / "main.tex", CAS / "cas-dc.cls", CAS / "cas-common.sty",
        CAS / "cas-model2-names.bst", MANUSCRIPT / "references.bib",
        FIGURES / "ten_million" / "fig01_mechanism_map.pdf",
        FIGURES / "fig03_forward_q_cluster_bootstrap.pdf",
    ]
    required.extend(
        MANUSCRIPT / "sections_short" / f"{item}.tex" for item in SECTIONS
    )
    missing = [str(p.relative_to(ROOT)) for p in required if not p.is_file()]
    if missing:
        raise ValueError("CAS draft prerequisites missing: " + ", ".join(missing))
    source = (HERE / "main.tex").read_text(encoding="utf-8")
    if r"\documentclass[a4paper,fleqn]{cas-dc}" not in source:
        raise ValueError("The working paper must use the author's CAS-dc template")
    for item in SECTIONS:
        if rf"\input{{sections_short/{item}}}" not in source:
            raise ValueError(f"Missing original verified manuscript section: {item}")
    if "2020--2026" not in source or "not yet" not in source:
        raise ValueError("Data-not-yet-validated disclosure is mandatory")


def prepare_stage() -> None:
    validate_layout()
    if STAGE.exists():
        shutil.rmtree(STAGE)
    STAGE.mkdir(parents=True)
    for name in ("cas-dc.cls", "cas-common.sty", "cas-model2-names.bst"):
        shutil.copy2(CAS / name, STAGE / name)
    shutil.copy2(HERE / "main.tex", STAGE / "main.tex")
    shutil.copy2(MANUSCRIPT / "references.bib", STAGE / "references.bib")
    shutil.copytree(MANUSCRIPT / "sections_short", STAGE / "sections_short")
    shutil.copytree(FIGURES, STAGE / "figures" / "publication")


def build() -> None:
    prepare_stage()
    latexmk = shutil.which("latexmk")
    pdflatex = shutil.which("pdflatex")
    bibtex = shutil.which("bibtex")
    if latexmk and pdflatex:
        commands = [[latexmk, "-pdf", "-interaction=nonstopmode",
                     "-halt-on-error", "-file-line-error", "main.tex"]]
    elif pdflatex and bibtex:
        base = [pdflatex, "-interaction=nonstopmode", "-halt-on-error", "main.tex"]
        commands = [base, [bibtex, "main"], base, base]
    else:
        raise SystemExit("Install pdflatex and bibtex, preferably latexmk")
    for command in commands:
        subprocess.run(command, cwd=STAGE, check=True)
    result = STAGE / "main.pdf"
    if not result.is_file():
        raise RuntimeError("TeX did not produce a PDF")
    shutil.copy2(result, PDF)
    print(PDF)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--clean", action="store_true")
    args = parser.parse_args()
    if args.clean:
        shutil.rmtree(BUILD, ignore_errors=True)
    elif args.check:
        validate_layout()
        print("CAS working draft source check passed")
    else:
        build()


if __name__ == "__main__":
    main()
