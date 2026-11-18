"""Step 4 checks needing both equations, plus the replication comparison for dG.

  1. How firmly democracy enters dG: best model with no democracy term
     (subsets of 1, G, 1/G, G^2, 1/G^2) against the selected model, by evidence.
  2. Cross-equation error correlation of the two selected models, and the iterated
     seemingly-unrelated-regressions (feasible GLS) re-estimate of their coefficients
     (Ranganathan et al. 2014). Appendix only unless it changes the answer.
  3. The 2013 paper's dG model (D, G, G^2) on our data (replication; appendix only).

Reads outputs/panel.csv, outputs/06_fit_D.json, outputs/06_fit_G.json.
Writes outputs/07_joint_checks.txt.
"""
import itertools
import json
import sys

import numpy as np

from sds_common import OUT, load_panel

TERMS = ["1", "D", "G", "1/G", "D/G", "DG", "D^2", "G^2", "1/G^2"]
import pandas as pd
MEASURE = sys.argv[1] if len(sys.argv) > 1 else "welzel"   # "welzel" (main) or "vdem" (question 2)
TAG = "" if MEASURE == "welzel" else "_vdem"
if MEASURE == "welzel":
    p = load_panel()
    ch = p.dropna(subset=["dD", "dG"]).reset_index(drop=True)
else:
    p = pd.read_csv(OUT / "panel_vdem.csv")
    ch = p[p.period == "fit"].dropna(subset=["dD", "dG"]).reset_index(drop=True)
D, G = ch.D.values, ch.G.values
X = np.column_stack([np.ones_like(D), D, G, 1 / G, D / G, D * G, D ** 2, G ** 2, 1 / G ** 2])
rms = np.sqrt((X ** 2).mean(axis=0))
fits = {o: json.load(open(OUT / f"06_fit_{o}{TAG}.json")) for o in ("D", "G")}
lines = []


def evidence(idx, y):
    n, sig = len(y), y.std(ddof=1)
    lam = sig
    Xs = X[:, idx] / rms[idx]
    A, b = Xs.T @ Xs, Xs.T @ y
    M = A + (sig / lam) ** 2 * np.eye(len(idx))
    _, ld = np.linalg.slogdet(np.eye(len(idx)) + (lam / sig) ** 2 * A)
    le = -0.5 * n * np.log(2 * np.pi * sig ** 2) - 0.5 * ld - 0.5 * (y @ y - b @ np.linalg.solve(M, b)) / sig ** 2
    mu = np.linalg.solve(M, b) / rms[idx]
    sd = np.sqrt(np.diag(sig ** 2 * np.linalg.inv(M))) / rms[idx]
    return le, mu, sd


# 1. democracy in dG
yG = ch.dG.values
noD = [TERMS.index(t) for t in ["1", "G", "1/G", "G^2", "1/G^2"]]
best = max((evidence(list(S), yG)[0], S) for m in range(1, 6)
           for S in itertools.combinations(noD, m))
sel_G = fits["G"]["sizes"][str(fits["G"]["selected_size"])]
lines += ["1. Democracy in the dG equation",
          f"  selected model log-evidence {sel_G['logev']:.2f} ({', '.join(sel_G['terms'])})",
          f"  best model with no democracy term: {', '.join(TERMS[i] for i in best[1])}, "
          f"log-evidence {best[0]:.2f}",
          f"  log Bayes factor for including democracy: {sel_G['logev'] - best[0]:.2f}", ""]

# 2. cross-equation correlation and SUR
idx = {o: [TERMS.index(t) for t in fits[o]["sizes"][str(fits[o]["selected_size"])]["terms"]]
       for o in ("D", "G")}
Y = {"D": ch.dD.values, "G": yG}
beta = {o: np.linalg.lstsq(X[:, idx[o]], Y[o], rcond=None)[0] for o in ("D", "G")}
ols = {o: beta[o].copy() for o in beta}
res = {o: Y[o] - X[:, idx[o]] @ beta[o] for o in beta}
rho0 = np.corrcoef(res["D"], res["G"])[0, 1]
n = len(yG)
for it in range(50):
    S = np.cov(np.vstack([res["D"], res["G"]]), bias=True)
    Si = np.linalg.inv(S)
    XD, XG = X[:, idx["D"]], X[:, idx["G"]]
    kD = XD.shape[1]
    top = np.hstack([Si[0, 0] * XD.T @ XD, Si[0, 1] * XD.T @ XG])
    bot = np.hstack([Si[1, 0] * XG.T @ XD, Si[1, 1] * XG.T @ XG])
    rhs = np.concatenate([Si[0, 0] * XD.T @ Y["D"] + Si[0, 1] * XD.T @ Y["G"],
                          Si[1, 0] * XG.T @ Y["D"] + Si[1, 1] * XG.T @ Y["G"]])
    b = np.linalg.solve(np.vstack([top, bot]), rhs)
    new = {"D": b[:kD], "G": b[kD:]}
    done = all(np.allclose(new[o], beta[o], rtol=1e-10, atol=1e-14) for o in beta)
    beta = new
    res = {o: Y[o] - X[:, idx[o]] @ beta[o] for o in beta}
    if done:
        break
lines += ["2. Cross-equation errors (selected models)",
          f"  residual correlation dD vs dG: {rho0:+.3f}",
          f"  iterated SUR converged after {it + 1} iterations; coefficients OLS -> SUR:"]
for o in ("D", "G"):
    for t, a, c in zip([TERMS[i] for i in idx[o]], ols[o], beta[o]):
        lines.append(f"    d{o} {t:<6} {a:+.5f} -> {c:+.5f}  ({100 * (c - a) / abs(a):+.1f}%)")
lines.append("")

# 3. paper's dG model (main analysis only)
if MEASURE != "welzel":
    text = "\n".join(lines); print(text)
    (OUT / f"07_joint_checks{TAG}.txt").write_text(text + "\n"); sys.exit(0)
pidx = [TERMS.index(t) for t in ["D", "G", "G^2"]]
le, mu, sd = evidence(pidx, yG)
lines += ["3. Ranganathan, Spaiser and Sumpter (2013) dG model (D, G, G^2) on our data",
          *[f"  {t:<4} {m:+.5f} [{m - 1.96 * s:+.5f}, {m + 1.96 * s:+.5f}]"
            for t, m, s in zip(["D", "G", "G^2"], mu, sd)],
          "  paper's coefficients converted to our scale: D +0.00205, G +0.0017, G^2 -0.0024",
          f"  log-evidence {le:.2f} vs selected {sel_G['logev']:.2f}: log Bayes factor "
          f"{sel_G['logev'] - le:.2f} in favour of the selected model"]
text = "\n".join(lines)
print(text)
(OUT / "07_joint_checks.txt").write_text(text + "\n")
