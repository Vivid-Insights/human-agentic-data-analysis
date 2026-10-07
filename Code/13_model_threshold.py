"""Sub-questions 1 and 2 — logistic models of heavy loss against log income.

For each outcome a country is coded 1 if its cumulative 2001-2024 loss share
exceeds a threshold, and the log odds of that are modelled as a quadratic in log
GDP per capita:

    logit P(share > T) = b0 + b1 * log_gdp + b2 * log_gdp^2

The quadratic term is what permits an inverted U. The logit is monotone in the
probability, so the income at which the log odds peak is the income at which the
probability peaks, and the step-2 criterion — that the turning point lie inside
the observed income range — applies to it unchanged.

Thresholds differ between the outcomes on purpose. The medians are 0.013 and
0.106, so one cut would sit in the upper tail of one outcome and the lower tail
of the other. 0.02 and 0.10 each fall near their own median, which is what makes
the two models answer the same question.

Three things are computed beyond the coefficients:

  * The turning point, with a Fieller interval. It is a ratio of coefficients, so
    a delta-method interval understates the uncertainty when the denominator is
    not comfortably away from zero; both are reported and the Fieller one is the
    one quoted.
  * The Lind-Mehlum joint condition. A significant quadratic term is not evidence
    of a turning point inside the data: a curve can decelerate throughout. The
    test requires the slope to be positive at the bottom of the observed range and
    negative at the top, and takes the larger of the two one-sided p-values.
  * The turning point again, found by searching the fitted probability on a grid
    rather than solving the formula, as an independent route to the same number.
  * A linear specification of the same model, and the rank correlation on the
    continuous outcome. Finding no inverted U leaves open whether there is a
    straight-line relationship, and these two answer that. The correlation also
    answers it without the threshold, so a null in the logistic that was really an
    artefact of dichotomising would show up as a disagreement between them.

Reads  outputs/analysis_dataset.csv
Writes outputs/model_threshold.csv   (coefficients and fit statistics)
       outputs/model_threshold.json  (everything the report quotes)
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.api as sm
from scipy import stats

HERE = Path(__file__).resolve().parent
OUT = HERE / "outputs"

XCOL = "log_gdp_pc_mean"
SPECS = [
    ("sub_question_1", "permanent_loss_share", 0.02, "Permanent conversion"),
    ("sub_question_2", "total_loss_share", 0.10, "All tree cover loss"),
]


def fieller(b1: float, b2: float, V: np.ndarray, level: float = 0.95) -> tuple:
    """Fieller interval for the turning point -b1 / (2 b2).

    Solves the quadratic in x arising from |b1 + 2 b2 x| <= z * se(b1 + 2 b2 x).
    Returns (lo, hi), either of which may be nan when the interval is unbounded —
    which is itself the answer when the data cannot locate the turning point.
    """
    z = stats.norm.ppf(1 - (1 - level) / 2)
    v11, v12, v22 = V[0, 0], V[0, 1], V[1, 1]
    # (b1 + 2 b2 x)^2 = z^2 (v11 + 4 x v12 + 4 x^2 v22)
    A = 4 * b2**2 - 4 * z**2 * v22
    B = 4 * b1 * b2 - 4 * z**2 * v12
    C = b1**2 - z**2 * v11
    if A == 0:
        return (np.nan, np.nan)
    disc = B**2 - 4 * A * C
    if disc < 0 or A < 0:
        return (np.nan, np.nan)   # unbounded: the turning point is not located
    r = np.sqrt(disc)
    roots = sorted([(-B - r) / (2 * A), (-B + r) / (2 * A)])
    return (-roots[1], -roots[0])


def fit_one(d: pd.DataFrame, key: str, col: str, thr: float, label: str) -> dict:
    y = (d[col] > thr).astype(int)
    x = d[XCOL].to_numpy()
    X = sm.add_constant(np.column_stack([x, x**2]))
    m = sm.Logit(y, X).fit(disp=0)
    b0, b1, b2 = np.asarray(m.params)
    # statsmodels returns these as pandas objects here; fix the type once.
    V = np.asarray(m.cov_params())[1:, 1:]

    xlo, xhi = x.min(), x.max()
    star = -b1 / (2 * b2)

    # A negative quadratic turns at a maximum, a positive one at a minimum. The
    # step-2 criterion is about an inverted U, so the sign decides whether the
    # turning point is the peak the question asks about or its opposite.
    shape = "maximum" if b2 < 0 else "minimum"

    # Independent route to the same number: search the fitted probability for the
    # turning point of the relevant kind, rather than assuming a maximum.
    grid = np.linspace(xlo, xhi, 200_001)
    p = 1 / (1 + np.exp(-(b0 + b1 * grid + b2 * grid**2)))
    star_grid = grid[int(np.argmax(p) if b2 < 0 else np.argmin(p))]

    # Delta method, for comparison with the Fieller interval.
    g = np.array([-1 / (2 * b2), b1 / (2 * b2**2)])
    se_star = float(np.sqrt(g @ V @ g))
    lo_d, hi_d = star - 1.96 * se_star, star + 1.96 * se_star
    lo_f, hi_f = fieller(b1, b2, V)

    # Lind-Mehlum: slope positive at the bottom of the range and negative at the
    # top. Intersection-union, so the joint p-value is the larger of the two.
    def slope(xv):
        est = b1 + 2 * b2 * xv
        g2 = np.array([1.0, 2 * xv])
        return est, float(np.sqrt(g2 @ V @ g2))

    s_lo, se_lo = slope(xlo)
    s_hi, se_hi = slope(xhi)
    p_lo = stats.norm.sf(s_lo / se_lo)        # H1: slope > 0 at the bottom
    p_hi = stats.norm.cdf(s_hi / se_hi)       # H1: slope < 0 at the top
    p_joint = max(p_lo, p_hi)

    interior = bool(xlo < star < xhi)
    ci = np.asarray(m.conf_int())
    res = {
        "key": key, "label": label, "outcome": col, "threshold": thr,
        "n": int(len(y)), "n_above": int(y.sum()), "n_below": int(len(y) - y.sum()),
        "converged": bool(m.mle_retvals["converged"]),
        "llf": float(m.llf), "llnull": float(m.llnull),
        "pseudo_r2": float(m.prsquared),
        "lr_p": float(m.llr_pvalue),
        "coefs": {n: {"est": float(v), "se": float(se), "z": float(zz), "p": float(pp),
                      "lo": float(c0), "hi": float(c1)}
                  for n, v, se, zz, pp, c0, c1 in zip(
                      ["const", "log_gdp", "log_gdp_sq"], np.asarray(m.params),
                      np.asarray(m.bse), np.asarray(m.tvalues), np.asarray(m.pvalues),
                      ci[:, 0], ci[:, 1])},
        "turning_point": {
            "log_gdp": float(star), "usd": float(np.exp(star)),
            "usd_grid_check": float(np.exp(star_grid)),
            "delta_lo_usd": float(np.exp(lo_d)), "delta_hi_usd": float(np.exp(hi_d)),
            "fieller_lo_usd": float(np.exp(lo_f)) if np.isfinite(lo_f) else None,
            "fieller_hi_usd": float(np.exp(hi_f)) if np.isfinite(hi_f) else None,
            "interior": interior, "shape": shape,
            "range_lo_usd": float(np.exp(xlo)), "range_hi_usd": float(np.exp(xhi)),
        },
        "lind_mehlum": {
            "slope_lo": float(s_lo), "se_lo": float(se_lo), "p_lo": float(p_lo),
            "slope_hi": float(s_hi), "se_hi": float(se_hi), "p_hi": float(p_hi),
            "p_joint": float(p_joint),
        },
        "fitted_p_at_turning_point": float(1 / (1 + np.exp(-(b0 + b1 * star + b2 * star**2)))),
        "fitted_p_range": [float(p.min()), float(p.max())],
    }

    # Linear specification: is there a monotone relationship, having found no
    # inverted U? Reported alongside the quadratic.
    X1 = sm.add_constant(x)
    m1 = sm.Logit(y, X1).fit(disp=0)
    ci1 = np.asarray(m1.conf_int())
    b1l = float(np.asarray(m1.params)[1])
    res["linear"] = {
        "slope": b1l, "se": float(np.asarray(m1.bse)[1]),
        "lo": float(ci1[1, 0]), "hi": float(ci1[1, 1]),
        "p": float(np.asarray(m1.pvalues)[1]),
        "or_per_doubling": float(np.exp(b1l * np.log(2))),
        "or_lo": float(np.exp(ci1[1, 0] * np.log(2))),
        "or_hi": float(np.exp(ci1[1, 1] * np.log(2))),
        "lr_p": float(m1.llr_pvalue), "pseudo_r2": float(m1.prsquared),
    }

    # The same question without the threshold, on the continuous outcome. Spearman
    # because the share is bounded and skewed; it assumes monotonicity only.
    sp = stats.spearmanr(d[col], x)
    res["correlation"] = {"spearman_rho": float(sp.statistic), "spearman_p": float(sp.pvalue),
                          "n": int(len(x))}

    # Diagnostic: does a cubic term change the picture? Reported in the appendix.
    X3 = sm.add_constant(np.column_stack([x, x**2, x**3]))
    m3 = sm.Logit(y, X3).fit(disp=0)
    lr = 2 * (m3.llf - m.llf)
    res["cubic_check"] = {"lr_stat": float(lr),
                          "p": float(stats.chi2.sf(lr, 1)),
                          "converged": bool(m3.mle_retvals["converged"])}
    return res


def main() -> None:
    d = pd.read_csv(OUT / "analysis_dataset.csv")
    results = [fit_one(d, *s) for s in SPECS]

    for r in results:
        tp = r["turning_point"]
        lm = r["lind_mehlum"]
        print(f"\n=== {r['label']}  (> {r['threshold']}) ===")
        print(f"  n {r['n']}  above {r['n_above']}  below {r['n_below']}"
              f"  converged {r['converged']}  pseudo-R2 {r['pseudo_r2']:.3f}")
        for n, c in r["coefs"].items():
            print(f"  {n:<11} {c['est']:>9.3f}  95% CI [{c['lo']:.3f}, {c['hi']:.3f}]"
                  f"  p {c['p']:.3g}")
        print(f"  model fit: LR p {r['lr_p']:.3g}")
        print(f"  turning point ({tp['shape']})  ${tp['usd']:,.0f}"
              f"   grid check ${tp['usd_grid_check']:,.0f}")
        if tp["fieller_lo_usd"] is None:
            print("  Fieller 95% interval: unbounded — the turning point is not located")
        else:
            print(f"  Fieller 95%  [${tp['fieller_lo_usd']:,.0f}, ${tp['fieller_hi_usd']:,.0f}]")
        print(f"  delta  95%   [${tp['delta_lo_usd']:,.0f}, ${tp['delta_hi_usd']:,.0f}]")
        print(f"  observed income range  ${tp['range_lo_usd']:,.0f} to ${tp['range_hi_usd']:,.0f}"
              f"   interior: {tp['interior']}")
        print(f"  Lind-Mehlum  slope at bottom {lm['slope_lo']:+.3f} (p {lm['p_lo']:.3g}), "
              f"at top {lm['slope_hi']:+.3f} (p {lm['p_hi']:.3g})  joint p {lm['p_joint']:.3g}")
        print(f"  fitted probability at the turning point {r['fitted_p_at_turning_point']:.3f}"
              f"   across the range {r['fitted_p_range'][0]:.3f} to {r['fitted_p_range'][1]:.3f}")
        li, co = r["linear"], r["correlation"]
        print(f"  linear-only slope {li['slope']:+.3f}  95% CI [{li['lo']:+.3f}, {li['hi']:+.3f}]"
              f"  p {li['p']:.3g}   OR per doubling {li['or_per_doubling']:.3f}"
              f" [{li['or_lo']:.3f}, {li['or_hi']:.3f}]")
        print(f"  Spearman on the continuous outcome  rho {co['spearman_rho']:+.3f}  p {co['spearman_p']:.3g}")
        print(f"  cubic term: LR {r['cubic_check']['lr_stat']:.2f}, p {r['cubic_check']['p']:.3g}")

    (OUT / "model_threshold.json").write_text(json.dumps(results, indent=2))
    rows = []
    for r in results:
        for n, c in r["coefs"].items():
            rows.append({"key": r["key"], "outcome": r["outcome"],
                         "threshold": r["threshold"], "term": n, **c})
    pd.DataFrame(rows).to_csv(OUT / "model_threshold.csv", index=False)
    print(f"\n  wrote outputs/model_threshold.json and .csv")


if __name__ == "__main__":
    main()
