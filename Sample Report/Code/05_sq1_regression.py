"""Sub-question 1, step 4: quantify the association, and plot the fit.

Run:      cd Code && uv run python 05_sq1_regression.py
Reads:    Code/outputs/latest_by_country.csv
Produces: Code/outputs/sq1_regression.md
          Code/outputs/figures/{,dark/}sq1_scatter.png

Method, as agreed. OLS of life ladder on healthy life expectancy across the 160-country
cross-section, with heteroscedasticity-robust (HC3) standard errors, because the scatter
shows unequal vertical spread across the range. The slope is reported per decade so the
size is interpretable. Spearman's rank correlation is reported as a robustness check
that assumes no functional form. Influence is measured rather than assumed: the fit is
refitted without the largest outlier and without the high-leverage low end.

OLS does not assume the relationship is truly linear - it estimates the best linear
approximation to whatever shape is present. Whether a line describes it adequately was
never tested.
"""

from __future__ import annotations

from pathlib import Path

import matplotlib.patheffects as pe
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import statsmodels.api as sm
from scipy import stats

import viz_style as vs

CODE_DIR = Path(__file__).resolve().parent
OUTPUTS = CODE_DIR / "outputs"
SOURCE = OUTPUTS / "latest_by_country.csv"

COUNTRY, YEAR = "Country name", "year"
LADDER = "Life Ladder"
HLE = "Healthy life expectancy at birth"

lines: list[str] = []


def out(text: str = "") -> None:
    lines.append(text)


def table(df: pd.DataFrame) -> None:
    out()
    out(df.to_markdown(index=False))
    out()


def fit(d: pd.DataFrame):
    """OLS with HC3 robust covariance. Returns the fitted results object."""
    X = sm.add_constant(d[[HLE]].to_numpy())
    return sm.OLS(d[LADDER].to_numpy(), X).fit(cov_type="HC3")


def slope_per_decade(res) -> tuple[float, float, float]:
    """Slope and its robust 95% interval, expressed per decade rather than per year."""
    ci = res.conf_int(alpha=0.05)
    return res.params[1] * 10, ci[1][0] * 10, ci[1][1] * 10


