"""Build the analysis dataset: one row per country, from the four source files.

This is the only dataset the analysis uses. Every later script reads this file and
nothing else, so the sample definition lives in exactly one place.

Sample rule, all decided in steps 1 and 2:
  - at least 100,000 ha of tree cover in 2000 (canopy density >= 30%)
  - a non-aggregate country in the World Bank metadata
  - at least one GDP per capita observation in 2001-2024

Run with:  cd Code && uv run python 07_build_analysis_dataset.py
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
ATTACH = HERE.parent / "Attachments"
OUT = HERE / "outputs"

FOREST_FLOOR_HA = 100_000
Y0, Y1 = 2001, 2024

PERMANENT = ["Permanent agriculture", "Hard commodities", "Settlements & Infrastructure"]
SHIFTING = ["Shifting cultivation"]


def main() -> None:
    OUT.mkdir(exist_ok=True)

    loss = pd.read_csv(ATTACH / "gfw_tree_cover_loss_by_driver.csv")
    extent = pd.read_csv(ATTACH / "gfw_tree_cover_extent_2000.csv")
    gdp = pd.read_csv(ATTACH / "worldbank_gdp_per_capita_ppp.csv")
    meta = pd.read_csv(ATTACH / "worldbank_country_metadata.csv")

    # --- denominator ---------------------------------------------------------
    ext = extent.groupby("iso").tree_cover_extent_2000_ha.sum().rename("extent_2000_ha")

    # --- numerators, restricted to the analysis window -----------------------
    w = loss[loss.year.between(Y0, Y1)]
    agg = w.groupby("iso").apply(lambda g: pd.Series({
        "permanent_loss_ha": g.loc[g.driver.isin(PERMANENT), "tree_cover_loss_ha"].sum(),
        "shifting_loss_ha": g.loc[g.driver.isin(SHIFTING), "tree_cover_loss_ha"].sum(),
        "total_loss_ha": g.tree_cover_loss_ha.sum(),
    }), include_groups=False)

    # --- income --------------------------------------------------------------
    gw = gdp[gdp.year.between(Y0, Y1) & gdp.gdp_per_capita_ppp_const2021_intl_usd.notna()]
    inc = gw.groupby("iso3").gdp_per_capita_ppp_const2021_intl_usd.agg(
        gdp_pc_mean="mean",
        gdp_pc_geomean=lambda v: float(np.exp(np.log(v).mean())),
        gdp_pc_first="first",
        gdp_pc_last="last",
        gdp_years_used="size",
    )

    countries = (meta[meta.region != "Aggregates"]
                 .set_index("iso3")[["country", "income_group"]])

    d = (countries
         .join(ext, how="inner")
         .join(agg, how="inner")
         .join(inc, how="inner"))
    d.index.name = "iso3"

    before = len(d)
    d = d[d.extent_2000_ha >= FOREST_FLOOR_HA].copy()

    # --- outcome variables ---------------------------------------------------
    d["permanent_loss_share"] = d.permanent_loss_ha / d.extent_2000_ha
    d["total_loss_share"] = d.total_loss_ha / d.extent_2000_ha
    d["permanent_plus_shifting_share"] = (
        (d.permanent_loss_ha + d.shifting_loss_ha) / d.extent_2000_ha)
    d["log_gdp_pc_mean"] = np.log(d.gdp_pc_mean)

    d = d.sort_index()
    cols = ["country", "income_group", "extent_2000_ha",
            "permanent_loss_ha", "shifting_loss_ha", "total_loss_ha",
            "permanent_loss_share", "total_loss_share",
            "permanent_plus_shifting_share",
            "gdp_pc_mean", "gdp_pc_geomean", "log_gdp_pc_mean", "gdp_years_used"]
    d[cols].to_csv(OUT / "analysis_dataset.csv", float_format="%.10g")

    # --- report --------------------------------------------------------------
    print(f"countries with metadata, extent, loss and GDP : {before}")
    print(f"after the {FOREST_FLOOR_HA:,} ha forest floor        : {len(d)}")
    print(f"\nwritten: {OUT / 'analysis_dataset.csv'}")

    print("\n--- sample by income group ---")
    order = ["Low income", "Lower middle income", "Upper middle income", "High income"]
    print(d.income_group.value_counts().reindex(order).to_string())

    print("\n--- the variables ---")
    v = ["permanent_loss_share", "total_loss_share",
         "permanent_plus_shifting_share", "gdp_pc_mean", "log_gdp_pc_mean"]
    print(d[v].describe().T.to_string(float_format=lambda x: f"{x:,.4f}"))

    print("\n--- integrity checks ---")
    print(f"any share above 1                     : {(d[['permanent_loss_share', 'total_loss_share']] > 1).any().any()}")
    print(f"any share below 0                     : {(d[['permanent_loss_share', 'total_loss_share']] < 0).any().any()}")
    print(f"permanent exceeds total anywhere      : {(d.permanent_loss_ha > d.total_loss_ha).sum()}")
    print(f"any missing value in the used columns : {d[cols].isna().sum().sum()}")
    print(f"countries with fewer than 24 GDP years: {(d.gdp_years_used < 24).sum()}")
    print(f"arithmetic vs geometric mean income, Spearman: "
          f"{d.gdp_pc_mean.corr(d.gdp_pc_geomean, method='spearman'):.6f}")
    print(f"max relative gap between the two means: "
          f"{((d.gdp_pc_mean - d.gdp_pc_geomean) / d.gdp_pc_mean).max():.4f}")

    print("\n--- H3 cases: top two by permanent_loss_share within each income group ---")
    cases = (d.reset_index().sort_values("permanent_loss_share", ascending=False)
             .groupby("income_group").head(2)
             .sort_values(["income_group", "permanent_loss_share"], ascending=[True, False]))
    print(cases[["iso3", "country", "income_group", "permanent_loss_share",
                 "gdp_pc_mean"]].to_string(index=False,
                                           float_format=lambda x: f"{x:,.4f}"))
    cases[["iso3", "country", "income_group", "permanent_loss_share"]].to_csv(
        OUT / "h3_cases.csv", index=False, float_format="%.10g")
    print(f"\nwritten: {OUT / 'h3_cases.csv'}")


if __name__ == "__main__":
    main()
