"""Re-audit original REMEF lagged-IV result from committed contract-level outputs.

Read-only unless --write-json is specified. No vendor calls or simulation reruns.
Checks mathematical/numerical integrity and **date-only** source precedence.
A chronological calendar date does NOT prove contemporaneous public availability,
vendor archival vintages, original as-of availability, or licensed dissemination.

Run: python -m scripts.audit_remef_forward_iv
     python -m scripts.audit_remef_forward_iv --write-json
"""
from __future__ import annotations

import argparse
from hashlib import sha256
import json
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "results/analysis/wti_extended_forward"
FORWARD = BASE / "forward_q_validation/forward_q_predictions.csv"
CARRY = ROOT / "results/analysis/wti_prior_contract_iv_carry/prior_contract_iv_carry_predictions.csv"
HISTORY = BASE / "apo_implied_volatility/apo_contract_implied_volatility.csv"
OUT = ROOT / "results/analysis/remef_science_audit/forward_iv_verified_aggregates.json"
KEY = ["valuation_date", "apo_expiry", "contract_id"]
RIDGE = 1e-6
HALF_LIFE = 5.0


def _read(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path)
    if df.empty:
        raise ValueError(f"empty audit source {path}")
    return df


def _date(df: pd.DataFrame, col: str) -> pd.Series:
    values = pd.to_datetime(df[col], errors="raise").dt.normalize()
    if values.isna().any():
        raise ValueError(f"null dates in {col}")
    return values


def _unique(frame: pd.DataFrame, keys: list[str], label: str) -> None:
    if frame.duplicated(keys).any():
        raise AssertionError(f"duplicate {label} keys")


def _metric(frame: pd.DataFrame, col: str) -> dict:
    x = frame[col].to_numpy(dtype=float)
    if len(x) == 0 or not np.isfinite(x).all():
        raise AssertionError(f"invalid errors in {col}")
    return {
        "n": int(len(x)),
        "n_valuation_dates": int(frame.valuation_date.nunique()),
        "bias_usd_per_bbl": float(x.mean()),
        "mae_usd_per_bbl": float(np.abs(x).mean()),
        "rmse_usd_per_bbl": float(np.sqrt(np.mean(x * x))),
    }


def _max_residual(frame: pd.DataFrame, actual: str, price: str) -> float:
    delta = frame[price].to_numpy(float) - frame.market_settlement.to_numpy(float)
    return float(np.max(np.abs(frame[actual].to_numpy(float) - delta)))


def _design(frame: pd.DataFrame) -> np.ndarray:
    x = frame.log_moneyness.to_numpy(float)
    call = frame.option_type.astype(str).str.lower().eq("call").to_numpy(float)
    return np.column_stack([np.ones(len(frame)), x, x**2, call, call*x, call*x*x])


def _reconstruct_smiles(forward: pd.DataFrame, history: pd.DataFrame) -> dict:
    """Independently estimate each six-parameter ridge smile from stored earlier IVs."""
    max_abs_sigma_difference = 0.0
    groups = 0
    n_estimated = 0
    for (expiry, target, method), frame in forward.groupby(
        ["apo_expiry", "valuation_date", "method"], sort=True
    ):
        target_date = pd.Timestamp(target)
        earlier = history.loc[
            history.apo_expiry.astype(str).eq(str(expiry))
            & history.valuation_date.lt(target_date)
            & history.apo_implied_sigma_q.notna()
        ].copy()
        if earlier.empty:
            raise AssertionError("no strictly earlier IV data")
        last = earlier.valuation_date.max()
        train = earlier.loc[earlier.valuation_date.eq(last)] if method == "previous_day_smile" else earlier
        if method not in ("previous_day_smile", "expanding_smile"):
            raise AssertionError(f"unknown forward method {method}")
        if len(train) != int(frame.n_training_rows.iloc[0]):
            raise AssertionError(f"training count mismatch {expiry}/{target}/{method}")
        if not frame.n_training_rows.eq(len(train)).all():
            raise AssertionError("training count varies within group")
        if not frame.training_end_date.eq(last).all():
            raise AssertionError("training date mismatch")
        X = _design(train)
        y = train.apo_implied_sigma_q.to_numpy(float)
        if method == "previous_day_smile":
            w = np.ones(len(train))
        else:
            age = (target_date - train.valuation_date).dt.days.to_numpy(float)
            w = np.exp(-np.log(2) * np.maximum(age, 0) / HALF_LIFE)
        penalty = RIDGE * np.eye(6)
        penalty[0, 0] = 0.0
        lhs = X.T @ (w[:, None] * X) + penalty
        rhs = X.T @ (w * y)
        try:
            beta = np.linalg.solve(lhs, rhs)
        except np.linalg.LinAlgError:
            beta = np.linalg.pinv(lhs) @ rhs
        sigma = np.clip(_design(frame) @ beta, 1e-6, 3.0)
        diff = np.max(np.abs(sigma - frame.predicted_sigma_q.to_numpy(float)))
        max_abs_sigma_difference = max(max_abs_sigma_difference, float(diff))
        n_estimated += len(frame)
        groups += 1
    if n_estimated != len(forward) or max_abs_sigma_difference > 1e-8:
        raise AssertionError("stored forward IVs do not match independent reconstruction")
    return {
        "groups": groups,
        "reconstructed_prediction_rows": n_estimated,
        "max_abs_sigma_discrepancy": max_abs_sigma_difference,
        "model": "six-feature prior-only ridge: intercept, log-moneyness, square, call and interactions",
        "ridge": RIDGE,
        "expanding_half_life_calendar_days": HALF_LIFE,
    }


