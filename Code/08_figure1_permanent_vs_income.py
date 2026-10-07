"""Figure 1 — permanent forest conversion against income, across countries.

Sub-question 1, shown before it is tested. One point per country: cumulative
share of year-2000 tree cover permanently converted 2001-2024 against mean GDP
per capita over the same period. Observations only — no fitted curve, because
the shape is what step 4 estimates and drawing it here would answer the question
in the figure.

Two y-scales are produced. The linear one is Figure 1: the sub-question asks
about an inverted U in the level of the share, so that is the scale the
hypothesis is stated on. The log one goes in the appendix, where it shows the
spread that the skew hides on a linear axis.

Reads  outputs/analysis_dataset.csv
Writes outputs/figures/fig1_permanent_vs_income{,_logy}.png  (and dark/)
"""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.ticker import FixedLocator, FuncFormatter, NullLocator

import viz_style as vs

CODE_DIR = Path(__file__).resolve().parent
DATA = CODE_DIR / "outputs" / "analysis_dataset.csv"

XCOL, YCOL, NAMECOL = "gdp_pc_mean", "permanent_loss_share", "country"

# Income ticks in dollars rather than log units: the spacing is logarithmic but
# a reader should not have to exponentiate to place a country.
XTICKS = [1_000, 3_000, 10_000, 30_000, 100_000]

HEADLINE = "Permanent forest conversion against income, 2001–2024"
XLABEL = "GDP per capita, PPP (constant 2021 international $), mean 2001–2024"
YLABEL = "Share of year-2000 forest\npermanently converted"
SOURCE = (
    "Each point is one of 135 countries with at least 100,000 ha of tree cover in 2000. "
    "Permanent conversion is tree cover loss attributed to permanent agriculture, hard "
    "commodities, or settlements and infrastructure. Sources: Global Forest Watch / WRI "
    "and Google DeepMind drivers v1.3; World Bank World Development Indicators."
)


def draw(d: pd.DataFrame, theme_name: str, logy: bool) -> None:
    t = vs.use(theme_name)
    fig, ax = plt.subplots(figsize=(9.0, 5.6))

    ax.scatter(d[XCOL], d[YCOL], s=46, color=t.series[0], alpha=0.78,
               edgecolors=t.surface, linewidths=0.6, zorder=3)

    ax.set_xscale("log")
    ax.xaxis.set_major_locator(FixedLocator(XTICKS))
    ax.xaxis.set_minor_locator(NullLocator())
    ax.xaxis.set_major_formatter(FuncFormatter(lambda v, _: f"{v:,.0f}"))
    ax.set_xlim(d[XCOL].min() / 1.35, d[XCOL].max() * 1.35)

    if logy:
        ax.set_yscale("log")
        ax.set_ylim(d[YCOL].min() / 1.6, d[YCOL].max() * 1.6)
        ax.yaxis.set_major_locator(FixedLocator([0.001, 0.01, 0.1]))
        ax.yaxis.set_minor_locator(NullLocator())
        ax.yaxis.set_major_formatter(FuncFormatter(lambda v, _: f"{v:g}"))
    else:
        ax.set_ylim(0, d[YCOL].max() * 1.08)

    ax.set_xlabel(XLABEL)
    ax.set_ylabel(YLABEL)

    # Axis extremes only. The eight cases selected for sub-question 3 are not
    # marked here; they carry no meaning for this comparison.
    vs.label_extremes(ax, vs.pick_extremes(d, XCOL, YCOL, NAMECOL),
                      XCOL, YCOL, lambda r: r[NAMECOL])

    vs.header(fig, HEADLINE)
    vs.source_note(fig, SOURCE)
    vs.layout(fig)
    vs.save(fig, "fig1_permanent_vs_income" + ("_logy" if logy else ""))


def main() -> None:
    d = pd.read_csv(DATA)
    print(f"  {len(d)} countries read from {DATA.name}")
    print(f"  x {XCOL}: {d[XCOL].min():,.0f} to {d[XCOL].max():,.0f}")
    print(f"  y {YCOL}: {d[YCOL].min():.4f} to {d[YCOL].max():.4f}")
    for row in vs.pick_extremes(d, XCOL, YCOL, NAMECOL):
        print(f"  labelled {row[0]:>5}: {row[1][NAMECOL]}")
    for logy in (False, True):
        for theme_name in ("light", "dark"):
            draw(d, theme_name, logy)


if __name__ == "__main__":
    main()
