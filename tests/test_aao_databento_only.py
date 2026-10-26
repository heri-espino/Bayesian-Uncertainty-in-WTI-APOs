"""Synthetic tests: AAO-only parity, disjoint anchors and lagged sigma."""
import numpy as np
import pandas as pd
import pytest

from bayesian_asian_options.aao_databento_only import (
    METHODS, average_black, date_cluster_ci, implied_average_sigma,
    prior_volatility_features, reserve_parity_anchors, summarize_errors,
)
from experiments.wti_aao_databento_only import (
    option_groups, previous_returns, priced_rows, prior_implied_vol,
)


def sample_frame(fwd=72., df=.98, t=.4, sigma=.31):
    strikes = np.arange(55., 92., 2.)
    rows = []
    for strike in strikes:
        for side in ("C", "P"):
            rows.append({
                "strike": float(strike), "side": side,
                "price": float(average_black(
                    fwd, strike, sigma, t, df, side
                )),
                "actual": True,
            })
    return pd.DataFrame(rows)


def test_exact_asian_put_call_parity_identifies_forward_and_discount():
    frame = sample_frame()
    anchor = reserve_parity_anchors(frame)
    assert anchor is not None
    assert anchor.forward_average == pytest.approx(72., abs=1e-7)
    assert anchor.discount_factor == pytest.approx(.98, abs=1e-7)
    assert anchor.parity_rmse < 1e-9
    assert len(anchor.anchor_strikes) == 7


def test_parity_strikes_never_appear_in_evaluated_contracts():
    f = sample_frame()
    a = reserve_parity_anchors(f)
    returns = np.linspace(-.025, .025, 60)
    rows = priced_rows(
        day="2026-01-15", expiry="2026-06-30",
        group=f.assign(expiry="2026-06-30"),
        forward=a.forward_average, discount=a.discount_factor,
        anchor_strikes=a.anchor_strikes,
        proxy_returns=returns, prev_iv=.3, seed=123, max_contracts=16,
    )
    assert rows
    assert not set(x["strike"] for x in rows).intersection(a.anchor_strikes)
    assert set(x["method"] for x in rows) == set(METHODS)
    assert len(rows) % len(METHODS) == 0


def test_true_implied_volatility_recovers_input():
    target = float(average_black(70, 71, .37, .6, .97, "P"))
    implied = implied_average_sigma(
        target, forward=70, strike=71, maturity=.6,
        discount=.97, side="P",
    )
    assert implied == pytest.approx(.37, abs=1e-6)


def test_arbitrage_intrinsic_quote_refused():
    assert np.isnan(implied_average_sigma(
        1., forward=80., strike=75., maturity=.3,
        discount=1., side="C"
    ))


def test_bayesian_draws_deterministic_and_strictly_positive():
    r = np.random.default_rng(2).normal(0., .012, 120)
    f1 = prior_volatility_features(r, seed=17)
    f2 = prior_volatility_features(r, seed=17)
    np.testing.assert_array_equal(f1["draws"], f2["draws"])
    assert f1["sigma_pm"] > 0
    assert f1["rolling21"] > 0
    assert f1["rolling63"] > 0
    assert f1["ewma63"] > 0
    with pytest.raises(ValueError, match=">=20"):
        prior_volatility_features(r[:19])


def test_history_returns_skip_gaps_and_use_only_passed_history():
    h = [
        ("2026-01-02", 70, .3), ("2026-01-05", 71, .3),
        ("2026-01-12", 72, .3), ("2026-01-13", 74, .3),
    ]
    z = previous_returns(h)
    assert len(z) == 2
    assert z[0] == pytest.approx(np.log(71/70))
    assert z[1] == pytest.approx(np.log(74/72))


def test_prior_iv_from_available_nonanchor_quotes():
    f = sample_frame()
    anchor = reserve_parity_anchors(f)
    value = prior_implied_vol(
        f, forward=anchor.forward_average, discount=anchor.discount_factor,
        maturity=.4, anchor_strikes=anchor.anchor_strikes,
    )
    assert value == pytest.approx(.31, abs=1e-5)


def test_partial_fixing_period_excluded_without_cl_fixings():
    frame = sample_frame().assign(expiry="2026-06-30")
    assert list(option_groups(frame, "2026-05-15"))
    assert not list(option_groups(frame, "2026-06-15"))


def test_common_support_summary_and_date_cluster_inference():
    data = pd.DataFrame([
        {"date": d, "method": m, "actual": True,
         "error": (.5 if m=="PI" else 1.)}
        for d in ("2026-01-01", "2026-01-02", "2026-01-03")
        for m in ("PI", "PM")
    ])
    result = summarize_errors(data)
    assert set(result["method"]) == {"PI", "PM"}
    ci = date_cluster_ci(data, "PI", "PM", n_boot=99, seed=123)
    assert ci["mean_daily_mae_improvement"] == pytest.approx(.5)
    assert ci["n_paired_dates"] == 3
    assert ci["ci_low"] == pytest.approx(.5)



def test_end_to_end_sqlite_fixture_without_databento_client(tmp_path, monkeypatch):
    """Synthetic 45-day panel exercises real SQLite, all benchmarks and outputs."""
    import sqlite3
    from experiments import wti_aao_databento_only as driver

    definition_rows = []
    for k in np.arange(55., 92., 2.):
        for side in ("C", "P"):
            definition_rows.append({
                "publisher_id": 1,
                "symbol": f"AAO_{int(k)}_{side}",
                "strike": float(k),
                "expiry": "2026-04-30",
                "side": side,
            })
    defs = pd.DataFrame(definition_rows)
    monkeypatch.setattr(driver, "date_definitions", lambda _root, _day: defs)
    state = tmp_path / "contract_candidates.sqlite3"
    conn = sqlite3.connect(state)
    conn.execute(
        "CREATE TABLE states (publisher_id INTEGER,symbol TEXT,"
        "ref_date TEXT,price REAL,flags INTEGER,action INTEGER,"
        "tie_conflict INTEGER)"
    )
    calendar = pd.bdate_range("2026-01-02", periods=49)
    for i, ref_date in enumerate(calendar):
        forward = 71. + .12*np.sin(i/2.) + .008*i
        t = (pd.Timestamp("2026-04-30")-ref_date).days/365.25
        for rec in definition_rows:
            premium = float(average_black(
                forward, rec["strike"], .31, t, .985, rec["side"]
            ))
            conn.execute(
                "INSERT INTO states VALUES(?,?,?,?,?,?,?)",
                (1, rec["symbol"], ref_date.strftime("%Y-%m-%d"),
                 premium, 3, 1, 0)
            )
    conn.commit()
    conn.close()
    output = tmp_path / "results"
    private = tmp_path / "private"
    report = driver.evaluate(
        sqlite_path=state, raw_dir=tmp_path,
        output_dir=output, private_dir=private,
        start_date="2026-01-02", eval_start="2026-02-03",
        date_stride=5, max_dates=0, max_contracts=20, n_boot=19,
    )
    assert report["n_priced_dates"] >= 2
    assert report["n_target_contract_dates"] > 0
    assert set(pd.read_csv(output/"method_metrics.csv")["method"]) == set(METHODS)
    assert (output/"cluster_intervals.csv").is_file()
    assert (private/"AAO_DATABENTO_REDUCED_FORM_CONTRACT_PRICING.csv.gz").is_file()
    assert report["no_barchart"] is True
    assert report["no_provider_calls"] is True
