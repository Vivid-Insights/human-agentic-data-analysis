"""Figure 3 — annual permanent conversion in the eight cases, 2001-2024.

Sub-question 3, shown before any trend is fitted. Eight panels, one per country,
ordered by mean income so that income is the direction the reader's eye travels.

Each year is drawn as its own bar rather than as a point on a connected line.
Hansen allocates loss to years by heuristic, so the path between two years is not
something the data establishes; a line would assert it. A bar says how much was
assigned to that year and claims nothing about the way in or out.

The panels share a y-axis. The eight differ by roughly a factor of five in how
much they cleared, and separate scales would make a country clearing a fifth as
fast look the same as one clearing fastest.

No trend line. The trend is sub-question 3's answer and step 4 estimates it.

Reads  outputs/annual_cases.csv
Writes outputs/figures/fig3_annual_cases.png  (and dark/)
"""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.ticker import FixedLocator

import viz_style as vs

HERE = Path(__file__).resolve().parent
DATA = HERE / "outputs" / "annual_cases.csv"

NCOLS, NROWS = 4, 2
XTICKS = [2001, 2008, 2016, 2024]

HEADLINE = "Annual permanent forest conversion in eight countries, 2001–2024"
XLABEL = "Year"
YLABEL = "Share of year-2000 forest\nconverted in the year"
SOURCE = (
    "Panels in order of mean GDP per capita 2001–2024, lowest first. The eight countries are "
    "the two with the highest cumulative permanent conversion in each World Bank income group, "
    "fixed before any trend was examined. Each bar is one year's loss attributed to permanent "
    "agriculture, hard commodities, or settlements and infrastructure, divided by that country's "
    "year-2000 tree cover. Sources: Global Forest Watch / WRI and Google DeepMind drivers v1.3; "
    "World Bank World Development Indicators."
)

# Income group as it appears in the data, shortened for a panel title.
SHORT = {"Low income": "low income", "Lower middle income": "lower-middle income",
         "Upper middle income": "upper-middle income", "High income": "high income"}


def draw(d: pd.DataFrame, theme_name: str) -> None:
    t = vs.use(theme_name)
    fig, axes = plt.subplots(NROWS, NCOLS, figsize=(13.0, 6.6),
                             sharex=True, sharey=True)
    flat = axes.ravel()

    order = (d.drop_duplicates("iso3").sort_values("gdp_pc_mean")["iso3"].tolist())
    ymax = d.annual_permanent_rate.max()

    for ax, iso in zip(flat, order):
        c = d[d.iso3 == iso].sort_values("year")
        name = c.country.iloc[0]
        ax.bar(c.year, c.annual_permanent_rate, width=0.78,
               color=t.series[0], linewidth=0, zorder=3)
        ax.set_title(f"{name} · {SHORT[c.income_group.iloc[0]]}",
                     fontsize=13, color=t.text_primary, pad=8)
        ax.set_xlim(2000.2, 2024.8)
        ax.set_ylim(0, ymax * 1.08)
        ax.xaxis.set_major_locator(FixedLocator(XTICKS))
        ax.tick_params(labelsize=12)
        # Vertical gridlines would read as year dividers between the bars.
        ax.grid(axis="x", visible=False)

    for ax in axes[:, 0]:
        ax.set_ylabel(YLABEL, fontsize=13)

    vs.header(fig, HEADLINE)
    vs.source_note(fig, SOURCE)

    lines = getattr(fig, "_source_lines", 1)
    note_h = 0.012 + lines * (vs.SOURCE_SIZE * 1.35 / 72) / fig.get_figheight()
    label_y = note_h + 0.016
    fig.text(0.5, label_y, XLABEL, ha="center", va="bottom",
             fontsize=14, color=t.text_secondary)
    fig.tight_layout(rect=(0, label_y + 0.05, 1, 0.93))

    vs.save(fig, "fig3_annual_cases")


def main() -> None:
    d = pd.read_csv(DATA)
    print(f"  {d.iso3.nunique()} countries x {d.year.nunique()} years = {len(d)} rows")
    print(f"  shared y-axis ceiling from the maximum annual rate: "
          f"{d.annual_permanent_rate.max():.4f}")
    for theme_name in ("light", "dark"):
        draw(d, theme_name)


if __name__ == "__main__":
    main()