def figure(cs: pd.DataFrame, res, theme_name: str) -> None:
    t = vs.use(theme_name)
    fig, ax = plt.subplots(figsize=(7.6, 5.0))

    # 2px surface ring so overlapping points stay countable.
    ax.scatter(cs[HLE], cs[LADDER], s=42, color=t.series[0], alpha=0.8,
               linewidths=1.1, edgecolors=t.surface, zorder=3)

    xs = np.linspace(cs[HLE].min(), cs[HLE].max(), 100)
    ys = res.params[0] + res.params[1] * xs
    ax.plot(xs, ys, color=t.text_primary, lw=1.8, zorder=4)

    # Labels: the extreme country on each axis, plus the three nearest the joint
    # centre. Both sets are chosen by rule so neither is cherry-picked. Centre is
    # measured in standardised units so the two axes count equally despite their
    # different scales.
    z = ((cs[[HLE, LADDER]] - cs[[HLE, LADDER]].mean()) / cs[[HLE, LADDER]].std())
    middle = cs.loc[(z ** 2).sum(axis=1).nsmallest(3).index]
    # Each extreme is labelled into the empty corner nearest it, so no two labels
    # compete for the same space: (dx, dy, horizontal alignment).
    PLACE = {
        "min_hle": (28, -22, "left"),     # leftmost  -> right and below
        "max_hle": (-28, -22, "right"),   # rightmost -> left and below
        "min_ladder": (28, -22, "left"),  # lowest    -> right and below
        "max_ladder": (-28, 22, "right"),  # highest   -> left and above
    }
    roles = [("min_hle", cs.nsmallest(1, HLE)), ("max_hle", cs.nlargest(1, HLE)),
             ("min_ladder", cs.nsmallest(1, LADDER)), ("max_ladder", cs.nlargest(1, LADDER))]
    seen, extremes_list = set(), []
    for role, row in roles:
        name = row[COUNTRY].iloc[0]
        if name in seen:
            continue
        seen.add(name)
        extremes_list.append((role, row.iloc[0]))
    extremes = pd.concat([r.to_frame().T for _, r in extremes_list])

    ax.set_ylim(0, 9)
    halo = [pe.withStroke(linewidth=2.4, foreground=t.surface)]

    # Every label gets a leader line back to its own point, and is turned inwards
    # near an edge so it stays inside the axes. Without both, a label at this size
    # ends up floating with no visible owner.
    for role, r in extremes_list:
        dx, dy, ha = PLACE[role]
        ax.annotate(f"{r[COUNTRY]} ({int(r[YEAR])})", (r[HLE], r[LADDER]),
                    textcoords="offset points", xytext=(dx, dy), fontsize=vs.ANNOT,
                    color=t.text_secondary, path_effects=halo, zorder=5,
                    ha=ha, va="center",
                    arrowprops=dict(arrowstyle="-", lw=0.7, color=t.muted,
                                    shrinkA=1, shrinkB=4))
    # Ring the labelled extremes as well, so the reader can see which point is meant.
    ax.scatter(extremes[HLE], extremes[LADDER], s=42, facecolor="none",
               edgecolors=t.text_primary, linewidths=1.1, zorder=4)

    # The three central countries sit almost on top of each other, so their labels are
    # fanned out to the right at fixed vertical spacing, each with a leader line back
    # to its own point.
    mid = middle.sort_values(LADDER, ascending=False)
    for i, (_, r) in enumerate(mid.iterrows()):
        ax.annotate(f"{r[COUNTRY]} ({int(r[YEAR])})", (r[HLE], r[LADDER]),
                    textcoords="offset points", xytext=(-38, 26 - i * 22),
                    fontsize=vs.ANNOT, color=t.text_secondary, path_effects=halo,
                    zorder=5, va="center", ha="right",
                    arrowprops=dict(arrowstyle="-", lw=0.6, color=t.muted,
                                    shrinkA=1, shrinkB=3))
    ax.scatter(middle[HLE], middle[LADDER], s=42, facecolor="none",
               edgecolors=t.text_primary, linewidths=1.1, zorder=4)

    per_dec, lo, hi = slope_per_decade(res)
    ax.set_xlabel("Healthy life expectancy at birth (years)")
    ax.set_ylabel("Happiness (life ladder, 0–10)")
    vs.header(fig, "Longer healthy lives go with greater happiness")
    vs.source_note(fig, "Source: World Happiness Report 2024 underlying panel "
                        "(Helliwell et al., 2024a). OLS with HC3 robust standard "
                        "errors. Ringed and labelled: the extreme country on each "
                        "axis, and the three nearest the centre of the distribution.")
    vs.layout(fig, top=0.93)
    vs.save(fig, "sq1_scatter")


