"""Validate the JFM review PDF and isolated figure bundle after local/runner builds.

Does not mutate files or call external services. Requires the existing asian-options
environment (pypdf, which is included in environment.yml).
"""
from __future__ import annotations

import json
from pathlib import Path

from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[1]
PDF = ROOT / "paper" / "espino_2026_bayess-on-wti.pdf"
STAGE = ROOT / "paper" / "build" / "stage"
ART = ROOT / "figures" / "jfm"
NAMES = (
    "fig01_mechanism_map",
    "fig02_historical_vs_apo_implied_volatility",
    "fig03_forward_q_cluster_bootstrap",
    "fig04_numerical_identification",
)
IDENTIFIERS = ("heriberto", "espino-montelongo", "heri-espino", "@udlap.mx")


def main() -> None:
    if not PDF.is_file() or PDF.stat().st_size < 5_000:
        raise SystemExit(f"Missing or suspiciously small Wiley PDF: {PDF}")
    if not STAGE.is_dir():
        raise SystemExit("Wiley staging directory is missing")
    if (STAGE / "jfm_title_page.tex").exists() or (STAGE / "main_short.tex").exists():
        raise SystemExit("Identifying or redundant JFM manuscript staged with the blinded source")
    staged_text = (STAGE / "main.tex").read_text(encoding="utf-8")
    if any(item in staged_text.lower() for item in IDENTIFIERS):
        raise SystemExit("Identifying author text was staged into the reviewer manuscript")

    manifest_file = ART / "figure_manifest.json"
    if not manifest_file.is_file():
        raise SystemExit("JFM figure manifest missing")
    manifest = json.loads(manifest_file.read_text(encoding="utf-8"))
    if manifest.get("journal_target") != "jfm":
        raise SystemExit("Wrong figure target: expected JFM-only outputs")
    publication = manifest.get("awesomefigures_publication")
    if not publication or manifest.get("font_mode") != "exact-tex-preamble":
        raise SystemExit("JFM figure manifest does not certify exact Wiley XeLaTeX typography")
    if publication.get("engine") != "xelatex" or not publication.get("all_passed"):
        raise SystemExit("JFM AwesomeFigures engine or font/size audit failed")
    if publication.get("exact_pdf_count") != len(NAMES):
        raise SystemExit("Expected exactly four audited XeLaTeX PDF figures")
    af_report = ART / "awesomefigures_manifest.json"
    if not af_report.is_file():
        raise SystemExit("AwesomeFigures manifest missing")
    audit = json.loads(af_report.read_text(encoding="utf-8"))
    if audit.get("all_passed") is not True:
        raise SystemExit("AwesomeFigures report contains failed publication audits")
    expected_width_pt = float(audit["layout"]["textwidth_pt"])
    if expected_width_pt <= 0:
        raise SystemExit("Invalid Wiley LaTeX textwidth")
    pdf_records = [record for record in audit["figures"] if record["format"] == "pdf"]
    if len(pdf_records) != len(NAMES):
        raise SystemExit("AwesomeFigures report is incomplete for JFM PDFs")
    for record in pdf_records:
        if record["typography"] != "exact-tex-preamble" or record["warnings"]:
            raise SystemExit(f"Figure has fallback fonts or audit warnings: {record['path']}")
        actual = record.get("actual_width_tex_pt")
        if actual is None or abs(float(actual) - expected_width_pt) > 0.75:
            raise SystemExit(f"Figure not at final Wiley textwidth: {record['path']}")
        fonts = record["pdf_fonts"]
        if not fonts or any(not item["embedded"] for item in fonts):
            raise SystemExit(f"Figure does not embed all TeX fonts: {record['path']}")
    for name in NAMES:
        for ext in ("pdf", "png", "svg", "pgf"):
            file = ART / f"{name}.{ext}"
            if not file.is_file() or file.stat().st_size == 0:
                raise SystemExit(f"Missing JFM figure: {file}")

    reader = PdfReader(str(PDF))
    text = "\n".join(page.extract_text() or "" for page in reader.pages)
    meta = " ".join(str(v) for v in (reader.metadata or {}).values())
    if len(reader.pages) < 2 or not text.strip():
        raise SystemExit("Could not extract text from compiled JFM review PDF")
    if any(item in (text + "\n" + meta).lower() for item in IDENTIFIERS):
        raise SystemExit("Author identifying information leaked into the reviewer PDF")
    print(f"PASS: {len(reader.pages)} PDF pages, anonymous visible text/metadata")
    print(f"PASS: {len(NAMES)} Wiley-width PGF/XeLaTeX PDF figures with embedded fonts and SVG/PNG previews")
    print("NOTE: this is a draft; manual visual/typographic inspection is still required")


if __name__ == "__main__":
    main()
