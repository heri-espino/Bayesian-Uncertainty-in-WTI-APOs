#!/usr/bin/env python3
"""Build the concise Journal of Futures Markets manuscript.

This build is intentionally separate from paper/build.py so the concise rewrite
can be compiled and reviewed without replacing the full manuscript or its PDF.

Usage
-----
python paper/build_short.py
python paper/build_short.py --check
python paper/build_short.py --clean
python paper/build_short.py --skip-figures
"""
from __future__ import annotations

import argparse
from pathlib import Path
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
PAPER_DIR = ROOT / "paper"
SOURCE_DIR = PAPER_DIR / "manuscript"
VENDOR_DIR = PAPER_DIR / "vendor" / "wiley_njd_v5"
PUBLICATION_FIGURES_DIR = ROOT / "figures" / "publication"

BUILD_DIR = PAPER_DIR / "build_short"
STAGE_DIR = BUILD_DIR / "stage"
MAIN_TEX = SOURCE_DIR / "main_short.tex"
STAGED_MAIN_NAME = MAIN_TEX.name
STAGED_STEM = MAIN_TEX.stem
FINAL_PDF = PAPER_DIR / "espino_2026_bayess-on-wti_short.pdf"

EXPECTED_CLASS = r"\documentclass[HARVARD,Utopia2COL]{WileyNJDv5}"
LEGACY_RESERVE_INSERTS = r"\reserveinserts{28}"
GUARDED_RESERVE_INSERTS = (
    r"\ifdefined\reserveinserts\reserveinserts{28}\fi"
)


def validate_layout() -> None:
    """Fail early when the concise manuscript or Wiley layout has drifted."""
    required = [
        MAIN_TEX,
        SOURCE_DIR / "references.bib",
        SOURCE_DIR / "sections_short",
        VENDOR_DIR / "WileyNJDv5.cls",
        VENDOR_DIR / "wileyNJD-Harvard.bst",
        VENDOR_DIR / "Fonts",
        PUBLICATION_FIGURES_DIR / "fig01_mechanism_map.pdf",
        PUBLICATION_FIGURES_DIR / "fig03_forward_q_cluster_bootstrap.pdf",
        PUBLICATION_FIGURES_DIR / "figure_manifest.json",
    ]
    missing = [path.relative_to(ROOT) for path in required if not path.exists()]
    if missing:
        formatted = "\n- ".join(str(path) for path in missing)
        raise SystemExit(
            "Concise manuscript layout check failed; missing:\n- " + formatted
        )

    source = MAIN_TEX.read_text(encoding="utf-8")
    if EXPECTED_CLASS not in source:
        raise SystemExit(
            "main_short.tex must preserve the selected Wiley layout: "
            + EXPECTED_CLASS
        )
    if "\\journal{Journal of Futures Markets}" not in source:
        raise SystemExit(
            "main_short.tex must identify Journal of Futures Markets"
        )

    expected_inputs = (
        "sections_short/01_introduction",
        "sections_short/02_posterior_pricing",
        "sections_short/03_data_design",
        "sections_short/04_results",
        "sections_short/05_robustness",
        "sections_short/06_conclusion",
    )
    missing_inputs = [
        section
        for section in expected_inputs
        if f"\\input{{{section}}}" not in source
    ]
    if missing_inputs:
        formatted = "\n- ".join(missing_inputs)
        raise SystemExit(
            "main_short.tex is missing expected section inputs:\n- " + formatted
        )


def clean() -> None:
    """Remove only concise-manuscript generated products."""
    shutil.rmtree(BUILD_DIR, ignore_errors=True)
    FINAL_PDF.unlink(missing_ok=True)


def prepare_stage() -> None:
    """Create an isolated compilation tree under paper/build_short/."""
    STAGE_DIR.parent.mkdir(parents=True, exist_ok=True)
    if STAGE_DIR.exists():
        shutil.rmtree(STAGE_DIR)

    shutil.copytree(VENDOR_DIR, STAGE_DIR)
    shutil.copytree(SOURCE_DIR, STAGE_DIR, dirs_exist_ok=True)

    if PUBLICATION_FIGURES_DIR.exists():
        shutil.copytree(
            PUBLICATION_FIGURES_DIR,
            STAGE_DIR / "figures" / "publication",
            dirs_exist_ok=True,
        )

    staged_class = STAGE_DIR / "WileyNJDv5.cls"
    source = staged_class.read_text(encoding="utf-8")
    if source.count(LEGACY_RESERVE_INSERTS) != 1:
        raise SystemExit(
            "Could not apply the Wiley/LaTeX compatibility patch: expected "
            "one \\reserveinserts{28} command in the staged class"
        )
    staged_class.write_text(
        source.replace(LEGACY_RESERVE_INSERTS, GUARDED_RESERVE_INSERTS),
        encoding="utf-8",
    )

    (STAGE_DIR / "listings.sty").unlink(missing_ok=True)


def run(command: list[str]) -> None:
    """Run one compiler command in the concise staging directory."""
    print("+", " ".join(command), flush=True)
    subprocess.run(command, cwd=STAGE_DIR, check=True)


def compiler(name: str) -> str | None:
    return shutil.which(name)


def build_publication_figures() -> None:
    """Regenerate publication figures from committed results."""
    command = [
        sys.executable,
        "-m",
        "scripts.build_publication_figures",
        "--formats",
        "pdf",
        "png",
    ]
    print("+", " ".join(command), flush=True)
    subprocess.run(command, cwd=ROOT, check=True)


def build(*, skip_figures: bool = False) -> Path:
    """Compile main_short.tex and return the exported concise PDF path."""
    validate_layout()
    if not skip_figures:
        build_publication_figures()
    prepare_stage()

    latexmk = compiler("latexmk")
    xelatex = compiler("xelatex")
    bibtex = compiler("bibtex")

    if latexmk and xelatex:
        run(
            [
                latexmk,
                "-xelatex",
                "-bibtex",
                "-interaction=nonstopmode",
                "-halt-on-error",
                "-file-line-error",
                STAGED_MAIN_NAME,
            ]
        )
    elif xelatex and bibtex:
        common = [
            xelatex,
            "-interaction=nonstopmode",
            "-halt-on-error",
            "-file-line-error",
            STAGED_MAIN_NAME,
        ]
        run(common)
        run([bibtex, STAGED_STEM])
        run(common)
        run(common)
    else:
        raise SystemExit(
            "XeLaTeX toolchain not found. Install TeX Live with xelatex, "
            "bibtex and preferably latexmk. Run "
            "python paper/build_short.py --check for a compiler-free "
            "structure check."
        )

    staged_pdf = STAGE_DIR / f"{STAGED_STEM}.pdf"
    if not staged_pdf.exists():
        raise SystemExit(
            f"Compilation finished without producing {staged_pdf.name}"
        )

    FINAL_PDF.unlink(missing_ok=True)
    shutil.move(staged_pdf, FINAL_PDF)
    print(f"Built {FINAL_PDF.relative_to(ROOT)}")
    return FINAL_PDF


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check",
        action="store_true",
        help="validate concise manuscript/vendor structure without invoking LaTeX",
    )
    parser.add_argument(
        "--clean",
        action="store_true",
        help="remove paper/build_short and the concise exported PDF",
    )
    parser.add_argument(
        "--skip-figures",
        action="store_true",
        help="use existing publication figures instead of regenerating them",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)

    if args.clean:
        clean()
        if not args.check:
            return 0

    if args.check:
        validate_layout()
        print("Concise JFM manuscript layout check passed")
        return 0

    build(skip_figures=args.skip_figures)
    return 0


if __name__ == "__main__":
    sys.exit(main())
