# JFM pre-submission scientific, figure and editorial audit — 2026-10-29

**Status: NOT SUBMISSION-READY.** This checklist applies only to canonical
`paper/manuscript/main_short.tex` (Paper A); the historical full Wiley draft,
REMEF version and proposed JCM Paper B are separate. No simultaneous submission
of overlapping versions.

## Evidence and scientific claims

- [x] Prior main experiment: 10 million simulated return histories; PI--PM
  mechanism and numerical validation previously reported.
- [x] Date-ordered APO comparison: 2,381 option-date rows on **15 valuation
  dates**; `Latest` vendor field is a settlement-price *proxy*, not verified
  trade or official final exchange settlement.
- [x] Cross-instrument comparison: 253 October APO contract-date rows on 10 dates.
- [x] Pilot artifacts: successful Windows runner #40822904143 archived in
  `results/analysis/jfm_oracle_pilot/recovered_original_pilot_20261029.zip`.
- [x] Independent payoff QMC reference and pilot-informed, independent-seed
  bounded follow-up: scripts and outputs in `experiments/jfm_*.py` and
  `results/analysis/jfm_confirmatory/`. Repeated strikes and rho references
  are **not** independent historical replications.
- [x] Concise manuscript table and uncertainty caveats: method, results,
  robustness and conclusion now separate PI--PM disagreement from known-sigma
  pricing error and dependence misspecification.
- [x] **Bounded numerical coverage-frequency sensitivity complete:** full
  160-history, three-strike, three-rho replay at 513/1025/2049/4097
  posterior nodes gives unchanged 456/313/153 covered of 480 per rho.
  Full rows and SHA-256 manifest are versioned under
  `results/analysis/jfm_confirmatory/grid_coverage_*`; this does NOT
  establish exchange-price or real-market coverage.
- [ ] **Numerical absolute-price precision remains qualified:**
  513-vs-4097 interval endpoints differ by up to $0.005227/bbl and the
  4097-point result is not an exact continuous-grid proof. One rho=0.75
  value lies near its independent QMC reference-uncertainty boundary.
- [ ] The $0.001/bbl tolerance is too fine to claim exact-payoff validation:
  maximum observed one-factor Curran bias $0.000922/bbl, QMC reference
  halfwidth $0.000154/bbl. No precision claims below validated resolution.
- [ ] Earlier vendor release timestamps and revision vintages remain
  unverified; 2,319 of 2,381 original market comparison rows report zero
  volume. Do not call this independently executable forward pricing.
- [x] CME Clearing Advisory #20-198 (May 15, 2020) confirms the Curran model
  for **WTI AAO end-of-day settlement valuation** effective May 18, 2020:
  https://www.cmegroup.com/notices/clearing/2020/05/Chadv20-198.pdf
  Consequently, Curran-model agreement with settlement marks may be
  mechanical; include this benchmark-dependence caveat and citation.
- [ ] Review data licensing and public derived output rights with the author.

## Figures and compiled PDF

- [x] JFM branch isolates assets under `figures/jfm/` and uses pinned
  AwesomeFigures `af.paper` with staged Wiley LaTeX, measured `\textwidth`,
  XeLaTeX PGF PDF, and strict embedded-font validation. REMEF unchanged.
- [x] Recent manual `PCAG103A-15` build runs 40858842086,
  40858843594 and 40858844835: Conda, MiKTeX and pinned AF installation
  succeed, **figure rendering fails** because PGF refers to
  `fig01_mechanism_map-img0.png` outside the TeX working directory.
- [x] Versioned JFM-only adapter now extends the exact AF compilation
  preamble with a `\graphicspath` for adjacent PGF image sidecars; AF
  continues to own PDF/embedding/width audits. It does not substitute fonts.
- [x] **Manual build succeeded**, run #40955826056, commit
  `b3d59dac2795a3db975f1efbca6b95158a18da74`, on PCAG103A-15
  in `asian-options`. Outputs remain in a GitHub Actions artifact, not
  auto-committed.
- [x] Confirmed compilation, four PGF/TeX PDF figures, all four SVG/PNG
  previews, metadata manifest and anonymous reviewer PDF in the uploaded artifact.
- [x] Independently rendered all ten PDF pages; no apparent clipping,
  and manuscript figures/tables legible. Still needs proof refinement:
  page 1 production placeholders; page 6 dense Figure 1 labels/inset.
  Detailed proof notes: `docs/JFM_PDF_PROOFREVIEW_2026-10-29.md`.
- [x] Confirmed exact font embedding and matching Wiley width using
  successful runner verifier plus independent artifact and PDF review.
  The review PDF is metadata-blinded (blank Author/Title fields).
- [ ] Commit final inspected artifacts to `figures/jfm/` and snapshot PDF
  only after manual verification (do not auto-commit generated files).

## Current Journal of Futures Markets requirements

Official author instructions:
https://onlinelibrary.wiley.com/page/journal/10969934/homepage/forauthors.html

- [x] Research Article, **free-format** initial submission allowed. Exact
  two-column NJDv5 layout is a quality preference, not a required pre-review
  formatting condition.
- [x] **Double-anonymized** review: main source/PDF excludes author identity;
  separate `paper/manuscript/jfm_title_page.tex` identifies the author.
- [x] Abstract, keywords, plain-language summary, AI-assisted preparation,
  disclosures, and separate author-title metadata are present in sources.
- [x] AI use is described in the Methods and disclosure sections; the author
  must verify the accuracy and completeness of the description before upload.
- [ ] At upload select "Main Document - LaTeX .text File" and also provide
  "Main Document - LaTeX PDF" for review; supply all needed classes,
  bibliography, figures and inputs as "LaTeX Supplementary File".
- [ ] Ensure funding, acknowledgments, data availability and conflict
  declarations comply with *current* journal-specific placement requirements,
  including title page and system fields.
- [ ] Submitting author's ORCID; check all editorial metadata and rights.
- [x] Standalone anonymized supporting-information LaTeX source
  `paper/supplement/jfm_supporting_information.tex` contains S1--S5;
  `paper/build_jfm_addenda.py` builds its PDF and the distinct identifying
  title-page PDF in the manual Wiley workflow.
- [ ] Inspect the *newly compiled* addenda PDFs, check title-page declarations
  and supply the correct files under their submission-system designations.
- [ ] Author review of originality, prior Asian/WTI and Bayesian literature,
  market-versus-model interpretation, permissions, all statistical numbers,
  compiled bibliography and final blinded/unblinded file separation.
- [ ] Verify external sources and DOIs; do not claim that generated PDF
  snapshots or a passing CI check establish editorial readiness.

## Current decision

The manuscript reports bounded synthetic evidence with explicit
numerical limits. The full fixed-history posterior grid sensitivity now
establishes **stability of coverage classifications**, not actual market
calibration. The study remains pilot-informed, not preregistered. The
Barchart AAO price-vintage/settlement provenance gate remains OPEN;
see `research/JFM_WTI_APO_PRICE_PROVENANCE_2026-10-29.md`. The **technical PDF and figure build is verified** in run #40955826056,
but the print proof still has production placeholders and the scientific,
supplement, and source-verification gates remain open. Do not submit yet.
