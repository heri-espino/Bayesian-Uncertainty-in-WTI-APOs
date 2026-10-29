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
    assert figures.FIG3_COLORS["previous_day_edge"] == "#5c0010"
    assert figures.FIG4_COLORS == {
        "pseudo_mc": "#9b6500",
        "curran": "#0083f9",
        "sobol": "#97001c",
    }
    assert figures.FIG4_EDGE_COLORS == {
        "pseudo_mc": "#5f3d00",
        "curran": "#005aa8",
        "sobol": "#5c0010",
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
    shared_title = inspect.getsource(figures._apply_suptitle)
    assert "_apply_suptitle" in source
    assert "y=1.02" not in source
    assert "y=0.985" in shared_title
    assert 'PUBLICATION_FONT_PT["suptitle"]' in shared_title


def test_final_default_exports_include_png_pdf_and_svg():
    import inspect
    source = inspect.getsource(figures.parse_args)
    assert 'default=("png", "pdf", "svg")' in source


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



def test_panel_title_keeps_bold_letter_inline() -> None:
    import matplotlib.pyplot as plt

    figures._configure_matplotlib(force_no_tex=True)
    fig, ax = plt.subplots()
    figures._panel_title(ax, "A", "MAE difference by expiry")
    assert ax.get_title(loc="left") == (
        r"$\mathbf{(A)}$  MAE difference by expiry"
    )
    assert ax.get_title(loc="center") == ""
    assert not any(t.get_text() == "A" for t in ax.texts)
    plt.close(fig)


def test_categorical_endpoint_ticks_meet_spines_without_cropping() -> None:
    import numpy as np
    import matplotlib.pyplot as plt

    figures._configure_matplotlib(force_no_tex=True)
    fig, (a, b) = plt.subplots(1, 2)
    labels = ["first", "second", "third"]
    for ax in (a, b):
        positions = np.arange(1, 4, dtype=float)
        ax.errorbar(positions, positions, yerr=0.15, xerr=0.19, fmt="s")
    figures._category_ticks_with_endpoints(a, "x", labels)
    figures._category_ticks_with_endpoints(b, "y", labels)
    xlim, ylim = a.get_xlim(), b.get_ylim()
    figures._align_numeric_axes(
        fig,
        categorical_x_axes=(a,),
        categorical_y_axes=(b,),
    )
    assert a.get_xlim() == xlim == (0.0, 4.0)
    assert b.get_ylim() == ylim == (4.0, 0.0)
    assert a.get_xticks()[0] == a.get_xlim()[0]
    assert a.get_xticks()[-1] == a.get_xlim()[-1]
    assert b.get_yticks()[0] == min(b.get_ylim())
    assert b.get_yticks()[-1] == max(b.get_ylim())
    assert len(a.get_xticklabels()) == 5
    assert a.get_xticklabels()[0].get_text() == ""
    assert a.get_xticklabels()[-1].get_text() == ""
    plt.close(fig)


def test_figure3_previous_day_squares_use_dark_red_edges() -> None:
    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt

    rows = []
    for expiry in (
        "2026-09", "2026-10", "2026-11", "2027-03",
        "2027-09", "2028-03", "2028-09",
    ):
        for method in ("forward_q_expanding_smile", "forward_q_previous_day_smile"):
            rows.append({
                "scope": "expiry", "sample": "all", "apo_expiry": expiry,
                "experiment": method, "n": 10,
                "delta_mae": -0.2, "delta_mae_ci025": -0.3,
                "delta_mae_ci975": -0.1,
            })
    fig, ax = plt.subplots()
    figures._forest_panel(ax, pd.DataFrame(rows), metric="mae")
    assert len(ax.containers) == 2
    circle = ax.containers[0].lines[0]
    square = ax.containers[1].lines[0]
    assert circle.get_marker() == "o"
    assert square.get_marker() == "s"
    assert square.get_markeredgecolor().lower() == "#5c0010"
    assert square.get_markerfacecolor().lower() == "#97001c"
    plt.close(fig)


def test_all_three_formats_and_blue_short_maturity_circles(tmp_path: Path, monkeypatch) -> None:
    import matplotlib.pyplot as plt
    from matplotlib.collections import PathCollection

    figures._configure_matplotlib(force_no_tex=True)
    run = figures._discover_monster_mechanism_run(None)
    captured = {}
    real_save = figures._save

    def recording_save(fig, stem, formats):
        captured["fig"] = fig
        return real_save(fig, stem, formats)

    monkeypatch.setattr(figures, "_save", recording_save)
    outputs, _ = figures.build_figure_1(
        run, tmp_path, ("png", "pdf", "svg"),
    )
    assert len(outputs) == 3
    for path in outputs:
        from pathlib import Path as P
        assert P(path).is_file()
    assert len(captured["fig"].axes) >= 4
    ax_c = captured["fig"].axes[2]
    assert any(
        isinstance(c, PathCollection)
        and len(c.get_offsets()) >= 2
        and c.get_zorder() >= 8
        for c in ax_c.collections
    )
    for ax in captured["fig"].axes[:4]:
        assert r"\mathbf{(" in ax.get_title(loc="left")
    plt.close(captured["fig"])



def test_figure1_panel_c_zoom_is_inset_and_preserves_main_domain(tmp_path: Path) -> None:
    import matplotlib.pyplot as plt
    import numpy as np
    import pandas as pd
    from xml.etree import ElementTree as ET

    figures._configure_matplotlib(force_no_tex=True)
    curve = pd.DataFrame({
        "maturity_days": [21, 21, 21, 63, 63, 63, 126, 126, 126],
        "fraction_fixed": [0.0, 0.75, 0.90] * 3,
        "mean_abs_pi_minus_pm": [
            0.016, 0.002, 0.0002,
            0.08, 0.020, 0.001,
            0.12, 0.019, 0.002,
        ],
    })
    fig, ax = plt.subplots()
    ax.plot(curve["fraction_fixed"][:3], curve["mean_abs_pi_minus_pm"][:3])
    old = (ax.get_xlim(), ax.get_ylim())
    inset = figures._add_partial_fixing_zoom(ax, curve)
    assert inset in ax.child_axes
    assert tuple(round(v, 3) for v in inset.get_xlim()) == (0.75, 1.0)
    assert tuple(round(v, 3) for v in inset.get_ylim()) == (-0.001, 0.023)
    assert len(inset.lines) == 3
    assert inset.lines[0].get_marker() == "o"
    assert inset.lines[0].get_markerfacecolor() == "white"
    assert np.allclose(inset.get_xticks(), [0.75, 0.875, 1.0])
    assert len(inset.get_yticks()) == 3
    assert np.allclose(ax.get_xlim(), old[0])
    assert np.allclose(ax.get_ylim(), old[1])

    svg = tmp_path / "partial_fixing_zoom.svg"
    fig.savefig(svg)
    assert "Near-zero detail" in svg.read_text(encoding="utf-8")
    ET.parse(svg)
    plt.close(fig)


def test_figure4_marker_borders_have_distinct_dark_outline_colors(
    tmp_path: Path, monkeypatch,
) -> None:
    import matplotlib.pyplot as plt

    figures._configure_matplotlib(force_no_tex=True)
    captured = {}
    def save_figure(fig, stem, formats):
        captured["fig"] = fig
        return []  # Inspect actual artists before any save/close.
    monkeypatch.setattr(figures, "_save", save_figure)
    figures.build_figure_4(tmp_path, ("svg",))
    top, bottom = captured["fig"].axes[:2]
    for ax, expected in (
        (top, ("pseudo_mc", "curran", "sobol")),
        (bottom, ("pseudo_mc", "sobol")),
    ):
        artists = [
            container.lines[0]
            for container in ax.containers
            if hasattr(container, "lines") and container.lines[0] is not None
        ]
        assert len(artists) == len(expected)
        for artist, key in zip(artists, expected, strict=True):
            assert artist.get_markeredgecolor().lower() == figures.FIG4_EDGE_COLORS[key]
            assert artist.get_markeredgewidth() >= 0.95
            assert artist.get_markerfacecolor().lower() in (
                figures.FIG4_COLORS[key], "white",
            )
    plt.close(captured["fig"])



def test_requested_figure1_ranges_full_heatmap_and_identity_line(
    tmp_path: Path, monkeypatch,
) -> None:
    import numpy as np
    import matplotlib.pyplot as plt

    figures._configure_matplotlib(force_no_tex=True)
    figure = {}
    def retain(fig, stem, formats):
        figure["fig"] = fig
        return []
    monkeypatch.setattr(figures, "_save", retain)
    run = figures._discover_monster_mechanism_run(None)
    figures.build_figure_1(run, tmp_path, ("svg",))
    a, b, c, d = figure["fig"].axes[:4]
    assert np.allclose(a.get_ylim(), [0.0, 0.15])
    assert np.allclose(c.get_ylim(), [0.0, 0.15])
    assert np.allclose(c.get_xlim(), [0.0, 1.0])
    assert np.allclose(c.get_xticks(), [0.0, 0.25, 0.5, 0.75, 1.0])

    heat = b.images[0].get_array()
    assert len(b.get_xticks()) == heat.shape[1]
    assert len(b.get_yticks()) == heat.shape[0]
    assert np.allclose(b.get_xlim(), [-0.5, heat.shape[1] - 0.5])
    assert np.allclose(b.get_ylim(), [-0.5, heat.shape[0] - 0.5])

    # Axline is unbounded in data space and draws the y=x reference through
    # the entire visible shared data range, unlike the old data-range segment.
    assert len(d.lines) == 1
    assert type(d.lines[0]).__name__ in {"AxLine", "_AxLine"}
    assert np.allclose(d.get_xlim(), d.get_ylim())
    assert np.isclose(d.get_xlim()[0], d.get_xticks()[0])
    assert np.isclose(d.get_xlim()[1], d.get_xticks()[-1])
    assert np.isclose(d.get_ylim()[0], d.get_yticks()[0])
    assert np.isclose(d.get_ylim()[1], d.get_yticks()[-1])
    plt.close(figure["fig"])


def test_requested_figure2_explicit_a_and_c_ylims(tmp_path: Path, monkeypatch) -> None:
    import matplotlib.pyplot as plt
    import numpy as np

    figures._configure_matplotlib(force_no_tex=True)
    figure = {}
    def retain(fig, stem, formats):
        figure["fig"] = fig
        return []
    monkeypatch.setattr(figures, "_save", retain)
    figures.build_figure_2(tmp_path, ("svg",))
    axes = figure["fig"].axes
    assert np.allclose(axes[0].get_ylim(), [0.4, 0.6])
    assert np.allclose(axes[2].get_ylim(), [0.3, 0.8])
    assert np.allclose(axes[2].get_xlim(), [-0.5, 0.75])
    assert np.allclose(
        axes[2].get_xticks(), [-0.5, -0.25, 0.0, 0.25, 0.5, 0.75]
    )
    plt.close(figure["fig"])


def test_requested_figure4_square_dashboard_and_taller_panel_b(
    tmp_path: Path, monkeypatch,
) -> None:
    import matplotlib.pyplot as plt
    import numpy as np

    figures._configure_matplotlib(force_no_tex=True)
    figure = {}
    def retain(fig, stem, formats):
        figure["fig"] = fig
        return []
    monkeypatch.setattr(figures, "_save", retain)
    figures.build_figure_4(tmp_path, ("svg",))
    fig = figure["fig"]
    a, b = fig.axes[:2]
    width, height = fig.get_size_inches()
    assert np.isclose(width, height)
    assert np.isclose(width, figures.WORD_TEXT_WIDTH_IN)
    assert list(a.get_gridspec().get_height_ratios()) == [0.78, 1.22]
    assert np.allclose(b.get_ylim(), [-15.0, 15.0])
    assert np.allclose(
        b.get_yticks(), [-15.0, -10.0, -5.0, 0.0, 5.0, 10.0, 15.0]
    )
    assert a.get_position().height < b.get_position().height
    assert np.isclose(
        a.get_position().height / b.get_position().height,
        0.78 / 1.22,
        rtol=1e-6,
    )
    plt.close(fig)
