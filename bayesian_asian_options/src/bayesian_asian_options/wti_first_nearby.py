"""Helpers for reconstructing the first-nearby WTI CL roll used by CME APOs."""

from __future__ import annotations

import pandas as pd


def assign_first_nearby_contract(
    fixing_dates: pd.Series | pd.DatetimeIndex,
    contract_expiries: pd.DataFrame,
    *,
    contract_col: str = "contract",
    last_trade_col: str = "last_trade_date",
) -> pd.DataFrame:
    """Assign each fixing date to the earliest CL contract still trading.

    Exact exchange last-trade dates are supplied as data rather than inferred
    from a simplified holiday rule.
    """
    dates = pd.to_datetime(pd.Series(fixing_dates), errors="raise").dt.normalize()
    expiries = contract_expiries[[contract_col, last_trade_col]].copy()
    expiries[last_trade_col] = pd.to_datetime(expiries[last_trade_col], errors="raise").dt.normalize()
    expiries = expiries.sort_values(last_trade_col).reset_index(drop=True)

    rows: list[dict[str, object]] = []
    for date in dates:
        eligible = expiries.loc[expiries[last_trade_col] >= date]
        if eligible.empty:
            raise ValueError(f"No non-expired CL contract for fixing date {date.date()}")
        first = eligible.iloc[0]
        rows.append(
            {
                "fixing_date": date,
                "contract": first[contract_col],
                "contract_last_trade_date": first[last_trade_col],
            }
        )
    return pd.DataFrame(rows)


def build_forward_fixing_curve(
    fixing_dates: pd.Series | pd.DatetimeIndex,
    contract_expiries: pd.DataFrame,
    futures_curve: pd.DataFrame,
    *,
    contract_col: str = "contract",
    settlement_col: str = "settlement",
) -> pd.DataFrame:
    """Map remaining fixing dates to first-nearby contracts and current futures levels."""
    mapping = assign_first_nearby_contract(
        fixing_dates,
        contract_expiries,
        contract_col=contract_col,
    )
    curve = futures_curve[[contract_col, settlement_col]].copy()
    out = mapping.merge(curve, left_on="contract", right_on=contract_col, how="left")
    if out[settlement_col].isna().any():
        missing = out.loc[out[settlement_col].isna(), "contract"].drop_duplicates().tolist()
        raise ValueError(f"Missing current futures settlements for contracts: {missing}")
    return out[["fixing_date", "contract", "contract_last_trade_date", settlement_col]]
