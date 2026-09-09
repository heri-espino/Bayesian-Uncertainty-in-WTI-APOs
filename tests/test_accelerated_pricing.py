import inspect

import numpy as np

from src.accelerated_pricing import (
    asian_arithmetic_call_mc_chunked,
    backend_info,
)
from src.asian_pricing import asian_arithmetic_call_mc


def test_numpy_backend_is_always_available():
    info = backend_info("numpy")
    assert info["backend"] == "numpy"


def test_accelerated_pricer_excludes_physical_drift():
    params = inspect.signature(asian_arithmetic_call_mc_chunked).parameters
    assert "mu" not in params


def test_chunked_control_variate_reduces_standard_error():
    estimate = asian_arithmetic_call_mc_chunked(
        100.0,
        100.0,
        0.03,
        0.25,
        1.0,
        n_steps=32,
        n_paths=8_000,
        seed=2026,
        backend="numpy",
        chunk_size=2_000,
    )
    assert np.isfinite(estimate.price)
    assert estimate.price > 0.0
    assert estimate.standard_error < estimate.raw_standard_error
    assert estimate.n_paths == 8_000


def test_chunked_and_reference_pricers_agree_within_mc_error():
    chunked = asian_arithmetic_call_mc_chunked(
        100.0,
        100.0,
        0.03,
        0.25,
        1.0,
        n_steps=32,
        n_paths=20_000,
        seed=31,
        backend="numpy",
        chunk_size=5_000,
    )
    reference = asian_arithmetic_call_mc(
        100.0,
        100.0,
        0.03,
        0.25,
        1.0,
        n_steps=32,
        n_paths=20_000,
        seed=47,
        antithetic=True,
        geometric_control=True,
    )
    tolerance = 6.0 * np.sqrt(
        chunked.standard_error**2 + reference.standard_error**2
    )
    assert abs(chunked.price - reference.price) <= max(tolerance, 0.03)
