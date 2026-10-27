# REMEF submission candidate (separate from JFM)

> **PRIORITIZED PUBLICATION PLAN (2026-10-27):** Read [PUBLICATION_EXECUTION_PLAN.md](PUBLICATION_EXECUTION_PLAN.md) first for novelty, data-as-of, paired robustness, literature, writing and REMEF submission gates. This is a task plan, not permission to submit; scientific and data-rights blockers remain open.

> **2026-10-27 SCIENTIFIC MANUSCRIPT REVISED ON A DEDICATED BRANCH:** The paper now has REMEF-only body sections at [sections/](sections/), an integrated but **strictly separate** older Barchart/LO and newer Databento experimental discussion, updated bilingual abstracts and conclusions, corrected October-**expiry** timing, and stronger settlement-model/data-vintage cautions. The separate Wiley/JFM scientific source is unchanged. The REMEF Word builder now reads these journal-only sections. See [claim-level evidence map and remaining submission gates](REVISED_MANUSCRIPT_EVIDENCE_MAP_2026-10-27.md) and [independent source-output audit](SCIENTIFIC_AUDIT_FINDINGS_2026-10-27.md). **This is a complete revised scientific draft, NOT certified submission-ready:** vendor original-file/timing audits, rights checks, Word rendering/page count and author-signed forms remain outstanding. Nothing has been submitted. The older October 25 single-paper journal-ranking text below is historical.

**Build and verify this revised REMEF-only Word manuscript on a complete private checkout:**

```powershell
python -m pytest tests/test_remef_build.py -q
python paper/remef/build.py --check
python paper/remef/build.py
python paper/remef/build.py --author-version
```

The resulting **blinded** and **author-identifying** Word drafts are under paper/remef/build/ and must be visually inspected in Microsoft Word. All figures/Word equations must remain native and editable, both drafts must satisfy the <=25-page journal rule, the reviewer file must not reveal identifying metadata, and no GitHub Actions or experimental reruns are required merely to build the paper.

> **2026-10-27 numerical audit update:** [Independent audit](SCIENTIFIC_AUDIT_FINDINGS_2026-10-27.md) verifies older REMEF core 310-row, 2,381-row historical PI, and 253-row LO prices from source contract-level outputs; confirms 10M report metadata. **Scientific and editorial submission gates remain OPEN.** This is not approval to submit. Run new read-only source arithmetic checker locally with python -m scripts.audit_remef_science (not an expensive simulation).

> **PAPER A TRACK — 2026-10-27:** The author chose to prioritize completion of the existing Bayesian posterior-integration and volatility-information manuscript for a possible **REMEF** submission, independently of a separate NEW structural WTI AAO pricing/hedging project that might later target JCM. See [two-paper boundaries](../../docs/two_paper_publication_strategy_2026-10-27.md) and [REMEF scientific revision/submission gate](SCIENTIFIC_REVISION_AND_SUBMISSION_GATE_2026-10-27.md). The manuscript is **NOT submission-ready** and no submission has occurred. Earlier statements below that JCM might be the first journal for this **same** manuscript are now historical and superseded. The completed Experiments 003–005 must be reconciled with the older Barchart/LO/Curran manuscript before inserting results; their conditional terminal-average reduced-form assumptions are distinct. No automatic edits to manuscript sources, experiments or figures have been made by this strategy update.

The REMEF adaptation is based on the **concise** JFM research text, but it has its own
introduction, bilingual metadata and bibliography supplement. Nothing here replaces
`paper/manuscript/main.tex`, `paper/manuscript/main_short.tex`, or their Wiley builds.

## Expanded historical AAO acquisition — paper numbers unchanged

As of 25 October 2026 the author's VM reported **160 downloaded Databento
`AAO.OPT` definition/statistics chunks for 80 eligible months in 2020–2026**,
with USD 17.33487324 *quoted*, not verified actual billing. The original
[expansion plan](../../research/DATABENTO_AAO_EXPANSION_PLAN.md) is retained
for provenance; current operational checkpoint is
[October 25](../../research/CHECKPOINT_2026-10-25_AAO_EXPANSION.md).
Historical settlement identity, final-vs-theoretical marks, valid distinct
forward dates, Barchart reconciliation and new model results are **not yet
verified**. Do not replace REMEF tables or conclusions with assumed new
results. The 10-million-path synthetic experiment also stays unchanged.

**Conditional editorial decision:** review *Journal of Commodity Markets* as
the potentially stronger subject-fit submission **only after** actual improved
empirical work passes the gates in [journal strategy](../../docs/journal_strategy.md).
The existing REMEF Word manuscript remains the ready fallback, and Wiley/JFM
manuscripts remain separate alternatives. No simultaneous submissions.

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

