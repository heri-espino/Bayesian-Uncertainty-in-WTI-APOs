"""Integration checks for partial fixing against the committed WTI market data."""

from experiments.wti_apo_date_panel import _date_audit
from experiments.wti_apo_empirical import ROOT


def test_committed_september_data_exposes_eligible_partial_fixing_dates() -> None:
    audit = _date_audit(
        option_data_dir=ROOT / "data" / "csv",
        cl_data_dir=ROOT / "data" / "csv" / "CL",
        cl_expiry_file=ROOT / "data" / "csv" / "CL" / "contract_expiries.csv",
        apo_expiry="2026-09",
        min_open_interest=1.0,
        exclude_min_tick=True,
    )

    partial = audit[
        audit["eligible"]
        & (audit["fraction_fixed"] > 0.0)
        & (audit["fraction_fixed"] < 1.0)
    ]

    assert not partial.empty
    assert partial["realized_fixings_available"].all()
    assert partial["curve_available"].all()
