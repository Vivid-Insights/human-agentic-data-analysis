"""Figure 5: does the 1981-2006 model predict 2007-2024? Reads exported results only.

Locked format (sds_common), same GDP axis as Figures 2-4; democracy is the V-Dem
electoral democracy index. For the six representative countries, from their 2006
state: observed path to 2024 (solid) and the path predicted by the V-Dem model fitted
to 1981-2006 (dashed: the dash marks a prediction). The V-Dem democracy nullcline from
the 1981-2006 fit in light grey with its 95% band.

Reads outputs/13_predicted_paths.csv, 08_nullcline_vdem.csv.
Writes outputs/figures/fig5_prediction.png (light and dark).
"""
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.lines import Line2D
from matplotlib.patches import Patch

from sds_common import (CM, G_SCALE, GDP_LABEL, OUT, REP, REP_COLOUR, USD_XLIM,
                        dollar_axis, save, style)

paths = pd.read_csv(OUT / "13_predicted_paths.csv")
null = pd.read_csv(OUT / "08_nullcline_vdem.csv")
null = null[null.in_range & (null.D_star <= 1)]
usd = lambda g: np.exp(G_SCALE * g)

for theme_name in ("light", "dark"):
    t = style(theme_name)
    fig, ax = plt.subplots(figsize=(17 * CM, 10.5 * CM))
    ax.fill_between(null.usd, null.lo, null.hi, color=t.muted, alpha=0.15, lw=0, zorder=1)
    ax.plot(null.usd, null.D_star, color=t.muted, lw=2.0, zorder=2)
    for iso in REP:
        c = REP_COLOUR[iso]
        o = paths[(paths.iso3 == iso) & (paths.kind == "observed")].sort_values("year")
        s = paths[(paths.iso3 == iso) & (paths.kind == "simulated")].sort_values("year")
        ax.plot(usd(o.G), o.D, color=c, lw=1.8, zorder=4)
        ax.plot(usd(s.G), s.D, color=c, lw=1.8, ls=(0, (3, 2)), zorder=5)
        ax.scatter(usd(o.G.iloc[0]), o.D.iloc[0], s=28, color=c, zorder=6,
                   edgecolors=t.surface, linewidths=0.6)
    dollar_axis(ax, "x")
    ax.set_xlim(*USD_XLIM)
    ax.set_ylim(-0.05, 1.05)
    ax.set_xlabel(GDP_LABEL)
    ax.set_ylabel("Electoral democracy (V-Dem index, 0 to 1)")
    handles = [Line2D([0], [0], color=t.text_secondary, lw=1.8),
               Line2D([0], [0], color=t.text_secondary, lw=1.8, ls=(0, (3, 2))),
               (Patch(color=t.muted, alpha=0.15, lw=0), Line2D([0], [0], color=t.muted, lw=2.0))]
    labels = ["Observed", "Predicted", "Nullcline,\n1981–2006"]
    handles += [Line2D([0], [0], color=REP_COLOUR[i], lw=1.8) for i in REP]
    labels += list(REP.values())
    ax.legend(handles, labels, loc="upper left", bbox_to_anchor=(1.02, 1.0), frameon=False,
              handlelength=1.6, borderaxespad=0.0, labelspacing=0.35)
    fig.tight_layout()
    path = save(fig, "fig5_prediction", theme_name)
    print(f"figure: {path}")
