"""How to measure cumulative loss over the period, for a cross-sectional H1.

Compares the candidate definitions and shows how they relate to one another.
Describes the outcome only; GDP is not read, and no driver is related to any other.

Run with:  cd Code && uv run python 06_cumulative_outcome.py
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

ATTACH = Path(__file__).resolve().parent.parent / "Attachments"
pd.set_option("display.width", 200)

FOREST_FLOOR_HA = 100_000
CONVERSION = ["Permanent agriculture", "Hard commodities", "Settlements & Infrastructure"]
Y0, Y1 = 2001, 2024
T = Y1 - Y0 + 1


def rule(t: str) -> None:
    print(f"\n{'=' * 84}\n{t}\n{'=' * 84}")


def main() -> None:
    loss = pd.read_csv(ATTACH / "gfw_tree_cover_loss_by_driver.csv")
    extent = pd.read_csv(ATTACH / "gfw_tree_cover_extent_2000.csv")

    ext = extent.groupby("iso").tree_cover_extent_2000_ha.sum().rename("E2000")
    keep = ext[ext >= FOREST_FLOOR_HA].index
    w = loss[loss.iso.isin(keep) & loss.year.between(Y0, Y1)].copy()

    conv = (w[w.driver.isin(CONVERSION)].groupby("iso").tree_cover_loss_ha.sum()
            .reindex(keep, fill_value=0.0).rename("conv_ha"))
    d = pd.concat([ext.loc[keep], conv], axis=1)

    # --- the two candidate measures ------------------------------------------
    d["C_share"] = d.conv_ha / d.E2000                      # cumulative share lost
    d["r_annual"] = 1 - (1 - d.C_share) ** (1 / T)          # constant annual depletion
    d["naive_mean"] = d.C_share / T                          # simple average per year

    rule(f"1. The two definitions, over {Y0}-{Y1} (T = {T} years), n = {len(d)}")
    print("C_share   = cumulative conversion loss / tree cover extent in 2000")
    print("r_annual  = 1 - (1 - C_share)^(1/T), the constant proportional rate that would")
    print("            produce the same depletion over T years, allowing for a shrinking base")
    print("naive     = C_share / T, which ignores the shrinking base\n")
    print(d[["C_share", "r_annual", "naive_mean"]].describe()
          .to_string(float_format=lambda v: f"{v:.5f}"))

    rule("2. They carry the same information: the transform is strictly monotone")
    print("Spearman rank correlation:")
    print(d[["C_share", "r_annual", "naive_mean"]].corr(method="spearman")
          .to_string(float_format=lambda v: f"{v:.6f}"))
    print("\nPearson between C_share and r_annual: "
          f"{d.C_share.corr(d.r_annual):.6f}")
    print("\nSo the choice cannot change how countries rank. It changes the SCALE, and")
    print("therefore the shape a quadratic in log income has to fit. Worked examples:")
    ex = d.nlargest(4, "C_share")
    for iso, row in ex.iterrows():
        print(f"  {iso}: C = {row.C_share:.4f} -> r_annual = {row.r_annual:.5f}"
              f"  (naive C/T = {row.naive_mean:.5f}, understated by "
              f"{100 * (1 - row.naive_mean / row.r_annual):.1f}%)")
    small = d[d.C_share < 0.01].nlargest(1, "C_share")
    for iso, row in small.iterrows():
        print(f"  {iso}: C = {row.C_share:.4f} -> r_annual = {row.r_annual:.5f}"
              f"  (naive C/T = {row.naive_mean:.5f}, understated by "
              f"{100 * (1 - row.naive_mean / row.r_annual):.1f}%)")
    print("\nThe gap between r_annual and the naive average matters only where C is large.")

    rule("3. The outcome is a proportion, bounded and heavily skewed")
    print(f"minimum  {d.C_share.min():.6f}   ({d.C_share.idxmin()})")
    print(f"median   {d.C_share.median():.6f}")
    print(f"maximum  {d.C_share.max():.6f}   ({d.C_share.idxmax()})")
    print(f"skew     {d.C_share.skew():.2f}")
    print(f"countries with C_share exactly 0: {(d.C_share == 0).sum()}")
    print(f"countries with C_share < 0.001:   {(d.C_share < 0.001).sum()}")
    print(f"countries with C_share > 0.20:    {(d.C_share > 0.20).sum()}")
    print(f"\nskew of log(C_share) among the {(d.C_share > 0).sum()} non-zero countries: "
          f"{np.log(d.C_share[d.C_share > 0]).skew():.2f}")
    print("\nThe bound at 0 and 1 and the skew are why OLS on C_share is the wrong fit.")
    print("A fractional logit (GLM binomial, logit link, robust SE) respects both.")

    rule("4. Distribution across the sample")
    bins = [-1e-9, 0.001, 0.01, 0.05, 0.10, 0.20, 1.0]
    labels = ["<0.1%", "0.1-1%", "1-5%", "5-10%", "10-20%", ">20%"]
    print("share of 2000 forest permanently converted over the period:")
    print(pd.cut(d.C_share, bins=bins, labels=labels).value_counts()
          .reindex(labels).to_string())

    rule("5. The extremes, as a sanity check on the measure")
    show = ["C_share", "r_annual", "conv_ha", "E2000"]
    print("Highest cumulative conversion share:")
    print(d.nlargest(12, "C_share")[show]
          .to_string(float_format=lambda v: f"{v:,.5f}"))
    print("\nLowest, among countries with over 1 Mha of forest:")
    big = d[d.E2000 > 1_000_000]
    print(big.nsmallest(10, "C_share")[show]
          .to_string(float_format=lambda v: f"{v:,.5f}"))

    rule("6. Does dropping 2025 change anything?")
    w25 = loss[loss.iso.isin(keep) & loss.year.between(2001, 2025)]
    conv25 = (w25[w25.driver.isin(CONVERSION)].groupby("iso").tree_cover_loss_ha.sum()
              .reindex(keep, fill_value=0.0))
    c25 = conv25 / d.E2000
    print(f"mean C_share to 2024: {d.C_share.mean():.5f}")
    print(f"mean C_share to 2025: {c25.mean():.5f}")
    print(f"Spearman between the two: {d.C_share.corr(c25, method='spearman'):.6f}")
    print("\nAdding 2025 raises every country's total slightly and reorders almost nothing.")


if __name__ == "__main__":
    main()
