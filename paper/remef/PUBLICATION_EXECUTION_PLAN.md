# REMEF publication execution plan — Paper A

> **Phase 2 progress (2026-10-27):** [Original 2,381/2,366 IV recalculation and 4,762 fitted-forecast reconstruction PASS](IV_NUMERICAL_AND_ASOF_AUDIT_2026-10-27.md). An independent date-field audit also passes. **Source-vendor as-of timestamps and first-release historical snapshots CANNOT be certified from the date-only Barchart records**; thus Phase 2 remains **PARTIAL / BLOCKED** for stronger fully ex-ante forecasting claims. The simpler lagged contract-IV persistence beats the fitted smile on matched MAE; retain this negative model-complexity result.


**Created:** 2026-10-27  
**Status:** ACTION PLAN ONLY — no new analysis has been run or validated by this document; the manuscript is NOT submission-ready.  
**Target:** *Revista Mexicana de Economía y Finanzas* (REMEF), original research article.  
**Active manuscript:** draft PR #115, `paper/remef-scientific-completion-20261027`; base branch `results/aao-databento-pilot-2023h1-20261026`. Do **not** merge or submit without the author's authorization.

This is the executable priority order for getting **Paper A** into a form suitable for REMEF editorial consideration. It complements—not supersedes—the existing [scientific revision gate](SCIENTIFIC_REVISION_AND_SUBMISSION_GATE_2026-10-27.md), [numerical audit](SCIENTIFIC_AUDIT_FINDINGS_2026-10-27.md), [claim-to-evidence map](REVISED_MANUSCRIPT_EVIDENCE_MAP_2026-10-27.md), [presubmission audit](PRESUBMISSION_AUDIT.md), [two-paper strategy](../../docs/two_paper_publication_strategy_2026-10-27.md), and [supplement](ONLINE_SUPPLEMENT_DRAFT.md). Keep the Wiley/JFM version unchanged and the new structural CL pricing/hedging **Paper B** separate.

## 0. Thesis, claims and boundaries (freeze before more modeling)

**Research question.** For WTI average-price options, under clearly specified conditional pricing models and information sets, how large is the effect of posterior-integrating volatility uncertainty on the *point price*, relative to the effect of choosing the volatility information source? Does a Bayesian forecast of lagged market-implied volatility improve on unchanged lagged IV?

**Preferred defensible thesis (conditional, not universal):** In the tested WTI AAO valuation settings, volatility information source is much more consequential for observed settlement-mark pricing errors than posterior integration of volatility into a conditional price; a more elaborate Bayesian lagged-IV forecast has no demonstrated gain over IV persistence. Posterior *conditional-model-price dispersion* and future *market-mark forecast-error calibration* are different uncertainty objects.

**Do not claim:** new mathematics in the second-order Taylor expansion; an identified `P` versus `Q` variance risk premium; accurate prediction of independently executed trades; reliable hedging P&L; structural validation of the terminal-average Black approximation; causal explanation of the March–April 2026 calibration breakdown; an untouched confirmatory 2025–26 test set; or that Paper A and Paper B provide independent replications when they reuse marks.

**Core numerical evidence already reported (not all raw-input audited):**
- Synthetic study: 10 million simulated histories; PI–PM curvature-variance correlation ~0.9995 at the reported cell level. This illustrates the **mechanism**, not theoretical novelty.
- Original first-nearby/CL/Curran **October 2026 expiry**: 310 contract-date rows on 12 **August–September 2026 valuation dates**, mean `|PI-PM|` USD 0.000745/bbl; 95% conditional-model-price posterior interval mean width USD 0.2733/bbl. These two quantities are not interchangeable.
- Original Barchart/LO panel: 2,381 rows on **15 dates**; historical PI MAE USD 2.6187/bbl and prior AAO-IV smile MAE USD 0.1075/bbl. External LO common-support check: 253 rows on **10 dates**.
- Separate Databento reduced-form study: 97,341 actual-flagged marks on 189 dates; historical parity-forward proxy PI MAE USD 0.8040/bbl versus lagged AAO IV USD 0.2184/bbl. The model uses **same-date other-strike put-call parity** to infer expected terminal average/discount: this is *conditional settlement-mark pricing*, not a fully ex-ante CL fixing-path forecast.
- Separate Bayesian-market-IV holdout (already inspected): 47,718 marks on 88 dates, Bayesian IV PI MAE ~0.20983/bbl versus lagged unchanged IV ~0.20892; matched month-block CI for improvement crosses zero.
- Separate mark-error interval calibration: nominal 90% Bayesian residual intervals covered 59.0% / 56.9% in March / April 2026. Neither implies a validated structural payoff interval nor identifies the cause.