## REMEF-specific reviewer-safe supplement (2026-10-27)

A **separate, internally consistent** [online supplement working draft](ONLINE_SUPPLEMENT_DRAFT.md) has been prepared for Paper A. It records the theoretical PI–PM distinction, the original Barchart/LO evidence, the *separate* Databento Experiments 003–005 and limits on conditional mark comparisons without recycling the legacy heterogeneous archived supplement. It contains no protected market-data rows or author-identifying links. **The journal's acceptance of separate supplementary material has not been verified**, so this is an optional editorial working document, not guaranteed submission content. The supplement currently exists as Markdown; convert and inspect it alongside the Word manuscript only after the editor's current instructions are checked. The source audit, independent input-vintage checks, data rights and release gates remain open.

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
with the verified author identity, academic email, ORCID, optional
professional links and a corresponding-author footnote. **The institutional postal address and telephone are now supplied by the author**. Generated drafts stay ignored by Git.

The build reads the existing six-section concise research text (substituting
`paper/remef/introduction.tex` for its introduction), uses the REMEF front
matter and two additional references, converts equations to native Word math
via Pandoc, and styles native Word tables to 10 pt. Its two inserted publication
figures use native SVG created from the committed vector PDF outputs. This is **format conversion**,
not a new statistical estimation or independent experimental reproduction.

### Manual GitHub build

Run **Actions → build-remef → Run workflow**. The manual-only workflow
generates **both** the blinded and author-identifying Word drafts and an intermediate PDF for
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

## REMEF section and formatting compliance pass — 2026-10-18

The reviewer manuscript is now rebuilt through an explicit **APA 7 CSL** style
(`paper/remef/apa.csl`) and a reproducible **Word postprocessing step**
(`paper/remef/postprocess.py`). It retains the original scientific core and
moves its sections into the structure REMEF requests:

1. Introduction
2. Literature review (including both REMEF Asian-option precedents and Gilder–Tsiaras)
3. Methodology (Bayesian inference, synthetic design, empirical data, software,
   reproducibility and AI assistance)
4. Results and discussion (including robustness and limitations)
5. Conclusions and recommendations

The numbered headings are styled consistently in black Times New Roman 12 pt,
with editable native Word math and tables, 10-pt table text, sources below
figures/tables, 2.5-cm vertical margins, 3-cm horizontal margins and page
numbers. JEL classifications are explicitly labelled in both languages.

A supplied published REMEF article provided a **typographic reference**, not an
editable Word template. Do not copy its publisher-only logos, issue masthead,
acceptance dates or DOI into a new submission.

The manual workflow now checks the required headings, APA bibliography, editable
math/table structures and presence of Greek equations in the rendered PDF. It
**does not certify scientific validity or legal data-sharing permission**.
A previously generated 12-page Word draft was visually inspected in this
conversation. The updated workflow must still be run and its **new** PDF inspected.

### Items that cannot be made compliant without the author

- **Confirmed:** campus correspondence address and telephone are in the
  author-identifying first-page footnote, never in the blinded version
- **Confirmed:** no external research funding and no conflicts of interest;
  both versions include these author-confirmed declarations
- Signed authorship, originality and rights-transfer documentation
- Data redistribution permissions and an approved anonymized data/code access route
- Final empirical result-level audit, supplement packaging and editorial approval

Accordingly, the Word output is an **editorial review draft, not an assertion
that all REMEF submission checks have been satisfied**.

## Confirmed author information — 2026-10-18

- Author name: **Heriberto Espino-Montelongo** (author-confirmed spelling)
- Affiliation: Universidad de las Américas Puebla, Mexico
- Corresponding email: **heriberto.espinomo@udlap.mx**
- ORCID: https://orcid.org/0009-0009-1230-2931
- Personal website: https://heri-espino.github.io
- LinkedIn: `in/heri-espino` (expanded to conventional LinkedIn URL in the author version; verify link before upload)
- Funding: **This research received no external funding.**
- Conflicts: **The author declares no conflicts of interest.**

The personal website and LinkedIn are optional editorial contact information,
not scientific references. Neither they nor the name, email, or ORCID appear
in the blinded Word manuscript. They are included only in the author-identifying
version. Campus postal address and phone are now supplied for the first-page
correspondence footnote; the generated author version still requires review.

## REMEF correspondence and build regression — 2026-10-18

- Postal address supplied by the author: **Ex Hacienda Santa Catarina Mártir s/n,
  San Andrés Cholula, Puebla, C.P. 72810, México**.
