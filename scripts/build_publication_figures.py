"""Build the four main publication figures from committed experiment summaries.

The script is intentionally a pure post-processing layer: it does not rerun inference,
pricing, calibration, or bootstrap experiments.  Every plotted quantity is read from a
versioned CSV produced by the publication experiment suite.

Usage
-----
From the repository root::

    python -m scripts.build_publication_figures

Optionally choose another output directory or subset of figures::

    python -m scripts.build_publication_figures --output-dir figures/publication
    python -m scripts.build_publication_figures --figures 1 3

Outputs
-------
fig01_mechanism_map.{png,pdf,svg}
    When posterior integration matters and how the Taylor mechanism explains it.
fig02_historical_vs_apo_implied_volatility.{png,pdf,svg}
    Historical posterior volatility versus APO-implied effective volatility and
    representative strike smiles.
fig03_forward_q_cluster_bootstrap.{png,pdf,svg}
    Strict forward-in-time pricing improvement with valuation-date cluster intervals.
fig04_numerical_identification.{png,pdf,svg}
    Agreement of Curran, high-precision pseudo-MC, and randomized Sobol PI--PM gaps.
figure_manifest.json
    Source paths and plotting choices used for the build.

The REMEF figures use the Times New Roman font family and the physical content
width of the Word manuscript. The optional contrastcolors library supplies
endpoint-aligned axes. This script does not rerun scientific experiments.
"""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
from pathlib import Path
from typing import Iterable

import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.ticker import MaxNLocator, NullLocator, ScalarFormatter
from matplotlib.colors import LinearSegmentedColormap
import numpy as np
import pandas as pd

from scripts.vendor_utopia_fonts import (
    archives_available,
    diagnostic_report,
    ensure_tex_toolchain_on_path,
    prepare_vendored_texmf,
)


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT_DIR = ROOT / "figures" / "publication"

MECHANISM_ROOT = ROOT / "results" / "analysis" / "massive_mechanism_map"
IV_DIR = ROOT / "results" / "analysis" / "wti_apo_implied_volatility"
BOOTSTRAP_PATH = (
    ROOT
    / "results"
    / "analysis"
    / "wti_extended_forward"
    / "liquidity_bootstrap"
    / "liquidity_cluster_bootstrap_monster.csv"
)
HIGH_PRECISION_PATH = (
    ROOT
    / "results"
    / "analysis"
    / "wti_high_precision_pricing"
    / "high_precision_summary_monster.csv"
)
QMC_PATH = (
    ROOT
    / "results"
    / "analysis"
    / "wti_randomized_qmc"
    / "qmc_summary_monster.csv"
)

# These two dates deliberately show an early and a late October cross-section.
SMILE_DATES = (pd.Timestamp("2026-08-26"), pd.Timestamp("2026-09-10"))
MECHANISM_N = 21
MECHANISM_SIGMA = 0.80
MECHANISM_MONEYNESS = 1.50
MECHANISM_HEATMAP_MATURITY_DAYS = 126

# Final publication palette. Color is always redundant with marker shape,
# line pattern, or marker fill so the figures remain interpretable in grayscale.
FIG1_DISCRETE = [
    "#97001c",
    "#0083f9",
    "#00b49c",
    "#9b6500",  # dark ochre, readable on white
    "#f198ff",
]

IRIDESCENT_HEX = [
    "#FEFBE9", "#FCF7D5", "#F5F3C1", "#EAF0B5", "#DDECBF", "#D0E7CA",
    "#C2E3D2", "#B5DDD8", "#A8D8DC", "#9BD2E1", "#8DCBE4", "#81C4E7",
    "#7BBCE7", "#7EB2E4", "#88A5DD", "#9398D2", "#9B8AC4", "#9D7DB2",
    "#9A709E", "#906388", "#805770", "#684957", "#46353A",
]
BAD_DATA_COLOR = "#999999"
HEATMAP_CMAP = LinearSegmentedColormap.from_list(
    "tol_iridescent",
    IRIDESCENT_HEX,
    N=256,
)
HEATMAP_CMAP.set_bad(BAD_DATA_COLOR)
# Avoid pale yellow near-white bins in the second-order mechanism panel.
# A restricted cividis range remains perceptually ordered and print readable.
MECHANISM_CMAP = LinearSegmentedColormap.from_list(
    "cividis_ink",
    mpl.colormaps["cividis"](np.linspace(0.08, 0.82, 256)),
)

NEUTRAL = {
    "black": "#111111",
    "dark": "#3A3A3A",
    "mid": "#777777",
    "light": "#B0B0B0",
    "grid": "#D8D8D8",
}

FIG2_COLORS = {
    "calls": "#0083f9",
    "puts": "#97001c",
    "historical": "#00b49c",
    "apo_common": "#f198ff",
}

FIG3_COLORS = {
    "expanding": "#a5d3ff",
    "previous_day": "#97001c",
    "previous_day_edge": "#5c0010",
    "zero_line": "#555555",
}

FIG4_COLORS = {
    "pseudo_mc": "#9b6500",
    "curran": "#0083f9",
    "sobol": "#97001c",
}

# Darker outlines preserve marker shape against colored lines and white paper.
FIG4_EDGE_COLORS = {
    "pseudo_mc": "#5f3d00",
    "curran": "#005aa8",
    "sobol": "#5c0010",
}

SIGMA_STYLES = {
    0.10: {"color": FIG1_DISCRETE[0], "linestyle": "-", "marker": "o", "filled": False},
    0.20: {"color": FIG1_DISCRETE[1], "linestyle": (0, (5, 2)), "marker": "s", "filled": False},
    0.35: {"color": FIG1_DISCRETE[2], "linestyle": (0, (1, 1)), "marker": "^", "filled": True},
    0.50: {"color": FIG1_DISCRETE[3], "linestyle": (0, (3, 1, 1, 1)), "marker": "D", "filled": False},
    0.80: {"color": FIG1_DISCRETE[4], "linestyle": (0, (7, 2, 1, 2)), "marker": "v", "filled": True},
}

MATURITY_STYLES = {
    21: {"color": FIG1_DISCRETE[1], "linestyle": "-", "marker": "o", "filled": False},
    63: {"color": FIG1_DISCRETE[2], "linestyle": (0, (5, 2)), "marker": "s", "filled": True},
    126: {"color": FIG1_DISCRETE[3], "linestyle": (0, (1, 1)), "marker": "^", "filled": False},
    252: {"color": FIG1_DISCRETE[0], "linestyle": (0, (3, 1, 1, 1)), "marker": "D", "filled": True},
}

def _kpsewhich(filename: str) -> bool:
    ensure_tex_toolchain_on_path()
    executable = shutil.which("kpsewhich")
    if executable is None:
        return False
    proc = subprocess.run(
        [executable, filename],
        capture_output=True,
        text=True,
        check=False,
    )
    return proc.returncode == 0 and bool(proc.stdout.strip())


def _wiley_utopia_mode() -> str | None:
    """Prefer the fully repo-vendored Wiley Utopia stack, then system TeX."""
    tools = ensure_tex_toolchain_on_path()
    if tools.get("latex") is None:
        return None

    if archives_available():
        try:
            prepare_vendored_texmf()
        except Exception:
            # A broken local cache must not prevent a system TeX fallback.
            pass
        else:
            if _kpsewhich("utopia.sty") and _kpsewhich("mathastext.sty"):
                return "wiley-utopia-vendored"

    if _kpsewhich("utopia.sty") and _kpsewhich("mathastext.sty"):
        return "wiley-utopia-system"
    return None