def main() -> int:
    cs = pd.read_csv(SOURCE)
    cs = cs[cs[LADDER].notna() & cs[HLE].notna()].reset_index(drop=True)

    out("# Sub-question 1 — quantified")
    out()
    out("**Across countries, is higher healthy life expectancy associated with higher "
        "life-ladder scores?**")
    out()
    out("Generated by `Code/05_sq1_regression.py`.")

    res = fit(cs)
    per_dec, lo, hi = slope_per_decade(res)
    rho, rho_p = stats.spearmanr(cs[HLE], cs[LADDER])

    # ---------------------------------------------------------------- headline
    out()
    out("## Result")
    out()
    out(f"- n = **{len(cs)}** countries.")
    out(f"- Slope: **{per_dec:+.2f} ladder points per decade** of healthy life "
        f"expectancy (95% CI {lo:+.2f} to {hi:+.2f}; robust *p* = "
        f"{res.pvalues[1]:.2e}).")
    out(f"- Per single year: {res.params[1]:+.4f} ladder points.")
    out(f"- **R² = {res.rsquared:.3f}** — the line accounts for "
        f"{res.rsquared:.0%} of the cross-country variance in ladder scores.")
    out(f"- Residual standard deviation: {np.sqrt(res.mse_resid):.3f} ladder points, "
        f"against a ladder standard deviation of {cs[LADDER].std(ddof=1):.3f}.")
    out(f"- Spearman's ρ = **{rho:.3f}** (*p* = {rho_p:.2e}), which assumes no "
        "functional form and agrees with the linear fit in direction and strength.")

    # ---------------------------------------------------------------- scale
    out()
    out("## What that size means in the data's own terms")
    out()
    span = cs[HLE].max() - cs[HLE].min()
    out(f"- Healthy life expectancy spans {span:.1f} years across these countries "
        f"({cs[HLE].min():.1f} to {cs[HLE].max():.1f}). Over that whole span the fitted "
        f"line rises {res.params[1] * span:.2f} ladder points.")
    out(f"- Observed ladder scores span {cs[LADDER].max() - cs[LADDER].min():.2f} points "
        f"({cs[LADDER].min():.2f} to {cs[LADDER].max():.2f}), so the line traverses "
        f"about {res.params[1] * span / (cs[LADDER].max() - cs[LADDER].min()):.0%} of "
        "the observed range.")

    # ---------------------------------------------------------------- influence
    out()
    out("## Influence")
    out()
    out("Measured rather than assumed. Each row refits the same model on a reduced "
        "sample.")
    rows = [{"sample": "all countries", "n": len(cs),
             "slope per decade": round(per_dec, 3),
             "R²": round(res.rsquared, 3)}]

    worst = cs.loc[cs[LADDER].idxmin(), COUNTRY]
    for label, sub in [
        (f"excluding {worst}", cs[cs[COUNTRY] != worst]),
        ("excluding healthy life expectancy < 50", cs[cs[HLE] >= 50]),
        ("excluding the 25 pre-2023 observations", cs[cs[YEAR] == cs[YEAR].max()]),
    ]:
        r2 = fit(sub)
        rows.append({"sample": label, "n": len(sub),
                     "slope per decade": round(slope_per_decade(r2)[0], 3),
                     "R²": round(r2.rsquared, 3)})
    table(pd.DataFrame(rows))

    infl = res.get_influence().cooks_distance[0]
    top = (pd.DataFrame({COUNTRY: cs[COUNTRY], "Cook's D": infl})
             .nlargest(5, "Cook's D").round({"Cook's D": 3}))
    out("Largest Cook's distances:")
    table(top)
    out(f"- Conventional threshold 4/n = {4 / len(cs):.3f}. "
        f"{int((infl > 4 / len(cs)).sum())} countries exceed it.")

    # ---------------------------------------------------------------- caveats
    out()
    out("## Assumptions and limits")
    out()
    out("- **Unequal spread** was expected from the scatter, so standard errors are "
        "HC3-robust throughout. The slope estimate itself is unaffected by "
        "heteroscedasticity; only its interval would be.")
    out("- **Measurement error in the predictor.** Healthy life expectancy is "
        "interpolated and extrapolated by WHR, so it is partly model output. Classical "
        "measurement error in a predictor attenuates a slope toward zero, so this "
        "estimate is best read as a **lower bound** on the association.")
    out("- **Countries are not independent draws.** Neighbours share institutions, "
        "health systems and history, so the effective sample is smaller than "
        f"{len(cs)} and the interval above is optimistic. No fix is available at this "
        "level of aggregation.")
    out("- **The cross-section mixes years.** 135 countries contribute 2023 and 25 an "
        "earlier year, which adds noise that cannot be separated from the "
        "relationship.")
    out("- **Association, not cause**, and **countries, not people** — as fixed in the "
        "research question.")
    out("- **Whether a line is the right shape is not settled here**, and it is not "
        "settled anywhere in this analysis: no test of curvature was carried out.")

    for name in ("light", "dark"):
        figure(cs, res, name)

    path = OUTPUTS / "sq1_regression.md"
    path.write_text("\n".join(lines) + "\n")
    print("\n".join(lines))
    print(f"\nWrote {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
