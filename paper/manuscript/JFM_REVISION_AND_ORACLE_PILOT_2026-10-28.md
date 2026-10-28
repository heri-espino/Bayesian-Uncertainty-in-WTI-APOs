# JFM Paper A: focused revision and bounded experiment roadmap

**Date:** 2026-10-28  
**Priority:** *Journal of Futures Markets* (Wiley) is the active **ambitious** target for **Paper A**. The existing REMEF manuscript under \`paper/remef/\` is the unchanged fallback. JCM Paper B in \`paper/jcm/\` is a **separate unfinished research proposal**. Do not submit the overlapping REMEF/JFM versions simultaneously.

## What changed in the JFM branch

1. The **concise Wiley manuscript** \`paper/manuscript/main_short.tex\` is the default build. The older full \`main.tex\` is retained as a historical reference and must not be mistaken for the new submission manuscript.
2. The abstract now reports the **existing** 10-million-history mechanism study rather than the old 175,000-history version. It highlights the 310-option October sample, 2,381 observations on only 15 valuation dates and the economic difference between **posterior price dispersion** and a point-price correction.
3. Language explicitly distinguishes date-ordered **conditional repricing** from an independently verified prospective forecast. We cannot verify the vendor's original publication times or all historical revisions, and many observations have no reported trade volume.
4. The Wiley build stages committed figure PDFs rather than regenerating shared REMEF figure assets. If dedicated \`figures/jfm/*.pdf\` files exist, it overlays those only into the disposable LaTeX stage. REMEF source, figures and Word/PDF review artifacts remain untouched.
5. \`scripts.build_publication_figures --journal jfm\` writes **separate JFM draft figures** under \`figures/jfm/\`, with a corrected Figure 3 title ("Date-ordered conditional pricing comparisons across expiries") and a provisional two-column width. **Do not consider them final font proofs** until the installed Wiley Utopia typography and actual TeX text-width have been matched by inspection.
6. We cite Cummins and Esposito (2025, JFM, DOI 10.1002/fut.22575), who compare complex stochastic-volatility/jump models. This paper's narrower question concerns **volatility posterior integration, the information in volatility inputs, and the conditions under which apparent estimator agreement is uninformative**. Do not imply priority over their contribution.

## Scientific extension: no new market data

The purpose is **not** to increase simulation count. It is to test whether a small PI–PM price difference reliably indicates low statistical or model error. The core quantities are

\[
\Delta_{\mathrm{PI}}=\lvert E[C(\sigma)\mid D]-C(E[\sigma\mid D])\rvert,\quad
e_{\mathrm{est}}=\lvert C(E[\sigma\mid D])-C^\star\rvert,\quad
s_C=\operatorname{SD}(C(\sigma)\mid D).
\]

The controlled pilot in \`experiments/jfm_oracle_pilot.py\` uses the repository's analytical Gaussian volatility-posterior quadrature and Curran's arithmetic-average option approximation. **Here \(C^\star\) is a Curran-model price at a known generating volatility, not an exact Asian-option price.** This first stage isolates parameter estimation under a fixed pricing approximation. It records a Taylor-curvature rule at declared \$/bbl tolerances (0.001, 0.005 and 0.01), false reassurance, unnecessary integration, and approximate posterior-price interval coverage over fixed-parameter repeated samples.

Separately, the same pilot generates multi-futures Brownian paths with fixed mapping of fixing dates to underlying contracts and correlation stress \(\rho\in\{1,0.75,0.50\}\). The model uses \(\sqrt\rho\,dW^0+\sqrt{1-\rho}\,dW^u\); each futures contract reuses its own idiosyncratic driver at all fixings. The \(\rho=1\) control equals a single common factor. It records **antithetic-pair Monte Carlo standard errors** and paired-difference standard errors. The simulated reference is NOT exact, and small errors must not be overinterpreted if they are comparable to Monte Carlo noise.

### Execution stages and stop gates

1. **Pilot only:** Run the small, deterministic configuration. Inspect every CSV, the manifest and \`NOTES.md\`. Verify correct contracts-to-fixings correlation mapping, plausible option prices, posterior quadrature stability and MC standard errors. Preserve/push **all outputs**, including failures and seeds.
2. **Numerical gate:** Independently assess Curran approximation bias against high-precision payoff Monte Carlo at \(\rho=1\); refine the volatility grid and MC paths until numerical error is below the smallest difference discussed. If insufficient, report inconclusive rather than strong conclusions.
3. **Design freeze:** Only after inspecting the pilot, fix scenarios, seeds, pricing tolerances, evaluation metrics, repeated-sample coverage definitions, and the development/confirmatory split. No using held-out results to select thresholds or scenarios.
4. **Controlled final experiment:** Reuse the verified code, compare correct-specification versus correlation stress with independent reference replications and report paired MC uncertainty. Do **not** claim market correlation was estimated or trading performance validated.
5. **Editorial incorporation:** Add results to the JFM LaTeX and produce two simple figures only if results clarify a nontrivial boundary. Otherwise present this as a concise technical appendix. Never invent results before running the program.

### Local commands

Run from a repository checkout containing this change:

~~~powershell
conda activate asian-options
python paper/build.py --check

# Use only archived derived results; never rerun the original 10-million study:
python -m scripts.build_publication_figures --journal jfm --figures 1 2 3 4 --formats pdf png svg

# JFM draft PDF; never overwrites REMEF's Word files:
python paper/build.py
Start-Process .\paper\espino_2026_bayess-on-wti.pdf

# Small bounded development pilot (not final scientific evidence):
python -m experiments.jfm_oracle_pilot --quick
~~~

Preserve the new \`figures/jfm/\` vector figures and ALL \`results/analysis/jfm_oracle_pilot/<run-id>/\` CSV, JSON and notes in GitHub. No paid or outside market data are needed for these commands. Do not launch heavy computational workflows from push CI; those must remain manual-only.

### Remaining publication gates

- Visually inspect all pages, native LaTeX math, bibliography, tables and figure legibility. Verify Wiley's **current** submission instructions, final class/font requirements and actual paper width before considering the artwork print-ready. A legacy Wiley NJDv5 template being buildable is not proof of current format compliance.
- Resolve market-data timestamp/vintage and dissemination uncertainties; acknowledge the 15 valuation dates and zero-volume settlements. Do not label the settlement-proxy comparison as independently executable pricing.
- Complete independent numerical reference controls before discussing the pilot or tolerance decisions in a submission.
- The new approach is **JFM Paper A**. JCM Paper B remains a distinct, unvalidated proposal and must not reuse Paper A evidence as new results.
