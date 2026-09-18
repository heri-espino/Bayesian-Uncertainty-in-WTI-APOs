"""Prepare vendored Adobe Utopia / PSNFSS support for local figure builds.

The repository keeps upstream CTAN archives intact under
paper/vendor/fonts/utopia/upstream. This module expands them only into the ignored
paper/build/vendor_fonts tree and exposes that tree to kpathsea through environment
variables. No system-wide TeX installation is modified.

The Utopia archive supplies Adobe Type 1 PFB/AFM files. PSNFSS supplies the LaTeX
interface plus the nested freenfss.zip metrics/font-definition support and Utopia map.
mathastext is vendored separately from its CTAN .dtx source and extracted into the
same local TDS tree. The three components together reproduce the typography stack
loaded by WileyNJDv5 under Utopia2COL.

Diagnostic:
    python -m scripts.vendor_utopia_fonts
"""

from __future__ import annotations

import hashlib
import json
import os
import shutil
import subprocess
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VENDOR_ROOT = ROOT / "paper" / "vendor" / "fonts" / "utopia"
UPSTREAM_ROOT = VENDOR_ROOT / "upstream"
UTOPIA_ZIP = UPSTREAM_ROOT / "utopia.zip"
PSNFSS_ZIP = UPSTREAM_ROOT / "psnfss.zip"
MATHASTEXT_ROOT = ROOT / "paper" / "vendor" / "fonts" / "mathastext"
MATHASTEXT_UPSTREAM = MATHASTEXT_ROOT / "upstream"
MATHASTEXT_DTX = MATHASTEXT_UPSTREAM / "mathastext.dtx"
CACHE_ROOT = ROOT / "paper" / "build" / "vendor_fonts" / "utopia"
TEXMF_ROOT = CACHE_ROOT / "texmf"
SOURCE_ROOT = CACHE_ROOT / "source"
MARKER = CACHE_ROOT / "prepared.json"


def _candidate_tex_bin_dirs() -> list[Path]:
    """Return plausible per-user/system TeX bin directories, especially on Windows."""
    candidates: list[Path] = []

    def add(path: Path | None) -> None:
        if path is not None and path not in candidates:
            candidates.append(path)

    local = os.environ.get("LOCALAPPDATA")
    roaming = os.environ.get("APPDATA")
    program_files = os.environ.get("ProgramFiles")
    program_files_x86 = os.environ.get("ProgramFiles(x86)")
    user_profile = os.environ.get("USERPROFILE")

    for base in filter(None, (local, roaming, program_files, program_files_x86)):
        root = Path(base)
        add(root / "Programs" / "MiKTeX" / "miktex" / "bin" / "x64")
        add(root / "MiKTeX" / "miktex" / "bin" / "x64")
        add(root / "MiKTeX" / "miktex" / "bin")

    texlive_roots = [Path("C:/texlive")]
    if user_profile:
        texlive_roots.append(Path(user_profile) / "texlive")
    if local:
        texlive_roots.append(Path(local) / "Programs" / "TeXLive")

    for root in texlive_roots:
        if root.is_dir():
            for version_dir in sorted(root.glob("*"), reverse=True):
                add(version_dir / "bin" / "windows")
                add(version_dir / "bin" / "win32")

    return [path for path in candidates if path.is_dir()]


def _find_executable(name: str) -> str | None:
    """Find a TeX executable on PATH or in common Windows install locations."""
    found = shutil.which(name)
    if found:
        return found

    names = [name]
    if os.name == "nt" and not name.lower().endswith(".exe"):
        names.append(name + ".exe")

    for directory in _candidate_tex_bin_dirs():
        for candidate_name in names:
            candidate = directory / candidate_name
            if candidate.is_file():
                return str(candidate)
    return None


