# Referee-style revision tracker — 2026-09-29

Source: user-supplied substantive review of the 23-page JFM manuscript.

## Completed in PR #67

- [x] Narrow title to the point-price posterior-integration question.
- [x] Shorten and narrow abstract.
- [x] Remove unsupported claim that the empirical ordering can reverse.
- [x] State contribution as a controlled empirical/mechanism diagnostic, not a new pricing method.
- [x] Distinguish PI--PM mean-price correction from posterior model-price dispersion.
- [x] Add delta-method price-uncertainty approximation.
- [x] Add posterior-RMS volatility plug-in definition.
- [x] Add October table panel comparing mean |PI-PM| with 95% posterior price-interval width.
- [x] Remove repeated estimator-specific coverage from Table 1; attribute coverage to the common posterior interval procedure.
- [x] Put the synthetic maximum on an economic scale using the WTI APO 1,000-barrel multiplier and $0.01/bbl ordinary tick.
- [x] Clarify that LO fixing-count RMS aggregation is an effective scalar transfer, not an exact arithmetic-average variance identity.
- [x] Add full covariance expression for arithmetic-average variance.
- [x] Document 160-step American CRR production inversion.
- [x] Add a true moment-matched LO-to-APO surface transfer using target fixing times, futures levels, and the common-factor covariance structure; retain weighted mean as an optional simple diagnostic.
- [x] Remove decorative hierarchy display equations and state the comparison in prose.
- [x] Replace computational-effort counts with achieved numerical precision in the main text.
- [x] Qualify cluster-bootstrap improvement frequencies as resampling results conditional on observed dates.
- [x] State temporal limitation: 15 forward target dates and 10 external common-support target dates.
- [x] Note that date clustering does not eliminate dependence across adjacent dates.
- [x] Fix hyperlink boxes and two-column equation overflow.
- [x] Apply final publication palette and Iridescent continuous map.

## New deterministic/lightweight robustness checks implemented

### Recent historical volatility on exact forward holdouts
`experiments/wti_recent_historical_benchmarks.py`

Pre-specified: rolling 63, 126, and 252 usable returns plus EWMA with a 63-business-day half-life. Uses the exact target-date information cutoff and the same Curran target state.

### Posterior RMS plug-in
`experiments/wti_rms_plugin_comparison.py`

Compares posterior-mean volatility with `sigma_RMS = sqrt(E[sigma^2 | D])` on the exact strict-forward holdouts without rerunning MCMC.

### APO mark-persistence benchmark
`experiments/wti_prior_contract_iv_carry.py`

For each eligible target contract, carries its latest strictly-prior contract IV forward and reprices with the target-date futures curve/fixing state. Compares on exact common rows against the previous-day APO smile and historical PI.

### LO transfer sensitivity
`experiments/wti_external_vanilla_q_validation.py`

The primary referee-facing sensitivity now uses `--surface-aggregation moment_matched`. It chooses the single APO volatility that matches the variance of the unresolved arithmetic-average component under the maintained one-common-factor representation. `weighted_mean` remains available as a simpler non-variance-matching diagnostic.

### LO CRR convergence
`experiments/wti_lo_tree_convergence.py`

Deterministic low/ATM/high-strike sample by date/underlying/side. Re-inverts at 80, 160, and 320 tree steps.

### LO surface-shape audit
`experiments/wti_lo_surface_shape_audit.py`

Checks strictly-prior fitted surfaces for finite/positive IV inside prior support, more than one direction change, and call/put fitted-IV gaps on overlapping support. Because LO is American-style, the audit deliberately does not impose European put-call parity.

## One-command production run

```powershell
python -m scripts.run_reviewer_robustness
```

## Pending before merging PR #67

- [ ] Run the reviewer robustness suite on the external machine.
- [ ] Commit/push the new derived result directories.
- [ ] Inspect exact recent-history, RMS, persistence, moment-matched LO, tree-convergence, and surface-shape results.
- [ ] Integrate only supported numerical conclusions into Results/Robustness.
- [ ] Recompile Wiley PDF and visually inspect the revised manuscript.
- [ ] Complete corresponding-author email.
- [ ] Complete acknowledgments.
- [ ] Final referee/readability pass.
