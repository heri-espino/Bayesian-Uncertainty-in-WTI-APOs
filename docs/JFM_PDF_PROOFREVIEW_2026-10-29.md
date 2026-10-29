# JFM PDF proof review — 29 October 2026

**Build verified; submission clearance OPEN.**

Successful PCAG103A-15 manual build #40955826056 at commit b3d59dac2795a3db975f1efbca6b95158a18da74. The supplied PDF matches the workflow artifact exactly: 10 pages, 137,670 bytes, SHA-256 e4a9fddf3294f8c780e969163ddf0a4093ec1dbec9c9086023b97c4a862b8cca.

All four standalone AwesomeFigures XeLaTeX PDF figures passed exact-font and width verification (actual 507.506 TeX pt, expected 507.508 TeX pt). The article itself embeds only two graphics: Figure 1 is the mechanism map, and Figure 2 is the cluster-bootstrap comparison. The other two generated figures are available but not included in the main text.

**10 million histories is correct** per results/analysis/massive_mechanism_map/6e23d5aabc519982/mechanism_map_report.json (synthetic_datasets=10000000, root_seed=2468). An older 175,000-history experiment is preserved in the supplement archive and must be distinguished.

## Must fix or verify before journal submission

1. **Page 1 production placeholders:** red Received/Revised/Accepted 'Added at production', DOI 'xxx/xxxx', and copyright-holder footer are still printed. Suppress in the review proof.
2. **Figure 1 readability:** dense rotated moneyness ticks and the near-zero inset in panel C. Inspect a true print-size copy; Figure 2 looks legible.
3. **Numerical coverage:** the 95%, 65%, and 32% synthetic nominal-interval coverage values are correctly labeled provisional. More complete 513-vs-1025-point posterior quantile convergence is missing; checked endpoints differed by up to $0.002281/bbl. Do not certify interval coverage at a $0.001 tolerance.
4. **Market provenance:** 2,319 of 2,381 original market comparison rows report zero volume (97.4%). The main comparison has only 15 valuation dates and external LO comparison 10. Vendor first-publication timestamps and actual settlement source have not been independently verified, so this is not an executable trading forecast.
5. **Potential circularity:** CME Clearing adopted Curran for WTI APO EOD settlement valuation effective May 18, 2020. A Curran-based method matching model-produced settlement marks may partly share the reference's assumptions. The LO check mitigates but does not eliminate this.
6. **Supplement:** S1-S4 currently reside in paper/supplement/online_supplement.md (which also embeds old archived LaTeX working material); prepare a separate polished supporting-information PDF.
7. **Editorial:** final originality/literature and data-licensing checks, separate identifying title page, complete LaTeX source+figure+BibTeX upload package, ORCID and signed author review. AI use is described in Methods and again in end matter.

## Normal Git storage (not LFS)

The existing paper/espino_2026_bayess-on-wti.pdf in main is an **older 226,005-byte ordinary Git blob**, not the reviewed 137,670-byte PDF. The .gitattributes LFS patterns cover data/ and selected vendor files, not paper/*.pdf. The path is also listed in .gitignore, so use manual git add -f to intentionally version the final reviewed manuscript after its corrections. Never auto-commit the expensive PDF/figure build from push-triggered CI.

Official Journal of Futures Markets author requirements: https://onlinelibrary.wiley.com/page/journal/10969934/homepage/forauthors.html . Free-format first submission; double-anonymized review; LaTeX main source + reviewer PDF + supporting source/figures; title page with author identity as separate upload.