def ensure_tex_toolchain_on_path() -> dict[str, str | None]:
    """Discover TeX tools and prepend their directory to PATH when necessary."""
    tool_names = ("latex", "kpsewhich", "dvipng", "tex", "etex", "pdftex")
    discovered = {name: _find_executable(name) for name in tool_names}

    directories: list[str] = []
    for path in discovered.values():
        if path:
            directory = str(Path(path).resolve().parent)
            if directory not in directories:
                directories.append(directory)

    if directories:
        current = os.environ.get("PATH", "")
        current_parts = current.split(os.pathsep) if current else []
        missing = [directory for directory in directories if directory not in current_parts]
        if missing:
            os.environ["PATH"] = os.pathsep.join(missing + current_parts)

    # Re-resolve after PATH mutation so subprocesses and diagnostics see canonical paths.
    return {name: shutil.which(name) or discovered[name] for name in tool_names}


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _fingerprint() -> dict[str, str]:
    return {
        "utopia_zip_sha256": _sha256(UTOPIA_ZIP),
        "psnfss_zip_sha256": _sha256(PSNFSS_ZIP),
        "mathastext_dtx_sha256": _sha256(MATHASTEXT_DTX),
    }


def archives_available() -> bool:
    return (
        UTOPIA_ZIP.is_file()
        and PSNFSS_ZIP.is_file()
        and MATHASTEXT_DTX.is_file()
    )


def inspect_archives() -> dict[str, object]:
    if not archives_available():
        missing = [
            str(p)
            for p in (UTOPIA_ZIP, PSNFSS_ZIP, MATHASTEXT_DTX)
            if not p.is_file()
        ]
        raise FileNotFoundError(f"Missing vendored font archive(s): {missing}")

    with zipfile.ZipFile(UTOPIA_ZIP) as zf:
        utopia_members = [name for name in zf.namelist() if not name.endswith("/")]
    with zipfile.ZipFile(PSNFSS_ZIP) as zf:
        psnfss_members = [name for name in zf.namelist() if not name.endswith("/")]

    utopia_basenames = {Path(name).name for name in utopia_members}
    psnfss_basenames = {Path(name).name for name in psnfss_members}
    expected_utopia = {
        "LICENSE-utopia.txt",
        "README-utopia.txt",
        "putr8a.afm",
        "putr8a.pfb",
        "putri8a.afm",
        "putri8a.pfb",
        "putb8a.afm",
        "putb8a.pfb",
        "putbi8a.afm",
        "putbi8a.pfb",
    }

    return {
        **_fingerprint(),
        "utopia_members": len(utopia_members),
        "psnfss_members": len(psnfss_members),
        "missing_expected_utopia_files": sorted(expected_utopia - utopia_basenames),
        "psnfss_has_freenfss_zip": "freenfss.zip" in psnfss_basenames,
        "psnfss_has_psfonts_ins": "psfonts.ins" in psnfss_basenames,
        "psnfss_has_psfonts_dtx": "psfonts.dtx" in psnfss_basenames,
        "psnfss_has_utopia_map": "utopia.map" in psnfss_basenames,
        "psnfss_has_8r_enc": "8r.enc" in psnfss_basenames,
        "mathastext_dtx_present": MATHASTEXT_DTX.is_file(),
    }


def _prepend_env_path(name: str, value: Path) -> None:
    previous = os.environ.get(name, "")
    prefix = str(value)
    os.environ[name] = prefix + os.pathsep + previous if previous else prefix + os.pathsep


def _activate_texmf_paths(texmf: Path) -> None:
    _prepend_env_path("TEXINPUTS", texmf / "tex" / "latex" / "mathastext")
    _prepend_env_path("TEXINPUTS", texmf / "tex" / "latex" / "psnfss")
    _prepend_env_path("TEXINPUTS", texmf / "tex")
    _prepend_env_path("TFMFONTS", texmf / "fonts" / "tfm")
    _prepend_env_path("VFFONTS", texmf / "fonts" / "vf")
    _prepend_env_path("T1FONTS", texmf / "fonts" / "type1")
    _prepend_env_path("AFMFONTS", texmf / "fonts" / "afm")
    _prepend_env_path("TEXFONTMAPS", texmf / "fonts" / "map")
    _prepend_env_path("ENCFONTS", texmf / "fonts" / "enc")


