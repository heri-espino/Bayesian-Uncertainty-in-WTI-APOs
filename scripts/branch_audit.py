"""Audit and optionally delete remote branches already merged into the base branch.

Examples
--------
Refresh remote refs and list branches already merged into ``origin/main``::

    python -m scripts.branch_audit --fetch

Print explicit deletion commands without changing the remote::

    python -m scripts.branch_audit --fetch --delete-commands

Delete only branches Git reports as fully merged into ``origin/main``::

    python -m scripts.branch_audit --fetch --delete-merged --yes

Deletion is opt-in and requires ``--yes``. Branches with unique commits are never deleted by
``--delete-merged``; inspect and remove intentionally superseded branches manually.
"""

from __future__ import annotations

import argparse
from pathlib import Path
import subprocess


ROOT = Path(__file__).resolve().parents[1]


def _git(*args: str) -> str:
    completed = subprocess.run(
        ["git", *args],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    return completed.stdout.strip()


def merged_remote_branches(remote: str = "origin", base: str = "main") -> list[str]:
    """Return remote branch names fully merged into ``remote/base``.

    The returned names do not include the base branch or the synthetic ``HEAD`` ref.
    """
    target = f"{remote}/{base}"
    output = _git("branch", "-r", "--merged", target, "--format=%(refname:short)")
    branches: list[str] = []
    prefix = f"{remote}/"
    for line in output.splitlines():
        ref = line.strip()
        if not ref.startswith(prefix):
            continue
        name = ref[len(prefix) :]
        if name in {base, "HEAD"} or name.startswith("HEAD ->"):
            continue
        branches.append(name)
    return sorted(set(branches))


def delete_merged_remote_branches(
    branches: list[str],
    *,
    remote: str = "origin",
) -> None:
    """Delete an already-audited list of merged remote branches.

    ``branches`` must come from :func:`merged_remote_branches`. The base branch is not part
    of that list, so this helper cannot delete it through the normal CLI path.
    """
    if not branches:
        return
    subprocess.run(
        ["git", "push", remote, "--delete", *branches],
        cwd=ROOT,
        check=True,
    )
    subprocess.run(["git", "fetch", remote, "--prune"], cwd=ROOT, check=True)


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--remote", default="origin")
    parser.add_argument("--base", default="main")
    parser.add_argument("--fetch", action="store_true", help="Run git fetch --prune first")
    parser.add_argument(
        "--delete-commands",
        action="store_true",
        help="Print deletion commands for review; never executes them",
    )
    parser.add_argument(
        "--delete-merged",
        action="store_true",
        help="Delete only remote branches Git reports as fully merged into remote/base",
    )
    parser.add_argument(
        "--yes",
        action="store_true",
        help="Required confirmation for --delete-merged",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> None:
    args = parse_args(argv)
    if args.fetch:
        subprocess.run(["git", "fetch", args.remote, "--prune"], cwd=ROOT, check=True)

    branches = merged_remote_branches(args.remote, args.base)
    print(f"Base: {args.remote}/{args.base}")
    print(f"Fully merged remote feature branches: {len(branches)}")
    for branch in branches:
        print(f"  {branch}")

    if args.delete_commands and branches:
        print("\nReview before running:")
        for branch in branches:
            print(f"git push {args.remote} --delete {branch}")

    if args.delete_merged:
        if not args.yes:
            raise SystemExit("Refusing branch deletion without explicit --yes confirmation")
        delete_merged_remote_branches(branches, remote=args.remote)
        print(f"\nDeleted {len(branches)} fully merged remote feature branches.")

    print(
        "\nBranches with unique unmerged commits are intentionally not classified as safe "
        "by this script; inspect their PR/history manually before deletion."
    )


if __name__ == "__main__":
    main()
