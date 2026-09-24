from __future__ import annotations

import pandas as pd

from experiments.wti_external_q_cluster_bootstrap import (
    _common_support_wide,
    run_bootstrap,
)


def test_common_support_wide_intersects_all_methods() -> None:
    keys = [
        ("2026-09-01", "2026-10", "a"),
        ("2026-09-01", "2026-10", "b"),
        ("2026-09-02", "2026-10", "c"),
    ]
    ext_rows = []
    for method in (
        "vanilla_surface_previous_day",
        "vanilla_surface_expanding",
    ):
        for i, (date, expiry, contract) in enumerate(keys):
            ext_rows.append(
                {
                    "method": method,
                    "valuation_date": date,
                    "apo_expiry": expiry,
                    "contract_id": contract,
                    "forward_error": 0.1 + i,
                    "baseline_pi_error": 0.3 + i,
                    "surface_components_clipped": (
                        1 if contract == "c" else 0
                    ),
                }
            )
    external = pd.DataFrame(ext_rows)

    apo_rows = []
    for method in ("previous_day_smile", "expanding_smile"):
        for i, (date, expiry, contract) in enumerate(keys):
            apo_rows.append(
                {
                    "method": method,
                    "valuation_date": date,
                    "apo_expiry": expiry,
                    "contract_id": contract,
                    "forward_error": 0.05 + i,
                }
            )
    apo = pd.DataFrame(apo_rows)

    wide = _common_support_wide(
        external, apo, apo_expiry="2026-10"
    )

    assert len(wide) == 2
    assert set(wide["contract_id"]) == {"a", "b"}
    assert {
        "external_previous_error",
        "external_expanding_error",
        "apo_previous_error",
        "apo_expanding_error",
        "baseline_pi_error",
    }.issubset(wide.columns)


def test_run_bootstrap_returns_paired_comparisons() -> None:
    wide = pd.DataFrame(
        {
            "valuation_date": [
                "2026-09-01",
                "2026-09-01",
                "2026-09-02",
                "2026-09-02",
            ],
            "apo_expiry": ["2026-10"] * 4,
            "contract_id": ["a", "b", "c", "d"],
            "external_previous_error": [0.1, 0.2, 0.1, 0.2],
            "external_expanding_error": [0.1, 0.2, 0.1, 0.2],
            "apo_previous_error": [0.15, 0.25, 0.15, 0.25],
            "apo_expanding_error": [0.15, 0.25, 0.15, 0.25],
            "baseline_pi_error": [0.5, 0.6, 0.5, 0.6],
        }
    )

    out = run_bootstrap(
        wide, iterations=2_000, seed=123
    )

    assert len(out) == 6
    assert (
        out.loc[
            out["comparison"].eq(
                "external_previous_vs_historical_pi"
            ),
            "delta_mae",
        ].iloc[0]
        < 0
    )
    assert (
        out.loc[
            out["comparison"].eq(
                "external_previous_vs_apo_previous"
            ),
            "delta_mae",
        ].iloc[0]
        < 0
    )
