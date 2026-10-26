# Execution plan: 81-month WTI APO historical research and JCM working paper

## Scope and evidence cutoff

The author reports Databento AAO definition/statistics data **acquired for all 81 months** (January 2020–September 2026), **162 DBN files** in two local acquisition ledgers, **USD 17.49357489 combined quoted**. These are *not* 81 months of validated pricing observations. An earlier **80-month** inventory contained 1,682 final settlement reference dates and 5,843,770 final settlement **events**. A refreshed 81-month inventory was reported by the author as processed, but its aggregate counts and file-based report are not available in GitHub; do not reuse the 80-month numbers as if they were updated.

The previous strict-forward evidence (2,381 option rows on 15 dates and 253 cross-instrument LO rows on 10 dates) remains the validated baseline. Never claim a new MAE, RMSE, inference interval, count of eligible pricing days, or market improvement until the new experiment actually runs and is audited.

## Local sequence on Windows PowerShell

~~~powershell
git switch main
git pull --ff-only origin main
conda activate asian-options

# Gate 1: verify actual bytes / hashes from BOTH ledgers; no API requests
python -m scripts.audit_aao_manifests

# Gate 2: recompute the complete 81-month event inventory; no API requests
python -m experiments.wti_databento_aao_inventory --all

# Gate 3: updated event-coverage figure, diagnostic ONLY
python -m scripts.plot_aao_history_coverage

# Gate 4: verify new Elsevier working-draft source without compiling
python paper/jcm/build.py --check

# Gate 5: compile Elsevier draft, only if pdflatex/bibtex available
python paper/jcm/build.py
~~~

**Stop on any failure.** The integrity report goes to results/analysis/wti_aao_history_feasibility/integrity/combined_manifest_audit.json. It expects 162 local files and checks SHA256 and size against the old 80-month and February-specific ledgers. The coverage generator requires 81 error-free consecutive month entries with consistent final/theoretical/actual event counts; it produces fig05_aao_final_settlement_event_coverage in PDF, PNG and SVG, plus a figure-provenance manifest, all gitignored.

Neither gate 1 nor gate 2 establishes the correct option prices. They identify trustworthy local source files and their settlement-statistics metadata.

## Exploratory instrument identity experiment (strictly offline)

After SHA256 and event-inventory checks, run:

~~~powershell
python -m experiments.wti_aao_identity_probe --month 2021-02
python -m experiments.wti_aao_identity_probe --month 2026-06
~~~

This diagnostic reads only one local month at a time and writes **aggregate**
counts under results/analysis/wti_aao_history_feasibility/identity_probe/.
It examines definition asset/class frequencies, how many final settlement
events reference a same-month outright (`AAO`, class `C` or `P`)
publisher/instrument ID, how many are unmatched, and how often instrument
IDs map to multiple raw symbols. It also reports **tentative**, unvalidated
ID/date keys to identify where event updates or identity reuse require
attention. No raw symbols or prices are printed. **It is not** a
timestamp-as-of contract mapping or stable contract-date pricing panel.
If required fields are missing or unparseable, it explicitly reports a
blocking error instead of guessing. Use the resulting report to specify
a correct time-aware normalization algorithm before attempting all
81 months or any pricing experiment.

## Required scientific implementation after gates 1–3

**Workstream A — contract/settlement master.** Decode definitions and statistics in bounded monthly batches. Resolve `publisher_id + instrument_id` under time-aware historical definitions; explicitly separate outright call/put (`C`/`P`) from strategy/leg records and instrument ID changes. CME `ts_ref` defines the settlement reference date; apply `update_action` and the final/actual flags. Keep local price-level outputs out of Git. Report counts of unique outright contract × reference-day final settlement prices, theoretical/actual composition, expiries, C/P and liquidity event alignment. Fail closed on ambiguous joins and record it as attrition rather than backfilling guessed matches.

**Workstream B — cross-vendor and pricing inputs.** Match normalized contract/day/strike/side/expiry against Barchart `Latest` marks on overlapping dates; report unmatched and discrepancies by date/class. Reconstruct the correct first-nearby CL fixing calendar, valuation-date curve, CL last-trade date, actual already-realized fixings and dated Treasury discount approximation. External LO IV requires paid data only if the existing LO subset is insufficient and the author approves a new quote/purchase.

**Workstream C — forward prediction samples.** Freeze the method and chronological holdouts before inspecting test errors. Historical P volatility and earlier-date option-informed Q volatility inputs are distinct estimation objects. Prevent pricing target leakage (no same-day APO mark used to calibrate its own IV); require valid prior-date smile/LO or same-contract IV support. Publish year/expiry-level attrition funnels: total final marks → unique contract-day keys → fixed CL/rates support → previously available IV → independently eligible target dates.

**Workstream D — new experiments and uncertainty.** Reuse the canonical `experiments/wti_apo_empirical.py`, `experiments/wti_apo_date_panel.py` and `scripts/run_extended_forward_validation.py`, adapting input loaders rather than creating competing pricing engines. Rerun PI/PM, historical expanding/rolling/EWMA/GARCH, prior APO IV and independent LO IV with identical matched rows where comparable. Date-cluster and temporal-block intervals are required; record bias/MAE/RMSE and breakdowns by year/regime/expiry, liquidity, actual/theoretical settlements and fixing progress. Retain seed/config/commit/data provenance and compare historical overlap with old results before accepting conclusions.

**Workstream E — publication artifacts.** *Only after D passes:* regenerate model figures from the new versioned result tables and the extended-sample comparisons; add any additional explanatory figures with precise reference-day counts. Reconcile every old 2026 number/caption/table, rework introduction, limits, abstracts and supplement, then create submission-ready Elsevier CAS files **without overwriting** the original Wiley/REMEF sources. Choose JCM versus REMEF versus JFM based on demonstrated novelty and external validity, not on 162 files or a 1,682-date pre-Feb event inventory.

## Agent/reproducibility contract

Read AGENTS.md, research/AAO_AGENT_TASKS.md and research/AI_HANDOFF.md. Start from updated main in a new short-lived PR; preserve date cutoffs and source identities. Automated CI should contain only lightweight tests, lint, documentation and deterministic small fixtures. Heavy analytics, figure/PDF generation and proprietary data downloads are **manual-only**. Do not commit raw DBN/parquet, priced contract-level output, plaintext keys, Windows profile information, or licensed user-specific data. Do not add completed-output numbers to the manuscript without actual reproducible experimental artifacts.
