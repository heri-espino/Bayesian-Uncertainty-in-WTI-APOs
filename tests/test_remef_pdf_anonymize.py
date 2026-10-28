"""Regression tests for Word-exported REMEF reviewer PDF anonymity."""
from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "paper" / "remef" / "anonymize_review_pdf.py"


def _module():
    spec = importlib.util.spec_from_file_location("_remef_anonymize", SOURCE)
    assert spec is not None and spec.loader is not None
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_pdf_anonymizer_rejects_nonblinded_name(tmp_path):
    mod = _module()
    with pytest.raises(ValueError, match="Only the blinded"):
        mod.anonymize(tmp_path / "remef_author_draft.pdf", tmp_path / "out.pdf")


def test_word_exported_author_metadata_removed(tmp_path):
    pypdf = pytest.importorskip("pypdf")
    mod = _module()
    source = tmp_path / "remef_blinded_draft.pdf"
    output = tmp_path / "review_sanitized.pdf"
    writer = pypdf.PdfWriter()
    writer.add_blank_page(width=612, height=792)
    writer.add_metadata({
        "/Author": "Heriberto Espino Montelongo",
        "/Creator": "Microsoft Word",
        "/Title": "Draft",
    })
    with source.open("wb") as out:
        writer.write(out)

    mod.anonymize(source, output)
    result = pypdf.PdfReader(str(output))
    assert len(result.pages) == 1
    assert result.metadata.get("/Author") == ""
    assert result.metadata.get("/Creator") == ""
    assert result.xmp_metadata is None
    assert result.metadata.get("/Title") == mod.TITLE
