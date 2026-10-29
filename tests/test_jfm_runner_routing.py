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


def test_missing_cuted_sty_has_nonadmin_official_ctan_fallback():
    script = (ROOT / "scripts/ensure_jfm_miktex_packages.ps1").read_text(encoding="utf-8")
    build = (ROOT / "paper/build.py").read_text(encoding="utf-8")
    assert "packages update-package-database" in script
    assert "packages install sttools" in script
    assert "https://mirrors.ctan.org/macros/latex/contrib/sttools.zip" in script
    assert "latex" in script and "sttools.ins" in script
    assert "paper\\build\\local_tex" in script
    assert 'BUILD_DIR / "local_tex" / "cuted.sty"' in build
    assert 'shutil.copy2(local_cuted, STAGE_DIR / "cuted.sty")' in build
    assert "--admin" not in script

def test_miktex_update_reminder_on_stderr_is_not_a_hard_failure():
    """MiKTeX's 'major issue' update reminder does not imply a failed lookup."""
    script = (ROOT / "scripts/ensure_jfm_miktex_packages.ps1").read_text(encoding="utf-8")
    assert "Invoke-MiKTeXProcess" in script
    assert "System.Diagnostics.ProcessStartInfo" in script
    assert "RedirectStandardError = $true" in script
    assert "RedirectStandardOutput = $true" in script
    assert "$result.ExitCode -eq 0" in script
    assert "$result.StdOut" in script
    assert "No MiKTeX package installation or update is necessary" in script
    assert "exit 0" in script
    # Native stderr is handled by redirected .NET streams, not PowerShell's
    # NativeCommandError under ErrorActionPreference=Stop.
    assert '& $kpsewhich.Source cuted.sty 2>$null' not in script


def test_awesomefigures_pip_build_distutils_windows_repair():
    """Keep the Conda/setuptools workaround scoped to JFM AwesomeFigures install."""
    build = (ROOT / ".github/workflows/build-paper.yml").read_text(encoding="utf-8")
    assert "SETUPTOOLS_USE_DISTUTILS: stdlib" in build
    assert "_distutils_hack" in build
    assert "python -m pip install -r paper/requirements-awesomefigures.txt" in build
    assert "workflow_dispatch:" in build and "push:" not in build
