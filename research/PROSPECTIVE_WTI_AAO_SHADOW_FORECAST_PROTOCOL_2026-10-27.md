# Preregistered design: prospective, time-stamped WTI AAO shadow forecasts

**Protocol drafted:** 2026-10-27 (no live data acquired, forecast issued, or outcome observed).  
**Research stream:** REMEF Paper A follow-up; compatible with Paper A but **not** a retroactive fix to the August–September 2026 data vintages.  
**Current state:** **DESIGN/PRE-REGISTRATION ONLY; NOT AN EXECUTED EXPERIMENT**. No initial forecasts exist. No API keys, licensed purchases, automated scraping, source copying, or GitHub Actions jobs authorized.  
**Related audits:** [original 2,381/2,366 row check](../paper/remef/IV_NUMERICAL_AND_ASOF_AUDIT_2026-10-27.md), [REMEF execution plan](../paper/remef/PUBLICATION_EXECUTION_PLAN.md), and [Databento research handoff](AI_HANDOFF.md).

## Why we need a new study

The prior 'strict forward' experiment used `sigma_Q` inferred from **prior-date** option prices but **repriced it on the target date** with target-day CL futures settlement curves, observed fixings and target-day discounts. It is a legitimate **retrospective date-ordered conditional settlement-mark valuation**, but it cannot establish a forecast that was fully available **before** the option's target-day close.

No amount of date-level train/test splitting or bootstrap resampling can prove that a historical Barchart CSV was available and unmodified *as of* the old target-day prediction time. Do **not** call the 2,381-row or 97,341 actual-flagged retrospective results “verified live forecasts.”

The prospective remedy is **to create point-in-time evidence**, rather than assume it existed before. The experiment generates real forecasts *before* future target settlements, locks evidence with a trustworthy independent receipt, and only then evaluates future observed outcomes.

## Research hypothesis / estimand

**Primary question:** Conditional on only an admissible, sealed information set available *before* the AAO target-day settlement mark, does posterior integration or Bayesian prediction of implied volatility reduce error against a simple **unchanged previous-option-settlement** benchmark or **unchanged previous-contract-IV repricing** benchmark?

Separate estimands:
- **Outcome A (primary):** future CME WTI AAO **official final EOD settlement mark**. This is not a transaction, bid, ask, fill or hedge P&L. CME has used a Curran-style model to generate AAO settlements; an IV-based predictor can reproduce the clearing methodology without predicting executable value.
- **Outcome B (secondary, only if independently sourced/licensed):** *future time-stamped executable quotes/trades* in the same listed contract with clearly defined bid/ask or executable cost. Optional; **do not claim** verified trade-forecast performance without such data.
- **PI–PM sensitivity:** `mean_m price(σ^(m)) - price(mean_m σ^(m))` from the **same sealed underlying state and posterior**; do not confuse small point difference with posterior model-price intervals.
- **Mark-error predictive calibration:** independently evaluate forecast-error coverage over future days; not the same quantity as posterior theoretical-price credible intervals.

## Forecast information cutoffs and timings

**Recommended pilot design:** each eligible NYMEX trade date `T`, issue forecast at **11:00 a.m. America/Chicago** on `T` **only if** all required `T-1` final settlement inputs have actually been obtained and the published calendar indicates the targeted AAO settlement has not begun. `T-1` means the immediately preceding *exchange trading date*, not necessarily calendar yesterday. This is an **experimental proposed cutoff**, not proof that every AAO contract settles after 11 a.m. CT. Validate each targeted AAO product's official timetable *before* activating; if not confirmed, select a more conservative `T-1` pre-commit cutoff or skip the trade date.

