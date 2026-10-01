# Paper wording dictionary

## Purpose

This file is the editorial vocabulary guide for the WTI APO manuscript. It is based on the
project literature corpus in `literature/extracted/` and its `bundle.md`, with particular
weight on Curran (1994), Kemna and Vorst (1990), Bakshi, Cao, and Chen (1997), Dumas,
Fleming, and Whaley (1998), Guidolin and Timmermann, Rombouts and Stentoft, Gilder and
Tsiaras (2020), Ewald, Wu, and Zhang (2023), and the other Asian-option / crude-oil /
Bayesian-option papers in the bundle.

The objective is not to force identical prose across papers. It is to use the vocabulary that
already exists in the option-pricing and volatility-forecasting literature, and to avoid
software-like or newly coined labels when an established term is available.

## Core editorial rules

1. Use **Asian option** as the generic product class and **arithmetic-average Asian option**
   when the averaging convention matters. Use **WTI Average Price Option (APO)** for the
   actual CME product.
2. Use **physical measure** (`P`) and **risk-neutral measure** (`Q`) consistently.
3. Use **implied volatility** / **option-implied volatility** when the quantity is literally
   recovered from option prices. Prefer this to the manuscript-created umbrella term
   “option-informed state.”
4. Use **out-of-sample pricing** and **out-of-sample pricing errors** for the forward
   evaluation. Describe the information restriction as “using only earlier dates” or
   “strictly prior observations.” Avoid ML vocabulary such as “holdout” in the paper.
5. Use **pricing method**, **valuation method**, or **pricing approximation**, not
   “pricing engine,” except in code/documentation.
6. Use **pricing error** for the difference between model and observed option prices.
   State the sign convention explicitly when signed errors are used.
7. Reserve **realized volatility** for an ex-post realized-volatility quantity. A standard
   deviation estimated from past daily returns is a **historical volatility estimate**, not
   automatically “realized volatility.”
8. Use **implied-volatility smile** for a same-maturity cross-section across moneyness.
   Use **implied-volatility surface** only when both moneyness and maturity dimensions are
   genuinely represented.
9. Prefer descriptive empirical statements (“has lower RMSE,” “does not reproduce the
   out-of-sample performance”) to broad exclusion language (“rules out,” “explains”).
10. Give each nonstandard project term a standard-language definition before using an
    abbreviation.

---

## 1. Contract and Asian-option terminology

| Concept | Preferred wording | Use / definition | Avoid or restrict |
|---|---|---|---|
| Generic derivative class | **Asian option** | Generic literature term for a payoff depending on an average of the underlying. | “average option” by itself when ambiguity is possible |
| Specific averaging convention | **arithmetic-average Asian option** | Use when distinguishing it from the geometric-average case. | “arithmetic option” |
| Geometric comparator | **geometric-average Asian option** | Standard wording when discussing Curran / Kemna--Vorst style methods and control variates. | “geometric Asian” unless space is tight |
| CME contract | **WTI Average Price Option (APO)** on first use; **WTI APO** thereafter | Preserve the exchange/product name. | Replacing the official product name with a newly coined generic label |
| Averaging observations | **fixing dates** for the WTI contract; **monitoring dates** in generic Asian-option discussion | “Fixing” is contract-specific; “monitoring” is generic numerical-option terminology. | Using both interchangeably within one paragraph |
| Known part of average | **realized fixings** / **already fixed observations** | For valuation dates inside the averaging period. | “observed leg,” “fixed state” |
| Remaining part | **remaining fixings** / **unresolved fixings** | Use consistently for future components of the average. | “future leg” unless explicitly defined |
| Strike relation | **moneyness** | Standard cross-sectional option term. Define the exact ratio used. | “relative strike” as the main term |
| Contract time dimension | **time to maturity** in prose; **expiry month** for named contracts | Use “expiry” for Sep-2026, Oct-2026, etc.; “maturity” for comparative analysis. | Switching among horizon/maturity/expiry without a reason |
| Market observation | **contract-date observation** | Neutral unit of the empirical panel. | “holdout row” |

---

## 2. Bayesian inference and parameter uncertainty

