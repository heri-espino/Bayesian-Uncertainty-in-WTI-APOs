"""Guard the authoritative AAO paper handoff entry points and numerical labels.

Lightweight, deterministic repository-only assertions: no private DBNs or paid
Databento calls are needed to run these tests.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESEARCH = ROOT / "research"

DOCS = (
    ROOT / "HANDOFF.md",
    RESEARCH / "PAPER_COMPLETION_MASTER_PLAN_2026-10-26.md",
    RESEARCH / "AAO_EVIDENCE_LEDGER_2026-10-26.md",
    RESEARCH / "AAO_EXPERIMENT_REGISTER_2026-10-26.md",
    RESEARCH / "AAO_AGENT_VERIFICATION_PROTOCOL_2026-10-26.md",
    RESEARCH / "AAO_RECOVERY_AND_LFS_BACKUP_2026-10-26.md",
)


def test_handoff_bundle_files_are_present():
    for path in DOCS:
        assert path.is_file(), f"Missing required agent source: {path}"


def test_root_handoff_points_to_complete_packet():
    content = (ROOT / "HANDOFF.md").read_text(encoding="utf-8")
    for path in DOCS[1:]:
        assert path.name in content, f"Missing link to {path.name}"


def test_experiment_ids_are_ordered_and_unexecuted():
    import re

    content = (
        RESEARCH / "AAO_EXPERIMENT_REGISTER_2026-10-26.md"
    ).read_text(encoding="utf-8")
    headings = re.findall(r"^## (experiment\d{3})\b", content, re.MULTILINE)
    assert headings == [f"experiment{i:03d}" for i in range(1, 9)]
    assert "not yet" in content.lower() or "not executed" in content.lower()


def test_evidence_historical_counts_and_missing_data_are_explicit():
    content = (
        RESEARCH / "AAO_EVIDENCE_LEDGER_2026-10-26.md"
    ).read_text(encoding="utf-8")
    for text in ("70,154,064", "13,412,045", "5,899,096",
                 "5,105,603", "1,701", "1,700", "2024-01-26",
                 "2,381", "253", "17.49357489"):
        assert text in content
    assert "not" in content.lower() and "162" in content


def test_original_wti_work_is_retained():
    original_paths = (
        ROOT / "paper/jcm/main.tex",
        ROOT / "paper/manuscript/main.tex",
        ROOT / "paper/remef/README.md",
        ROOT / "figures/publication/figure_manifest.json",
        ROOT / "experiments/wti_aao_cross_month.py",
        ROOT / "scripts/aao_replay_offline.py",
        ROOT / "scripts/aao_lfs_preflight.py",
    )
    for path in original_paths:
        assert path.exists(), f"Missing historical source: {path}"
