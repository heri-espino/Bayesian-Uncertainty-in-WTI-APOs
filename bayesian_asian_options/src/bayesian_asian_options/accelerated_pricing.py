"""Chunked CPU/GPU Monte Carlo for arithmetic Asian calls.

The implementation is designed for long publication runs.  It keeps only one chunk of
paths in device memory and accumulates sufficient statistics, so path counts can be
increased without requiring a correspondingly large RAM/VRAM allocation.

GPU execution is optional and uses CuPy when available.  CPU execution uses NumPy.
The physical drift ``mu`` is intentionally absent: pricing is under Q with drift r-q.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import numpy as np

from bayesian_asian_options.asian_pricing import discrete_geometric_asian_call_price


@dataclass(frozen=True)
class AcceleratedMonteCarloEstimate:
    price: float
    standard_error: float
    raw_price: float
    raw_standard_error: float
    control_beta: float
    n_paths: int
    backend: str
    chunk_size: int


def _backend(name: str):
    name = name.lower()
    if name not in {"auto", "numpy", "cupy"}:
        raise ValueError("backend must be 'auto', 'numpy', or 'cupy'")
    if name in {"auto", "cupy"}:
        try:
            import cupy as cp  # type: ignore

            if cp.cuda.runtime.getDeviceCount() > 0:
                return cp, "cupy"
        except Exception:
            if name == "cupy":
                raise RuntimeError(
                    "CuPy GPU backend requested but no working CUDA/CuPy device was found"
                )
    return np, "numpy"


def backend_info(name: str = "auto") -> dict[str, Any]:
    """Return lightweight information about the selected numerical backend."""
    xp, resolved = _backend(name)
    info: dict[str, Any] = {"backend": resolved}
    if resolved == "cupy":
        device = xp.cuda.Device()
        props = xp.cuda.runtime.getDeviceProperties(device.id)
        raw_name = props.get("name", b"unknown")
        if isinstance(raw_name, bytes):
            raw_name = raw_name.decode(errors="replace")
        info.update(
            {
                "device_id": int(device.id),
                "device_name": str(raw_name),
                "total_global_memory_bytes": int(props.get("totalGlobalMem", 0)),
                "cupy_version": xp.__version__,
            }
        )
    else:
        info["numpy_version"] = np.__version__
    return info


def _scalar(value: Any, resolved: str) -> float:
    if resolved == "cupy":
        import cupy as cp  # type: ignore

        return float(cp.asnumpy(value))
    return float(value)


def asian_arithmetic_call_mc_chunked(
    S0: float,
    K: float,
    r: float,
    sigma: float,
    T: float,
    *,
    q: float = 0.0,
    n_steps: int = 252,
    n_paths: int = 1_000_000,
    seed: int = 12345,
    backend: str = "auto",
    chunk_size: int = 100_000,
    antithetic: bool = True,
    geometric_control: bool = True,
) -> AcceleratedMonteCarloEstimate:
    """Price a discretely monitored arithmetic Asian call in bounded memory.

    Sufficient statistics for the arithmetic payoff Y and geometric control X are
    accumulated across chunks.  The global control coefficient and adjusted standard
    error are therefore computed as if all discounted payoff pairs had been retained.
    """
    if S0 <= 0 or K < 0 or sigma <= 0 or T <= 0:
        raise ValueError("invalid model inputs")
    if n_steps < 1 or n_paths < 2 or chunk_size < 2:
        raise ValueError("n_steps>=1, n_paths>=2, and chunk_size>=2 are required")

    xp, resolved = _backend(backend)
    rng = xp.random.RandomState(int(seed))
    dt = T / n_steps
    sqrt_dt = float(np.sqrt(dt))
    discount = float(np.exp(-r * T))

    n_total = 0
    sum_y = sum_x = sum_y2 = sum_x2 = sum_xy = 0.0

    while n_total < n_paths:
        m = min(chunk_size, n_paths - n_total)
        if antithetic:
            half = (m + 1) // 2
            z_half = rng.standard_normal((half, n_steps))
            z = xp.concatenate((z_half, -z_half), axis=0)[:m]
        else:
            z = rng.standard_normal((m, n_steps))

        increments = (r - q - 0.5 * sigma**2) * dt + sigma * sqrt_dt * z
        log_paths = np.log(S0) + xp.cumsum(increments, axis=1)
        paths = xp.exp(log_paths)
        arithmetic = xp.mean(paths, axis=1)
        geometric = xp.exp(xp.mean(log_paths, axis=1))

        y = discount * xp.maximum(arithmetic - K, 0.0)
        x = discount * xp.maximum(geometric - K, 0.0)

        sum_y += _scalar(xp.sum(y), resolved)
        sum_x += _scalar(xp.sum(x), resolved)
        sum_y2 += _scalar(xp.sum(y * y), resolved)
        sum_x2 += _scalar(xp.sum(x * x), resolved)
        sum_xy += _scalar(xp.sum(x * y), resolved)
        n_total += m

        del z, increments, log_paths, paths, arithmetic, geometric, y, x
        if resolved == "cupy":
            xp.get_default_memory_pool().free_all_blocks()

    n = float(n_total)
    mean_y = sum_y / n
    mean_x = sum_x / n
    var_y = max((sum_y2 - n * mean_y**2) / (n - 1.0), 0.0)
    var_x = max((sum_x2 - n * mean_x**2) / (n - 1.0), 0.0)
    cov_xy = (sum_xy - n * mean_x * mean_y) / (n - 1.0)

    raw_se = float(np.sqrt(var_y / n))
    beta = 0.0
    price = mean_y
    adjusted_var = var_y

    if geometric_control and var_x > 0.0:
        beta = cov_xy / var_x
        control_mean = discrete_geometric_asian_call_price(
            S0, K, r, sigma, T, q=q, n_steps=n_steps
        )
        price = mean_y - beta * (mean_x - control_mean)
        adjusted_var = max(var_y + beta**2 * var_x - 2.0 * beta * cov_xy, 0.0)

    return AcceleratedMonteCarloEstimate(
        price=float(price),
        standard_error=float(np.sqrt(adjusted_var / n)),
        raw_price=float(mean_y),
        raw_standard_error=raw_se,
        control_beta=float(beta),
        n_paths=n_total,
        backend=resolved,
        chunk_size=int(chunk_size),
    )
