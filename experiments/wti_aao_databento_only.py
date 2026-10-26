"""Manual Databento-AAO-only reduced-form Bayesian/benchmark experiment.

Uses ONLY purchased AAO definitions, reconciled AAO settlement statistics,
and same-family AAO put/call parity. No Barchart, CL futures, Treasury,
Yahoo, or new Databento API calls. This does NOT recover actual CL fixings,
so option pricing is a disclosed lognormal TERMINAL-AVERAGE approximation.

The same-date anchor strikes are excluded from price-error evaluation.
All volatility estimators and lagged AAO implied volatility use STRICTLY
EARLIER reference dates. Observed terminal marks use the last known
archive-end revision; this is retrospective cross-sectional valuation,
not a fully ex-ante independently sourced option-price forecast.

DRY RUN by default. --execute performs manual local computation.
"""
from __future__ import annotations

import argparse
from collections import defaultdict
from datetime import date
import hashlib
import json
from pathlib import Path
import sqlite3

import numpy as np
import pandas as pd

from bayesian_asian_options.aao_databento_only import (
    METHODS, average_black, date_cluster_ci, implied_average_sigma,
    prior_volatility_features, reserve_parity_anchors, summarize_errors,
)

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "databento" / "wti_aao_bulk" / "raw"
SQLITE = (
    ROOT / "data" / "databento" / "wti_aao_bulk" / "derived_private"
    / "aao_cross_month_PROVISIONAL_81_months.sqlite3"
)
PRIVATE = ROOT / "data" / "databento" / "wti_aao_bulk" / "derived_private"
OUT = ROOT / "results" / "analysis" / "wti_aao_databento_only"
VALID_SQL = (
    "action=1 AND (flags & 1)!=0 AND (flags & 8)=0 AND "
    "price IS NOT NULL AND price>=0 AND tie_conflict=0"
)


def utc_dates(values: pd.Series) -> pd.Series:
    """Read DBN timestamp fields without silently treating ns as seconds."""
    if pd.api.types.is_numeric_dtype(values):
        return pd.to_datetime(values, unit="ns", utc=True, errors="coerce")
    return pd.to_datetime(values, utc=True, errors="coerce")


def local_contract_master(definition_path: Path) -> pd.DataFrame:
    """Require nonconflicting native symbols and sensible *unscaled* strikes."""
    import databento as db  # local DBNStore only; no network client

    d = db.DBNStore.from_file(definition_path).to_df(
        map_symbols=True, price_type="float"
    )
    needed = ["publisher_id", "raw_symbol", "asset", "instrument_class",
              "leg_count", "strike_price", "expiration"]
    if set(needed)-set(d):
        raise ValueError(f"Definition missing {sorted(set(needed)-set(d))}")
    d = d.loc[
        d["asset"].astype("string").eq("AAO")
        & d["instrument_class"].astype("string").isin(("C", "P"))
        & pd.to_numeric(d["leg_count"], errors="coerce").eq(0),
        needed,
    ].copy()
    d["symbol"] = d["raw_symbol"].astype("string").str.strip()
    d["strike"] = pd.to_numeric(d["strike_price"], errors="coerce")
    d["expiry"] = utc_dates(d["expiration"]).dt.strftime("%Y-%m-%d")
    d["side"] = d["instrument_class"].astype("string")
    d = d.dropna(subset=["symbol", "strike", "expiry"])
    if d.empty:
        raise ValueError(
            "No candidate AAO definitions: investigate DBN strike_price "
            "scale/expiration fields instead of inventing conversions"
        )
    d["publisher_id"] = pd.to_numeric(
        d["publisher_id"], errors="raise"
    ).astype("int64")
    by = d.groupby(["publisher_id", "symbol"], sort=False)
    ambiguous = by[["strike", "expiry", "side"]].nunique().gt(1).any(axis=1)
    stable = d.drop_duplicates(["publisher_id", "symbol"])
    if ambiguous.any():
        rejected = ambiguous[ambiguous].index
        bad = pd.MultiIndex.from_frame(stable[["publisher_id", "symbol"]]).isin(
            rejected
        )
        stable = stable.loc[~bad].copy()
    stable = stable.loc[stable["strike"].between(5, 300)].copy()
    if stable.empty:
        raise ValueError(
            "Every AAO strike failed the $5-$300 sanity band: verify DBN "
            "strike unit scaling before pricing; no silent conversion"
        )
    return stable[["publisher_id", "symbol", "strike", "expiry", "side"]]


