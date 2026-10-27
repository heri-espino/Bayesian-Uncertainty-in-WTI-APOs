# Structural WTI Asian-option pricing and hedging — independent Paper B research plan

**Approved direction:** October 27, 2026. **Status:** proposal and data feasibility audit **not yet executed**. **Provisional target:** Journal of Commodity Markets, subject to sufficient independent new economic evidence, novelty and scientific soundness. Paper A (REMEF) is a separate Bayesian posterior-integration/volatility-input study. See [two-paper boundaries](../docs/two_paper_publication_strategy_2026-10-27.md).

## 1. Research question and required distinction

**Paper B question:** How accurately can the path-dependent WTI Average Price Option payoff be valued and risk-managed when the actual daily first-nearby CL fixing calendar, current CL futures term structure, and historically available market quotations are respected?

A genuine Paper B contribution is NOT merely adding more posterior draws, another prior, or a new reduced-form volatility forecast to Paper A's 189-date Databento conditional cross-sectional pricing comparison. Model error, futures curve, average fixings, independent target valuations, and hedging economics become the fundamental objects.

**Working hypotheses, not findings:**
- Path and fixing-calendar consistency changes pricing accuracy and risk sensitivities compared with terminal-average lognormal proxy valuations in predictable regimes.
- Forward-curve modeling and genuine futures-path uncertainty can matter more than posterior integration for pricing and hedging decisions.
- A robust method may improve out-of-sample hedge P&L or independently observed bid/ask price fit, after fair transaction costs. It may also **fail**; publication cannot depend on assuming success.

## 2. Correct payoff and what must be verified

For one observed AAO calendar-month schedule with N fixing days, at valuation date t let R(t) be days whose eligible first-nearby CL settlement is already known, and U(t) unobserved future fixing days. The terminal average payoff input is

A = (sum of observed first-nearby CL settlement fixes over R(t) + sum of future eligible CL settlement fixes over U(t)) / N.

A call pays max(A-K, 0) times the correct contract payoff multiplier; a put pays max(K-A,0) times the appropriate multiplier, subject to actual exchange cash-settlement/expiry conventions. The risk-neutral discounted expectation must respect timing, fixing progress, roll conventions and any payoff multiplier. This is a **schematic** mathematical identity, NOT yet a fully verified exchange contract specification.

**Verification blockers:** exchange/product code and security type; option expiry vs month of average; fixing day definitions and holidays; how first-nearby CL is selected near futures expiry; settlement observation reference and publication timestamps; adjustments/corrections; premium/price quote units, dollars per barrel and multipliers; handling of first/last fixing day and already fixed average. Record the original exchange document version and exact tested cases.

**Boundary:** Before any fixing has occurred (R empty), full average is stochastic. As fixing progresses, the observed component becomes deterministic; at complete fixing, the payoff is determined. The model must not pretend that the already observed portion remains volatile.

## 3. Data-feasibility inventory — NO PURCHASES UNTIL DECISION

### Available evidence, still requiring availability/path checks

- 81-month January 2020–September 2026 AAO option definitions/statistics in private Git LFS (162 compressed DBNs), original raw manifests/audit and derived full SQLite states. These are **AAO option** data; their existence does NOT establish availability of nearby CL underlying settlement **fixing paths**, a full futures curve, risk-free discount term structure, quotes or transaction data.
- Results of Experiments 003–005, including 111,585 Databento reduced-form contract-date target observations on 189 valuation dates, are prior *retrospective/conditional benchmark evidence*. The related 2025–2026 outcomes have been inspected, hence cannot become a magically untouched new test set.
- Older Barchart/LO data may exist in repo but must be audited for coverage, vendor rights, timestamps and possible duplication. No assumptions of permission to redistribute them.

### Inspect these fields, without provider API calls

| Source/instrument | What must exist | Essential check | Status |
| --- | --- | --- | --- |
| CL outright front/first-nearby daily settlements for every relevant fixing day | Exchange settlement, instrument ID, reference date, publication/ingestion timestamps | Exact nearby selection and roll calendar; missing fixings; corrections | **Unknown / audit** |
| Historical CL futures curve on every model valuation day | At least the contract tenors needed for future fixings, effective timestamps | Curve quote convention, seasonality, interpolation/extrapolation and stale tenors | **Unknown / audit** |
| AAO premiums and metadata | Symbol, strike, side, expiry/average month, quote type, mark/trade, flags, reference time, traded volume and OI where available | Actual vs theoretical CME settlement; premium quantity and option/underlying calendars | **AAO option observations exist; independence/quotes unverified** |
| Independent market target for validation | Real trades, bid/ask if available, multiple vendor agreement or clearly documented alternative independent target | Timestamp strictly later than inputs, liquidity, transaction costs and reliability | **Unknown / audit** |
| Risk-free/discount information | Dated curve or explicit audited constant-rate assumption | Match tenor, exact source availability by valuation time | **Not established** |
| Executable hedging instruments | Eligible CL futures, settlement/transaction history, sizes, margin/cost assumptions | Tradeability, rebalancing schedule, slippage/bid-ask, position/exposure mapping | **Unknown / audit** |

**First execution request:** create an inventory from only already-owned local metadata/manifests; do **not** query or spend with Databento or any other vendor. Present a missing-data matrix with date coverage and a quote-before-purchase option **only if needed**, separately requiring author's budget approval. Never assume existing AAO-OPT history includes CL futures.

## 4. Staged technical research program

