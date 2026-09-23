"""Phase portrait of the two-variable system, after Ranganathan et al. (2014).

Run:      cd Code && uv run python 09_phase_portrait.py
Reads:    Code/outputs/consecutive_pairs.csv
          Code/outputs/sq3_coefficients.json, sq3b_coefficients.json
Produces: Code/outputs/phase_portrait.md
          Code/outputs/figures/{,dark/}phase_portrait.png

The two fitted models together form a dynamical system in the (E, H) plane:

    dH = kH + a0 H + a1 H^2 + a2 E
    dE = kE + b1 E + b2 E^2 + b3 H

At each point the pair (dE, dH) is a vector giving the direction and magnitude of one
year's expected movement. Drawing that vector on a grid is a phase portrait, the
approach of Ranganathan, Spaiser, Mann and Sumpter (2014), whose Figure 5 plots
democracy against log GDP per capita the same way.

Coefficients are read from the JSON written by 07 and 08 rather than refitted, so the
figure cannot silently diverge from the numbers reported in the appendix.

On reading the arrow angles. The components are plotted in data units, which means the
angle on the page reflects movement as a fraction of each plotted axis - the direction a
country moves *on this figure*. The two axes carry different units, so the angle is not
a ratio of years to ladder points.

On what is trustworthy. The vertical component is the change in happiness, a survey
measure that genuinely moves year to year. The horizontal component is the change in
healthy life expectancy, which the source interpolates - it is close to a country-level
constant and should not be read as measured movement. The vertical flow is the result;
the horizontal flow is largely an artefact of how the series was constructed.
"""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

import viz_style as vs

CODE_DIR = Path(__file__).resolve().parent
OUTPUTS = CODE_DIR / "outputs"

COUNTRY = "Country name"

lines: list[str] = []


def out(text: str = "") -> None:
    lines.append(text)


def table(df: pd.DataFrame) -> None:
    lines.append("")
    lines.append(df.to_markdown(index=False))
    lines.append("")


def load():
    d = pd.read_csv(OUTPUTS / "consecutive_pairs.csv")
    cH = json.loads((OUTPUTS / "sq3_coefficients.json").read_text())
    cE = json.loads((OUTPUTS / "sq3b_coefficients.json").read_text())
    return d, cH, cE


def dH_of(H, E, c):
    return c["k"] + c["a0"] * H + c["a1"] * H ** 2 + c["a2"] * E


def dE_of(H, E, c):
    return c["k"] + c["a1"] * E + c["a2"] * E ** 2 + c["a3"] * H


def fixed_point(cH, cE, E_rng, H_rng):
    """Where both changes vanish. Solved numerically on a fine grid, then refined."""
    Es = np.linspace(*E_rng, 2001)
    Hs = np.linspace(*H_rng, 2001)
    EE, HH = np.meshgrid(Es, Hs)
    resid = np.abs(dH_of(HH, EE, cH)) + np.abs(dE_of(HH, EE, cE))
    i = np.unravel_index(np.argmin(resid), resid.shape)
    return float(EE[i]), float(HH[i]), float(resid[i])


def trajectory(E0, H0, cH, cE, years=45):
    """Integrate the system forward with annual Euler steps, as the models are annual."""
    E, H = [E0], [H0]
    for _ in range(years):
        e, h = E[-1], H[-1]
        E.append(e + dE_of(h, e, cE))
        H.append(h + dH_of(h, e, cH))
    return np.array(E), np.array(H)


