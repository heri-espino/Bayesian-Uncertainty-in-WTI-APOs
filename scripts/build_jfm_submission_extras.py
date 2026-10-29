"""Build JFM title-page and supporting-information PDFs, and package blind TeX.

Manual submission artifact only. No experiments, no Git commits.
The identifying title page is NEVER copied into the blinded source bundle.
"""
from __future__ import annotations

from pathlib import Path
import shutil
import subprocess
import tempfile
import zipfile

ROOT = Path(__file__).resolve().parents[1]
PAPER = ROOT / "paper"


def compile_tex(source: Path, destination: Path) -> Path:
    command = shutil.which("xelatex")
    if not command:
        raise RuntimeError("XeLaTeX is required for JFM submission extras")
    with tempfile.TemporaryDirectory(prefix="jfm-extra-") as folder:
        stage = Path(folder)
        shutil.copy2(source, stage / source.name)
        for _ in range(2):
            subprocess.run([command, "-interaction=nonstopmode",
                            "-halt-on-error", "-file-line-error", source.name],
                           cwd=stage, check=True)
        pdf = stage / f"{source.stem}.pdf"
        if not pdf.is_file() or pdf.stat().st_size < 1500:
            raise RuntimeError(f"No complete PDF for {source.name}")
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(pdf, destination)
    return destination


def blinded_source_package(source_dir: Path, target: Path) -> Path:
    main = source_dir / "main.tex"
    if not main.is_file():
        raise FileNotFoundError("The canonical Wiley build must run before packaging")
    approved = {".cls", ".sty", ".bst", ".tex", ".bib", ".tfm",
                ".pfb", ".enc", ".map", ".fd", ".otf", ".ttf"}
    target.parent.mkdir(parents=True, exist_ok=True)
    files = []
    for path in source_dir.rglob("*"):
        if not path.is_file():
            continue
        rel = path.relative_to(source_dir)
        if path.suffix.lower() in approved or (
            path.suffix.lower() == ".pdf" and
            "figures" in rel.parts
        ):
            files.append(path)
    if not any(path.name == "main.tex" for path in files):
        raise RuntimeError("Missing main.tex")
    with zipfile.ZipFile(target, "w", compression=zipfile.ZIP_DEFLATED) as package:
        for path in sorted(files):
            rel = path.relative_to(source_dir)
            # Fail closed: the editor-only author title page must be separate.
            if "jfm_title_page" in rel.as_posix().lower():
                raise RuntimeError("Identifying title page leaked into anonymous ZIP")
            package.write(path, arcname=rel.as_posix())
    return target


def main() -> None:
    outputs = (
        compile_tex(PAPER / "manuscript/jfm_title_page.tex",
                    PAPER / "jfm_title_page.pdf"),
        compile_tex(PAPER / "supplement/jfm_supporting_information.tex",
                    PAPER / "supplement/jfm_supporting_information.pdf"),
        blinded_source_package(PAPER / "build/stage",
                               PAPER / "jfm_blinded_latex_sources.zip"),
    )
    for output in outputs:
        print(f"Built {output.relative_to(ROOT)} ({output.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
