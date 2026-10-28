# Literature and novelty matrix — REMEF Paper A

**Research snapshot:** 2026-10-27  

> **Full-text source review added (2026-10-27):** [Read the source-based comparison of Rombouts–Stentoft's supplied **2009 CIRANO working paper**, the **2014 journal abstract**, and Sagor–Boone–Ghanam's supplied **2026 full article**](SOURCE_REVIEW_ROMBOUTS_SAGOR_2026-10-27.md). Important: 2009 tests MNGARCH against GARCH, whereas 2014 explicitly tests Bayesian versus ML inference. Sagor's WTI **European call** is an illustrative hypothetical contract priced using historical returns, not an observed AAO settlement-mark sample. The 2014 full journal article has **not** been independently read; that literature gate remains open.
**Status:** substantive first-pass literature positioning; **not a systematic/exhaustive review**, no new empirical run, and no submission clearance.  
**Primary basis:** extracted academic articles under literature/extracted/ and their supplied Markdown copies, the existing REMEF manuscript and [evidence map](REVISED_MANUSCRIPT_EVIDENCE_MAP_2026-10-27.md), plus linked journal/publisher records. Source summaries refer to **specific published articles** when working-paper and final-publication versions differ.

## 1. The research question worth testing

> How much does integrating the posterior distribution of volatility into a conditional WTI average-price option value change the resulting **point price**, relative to changing the **information source** used to choose volatility? And, when strictly earlier implied volatility is available, does Bayesian smoothing/forecasting add demonstrable value over its persistence?

The study is **not** a new pricing formula for arithmetic-average options, an identification of the physical-to-risk-neutral variance premium, or a test of executable hedge profitability. Its possible originality is the **controlled, commodity-contract-specific measurement and careful separation** of (i) posterior integration versus plug-in pricing, (ii) historical versus option-implied volatility information, and (iii) posterior conditional-model-price spread versus observed settlement-mark forecast-error calibration.

**Status of originality:** potentially credible as a narrowly specified empirical comparison, **conditional on temporal/source audits and stronger positioning against prior empirical Bayesian option-pricing papers**. Do not say the question has never been studied or that a small PI–PM difference is a new universal discovery.

## 2. Direct comparison with closest research