def _date_gains(frame: pd.DataFrame, base: str, candidate: str) -> np.ndarray:
    out = []
    for _, day in frame.groupby("valuation_date", sort=True):
        b = np.abs(day[base].to_numpy(float))
        c = np.abs(day[candidate].to_numpy(float))
        out.append(float(np.mean(b-c)))
    return np.asarray(out)


def _boot(gains: np.ndarray, *, block: int, seed: int = 17347, n_rep: int = 20000) -> dict:
    rng = np.random.default_rng(seed)
    n = len(gains)
    samples = []
    for _ in range(n_rep):
        idx = []
        while len(idx) < n:
            start = int(rng.integers(0, n))
            idx.extend((start + j) % n for j in range(block))
        samples.append(float(gains[np.asarray(idx[:n])].mean()))
    lo, hi = np.quantile(samples, [0.025, 0.975])
    return {
        "n_independent_date_clusters": int(n),
        "date_equal_weight_gain_usd_per_bbl": float(gains.mean()),
        "ci_95": [float(lo), float(hi)],
        "bootstrap": "exploratory circular date-block resampling",
        "block_length_dates": int(block),
        "seed": int(seed),
        "replications": int(n_rep),
    }


def audit() -> dict:
    forward = _read(FORWARD)
    carry = _read(CARRY)
    history = _read(HISTORY)
    for df in (forward, carry, history):
        df["valuation_date"] = _date(df, "valuation_date")
        df["apo_expiry"] = df.apo_expiry.astype(str)
        df["contract_id"] = df.contract_id.astype(str)
        _unique(df, KEY if df is not forward else KEY + ["method"], "contract-date")
    forward["training_end_date"] = _date(forward, "training_end_date")
    carry["prior_iv_date"] = _date(carry, "prior_iv_date")
    if not forward.training_end_date.lt(forward.valuation_date).all():
        raise AssertionError("forward smile uses a nonprior IV date")
    if not carry.prior_iv_date.lt(carry.valuation_date).all():
        raise AssertionError("carry uses a nonprior IV date")
    prev = forward.loc[forward.method.eq("previous_day_smile")].copy()
    expanded = forward.loc[forward.method.eq("expanding_smile")].copy()
    if len(prev) != 2381 or len(expanded) != 2381 or len(carry) != 2366:
        raise AssertionError("original sample sizes have changed")
    pkeys = set(map(tuple, prev[KEY].itertuples(index=False, name=None)))
    ekeys = set(map(tuple, expanded[KEY].itertuples(index=False, name=None)))
    ckeys = set(map(tuple, carry[KEY].itertuples(index=False, name=None)))
    if pkeys != ekeys or not ckeys.issubset(pkeys) or len(pkeys) != 2381 or len(ckeys) != 2366:
        raise AssertionError("prediction samples are not matched")
    for df in (prev, expanded):
        if _max_residual(df, "forward_error", "forward_q_price") > 1e-9:
            raise AssertionError("forward_error is arithmetically inconsistent")
        if _max_residual(df, "baseline_pi_error", "baseline_pi_price") > 1e-9:
            raise AssertionError("historical baseline error inconsistent")
        if not np.allclose(
            df.predicted_sigma_q.to_numpy(float) - df.observed_same_day_implied_sigma_q.to_numpy(float),
            df.sigma_prediction_error.to_numpy(float),
            atol=1e-9, rtol=0,
        ):
            raise AssertionError("sigma forecast-error arithmetic inconsistent")
    for err, price in [
        ("carry_error", "carry_price"),
        ("previous_day_smile_error", "previous_day_smile_price"),
        ("baseline_pi_error", "baseline_pi_price"),
    ]:
        if _max_residual(carry, err, price) > 1e-9:
            raise AssertionError(f"carry error arithmetic mismatch: {err}")
    carry_f = carry.merge(
        prev[KEY + ["market_settlement", "forward_q_price", "baseline_pi_price"]],
        on=KEY, how="left", validate="one_to_one", suffixes=("", "_forward"),
    )
    for original, joined in [
        ("market_settlement", "market_settlement_forward"),
        ("previous_day_smile_price", "forward_q_price"),
        ("baseline_pi_price", "baseline_pi_price_forward"),
    ]:
        if carry_f[joined].isna().any() or not np.allclose(
            carry_f[original], carry_f[joined], rtol=0, atol=1e-8
        ):
            raise AssertionError(f"carry and forward samples differ: {original}")
    prior_iv = history.rename(columns={
        "valuation_date": "prior_iv_date",
        "apo_implied_sigma_q": "historical_prior_sigma_q",
    })
    merged = carry.merge(
        prior_iv[["prior_iv_date", "apo_expiry", "contract_id", "historical_prior_sigma_q"]],
        on=["prior_iv_date", "apo_expiry", "contract_id"],
        how="left", validate="many_to_one",
    )
    if merged.historical_prior_sigma_q.isna().any() or not np.allclose(
        merged.carried_sigma_q, merged.historical_prior_sigma_q, rtol=0, atol=1e-9
    ):
        raise AssertionError("carry IV does not match prior contract history")
    delta_days = (carry.valuation_date - carry.prior_iv_date).dt.days
    if not np.array_equal(delta_days, carry.days_since_prior_iv):
        raise AssertionError("stored carry lag inconsistent")
    fit = _reconstruct_smiles(forward, history)
    volumes = prev.volume.fillna(0).to_numpy(float)
    strata = {
        "all": prev,
        "positive_volume": prev.loc[volumes > 0],
        "zero_volume": prev.loc[volumes == 0],
        "open_interest_ge_100": prev.loc[prev.open_interest.ge(100)],
        "open_interest_ge_500": prev.loc[prev.open_interest.ge(500)],
    }
    return {
        "status": "output_arithmetic_and_stored_date_ordering_verified; raw_vendor_asof_NOT_verified",
        "source_sha256": {str(p.relative_to(ROOT)): sha256(p.read_bytes()).hexdigest()
                          for p in (FORWARD, CARRY, HISTORY)},
        "counts": {
            "forward_total": len(forward),
            "previous_day_smile": len(prev),
            "expanding_smile": len(expanded),
            "same_contract_carry": len(carry),
            "iv_history": len(history),
            "all_dates": int(prev.valuation_date.nunique()),
            "carry_prior_lag_calendar_days": {
                "min": int(delta_days.min()),
                "median": float(delta_days.median()),
                "max": int(delta_days.max()),
            },
        },
        "methods": {
            "historical_pi_on_forward": _metric(prev, "baseline_pi_error"),
            "previous_day_smile": _metric(prev, "forward_error"),
            "expanding_smile": _metric(expanded, "forward_error"),
            "same_contract_carry": _metric(carry, "carry_error"),
            "smile_on_carry_rows": _metric(carry, "previous_day_smile_error"),
            "historical_pi_on_carry_rows": _metric(carry, "baseline_pi_error"),
        },
        "previous_smile_reconstruction": fit,
        "liquidity": {
            k: {"historical_pi": _metric(v, "baseline_pi_error"),
                "previous_day_smile": _metric(v, "forward_error")}
            for k, v in strata.items()
        },
        "equal_date_paired_gain": {
            "pi_minus_prior_smile": {
                "date_1": _boot(_date_gains(prev, "baseline_pi_error", "forward_error"), block=1),
                "date_3": _boot(_date_gains(prev, "baseline_pi_error", "forward_error"), block=3),
            },
            "smile_minus_contract_carry": {
                "date_1": _boot(_date_gains(carry, "previous_day_smile_error", "carry_error"), block=1),
                "date_3": _boot(_date_gains(carry, "previous_day_smile_error", "carry_error"), block=3),
            },
        },
        "not_verified": [
            "original exchange publication timestamps and final mark/actual trade status",
            "historical Barchart snapshot vintages and provider corrections",
            "intraday ordering of target-day CL curve, fixings and Treasury par yields",
            "raw market-data license/redistribution terms",
            "independent source-level rerun of original Curran price calculation and any dirty git state",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write-json", action="store_true")
    args = parser.parse_args()
    report = audit()
    result = json.dumps(report, indent=2, sort_keys=True)
    if args.write_json:
        if OUT.exists():
            raise FileExistsError(f"refusing to overwrite {OUT}")
        OUT.parent.mkdir(parents=True, exist_ok=True)
        OUT.write_text(result + "\n", encoding="utf-8")
        print(f"Saved {OUT}")
    print(result)


if __name__ == "__main__":
    main()
