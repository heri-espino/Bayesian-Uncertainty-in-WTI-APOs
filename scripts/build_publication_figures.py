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
fig01_mechanism_map.{pdf,png}
    When posterior integration matters and how the Taylor mechanism explains it.
fig02_historical_vs_apo_implied_volatility.{pdf,png}
    Historical posterior volatility versus APO-implied effective volatility and
    representative strike smiles.
fig03_forward_q_cluster_bootstrap.{pdf,png}
    Strict forward-in-time pricing improvement with valuation-date cluster intervals.
fig04_numerical_identification.{pdf,png}
    Agreement of Curran, high-precision pseudo-MC, and randomized Sobol PI--PM gaps.
figure_manifest.json
    Source paths and plotting choices used for the build.

The plotting code uses only matplotlib/pandas/numpy at runtime.  When the exact Wiley
Utopia TeX stack is installed, labels are rendered with the same Utopia + mathastext
configuration used by WileyNJDv5; otherwise the script falls back deterministically to STIX.
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
    / "wti_liquidity_bootstrap"
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

PALETTE = {
    "ink": "#17324D",
    "teal": "#2A6F97",
    "green": "#3A7D44",
    "gold": "#C28F2C",
    "wine": "#8E4B5B",
    "purple": "#6C5B9A",
    "charcoal": "#3B3F46",
    "midgray": "#7F8790",
    "light_gray": "#D9DDE3",
    "very_light_gray": "#F4F6F8",
}

SIGMA_COLORS = {
    0.10: PALETTE["green"],
    0.20: PALETTE["teal"],
    0.35: PALETTE["ink"],
    0.50: PALETTE["purple"],
    0.80: PALETTE["wine"],
}

