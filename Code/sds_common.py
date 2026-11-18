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


def dollar_axis(ax, which: str = "x") -> None:
    """Log axis labelled in dollars. Position is linear in ln(GDP), i.e. in G."""
    from matplotlib.ticker import FixedLocator, FuncFormatter, NullLocator
    axis = ax.xaxis if which == "x" else ax.yaxis
    (ax.set_xscale if which == "x" else ax.set_yscale)("log")
    axis.set_major_locator(FixedLocator(GDP_TICKS))
    axis.set_major_formatter(FuncFormatter(
        lambda v, _: f"${v/1000:g}k" if v >= 1000 else f"${v:g}"))
    axis.set_minor_locator(NullLocator())


def load_panel() -> pd.DataFrame:
    return pd.read_csv(PANEL)
