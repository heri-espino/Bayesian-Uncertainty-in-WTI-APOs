# Paper A — REMEF final editorial and submission handoff

**Date:** 28 October 2026  
**Scope:** REMEF-specific scientific manuscript, not the existing Wiley/JFM source or proposed JCM Paper B.  
**Current status:** Scientific manuscript **source draft completed**. Final Word production, licensing and author approval **not certified**. No journal submission has occurred.

## Contribution and final claims

**Research question.** In WTI average-price option valuation, how much does averaging over a volatility posterior affect the **conditional point price**, relative to the observed pricing-error difference arising from volatility information sources? When earlier AAO implied volatility is available, does modeling its innovations with Bayesian updating improve upon carrying forward the last observation?

The paper reports a bounded *negative* result: in the tested models and samples, posterior integration modifies point prices relatively little; earlier AAO implied-volatility signals outperform the tested historical-volatility inputs against settlement proxies; and fitted-smile or Bayesian-IV elaboration does not reliably outperform the simple matched persistence control. These results do **not** constitute a new Asian option formula, a universal Bayesian-model ranking, a risk-premium measurement or a validated tradable prediction.

Closest references explicitly acknowledged include Curran (1994), Kemna and Vorst (1990), Guidolin and Timmermann (2003), Rombouts and Stentoft (2014), Sagor, Boone and Ghanam (2026), and previous Asian-option publications in REMEF. The Rombouts 2014 full-text article remains unreviewed; the 2009 CIRANO working paper and 2014 published abstract must not be conflated.

## Key numerical results (archived-output audit, not vendor-vintage certification)

| Distinct design | Defensible summary |
| --- | --- |
| Synthetic mechanism | Ten million return histories; mean PI−PM curvature/variance cell diagnostic correlation ~0.9995; descriptive, not a new theorem |
| Original October-**expiry** panel | 310 option-date rows / 12 August–September 2026 dates; mean absolute PI−PM USD 0.000745/bbl; mean 95% **conditional model-price posterior** interval width USD 0.2733/bbl (not market-error coverage) |
| Original Barchart/CL/Curran comparison | 2,381 contract-date observations over only **15 dates**: historical PI MAE 2.618699 versus earlier AAO-IV smile MAE 0.107546 USD/bbl; target-date CL curve and fixing information are conditioned upon |
| Same-contract persistence comparison | 2,366 common observations / **15 dates**: latest same-contract earlier IV carry MAE **0.099156** vs matched fitted smile **0.107417** USD/bbl; exact arithmetic, archived dates and all **4,762** fitted smile IV forecasts independently reconciled |
| LO cross-instrument comparison | 253 common target rows / **10 dates**: prior LO IV MAE 0.1559, prior AAO IV 0.1676 and historical PI 0.4464 USD/bbl; underlying source-vintage still open |
| Different Databento conditional terminal-average proxy | 97,341 actual-flagged targets / 189 dates; lagged AAO-IV MAE 0.218420 vs historical parity-forward proxy Bayesian PI 0.804044 USD/bbl, under contemporaneous other-strike parity anchors |
| Matched market-IV Bayes comparison | 47,718 actual-flagged targets / 88 inspected dates: lagged-IV MAE 0.208924 vs Bayesian IV PI 0.209830 USD/bbl; monthly-block interval for improvement includes zero |
| Predictive mark-error intervals | Inspected 2025–September 2026 nominal 90% coverage 86.43%; March/April 2026 coverage 59.0%/56.9%; a **different estimand** from posterior model-price width |

The Barchart `Time` field gives dates but **not** vendor release timestamps/vintage. The original 2,381-row comparison contains **2,319 rows with recorded zero volume**; settlement marks may be generated from exchange valuation methods. Therefore the paper deliberately makes **no** trade-level profitability, real-time executability, identified variance-risk-premium or prospective accuracy claims.

## Completed editorial actions

- Made the literature context explicit and limited novelty to the WTI contract-specific matched comparison. Added the Sagor et al. 2026 reference to the REMEF-specific bibliography.
- Removed misleading unqualified prediction language, while retaining verified *archived date-order* volatility comparisons.
- Distinguished model-price posterior width from observed mark-error calibration, which cannot be interchanged.
- Brought the online supplement in line with the completed numerical 2,381/2,366-source-row and 4,762-IV reconstruction audits.
- Reconciled the manual-only Word CI workflow with the revised manuscript's **five numbered captions and six editable Word tables**, and added a lightweight regression test.
- Kept the independent Wiley/JFM paper, JCM Paper B, source market files, experiments, and prior results unchanged.

## Required pre-submission checks — not claimed done

- [ ] On an authorized complete checkout, run:
      `python -m pytest tests/test_remef_build.py tests/test_remef_manuscript_scientific_integrity.py -q`,
      `python -m scripts.audit_remef_science`,
      `python -m scripts.audit_remef_forward_iv`,
      `python paper/remef/build.py --check`.
- [ ] Dispatch **manual-only** `build-remef` GitHub Actions workflow at the final commit. Download the blinded and author Word artifacts and the mathematical-content reference PDF.
- [ ] Review the actual Word files in Microsoft Word: 25-page maximum **including** bibliography and figures, Times New Roman 12 pt, single spacing, 2.5/3 cm margins, page numbers, bilingual structured abstracts/JEL, five numbered scientific sections, five numbered tables with six editable tabular blocks, native math, two figures, correct APA references, corresponding author footnote, and blinded metadata. LibreOffice and XeLaTeX PDF checks do not replace this inspection.
- [ ] Independently audit vendor data redistribution permissions, previously exposed public Git history, actual vendor first-publication timestamps, revisions and end-of-day mark status; if these records remain unavailable, **retain** all retrospective, settlement-mark and date-order qualifiers and ensure the editor understands the limits.
- [ ] Verify original CL/LO/rate source record vintages, any required end-to-end input-price replay, the full published Rombouts–Stentoft (2014) text if obtainable, and bibliographic/citation formatting.
- [ ] Author confirms final article text and correspondence, AI-use disclosure, contributor statements and original data limits; signs REMEF's required authorship/rights/originality declaration. Submission must be exclusive. Do not sign or submit without the author.

## REMEF requirements checked 2026-10-28

Official <https://remef.org.mx/index.php/remef/directrices> and <https://remef.org.mx/index.php/remef/codigo_etica> require an original research paper, no simultaneous submission, bilingual title/abstract/keywords and JEL terms, structured abstracts not exceeding **180 words**, up to **five keywords**, editable Word, Times New Roman 12 pt, single spacing, margins 2.5 cm top/bottom and 3 cm left/right, page numbers, a **maximum 25 pages**, double-blind handling, ORCID requirement and specific disclosure of any generative-AI assistance in Methods. The author must sign the journal's `Carta de Autoría, Cesión de Derechos y Declaración de Originalidad`.

**Boundary:** The above is a source-complete manuscript and actionable handoff, **not** a certificate of reproducibility, data rights, DOCX integrity or submitted/accepted status.
