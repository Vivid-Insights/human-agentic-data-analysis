"""Figure 2: trajectories in the GDP-democracy plane.

GDP per capita (constant 2015 US$, log axis) across, democracy up: the same axes
as the phase portraits. All countries with both variables in the last year as faint
points; the six representative countries' paths over the whole period as lines
(gaps left where a year is missing), each start marked with a filled circle.
No mean path (locked format).

Reads Code/outputs/panel.csv. Writes outputs/figures/fig2_trajectories_plane.png
and outputs/figures/dark/fig2_trajectories_plane.png.
"""
import matplotlib.pyplot as plt
import numpy as np

from sds_common import (CM, D_LABEL, G_SCALE, GDP_LABEL, REP, REP_COLOUR, YEARS,
                        USD_XLIM, dollar_axis, load_panel, save, style)

p = load_panel()
p["gdp_usd"] = np.exp(G_SCALE * p["G"])
years = np.arange(YEARS[0], YEARS[1] + 1)
last = p[p.year == YEARS[1]]

for theme_name in ("light", "dark"):
    t = style(theme_name)
    fig, ax = plt.subplots(figsize=(17 * CM, 10.5 * CM))
    ax.scatter(last.gdp_usd, last.D, s=10, color=t.muted, alpha=0.45, lw=0,
               label=f"All countries, {YEARS[1]}", zorder=1)
    for iso, name in REP.items():
        s = p[p.iso3 == iso].set_index("year")[["gdp_usd", "D"]].reindex(years)  # NaN -> gap
        c = REP_COLOUR[iso]
        ax.plot(s.gdp_usd.values, s.D.values, color=c, lw=1.5, label=name, zorder=3)
        first = s.dropna().iloc[0]
        ax.scatter(first.gdp_usd, first.D, s=28, color=c, zorder=4,
                   edgecolors=t.surface, linewidths=0.6)
    dollar_axis(ax, "x")
    ax.set_xlim(*USD_XLIM)
    ax.set_xlabel(GDP_LABEL)
    ax.set_ylabel(D_LABEL)
    ax.set_ylim(-0.03, 1.03)
    ax.legend(loc="upper left", bbox_to_anchor=(1.02, 1.0), frameon=False,
              handlelength=1.4, borderaxespad=0.0)
    fig.tight_layout()
    path = save(fig, "fig2_trajectories_plane", theme_name)
    print(f"figure: {path}")
