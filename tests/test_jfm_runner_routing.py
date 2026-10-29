"""Safety guards for manual JFM workloads on the dedicated university VM."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_manual_jfm_workflows_target_only_pcag103a_15():
    for file in ("jfm-oracle-pilot.yml", "build-paper.yml"):
        text = (ROOT / ".github" / "workflows" / file).read_text(encoding="utf-8")
        assert "workflow_dispatch:" in text
        assert "runs-on: [self-hosted, windows, x64]" in text
        assert '$env:RUNNER_NAME -ne "PCAG103A-15"' in text
        assert "lfs: false" in text
        assert "push:" not in text
        assert "upload-artifact@v4" in text
        assert "CONDA_EXE" in text
        assert "sudo apt-get" not in text
        assert "git push " not in text


def test_remef_files_not_targeted_by_manual_jfm_build():
    build = (ROOT / ".github/workflows/build-paper.yml").read_text(encoding="utf-8")
    assert "ensure_jfm_miktex_packages.ps1" in build
    assert "scripts.verify_jfm_runner_build" in build
    assert "scripts.build_publication_figures --journal jfm" in build
    assert "paper/remef/" not in build
