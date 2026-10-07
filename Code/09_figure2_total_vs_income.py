"""Figure 2 — the two outcomes against income, side by side on a shared scale.

Sub-question 2 asks whether the shape found for permanent conversion survives
when the outcome is all tree cover loss however caused. Half of that question is
the comparison with sub-question 1, so the two outcomes are drawn as panels of
one figure sharing a y-axis: a shape read off the left panel and a shape read
off the right are then being read on the same ruler.

Permanent conversion keeps the blue it has in Figure 1 and total loss takes
orange. The colour belongs to the variable, so the pair reads the same way
wherever either appears again.

Observations only. No curve is fitted — that is step 4's.

Reads  outputs/analysis_dataset.csv
Writes outputs/figures/fig2_outcomes_vs_income{,_logy}.png  (and dark/)
"""

from __future__ import annotations

import importlib
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.ticker import FixedLocator, FuncFormatter, NullLocator

import viz_style as vs

# The thresholds come from the model script rather than being restated here, so
# the line in the figure cannot drift from the cut the model actually used.
_model = importlib.import_module("13_model_threshold")
THRESHOLDS = {col: thr for _, col, thr, _ in _model.SPECS}

CODE_DIR = Path(__file__).resolve().parent
DATA = CODE_DIR / "outputs" / "analysis_dataset.csv"

XCOL, NAMECOL = "gdp_pc_mean", "country"
# (column, panel title, index into the shared palette)
PANELS = [
    ("permanent_loss_share", "Permanent conversion only", 0),
    ("total_loss_share", "All tree cover loss", 1),
]

XTICKS = [1_000, 3_000, 10_000, 30_000, 100_000]

HEADLINE = "Two measures of forest loss against income, 2001–2024"
XLABEL = "GDP per capita, PPP (constant 2021 international $), mean 2001–2024"
YLABEL = "Share of year-2000 forest lost"
SOURCE = (
    "Each point is one of 135 countries with at least 100,000 ha of tree cover in 2000. "
    "Left: loss attributed to permanent agriculture, hard commodities, or settlements and "
    "infrastructure. Right: loss from all eight driver classes. Both panels share the same "
    "axes and divide by the same year-2000 tree cover. The horizontal line in each panel is the "
    "threshold used by that panel's model. Sources: Global Forest Watch / WRI "
    "and Google DeepMind drivers v1.3; World Bank World Development Indicators."
)


def draw(d: pd.DataFrame, theme_name: str, logy: bool) -> None:
    t = vs.use(theme_name)
    fig, axes = plt.subplots(1, 2, figsize=(12.0, 6.0), sharex=True, sharey=True)

    ymax = max(d[c].max() for c, _, _ in PANELS)
    ymin = min(d[c].min() for c, _, _ in PANELS)

    for ax, (ycol, title, ci) in zip(axes, PANELS):
        ax.scatter(d[XCOL], d[ycol], s=40, color=t.series[ci], alpha=0.78,
                   edgecolors=t.surface, linewidths=0.6, zorder=3)
        ax.set_title(title, fontsize=15, color=t.text_primary, pad=10)
        # Reference line, not a data series: drawn in ink rather than in either
        # outcome's colour, and behind the points, so it cannot read as a third
        # variable. Each panel carries its own model's threshold.
        thr = THRESHOLDS[ycol]
        ax.axhline(thr, color=t.text_secondary, lw=1.2, zorder=2)
        ax.annotate(f"{thr:g}", (1.0, thr), xycoords=("axes fraction", "data"),
                    xytext=(-3, 3), textcoords="offset points", ha="right", va="bottom",
                    fontsize=12, color=t.text_secondary, zorder=5)

        ax.set_xscale("log")
        ax.xaxis.set_major_locator(FixedLocator(XTICKS))
        ax.xaxis.set_minor_locator(NullLocator())
        ax.xaxis.set_major_formatter(FuncFormatter(lambda v, _: f"{v:,.0f}"))
        ax.set_xlim(d[XCOL].min() / 1.35, d[XCOL].max() * 1.35)

        if logy:
            ax.set_yscale("log")
            ax.set_ylim(ymin / 1.7, ymax * 1.7)
            ax.yaxis.set_major_locator(FixedLocator([0.001, 0.01, 0.1]))
            ax.yaxis.set_minor_locator(NullLocator())
            ax.yaxis.set_major_formatter(FuncFormatter(lambda v, _: f"{v:g}"))
        else:
            ax.set_ylim(0, ymax * 1.08)

        # Only the outcome extremes. The income extremes are the same two points
        # in both panels, so labelling them here would say it four times.
        rows = [("min_y", d.nsmallest(1, ycol).iloc[0]),
                ("max_y", d.nlargest(1, ycol).iloc[0])]
        vs.label_extremes(ax, rows, XCOL, ycol, lambda r: r[NAMECOL])

    axes[0].set_ylabel(YLABEL)

    vs.header(fig, HEADLINE)
    vs.source_note(fig, SOURCE)

    # One x-label serves both panels, so it is placed on the figure rather than
    # on an axis. vs.layout() reserves room for the source note only, and a
    # figure-level label at a fixed offset lands on top of it; the band the note
    # occupies is measured here and the label sits immediately above it.
    lines = getattr(fig, "_source_lines", 1)
    note_h = 0.012 + lines * (vs.SOURCE_SIZE * 1.35 / 72) / fig.get_figheight()
    label_y = note_h + 0.018
    fig.text(0.5, label_y, XLABEL, ha="center", va="bottom",
             fontsize=15, color=t.text_secondary)
    fig.tight_layout(rect=(0, label_y + 0.055, 1, 0.92))

    vs.save(fig, "fig2_outcomes_vs_income" + ("_logy" if logy else ""))


def main() -> None:
    d = pd.read_csv(DATA)
    print(f"  {len(d)} countries read from {DATA.name}")
    for ycol, title, _ in PANELS:
        lo, hi = d.nsmallest(1, ycol).iloc[0], d.nlargest(1, ycol).iloc[0]
        print(f"  {title}: {lo[NAMECOL]} {lo[ycol]:.4f} to {hi[NAMECOL]} {hi[ycol]:.4f}")
    for logy in (False, True):
        for theme_name in ("light", "dark"):
            draw(d, theme_name, logy)


if __name__ == "__main__":
    main()
