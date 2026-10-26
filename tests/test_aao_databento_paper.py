"""Ensure the separate Databento-only Elsevier draft remains honest."""
from pathlib import Path
import subprocess
import sys

import pytest

from scripts.plot_aao_databento_only import check_results

ROOT = Path(__file__).resolve().parents[1]


def test_new_cas_paper_is_separate_from_earlier_barchart_paper():
    draft = (ROOT/"paper/jcm/databento_main.tex").read_text(encoding="utf-8")
    assert r"\documentclass[a4paper,fleqn]{cas-dc}" in draft
    assert "reduced-form" in draft
    assert "Databento" in draft
    assert "not yet been run" in draft
    assert "2026-09-04" not in draft
    assert r"\bibliography{references}" in draft


def test_new_cas_builder_checks_owner_template_without_results():
    subprocess.run(
        [sys.executable, str(ROOT/"paper/jcm/build_databento.py"), "--check"],
        cwd=ROOT, check=True, capture_output=True, text=True,
    )


def test_figure_builder_fails_closed_if_analyses_are_missing(tmp_path):
    with pytest.raises(FileNotFoundError, match="Missing completed"):
        check_results(tmp_path)


def test_new_manual_driver_has_no_databento_api_request():
    driver = (ROOT/"experiments/wti_aao_databento_only.py").read_text(
        encoding="utf-8"
    )
    assert "timeseries.get_range(" not in driver
    assert "db.Historical(" not in driver
    assert '"--execute"' in driver
    assert "reserve_parity_anchors" in driver
    assert "date_cluster_ci" in driver
