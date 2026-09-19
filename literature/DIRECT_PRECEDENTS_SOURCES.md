# Direct-precedent source manifest

These are the verified legal/free sources for the direct-overlap papers identified after the
eight-paper synthesis. The repository connector used for this update can write UTF-8 text but
cannot transfer arbitrary external binary PDFs into GitHub, so this file records the canonical
download source and normalized target filename. Once the PDFs are placed in `literature/pdf/`,
the existing extraction pipeline should generate the corresponding Markdown.

| Paper | Verified free source | Target filename | Status |
|---|---|---|---|
| Shiraya & Takahashi (2011), *Pricing Average Options on Commodities* | University of Tokyo working-paper PDF: `https://park.itc.u-tokyo.ac.jp/takahashi-lab/WPs/p35.pdf` | `shiraya_2011_pricing-average-options-commodities.pdf` | Full working paper verified; same core study as the JFM article |
| Gupta & Reisinger (2014), *Robust Calibration of Financial Models Using Bayesian Estimators* | Oxford author PDF: `https://people.maths.ox.ac.uk/~reisinge/Publications/RobustnessPaper.pdf` | `gupta_2014_robust-calibration-bayesian-estimators.pdf` | Full author manuscript verified |
| Gan, Wang & Yang (2020), *Machine Learning Solutions to Challenges in Finance* | Kent accepted manuscript: `https://kar.kent.ac.uk/79670/1/asian-option-ml-revision202001.pdf`; SSRN: `https://ssrn.com/abstract=3446042` | `gan_2020_machine-learning-asian-option-pricing.pdf` | Accepted manuscript is CC BY-NC-ND; full-text WTI APO empirical section verified via repository/search index |
| Guillaume & Schoutens (2015), *Bid-Ask Spread for Exotic Options under Conic Finance* | University of Antwerp PDF: `https://repository.uantwerpen.be/docman/irua/4fba6c/23954e2e.pdf`; Springer chapter is Open Access | `guillaume_2015_bid-ask-spread-exotic-options-conic-finance.pdf` | Open-access chapter verified |

## Why the first three are submission-critical

### Shiraya & Takahashi (2011)

This is the closest direct WTI APO precedent found so far. The working paper states that WTI
average-price options are valued using parameters calibrated to more liquid American vanilla
options on WTI futures, models the actual first-nearby roll across two consecutive futures
maturities, and compares Heston / extended lambda-SABR average-option estimates with CME
settlements.

**Implication:** this paper cannot claim to be the first contract-consistent structural valuation
of WTI APOs, nor the first to propose vanilla-WTI calibration as an external Q-information source.

### Gupta & Reisinger (2014)

The paper casts derivative-model calibration as a Bayesian inverse problem, obtains a posterior
over model parameters, and translates that posterior into a distribution / Bayesian estimate of
exotic derivative prices.

**Implication:** posterior propagation to exotic prices is not itself novel. The present paper's
increment is the PI-versus-PM mechanism, the posterior-dispersion times pricing-curvature map,
and the empirical comparison with volatility specification in WTI APOs.

### Gan, Wang & Yang (2020)

The paper applies deep learning to arithmetic Asian pricing and evaluates it on real WTI Average
Price Option data downloaded from Barchart, including several WTI APO maturities.

**Implication:** use of Barchart WTI APO data is not novel. The present paper differs by using a
structural P/Q decomposition, explicit posterior parameter uncertainty, contract mechanics,
simulation/mechanism experiments, and forward volatility-specification tests.

## Secondary precedent

Guillaume & Schoutens (2015) is useful for the broader distinction between parameter/calibration
uncertainty and model uncertainty. It explicitly cites Bayesian propagation of calibration
uncertainty to exotic prices as one approach among several and studies how plausible calibration
procedures induce different risk-neutral measures and exotic valuations.