# REMEF Word (US Letter; 3 cm side margins), measured from the final DOCX.
WORD_TEXT_WIDTH_IN = 6.1375
JFM_TWO_COLUMN_WIDTH_IN = 7.0  # provisional proof width; verify against compiled Wiley template
CURRENT_FIGURE_WIDTH_IN = WORD_TEXT_WIDTH_IN
CURRENT_JOURNAL = "remef"
CURRENT_JFM_PAPER = None  # Only active in an AwesomeFigures Wiley session
FIGURE_ASPECT_RATIOS = {1: 5.8 / 7.25, 2: 5.8 / 7.25, 3: 3.7 / 7.2, 4: 4.9 / 7.2}


def _word_figsize(number: int) -> tuple[float, float]:
    return CURRENT_FIGURE_WIDTH_IN, CURRENT_FIGURE_WIDTH_IN * FIGURE_ASPECT_RATIOS[number]



# Typographic hierarchy in points at the real 6.1375-inch Word width.
PUBLICATION_FONT_PT = {
    "suptitle": 9.0,
    "panel_title": 8.0,
    "axis_label": 7.3,
    "tick": 6.5,
    "legend": 6.5,
    "panel_letter": 7.5,
}


def _configure_matplotlib(
    *, force_no_tex: bool = False, require_times_new_roman: bool = False,
) -> str:
    """Use Times New Roman, no external LaTeX, and retain native SVG text.

    Publication CLI builds require the font on the machine; portable unit
    tests and explicit non-submission previews may use a visible fallback.
    """
    import warnings
    from matplotlib import font_manager

    plt.style.use("default")
    try:
        font_manager.findfont(
            font_manager.FontProperties(family="Times New Roman"),
            fallback_to_default=False,
        )
        family, mode = "Times New Roman", "times-new-roman"
    except ValueError as exc:
        if require_times_new_roman:
            raise SystemExit(
                "Times New Roman is not installed or visible to Matplotlib. "
                "Install it and refresh the font cache, then rerun. "
                "Use --allow-font-fallback only for a NON-SUBMISSION preview."
            ) from exc
        family, mode = "Liberation Serif", "preview-font-fallback"
        warnings.warn(
            "Preview only: Times New Roman unavailable; using Liberation Serif. "
            "Do not submit these figures.", RuntimeWarning, stacklevel=2,
        )
    rc = {
        "text.usetex": False,
        "font.family": [family],
        "font.serif": [family],
        "font.size": PUBLICATION_FONT_PT["axis_label"],
        "figure.titlesize": PUBLICATION_FONT_PT["suptitle"],
        "axes.titlesize": PUBLICATION_FONT_PT["panel_title"],
        "axes.labelsize": PUBLICATION_FONT_PT["axis_label"],
        "legend.fontsize": PUBLICATION_FONT_PT["legend"],
        "xtick.labelsize": PUBLICATION_FONT_PT["tick"],
        "ytick.labelsize": PUBLICATION_FONT_PT["tick"],
        "mathtext.fontset": "custom",
        "mathtext.rm": family,
        "mathtext.it": family + ":italic",
        "mathtext.bf": family + ":bold",
        "mathtext.fallback": "stix",
        "axes.unicode_minus": False,
        "svg.fonttype": "none",
        "pdf.fonttype": 42,
        "ps.fonttype": 42,
        "figure.dpi": 180,
        "savefig.dpi": 600,
        "savefig.bbox": None,
        "savefig.pad_inches": 0,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.linewidth": 0.8,
        "axes.edgecolor": NEUTRAL["dark"],
        "axes.facecolor": "white",
        "axes.axisbelow": True,
        "axes.grid": True,
        "grid.color": NEUTRAL["grid"],
        "grid.linewidth": 0.45,
        "grid.alpha": 0.35,
        "xtick.direction": "out",
        "ytick.direction": "out",
        "xtick.major.size": 2.5,
        "ytick.major.size": 2.5,
        "lines.linewidth": 1.15,
        "lines.markersize": 4.0,
        "legend.frameon": False,
    }
    mpl.rcParams.update(rc)
    return mode


def _snap_numeric_axis_to_ticks(ax: plt.Axes, axis: str, *, bins: int = 4) -> None:
    """Expand a numeric axis to regular outer ticks; never crop data or errors."""
    dim = ax.xaxis if axis == "x" else ax.yaxis
    if (ax.get_xscale() if axis == "x" else ax.get_yscale()) != "linear":
        return
    lo0, hi0 = ax.get_xlim() if axis == "x" else ax.get_ylim()
    if not (np.isfinite(lo0) and np.isfinite(hi0)) or np.isclose(lo0, hi0):
        return
    inverted = lo0 > hi0
    lo, hi = sorted((float(lo0), float(hi0)))
    locator = MaxNLocator(nbins=bins, min_n_ticks=3, steps=[1, 2, 2.5, 5, 10])
    ticks = np.asarray(locator.tick_values(lo, hi), dtype=float)
    ticks = ticks[np.isfinite(ticks)]
    if len(ticks) > 6:
        locator = MaxNLocator(nbins=3, min_n_ticks=3, steps=[1, 2, 2.5, 5, 10])
        ticks = np.asarray(locator.tick_values(lo, hi), dtype=float)
    if len(ticks) < 2:
        return
    # MaxNLocator does not guarantee strict inclusion on every Matplotlib
    # version/scale (notably with the small, negative CI differences plotted
    # by Figure 3). Rather than raising or cropping the original error bars,
    # extend its existing regular grid by as many whole steps as necessary.
    step = float(np.median(np.diff(ticks)))
    if not np.isfinite(step) or step <= 0:
        return
    if ticks[0] > lo:
        nleft = int(np.ceil((float(ticks[0]) - lo) / step))
        ticks = np.r_[ticks[0] - step * np.arange(nleft, 0, -1), ticks]
    if ticks[-1] < hi:
        nright = int(np.ceil((hi - float(ticks[-1])) / step))
        ticks = np.r_[ticks, ticks[-1] + step * np.arange(1, nright + 1)]
    # Round-off near a tick boundary must also never crop any original data.
    lower = min(lo, float(ticks[0]))
    upper = max(hi, float(ticks[-1]))
    if axis == "x":
        ax.set_xticks(ticks)
        ax.set_xlim(upper, lower) if inverted else ax.set_xlim(lower, upper)
    else:
        ax.set_yticks(ticks)
        ax.set_ylim(upper, lower) if inverted else ax.set_ylim(lower, upper)
    dim.set_minor_locator(NullLocator())


