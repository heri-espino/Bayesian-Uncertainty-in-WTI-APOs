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
    def relative_luminance(hex_color: str) -> float:
        value = hex_color.lstrip("#")
        assert len(value) == 6
        rgb = [int(value[i : i + 2], 16) / 255.0 for i in (0, 2, 4)]
        linear = [
            channel / 12.92
            if channel <= 0.04045
            else ((channel + 0.055) / 1.055) ** 2.4
            for channel in rgb
        ]
        return 0.2126 * linear[0] + 0.7152 * linear[1] + 0.0722 * linear[2]

    # The high-contrast categorical palette must retain visibly separated
    # lightness levels after grayscale conversion.
    high_luminances = sorted(
        relative_luminance(color)
        for color in figures.TOL_HIGH_CONTRAST.values()
    )
    assert min(
        right - left
        for left, right in zip(high_luminances, high_luminances[1:], strict=True)
    ) > 0.10

    # Continuous maps use a perceptually uniform, color-vision-friendly map.
    assert figures.HEATMAP_CMAP == "cividis"

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

    # At least one categorical palette entry must genuinely use color.
    assert any(
        len({color[1:3], color[3:5], color[5:7]}) > 1
        for color in figures.TOL_HIGH_CONTRAST.values()
    )
