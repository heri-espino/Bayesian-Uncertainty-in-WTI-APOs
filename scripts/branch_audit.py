"""Report stale remote branches without deleting anything.

Examples
--------
Refresh remote refs and list branches already merged into ``origin/main``::

    python -m scripts.branch_audit --fetch

Also print explicit deletion commands::

    python -m scripts.branch_audit --fetch --delete-commands

The script is intentionally read-only with respect to branch deletion. A human must review
and run the printed ``git push <remote> --delete <branch>`` commands.
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

    print(
        "\nBranches with unique unmerged commits are intentionally not classified as safe "
        "by this script; inspect their PR/history manually before deletion."
    )


if __name__ == "__main__":
    main()
