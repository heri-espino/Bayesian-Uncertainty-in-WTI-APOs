# Research project wiki

This documentation site is the canonical project wiki for the WTI Average Price Option
paper.

## Start here

- [Research roadmap](research_roadmap.md) — milestones, Issues, workstreams, and Project-board design.
- [Literature strategy](literature_strategy.md) — how the literature is screened and used.
- [WTI empirical workflow](empirical_wti.md) — contract/data and empirical implementation.
- [Architecture](architecture.md) — package and experiment architecture.
- [Development](development.md) — engineering workflow.
- [Submission checklist](submission_checklist.md) — final Journal of Futures Markets package.

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
