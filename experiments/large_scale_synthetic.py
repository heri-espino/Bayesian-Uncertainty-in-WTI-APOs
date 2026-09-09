"""Large-scale, resumable synthetic experiment for the publication study.

Architecture
------------
* Historical inference is embarrassingly parallel on CPU and is checkpointed per
  (n_obs, sigma_true, replication).
* Risk-neutral Asian pricing grids are computed once per (moneyness, maturity), using
  the optional CuPy GPU backend when available.
* Posterior draws are stored in compressed checkpoints.  Pricing rules are evaluated
  later by interpolation, avoiding redundant MCMC when contract terms change.
* Every checkpoint is atomic.  Re-running the same configuration resumes from the
  missing units rather than starting over.

Run examples
------------
    python -m experiments.large_scale_synthetic --preset quick
    python -m experiments.large_scale_synthetic --preset research --backend auto
    python -m experiments.large_scale_synthetic --preset extreme --backend cupy
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import platform
import subprocess
from concurrent.futures import ProcessPoolExecutor, as_completed
from dataclasses import asdict, dataclass, replace
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

from src.accelerated_pricing import asian_arithmetic_call_mc_chunked, backend_info
from src.bayesian_gbm import gbm_log_returns, gbm_mle, random_walk_metropolis_gbm


SCRIPT_VERSION = "1.0.0"


@dataclass(frozen=True)
class LargeScaleConfig:
    root_seed: int = 20260909
    mu_true: float = 0.08
    S0: float = 100.0
    r: float = 0.03
    q: float = 0.0
    historical_dt: float = 1.0 / 252.0
    sample_sizes: tuple[int, ...] = (63, 252, 1260)
    sigma_true_values: tuple[float, ...] = (0.15, 0.25, 0.40)
    moneyness_values: tuple[float, ...] = (0.80, 1.00, 1.20)
    maturities: tuple[float, ...] = (0.50, 1.00, 2.00)
    replications: int = 1000
    mcmc_iter: int = 12_000
    burn_in: int = 2_400
    posterior_thin: int = 2
    base_proposal_mu_sd: float = 0.30
    base_proposal_logsigma_sd: float = 0.08
    price_sigma_min: float = 0.03
    price_sigma_max: float = 0.90
    price_grid_points: int = 121
    pricing_paths: int = 500_000
    pricing_chunk_size: int = 50_000


@dataclass(frozen=True)
class QuickConfig(LargeScaleConfig):
    sample_sizes: tuple[int, ...] = (63, 252)
    sigma_true_values: tuple[float, ...] = (0.15, 0.25)
    moneyness_values: tuple[float, ...] = (0.80, 1.00, 1.20)
    maturities: tuple[float, ...] = (0.50, 1.00)
    replications: int = 4
    mcmc_iter: int = 2_000
    burn_in: int = 400
    posterior_thin: int = 2
    price_grid_points: int = 21
    pricing_paths: int = 5_000
    pricing_chunk_size: int = 2_500


@dataclass(frozen=True)
class ExtremeConfig(LargeScaleConfig):
    replications: int = 2000
    mcmc_iter: int = 20_000
    burn_in: int = 4_000
    posterior_thin: int = 2
    price_sigma_min: float = 0.02
    price_sigma_max: float = 1.00
    price_grid_points: int = 161
    pricing_paths: int = 2_000_000
    pricing_chunk_size: int = 100_000


def _seed(root: int, family: int, *parts: int) -> int:
    return int(
        np.random.SeedSequence([root, family, *parts]).generate_state(
            1, dtype=np.uint32
        )[0]
    )


def _fingerprint(cfg: LargeScaleConfig) -> str:
    payload = json.dumps(asdict(cfg), sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode()).hexdigest()[:16]


def _atomic_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    with tmp.open("w", encoding="utf-8") as fh:
        json.dump(payload, fh, indent=2, sort_keys=True)
        fh.write("\n")
    os.replace(tmp, path)


def _atomic_npz(path: Path, **arrays: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(".tmp.npz")
    np.savez_compressed(tmp, **arrays)
    os.replace(tmp, path)


def _git_commit() -> str | None:
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], text=True, stderr=subprocess.DEVNULL
        ).strip()
    except Exception:
        return None


def _nvidia_smi() -> list[dict[str, str]]:
    try:
        output = subprocess.check_output(
            [
                "nvidia-smi",
                "--query-gpu=name,memory.total,driver_version",
                "--format=csv,noheader,nounits",
            ],
            text=True,
            stderr=subprocess.DEVNULL,
        )
    except Exception:
        return []
    rows = []
    for line in output.splitlines():
        parts = [x.strip() for x in line.split(",")]
        if len(parts) == 3:
            rows.append(
                {
                    "name": parts[0],
                    "memory_total_mib": parts[1],
                    "driver_version": parts[2],
                }
            )
    return rows


def _hardware_manifest(backend: str) -> dict[str, Any]:
    try:
        selected_backend = backend_info(backend)
    except Exception as exc:
        selected_backend = {"backend": backend, "error": repr(exc)}
    return {
        "platform": platform.platform(),
        "processor": platform.processor(),
        "machine": platform.machine(),
        "logical_cpu_count": os.cpu_count(),
        "python": platform.python_version(),
        "numpy": np.__version__,
        "nvidia_smi": _nvidia_smi(),
        "selected_backend": selected_backend,
    }


def _monitoring_steps(T: float) -> int:
    return max(1, int(round(252 * T)))


def _proposal(cfg: LargeScaleConfig, n_obs: int) -> tuple[float, float]:
    scale = float(np.sqrt(252.0 / n_obs))
    return (
        cfg.base_proposal_mu_sd * scale,
        cfg.base_proposal_logsigma_sd * scale,
    )


def _inference_checkpoint_path(
    run_dir: Path, n_obs: int, sigma_index: int, replication: int
) -> Path:
    return (
        run_dir
        / "checkpoints"
        / "inference"
        / f"n{n_obs}_s{sigma_index:02d}"
        / f"rep_{replication:06d}.npz"
    )


def _run_inference_unit(
    cfg: LargeScaleConfig,
    n_obs: int,
    sigma_true: float,
    sigma_index: int,
    replication: int,
) -> dict[str, Any]:
    data_seed = _seed(cfg.root_seed, 501, n_obs, sigma_index, replication)
    chain_seed = _seed(cfg.root_seed, 502, n_obs, sigma_index, replication)
    returns = gbm_log_returns(
        mu=cfg.mu_true,
        sigma=sigma_true,
        dt=cfg.historical_dt,
        n_obs=n_obs,
        seed=data_seed,
    )
    mu_mle, sigma_mle = gbm_mle(returns, cfg.historical_dt)
    post = random_walk_metropolis_gbm(
        returns,
        cfg.historical_dt,
        n_iter=cfg.mcmc_iter,
        burn_in=cfg.burn_in,
        proposal_sd=_proposal(cfg, n_obs),
        seed=chain_seed,
    )
    thin = max(1, int(cfg.posterior_thin))
    sigma_draws = post.sigma[::thin].astype(np.float32)
    mu_draws = post.mu[::thin]
    mu_low, mu_high = np.percentile(mu_draws, [2.5, 97.5])
    sigma_low, sigma_high = np.percentile(sigma_draws, [2.5, 97.5])
    hist, edges = np.histogram(sigma_draws, bins="fd")
    mode_index = int(np.argmax(hist))
    sigma_mode = float(0.5 * (edges[mode_index] + edges[mode_index + 1]))
    return {
        "sigma_draws": sigma_draws,
        "meta": {
            "n_obs": n_obs,
            "sigma_true": sigma_true,
            "sigma_index": sigma_index,
            "replication": replication,
            "data_seed": data_seed,
            "chain_seed": chain_seed,
            "acceptance_rate": post.acceptance_rate,
            "mu_mle": mu_mle,
            "sigma_mle": sigma_mle,
            "mu_post_mean": float(np.mean(mu_draws)),
            "sigma_post_mean": float(np.mean(sigma_draws)),
            "sigma_post_median": float(np.median(sigma_draws)),
            "sigma_map_hist": sigma_mode,
            "mu_ci_low": float(mu_low),
            "mu_ci_high": float(mu_high),
            "sigma_ci_low": float(sigma_low),
            "sigma_ci_high": float(sigma_high),
            "mu_covered": int(mu_low <= cfg.mu_true <= mu_high),
            "sigma_covered": int(sigma_low <= sigma_true <= sigma_high),
        },
    }


def _save_inference_checkpoint(path: Path, result: dict[str, Any]) -> None:
    meta_json = json.dumps(result["meta"], sort_keys=True)
    _atomic_npz(
        path,
        sigma_draws=result["sigma_draws"],
        meta_json=np.array(meta_json),
    )


def _load_inference_checkpoint(path: Path) -> tuple[np.ndarray, dict[str, Any]]:
    with np.load(path, allow_pickle=False) as data:
        draws = data["sigma_draws"].astype(float)
        meta = json.loads(str(data["meta_json"].item()))
    return draws, meta


def _price_grid_path(run_dir: Path, mi: int, ti: int) -> Path:
    return run_dir / "checkpoints" / "pricing" / f"m{mi:02d}_t{ti:02d}.npz"


def _build_price_grid(
    cfg: LargeScaleConfig,
    run_dir: Path,
    *,
    backend: str,
    mi: int,
    ti: int,
    moneyness: float,
    maturity: float,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, str]:
    path = _price_grid_path(run_dir, mi, ti)
    if path.exists():
        with np.load(path, allow_pickle=False) as data:
            return (
                data["sigma_grid"].astype(float),
                data["prices"].astype(float),
                data["standard_errors"].astype(float),
                str(data["backend"].item()),
            )

    sigma_grid = np.linspace(
        cfg.price_sigma_min, cfg.price_sigma_max, cfg.price_grid_points
    )
    prices = np.empty_like(sigma_grid)
    ses = np.empty_like(sigma_grid)
    resolved_backend = "unknown"
    common_seed = _seed(cfg.root_seed, 601, mi, ti)
    K = cfg.S0 * moneyness
    steps = _monitoring_steps(maturity)

    for i, sigma in enumerate(sigma_grid):
        estimate = asian_arithmetic_call_mc_chunked(
            cfg.S0,
            K,
            cfg.r,
            float(sigma),
            maturity,
            q=cfg.q,
            n_steps=steps,
            n_paths=cfg.pricing_paths,
            seed=common_seed,
            backend=backend,
            chunk_size=cfg.pricing_chunk_size,
            antithetic=True,
            geometric_control=True,
        )
        prices[i] = estimate.price
        ses[i] = estimate.standard_error
        resolved_backend = estimate.backend

    _atomic_npz(
        path,
        sigma_grid=sigma_grid,
        prices=prices,
        standard_errors=ses,
        backend=np.array(resolved_backend),
        moneyness=np.array(moneyness),
        maturity=np.array(maturity),
        monitoring_steps=np.array(steps),
        seed=np.array(common_seed),
    )
    return sigma_grid, prices, ses, resolved_backend


def _interp_prices(draws: np.ndarray, sigma_grid: np.ndarray, prices: np.ndarray) -> np.ndarray:
    if draws.min() < sigma_grid[0] or draws.max() > sigma_grid[-1]:
        raise RuntimeError(
            f"posterior sigma outside pricing grid: [{draws.min():.4g}, {draws.max():.4g}] "
            f"vs [{sigma_grid[0]:.4g}, {sigma_grid[-1]:.4g}]"
        )
    return np.interp(draws, sigma_grid, prices)


def _run_inference_stage(
    cfg: LargeScaleConfig, run_dir: Path, workers: int
) -> tuple[int, int]:
    tasks: list[tuple[int, float, int, int, Path]] = []
    total = 0
    for n_obs in cfg.sample_sizes:
        for si, sigma_true in enumerate(cfg.sigma_true_values):
            for rep in range(cfg.replications):
                total += 1
                path = _inference_checkpoint_path(run_dir, n_obs, si, rep)
                if not path.exists():
                    tasks.append((n_obs, sigma_true, si, rep, path))

    completed_before = total - len(tasks)
    _atomic_json(
        run_dir / "progress.json",
        {
            "stage": "inference",
            "total_units": total,
            "completed_units": completed_before,
            "remaining_units": len(tasks),
            "updated_at_utc": datetime.now(timezone.utc).isoformat(),
        },
    )
    if not tasks:
        return total, total

    done = completed_before
    with ProcessPoolExecutor(max_workers=workers) as pool:
        futures = {
            pool.submit(_run_inference_unit, cfg, n, s, si, rep): path
            for n, s, si, rep, path in tasks
        }
        for future in as_completed(futures):
            result = future.result()
            _save_inference_checkpoint(futures[future], result)
            done += 1
            if done % 10 == 0 or done == total:
                _atomic_json(
                    run_dir / "progress.json",
                    {
                        "stage": "inference",
                        "total_units": total,
                        "completed_units": done,
                        "remaining_units": total - done,
                        "updated_at_utc": datetime.now(timezone.utc).isoformat(),
                    },
                )
    return done, total


def _aggregate(
    cfg: LargeScaleConfig,
    run_dir: Path,
    price_grids: dict[tuple[int, int], tuple[np.ndarray, np.ndarray]],
) -> tuple[pd.DataFrame, pd.DataFrame]:
    rows: list[dict[str, Any]] = []
    for n_obs in cfg.sample_sizes:
        for si, sigma_true in enumerate(cfg.sigma_true_values):
            for rep in range(cfg.replications):
                draws, meta = _load_inference_checkpoint(
                    _inference_checkpoint_path(run_dir, n_obs, si, rep)
                )
                for mi, moneyness in enumerate(cfg.moneyness_values):
                    for ti, maturity in enumerate(cfg.maturities):
                        sigma_grid, prices = price_grids[(mi, ti)]
                        posterior_prices = _interp_prices(draws, sigma_grid, prices)
                        benchmark = float(np.interp(sigma_true, sigma_grid, prices))
                        pm = float(np.interp(meta["sigma_post_mean"], sigma_grid, prices))
                        map_price = float(np.interp(meta["sigma_map_hist"], sigma_grid, prices))
                        mle = float(np.interp(meta["sigma_mle"], sigma_grid, prices))
                        lo, hi = np.percentile(posterior_prices, [2.5, 97.5])
                        rows.append(
                            {
                                "n_obs": n_obs,
                                "history_years": n_obs * cfg.historical_dt,
                                "sigma_true": sigma_true,
                                "replication": rep,
                                "moneyness_K_over_S0": moneyness,
                                "maturity": maturity,
                                "monitoring_steps": _monitoring_steps(maturity),
                                "benchmark": benchmark,
                                "full_bayes": float(np.mean(posterior_prices)),
                                "postmean_plugin": pm,
                                "map_plugin": map_price,
                                "mle_plugin": mle,
                                "price_ci_low": float(lo),
                                "price_ci_high": float(hi),
                                "price_covered": int(lo <= benchmark <= hi),
                                "acceptance_rate": meta["acceptance_rate"],
                                "sigma_post_mean": meta["sigma_post_mean"],
                                "sigma_mle": meta["sigma_mle"],
                            }
                        )

    raw = pd.DataFrame(rows)
    group_cols = ["n_obs", "sigma_true", "moneyness_K_over_S0", "maturity"]
    summary_rows: list[dict[str, Any]] = []
    for keys, group in raw.groupby(group_cols, sort=True):
        base = dict(zip(group_cols, keys))
        for method in ("full_bayes", "postmean_plugin", "map_plugin", "mle_plugin"):
            err = group[method] - group["benchmark"]
            summary_rows.append(
                {
                    **base,
                    "method": method,
                    "replications": len(group),
                    "bias": float(err.mean()),
                    "mae": float(np.mean(np.abs(err))),
                    "rmse": float(np.sqrt(np.mean(err**2))),
                    "coverage_95": float(group["price_covered"].mean()),
                    "mean_acceptance_rate": float(group["acceptance_rate"].mean()),
                }
            )
    return raw, pd.DataFrame(summary_rows)


def _config_for_preset(name: str) -> LargeScaleConfig:
    if name == "quick":
        return QuickConfig()
    if name == "research":
        return LargeScaleConfig()
    if name == "extreme":
        return ExtremeConfig()
    raise ValueError(name)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--preset", choices=("quick", "research", "extreme"), default="research")
    parser.add_argument("--backend", choices=("auto", "numpy", "cupy"), default="auto")
    parser.add_argument("--workers", type=int, default=max(1, (os.cpu_count() or 2) - 1))
    parser.add_argument("--seed", type=int, default=None)
    parser.add_argument("--replications", type=int, default=None)
    parser.add_argument("--output-root", type=Path, default=Path("results/large_scale_synthetic"))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    cfg = _config_for_preset(args.preset)
    if args.seed is not None:
        cfg = replace(cfg, root_seed=args.seed)
    if args.replications is not None:
        if args.replications < 1:
            raise ValueError("replications must be positive")
        cfg = replace(cfg, replications=args.replications)
    if args.workers < 1:
        raise ValueError("workers must be positive")

    fingerprint = _fingerprint(cfg)
    run_dir = args.output_root / fingerprint
    run_dir.mkdir(parents=True, exist_ok=True)
    manifest_path = run_dir / "manifest.json"
    manifest = {
        "script_version": SCRIPT_VERSION,
        "config_fingerprint": fingerprint,
        "preset": args.preset,
        "config": asdict(cfg),
        "git_commit": _git_commit(),
        "requested_backend": args.backend,
        "workers": args.workers,
        "hardware": _hardware_manifest(args.backend),
        "created_or_resumed_at_utc": datetime.now(timezone.utc).isoformat(),
        "checkpoint_policy": "atomic per inference replication and per pricing grid; reruns resume missing units",
    }
    _atomic_json(manifest_path, manifest)

    print(f"run_dir={run_dir}")
    print(f"config_fingerprint={fingerprint}")
    print("Building/resuming pricing grids...")
    price_grids: dict[tuple[int, int], tuple[np.ndarray, np.ndarray]] = {}
    pricing_backend_rows: list[dict[str, Any]] = []
    for mi, moneyness in enumerate(cfg.moneyness_values):
        for ti, maturity in enumerate(cfg.maturities):
            sg, prices, ses, resolved = _build_price_grid(
                cfg,
                run_dir,
                backend=args.backend,
                mi=mi,
                ti=ti,
                moneyness=moneyness,
                maturity=maturity,
            )
            price_grids[(mi, ti)] = (sg, prices)
            pricing_backend_rows.append(
                {
                    "moneyness": moneyness,
                    "maturity": maturity,
                    "backend": resolved,
                    "max_pricing_se": float(np.max(ses)),
                }
            )

    print("Running/resuming CPU-parallel inference checkpoints...")
    done, total = _run_inference_stage(cfg, run_dir, args.workers)
    print(f"inference_checkpoints={done}/{total}")

    print("Aggregating pricing rules...")
    raw, summary = _aggregate(cfg, run_dir, price_grids)
    raw.to_csv(run_dir / "pricing_results_raw.csv", index=False)
    summary.to_csv(run_dir / "pricing_results_summary.csv", index=False)
    pd.DataFrame(pricing_backend_rows).to_csv(
        run_dir / "pricing_backend_summary.csv", index=False
    )

    manifest["completed_at_utc"] = datetime.now(timezone.utc).isoformat()
    manifest["inference_checkpoints"] = {"completed": done, "total": total}
    manifest["raw_rows"] = len(raw)
    manifest["summary_rows"] = len(summary)
    _atomic_json(manifest_path, manifest)
    _atomic_json(
        run_dir / "progress.json",
        {
            "stage": "complete",
            "total_units": total,
            "completed_units": done,
            "remaining_units": 0,
            "updated_at_utc": datetime.now(timezone.utc).isoformat(),
        },
    )
    print(f"complete: {run_dir}")


if __name__ == "__main__":
    main()
