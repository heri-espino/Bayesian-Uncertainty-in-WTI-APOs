"""JFM source/archived-data regression checks; no expensive simulations."""
from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_grid_convergence_archive_and_original_design_not_modified():
    out = ROOT / "results/analysis/jfm_confirmatory"
    manifest = json.loads((out / "grid_coverage_manifest.json").read_text())
    assert manifest["historical_independent_datasets"] == 160
    assert manifest["grid_nodes"] == [513, 1025, 2049, 4097]
    for filename, checksum in manifest["files"].items():
        assert hashlib.sha256((out / filename).read_bytes()).hexdigest() == checksum
    with (out / "grid_coverage_summary.csv").open(newline="") as handle:
        rows = list(csv.DictReader(handle))
    assert len(rows) == 12
    for rho, count in ((1.0, 456), (0.75, 313), (0.5, 153)):
        group = [x for x in rows if float(x["rho"]) == rho]
        assert len(group) == 4
        assert all(int(x["covered"]) == count for x in group)
        assert all(int(x["state_rows"]) == 480 for x in group)
    with (out / "grid_coverage_rows.csv").open(newline="") as handle:
        assert sum(1 for _ in handle) - 1 == 5760


def test_review_pdf_has_no_fictitious_njd5_publication_metadata():
    source = (ROOT / "paper/manuscript/main_short.tex").read_text()
    verify = (ROOT / "scripts/verify_jfm_runner_build.py").read_text()
    assert r"\gdef\@received{}" in source
    assert r"\gdef\@accepted{}" in source
    assert r"\doiheadtext{}" in source
    assert "copyright holder name" in verify.lower()
    assert "added at production" in verify.lower()
    assert "xxx/xxxx" in verify


def test_jfm_addenda_are_separate_and_manual_only():
    build = (ROOT / "paper/build_jfm_addenda.py").read_text()
    supplement = (ROOT / "paper/supplement/jfm_supporting_information.tex").read_text()
    workflow = (ROOT / ".github/workflows/build-paper.yml").read_text()
    assert "jfm_supporting_information.tex" in build
    assert "jfm_title_page.tex" in build
    assert "Heriberto" not in supplement
    assert r"\begin{document}" in supplement
    assert r"\section{Bounded numerical reference" in supplement
    assert "python paper/build_jfm_addenda.py" in workflow
    assert "workflow_dispatch:" in workflow
    assert "paper/jfm_supporting_information.pdf" in workflow
    assert "paper/jfm_title_page.pdf" in workflow
    # The existing main reviewer PDF must remain independently anonymized.
    reviewer_source = (ROOT / "paper/manuscript/main_short.tex").read_text()
    assert r"\input{jfm_title_page.tex}" not in reviewer_source
    assert r"\include{jfm_title_page.tex}" not in reviewer_source