**Acceptable scholarly outcome:** a precise, well-powered *negative* comparison with reproducible caveats; not a forced positive Bayesian finding.

## 1. Literature and contribution positioning — P0

**Action**
1. Create an evidence-backed novelty matrix: `research/experiments/experiment006/literature_novelty_matrix.md` **only if a new experiment006 research cycle is initiated**; otherwise use `paper/remef/LITERATURE_NOVELTY_MATRIX.md`. For each closest study, record its observable, `P/Q` interpretation, model, baseline, validation type, and exactly what Paper A adds.
2. At minimum check Curran (1994), Kemna–Vorst (1990), Guidolin–Timmermann (Bayesian learning and option prices), Rombouts–Stentoft (Bayesian option valuation), REMEF Matías González et al. (2019), REMEF Ortiz Ramírez–Jiménez Preciado (online 2025 / issue 2026), and crude-oil option-IV studies such as Gilder–Tsiaras (2020). Check later model-complexity and empirical option-pricing comparisons in the existing library.
3. Write a two-paragraph contribution statement with **one empirical gap** and **one empirical finding**. Cite closest predecessors in Introduction *and* Results/Discussion, not just a bibliography dump.
4. Present Taylor/delta-method equations as known analytical explanations; use simulation to establish **quantitative parameter regions**, not a theorem claim.
5. Rewrite the title/abstract once the contribution wording is settled. Provisional title (nine words): **Volatility Information versus Posterior Integration in WTI Asian Options**.

**Pass:** a referee can answer “What do we learn beyond established Asian-option approximation and Bayesian pricing literature?” in two sentences, with explicit comparison references. **Fail/response:** narrow the claim, not artificially embellish it.

## 2. Audit remaining evidence and information timing — P0; hard stop for full empirical claims

**Action**
1. Independently reaggregate both missing original row-level results: 2,381-row prior-day AAO-IV smile (MAE/RMSE and paired errors) and 2,366-row same-contract lagged IV. Preserve input paths, row keys, scripts, hashes, exact run commit, and discrepancy ledger.
2. Build an **as-of information matrix** for each model and cohort: target valuation and settlement publication timestamp; previous-option-IV source publication; first-nearby CL fixing calendar and last-trade/roll rules; CL curve `Latest` field; LO American option settlement/tree calibration; discount source; parity strikes; vendor historical revision vintage. Distinguish a **same-day conditional repricing** from a **pre-close/prior-day forecast**. Never represent data available after the pricing decision as a past feature.
3. Inspect the meaning and origin of Barchart `Latest`; Databento actual/theoretical flags, final/initial publication and positive-volume/open-interest subsets. CME's Curran-based exchange clearing mark means even “actual” settlement flags do not automatically establish independently traded quotes.
4. Verify original source-data and LFS/object hashes, any `git_dirty=true` experiment state, source licensing/public Git history exposure, and reproducible dependency/seed/environment configurations. **Do not** download paid vendor data, change sparse checkout, or erase/rewrite source files as part of this plan.
5. Re-run only lightweight row-metric audits before contemplating an expensive replay. Log discrepancies and why each affects a claim.

**Pass:** every central paper table can be recomputed from retained contract-level records and linked to an admissible prior-date information set; data usage/publication rights are cleared or a legally compliant derived-data alternative is approved. **Fail/response:** remove the affected claim or restrict to honestly conditional/reduced-form mark comparisons. Do not “fix” missing provenance by untraceable substitution.

**Existing completed portion:** original 310/2,381 historical PI/253 LO row arithmetic and synthetic run metadata are already checked; do not rerun them merely for appearance of progress.

## 3. Minimal decisive robustness/falsification — P1; do not conduct a model zoo

**Predeclare contrasts and run only if required source records already exist and pass Phase 2.** If this is a genuinely new sequential experiment, assign `experiment006` (do not overwrite Experiments 003–005); write a protocol before execution and preserve all successes and failures.