def _align_numeric_axes(
    fig: plt.Figure,
    *,
    date_axes: tuple[plt.Axes, ...] = (),
    categorical_x_axes: tuple[plt.Axes, ...] = (),
    categorical_y_axes: tuple[plt.Axes, ...] = (),
) -> None:
    """Clean spines and few ticks; skip dates, categories, log axes and images."""
    for ax in fig.axes:
        if getattr(ax, "_colorbar", None) is not None:
            ax.tick_params(labelsize=PUBLICATION_FONT_PT["tick"])
            continue
        ax.tick_params(
            axis="both", which="major",
            labelsize=PUBLICATION_FONT_PT["tick"], length=2.5, width=0.8,
        )
        ax.tick_params(axis="both", which="minor", length=0)
        for side in ("top", "right"):
            ax.spines[side].set_visible(False)
        for side in ("left", "bottom"):
            ax.spines[side].set_linewidth(0.8)
        if ax.images:
            continue  # Heatmaps need visible outer cell boundaries.
        if ax not in date_axes and ax not in categorical_x_axes:
            _snap_numeric_axis_to_ticks(ax, "x")
        if ax not in categorical_y_axes:
            _snap_numeric_axis_to_ticks(ax, "y")


def _category_ticks_with_endpoints(ax: plt.Axes, axis: str, labels: list[str]) -> None:
    """Put unlabeled boundary ticks at integer endpoints of category axes.

    Actual category centers are 1..N; endpoints are 0 and N+1. This keeps
    shifted marker/errorbar groups fully visible while giving both spines
    a visible terminal tick and a clean shared lower-left corner.
    """
    positions = np.arange(len(labels) + 2, dtype=float)
    printed = ["", *labels, ""]
    if axis == "x":
        ax.set_xticks(positions)
        ax.set_xticklabels(printed, rotation=35, ha="right")
        ax.set_xlim(positions[0], positions[-1])
    elif axis == "y":
        ax.set_yticks(positions)
        ax.set_yticklabels(printed)
        ax.set_ylim(positions[-1], positions[0])
    else:
        raise ValueError("axis must be x or y")


def _apply_suptitle(fig: plt.Figure, text: str) -> None:
    """Apply one compact, in-canvas title and reserve a consistent top margin."""
    fig.suptitle(text, y=0.985, fontsize=PUBLICATION_FONT_PT["suptitle"])
    fig.tight_layout(rect=(0, 0, 1, 0.94))


def _portable_path(path: Path) -> str:
    """Return a repo-relative path when possible, otherwise an absolute path."""
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def _save(fig: plt.Figure, stem: Path, formats: Iterable[str]) -> list[str]:
    """Preserve REMEF's original export; JFM uses exact Wiley XeLaTeX/PGF."""
    outputs: list[str] = []
    stem.parent.mkdir(parents=True, exist_ok=True)
    metadata = {
        "Title": stem.stem,
        "Subject": "Posterior integration in WTI average price options",
    }
    try:
        for fmt in formats:
            path = stem.with_suffix(f".{fmt}")
            if CURRENT_JOURNAL == "jfm":
                if CURRENT_JFM_PAPER is None:
                    raise RuntimeError("JFM requires an active AwesomeFigures publication session")
                # Exact-font PDF: AwesomeFigures typesets PGF with the same Wiley
                # preamble as the article; SVG/PNG are explicitly only previews.
                CURRENT_JFM_PAPER.savefig(
                    fig, path, width="text", dpi=600, exact=(fmt == "pdf"),
                )
            else:
                fig.savefig(
                    path,
                    dpi=600,
                    bbox_inches=None,
                    pad_inches=0,
                    metadata=metadata if fmt == "pdf" else None,
                )
            outputs.append(_portable_path(path))
    finally:
        plt.close(fig)
    return outputs

def _discover_monster_mechanism_run(explicit: Path | None) -> Path:
    if explicit is not None:
        run_dir = explicit if explicit.is_absolute() else ROOT / explicit
        if not (run_dir / "mechanism_map_summary.csv").exists():
            raise FileNotFoundError(
                f"Mechanism run does not contain mechanism_map_summary.csv: {run_dir}"
            )
        return run_dir

    candidates: list[tuple[int, str, Path]] = []
    for report_path in MECHANISM_ROOT.glob("*/mechanism_map_report.json"):
        report = json.loads(report_path.read_text(encoding="utf-8"))
        if report.get("preset") not in {"monster", "ten-million"}:
            continue
        run_dir = report_path.parent
        if not (run_dir / "mechanism_map_summary.csv").exists():
            continue
        candidates.append(
            (
                int(report.get("synthetic_datasets", 0)),
                str(report.get("completed_at_utc", "")),
                run_dir,
            )
        )
    if not candidates:
        raise FileNotFoundError(
            "No completed monster mechanism-map run found under "
            f"{MECHANISM_ROOT.relative_to(ROOT)}"
        )
    candidates.sort()
    return candidates[-1][2]


def _panel_title(ax: plt.Axes, label: str, title: str) -> None:
    """Inline bold panel label followed by a normal-weight panel title."""
    ax.set_title(
        rf"$\mathbf{{({label})}}$  {title}",
        loc="left",
        pad=4,
        fontsize=PUBLICATION_FONT_PT["panel_title"],
        fontweight="normal",
        color=NEUTRAL["black"],
    )


def _add_partial_fixing_zoom(
    ax: plt.Axes, curve: pd.DataFrame,
) -> plt.Axes:
    """Show the near-zero PI--PM differences without changing the main axes.

    The inset occupies the bottom-right of panel C, below the existing legend.
    Plot it only after the main tight layout and numeric-axis alignment, so
    global tick formatting cannot override the zoom's deliberately small
    x/y ranges. The zoom window is explicitly outlined in the main panel.
    """
    zoom = ax.inset_axes((0.55, 0.10, 0.42, 0.41), zorder=9)
    for maturity, group in curve.groupby("maturity_days", sort=True):
        group = group.sort_values("fraction_fixed")
        style = MATURITY_STYLES.get(
            int(maturity),
            {"color": NEUTRAL["dark"], "linestyle": "-", "marker": "o", "filled": False},
        )
        zoom.plot(
            group["fraction_fixed"],
            group["mean_abs_pi_minus_pm"],
            marker=style["marker"],
            linestyle=style["linestyle"],
            color=style["color"],
            markerfacecolor=style["color"] if style["filled"] else "white",
            markeredgecolor=style["color"],
            markeredgewidth=0.9,
            markersize=3.6,
            linewidth=1.0,
            zorder=4,
        )
    zoom.set_xlim(0.75, 1.00)
    zoom.set_ylim(-0.001, 0.023)
    zoom.set_xticks((0.75, 0.875, 1.00))
    zoom.set_yticks((0.00, 0.01, 0.02))
    zoom.tick_params(
        axis="both", which="major",
        labelsize=PUBLICATION_FONT_PT["tick"] - 0.6,
        length=2.0, width=0.65, pad=1.0,
    )
    zoom.minorticks_off()
    zoom.grid(True, color=NEUTRAL["grid"], linewidth=0.35, alpha=0.45)
    zoom.set_facecolor("white")
    for side in ("top", "right"):
        zoom.spines[side].set_visible(False)
    for side in ("bottom", "left"):
        zoom.spines[side].set_color(NEUTRAL["dark"])
        zoom.spines[side].set_linewidth(0.65)
    zoom.set_title("Near-zero detail", fontsize=PUBLICATION_FONT_PT["tick"], pad=2)

    # Outlined rectangle and subdued connectors show which original domain
    # is magnified; no error bars or observations are removed from panel C.
    ax.indicate_inset_zoom(zoom, edgecolor=NEUTRAL["mid"], alpha=0.65)
    return zoom