### Stage 0 — enforce empirical separation

- Keep Paper A manuscript evidence and Experiments 003–005 frozen. Use a new named Paper B project/experiment directory, branch or PR with separate manifests, scripts, tests, figures, analyses and source provenance.
- Maintain an explicit [publication overlap ledger](../docs/two_paper_publication_strategy_2026-10-27.md), with shared market records, reused equations/methods and exact tables allowed only as disclosed prior-work baselines.
- Preserve every meaningful interim artifact (including failed data checks) in GitHub, not in temporary agent machines.

### Stage 1 — exchange contract and calendar reconstruction

- Write unit tests for fixing-month boundaries, expiry, holiday/skipped day, roll to next nearby, weekends, partial fixing and contract-price scaling.
- Validate at least several individual AAO months by manual exchange-document tracing, and reconcile the observed fixed sum against downloaded CL settlements. Record all disagreements, missing days and corrections.
- Deliver machine-readable verified contract specs, fixing-index table and auditable mapping for 2020–2026. Without verified CL historical settlements, stop here.

### Stage 2 — independent forward/rate and market target construction

- Reconstruct the CL futures curve as known on each valuation date; distinguish live available quotes and archive-end corrections. Use only contemporaneously available instruments known before the valuation decision.
- Construct a price-target panel separately for traded/bid-ask marks and theoretical exchange settlements. For an invalid or illiquid quoted target, record missingness instead of fabricating a price.
- Ensure the model does not calibrate to or use the evaluated target premium/same-contract implied volatility. Distinguish from the prior reduced-form experiments' same-date **disjoint option parity** anchors.

### Stage 3 — path-dependent model benchmarks, unit-tested

Implement the minimum meaningful set:
1. Independently specified discount and deterministic fixing offsets; a verified no-arbitrage one-factor conditional futures process driven by the dated CL futures curve.
2. A pathwise Monte Carlo price on the **actual remaining CL fixing times**, with independent reproducible seeds, correct contract multipliers, delta/sensitivity computation and confidence intervals.
3. Appropriate Curran-style approximation where model assumptions support it, plus numerical convergence and edge-case tests (zero remaining fixes, zero vol, all fixes remaining, strike extremes and deterministic forwards).
4. Conditional extensions only if the new economic question requires them: curve factors, stochastic vol/jumps or dynamic hedging. Show incremental value relative to simple models and quantify computation overhead.

Do not claim that an approximation exactly follows the exchange Curran settlement convention unless independently verified; do not claim another model is novel merely because it uses Monte Carlo or stochastic volatility.

### Stage 4 — distinct economic tests

- **Primary prospective evaluation, if data allow:** tradeable price/bid-ask alignment or hedge P&L/risk, after realistic trading costs and a chronological information cutoff, by expiry, fixing progress and maturity.
- Secondary: mark pricing, bias, liquidity/zero-volume splits, regime and calendar sensitivity, independent CL fixing curve input quality.
- Compare against parsimonious futures/Asian baselines **and** existing accepted literature implementations, not just our earlier historical Bayesian proxy.
- Date-block/expiry-aware uncertainty, numerical MC error separation, sensitivity and negative-results preservation. Specify economic materiality in actual contract dollars and ticks, not solely small statistically detectible differences.

### Stage 5 — reporting and editorial feasibility

- Draft primary Paper B only after a verified technical/empirical contribution emerges. At present [paper/jcm](../paper/jcm/README.md) builds older concise Paper A content; it is **NOT** this new paper.
- Independent abstract, title, claims, citations, visuals, supplemental material and tests. Refer/cite Paper A where applicable; no reused abstract, tables or figures presented as original new evidence.
- Inspect the official JCM guide, costs and data/code policies shortly before choosing it as a submission destination. REMEF submission of a genuinely distinct Paper A can be pending during the research, but do not submit substantially overlapping work simultaneously.

## 5. High-priority deliverables for the next agent / collaborator

1. **Metadata-only feasibility report**: enumerate local data roots, file types, contract symbology and date coverage, separately flag CL fixing/curve/AAO trades/rates missingness. Use repo files/live connected GitHub to inspect, but do not purchase or call providers without user authorization.
2. **Exchange spec and fixing calendar table**: exact month-by-month daily fixing identifiers, trade/reference dates, sources and case-by-case discrepancies; initially a research design, not presumed existing.
3. **Structural model spec and synthetic contract tests**, only once complete and reliable source fixings are established.
4. **Separate original research hypothesis** and analysis plan prioritizing independent price/hedge outcomes over reusing Paper A's PI−PM conclusions.
5. **Evidence audit** for new and shared figures, source versions, permissions, experimental timing, and whether prospective test days genuinely postdate prior inspection.

No local-data experiment has been performed in this document; no new price series, hedging P&L, or cost estimate has been fabricated. Do not modify Experiments 003–005 or launch GitHub Actions for heavy data processing.

## 6. Gate-based stop/go

**Go** only when exact fixing paths and contracts can be reconstructed, independently time-stamped forward/price targets are sufficiently observed, and an identifiable original research question can be fairly tested. **Narrow/reframe** if only official settlements but no independent trade evidence exist. **Stop/defer** if the necessary source coverage or licensing cannot be established; do not describe such cases as completed structural WTI Asian pricing.

**Connection back to Paper A:** finish the already developed REMEF Bayesian/volatility paper with scientific and editorial audits. No second paper is promised as a guaranteed consequence of purchasing or collecting more data.
