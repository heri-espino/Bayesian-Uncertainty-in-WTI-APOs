# REMEF presubmission evidence audit — 2026-10-17

This file records **checks actually performed** versus **checks still open**.
It is not a certificate that all original experiments were independently rerun.

## Result-to-source spot checks performed

| Reported claim | Located source in repository | Assessment |
| --- | --- | --- |
| Synthetic 175,000 histories | `results/analysis/massive_mechanism_map/200169bc7780a11d/mechanism_map_report.json` lists `synthetic_datasets: 175000` | Number corroborated; full experiment not rerun |
| Synthetic correlation approximately 0.9995 | `figures/publication/figure_manifest.json` reports 0.9995451248988855 | Rounded main-text claim agrees |
| 2,381 out-of-sample option-date observations | `results/analysis/wti_extended_forward/README.md` lists seven expiry counts totalling 2,381 | Claim corroborated by published derived report; raw panel not re-audited |
| Historical PI MAE 2.6187 and RMSE 3.4090 | Same extended-forward README pooled table | Matches main text |
| Prior-day APO-IV smile MAE 0.1075 and RMSE 0.1594 | Same extended-forward README pooled table | Matches main text |
| Figures 1 and 3 available for Word | `figures/publication/fig01_mechanism_map.png` and `fig03_forward_q_cluster_bootstrap.png`; plotting script saves PNG at 600 dpi | Files present; Word size/legibility must be inspected |
| 310 October APO contract-dates, PI--PM 0.000745, posterior interval 0.2733 | `paper/manuscript/sections_short/04_results.tex` and `paper/supplement/online_supplement.md` | Values appear consistently in authored text; independently verify from machine-readable source |
| 253 cross-instrument observations and LO IV MAE 0.1559 | Main short manuscript and supplement | Not independently recomputed in this audit |

## Literature and journal-source checks performed

- REMEF (Matías González, Martínez-Palacios & Ortiz-Ramírez, 2019),
  DOI `10.21919/remef.v14i3.408`: cross-checked with the extracted original
  under `literature/extracted/` and publisher PDF.
- REMEF (Ortiz Ramírez & Jiménez Preciado), DOI
  `10.21919/remef.v21i1.1470`: belongs to **Vol. 21 No. 1 (2026)** as the
  journal records, even though the extracted PDF displays a 2025 header and
  it first appeared online in 2025.
- Gilder & Tsiaras (2020), DOI `10.1002/fut.22114`: forecasts subsequent
  crude-oil *realized volatility*, not WTI APO settlement-price error.
- REMEF `directrices` and `about/submissions` consulted 2026-10-17;
  current 25-page, bilingual, Word-native requirements recorded in README.
- The JFM `references.bib` remains unchanged. New sources are held in
  `paper/remef/references.bib` and the REMEF-only introduction.

## Open scientific/data checks — blockers

- [ ] Independently recompute the October 310-observation PI--PM
      difference and central posterior-price interval width from versioned
      contract-date results and compare all four table numbers.
- [ ] Independently trace the LO common-support 253-row benchmark,
      external LO-tree settings, time cutoffs, and bootstrap differences.
- [ ] Reconstruct the 2,381-row forward panel and verify exact information
      sets for every earlier-date implied-volatility input.
- [ ] Review experiment manifests/hashes and confirm that results reported
      in the manuscript belong to the same coherent committed snapshot.
- [ ] Audit uncertainty quantification with only 15 valuation-date clusters;
      examine serial dependence and settlement-mark/zero-volume limitations.
- [ ] Check direct novelty against the closest prior work, especially the
      REMEF Asian-option papers and Gilder & Tsiaras, without claiming their
      research questions are identical.
- [ ] Verify data-vendor redistribution permissions for currently exposed
      Barchart market histories; note that removing working-tree files does
      **not** remove access through past public commits.

## Open production/editorial checks — blockers

- [ ] Run `python -m scripts.check_repo_structure`,
      `python paper/build.py --check`, tests, and the REMEF `--check`
      on an appropriately provisioned repository checkout.
- [ ] Produce blinded and author Word documents through the new builder,
      render each Word page and verify **≤25 pages**, native math/tables,
      complete bibliography, figure captions and styles.
- [ ] Verify bilingual titles/abstracts, final JEL codes, APA citation details.
- [ ] Prepare a clean, independently readable online supplement; current
      `online_supplement.md` retains legacy source archives.
- [x] Record author-confirmed spelling, academic email, ORCID, external-funding
      status (none) and conflicts of interest (none); include these declarations
      in the appropriate REMEF Word versions.
- [ ] Supply the REMEF-required institutional postal correspondence address
      and telephone; verify optional website/LinkedIn and final AI-use wording.