def _closest_rows(
    frame: pd.DataFrame,
    *,
    n_obs: int,
    sigma_true: float,
) -> pd.DataFrame:
    out = frame.loc[frame["n_obs"].eq(n_obs)].copy()
    if out.empty:
        raise ValueError(f"No mechanism rows with n_obs={n_obs}")
    sigma_values = np.sort(out["sigma_true"].unique())
    chosen_sigma = float(sigma_values[np.argmin(np.abs(sigma_values - sigma_true))])
    return out.loc[np.isclose(out["sigma_true"], chosen_sigma)].copy()


def build_figure_1(
    mechanism_run: Path,
    output_dir: Path,
    formats: Iterable[str],
) -> tuple[list[str], dict[str, object]]:
    summary = pd.read_csv(mechanism_run / "mechanism_map_summary.csv")
    posterior = pd.read_csv(mechanism_run / "posterior_cell_summary.csv")

    fig, axes = plt.subplots(2, 2, figsize=_word_figsize(1))
    ax_a, ax_b, ax_c, ax_d = axes.flat

    # A. Posterior dispersion shrinks with information.
    for sigma_true, group in posterior.groupby("sigma_true", sort=True):
        group = group.sort_values("n_obs")
        sigma_key = round(float(sigma_true), 2)
        style = SIGMA_STYLES.get(
            sigma_key,
            {"color": NEUTRAL["dark"], "linestyle": "-", "marker": "o", "filled": False},
        )
        marker_face = style["color"] if style["filled"] else "white"
        ax_a.plot(
            group["n_obs"],
            group["posterior_sigma_sd_mean"],
            marker=style["marker"],
            linestyle=style["linestyle"],
            color=style["color"],
            markerfacecolor=marker_face,
            markeredgecolor=style["color"],
            markeredgewidth=0.85,
            label=fr"$\sigma_0={sigma_true:.2f}$",
        )
    ax_a.set_xscale("log")
    ax_a.set_xticks([21, 63, 252, 1260])
    ax_a.set_xticklabels(["21", "63", "252", "1260"])
    ax_a.xaxis.set_major_formatter(ScalarFormatter())
    ax_a.xaxis.set_minor_locator(NullLocator())
    ax_a.set_xlim(21, 1260)
    for line in ax_a.lines:
        line.set_clip_on(False)
    ax_a.set_xlabel("Historical observations $n$")
    ax_a.set_ylabel(r"Mean posterior SD of $\sigma$")
    _panel_title(ax_a, "A", "Posterior dispersion")
    ax_a.legend(ncol=2, frameon=False)

    adverse = _closest_rows(summary, n_obs=MECHANISM_N, sigma_true=MECHANISM_SIGMA)

    # B. Heatmap: moneyness x fraction fixed for one adverse maturity.
    heat = adverse.loc[
        adverse["maturity_days"].eq(MECHANISM_HEATMAP_MATURITY_DAYS)
    ].pivot_table(
        index="fraction_fixed",
        columns="moneyness",
        values="mean_abs_pi_minus_pm",
        aggfunc="mean",
    )
    heat = heat.sort_index().sort_index(axis=1)
    image = ax_b.imshow(
        heat.to_numpy(),
        origin="lower",
        aspect="auto",
        interpolation="nearest",
        cmap=HEATMAP_CMAP,
        rasterized=True,
    )
    ax_b.grid(False)
    # Show the complete simulated design grid (not sampled tick labels).
    # Small type and vertical labels avoid overlaps at Word column width.
    ax_b.set_xticks(np.arange(len(heat.columns)))
    ax_b.set_xticklabels(
        [f"{value:.2f}" for value in heat.columns],
        rotation=(40 if CURRENT_JOURNAL == "jfm" else 65), ha="right",
        fontsize=PUBLICATION_FONT_PT["tick"] - (0.3 if CURRENT_JOURNAL == "jfm" else 0.6),
    )
    ax_b.set_yticks(np.arange(len(heat.index)))
    ax_b.set_yticklabels(
        [f"{value:.3g}" for value in heat.index],
        fontsize=PUBLICATION_FONT_PT["tick"] - 0.6,
    )
    ax_b.set_xlabel(r"Moneyness $K/F$")
    ax_b.set_ylabel("Fraction already fixed")
    _panel_title(ax_b, "B", r"Mean $|PI-PM|$ by option state")
    cbar = fig.colorbar(image, ax=ax_b, fraction=0.047, pad=0.04)
    cbar.set_label(r"Mean $|PI-PM|$")

    # C. Partial fixing for extreme moneyness, separated by maturity.
    curve = adverse.loc[
        np.isclose(adverse["moneyness"], MECHANISM_MONEYNESS)
    ].copy()
    for maturity, group in curve.groupby("maturity_days", sort=True):
        group = group.sort_values("fraction_fixed")
        style = MATURITY_STYLES.get(
            int(maturity),
            {"color": NEUTRAL["dark"], "linestyle": "-", "marker": "o", "filled": False},
        )
        marker_face = style["color"] if style["filled"] else "white"
        ax_c.plot(
            group["fraction_fixed"],
            group["mean_abs_pi_minus_pm"],
            marker=style["marker"],
            linestyle=style["linestyle"],
            color=style["color"],
            markerfacecolor=marker_face,
            markeredgecolor=style["color"],
            markeredgewidth=1.0,
            markersize=5.5,
            zorder=4,
            clip_on=False,
            label=f"{int(maturity)} days",
        )
    # Re-mark the short-maturity blue curve over the other lines and the
    # bottom spine. Its small positive gaps previously hid hollow circles.
    short_maturity = curve.loc[curve["maturity_days"].eq(21)]
    if not short_maturity.empty:
        ax_c.scatter(
            short_maturity["fraction_fixed"],
            short_maturity["mean_abs_pi_minus_pm"],
            marker="o",
            s=36,
            facecolors="white",
            edgecolors=FIG1_DISCRETE[1],
            linewidths=1.25,
            zorder=8,
            clip_on=False,
        )
    ax_c.set_xlabel("Fraction already fixed")
    ax_c.set_ylabel(r"Mean $|PI-PM|$")
    _panel_title(ax_c, "C", "Partial fixing by maturity")
    ax_c.legend(frameon=False)

    # D. Taylor mechanism across every synthetic cell.
    x = summary["mean_taylor_gap"].to_numpy(dtype=float)
    y = summary["mean_pi_minus_pm"].to_numpy(dtype=float)
    finite = np.isfinite(x) & np.isfinite(y)
    hb = ax_d.hexbin(
        x[finite],
        y[finite],
        gridsize=42,
        mincnt=1,
        cmap=MECHANISM_CMAP,
        linewidths=0.0,
        rasterized=True,
    )
    corr = float(np.corrcoef(x[finite], y[finite])[0, 1])
    ax_d.set_xlabel(
        r"Taylor prediction $\frac{1}{2}C^{Q\prime\prime}(\bar\sigma)"
        r"\mathrm{Var}(\sigma\mid D)$"
    )
    ax_d.set_ylabel(r"Actual mean $PI-PM$")
    _panel_title(ax_d, "D", fr"Second-order mechanism ($r={corr:.4f}$)")
    cbar2 = fig.colorbar(hb, ax=ax_d, fraction=0.047, pad=0.04)
    cbar2.set_label("Cell count")

    _apply_suptitle(fig, "When posterior integration matters")
    _align_numeric_axes(fig)

    # Explicit publication zoom ranges: apply AFTER automatic tick alignment.
    # Ticks end exactly on the requested bounds.
    ax_a.set_yticks((0.00, 0.05, 0.10, 0.15))
    ax_a.set_ylim(0.0, 0.15)
    # A realized-fixing fraction is defined on [0, 1]; do not show the
    # misleading legacy 1.5/2.0/2.5 ticks in panel C.
    ax_c.set_xticks((0.0, 0.25, 0.5, 0.75, 1.0))
    ax_c.set_yticks((0.00, 0.05, 0.10, 0.15))
    ax_c.set_xlim(0.0, 1.0)
    ax_c.set_ylim(0.0, 0.15)

    # The identity line must extend from corner to corner, not stop at the
    # observed minimum/maximum. Shared x/y limits preserve unit slope.
    xy_min = float(min(x[finite].min(), y[finite].min()))
    xy_max = float(max(x[finite].max(), y[finite].max()))
    pad = 0.04 * max(xy_max - xy_min, 1e-8)
    d_locator = MaxNLocator(nbins=4, min_n_ticks=3, steps=[1, 2, 2.5, 5, 10])
    d_ticks = d_locator.tick_values(xy_min - pad, xy_max + pad)
    ax_d.set_xticks(d_ticks)
    ax_d.set_yticks(d_ticks)
    ax_d.set_xlim(float(d_ticks[0]), float(d_ticks[-1]))
    ax_d.set_ylim(float(d_ticks[0]), float(d_ticks[-1]))
    ax_d.axline(
        (0.0, 0.0), slope=1.0,
        linestyle="--", linewidth=1.0, color=NEUTRAL["black"],
        zorder=5,
    )
    # The two-column Wiley page makes the tiny near-zero inset cover Panel C
    # labels and curves. Keep the historical REMEF figure unchanged; omit the
    # inset only in JFM, retaining every data point in the main axes.
    if CURRENT_JOURNAL != "jfm":
        _add_partial_fixing_zoom(ax_c, curve)
    outputs = _save(fig, output_dir / "fig01_mechanism_map", formats)
    metadata = {
        "mechanism_run": str(mechanism_run.relative_to(ROOT)),
        "heatmap_state": {
            "n_obs": MECHANISM_N,
            "sigma_true": MECHANISM_SIGMA,
            "maturity_days": MECHANISM_HEATMAP_MATURITY_DAYS,
        },
        "partial_fixing_state": {
            "n_obs": MECHANISM_N,
            "sigma_true": MECHANISM_SIGMA,
            "moneyness": MECHANISM_MONEYNESS,
        },
        "taylor_cell_correlation": corr,
    }
    return outputs, metadata


