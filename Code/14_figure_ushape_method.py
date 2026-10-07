"""Methods figure — how the inverted-U test works.

Illustrative only. The two curves are drawn from chosen coefficients, not fitted
to anything, and no number in this figure comes from the data. It exists because
the test the analysis uses is not one a general reader will know, and the thing
it turns on is easy to state and easy to miss: a negative quadratic coefficient
says the curve bends, not that it turns inside the range you observed.

Left panel: the curve turns within the observed range. The slope is positive at
the low end and negative at the high end, so the relationship rises and then
falls where there is data, and an inverted U is supported.

Right panel: the same shape of curve, positioned so its peak lies below the
lowest income observed. The quadratic coefficient is negative here too, and a
test of that coefficient alone would be satisfied. But both end slopes are
negative: across the observed range the relationship only falls. This is the case
the joint condition is there to separate out, and it is the case our first
sub-question turned out to be.

Reads  nothing
Writes outputs/figures/fig_ushape_test.png  (and dark/)
"""

from __future__ import annotations

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np

import viz_style as vs

# Chosen, not estimated. Each panel is y = a (x - peak)^2 + c on x in [0, 1],
# where x stands for log income. The peak of the left curve sits inside that
# interval and the peak of the right curve sits to the left of it.
PANELS = [
    {"peak": 0.45, "a": -6.0, "c": 1.5,
     "title": "The curve turns inside the range",
     "note": "an inverted U is supported"},
    {"peak": -0.40, "a": -2.0, "c": 2.0,
     "title": "The curve bends but does not turn",
     "note": "reported as a decline"},
]

HEADLINE = "How an inverted U is tested"
XLABEL = "Log income $x$, from the lowest to the highest observed"
YLABEL = "Log odds of heavy forest loss\n$\\beta_0 + \\beta_1 x + \\beta_2 x^2$"
SOURCE = (
    "Illustrative curves, not data: both are drawn from chosen coefficients and nothing here is "
    "fitted or measured. Each panel shows a quadratic in log income with a negative squared term, "
    "so a test of that coefficient alone would be satisfied by either. The joint condition asks "
    "instead for the slope to be positive at the low end of the observed range and negative at the "
    "high end — that is, for $b_1 + 2 b_2 x$ to change sign within it — which only the left panel "
    "meets."
)