- Institutional telephone: **+52 222 810 1202**.
- Corresponding email remains **heriberto.espinomo@udlap.mx**.
- Only the unblinded author version contains those identifying contact details.
- GitHub Actions run [39158592891](https://github.com/heri-espino/Bayesian-Uncertainty-in-WTI-APOs/actions/runs/39158592891)
  failed because Pandoc's Word headings were **unnumbered** while the REMEF
  postprocessor assumed numbered headings. The converter now maps the actual
  Pandoc headings explicitly, with a lightweight regression test that runs
  postprocessing on a Word fixture before merge. The manual Word workflow
  must be rerun on the repaired revision and both resulting files inspected.

## PDF math and GitHub Actions build — 2026-10-18

The original `build-remef` run 39161447621 produced both native Word drafts, 44 editable Word math elements, four tables and two images. Its final PDF-preview step failed because LibreOffice 24.2 dropped native Word OMML equations. The faulty LibreOffice PDF must never be submitted as a mathematical manuscript.

The manual-only build now uses LibreOffice **only for approximate pagination** (discarding that incomplete PDF), and runs `pandoc <blinded.docx> --pdf-engine=xelatex` to generate `remef_math_reference.pdf` from the **same Word document**. That separate reference displays equations, but its typesetting and pagination differ from Word. It is not a substitute for opening the native DOCX in Microsoft Word and inspecting every page. A local test on the failed build's actual blinded DOCX produced a 10-page XeLaTeX reference with visible math, versus the incomplete 12-page LibreOffice PDF. The workflow independently enforces the 25-page limit in both outputs and checks Greek math after Unicode normalization.

GitHub actions now use Node24-compatible checkout v5, setup-python v6 and upload-artifact v6, and the workflow pins Ubuntu 24.04. These address the Node.js warning and runner-image notice, which did not cause the math failure. This workflow remains exclusively `workflow_dispatch`; scientific experiments are never started by paper edits. Rerun the manual workflow after merge and inspect its new artifact.

## Word appearance benchmark — 2026-10-18

Use `remef_math_reference.pdf` (the Pandoc/XeLaTeX mathematical-content
reference built from the blinded DOCX) as the **visual benchmark** for the
mathematical manuscript, not as the file to upload to REMEF. The two Word
documents remain the required editable submission files.

The Word postprocessor aligns the English and Spanish article titles to the
left, as in that PDF, and adds real consecutively updating PAGE fields in the
centered footer. REMEF's Times New Roman 12-pt font, single spacing, 2.5/3-cm
margins, and native editable OMML equations take precedence over exact PDF
page breaks; therefore the Word draft has approximately 12 pages while
the independent XeLaTeX math reference has 10.

The original GitHub runner (LibreOffice 24.2) omitted native Word equations in
PDF exports. In a later local review, LibreOffice 25.2 rendered most equations
but truncated one long conditional-expectation formula. These are
**LibreOffice compatibility limitations**, and neither preview proves perfect
Microsoft Word math display. Before submission, open the actual DOCX in
Microsoft Word and compare every formula, especially the risk-neutral call
valuation, against the math-reference PDF. Do not replace editable equations
with screenshots or distribute the broken LibreOffice PDF.


## Vector figures in Word (2026-10-19)

The reviewed REMEF Word build **does not insert flattened PNG figures**.
The plotting script preserves publication-quality PDF exports for all four
figures. At manual build time, `paper/remef/build.py` converts each committed
vector PDF to a native SVG via Inkscape, removes inherited PDF metadata,
and inserts the SVG into the Pandoc Word source. Word's DrawingML
`asvg:svgBlip` uses the native SVG; a PNG fallback may exist solely for
older Office compatibility. The artwork is not flattened to PNG.

Figure 3's previously cropped main title is replaced in the SVG with a clean
centered vector heading. Its source plotting script also uses an in-bounds
suptitle position for any future plot regeneration. Numerical panels and
scientific statistics are not changed.

Run `python paper/remef/build.py` with `pandoc`, `inkscape`,
`rsvg-convert` (librsvg2-bin on Ubuntu), and `python-docx` installed.
The manual-only `build-remef` workflow verifies that at least two SVGs
are embedded as native Word SVG elements, that math is editable, and that
the blinded SVG assets do not contain author-identifying metadata.
The workflow uploads four SVG exports alongside both Word documents and
the clearly labeled mathematical-reference PDF. Do not submit the reference
PDF as a publisher-perfect Word export. Inspect the DOCX in Microsoft Word.
