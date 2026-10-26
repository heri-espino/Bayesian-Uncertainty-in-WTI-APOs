"""Static tests for source-safe staged Elsevier manuscript."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_jcm_draft_discloses_missing_extended_validation():
    source = (ROOT / "paper/jcm/main.tex").read_text(encoding="utf-8")
    assert r"\documentclass[a4paper,fleqn]{cas-dc}" in source
    assert "2020--2026" in source
    assert "not yet" in source
    assert r"\bibliography{references}" in source


def test_cas_builder_does_not_run_inference_or_figures():
    code = (ROOT / "paper/jcm/build.py").read_text(encoding="utf-8")
    assert "copytree(FIGURES" in code
    assert "build_publication_figures" not in code
    assert "timeseries.get_range" not in code

def test_cas_source_layout_check_uses_existing_template():
    import subprocess
    import sys

    subprocess.run(
        [sys.executable, str(ROOT / "paper/jcm/build.py"), "--check"],
        cwd=ROOT, check=True, capture_output=True, text=True,
    )
