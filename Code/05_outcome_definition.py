"""Make the outcome variable concrete: what is in the numerator, what is in the
denominator, and how the denominator behaves across the 25 years.

Describes the outcome only. GDP is not read. Illustrative driver scope, not a decision.

Run with:  cd Code && uv run python 05_outcome_definition.py
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd

ATTACH = Path(__file__).resolve().parent.parent / "Attachments"
pd.set_option("display.width", 220)

FOREST_FLOOR_HA = 100_000
CONVERSION = ["Permanent agriculture", "Hard commodities", "Settlements & Infrastructure"]
SHOW = ["BRA", "FIN", "PRT", "COD", "IDN", "KHM"]


def rule(t: str) -> None:
    print(f"\n{'=' * 100}\n{t}\n{'=' * 100}")


def main() -> None:
    loss = pd.read_csv(ATTACH / "gfw_tree_cover_loss_by_driver.csv")
    extent = pd.read_csv(ATTACH / "gfw_tree_cover_extent_2000.csv")

    ext = extent.groupby("iso").tree_cover_extent_2000_ha.sum().rename("E2000")
    keep = ext[ext >= FOREST_FLOOR_HA].index
    loss = loss[loss.iso.isin(keep)]

    grid = (loss.assign(is_conv=loss.driver.isin(CONVERSION))
            .groupby(["iso", "year"])
            .apply(lambda g: pd.Series({
                "conv_ha": g.loc[g.is_conv, "tree_cover_loss_ha"].sum(),
                "total_ha": g.tree_cover_loss_ha.sum(),
            }), include_groups=False)
            .reset_index()
            .merge(ext.reset_index(), on="iso"))
    grid = grid.sort_values(["iso", "year"])

    # Three denominators.
    g = grid.groupby("iso")
    grid["cum_total_prior"] = g.total_ha.cumsum() - grid.total_ha
    grid["cum_conv_prior"] = g.conv_ha.cumsum() - grid.conv_ha
    grid["den_fixed"] = grid.E2000
    grid["den_less_total"] = grid.E2000 - grid.cum_total_prior
    grid["den_less_conv"] = grid.E2000 - grid.cum_conv_prior

    for k in ["fixed", "less_total", "less_conv"]:
        grid[f"rate_{k}"] = 100 * grid.conv_ha / grid[f"den_{k}"]

    rule("1. The outcome, spelled out for one country-year")
    r = grid[(grid.iso == "BRA") & (grid.year == 2015)].iloc[0]
    print(f"Brazil, 2015")
    print(f"  numerator   conversion loss in 2015          = {r.conv_ha:>15,.0f} ha")
    print(f"              (drivers: {', '.join(CONVERSION)})")
    print(f"  total loss  all eight drivers, 2015          = {r.total_ha:>15,.0f} ha")
    print(f"  denominator tree cover extent 2000           = {r.E2000:>15,.0f} ha")
    print(f"              minus conversion loss 2001-2014  = {r.cum_conv_prior:>15,.0f} ha")
    print(f"              = forest still standing, start 2015 {r.den_less_conv:>13,.0f} ha")
    print(f"  outcome     rate = numerator / denominator   = {r.rate_less_conv:>15.4f} %")
    print(f"\n  the same year on a denominator fixed at 2000  = {r.rate_fixed:>15.4f} %")

    rule("2. Why subtracting ALL prior loss is wrong: forest that regrows")
    print("Cumulative loss 2001-2025 as a share of 2000 extent, split by what caused it.")
    print("Where the gap between the two columns is large, most of the 'loss' was fire or")
    print("logging, which regrows. Subtracting it would report a country as deforested")
    print("when its forest is still there.\n")
    summ = (grid.groupby("iso")
            .agg(E2000=("E2000", "first"), conv=("conv_ha", "sum"), tot=("total_ha", "sum")))
    summ["pct_total"] = 100 * summ.tot / summ.E2000
    summ["pct_conv"] = 100 * summ.conv / summ.E2000
    summ["gap"] = summ.pct_total - summ.pct_conv
    print(summ.nlargest(10, "gap")[["E2000", "pct_total", "pct_conv", "gap"]]
          .to_string(float_format=lambda v: f"{v:,.1f}"))
    print("\nFor contrast, where nearly all loss was permanent conversion:")
    print(summ[summ.pct_total > 10].nsmallest(8, "gap")[["E2000", "pct_total", "pct_conv", "gap"]]
          .to_string(float_format=lambda v: f"{v:,.1f}"))

    rule("3. How much the three denominators differ over the sample")
    last = grid[grid.year == 2025]
    print("Denominator in 2025 as a percentage of the 2000 extent:")
    print(pd.DataFrame({
        "fixed at 2000": 100 * last.den_fixed / last.E2000,
        "less all prior loss": 100 * last.den_less_total / last.E2000,
        "less prior conversion": 100 * last.den_less_conv / last.E2000,
    }).describe().to_string(float_format=lambda v: f"{v:,.1f}"))
    print("\nSpearman between the three resulting annual rate series (all country-years):")
    print(grid[["rate_fixed", "rate_less_total", "rate_less_conv"]]
          .corr(method="spearman").to_string(float_format=lambda v: f"{v:.4f}"))

    rule("4. The chosen outcome, for a few countries across the period")
    print("Annual conversion loss as % of forest still standing at the start of the year.\n")
    tab = (grid[grid.iso.isin(SHOW)]
           .pivot(index="year", columns="iso", values="rate_less_conv")
           .reindex(columns=SHOW))
    print(tab.to_string(float_format=lambda v: f"{v:.3f}"))

    rule("5. Year-to-year volatility, which is why year effects matter")
    tot_by_year = grid.groupby("year")[["conv_ha", "total_ha"]].sum()
    tot_by_year["conv_index"] = 100 * tot_by_year.conv_ha / tot_by_year.conv_ha.loc[2001]
    print("Global totals across the 135-country sample (ha), and conversion as an index:")
    print(tot_by_year.to_string(float_format=lambda v: f"{v:,.0f}"))
    cv = (grid.groupby("iso").rate_less_conv.std()
          / grid.groupby("iso").rate_less_conv.mean()).dropna()
    print(f"\nWithin-country coefficient of variation of the annual rate, across countries:")
    print(cv.describe().to_string(float_format=lambda v: f"{v:.2f}"))
    print("\nThe median country's annual rate varies by around this fraction of its own mean")
    print("from year to year. Single years are noisy; this is the case for year effects and")
    print("for considering multi-year averages.")


if __name__ == "__main__":
    main()