def _plot_sigma_timeseries(ax: plt.Axes, by_date: pd.DataFrame, expiry: str) -> None:
    group = by_date.loc[by_date["apo_expiry"].eq(expiry)].sort_values("valuation_date")
    if group.empty:
        raise ValueError(f"No implied-volatility date rows for expiry {expiry}")
    ax.plot(
        group["valuation_date"],
        group["sigma_p_posterior_mean"],
        marker="o",
        linestyle="-",
        color=FIG2_COLORS["historical"],
        markerfacecolor="white",
        markeredgecolor=FIG2_COLORS["historical"],
        markeredgewidth=0.9,
        label=r"Historical posterior mean $\sigma_P$",
    )
    ax.plot(
        group["valuation_date"],
        group["full_sample_sigma_q"],
        marker="s",
        linestyle="--",
        color=FIG2_COLORS["apo_common"],
        markerfacecolor="white",
        markeredgecolor=FIG2_COLORS["apo_common"],
        markeredgewidth=0.9,
        label=r"APO-implied common $\sigma_Q$",
    )
    dates = pd.to_datetime(group["valuation_date"]).drop_duplicates().sort_values()
    if len(dates) > 1:
        ids = np.unique(np.linspace(0, len(dates) - 1, min(5, len(dates))).round().astype(int))
        ax.set_xticks(dates.iloc[ids].tolist())
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%m-%d"))
        ax.xaxis.set_minor_locator(NullLocator())
        ax.set_xlim(dates.iloc[0], dates.iloc[-1])
        for line in ax.lines:
            line.set_clip_on(False)
    ax.set_ylabel("Annualized volatility")
    ax.tick_params(axis="x", rotation=20)
    ax.legend(frameon=False)


def _plot_smile(
    ax: plt.Axes,
    contracts: pd.DataFrame,
    by_date: pd.DataFrame,
    date: pd.Timestamp,
) -> dict[str, float]:
    day = contracts.loc[contracts["valuation_date"].eq(date)].copy()
    if day.empty:
        raise ValueError(f"No contract-level implied volatilities for {date.date()}")
    styles = {
        "call": ("o", FIG2_COLORS["calls"], "Calls", "white"),
        "put": (
            "s",
            FIG2_COLORS["puts"],
            "Puts",
            "white",
        ),
    }
    for option_type, (marker, color, label, facecolor) in styles.items():
        group = day.loc[day["option_type"].eq(option_type)].sort_values("log_moneyness")
        if group.empty:
            continue
        ax.scatter(
            group["log_moneyness"],
            group["apo_implied_sigma_q"],
            marker=marker,
            s=24,
            alpha=1.0,
            facecolors=facecolor,
            edgecolors=color,
            linewidth=0.9,
            label=label,
            rasterized=True,
        )

    date_summary = by_date.loc[by_date["valuation_date"].eq(date)]
    if date_summary.empty:
        raise ValueError(f"No date-level implied-volatility row for {date.date()}")
    sigma_p = float(date_summary.iloc[0]["sigma_p_posterior_mean"])
    sigma_q = float(date_summary.iloc[0]["full_sample_sigma_q"])
    ax.axhline(
        sigma_p,
        linestyle="-",
        linewidth=1.25,
        color=FIG2_COLORS["historical"],
        label=r"Historical $\sigma_P$",
    )
    ax.axhline(
        sigma_q,
        linestyle="--",
        linewidth=1.25,
        color=FIG2_COLORS["apo_common"],
        label=r"Common APO $\sigma_Q$",
    )
    ax.set_xlabel(r"Log moneyness $\log(K/\widehat A^Q)$")
    ax.set_ylabel("APO-implied volatility")
    ax.legend(frameon=False, ncol=2)
    return {"sigma_p": sigma_p, "sigma_q": sigma_q, "contracts": int(len(day))}


