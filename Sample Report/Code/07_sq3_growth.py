"""Sub-question 3: does the growth of happiness depend on healthy life expectancy?

Run:      cd Code && uv run python 07_sq3_growth.py
Reads:    Code/outputs/whr_clean.csv
Produces: Code/outputs/sq3_growth.md
          Code/outputs/consecutive_pairs.csv
          Code/outputs/figures/{,dark/}sq3_growth.png
          Code/outputs/figures/{,dark/}sq3_growth_by_hle.png

Notation. H is happiness, the national average Cantril life ladder. E is healthy life
expectancy at birth, in years.

Model, as specified by the user:

    H(t+1) - H(t) = k + H(t) (a0 + a1 H(t)) + a2 E(t)

which multiplied out is linear in the parameters:

    dH = k + a0 H + a1 H^2 + a2 E + e

Healthy life expectancy enters additively, not multiplied by happiness, so its effect
on growth is the same at every level of happiness. Two superseded forms - proportional
growth, and an interaction with happiness - are recorded in Appendix.md.

Standard errors are clustered by country, because consecutive pairs overlap: each year
ends one pair and starts the next, so the errors are serially correlated within a
country. Pooled, with no country fixed effects, as specified - adding them to a model
carrying H(t) on the right-hand side would introduce dynamic panel bias and need a
different estimator, not merely more dummies.
"""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import statsmodels.api as sm

import viz_style as vs

CODE_DIR = Path(__file__).resolve().parent
OUTPUTS = CODE_DIR / "outputs"
SOURCE = OUTPUTS / "whr_clean.csv"

COUNTRY, YEAR = "Country name", "year"
LADDER, HLE, GDP = "Life Ladder", "Healthy life expectancy at birth", "Log GDP per capita"

TERMS = ["H", "H2", "E"]
TERM_LABELS = ["$a_0$ — $H_t$", "$a_1$ — $H_t^2$", "$a_2$ — $E_t$"]

lines: list[str] = []


def out(text: str = "") -> None:
    lines.append(text)


def table(df: pd.DataFrame) -> None:
    lines.append("")
    lines.append(df.to_markdown(index=False))
    lines.append("")


def build_pairs(df: pd.DataFrame) -> pd.DataFrame:
    """Every pair of consecutive CALENDAR years with all three variables in both.

    Consecutive rows are not enough: countries have gaps, so the year numbers must
    actually differ by one.
    """
    need = [LADDER, HLE, GDP]
    ok = df[df[need].notna().all(axis=1)][[COUNTRY, YEAR] + need]
    nxt = ok.copy()
    nxt[YEAR] = nxt[YEAR] - 1          # so a join on YEAR aligns t with t+1
    pairs = ok.merge(nxt, on=[COUNTRY, YEAR], suffixes=("_t", "_t1"))
    pairs["dH"] = pairs[f"{LADDER}_t1"] - pairs[f"{LADDER}_t"]
    pairs["H"] = pairs[f"{LADDER}_t"]
    pairs["E"] = pairs[f"{HLE}_t"]
    pairs["H2"] = pairs["H"] ** 2
    return pairs.rename(columns={YEAR: "year_t"})


def fit(pairs: pd.DataFrame, cols: list[str]):
    X = sm.add_constant(pairs[cols].to_numpy())
    return sm.OLS(pairs["dH"].to_numpy(), X).fit(
        cov_type="cluster", cov_kwds={"groups": pairs[COUNTRY].to_numpy()})


def coef_table(res) -> pd.DataFrame:
    ci = res.conf_int()
    return pd.DataFrame({
        "term": ["$k$ (constant)"] + TERM_LABELS,
        "estimate": [round(v, 5) for v in res.params],
        "95% low": [round(v, 5) for v in ci[:, 0]],
        "95% high": [round(v, 5) for v in ci[:, 1]],
        "p": [f"{v:.3g}" for v in res.pvalues],
    })


