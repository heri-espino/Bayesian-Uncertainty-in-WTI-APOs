"""Bounded independent-seed confirmatory study; outputs are not auto-cleared for publication.
Uses the repository's one-factor Curran approximation and Gaussian sigma posterior,
with independent payoff references supplied by numerical_reference.py.
"""
import csv, hashlib, json
from pathlib import Path
import numpy as np
import pandas as pd
from scipy.optimize import brentq
from scipy.special import logsumexp, ndtr
from scipy.stats import beta
from experiments.jfm_numerical_reference import TIMES,FORWARD,RATE,CONTRACT

SEED=20261219
VOL=(.2,.5); SIZES=(21,252); STRIKES=(95.,100.,105.)
REPS=40
TOLS=(.001,.005,.01)
SIGMA_GRID=np.linspace(.02,1.5,513)

# Independent reproduction of repository's production Curran formula. Unit-check
# against six pilot-run prices to identify discrepancies before interpretation.
def curran(sigma,strike):
 t=TIMES;n=t.size
 mu=np.log(FORWARD)-.5*sigma*sigma*t
 vari=sigma*sigma*t
 cov=sigma*sigma*np.minimum.outer(t,t)
 mu_g=float(mu.mean()); v_g=float(cov.mean());sd=np.sqrt(v_g)
 cov_g=cov.mean(axis=1); b=cov_g/v_g
 cond_var=np.maximum(vari-cov_g**2/v_g,0.)
 def log_cond(x): return float(logsumexp(mu+b*(x-mu_g)+.5*cond_var)-np.log(n))
 xstar=brentq(lambda x: log_cond(x)-np.log(strike),mu_g-max(10*sd,.25),mu_g+max(10*sd,.25))
 d1=(mu_g+cov_g-xstar)/sd;d0=(mu_g-xstar)/sd
 return float(np.exp(-RATE*t[-1])*(np.mean(FORWARD*ndtr(d1))-strike*ndtr(d0)))


def posterior_weights(grid,n,sums,sumsq,dt=1/252):
 # Analytically integrate N(0,1) drift prior; InvGamma(2,.1) sigma prior.
 s=grid; sr=sums;ss=sumsq; v=s*s*dt;shift=.5*s*s*dt
 sum_y=sr+n*shift; ss_y=ss+2*shift*sr+n*shift**2
 rr=dt*dt
 logdet=n*np.log(v)+np.log1p(rr*n/v)
 corr=rr/(v*(v+rr*n))
 lp=-.5*(logdet+ss_y/v-corr*sum_y**2)-3*np.log(s)-.1/s
 trapez=np.full_like(s,grid[1]-grid[0]);trapez[[0,-1]]*=.5
 raw=np.exp(lp-lp.max())*trapez
 return raw/raw.sum()


def qtile(grid,weights,prices,p):
 # For these call options, Curran price is monotone in sigma across the grid.
 # Interpolate the posterior CDF between nodes rather than midpoint point masses.
 w=weights.copy();q=np.full_like(w,grid[1]-grid[0]);q[[0,-1]]*=.5
 dens=w/q
 masses=.5*(dens[:-1]+dens[1:])*np.diff(grid)
 cdf=np.r_[0.,np.cumsum(masses)];cdf/=cdf[-1]
 return float(np.interp(p,cdf,prices))


