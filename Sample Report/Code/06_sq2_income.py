"""Sub-question 2: does the association survive accounting for income?

Run:      cd Code && uv run python 06_sq2_income.py
Reads:    Code/outputs/latest_by_country.csv
Produces: Code/outputs/sq2_income.md
          Code/outputs/figures/{,dark/}sq2_added_variable.png
          Code/outputs/figures/{,dark/}sq2_collinearity.png

Method, as agreed. Sample option (a): the sub-question 1 cross-section, reduced to rows
that also carry income. Every country stays at the same year it had in sub-question 1,
so the two answers describe the same country-years. The healthy-life-expectancy-only
model is refitted on that reduced sample, so the before/after comparison is not
contaminated by the sample having changed.

Two nested fits with HC3 robust standard errors, and the income-only fit for symmetry so
neither predictor is silently treated as the explanation. Collinearity is reported
because it, not the fit, is the thing most likely to make the result ambiguous.
"""

from __future__ import annotations

from pathlib import Path

import matplotlib.patheffects as pe
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import statsmodels.api as sm

import viz_style as vs

CODE_DIR = Path(__file__).resolve().parent
OUTPUTS = CODE_DIR / "outputs"
SOURCE = OUTPUTS / "latest_by_country.csv"

COUNTRY, YEAR = "Country name", "year"
LADDER = "Life Ladder"
HLE = "Healthy life expectancy at birth"
GDP = "Log GDP per capita"
GDP_USD = "GDP per capita (PPP 2017 int$)"

SQ1_SLOPE_PER_DECADE = 1.472   # from 05_sq1_regression.py, full 160-country sample

lines: list[str] = []


def out(text: str = "") -> None:
    lines.append(text)


def table(df: pd.DataFrame) -> None:
    out()
    out(df.to_markdown(index=False))
    out()


def ols(d: pd.DataFrame, xs: list[str]):
    X = sm.add_constant(d[xs].to_numpy())
    return sm.OLS(d[LADDER].to_numpy(), X).fit(cov_type="HC3")


def ci_per_decade(res, i: int) -> tuple[float, float, float]:
    """Coefficient i and its robust 95% interval, per decade rather than per year."""
    lo, hi = res.conf_int(alpha=0.05)[i]
    return res.params[i] * 10, lo * 10, hi * 10


def residualise(d: pd.DataFrame, y: str, on: str) -> np.ndarray:
    """Residuals of y after removing the linear part explained by `on`."""
    X = sm.add_constant(d[[on]].to_numpy())
    return sm.OLS(d[y].to_numpy(), X).fit().resid


def label_by_rule(ax, d, xcol, ycol, t, fmt=lambda r: r[COUNTRY]):
    """Label the extreme point on each axis. Rule-based, so nothing is cherry-picked."""
    vs.label_extremes(ax, vs.pick_extremes(d, xcol, ycol, COUNTRY), xcol, ycol, fmt)


def figure_added_variable(d: pd.DataFrame, slope, lo, hi, theme_name: str) -> None:
    """Added-variable plot: what is left of Figure 1 once income is removed from both."""
    t = vs.use(theme_name)
    fig, ax = plt.subplots(figsize=(7.6, 5.0))
    ax.axhline(0, color=t.baseline, lw=0.8, zorder=1)
    ax.axvline(0, color=t.baseline, lw=0.8, zorder=1)
    ax.scatter(d["rx"], d["ry"], s=42, color=t.series[0], alpha=0.8,
               linewidths=1.1, edgecolors=t.surface, zorder=3)
    xs = np.linspace(d["rx"].min(), d["rx"].max(), 100)
    ax.plot(xs, (slope / 10) * xs, color=t.text_primary, lw=1.8, zorder=4)
    label_by_rule(ax, d, "rx", "ry", t)
    ax.set_xlabel("Healthy life expectancy, net of income (years)")
    ax.set_ylabel("Happiness, net of income (points)")
    vs.header(fig, "Adjusted for income, the relationship weakens but remains")
    vs.source_note(fig, "Source: World Happiness Report 2024 underlying panel "
                        "(Helliwell et al., 2024a). Labels mark the extremes on each "
                        "axis.")
    vs.layout(fig, top=0.93)
    vs.save(fig, "sq2_added_variable")


