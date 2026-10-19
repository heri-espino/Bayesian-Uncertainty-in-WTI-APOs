# REMEF publication figures and 10-million-history experiment

**Status:** source prepared; the 10,000,000-history run and its updated figures
have **not** been executed or accepted for publication yet.

## Source of the scientific numbers

The paper currently describes the previously completed 175,000-history
synthetic mechanism run. This change **does not replace or invalidate** those
recorded results. Do not change the paper's simulation count, correlation,
figure, or table until the new report and visualization have been generated
and inspected on the workstation.

## 10 million synthetic histories — seed 2468

From the private research repository (with its own Conda environment):

```powershell
git switch main
git pull --ff-only
git fetch origin
git switch paper/remef-figures-seed2468-10m-20261019

conda activate asian-options
python -m pytest tests/test_massive_mechanism_ten_million.py -q

# Optional: GPU backend needs a functional CuPy installation compatible with CUDA.
python -m experiments.massive_mechanism_map --preset ten-million --backend cupy
```

The 35 sample-size/true-volatility cells receive either 285,714 or 285,715
histories each (the first ten cells receive the extra history). The total is
**exactly 10,000,000**. The experiment uses an explicit root seed **2468**,
with derived deterministic batch seeds for restart consistency. It preserves
the monster sigma grid and original option-state design.

The 256-history batch avoids allocating the full 285k × 4097 posterior
matrix. Per-cell absolute-gap observations are temporarily held in a disk
memmap to compute **exact** median, 95th, and 99th percentiles; the temporary
file is removed after a cell completes. The final cell CSV/JSON checkpoint
is reused after interruption. Expect substantial computation time and
temporary disk usage; this is not a GitHub Actions push job.

The output directory is under `results/analysis/massive_mechanism_map/<fingerprint>/`.
The completed `mechanism_map_report.json` must report
`"synthetic_datasets": 10000000` and `"config": {"root_seed": 2468, ...}`.
Do **not** commit simulation checkpoints, licensed market data, or generated
results to GitHub automatically.

## Matching REMEF Word figures

The manuscript is US Letter, with **3 cm** left/right margins. The measured
available line width is **6.1375 inches**, using **Times New Roman** body text.
The four plot canvases now have that physical width; exported PDFs preserve
vector text and axes, with dense image artists rasterized when appropriate.
The Word figures should not be expanded or reduced after insertion.

The plotter uses neutral/default Matplotlib colors and layout choices rather
than the personalized Heri theme. It can additionally use the axis geometry
function from your own `heri-espino/Colors` project: specifically,
`contrastcolors.elegant.apply_elegant_axes`. This aligns numeric endpoint
ticks/spines; date, logarithmic and image panels keep their correct scaling.
Install the library locally:

```powershell
python -m pip install git+https://github.com/heri-espino/Colors.git
```

Generate all figures (includes private data-based figures 2–4) only when their
recorded inputs are locally present:

```powershell
python -m scripts.build_publication_figures --figures 1 2 3 4
```

To regenerate Figure 1 from the completed 10m experiment alone:

```powershell
python -m scripts.build_publication_figures --figures 1
```

The figure script discovers the largest completed monster/ten-million run.
Pass `--mechanism-run PATH` to select a particular run explicitly. The new
Figure 1 panel D has a darker truncated cividis scale so no bright-yellow
dots vanish on white. Figure 2 now uses **white-centred markers with coloured
edges for both circles and squares**.

**Font gate:** `figure_manifest.json` must report
`"font_mode": "times-new-roman"`. A machine lacking Times New Roman
uses a clearly labelled Liberation Serif fallback for a non-submission
preview; redo the final figure build on a machine with Times New Roman.

**Word gate:** Regenerate both Word files after new scientific results are
accepted. The document builder reads committed PNGs under
`figures/publication/`; generating a local image does not automatically
update the images already embedded inside DOCX. Open the final DOCX in Word
and inspect the equations, figure labels, colorbars and page breaks.

## Scientific provenance

Do not edit any original experiment outputs or vendor source data. For the
final figure report capture the run fingerprint, Git SHA, config, root seed,
number of histories, timestamp, figure manifest and SHA256 of resulting
figures. New derived results are distinct from Zenodo software v0.1.0;
that DOI refers to the original frozen source-only software archive.