MATURITY_STYLES = {
    21: (PALETTE["green"], "o"),
    63: (PALETTE["teal"], "s"),
    126: (PALETTE["ink"], "^"),
    252: (PALETTE["wine"], "D"),
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


def _configure_matplotlib(*, force_no_tex: bool = False) -> str:
    """Match the active Wiley Utopia2COL manuscript when TeX is available."""
    try:
        plt.style.use("seaborn-v0_8-whitegrid")
    except OSError:
        plt.style.use("default")

    utopia_mode = None if force_no_tex else _wiley_utopia_mode()
    use_tex = utopia_mode is not None
    rc = {
        "text.usetex": use_tex,
        "font.family": "serif",
        "font.size": 8.5,
        "axes.labelsize": 8.5,
        "axes.titlesize": 9.0,
        "legend.fontsize": 7.5,
        "xtick.labelsize": 7.5,
        "ytick.labelsize": 7.5,
        "axes.unicode_minus": False,
        "figure.dpi": 180,
        "savefig.dpi": 600,
        "savefig.bbox": "tight",
        "savefig.pad_inches": 0.035,
        "pdf.fonttype": 42,
        "ps.fonttype": 42,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.linewidth": 0.75,
        "axes.edgecolor": PALETTE["charcoal"],
        "axes.facecolor": "white",
        "axes.axisbelow": True,
        "axes.grid": True,
        "grid.color": PALETTE["light_gray"],
        "grid.linewidth": 0.55,
        "grid.alpha": 0.72,
        "xtick.direction": "out",
        "ytick.direction": "out",
        "xtick.major.size": 3.0,
        "ytick.major.size": 3.0,
        "xtick.major.width": 0.7,
        "ytick.major.width": 0.7,
        "lines.linewidth": 1.45,
        "lines.markersize": 4.0,
        "legend.frameon": False,
        "legend.borderaxespad": 0.25,
        "legend.handlelength": 1.8,
    }
    if use_tex:
        rc["text.latex.preamble"] = (
            r"\usepackage[T1]{fontenc}"
            r"\usepackage{utopia}"
            r"\usepackage[defaultmathsizes,italic]{mathastext}"
            r"\usepackage{amsmath,amssymb}"
        )
        font_mode = utopia_mode or "wiley-utopia-system"
    else:
        rc["mathtext.fontset"] = "stix"
        font_mode = "stix-fallback"
    mpl.rcParams.update(rc)
    return font_mode


def _portable_path(path: Path) -> str:
    """Return a repo-relative path when possible, otherwise an absolute path."""
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def _save(fig: plt.Figure, stem: Path, formats: Iterable[str]) -> list[str]:
    """Save hybrid PDFs: vector text/axes with dense artists rasterized at 600 dpi."""
    outputs: list[str] = []
    stem.parent.mkdir(parents=True, exist_ok=True)
    metadata = {
        "Title": stem.stem,
        "Author": "Heriberto Espino Montelongo",
        "Subject": "Bayesian parameter uncertainty in WTI average price options",
    }
    for fmt in formats:
        path = stem.with_suffix(f".{fmt}")
        fig.savefig(
            path,
            dpi=600,
            bbox_inches="tight",
            pad_inches=0.035,
            metadata=metadata if fmt == "pdf" else None,
        )
        outputs.append(_portable_path(path))
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
        if report.get("preset") != "monster":
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


def _panel_label(ax: plt.Axes, label: str) -> None:
    ax.text(
        -0.12,
        1.05,
        label,
        transform=ax.transAxes,
        fontweight="bold",
        va="bottom",
        ha="left",
        color=PALETTE["charcoal"],
    )


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

    fig, axes = plt.subplots(2, 2, figsize=(7.25, 5.8))
    ax_a, ax_b, ax_c, ax_d = axes.flat

    # A. Posterior dispersion shrinks with information.
    for sigma_true, group in posterior.groupby("sigma_true", sort=True):
        group = group.sort_values("n_obs")
        sigma_key = round(float(sigma_true), 2)
        ax_a.plot(
            group["n_obs"],
            group["posterior_sigma_sd_mean"],
            marker="o",
            color=SIGMA_COLORS.get(sigma_key, PALETTE["charcoal"]),
            label=fr"$\sigma_0={sigma_true:.2f}$",
        )
    ax_a.set_xscale("log")
    ax_a.set_xlabel("Historical observations $n$")
    ax_a.set_ylabel(r"Mean posterior SD of $\sigma$")
    ax_a.set_title("Posterior dispersion")
    ax_a.legend(ncol=2, frameon=False)
    _panel_label(ax_a, "A")

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
        cmap="magma",
        rasterized=True,
    )
    ax_b.grid(False)
    ax_b.set_xticks(np.arange(len(heat.columns)))
    ax_b.set_xticklabels([f"{x:.2f}" for x in heat.columns], rotation=45, ha="right")
    ax_b.set_yticks(np.arange(len(heat.index)))
    ax_b.set_yticklabels([f"{x:.3g}" for x in heat.index])
    ax_b.set_xlabel(r"Moneyness $K/F$")
    ax_b.set_ylabel("Fraction already fixed")
    ax_b.set_title(
        fr"Mean $|PI-PM|$: $n={MECHANISM_N}$, "
        fr"$\sigma_0={MECHANISM_SIGMA:.2f}$, "
        fr"$T={MECHANISM_HEATMAP_MATURITY_DAYS}$d"
    )
    cbar = fig.colorbar(image, ax=ax_b, fraction=0.047, pad=0.04)
    cbar.set_label(r"Mean $|PI-PM|$")
    _panel_label(ax_b, "B")

    # C. Partial fixing for extreme moneyness, separated by maturity.
    curve = adverse.loc[
        np.isclose(adverse["moneyness"], MECHANISM_MONEYNESS)
    ].copy()
    for maturity, group in curve.groupby("maturity_days", sort=True):
        group = group.sort_values("fraction_fixed")
        color, marker = MATURITY_STYLES.get(
            int(maturity), (PALETTE["charcoal"], "o")
        )
        ax_c.plot(
            group["fraction_fixed"],
            group["mean_abs_pi_minus_pm"],
            marker=marker,
            color=color,
            label=f"{int(maturity)} days",
        )
    ax_c.set_xlabel("Fraction already fixed")
    ax_c.set_ylabel(r"Mean $|PI-PM|$")
    ax_c.set_title(
        fr"Partial fixing: $n={MECHANISM_N}$, "
        fr"$\sigma_0={MECHANISM_SIGMA:.2f}$, "
        fr"$K/F={MECHANISM_MONEYNESS:.2f}$"
    )
    ax_c.legend(frameon=False)
    _panel_label(ax_c, "C")

    # D. Taylor mechanism across every synthetic cell.
    x = summary["mean_taylor_gap"].to_numpy(dtype=float)
    y = summary["mean_pi_minus_pm"].to_numpy(dtype=float)
    finite = np.isfinite(x) & np.isfinite(y)
    hb = ax_d.hexbin(
        x[finite],
        y[finite],
        gridsize=42,
        mincnt=1,
        cmap="Greys",
        linewidths=0.0,
        rasterized=True,
    )
    lo = float(min(x[finite].min(), y[finite].min()))
    hi = float(max(x[finite].max(), y[finite].max()))
    ax_d.plot(
        [lo, hi],
        [lo, hi],
        linestyle="--",
        linewidth=1.15,
        color=PALETTE["wine"],
    )
    corr = float(np.corrcoef(x[finite], y[finite])[0, 1])
    ax_d.set_xlabel(
        r"Taylor prediction $\frac{1}{2}C^{Q\prime\prime}(\bar\sigma)"
        r"\mathrm{Var}(\sigma\mid D)$"
    )
    ax_d.set_ylabel(r"Actual mean $PI-PM$")
    ax_d.set_title(fr"Second-order mechanism ($r={corr:.4f}$)")
    cbar2 = fig.colorbar(hb, ax=ax_d, fraction=0.047, pad=0.04)
    cbar2.set_label("Cell count")
    _panel_label(ax_d, "D")

    fig.suptitle("When posterior integration matters", y=1.01, fontsize=11)
    fig.tight_layout()
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
        color=PALETTE["ink"],
        label=r"Historical posterior mean $\sigma_P$",
    )
    ax.plot(
        group["valuation_date"],
        group["full_sample_sigma_q"],
        marker="s",
        color=PALETTE["gold"],
        label=r"APO-implied common $\sigma_Q$",
    )
    ax.set_ylabel("Annualized volatility")
    ax.set_title(f"{expiry} expiry")
    ax.tick_params(axis="x", rotation=35)
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
        "call": ("o", PALETTE["ink"], "Calls"),
        "put": ("s", PALETTE["wine"], "Puts"),
    }
    for option_type, (marker, color, label) in styles.items():
        group = day.loc[day["option_type"].eq(option_type)].sort_values("log_moneyness")
        if group.empty:
            continue
        ax.scatter(
            group["log_moneyness"],
            group["apo_implied_sigma_q"],
            marker=marker,
            s=27,
            alpha=0.92,
            color=color,
            edgecolor="white",
            linewidth=0.4,
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
        linestyle=":",
        linewidth=1.15,
        color=PALETTE["midgray"],
        label=r"Historical $\sigma_P$",
    )
    ax.axhline(
        sigma_q,
        linestyle="--",
        linewidth=1.15,
        color=PALETTE["gold"],
        label=r"Common APO $\sigma_Q$",
    )
    ax.set_xlabel(r"Log moneyness $\log(K/\widehat A^Q)$")
    ax.set_ylabel("APO-implied volatility")
    ax.set_title(str(date.date()))
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

    fig, axes = plt.subplots(2, 2, figsize=(7.25, 5.8))
    _plot_sigma_timeseries(axes[0, 0], by_date, "2026-09")
    _panel_label(axes[0, 0], "A")
    _plot_sigma_timeseries(axes[0, 1], by_date, "2026-10")
    _panel_label(axes[0, 1], "B")

    smile_meta: dict[str, object] = {}
    for ax, date, label in zip(axes[1], SMILE_DATES, ("C", "D"), strict=True):
        smile_meta[str(date.date())] = _plot_smile(ax, contracts, by_date, date)
        _panel_label(ax, label)

    fig.suptitle("Historical and APO-implied effective volatility", y=1.01, fontsize=11)
    fig.tight_layout()
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
    experiments = [
        ("forward_q_expanding_smile", "Expanding smile", "o", PALETTE["teal"]),
        ("forward_q_previous_day_smile", "Previous-day smile", "s", PALETTE["purple"]),
    ]
    samples = [
        "all",
        "open_interest_ge_10",
        "open_interest_ge_100",
        "open_interest_ge_500",
        "positive_volume",
    ]
    y_base = np.arange(len(samples), dtype=float)
    offsets = (-0.10, 0.10)

    for offset, (experiment, label, marker, color) in zip(
        offsets, experiments, strict=True
    ):
        group = boot.loc[boot["experiment"].eq(experiment)].set_index("sample")
        rows = group.loc[samples]
        value = rows[f"delta_{metric}"].to_numpy(dtype=float)
        lo = rows[f"delta_{metric}_ci025"].to_numpy(dtype=float)
        hi = rows[f"delta_{metric}_ci975"].to_numpy(dtype=float)
        xerr = np.vstack([value - lo, hi - value])
        ax.errorbar(
            value,
            y_base + offset,
            xerr=xerr,
            fmt=marker,
            markersize=4.6,
            color=color,
            ecolor=color,
            capsize=2.4,
            linewidth=1.05,
            label=label,
        )

    sample_labels = []
    for sample in samples:
        row = boot.loc[
            boot["experiment"].eq("forward_q_expanding_smile")
            & boot["sample"].eq(sample)
        ]
        if row.empty:
            sample_labels.append(_pretty_sample(sample))
        else:
            sample_labels.append(
                f"{_pretty_sample(sample)} ($n={int(row.iloc[0]['n'])}$)"
            )

    ax.axvline(
        0.0,
        linestyle="--",
        linewidth=0.95,
        color=PALETTE["midgray"],
    )
    ax.set_yticks(y_base)
    ax.set_yticklabels(sample_labels)
    ax.invert_yaxis()
    ax.set_xlabel(
        fr"$\Delta {metric.upper()}="
        fr"{metric.upper()}_{{\mathrm{{forward}}}}-"
        fr"{metric.upper()}_{{\mathrm{{historical\ PI}}}}$"
    )
    ax.set_title(f"{metric.upper()} difference")
    ax.legend(frameon=False)


