# Extreme synthetic experiment: Draft v2 evidence

Primary run fingerprint: `f497062f0c571126`  
Root seed: `20260909`  
Analysis script: `experiments/analyze_extreme_results.py`

## Design

- 81 scenarios: `n={63,252,1260}`, `sigma0={0.15,0.25,0.40}`, `K/S0={0.8,1.0,1.2}`, `T={0.5,1,2}`.
- 2,000 independent historical samples per scenario.
- 18,000 posterior fits in total.
- 20,000 Metropolis-Hastings iterations per fit, 4,000 burn-in, thinning 2.
- Nine risk-neutral pricing grids, 161 volatility points on `[0.02,1.00]`.
- 2,000,000 paths per pricing-grid point, antithetic sampling, geometric Asian control variate, common random numbers within each contract grid.
- CuPy GPU backend on NVIDIA RTX 4500 Ada Generation.
- 162,000 raw pricing-evaluation rows and 324 committed scenario/method summary rows.

## Main results

Across 81 scenarios, the minimum RMSE is attained by full Bayes in 35 scenarios, MLE in 35, MAP in 11, and posterior-mean plug-in in 0. Winner counts should not be interpreted as a ranking by themselves: posterior-mean plug-in has the smallest average RMSE at `n=63` and `n=252`, despite being narrowly second in many individual cells.

Full Bayes versus posterior-mean plug-in is essentially a point-pricing tie in most regimes. Full Bayes has lower RMSE in 45/81 scenarios and posterior-mean plug-in in 36/81. The median absolute relative RMSE gap is 0.0447%, the median absolute mean-price gap is 0.000736, and the largest mean-price gap in the tested design is 0.018964.

The gap is structured rather than random. Its median absolute magnitude falls from 0.007927 with `n=63`, to 0.001962 with `n=252`, and 0.000391 with `n=1260`. At-the-money (`K/S0=1`) the median gap is only 0.000049, compared with 0.001973 for `K/S0=0.8` and 0.003063 for `K/S0=1.2`. Median gaps also rise with maturity: 0.000268 at `T=0.5`, 0.000736 at `T=1`, and 0.000979 at `T=2`. This pattern is consistent with the second-order approximation in which the full-Bayes correction depends on both posterior variance of volatility and curvature of the pricing functional.

MAP is the least robust point rule in this design. Full Bayes has lower RMSE than MAP in 60/81 scenarios. MAP also has materially larger mean absolute bias: at `n=63`, 0.1046 versus 0.0329 for full Bayes and 0.0323 for posterior-mean plug-in; at `n=252`, 0.0259 versus 0.0065 and 0.0067; at `n=1260`, 0.00434 versus 0.00135 and 0.00111.

MLE and full Bayes are nearly tied. MLE has lower RMSE in 46/81 scenarios versus 35 for full Bayes, but the median difference `RMSE_FB-RMSE_MLE` is only about 0.000024. With long histories (`n=1260`), MLE is the minimum-RMSE rule in 20/27 contract/volatility regimes.

Historical information is quantitatively more important than the choice among full Bayes, posterior mean, and MLE. The median ratio `RMSE(n=63)/RMSE(n=1260)` is approximately 4.67 for full Bayes, 4.66 for posterior mean, 4.50 for MAP, and 4.55 for MLE.

Posterior price intervals are well calibrated in the synthetic design. Across the nine `(n,sigma0)` historical-data cells, empirical 95% coverage ranges from 0.938 to 0.956 with mean 0.9488. Mean Metropolis-Hastings acceptance rates range from 0.301 to 0.458. Acceptance rate alone is not treated as a convergence diagnostic; multichain R-hat/ESS/MCSE or low-dimensional quadrature validation remains pending.

The 2,000-replication extreme run is stable relative to the earlier 1,000-replication research run: across all 324 scenario/method rows, the median absolute RMSE change is 0.000996 and the median absolute relative RMSE change is 1.21%. Mean absolute coverage change is 0.0053.

## Paper interpretation

The Draft v2 conclusion is therefore not that full Bayes universally dominates plug-in pricing. In this Black-Scholes Asian-option laboratory, full posterior integration mainly adds a coherent distribution of theoretical prices. Its effect on the point price becomes most visible when historical information is scarce and the pricing functional is more curved with respect to volatility. With long histories, full Bayes, posterior-mean plug-in, and MLE rapidly converge in practical pricing performance.
