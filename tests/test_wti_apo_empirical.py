from pathlib import Path

import pandas as pd

from bayesian_asian_options.barchart_cl import load_cl_expiry_table
from experiments.wti_apo_empirical import (
    ROOT,
    _candidate_curve_contracts,
    _portable_path,
    _runtime_metadata,
)


def test_october_2026_curve_strip_uses_only_fixing_contracts() -> None:
    assert _candidate_curve_contracts("2026-10") == ["CLX26", "CLZ26"]


def test_other_apo_months_map_to_next_two_delivery_contracts() -> None:
    assert _candidate_curve_contracts("2026-09") == ["CLV26", "CLX26"]
    assert _candidate_curve_contracts("2026-11") == ["CLZ26", "CLF27"]
    assert _candidate_curve_contracts("2029-06") == ["CLN29", "CLQ29"]


def test_october_2026_expiry_reference_is_explicit() -> None:
    table = load_cl_expiry_table(
        ROOT / "data" / "csv" / "CL" / "contract_expiries.csv",
        contracts=["CLX26", "CLZ26"],
    ).set_index("contract")
    assert table.loc["CLX26", "last_trade_date"] == pd.Timestamp("2026-10-20")
    assert table.loc["CLZ26", "last_trade_date"] == pd.Timestamp("2026-11-20")
    assert table.loc["CLX26", "source"] == "CME_CL_termination_rule_explicit_study_table"


def test_manifest_path_is_repository_relative() -> None:
    path = ROOT / "data" / "csv" / "CL" / "contract_expiries.csv"
    assert _portable_path(path) == "data/csv/CL/contract_expiries.csv"


def test_external_manifest_path_does_not_expose_workstation_directories(
    tmp_path: Path,
) -> None:
    external = tmp_path / "external_reference.csv"
    external.write_text("x\n1\n", encoding="utf-8")
    assert _portable_path(external) == "<external>/external_reference.csv"


def test_runtime_metadata_records_versions_without_hostname() -> None:
    metadata = _runtime_metadata()
    assert {"git_commit", "git_dirty", "python", "platform", "numpy", "pandas", "scipy"} <= set(metadata)
    assert "hostname" not in metadata
    assert "user" not in metadata
