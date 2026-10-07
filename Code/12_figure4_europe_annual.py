"""Figure 4 — annual tree cover loss in four European countries.

Sub-question 2 compares the two outcomes across countries. This shows what that
loss looks like inside a country over time, for four European cases.

The four countries are named by the user. They are not a sample, not positions in
a distribution, and not the result of any rule, and nothing here should be read as
representative of Europe. The appendix says the same.

Only total loss is drawn, in the orange that outcome carries in Figure 2. The
permanent part is small in all four — a few percent of what each lost — so a
second bar in front of it showed nothing; the cumulative figures are printed by
this script and quoted in the caption instead.

All four panels share a ceiling of 0.04 so that bar heights are comparable.
Portugal runs past it in three years. Those bars are clipped and carry a break
mark, which is what tells a reader the bar continues; their values go in the
caption rather than inside the frame.

Reads  outputs/analysis_dataset.csv
       ../Attachments/gfw_tree_cover_loss_by_driver.csv
Writes outputs/europe_cases.csv
       outputs/figures/fig4_europe_annual.png  (and dark/)
"""

from __future__ import annotations

import importlib
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.ticker import FixedLocator

import viz_style as vs

HERE = Path(__file__).resolve().parent
ATTACH = HERE.parent / "Attachments"
OUT = HERE / "outputs"

_build = importlib.import_module("07_build_analysis_dataset")
PERMANENT: list[str] = _build.PERMANENT
Y0: int = _build.Y0
Y1: int = _build.Y1

# Named by the user, in the order they appear. No rule selects these and none is
# implied: change the list and the figure changes, with nothing else to update.
CASES = ["DEU", "ESP", "SWE", "PRT"]

XTICKS = [2001, 2008, 2016, 2024]
# Fixed rather than derived, so the scale is stable across rebuilds. Bars above it
# are clipped and marked; see break_mark.
Y_MAX = 0.04

HEADLINE = "Annual tree cover loss in four European countries, 2001–2024"
XLABEL = "Year"
YLABEL = "Share of year-2000 forest\nlost in the year"
SOURCE = (
    "Four countries, named rather than sampled: they are not representative of Europe and no "
    "rule selects them. Bars are tree cover loss from all eight driver classes, as a share of "
    "each country's own year-2000 tree cover. A break across a bar means it continues past the "
    "top of the scale. Sources: Global Forest Watch / WRI and Google DeepMind drivers v1.3; "
    "World Bank World Development Indicators."
)


def annual(cases: pd.DataFrame) -> pd.DataFrame:
    loss = pd.read_csv(ATTACH / "gfw_tree_cover_loss_by_driver.csv")
    w = loss[loss.year.between(Y0, Y1) & loss.iso.isin(cases.iso3)]
    tot = w.groupby(["iso", "year"])["tree_cover_loss_ha"].sum().rename("total_ha")
    per = (w[w.driver.isin(PERMANENT)].groupby(["iso", "year"])["tree_cover_loss_ha"]
           .sum().rename("permanent_ha"))
    grid = pd.MultiIndex.from_product([sorted(cases.iso3), range(Y0, Y1 + 1)],
                                      names=["iso", "year"])
    a = pd.concat([tot, per], axis=1).reindex(grid).fillna(0.0).reset_index()
    a = a.rename(columns={"iso": "iso3"}).merge(
        cases[["iso3", "country", "extent_2000_ha",
               "total_loss_share", "permanent_loss_share"]], on="iso3")
    a["total_rate"] = a.total_ha / a.extent_2000_ha
    a["permanent_rate"] = a.permanent_ha / a.extent_2000_ha

    for rate, cum in [("total_rate", "total_loss_share"),
                      ("permanent_rate", "permanent_loss_share")]:
        diff = (a.groupby("iso3")[rate].sum() - a.groupby("iso3")[cum].first()).abs()
        assert diff.max() < 1e-9, f"{rate} does not decompose {cum}"
        print(f"  {rate} sums to {cum}: max |difference| {diff.max():.2e}")
    assert (a.permanent_rate <= a.total_rate + 1e-12).all(), "permanent exceeds total"
    return a


