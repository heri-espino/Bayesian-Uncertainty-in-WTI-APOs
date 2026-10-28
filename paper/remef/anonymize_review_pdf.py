#!/usr/bin/env python3
"""Remove identifying PDF metadata from an already-blinded REMEF Word export.

Microsoft Word may insert the signed-in user's name into an exported PDF
even when the source DOCX has empty core author properties. This script
checks that the visible paper is blinded, removes document-info/XMP
metadata, and verifies the resulting PDF. It does not change scientific
text, re-run inference, or convert the author-identifying version.

Requires: python -m pip install pypdf
Usage:
  python paper/remef/anonymize_review_pdf.py paper/remef/review/remef_blinded_draft.pdf
  python paper/remef/anonymize_review_pdf.py input.pdf --output output.pdf
"""
from __future__ import annotations

import argparse
from pathlib import Path

TITLE = "Posterior Integration and Volatility Inputs in WTI Asian Options"
IDENTIFIERS = (
    "Heriberto",
    "Espino-Montelongo",
    "espinomo@udlap.mx",
    "0009-0009-1230-2931",
    "heri-espino.github.io",
)


def anonymize(input_path: Path, output_path: Path) -> None:
    if not input_path.is_file():
        raise FileNotFoundError(input_path)
    if "blinded" not in input_path.stem.lower():
        raise ValueError("Only the blinded review PDF may be anonymized by this script.")

    try:
        from pypdf import PdfReader, PdfWriter
        from pypdf.generic import NameObject
    except ImportError as exc:
        raise SystemExit("Install pypdf inside Conda: conda install -c conda-forge pypdf") from exc

    reader = PdfReader(str(input_path))
    if not reader.pages:
        raise ValueError("Empty PDF")
    for page_number, page in enumerate(reader.pages, start=1):
        visible = page.extract_text() or ""
        if any(marker.casefold() in visible.casefold() for marker in IDENTIFIERS):
            raise ValueError(f"Identifying text appears on page {page_number}. Fix the Word source first.")

    writer = PdfWriter()
    writer.append(reader)
    writer.add_metadata({
        "/Title": TITLE,
        "/Author": "",
        "/Creator": "",
        "/Producer": "",
        "/Subject": "",
        "/Keywords": "",
    })
    # Remove XMP, which can retain author fields independently of /Info.
    writer._root_object.pop(NameObject("/Metadata"), None)

    temporary = output_path.with_name(output_path.stem + ".sanitizing.tmp.pdf")
    try:
        with temporary.open("wb") as stream:
            writer.write(stream)
        checked = PdfReader(str(temporary))
        info = checked.metadata or {}
        if len(checked.pages) != len(reader.pages):
            raise ValueError("PDF page count changed during anonymization")
        if checked.xmp_metadata is not None:
            raise ValueError("XMP metadata still present")
        if any(marker.casefold() in str(info).casefold() for marker in IDENTIFIERS):
            raise ValueError("Identifying PDF document info still present")
        if str(info.get("/Author", "")).strip():
            raise ValueError("Blinded PDF Author field is not empty")
        temporary.replace(output_path)
    finally:
        temporary.unlink(missing_ok=True)
    print(f"Anonymized {len(reader.pages)} pages: {output_path}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("pdf", type=Path, help="blinded Word-exported PDF")
    parser.add_argument("--output", type=Path, help="output path; default: replace the original")
    args = parser.parse_args()
    anonymize(args.pdf, args.output or args.pdf)


if __name__ == "__main__":
    main()