def draw(theme_name: str) -> None:
    t = vs.use(theme_name)
    # Mathtext in the sans face the rest of the figure uses, so the algebra does
    # not arrive in a serif font that reads as a different document.
    mpl.rcParams["mathtext.fontset"] = "dejavusans"
    fig, axes = plt.subplots(1, 2, figsize=(11.4, 5.0), sharey=True)

    x = np.linspace(0, 1, 400)
    tangent = t.series[2]

    # Shared limits, computed from the curves and their tangents so a sign label
    # cannot land on the axis edge. Saving to a tight box would otherwise grow the
    # canvas around it and shrink everything else once the image is scaled.
    ext = []
    for spec in PANELS:
        a, peak, c = spec["a"], spec["peak"], spec["c"]
        yy = a * (x - peak) ** 2 + c
        ext += [yy.min(), yy.max()]
        for x0 in (0.0, 1.0):
            sl = 2 * a * (x0 - peak)
            y0 = a * (x0 - peak) ** 2 + c
            ext += [y0 - sl * 0.16, y0 + sl * 0.16]
    lo, hi = min(ext), max(ext)
    # Asymmetric: the negative-slope signs hang below their tangents, and the
    # lowest of them sits at the bottom-right corner of the right-hand panel.
    pad_lo, pad_hi = 0.34 * (hi - lo), 0.14 * (hi - lo)

    for ax, spec in zip(axes, PANELS):
        a, peak, c = spec["a"], spec["peak"], spec["c"]
        y = a * (x - peak) ** 2 + c
        ax.plot(x, y, color=t.text_primary, lw=2.4, zorder=4)

        # Short tangents at each end: the two quantities the joint condition tests.
        for x0 in (0.0, 1.0):
            slope = 2 * a * (x0 - peak)
            y0 = a * (x0 - peak) ** 2 + c
            dx = 0.16
            xs = np.array([x0 - dx, x0 + dx])
            ax.plot(xs, y0 + slope * (xs - x0), color=tangent, lw=2.6,
                    solid_capstyle="round", zorder=5,
                    label=r"Slope $\beta_1 + 2\beta_2 x$" if x0 == 0.0 else None)
            # Sign sits just beyond the outer end of its own tangent, on the side
            # the tangent points, so it reads as belonging to that segment.
            xe = x0 - dx if x0 == 0.0 else x0 + dx
            ye = y0 + slope * (xe - x0)
            ax.annotate("+" if slope > 0 else "−", (xe, ye), textcoords="offset points",
                        xytext=(-14 if x0 == 0.0 else 14, 14 if slope > 0 else -16),
                        ha="center", va="center", fontsize=20, color=tangent, zorder=6)

        # Where the slope is zero. Inside the range it can be drawn; outside it,
        # saying so is the whole content of the right-hand panel.
        if 0 <= peak <= 1:
            ax.axvline(peak, color=t.muted, lw=1.0, zorder=2)
            ax.plot([peak], [c], marker="o", ms=8, color=t.text_primary, zorder=6)

            ax.annotate(r"$x^* = -\beta_1 / 2\beta_2$", (peak, lo - pad_lo),
                        textcoords="offset points", xytext=(0, 16), ha="center",
                        va="bottom", fontsize=13, color=t.text_secondary, zorder=6)
        else:
            ax.annotate(r"$x^*$ lies below the range", (0.0, lo - pad_lo),
                        textcoords="offset points", xytext=(6, 16), ha="left",
                        va="bottom", fontsize=13, color=t.text_secondary, zorder=6)

        ax.set_title(f"{spec['title']}\n{spec['note']}", fontsize=14,
                     color=t.text_primary, pad=10, linespacing=1.5)
        ax.set_xlim(-0.22, 1.22)
        ax.set_ylim(lo - pad_lo, hi + pad_hi)
        # The ends of the observed range, which is what the test is evaluated at.
        # The tangents deliberately overrun them, so without these a reader cannot
        # see where the data stops and the extrapolation starts.
        ax.set_xticks([0.0, 1.0])
        ax.set_xticklabels([r"$x_{\mathrm{lo}}$", r"$x_{\mathrm{hi}}$"])
        ax.set_yticks([])
        ax.grid(False)

    axes[0].set_ylabel(YLABEL, fontsize=13)
    # Upper left of the left panel: the only corner of either panel that is clear
    # of a curve, a tangent and the x* label beneath the turning point.
    axes[0].legend(loc="upper left", fontsize=12, borderaxespad=0.6)

    vs.header(fig, HEADLINE)
    vs.source_note(fig, SOURCE)
    lines = getattr(fig, "_source_lines", 1)
    note_h = 0.012 + lines * (vs.SOURCE_SIZE * 1.35 / 72) / fig.get_figheight()
    label_y = note_h + 0.02
    fig.text(0.5, label_y, XLABEL, ha="center", va="bottom",
             fontsize=14, color=t.text_secondary)
    fig.tight_layout(rect=(0, label_y + 0.07, 1, 0.91))
    vs.save(fig, "fig_ushape_test")


def main() -> None:
    for spec in PANELS:
        a, peak = spec["a"], spec["peak"]
        lo, hi = 2 * a * (0.0 - peak), 2 * a * (1.0 - peak)
        print(f"  {spec['title']}: peak at x = {peak:+.2f}; "
              f"slope at 0 {lo:+.2f}, at 1 {hi:+.2f}")
    for theme_name in ("light", "dark"):
        draw(theme_name)


if __name__ == "__main__":
    main()
