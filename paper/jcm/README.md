# Journal of Commodity Markets — Elsevier CAS working draft

> **2026-10-27 CL source feasibility finding:** [Independent first-nearby CL audit](../../research/JCM_CL_FUTURES_FEASIBILITY_AUDIT_2026-10-27.md) finds a previously purchased, Git LFS-tracked 2024–Sep2026 CL futures source (33 contracts, 2,223,975 reported raw rows), a derived 673-date/632-return roll-clean front series, and 14 short 2026 Barchart CL futures curve files. However the 311MB CL LFS SHA256 **disagrees** with the saved acquisition manifest SHA256; exact raw version and the full 2020–2026 forward curve remain unverified. The new read-only local scanner is scripts/audit_jcm_cl_feasibility.py; no purchase or JCM experiment has been authorized/executed. The existing JCM CAS draft still reproduces old Paper A text.

> **PAPER B TRACK — 2026-10-27:** This is now the *prospective* venue/workspace for a **different original research project**: verified first-nearby CL fixing-path reconstruction, actual partly fixed WTI AAO payoff pricing under the futures term structure, and independent market-price or implementable hedging validation where possible. Read the [two-paper nonoverlap and publication plan](../../docs/two_paper_publication_strategy_2026-10-27.md) and the [separate structural JCM feasibility protocol](../../research/STRUCTURAL_WTI_AAO_PAPER_FEASIBILITY_PLAN_2026-10-27.md). **Current CAS builder still stages the OLD Paper A concise manuscript**; it is **not** a finished draft for this new JCM Paper B. No CL fixing-path research has yet been executed for Paper B and JCM is not selected for a live submission. Work only after auditing missing underlying data, economic targets and permissions.

This is a **pre-submission source adaptation**, not a validated 81-month option-pricing paper or an approved journal submission.

The author added Elsevier CAS v2.4 under paper/els-cas-templates/. This project uses **cas-dc.cls** (double-column) for an internal working draft. The final Journal of Commodity Markets Guide for Authors still needs verification before preparing the actual submission.

## Manual build (no inference or figures recomputed)

From the repository root:

~~~powershell
python paper/jcm/build.py --check
python paper/jcm/build.py
~~~

The script stages CAS classes, the original **validated** concise manuscript sections, bibliography and already produced figures in **paper/jcm/build/stage/**. A local PDF, when TeX is installed, is written to **paper/jcm/build/jcm_working_draft.pdf**. Both are ignored by Git. The tool does not run pricing, MCMC, figure generation or paid Databento calls.

**Important:** Existing section-specific numbers and plotted comparisons still refer to the original 2026 Barchart/LO study, not to the newly acquired January 2020–September 2026 AAO history. The abstract/data statement explicitly acknowledges that distinction.

## Release gates for the actual expanded manuscript

1. Verify both acquisition ledgers (original 80 months and February 2021) and **all 162** local DBN SHA256 values.
2. Run the full 81-month inventory, then generate the new diagnostic figure.
3. Confirm instrument-class membership and map statistical settlement updates to stable option contract keys and CME reference trading dates. Separate final actual-flagged and theoretical-flagged exchange marks.
4. Reconcile overlapping Barchart APO marks and CL futures, appropriate fixings, historical return sources, rates, and strictly earlier date APO/LO implied volatilities.
5. Construct the eligible-date funnel. Freeze chronological test periods and same-row model comparisons, complete date-cluster/block confidence intervals, and validate across market regimes.
6. Update results, figures, abstract, data availability and all corresponding tables **only** from a documented run and approved reproducibility snapshot. Reassess whether Journal of Commodity Markets is suitable; keep REMEF and Wiley/JFM alternatives until author selects one, with no simultaneous submission.

The figure script in scripts/plot_aao_history_coverage.py generates a **diagnostic event count figure**, not a substitute for the existing model performance figures. All raw market inputs and generated derived figure files remain on the user's VM.

Elsevier CAS has both cas-sc and cas-dc classes. This manuscript's use of cas-dc is an internal design choice, not an assertion that the journal requires it. See https://www.elsevier.com/researcher/author/policies-and-guidelines/latex-instructions .
