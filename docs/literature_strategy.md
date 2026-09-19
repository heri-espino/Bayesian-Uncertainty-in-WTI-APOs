# Literature strategy

The literature corpus is part of the scientific argument, not a decorative bibliography.

## Immediate priority

Issue [#33](https://github.com/heri-espino/Metropolis-Hastings-for-Asian-Options-Using-Bayesian-Inference-and-Black-Scholes--Article-/issues/33)
tracks the eight newly added papers.

The synthesis should answer, for every paper:

| Field | Question |
|---|---|
| Research question | What problem is the paper actually solving? |
| Model | What physical/risk-neutral model is used? |
| Market/data | What instruments and sample are studied? |
| Parameter uncertainty | Is uncertainty propagated, ignored, or approximated? |
| Volatility specification | Historical, implied, stochastic, smile/surface, or other? |
| Main empirical result | What does the evidence actually show? |
| Relevance here | Which claim in the WTI APO paper does it support or constrain? |
| Novelty boundary | What does the present paper do that this paper does not? |
| Manuscript location | Introduction, methodology, results, robustness, or limitations? |

## Core positioning buckets

### Bayesian option pricing

Use Guidolin–Timmermann and Rombouts–Stentoft as direct antecedents. The paper should
acknowledge that prior work already propagates parameter uncertainty into option values.

### Implied volatility and crude oil

Use the crude-oil IV literature to motivate why option-implied information may outperform
long-window historical volatility without claiming that a unique scalar `sigma_Q`
structurally governs the market.

### Asian and commodity option models

Curran and Kemna–Vorst support the pricing/numerical layer. Schwartz and richer commodity
Asian models establish what is intentionally omitted from the parsimonious benchmark.

### Model complexity and misspecification

This literature should support the distinction between:
- parameter integration *within* a pricing map, and
- changing the pricing map or volatility state itself.

That distinction is central to the manuscript's final contribution.

## Citation discipline

Do not cite a paper merely because it contains the same keywords. Every citation added to
the manuscript should have a documented role in the literature matrix and should support
the exact claim made in prose.
