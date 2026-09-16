"""Validate the repository/package/manuscript architecture expected by maintainers."""
from __future__ import annotations

from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
PACKAGE_DIR = ROOT / "bayesian_asian_options" / "src" / "bayesian_asian_options"
API_DOC = ROOT / "docs" / "api" / "index.md"
PAPER_DIR = ROOT / "paper"
MANUSCRIPT_DIR = PAPER_DIR / "manuscript"
WILEY_DIR = PAPER_DIR / "vendor" / "wiley_njd_v5"

REQUIRED = [
    ROOT / "AGENTS.md",
    ROOT / "CONTRIBUTING.md",
    ROOT / "pyproject.toml",
    ROOT / "docs" / "index.md",
    ROOT / "docs" / "architecture.md",
    ROOT / "docs" / "repository_layout.md",
    ROOT / "docs" / "development.md",
    PACKAGE_DIR / "__init__.py",
    PAPER_DIR / "README.md",
    PAPER_DIR / "build.py",
    MANUSCRIPT_DIR / "main.tex",
    MANUSCRIPT_DIR / "references.bib",
    WILEY_DIR / "WileyNJDv5.cls",
    WILEY_DIR / "wileyNJD-Harvard.bst",
]
FORBIDDEN_ROOT = [
    "src",
    "reporte",
    "presentacion",
    "notebook.ipynb",
    "notebook.py",
    "old_notebook.ipynb",
    ".DS_Store",
    "Wiley_New_Journal_Design_version_5__NJD_v5_",
]
LEGACY_IMPORT = re.compile(r"(^|\n)\s*(?:from|import)\s+src(?:\.|\s|$)")
EXPECTED_WILEY_CLASS = r"\documentclass[HARVARD,Utopia2COL]{WileyNJDv5}"
GENERATED_TEX_SUFFIXES = {
    ".aux", ".bbl", ".bcf", ".blg", ".fdb_latexmk", ".fls", ".log", ".out",
}
GENERATED_TEX_NAMES = {"main.pdf", "main.synctex.gz", "main.run.xml"}


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

    main_tex = MANUSCRIPT_DIR / "main.tex"
    if main_tex.exists():
        manuscript = main_tex.read_text(encoding="utf-8")
        if EXPECTED_WILEY_CLASS not in manuscript:
            errors.append(
                "JFM manuscript must preserve HARVARD,Utopia2COL WileyNJDv5 layout"
            )
        if "\\journal{Journal of Futures Markets}" not in manuscript:
            errors.append("JFM manuscript is missing the Journal of Futures Markets marker")

    if MANUSCRIPT_DIR.exists():
        for path in MANUSCRIPT_DIR.rglob("*"):
            if not path.is_file():
                continue
            if path.suffix in GENERATED_TEX_SUFFIXES or path.name in GENERATED_TEX_NAMES:
                errors.append(
                    f"generated LaTeX artifact must live in paper/build: {path.relative_to(ROOT)}"
                )

    if errors:
        raise SystemExit("Repository structure check failed:\n- " + "\n- ".join(errors))
    print("Repository structure check passed")


if __name__ == "__main__":
    main()
