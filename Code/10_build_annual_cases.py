"""Annual permanent-conversion series for the eight cases of sub-question 3.

The cross-section in `analysis_dataset.csv` is one row per country and carries no
time dimension. This builds the annual counterpart for the eight countries the
step-2 rule selected, and nothing wider: sub-question 3 is a comparison of those
eight and no other country's annual series is used anywhere.

The rate is annual permanent conversion divided by the country's year-2000 tree
cover — the same denominator the cumulative outcome uses, and constant within a
country. The 24 annual values therefore sum exactly to `permanent_loss_share`,
which the checks below assert. A second definition of the rate would make the
trend and the cross-section answer different questions.

The driver scope is imported from `07_build_analysis_dataset.py` rather than
restated, so the two cannot drift apart.

Reads  ../Attachments/gfw_tree_cover_loss_by_driver.csv
       outputs/analysis_dataset.csv   (extent and income, sample already fixed)
       outputs/h3_cases.csv           (the eight cases, fixed in step 2)
Writes outputs/annual_cases.csv       (8 countries x 24 years)
"""

from __future__ import annotations

import importlib
from pathlib import Path

import pandas as pd

HERE = Path(__file__).resolve().parent
ATTACH = HERE.parent / "Attachments"
OUT = HERE / "outputs"

_build = importlib.import_module("07_build_analysis_dataset")
PERMANENT: list[str] = _build.PERMANENT
Y0: int = _build.Y0
Y1: int = _build.Y1


def main() -> None:
    cases = pd.read_csv(OUT / "h3_cases.csv")
    panel = pd.read_csv(OUT / "analysis_dataset.csv")
    loss = pd.read_csv(ATTACH / "gfw_tree_cover_loss_by_driver.csv")

    print(f"  cases: {len(cases)}   drivers counted as permanent: {PERMANENT}")

    w = loss[loss.year.between(Y0, Y1) & loss.driver.isin(PERMANENT)]
    w = w[w.iso.isin(cases.iso3)]
    annual = (w.groupby(["iso", "year"])["tree_cover_loss_ha"].sum()
                .rename("permanent_loss_ha").reset_index()
                .rename(columns={"iso": "iso3"}))

    # Reindex onto the full grid so a year with no recorded loss is a zero rather
    # than a gap: a missing bar and a zero bar look different and mean different
    # things, and a gap would also bias any trend fitted in step 4.
    grid = pd.MultiIndex.from_product([sorted(cases.iso3), range(Y0, Y1 + 1)],
                                      names=["iso3", "year"]).to_frame(index=False)
    annual = grid.merge(annual, on=["iso3", "year"], how="left")
    annual["permanent_loss_ha"] = annual["permanent_loss_ha"].fillna(0.0)

    meta = panel[["iso3", "country", "income_group", "extent_2000_ha",
                  "gdp_pc_mean", "permanent_loss_share"]]
    annual = annual.merge(meta, on="iso3", how="left")
    annual["annual_permanent_rate"] = (annual.permanent_loss_ha
                                       / annual.extent_2000_ha)

    # The annual series must decompose the cross-sectional outcome exactly. If it
    # does not, the two sub-questions are measuring different things.
    check = (annual.groupby("iso3")["annual_permanent_rate"].sum()
             - annual.groupby("iso3")["permanent_loss_share"].first()).abs()
    worst = check.max()
    print(f"  annual rates sum to the cumulative share: max |difference| {worst:.2e}")
    assert worst < 1e-9, "annual series does not decompose permanent_loss_share"
    assert len(annual) == len(cases) * (Y1 - Y0 + 1), "grid is not complete"
    assert annual.annual_permanent_rate.notna().all(), "missing rate"
    assert (annual.annual_permanent_rate >= 0).all(), "negative rate"

    annual = annual.sort_values(["gdp_pc_mean", "year"])
    annual.to_csv(OUT / "annual_cases.csv", index=False)
    print(f"  wrote outputs/annual_cases.csv  ({len(annual)} rows)")

    peak = annual.loc[annual.groupby("iso3")["annual_permanent_rate"].idxmax()]
    print("  highest single year in each case, by mean income:")
    for _, r in peak.sort_values("gdp_pc_mean").iterrows():
        print(f"    {r.country:<16} {int(r.year)}  {r.annual_permanent_rate:.4f}"
              f"   (mean GDP {r.gdp_pc_mean:,.0f})")


if __name__ == "__main__":
    main()
