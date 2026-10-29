# JFM numerical convergence and price-provenance audit — 2026-10-29

## Numeric grid audit — executed

The pilot-informed independent-seed study's **original 1,440 rows** were
reconstructed from the archived random seed `20261219`, model, strikes,
reference prices, and Gaussian sufficient statistics. Reconstructed
513-point PI, PM, and both posterior interval endpoints matched the
archived values in every row (absolute tolerance `5e-10` USD/bbl).

Full population of 160 independent histories (3 strikes and 3 correlation
references per history), checked with 513/1,025/2,049/4,097 sigma nodes:

| Nodes | Coverage rho=1.00 | Coverage rho=.75 | Coverage rho=.50 | Classification changes from 4,097 |
|---:|---:|---:|---:|---:|
| 513 | 95.00% | 65.21% | 31.88% | 0 of 1,440 |
| 1,025 | 95.00% | 65.21% | 31.88% | 0 of 1,440 |
| 2,049 | 95.00% | 65.21% | 31.88% | 0 of 1,440 |
| 4,097 | 95.00% | 65.21% | 31.88% | reference |

Maximum absolute price-interval endpoint differences relative to the
4,097-point grid were 0.0052267151 (513), 0.0012146445 (1,025),
and 0.0002745385 (2,049) USD/bbl. Maximum PI change 513-to-4,097
was about 4.5e-9 USD/bbl; maximum PM change was ~5.56e-5.
The interval *binary coverage classifications* are stable **for the
tested synthetic states**. This is not a proof of posterior-quantile
accuracy below USD 0.001/bbl; it is not frequentist price coverage for
exchange settlements or other real-market observations.

Reproduction: `python -m experiments.jfm_grid_sensitivity` inside
`asian-options`, using already archived JFM follow-up data. No new
payoff Monte Carlo or large histories are required. Light summary
versioned at `results/analysis/jfm_grid_sensitivity/summary.csv`.
Separate manual-only runner workflow
`.github/workflows/jfm-grid-sensitivity.yml` uploads its output
without committing artifacts.

## Market-price evidence — limit of what can be verified

- The manuscript's Barchart `Latest` values have been treated as
  **settlement-price proxies**. A source field label is not proof that
  these rows were official **final** CME settlements or independently
  verified executed trades. The vendor's first publication timestamps
  and historical revision vintages have **not** been independently
  verified against the exact studied records.
- The date-ordered study uses 2,381 contract-date rows over only 15
  evaluation dates; 2,319/2,381 (97.4%) show zero daily volume.
  Cross-instrument LO check is 253 states over 10 dates. Valuation-date
  cluster resampling does not turn those into independent trading dates.
- **CME Clearing Advisory 20-198 (2020-05-15)** explicitly states
  it switched WTI Average Price Option (AAO) end-of-day valuation to
  Curran from 2020-05-18, so the use of Curran against a mark potentially
  produced by Curran is *not an independent pricing method test*.
  Source: https://www.cmegroup.com/notices/clearing/2020/05/Chadv20-198.pdf
- Barchart publicly markets settlement-based futures-options EOD data
  and implied volatilities, but that generic vendor documentation does
  **not** establish the actual extraction time and finality of the
  specific archives used in this study.
  Source: https://www.barchart.com/solutions/services/futures-options

**Status: cannot close official-settlement / first-publication-vintage
verification without original source provenance or exchange historical
reconciliation at the record level.** Do not invent a verification.

## Submission and editorial controls

JFM requires double-anonymized review, a separate identifying title
page, Main Document LaTeX source plus PDF for review, necessary LaTeX
supplementary files, and separate supporting information. It offers
free-format initial submission and expects data citation/sharing and
detailed disclosure of LLM use in Methods.

Current source: https://onlinelibrary.wiley.com/page/journal/10969934/homepage/ForAuthors.html

Separate `paper/supplement/jfm_supporting_information.tex` now
provides a self-contained S1--S6 supplement without uploading the
old archived long-form working LaTeX draft. Original
`paper/supplement/online_supplement.md` is retained as an audit source.

The author must inspect the updated Wiley PDF and standalone extra
files produced by a fresh manual workflow. Until then the artifact
build and typography are **not verified at the new commit**, regardless
of the older successful run.

**Decision:** numeric *classification* stability gate passed;
market provenance/settlement identification and new compiled proof
remain open. No substantive claims of market coverage or independent
settlement valuation have been added.