def equilibrium(res, E: float):
    """Solve dH = 0 for H at a given E, returning the stable root if there is one.

    With E entering additively the condition is a1 H^2 + a0 H + (k + a2 E) = 0, so the
    covariate shifts the constant rather than the slope.
    """
    k, a0, a1, a2 = res.params
    c = k + a2 * E
    if abs(a1) < 1e-12:
        return None, None
    disc = a0 ** 2 - 4 * a1 * c
    if disc < 0:
        return None, None
    roots = [(-a0 + s * np.sqrt(disc)) / (2 * a1) for s in (1, -1)]
    stable = [H for H in roots if (a0 + 2 * a1 * H) < 0]
    if not stable:
        return roots, None
    Hs = stable[0]
    slope = -a2 / (a0 + 2 * a1 * Hs)      # dH*/dE by implicit differentiation
    return roots, (Hs, slope)


def figure_by_happiness(pairs: pd.DataFrame, res, theme_name: str) -> None:
    """Growth against happiness, curves at three levels of healthy life expectancy."""
    t = vs.use(theme_name)
    k, a0, a1, a2 = res.params
    fig, ax = plt.subplots(figsize=(7.8, 5.0))
    ax.axhline(0, color=t.baseline, lw=0.9, zorder=1)
    ax.scatter(pairs["H"], pairs["dH"], s=14, color=t.muted, alpha=0.35,
               linewidths=0, zorder=2)
    xs = np.linspace(pairs["H"].min(), pairs["H"].max(), 100)
    for i, q in enumerate([0.1, 0.5, 0.9]):
        E = pairs["E"].quantile(q)
        ax.plot(xs, k + a0 * xs + a1 * xs ** 2 + a2 * E,
                color=t.series[i], lw=2.0, zorder=4,
                label=f"{E:.0f} years ({int(q * 100)}th pct)")
    ax.legend(title="Healthy life expectancy", loc="lower left", alignment="left")
    ax.set_xlabel("Happiness at year $t$ (life ladder, 0–10)")
    ax.set_ylabel("Change in happiness, $t$ to $t+1$")
    vs.header(fig, "Growth of happiness against its current level")
    vs.source_note(fig, "Source: World Happiness Report 2024 underlying panel "
                        "(Helliwell et al., 2024a). OLS, standard errors clustered "
                        "by country.")
    vs.layout(fig, top=0.93)
    vs.save(fig, "sq3_growth")


def figure_by_life_expectancy(pairs: pd.DataFrame, res, theme_name: str) -> None:
    """Growth against healthy life expectancy, lines at three levels of happiness.

    At a fixed H the model is linear in E with slope a2, so these are parallel lines.
    """
    t = vs.use(theme_name)
    k, a0, a1, a2 = res.params
    fig, ax = plt.subplots(figsize=(7.8, 5.0))
    ax.axhline(0, color=t.baseline, lw=0.9, zorder=1)
    ax.scatter(pairs["E"], pairs["dH"], s=14, color=t.muted, alpha=0.35,
               linewidths=0, zorder=2)
    xs = np.linspace(pairs["E"].min(), pairs["E"].max(), 100)
    for i, q in enumerate([0.1, 0.5, 0.9]):
        H = pairs["H"].quantile(q)
        ax.plot(xs, k + a0 * H + a1 * H ** 2 + a2 * xs,
                color=t.series[i], lw=2.0, zorder=4,
                label=f"{H:.1f} ({int(q * 100)}th pct)")
    ax.legend(title="Happiness at year $t$", loc="lower left", alignment="left")
    ax.set_xlabel("Healthy life expectancy at birth, year $t$ (years)")
    ax.set_ylabel("Change in happiness, $t$ to $t+1$")
    vs.header(fig, "Growth of happiness against healthy life expectancy")
    vs.source_note(fig, "Source: World Happiness Report 2024 underlying panel "
                        "(Helliwell et al., 2024a). OLS, standard errors clustered "
                        "by country.")
    vs.layout(fig, top=0.93)
    vs.save(fig, "sq3_growth_by_hle")