def figure(d, cH, cE, theme_name: str, fp) -> None:
    t = vs.use(theme_name)
    E_rng = (float(d["E"].min()) - 1, float(d["E"].max()) + 1)
    H_rng = (1.8, 8.4)

    fig, ax = plt.subplots(figsize=(8.0, 5.6))

    # Observed country-years, faint, for context.
    ax.scatter(d["E"], d["H"], s=8, color=t.muted, alpha=0.25, linewidths=0, zorder=1)

    # Vector field, drawn only where the data actually lies. Outside the cloud the
    # quadratics extrapolate hard and would draw confident arrows through empty space.
    Eg = np.linspace(E_rng[0] + 2, E_rng[1] - 2, 14)
    Hg = np.linspace(H_rng[0] + 0.5, H_rng[1] - 0.5, 11)
    EE, HH = np.meshgrid(Eg, Hg)
    near = np.zeros_like(EE, dtype=bool)
    for i in range(EE.shape[0]):
        for j in range(EE.shape[1]):
            near[i, j] = bool((
                (np.abs(d["E"] - EE[i, j]) < 2.6)
                & (np.abs(d["H"] - HH[i, j]) < 0.65)).any())
    EE, HH = EE[near], HH[near]
    U, V = dE_of(HH, EE, cE), dH_of(HH, EE, cH)

    # One magnification for both components, set so a typical arrow spans about 4% of
    # the vertical axis. Components stay in data units, so the angle on the page is
    # movement as a fraction of each plotted axis.
    H_span = H_rng[1] - H_rng[0]
    MAG = float(0.04 * H_span / np.median(np.abs(V)))
    ax.quiver(EE, HH, U * MAG, V * MAG, angles="xy", scale_units="xy", scale=1,
              width=0.0035, headwidth=4, headlength=5,
              color=t.text_secondary, alpha=0.8, zorder=3)

    # Nullclines: where each component alone vanishes.
    Ef = np.linspace(*E_rng, 400)
    a0, a1, a2, kH = cH["a0"], cH["a1"], cH["a2"], cH["k"]
    disc = a0 ** 2 - 4 * a1 * (kH + a2 * Ef)
    ok = disc >= 0
    H_null = (-a0 - np.sqrt(np.where(ok, disc, 0))) / (2 * a1)   # stable branch
    ax.plot(Ef[ok], H_null[ok], color=t.series[0], lw=2.2, zorder=4,
            label="stable $H$-nullcline ($\\Delta H = 0$)")

    # The health-unchanging curve exists only where dE can reach zero. On this fit it
    # cannot: dE is positive at every point in range, so the curve is not drawn.
    Hf = np.linspace(*H_rng, 400)
    b1, b2, b3, kE = cE["a1"], cE["a2"], cE["a3"], cE["k"]
    disc2 = b1 ** 2 - 4 * b2 * (kE + b3 * Hf)
    ok2 = disc2 >= 0
    if ok2.any():
        E_null = (-b1 - np.sqrt(np.where(ok2, disc2, 0))) / (2 * b2)
        ax.plot(E_null[ok2], Hf[ok2], color=t.series[1], lw=2.2, zorder=4,
                label="health unchanging ($\\Delta E = 0$)")

    # Trajectories from three real starting points.
    starts = []
    for name in ("Zimbabwe", "India", "Denmark"):
        s = d[d[COUNTRY] == name].nsmallest(1, "year_t")
        if not s.empty:
            starts.append((name, float(s["E"].iloc[0]), float(s["H"].iloc[0])))
    for name, E0, H0 in starts:
        Et, Ht = trajectory(E0, H0, cH, cE)
        ax.plot(Et, Ht, color=t.series[2], lw=1.4, ls="-", alpha=0.9, zorder=5)
        ax.plot([E0], [H0], "o", ms=6, color=t.series[2],
                markeredgecolor=t.surface, markeredgewidth=1.2, zorder=6)
        ax.annotate(name, (E0, H0), textcoords="offset points", xytext=(7, -10),
                    fontsize=vs.ANNOT, color=t.text_secondary, zorder=6)

    if fp is not None:
        ax.plot([fp[0]], [fp[1]], marker="*", ms=15, color=t.text_primary,
                markeredgecolor=t.surface, markeredgewidth=1.2, zorder=7)

    ax.set_xlim(*E_rng)
    ax.set_ylim(*H_rng)
    ax.set_xlabel("Healthy life expectancy at birth (years)")
    ax.set_ylabel("Happiness (life ladder, 0–10)")
    ax.legend(loc="lower right")
    vs.header(fig, "Phase portrait of happiness and healthy life expectancy")
    vs.source_note(fig, "Method after Ranganathan et al. (2014). Source: World "
                        "Happiness Report 2024 underlying panel (Helliwell et al., "
                        "2024a). The horizontal component rests on an interpolated "
                        "series — see the appendix.")
    vs.layout(fig, top=0.93)
    vs.save(fig, "phase_portrait")


def min_dE(cE, d):
    """Smallest fitted change in E across the observed country-years, and where."""
    dE = cE["k"] + cE["a1"] * d["E"] + cE["a2"] * d["E"] ** 2 + cE["a3"] * d["H"]
    i = dE.idxmin()
    return float(dE.loc[i]), float(d["E"].loc[i])