def _find_one(root: Path, basename: str) -> Path | None:
    matches = [p for p in root.rglob(basename) if p.is_file()]
    return matches[0] if matches else None


def _run_docstrip(psnfss_source: Path, texmf: Path) -> bool:
    latex = _find_executable("latex")
    ins = _find_one(psnfss_source, "psfonts.ins")
    if latex is None or ins is None:
        return False

    proc = subprocess.run(
        [latex, "-interaction=nonstopmode", "-halt-on-error", ins.name],
        cwd=ins.parent,
        capture_output=True,
        text=True,
        check=False,
    )
    if proc.returncode != 0:
        return False

    generated = _find_one(ins.parent, "utopia.sty")
    if generated is None:
        return False

    target = texmf / "tex" / "latex" / "psnfss"
    target.mkdir(parents=True, exist_ok=True)
    for sty in ins.parent.rglob("*.sty"):
        shutil.copy2(sty, target / sty.name)
    return True


def _extract_mathastext(texmf: Path) -> bool:
    """Extract mathastext.sty from the vendored .dtx without installing globally."""
    source_dir = SOURCE_ROOT / "mathastext"
    source_dir.mkdir(parents=True, exist_ok=True)
    source = source_dir / "mathastext.dtx"
    shutil.copy2(MATHASTEXT_DTX, source)

    engine = next(
        (_find_executable(name) for name in ("etex", "tex", "pdftex") if _find_executable(name)),
        None,
    )
    if engine is None:
        return False

    proc = subprocess.run(
        [engine, source.name],
        cwd=source_dir,
        capture_output=True,
        text=True,
        check=False,
    )
    generated = source_dir / "mathastext.sty"
    if proc.returncode != 0 or not generated.is_file():
        return False

    target = texmf / "tex" / "latex" / "mathastext"
    target.mkdir(parents=True, exist_ok=True)
    shutil.copy2(generated, target / "mathastext.sty")
    for optional in ("README.md", "ChangeLog.md"):
        candidate = source_dir / optional
        if candidate.is_file():
            doc_target = texmf / "doc" / "latex" / "mathastext"
            doc_target.mkdir(parents=True, exist_ok=True)
            shutil.copy2(candidate, doc_target / optional)
    return True


def _build_local_pdftex_map(texmf: Path, utopia_map: Path) -> None:
    target_dir = texmf / "fonts" / "map" / "dvips" / "psnfss"
    target_dir.mkdir(parents=True, exist_ok=True)
    target = target_dir / "pdftex.map"

    base_map = b""
    kpsewhich = _find_executable("kpsewhich")
    if kpsewhich is not None:
        proc = subprocess.run(
            [kpsewhich, "pdftex.map"],
            capture_output=True,
            text=True,
            check=False,
        )
        if proc.returncode == 0 and proc.stdout.strip():
            source = Path(proc.stdout.strip())
            if source.is_file():
                base_map = source.read_bytes()

    target.write_bytes(
        base_map.rstrip()
        + b"\n% Vendored Adobe Utopia map\n"
        + utopia_map.read_bytes().strip()
        + b"\n"
    )


