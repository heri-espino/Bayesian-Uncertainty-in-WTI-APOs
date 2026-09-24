from __future__ import annotations

import pandas as pd
import pytest

from experiments.wti_databento_external_q import (
    _raw_cl_symbol,
    _statistics_cache_covers_symbols,
    select_option_definitions,
)


@pytest.mark.parametrize(
    ("source", "expected"),
    [
        ("CLX26", "CLX6"),
        ("CLZ26", "CLZ6"),
        ("CLX2026", "CLX6"),
        ("CLX6", "CLX6"),
    ],
)
def test_raw_cl_symbol(source: str, expected: str) -> None:
    assert _raw_cl_symbol(source) == expected


def test_select_option_definitions_filters_underlying_strike_and_spreads() -> None:
    definitions = pd.DataFrame(
        {
            "raw_symbol": [
                "LOX6 C8500",
                "LOX6 P8500",
                "LOZ6 C9000",
                "LOX6 C10000",
                "LOX6-LOZ6",
            ],
            "instrument_id": [1, 2, 3, 4, 5],
            "underlying": ["CLX6", "CLX6", "CLZ6", "CLX6", "CLX6"],
            "strike_price": [85.0, 85.0, 90.0, 100.0, 90.0],
            "instrument_class": ["C", "P", "CALL", "C", "OPTION_SPREAD"],
        }
    )

    selected = select_option_definitions(
        definitions,
        underlyings=("CLX26", "CLZ26"),
        strike_min=85.0,
        strike_max=94.5,
    )

    assert selected["raw_symbol"].tolist() == [
        "LOX6 C8500",
        "LOX6 P8500",
        "LOZ6 C9000",
    ]
    assert selected["option_type"].tolist() == ["call", "put", "call"]


def test_select_option_definitions_fails_closed_when_nothing_matches() -> None:
    definitions = pd.DataFrame(
        {
            "raw_symbol": ["LOF7 C8000"],
            "underlying": ["CLF7"],
            "strike_price": [80.0],
            "instrument_class": ["C"],
        }
    )

    with pytest.raises(RuntimeError, match="No LO option definitions matched"):
        select_option_definitions(
            definitions,
            underlyings=("CLX26",),
            strike_min=85.0,
            strike_max=94.5,
        )



def test_statistics_cache_requires_all_symbols(tmp_path) -> None:
    path = tmp_path / "stats.csv"
    pd.DataFrame(
        {
            "symbol": ["A", "B", "B"],
            "price": [1.0, 2.0, 2.1],
        }
    ).to_csv(path)

    assert _statistics_cache_covers_symbols(path, ["A", "B"])
    assert not _statistics_cache_covers_symbols(path, ["A", "B", "C"])


def test_statistics_cache_fails_closed_without_symbol_column(tmp_path) -> None:
    path = tmp_path / "stats.csv"
    pd.DataFrame({"price": [1.0]}).to_csv(path)

    assert not _statistics_cache_covers_symbols(path, ["A"])
