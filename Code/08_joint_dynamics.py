"""Step 4, sub-question 3: what the two selected equations imply together. Agreed plan:

  1. Zero-change curves from posterior means. Democracy: for each G, solve the
     quadratic f_D(D, G) = 0 in D; GDP: f_G(D, G) = 0. Stability from the sign of
     d f / d(own variable) on the curve.
  2. 95% band from 1,000 posterior draws of each selected model (seed 20261118);
     band from the 500 country-resampled fits recorded for the appendix.
  3. Trajectories: step x_{t+1} = x_t + f(x_t) yearly from each country's first
     observed state to 2006. Convergence measure: distance |D - D*(G)| to the
     democracy zero-change curve, at the start and at the end, for all countries;
     the same for the observed paths.

Posterior mean and covariance are recomputed here with the formulas of
06_fit_change_model.py and checked against its exported means.
Writes outputs/08_dynamics.txt, 08_nullcline.csv, 08_simulated_paths.csv,
08_model_field.csv (model change at the Figure 3 cell positions).
"""
import json

import numpy as np
import pandas as pd

from sds_common import G_SCALE, OUT, REP, YEARS, load_panel

SEED, N_DRAW, N_BOOT = 20261118, 1000, 500
TERMS = ["1", "D", "G", "1/G", "D/G", "DG", "D^2", "G^2", "1/G^2"]


def design(D, G):
    D, G = np.asarray(D, float), np.asarray(G, float)
    return np.column_stack([np.ones_like(D), D, G, 1 / G, D / G, D * G,
                            D ** 2, G ** 2, 1 / G ** 2])


p = load_panel()
ch = p.dropna(subset=["dD", "dG"]).reset_index(drop=True)
Xfull = design(ch.D, ch.G)
rms = np.sqrt((Xfull ** 2).mean(axis=0))
fits = {o: json.load(open(OUT / f"06_fit_{o}.json")) for o in ("D", "G")}
model = {}
for o in ("D", "G"):
    sz = fits[o]["sizes"][str(fits[o]["selected_size"])]
    idx = [TERMS.index(t) for t in sz["terms"]]
    y = ch["d" + o].values
    sig = lam = y.std(ddof=1)
    Xs = Xfull[:, idx] / rms[idx]
    M = Xs.T @ Xs + (sig / lam) ** 2 * np.eye(len(idx))
    mean = np.linalg.solve(M, Xs.T @ y) / rms[idx]
    cov = sig ** 2 * np.linalg.inv(M) / np.outer(rms[idx], rms[idx])
    assert np.allclose(mean, sz["mean"]), "posterior mean differs from 06 output"
    model[o] = {"idx": idx, "terms": sz["terms"], "mean": mean, "cov": cov, "y": y}


def f(o, D, G, w=None):
    w = model[o]["mean"] if w is None else w
    return design(D, G)[:, model[o]["idx"]] @ w


def d_star(G, w):
    """Democracy zero-change curve: positive root in [0, 1.5] of f_D(D, G) = 0.

    Works for any term set by evaluating f_D on a fine D grid and locating the sign
    change from + to - (the attracting crossing); NaN if there is none.
    """
    Dg = np.linspace(0, 1.5, 1501)
    out = np.full(len(G), np.nan)
    for i, g in enumerate(G):
        v = design(Dg, np.full_like(Dg, g))[:, model["D"]["idx"]] @ w
        s = np.flatnonzero((v[:-1] > 0) & (v[1:] <= 0))
        if len(s):
            j = s[0]
            out[i] = Dg[j] - v[j] * (Dg[j + 1] - Dg[j]) / (v[j + 1] - v[j])
    return out


lines = []
for o in ("D", "G"):
    lines.append(f"d{o} = " + " ".join(f"{m:+.5f}*{t}" for t, m in zip(model[o]["terms"], model[o]["mean"])))
lines.append("")

# 1. zero-change curves
Ggrid = np.linspace(np.log(150) / G_SCALE, np.log(170000) / G_SCALE, 241)
Dstar = d_star(Ggrid, model["D"]["mean"])
# exact check from the quadratic (valid for the selected term set D, D/G, D^2, 1/G^2)
if model["D"]["terms"] == ["D", "D/G", "D^2", "1/G^2"]:
    a, b, c, e = model["D"]["mean"]
    A2, B1, C0 = c, a + b / Ggrid, e / Ggrid ** 2
    exact = (-B1 - np.sqrt(B1 ** 2 - 4 * A2 * C0)) / (2 * A2)
    lines.append(f"democracy curve: grid root vs exact quadratic root, max |diff| = "
                 f"{np.nanmax(np.abs(exact - Dstar)):.2e}")
    slope = 2 * c * exact + B1
    lines.append(f"  slope d f_D / dD on the curve: max {slope.max():+.4f} (negative = attracting)")
gobs = ch.G.values
in_range = (Ggrid >= gobs.min()) & (Ggrid <= gobs.max())
for usd in (500, 1000, 2000, 5000, 10000, 20000, 50000):
    g = np.log(usd) / G_SCALE
    lines.append(f"  at ${usd:>6,}: democracy stops changing at D* = {d_star([g], model['D']['mean'])[0]:.3f}")
