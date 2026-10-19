# REMEF publication figures and 10-million-history experiment

**Status (2026-10-19):** author executed the 10,000,000-history experiment
on an NVIDIA RTX 4500 Ada VM with CuPy and pushed the summary/report and
updated Figure 1 to PR #82. The scientific result and figure metadata have
been checked against the committed report; remaining figure 2–4 and final
Word-production steps are not yet complete.

## Source of the scientific numbers

The previous 175,000-history experiment remains preserved at
`results/analysis/massive_mechanism_map/200169bc7780a11d`.
The updated short-manuscript sources now cite the completed 10-million-history
run in `results/analysis/massive_mechanism_map/6e23d5aabc519982`
and point to the committed new Figure 1 under
`figures/publication/ten_million/`. All empirical results remain unchanged.
The 175k and 10m runs have different root seeds and sample sizes and are not
expected to have identical sample extremes.

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

## Verified ten-million result (2026-10-19)

| Item | Result |
| --- | --- |
| Completed simulations | 10,000,000 |
| Root seed | 2468 |
| Backend | cupy |
| Posterior sigma grid | 4,097 nodes |
| Contract-state scenarios | 168 |
| Scenario-cell summary rows | 5,880 |
| Maximum observed absolute PI–PM difference | 0.15653617444596035 |
| Largest within-cell 99th percentile | 0.12733794889857514 |
| Cell-level Taylor prediction / PI–PM correlation | 0.9995456741795187 |
| Completed run | `6e23d5aabc519982` |

Compared with the old 175k report, the maximum is larger
(0.13836448229415188 -> 0.15653617444596035) as expected for a much
larger simulation sample, while the 99th percentile changes little
(0.1270730579715583 -> 0.12733794889857514).
The older figure correlation was 0.9995451248988855, virtually identical
to the new 0.9995456741795187. This is stability of the **cell summary
relationship**, not an out-of-model validation theorem. The source comparison
uses the repository's versioned reports and manifests, not raw reruns.

The new Figure 1 is currently uploaded in
`figures/publication/ten_million/`; `figure_manifest.json` confirms the
Times New Roman font, width 6.1375 inches, and cividis_ink panel-D colormap.
The figure was visually reviewed for legend, annotations and contrast.
Figure 2 (outlined square/circle harmonization) and figures 3–4 still
require regeneration from their saved empirical summary tables before
the final Word build. Do not replace existing embedded DOCX figures
with previews on a different branch without reviewing the final documents.


## Native Times New Roman figure revision — 2026-10-19

The four plots use a consistent point hierarchy at 6.1375 inches:
suptitle 9, panel title 8, axes 7.3, major ticks 6.5, legends 6.5,
and panel labels 7.5. The CLI **requires actual Times New Roman**.
The preview-only --allow-font-fallback flag never produces submission-ready
artwork. SVG retains editable text and PDF uses embedded TrueType.
Axis endpoints expand to regular numeric ticks **without clipping data or
confidence intervals**; date, log, heatmap and categorical axes are treated
separately. External style packages are not necessary.

On the Windows VM, once this branch is merged into main, run:

    git switch main
    git pull --ff-only
    git sparse-checkout add results figures
    conda run --no-capture-output -n asian-options python -m pytest tests/test_publication_figures.py -q
    conda run --no-capture-output -n asian-options python -m scripts.build_publication_figures --figures 1 2 3 4 --formats pdf svg --mechanism-run results/analysis/massive_mechanism_map/6e23d5aabc519982 --output-dir figures/publication

Inspect the four PDFs and four SVGs and confirm font_mode =
times-new-roman in figures/publication/figure_manifest.json. Version only
those eight PDF/SVG files and that manifest; do not stage raw market data
or checkpoint archives. The REMEF Word builder must be run separately only
after final figures are available and reviewed.


## Final panel titles, categorical endpoints and all three figure formats (2026-10-19)

Panel letters are bold inline prefixes in their titles, rather than floating
separately outside the axes. Figure 3 previous-day red square markers use
#5c0010 dark-red edges. Figure 1 deliberately draws white-centered blue-edged
circles over the short-maturity blue line and over the bottom spine.

The numeric axes retain nice tick endpoints and do not crop numerical data or
confidence intervals. In Figure 3 expiry categories and Figure 4 target IDs,
blank boundary ticks at integer 0 and N+1 make each axis end at a real tick
and keep its lower-left corner connected. Category positions remain inside
those boundaries; the points and error bars are not cropped. Figure 1's
logarithmic sample axis keeps four representative observations and no minor
ticks. Heatmap cells are not truncated to their tick centers.

The plotter now produces PNG, PDF, and SVG by default. PNG is a convenient
proof image; PDF and SVG are manuscript-quality vector deliverables.
A submission run requires an installed Times New Roman. Verify that the
figure manifest reports font_mode times-new-roman, not a preview fallback.

After merging the PR into main, from Windows PowerShell in the repository:

    git switch main
    git pull --ff-only origin main
    git sparse-checkout add results figures
    conda run --no-capture-output -n asian-options python -m pytest tests/test_publication_figures.py -q
    conda run --no-capture-output -n asian-options python -m scripts.build_publication_figures --figures 1 2 3 4 --formats png pdf svg --mechanism-run results/analysis/massive_mechanism_map/6e23d5aabc519982 --output-dir figures/publication

Inspect all four PNGs, SVGs, PDFs and figure_manifest.json. Stage only the
12 final image files and the manifest (no proprietary data or checkpoints):

    $stem = @('fig01_mechanism_map', 'fig02_historical_vs_apo_implied_volatility', 'fig03_forward_q_cluster_bootstrap', 'fig04_numerical_identification')
    $paths = foreach ($name in $stem) { foreach ($ext in @('png', 'pdf', 'svg')) { "figures/publication/$name.$ext" } }
    $paths += 'figures/publication/figure_manifest.json'
    git add --sparse -- $paths
    git diff --cached --name-only
    git commit -m 'Regenerate final REMEF figures in PNG PDF SVG'
    git push origin main

These outputs use previously committed synthetic and empirical summaries.
No new Monte Carlo simulation or raw market-data download is required.
