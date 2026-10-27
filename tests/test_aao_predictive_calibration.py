"""Synthetic leakage and calibration tests; no paid data/provider calls."""
from __future__ import annotations
import numpy as np
import pandas as pd
import pytest
from experiments.wti_aao_predictive_calibration import (
    POINTS, load_contracts, weighted_quantile, interval_from_past,
    interval_score, execute, month_block_ci,
)


def fixture(n_days=35):
    rows=[]
    for i, date in enumerate(pd.bdate_range("2024-09-02",periods=n_days)):
        for method in POINTS:
            for side in ("C","P"):
                for j, strike in enumerate([60.,70.,80.]):
                    forward=70.
                    # Date-varying error, same sample for all point methods.
                    err=(.22*np.sin(i*.41+j)-.07)+(.01 if method=="bayes_IV_PI" else 0.)
                    observed=4.0+0.1*j
                    rows.append({"date":date,"expiry":"2025-07-30","side":side,
                        "strike":strike,"actual":True,"method":method,
                        "expected_average":forward,"observed":observed,
                        "predicted":observed+err,"error":err})
    return pd.DataFrame(rows)


def test_weighted_quantile():
    assert weighted_quantile(np.array([4.,1.,8.]),np.ones(3),0.5)==4.
    with pytest.raises(ValueError):
        weighted_quantile(np.array([1.]),np.array([0.]),0.5)


def test_bayesian_interval_vs_empirical_are_finite():
    past=[(f"2024-01-{i:02d}",np.array([.1*i,-.05*i])) for i in range(1,21)]
    for name in ["bayesian_nig","rolling_empirical"]:
        l,u=interval_from_past(past,.90,name)
        assert np.isfinite(l) and np.isfinite(u) and l<u


def test_score_penalizes_outside():
    a=interval_score(np.array([0.,3.]),np.array([-1.,-1.]),np.array([1.,1.]),.9)
    assert a[1]>a[0]


def test_contract_load_validation(tmp_path):
    f=tmp_path/"test.csv.gz"
    fixture().to_csv(f,index=False,compression="gzip")
    d=load_contracts(f)
    assert len(d)==len(fixture())
    assert (d["actual"]==True).all()
    broken=fixture()
    broken.loc[0,"error"]=1e6
    broken.to_csv(f,index=False,compression="gzip")
    with pytest.raises(ValueError, match="inconsistent"):
        load_contracts(f)


def test_date_leakage_prevention_and_support(tmp_path):
    f=tmp_path/"test.csv.gz"
    fixture().to_csv(f,index=False,compression="gzip")
    d=load_contracts(f)
    manifest,tables=execute(d,min_dates=5,window_dates=20,bootstrap=99,
                             test_start="2024-10-01")
    assert manifest["n_source_actual_contract_dates"]==35*6
    assert manifest["n_eligible_valuation_dates"]>=20
    sc=tables["summary_by_split"]
    assert set(sc.method)==set(POINTS)
    assert set(sc.calibrator)=={"bayesian_nig","rolling_empirical"}
    daily=tables["daily_actual_scores"]
    assert daily.groupby(["split","date","level","calibrator"]).method.nunique().eq(3).all()
    assert daily["coverage"].between(0,1).all()
    assert (daily["mean_width"]>0).all()
    assert (daily["mean_interval_score"]>0).all()
    # Replacing future outcomes must NOT alter already issued intervals.
    later=d.copy()
    chosen=later.date.max()
    later.loc[later.date==chosen,"error"]+=1.
    later.loc[later.date==chosen,"predicted"]+=1.
    _,changed=execute(later,min_dates=5,window_dates=20,bootstrap=99,test_start="2024-10-01")
    old=daily[daily.date!=chosen.strftime("%Y-%m-%d")].sort_values(list(daily.columns)).reset_index(drop=True)
    new=changed["daily_actual_scores"]
    new=new[new.date!=chosen.strftime("%Y-%m-%d")].sort_values(list(new.columns)).reset_index(drop=True)
    pd.testing.assert_frame_equal(old,new)


def test_bootstrap_outputs():
    d=pd.DataFrame([{"date":x,"calibrator":model,
                     "mean_interval_score":1. if model=="bayesian_nig" else 2.}
                    for x in pd.date_range("2025-01-01",periods=100,freq="3D")
                    for model in ("bayesian_nig","rolling_empirical")])
    ans=month_block_ci(d,"bayesian_nig","rolling_empirical",n_boot=199)
    assert ans.iloc[0].mean_daily_interval_score_improvement==pytest.approx(1.)
    assert ans.iloc[0].ci_low==pytest.approx(1.)