Required contrasts:
1. **Matched estimand and support:** within each pricing engine, compare PI vs PM for the *same volatility posterior*, contracts, curves, price function, discount, maturity, and observation dates. Separately compare historical volatility vs **strictly lagged IV** on identical targets. Do not attribute changes in engine or same-day parity inputs to Bayes itself.
2. **Simple strong baselines:** same-contract IV persistence; prior-day smile; historical rolling/EWMA/GARCH; Bayes lagged-IV PI vs its own PM; if already supported, a parsimonious lagged-IV drift/mean baseline. Report failure to improve.
3. **Conditional-information falsification:** in the Databento proxy, test stability under parity-anchor selection, option sides/moneyness and maturity strata, and any allowable as-of/anchor exclusions. State clearly when contemporaneous anchors make pure forecasting claims impossible.
4. **Market-quality sensitivity:** separately report actual/theoretical flags, positive-volume and/or open-interest availability, and maturity/date groups. If no independent quote/trade series is licensed and available, **stop** at mark-replication language; do not postpone Paper A indefinitely to acquire structural Paper B inputs.
5. **Date-appropriate inference:** for paired model errors define `d_t = mean_{i on date t}(|e_{i,baseline}| - |e_{i,candidate}|)`. Estimate the date-average `mean_t(d_t)` and a date/month-block uncertainty interval; compare with contract-weighted MAE transparently. Check sensitivity to serial dependence and only 15 original dates / 10 LO dates, and avoid treating strikes as independent replicates. Report MAE, RMSE, signed bias, coverage/interval score when applicable, and price-improvement magnitude versus USD 0.01/bbl standard quote tick (without treating a tick as universal trading-cost bound).
6. **No post-hoc “out-of-sample” label:** 2025–Sep 2026 has already been inspected. Report exploratory analyses as such; if future genuinely unseen observations are later used, lock the protocol and analysis code first. Do not manufacture a new confirmatory split within an already-used interval.

**Decision:** If the large historical-vs-implied mark-error gap survives time-vintage, matched-sample and market-quality checks, retain it as a **conditional empirical ranking**. If it collapses, make the narrower but potentially publishable PI–PM/complexity null the main result, with transparent limitations; re-evaluate scientific sufficiency before submission rather than forcing the original headline.

## 4. Reconstruct the paper around one argument — P1

Suggested REMEF structure (edit ONLY `paper/remef/`; preserve `paper/manuscript/`):
1. **Introduction:** economic decision question, why Bayesian integration might matter, result in plain terms, explicit conditional scope and contributions.
2. **Literature / closest studies:** Asian option computation (Curran); Bayesian predictive pricing (Guidolin–Timmermann, Rombouts–Stentoft); crude oil market IV / complexity; closest REMEF work. Matrix-backed differentiation.
3. **Methods:** define `P` inference versus `Q` conditional pricing; PI, PM, posterior price SD, and distinct market-mark residual intervals. Explain original first-nearby futures-based Asian payoff and separate terminal-average Black/parity conditional model. Include timing/audit table.
4. **Results and discussion:** (i) transparent small PI–PM point correction plus wider conditional model price posterior distribution; (ii) strict matched historical vs lagged-IV ranking in older CL/Curran sample; (iii) cross-instrument LO check; (iv) separately labelled Databento conditional evidence + null Bayes-IV-vs-persistence; (v) mark-error residual undercoverage only if it advances the argument.
5. **Limitations and conclusions:** distinguish model marks vs executable prices, 15/10 original dates, same-day parity anchors, data-rights/reproducibility, and no demonstrated price/hedge gains.

**Writing rules:** use common finance vocabulary; avoid repeated defensive paragraphs and overlong multi-number abstracts; explain why negative findings matter; display tables showing *independent valuation dates* alongside contracts; do not conflate PI-PM, posterior price widths and market residual coverage. Keep each original and Databento table labelled with engine, target definition, timing and number of dates. Remove secondary exploratory tables to the supplement if the journal permits it. Have one non-author critically read the draft for clarity and falsifiability.

**Pass:** title, abstract, introduction, tables and conclusion make the *same bounded statement*; every number appears in the evidence map; no ungrounded structural/trading claim.

## 5. Journal specification and production gate — P0 before upload