def build_figure_2(
    output_dir: Path,
    formats: Iterable[str],
) -> tuple[list[str], dict[str, object]]:
    by_date = pd.read_csv(IV_DIR / "apo_implied_volatility_by_date.csv")
    contracts = pd.read_csv(IV_DIR / "apo_contract_implied_volatility.csv")
    by_date["valuation_date"] = pd.to_datetime(by_date["valuation_date"])
    contracts["valuation_date"] = pd.to_datetime(contracts["valuation_date"])

    fig, axes = plt.subplots(2, 2, figsize=_word_figsize(2))
    _plot_sigma_timeseries(axes[0, 0], by_date, "2026-09")
    _panel_title(axes[0, 0], "A", "2026-09 expiry")
    _plot_sigma_timeseries(axes[0, 1], by_date, "2026-10")
    _panel_title(axes[0, 1], "B", "2026-10 expiry")

    smile_meta: dict[str, object] = {}
    for ax, date, label in zip(axes[1], SMILE_DATES, ("C", "D"), strict=True):
        smile_meta[str(date.date())] = _plot_smile(ax, contracts, by_date, date)
        _panel_title(ax, label, str(date.date()))

    _apply_suptitle(fig, "Historical and APO-implied effective volatility")
    _align_numeric_axes(fig, date_axes=(axes[0, 0], axes[0, 1]))

    # Preserve the explicitly requested zooms even when the generic clean
    # tick alignment would otherwise expand their limits.
    axes[0, 0].set_yticks((0.40, 0.45, 0.50, 0.55, 0.60))
    axes[0, 0].set_ylim(0.4, 0.6)
    axes[1, 0].set_yticks((0.3, 0.4, 0.5, 0.6, 0.7, 0.8))
    axes[1, 0].set_ylim(0.3, 0.8)
    axes[1, 0].set_xticks((-0.5, -0.25, 0.0, 0.25, 0.5, 0.75))
    axes[1, 0].set_xlim(-0.5, 0.75)
    outputs = _save(
        fig,
        output_dir / "fig02_historical_vs_apo_implied_volatility",
        formats,
    )
    return outputs, {"smile_dates": smile_meta}


def _pretty_sample(sample: str) -> str:
    mapping = {
        "all": "All",
        "positive_volume": "Positive volume",
        "open_interest_ge_1": r"$OI\geq1$",
        "open_interest_ge_10": r"$OI\geq10$",
        "open_interest_ge_100": r"$OI\geq100$",
        "open_interest_ge_500": r"$OI\geq500$",
    }
    return mapping.get(sample, sample)


def _forest_panel(
    ax: plt.Axes,
    boot: pd.DataFrame,
    *,
    metric: str,
) -> None:
    """Plot forward-minus-historical error differences by APO expiry."""
    experiments = [
        (
            "forward_q_expanding_smile",
            "Expanding smile",
            "o",
            FIG3_COLORS["expanding"],
            FIG3_COLORS["expanding"],
        ),
        (
            "forward_q_previous_day_smile",
            "Previous-day smile",
            "s",
            FIG3_COLORS["previous_day"],
            FIG3_COLORS["previous_day"],
        ),
    ]
    expiry_order = [
        "2026-09",
        "2026-10",
        "2026-11",
        "2027-03",
        "2027-09",
        "2028-03",
        "2028-09",
    ]
    rows = boot.loc[
        boot["scope"].eq("expiry")
        & boot["sample"].eq("all")
        & boot["apo_expiry"].isin(expiry_order)
    ].copy()
    y_base = np.arange(1, len(expiry_order) + 1, dtype=float)
    offsets = (-0.11, 0.11)

    for offset, (experiment, label, marker, color, facecolor) in zip(
        offsets, experiments, strict=True
    ):
        group = (
            rows.loc[rows["experiment"].eq(experiment)]
            .set_index("apo_expiry")
            .loc[expiry_order]
        )
        value = group[f"delta_{metric}"].to_numpy(dtype=float)
        lo = group[f"delta_{metric}_ci025"].to_numpy(dtype=float)
        hi = group[f"delta_{metric}_ci975"].to_numpy(dtype=float)
        xerr = np.vstack([value - lo, hi - value])
        marker_edge = (
            NEUTRAL["dark"]
            if experiment == "forward_q_expanding_smile"
            else FIG3_COLORS["previous_day_edge"]
        )
        ax.errorbar(
            value,
            y_base + offset,
            xerr=xerr,
            fmt=marker,
            markersize=5.8,
            color=color,
            ecolor=color,
            markerfacecolor=facecolor,
            markeredgecolor=marker_edge,
            markeredgewidth=1.05,
            capsize=3.0,
            linewidth=1.35,
            label=label,
        )

    labels = []
    expanding = rows.loc[
        rows["experiment"].eq("forward_q_expanding_smile")
    ].set_index("apo_expiry")
    for expiry in expiry_order:
        n = int(expanding.loc[expiry, "n"])
        labels.append(f"{expiry} ($n={n}$)")

    ax.axvline(
        0.0,
        linestyle=":",
        linewidth=1.25,
        color=FIG3_COLORS["zero_line"],
        zorder=0,
    )
    _category_ticks_with_endpoints(ax, "y", labels)
    ax.set_xlabel(
        fr"$\Delta {metric.upper()}="
        fr"{metric.upper()}_{{\mathrm{{forward}}}}-"
        fr"{metric.upper()}_{{\mathrm{{historical\ PI}}}}$"
    )
    ax.legend(frameon=False)


def build_figure_3(
    output_dir: Path,
    formats: Iterable[str],
) -> tuple[list[str], dict[str, object]]:
    boot = pd.read_csv(BOOTSTRAP_PATH)
    fig, axes = plt.subplots(1, 2, figsize=_word_figsize(3), sharey=True)
    _forest_panel(axes[0], boot, metric="mae")
    _panel_title(axes[0], "A", "MAE difference by expiry")
    _forest_panel(axes[1], boot, metric="rmse")
    _panel_title(axes[1], "B", "RMSE difference by expiry")
    _apply_suptitle(fig, "Date-ordered conditional pricing comparisons across expiries" if CURRENT_JOURNAL == "jfm" else "Forward-in-time volatility comparisons across expiries")
    _align_numeric_axes(fig, categorical_y_axes=tuple(axes))
    outputs = _save(fig, output_dir / "fig03_forward_q_cluster_bootstrap", formats)

    selected = boot.loc[
        boot["scope"].eq("expiry")
        & boot["sample"].eq("all")
        & boot["experiment"].isin(
            ["forward_q_expanding_smile", "forward_q_previous_day_smile"]
        )
    ].copy()
    return outputs, {
        "bootstrap_iterations": int(selected["bootstrap_iterations"].max()),
        "experiments": sorted(selected["experiment"].unique().tolist()),
        "expiries": sorted(selected["apo_expiry"].unique().tolist()),
    }


def _target_label(row: pd.Series) -> str:
    date = pd.Timestamp(row["valuation_date"]).strftime("%m-%d")
    return f"{date}\n$K={row['strike']:g}$"