def figure_collinearity(d: pd.DataFrame, r: float, theme_name: str) -> None:
    """The diagnostic: how far the two predictors are separable at all."""
    t = vs.use(theme_name)
    fig, ax = plt.subplots(figsize=(7.6, 4.6))
    ax.scatter(d[GDP], d[HLE], s=42, color=t.series[1], alpha=0.8,
               linewidths=1.1, edgecolors=t.surface, zorder=3)
    label_by_rule(ax, d, GDP, HLE, t)
    ticks = [500, 1000, 2000, 5000, 10000, 20000, 50000, 100000]
    ax.set_xticks(np.log(ticks), [f"{v // 1000}k" if v >= 1000 else str(v)
                                  for v in ticks])
    ax.set_xlabel("GDP per capita (PPP 2017 int$, log scale)")
    ax.set_ylabel("Healthy life expectancy at birth (years)")
    vs.header(fig, "The two predictors are closely related")
    vs.source_note(fig, "Source: World Happiness Report 2024 underlying panel "
                        "(Helliwell et al., 2024a).")
    vs.layout(fig, top=0.93)
    vs.save(fig, "sq2_collinearity")


def main() -> int:
    cs = pd.read_csv(SOURCE)
    full = cs[cs[LADDER].notna() & cs[HLE].notna()]
    d = full[full[GDP].notna()].copy().reset_index(drop=True)
    dropped = sorted(set(full[COUNTRY]) - set(d[COUNTRY]))

    out("# Sub-question 2 — does the association survive accounting for income?")
    out()
    out("Generated by `Code/06_sq2_income.py`. Sample option (a), as agreed: the "
        "sub-question 1 cross-section reduced to rows that also carry income, with "
        "every country at the same year it had there.")

    # ---------------------------------------------------------------- sample
    out()
    out("## Sample")
    out()
    out(f"- **{len(d)} countries**, down from {len(full)} in sub-question 1.")
    out(f"- Dropped for having no income figure: {len(dropped)} — "
        f"{', '.join(dropped)}.")
    out("- Venezuela's absence is a consequence of the cleaning decision: its GDP "
        "series was set to missing in full.")

    # ------------------------------------------------------- collinearity first
    r_pred = float(np.corrcoef(d[GDP], d[HLE])[0, 1])
    out()
    out("## First, how separable are the two predictors?")
    out()
    out(f"Pearson correlation between log GDP per capita and healthy life expectancy: "
        f"**r = {r_pred:.3f}** (r² = {r_pred ** 2:.2f}).")
    out()
    out("![sq2_collinearity](figures/sq2_collinearity.png)")
    out()
    out("*Healthy life expectancy against income across the same countries.*")
    out()
    out("This matters more than the fit itself. The more closely the two move "
        "together, the less the data can say about which of them the ladder tracks, "
        "and the more any split between them is a property of the specification "
        "rather than of the world.")

    # ---------------------------------------------------------------- models
    mA = ols(d, [HLE])
    mB = ols(d, [HLE, GDP])
    mG = ols(d, [GDP])

    a_dec, a_lo, a_hi = ci_per_decade(mA, 1)
    b_dec, b_lo, b_hi = ci_per_decade(mB, 1)

    out()
    out("## The fits")
    out()
    rows = [
        {"model": "A — healthy life expectancy only", "n": len(d),
         "HLE per decade": f"{a_dec:+.2f} [{a_lo:+.2f}, {a_hi:+.2f}]",
         "log GDP coefficient": "—", "R²": round(mA.rsquared, 3)},
        {"model": "B — plus log GDP per capita", "n": len(d),
         "HLE per decade": f"{b_dec:+.2f} [{b_lo:+.2f}, {b_hi:+.2f}]",
         "log GDP coefficient":
             f"{mB.params[2]:+.3f} [{mB.conf_int()[2][0]:+.3f}, "
             f"{mB.conf_int()[2][1]:+.3f}]",
         "R²": round(mB.rsquared, 3)},
        {"model": "income only, for symmetry", "n": len(d),
         "HLE per decade": "—",
         "log GDP coefficient":
             f"{mG.params[1]:+.3f} [{mG.conf_int()[1][0]:+.3f}, "
             f"{mG.conf_int()[1][1]:+.3f}]",
         "R²": round(mG.rsquared, 3)},
    ]
    table(pd.DataFrame(rows))
    out(f"Intervals are 95% and HC3-robust. For reference, the sub-question 1 slope on "
        f"the full {len(full)}-country sample was {SQ1_SLOPE_PER_DECADE:+.2f}, so "
        f"reducing the sample by {len(full) - len(d)} country moved it to "
        f"{a_dec:+.2f} before income was added at all.")

    out()
    out("### What happens to the healthy-life-expectancy slope")
    out()
    retained = b_dec / a_dec
    out(f"- Before adjustment (same sample): **{a_dec:+.2f}** ladder points per decade.")
    out(f"- After adjustment: **{b_dec:+.2f}** "
        f"(95% CI {b_lo:+.2f} to {b_hi:+.2f}).")
    out(f"- **{retained:.0%} of the slope survives**, and the interval "
        f"{'excludes' if b_lo > 0 else 'includes'} zero.")
    out(f"- R² rises from {mA.rsquared:.3f} to {mB.rsquared:.3f}, an increase of "
        f"{mB.rsquared - mA.rsquared:.3f}.")
    out(f"- Income alone reaches R² = {mG.rsquared:.3f}, "
        f"{'above' if mG.rsquared > mA.rsquared else 'below'} healthy life expectancy "
        f"alone at {mA.rsquared:.3f}.")

    # ---------------------------------------------------------------- VIF
    from statsmodels.stats.outliers_influence import variance_inflation_factor
    Xv = sm.add_constant(d[[HLE, GDP]].to_numpy())
    vifs = [variance_inflation_factor(Xv, i) for i in (1, 2)]
    out()
    out("### Collinearity diagnostics")
    out()
    table(pd.DataFrame({"predictor": [HLE, GDP], "VIF": [round(v, 2) for v in vifs]}))
    out(f"- A VIF of {max(vifs):.2f} means that predictor's standard error is "
        f"{np.sqrt(max(vifs)):.2f}× wider than it would be if the two were unrelated.")
    out("- Conventional thresholds put 5 as a concern and 10 as serious. The values "
        "here are moderate, so the two coefficients are separable — but not sharply.")

    # ---------------------------------------------------------------- AV plot
    d["rx"] = residualise(d, HLE, GDP)
    d["ry"] = residualise(d, LADDER, GDP)
    out()
    out("## Added-variable plot")
    out()
    out("![sq2_added_variable](figures/sq2_added_variable.png)")
    out()
    out("*Both variables residualised on log GDP per capita: what is left of Figure 1 "
        "once income is removed from each. The slope of this plot is exactly the "
        "partial coefficient from model B.*")

    # ---------------------------------------------------------------- limits
    out()
    out("## What this does and does not establish")
    out()
    out("- The partial coefficient answers a narrow question: **among countries with "
        "similar income, do those with longer healthy lives report higher ladder "
        "scores?** It is not a claim that healthy life expectancy matters "
        "independently of income in any causal sense.")
    out("- **Adjusting for income is not a neutral operation here.** Income and health "
        "are both partly produced by the same development processes, so income is not "
        "a confounder sitting outside the relationship. Removing it may remove part of "
        "the pathway by which longer healthy lives arise, which would make the "
        "adjusted slope an *under*-statement rather than a correction.")
    out("- **Measurement error still attenuates.** Healthy life expectancy is partly "
        "interpolated, so its coefficient remains a lower bound — and in a "
        "multivariable fit, error in one predictor can bias the other's coefficient "
        "in either direction.")
    out("- Unequal spread, non-independent countries and the mixed-year cross-section "
        "all carry over from sub-question 1.")

    for name in ("light", "dark"):
        figure_collinearity(d, r_pred, name)
        figure_added_variable(d, b_dec, b_lo, b_hi, name)

    path = OUTPUTS / "sq2_income.md"
    path.write_text("\n".join(lines) + "\n")
    print("\n".join(lines))
    print(f"\nWrote {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
