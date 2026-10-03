"""Describe the three downloaded source files. Describing pass only: no judgement
about whether the data can answer anything.

Run with:  cd Code && uv run python 02_describe_data.py
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd

ATTACH = Path(__file__).resolve().parent.parent / "Attachments"
pd.set_option("display.width", 200)


def rule(title: str) -> None:
    print(f"\n{'=' * 78}\n{title}\n{'=' * 78}")


def main() -> None:
    loss = pd.read_csv(ATTACH / "gfw_tree_cover_loss_by_driver.csv")
    extent = pd.read_csv(ATTACH / "gfw_tree_cover_extent_2000.csv")
    gdp = pd.read_csv(ATTACH / "worldbank_gdp_per_capita_ppp.csv")

    rule("1. GFW tree cover loss by driver")
    print(f"shape: {loss.shape[0]:,} rows x {loss.shape[1]} columns")
    print("\ndtypes:")
    print(loss.dtypes.to_string())
    print("\nfirst rows:")
    print(loss.head(4).to_string(index=False))
    print(f"\nyears: {loss.year.min()}-{loss.year.max()} ({loss.year.nunique()} distinct)")
    print(f"countries (ISO3): {loss.iso.nunique()}")
    print(f"missing cells per column:\n{loss.isna().sum().to_string()}")
    print("\ndriver categories, total ha 2001-2025:")
    by_driver = loss.groupby("driver").tree_cover_loss_ha.agg(["sum", "size"])
    by_driver["pct"] = 100 * by_driver["sum"] / by_driver["sum"].sum()
    print(by_driver.sort_values("sum", ascending=False).to_string(
        float_format=lambda v: f"{v:,.1f}"))
    print("\nnatural_forest_class, total ha:")
    print(loss.groupby("natural_forest_class").tree_cover_loss_ha.sum()
          .sort_values(ascending=False).to_string(float_format=lambda v: f"{v:,.1f}"))
    print("\nis_primary_forest, total ha:")
    print(loss.groupby("is_primary_forest").tree_cover_loss_ha.sum()
          .to_string(float_format=lambda v: f"{v:,.1f}"))
    print(f"\nglobal total loss, all drivers, 2001-2025: "
          f"{loss.tree_cover_loss_ha.sum():,.0f} ha")
    print("\nglobal total by year (ha):")
    print(loss.groupby("year").tree_cover_loss_ha.sum()
          .to_string(float_format=lambda v: f"{v:,.0f}"))
    print("\nten largest countries by total loss (ha):")
    print(loss.groupby("iso").tree_cover_loss_ha.sum().nlargest(10)
          .to_string(float_format=lambda v: f"{v:,.0f}"))
    zero = loss[loss.tree_cover_loss_ha == 0]
    print(f"\nrows with exactly zero loss: {len(zero):,}")
    print(f"negative loss values: {(loss.tree_cover_loss_ha < 0).sum()}")

    rule("2. GFW tree cover extent 2000 (denominator)")
    print(f"shape: {extent.shape[0]:,} rows x {extent.shape[1]} columns")
    print("\nfirst rows:")
    print(extent.head(4).to_string(index=False))
    print(f"\ncountries: {extent.iso.nunique()}")
    print(f"missing cells per column:\n{extent.isna().sum().to_string()}")
    tot = extent.groupby("iso")[["tree_cover_extent_2000_ha", "area_ha"]].sum()
    print(f"\nglobal tree cover extent 2000: {tot.tree_cover_extent_2000_ha.sum():,.0f} ha")
    print(f"global land area covered:       {tot.area_ha.sum():,.0f} ha")
    print("\nten largest by extent 2000 (ha):")
    print(tot.tree_cover_extent_2000_ha.nlargest(10)
          .to_string(float_format=lambda v: f"{v:,.0f}"))
    print(f"\ncountries with zero tree cover extent 2000: "
          f"{(tot.tree_cover_extent_2000_ha == 0).sum()}")

    rule("3. World Bank GDP per capita, PPP, constant 2021 international $")
    print(f"shape: {gdp.shape[0]:,} rows x {gdp.shape[1]} columns")
    print("\nfirst rows:")
    print(gdp.head(4).to_string(index=False))
    print(f"\nyears: {gdp.year.min()}-{gdp.year.max()}")
    print(f"entities (rows include aggregates): {gdp.iso3.nunique()} distinct iso3 codes")
    blank = gdp.iso3.isna() | (gdp.iso3.astype(str).str.strip() == "")
    print(f"rows with a blank iso3 code: {blank.sum():,} "
          f"({gdp.loc[blank, 'country'].nunique()} distinct entities)")
    val = gdp.gdp_per_capita_ppp_const2021_intl_usd
    print(f"non-missing GDP values: {val.notna().sum():,} of {len(gdp):,} "
          f"({100 * val.notna().mean():.1f}%)")
    print("\nvalue distribution (non-missing):")
    print(val.describe().to_string(float_format=lambda v: f"{v:,.1f}"))
    ov = gdp[val.notna() & gdp.year.between(2001, 2025)]
    print(f"\nnon-missing values within the loss window 2001-2025: {len(ov):,}")
    print("non-missing entity-count by year, 2001-2025:")
    print(ov.groupby("year").size().to_string())

    rule("4. Overlap between the files")
    loss_iso = set(loss.iso.unique())
    gdp_iso = set(gdp.loc[gdp.iso3.notna() & val.notna(), "iso3"].unique())
    print(f"ISO3 codes in loss file:            {len(loss_iso)}")
    print(f"ISO3 codes in GDP file (any value): {len(gdp_iso)}")
    print(f"in both:                            {len(loss_iso & gdp_iso)}")
    print(f"\nin loss but not GDP ({len(loss_iso - gdp_iso)}): "
          f"{sorted(loss_iso - gdp_iso)}")
    print(f"\nin GDP but not loss ({len(gdp_iso - loss_iso)}): "
          f"{sorted(gdp_iso - loss_iso)}")


if __name__ == "__main__":
    main()