def main() -> int:
    df = pd.read_csv(SOURCE)
    pairs = build_pairs(df)

    out("# Sub-question 3 — the growth of happiness")
    out()
    out("**Year to year within countries, does the growth rate of happiness depend on "
        "healthy life expectancy, and does it slow as happiness rises?**")
    out()
    out("Generated by `Code/07_sq3_growth.py`. Notation: $H$ is happiness, the national "
        "average life ladder; $E$ is healthy life expectancy at birth in years.")

    # ---------------------------------------------------------------- sample
    out()
    out("## The paired sample")
    out()
    out("Every pair of consecutive **calendar** years in which the life ladder, log GDP "
        "per capita and healthy life expectancy are all present in both years. "
        "Consecutive rows would not do: countries have gaps, so the year numbers must "
        "differ by exactly one.")
    out()
    out(f"- **{len(pairs):,} pairs**, from **{pairs[COUNTRY].nunique()} countries**.")
    out(f"- Start years {int(pairs['year_t'].min())}–{int(pairs['year_t'].max())}.")
    per = pairs.groupby(COUNTRY).size()
    out(f"- Pairs per country: min {per.min()}, median {int(per.median())}, "
        f"max {per.max()}.")
    out("- Income is required for selection although this model does not use it, so "
        "that adding income later cannot change the sample.")
    out()
    out(f"- Change in happiness, $\\Delta H$: mean {pairs['dH'].mean():+.4f}, "
        f"SD {pairs['dH'].std():.4f}, range {pairs['dH'].min():+.2f} to "
        f"{pairs['dH'].max():+.2f}.")
    out(f"- $H_t$: {pairs['H'].min():.2f} to {pairs['H'].max():.2f}. "
        f"$E_t$: {pairs['E'].min():.1f} to {pairs['E'].max():.1f} years.")
    out()
    out("Note that **pairs overlap**: each year is the end of one pair and the start "
        "of the next, so the errors are serially correlated within a country. "
        "Standard errors are clustered by country throughout.")

    yr = pairs.groupby("year_t").size().reset_index()
    yr.columns = ["Start year", "Pairs"]
    table(yr)

    # ---------------------------------------------------------------- fit
    res = fit(pairs, TERMS)
    out("## The model")
    out()
    out("$$\\Delta H = k + a_0 H_t + a_1 H_t^2 + a_2 E_t + \\varepsilon$$")
    out()
    table(coef_table(res))
    out(f"- n = {int(res.nobs):,} pairs, clustered on "
        f"{pairs[COUNTRY].nunique()} countries. R² = {res.rsquared:.4f}.")
    out(f"- Residual SD {np.sqrt(res.mse_resid):.4f} against an outcome SD of "
        f"{pairs['dH'].std():.4f}.")
    fstat = res.f_test(np.eye(4)[1:])
    out(f"- Joint test that $a_0 = a_1 = a_2 = 0$: F = {float(fstat.fvalue):.2f}, "
        f"p = {float(fstat.pvalue):.3g}.")

    out()
    out("### What each term adds")
    out()
    rows = [{"model": "constant only", "R²": 0.0}]     # by definition
    for label, cols in [("+ $H_t$", ["H"]), ("+ $H_t^2$", ["H", "H2"]),
                        ("+ $E_t$ (full)", TERMS)]:
        rows.append({"model": label, "R²": round(fit(pairs, cols).rsquared, 4)})
    table(pd.DataFrame(rows))
    out("R² is low throughout, which is expected: year-on-year change in a national "
        "survey mean is mostly noise, and the question is whether any systematic part "
        "of it tracks happiness and healthy life expectancy — not whether the model "
        "predicts individual changes well.")

    k, a0, a1, a2 = res.params
    out()
    out(f"Note the sign of $a_1$ is positive, which does **not** mean growth "
        "accelerates with happiness. The slope of the growth curve is "
        f"$a_0 + 2a_1 H$, which is negative across the whole observed range of $H$ "
        f"({a0 + 2 * a1 * pairs['H'].min():+.3f} at the lowest, "
        f"{a0 + 2 * a1 * pairs['H'].max():+.3f} at the highest); the positive $a_1$ "
        "only means the slowing is slightly less steep at high levels.")

    # ---------------------------------------------------------------- collinearity
    from statsmodels.stats.outliers_influence import variance_inflation_factor
    Xv = sm.add_constant(pairs[TERMS].to_numpy())
    vifs = [variance_inflation_factor(Xv, i) for i in (1, 2, 3)]
    out()
    out("### Collinearity")
    out()
    table(pd.DataFrame({"term": ["$H_t$", "$H_t^2$", "$E_t$"],
                        "VIF": [round(v, 1) for v in vifs]}))
    out("$H$ and $H^2$ are necessarily collinear, being functions of the same "
        "variable, so their individual coefficients are imprecise and are best read "
        "together as the shape of the growth curve. $E$ now enters on its own rather "
        "than multiplied by $H$, so its coefficient is far better identified than in "
        "the superseded interaction form, where every regressor was a function of the "
        "same two variables.")

    # ---------------------------------------------------------------- equilibrium
    out()
    out("## Implied equilibrium")
    out()
    Emed = float(pairs["E"].median())
    roots, stable = equilibrium(res, Emed)
    if roots is None:
        out(f"At the median healthy life expectancy of {Emed:.1f} years the fitted "
            "curve does not cross zero, so the model implies no equilibrium level "
            "within reach of the data.")
    else:
        out(f"Setting $\\Delta H = 0$ at the median healthy life expectancy "
            f"({Emed:.1f} years) gives roots at $H$ = "
            + ", ".join(f"{r:.2f}" for r in roots) + ".")
        if stable is None:
            out("Neither root is stable, so the model does not imply a level "
                "happiness settles at.")
        else:
            Hs, slope = stable
            out(f"- Stable root: **$H^*$ = {Hs:.2f}**, against an observed range of "
                f"{pairs['H'].min():.2f}–{pairs['H'].max():.2f}.")
            out(f"- Long-run response of happiness to healthy life expectancy there: "
                f"**{slope * 10:+.2f} points per decade**, against **+1.47** measured "
                "across countries in sub-question 1.")
            rows = []
            for q in (0.1, 0.5, 0.9):
                E = float(pairs["E"].quantile(q))
                _, st = equilibrium(res, E)
                rows.append({"$E$ (years)": round(E, 1),
                             "stable $H^*$": round(st[0], 2) if st else None,
                             "d$H^*$/d$E$ per decade":
                                 round(st[1] * 10, 2) if st else None})
            table(pd.DataFrame(rows))
            out("The long-run response still varies with the level, because the "
                "equilibrium condition remains quadratic in $H$ — but through "
                "$a_0 + 2a_1 H^*$ alone, not through $E$ as well.")

    out()
    out("### Where growth stops")
    out()
    out("Solving $\\Delta H = 0$ for $E$ at a fixed level of happiness gives the "
        "healthy life expectancy at which the model predicts no further change — the "
        "zero crossings visible in the second figure below.")
    rows = []
    for q in (0.1, 0.5, 0.9):
        H = float(pairs["H"].quantile(q))
        Estar = -(k + a0 * H + a1 * H ** 2) / a2
        rows.append({"happiness $H$": round(H, 1), "percentile": f"{int(q * 100)}th",
                     "$E$ where growth stops (years)": round(Estar, 1)})
    table(pd.DataFrame(rows))

    # ------------------------------------------------------- measurement error
    out()
    out("## Measurement error in $H_t$")
    out()
    out("$H_t$ appears on both sides of the equation: inside "
        "$\\Delta H = H_{t+1} - H_t$ with a negative sign, and as a regressor with a "
        "positive one. Sampling error in the ladder therefore induces a *negative* "
        "correlation between the two, pushing $a_0$ downward whether or not growth "
        "genuinely slows as happiness rises. **Part of the strongly negative $a_0$ may "
        "be manufactured this way**, so the size of the bias matters.")
    out()
    out("This panel publishes no confidence intervals, so the ladder's sampling error "
        "cannot be read from the file. The table below therefore simulates it: fresh "
        "noise of a stated size is added to the ladder **once per country-year in the "
        "underlying panel**, the pairs are rebuilt from that noisy series, and the "
        "model refitted. Adding noise this way is what reproduces the mechanism — the "
        "same draw enters $\\Delta H$ for one pair and the regressor for the next, "
        "exactly as real sampling error does. Adding independent noise to the "
        "regressor alone would test classical attenuation instead, which is a "
        "different and much milder problem.")
    rng = np.random.default_rng(20260907)
    rows = [{"assumed SE of ladder": 0.0, "$k$": round(res.params[0], 4),
             "$a_0$": round(res.params[1], 4), "$a_1$": round(res.params[2], 4),
             "$a_2$": round(res.params[3], 5)}]
    for se in (0.05, 0.10, 0.15):
        est = []
        for _ in range(40):
            noisy = df.copy()
            noisy[LADDER] = noisy[LADDER] + rng.normal(0, se, len(noisy))
            est.append(fit(build_pairs(noisy), TERMS).params)
        m = np.mean(est, axis=0)
        rows.append({"assumed SE of ladder": se, "$k$": round(m[0], 4),
                     "$a_0$": round(m[1], 4), "$a_1$": round(m[2], 4),
                     "$a_2$": round(m[3], 5)})
    table(pd.DataFrame(rows))
    out("Read this as a sensitivity check rather than a correction: it shows how far "
        "the estimates would move if the ladder carried that much noise, averaged over "
        "40 draws per row. It does not establish how much noise the ladder actually "
        "carries.")

    # ---------------------------------------------------------------- year effects
    out()
    out("## With year effects")
    out()
    yd = pd.get_dummies(pairs["year_t"], prefix="y", drop_first=True).astype(float)
    Xy = pd.concat([pairs[TERMS].reset_index(drop=True),
                    yd.reset_index(drop=True)], axis=1)
    ry = sm.OLS(pairs["dH"].to_numpy(), sm.add_constant(Xy.to_numpy())).fit(
        cov_type="cluster", cov_kwds={"groups": pairs[COUNTRY].to_numpy()})
    ciy = ry.conf_int()
    table(pd.DataFrame({
        "term": TERM_LABELS,
        "pooled": [round(res.params[i], 5) for i in (1, 2, 3)],
        "with year effects": [round(ry.params[i], 5) for i in (1, 2, 3)],
        "95% low": [round(ciy[i, 0], 5) for i in (1, 2, 3)],
        "95% high": [round(ciy[i, 1], 5) for i in (1, 2, 3)],
    }))
    out("Year effects absorb anything that moved global happiness in a given year — "
        "the pandemic being the obvious case. If the coefficients hold up, the result "
        "is not an artefact of a common time pattern.")

    # ---------------------------------------------------------------- figures
    out()
    out("## Figures")
    out()
    out("**Used in the report** — growth against healthy life expectancy, lines by "
        "level of happiness.")
    out()
    out("![sq3_growth_by_hle](figures/sq3_growth_by_hle.png)")
    out()
    out("*At a fixed level of happiness the model is linear in healthy life "
        "expectancy, so these are parallel straight lines with slope $a_2$.*")
    out()
    out("**Alternative, not used** — growth against happiness, curves by healthy life "
        "expectancy.")
    out()
    out("![sq3_growth](figures/sq3_growth.png)")
    out()
    out("*Curves slope downward: growth slows as happiness rises. With $E$ additive "
        "the three curves are vertical shifts of one another, and where each crosses "
        "zero is the equilibrium level at that healthy life expectancy.*")

    pairs.to_csv(OUTPUTS / "consecutive_pairs.csv", index=False)

    # Export the fitted coefficients so the phase portrait in 09 uses exactly the
    # numbers reported here, rather than refitting and risking a silent divergence.
    import json
    (OUTPUTS / "sq3_coefficients.json").write_text(json.dumps({
        "model": "dH = k + a0*H + a1*H^2 + a2*E",
        "k": float(res.params[0]), "a0": float(res.params[1]),
        "a1": float(res.params[2]), "a2": float(res.params[3]),
        "n": int(res.nobs), "countries": int(pairs[COUNTRY].nunique()),
    }, indent=2) + "\n")
    out()
    out("## Output")
    out()
    out(f"`outputs/consecutive_pairs.csv` — {len(pairs):,} rows, the paired sample.")

    for name in ("light", "dark"):
        figure_by_happiness(pairs, res, name)
        figure_by_life_expectancy(pairs, res, name)

    path = OUTPUTS / "sq3_growth.md"
    path.write_text("\n".join(lines) + "\n")
    print("\n".join(lines))
    print(f"\nWrote {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
