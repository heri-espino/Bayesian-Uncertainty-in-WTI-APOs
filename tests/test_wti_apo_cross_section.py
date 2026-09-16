import numpy as np

from bayesian_asian_options.wti_apo_pricing import (
    wti_apo_cross_section_mc,
    wti_average_price_option_mc,
)


def test_direct_discount_factor_is_supported() -> None:
    est = wti_average_price_option_mc(
        realized_fixings=np.array([90.0, 100.0, 110.0]),
        forward_fixings=np.array([]),
        fixing_times=np.array([]),
        strike=95.0,
        sigma=0.30,
        rate=None,
        time_to_expiry=1.0,
        discount_factor=0.95,
        option_type="call",
        n_paths=1000,
        seed=1,
    )
    assert est.price == 4.75


def test_cross_section_reuses_same_average_paths() -> None:
    common = dict(
        realized_fixings=np.array([]),
        forward_fixings=np.array([95.0, 100.0, 105.0]),
        fixing_times=np.array([10, 20, 30]) / 365.0,
        sigma=0.35,
        rate=None,
        time_to_expiry=30 / 365.0,
        discount_factor=0.99,
        n_paths=20_000,
        seed=7,
    )
    cross = wti_apo_cross_section_mc(
        strikes=np.array([95.0, 105.0]),
        option_types=["call", "call"],
        **common,
    )
    single = wti_average_price_option_mc(
        strike=95.0,
        option_type="call",
        **common,
    )
    assert np.isclose(cross.prices[0], single.price)
    assert cross.prices[0] > cross.prices[1]