def date_definitions(raw: Path, reference_date: str) -> pd.DataFrame:
    month = reference_date[:7]
    matches = sorted(raw.glob(f"aao_definition__{month}-*.dbn.zst"))
    if len(matches) != 1:
        raise FileNotFoundError(
            f"Require one local AAO definition DBN for {month}; "
            f"found {len(matches)} (no provider calls)"
        )
    return local_contract_master(matches[0])


def read_date(conn: sqlite3.Connection, day: str, definitions: pd.DataFrame) -> pd.DataFrame:
    """Joined candidate prices; keys and option prices never printed."""
    s = pd.read_sql_query(
        f"SELECT publisher_id, symbol, price, flags "
        f"FROM states WHERE ref_date=? AND {VALID_SQL}",
        conn, params=(day,),
    )
    if s.empty:
        return pd.DataFrame()
    s["actual"] = (s["flags"].astype("int64") & 2) != 0
    merged = s.merge(
        definitions, how="inner", on=["publisher_id", "symbol"],
        validate="many_to_one",
    )
    return merged.loc[
        merged["price"].between(0, 300)
        & merged["strike"].between(5, 300)
        & merged["side"].isin(("C", "P"))
    ].copy()


def option_groups(frame: pd.DataFrame, day: str):
    """Pre-fixing contract groups only; fixings not available in AAO files."""
    if frame.empty:
        return
    now = pd.Timestamp(day)
    for expiry, group in frame.groupby("expiry", sort=True):
        expiry_ts = pd.Timestamp(expiry)
        first_fixing_month_day = expiry_ts.replace(day=1)
        # No partially-fixed period: the actual fixing path is absent.
        if not (now < first_fixing_month_day and
                7 <= (expiry_ts-now).days <= 366):
            continue
        if len(group) >= 15:
            yield expiry, group


def previous_returns(
    history: list[tuple[str, float, float]],
) -> np.ndarray:
    """Daily log-change of parity implied forward for identical AAO expiry."""
    values = []
    for (d0, f0, _), (d1, f1, _) in zip(history, history[1:]):
        if 0 < (pd.Timestamp(d1)-pd.Timestamp(d0)).days <= 4:
            values.append(np.log(f1/f0))
    return np.array(values, dtype=float)


def prior_implied_vol(
    group: pd.DataFrame, *, forward: float, discount: float,
    maturity: float, anchor_strikes: tuple[float, ...],
) -> float:
    """Near-ATM lagged smile scalar, computed on a past day only."""
    eligible = group.loc[
        ~group["strike"].isin(anchor_strikes)
        & group["actual"]
        & group["price"].between(.02, 100)
        & group["strike"].between(.82*forward, 1.18*forward)
    ].copy()
    eligible["distance"] = (eligible["strike"]-forward).abs()
    eligible = eligible.sort_values("distance").head(12)
    values = [
        implied_average_sigma(
            float(row.price), forward=forward, strike=float(row.strike),
            maturity=maturity, discount=discount, side=str(row.side),
        )
        for row in eligible.itertuples(index=False)
    ]
    valid = np.asarray(values)
    valid = valid[np.isfinite(valid)]
    return float(np.median(valid)) if len(valid) >= 2 else float("nan")


def priced_rows(
    *, day: str, expiry: str, group: pd.DataFrame,
    forward: float, discount: float, anchor_strikes: tuple[float, ...],
    proxy_returns: np.ndarray, prev_iv: float, seed: int,
    max_contracts: int,
) -> list[dict]:
    maturity = (pd.Timestamp(expiry)-pd.Timestamp(day)).days/365.25
    if not np.isfinite(prev_iv) or not 0.005 < prev_iv < 3:
        return []
    if len(proxy_returns) < 20:
        return []
    features = prior_volatility_features(proxy_returns, seed=seed)
    # Exclude every current-date strike used in parity input, regardless
    # of call/put side; otherwise the target contaminates the forward.
    test = group.loc[
        ~group["strike"].isin(anchor_strikes)
        & group["strike"].between(.75*forward, 1.25*forward)
        & group["price"].between(0, 200)
    ].copy()
    test = test.sort_values(["strike", "side"])
    if max_contracts and len(test) > max_contracts:
        indices = np.unique(np.linspace(
            0, len(test)-1, max_contracts, dtype=int
        ))
        test = test.iloc[indices]
    if test.empty:
        return []
    strikes = test["strike"].to_numpy(dtype=float)
    sides = test["side"].to_numpy(dtype=str)
    sigmas = features["draws"]
    pi = average_black(
        forward, strikes[None, :], sigmas[:, None], maturity,
        discount, sides[None, :],
    ).mean(axis=0)
    params = {
        "PI": pi,
        "PM": average_black(
            forward, strikes, float(features["sigma_pm"]),
            maturity, discount, sides,
        ),
        "rolling21": average_black(
            forward, strikes, features["rolling21"], maturity, discount, sides,
        ),
        "rolling63": average_black(
            forward, strikes, features["rolling63"], maturity, discount, sides,
        ),
        "ewma63": average_black(
            forward, strikes, features["ewma63"], maturity, discount, sides,
        ),
        "lagged_IV": average_black(
            forward, strikes, prev_iv, maturity, discount, sides,
        ),
    }
    out = []
    for index, observation in enumerate(test.itertuples(index=False)):
        for method in METHODS:
            predicted = float(params[method][index])
            out.append({
                "date": day,
                "expiry": expiry,
                "side": str(observation.side),
                "strike": float(observation.strike),
                "actual": bool(observation.actual),
                "observed": float(observation.price),
                "predicted": predicted,
                "error": predicted-float(observation.price),
                "method": method,
                "expected_average": forward,
                "parity_discount_factor": discount,
                "sigma_posterior_sd": float(features["posterior_sd"]),
                "n_lagged_proxy_returns": int(features["n_returns"]),
                "prior_iv_sigma": prev_iv,
                "pricing_model": "lognormal_terminal_average_proxy",
                "same_day_disjoint_parity_anchors": True,
                "historical_sigma_source": "lagged_AAO_parity_forward_changes",
            })
    return out


