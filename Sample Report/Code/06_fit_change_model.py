"""Step 4: fit the change model for one outcome (D or G). Agreed method:

  dx_it = sum_{k in S} w_k phi_k(D_it, G_it) + e_it,   e ~ N(0, sigma^2)

  - library: 1, D, G, 1/G, D/G, DG, D^2, G^2, 1/G^2  (inverse-D terms removed)
  - every subset S (512); best per size m by likelihood (least squares)
  - sigma fixed at sd(dx) (Ranganathan et al. 2014 convention)
  - prior: each term divided by its RMS; rescaled coefficients ~ N(0, lambda^2),
    lambda = sd(dx). Evidence in closed form, dx ~ N(0, sigma^2 I + lambda^2 X X'),
    computed through m x m matrices (Woodbury), so no n x n matrix is formed.
  - sizes compared by evidence of their best model; equal prior on sizes
  - posterior for the selected model: Gaussian, mean M^-1 X'y, cov sigma^2 M^-1,
    M = X'X + (sigma/lambda)^2 I, reported on the original scale
  - checks (appendix): lambda x0.1 and x10; sigma from residuals; within-country
    lag-1 residual correlation; 500 country-resamples (seed 20261118)

Usage: uv run python 06_fit_change_model.py D [vdem]   (or G)
Writes Code/outputs/06_fit_<outcome>[_vdem].txt and .json. With "vdem", democracy is the
V-Dem electoral democracy index and only the 1981-2006 fit window is used (question 2).
"""
import itertools
import json
import sys

import numpy as np

from sds_common import OUT, load_panel

OUTCOME = sys.argv[1] if len(sys.argv) > 1 else "D"
MEASURE = sys.argv[2] if len(sys.argv) > 2 else "welzel"   # "welzel" (main) or "vdem" (question 2)
assert MEASURE in ("welzel", "vdem")
TAG = "" if MEASURE == "welzel" else "_vdem"
assert OUTCOME in ("D", "G")
SEED = 20261118
N_BOOT = 500
TERMS = ["1", "D", "G", "1/G", "D/G", "DG", "D^2", "G^2", "1/G^2"]


def design(D, G):
    return np.column_stack([np.ones_like(D), D, G, 1 / G, D / G, D * G,
                            D ** 2, G ** 2, 1 / G ** 2])


SUBSETS = [s for m in range(1, len(TERMS) + 1)
           for s in itertools.combinations(range(len(TERMS)), m)]


def fit_all(X, y, lam_mult=1.0, sigma=None):
    """Best subset per size, with log-likelihood and log-evidence for each."""
    n = len(y)
    sig = y.std(ddof=1) if sigma is None else sigma
    lam = lam_mult * y.std(ddof=1)
    rms = np.sqrt((X ** 2).mean(axis=0))
    Xs = X / rms
    A, b, yy = Xs.T @ Xs, Xs.T @ y, y @ y
    best = {}
    for S in SUBSETS:
        idx = list(S)
        As, bs = A[np.ix_(idx, idx)], b[idx]
        w = np.linalg.solve(As, bs)
        sse = yy - 2 * w @ bs + w @ As @ w
        m = len(idx)
        if m not in best or sse < best[m]["sse"]:
            best[m] = {"S": S, "sse": sse}
    out = {}
    for m, r in best.items():
        idx = list(r["S"])
        As, bs = A[np.ix_(idx, idx)], b[idx]
        loglik = -0.5 * n * np.log(2 * np.pi * sig ** 2) - r["sse"] / (2 * sig ** 2)
        M = As + (sig / lam) ** 2 * np.eye(len(idx))
        _, logdet = np.linalg.slogdet(np.eye(len(idx)) + (lam / sig) ** 2 * As)
        quad = (yy - bs @ np.linalg.solve(M, bs)) / sig ** 2
        logev = -0.5 * n * np.log(2 * np.pi * sig ** 2) - 0.5 * logdet - 0.5 * quad
        mean_s = np.linalg.solve(M, bs)
        cov_s = sig ** 2 * np.linalg.inv(M)
        out[m] = {"terms": [TERMS[i] for i in idx], "idx": idx, "sse": r["sse"],
                  "loglik": loglik, "logev": logev,
                  "mean": mean_s / rms[idx],
                  "sd": np.sqrt(np.diag(cov_s)) / rms[idx],
                  "r2": 1 - r["sse"] / ((y - y.mean()) @ (y - y.mean()))}
    return out, sig, lam


def size_posterior(res):
    ms = sorted(res)
    le = np.array([res[m]["logev"] for m in ms])
    p = np.exp(le - le.max()); p /= p.sum()
    return dict(zip(ms, p))


if MEASURE == "welzel":
    p = load_panel()
    ch = p.dropna(subset=["dD", "dG"]).reset_index(drop=True)
else:  # V-Dem: fit window only (changes ending by 2006)
    import pandas as pd
    p = pd.read_csv(OUT / "panel_vdem.csv")
    ch = p[p.period == "fit"].dropna(subset=["dD", "dG"]).reset_index(drop=True)
D, G = ch.D.values, ch.G.values
y = ch["d" + OUTCOME].values
X = design(D, G)
n, n_c = len(y), ch.iso3.nunique()

res, sig, lam = fit_all(X, y)
post = size_posterior(res)
m_sel = max(res, key=lambda m: res[m]["logev"])
sel = res[m_sel]
ranked = sorted(post, key=post.get, reverse=True)
m_next = ranked[1]