def main() -> int:
    d, cH, cE = load()
    E_rng = (float(d["E"].min()), float(d["E"].max()))
    H_rng = (float(d["H"].min()), float(d["H"].max()))
    fp = fixed_point(cH, cE, E_rng, H_rng)
    inside = fp[2] < 0.01

    out("# Phase portrait of the two-variable system")
    out()
    out("Generated by `Code/09_phase_portrait.py`. Method after Ranganathan et al. "
        "(2014), whose Figure 5 plots democracy against log GDP per capita in the same "
        "way.")

    out()
    out("## The system")
    out()
    out("The two fitted models together define a dynamical system in the "
        "$(E, H)$ plane:")
    out()
    out(f"$$\\Delta H = {cH['k']:+.4f} {cH['a0']:+.4f}\\,H {cH['a1']:+.4f}\\,H^2 "
        f"{cH['a2']:+.4f}\\,E$$")
    out()
    out(f"$$\\Delta E = {cE['k']:+.4f} {cE['a1']:+.4f}\\,E {cE['a2']:+.6f}\\,E^2 "
        f"{cE['a3']:+.4f}\\,H$$")
    out()
    out("Coefficients are read from the JSON written by `07_sq3_growth.py` and "
        "`08_sq3b_life_expectancy.py`, so the figure cannot diverge from the fits "
        "reported in the appendix.")

    out()
    out("## Fixed point")
    out()
    if inside:
        out(f"Both changes vanish at approximately **$E$ = {fp[0]:.1f} years, "
            f"$H$ = {fp[1]:.2f}** — located numerically on a fine grid; residual "
            f"{fp[2]:.2e}.")
        out()
        out("Read with care. This is where the two fitted curves cross, so it is the "
            "point the system would sit still at if both equations held exactly and "
            "nothing else changed over decades. It is an implication of two "
            "regressions fitted to sixteen years of data, not a destination anyone has "
            "observed.")
    else:
        out("The two curves do not cross within the observed data, so the system has "
            "no fixed point in the region the data covers. The best numerical residual "
            f"was {fp[2]:.3f} at $E$ = {fp[0]:.1f}, $H$ = {fp[1]:.2f}.")

    out()
    out("## What the curve means")
    out()
    out("- The blue curve is the **stable branch of the $H$-nullcline**, where the "
        "happiness component of the vector field vanishes. Above it happiness falls, "
        "below it rises, so trajectories are drawn to it *vertically*. It is the same "
        "relationship reported as the implied equilibrium in sub-question 3, which is "
        "an equilibrium of the happiness equation at a **fixed** healthy life "
        "expectancy.")
    out("- **It is not a curve on which happiness is unchanging.** A state sitting on "
        "it is only momentarily stationary in $H$. Because $\\Delta E > 0$ the state "
        "moves rightward, and because the curve rises with $E$ the state is then below "
        "it, so happiness resumes climbing. Motion along the nullcline is driven "
        "entirely by the change in healthy life expectancy — which is the component "
        "resting on an interpolated series.")
    dE_min, dE_at_E = min_dE(cE, d)
    out(f"- **There is no health-unchanging curve.** On this fit $\\Delta E$ is positive "
        f"at every point in the observed range — its minimum over the observed points is "
        f"{dE_min:+.2f} years per year, at $E \\approx {dE_at_E:.0f}$ — so healthy life "
        "expectancy never stops rising anywhere "
        "in the figure, and the curve is not drawn. That is exactly the behaviour a "
        "monotonically interpolated series produces, and it is the reason the system "
        "has no fixed point: the arrows always drift rightward.")

    out()
    out("## What is trustworthy in this figure")
    out()
    out("**The vertical flow is the result. The horizontal flow is largely an "
        "artefact.**")
    out()
    out("- Vertical movement is the change in happiness — a survey measure that "
        "genuinely varies year to year, with 96% of its variance within countries.")
    out("- Horizontal movement is the change in healthy life expectancy, which the "
        "source interpolates. It takes 152 distinct values across 1,874 country-years "
        "and 68% of its variance lies between countries. The arrows therefore drift "
        "rightward at a rate set mostly by how the series was constructed, not by "
        "anything happening in those countries.")
    out()
    out("The consequence for the trajectories is direct: their vertical path carries "
        "meaning, their horizontal path carries the interpolation. A reader should take "
        "them as an illustration of the fitted system, not a forecast.")

    out()
    out("## Figure")
    out()
    out("![phase_portrait](figures/phase_portrait.png)")
    out()
    out("*Arrows are one year of expected movement. Because the axes "
        "carry different units, the angle shows the direction of travel on the figure "
        "rather than a ratio of years to ladder points.*")

    out()
    out("## Reference")
    out()
    out("Ranganathan, S., Spaiser, V., Mann, R. P., & Sumpter, D. J. T. (2014). "
        "Bayesian dynamical systems modelling in the social sciences. *PLoS ONE*, "
        "9(1), e86468. "
        "[https://doi.org/10.1371/journal.pone.0086468]"
        "(https://doi.org/10.1371/journal.pone.0086468)")

    figure(d, cH, cE, "light", fp if inside else None)
    figure(d, cH, cE, "dark", fp if inside else None)

    path = OUTPUTS / "phase_portrait.md"
    path.write_text("\n".join(lines) + "\n")
    print("\n".join(lines))
    print(f"\nWrote {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
