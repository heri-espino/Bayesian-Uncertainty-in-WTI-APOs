"""Audit prior-date LO fitted surfaces for obvious shape inconsistencies.

Because standard monthly WTI options are American-style, this audit does not
impose European put-call parity. Instead it checks the quantities actually used
by the external-Q construction:

* fitted implied volatility remains finite and positive inside observed prior
  moneyness support;
* the quadratic smile has no more than one interior direction change on each
  option-type support;
* call and put fitted volatilities are compared on their overlapping observed
  support for the same underlying and training information set.

The audit is diagnostic; it does not reinterpret the fitted scalar volatility
as a structural diffusion coefficient.
"""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

from experiments.wti_external_vanilla_q_validation import (
    _fit_surface_models,
)
from experiments.wti_forward_q_validation import _predict


DEFAULT_PANEL = Path(
    "results/analysis/wti_databento_external_q/vanilla_iv_panel.csv"
)
DEFAULT_APO_IV = Path(
    "results/analysis/wti_apo_implied_volatility/apo_contract_implied_volatility.csv"
)
DEFAULT_OUTPUT = Path(
    "results/analysis/wti_databento_external_q/surface_shape_audit"
)


def _grid_prediction(
    beta: np.ndarray,
    option_type: str,
    lo: float,
    hi: float,
    *,
    points: int,
) -> tuple[np.ndarray, np.ndarray]:
    x = np.linspace(float(lo), float(hi), int(points))
    frame = pd.DataFrame(
        {
            "log_moneyness": x,
            "option_type": [option_type] * len(x),
        }
    )
    sigma = _predict(frame, beta)
    return x, np.asarray(sigma, dtype=float)


def _direction_changes(values: np.ndarray, tolerance: float = 1e-10) -> int:
    diff = np.diff(np.asarray(values, dtype=float))
    sign = np.sign(diff[np.abs(diff) > tolerance])
    if sign.size <= 1:
        return 0
    return int(np.sum(sign[1:] != sign[:-1]))


