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
- [ ] **Numeric gate still open:** 513/1025 sigma grids differed by up to
  $0.002281/bbl in representative posterior interval endpoints; broader
  coverage-rate sensitivity is still unverified. The resulting 95%/65%/32%
  coverage values must be labeled illustrative/provisional, NOT exact
  coverage-calibration results.
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
- [ ] Complete portable **supplementary** files (not just a local Markdown
  planning document); verify table/figure citations and source completeness.
- [ ] Author review of originality, prior Asian/WTI and Bayesian literature,
  market-versus-model interpretation, permissions, all statistical numbers,
  compiled bibliography and final blinded/unblinded file separation.
- [ ] Verify external sources and DOIs; do not claim that generated PDF
  snapshots or a passing CI check establish editorial readiness.

## Current decision

The manuscript revision includes the bounded synthetic results as
**qualified illustrative evidence** with explicit numerical limits. It does
not relabel the study as preregistered or eliminate the outstanding
coverage-convergence requirement. The **technical PDF and figure build is verified** in run #40955826056,
but the print proof still has production placeholders and the scientific,
supplement, and source-verification gates remain open. Do not submit yet.

## 2026-10-29 follow-up: numerical gate and packaging

- [x] Repeated **all 1,440** synthetic price-state rows on four posterior grids (513, 1,025, 2,049, 4,097). Coverage classifications stable: 95.00% / 65.21% / 31.88% for rho 1/.75/.5, with no state flips. Endpoint changes up to $0.005227/bbl between 513 and 4,097; do not call this sub-cent endpoint precision or real-market calibration.
- [x] Versioned deterministic convergence script and lightweight aggregate CSV; manual-only runner replay available.
- [x] Prepared anonymized standalone S1--S6 TeX supplement, editor-only title page, and exact-source manuscript upload packaging in the **manual** build.
- [x] Suppressed unassigned NJDv5 production metadata in the review source; improved Figure 1 layout only for JFM.
- [ ] Rebuild the *new commit*, check that the production placeholders have disappeared, inspect the revised figures and support PDF, and archive signed-off normal-Git PDF.
- [ ] Original Barchart `Latest` values and release vintages have **not** been independently verified as final CME settlements. This research/data-provenance gate stays OPEN. See `research/JFM_NUMERICAL_AND_PRICE_PROVENANCE_2026-10-29.md`.
- [ ] Final author approval of AI declaration, claims, citations, data-licensing compliance and separate identifying metadata.
