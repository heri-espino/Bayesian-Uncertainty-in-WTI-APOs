# REMEF submission candidate (separate from JFM)

The REMEF adaptation is based on the **concise** JFM research text, but it has its own
introduction, bilingual metadata and bibliography supplement. Nothing here replaces
`paper/manuscript/main.tex`, `paper/manuscript/main_short.tex`, or their Wiley builds.

## Editorial framing

**English title (9 words):** Posterior Integration and Volatility Inputs in WTI Asian Options

**Spanish title (8 words):** Integración posterior y volatilidad en opciones asiáticas WTI

Both abstracts are under 180 words and are arranged in REMEF's required order:
objective, method, results, recommendation, limitations, originality, conclusion.
The REMEF-specific introduction cites two relevant articles from the journal
(Matías González et al., 2019, and Ortiz Ramírez & Jiménez Preciado, 2026)
and Gilder & Tsiaras (2020). The final article is in the journal's
**January–March 2026** issue despite its initial online publication in 2025.

The REMEF version **does not claim** to discover that options predict realized
WTI volatility; Gilder & Tsiaras study that question. It evaluates APO
market-pricing errors and posterior integration under a maintained one-factor
futures pricing model.

## Author instructions checked 17 October 2026

- https://remef.org.mx/index.php/remef/directrices
- https://remef.org.mx/index.php/remef/about/submissions
- Word document, Times New Roman 12 pt, single line spacing,
  2.5 cm top/bottom and 3 cm left/right margins, numbered pages;
  **no more than 25 pages including all figures, tables, equations, references**.
- Title, abstract, keywords and JEL metadata in **English and Spanish**;
  titles at most ten words, abstracts at most 180 words.
- Word-editable equations and tables (not equation screenshots).
- Double-anonymous peer review; handle personal information and document
  metadata carefully. Journal also requests author details on the first page;
  clarify the appropriate file separation with the editorial office if needed.
- Disclosure of AI-assisted writing/editing in Methods, accurate to actual usage.
- Author-confirmed ORCID, contact, funding and signed originality/authorship
  documentation are required for submission.
- **No simultaneous submission** with JFM or any other journal.

## Build Word draft without rerunning experiments

Requires Python 3.11+, [Pandoc](https://pandoc.org/) and `python-docx`.
Install the latter in the project environment if needed:

```powershell
conda activate asian-options
python -m pip install python-docx
python paper/remef/build.py --check
python paper/remef/build.py
```

The default is a **blinded review draft** at
`paper/remef/build/remef_blinded_draft.docx`. Use
`python paper/remef/build.py --author-version` for a separate author draft
with author metadata placeholders to be completed. Generated drafts stay
ignored by Git.

The build reads the existing six-section concise research text (substituting
`paper/remef/introduction.tex` for its introduction), uses the REMEF front
matter and two additional references, converts equations to native Word math
via Pandoc, and styles native Word tables to 10 pt. Its two inserted publication
figures use the committed 600-dpi PNG outputs. This is **format conversion**,
not a new statistical estimation or independent experimental reproduction.

### Manual GitHub build

Run **Actions → build-remef → Run workflow**. The manual-only workflow
generates the blinded editable Word draft and an intermediate PDF for
page-count verification, then uploads the Word artifact (30-day retention).
No heavy inference or simulation is launched.

### Mandatory manual acceptance checks

1. Open the Word document and check that equations are genuinely editable,
   references/cross-references render meaningfully, and tables/figures fit.
2. Check the compiled page count (≤25), 300-dpi figure legibility, table
   numbering and attribution, JEL classifications, and consistency of
   English/Spanish summaries.
3. Convert the existing Markdown online supplement to a **clean submission
   supplement**; it currently includes archival material after S1–S4.
4. Confirm the editor's preference for blinded/unblinded metadata handling,
   author details, exact disclosures, and signed submission documents.
5. Resolve the vendor market-data redistribution question, including
   historical public Git versions. No automated script claims to solve it.
6. Complete the independent result-by-result audit in
   [PRESUBMISSION_AUDIT.md](PRESUBMISSION_AUDIT.md). Do not submit until
   the unresolved items are signed off.

The **JFM** source and the **REMEF** Word draft are alternative targets for
the **same paper**, not simultaneous submissions.
