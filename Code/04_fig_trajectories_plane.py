"""Figure 2: trajectories in the (G, D) plane.

All countries with both variables in the last year as faint points; the six
representative countries' paths over the whole period as lines (gaps left where a
year is missing), each start marked with a filled circle; the path of the mean over
the balanced countries as a thick line. GDP across, democracy up: the same axes as
the phase portraits.

Reads Code/outputs/panel.csv. Writes outputs/figures/fig2_trajectories_plane.png
and outputs/figures/dark/fig2_trajectories_plane.png.
"""
import matplotlib.pyplot as plt
import numpy as np

from sds_common import (CM, REP, REP_COLOUR, YEARS, load_panel, mean_colour,
                        save, style)

p = load_panel()
years = np.arange(YEARS[0], YEARS[1] + 1)
mean = p[p.balanced].groupby("year")[["D", "G"]].mean().reindex(years)
n_bal = p.loc[p.balanced, "iso3"].nunique()
last = p[p.year == YEARS[1]]

for theme_name in ("light", "dark"):
    t = style(theme_name)
    fig, ax = plt.subplots(figsize=(17 * CM, 10.5 * CM))
    ax.scatter(last.G, last.D, s=10, color=t.muted, alpha=0.45, lw=0,
               label=f"All countries, {YEARS[1]}", zorder=1)
    for iso, name in REP.items():
        s = p[p.iso3 == iso].set_index("year")[["G", "D"]].reindex(years)  # NaN -> gap
        c = REP_COLOUR[iso]
        ax.plot(s.G.values, s.D.values, color=c, lw=1.5, label=name, zorder=3)
        first = s.dropna().iloc[0]
        ax.scatter(first.G, first.D, s=28, color=c, zorder=4, edgecolors=t.surface,
                   linewidths=0.6)
    ax.plot(mean.G.values, mean.D.values, color=mean_colour(t), lw=3.2,
            label=f"Mean of {n_bal} countries", zorder=5)
    m0 = mean.iloc[0]
    ax.scatter(m0.G, m0.D, s=40, color=mean_colour(t), zorder=6,
               edgecolors=t.surface, linewidths=0.6)
    ax.set_xlabel("Log GDP per capita ÷ 12, $G$")
    ax.set_ylabel("Democracy, $D$")
    ax.set_ylim(-0.03, 1.03)
    ax.legend(loc="upper left", bbox_to_anchor=(1.02, 1.0), frameon=False,
              handlelength=1.4, borderaxespad=0.0)
    fig.tight_layout()
    path = save(fig, "fig2_trajectories_plane", theme_name)
    print(f"figure: {path}")
