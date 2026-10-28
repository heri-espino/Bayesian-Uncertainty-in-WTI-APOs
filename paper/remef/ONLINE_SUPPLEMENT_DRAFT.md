# Online supplement — working reviewer-safe draft

**Companion manuscript:** Posterior Integration and Volatility Inputs in WTI Asian Options

**Status:** Scientific draft, not verified as accepted supplementary material by the journal. No author-identifying website, no market-data contract rows and no assertion of vendor redistribution permission. The earlier archival supplement is preserved separately.

## S1. Posterior integration and price uncertainty

For the original one-factor Asian option pricing model, the posterior-integrated price is the posterior mean of conditional option prices, whereas the plug-in price evaluates the same conditional pricing function at posterior-mean volatility:

\[
C_{\mathrm{PI}}=E[C^Q(\sigma)\mid\mathcal D],\quad
C_{\mathrm{PM}}=C^Q(E[\sigma\mid\mathcal D]).
\]

Locally, the difference is approximately one half of option-price volatility curvature multiplied by posterior volatility variance. This is a POINT-PRICE correction, not a credible interval for transaction prices. The posterior distribution of conditional model prices is another object. Neither is a predictive distribution of the actual Asian payoff.

The synthetic experiment includes 10 million simulated return histories (seed 2468) and 5,880 reported scenario cells. The maximum simulated absolute PI–PM difference is about USD 0.1565 for the normalized USD 100 forward, the largest cell 99th percentile is 0.1273, and the curvature–variance approximation has a reported scenario-cell correlation of approximately 0.9995. These are within-model mathematical findings, not independent market observations. Evidence: results/analysis/massive_mechanism_map/6e23d5aabc519982/mechanism_map_report.json and figures/publication/ten_million/figure_manifest.json. The older 175,000-history run is not the same experiment.

## S2. Original futures-curve-based Barchart/LO exercise

The original empirical design uses a one-factor futures pricing process, partially fixed daily first-nearby WTI futures settlements, curve-based future fixing levels and a Curran pricing approximation. The Barchart end-of-day Latest column is treated as a settlement *proxy*, not independently certified as a final exchange trade. Historical return proxies include both continuous/front-month and contract-reconstructed CL changes.

The main reported forward-in-time comparison uses 2,381 contract-date rows across only 15 valuation dates. On identical rows, historical PI MAE/RMSE are 2.6187/3.4090 USD/bbl; reconstructed first-nearby historical PI MAE/RMSE are 2.6468/3.4451; the prior-day fitted AAO IV smile has reported MAE/RMSE 0.1075/0.1594. The first two sets of error arithmetic were recomputed from saved individual rows. All 2,381 prior-day and expanding fitted-smile rows were independently reaggregated, including exact reconstruction of their 4,762 fitted volatilities from 2,574 archived source-IV inputs. This is an output-level audit, not certification of the original vendor publication time.

The same-contract previous-IV test contains 2,366 matched eligible rows with MAE 0.099156 USD/bbl, versus 0.107417 USD/bbl for the fitted smile on exactly the same rows. The contract-level carry values, joins and original date-field precedence were independently reconciled. The external vanilla LO-IV matched subset has 253 targets on 10 valuation dates and MAE 0.4464 historical PI, 0.1559 prior LO IV and 0.1676 prior AAO IV. Those three values were recomputed from saved common-support contract errors, but underlying original option-tree vintages and time cutoffs remain to be audited.

**October 2026 means option EXPIRY, not October valuation dates.** The separate posterior-price sample has 310 contract-date rows across 12 evaluation dates, August 25–September 10, 2026. Saved individual rows yield PI RMSE 0.517741, PM RMSE 0.518337, mean absolute PI–PM 0.000745132, and mean 95% posterior conditional model-price width 0.273272684 USD/bbl.

These samples contain many contract rows but few date clusters. Date-cluster bootstrap analysis is appropriate as a sensitivity check; it does not remove serial dependence or certify market-time availability. Exchange-generated theoretical marks, vendor revisions, and zero reported volume weaken conclusions about prices achievable in trading.

Sources: results/analysis/wti_first_nearby/pricing_holdout_comparison.csv; results/analysis/wti_extended_forward/forward_q_validation/forward_q_error_summary.csv; results/analysis/wti_external_vanilla_q_validation/surface_common_support_paired_errors.csv; results/wti_apo_empirical/YYYY-MM-DD_202610/contract_pricing.csv; paper/remef/SCIENTIFIC_AUDIT_FINDINGS_2026-10-27.md.

## S3. Separate 81-month Databento conditional experiment

The expanded AAO option-definition and settlement-statistics archive does not itself supply the CL first-nearby daily fixing path or a contemporaneous independently observed futures curve. Experiments 003–005 therefore use a different, reduced-form lognormal terminal-average price approximation. Expected average and discount are derived from other *same-date* AAO put/call parity strikes, excluded from target-strike pricing. The historical Bayesian volatility proxy tracks prior changes in these parity-implied average forwards rather than direct physical-measure CL futures returns. It is not scientifically valid to pool its contract-date rows with the earlier structural one-factor/Curran exercise.