| Concept | Preferred wording | Use / definition | Avoid or restrict |
|---|---|---|---|
| General statistical issue | **parameter uncertainty** | This is the established umbrella term in the Bayesian option-pricing literature. | “Bayesian uncertainty” when parameter uncertainty is what is meant |
| Bayesian object | **posterior distribution** | Standard term. | “Bayesian distribution” |
| Summaries | **posterior mean**, **posterior mode**, **posterior moments** | Literature-standard Bayesian terminology. | “Bayesian mean” |
| Price integrating parameters | **posterior-integrated price** only after definition as “the posterior average of the conditional option value” | Keep because it is central to this paper and transparent once defined. | “full-Bayes price”; the corpus does not use this label |
| Comparison price | **price evaluated at posterior mean volatility** on first use; **posterior-mean price (PM)** thereafter | More explicit than repeatedly saying “plug-in.” | Heavy use of “plug-in price” in narrative prose |
| Central contrast | **PI--PM difference** / **effect of posterior integration on the point price** | Descriptive and tied to the estimands. | “Bayesian correction” as if it were universally required |
| Uncertainty in theoretical prices | **posterior distribution of model prices induced by parameter uncertainty** | Most precise description of the push-forward distribution used here. | “predictive price density” for this object: in Rombouts/Stentoft that term includes predictive return uncertainty, not only our parameter push-forward |
| Interval | **central 95% posterior interval for the model price** | Clear without implying a future-market predictive interval. | “95% predictive interval” |
| Width / dispersion | **dispersion of the posterior distribution of model prices** or **parameter-induced uncertainty in option values** | Prefer in prose. | “model-price uncertainty” as an undefined standalone concept |
| Local mechanism | **curvature of the option price with respect to volatility** | Directly describes (C^{Q\prime\prime}(\sigma)). | Introducing “volga/vomma” unless needed for a finance-specialist aside |

### Canonical definition

> The posterior-integrated price averages the conditional option value over the posterior
> distribution of volatility, whereas the posterior-mean price evaluates the same pricing
> model at posterior mean volatility.

This is the preferred first-use definition. After it, `PI` and `PM` are enough.

---

## 3. Measures and pricing language

| Concept | Preferred wording | Use / definition | Avoid or restrict |
|---|---|---|---|
| Statistical measure | **physical measure** (mathbb P) | Use consistently for return inference. | “real-world measure” unless discussing a source that uses that terminology |
| Pricing measure | **risk-neutral measure** (mathbb Q) | Hyphenate “risk-neutral” as an adjective. | Alternating among pricing measure / equivalent martingale measure / Q without need |
| Dynamics under Q | **risk-neutral dynamics** | Literature-standard wording. | “Q process” in prose |
| Theoretical value | **model price**, **theoretical option price**, or **option value** | “Model price” works well when contrasting with market settlement. | “predicted price” when no forecasting experiment is involved |
| Observed target | **market price** or, for these data, **settlement price** / **option settlement** | Preserve the fact that the empirical target is an end-of-day settlement. | “true price” |
| Difference | **pricing error** | Default empirical term. | “loss” unless a defined loss function is being used |
| Absolute error | **absolute pricing error**, **MAE** | Standard. | “valuation distance” |
| Squared-error summary | **RMSE** / **root mean squared pricing error** | Use full form on first use. | “RMS pricing loss” |
| Approximation | **pricing approximation** / **valuation approximation** | For Curran or other deterministic approximations. | “engine” |
| Simulation | **Monte Carlo simulation** / **Monte Carlo pricing** | Literature-standard. | “MC engine” in manuscript prose |
| Variance reduction | **control variate**, **antithetic variates** | Standard numerical-option language. | “control-variable trick” |
| Curran | **Curran conditioning approximation** / **Curran approximation** | Describe as an approximation under the maintained model. | Calling Curran an exact pricing formula for the arithmetic-average option |

---

## 4. Volatility terminology

| Concept | Preferred wording | Use / definition | Avoid or restrict |
|---|---|---|---|
| From past returns | **historical volatility estimate** / **historical-volatility benchmark** | For volatility estimated from historical daily returns. | Calling every such estimate “realized volatility” |
| Ex-post realized quantity | **realized volatility** / **realized variance** | Reserve for an ex-post volatility target, especially in the forecasting literature. | Using as a synonym for historical sample standard deviation without qualification |
| From option prices | **implied volatility (IV)** | Default term. | “market volatility state” |
| Emphasizing source | **option-implied volatility** | Strongly preferred over “option-informed volatility.” | “option-informed state” |
| APO inversion | **APO-implied volatility** | Volatility implied by an APO settlement under the maintained pricing model. | “APO risk-neutral state” |
| Vanilla inversion | **LO-implied volatility** / **vanilla-WTI implied volatility** | For the external option family. | “external state” when the actual quantity is implied volatility |
| Same-expiry moneyness relation | **implied-volatility smile** | Use for one expiry / date. | “surface” if maturity does not vary |
| Moneyness + maturity object | **implied-volatility surface** | Use only when a genuine two-dimensional cross-section is represented. | Calling every fitted smile a surface |
| Historical model forecast | **GARCH(1,1) volatility forecast** | First use should state that it is matched to the remaining APO fixing horizon. | Treating it as a risk-neutral GARCH pricing model |
| Scalar mapping across fixings | **effective scalar volatility under the maintained pricing model** | Use only where a multi-fixing or multi-contract volatility object is collapsed to one scalar. | Presenting it as a structural volatility parameter |
| Option-vs-history umbrella | **option-implied versus historical volatility inputs** | Preferred statement of the empirical contrast. | “risk-neutral state versus P-state” |