def build_figure_4(
    output_dir: Path,
    formats: Iterable[str],
) -> tuple[list[str], dict[str, object]]:
    mc = pd.read_csv(HIGH_PRECISION_PATH)
    qmc = pd.read_csv(QMC_PATH)
    keys = ["valuation_date", "apo_expiry", "contract_id", "option_type", "strike"]
    matched = mc.merge(qmc, on=keys, suffixes=("_mc", "_qmc"), how="inner")
    if matched.empty:
        raise ValueError("No matched high-precision MC and randomized-QMC targets")
    matched = matched.sort_values(["valuation_date", "strike", "contract_id"]).reset_index(drop=True)

    x = np.arange(1, len(matched) + 1, dtype=float)
    offsets = (-0.18, 0.0, 0.18)

    fig, axes = plt.subplots(
        2,
        1,
        figsize=(CURRENT_FIGURE_WIDTH_IN, CURRENT_FIGURE_WIDTH_IN),
        sharex=True,
        gridspec_kw={"height_ratios": [0.78, 1.22]},
    )
    ax_top, ax_bottom = axes

    values = [
        (
            "Pseudo-MC",
            matched["mc_pi_minus_pm"].to_numpy(dtype=float),
            matched["mc_pi_minus_pm_mcse"].to_numpy(dtype=float),
            "o",
            FIG4_COLORS["pseudo_mc"],
            FIG4_COLORS["pseudo_mc"],
            FIG4_EDGE_COLORS["pseudo_mc"],
        ),
        (
            "Curran",
            matched["curran_pi_minus_pm_mc"].to_numpy(dtype=float),
            np.zeros(len(matched)),
            "D",
            FIG4_COLORS["curran"],
            FIG4_COLORS["curran"],
            FIG4_EDGE_COLORS["curran"],
        ),
        (
            "Randomized Sobol",
            matched["qmc_pi_minus_pm"].to_numpy(dtype=float),
            matched["qmc_gap_mcse"].to_numpy(dtype=float),
            "s",
            FIG4_COLORS["sobol"],
            "white",
            FIG4_EDGE_COLORS["sobol"],
        ),
    ]

    for offset, (label, value, se, marker, color, facecolor, edgecolor) in zip(
        offsets, values, strict=True
    ):
        ax_top.errorbar(
            x + offset,
            value,
            yerr=1.96 * se,
            fmt=marker,
            markersize=4.3,
            linewidth=1.0,
            color=color,
            ecolor=color,
            markerfacecolor=facecolor,
            markeredgecolor=edgecolor,
            markeredgewidth=1.0,
            capsize=2,
            label=label,
        )
    ax_top.set_ylabel(r"$PI-PM$ price difference")
    _panel_title(ax_top, "A", "Pricing engine comparison")
    ax_top.legend(frameon=False, ncol=3)

    curran = matched["curran_pi_minus_pm_mc"].to_numpy(dtype=float)
    deviations = [
        (
            "Pseudo-MC minus Curran",
            1e6 * (matched["mc_pi_minus_pm"].to_numpy(dtype=float) - curran),
            1e6 * matched["mc_pi_minus_pm_mcse"].to_numpy(dtype=float),
            "o",
            FIG4_COLORS["pseudo_mc"],
            FIG4_COLORS["pseudo_mc"],
            FIG4_EDGE_COLORS["pseudo_mc"],
        ),
        (
            "Sobol minus Curran",
            1e6 * (matched["qmc_pi_minus_pm"].to_numpy(dtype=float) - curran),
            1e6 * matched["qmc_gap_mcse"].to_numpy(dtype=float),
            "s",
            FIG4_COLORS["sobol"],
            "white",
            FIG4_EDGE_COLORS["sobol"],
        ),
    ]
    for offset, (label, value, se, marker, color, facecolor, edgecolor) in zip(
        (-0.09, 0.09), deviations, strict=True
    ):
        ax_bottom.errorbar(
            x + offset,
            value,
            yerr=1.96 * se,
            fmt=marker,
            markersize=4.0,
            linewidth=1.0,
            color=color,
            ecolor=color,
            markerfacecolor=facecolor,
            markeredgecolor=edgecolor,
            markeredgewidth=0.95,
            capsize=2,
            label=label,
        )
    ax_bottom.axhline(
        0.0,
        linestyle="--",
        linewidth=0.95,
        color=NEUTRAL["mid"],
    )
    ax_bottom.set_ylabel(r"Difference from Curran ($\times 10^6$)")
    ax_bottom.set_xlabel("Empirical target")
    ax_bottom.legend(frameon=False, ncol=2)
    _panel_title(ax_bottom, "B", "Deviation from Curran")

    labels = [_target_label(row) for _, row in matched.iterrows()]
    _category_ticks_with_endpoints(ax_bottom, "x", labels)

    _apply_suptitle(fig, "Numerical identification of the posterior-integration effect")
    _align_numeric_axes(fig, categorical_x_axes=tuple(axes))
    ax_bottom.set_yticks((-15.0, -10.0, -5.0, 0.0, 5.0, 10.0, 15.0))
    ax_bottom.set_ylim(-15.0, 15.0)
    outputs = _save(fig, output_dir / "fig04_numerical_identification", formats)
    return outputs, {
        "matched_targets": int(len(matched)),
        "target_labels": labels,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=None,
        help="Output directory (defaults to figures/publication for REMEF and figures/jfm for JFM).",
    )
    parser.add_argument(
        "--journal", choices=("remef", "jfm"), default="remef",
        help="REMEF retains its unchanged defaults; JFM uses a separate draft figure directory.",
    )
    parser.add_argument(
        "--formats",
        nargs="+",
        choices=("pdf", "png", "svg"),
        default=("png", "pdf", "svg"),
    )
    parser.add_argument(
        "--figures",
        nargs="+",
        type=int,
        choices=(1, 2, 3, 4),
        default=(1, 2, 3, 4),
        help="Subset of main figures to build.",
    )
    parser.add_argument(
        "--mechanism-run",
        type=Path,
        default=None,
        help="Optional explicit massive mechanism-map run directory.",
    )
    parser.add_argument(
        "--no-tex",
        action="store_true",
        help="Legacy flag: REMEF Word figures always avoid external TeX.",
    )
    parser.add_argument(
        "--allow-font-fallback",
        action="store_true",
        help="Preview only: permit Liberation Serif when Times New Roman is unavailable.",
    )
    return parser.parse_args()


def _open_wiley_publication():
    """Measure the actual trusted Wiley class, fonts, and TeX text width."""
    try:
        import awesomefigures as af
    except ImportError as exc:
        raise SystemExit(
            "JFM exact typography requires AwesomeFigures. Install "
            "paper/requirements-awesomefigures.txt in asian-options."
        ) from exc
    if not callable(getattr(af, "paper", None)):
        raise SystemExit(
            "AwesomeFigures is outdated: af.paper() not found. "
            "Install paper/requirements-awesomefigures.txt."
        )
    # The Wiley class loads bundled resources relative to the source folder.
    # Stage the *same* manuscript and vendor font tree as paper/build.py.
    from paper.build import STAGE_DIR, prepare_stage, validate_layout
    validate_layout()
    prepare_stage()
    af.clear_publication_cache()
    return af.paper(
        STAGE_DIR / "main.tex", engine="xelatex",
        style="elegante", palette="okabe-ito", width="text",
        minimum_text_pt=7.0, strict=True, timeout=180,
    )