def prepare_vendored_texmf(*, force: bool = False) -> Path | None:
    """Prepare and return a local TDS tree, or None when archives are absent."""
    ensure_tex_toolchain_on_path()
    if not archives_available():
        return None

    fingerprint = _fingerprint()
    if not force and MARKER.is_file():
        try:
            marker = json.loads(MARKER.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            marker = {}
        if marker.get("fingerprint") == fingerprint and TEXMF_ROOT.is_dir():
            _activate_texmf_paths(TEXMF_ROOT)
            return TEXMF_ROOT

    if CACHE_ROOT.exists():
        shutil.rmtree(CACHE_ROOT)
    TEXMF_ROOT.mkdir(parents=True, exist_ok=True)
    SOURCE_ROOT.mkdir(parents=True, exist_ok=True)

    psnfss_source = SOURCE_ROOT / "psnfss"
    with zipfile.ZipFile(PSNFSS_ZIP) as zf:
        zf.extractall(psnfss_source)

    freenfss = _find_one(psnfss_source, "freenfss.zip")
    if freenfss is not None:
        with zipfile.ZipFile(freenfss) as zf:
            zf.extractall(TEXMF_ROOT)

    with zipfile.ZipFile(UTOPIA_ZIP) as zf:
        for member in zf.namelist():
            if member.endswith("/"):
                continue
            name = Path(member).name
            suffix = Path(name).suffix.lower()
            if suffix == ".pfb":
                dest = TEXMF_ROOT / "fonts" / "type1" / "adobe" / "utopia" / name
            elif suffix == ".afm":
                dest = TEXMF_ROOT / "fonts" / "afm" / "adobe" / "utopia" / name
            elif name.startswith("LICENSE") or name.startswith("README"):
                dest = TEXMF_ROOT / "doc" / "fonts" / "utopia" / name
            else:
                continue
            dest.parent.mkdir(parents=True, exist_ok=True)
            with zf.open(member) as src, dest.open("wb") as dst:
                shutil.copyfileobj(src, dst)

    map_source = _find_one(psnfss_source, "utopia.map")
    enc_source = _find_one(psnfss_source, "8r.enc")
    if map_source is not None:
        map_target = TEXMF_ROOT / "fonts" / "map" / "dvips" / "psnfss" / "utopia.map"
        map_target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(map_source, map_target)
        _build_local_pdftex_map(TEXMF_ROOT, map_target)
    if enc_source is not None:
        enc_target = TEXMF_ROOT / "fonts" / "enc" / "dvips" / "base" / "8r.enc"
        enc_target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(enc_source, enc_target)

    generated_utopia_sty = _run_docstrip(psnfss_source, TEXMF_ROOT)
    generated_mathastext_sty = _extract_mathastext(TEXMF_ROOT)
    _activate_texmf_paths(TEXMF_ROOT)

    MARKER.parent.mkdir(parents=True, exist_ok=True)
    MARKER.write_text(
        json.dumps(
            {
                "fingerprint": fingerprint,
                "generated_utopia_sty": generated_utopia_sty,
                "generated_mathastext_sty": generated_mathastext_sty,
                "texmf_root": str(TEXMF_ROOT),
            },
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )
    return TEXMF_ROOT


def _kpsewhich_path(filename: str) -> str | None:
    executable = _find_executable("kpsewhich")
    if executable is None:
        return None
    proc = subprocess.run(
        [executable, filename],
        capture_output=True,
        text=True,
        check=False,
    )
    if proc.returncode != 0 or not proc.stdout.strip():
        return None
    return proc.stdout.strip()


def diagnostic_report() -> dict[str, object]:
    tools = ensure_tex_toolchain_on_path()
    marker: dict[str, object] = {}
    if MARKER.is_file():
        try:
            marker = json.loads(MARKER.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            marker = {"error": "Could not read prepared.json"}

    return {
        "tex_tools": tools,
        "candidate_tex_bin_dirs": [str(p) for p in _candidate_tex_bin_dirs()],
        "generated_utopia_sty": marker.get("generated_utopia_sty"),
        "generated_mathastext_sty": marker.get("generated_mathastext_sty"),
        "kpsewhich_utopia_sty": _kpsewhich_path("utopia.sty"),
        "kpsewhich_mathastext_sty": _kpsewhich_path("mathastext.sty"),
        "ready_for_matplotlib_usetex": bool(
            tools.get("latex")
            and tools.get("kpsewhich")
            and _kpsewhich_path("utopia.sty")
            and _kpsewhich_path("mathastext.sty")
        ),
    }


def main() -> None:
    info = inspect_archives()
    texmf = prepare_vendored_texmf(force=True)
    report = {
        **info,
        "prepared_texmf": str(texmf) if texmf else None,
        **diagnostic_report(),
    }
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
