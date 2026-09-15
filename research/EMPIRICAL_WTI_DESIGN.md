# Empirical WTI Average Price Option design

## Purpose

The empirical application complements, rather than replaces, the controlled
synthetic Monte Carlo experiment. The synthetic design retains known true
parameters and therefore supports bias/RMSE/coverage evaluation. The WTI
application asks whether posterior parameter uncertainty is economically
material when pricing real CME WTI Average Price Options (APOs).

## Contract definition

CME Rulebook Chapter 341 defines the WTI Average Price Option as a cash-settled
European-style option on the arithmetic average of the **daily settlement price
of the first-nearby Light Sweet Crude Oil (CL) futures contract during the
calendar month**. Consequently the empirical pricer must not evolve one spot
asset or one fixed futures maturity. It must reconstruct the first-nearby roll
and the current WTI futures term structure for the remaining fixing dates.

## Maturity design

The initial empirical panel deliberately spans the curve instead of downloading
many nearly redundant adjacent expiries:

- Sep-2026
- Oct-2026
- Nov-2026
- Mar-2027
- Sep-2027
- Mar-2028
- Sep-2028
- Jun-2029

Near-the-money downloads are retained in full. Calls and puts are both useful.
No strike is selected merely because it is near the money on the final download
date; WTI moved sharply during the sample and a fixed strike can cross between
ITM, ATM and OTM states over its life.

## Raw panel versus representative contracts

The estimation sample and the figures serve different purposes.

1. **Raw panel**: retain every downloaded option-date observation and every raw
   Barchart field. Do not delete zero-volume observations because an exchange
   settlement/mark can remain economically relevant on an illiquid day.
2. **Main panel**: apply pre-specified data-quality filters, initially positive
   open interest and price above the minimum tick. Sensitivity checks vary the
   OI threshold and include/exclude minimum-tick observations.
3. **Representative contracts**: rank contracts only for figures and case-study
   discussion. Favor long histories, informative (non-minimum-tick) marks,
   persistent open interest, days near effective ATM, and contracts that cross
   moneyness states. This ranking must not define the main estimation sample.

## Effective moneyness

For an APO the current front-month futures price alone is not the right state
variable, especially once the averaging month has begun. Define the expected
terminal average under Q as

    Ahat_t,T = [sum(realized fixings) + sum(current forward levels assigned to
                remaining first-nearby fixing dates)] / N.

Then classify each option-date with

    m_t,K,T = log(K / Ahat_t,T).

Suggested descriptive buckets are |m| <= 0.05 (ATM), 0.05 < |m| <= 0.15
(moderate), and |m| > 0.15 (deep). These are reporting buckets, not filters
that determine whether an observation enters the model.

## Risk-neutral pricing baseline

For each remaining fixing date j, use the observed futures curve to assign a
current first-nearby level F_j(0). The baseline one-factor model is

    F_j(t_j) = F_j(0) exp[-0.5 sigma^2 t_j + sigma W^Q_{t_j}],

so every futures level is a Q-martingale. The term structure and roll are in
F_j(0), while posterior uncertainty is propagated through sigma. This is a
transparent baseline rather than a claim that WTI has one constant volatility
factor in reality; richer term-structure/stochastic-volatility specifications
are robustness extensions.

For each option-date compare:

- full Bayes: E[C^Q(sigma) | D_t],
- posterior-mean plug-in: C^Q(E[sigma | D_t]),
- MAP plug-in,
- MLE plug-in,
- observed market end-of-day price/settlement proxy.

## Volatility regimes

The recent WTI episode is useful precisely because it contains large price
moves. Define volatility regimes from data, not from hand-picked geopolitical
labels. A baseline is 21-day annualized realized volatility, split into
low/medium/high quantile regimes. The main empirical question becomes whether

    Delta_FB-PM = C_FB - C_PM

is larger when posterior uncertainty in sigma is larger, and how the effect
varies with effective moneyness and time to expiry.

Geopolitical events can be discussed as economic context after the quantitative
regime classification, but should not be used as causal labels without a
separate event-study design.

## Data provenance and redistribution

Barchart per-contract CSVs should be treated as licensed research inputs.
Unless redistribution rights are confirmed, keep raw downloads local and do
not commit them to the public repository. Commit parsers, manifests, aggregate
summaries and reproducible code instead. CME Daily Bulletin/QuikStrike can be
used for spot checks against official settlements.