# GDP curve: f_G(D, G) = 0 within D in [0,1] and observed G?
Dg = np.linspace(0, 1, 201)
GG, DD = np.meshgrid(Ggrid[in_range], Dg)
fG = f("G", DD.ravel(), GG.ravel()).reshape(DD.shape)
lines.append(f"GDP equation over observed range, D in [0,1]: min dG = {fG.min():+.5f}, "
             f"max = {fG.max():+.5f} -> zero-change curve in range: {bool((fG <= 0).any())}")
lines.append(f"  minimum yearly growth in range: {100 * (np.exp(G_SCALE * fG.min()) - 1):.2f}% "
             f"(at D = 0, richest G); at D = 0 and the poorest G: "
             f"{100 * (np.exp(G_SCALE * fG[0, 0]) - 1):.2f}%")
lines.append("")

# 2. bands
rng = np.random.default_rng(SEED)
draws = rng.multivariate_normal(model["D"]["mean"], model["D"]["cov"], size=N_DRAW)
band = np.array([d_star(Ggrid, w) for w in draws])
lo, hi = np.nanpercentile(band, [2.5, 97.5], axis=0)
groups = {c: np.flatnonzero(ch.iso3.values == c) for c in ch.iso3.unique()}
countries = np.array(list(groups))
bands_b = []
for _ in range(N_BOOT):
    rows = np.concatenate([groups[c] for c in rng.choice(countries, len(countries))])
    w = np.linalg.lstsq(Xfull[rows][:, model["D"]["idx"]], model["D"]["y"][rows], rcond=None)[0]
    bands_b.append(d_star(Ggrid, w))
lo_b, hi_b = np.nanpercentile(np.array(bands_b), [2.5, 97.5], axis=0)
w_post = np.nanmedian((hi - lo)[in_range]); w_boot = np.nanmedian((hi_b - lo_b)[in_range])
lines.append(f"95% band on D*, median width over observed GDP range: posterior {w_post:.3f}, "
             f"country resampling {w_boot:.3f} (ratio {w_boot / w_post:.2f})")
pd.DataFrame({"G": Ggrid, "usd": np.exp(G_SCALE * Ggrid), "D_star": Dstar, "lo": lo, "hi": hi,
              "lo_boot": lo_b, "hi_boot": hi_b, "in_range": in_range}) \
  .to_csv(OUT / "08_nullcline.csv", index=False)
lines.append("")

# 3. trajectories and convergence
first = p.sort_values("year").groupby("iso3").first().reset_index()
last = p.sort_values("year").groupby("iso3").last().reset_index()
first = first[first.iso3.isin(ch.iso3)]
last = last.set_index("iso3").loc[first.iso3].reset_index()
sims = []
for r in first.itertuples():
    D_, G_ = r.D, r.G
    for yr in range(r.year, YEARS[1] + 1):
        sims.append((r.iso3, yr, D_, G_))
        if yr == YEARS[1]:
            break
        dD_, dG_ = f("D", [D_], [G_])[0], f("G", [D_], [G_])[0]
        D_, G_ = D_ + dD_, G_ + dG_
sim = pd.DataFrame(sims, columns=["iso3", "year", "D", "G"])
sim.to_csv(OUT / "08_simulated_paths.csv", index=False)
s0 = sim.groupby("iso3").first(); s1 = sim.groupby("iso3").last()
dist = lambda D_, G_: np.abs(D_ - d_star(G_, model["D"]["mean"]))
sim_start, sim_end = dist(s0.D.values, s0.G.values), dist(s1.D.values, s1.G.values)
obs_start = dist(first.D.values, first.G.values)
obs_end = dist(last.D.values, last.G.values)
lines += [f"trajectories: {len(first)} countries, from each first observed year to {YEARS[1]}",
          f"  simulated |D - D*(G)|: median start {np.median(sim_start):.3f}, end {np.median(sim_end):.3f}; "
          f"closer at end for {(sim_end < sim_start).sum()} of {len(first)}",
          f"  observed  |D - D*(G)|: median first year {np.median(obs_start):.3f}, last year "
          f"{np.median(obs_end):.3f}; closer at end for {(obs_end < obs_start).sum()} of {len(first)}",
          f"  simulated D outside [0,1] at any step: {int(((sim.D < 0) | (sim.D > 1)).sum())} country-years",
          f"  simulated 2006 GDP range: ${np.exp(G_SCALE * s1.G.min()):,.0f} to ${np.exp(G_SCALE * s1.G.max()):,.0f}"]
for iso, name in REP.items():
    a0, a1 = s0.loc[iso], s1.loc[iso]
    o1 = last.set_index("iso3").loc[iso]
    lines.append(f"  {name:<8} start D {a0.D:.2f} at ${np.exp(G_SCALE * a0.G):,.0f}; simulated 2006 D {a1.D:.2f} "
                 f"at ${np.exp(G_SCALE * a1.G):,.0f}; observed {int(o1.year)} D {o1.D:.2f} at ${o1.gdppc:,.0f}")

# model field at the Figure 3 cell positions
cells = pd.read_csv(OUT / "05_phase_cells.csv")
cells["mdD"] = f("D", cells.D, cells.G)
cells["mdG"] = f("G", cells.D, cells.G)
cells[["G", "D", "n", "mdG", "mdD"]].to_csv(OUT / "08_model_field.csv", index=False)

text = "\n".join(lines)
print(text)
(OUT / "08_dynamics.txt").write_text(text + "\n")