lines = [f"Outcome: d{OUTCOME}   changes: {n}   countries: {n_c}",
         f"sigma (fixed, sd of d{OUTCOME}): {sig:.5f}   lambda: {lam:.5f} (on RMS-scaled terms)",
         "", "Best model per size:",
         f"{'m':>2} {'log-lik':>10} {'log-evidence':>13} {'P(size)':>8} {'R2':>7}  terms"]
for m in sorted(res):
    r = res[m]
    lines.append(f"{m:>2} {r['loglik']:>10.2f} {r['logev']:>13.2f} {post[m]:>8.4f} {r['r2']:>7.4f}  "
                 + ", ".join(r["terms"]))
lines += ["", f"Selected: size {m_sel}, P = {post[m_sel]:.4f}; next best size {m_next}, "
          f"P = {post[m_next]:.4f}; log Bayes factor selected vs next = "
          f"{res[m_sel]['logev'] - res[m_next]['logev']:.2f}", "",
          "Selected model, posterior mean and 95% credible interval (original scale):"]
for t, mu, sd in zip(sel["terms"], sel["mean"], sel["sd"]):
    lines.append(f"  {t:<6} {mu:+.5f}  [{mu - 1.96 * sd:+.5f}, {mu + 1.96 * sd:+.5f}]")

# --- checks -----------------------------------------------------------------
lines += ["", "Checks (appendix only unless they change the answer)"]
for mult in (0.1, 10.0):
    r2, _, _ = fit_all(X, y, lam_mult=mult)
    ms = max(r2, key=lambda m: r2[m]["logev"])
    lines.append(f"  lambda x{mult:g}: selected size {ms}: {', '.join(r2[ms]['terms'])}")
Xsel = X[:, sel["idx"]]
w_ols = np.linalg.lstsq(Xsel, y, rcond=None)[0]
resid = y - Xsel @ w_ols
sig_res = resid.std(ddof=len(sel["idx"]))
r3, _, _ = fit_all(X, y, sigma=sig_res)
ms3 = max(r3, key=lambda m: r3[m]["logev"])
lines.append(f"  sigma from residuals ({sig_res:.5f} vs {sig:.5f}): selected size {ms3}: "
             f"{', '.join(r3[ms3]['terms'])}")
ch["resid"] = resid
nxt = ch[["iso3", "year", "resid"]].copy(); nxt["year"] -= 1
pair = ch.merge(nxt, on=["iso3", "year"], suffixes=("", "_next"))
rho = np.corrcoef(pair.resid, pair.resid_next)[0, 1]
lines.append(f"  within-country lag-1 residual correlation: {rho:+.3f} over {len(pair)} pairs")

rng = np.random.default_rng(SEED)
countries = ch.iso3.unique()
groups = {c: np.flatnonzero(ch.iso3.values == c) for c in countries}
sel_sets, coefs = {}, []
for _ in range(N_BOOT):
    pick = rng.choice(countries, size=len(countries), replace=True)
    rows = np.concatenate([groups[c] for c in pick])
    rb, _, _ = fit_all(X[rows], y[rows])
    mb = max(rb, key=lambda m: rb[m]["logev"])
    key = ", ".join(rb[mb]["terms"])
    sel_sets[key] = sel_sets.get(key, 0) + 1
    coefs.append(np.linalg.lstsq(X[rows][:, sel["idx"]], y[rows], rcond=None)[0])
coefs = np.array(coefs)
lines.append(f"  country resampling ({N_BOOT} draws, seed {SEED}); selected term sets:")
for k, v in sorted(sel_sets.items(), key=lambda kv: -kv[1])[:6]:
    lines.append(f"    {v:>4}  {k}")
lines.append("  term frequency across resamples (of %d):" % N_BOOT)
for t_ in TERMS:
    k_ = sum(v for s_, v in sel_sets.items() if t_ in [x.strip() for x in s_.split(",")])
    lines.append(f"    {t_:<6} {k_}")
other = "G" if OUTCOME == "D" else "D"
k_other = sum(v for s_, v in sel_sets.items()
              if any(other in x for x in s_.split(",")))
lines.append(f"    any term containing {other}: {k_other}")
lines.append("  selected model's coefficients across resamples (2.5-97.5 percentile) "
             "vs posterior interval width:")
for j, t in enumerate(sel["terms"]):
    lo, hi = np.percentile(coefs[:, j], [2.5, 97.5])
    lines.append(f"    {t:<6} [{lo:+.5f}, {hi:+.5f}]  width {hi - lo:.5f} vs "
                 f"posterior {2 * 1.96 * sel['sd'][j]:.5f}")

text = "\n".join(lines)
print(text)
(OUT / f"06_fit_{OUTCOME}{TAG}.txt").write_text(text + "\n")
json.dump({"outcome": OUTCOME, "n": int(n), "countries": int(n_c), "sigma": sig,
           "lambda": lam, "selected_size": int(m_sel),
           "sizes": {int(m): {"terms": r["terms"], "loglik": r["loglik"],
                              "logev": r["logev"], "post": post[m],
                              "mean": list(map(float, r["mean"])),
                              "sd": list(map(float, r["sd"])), "r2": r["r2"]}
                     for m, r in res.items()},
           "lag1_resid_corr": rho, "boot_sets": sel_sets},
          open(OUT / f"06_fit_{OUTCOME}{TAG}.json", "w"), indent=1, default=float)
