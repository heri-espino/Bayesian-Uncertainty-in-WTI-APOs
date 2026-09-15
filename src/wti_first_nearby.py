"""Helpers for mapping WTI APO fixing dates to first-nearby CL futures."""

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

    Exact CL last-trade dates should come from an exchange/calendar source.
    They are input data here rather than inferred from a brittle holiday rule.
    """
    dates = pd.to_datetime(pd.Series(fixing_dates), errors="raise").dt.normalize()
    expiries = contract_expiries[[contract_col, last_trade_col]].copy()
    expiries[last_trade_col] = pd.to_datetime(expiries[last_trade_col]).dt.normalize()
    expiries = expiries.sort_values(last_trade_col).reset_index(drop=True)

    rows = []
    for date in dates:
        eligible = expiries.loc[expiries[last_trade_col] >= date]
        if eligible.empty:
            raise ValueError(f"No non-expired CL contract available for fixing date {date.date()}")
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
    """Map future fixing dates to first-nearby contracts and current settlements."""
    mapping = assign_first_nearby_contract(
        fixing_dates,
        contract_expiries,
        contract_col=contract_col,
    )
    curve = futures_curve[[contract_col, settlement_col]].copy()
    merged = mapping.merge(curve, left_on="contract", right_on=contract_col, how="left")
    if merged[settlement_col].isna().any():
        missing = merged.loc[merged[settlement_col].isna(), "contract"].unique().tolist()
        raise ValueError(f"Missing current futures settlements for contracts: {missing}")
    return merged[["fixing_date", "contract", "contract_last_trade_date", settlement_col]]