| Source | What the source actually investigates or establishes | Material overlap with Paper A | What Paper A might add; caveat | Risk to novelty |
| --- | --- | --- | --- | --- |
| **Kemna & Vorst (1990)**, *Journal of Banking & Finance* | Pricing options on average asset values using Monte Carlo and variance-reduction ideas; crude oil already figures in the economic motivation. | Arithmetic-average payoff and computational methods. | The WTI contract is **not** a new exotic payoff. Our question is volatility-source versus posterior-integration effect. | Low, if cited as foundational. |
| **Curran (1994)**, *Management Science* | Efficient Asian/portfolio option valuation by conditioning on the geometric mean when the arithmetic average involves correlated lognormal components. | Numerical engine in the original Barchart/CL study. | Curran is a **benchmark method we employ**, not a novel method. Numerical-model error must be distinguished from volatility-source error. | Low as a method claim; high if we claim pricing-method novelty. |
| **Guidolin & Timmermann (2003)**, *Journal of Economic Dynamics and Control* | Bayesian learning within an equilibrium model, European S&P 500 option prices, implied-volatility skews and pricing/hedging forecasts. | Bayesian uncertainty can matter for pricing; Bayesian option pricing is well established. | Different payoff, underlying and source-of-information experiment. Contrasts must acknowledge their positive Bayesian evidence rather than assert Bayesian pricing is generally unhelpful. | **High** for general Bayesian novelty. |
| **Rombouts & Stentoft (2014)**, *Computational Statistics & Data Analysis* | Bayesian risk-neutral predictive option pricing under mixed-normal heteroskedasticity with S&P 500 options; **published abstract concludes parameter uncertainty has a minor impact** on option-pricing losses with abundant data. | **Very close to the claim that parameter uncertainty may have little effect on point pricing.** | The published finding **pre-empts any claim that small Bayesian integration effects are new in general**. Possible increment is quantifying PI vs PM *within a WTI arithmetic-average contract context*, alongside strictly lagged IV and settlement-mark information limitations. Must cite 2014 final version, not only a 2009 working paper. | **Critical**; central source for novelty test. |
| **Bakshi, Cao & Chen (1997)**, *Journal of Finance* | Empirically assess increasing complexity of equity option models with pricing, parameter consistency, and actual hedging metrics. | Strong precedent that extra option-model complexity requires economic justification. | We evaluate one particularly narrow Bayesian integration increment, **not** comparable stochastic jump-factor model classes or hedging. | High to any broad complexity claim. |
| **Dumas, Fleming & Whaley (1998)**, *Journal of Finance* | Empirical performance of fitted implied-volatility functions and out-of-sample pricing issues. | Lagged smile and persistence benchmarks are standard, not invented here. | WTI AAO and model-specific information timing; must be strict about no current-target leakage. | Medium/high. |
| **Gilder & Tsiaras (2020)**, *Journal of Futures Markets* | Compare option-implied measures for predicting **subsequent realized crude-oil return volatility**; corridor IV is a strong competitor. | Economic value of option-implied versus historical volatility information in oil is prior art. | Our measured loss is **WTI average-price option settlement-mark price error**, not later realized return variance. We do not identify a variance risk premium. | **High** to broad “implied beats historical in oil” novelty. |
| **Cummins & Esposito (2025)**, *Journal of Futures Markets* | Tests whether increased complexity in option models pays off using model confidence set comparisons across volatility/jump specifications. | “More complexity need not improve pricing” already established as an empirical research question. | A controlled Bayesian point-price integration increment and simple lagged-IV comparator on Asian options, not general model-complexity superiority. | High to general complexity claim. |
| **Matías González, Martínez-Palacios & Ortiz-Ramírez (2019)**, *REMEF* | Optimal consumption/investment theory, a floating/average-strike Asian put in a stochastic-volatility setting; also uses Monte Carlo for Asian/European comparisons. | REMEF **already publishes Asian-option studies** and Monte Carlo. | Different economic problem, underlying, contract and empirical estimand. Cite accurately; “Asian options have not been studied in REMEF” is false. | Medium. |
| **Ortiz Ramírez & Jiménez Preciado (2026 issue)**, *REMEF* | Realized volatility and mean reversion to simulate CEMEXCPO Asian options and compare against European option prices. Online publisher date **2025-12-23**; formally **Vol. 21(1), 2026**. | Asian-option volatility estimation and simulation; same journal. | We benchmark option-implied versus historical inputs for observed WTI AAO *marks* and the Bayesian integration increment. Theirs uses a different Mexican-equity-based design. | **High** for claims about REMEF-specific gaps; otherwise medium. |
| **Ewald, Wu & Zhang (2023)**, *Quantitative Finance* | Pricing Asian options with stochastic convenience yield and jumps for commodity applications. | Commodity-specific payoff pricing sophistication predates this paper. | Our maintained one-factor/constant-volatility approximation isolates **input choice**; do not claim structural realism or better commodity dynamics. | Medium. |
| **Sagor, Boone & Ghanam (2026)**, *Risks* | Joint Bayesian Hurst/volatility inference propagated to option-price posterior distributions with **WTI and natural-gas data**; illustrative **European fractional Black–Scholes** prices. | **Bayesian option-price uncertainty propagation using WTI data is already published.** | Our payoff is WTI arithmetic-average options and our empirical comparison is posterior point integration vs IV inputs and actual settlement-mark metrics, rather than joint fractional-model inference and European example prices. | **High** to “first Bayesian WTI uncertainty pricing” claim. |
| **Schwartz (1997)**, *Journal of Finance* | Commodity price dynamics, convenience yields and futures valuation/hedging implications. | First-nearby CL futures path and commodity term structures are nontrivial. | We hold a highly simplified dynamics fixed; cannot claim model-robust market efficiency or hedging conclusions. | Medium (model-validity risk). |

### Version hygiene — important factual correction

The supplied literature bundle includes an **Rombouts & Stentoft 2009 working-paper extraction**, whose abstract stresses improvements over benchmarks. The **final 2014 journal article** of the same title explicitly reports that the measured impact of parameter uncertainty is minor in its setting. These are **different claims / document versions**, not independent research replications. Cite and compare with the final **2014** article first; do not treat the 2009 and 2014 versions as two separate supportive studies.

