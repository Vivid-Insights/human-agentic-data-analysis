"""Figure 4: the fitted model's phase portrait. Reads exported results only; refits nothing.

Locked format (instructions.md, Report Format), same axes and arrow cells as Figure 3:
  - model change (dG, dD) at the Figure 3 cell positions, locked arrows
  - the curve where democracy stops changing, with its 95% posterior band,
    drawn over the observed GDP range
  - the six representative countries: simulated paths solid with a start dot,
    observed paths faint

Reads outputs/08_model_field.csv, 08_nullcline.csv, 08_simulated_paths.csv, panel.csv.
Writes outputs/figures/fig4_model_phase_portrait.png (light and dark).
"""
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.lines import Line2D
from matplotlib.patches import Patch

from sds_common import (ARROW_LEGEND, CM, D_LABEL, G_SCALE, GDP_LABEL, OUT, REP,
                        REP_COLOUR, USD_XLIM, YEARS, dollar_axis, draw_capped_arrows,
                        load_panel, save, style)

field = pd.read_csv(OUT / "08_model_field.csv")
null = pd.read_csv(OUT / "08_nullcline.csv")
null = null[null.in_range & (null.D_star <= 1)]  # curve only where the index can be
sim = pd.read_csv(OUT / "08_simulated_paths.csv")
p = load_panel()
usd = lambda g: np.exp(G_SCALE * g)
years = np.arange(YEARS[0], YEARS[1] + 1)

for theme_name in ("light", "dark"):
    t = style(theme_name)
    fig, ax = plt.subplots(figsize=(17 * CM, 10.5 * CM))
    ink = t.text_primary
    ax.fill_between(null.usd, null.lo, null.hi, color=t.muted, alpha=0.25, lw=0, zorder=1)
    ax.plot(null.usd, null.D_star, color=t.text_secondary, lw=2.0, zorder=3)
    for iso in REP:
        c = REP_COLOUR[iso]
        o = p[p.iso3 == iso].set_index("year")[["G", "D"]].reindex(years)
        ax.plot(usd(o.G.values), o.D.values, color=c, lw=1.0, alpha=0.35, zorder=2)
        s = sim[sim.iso3 == iso]
        ax.plot(usd(s.G.values), s.D.values, color=c, lw=1.8, zorder=6)
        ax.scatter(usd(s.G.values[0]), s.D.values[0], s=28, color=c, zorder=7,
                   edgecolors=t.surface, linewidths=0.6)
    dollar_axis(ax, "x")
    ax.set_xlim(*USD_XLIM)
    ax.set_ylim(-0.05, 1.05)
    ax.set_xlabel(GDP_LABEL)
    ax.set_ylabel(D_LABEL)
    handles = [Line2D([0], [0], color=ink, lw=1.1),
               (Patch(color=t.muted, alpha=0.25, lw=0), Line2D([0], [0], color=t.text_secondary, lw=2.0)),
               Line2D([0], [0], color=t.muted, lw=1.8),
               Line2D([0], [0], color=t.muted, lw=1.0, alpha=0.35)]
    labels = [ARROW_LEGEND.replace("Mean change", "Model change"),
              "Democracy stops\nchanging (95% band)", "Simulated path", "Observed path"]
    handles += [Line2D([0], [0], color=REP_COLOUR[i], lw=1.8) for i in REP]
    labels += list(REP.values())
    ax.legend(handles, labels, loc="upper left", bbox_to_anchor=(1.02, 1.0),
              frameon=False, handlelength=1.4, borderaxespad=0.0, labelspacing=0.35)
    fig.tight_layout()
    n_capped = draw_capped_arrows(fig, ax, field.G, field.D, field.mdG, field.mdD, ink)
    if theme_name == "light":
        (OUT / "09_model_portrait_counts.txt").write_text(
            f"model arrows: {len(field)} cells; shortened to the cap: {n_capped}\n")
        print(f"capped: {n_capped} of {len(field)}")
    path = save(fig, "fig4_model_phase_portrait", theme_name)
    print(f"figure: {path}")
