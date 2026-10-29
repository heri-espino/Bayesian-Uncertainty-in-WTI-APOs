"""Independent scrambled-Sobol + exact geometric-control Asian-option reference.
No reference to the project's Curran approximation.
"""
import numpy as np
from scipy.stats import qmc
from scipy.special import ndtr, ndtri
from scipy.stats import t as student_t

TIMES=np.arange(1,9,dtype=float)*7/252
CONTRACT=np.repeat(np.arange(4),2)
FORWARD=100.
RATE=0.03


def exact_geometric_call(sigma,strike,rho=1.0):
    t=TIMES
    corr=rho+(1-rho)*(CONTRACT[:,None]==CONTRACT[None,:])
    covariance=sigma*sigma*np.minimum.outer(t,t)*corr
    mu=np.mean(np.log(FORWARD)-.5*sigma*sigma*t)
    var=np.mean(covariance)
    g_mean=np.exp(mu+.5*var)
    d=(mu-np.log(strike))/np.sqrt(var)
    return np.exp(-RATE*t[-1])*(g_mean*ndtr(d+np.sqrt(var))-strike*ndtr(d))


def qmc_reference(sigma,strike,rho,seed=912781,pow2=14,scrambles=10):
    """Independent scrambles yield SE for the controlled arithmetic price.

    Same Brownian shocks drive arithmetic and geometric payoffs; each contract
    retains its own idiosyncratic Brownian path across all of its fixing dates.
    Antithetic +/- normal shocks reduce variance. Geometric control price is exact.
    """
    dt=np.diff(np.r_[0.,TIMES]); sqrt_dt=np.sqrt(dt)
    geom=exact_geometric_call(sigma,strike,rho)
    values=[]
    discount=np.exp(-RATE*TIMES[-1])
    for j in range(scrambles):
        sobol=qmc.Sobol(d=40,scramble=True,seed=seed+1009*j)
        uniforms=sobol.random_base2(pow2)
        normal=ndtri(np.clip(uniforms,np.finfo(float).eps,1-np.finfo(float).eps)).reshape(-1,8,5)
        diffs=[]
        for sign in (1.,-1.):
            w=np.cumsum(sign*normal*sqrt_dt[None,:,None],axis=1)
            drv=np.sqrt(rho)*w[:,:,0] + np.sqrt(1-rho)*w[:,np.arange(8),CONTRACT+1]
            levels=FORWARD*np.exp(-.5*sigma*sigma*TIMES[None,:]+sigma*drv)
            arithmetic=np.mean(levels,axis=1)
            geometric=np.exp(np.mean(np.log(levels),axis=1))
            diffs.append(discount*(np.maximum(arithmetic-strike,0)-np.maximum(geometric-strike,0)))
        values.append(geom+np.mean((diffs[0]+diffs[1])*.5))
    arr=np.asarray(values)
    se=arr.std(ddof=1)/np.sqrt(scrambles)
    tcrit=student_t.ppf(.975,scrambles-1)
    return dict(sigma_true=sigma,strike=strike,rho=rho,qmc_reference_price=arr.mean(),qmc_standard_error=se,ci95_halfwidth=tcrit*se,replicate_min=arr.min(),replicate_max=arr.max(),scrambles=scrambles,sobol_pairs_per_scramble=2**pow2,seed=seed)

if __name__=='__main__':
    import csv,json,pathlib,hashlib
    out=pathlib.Path('results/analysis/jfm_confirmatory');out.mkdir(parents=True,exist_ok=True);rows=[]
    for sigma in (.2,.5):
     for strike in (95.,100.,105.):
      for rho in (1.,.75,.5):
       row=qmc_reference(sigma,strike,rho,pow2=16,scrambles=12) if rho==1.0 else qmc_reference(sigma,strike,rho)
       rows.append(row);print(sigma,strike,rho,round(row['qmc_reference_price'],6),round(row['qmc_standard_error'],7),flush=True)
    path=out/'reference_prices.csv'
    with path.open('w',newline='') as f:
     w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
    print('Saved',path)