def run(
    panel_path: Path,
    apo_iv_path: Path,
    output_dir: Path,
    *,
    half_life_days: float = 5.0,
    ridge: float = 1e-6,
    points: int = 101,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    panel = pd.read_csv(panel_path)
    panel["reference_ts"] = pd.to_datetime(
        panel["reference_date"]
    ).dt.normalize()

    apo = pd.read_csv(apo_iv_path)
    apo = apo[apo["apo_expiry"].astype(str).eq("2026-10")].copy()
    target_dates = sorted(
        pd.to_datetime(apo["valuation_date"]).dt.normalize().unique()
    )

    rows: list[dict[str, Any]] = []
    for target_raw in target_dates:
        target = pd.Timestamp(target_raw).normalize()
        for method, half_life in (
            ("previous_day", None),
            ("expanding", float(half_life_days)),
        ):
            try:
                models, supports, training_end, n_dates = _fit_surface_models(
                    panel,
                    target_date=target,
                    half_life_days=half_life,
                    ridge=float(ridge),
                )
            except ValueError:
                continue

            for underlying, beta in sorted(models.items()):
                side_values: dict[str, tuple[np.ndarray, np.ndarray]] = {}
                for option_type in ("call", "put"):
                    support = supports.get((underlying, option_type))
                    if support is None:
                        continue
                    x, sigma = _grid_prediction(
                        beta,
                        option_type,
                        support[0],
                        support[1],
                        points=points,
                    )
                    side_values[option_type] = (x, sigma)
                    rows.append(
                        {
                            "target_date": target.strftime("%Y-%m-%d"),
                            "method": method,
                            "training_end_date": training_end,
                            "n_training_dates": int(n_dates),
                            "underlying": underlying,
                            "diagnostic": f"{option_type}_shape",
                            "support_lo": float(support[0]),
                            "support_hi": float(support[1]),
                            "min_sigma": float(np.min(sigma)),
                            "max_sigma": float(np.max(sigma)),
                            "n_nonpositive": int(np.sum(sigma <= 0)),
                            "n_nonfinite": int(np.sum(~np.isfinite(sigma))),
                            "direction_changes": _direction_changes(sigma),
                            "mean_call_put_gap": np.nan,
                            "max_call_put_gap": np.nan,
                        }
                    )

                call_support = supports.get((underlying, "call"))
                put_support = supports.get((underlying, "put"))
                if call_support is None or put_support is None:
                    continue
                lo = max(call_support[0], put_support[0])
                hi = min(call_support[1], put_support[1])
                if lo >= hi:
                    continue
                x = np.linspace(lo, hi, points)
                call = _predict(
                    pd.DataFrame(
                        {
                            "log_moneyness": x,
                            "option_type": ["call"] * points,
                        }
                    ),
                    beta,
                )
                put = _predict(
                    pd.DataFrame(
                        {
                            "log_moneyness": x,
                            "option_type": ["put"] * points,
                        }
                    ),
                    beta,
                )
                gap = np.abs(np.asarray(call) - np.asarray(put))
                rows.append(
                    {
                        "target_date": target.strftime("%Y-%m-%d"),
                        "method": method,
                        "training_end_date": training_end,
                        "n_training_dates": int(n_dates),
                        "underlying": underlying,
                        "diagnostic": "call_put_overlap",
                        "support_lo": float(lo),
                        "support_hi": float(hi),
                        "min_sigma": float(
                            min(np.min(call), np.min(put))
                        ),
                        "max_sigma": float(
                            max(np.max(call), np.max(put))
                        ),
                        "n_nonpositive": int(
                            np.sum(np.asarray(call) <= 0)
                            + np.sum(np.asarray(put) <= 0)
                        ),
                        "n_nonfinite": int(
                            np.sum(~np.isfinite(call))
                            + np.sum(~np.isfinite(put))
                        ),
                        "direction_changes": np.nan,
                        "mean_call_put_gap": float(np.mean(gap)),
                        "max_call_put_gap": float(np.max(gap)),
                    }
                )

    detail = pd.DataFrame(rows)
    if detail.empty:
        raise RuntimeError("surface-shape audit produced no rows")

    summary = pd.DataFrame(
        [
            {
                "n_diagnostics": int(len(detail)),
                "n_target_dates": int(detail["target_date"].nunique()),
                "total_nonpositive_predictions": int(
                    detail["n_nonpositive"].sum()
                ),
                "total_nonfinite_predictions": int(
                    detail["n_nonfinite"].sum()
                ),
                "max_direction_changes": float(
                    pd.to_numeric(
                        detail["direction_changes"],
                        errors="coerce",
                    ).max()
                ),
                "mean_call_put_gap": float(
                    pd.to_numeric(
                        detail["mean_call_put_gap"],
                        errors="coerce",
                    ).mean()
                ),
                "max_call_put_gap": float(
                    pd.to_numeric(
                        detail["max_call_put_gap"],
                        errors="coerce",
                    ).max()
                ),
            }
        ]
    )
    output_dir.mkdir(parents=True, exist_ok=True)
    detail.to_csv(output_dir / "surface_shape_detail.csv", index=False)
    summary.to_csv(output_dir / "surface_shape_summary.csv", index=False)
    return detail, summary


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--panel-path", type=Path, default=DEFAULT_PANEL)
    parser.add_argument("--apo-iv-path", type=Path, default=DEFAULT_APO_IV)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--half-life-days", type=float, default=5.0)
    parser.add_argument("--ridge", type=float, default=1e-6)
    parser.add_argument("--points", type=int, default=101)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    _, summary = run(
        args.panel_path,
        args.apo_iv_path,
        args.output_dir,
        half_life_days=float(args.half_life_days),
        ridge=float(args.ridge),
        points=int(args.points),
    )
    print(summary.to_string(index=False))
    print(f"output_dir={args.output_dir}")


if __name__ == "__main__":
    main()