def _apply_jfm_latex_metrics(pub) -> None:
    """Match final figure* width and font sizes to the TeX document."""
    global CURRENT_FIGURE_WIDTH_IN
    CURRENT_FIGURE_WIDTH_IN = pub.layout.width_inches("text")
    body = float(pub.layout.fontsize_pt)
    PUBLICATION_FONT_PT.update({
        "suptitle": body,
        "panel_title": body * 0.9,
        "axis_label": body * 0.9,
        "tick": body * 0.8,
        "legend": body * 0.8,
        "panel_letter": body * 0.9,
    })
    # af.paper supplies the actual font through the exact PGF PDF. Only
    # customize axis decoration here; do not restore Times New Roman.
    mpl.rcParams.update({
        "axes.labelsize": PUBLICATION_FONT_PT["axis_label"],
        "axes.titlesize": PUBLICATION_FONT_PT["panel_title"],
        "figure.titlesize": PUBLICATION_FONT_PT["suptitle"],
        "xtick.labelsize": PUBLICATION_FONT_PT["tick"],
        "ytick.labelsize": PUBLICATION_FONT_PT["tick"],
        "legend.fontsize": PUBLICATION_FONT_PT["legend"],
        "axes.unicode_minus": False,
        "axes.grid": True,
        "grid.color": NEUTRAL["grid"],
        "grid.linewidth": 0.45,
        "grid.alpha": 0.35,
        "savefig.bbox": None,
        "savefig.pad_inches": 0,
        "svg.fonttype": "none",
    })


def _awesomefigures_report(pub, output_dir: Path) -> dict[str, object]:
    """Preserve audit and replace Windows-specific absolute paths in JSON."""
    report_path = pub.report(output_dir / "awesomefigures_manifest.json")
    audit = json.loads(report_path.read_text(encoding="utf-8"))
    audit["manuscript"] = "paper/build/stage/main.tex"
    for item in audit["figures"]:
        item["path"] = _portable_path(Path(item["path"]))
    report_path.write_text(
        json.dumps(audit, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    md = report_path.with_suffix(".md")
    md.write_text(
        md.read_text(encoding="utf-8").replace(
            str(pub.manuscript), "paper/build/stage/main.tex"
        ),
        encoding="utf-8",
    )
    pdfs = [record for record in audit["figures"] if record["format"] == "pdf"]
    if not pdfs or any(
        record["typography"] != "exact-tex-preamble" for record in pdfs
    ):
        raise RuntimeError("JFM PDF typography must use the Wiley TeX preamble, never a fallback")
    if not audit["all_passed"]:
        raise RuntimeError("AwesomeFigures reported nonconforming figure sizes/fonts")
    return {
        "engine": "xelatex",
        "tex_source": "paper/build/stage/main.tex",
        "manuscript_sha256": audit["manuscript_sha256"],
        "font_mode": "exact-tex-preamble",
        "layout": audit["layout"],
        "report": _portable_path(report_path),
        "exact_pdf_count": len(pdfs),
        "all_passed": True,
        "preview_font_identity": "SVG/PNG do not guarantee exact TeX fonts",
    }


def main() -> None:
    args = parse_args()
    global CURRENT_FIGURE_WIDTH_IN, CURRENT_JOURNAL, CURRENT_JFM_PAPER
    CURRENT_JOURNAL = args.journal
    if args.journal == "jfm" and (args.no_tex or args.allow_font_fallback):
        raise SystemExit(
            "JFM uses exact AwesomeFigures XeLaTeX; --no-tex and "
            "--allow-font-fallback are REMEF-only preview flags."
        )
    formats = tuple(dict.fromkeys(args.formats))
    requested = tuple(dict.fromkeys(args.figures))
    if args.journal == "jfm" and "pdf" not in formats:
        raise SystemExit("JFM requires an audited exact XeLaTeX PDF (include --formats pdf)")

    output_dir = args.output_dir or (
        Path("figures/jfm") if args.journal == "jfm" else DEFAULT_OUTPUT_DIR
    )
    if not output_dir.is_absolute():
        output_dir = ROOT / output_dir
    output_dir.mkdir(parents=True, exist_ok=True)

    if args.journal == "remef":
        CURRENT_FIGURE_WIDTH_IN = WORD_TEXT_WIDTH_IN
        font_mode = _configure_matplotlib(
            force_no_tex=args.no_tex,
            require_times_new_roman=not args.allow_font_fallback,
        )
    else:
        font_mode = "exact-tex-preamble"

    def render() -> dict[str, object]:
        items = {}
        if 1 in requested:
            mechanism_run = _discover_monster_mechanism_run(args.mechanism_run)
            outputs, metadata = build_figure_1(mechanism_run, output_dir, formats)
            items["1"] = {"outputs": outputs, **metadata}
        if 2 in requested:
            outputs, metadata = build_figure_2(output_dir, formats)
            items["2"] = {"outputs": outputs, **metadata}
        if 3 in requested:
            outputs, metadata = build_figure_3(output_dir, formats)
            items["3"] = {"outputs": outputs, **metadata}
        if 4 in requested:
            outputs, metadata = build_figure_4(output_dir, formats)
            items["4"] = {"outputs": outputs, **metadata}
        return items

    jfm_publication = None
    if args.journal == "jfm":
        from scripts.jfm_pgf_asset_paths import jfm_pgf_sidecar_support
        with _open_wiley_publication() as pub, jfm_pgf_sidecar_support():
            CURRENT_JFM_PAPER = pub
            try:
                _apply_jfm_latex_metrics(pub)
                figures = render()
                jfm_publication = _awesomefigures_report(pub, output_dir)
            finally:
                CURRENT_JFM_PAPER = None
    else:
        figures = render()

    manifest: dict[str, object] = {
        "output_dir": _portable_path(output_dir),
        "formats": list(formats),
        "font_mode": font_mode,
        "word_text_width_inches": WORD_TEXT_WIDTH_IN,
        "format_target": (
            "JFM Wiley measured XeLaTeX/PGF PDFs; SVG/PNG are previews"
            if args.journal == "jfm" else "REMEF Word, Times New Roman"
        ),
        "figure_width_inches": CURRENT_FIGURE_WIDTH_IN,
        "journal_target": args.journal,
        "numeric_axis_alignment": "built-in nice-tick endpoints (never crop data)",
        "typographic_hierarchy_pt": dict(PUBLICATION_FONT_PT),
        "svg_text_mode": "editable-native-text",
        "hybrid_pdf": True,
        "raster_dpi": 600,
        "categorical_palettes": {
            "figure1_discrete": FIG1_DISCRETE,
            "figure2": FIG2_COLORS,
            "figure3": FIG3_COLORS,
            "figure4": FIG4_COLORS,
        },
        "continuous_colormap": "Paul Tol Iridescent (heatmap B)",
        "second_order_colormap": MECHANISM_CMAP.name,
        "continuous_colormap_hex": IRIDESCENT_HEX,
        "bad_data_color": BAD_DATA_COLOR,
        "neutral_palette": NEUTRAL,
        "print_mode": "color + grayscale-safe redundancy",
        "style_encoding": "color + marker + line pattern + marker fill",
        "figures": figures,
    }
    if jfm_publication is not None:
        manifest["awesomefigures_publication"] = jfm_publication
    manifest_path = output_dir / "figure_manifest.json"
    manifest_path.write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(f"Built publication figures under {output_dir}")
    print(f"Font mode: {font_mode}")
    for item in manifest["figures"].values():
        for output in item["outputs"]:
            print(f"  {output}")
    print(f"  {_portable_path(manifest_path)}")

if __name__ == "__main__":
    main()