def evaluate(*, sqlite_path: Path, raw_dir: Path, output_dir: Path,
             private_dir: Path, start_date: str, eval_start: str,
             date_stride: int, max_dates: int, max_contracts: int,
             n_boot: int = 399) -> dict:
    if date_stride < 1 or max_dates < 0 or max_contracts < 1:
        raise ValueError("Require stride>=1, max_dates>=0, max_contracts>=1")
    if not sqlite_path.is_file():
        raise FileNotFoundError(
            f"Missing reconstructed Databento-only SQLite: {sqlite_path}. "
            "Restore/rebuild raw DBNs and run wti_aao_cross_month --all first."
        )
    conn = sqlite3.connect(sqlite_path.resolve().as_uri()+"?mode=ro", uri=True)
    try:
        dates = [
            str(row[0]) for row in conn.execute(
                f"SELECT DISTINCT ref_date FROM states WHERE {VALID_SQL} "
                "AND ref_date>=? ORDER BY ref_date", (start_date,)
            )
        ]
        if max_dates:
            dates = dates[:max_dates]
        histories: dict[str, list[tuple[str, float, float]]] = defaultdict(list)
        monthly_defs: dict[str, pd.DataFrame] = {}
        outputs: list[dict] = []
        audit = {
            "selected_source_days": len(dates),
            "groups_seen": 0,
            "groups_with_anchor": 0,
            "groups_with_lagged_history": 0,
            "groups_priced": 0,
            "anchor_strikes_excluded": True,
            "no_barchart": True,
            "no_external_futures_or_rates": True,
            "no_provider_calls": True,
            "model": "reduced_form_lognormal_terminal_average",
            "evaluation_not_strictly_ex_ante": True,
        }
        for counter, day in enumerate(dates):
            month = day[:7]
            if month not in monthly_defs:
                # Bound memory to one month's definitions.
                monthly_defs.clear()
                monthly_defs[month] = date_definitions(raw_dir, day)
            panel = read_date(conn, day, monthly_defs[month])
            for expiry, group in option_groups(panel, day):
                audit["groups_seen"] += 1
                anchor = reserve_parity_anchors(group, actual_only=True)
                if anchor is None:
                    continue
                audit["groups_with_anchor"] += 1
                history = histories[expiry]
                past_returns = previous_returns(history)
                # Last earlier date's IV, never today's IV.
                lagged_iv = next(
                    (iv for past_date, _, iv in reversed(history)
                     if np.isfinite(iv) and
                     0 < (pd.Timestamp(day)-pd.Timestamp(past_date)).days <= 10),
                    float("nan"),
                )
                if (day >= eval_start and counter % date_stride == 0
                    and len(past_returns) >= 20 and np.isfinite(lagged_iv)):
                    audit["groups_with_lagged_history"] += 1
                    stable_seed = int.from_bytes(hashlib.sha256(
                        f"{day}/{expiry}".encode()).digest()[:4], "big"
                    )
                    rows = priced_rows(
                        day=day, expiry=expiry, group=group,
                        forward=anchor.forward_average,
                        discount=anchor.discount_factor,
                        anchor_strikes=anchor.anchor_strikes,
                        proxy_returns=past_returns, prev_iv=lagged_iv,
                        seed=stable_seed, max_contracts=max_contracts,
                    )
                    if rows:
                        outputs.extend(rows)
                        audit["groups_priced"] += 1
                # Update ONLY after evaluating target date.
                this_iv = prior_implied_vol(
                    group, forward=anchor.forward_average,
                    discount=anchor.discount_factor,
                    maturity=(pd.Timestamp(expiry)-pd.Timestamp(day)).days/365.25,
                    anchor_strikes=anchor.anchor_strikes,
                )
                history.append((day, anchor.forward_average, this_iv))
    finally:
        conn.close()
    if not outputs:
        raise RuntimeError(
            "No eligible Databento-only targets. Inspect anchor coverage, "
            "strike units and lagged volatility; do NOT fabricate scores."
        )
    full = pd.DataFrame(outputs)
    # Every contract/date is priced by exactly the same method set.
    key = ["date", "expiry", "side", "strike", "actual"]
    counts = full.groupby(key)["method"].nunique()
    if not counts.eq(len(METHODS)).all():
        raise AssertionError("Methods have different support")
    summary = summarize_errors(full)
    bydate = full.assign(abs_error=full["error"].abs()).groupby(
        ["date", "method"], as_index=False
    ).agg(mae=("abs_error", "mean"), n=("error", "size"))
    ci = []
    for method in METHODS:
        if method != "PM":
            ci.append(date_cluster_ci(
                full, method, "PM", n_boot=n_boot
            ))
    audit.update({
        "n_priced_dates": int(full["date"].nunique()),
        "n_target_contract_dates": int(len(full)//len(METHODS)),
        "n_actual_target_rows": int(
            full[full["method"]=="PM"]["actual"].sum()
        ),
        "n_theoretical_target_rows": int(
            (~full[full["method"]=="PM"]["actual"]).sum()
        ),
        "methods": list(METHODS),
        "first_priced_date": full["date"].min(),
        "last_priced_date": full["date"].max(),
        "n_posterior_draws": 128,
        "disclosure": (
            "Conditional cross-section using contemporaneous disjoint parity "
            "pairs for expected average/discount; volatility strictly lagged. "
            "The P-volatility proxy is AAO parity forward-average changes, "
            "not actual first-nearby CL historical returns; not structural "
            "Asian Q-pricing, nor a fully ex-ante independent-price forecast."
        ),
    })
    output_dir.mkdir(parents=True, exist_ok=True)
    private_dir.mkdir(parents=True, exist_ok=True)
    full.to_csv(
        private_dir / "AAO_DATABENTO_REDUCED_FORM_CONTRACT_PRICING.csv.gz",
        compression="gzip", index=False,
    )
    summary.to_csv(output_dir/"method_metrics.csv", index=False)
    bydate.to_csv(output_dir/"daily_metrics.csv", index=False)
    pd.DataFrame(ci).to_csv(output_dir/"cluster_intervals.csv", index=False)
    (output_dir/"experiment_manifest.json").write_text(
        json.dumps(audit, indent=2)+"\n", encoding="utf-8"
    )
    return audit


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--execute", action="store_true",
                        help="Explicitly run the heavy local study")
    parser.add_argument("--sqlite", type=Path, default=SQLITE)
    parser.add_argument("--raw-dir", type=Path, default=RAW)
    parser.add_argument("--output-dir", type=Path, default=OUT)
    parser.add_argument("--private-dir", type=Path, default=PRIVATE)
    parser.add_argument("--source-start", default="2021-01-01")
    parser.add_argument("--eval-start", default="2023-01-01")
    parser.add_argument("--date-stride", type=int, default=5)
    parser.add_argument("--max-dates", type=int, default=0)
    parser.add_argument("--max-contracts", type=int, default=80)
    parser.add_argument("--bootstrap", type=int, default=399)
    args = parser.parse_args()
    if not args.execute:
        print(json.dumps({
            "execute": False,
            "no_databento_api_calls": True,
            "no_barchart_files_needed": True,
            "source": "81 local AAO definition DBNs plus private SQLite",
            "methodology": "reduced-form terminal-average Black proxy",
            "source_start": args.source_start,
            "evaluation_start": args.eval_start,
            "date_stride": args.date_stride,
            "max_dates": args.max_dates,
            "max_contracts_per_expiry": args.max_contracts,
            "note": "Run --execute only after AAO files and SQLite are restored",
        }, indent=2))
        return
    result = evaluate(
        sqlite_path=args.sqlite, raw_dir=args.raw_dir,
        output_dir=args.output_dir, private_dir=args.private_dir,
        start_date=args.source_start, eval_start=args.eval_start,
        date_stride=args.date_stride, max_dates=args.max_dates,
        max_contracts=args.max_contracts, n_boot=args.bootstrap,
    )
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
