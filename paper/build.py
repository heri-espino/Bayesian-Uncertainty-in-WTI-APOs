#!/usr/bin/env python3
"""Build the internal Journal of Futures Markets manuscript.

The active manuscript is staged together with the unmodified Wiley NJDv5 vendor
bundle so that XeLaTeX can resolve the class, bibliography style, and bundled
Utopia fonts without system-wide font installation.

Usage
-----
python paper/build.py
python paper/build.py --check
python paper/build.py --clean
"""
from __future__ import annotations

import argparse
import os
from pathlib import Path
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
PAPER_DIR = ROOT / "paper"
SOURCE_DIR = PAPER_DIR / "manuscript"
VENDOR_DIR = PAPER_DIR / "vendor" / "wiley_njd_v5"
BUILD_DIR = PAPER_DIR / "build"
STAGE_DIR = BUILD_DIR / "stage"
MAIN_TEX = SOURCE_DIR / "main.tex"
FINAL_PDF = PAPER_DIR / "espino_2026_bayess-on-wti.pdf"
LEGACY_FINAL_PDFS = (
    BUILD_DIR / "jfm_internal_draft.pdf",
    BUILD_DIR / FINAL_PDF.name,
)
EXPECTED_CLASS = r"\documentclass[HARVARD,Utopia2COL]{WileyNJDv5}"
LEGACY_RESERVE_INSERTS = r"\reserveinserts{28}"
GUARDED_RESERVE_INSERTS = (
    r"\ifdefined\reserveinserts\reserveinserts{28}\fi"
)


def validate_layout() -> None:
    """Fail early when the manuscript or vendor layout has drifted."""
    required = [
        MAIN_TEX,
        SOURCE_DIR / "references.bib",
        VENDOR_DIR / "WileyNJDv5.cls",
        VENDOR_DIR / "wileyNJD-Harvard.bst",
        VENDOR_DIR / "Fonts",
    ]
    missing = [path.relative_to(ROOT) for path in required if not path.exists()]
    if missing:
        formatted = "\n- ".join(str(path) for path in missing)
        raise SystemExit(f"Manuscript layout check failed; missing:\n- {formatted}")

    source = MAIN_TEX.read_text(encoding="utf-8")
    if EXPECTED_CLASS not in source:
        raise SystemExit(
            "main.tex must preserve the selected Wiley layout: " + EXPECTED_CLASS
        )
    if "\\journal{Journal of Futures Markets}" not in source:
        raise SystemExit("main.tex must identify Journal of Futures Markets")


def clean() -> None:
    """Remove all generated LaTeX products."""
    shutil.rmtree(BUILD_DIR, ignore_errors=True)
    FINAL_PDF.unlink(missing_ok=True)


def prepare_stage() -> None:
    """Create an isolated compilation tree under paper/build/."""
    STAGE_DIR.parent.mkdir(parents=True, exist_ok=True)
    if STAGE_DIR.exists():
        shutil.rmtree(STAGE_DIR)

    # Wiley's class resolves bundled fonts using paths relative to the working
    # directory. Copying the vendor bundle into the disposable stage is more
    # portable than requiring local font installation or symlink support.
    shutil.copytree(VENDOR_DIR, STAGE_DIR)
    shutil.copytree(SOURCE_DIR, STAGE_DIR, dirs_exist_ok=True)

    # LaTeX releases from 2026 no longer expose etex's \reserveinserts
    # command because the extended allocation mechanism is built in.  Patch
    # only the disposable staged class so the frozen Wiley bundle continues
    # to work with both older and newer TeX installations.
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

    # The bundle's 2020 listings.sty is incompatible with the newer lstmisc
    # and lstpatch companion files installed by current MiKTeX/TeX Live.
    # Let the TeX installation resolve a consistent listings package instead.
    (STAGE_DIR / "listings.sty").unlink(missing_ok=True)


def run(command: list[str]) -> None:
    """Run one compiler command in the staging directory."""
    print("+", " ".join(command), flush=True)
    subprocess.run(command, cwd=STAGE_DIR, check=True)


def compiler(name: str) -> str | None:
    return shutil.which(name)


def build() -> Path:
    """Compile the manuscript with XeLaTeX and return the final PDF path."""
    validate_layout()
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
                "main.tex",
            ]
        )
    elif xelatex and bibtex:
        common = [
            xelatex,
            "-interaction=nonstopmode",
            "-halt-on-error",
            "-file-line-error",
            "main.tex",
        ]
        run(common)
        run([bibtex, "main"])
        run(common)
        run(common)
    else:
        raise SystemExit(
            "XeLaTeX toolchain not found. Install TeX Live with xelatex, bibtex "
            "and preferably latexmk. Run `python paper/build.py --check` for a "
            "compiler-free structure check."
        )

    staged_pdf = STAGE_DIR / "main.pdf"
    if not staged_pdf.exists():
        raise SystemExit("Compilation finished without producing main.pdf")
    for legacy_pdf in LEGACY_FINAL_PDFS:
        legacy_pdf.unlink(missing_ok=True)
    FINAL_PDF.unlink(missing_ok=True)
    shutil.move(staged_pdf, FINAL_PDF)
    print(f"Built {FINAL_PDF.relative_to(ROOT)}")
    return FINAL_PDF


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check",
        action="store_true",
        help="validate manuscript/vendor structure without invoking LaTeX",
    )
    parser.add_argument(
        "--clean",
        action="store_true",
        help="remove paper/build and the exported PDF before any requested check/build",
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
        print("JFM manuscript layout check passed")
        return 0
    build()
    return 0


if __name__ == "__main__":
    sys.exit(main())