Likewise, the supplied **Guidolin & Timmermann 2001** extraction is a discussion paper of an article ultimately published in **2003**; cite the 2003 journal paper. The Ortiz–Jiménez extracted PDF has a 2025 header; REMEF's official volume assignment is **2026**, notwithstanding early online publication.

## 3. The actual novelty boundary

### Previously known; explicitly concede

- Bayesian parameter/posterior uncertainty can affect option values and option-value distributions.
- With enough data, parameter uncertainty may have **small impact on prices** (Rombouts & Stentoft 2014 already shows a related empirical result).
- Second-order expansions, the delta method, and Jensen-type curvature logic are standard analytical tools.
- Bayesian option pricing, historical-versus-IV comparison, Asian arithmetic averages, Curran conditioning and “more complex is not always better” are established research themes.
- WTI-data Bayesian propagation of parameter uncertainty to **European-option** price distributions was studied in 2026.
- REMEF itself has published Asian-option papers.

### Candidate **specific** contribution, subject to evidence gates

1. **A joint decomposition in an average-price contract:** distinguish posterior-integrated minus posterior-mean **point prices**, conditional model-price posterior dispersion and volatility-source-induced differences. They are distinct estimands. The synthetic study illustrates where curvature/variance matters; it is not a new identity.
2. **Original WTI AAO empirical benchmark:** under one specified futures-based arithmetic-average valuation scheme, test whether lagged option-implied volatility dominates physical historical-return inference across *matched* APO contracts/dates, with independent valuation-date inference and an LO-derived signal check. Our older cohort has **2,381 rows but only 15 valuation dates**, and original smile prediction-row/timestamp audits remain unfinished.
3. **Separately identified, nonreplicated conditional evidence:** in the Databento **terminal-average lognormal and same-date other-strike parity** benchmark, compare lagged AAO-IV persistence with Bayesian innovations; the Bayesian approach has **no robust incremental improvement** on an already-inspected 2025–Sep 2026 split. This supports a modest practical recommendation about modeling increment, not risk-neutral structural accuracy or pure ex-ante forecasting.
4. **Clarify the limits of uncertainty calibration:** distinguish volatility-parameter pushforward credible bands from **settlement-mark residual prediction intervals**, which show substantial undercoverage in early 2026. Do not invent a cause or generalize beyond this conditional model.

This is an **empirical comparison / research-design contribution**, not a new algorithm or theoretical pricing model. The split into Paper A (the above) and separate structural/CL-hedging Paper B must remain intact.

## 4. Critical tests a referee could demand

| Referee objection | Source that makes it unavoidable | Audit or response | Current status |
| --- | --- | --- | --- |
| “Small impact of posterior uncertainty is already known.” | Rombouts & Stentoft (2014); Sagor et al. (2026) | Cite both; specify PI–PM *point estimate*, AAO payoff, fixed benchmark and source comparison; do **not** present this alone as novelty. | Literature issue **identified**, narrative remedy **drafted**, publication sufficiency **not yet proven**. |
| “Implied volatility matching model-generated settlements is unsurprising.” | CME Curran settlement model (Clearing Advisory 20-198); implied-volatility literature | Explicitly limit estimand to **settlement-mark replication** unless independent quote/trade data are verified; stratify by actual/theoretical/volume where available. | **Open**. |
| “The real sampling unit is valuation date.” | Original 15-date Barchart and 10-date LO observations | Paired date/month-block inference and robust sensitivity; do not use 2,381 strike-date rows as independent dates. | **Open**. |
| “Are all predictors actually known by the pricing cutoff?” | Previous-day IV source, Barchart Latest, same-day parity anchors, LO tree timestamps | Write field-level source and as-of ledger; label target-day conditioning separately from prior-day volatility forecasts. | **Open**. |
| “How do we know this isn't merely P-versus-Q mismatch?” | Gilder–Tsiaras (2020); option-pricing theory | Avoid identifying a variance risk premium; make it a conditional volatility-*signal suitability* comparison, not a general claim historical volatility fails. | Interpretive remedy identified; source-timing check **open**. |
| “Is the 2014 conclusion reproduced in your WTI test rather than assumed?” | Rombouts–Stentoft (2014) | Provide matched volatility posterior PI/PM point estimates and uncertainty bands; distinguish observed mark error from theoretical price posterior spread. | October 310-row arithmetic **checked**, full information-set audit **open**. |
| “Does adding a Bayes layer beat a strong naive IV baseline?” | Cummins–Esposito (2025); standard model evaluation | Report **Bayes market-IV versus unchanged lagged-IV null**, together with actual price difference, date/month uncertainty and inspected-test disclaimer. | Aggregate result **exists**; original-source validation **not complete**. |

