"""Characterise the denominator problem: countries differ in size and in how much
forest they have, so absolute hectares of loss are not comparable across them.

Describes the candidate denominators and what each does to the data. Deliberately
does not touch GDP: the relationship is step 2's to frame and step 4's to test.

Run with:  cd Code && uv run python 03_denominator_options.py
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd

ATTACH = Path(__file__).resolve().parent.parent / "Attachments"
pd.set_option("display.width", 200)

# Drivers that represent permanent conversion out of forest, as opposed to
# rotation (Logging), natural disturbance (Wildfire, Other) or unclassified.
# Provisional, for illustration only - the scoping decision is still open.
CONVERSION_DRIVERS = ["Permanent agriculture", "Hard commodities"]


def rule(title: str) -> None:
    print(f"\n{'=' * 78}\n{title}\n{'=' * 78}")


def main() -> None:
    loss = pd.read_csv(ATTACH / "gfw_tree_cover_loss_by_driver.csv")
    extent = pd.read_csv(ATTACH / "gfw_tree_cover_extent_2000.csv")
    gdp = pd.read_csv(ATTACH / "worldbank_gdp_per_capita_ppp.csv")

    rule("1. How much countries differ, before any normalisation")
    ext = extent.groupby("iso").agg(
        extent_2000_ha=("tree_cover_extent_2000_ha", "sum"),
        area_ha=("area_ha", "sum"),
    )
    ext["forest_share_of_land"] = ext.extent_2000_ha / ext.area_ha
    tot_loss = loss.groupby("iso").tree_cover_loss_ha.sum().rename("loss_ha")
    d = ext.join(tot_loss, how="inner")

    print(f"countries with both extent and loss: {len(d)}")
    print("\nland area (ha) across countries:")
    print(d.area_ha.describe().to_string(float_format=lambda v: f"{v:,.0f}"))
    print(f"  ratio largest:smallest = {d.area_ha.max() / d.area_ha.min():,.0f} : 1")
    print("\ntree cover extent 2000 (ha) across countries:")
    print(d.extent_2000_ha.describe().to_string(float_format=lambda v: f"{v:,.0f}"))
    print("\nforest share of land area:")
    print(d.forest_share_of_land.describe().to_string(float_format=lambda v: f"{v:.4f}"))

    rule("2. The two candidate denominators are not interchangeable")
    d["loss_pct_of_forest"] = 100 * d.loss_ha / d.extent_2000_ha.where(d.extent_2000_ha > 0)
    d["loss_pct_of_land"] = 100 * d.loss_ha / d.area_ha
    sub = d[d.extent_2000_ha > 0].copy()
    print("Spearman rank correlation between the three ways of expressing loss:")
    print(sub[["loss_ha", "loss_pct_of_forest", "loss_pct_of_land"]]
          .corr(method="spearman").to_string(float_format=lambda v: f"{v:.3f}"))
    print("\nTop 10 by ABSOLUTE loss (ha):")
    print(sub.nlargest(10, "loss_ha")[["loss_ha", "extent_2000_ha",
                                       "loss_pct_of_forest"]]
          .to_string(float_format=lambda v: f"{v:,.1f}"))
    print("\nTop 10 by loss as % OF ITS OWN FOREST:")
    print(sub.nlargest(10, "loss_pct_of_forest")[["loss_pct_of_forest", "loss_ha",
                                                  "extent_2000_ha"]]
          .to_string(float_format=lambda v: f"{v:,.1f}"))

    rule("3. Why a small-forest floor is needed")
    tiny = sub[sub.extent_2000_ha < 100_000].sort_values("loss_pct_of_forest",
                                                         ascending=False)
    print(f"countries with under 100,000 ha of tree cover in 2000: {len(tiny)}")
    print("\nthe ten most extreme rates among them:")
    print(tiny.head(10)[["extent_2000_ha", "loss_ha", "loss_pct_of_forest"]]
          .to_string(float_format=lambda v: f"{v:,.1f}"))
    over = sub[sub.loss_pct_of_forest > 100]
    print(f"\ncountries whose 2001-2025 loss EXCEEDS their 2000 tree cover: {len(over)}")
    if len(over):
        print(over[["extent_2000_ha", "loss_ha", "loss_pct_of_forest"]]
              .sort_values("loss_pct_of_forest", ascending=False)
              .to_string(float_format=lambda v: f"{v:,.1f}"))

    print("\nEffect of candidate floors on sample size and on the maximum rate:")
    rows = []
    for floor in [0, 10_000, 50_000, 100_000, 500_000, 1_000_000]:
        k = sub[sub.extent_2000_ha >= floor]
        gdp_iso = set(gdp.loc[gdp.gdp_per_capita_ppp_const2021_intl_usd.notna()
                              & gdp.iso3.notna(), "iso3"])
        rows.append({
            "floor_ha": floor,
            "n_countries": len(k),
            "n_with_gdp": len(set(k.index) & gdp_iso),
            "max_rate_pct": k.loss_pct_of_forest.max(),
            "median_rate_pct": k.loss_pct_of_forest.median(),
            "share_of_global_loss": 100 * k.loss_ha.sum() / sub.loss_ha.sum(),
        })
    print(pd.DataFrame(rows).to_string(index=False,
                                       float_format=lambda v: f"{v:,.2f}"))

    rule("4. The denominator must match the numerator")
    ext_p = (extent[extent.is_primary_forest]
             .groupby("iso").tree_cover_extent_2000_ha.sum().rename("primary_extent"))
    loss_p = (loss[loss.is_primary_forest]
              .groupby("iso").tree_cover_loss_ha.sum().rename("primary_loss"))
    pf = pd.concat([ext_p, loss_p], axis=1).dropna()
    pf = pf[pf.primary_extent > 1_000_000]
    pf["primary_loss_pct"] = 100 * pf.primary_loss / pf.primary_extent
    print("If the numerator is primary-forest loss, the denominator must be primary")
    print("forest, not all tree cover. Ten largest primary-forest countries:")
    print(pf.nlargest(10, "primary_extent").to_string(
        float_format=lambda v: f"{v:,.1f}"))

    conv = (loss[loss.driver.isin(CONVERSION_DRIVERS)]
            .groupby("iso").tree_cover_loss_ha.sum().rename("conversion_loss"))
    c = ext.join(conv, how="inner")
    c = c[c.extent_2000_ha >= 100_000]
    c["conv_pct_of_forest"] = 100 * c.conversion_loss / c.extent_2000_ha
    print(f"\nProvisional conversion-only measure ({' + '.join(CONVERSION_DRIVERS)}),")
    print("countries with at least 100,000 ha tree cover, top 10 by rate:")
    print(c.nlargest(10, "conv_pct_of_forest")[["conv_pct_of_forest",
                                                "conversion_loss", "extent_2000_ha"]]
          .to_string(float_format=lambda v: f"{v:,.1f}"))
    print("\nand how that reorders the absolute-loss leaders:")
    print(c.nlargest(10, "conversion_loss")[["conversion_loss", "conv_pct_of_forest",
                                             "extent_2000_ha"]]
          .to_string(float_format=lambda v: f"{v:,.1f}"))

    rule("5. A declining denominator, if an annual rate is ever wanted")
    ann = loss.groupby(["iso", "year"]).tree_cover_loss_ha.sum().reset_index()
    ann = ann.merge(ext.reset_index()[["iso", "extent_2000_ha"]], on="iso")
    ann = ann[ann.extent_2000_ha >= 100_000].sort_values(["iso", "year"])
    ann["cum_prior"] = ann.groupby("iso").tree_cover_loss_ha.cumsum() - ann.tree_cover_loss_ha
    ann["stock_start"] = ann.extent_2000_ha - ann.cum_prior
    worst = (ann[ann.year == 2025]
             .assign(depleted=lambda x: 100 * x.cum_prior / x.extent_2000_ha)
             .nlargest(8, "depleted"))
    print("By 2025 the stock has fallen well below its 2000 value in some countries.")
    print("Share of 2000 tree cover already lost before 2025 begins, eight largest:")
    print(worst[["iso", "extent_2000_ha", "cum_prior", "depleted"]]
          .to_string(index=False, float_format=lambda v: f"{v:,.1f}"))
    print("\nHolding the denominator at its 2000 value understates later-year rates")
    print("by roughly that share.")


if __name__ == "__main__":
    main()
