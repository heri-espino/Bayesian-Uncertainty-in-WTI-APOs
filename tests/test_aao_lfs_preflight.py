"""Offline Git LFS preflight unit tests; no API, paid requests or vendor data."""
from pathlib import Path
from subprocess import CompletedProcess

from scripts.aao_lfs_preflight import expected_source_paths, inspect, windows


def test_expected_81_month_two_schema_source_inventory():
    paths = expected_source_paths()
    assert len(windows()) == 81
    assert len(paths) == 162
    assert all(str(p).endswith(".dbn.zst") for p in paths)
    assert str(paths[0]).replace("\\", "/").endswith(
        "aao_definition__2020-01-01__2020-02-01.dbn.zst"
    )
    assert str(paths[-1]).replace("\\", "/").endswith(
        "aao_statistics__2026-09-01__2026-10-01.dbn.zst"
    )
    assert len(set(paths)) == 162


def test_preflight_missing_lfs_or_anchor_fails_before_download(monkeypatch, tmp_path):
    def mock_git(root, *args):
        if args[:2] == ("rev-parse", "--show-toplevel"):
            return CompletedProcess(args, 0, stdout=str(tmp_path))
        if args[:2] == ("lfs", "version"):
            return CompletedProcess(args, 1, stdout="")
        if args[:2] == ("check-attr", "filter"):
            return CompletedProcess(args, 0, stdout="path: filter: unspecified")
        if args[:2] == ("check-ignore", "--no-index"):
            return CompletedProcess(args, 0, stdout=".gitignore:1:raw/*\tpath")  # ignored
        return CompletedProcess(args, 1, stdout="")
    monkeypatch.setattr("scripts.aao_lfs_preflight.git", mock_git)
    result = inspect(tmp_path)
    assert not result["ready"]
    assert result["source_files_currently_present"] == 0
    assert any("git_lfs_unavailable" in x for x in result["issues"])
    assert any("source_file_still_ignored" in x for x in result["issues"])
    assert result["market_provider_contacted"] is False


def test_preflight_successful_config_and_complete_gate(monkeypatch, tmp_path):
    anchor = tmp_path / "data" / "databento" / "wti_aao_bulk" / "README.md"
    anchor.parent.mkdir(parents=True)
    anchor.write_text("backup root")
    def mock_git(root, *args):
        if args[:2] == ("rev-parse", "--show-toplevel"):
            return CompletedProcess(args, 0, stdout=str(tmp_path))
        if args[:2] == ("ls-files", "--error-unmatch"):
            return CompletedProcess(args, 0, stdout="anchor")
        if args[:2] == ("lfs", "version"):
            return CompletedProcess(args, 0, stdout="git-lfs/3.x")
        if args[:2] == ("check-attr", "filter"):
            return CompletedProcess(args, 0, stdout="path: filter: lfs")
        if args[:2] == ("check-ignore", "--no-index"):
            return CompletedProcess(args, 0, stdout=".gitignore:1:!raw/aao_*.dbn.zst\tpath")
        return CompletedProcess(args, 1, stdout="")
    monkeypatch.setattr("scripts.aao_lfs_preflight.git", mock_git)
    assert inspect(tmp_path)["ready"]
    result = inspect(tmp_path, require_complete=True)
    assert not result["ready"]
    assert "missing_source_files:162" in result["issues"]



def test_real_git_negative_ignore_rule_is_not_reported_as_ignored(tmp_path):
    """Regression: check-ignore -q reports negations as matches."""
    import shutil
    import subprocess

    if not shutil.which("git"):
        return
    subprocess.run(["git", "init", "-q"], cwd=tmp_path, check=True)
    anchor = tmp_path / "data/databento/wti_aao_bulk/README.md"
    anchor.parent.mkdir(parents=True)
    anchor.write_text("anchor")
    subprocess.run(["git", "add", str(anchor.relative_to(tmp_path))],
                   cwd=tmp_path, check=True)
    (tmp_path / ".gitignore").write_text(
        "data/databento/**/raw/\n"
        "!data/databento/wti_aao_bulk/raw/\n"
        "data/databento/wti_aao_bulk/raw/*\n"
        "!data/databento/wti_aao_bulk/raw/aao_definition__*.dbn.zst\n"
        "!data/databento/wti_aao_bulk/raw/aao_statistics__*.dbn.zst\n"
        "data/databento/wti_aao_bulk/raw/*.partial.dbn.zst\n"
    )
    (tmp_path / ".gitattributes").write_text(
        "data/databento/wti_aao_bulk/raw/*.dbn.zst filter=lfs "
        "diff=lfs merge=lfs -text\n"
    )
    from scripts.aao_lfs_preflight import inspect

    result = inspect(tmp_path)
    # Git LFS might not be installed in arbitrary test environments;
    # the critical check is the absence of false "ignored" errors.
    assert not any("source_file_still_ignored" in issue
                   for issue in result["issues"])
