"""Step 2 feasibility check. Counts only: how many countries fall in each region and
income group after the 100,000 ha forest floor, and how complete the GDP series is.

Deliberately reports no relationship between forest loss and income. The question is
being framed here; testing it is steps 3 and 4. Marginal distributions of each variable
are described separately and are never crossed.

Run with:  cd Code && uv run python 04_feasibility.py
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd

ATTACH = Path(__file__).resolve().parent.parent / "Attachments"
pd.set_option("display.width", 200)

FOREST_FLOOR_HA = 100_000  # decided in step 1


def rule(title: str) -> None:
    print(f"\n{'=' * 78}\n{title}\n{'=' * 78}")


def main() -> None:
    extent = pd.read_csv(ATTACH / "gfw_tree_cover_extent_2000.csv")
    gdp = pd.read_csv(ATTACH / "worldbank_gdp_per_capita_ppp.csv")
    meta = pd.read_csv(ATTACH / "worldbank_country_metadata.csv")

    ext = extent.groupby("iso").tree_cover_extent_2000_ha.sum()
    eligible = set(ext[ext >= FOREST_FLOOR_HA].index)

    countries = meta[meta.region != "Aggregates"].copy()
    gdp_any = set(gdp.loc[gdp.gdp_per_capita_ppp_const2021_intl_usd.notna()
                          & gdp.iso3.notna(), "iso3"])

    rule("1. Sample after the 100,000 ha forest floor")
    print(f"countries meeting the floor:        {len(eligible)}")
    print(f"of those, with at least one GDP:    {len(eligible & gdp_any)}")

    sample = countries[countries.iso3.isin(eligible & gdp_any)].copy()
    print(f"of those, non-aggregate in WB meta: {len(sample)}")

    rule("2. Sample by World Bank region")
    print(sample.region.value_counts().to_string())

    rule("3. Sample by World Bank income group")
    order = ["Low income", "Lower middle income", "Upper middle income", "High income"]
    print(sample.income_group.value_counts().reindex(order).to_string())

    rule("4. The European sub-sample")
    eur = sample[sample.region == "Europe & Central Asia"].sort_values("country")
    print(f"'Europe & Central Asia' countries meeting the floor: {len(eur)}")
    print("\nthis region mixes western Europe with central Asia:")
    print(eur[["iso3", "country", "income_group"]].to_string(index=False))

    rule("5. GDP series completeness over the loss window, sample countries only")
    g = gdp[gdp.iso3.isin(sample.iso3) & gdp.year.between(2001, 2025)]
    have = g[g.gdp_per_capita_ppp_const2021_intl_usd.notna()]
    per_country = have.groupby("iso3").size()
    print(f"countries with all 25 years present: {(per_country == 25).sum()}")
    print(f"countries with 20-24 years:          {per_country.between(20, 24).sum()}")
    print(f"countries with under 20 years:       {(per_country < 20).sum()}")
    short = per_country[per_country < 25].sort_values()
    if len(short):
        print("\ncountries with an incomplete series:")
        print(short.to_string())

    rule("6. Spread of income in the sample, single variable only")
    latest = (have.sort_values("year").groupby("iso3").tail(1)
              .set_index("iso3").gdp_per_capita_ppp_const2021_intl_usd)
    print(f"most recent GDP per capita available per country, n = {len(latest)}")
    print(latest.describe().to_string(float_format=lambda v: f"{v:,.0f}"))
    import numpy as np
    print(f"\nrange in logs: {np.log(latest.min()):.2f} to {np.log(latest.max()):.2f} "
          f"({np.log(latest.max()) - np.log(latest.min()):.2f} log points, "
          f"a {latest.max() / latest.min():,.0f}-fold span)")
    print("\ncount by order of magnitude (int'l $ per person):")
    bins = [0, 2_000, 5_000, 10_000, 20_000, 40_000, 1_000_000]
    labels = ["<2k", "2-5k", "5-10k", "10-20k", "20-40k", ">40k"]
    print(pd.cut(latest, bins=bins, labels=labels).value_counts()
          .reindex(labels).to_string())

    rule("7. Income growth over the window, single variable only")
    first = (have[have.year == 2001].set_index("iso3")
             .gdp_per_capita_ppp_const2021_intl_usd)
    last = (have[have.year == 2024].set_index("iso3")
            .gdp_per_capita_ppp_const2021_intl_usd)
    both = pd.concat([first.rename("y2001"), last.rename("y2024")], axis=1).dropna()
    both["log_change"] = np.log(both.y2024) - np.log(both.y2001)
    print(f"countries with both 2001 and 2024 GDP: {len(both)}")
    print("\nchange in log GDP per capita, 2001 to 2024:")
    print(both.log_change.describe().to_string(float_format=lambda v: f"{v:.3f}"))
    print(f"\ncountries whose real GDP per capita fell: {(both.log_change < 0).sum()}")
    print("This is the variation any within-country test would have to work with.")


if __name__ == "__main__":
    main()
