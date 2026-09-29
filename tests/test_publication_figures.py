from __future__ import annotations

from pathlib import Path

from scripts import build_publication_figures as figures


def test_publication_figures_build_from_committed_results(tmp_path: Path) -> None:
    figures._configure_matplotlib(force_no_tex=True)
    mechanism_run = figures._discover_monster_mechanism_run(None)

    outputs_1, meta_1 = figures.build_figure_1(mechanism_run, tmp_path, ("png",))
    outputs_2, meta_2 = figures.build_figure_2(tmp_path, ("png",))
    outputs_3, meta_3 = figures.build_figure_3(tmp_path, ("png",))
    outputs_4, meta_4 = figures.build_figure_4(tmp_path, ("png",))

    assert -1.0 <= meta_1["taylor_cell_correlation"] <= 1.0
    assert len(meta_2["smile_dates"]) == 2
    assert meta_3["bootstrap_iterations"] == 100000
    assert meta_4["matched_targets"] >= 8

    for output in outputs_1 + outputs_2 + outputs_3 + outputs_4:
        path = figures.ROOT / output
        assert path.exists()
        assert path.stat().st_size > 0



def test_publication_styles_are_grayscale_safe() -> None:
    def is_gray(hex_color: str) -> bool:
        value = hex_color.lstrip("#")
        assert len(value) == 6
        return value[0:2] == value[2:4] == value[4:6]

    assert all(is_gray(color) for color in figures.PALETTE.values())

    sigma_encodings = {
        (
            style["marker"],
            repr(style["linestyle"]),
            bool(style["filled"]),
        )
        for style in figures.SIGMA_STYLES.values()
    }
    maturity_encodings = {
        (
            style["marker"],
            repr(style["linestyle"]),
            bool(style["filled"]),
        )
        for style in figures.MATURITY_STYLES.values()
    }

    assert len(sigma_encodings) == len(figures.SIGMA_STYLES)
    assert len(maturity_encodings) == len(figures.MATURITY_STYLES)
