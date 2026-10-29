"""Build JFM anonymized supporting information and separate identifying title page.

Manual-only. Never mix the title page into the anonymous main manuscript or
supplement. The output PDFs are generated files and never auto-committed.
Usage: python paper/build_jfm_addenda.py [--check]
"""
from __future__ import annotations

import argparse
from pathlib import Path
import shutil
import subprocess

ROOT = Path(__file__).resolve().parents[1]
PAPER = ROOT / "paper"
BUILD = PAPER / "build" / "jfm_addenda"
ITEMS = (
    (PAPER / "supplement" / "jfm_supporting_information.tex",
     PAPER / "jfm_supporting_information.pdf", False),
    (PAPER / "manuscript" / "jfm_title_page.tex",
     PAPER / "jfm_title_page.pdf", True),
)
IDENTIFIERS = ("heri-espino", "espino-montelongo", "@udlap.mx", "heriberto")


def build(*, check: bool = False) -> None:
    for source, _, identified in ITEMS:
        if not source.exists():
            raise SystemExit(f"Missing JFM addendum source: {source}")
        text = source.read_text(encoding="utf-8")
        if not identified and any(tok in text.lower() for tok in IDENTIFIERS):
            raise SystemExit("Identifying author content in anonymous JFM supplement")
        if identified and "Heriberto Espino-Montelongo" not in text:
            raise SystemExit("Identifying title page does not contain author name")
        if r"\begin{document}" not in text:
            raise SystemExit(f"Malformed TeX source: {source}")
    if check:
        print("PASS: JFM addenda exist and are separated by anonymity")
        return
    if shutil.which("xelatex") is None:
        raise SystemExit("XeLaTeX is required for JFM addenda build")
    from pypdf import PdfReader

    for source, target, identified in ITEMS:
        stage = BUILD / source.stem
        stage.mkdir(parents=True, exist_ok=True)
        local = stage / source.name
        shutil.copy2(source, local)
        command = ["xelatex", "-interaction=nonstopmode", "-halt-on-error",
                   "-file-line-error", source.name]
        for _ in range(2):
            subprocess.run(command, cwd=stage, check=True,
                           timeout=120, stdout=subprocess.PIPE,
                           stderr=subprocess.STDOUT)
        built = stage / source.with_suffix(".pdf").name
        if not built.exists() or built.stat().st_size < 3000:
            raise SystemExit(f"No compiled PDF for {source}")
        reviewer = PdfReader(str(built))
        alltext = "\n".join(page.extract_text() or "" for page in reviewer.pages)
        if not identified and any(tok in alltext.lower() for tok in IDENTIFIERS):
            raise SystemExit("Identifying author content leaked into supplement PDF")
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(built, target)
        print(f"Built {target.relative_to(ROOT)} ({len(reviewer.pages)} pages)")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    build(check=parser.parse_args().check)
