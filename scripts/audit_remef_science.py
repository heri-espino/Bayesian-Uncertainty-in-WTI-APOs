"""Recalculate REMEF numerical claims from versioned contract-level outputs.

Read-only by default; --write-json saves an aggregate report, never market rows.
No vendor API calls, purchases, simulation/MCMC reruns, SQLite reads or GitHub
Actions. This checks arithmetic and provenance, NOT independent source vintages,
vendor rights, settlement transaction independence, or journal compliance.

Run: python -m scripts.audit_remef_science
     python -m scripts.audit_remef_science --write-json
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results/analysis/remef_science_audit/verified_aggregate_claims.json"


def _metrics(v: pd.Series) -> dict:
    x = pd.to_numeric(v, errors="raise").to_numpy(dtype=float)
    if x.size == 0 or not np.all(np.isfinite(x)):
        raise ValueError("Empty/nonfinite audited errors")
    return {
        "n": int(x.size), "bias": float(x.mean()),
        "mae": float(np.abs(x).mean()),
        "rmse": float(np.sqrt(np.mean(x*x)))
    }


def _check(got: float | int, expected: float | int, tolerance=1e-6) -> None:
    if not np.isclose(float(got), float(expected), atol=tolerance, rtol=0):
        raise AssertionError(f"Observed {got} != declared {expected}")


def audit() -> dict:
    old = ROOT / "results/wti_apo_empirical"
    dates = (
        "2026-08-25", "2026-08-26", "2026-08-27", "2026-08-28",
        "2026-08-31", "2026-09-01", "2026-09-02", "2026-09-03",
        "2026-09-04", "2026-09-08", "2026-09-09", "2026-09-10",
    )
    blocks = []
    sizes = {}
    for day in dates:
        f = old / f"{day}_202610/contract_pricing.csv"
        tab = pd.read_csv(f)
        assert (tab["trade_date"].astype(str) == day).all(), f
        assert (tab["expiry_month"].astype(str) == "2026-10").all(), f
        sizes[day] = len(tab)
        blocks.append(tab)
    october = pd.concat(blocks, ignore_index=True)
    _check(len(october), 310, 0)
    oct_stats = {
        "n_rows": len(october), "n_dates": len(dates),
        "daily_counts": sizes,
        "PI": _metrics(october["fb_error"]),
        "PM": _metrics(october["pm_error"]),
        "mean_abs_PI_minus_PM": float(october["fb_minus_pm"].abs().mean()),
        "mean_width_95pct_posterior_model_price": float(
            (october["posterior_price_q975"]
             - october["posterior_price_q025"]).mean()),
    }
    _check(oct_stats["PI"]["rmse"], .5177412470)
    _check(oct_stats["PM"]["rmse"], .5183370736)
    _check(oct_stats["mean_abs_PI_minus_PM"], .000745132275, 1e-8)
    _check(oct_stats["mean_width_95pct_posterior_model_price"], .2732726840)

    main_file = ROOT / "results/analysis/wti_first_nearby/pricing_holdout_comparison.csv"
    main = pd.read_csv(main_file)
    _check(len(main), 2381, 0)
    main_stats = {
        "n":len(main), "n_dates":int(main["valuation_date"].nunique()),
        "historical_PI_Yahoo_CL_F":_metrics(main["baseline_pi_error_yahoo"]),
        "historical_PI_reconstructed_first_nearby":_metrics(
            main["baseline_pi_error_first_nearby"]),
    }
    _check(main_stats["n_dates"], 15, 0)
    _check(main_stats["historical_PI_Yahoo_CL_F"]["mae"], 2.6186993843)
    _check(main_stats["historical_PI_Yahoo_CL_F"]["rmse"], 3.4089906045)
    _check(main_stats["historical_PI_reconstructed_first_nearby"]["mae"], 2.646807895)
    _check(main_stats["historical_PI_reconstructed_first_nearby"]["rmse"], 3.4450875335)

    ex = pd.read_csv(ROOT / "results/analysis/wti_external_vanilla_q_validation/surface_common_support_paired_errors.csv")
    _check(len(ex), 253, 0)
    ext_stats = {"n":len(ex), "n_dates":int(ex.valuation_date.nunique())}
    for name,col in [
        ("historical_PI","baseline_pi_error"),
        ("LO_previous_day","external_previous_error"),
        ("LO_expanding","external_expanding_error"),
        ("AAO_previous_day","apo_previous_error"),
        ("AAO_expanding","apo_expanding_error"),
    ]:
        ext_stats[name]=_metrics(ex[col])
    _check(ext_stats["n_dates"], 10, 0)
    _check(ext_stats["historical_PI"]["mae"], .4463621973)
    _check(ext_stats["LO_previous_day"]["mae"], .1558843083)
    _check(ext_stats["AAO_previous_day"]["mae"], .1676320452)

    sim_dir = ROOT / "results/analysis/massive_mechanism_map/6e23d5aabc519982"
    sim = json.loads((sim_dir/"mechanism_map_report.json").read_text(encoding="utf-8"))
    fig = json.loads((ROOT/"figures/publication/ten_million/figure_manifest.json").read_text(encoding="utf-8"))
    _check(sim["synthetic_datasets"], 10_000_000, 0)
    _check(sim["summary_rows"], 5880, 0)
    _check(sim["max_observed_abs_pi_minus_pm"], .15653617444596035)
    _check(sim["max_p99_abs_pi_minus_pm"], .12733794889857514)
    _check(fig["figures"]["1"]["taylor_cell_correlation"], .9995456741795187)
    mechanism={
        "run_id":sim["config_fingerprint"],
        "n_synthetic_histories":sim["synthetic_datasets"],
        "n_scenario_cells":sim["summary_rows"],
        "root_seed":sim["config"]["root_seed"],
        "maximum_observed_abs_PI_minus_PM":sim["max_observed_abs_pi_minus_pm"],
        "max_cell_p99_abs_PI_minus_PM":sim["max_p99_abs_pi_minus_pm"],
        "figure_1_Taylor_cell_correlation":fig["figures"]["1"]["taylor_cell_correlation"],
        "level":"reported-run metadata and figure manifest cross-check; no GPU rerun",
    }
    result={
        "audit":"REMEF internal numerical cross-check",
        "status":"arithmetic_spot_checks_passed_not_submission_clearance",
        "october":oct_stats,
        "strict_forward":main_stats,
        "cross_instrument_LO":ext_stats,
        "synthetic_mechanism":mechanism,
        "open_critical_gates":[
            "Original market timestamps and permitted as-of information vintages",
            "Vendor licenses and public Git history containing raw files",
            "Independent settlement/transaction-price identity and data quality",
            "2,381-row prior-IV smile predictions verified only by summary, not fully rederived here",
            "2,366-row same-contract prior-IV result not independently recomputed here",
            "Exact original LO CRR tree input/cutoff and benchmark reproducibility beyond errors",
            "Original manuscript scientific literature/novelty independent referee check",
            "REMEF bilingual Word layouts, links, anonymization, forms and submission checks",
        ],
        "do_not_claim_full_reproduction":True,
    }
    return result


def main() -> None:
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--write-json",action="store_true",
                   help="Write aggregate JSON, refusing to overwrite previous output")
    args=p.parse_args()
    out=audit()
    print(json.dumps(out,indent=2))
    if args.write_json:
        if OUT.exists():
            raise FileExistsError(f"Cannot overwrite existing audit: {OUT}")
        OUT.parent.mkdir(parents=True,exist_ok=True)
        OUT.write_text(json.dumps(out,indent=2)+"\n",encoding="utf-8")
        print(f"Saved aggregate audit: {OUT}")


if __name__=="__main__":
    main()
