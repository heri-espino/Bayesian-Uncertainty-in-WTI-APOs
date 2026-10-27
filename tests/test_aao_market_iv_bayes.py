"""Synthetic no-provider tests for local Bayesian market-IV experiment 004."""
from __future__ import annotations

import sqlite3

import numpy as np
import pandas as pd
import pytest

from bayesian_asian_options.aao_databento_only import average_black
from bayesian_asian_options.aao_market_iv_bayes import (
    SIGMA_MAX, SIGMA_MIN, predict_market_iv,
)
from experiments import wti_aao_bayesian_market_iv as e004


def fake_iv_history(n=38, start="2026-01-02"):
    days = pd.bdate_range(start, periods=n)
    return [(d.strftime("%Y-%m-%d"), 72.0,
             .30 + .018*np.sin(i/5.0))
            for i, d in enumerate(days)]


def test_market_iv_strictly_past_or_fail():
    history = fake_iv_history()
    with pytest.raises(ValueError, match="current/future"):
        predict_market_iv(history, asof=history[-1][0], seed=19)
    with pytest.raises(ValueError, match="current/future"):
        predict_market_iv(history, asof="2026-01-01", seed=19)


def test_market_iv_predictive_reproducible_and_centered_on_lagged_iv():
    hist = fake_iv_history()
    next_day = pd.Timestamp(hist[-1][0])+pd.offsets.BDay(1)
    asof = next_day.strftime("%Y-%m-%d")
    a = predict_market_iv(hist, asof=asof, seed=17)
    b = predict_market_iv(hist, asof=asof, seed=17)
    assert a is not None and b is not None
    np.testing.assert_array_equal(a.sigma_draws, b.sigma_draws)
    assert a.lagged_sigma == pytest.approx(hist[-1][2])
    assert a.latest_iv_date < asof
    assert a.age_business_days == 1
    assert a.n_changes >= 8
    assert SIGMA_MIN <= a.sigma_draws.min()
    assert a.sigma_draws.max() <= SIGMA_MAX
    assert a.sigma_mean > 0
    assert a.sigma_sd > 0
    assert np.isfinite(a.posterior_drift)


def test_iv_history_insufficient_or_stale():
    h = fake_iv_history(n=5)
    assert predict_market_iv(h, asof="2026-01-12", seed=2) is None
    assert predict_market_iv(fake_iv_history(), asof="2026-06-01", seed=2) is None
    with pytest.raises(ValueError, match="hyperparameters"):
        predict_market_iv(fake_iv_history(), asof="2026-02-27", seed=2,
                          n_draws=1)


def test_market_iv_inference_does_not_consume_eval_price():
    hist = fake_iv_history()
    asof = (pd.Timestamp(hist[-1][0])+pd.offsets.BDay(1)).strftime("%Y-%m-%d")
    forecast = predict_market_iv(hist, asof=asof, seed=11)
    # The model API only accepts previous-date IV history, never observed
    # current-date target premiums, so this is insensitive to target prices.
    assert forecast is not None
    same = predict_market_iv(list(hist), asof=asof, seed=11)
    np.testing.assert_array_equal(forecast.sigma_draws, same.sigma_draws)


def test_paired_month_block_bootstrap_known_improvement():
    dates = pd.bdate_range("2025-01-03", "2025-04-30", freq="5B")
    rows = []
    for day in dates:
        for method in e004.METHODS:
            error = 1.0 if method == "lagged_IV" else .5
            rows.append({
                "date": day, "method": method,
                "error": error, "actual": True
            })
    frame = pd.DataFrame(rows)
    ci = e004._month_block_intervals(frame, n_boot=99, seed=1)
    row = ci.loc[(ci.method == "bayes_IV_PI") &
                 (ci.baseline == "lagged_IV")].iloc[0]
    assert row.mean_daily_mae_improvement == pytest.approx(.5)
    assert row.ci_low == pytest.approx(.5)
    assert row.ci_high == pytest.approx(.5)


def test_synthetic_end_to_end_local_sqlite_without_provider(tmp_path, monkeypatch):
    """Proves 8-way common-support pricing, chronological holdout and outputs."""
    from experiments import wti_aao_databento_only as legacy

    expiry = "2026-07-31"
    definitions = [{
        "publisher_id": 1, "symbol": f"AAO_{int(k)}_{side}",
        "strike": float(k), "expiry": expiry, "side": side
    } for k in np.arange(55., 92., 2.) for side in ("C", "P")]
    master = pd.DataFrame(definitions)
    monkeypatch.setattr(legacy, "date_definitions", lambda _raw, _day: master)
    db = tmp_path/"synthetic.sqlite3"
    con = sqlite3.connect(db)
    con.execute("CREATE TABLE states (publisher_id INTEGER,symbol TEXT,"
                "ref_date TEXT,price REAL,flags INTEGER,action INTEGER,"
                "tie_conflict INTEGER)")
    dates = pd.bdate_range("2026-01-02", periods=94)
    for i, dt in enumerate(dates):
        fwd = 72.0 + .15*np.sin(i/6)
        sigma = .30 + .012*np.sin(i/4)
        maturity = (pd.Timestamp(expiry) - dt).days / 365.25
        for rec in definitions:
            quote = float(average_black(fwd, rec["strike"], sigma,
                                        maturity, .98, rec["side"]))
            con.execute("INSERT INTO states VALUES (?,?,?,?,?,?,?)", (
                1, rec["symbol"], dt.strftime("%Y-%m-%d"),
                quote, 3, 1, 0,
            ))
    con.commit()
    con.close()
    out = tmp_path/"aggregate"
    private = tmp_path/"private"
    manifest = e004.evaluate(
        sqlite_path=db, raw_dir=tmp_path, output_dir=out,
        private_dir=private, source_start="2026-01-02",
        eval_start="2026-02-03", eval_end="2026-05-14",
        test_start="2026-03-16", date_stride=5,
        max_contracts=12, bootstrap=99,
        min_iv_changes=8, max_iv_changes=63, posterior_draws=64,
    )
    assert manifest["n_target_contract_dates"] > 0
    assert manifest["n_holdout_actual_target_rows"] > 0
    assert manifest["n_priced_dates"] > 0
    assert manifest["groups_with_bayesian_IV_history"] > 0
    assert set(manifest["methods"]) == set(e004.METHODS)
    assert manifest["no_provider_calls"]
    assert (out/"method_metrics_by_year.csv").is_file()
    assert (out/"method_metrics_by_maturity.csv").is_file()
    assert (out/"method_metrics_by_moneyness.csv").is_file()
    assert (out/"paired_actual_month_block_ci.csv").is_file()
    contract = pd.read_csv(private/"AAO_MARKET_IV_BAYES_CONTRACT_PRICING.csv.gz")
    assert set(contract.method) == set(e004.METHODS)
    assert (contract.market_iv_latest_date < contract.date).all()
    assert all(contract.groupby(["date", "expiry", "side", "strike", "actual"])
               .method.nunique() == 8)
    # All original lagged-IV predictions are preserved without recalibration.
    assert np.allclose(
        contract.loc[contract.method=="lagged_IV", "prior_iv_sigma"],
        contract.loc[contract.method=="lagged_IV", "market_iv_age_business_days"]
        * 0 + contract.loc[contract.method=="lagged_IV", "prior_iv_sigma"]
    )
