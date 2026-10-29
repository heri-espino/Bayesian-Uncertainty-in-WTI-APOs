"""Offline regression checks for the JFM editor/reviewer submission boundary."""
from pathlib import Path
import zipfile

from scripts import build_jfm_submission_extras as extras

ROOT = Path(__file__).resolve().parents[1]


def test_reviewer_pdf_removes_wiley_unassigned_production_text():
    main = (ROOT / "paper/manuscript/main_short.tex").read_text()
    assert r"\gdef\@history@dates{}" in main
    assert r"\gdef\@DOI@text{}" in main
    assert r"\gdef\oddfoot@titlepage@info{}" in main
    assert r"\author[1]{Anonymous Author}" in main


def test_jfm_figure1_only_removes_inset_for_wiley():
    src = (ROOT / "scripts/build_publication_figures.py").read_text()
    assert 'rotation=(40 if CURRENT_JOURNAL == "jfm" else 65)' in src
    assert 'if CURRENT_JOURNAL != "jfm":\n        _add_partial_fixing_zoom(ax_c, curve)' in src


def test_submission_package_excludes_editor_identifiers(tmp_path):
    folder = tmp_path / "stage"
    (folder / "sections_short").mkdir(parents=True)
    (folder / "figures" / "publication").mkdir(parents=True)
    (folder / "main.tex").write_text("\\author{Anonymous Author}\n")
    (folder / "sections_short" / "01.tex").write_text("Blind main text\n")
    (folder / "references.bib").write_text("")
    (folder / "figures" / "publication" / "plot.pdf").write_bytes(b"%PDF-1.4\n")
    (folder / "jfm_title_page.tex").write_text("Author's private identity")
    target = extras.blinded_source_package(folder, tmp_path / "blind.zip")
    with zipfile.ZipFile(target) as z:
        paths = z.namelist()
        assert "main.tex" in paths
        assert "sections_short/01.tex" in paths
        assert "figures/publication/plot.pdf" in paths
        assert "jfm_title_page.tex" not in paths


def test_supplement_exists_and_convergence_does_not_claim_market_calibration():
    supplement = (ROOT / "paper/supplement/jfm_supporting_information.tex").read_text()
    grid = (ROOT / "experiments/jfm_grid_sensitivity.py").read_text()
    assert r"\section*{S6. Market-price provenance" in supplement
    assert "513" in supplement and "4,097" in supplement
    assert "not a validated statement" in supplement
    assert "GRIDS = (513, 1025, 2049, 4097)" in grid
    assert "original_rows" in grid
    assert "archived_original" in grid


def test_manual_build_contains_separate_files_and_does_not_autocommit():
    workflow = (ROOT / ".github/workflows/build-paper.yml").read_text()
    assert "python -m scripts.build_jfm_submission_extras" in workflow
    assert "paper/jfm_title_page.pdf" in workflow
    assert "paper/supplement/jfm_supporting_information.pdf" in workflow
    assert "paper/jfm_blinded_latex_sources.zip" in workflow
    assert "workflow_dispatch:" in workflow
    assert "git push" not in workflow
