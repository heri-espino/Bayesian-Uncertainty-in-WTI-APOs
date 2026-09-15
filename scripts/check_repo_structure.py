"""Validate the repository/package architecture expected by maintainers and agents."""
from __future__ import annotations

from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
PACKAGE_DIR = ROOT / "bayesian_asian_options" / "src" / "bayesian_asian_options"
API_DOC = ROOT / "docs" / "api" / "index.md"

REQUIRED = [
    ROOT / "AGENTS.md",
    ROOT / "pyproject.toml",
    ROOT / "docs" / "index.md",
    ROOT / "docs" / "architecture.md",
    PACKAGE_DIR / "__init__.py",
]
FORBIDDEN_ROOT = [
    "src",
    "reporte",
    "presentacion",
    "notebook.ipynb",
    "notebook.py",
    "old_notebook.ipynb",
    ".DS_Store",
]
LEGACY_IMPORT = re.compile(r"(^|\n)\s*(?:from|import)\s+src(?:\.|\s|$)")


def main() -> None:
    errors: list[str] = []
    for path in REQUIRED:
        if not path.exists():
            errors.append(f"missing required path: {path.relative_to(ROOT)}")
    for name in FORBIDDEN_ROOT:
        if (ROOT / name).exists():
            errors.append(f"forbidden root-level path returned: {name}")

    scan_roots = [PACKAGE_DIR, ROOT / "experiments", ROOT / "tests", ROOT / "scripts"]
    for base in scan_roots:
        if not base.exists():
            continue
        for path in base.rglob("*.py"):
            text = path.read_text(encoding="utf-8")
            if LEGACY_IMPORT.search(text):
                errors.append(f"legacy 'src' import in {path.relative_to(ROOT)}")

    if PACKAGE_DIR.exists() and API_DOC.exists():
        api = API_DOC.read_text(encoding="utf-8")
        modules = sorted(
            path.stem for path in PACKAGE_DIR.glob("*.py") if path.name != "__init__.py"
        )
        for module in modules:
            dotted = f"bayesian_asian_options.{module}"
            if dotted not in api:
                errors.append(f"public module missing from Sphinx API reference: {dotted}")

    if errors:
        raise SystemExit("Repository structure check failed:\n- " + "\n- ".join(errors))
    print("Repository structure check passed")


if __name__ == "__main__":
    main()
