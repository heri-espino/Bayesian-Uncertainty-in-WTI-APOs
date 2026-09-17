import numpy as np
from scipy.special import ndtr

from bayesian_asian_options.asian_futures_pricing import curran_arithmetic_futures_option
from bayesian_asian_options.wti_apo_pricing import wti_average_price_option_mc


def _black_futures_call(F: float, K: float, sigma: float, T: float, discount: float) -> float:
    vol = sigma * np.sqrt(T)
    d1 = (np.log(F / K) + 0.5 * vol**2) / vol
    d2 = d1 - vol
    return float(discount * (F * ndtr(d1) - K * ndtr(d2)))


def test_curran_is_exact_for_one_future_fixing():
    F = 82.0
    K = 80.0
    sigma = 0.35
    T = 0.4
    discount = 0.98
    estimate = curran_arithmetic_futures_option(
        realized_fixings=np.array([]),
        forward_fixings=np.array([F]),
        fixing_times=np.array([T]),
        strike=K,
        sigma=sigma,
        discount_factor=discount,
        option_type="call",
    )
    target = _black_futures_call(F, K, sigma, T, discount)
    assert abs(estimate - target) < 1e-10


def test_curran_put_call_parity_with_realized_fixings():
    realized = np.array([78.0, 79.0])
    forwards = np.array([81.0, 82.0, 83.0])
    times = np.array([0.05, 0.10, 0.15])
    strike = 80.0
    discount = 0.99
    call = curran_arithmetic_futures_option(
        realized_fixings=realized,
        forward_fixings=forwards,
        fixing_times=times,
        strike=strike,
        sigma=0.30,
        discount_factor=discount,
        option_type="call",
    )
    put = curran_arithmetic_futures_option(
        realized_fixings=realized,
        forward_fixings=forwards,
        fixing_times=times,
        strike=strike,
        sigma=0.30,
        discount_factor=discount,
        option_type="put",
    )
    expected_average = np.concatenate([realized, forwards]).mean()
    assert abs((call - put) - discount * (expected_average - strike)) < 1e-10


def test_curran_tracks_high_precision_mc_for_regular_case():
    forwards = np.full(12, 100.0)
    times = np.linspace(1 / 12, 1.0, 12)
    curran = curran_arithmetic_futures_option(
        realized_fixings=np.array([]),
        forward_fixings=forwards,
        fixing_times=times,
        strike=100.0,
        sigma=0.20,
        discount_factor=np.exp(-0.03),
        option_type="call",
    )
    mc = wti_average_price_option_mc(
        realized_fixings=np.array([]),
        forward_fixings=forwards,
        fixing_times=times,
        strike=100.0,
        sigma=0.20,
        rate=None,
        time_to_expiry=1.0,
        discount_factor=np.exp(-0.03),
        option_type="call",
        n_paths=200_000,
        seed=17,
        antithetic=True,
    )
    assert abs(curran - mc.price) < 0.08


def test_curran_all_realized_is_discounted_intrinsic():
    price = curran_arithmetic_futures_option(
        realized_fixings=np.array([70.0, 72.0]),
        forward_fixings=np.array([]),
        fixing_times=np.array([]),
        strike=69.0,
        sigma=0.40,
        discount_factor=0.99,
        option_type="call",
    )
    assert price == 0.99 * (71.0 - 69.0)
