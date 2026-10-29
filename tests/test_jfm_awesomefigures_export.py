"""Offline interface tests for JFM's exact-font AwesomeFigures path.

No market data, TeX compilation, or experimental computation required.
"""
from pathlib import Path
from types import SimpleNamespace

import matplotlib
matplotlib.use("Agg", force=True)
import matplotlib.pyplot as plt
import pytest

from scripts import build_publication_figures as figures


class FakePublication:
    def __init__(self):
        self.calls = []
        self.layout = SimpleNamespace(
            fontsize_pt=10.0,
            width_inches=lambda kind: 6.5 if kind == "text" else 3.15,
        )

    def savefig(self, fig, path, *, width, dpi, exact):
        self.calls.append((Path(path).suffix, width, dpi, exact))
        Path(path).write_bytes(b"test-export")


def test_jfm_save_uses_exact_tex_pdf_and_marks_previews(tmp_path, monkeypatch):
    pub = FakePublication()
    monkeypatch.setattr(figures, "CURRENT_JOURNAL", "jfm")
    monkeypatch.setattr(figures, "CURRENT_JFM_PAPER", pub)
    fig, ax = plt.subplots()
    ax.plot([0, 1], [0, 1])
    out = figures._save(fig, tmp_path / "sample", ("pdf", "svg", "png"))
    assert len(out) == 3
    assert pub.calls == [
        (".pdf", "text", 600, True),
        (".svg", "text", 600, False),
        (".png", "text", 600, False),
    ]


def test_jfm_dimensions_derive_from_wiley_layout_not_word(tmp_path, monkeypatch):
    original_fonts = dict(figures.PUBLICATION_FONT_PT)
    original_width = figures.CURRENT_FIGURE_WIDTH_IN
    try:
        figures._apply_jfm_latex_metrics(FakePublication())
        assert figures.CURRENT_FIGURE_WIDTH_IN == pytest.approx(6.5)
        assert figures.PUBLICATION_FONT_PT["axis_label"] == pytest.approx(9.0)
        assert figures.PUBLICATION_FONT_PT["tick"] == pytest.approx(8.0)
        assert figures.PUBLICATION_FONT_PT["suptitle"] == pytest.approx(10.0)
    finally:
        figures.PUBLICATION_FONT_PT.clear()
        figures.PUBLICATION_FONT_PT.update(original_fonts)
        figures.CURRENT_FIGURE_WIDTH_IN = original_width
        plt.rcdefaults()