def main():
 out=Path('results/analysis/jfm_confirmatory');out.mkdir(parents=True,exist_ok=True)
 source=pd.read_csv(out/'reference_prices.csv')
 reference={(float(row.sigma_true),float(row.strike),float(row.rho)):float(row.qmc_reference_price) for row in source.itertuples()}
 from bayesian_asian_options.asian_futures_pricing import curran_arithmetic_futures_option
 for sigma in VOL:
  for strike in STRIKES:
   original=curran_arithmetic_futures_option(realized_fixings=np.empty(0), forward_fixings=np.full(8,FORWARD), fixing_times=TIMES, strike=strike, sigma=sigma,discount_factor=np.exp(-RATE*TIMES[-1]))
   assert abs(curran(sigma,strike)-original)<1e-9,(sigma,strike)
 print('Curran prices: six production-function cross-checks within 1e-9')
 assert all(np.all(np.diff(np.array([curran(s,k) for s in SIGMA_GRID]))>=-1e-9) for k in STRIKES)
 curves={k:np.array([curran(s,k) for s in SIGMA_GRID]) for k in STRIKES}
 rows=[]
 rng=np.random.default_rng(SEED)
 for true in VOL:
  for n in SIZES:
   r=rng.normal(size=REPS)
   chisq=rng.chisquare(n-1,size=REPS)
   mu=(.08-.5*true**2)/252
   var=true**2/252
   m=mu+np.sqrt(var/n)*r
   sumr=n*m; ss=var*chisq+n*m*m
   for j in range(REPS):
    w=posterior_weights(SIGMA_GRID,n,sumr[j],ss[j]); mean_sig=float(w@SIGMA_GRID)
    for strike in STRIKES:
     curve=curves[strike];pi=float(w@curve); pm=float(np.interp(mean_sig,SIGMA_GRID,curve))
     lo=qtile(SIGMA_GRID,w,curve,.025);hi=qtile(SIGMA_GRID,w,curve,.975)
     interval_width=hi-lo;gap=abs(pi-pm)
     for rho in (1.,.75,.5):
      oracle=reference[true,strike,rho]
      row=dict(sigma_true=true,n_obs=n,strike=strike,replication=j,rho=rho,
          price_pi=pi,price_pm=pm,abs_gap=gap,
          qmc_reference=oracle,pm_abs_error=abs(pm-oracle),pi_abs_error=abs(pi-oracle),
          posterior_interval_low=lo,posterior_interval_high=hi,
          posterior_interval_width=interval_width,
          qmc_reference_covered=int(lo<=oracle<=hi))
      for tol in TOLS:
       row[f'gap_small_{tol}']=int(gap<=tol)
       row[f'false_reassurance_estimation_{tol}']=int(gap<=tol and abs(pm-oracle)>tol)
      rows.append(row)
 df=pd.DataFrame(rows)
 df.to_csv(out/'confirmatory_rows.csv',index=False,float_format='%.14g')
 a=[]
 for (sigma,n,rho),x in df.groupby(['sigma_true','n_obs','rho'],sort=True):
  # 40 independent returns datasets, each with three correlated strikes.
  dates=x.groupby('replication').agg(
     mean_abs_gap=('abs_gap','mean'),pm_mae=('pm_abs_error','mean'),
     coverage=('qmc_reference_covered','mean'),width=('posterior_interval_width','mean'),
     false_small_gap_005=('false_reassurance_estimation_0.005','mean')
   )
  a.append(dict(sigma_true=sigma,n_obs=n,rho=rho,historical_replications=len(dates),
    state_rows=len(x),mean_abs_gap=x.abs_gap.mean(),pm_mae=x.pm_abs_error.mean(),
    interval_coverage=x.qmc_reference_covered.mean(),mean_interval_width=x.posterior_interval_width.mean(),
    false_reassurance_005_per_state=x['false_reassurance_estimation_0.005'].mean(),
    coverage_cluster_se=dates.coverage.std(ddof=1)/np.sqrt(len(dates)),
    pm_mae_cluster_se=dates.pm_mae.std(ddof=1)/np.sqrt(len(dates))))
 ag=pd.DataFrame(a);ag.to_csv(out/'confirmatory_summary.csv',index=False,float_format='%.14g')
 print(ag.to_string(index=False,float_format=lambda v: f'{v:.6f}'))
 for rho,x in df.groupby('rho'):
  print('RHO',rho,'count',len(x),'gapMAE',x.abs_gap.mean(),'PM_MAE',x.pm_abs_error.mean(),'COVERAGE',x.qmc_reference_covered.mean())
  for tol in TOLS:
   small=x[x.abs_gap<=tol];cnt=int((small.pm_abs_error>tol).sum())
   print('  tol',tol,'small',len(small),'false',cnt,'rate',cnt/len(small) if len(small) else np.nan)
 manifest=dict(status='BOUNDED_INDEPENDENT_SEED_EXPLORATORY_CONFIRMATORY_NOT_EDITORIALLY_CLEARED',
   seed=SEED,repetitions=REPS,original_pilot_seed=20261103,
   sigma_grid_points=len(SIGMA_GRID),historical_sizes=SIZES,volatilities=VOL,strikes=STRIKES,
   rho=(1.,.75,.5),qmc_reference='randomized Sobol independent payoff with exact geometric control',
   reuse='three strikes from each history; do not use naive binomial SE over rows',
   limitation='Curran posterior prices versus independent QMC truth; pilot-informed, not preregistered study design',
   files={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in (out/'confirmatory_rows.csv',out/'confirmatory_summary.csv',out/'reference_prices.csv')})
 (out/'confirmatory_manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')

if __name__=='__main__':main()
