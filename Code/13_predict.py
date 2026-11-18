"""Step 4 (question 2): does the V-Dem model fitted to 1981-2006 predict 2007-2024?

Model: the selected V-Dem equations from 06_fit_change_model.py (posterior mean and
covariance recomputed here and checked against the export), sigma = sd of the
1981-2006 changes. Agreed design:

  1. Year by year: for each test change (2006->2007 ... 2023->2024), the posterior
     predictive density N(x w, sigma^2 + x S x'). Mean log predictive density per
     change against two baselines:
       - average change: an intercept-only model fitted to 1981-2006 (same prior and
         sigma), i.e. no dependence on the state;
       - refit: the same terms refitted to 2007-2024 itself, scored in sample, the best
         these terms could do on the test period.
     Also the share of the test variance explained (out of sample).
  2. Whole period: every country with both variables in 2006 and 2024, stepped
     x_{t+1} = x_t + f(x_t) for 18 years from its 2006 state; error against the observed
     2024 state, against the average-change baseline stepped the same way.
     Also whether observed countries moved closer to the 1981-2006 democracy nullcline.

Writes outputs/13_predict.txt, 13_predicted_paths.csv (six countries, simulated and
observed 2006-2024).
"""
import json

import numpy as np
import pandas as pd

from sds_common import G_SCALE, OUT, REP

TERMS = ["1", "D", "G", "1/G", "D/G", "DG", "D^2", "G^2", "1/G^2"]
Y_FIT, Y1 = 2006, 2024


def design(D, G):
    D, G = np.asarray(D, float), np.asarray(G, float)
    return np.column_stack([np.ones_like(D), D, G, 1 / G, D / G, D * G, D ** 2, G ** 2, 1 / G ** 2])


def posterior(X, y, idx, rms):
    sig = lam = y.std(ddof=1)
    Xs = X[:, idx] / rms[idx]
    M = Xs.T @ Xs + (sig / lam) ** 2 * np.eye(len(idx))
    mean = np.linalg.solve(M, Xs.T @ y) / rms[idx]
    cov = sig ** 2 * np.linalg.inv(M) / np.outer(rms[idx], rms[idx])
    return mean, cov, sig


def lpd(X, y, idx, mean, cov, sig):
    Xi = X[:, idx]
    mu = Xi @ mean
    var = sig ** 2 + np.einsum("ij,jk,ik->i", Xi, cov, Xi)
    return -0.5 * np.log(2 * np.pi * var) - 0.5 * (y - mu) ** 2 / var


p = pd.read_csv(OUT / "panel_vdem.csv")
fit = p[p.period == "fit"].dropna(subset=["dD", "dG"]).reset_index(drop=True)
test = p[p.period == "test"].dropna(subset=["dD", "dG"]).reset_index(drop=True)
Xf, Xt = design(fit.D, fit.G), design(test.D, test.G)
rms = np.sqrt((Xf ** 2).mean(axis=0))   # scaling from the fit period
lines, model = [], {}
for o in ("D", "G"):
    sz = json.load(open(OUT / f"06_fit_{o}_vdem.json"))
    sel = sz["sizes"][str(sz["selected_size"])]
    idx = [TERMS.index(t) for t in sel["terms"]]
    yf, yt = fit["d" + o].values, test["d" + o].values
    mean, cov, sig = posterior(Xf, yf, idx, rms)
    assert np.allclose(mean, sel["mean"]), "posterior mean differs from 06 output"
    model[o] = (idx, mean)
    m_lpd = lpd(Xt, yt, idx, mean, cov, sig)
    b_mean, b_cov, b_sig = posterior(Xf, yf, [0], rms)          # average change
    b_lpd = lpd(Xt, yt, [0], b_mean, b_cov, b_sig)
    r_mean, r_cov, r_sig = posterior(Xt, yt, idx, np.sqrt((Xt ** 2).mean(axis=0)))
    r_lpd = lpd(Xt, yt, idx, r_mean, r_cov, r_sig)
    pred = Xt[:, idx] @ mean
    r2_oos = 1 - ((yt - pred) ** 2).sum() / ((yt - yt.mean()) ** 2).sum()
    r2_in = sel["r2"]
    lines += [f"d{o}: model {', '.join(sel['terms'])}; {len(yt)} test changes from {test.iso3.nunique()} countries",
              f"  mean log predictive density per change: model {m_lpd.mean():.4f}, "
              f"average-change baseline {b_lpd.mean():.4f}, refit on 2007-2024 {r_lpd.mean():.4f}",
              f"  total log predictive density, model minus baseline: {m_lpd.sum() - b_lpd.sum():+.1f}; "
              f"refit minus model: {r_lpd.sum() - m_lpd.sum():+.1f}",
              f"  model better than baseline for {(m_lpd > b_lpd).mean() * 100:.1f}% of test changes",
              f"  variance explained: in 1981-2006 (in sample) {100 * r2_in:.1f}%, "
              f"in 2007-2024 (out of sample) {100 * r2_oos:.1f}%",
              f"  refit coefficients on 2007-2024: " + ", ".join(f"{t} {m:+.5f}" for t, m in zip(sel['terms'], r_mean))
              + "   (1981-2006: " + ", ".join(f"{m:+.5f}" for m in mean) + ")", ""]


