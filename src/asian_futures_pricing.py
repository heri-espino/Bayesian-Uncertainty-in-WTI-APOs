"""Asian-option pricing wrappers for a lognormal futures price under Q.

With deterministic interest rates, a futures price is modeled here as

    dF_t = sigma F_t dW_t^Q,

so its risk-neutral drift is zero.  The existing spot-style pricer implements drift
``r-q``; setting ``q=r`` therefore gives the futures dynamics while retaining the
usual discount factor exp(-rT).
"""

from __future__ import annotations

from src.accelerated_pricing import (
    AcceleratedMonteCarloEstimate,
    asian_arithmetic_call_mc_chunked,
)
from src.asian_pricing import MonteCarloEstimate, asian_arithmetic_call_mc


def asian_futures_arithmetic_call_mc(
    F0: float,
    K: float,
    r: float,
    sigma: float,
    T: float,
    *,
    n_steps: int = 252,
    n_paths: int = 100_000,
    seed: int | None = None,
) -> MonteCarloEstimate:
    """Price an arithmetic Asian call on a lognormal futures-price process."""
    return asian_arithmetic_call_mc(
        F0,
        K,
        r,
        sigma,
        T,
        q=r,
        n_steps=n_steps,
        n_paths=n_paths,
        seed=seed,
        antithetic=True,
        geometric_control=True,
    )


def asian_futures_arithmetic_call_mc_chunked(
    F0: float,
    K: float,
    r: float,
    sigma: float,
    T: float,
    *,
    n_steps: int = 252,
    n_paths: int = 1_000_000,
    seed: int = 12345,
    backend: str = "auto",
    chunk_size: int = 100_000,
) -> AcceleratedMonteCarloEstimate:
    """CPU/GPU chunked version of the lognormal-futures Asian pricer."""
    return asian_arithmetic_call_mc_chunked(
        F0,
        K,
        r,
        sigma,
        T,
        q=r,
        n_steps=n_steps,
        n_paths=n_paths,
        seed=seed,
        backend=backend,
        chunk_size=chunk_size,
        antithetic=True,
        geometric_control=True,
    )
