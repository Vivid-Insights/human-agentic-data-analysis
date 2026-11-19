"""Figure 1: trajectories over time.

Two panels: democracy D, and GDP per capita in constant 2015 US$ on a log axis,
against year. The six representative countries are thin lines (gaps left where a
year is missing). No mean line (locked format).

Reads Code/outputs/panel.csv. Writes outputs/figures/fig1_trajectories_time.png
and outputs/figures/dark/fig1_trajectories_time.png.
"""
import matplotlib.pyplot as plt
import numpy as np

from sds_common import (CM, D_LABEL, G_SCALE, GDP_LABEL, REP, REP_COLOUR, YEARS,
                        dollar_axis, load_panel, save, style)

p = load_panel()
p["gdp_usd"] = np.exp(G_SCALE * p["G"])  # equals gdppc (checked to 4e-10)
years = np.arange(YEARS[0], YEARS[1] + 1)

for theme_name in ("light", "dark"):
    t = style(theme_name)
    fig, axes = plt.subplots(1, 2, figsize=(18 * CM, 8.5 * CM))
    for ax, var, label in [(axes[0], "D", D_LABEL), (axes[1], "gdp_usd", GDP_LABEL)]:
        for iso, name in REP.items():
            s = p[p.iso3 == iso].set_index("year")[var].reindex(years)  # NaN -> gap
            ax.plot(years, s.values, color=REP_COLOUR[iso], lw=1.5, label=name)
        ax.set_xlabel("Year")
        ax.set_ylabel(label)
        ax.set_xlim(YEARS[0] - 0.5, YEARS[1] + 0.5)
        ax.xaxis.set_minor_locator(plt.MultipleLocator(1))
        ax.set_xticks([1985, 1990, 1995, 2000, 2005])
    axes[0].set_ylim(-0.02, 1.02)
    dollar_axis(axes[1], "y")
    handles, labels = axes[0].get_legend_handles_labels()
    fig.legend(handles, labels, loc="lower center", ncol=6, frameon=False,
               bbox_to_anchor=(0.5, 0.0))
    fig.tight_layout(rect=(0, 0.1, 1, 1))
    path = save(fig, "fig1_trajectories_time", theme_name)
    print(f"figure: {path}")
