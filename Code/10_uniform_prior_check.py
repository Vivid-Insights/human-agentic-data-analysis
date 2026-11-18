"""Sensitivity check: does a uniform prior (as in Ranganathan et al. 2013) change the
selected models? Appendix only unless it changes the answer.

Stage 1 (best model of each size by likelihood) does not depend on the prior, so the
same best-per-size models from 06_fit_change_model.py are compared by evidence under a
uniform prior on each RMS-scaled coefficient, w_k ~ U(-a, a). sigma is fixed at sd(dx)
as before. With a Gaussian likelihood in w,

  log Z = log L_max + (m/2) log 2pi - 1/2 log|H| + log P(w in box) - m log(2a),

H = X_s'X_s / sigma^2, w ~ N(w_hat, H^-1); P(w in box) by Monte Carlo (200,000 draws,
seed 20261118). Widths: a = sqrt(3) * lambda (same variance as the normal prior),
10x and 100x that, lambda = sd(dx).

Writes outputs/10_uniform_prior_check.txt.
"""
import json

import numpy as np

from sds_common import OUT, load_panel

TERMS = ["1", "D", "G", "1/G", "D/G", "DG", "D^2", "G^2", "1/G^2"]
SEED, N_MC = 20261118, 200_000
p = load_panel()
ch = p.dropna(subset=["dD", "dG"])
D, G = ch.D.values, ch.G.values
X = np.column_stack([np.ones_like(D), D, G, 1 / G, D / G, D * G, D ** 2, G ** 2, 1 / G ** 2])
rms = np.sqrt((X ** 2).mean(axis=0))
rng = np.random.default_rng(SEED)
lines = []
for o in ("D", "G"):
    y = ch["d" + o].values
    n, sig = len(y), y.std(ddof=1)
    lam = sig
    fit = json.load(open(OUT / f"06_fit_{o}.json"))
    sel_normal = fit["selected_size"]
    lines.append(f"d{o}: normal prior (agreed) selects size {sel_normal}: "
                 f"{', '.join(fit['sizes'][str(sel_normal)]['terms'])}")
    for mult in (1, 10, 100):
        a = np.sqrt(3) * lam * mult
        logZ, pbox = {}, {}
        for m_str, r in fit["sizes"].items():
            idx = [TERMS.index(t) for t in r["terms"]]
            Xs = X[:, idx] / rms[idx]
            H = Xs.T @ Xs / sig ** 2
            w_hat = np.linalg.solve(Xs.T @ Xs, Xs.T @ y)
            draws = rng.multivariate_normal(w_hat, np.linalg.inv(H), size=N_MC)
            pb = np.mean(np.all(np.abs(draws) <= a, axis=1))
            m = len(idx)
            _, logdetH = np.linalg.slogdet(H)
            lz = (r["loglik"] + 0.5 * m * np.log(2 * np.pi) - 0.5 * logdetH
                  + (np.log(pb) if pb > 0 else -np.inf) - m * np.log(2 * a))
            logZ[int(m_str)], pbox[int(m_str)] = lz, pb
        ms = sorted(logZ)
        le = np.array([logZ[m] for m in ms])
        post = np.exp(le - le.max()); post /= post.sum()
        best = ms[int(np.argmax(le))]
        lines.append(f"  uniform, a = {mult:>3} x sqrt(3) lambda = {a:.4g}: selected size {best} "
                     f"({', '.join(fit['sizes'][str(best)]['terms'])}), P = {post[ms.index(best)]:.3f}")
        lines.append("     P(size): " + ", ".join(f"{m}:{q:.3f}" for m, q in zip(ms, post))
                     + "   | share of likelihood in box: "
                     + ", ".join(f"{m}:{pbox[m]:.2f}" for m in ms))
    lines.append("")
text = "\n".join(lines)
print(text)
(OUT / "10_uniform_prior_check.txt").write_text(text + "\n")