### Decision after reviewing these sources

**Proceed with REMEF as a potential journal fit**, but use a restrained headline. The overlap with Rombouts–Stentoft (2014) and Sagor et al. (2026) rules out easy originality claims about Bayes or WTI alone. If the original 15-date same-day market/timestamp audit fails, either narrow the empirical claim or assess whether the distinct Databento conditional study independently supports a publishable contribution; do **not** combine incompatible engines to rescue sample size.

## 5. Two-paragraph contribution statement for the eventual paper

**Literature gap (provisional):** Existing work provides established numerical methods for arithmetic-average option valuation and Bayesian approaches for incorporating parameter uncertainty into option prices. Empirical option-pricing studies already find cases where parameter uncertainty or added model complexity delivers little improvement, while crude-oil studies show that market-implied volatility is informative about future underlying volatility. These results do not, by themselves, quantify on identical WTI average-price option targets how the conditional price adjustment from volatility-posterior integration compares with the adjustment from using earlier option-implied rather than historical volatility signals. A distinction is also needed between the posterior distribution of *conditional theoretical prices* and uncertainty intervals for errors relative to observed market settlement marks.

**What this study does (provisional):** We keep a specified WTI average-price option pricing approximation fixed and separate the posterior-integrated-minus-plug-in point-price difference from the change in pricing error associated with the volatility information source. A synthetic experiment characterizes the familiar price-curvature mechanism, and an original futures-based WTI AAO exercise evaluates posterior and earlier option-implied inputs on dated options, with a separate cross-instrument LO check. A larger **non-identical**, explicitly conditional Databento settlement-mark exercise tests whether modeling strictly lagged implied-volatility innovations in a Bayesian framework improves upon carrying forward the latest implied volatility; the observed improvement is not reliable in the inspected comparison. The resulting contribution is a qualified comparison of empirical signal value and Bayesian integration—not a new Bayesian pricing formula, proof of market tradability, or identification of a volatility-risk premium.

**Editorial qualifier:** The “identical target / admissible information set” language is a **design requirement**, not certified for the entire old sample yet. The paragraphs must be revised or narrowed if the outstanding timestamp, original IV-row, model-generated-mark and vendor-rights audits fail.

## 6. Specific manuscript changes suggested by this review (NOT implemented)

1. In **Introduction / literature**, cite and contrast *Rombouts & Stentoft (2014)* directly, rather than mentioning only general Bayesian learning. Present our small PI–PM result as **consistent with**, not contradictory to, that source.
2. Explicitly cite *Sagor, Boone & Ghanam (2026)* to avoid implying Bayesian WTI option-price uncertainty propagation is new; contrast their European fractional-model illustration with WTI AAO mark-error evaluation.
3. Add *Cummins & Esposito (2025)* and *Gilder & Tsiaras (2020)*, but distinguish model-complexity choice and realized-volatility forecasting from our conditional AAO mark-price errors.
4. Discuss the two REMEF precedents using their **actual** Asian payoff designs and empirical datasets; avoid claiming an unexplored journal topic.
5. State what is a **baseline**, **analytical identity**, **already-published finding**, **market result**, or **novel limited comparison** in the abstract and contribution paragraph.
6. Preserve the original-vs-Databento methodological divide; do not suggest the 189 Databento dates are direct independent replication of the original 15-date Curran study.

## 7. Source index and verification status

These links document which publication is actually being discussed. **Publisher abstracts/full available versions** were inspected for substantive claims; this is **not** a full line-by-line systematic literature review. Existing local PDFs/Markdown are extracted text and may reflect **earlier versions**.

