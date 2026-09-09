# Bayesian parameter uncertainty for Asian options

This repository studies Bayesian inference for a geometric Brownian motion (GBM) and the propagation of parameter uncertainty into arithmetic-average Asian option valuation.

> **Research status:** publication-oriented refactor on `main`. The legacy notebook is preserved for traceability, while the current codebase contains a rewritten manuscript, physical-measure inference, risk-neutral pricing, reproducible synthetic validation, checkpointed large-scale experiments, and automatic workstation metadata capture.

## Core distinction: physical inference vs. risk-neutral pricing

Historical returns are modeled under the physical measure \(\mathbb P\):

\[
dS_t = \mu S_t\,dt + \sigma S_t\,dW_t^{\mathbb P}.
\]

Bayesian inference targets \(p(\mu,\sigma\mid\mathcal D)\). In the Black-Scholes complete-market model, however, a traded contingent claim is priced under \(\mathbb Q\):

\[
dS_t = (r-q)S_t\,dt + \sigma S_t\,dW_t^{\mathbb Q}.
\]

The historical drift \(\mu\) therefore does **not** enter the pricing dynamics. Conditional on \(\sigma\), a discretely monitored arithmetic Asian call is

\[
C^{\mathbb Q}(\sigma)=e^{-rT}\,\mathbb E^{\mathbb Q}\!\left[(\bar S-K)^+\mid\sigma\right].
\]

Posterior parameter uncertainty is propagated through

\[
p(C\mid\mathcal D)=\int \delta_{C^{\mathbb Q}(\sigma)}\,p(\sigma\mid\mathcal D)\,d\sigma.
\]

The legacy notebook propagated posterior draws of both \(\mu\) and \(\sigma\) through discounted physical-measure simulations. Those outputs remain for traceability but are not interpreted as Black-Scholes no-arbitrage prices.

## Publication manuscript

`reporte/reporte.tex` contains the corrected publication-oriented manuscript, while `reporte/draft_v1.tex` is the first full literature-informed draft.

The manuscript includes the P/Q separation, transformed Metropolis-Hastings inference, risk-neutral Asian pricing with variance reduction, full-Bayes versus plug-in comparisons, repeated-sampling evaluation, reproducibility, limitations, and an AI-use disclosure.

The current 80-replication experiment remains preliminary. The large-scale synthetic framework below is intended to produce the final evidence.

## Conda-first environment

The research workstation may not provide administrator privileges. The supported workflow therefore uses a user-level Conda environment rather than system-wide Python/CUDA installations.

Create the base environment from the repository root:

```powershell
conda env create -f environment.yml
```

Activate it:

```powershell
conda activate asian-options
```

Or run commands without activating it:

```powershell
conda run -n asian-options python --version
```

The base `environment.yml` contains Python, NumPy, pandas, SciPy, Matplotlib, pytest, and psutil. GPU support is deliberately installed separately after inspecting the NVIDIA driver:

```powershell
conda run -n asian-options nvidia-smi
```

If the installed NVIDIA driver is compatible, install CuPy inside the same user-level Conda environment:

```powershell
conda install -n asian-options -c conda-forge cupy -y
```

No administrator privileges or system-wide CUDA toolkit installation are required by the project workflow; compatibility still depends on the NVIDIA driver provided by the workstation.

## Automatic workstation probe

`scripts/system_probe.py` records the machine used for an experiment. It is safe to run in restricted environments and continues even when `nvidia-smi`, CuPy, or psutil are unavailable.

Run it with:

```powershell
conda run -n asian-options python -m scripts.system_probe
```

It automatically writes both timestamped reports and rolling `latest` reports under:

```text
results/system/
```

Specifically:

```text
hardware_report_<timestamp>.json
hardware_report_<timestamp>.txt
hardware_report_latest.json
hardware_report_latest.txt
```

The report attempts to record:

- hostname, operating system, architecture, and platform;
- CPU model, physical cores, logical cores, and reported frequencies;
- total/available RAM;
- mounted disks, capacity, and free space;
- NVIDIA GPU model(s), dedicated VRAM, driver version, and CUDA version advertised by the driver;
- whether CuPy is installed and can actually access CUDA;
- CuPy CUDA runtime/driver versions and GPU compute capability when available;
- Python executable/version;
- Conda environment, prefix, and Conda version;
- NumPy, pandas, SciPy, Matplotlib, pytest, psutil, and CuPy versions;
- Git branch, commit SHA, and whether the working tree contains uncommitted changes.

The JSON is intended for machine-readable reproducibility manifests; the text report is intended for quick inspection.

## Reproducible code

- `src/bayesian_gbm.py`: physical-measure GBM likelihood, transformed M-H sampler, and MLE.
- `src/asian_pricing.py`: reference risk-neutral Asian-call Monte Carlo and geometric control variate.
- `src/accelerated_pricing.py`: bounded-memory NumPy/CuPy pricing backend for very large path counts.
- `src/synthetic_validation.py`: deterministic, stochastic, and theoretical validation utilities.
- `experiments/synthetic_validation.py`: reproducible validation suite with explicit seed scheme and manifest.
- `experiments/precompute_pricing_grids.py`: GPU-oriented pricing-grid precomputation with one atomic checkpoint per volatility point.
- `experiments/large_scale_synthetic.py`: CPU-parallel, resumable repeated-sampling study over sample size, true volatility, moneyness, and maturity.
- `experiments/publication_experiment.py`: earlier pilot repeated-sampling experiment.
- `scripts/system_probe.py`: automatic hardware/software/Conda/GPU reproducibility report.
- `environment.yml`: Conda-first base research environment.
- `requirements-publication.txt`: legacy/base dependency listing retained for reference.
- `requirements-gpu.txt`: optional pip-oriented legacy GPU listing; Conda is preferred on the research workstation.
- `tests/`: regression and theoretical tests.

