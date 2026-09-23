"""Chart styling shared by every figure in this analysis.

One place defines the palette, ink and mark geometry so all figures read as one system.
Colours are the validated default palette from the `dataviz` skill; the accessibility
validator output is recorded in `palette_validation.txt`.

Figures render twice - `outputs/figures/` on a light surface and `outputs/figures/dark/`
on a dark one - both opaque. An Obsidian vault may be read in either theme and a PNG
cannot adapt, while a transparent PNG with dark ink is illegible on a dark theme.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import textwrap

import matplotlib as mpl
import matplotlib.patheffects as pe
import matplotlib.pyplot as plt

CODE_DIR = Path(__file__).resolve().parent
FIGURES = CODE_DIR / "outputs" / "figures"
DPI = 200

# Point-label size. Figures are scaled to the note's pane width, so labels set
# for the raw PNG come out unreadable; this is sized for the rendered note.
ANNOT = 12


@dataclass(frozen=True)
class Theme:
    name: str
    surface: str
    text_primary: str
    text_secondary: str
    muted: str
    grid: str
    baseline: str
    series: list[str]


LIGHT = Theme("light", "#fcfcfb", "#0b0b0b", "#52514e", "#898781", "#e1e0d9",
              "#c3c2b7", ["#2a78d6", "#eb6834", "#1baf7a"])
DARK = Theme("dark", "#1a1a19", "#ffffff", "#c3c2b7", "#898781", "#2c2c2a",
             "#383835", ["#3987e5", "#d95926", "#199e70"])
THEMES = {"light": LIGHT, "dark": DARK}

_active: Theme = LIGHT


def theme() -> Theme:
    return _active


def use(name: str) -> Theme:
    """Activate a theme and apply it to matplotlib's global style."""
    global _active
    t = THEMES[name]
    _active = t
    mpl.rcParams.update({
        "figure.dpi": DPI, "savefig.dpi": DPI,
        "figure.facecolor": t.surface, "axes.facecolor": t.surface,
        "savefig.facecolor": t.surface, "savefig.transparent": False,
        "font.family": "sans-serif",
        "font.sans-serif": ["Helvetica Neue", "Helvetica", "Arial", "DejaVu Sans"],
        "font.size": 15,
        "text.color": t.text_primary,
        "axes.edgecolor": t.baseline, "axes.labelcolor": t.text_secondary,
        "axes.labelsize": 15, "axes.linewidth": 1.0,
        "axes.spines.top": False, "axes.spines.right": False,
        "axes.grid": True, "axes.axisbelow": True,
        # Solid hairline grid: dashed grids read as data.
        "grid.color": t.grid, "grid.linewidth": 0.7, "grid.linestyle": "-",
        "xtick.color": t.muted, "ytick.color": t.muted,
        "xtick.labelcolor": t.text_secondary, "ytick.labelcolor": t.text_secondary,
        "xtick.labelsize": 13, "ytick.labelsize": 13,
        "xtick.major.size": 0, "ytick.major.size": 0,
        "legend.frameon": False, "legend.fontsize": 13, "legend.title_fontsize": 13,
        "lines.linewidth": 2.0,
    })
    return t


def header(fig, headline: str) -> None:
    """Figure-level headline, flush left. Title only — no subtitle.

    Anchored to the figure rather than the axes so the text starts at the left edge
    instead of after the y-axis labels. Anything a subtitle would have said belongs
    in the caption beneath the figure, not inside the frame.
    """
    fig.text(0.004, 0.99, headline, ha="left", va="top", fontsize=18,
             fontweight="bold", color=_active.text_primary)


def label_extremes(ax, rows, xcol, ycol, text):
    """Label the extreme point on each axis, each with a leader line and a ring.

    `rows` maps a role — "min_x", "max_x", "min_y", "max_y" — to the row to label.
    Each label is thrown into the empty corner nearest its own extreme, so no two
    compete for the same space, and a leader line ties it to a ringed marker. At
    the type sizes these figures use, an unconnected label floats free of any
    point and the reader cannot tell which one it names.
    """
    place = {"min_x": (28, -22, "left"), "max_x": (-28, -22, "right"),
             "min_y": (28, -22, "left"), "max_y": (-28, 22, "right")}
    halo = [pe.withStroke(linewidth=2.6, foreground=_active.surface)]
    # Axis limits must already be final: a label thrown outward from a point near
    # the top or bottom lands on the tick labels, so it is flipped inward instead.
    y0, y1 = ax.get_ylim()
    span = (y1 - y0) or 1.0
    xs, ys = [], []
    for role, r in rows:
        dx, dy, ha = place[role]
        frac = (r[ycol] - y0) / span
        if dy < 0 and frac < 0.12:
            dy = -dy
        elif dy > 0 and frac > 0.88:
            dy = -dy
        ax.annotate(text(r), (r[xcol], r[ycol]), textcoords="offset points",
                    xytext=(dx, dy), fontsize=ANNOT, color=_active.text_secondary,
                    path_effects=halo, zorder=5, ha=ha, va="center",
                    arrowprops=dict(arrowstyle="-", lw=0.7, color=_active.muted,
                                    shrinkA=1, shrinkB=4))
        xs.append(r[xcol]); ys.append(r[ycol])
    ax.scatter(xs, ys, s=42, facecolor="none", edgecolors=_active.text_primary,
               linewidths=1.1, zorder=4)


def pick_extremes(d, xcol, ycol, namecol):
    """Rows for the four axis extremes, tagged by role, each country only once."""
    roles = [("min_x", d.nsmallest(1, xcol)), ("max_x", d.nlargest(1, xcol)),
             ("min_y", d.nsmallest(1, ycol)), ("max_y", d.nlargest(1, ycol))]
    seen, out = set(), []
    for role, row in roles:
        name = row[namecol].iloc[0]
        if name not in seen:
            seen.add(name)
            out.append((role, row.iloc[0]))
    return out


def layout(fig, top: float = 0.93) -> None:
    """Fit the axes into the figure, leaving room for the header and source note.

    The bottom margin is derived from how many lines the source note wrapped to,
    so a long note pushes the axes up instead of overprinting the x-axis label.
    """
    lines = getattr(fig, "_source_lines", 1)
    bottom = 0.012 + lines * (SOURCE_SIZE * 1.35 / 72) / fig.get_figheight()
    fig.tight_layout(rect=(0, bottom, 1, top))


SOURCE_SIZE = 10


def source_note(fig, text: str) -> None:
    """Source line under the figure, wrapped to the figure's own width.

    Saving with bbox_inches="tight" grows the canvas to fit any text that overruns
    it, so an unwrapped note silently stretches the figure — and every element in
    it then renders smaller once the image is scaled to the note's pane width.
    """
    chars = max(40, int(fig.get_figwidth() * 72 / (SOURCE_SIZE * 0.52)))
    wrapped = textwrap.fill(text, chars)
    fig.text(0.004, 0.004, wrapped, ha="left", va="bottom",
             fontsize=SOURCE_SIZE, color=_active.muted)
    # layout() reads this to reserve the right amount of room underneath.
    fig._source_lines = wrapped.count("\n") + 1


def save(fig, name: str) -> None:
    out = FIGURES if _active.name == "light" else FIGURES / "dark"
    out.mkdir(parents=True, exist_ok=True)
    path = out / f"{name}.png"
    fig.savefig(path, bbox_inches="tight", pad_inches=0.22,
                facecolor=_active.surface)
    plt.close(fig)
    print(f"  figure: {path.relative_to(CODE_DIR)}")