def break_mark(ax, x: float, width: float, t) -> None:
    """Mark a bar as continuing past the top of the axis.

    Two surface-coloured bands cut across the bar with a muted rule along each, so
    the bar reads as severed rather than as ending. Drawn above the bar and kept
    clear of the axis top, so the bar is visibly still rising as it leaves frame.
    """
    y = Y_MAX * 0.88
    h = Y_MAX * 0.020
    over = width * 0.62
    for dy in (0.0, h * 2.2):
        ax.fill_between([x - over, x + over], y + dy, y + dy + h,
                        color=t.surface, lw=0, zorder=6)
        ax.plot([x - over, x + over], [y + dy, y + dy + h],
                color=t.muted, lw=1.0, zorder=7, solid_capstyle="butt")


def draw(a: pd.DataFrame, cases: pd.DataFrame, theme_name: str) -> None:
    t = vs.use(theme_name)
    fig, axes = plt.subplots(1, 4, figsize=(13.4, 4.6), sharex=True, sharey=True)

    for ax, iso in zip(axes, cases.iso3):
        c = a[a.iso3 == iso].sort_values("year")
        name = cases.loc[cases.iso3 == iso, "country"].iloc[0]
        ax.bar(c.year, c.total_rate, width=0.78, color=t.series[1],
               linewidth=0, zorder=3)
        ax.set_title(name, fontsize=14, color=t.text_primary, pad=8)
        ax.set_xlim(2000.2, 2024.8)
        ax.set_ylim(0, Y_MAX)
        ax.xaxis.set_major_locator(FixedLocator(XTICKS))
        ax.tick_params(labelsize=12)
        ax.grid(axis="x", visible=False)
        for _, r in c[c.total_rate > Y_MAX].iterrows():
            break_mark(ax, r.year, 0.78, t)

    axes[0].set_ylabel(YLABEL, fontsize=13)

    vs.header(fig, HEADLINE)
    vs.source_note(fig, SOURCE)
    lines = getattr(fig, "_source_lines", 1)
    note_h = 0.012 + lines * (vs.SOURCE_SIZE * 1.35 / 72) / fig.get_figheight()
    label_y = note_h + 0.02
    fig.text(0.5, label_y, XLABEL, ha="center", va="bottom",
             fontsize=14, color=t.text_secondary)
    fig.tight_layout(rect=(0, label_y + 0.07, 1, 0.91))
    vs.save(fig, "fig4_europe_annual")


def main() -> None:
    d = pd.read_csv(OUT / "analysis_dataset.csv")
    missing = [i for i in CASES if i not in set(d.iso3)]
    assert not missing, f"not in the sample: {missing}"
    cases = d[d.iso3.isin(CASES)].set_index("iso3").loc[CASES].reset_index()
    cases.to_csv(OUT / "europe_cases.csv", index=False)

    a = annual(cases)
    print(f"  fixed y ceiling {Y_MAX}")
    print("  cumulative 2001-2024, permanent as a share of all tree cover loss:")
    for _, r in cases.iterrows():
        print(f"    {r.country:<16} permanent {r.permanent_loss_share:.4f}"
              f"  all {r.total_loss_share:.4f}"
              f"  permanent/all {r.permanent_loss_share / r.total_loss_share:.3f}")
    over = a[a.total_rate > Y_MAX].sort_values(["country", "year"])
    print(f"  bars past the {Y_MAX} ceiling: {len(over)}")
    for _, r in over.iterrows():
        print(f"    {r.country} {int(r.year)}  {r.total_rate:.4f}")

    for theme_name in ("light", "dark"):
        draw(a, cases, theme_name)


if __name__ == "__main__":
    main()