**Experiment 003:** 111,585 eligible contract-date target observations across 189 valuation dates, of which 97,341 are actual-flagged and 14,244 theoretical-flagged. The actual-only MAE/RMSE for previous-date AAO IV are 0.218420/0.297907 USD/bbl, compared with 0.804044/1.137151 for historical forward-average-change Bayesian PI and 0.806818/1.140106 for matched PM. These results condition on contemporaneous disjoint parity anchors and are NOT an independent CL-path risk-neutral Asian pricing forecast.

The retrospective volatility-gap inversion, **never used as a forecasting feature**, gave average current target option IV 30.97%, previous-date AAO IV 30.88%, and a historical-proxy Bayesian PM price-equivalent sigma 26.68% across 1,689 eligible expiry-date groups. This is not a clean physical-versus-risk-neutral variance-risk-premium estimate.

**Experiment 004:** in the inspected 2025–September 2026 subset on 47,718 actual-flagged target rows across 88 dates, unchanged lagged IV MAE is 0.208924 USD/bbl versus 0.209830 for Bayesian market-IV PI. The equal-date mean daily MAE improvement of PI against lagged IV is -0.001002 USD/bbl, with calendar-month block 95% percentile interval [-0.003307, +0.000820]. There is no reliable incremental Bayesian market-IV integration gain on that inspected sample.

**Experiment 005:** a subsequent historical-residual Bayesian normal-inverse-gamma interval model is NOT the same as the posterior volatility-price distribution. After rolling calibration warm-up, 89,696 actual targets over 174 dates remain. In 2025–September 2026, nominal 90% residual-mark intervals around Bayesian IV PI covered 86.43% under Bayesian NIG versus 84.72% using date-balanced empirical residual quantiles; nominal 95% intervals covered 90.11% versus 90.66%. March and April 2026 Bayesian nominal 90% coverage fell to 59.0% and 56.9%, respectively. Neither calibration method maintains uniform nominal coverage across market regimes. No causal explanation for the failure has been established.

The 2025–2026 holdout in Experiments 004/005 has been inspected and is not a genuinely untouched validation period for later model tuning.

Sources: the experiment manifest, method metrics and inferential CSVs under results/analysis/wti_aao_databento_only/full_2023_2026/, results/analysis/wti_aao_market_iv_bayes/experiment004/ and results/analysis/wti_aao_predictive_calibration/experiment005/. Independent research handoffs reside under research/experiments/experiment003/, experiment004/ and experiment005/.

## S4. Market-mark interpretation and disclosure

CME Clearing introduced a Curran-based end-of-day AAO valuation process effective May 18, 2020 (Clearing Advisory 20-198). Hence fitting lagged option implied volatility to reported marks can partly reproduce a persistent exchange valuation methodology rather than predict separately observed trades. The standard AAO price quotation increment is USD 0.01/bbl; the original average absolute PI–PM difference USD 0.000745/bbl is considerably smaller. Small numerical gains do not establish executable arbitrage or hedge profitability.

The original Barchart/LO and newer Databento approaches have different input providers, maturity support, price approximations, volatility estimation objects, as-of assumptions and target definitions. They are presented as SEPARATE studies addressing a shared methodological question. The larger Databento panel does not retroactively enlarge the original Curran 15-date sample.

## S5. Independent checks and release requirements

Saved-row error arithmetic is independently checked for the original 310-row October-expiry sample, original 2,381-row historical baseline and 253-row LO common-support subset. Completed synthetic-run statistics are checked against a saved run manifest and figure metadata, not independently regenerated. The original fitted-smile and same-contract lagged-IV contract-level numerical reconciliations are COMPLETE at the archived output-and-date-field level (see IV_NUMERICAL_AND_ASOF_AUDIT_2026-10-27.md). They do not establish provider first-publication times, record vintages, vendor permissions or independently executable trade prices. Exact quote/fixing/rate timestamp vintages, legal data redistribution rights (including public Git histories), actual trades versus theoretical exchange marks and executable trading costs remain OPEN.

Local integrity and numerical audit commands (require a complete authorized checkout, no provider calls):

    python -m scripts.audit_remef_science
    python -m scripts.audit_remef_forward_iv
    python -m pytest tests/test_remef_build.py tests/test_remef_manuscript_scientific_integrity.py -q
    python paper/remef/build.py --check

Final DOCX files must be rendered and reviewed for <=25-page REMEF limit, genuinely editable formulas/tables, figure legibility, bilingual content, APA references and full anonymization. Submission or public data release requires separate author approval and journal/vendor rights verification.

**Editorial status:** Companion research draft, not a claim of approval, a signed rights submission, or a substitute for the journal's latest author instructions.