## Synthetic/stochastic/theoretical validation

Quick smoke run:

```powershell
conda run -n asian-options python -m experiments.synthetic_validation --quick
```

Publication-oriented validation run:

```powershell
conda run -n asian-options python -m experiments.synthetic_validation
```

The suite writes raw/summary CSV files plus a `manifest.json` containing configuration, root seed, software versions, Git commit, and SHA-256 hashes. The default root seed is `20260909` and individual seeds are derived deterministically with NumPy `SeedSequence`.

## Large-scale workstation experiment

The project assumes that wall-clock runtime is **not a binding scientific constraint** on the available workstation. Statistical precision and robust restartability are prioritized over minimizing compute.

The visually confirmed machine has an **NVIDIA RTX 4500 Ada Generation**, approximately **64 GB RAM**, an **Intel UHD Graphics 770** iGPU, and an **NVMe SSD**. Exact CPU model and dedicated RTX VRAM were not visible in the supplied Task Manager capture; the automatic system probe records the actual machine rather than guessing these values. See [`research/COMPUTE.md`](research/COMPUTE.md).

The recommended division of work is:

- **GPU:** very large risk-neutral Monte Carlo pricing grids;
- **CPU multiprocess:** independent historical datasets and MCMC posterior fits;
- **disk checkpoints:** every inference replication and every pricing-grid volatility point.

### 1. Record the machine

```powershell
conda run -n asian-options python -m scripts.system_probe
```

### 2. Precompute pricing grids with point-level checkpoints

Research preset:

```powershell
conda run -n asian-options python -m experiments.precompute_pricing_grids --preset research --backend auto
```

Extreme GPU run:

```powershell
conda run -n asian-options python -m experiments.precompute_pricing_grids --preset extreme --backend cupy
```

Every `(moneyness, maturity, sigma-grid point)` is stored atomically. If the workstation disconnects, re-running the identical command skips completed points.

### 3. Run/resume CPU-parallel posterior experiments

Research preset:

```powershell
conda run -n asian-options python -m experiments.large_scale_synthetic --preset research --backend auto
```

Extreme preset:

```powershell
conda run -n asian-options python -m experiments.large_scale_synthetic --preset extreme --backend cupy
```

By default the experiment uses all but one logical CPU. Override explicitly if desired:

```powershell
conda run -n asian-options python -m experiments.large_scale_synthetic --preset extreme --backend cupy --workers 24
```

The run directory is keyed by a SHA-256 fingerprint of the full scientific configuration. Each `(n_obs, sigma_true, replication)` posterior is stored independently, including compressed posterior volatility draws. Restarting the same configuration resumes missing units rather than recomputing completed work.

### Experiment scales

`research` uses:

- \(n\in\{63,252,1260\}\) daily returns with fixed \(\Delta t=1/252\), corresponding to roughly 0.25, 1, and 5 historical years;
- \(\sigma_0\in\{0.15,0.25,0.40\}\);
- \(K/S_0\in\{0.80,1.00,1.20\}\);
- \(T\in\{0.5,1,2\}\);
- 1,000 posterior replications for each `(n, sigma_true)` pair = **9,000 posterior fits**;
- 12,000 MCMC iterations per fit;
- 121 volatility-grid points for each of 9 contract configurations;
- 500,000 risk-neutral paths per grid point.

`extreme` raises this to **18,000 posterior fits**, 20,000 MCMC iterations per fit, 161 pricing-grid points, and 2,000,000 paths per grid point.

Inference is deliberately computed only once for each historical-data scenario and then reused across all contract terms. This is both statistically correct and much more efficient than rerunning MCMC for every strike/maturity.

## Reproducibility and interruption safety

Long runs create:

- automatic workstation reports in `results/system/`;
- atomic inference checkpoints;
- atomic pricing-point checkpoints;
- completed pricing-grid checkpoints;
- `progress.json` / `pricing_progress.json`;
- configuration fingerprints;
- hardware/software manifests;
- final raw and summary CSV tables.

A disconnected session should therefore be handled by simply rerunning the same Conda command. Completed units remain on disk.

For a publication run, preserve the Conda environment specification as well:

```powershell
conda env export -n asian-options --no-builds > results/system/environment_export.yml
```

## Publication-oriented research question

> **How does Bayesian parameter uncertainty in the physical model propagate into risk-neutral prices of path-dependent options, and when does full posterior integration materially differ from plug-in pricing?**

The estimators are evaluated against known risk-neutral benchmarks across independently generated datasets, avoiding the original circular posterior-mean comparison.

See [`research/REFRAMING.md`](research/REFRAMING.md) for the methodological roadmap and [`research/COMPUTE.md`](research/COMPUTE.md) for the compute protocol.

## Repository map

- `notebook.ipynb`, `notebook.py`: legacy exploratory analysis.
- `reporte/reporte.tex`: corrected publication-oriented manuscript.
- `reporte/draft_v1.tex`: first full literature-informed draft.
- `literature/`: local literature corpus.
- `src/`: inference, reference pricing, accelerated pricing, and validation modules.
- `experiments/`: synthetic validation, point-checkpointed pricing, and repeated-sampling experiments.
- `scripts/`: reproducibility and workstation utilities.
- `results/`: generated results and checkpointed run directories.
- `tests/`: automated regression and theoretical tests.
- `environment.yml`: Conda-first research environment.
- `research/REFRAMING.md`: publication roadmap.
- `research/COMPUTE.md`: workstation specifications, compute policy, Conda workflow, presets, checkpointing, and recommended execution sequence.
