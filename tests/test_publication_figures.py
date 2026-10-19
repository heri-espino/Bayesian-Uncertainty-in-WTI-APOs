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
        "#9b6500",
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
        "pseudo_mc": "#9b6500",
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

def test_remef_word_plot_geometry_and_contrast() -> None:
    assert abs(figures.WORD_TEXT_WIDTH_IN - 6.1375) < 1e-10
    assert all(abs(figures._word_figsize(i)[0] - 6.1375) < 1e-10
               for i in (1, 2, 3, 4))
    assert figures.MECHANISM_CMAP.name == "cividis_ink"
    assert max(figures.MECHANISM_CMAP(0.0)[:3]) < 0.6



def test_figure_three_title_stays_inside_canvas():
    import inspect
    source = inspect.getsource(figures.build_figure_3)
    assert "y=1.02" not in source
    assert "y=0.98" in source


def test_final_default_exports_are_vector_formats():
    import inspect
    source = inspect.getsource(figures.parse_args)
    assert 'default=("pdf", "svg")' in source


def test_times_font_svg_and_numeric_axes(tmp_path: Path):
    import matplotlib as mpl
    import matplotlib.pyplot as plt
    import numpy as np
    from xml.etree import ElementTree as ET

    figures._configure_matplotlib(force_no_tex=True)
    assert mpl.rcParams["svg.fonttype"] == "none"
    assert mpl.rcParams["pdf.fonttype"] == 42
    assert mpl.rcParams["figure.titlesize"] == figures.PUBLICATION_FONT_PT["suptitle"]
    assert mpl.rcParams["axes.labelsize"] == figures.PUBLICATION_FONT_PT["axis_label"]
    assert mpl.rcParams["xtick.labelsize"] == figures.PUBLICATION_FONT_PT["tick"]

    fig, ax = plt.subplots()
    ax.plot([-2.31, 1.76], [0.013, 0.237], marker="o")
    initial_x, initial_y = ax.get_xlim(), ax.get_ylim()
    figures._align_numeric_axes(fig)
    final_x, final_y = ax.get_xlim(), ax.get_ylim()
    assert final_x[0] <= initial_x[0] and final_x[1] >= initial_x[1]
    assert final_y[0] <= initial_y[0] and final_y[1] >= initial_y[1]
    assert 3 <= len(ax.get_xticks()) <= 6
    assert 3 <= len(ax.get_yticks()) <= 6
    assert np.allclose(final_x, [ax.get_xticks()[0], ax.get_xticks()[-1]])
    assert np.allclose(final_y, [ax.get_yticks()[0], ax.get_yticks()[-1]])
    fig.suptitle("Test")
    vector = tmp_path / "test.svg"
    fig.savefig(vector)
    plt.close(fig)
    assert any(e.tag.endswith("text") for e in ET.parse(vector).getroot().iter())


def test_date_and_categorical_axes_are_not_snapped():
    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt
    figures._configure_matplotlib(force_no_tex=True)
    fig, (time_ax, category_ax) = plt.subplots(1, 2)
    dates = pd.date_range("2026-08-25", periods=12)
    time_ax.plot(dates, np.arange(12))
    time_ax.set_xlim(dates[0], dates[-1])
    category_ax.plot([-6, 0], [0, 6])
    category_ax.set_yticks(range(7), [str(k) for k in range(7)])
    category_ax.invert_yaxis()
    x0, y0 = time_ax.get_xlim(), category_ax.get_ylim()
    figures._align_numeric_axes(fig, date_axes=(time_ax,), categorical_y_axes=(category_ax,))
    assert time_ax.get_xlim() == x0
    assert category_ax.get_ylim() == y0
    plt.close(fig)


def test_missing_times_new_roman_fails_publication(monkeypatch):
    from matplotlib import font_manager
    import pytest

    def missing(*args, **kwargs):
        if kwargs.get("fallback_to_default") is False:
            raise ValueError("not installed")
        return "fallback.ttf"

    monkeypatch.setattr(font_manager, "findfont", missing)
    with pytest.raises(SystemExit, match="Times New Roman"):
        figures._configure_matplotlib(require_times_new_roman=True)
    with pytest.warns(RuntimeWarning, match="Preview only"):
        assert figures._configure_matplotlib() == "preview-font-fallback"