def build_figure_3(
    output_dir: Path,
    formats: Iterable[str],
) -> tuple[list[str], dict[str, object]]:
    boot = pd.read_csv(BOOTSTRAP_PATH)
    fig, axes = plt.subplots(1, 2, figsize=(7.20, 3.35), sharey=True)
    _forest_panel(axes[0], boot, metric="mae")
    _panel_label(axes[0], "A")
    _forest_panel(axes[1], boot, metric="rmse")
    _panel_label(axes[1], "B")
    fig.suptitle(
        "Strict forward-in-time volatility improvement",
        y=1.02,
        fontsize=10.5,
    )
    fig.tight_layout()
    outputs = _save(fig, output_dir / "fig03_forward_q_cluster_bootstrap", formats)

    selected = boot.loc[
        boot["experiment"].isin(
            ["forward_q_expanding_smile", "forward_q_previous_day_smile"]
        )
    ].copy()
    return outputs, {
        "bootstrap_iterations": int(selected["bootstrap_iterations"].max()),
        "experiments": sorted(selected["experiment"].unique().tolist()),
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

    x = np.arange(len(matched), dtype=float)
    offsets = (-0.18, 0.0, 0.18)

    fig, axes = plt.subplots(
        2,
        1,
        figsize=(7.20, 4.90),
        sharex=True,
        gridspec_kw={"height_ratios": [2.1, 1.0]},
    )
    ax_top, ax_bottom = axes

    values = [
        (
            "Pseudo-MC",
            matched["mc_pi_minus_pm"].to_numpy(dtype=float),
            matched["mc_pi_minus_pm_mcse"].to_numpy(dtype=float),
            "o",
            PALETTE["ink"],
        ),
        (
            "Curran",
            matched["curran_pi_minus_pm_mc"].to_numpy(dtype=float),
            np.zeros(len(matched)),
            "D",
            PALETTE["gold"],
        ),
        (
            "Randomized Sobol",
            matched["qmc_pi_minus_pm"].to_numpy(dtype=float),
            matched["qmc_gap_mcse"].to_numpy(dtype=float),
            "s",
            PALETTE["wine"],
        ),
    ]

    for offset, (label, value, se, marker, color) in zip(
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
            capsize=2,
            label=label,
        )
    ax_top.set_ylabel(r"$PI-PM$ price difference")
    ax_top.set_title("Independent pricing engines recover the same integration gap")
    ax_top.legend(frameon=False, ncol=3)
    _panel_label(ax_top, "A")

    curran = matched["curran_pi_minus_pm_mc"].to_numpy(dtype=float)
    deviations = [
        (
            "Pseudo-MC minus Curran",
            1e6 * (matched["mc_pi_minus_pm"].to_numpy(dtype=float) - curran),
            1e6 * matched["mc_pi_minus_pm_mcse"].to_numpy(dtype=float),
            "o",
            PALETTE["ink"],
        ),
        (
            "Sobol minus Curran",
            1e6 * (matched["qmc_pi_minus_pm"].to_numpy(dtype=float) - curran),
            1e6 * matched["qmc_gap_mcse"].to_numpy(dtype=float),
            "s",
            PALETTE["wine"],
        ),
    ]
    for offset, (label, value, se, marker, color) in zip(
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
            capsize=2,
            label=label,
        )
    ax_bottom.axhline(
        0.0,
        linestyle="--",
        linewidth=0.95,
        color=PALETTE["midgray"],
    )
    ax_bottom.set_ylabel(r"Difference from Curran ($\times 10^6$)")
    ax_bottom.set_xlabel("Empirical target")
    ax_bottom.legend(frameon=False, ncol=2)
    _panel_label(ax_bottom, "B")

    labels = [_target_label(row) for _, row in matched.iterrows()]
    ax_bottom.set_xticks(x)
    ax_bottom.set_xticklabels(labels, rotation=45, ha="right")

    fig.suptitle(
        "Numerical identification of the posterior-integration effect",
        y=1.005,
        fontsize=10.5,
    )
    fig.tight_layout()
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
        default=DEFAULT_OUTPUT_DIR,
        help="Output directory (default: figures/publication).",
    )
    parser.add_argument(
        "--formats",
        nargs="+",
        choices=("pdf", "png", "svg"),
        default=("pdf", "png"),
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
        help="Force STIX fallback instead of the Wiley Utopia TeX stack.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    font_mode = _configure_matplotlib(force_no_tex=args.no_tex)
    output_dir = args.output_dir
    if not output_dir.is_absolute():
        output_dir = ROOT / output_dir
    output_dir.mkdir(parents=True, exist_ok=True)

    formats = tuple(dict.fromkeys(args.formats))
    requested = tuple(dict.fromkeys(args.figures))
    manifest: dict[str, object] = {
        "output_dir": _portable_path(output_dir),
        "formats": list(formats),
        "font_mode": font_mode,
        "hybrid_pdf": True,
        "raster_dpi": 600,
        "palette": PALETTE,
        "figures": {},
    }

    if 1 in requested:
        mechanism_run = _discover_monster_mechanism_run(args.mechanism_run)
        outputs, metadata = build_figure_1(mechanism_run, output_dir, formats)
        manifest["figures"]["1"] = {"outputs": outputs, **metadata}

    if 2 in requested:
        outputs, metadata = build_figure_2(output_dir, formats)
        manifest["figures"]["2"] = {"outputs": outputs, **metadata}

    if 3 in requested:
        outputs, metadata = build_figure_3(output_dir, formats)
        manifest["figures"]["3"] = {"outputs": outputs, **metadata}

    if 4 in requested:
        outputs, metadata = build_figure_4(output_dir, formats)
        manifest["figures"]["4"] = {"outputs": outputs, **metadata}

    manifest_path = output_dir / "figure_manifest.json"
    manifest_path.write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(f"Built publication figures under {output_dir}")
    print(f"Font mode: {font_mode}")
    if font_mode == "stix-fallback":
        report = diagnostic_report()
        print("TeX diagnostic:")
        print(json.dumps(report, indent=2))
    for item in manifest["figures"].values():
        for output in item["outputs"]:
            print(f"  {output}")
    print(f"  {_portable_path(manifest_path)}")


if __name__ == "__main__":
    main()
