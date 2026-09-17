import numpy as np

from experiments.taylor_mechanism import local_quadratic_curvature


def test_local_quadratic_curvature_recovers_second_derivative():
    sigma = np.linspace(0.10, 0.60, 41)
    prices = 3.0 + 2.0 * sigma + 4.0 * sigma**2
    curvature = local_quadratic_curvature(sigma, prices, 0.31, points=9)
    assert abs(curvature - 8.0) < 1e-10


def test_local_quadratic_curvature_rejects_outside_grid():
    sigma = np.linspace(0.10, 0.60, 11)
    prices = sigma**2
    try:
        local_quadratic_curvature(sigma, prices, 0.80)
    except ValueError as exc:
        assert "inside the pricing grid" in str(exc)
    else:
        raise AssertionError("expected ValueError")