Sources:
- [CME Daily Bulletin](https://www.cmegroup.com/market-data/daily-bulletin.html): preliminary around midnight CT after trade date and **final around 10 a.m. CT the next business day**. Verify actual file availability at ingestion, not merely the nominal schedule.
- [CME last-settlement snapshot and history technical description](https://cmegroupclientsite.atlassian.net/wiki/spaces/EPICSANDBOX/pages/1892122625/CME%2BGroup%2BPublic%2BWebsite%2BDistribution%2BREST%2BAPI): T+1 delayed settlement snapshots (about 7 a.m. CT), conditional on access/terms; no uncontrolled API polling or scraping.
- [CME crude-oil futures settlement methodology](https://www.cmegroup.com/trading/energy/files/NYMEX_Energy_Futures_Daily_Settlement_Procedure.pdf): relevant CL futures settle based on the later afternoon ET window. **The actual AAO option daily mark cutoff/publication time must be separately established**, not inferred blindly from the CL window.
- [CME settlement data FAQ](https://www.cmegroup.com/articles/faqs/access-to-cme-group-settlement-data-faq.html): publication channel and delayed options.
- [Databento CME AAO instrument catalog](https://databento.com/catalog/cme/GLBX.MDP3/options/AAO): explicitly distinguishes venue event `ts_event` and capture-server `ts_recv`; timestamped data may be available under separately licensed access, **not pre-authorized here**.
- [CME June 2026 market-data licensing policy update](https://www.cmegroup.com/market-data/files/market-data-license-agreement-updates-june-2026.pdf): material restrictions on copying, distribution and some data-dependent automation/derived work. **Legal permission for the particular source and use is a hard prerequisite**; a publicly accessible webpage is not an automatic permission to scrape it, use it for training or redistribute derived prices.

**Critical no-peeking convention:** at issuance `T 11:00 CT`, **do not** use the `T` AAO settlement, `T` CL end-of-day curve, `T` realized fixing, `T` Treasury par yield not yet published, `T` parity anchors, `T` official option-implied volatility, or `T` daily volume/OI as features. Use actual acquired and authorized prior-trading-date final snapshots only. A target-day source that was *actually received before* issuance could be added as a separately predeclared **intraday-information** model later, with its authenticated receipt timestamp; it is not part of the pilot.

**Valuation state:** fix the as-of date and path state at issue time, **not** at the future target close. For existing Curran pathwise code, build future fixings from the latest *admissible prior-date* CL curve and known prior fixings, discounting from last-published curve; use the same state for every model. This is not an unmodified rerun of `experiments/wti_forward_q_validation.py` or `experiments/wti_prior_contract_iv_carry.py`. Those scripts explicitly consume **target-day** settlement curves. Implement a prospective state/pricing adapter and verify it against controlled tests **before the first live forecast**.

## Experimental arms (freeze before first forecast)

| ID | Model at issue time | Model/source requirements |
| --- | --- | --- |
| `M0_last_mark` | **Carry previous known official AAO settlement price unchanged** to the future target-day mark | Strongest simple pricing baseline; must be available by issue cutoff |
| `M1_contract_iv` | Previous known AAO contract implied volatility, **repriced using the sealed prior-date CL/fixing/discount state** | IV source date strictly before issue; requires existing Curran/AAO inversion; no target date curve |
| `M2_smile_iv` | Previous known date's **six-term smile**, repriced on same sealed state | Same strike-side support/extrapolation rules as past experiment, predeclared ridge hyperparameters |
| `M3_historical_pi` | Historical-return volatility posterior **integrated** under identical sealed price map | Physical-`P` return model can differ from option-implied `Q`; explicitly diagnostic comparison |
| `M4_historical_pm` | Plug-in posterior mean volatility under identical sealed price map | Isolates PI versus PM on same target and input state |
| `M5_bayesian_lagged_iv` | Existing **frozen** Bayesian lagged-IV state model, if reproducible with prior-only sources | Complex model vs M1; disable this arm unless its pretrained hyperparameters/model structure are sealed *before* target outcome. No post hoc tuning. |

**Do not introduce a new model zoo.** If M1 cannot be priced without target-date state or M5 requires new selection, predeclare missing arms and compare only genuinely eligible M0/M2. Missing or failed forecasts must be logged—not replaced after seeing outcomes.

## Universe, eligibility, horizon, and sample plan

- Candidate instruments: current eligible CME WTI AAO listed options, fixed upfront to a predeclared set of expiry months, strike ranges or moneyness bands, option sides, and identity mapping; monitor delistings and contract symbol changes. Do not select a “best-fitting” contract/strike after marks are published.
- Primary horizon: **same-trading-day pre-settlement forecast using exclusively prior-trading-date EOD inputs** (issue at `T` before the target settlement window, predict **that day's `T` final mark**). It is an authentic **prospective** forecast, but **not** a full one-trading-day-ahead horizon: the prediction-to-mark lead time is only several hours. Report the actual UTC lead time for every target. A separate full-trading-day-ahead horizon may be preregistered later, using earlier cutoffs and independently sealed predictions, but must never be silently pooled with this pilot.
- Initial target: **at least 60 distinct eligible trading dates**, not 60 option rows. Report daily progress; 100 or more dates would support better month/block inference. If there are 0 eligible AAO settlements on a day, record an exclusion and retain the calendar count.
- Freeze fixed training history, input inclusion, model grid and eligibility rules before first issue. Do not treat the already inspected August–September 2026 data or Databento 2023–2026 splits as future unseen evaluation.
- Match all models on the same contracts/dates when comparing; distinguish all-enrolled and each model's availability coverage.
- Always stratify outcome quality by exchange actual/theoretical flags (where available), volume/OI, calls/puts, maturity and abs moneyness. Use only post-target metadata **for reporting strata**, never for prediction eligibility or model selection.

## Required evidence per forecast batch; private retention and independent receipt

Before publication of the target-day AAO mark, create and protect a **sealed forecast batch** with:
1. Forecast batch UUID and target NYMEX trade date, planned AAO settlement publication cutoff, exact `asof_utc` and `America/Chicago` trading calendar/time conversion.
2. Instrument stable IDs, contract specs, right/strike/expiry, a **frozen list of eligible contracts**, each model's forecast and any interval, baseline price and immutable model version. All target outcomes must be **absent** from the sealed file.
3. For each feature source: provider/dataset/instrument, actual observation/reference time, **originally received time (UTC)**, if available authoritative provider-published time, version/sequence/finality flag, license permissions, original content checksum, and how snapshot is retained in **access-controlled licensed storage**. A `T-1` date without `received_at` is insufficient for **fully verified** point-in-time claims.
4. The exact commit SHA of the code/model; package lock; model/training cutoffs; seed; pricing-engine version; timestamped generation log; UTC clock sync info and run success/failure.
5. A **cryptographic SHA-256 commitment** to the full sealed prediction file and input manifest, anchored to an **independently recorded pre-outcome GitHub push/PR event timestamp or other trusted timestamp receipt**. The local Git commit *author/committer date can be spoofed*, so a SHA and self-reported `generated_at` are **not sufficient** alone. Avoid force-push/rewrite, and save independent timestamp evidence outside the experiment repository as a backup.
6. Only after verified later target-mark publication: new outcome file (kept distinct from sealed predictions), publication receipt time, actual/theoretical/volume flags, data revision status, checksum, matched scoring script, result and error ledger.

**Store meaningful results in GitHub before VM teardown**, respecting the repository's standing rules, but **do not publish restricted price snapshots, quotes, model outputs that may count as derived licensed data, provider credentials, or vendor redistribution**. Restricted raw/source evidence belongs in **approved private license-compliant storage** with a cryptographic hash and authorized recovery procedure. A private repo may still be subject to license limits; do not assume privacy itself authorizes storage/distribution.

## Analysis (frozen acceptance gates)

- **Primary metric:** matched forecast-vs-future-final-AAO-settlement MAE, USD/bbl, plus RMSE, signed bias and interval score. Define per-trading-date loss contrast as `mean_{eligible options on date}(|err_simple|-|err_complex|)`; equal-weight trading dates. Contract-weighted results secondary.
- **Main predeclared contrast:** M1 **same-contract IV** vs M5 **Bayesian-IV**, evaluated on their common forecasts; M0 unchanged mark baseline and M2 IV smile must also be reported. **M5 superiority is not assumed**. M3 PI vs M4 PM is a distinct sensitivity test.
- **Uncertainty:** report paired mean difference by date with chronological circular/block or calendar-week/month block interval (block length documented *before unblinding*, include at least sensitivity to week and month), and number of independent target dates. With only 60-100 consecutive dates, power for changes of order USD 0.01/bbl may remain limited.
- **Failure accounting:** missing source at cutoff, late forecasts, missing marks, zero volume, model errors, stale data, stale contract identity and source corrections are tabulated *per date*, not erased.
- **Economic claim gate:** compare differences with the standard USD 0.01/bbl tick, but do **not** equate outperforming a mark with tradable edge, fill profitability or observed arbitrage.
- **Data endpoint:** any settlement publication/revision after the target must be checked against the frozen target definition, with final marks and corrections handled by a predeclared rule. No model modification after target.

## Hard exclusions and gates

**Cannot be claimed without original point-in-time inputs or a prospective sealed record:**
- A verified live historical August/September 2026 forecasting result.
- Proven tradable option predictions from AAO **model settlements alone**.
- “Leak-free” merely because `training_date < target_date` when **target-day futures**, fixes, rates or parity are included.
- A publication-grade result from forecasts that can be edited after outcomes or whose source observations were first fetched too late.

**Activation requirements (currently NOT met):**
- [x] Pre-register the method and known constraints as Markdown before observing any new future target.
- [ ] Verify CME **AAO-specific settlement** time relative to the chosen issuance cutoff; document holiday/early-close exceptions.
- [ ] Confirm authorized data access, **actual availability timestamp and licensing**, plus a compliant source snapshot-retention plan. Never scrape prohibited exchange pages.
- [ ] Implement and separately test a genuinely sealed **prior-date CL/fixing/rate pricing state**; existing forward scripts are **not ex-ante full-information forecasts**.
- [ ] Define stable option contract universe from an authorized recent instrument definition snapshot, freeze model choices/hyperparameters and handle delisted/no-price contracts.
- [ ] Ensure an **independently trusted pre-outcome receipt** of forecast hash and a second recoverable evidence copy; a local “created” timestamp alone is inadequate.
- [ ] Collect first live inputs after confirming acquisition rights, emit an actual forecast **before** target mark, and log receipt before settlement. **No forecasts have been issued yet.**
- [ ] After later official final marks, evaluate outcomes without changing previous forecasts, commit derived aggregate metrics and audit logs under approved terms.

## Priority and intended publication use

This study is **an optional prospective confirmation**, not a prerequisite to publishing the well-qualified existing REMEF Paper A. The old Barchart numerical audit remains valid for **retrospective conditional settlement-proxy** claims even if no trusted future feed is obtained. If a prospective panel grows to a sufficient number of independently dated events, it may strengthen a revised REMEF manuscript or become a **separate, transparently reported validation**; do not invent sample size, promise a submission date or delay all writing for an unbounded future study.

**Practical first step:** obtain a **license-compliant, actually time-stamped, no-cost or already-permissioned** delivery mechanism, an authoritative AAO settlement cutoff, and an append-only remote evidence receipt. Only then turn this pre-registration into an executable live market-data experiment.

## Protocol references

- CME [Daily Bulletin](https://www.cmegroup.com/market-data/daily-bulletin.html) and [Daily Settlements](https://www.cmegroup.com/market-data/daily-settlements.html).
- CME [Settlement-data availability FAQ](https://www.cmegroup.com/articles/faqs/access-to-cme-group-settlement-data-faq.html).
- CME [Energy CL settlement window procedure](https://www.cmegroup.com/trading/energy/files/NYMEX_Energy_Futures_Daily_Settlement_Procedure.pdf).
- CME [AAO settlement Curran methodology advisory](https://www.cmegroup.com/notices/clearing/2020/05/Chadv20-198.pdf).
- CME [June 2026 market-data license amendment](https://www.cmegroup.com/market-data/files/market-data-license-agreement-updates-june-2026.pdf).
- [Databento AAO catalog](https://databento.com/catalog/cme/GLBX.MDP3/options/AAO).
