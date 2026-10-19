"""Cheap regression checks for the optional 10-million-history mode.

These tests intentionally use a tiny synthetic cell. A full 10m experiment
must run manually on the research workstation, never in automatic CI.
"""
from __future__ import annotations

from dataclasses import replace

import numpy as np
import pandas as pd
import pytest

from experiments.massive_mechanism_map import (
    TenMillionConfig, _scenario_table, _summarize_cell_chunked,
)


def test_ten_million_allocation_and_seed() -> None:
    cfg = TenMillionConfig()
    cells = len(cfg.sample_sizes) * len(cfg.sigma_true_values)
    q, r = divmod(cfg.target_histories, cells)
    counts = [q + int(i < r) for i in range(cells)]
    assert cfg.root_seed == 2468
    assert cells == 35
    assert (q, r) == (285714, 10)
    assert sum(counts) == 10_000_000
    assert max(counts) - min(counts) == 1


def test_chunked_small_cell_is_deterministic_and_cleans_temp(tmp_path) -> None:
    cfg = replace(
        TenMillionConfig(),
        sample_sizes=(21,), sigma_true_values=(0.20,),
        moneyness_values=(1.0,), maturity_days=(21,),
        fraction_fixed_values=(0.0,), sigma_grid_points=65,
        batch_size=4, target_histories=11,
    )
    grid = np.linspace(cfg.sigma_grid_min, cfg.sigma_grid_max, cfg.sigma_grid_points)
    scenarios = _scenario_table(cfg)
    prices = np.square(np.maximum(grid[:, None] - 0.1, 0.0))
    def calculate():
        return _summarize_cell_chunked(
            cfg=cfg, n_obs=21, sigma_true=0.2, replications=11,
            sigma_grid=grid, price_curves=prices, scenarios=scenarios,
            xp=np, resolved="numpy", checkpoint_dir=tmp_path,
        )
    first, cell = calculate()
    second, again = calculate()
    pd.testing.assert_frame_equal(first, second)
    assert cell == again
    assert len(first) == 1
    assert cell["replications"] == 11
    assert np.isfinite(first["mean_pi_minus_pm"]).all()
    assert (first["taylor_mae"] >= 0).all()
    assert (first["taylor_rmse"] >= 0).all()
    assert not list(tmp_path.glob("temporary_abs_gaps*"))
