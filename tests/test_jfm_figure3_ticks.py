"""Regression tests: Figure 3 CI limits must never crop forest-plot error bars."""
from pathlib import Path

import matplotlib
matplotlib.use("Agg", force=True)
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pytest

from scripts import build_publication_figures as figures


class IncompleteLocator:
    """Simulate a backend returning attractive but non-enclosing ticks."""

    def __init__(self, **kwargs):
        pass

    def tick_values(self, lower, upper):
        return np.array([-2.0, -1.0, 0.0])


@pytest.mark.parametrize("axis,inverted", [
    ("x", False), ("x", True), ("y", False), ("y", True),
])
def test_nice_ticks_preserve_original_limits_when_locator_is_incomplete(
    monkeypatch, axis, inverted,
):
    monkeypatch.setattr(figures, "MaxNLocator", IncompleteLocator)
    fig, ax = plt.subplots()
    try:
        lo, hi = -2.75, 0.75
        if axis == "x":
            ax.set_xlim(hi, lo) if inverted else ax.set_xlim(lo, hi)
        else:
            ax.set_ylim(hi, lo) if inverted else ax.set_ylim(lo, hi)

        figures._snap_numeric_axis_to_ticks(ax, axis)
        actual = ax.get_xlim() if axis == "x" else ax.get_ylim()
        ticks = ax.get_xticks() if axis == "x" else ax.get_yticks()
        assert actual[0] > actual[1] if inverted else actual[0] < actual[1]
        assert min(actual) <= lo
        assert max(actual) >= hi
        assert ticks[0] <= lo
        assert ticks[-1] >= hi
        assert np.all(np.diff(ticks) > 0)
        assert len(ticks) > 3  # Extended the initially incomplete locator.
    finally:
        plt.close(fig)


def test_figure3_actual_committed_cluster_bootstrap_extrema_not_clipped():
    """The published CI dataset triggers the full Figure 3 axis setup."""
    source = (
        Path(__file__).resolve().parents[1]
        / "results/analysis/wti_extended_forward/liquidity_bootstrap/"
        / "liquidity_cluster_bootstrap_monster.csv"
    )
    table = pd.read_csv(source)
    fig, axes = plt.subplots(1, 2, sharey=True)
    try:
        figures._forest_panel(axes[0], table, metric="mae")
        figures._forest_panel(axes[1], table, metric="rmse")
        original = [ax.get_xlim() for ax in axes]
        figures._align_numeric_axes(fig, categorical_y_axes=tuple(axes))
        for before, ax in zip(original, axes):
            after = ax.get_xlim()
            assert min(after) <= min(before)
            assert max(after) >= max(before)
            assert len(ax.get_xticks()) >= 2
    finally:
        plt.close(fig)