**Official sources reviewed 2026-10-27:** [REMEF author guidelines](https://remef.org.mx/index.php/remef/directrices), [submission checklist](https://remef.org.mx/index.php/remef/about/submissions), [editorial policies](https://remef.org.mx/index.php/remef/politica). The dedicated `/directrices` page is the primary current source when older submission pages differ.

- Research article; <=25 pages **including references, equations, tables and figures**; Word with Times New Roman 12 pt, single-spaced, vertical 2.5 cm and horizontal 3 cm margins, numbered pages.
- English **and** Spanish title (<=10 words each), abstract (<=180 words each, prescribed order: objective / methods / results / recommendations / limitations / originality / conclusions), up to five keywords per language, six JEL codes. The current 2026 guidelines explicitly require ORCID.
- Word-native editable equation objects and tables; figures readable, with correct captions, sources and appropriate 300-dpi raster where applicable. APA author-year references, correct numbering, figure references and complete methods/software disclosures.
- Double-blind review **versus** guideline requiring identifying author footnotes on first page: keep *separate blinded and author-identified Word files*; confirm with editorial office/portal which file belongs in reviewer manuscript and which as metadata/title page. Inspect document properties, alt text, figures, tracked changes, citations, supplement filenames and embedded metadata for identity leakage.
- Explicitly disclose actual AI-tool uses in Methods, consistent with REMEF/COPE policy. Confirm all coauthors/contributors, author order and ownership, funding/no-funding, conflicts/no-conflicts and data access. Obtain the signed **Carta de Autoría, Cesión de Derechos y Declaración de Originalidad**; no simultaneous submission of essentially the same manuscript to JFM/JCM.
- Resolve vendor redistribution and whether a separate supplement is permitted before attaching datasets or `ONLINE_SUPPLEMENT_DRAFT.md`. Public repository availability does *not* imply a right to redistribute licensed raw prices.
- Check final bilingual content and inspect **both native Word documents in Microsoft Word page by page**, especially OMML equations (LibreOffice PDF export may lose or truncate them), figures, bibliography, total page count and blinded status.

**Local non-heavy checks** (from a safe, full checkout with dependencies):
```powershell
python -m scripts.audit_remef_science
python -m pytest tests/test_remef_build.py tests/test_remef_manuscript_scientific_integrity.py -q
python -m scripts.check_repo_structure
python paper/build.py --check
python paper/remef/build.py --check
python paper/remef/build.py
python paper/remef/build.py --author-version
```
Do not auto-run GitHub Actions or paid computations. Heavy builds may use existing **manual-only** workflow with explicit user authorization. Generated submission artifacts need a documented safe storage route (do not commit restricted raw inputs or secrets).

## 6. Independent referee simulation, final decision and submission — P0

Conduct one internal **hostile referee review** before upload. Ask:
- Are the marginal Bayesian point-price effects already explained by Jensen/Taylor? Exactly what is new empirically?
- Does lagged option-IV outperform because exchange theoretical marks mechanically reflect similar models?
- Are comparable MAEs based on identical contracts, dates, price functions and as-of information?
- Is `P`-return volatility being compared to a `Q`-consistent model input without overinterpreting the gap?
- How many genuinely independent **dates** are there; do dependence-robust uncertainty intervals support claims?
- Are legal access, time vintages, blinding, literature and manuscript metadata verified?

Resolve every **fatal** objection in `PRESUBMISSION_AUDIT.md` with a link to evidence; nonfatal limitations can be transparently stated. Have the author personally sign off final results and representations.

**GO:** all fatal scientific/rights/timing claims validated (or removed), clear bounded novelty, reviewer-readable narrative, journal compliance confirmed, author explicitly approves the exact blinded/identified manuscript and any supplement.

**NO-GO:** unverified temporal leakage, materially irreproducible key errors, prohibited market-data redistribution, or claims of executable trade accuracy based only on model-generated settlement marks. Do not submit to meet an arbitrary date.

**Submission:** upload the approved Word files and required documents only through REMEF's official portal; log manuscript ID, journal correspondence, exact source commit, checksum of sent artifacts and submission date in a private appropriate repository record **without sharing credentials or personal secrets**. Track reviewer requests as a new sequential revision log and respond point-by-point with code/results provenance. Publication and acceptance are editorial decisions, never guaranteed by a completed plan.

## Work order / critical path

| Order | Deliverable | Priority | Pass criterion |
| --- | --- | --- | --- |
| 1 | Novelty matrix and 2-paragraph contribution | P0 | Specific empirical gap relative to named predecessors |
| 2 | Missing 2,381/2,366 row audit and as-of matrix | P0 | Claims reproducible with dates/timestamps |
| 3 | Market-mark, vendor license, LFS/source audit | P0 | No false independence or public-rights assumption |
| 4 | **Only targeted** paired robustness/falsification | P1 | Date/month-block results and simple baselines, no leakage |
| 5 | Focused paper rewrite / evidence map refresh | P1 | One coherent bounded thesis; all tables sourced |
| 6 | Independent reviewer-style critique | P0 | No unresolved fatal scientific objections |
| 7 | Native REMEF Word, anonymity, rights/form check | P0 | Journal-compliant and fully inspected |
| 8 | Author-approved exclusive REMEF submission | P0 | Exact final artifacts approved; portal receipt recorded |

**Scope budget:** preferentially reuse existing saved experiments, figures, code and market inputs. No additional MCMC variants, additional data purchase, GPU-scale reruns or structural CL-hedging work unless a documented falsification gap makes them indispensable for **Paper A**.

## Handoff and repository integrity

All new work must be committed and pushed in the appropriate review branch. Every new experiment gets the next sequential identifier (currently proposed `experiment006`, **verify against existing repository before creating**) and includes protocol, reproducible script, inputs and provenance, raw/processed results where licensed, metrics, failures, interpretation and next step. Read `AGENTS.md`, `research/AI_HANDOFF.md`, the evidence map and current branch state before changing code; preserve the manuscript sources, old results, data and logs. Use Git LFS only with verified remote persistence and lawful access. Never merge draft PR #115 without express authorization.
