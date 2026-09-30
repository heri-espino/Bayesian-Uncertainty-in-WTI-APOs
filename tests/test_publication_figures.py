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



def test_publication_styles_are_colorful_and_grayscale_safe() -> None:
    assert figures.FIG1_DISCRETE == [
        "#97001c",
        "#0083f9",
        "#00b49c",
        "#ffc600",
        "#f198ff",
    ]
    assert figures.HEATMAP_CMAP.name == "tol_iridescent"
    assert figures.IRIDESCENT_HEX[0] == "#FEFBE9"
    assert figures.IRIDESCENT_HEX[-1] == "#46353A"
    assert figures.BAD_DATA_COLOR == "#999999"

    assert figures.FIG2_COLORS == {
        "calls": "#0083f9",
        "puts": "#97001c",
        "historical": "#00b49c",
        "apo_common": "#f198ff",
    }
    assert figures.FIG3_COLORS["expanding"] == "#a5d3ff"
    assert figures.FIG3_COLORS["previous_day"] == "#97001c"
    assert figures.FIG4_COLORS == {
        "pseudo_mc": "#ffc600",
        "curran": "#0083f9",
        "sobol": "#97001c",
    }

    # Color is never the only categorical cue.
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
