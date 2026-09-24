"""Paired valuation-date bootstrap for independent vanilla-Q validation.

The bootstrap operates on the exact no-clipping common-support contract-date
sample shared by:
- external LO surface previous-day;
- external LO surface expanding;
- prior-date APO smile previous-day;
- prior-date APO smile expanding.

Valuation dates, not individual contracts, are resampled because contracts on
one date share the same futures curve and volatility state.
"""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

import pandas as pd

from experiments.wti_liquidity_bootstrap import _cluster_bootstrap

DEFAULT_EXTERNAL = Path(
    "results/analysis/wti_external_vanilla_q_validation/"
    "external_vanilla_q_predictions.csv"
)
DEFAULT_APO = Path(
    "results/analysis/wti_forward_q_validation/"
    "forward_q_predictions.csv"
)
DEFAULT_OUTPUT = Path(
    "results/analysis/wti_external_vanilla_q_validation/"
    "surface_common_support_cluster_bootstrap.csv"
)

KEYS = ["valuation_date", "apo_expiry", "contract_id"]


def _common_support_wide(
    external: pd.DataFrame,
    apo: pd.DataFrame,
    *,
    apo_expiry: str,
) -> pd.DataFrame:
    """Return exact common-support observations in one wide error table."""
    external = external[
        external["apo_expiry"].astype(str).eq(apo_expiry)
    ].copy()
    apo = apo[
        apo["apo_expiry"].astype(str).eq(apo_expiry)
    ].copy()

    ext_methods = {
        "vanilla_surface_previous_day": "external_previous_error",
        "vanilla_surface_expanding": "external_expanding_error",
    }
    apo_methods = {
        "previous_day_smile": "apo_previous_error",
        "expanding_smile": "apo_expanding_error",
    }

    key_sets: list[set[tuple[str, str, str]]] = []
    external_parts: list[pd.DataFrame] = []
    for method, error_name in ext_methods.items():
        group = external[
            external["method"].eq(method)
            & external["surface_components_clipped"].fillna(1).eq(0)
        ].copy()
        if group.duplicated(KEYS).any():
            raise RuntimeError(f"duplicate keys for {method}")
        key_sets.append(
            set(map(tuple, group[KEYS].astype(str).to_numpy()))
        )
        cols = KEYS + ["forward_error"]
        if method == "vanilla_surface_previous_day":
            cols += ["baseline_pi_error"]
        part = group[cols].rename(
            columns={"forward_error": error_name}
        )
        external_parts.append(part)

    apo_parts: list[pd.DataFrame] = []
    for method, error_name in apo_methods.items():
        group = apo[apo["method"].eq(method)].copy()
        if group.duplicated(KEYS).any():
            raise RuntimeError(f"duplicate keys for {method}")
        key_sets.append(
            set(map(tuple, group[KEYS].astype(str).to_numpy()))
        )
        apo_parts.append(
            group[KEYS + ["forward_error"]].rename(
                columns={"forward_error": error_name}
            )
        )

    if any(not keys for keys in key_sets):
        raise RuntimeError("one or more required methods have no observations")
    common = set.intersection(*key_sets)
    if not common:
        raise RuntimeError("no exact common-support contract-dates")

    wanted = pd.MultiIndex.from_tuples(
        sorted(common), names=KEYS
    )

    def restrict(frame: pd.DataFrame) -> pd.DataFrame:
        key = pd.MultiIndex.from_frame(frame[KEYS].astype(str))
        return frame.loc[key.isin(wanted)].copy()

    wide = restrict(external_parts[0])
    for frame in external_parts[1:] + apo_parts:
        wide = wide.merge(
            restrict(frame),
            on=KEYS,
            how="inner",
            validate="one_to_one",
        )

    if len(wide) != len(common):
        raise RuntimeError(
            "wide common-support table lost contract-date observations"
        )
    return wide.sort_values(KEYS).reset_index(drop=True)


def run_bootstrap(
    wide: pd.DataFrame,
    *,
    iterations: int,
    seed: int,
) -> pd.DataFrame:
    """Run paired date-cluster comparisons on the same observations."""
    comparisons = [
        (
            "external_previous_vs_historical_pi",
            "external_previous_error",
            "baseline_pi_error",
        ),
        (
            "external_expanding_vs_historical_pi",
            "external_expanding_error",
            "baseline_pi_error",
        ),
        (
            "apo_previous_vs_historical_pi",
            "apo_previous_error",
            "baseline_pi_error",
        ),
        (
            "apo_expanding_vs_historical_pi",
            "apo_expanding_error",
            "baseline_pi_error",
        ),
        (
            "external_previous_vs_apo_previous",
            "external_previous_error",
            "apo_previous_error",
        ),
        (
            "external_expanding_vs_apo_expanding",
            "external_expanding_error",
            "apo_expanding_error",
        ),
    ]

    rows: list[dict[str, Any]] = []
    for i, (label, model_error, baseline_error) in enumerate(
        comparisons
    ):
        stats = _cluster_bootstrap(
            wide,
            model_error=model_error,
            baseline_error=baseline_error,
            iterations=iterations,
            seed=seed + i,
        )
        rows.append(
            {
                "comparison": label,
                "interpretation": (
                    "negative delta favors first-named model"
                ),
                "bootstrap_iterations": iterations,
                **stats,
            }
        )
    return pd.DataFrame(rows)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--external", type=Path, default=DEFAULT_EXTERNAL
    )
    parser.add_argument("--apo", type=Path, default=DEFAULT_APO)
    parser.add_argument(
        "--apo-expiry", default="2026-10"
    )
    parser.add_argument(
        "--iterations", type=int, default=100_000
    )
    parser.add_argument("--seed", type=int, default=20260923)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.iterations < 1_000:
        raise ValueError("--iterations must be at least 1000")

    external = pd.read_csv(args.external)
    apo = pd.read_csv(args.apo)
    wide = _common_support_wide(
        external, apo, apo_expiry=args.apo_expiry
    )
    result = run_bootstrap(
        wide,
        iterations=int(args.iterations),
        seed=int(args.seed),
    )

    args.output.parent.mkdir(parents=True, exist_ok=True)
    result.to_csv(args.output, index=False)
    wide.to_csv(
        args.output.parent / "surface_common_support_paired_errors.csv",
        index=False,
    )
    print(result.to_csv(index=False), end="")


if __name__ == "__main__":
    main()
