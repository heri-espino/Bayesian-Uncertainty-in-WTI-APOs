# Research project wiki

This documentation site is the canonical project wiki for the WTI Average Price Option
paper.

## Start here

- [Research roadmap](research_roadmap.md) — milestones, Issues, workstreams, and Project-board design.
- [Literature strategy](literature_strategy.md) — how the literature is screened and used.
- [WTI empirical workflow](empirical_wti.md) — contract/data and empirical implementation.
- [Architecture](architecture.md) — package and experiment architecture.
- [Development](development.md) — engineering workflow.
- [Journal strategy](journal_strategy.md) — conditional JCM, REMEF fallback, JFM alternative.
- [Submission checklist](submission_checklist.md) — journal-specific readiness gates.

## Current empirical extension: historical AAO files acquired, audit pending

The author's VM reported **160 downloaded compressed AAO definition/statistics files across
80 eligible monthly windows (January 2020–September 2026)** at USD 17.33487324 *quoted*.
Raw proprietary files are local only. Actual billing, excluded month, instrument/settlement
identity, theoretical/actual mix, liquidity, chronology and newly independent eligible
dates are **still unverified**.

See [dated checkpoint](https://github.com/heri-espino/Bayesian-Uncertainty-in-WTI-APOs/blob/main/research/CHECKPOINT_2026-10-25_AAO_EXPANSION.md),
[agent workstreams](https://github.com/heri-espino/Bayesian-Uncertainty-in-WTI-APOs/blob/main/research/AAO_AGENT_TASKS.md),
and [Issue #90](https://github.com/heri-espino/Bayesian-Uncertainty-in-WTI-APOs/issues/90).
Run only the **offline** inventory until the dataset passes identity/quality gates.
The previous 15-date main and 10-date LO comparisons remain the published-draft baseline.

**Conditional journal strategy:** [Journal of Commodity Markets prospect, REMEF fallback,
preserved JFM](journal_strategy.md). A new journal target or stronger publication
claim is not automatically established by downloading records.

## Current scientific thesis

The paper asks when Bayesian posterior integration materially changes a WTI Average Price
Option value and when the larger source of error is the volatility/model state supplied
to the risk-neutral pricing map.

The current evidence supports a conditional hierarchy:
- posterior integration can be economically meaningful when posterior dispersion and
  pricing curvature are simultaneously large;
- the observed long-history WTI posterior is concentrated, making PI and PM prices nearly
  identical;
- in the September–October WTI APO application, volatility specification produces a much
  larger empirical effect than posterior integration.

This wiki should describe the project as it exists, not as originally conceived.