- [ ] Resolve dual-anonymity versus first-page author metadata with the editor.
- [ ] Sign the authorship/rights/originality form and make one exclusive
      submission (REMEF **or** JFM, not both).

**Status:** REMEF editorial adaptation initiated; **not submission-ready**.

## 2026-10-18 REMEF layout remediation

- [x] Corrected the scientific section sequence to REMEF's introduction,
      literature review, methodology, results/discussion and conclusions/
      recommendations pattern, with progressively numbered subsections.
- [x] Bundled the current official APA 7 CSL and configured Pandoc to apply
      it to all in-text citations and references.
- [x] Added a Word-level deterministic typography and caption/table cleanup;
      Word math objects and native Word tables are retained.
- [x] Added Python software/reproducibility text without inventing methods or
      numerical findings.
- [x] Added a clear comparison between the two REMEF studies, the crude-oil
      volatility-forecasting precedent and our APO pricing question.
- [x] Replaced the unfinished funding and COI placeholders with the author's
      explicit declarations: no external research funding; no conflicts.
- [x] A locally revised copy of the existing 12-page Word draft was rendered:
      equations appeared in the PDF; tables and references were visually
      inspected; the document remained 12 pages.
- [ ] Run the updated GitHub manual `build-remef` workflow on the merged
      commit and verify its **new** Word/PDF output, not the older artifact.
- [ ] Have the author check the edited Word file in Microsoft Word and supply
      complete private author/correspondence metadata to the editorial office.
- [ ] Confirm data-vendor redistribution rights, signed authorship/copyright
      declarations and scientific evidence audit; the author has now resolved
      the funding and conflict-of-interest declarations.

The supplied `jace,+F26+PLANTILLA.pdf` is a published REMEF article used as a
layout example; it is not a Word submission template and its publisher masthead,
DOI, issue data and acceptance dates must not be reproduced.

## 2026-10-18 author-identification update

- [x] Author spelling confirmed as **Heriberto Espino-Montelongo**.
- [x] Academic contact email confirmed: `heriberto.espinomo@udlap.mx`.
- [x] ORCID confirmed by the author: `0009-0009-1230-2931`.
- [x] Author supplied an academic website and LinkedIn handle; kept out
      of the blinded version and reserved for the author-identifying draft.
- [x] Author explicitly confirmed **no research funding** and **no conflicts
      of interest**; both declarations are included in both Word outputs.
- [x] REMEF first-page correspondence footnote now has the author-supplied
      institutional mailing address and telephone; verify generated Word layout.
- [ ] Build both outputs in the manual GitHub workflow, inspect the new author
      first page, footnote, blinded metadata and PDF math rendering.

## 2026-10-18 failed-build diagnosis and institutional contact

- [x] Identified exact failure in GitHub Actions run 39158592891:
      `ValueError: Expected REMEF paragraph not found: 1 Introduction`.
      Pandoc-generated DOCX contains unnumbered section titles, and the
      postprocessor erroneously expected pre-numbered titles.
- [x] Updated the postprocessor's source-heading mapping and added a
      reproducible Word fixture to the unit tests to check the full
      REMEF section conversion (not just its Python source).
- [x] Added the author-confirmed campus address
      (Ex Hacienda Santa Catarina Mártir s/n, San Andrés Cholula,
      Puebla, C.P. 72810, México) and institutional telephone
      (+52 222 810 1202) to the *author-identifying version only*.
- [ ] After merge, manually rerun `build-remef`, verify both Word files,
      the corresponding-author footnote, blind metadata, equations,
      citation style, and the 25-page limit. Do not infer success from
      source compilation or lightweight CI alone.

## 2026-10-18 REMEF math-preview remediation

- [x] Inspected failed run 39161447621: blinded and author DOCX generated, editable math and table QA passed; LibreOffice PDF missing equations.
- [x] Independently typeset the same blinded Word artifact using Pandoc and XeLaTeX; mathematical content rendered successfully in the local 10-page reference PDF.
- [x] Revised the manual-only workflow to retain both DOCX files, discard the broken LibreOffice preview, check its page count only, and upload a **separately labeled math-content reference PDF** with actual equations.
- [x] Replace the brittle literal-sigma grep with mathematical-symbol extraction after NFKC normalization; require sigma, mu, scientific methods text and native OOXML math.
- [x] Pin Ubuntu 24.04 and update Node.js 24-compatible checkout/setup-python/upload-artifact actions. Neither warning was the build error.
- [ ] Execute the updated manual workflow on merged `main`; examine both DOCX outputs in Microsoft Word (including their math), preview figures, page count, references and blinding.
- [ ] Finish scientific-data and rights audit, supplement and journal-signed forms before submission.
