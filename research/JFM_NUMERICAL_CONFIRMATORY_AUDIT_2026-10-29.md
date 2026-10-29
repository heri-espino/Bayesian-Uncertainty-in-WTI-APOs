# JFM numerical reference and independent-seed follow-up — 2026-10-29

**Status: bounded, pilot-informed follow-up; NOT preregistered and NOT automatically cleared for publication.** This report is not the 10-million-history simulation and is not the Databento study. No paid or vendor market data were used.

## Sources, code, and outputs

The pilot was run on Windows runner `PCAG103A-15` via [workflow run #40822904143](https://github.com/heri-espino/Bayesian-Uncertainty-in-WTI-APOs/actions/runs/40822904143) and was reviewed in merged PR #126. The original five-file pilot artifact is archived as `results/analysis/jfm_oracle_pilot/recovered_original_pilot_20261029.zip` (unchanged ZIP bytes).

The independent numerical-reference implementation is `experiments/jfm_numerical_reference.py`. The independent-seed historical follow-up is `experiments/jfm_confirmatory.py`. Original full follow-up rows, QMC prices, reproducibility manifest, quadrature snapshots, and console log are archived as `results/analysis/jfm_confirmatory/jfm_confirmatory_execution_20261029.zip`; summary and QMC reference CSVs are also committed separately. Both scripts use SciPy and NumPy; the second also cross-checks its reimplemented Curran formula against the package's production Curran pricer. Source files and outputs are versioned rather than left only in ephemeral artifacts.

## Independent payoff reference (step 2)

The numerical oracle **simulates the actual arithmetic average payoff rather than using Curran conditioning**, with randomized scrambled Sobol normal shocks and antithetic paths, using an *exact analytical geometric-average call* as a control variate. Ten independent scrambles of 2^14 antithetic pairs per scramble were used for correlation stress (rho=0.75 and 0.50); 12 independent scrambles of 2^16 pairs per scramble were used for rho=1. Each futures contract retains the same idiosyncratic Brownian driver across its two fixings. The six (sigma, strike) combinations use sigma=0.20 or 0.50 and strike=95,100,105, with 8 fixings on business days 7,14,...,56. These are small, fixed tests of the maintained payoff model, not an expanding scenario search.

At rho=1, comparing the QMC payoff reference with the independent Curran formula reproduces six of six original pilot Curran prices to better than 1e-9. The maximum absolute **Curran pricing approximation bias** across the six scenarios is **$0.0009215/bbl**, while the largest 95% QMC reference interval halfwidth at rho=1 is **$0.0001536/bbl**. This makes it unsafe to treat all differences at the smallest $0.001/bbl threshold as exact-payoff effects. Under rho=0.50 the largest QMC 95% reference halfwidth is $0.001023/bbl, but the model-correlation price differences are on the order of tenths of a dollar/bbl.

The rho=1 Curran bias is systematically negative in these six scenarios. The one-factor control thus quantifies a *small but nonzero* pricing-approximation error rather than assuming zero model bias.

## Independent-seed fixed follow-up (step 3)

Pilot-informed settings were frozen within this run: generating volatility {0.2, 0.5}, historical length {21,252}, strike {95,100,105}, vol-grid 513, price tolerances {$0.001,$0.005,$0.010}/bbl, and correlation weights rho={1,0.75,0.50}. **The historical random seed is 20261219**, different from the pilot seed 20261103. Forty independent histories per (generating sigma, n) cell give **160 independent return histories**, each repriced at three strikes and three correlation references (1,440 option-scenario rows). Three strikes *reuse the same history*; the three correlation references *also reuse it*. The posterior and PI/PM prices assume rho=1 throughout; the independent payoff reference varies by rho.

| True futures-correlation weight | Mean absolute PI–PM gap (USD/bbl) | Mean PM error vs QMC payoff oracle (USD/bbl) | Nominal 95% price-interval coverage vs QMC | Stratified history-bootstrap 95% coverage interval |
| ---: | ---: | ---: | ---: | ---: |
| rho=1.00 | 0.003709 | 0.318736 | 95.00% | [91.25%, 98.13%] |
| rho=0.75 | 0.003709 | 0.451675 | 65.21% | [58.33%, 71.88%] |
| rho=0.50 | 0.003709 | 0.721005 | 31.88% | [26.88%, 36.88%] |

Bootstrap confidence intervals resample historical replications *within each (sigma,n) cell*, not individual strikes, and aggregate equally over four design cells. This reflects the intentional repeated-strike/correlation dependence. The finite-sample interval frequencies are **frequentist checks against a fixed-parameter payoff reference**, not forecasts of future settlement prices, traded option prices, or trading profitability.

Under rho=1, among the **327/480** cases where |PI–PM|≤$0.005/bbl, **315** had |PM−QMC oracle|>$0.005/bbl, i.e. **96.33%** of these seemingly reassuring comparisons. The analogous counts under rho=0.75 and rho=0.50 were 324/327 and 327/327. These are **conditional false-reassurance proportions** about total price error, not the earlier Taylor-approximation false-reassurance indicator (which tests only prediction of the PI–PM gap). These selected tight price tolerances make the mismatch partly mechanical; do not extrapolate the proportions to realistic commercial trading risks or markets.

## Numerical grid qualification

For four representative at-the-money histories, 513-versus-1025 point volatility grids change posterior mean prices (PI) by at most ~4e-9 and plug-in prices (PM) by ~1.8e-7 USD/bbl. **The posterior interval endpoints converge more slowly**: at most **$0.002281/bbl** discrepancy between those grids and up to $0.017815/bbl for 257 versus 1025 in these checks. These are **not** negligible for interpreting a $0.001 pricing tolerance, although they are small compared with the posterior interval widths. A full coverage-sensitivity sweep using finer grids is still required before describing the interval coverage as numerically converged.

We therefore interpret the follow-up's coverage as a numerically *provisional* rate; do **not** claim exact 95% calibration or compare differences smaller than the estimated quadrature/MC resolution.

## Independence and research boundaries

- The reference payoff calculation is independent of Curran's conditioning but assumes the **same stylized lognormal futures dynamics**, with a controlled, hypothetical correlation stress. It is not validation of an exchange settlement algorithm.
- New historical draws (seed 20261219) are independent of the development pilot's draws (20261103), but the study design is **pilot-informed rather than preregistered**.
- The high-precision one-factor reference has sub-$0.0002/bbl halfwidth, yet Curran bias and interval-quantile grid effects remain; the smallest threshold must be interpreted cautiously.
- The prices studied here are **synthetic model prices**, not Barchart/Databento settlements or actual transactions.
- A change in coverage under rho stress demonstrates sensitivity *within this stylized model*, not an estimate of real-market correlation misspecification.

## Manuscript and figure gates (step 4)

**Scientific:** Do not insert the 95% / 65% / 32% coverage values in the main JFM manuscript as a confirmed result until the coverage-sensitivity checks on denser sigma grids are complete and the independently generated artifacts have been reproduced with `asian-options` in the canonical repository. A short appendix could identify this as an illustrative controlled stress test with numerical limitations.

**Typographic:** The repo already uses the exact Wiley staged LaTeX preamble through AwesomeFigures `af.paper()` for JFM figures. The committed JFM PDFs were built *before* that integration. The heavy build remains deliberately **manual-only**: [GitHub Actions build-paper](https://github.com/heri-espino/Bayesian-Uncertainty-in-WTI-APOs/actions/workflows/build-paper.yml) → **Run workflow** on `main` with `PCAG103A-15` online and its existing `asian-options` environment. The job builds all four PGF/XeLaTeX PDFs and Wiley reviewer paper, verifies actual font embedding and dimensions, then uploads a 30-day artifact. Visually inspect all pages before committing output PDFs/PGF/manifest. **This report does not claim that the runner was dispatched or that the old figures were replaced.**

## Reproduction

At the repository root (with the conda environment loaded):

```powershell
conda activate asian-options
python -m experiments.jfm_numerical_reference
python -m experiments.jfm_confirmatory
```

The independent numerical reference uses the frozen fixed scenario design; these scripts should be run manually, not from push-triggered CI. Additional scenario expansion or multiple-seed searches must be disclosed separately and must not be used to manufacture a larger sample.
