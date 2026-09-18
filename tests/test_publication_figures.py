from __future__ import annotations

import json
from pathlib import Path

from scripts import build_publication_figures as figures


def test_publication_figures_build_from_committed_results(tmp_path: Path) -> None:
    figures._configure_matplotlib()
    mechanism_run = figures._discover_monster_mechanism_run(None)

    outputs_1, meta_1 = figures.build_figure_1(mechanism_run, tmp_path, ("png",))
    outputs_2, meta_2 = figures.build_figure_2(tmp_path, ("png",))
    outputs_3, meta_3 = figures.build_figure_3(tmp_path, ("png",))
    outputs_4, meta_4 = figures.build_figure_4(tmp_path, ("png",))

    assert meta_1["taylor_cell_correlation"] > 0.99
    assert len(meta_2["smile_dates"]) == 2
    assert meta_3["bootstrap_iterations"] == 100000
    assert meta_4["matched_targets"] >= 8

    for output in outputs_1 + outputs_2 + outputs_3 + outputs_4:
        path = figures.ROOT / output
        assert path.exists()
        assert path.stat().st_size > 0