### Important distinction

Use **option-implied** when the number is actually inverted/calibrated from option prices.
Use **option-based** only as a broader adjective for a family of forecasts or benchmarks.
Use **option-informed** sparingly, preferably not at all in formal results.

---

## 5. Forecasting and empirical evaluation

| Concept | Preferred wording | Use / definition | Avoid or restrict |
|---|---|---|---|
| Forward test | **out-of-sample pricing experiment** / **out-of-sample pricing performance** | Closest match to Bakshi, Dumas, Guidolin, and Rombouts/Stentoft. | “holdout experiment” |
| Time restriction | **using only observations from earlier dates** / **strictly prior observations** | State the information set directly. | Repeated use of “strict forward-in-time” |
| One-day variant | **previous-day implied-volatility specification** | Literature frequently describes using previous-day implied parameters to price the next date. | “T-1 state” |
| Expanding variant | **implied-volatility specification estimated from all earlier dates** | Plain, explicit. | “expanding state” without definition |
| Same-contract benchmark | **same-contract lagged-IV benchmark** or **previous implied-volatility benchmark** | Prefer over “IV carry” in formal prose. “Carry” may remain as a short table label. | Treating “carry” as established terminology |
| Performance object | **out-of-sample pricing errors** | Standard empirical option-pricing wording. | “settlement prediction loss” |
| Comparison group | **benchmark** / **benchmark specification** | Corpus-standard. | “baseline competitor” |
| Multiple alternatives | **competing specifications**, **competing models**, **competing forecasts** | Literature-standard. | “challengers” |
| Prediction language | **forecast / predict option prices** only when information is restricted to earlier dates | Appropriate in the forward experiment. | Using “prediction” for contemporaneous calibration |
| Information statement | **information content of option-implied volatility** / **forward-looking information in option prices** | Literature-standard framing, especially in crude-oil volatility forecasting. | “the option state knows more” |
| Cross-section | **cross-sectional pricing** / **option cross-section** | Standard. | “cross-sectional state” |
| Common sample | **exact common sample** / **common-support sample** if support restriction is essential | Define support once. | “matched rows” in polished prose |
| Market-date resampling | **valuation-date cluster bootstrap** | Clear and statistically descriptive. | “date bootstrap” without saying what is clustered |

---

## 6. Model specification and interpretation

| Concept | Preferred wording | Use / definition | Avoid or restrict |
|---|---|---|---|
| Imperfect model | **model misspecification** / **misspecified model** | Established option-pricing terminology. | “model mismatch” as main academic term |
| Richer dynamics | **model specification** / **alternative option-pricing model** | Standard. | “model enrichment” in core prose |
| Comparing model classes | **pricing performance**, **out-of-sample pricing performance** | Literature-standard. | “model quality” |
| Flexible IV relation | **implied-volatility function**, **smile specification**, or **implied-volatility surface**, depending on dimensionality | Match the actual object. | “flexible cross-sectional smoother” |
| Endogenous APO IV | **APO-implied volatility estimated from the target option family** | Explicitly identifies within-family source. | “endogenous Q-state” |
| External LO check | **cross-instrument validation using vanilla-WTI implied volatility** | Describes what the experiment does. | “independent Q-state experiment” |
| Risk-premium interpretation | **physical versus risk-neutral distinction** / **variance risk premium** only when actually estimated | Maintain caution. | Describing the historical-vs-IV pricing gap itself as a risk premium |
| Structural claim | **under the maintained pricing model** | Repeat when interpreting implied volatility structurally. | “true risk-neutral volatility” |

---

## 7. Claim verbs and evidentiary strength

### Preferred

- **shows**
- **indicates**
- **is consistent with**
- **has lower MAE/RMSE**
- **improves out-of-sample pricing performance**
- **does not reproduce the option-implied performance**
- **is robust to**
- **remains similar under**
- **provides a cross-instrument check**
- **contains forward-looking information**
- **has greater information content for this pricing exercise**

### Use only with direct support

- **outperforms** — acceptable for a clearly defined metric/sample, but do not imply statistical
  significance unless tested.
- **significantly outperforms** — only with an explicit statistical test.
- **explains** — only when the design identifies an explanation, not merely a ranking.
- **driven by** — only after a direct robustness/decomposition test.

### Avoid

- **proves**
- **rules out**
- **establishes that no historical model can...**
- **dominates** unless dominance is formally demonstrated
- **the key information is...** when the design only shows lower pricing error
- **survives** as the default academic verb; prefer **is robust to** or **persists under**

---

## 8. Project terms that should be normalized

