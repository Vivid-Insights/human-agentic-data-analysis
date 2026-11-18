"""Shared constants and helpers for the democracy-GDP dynamical-systems analysis.

Holds the representative countries, their fixed colours, and the figure style
(David's graph style inside the workspace's light/dark themes), so every figure
script uses the same choices.
"""
from __future__ import annotations

from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd

import viz_style

CODE = Path(__file__).resolve().parent
ROOT = CODE.parent
OUT = CODE / "outputs"
PANEL = OUT / "panel.csv"
COUNTS = OUT / "02_panel_counts.txt"

YEARS = (1981, 2006)
G_SCALE = 12.0  # G = ln(GDP per capita) / 12  (Spaiser et al. 2014, File S1, S12.4)

# Representative countries: fixed before any figure was drawn (Appendix, Research
# Question). Order fixes the colour, so a country keeps its colour in every figure.
REP = {"ITA": "Italy", "SWE": "Sweden", "IND": "India",
       "CHL": "Chile", "ALB": "Albania", "NGA": "Nigeria"}
PALETTE = ["#4E79A7", "#E15759", "#59A14F", "#9B6BB5", "#F28E2B", "#76B7B2"]
REP_COLOUR = dict(zip(REP, PALETTE))

CM = 1 / 2.54
DPI = 300


def style(theme_name: str):
    """Workspace theme (surface, grid, ink) with David's sizes on top."""
    t = viz_style.use(theme_name)
    mpl.rcParams.update({
        "font.size": 11, "axes.labelsize": 11, "axes.titlesize": 11,
        "xtick.labelsize": 11, "ytick.labelsize": 11,
        "legend.fontsize": 10, "legend.frameon": False,
        "lines.linewidth": 1.5, "savefig.dpi": DPI, "figure.dpi": 100,
        "xtick.major.size": 3, "ytick.major.size": 3,
        "xtick.minor.size": 1.5,
    })
    return t


def mean_colour(t) -> str:
    """The mean is drawn in the theme's ink, not a series colour (never pure black)."""
    return t.text_secondary


def save(fig, name: str, theme_name: str) -> Path:
    out = OUT / "figures" if theme_name == "light" else OUT / "figures" / "dark"
    out.mkdir(parents=True, exist_ok=True)
    path = out / f"{name}.png"
    # Fixed canvas: no bbox_inches="tight", so the figure cannot grow to fit stray text.
    fig.savefig(path, dpi=DPI, facecolor=fig.get_facecolor())
    plt.close(fig)
    return path


GDP_LABEL = "GDP per capita (2015 US$)"
D_LABEL = "Democracy (index, 0 to 1)"
GDP_TICKS = [500, 1000, 2000, 5000, 10000, 20000, 50000, 100000]
# Shared GDP range for the plane figures and phase portraits, so their axes match.
USD_XLIM = (150, 170000)


def dollar_axis(ax, which: str = "x") -> None:
    """Log axis labelled in dollars. Position is linear in ln(GDP), i.e. in G."""
    from matplotlib.ticker import FixedLocator, FuncFormatter, NullLocator
    axis = ax.xaxis if which == "x" else ax.yaxis
    (ax.set_xscale if which == "x" else ax.set_yscale)("log")
    axis.set_major_locator(FixedLocator(GDP_TICKS))
    axis.set_major_formatter(FuncFormatter(
        lambda v, _: f"${v/1000:g}k" if v >= 1000 else f"${v:g}"))
    axis.set_minor_locator(NullLocator())


# Locked phase-portrait arrow format (instructions.md, Report Format).
ARROW_K = 5 * 2 / 3              # arrow = yearly change x 3 1/3 years
ARROW_CAP_CM = 0.7 * 2 / 3       # longest drawn arrow, cm on the page (direction kept)
ARROW_LEGEND = "Mean change,\n3⅓ years (capped)"


def draw_capped_arrows(fig, ax, G, D, dG, dD, colour) -> int:
    """Draw locked-format arrows from (G, D) along (dG, dD); returns number capped.

    Call after the axes limits and fig.tight_layout() are final: the cap is in cm on
    the page. The x axis is linear in G (log dollars), so scaling (dG, dD) by one
    factor leaves the direction on the page unchanged.
    """
    import numpy as np
    usd = lambda g: np.exp(G_SCALE * g)
    bb = ax.get_window_extent().transformed(fig.dpi_scale_trans.inverted())
    w_cm, h_cm = bb.width / CM, bb.height / CM
    gx0, gx1 = np.log(ax.get_xlim()) / G_SCALE
    dy0, dy1 = ax.get_ylim()
    n_capped = 0
    for g, d, vg, vd in zip(G, D, dG, dD):
        vx_cm = ARROW_K * vg / (gx1 - gx0) * w_cm
        vy_cm = ARROW_K * vd / (dy1 - dy0) * h_cm
        length = np.hypot(vx_cm, vy_cm)
        f = min(1.0, ARROW_CAP_CM / length) if length > 0 else 1.0
        n_capped += f < 1.0
        ax.annotate("", xy=(usd(g + f * ARROW_K * vg), d + f * ARROW_K * vd),
                    xytext=(usd(g), d), zorder=4,
                    arrowprops=dict(arrowstyle="-|>", color=colour, lw=1.1,
                                    mutation_scale=7, shrinkA=0, shrinkB=0))
        ax.scatter([usd(g)], [d], s=6, color=colour, zorder=5, lw=0)
    return int(n_capped)


def load_panel() -> pd.DataFrame:
    return pd.read_csv(PANEL)
