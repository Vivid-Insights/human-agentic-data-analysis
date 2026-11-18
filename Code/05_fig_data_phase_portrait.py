"""Figure 3: the data phase portrait.

The observed yearly changes, averaged within cells of a grid over the state
(G, D). Each arrow starts at the mean state of the observations in its cell and
points along their mean change (dG, dD), multiplied by K years, so an arrow shows
where a country starting there would be after K years at that average rate. Both
components are scaled by the same K in model units, so arrow directions are true
on these axes. Cells with fewer than MIN_N changes are left empty. The six
representative countries' paths are drawn thinly in their fixed colours.

Locked format: GDP per capita in constant 2015 US$ on a log axis (position is
linear in G), democracy as an index 0 to 1, the six-colour palette, legend off
the data.

Reads Code/outputs/panel.csv. Writes outputs/figures/fig3_data_phase_portrait.png
(light and dark), outputs/05_phase_cells.csv and outputs/05_phase_portrait_counts.txt.
"""
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.lines import Line2D

from sds_common import (CM, D_LABEL, G_SCALE, GDP_LABEL, OUT, REP, REP_COLOUR,
                        YEARS, USD_XLIM, dollar_axis, load_panel, save, style)

LENGTH = 2 / 3  # user: two thirds of the 5-year, 0.7 cm version (locked format)
K = 5 * LENGTH  # arrow = average yearly change x K years (3 1/3)
CAP_CM = 0.7 * LENGTH  # maximum drawn arrow length, cm on the page (~ one grid cell); longer
               # arrows are shortened to this length with their direction unchanged
MIN_N = 10     # minimum observed changes for a cell to get an arrow
G_EDGES = np.arange(0.42, 1.00 + 1e-9, 0.04)   # G = ln(GDP)/12; 0.04 in G = x1.62 in GDP
D_EDGES = np.linspace(0.0, 1.0, 11)            # 0.1 in democracy

p = load_panel()
ch = p.dropna(subset=["dD", "dG"]).copy()
ch["g_bin"] = pd.cut(ch.G, G_EDGES, include_lowest=True)
ch["d_bin"] = pd.cut(ch.D, D_EDGES, include_lowest=True)
cells = (ch.groupby(["g_bin", "d_bin"], observed=True)
           .agg(n=("dD", "size"), G=("G", "mean"), D=("D", "mean"),
                dG=("dG", "mean"), dD=("dD", "mean"))
           .reset_index())
shown = cells[cells.n >= MIN_N].copy()

usd = lambda g: np.exp(G_SCALE * g)
years = np.arange(YEARS[0], YEARS[1] + 1)

counts = [
    f"changes used: {len(ch)}",
    f"grid: {len(G_EDGES)-1} G bins of 0.04 x {len(D_EDGES)-1} D bins of 0.1",
    f"occupied cells: {len(cells)}; cells with >= {MIN_N} changes (arrows): {len(shown)}",
    f"changes in cells with arrows: {int(shown.n.sum())} of {len(ch)}",
    f"arrow scale K = {K:.4f} years",
    f"mean yearly dD over all changes: {ch.dD.mean():.4f}; mean yearly dG: {ch.dG.mean():.5f}"
    f" (= {100*(np.exp(G_SCALE*ch.dG.mean())-1):.2f}% GDP growth per year)",
]
(OUT / "05_phase_portrait_counts.txt").write_text("\n".join(counts) + "\n")
shown.assign(g_bin=shown.g_bin.astype(str), d_bin=shown.d_bin.astype(str)) \
     .to_csv(OUT / "05_phase_cells.csv", index=False)
print("\n".join(counts))

for theme_name in ("light", "dark"):
    t = style(theme_name)
    fig, ax = plt.subplots(figsize=(17 * CM, 10.5 * CM))
    for iso, name in REP.items():
        s = p[p.iso3 == iso].set_index("year")[["G", "D"]].reindex(years)
        ax.plot(usd(s.G.values), s.D.values, color=REP_COLOUR[iso], lw=1.0,
                alpha=0.55, label=name, zorder=2)
    arrow_col = t.text_primary
    dollar_axis(ax, "x")
    ax.set_xlim(*USD_XLIM)
    ax.set_ylim(-0.05, 1.05)
    ax.set_xlabel(GDP_LABEL)
    ax.set_ylabel(D_LABEL)
    handles, labels = ax.get_legend_handles_labels()
    handles = [Line2D([0], [0], color=arrow_col, lw=1.1)] + handles
    labels = ["Mean change,\n3⅓ years (capped)"] + labels
    ax.legend(handles, labels, loc="upper left", bbox_to_anchor=(1.02, 1.0),
              frameon=False, handlelength=1.4, borderaxespad=0.0)
    fig.tight_layout()

    # Arrows are drawn after layout so the cap can be applied in cm on the page.
    # The x axis is linear in G (log dollars), so scaling (dG, dD) by one factor
    # leaves the direction on the page unchanged.
    bb = ax.get_window_extent().transformed(fig.dpi_scale_trans.inverted())
    w_cm, h_cm = bb.width / CM, bb.height / CM
    gx0, gx1 = np.log(USD_XLIM) / G_SCALE
    (dy0, dy1) = ax.get_ylim()
    n_capped = 0
    for r in shown.itertuples():
        vx_cm = K * r.dG / (gx1 - gx0) * w_cm
        vy_cm = K * r.dD / (dy1 - dy0) * h_cm
        length = np.hypot(vx_cm, vy_cm)
        f = min(1.0, CAP_CM / length) if length > 0 else 1.0
        n_capped += f < 1.0
        x0, y0 = usd(r.G), r.D
        x1, y1 = usd(r.G + f * K * r.dG), r.D + f * K * r.dD
        ax.annotate("", xy=(x1, y1), xytext=(x0, y0), zorder=4,
                    arrowprops=dict(arrowstyle="-|>", color=arrow_col, lw=1.1,
                                    mutation_scale=7, shrinkA=0, shrinkB=0))
        ax.scatter([x0], [y0], s=6, color=arrow_col, zorder=5, lw=0)
    if theme_name == "light":
        with open(OUT / "05_phase_portrait_counts.txt", "a") as fh:
            fh.write(f"arrow cap: {CAP_CM:.3f} cm on the page; arrows shortened to the cap: "
                     f"{int(n_capped)} of {len(shown)}\n")
        print(f"capped: {int(n_capped)} of {len(shown)}")
    path = save(fig, "fig3_data_phase_portrait", theme_name)
    print(f"figure: {path}")