| Current manuscript-style term | Preferred replacement |
|---|---|
| option-informed state | option-implied volatility / option-implied volatility input |
| option-informed specification | option-implied specification / option-based specification |
| risk-neutral state | implied-volatility input / implied-volatility surface |
| pricing engine | pricing method / valuation method / pricing approximation |
| holdout(s) | out-of-sample observation(s) / contract-date observation(s) |
| strict forward-in-time panel | out-of-sample panel using only earlier-date information |
| posterior model-price interval | posterior interval for the model price |
| posterior model-price dispersion | dispersion of the posterior distribution of model prices |
| parameter-induced price uncertainty | parameter uncertainty in option values |
| recent-history rule | historical-volatility benchmark |
| IV carry | same-contract lagged-IV benchmark (table label may remain “IV carry”) |
| common-Curran comparison | comparison under the same Curran approximation |
| fitted smile | fitted implied-volatility smile |
| external state | vanilla-WTI implied-volatility input |
| scalar transfer rule | scalar volatility mapping |
| historical-versus-option-informed gap | historical-versus-option-implied pricing difference |
| model enrichment | richer model specification |
| pricing map | pricing function / option-pricing function when mathematical; pricing model when structural |

---

## 9. Canonical wording for the paper's three findings

### Finding 1 — posterior integration

Preferred:

> The difference between posterior-integrated and posterior-mean prices is governed locally by
> posterior variance and the curvature of the option-pricing function with respect to
> volatility.

Avoid:

> Bayesian integration corrects the option price through a second-order effect.

The latter sounds normative and suggests that PM is an error that must be corrected.

### Finding 2 — point-price effect versus parameter uncertainty

Preferred:

> In the observed WTI sample, posterior-integrated and posterior-mean prices are close, even
> though the posterior distribution of model prices remains materially dispersed.

or

> A small PI--PM difference does not imply little parameter uncertainty in the option value.

Avoid:

> Posterior uncertainty is large even though Bayes barely matters.

### Finding 3 — empirical volatility input

Preferred:

> In the out-of-sample pricing experiment, prior option-implied volatility inputs produce
> substantially lower pricing errors than the historical-volatility benchmarks evaluated in
> this paper.

Then qualify:

> The result is robust to the evaluated rolling-window, EWMA, and horizon-matched GARCH
> benchmarks and does not require a flexible implied-volatility smile.

For the external experiment:

> A cross-instrument validation using prior vanilla-WTI implied volatility yields the same
> qualitative ordering relative to the historical-volatility benchmark.

Avoid:

> Risk-neutral volatility dominates physical volatility.

That statement is structurally much stronger than the experiment supports.

---

## 10. Recommended terminology for tables and headings

Preferred table/section labels:

- **Out-of-sample APO pricing errors**
- **Historical-volatility benchmarks**
- **Previous-day and earlier-date implied-volatility specifications**
- **Same-contract lagged-IV benchmark**
- **Cross-instrument validation using vanilla-WTI options**
- **Numerical accuracy**
- **Parameter and model-specification robustness**
- **Liquidity and valuation-date dependence**

Prefer column headers:

- `Model / volatility input`
- `N`
- `Target dates`
- `MAE`
- `RMSE`

Avoid headings built around internal implementation labels such as “state,” “engine,” “runner,”
“pipeline,” or “holdout.”

---

## 11. Abbreviation policy

Use only abbreviations that materially reduce repetition:

- **APO** — Average Price Option
- **IV** — implied volatility
- **PI** — posterior-integrated price
- **PM** — posterior-mean price
- **LO** — define as the CME/NYMEX vanilla WTI option product before using
- **GARCH**
- **EWMA**
- **MAE**
- **RMSE**

Do not introduce abbreviations for concepts used only a few times.

---

## 12. Source-language anchors from the literature corpus

The dictionary follows recurring language in the bundle:

- **Asian-option literature:** “Asian option,” “arithmetic average Asian option,” “geometric
  average Asian option,” “Monte Carlo simulation,” “control variate,” “moneyness,” and
  “maturity.”
- **Empirical option-pricing literature:** “out-of-sample pricing,” “out-of-sample pricing
  errors,” “pricing performance,” “model misspecification,” “benchmark model,” and
  “previous day's implied parameters.”
- **Bayesian option-pricing literature:** “posterior distribution,” “posterior moments,”
  “parameter uncertainty,” and integration “over the entire parameter space.”
- **Crude-oil volatility literature:** “option-implied volatility measures,” “volatility
  forecasts,” “forecast performance,” “realized volatility,” “GARCH,” and
  “forward-looking” option information.
- **Volatility cross-sections:** “implied volatility smile,” “implied volatility function,”
  and “implied volatility surface.”

This file is an editorial constraint for future manuscript edits. When a wording choice is not
covered here, prefer the terminology in the most directly relevant paper in
`literature/extracted/` rather than inventing a new label.