- Kemna & Vorst (1990), DOI [10.1016/0378-4266(90)90039-5](https://doi.org/10.1016/0378-4266(90)90039-5).
- Curran (1994), DOI [10.1287/mnsc.40.12.1705](https://doi.org/10.1287/mnsc.40.12.1705).
- Guidolin & Timmermann (**published 2003**, draft 2001), DOI [10.1016/S0165-1889(01)00069-0](https://doi.org/10.1016/S0165-1889(01)00069-0).
- Rombouts & Stentoft (**published 2014**, manuscript 2009), DOI [10.1016/j.csda.2013.06.023](https://doi.org/10.1016/j.csda.2013.06.023).
- Bakshi, Cao & Chen (1997), DOI [10.1111/j.1540-6261.1997.tb02749.x](https://doi.org/10.1111/j.1540-6261.1997.tb02749.x).
- Dumas, Fleming & Whaley (1998), DOI [10.1111/0022-1082.00083](https://doi.org/10.1111/0022-1082.00083).
- Gilder & Tsiaras (2020), DOI [10.1002/fut.22114](https://doi.org/10.1002/fut.22114).
- Cummins & Esposito (2025), DOI [10.1002/fut.22575](https://doi.org/10.1002/fut.22575).
- Matías González, Martínez-Palacios & Ortiz-Ramírez (2019), DOI [10.21919/remef.v14i3.408](https://doi.org/10.21919/remef.v14i3.408).
- Ortiz Ramírez & Jiménez Preciado (2026 issue), DOI [10.21919/remef.v21i1.1470](https://doi.org/10.21919/remef.v21i1.1470).
- Ewald, Wu & Zhang (2023), DOI [10.1080/14697688.2022.2160799](https://doi.org/10.1080/14697688.2022.2160799).
- Schwartz (1997), DOI [10.1111/j.1540-6261.1997.tb02721.x](https://doi.org/10.1111/j.1540-6261.1997.tb02721.x).
- Sagor, Boone & Ghanam (**2026**, new close comparator), DOI [10.3390/risks14080173](https://doi.org/10.3390/risks14080173). July 24, 2026 journal article.
- CME Clearing Advisory 20-198, effective May 18, 2020: [official notice](https://www.cmegroup.com/notices/clearing/2020/05/Chadv20-198.pdf).
- [REMEF official author guidelines](https://remef.org.mx/index.php/remef/directrices): original scientific contribution; explicit literature, results/discussion and research methods; bilingual structured abstract and Word submission.

**Existing bibliography:** Most older articles have keys in paper/manuscript/references.bib; the two REMEF articles are in paper/remef/references.bib. **Sagor et al. 2026 has no checked-in BibTeX entry yet**; prepare the bibliography entry only once the authors approve inclusion in manuscript text. This Markdown file does not silently change the bibliography or TeX manuscript.

## 8. Follow-up tasks to finish Phase 1

- [x] Compile a direct, source-linked comparison focused on closest Bayesian/Asian/WTI/REMEF papers.
- [x] Identify and document the critical 2014 publication-versus-2009 working-paper distinction.
- [x] Find and describe a contemporaneous 2026 WTI Bayesian posterior option-pricing comparator.
- [x] Draft a restrained contribution and concrete manuscript edit instructions in Markdown.
- [ ] Review the complete final published Rombouts–Stentoft paper beyond its published abstract for the exact **definition** of uncertainty impact and empirical comparison; avoid inferring PI–PM equivalence from a Bayesian-vs-ML metric.
- [ ] Recheck recent 2023–2026 commodity Asian option and Bayesian market-IV papers for possible closer overlaps; this matrix is not exhaustive.
- [ ] Resolve outstanding original IV predictions, timing and mark-source audits before marking the **empirical originality claim** verified.
- [ ] Revise journal-specific TeX and APA references **only after** agreeing this scoped argument; do not edit original Wiley/JFM source.

**Gate state:** **Phase 1 draft complete; scientific originality not yet cleared**. Continue with the as-of/missing-row audit in the [publication plan](PUBLICATION_EXECUTION_PLAN.md).
