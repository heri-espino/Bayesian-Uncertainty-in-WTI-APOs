from __future__ import annotations

from types import SimpleNamespace

import pytest

from scripts import branch_audit


def test_merged_remote_branches_excludes_base_and_head(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(
        branch_audit,
        "_git",
        lambda *args: "\n".join(
            [
                "origin/HEAD -> origin/main",
                "origin/main",
                "origin/feature/a",
                "origin/fix/b",
            ]
        ),
    )
    assert branch_audit.merged_remote_branches() == ["feature/a", "fix/b"]


def test_delete_merged_remote_branches_pushes_only_supplied_branches(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    calls: list[list[str]] = []

    def fake_run(command, **kwargs):  # type: ignore[no-untyped-def]
        calls.append(list(command))
        return SimpleNamespace(stdout="")

    monkeypatch.setattr(branch_audit.subprocess, "run", fake_run)
    branch_audit.delete_merged_remote_branches(
        ["feature/a", "fix/b"], remote="origin"
    )

    assert calls[0] == ["git", "push", "origin", "--delete", "feature/a", "fix/b"]
    assert calls[1] == ["git", "fetch", "origin", "--prune"]


def test_delete_merged_requires_explicit_yes(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(branch_audit, "merged_remote_branches", lambda *args: ["feature/a"])
    with pytest.raises(SystemExit, match="explicit --yes"):
        branch_audit.main(["--delete-merged"])
