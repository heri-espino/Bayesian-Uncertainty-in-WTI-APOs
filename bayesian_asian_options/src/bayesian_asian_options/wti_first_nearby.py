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
    expiries[last_trade_col] = pd.to_datetime(
        expiries[last_trade_col], errors="raise"
    ).dt.normalize()
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
        missing = (
            out.loc[out[settlement_col].isna(), "contract"].drop_duplicates().tolist()
        )
        raise ValueError(f"Missing current futures settlements for contracts: {missing}")
    return out[["fixing_date", "contract", "contract_last_trade_date", settlement_col]]


def build_realized_fixing_curve(
    fixing_dates: pd.Series | pd.DatetimeIndex,
    contract_expiries: pd.DataFrame,
    futures_history: pd.DataFrame,
    *,
    contract_col: str = "contract",
    trade_date_col: str = "trade_date",
    history_price_col: str = "latest",
    settlement_col: str = "settlement",
) -> pd.DataFrame:
    """Reconstruct realized first-nearby fixings from contract-level CL history.

    Each fixing date is first mapped to the applicable CL contract using the
    explicit last-trade-date table.  The realized fixing is then taken from the
    exact contract/date observation in ``futures_history``.  Missing dates are
    rejected rather than forward-filled so that exchange holidays or data gaps
    cannot silently become synthetic settlements.

    Parameters
    ----------
    fixing_dates:
        Fixing dates already known at the valuation timestamp.
    contract_expiries:
        Explicit CL contract last-trade-date table.
    futures_history:
        Normalized contract-level history containing at least trade date,
        contract, and the source price field (``latest`` by default).

    Returns
    -------
    pandas.DataFrame
        One row per fixing date with the mapped contract and realized
        ``settlement`` proxy.  Source metadata columns are retained when
        present in ``futures_history``.
    """
    mapping = assign_first_nearby_contract(
        fixing_dates,
        contract_expiries,
        contract_col=contract_col,
    )
    if mapping.empty:
        return pd.DataFrame(
            columns=[
                "fixing_date",
                "contract",
                "contract_last_trade_date",
                settlement_col,
            ]
        )

    required = {trade_date_col, contract_col, history_price_col}
    missing_columns = required.difference(futures_history.columns)
    if missing_columns:
        raise ValueError(
            f"Futures history missing columns: {sorted(missing_columns)}"
        )

    metadata_columns = [
        column
        for column in ["source_file", "source_field", "price_interpretation"]
        if column in futures_history.columns
    ]
    history = futures_history[
        [trade_date_col, contract_col, history_price_col, *metadata_columns]
    ].copy()
    history[trade_date_col] = pd.to_datetime(
        history[trade_date_col], errors="raise"
    ).dt.normalize()
    history = history.drop_duplicates([trade_date_col, contract_col], keep="last")

    out = mapping.merge(
        history,
        left_on=["fixing_date", "contract"],
        right_on=[trade_date_col, contract_col],
        how="left",
    )
    missing = out[history_price_col].isna()
    if missing.any():
        detail = ", ".join(
            f"{row.fixing_date.date()}:{row.contract}"
            for row in out.loc[missing, ["fixing_date", "contract"]].itertuples(
                index=False
            )
        )
        raise ValueError(
            "Missing realized first-nearby settlements for fixing dates: " + detail
        )

    out = out.rename(columns={history_price_col: settlement_col})
    columns = [
        "fixing_date",
        "contract",
        "contract_last_trade_date",
        settlement_col,
        *metadata_columns,
    ]
    return out[columns].sort_values("fixing_date").reset_index(drop=True)
