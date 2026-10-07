"""Threshold sensitivity for sub-question 1.

The headline model cuts permanent conversion at 0.02, a threshold chosen after
seeing the distribution. This refits across a grid of thresholds so a reader can
see how much of the answer rests on that choice.

Ten thresholds spaced logarithmically from 0.005 to 0.05, which brackets the
headline cut of 0.02 and spans from well below the median of 0.0134 to roughly
three times it. Log spacing because the outcome is skewed. For each threshold,
the straight-line logistic model of the log odds against log income, and the
quadratic with its joint condition.

The degenerate and small-cell checks below are kept even though every threshold
in this range leaves plenty of countries on both sides. They cost nothing and
they are what would catch a later widening of the grid past the sample maximum
of 0.3198, where there is no longer anything to fit.

Reads  outputs/analysis_dataset.csv
Writes outputs/threshold_sensitivity.csv
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.api as sm
from scipy import stats

HERE = Path(__file__).resolve().parent
OUT = HERE / "outputs"

COL = "permanent_loss_share"
XCOL = "log_gdp_pc_mean"
LO, HI, N = 0.005, 0.05, 10
HEADLINE = 0.02          # the threshold the report uses
MIN_CELL = 5             # below this, a logistic fit is not worth quoting


def fit(y: np.ndarray, x: np.ndarray) -> dict:
    out: dict = {}
    m = sm.Logit(y, sm.add_constant(x)).fit(disp=0)
    ci = np.asarray(m.conf_int())
    out["slope"] = float(np.asarray(m.params)[1])
    out["lo"] = float(ci[1, 0])
    out["hi"] = float(ci[1, 1])
    out["p"] = float(np.asarray(m.pvalues)[1])
    out["converged"] = bool(m.mle_retvals["converged"])

    # Quadratic and the joint condition, to see whether an inverted U ever
    # becomes supportable at some other cut.
    X = sm.add_constant(np.column_stack([x, x**2]))
    m2 = sm.Logit(y, X).fit(disp=0)
    b = np.asarray(m2.params)
    V = np.asarray(m2.cov_params())[1:, 1:]
    ps = []
    for xv, tail in [(x.min(), "lo"), (x.max(), "hi")]:
        est = b[1] + 2 * b[2] * xv
        g = np.array([1.0, 2 * xv])
        se = float(np.sqrt(g @ V @ g))
        ps.append(stats.norm.sf(est / se) if tail == "lo" else stats.norm.cdf(est / se))
    out["joint_p"] = float(max(ps))
    out["b2"] = float(b[2])
    return out


def main() -> None:
    d = pd.read_csv(OUT / "analysis_dataset.csv")
    x = d[XCOL].to_numpy()
    grid = np.geomspace(LO, HI, N)

    rows = []
    for thr in grid:
        y = (d[COL] > thr).astype(int).to_numpy()
        n_above = int(y.sum())
        row = {"threshold": float(thr), "n": len(y), "n_above": n_above,
               "n_below": int(len(y) - n_above),
               "pct_above": round(100 * n_above / len(y), 1)}
        if n_above == 0 or n_above == len(y):
            row["status"] = "degenerate: no variation in the outcome"
        elif n_above < MIN_CELL:
            row["status"] = f"too few above ({n_above}) to quote a fit"
            row.update(fit(y, x))
        else:
            row["status"] = "ok"
            row.update(fit(y, x))
        rows.append(row)

    r = pd.DataFrame(rows)
    r.to_csv(OUT / "threshold_sensitivity.csv", index=False)

    print(f"  outcome `{COL}`: max {d[COL].max():.4f}, median {d[COL].median():.4f}")
    print(f"  {N} thresholds, log-spaced from {LO} to {HI}\n")
    print(f"  {'thr':>7} {'above':>6} {'%':>6} {'slope':>8} {'95% CI':>20} "
          f"{'p':>10} {'joint p':>8}  status")
    for _, v in r.iterrows():
        if pd.isna(v.get("slope")):
            print(f"  {v.threshold:>7.4f} {v.n_above:>6} {v.pct_above:>6.1f} "
                  f"{'—':>8} {'—':>20} {'—':>10} {'—':>8}  {v.status}")
        else:
            print(f"  {v.threshold:>7.4f} {v.n_above:>6} {v.pct_above:>6.1f} "
                  f"{v.slope:>+8.3f} {f'[{v.lo:+.3f}, {v.hi:+.3f}]':>20} "
                  f"{v.p:>10.2e} {v.joint_p:>8.3f}  {v.status}")

    ok = r[r.status == "ok"]
    neg = ok[(ok.hi < 0)]
    print(f"\n  fits worth quoting: {len(ok)} of {N}")
    print(f"  of those, slope negative with the whole 95% interval below zero: {len(neg)}")
    if len(ok):
        print(f"  slope ranges from {ok.slope.min():+.3f} to {ok.slope.max():+.3f}")
        print(f"  largest p-value among them: {ok.p.max():.2e}")
        print(f"  joint condition for an inverted U met at any threshold "
              f"(p < 0.05): {bool((ok.joint_p < 0.05).any())}; "
              f"smallest joint p {ok.joint_p.min():.3f}")
    print(f"\n  headline threshold {HEADLINE} is in the grid: "
          f"{bool(np.isclose(grid, HEADLINE).any())}")
    print(f"  wrote outputs/threshold_sensitivity.csv")


if __name__ == "__main__":
    main()