def step(D, G):
    x = design([D], [G])
    return (D + (x[:, model["D"][0]] @ model["D"][1])[0], G + (x[:, model["G"][0]] @ model["G"][1])[0])


a = p[p.year == Y_FIT].set_index("iso3")[["D", "G"]]
b = p[p.year == Y1].set_index("iso3")[["D", "G"]]
both = a.index.intersection(b.index)
mD, mG = fit.dD.mean(), fit.dG.mean()
rows, paths = [], []
for c in both:
    D_, G_ = a.loc[c, "D"], a.loc[c, "G"]
    for yr in range(Y_FIT, Y1 + 1):
        if c in REP:
            paths.append((c, yr, D_, G_, "simulated"))
        if yr < Y1:
            D_, G_ = step(D_, G_)
    n = Y1 - Y_FIT
    rows.append((c, D_, G_, a.loc[c, "D"] + n * mD, a.loc[c, "G"] + n * mG, b.loc[c, "D"], b.loc[c, "G"]))
r = pd.DataFrame(rows, columns=["iso3", "D_sim", "G_sim", "D_base", "G_base", "D_obs", "G_obs"])
eD_m, eD_b = (r.D_sim - r.D_obs).abs(), (r.D_base - r.D_obs).abs()
eG_m, eG_b = (r.G_sim - r.G_obs).abs(), (r.G_base - r.G_obs).abs()
pct = lambda e: 100 * (np.exp(G_SCALE * e) - 1)


def wD_null(G):
    """V-Dem democracy nullcline from the 1981-2006 fit (quadratic in D)."""
    w = dict(zip([TERMS[i] for i in model["D"][0]], model["D"][1]))
    G = np.asarray(G, float)
    A2 = w.get("D^2", 0); B1 = w.get("D", 0) + w.get("D/G", 0) / G + w.get("DG", 0) * G
    C0 = w.get("1", 0) + w.get("G", 0) * G + w.get("1/G", 0) / G + w.get("G^2", 0) * G ** 2 + w.get("1/G^2", 0) / G ** 2
    return (-B1 - np.sqrt(B1 ** 2 - 4 * A2 * C0)) / (2 * A2)


d06 = (a.loc[both, "D"] - wD_null(a.loc[both, "G"])).abs()
d24 = (b.loc[both, "D"] - wD_null(b.loc[both, "G"])).abs()
lines += [f"Whole period: {len(both)} countries with both variables in {Y_FIT} and {Y1}, stepped {Y1 - Y_FIT} years",
          f"  democracy, |error| in {Y1}: model median {eD_m.median():.3f} (mean {eD_m.mean():.3f}); "
          f"average-change baseline median {eD_b.median():.3f} (mean {eD_b.mean():.3f}); "
          f"model closer for {(eD_m < eD_b).sum()} of {len(r)}",
          f"  GDP, |error| in {Y1}: model median {pct(eG_m.median()):.1f}% (mean {pct(eG_m.mean()):.1f}%); "
          f"baseline median {pct(eG_b.median()):.1f}% (mean {pct(eG_b.mean()):.1f}%); "
          f"model closer for {(eG_m < eG_b).sum()} of {len(r)}",
          f"  observed distance to the 1981-2006 democracy nullcline: median {d06.median():.3f} in {Y_FIT}, "
          f"{d24.median():.3f} in {Y1}; closer in {Y1} for {(d24 < d06).sum()} of {len(both)}",
          f"  simulated distance in {Y1}: median "
          f"{(r.D_sim - wD_null(r.G_sim)).abs().median():.3f}"]
for c, name in REP.items():
    rr = r.set_index("iso3").loc[c]
    lines.append(f"  {name:<8} {Y_FIT} D {a.loc[c, 'D']:.2f}; {Y1} simulated {rr.D_sim:.2f}, observed {rr.D_obs:.2f}; "
                 f"GDP simulated ${np.exp(G_SCALE * rr.G_sim):,.0f}, observed ${np.exp(G_SCALE * rr.G_obs):,.0f}")
    for yr, (D_, G_) in p[(p.iso3 == c) & p.year.between(Y_FIT, Y1)].set_index("year")[["D", "G"]].iterrows():
        paths.append((c, yr, D_, G_, "observed"))
pd.DataFrame(paths, columns=["iso3", "year", "D", "G", "kind"]).to_csv(OUT / "13_predicted_paths.csv", index=False)
r.to_csv(OUT / "13_predicted_2024.csv", index=False)
text = "\n".join(lines)
print(text)
(OUT / "13_predict.txt").write_text(text + "\n")
