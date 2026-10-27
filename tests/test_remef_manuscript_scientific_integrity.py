"""Lightweight scientific-integrity checks for the REMEF-only source.

These tests inspect claims/citations and do not reproduce vendor-data runs,
prove vintage validity, or certify journal acceptance/submission readiness.
"""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REMEF = ROOT / "paper" / "remef"
SOURCES = [
    REMEF / "frontmatter.tex",
    REMEF / "introduction.tex",
    *(REMEF / "sections" / n for n in (
        "02_posterior_pricing.tex",
        "03_data_design.tex",
        "04_results.tex",
        "05_robustness.tex",
        "06_conclusion.tex",
    )),
]


def manuscript() -> str:
    return "\n".join(f.read_text(encoding="utf-8") for f in SOURCES)


def test_all_citations_have_bib_entries():
    body = manuscript()
    refs = "\n".join(p.read_text(encoding="utf-8") for p in (
        ROOT / "paper/manuscript/references.bib", REMEF / "references.bib"))
    bibkeys = set(re.findall(r"@\w+\s*\{\s*([^,\s]+)", refs))
    cited = {
        key.strip()
        for m in re.finditer(
            r"\\cite(?:p|t|author|year|alt)?(?:\[[^\]]*\])?\{([^}]+)\}", body)
        for key in m.group(1).split(",")
    }
    assert cited, "No citations in REMEF body"
    assert cited <= bibkeys, f"Unresolved bibliography keys: {sorted(cited - bibkeys)}"


def test_references_labels_and_braces():
    body = manuscript()
    labels = re.findall(r"\\label\{([^}]+)\}", body)
    refs = re.findall(r"\\(?:eq)?ref\{([^}]+)\}", body)
    assert len(labels) == len(set(labels)), "Duplicate equation, figure or table labels"
    assert set(refs) <= set(labels), f"Unresolved labels: {sorted(set(refs)-set(labels))}"
    assert body.count("{") == body.count("}"), "Unbalanced TeX grouping braces"
    assert body.count(r"\begin{figure") == body.count(r"\end{figure")
    assert body.count(r"\begin{table") == body.count(r"\end{table")


def test_databento_and_original_cohorts_not_conflated():
    methods = (REMEF/"sections/03_data_design.tex").read_text(encoding="utf-8")
    results = (REMEF/"sections/04_results.tex").read_text(encoding="utf-8")
    limitations = (REMEF/"sections/05_robustness.tex").read_text(encoding="utf-8")
    combined = methods + results + limitations
    for expected in ("2,381", "15", "253", "10", "111,585", "97,341", "189"):
        assert expected in combined
    assert "same-date" in combined
    assert "parity" in combined
    assert "reduced-form" in combined
    assert "first-nearby" in combined
    assert "not" in limitations.lower()
    assert r"\label{tab:remef_databento}" in results
    assert r"\label{tab:remef_bayes_iv}" in results
    assert "0.2184" in results and "0.8040" in results
    assert "0.2089" in results and "0.2098" in results
    assert "59.0" in results and "56.9" in results


def test_october_contract_expiry_not_mislabeled_as_valuation_month():
    results = (REMEF/"sections/04_results.tex").read_text(encoding="utf-8")
    audit = (REMEF/"SCIENTIFIC_AUDIT_FINDINGS_2026-10-27.md").read_text(encoding="utf-8")
    assert "October-expiry" in results
    assert "August 25" in audit and "September 10" in audit
    assert "October-2026 sample contains" not in results


def test_no_cross_paper_cas_wiley_rewrites():
    build = (REMEF/"build.py").read_text(encoding="utf-8")
    assert 'REMEF_SECTIONS = HERE / "sections"' in build
    assert 'REMEF_SECTIONS / "04_results.tex"' in build
    assert "JCM" not in manuscript().split(r"\section{Conclusion}")[0].split(
        r"\section{Introduction}")[0], "JCM target must not be manuscript's subject"


def test_no_unverified_submission_ready_claim():
    docs = [
        REMEF/"SCIENTIFIC_AUDIT_FINDINGS_2026-10-27.md",
        REMEF/"REVISED_MANUSCRIPT_EVIDENCE_MAP_2026-10-27.md",
        REMEF/"PRESUBMISSION_AUDIT.md",
    ]
    for p in docs:
        assert p.exists(), str(p)
    assert "NOT CLEARED" in docs[0].read_text(encoding="utf-8")
