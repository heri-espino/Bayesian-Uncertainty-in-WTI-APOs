# Compute environment and long-run experiment policy

This project is intentionally configured for computation-heavy synthetic experiments.  Wall-clock time is not treated as a binding research constraint; statistical quality, reproducibility, and restartability take priority over finishing quickly.

## Observed workstation specifications

The following specifications were visually confirmed from Windows Task Manager on 2026-09-09:

- Dedicated GPU: **NVIDIA RTX 4500 Ada Generation**.
- Integrated GPU: **Intel UHD Graphics 770**.
- System memory: approximately **64 GB RAM** (Task Manager displayed 63.6 GB usable).
- Primary storage: **NVMe SSD**.
- Operating system family: Windows.

The screenshot did **not** show the exact CPU model or the dedicated VRAM capacity of the RTX 4500.  Those values must not be inferred from the shared-memory figure shown for the Intel iGPU.  Long experiment manifests therefore also query the actual machine at runtime and, when available, record `nvidia-smi` GPU name, VRAM, and driver version, logical CPU count, platform, Python, NumPy, and selected numerical backend.

Before a definitive publication run, capture:

```powershell
nvidia-smi
python --version
python -c "import os, platform; print(platform.processor()); print(os.cpu_count())"
pip freeze > results/environment-freeze.txt
```

## Compute policy

The experimental design should not be weakened merely to save runtime.  In particular:

1. Prefer many independent repeated-sampling replications over a single illustrative trajectory.
2. Use dense risk-neutral pricing grids with common random numbers and variance reduction.
3. Evaluate multiple historical sample lengths, true volatilities, moneyness levels, and maturities.
4. Keep Monte Carlo standard error materially below the parameter-estimation error being studied.
5. Use the GPU for path simulation/pricing and CPU processes for independent posterior fits.
6. Keep deterministic root seeds and record software/hardware metadata for each run.
7. Never rely on an uninterrupted interactive session to finish a publication experiment.

## Parallelization strategy

### GPU

GPU acceleration is most useful for the risk-neutral Monte Carlo layer.  The project provides `src/accelerated_pricing.py`, which can use CuPy and processes paths in bounded-memory chunks.  The geometric Asian control variate is evaluated from global sufficient statistics accumulated over all chunks.

The low-dimensional Random-Walk Metropolis chain itself is sequential and is not expected to benefit much from moving one chain to the GPU.  GPU resources are therefore reserved for the path-simulation workload where vectorization is large.

### CPU

Independent synthetic datasets/posterior fits are embarrassingly parallel.  `experiments/large_scale_synthetic.py` distributes these units with `ProcessPoolExecutor`.  By default it leaves one logical CPU free; `--workers N` can override this.

## Checkpoint and resume policy

Long runs are designed for machines that may disconnect or terminate a user session.

### Pricing checkpoints

Run:

```powershell
python -m experiments.precompute_pricing_grids --preset research --backend auto
```

or, after validating CuPy/CUDA:

```powershell
python -m experiments.precompute_pricing_grids --preset extreme --backend cupy
```

Every `(moneyness, maturity, sigma-grid point)` is saved as an atomic `.npz` checkpoint.  Re-running the command scans these files and computes only missing points.  When all points of a contract are complete, they are assembled into the full pricing-grid checkpoint expected by the large-scale experiment.

A disconnection therefore loses at most the currently running grid point, not the whole grid.

### Inference checkpoints

Run:

```powershell
python -m experiments.large_scale_synthetic --preset research --backend auto
```

Each `(n_obs, sigma_true, replication)` posterior fit is saved independently.  Posterior volatility draws are retained in compressed form so that new contract specifications can reuse the inference without rerunning MCMC.

The run directory is determined by a SHA-256 fingerprint of the full configuration.  Re-running the same command resumes the same experiment; changing a scientifically relevant configuration creates a different fingerprint and therefore a different run directory.

`progress.json` and `pricing_progress.json` provide human-readable progress snapshots.

## Presets

### `quick`

A smoke/integration test.  It is not evidence for the manuscript.

### `research`

Default large experiment:

- `n_obs = {63, 252, 1260}` with `dt = 1/252`, corresponding to roughly 0.25, 1, and 5 years of historical daily returns;
- `sigma_true = {0.15, 0.25, 0.40}`;
- `K/S0 = {0.80, 1.00, 1.20}`;
- `T = {0.50, 1.00, 2.00}`;
- 1,000 posterior replications for every `(n_obs, sigma_true)` pair: **9,000 independent posterior fits**;
- 12,000 MCMC iterations per fit;
- 121 volatility-grid points for every `(moneyness, maturity)` contract;
- 500,000 risk-neutral paths per grid point.

The 9,000 posterior fits are reused over 9 contract specifications, yielding 81,000 pricing-evaluation rows without rerunning inference.

### `extreme`

High-compute robustness run:

- 2,000 posterior replications per `(n_obs, sigma_true)`: **18,000 posterior fits**;
- 20,000 MCMC iterations per fit;
- 161 pricing-grid points per contract;
- 2,000,000 paths per pricing-grid point;
- wider volatility interpolation range.

This preset intentionally prioritizes numerical precision and repeated-sampling stability over runtime.

## Recommended execution sequence

1. Run the normal test suite.
2. Run `synthetic_validation --quick`.
3. Verify `nvidia-smi` and install a compatible CuPy build if GPU acceleration is desired.
4. Run `precompute_pricing_grids` and allow it to checkpoint all GPU pricing points.
5. Run `large_scale_synthetic`; it will reuse the completed grids and parallelize missing posterior fits.
6. Re-run the same command after any disconnect; completed checkpoints are preserved.
7. Archive the final run directory, `manifest.json`, environment freeze, and Git commit used for the manuscript.

## Scientific note

The large-scale experiment fixes historical observation spacing at `1/252` year.  Thus increasing `n_obs` increases the historical time span rather than merely sampling the same one-year interval more finely.  This is the appropriate interpretation when the study asks how additional historical information changes posterior uncertainty.
