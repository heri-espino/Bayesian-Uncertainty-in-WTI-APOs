"""JFM-only PGF bitmap asset paths and blinded manuscript regression checks."""
import sys
import types
from pathlib import Path

from scripts.jfm_pgf_asset_paths import (
    _add_pgf_graphicspath, jfm_pgf_sidecar_support
)


def test_pgf_asset_path_uses_actual_export_directory(tmp_path):
    pgf = tmp_path / "artwork" / "fig01_mechanism_map.pgf"
    orig = "\\documentclass{article}\n\\usepackage{graphicx}\n"
    orig += "\\begin{document}\nText\n\\end{document}\n"
    patched = _add_pgf_graphicspath(orig, pgf)
    expected = pgf.parent.resolve().as_posix() + "/"
    assert r"\graphicspath{{" + expected + "}}" in patched
    assert patched.index(r"\graphicspath") < patched.index(r"\begin{document}")
    assert patched.endswith("Text\n\\end{document}\n")
    assert orig not in (patched,)


def test_pgf_sidecar_context_restores_compiler_and_cleans_temporary_tex(
    tmp_path, monkeypatch,
):
    # Fake only the external library: the exact original compiler remains
    # in control, the patch changes only the staged LaTeX graphicspath.
    pkg = types.ModuleType("awesomefigures")
    auto = types.ModuleType("awesomefigures.auto_publication")
    pkg.auto_publication = auto
    monkeypatch.setitem(sys.modules, "awesomefigures", pkg)
    monkeypatch.setitem(sys.modules, "awesomefigures.auto_publication", auto)
    stage = tmp_path / "stage"
    stage.mkdir()
    art = tmp_path / "artwork"
    art.mkdir()
    manuscript = stage / "main.tex"
    text = "\\documentclass{article}\n\\usepackage{graphicx}\n"
    text += "\\begin{document}\nBody\n\\end{document}\n"
    manuscript.write_text(text, encoding="utf-8")
    pgf = art / "fig01_mechanism_map.pgf"
    pgf.write_text("content", encoding="utf-8")
    result = art / "figure.pdf"
    calls = []

    def compiler(p, pdf, temp_source, engine, timeout):
        alternate = Path(temp_source)
        assert alternate.exists()
        assert alternate.parent == stage
        assert r"\graphicspath{{" in alternate.read_text()
        assert art.resolve().as_posix() + "/" in alternate.read_text()
        assert manuscript.read_text() == text
        calls.append(engine)
        pdf.write_bytes(b"%PDF-1.4\n")
    auto._compile_exact_pdf = compiler
    with jfm_pgf_sidecar_support():
        auto._compile_exact_pdf(pgf, result, manuscript, "xelatex", 90)
    assert calls == ["xelatex"]
    assert auto._compile_exact_pdf is compiler
    assert not list(stage.glob("_jfm_figures_*.tex"))
    assert result.exists()


def test_controlled_results_explicitly_label_provisional_coverage():
    root = Path(__file__).resolve().parents[1]
    method = (root / "paper/manuscript/sections_short/02_posterior_pricing.tex").read_text()
    results = (root / "paper/manuscript/sections_short/04_results.tex").read_text()
    robustness = (root / "paper/manuscript/sections_short/05_robustness.tex").read_text()
    assert "160 independent return histories" in method
    assert "1,440 option-scenario" in method
    assert "tab:short_controlled_stress" in results
    assert "0.318736" in results
    assert "96.3" in results
    assert "numerically provisional" in results
    assert "0.002281" in robustness
    assert r"\citep{cmeclearing2020curran}" in robustness
