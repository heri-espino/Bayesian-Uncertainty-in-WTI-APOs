"""Regression checks for JFM-only manuscript edits and figure isolation."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_jfm_concise_source_current_and_remains_distinct_from_remef():
    main = (ROOT / "paper/manuscript/main_short.tex").read_text(encoding="utf-8")
    build = (ROOT / "paper/build.py").read_text(encoding="utf-8")
    # WileyNJDv5 needs two name tokens; one causes \filtername to fail at \maketitle.
    assert r"\author[1]{Anonymous Author}" in main
    assert "Heriberto" not in main and "heri-espino" not in main
    identifying = (ROOT / "paper/manuscript/jfm_title_page.tex").read_text(encoding="utf-8")
    assert "Heriberto Espino-Montelongo" in identifying
    assert "heriberto.espinomo@udlap.mx" in identifying
    assert "10 million synthetic return histories" in main
    assert "only 15 valuation dates" in main
    assert r"\citet{cumminsesposito2025}" in (
        ROOT / "paper/manuscript/sections_short/01_introduction.tex"
    ).read_text(encoding="utf-8")
    assert 'MAIN_TEX = SOURCE_DIR / "main_short.tex"' in build
    assert "shutil.copy2(MAIN_TEX, STAGE_DIR / \"main.tex\")" in build
    assert "shutil.copytree(SOURCE_DIR / \"sections_short\"" in build
    assert "shutil.copytree(SOURCE_DIR, STAGE_DIR" not in build
    assert '    build_publication_figures()\n    prepare_stage()' not in build


def test_jfm_figure_target_is_separate_and_default_remef_retained():
    src = (ROOT / "scripts/build_publication_figures.py").read_text(encoding="utf-8")
    assert 'CURRENT_JOURNAL = "remef"' in src
    assert 'choices=("remef", "jfm")' in src
    assert 'Path("figures/jfm")' in src
    assert "Date-ordered conditional pricing comparisons across expiries" in src
    assert '"REMEF Word, Times New Roman"' in src
    assert 'JFM_FIGURES_DIR = ROOT / "figures" / "jfm"' in (
        ROOT / "paper/build.py"
    ).read_text(encoding="utf-8")


def test_jfm_review_sections_do_not_disclose_identity():
    sections = ROOT / "paper/manuscript/sections_short"
    joined = "\n".join(p.read_text(encoding="utf-8") for p in sections.glob("*.tex"))
    for identifier in ("Heriberto", "Espino-Montelongo", "@udlap.mx", "heri-espino.github.io"):
        assert identifier not in joined
