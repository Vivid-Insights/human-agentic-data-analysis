"""Did African countries follow the 1981-2006 model? (post-hoc look, agreed with the user)

Africa = World Bank region "Sub-Saharan Africa" plus Algeria, Egypt, Libya, Morocco and
Tunisia. Uses the same V-Dem model fitted to 1981-2006 and the same average-change
baseline as 13_predict.py; nothing is refitted. Agreed criterion, stated before computing:
"Africa followed the model" if (1) the model beats the baseline year by year for African
countries, with a country-resampled 95% interval for the difference above zero, and (2) the
share "roughly as predicted" or "stayed, as predicted" is clearly higher in Africa than in
the rest of the world. One without the other is reported as mixed.

Reads outputs/panel_vdem.csv, 06_fit_*_vdem.json, 15_prediction_groups.csv, 13_predicted_2024.csv,
and the World Bank country metadata. Writes outputs/17_africa_prediction.txt.
"""
import json

import numpy as np
import pandas as pd

from sds_common import OUT, ROOT

SEED, N_BOOT = 20261118, 2000
TERMS = ["1", "D", "G", "1/G", "D/G", "DG", "D^2", "G^2", "1/G^2"]
NORTH = {"DZA", "EGY", "LBY", "MAR", "TUN"}

meta = pd.read_csv(ROOT / "Attachments" / "worldbank" /
                   "Metadata_Country_API_NY.GDP.PCAP.KD_DS2_en_csv_v2_71952.csv")
africa = set(meta.loc[meta.Region == "Sub-Saharan Africa", "Country Code"]) | NORTH


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
    var = sig ** 2 + np.einsum("ij,jk,ik->i", Xi, cov, Xi)
    return -0.5 * np.log(2 * np.pi * var) - 0.5 * (y - Xi @ mean) ** 2 / var


p = pd.read_csv(OUT / "panel_vdem.csv")
fit = p[p.period == "fit"].dropna(subset=["dD", "dG"]).reset_index(drop=True)
test = p[p.period == "test"].dropna(subset=["dD", "dG"]).reset_index(drop=True)
Xf, Xt = design(fit.D, fit.G), design(test.D, test.G)
rms = np.sqrt((Xf ** 2).mean(axis=0))
test["africa"] = test.iso3.isin(africa)
rng = np.random.default_rng(SEED)
lines = [f"Africa: {len(africa)} codes in the definition; in the test "
         f"{test[test.africa].iso3.nunique()} countries, {int(test.africa.sum())} changes; "
         f"rest {test[~test.africa].iso3.nunique()} countries, {int((~test.africa).sum())} changes", ""]
for o in ("D", "G"):
    sz = json.load(open(OUT / f"06_fit_{o}_vdem.json"))
    idx = [TERMS.index(t) for t in sz["sizes"][str(sz["selected_size"])]["terms"]]
    yf, yt = fit["d" + o].values, test["d" + o].values
    m = lpd(Xt, yt, idx, *posterior(Xf, yf, idx, rms))
    b = lpd(Xt, yt, [0], *posterior(Xf, yf, [0], rms))
    test["adv"] = m - b
    lines.append(f"d{o}: model minus average-change baseline, mean log predictive density per change")
    per_c = test.groupby("iso3").agg(adv=("adv", "sum"), n=("adv", "size"), africa=("africa", "first"))
    for lab, sel in (("Africa", per_c.africa), ("rest", ~per_c.africa)):
        c = per_c[sel]
        est = c.adv.sum() / c.n.sum()
        boot = []
        for _ in range(N_BOOT):
            k = rng.integers(0, len(c), len(c))
            boot.append(c.adv.values[k].sum() / c.n.values[k].sum())
        lo, hi = np.percentile(boot, [2.5, 97.5])
        lines.append(f"  {lab:<7} {est:+.4f}  (95% country-resampled interval {lo:+.4f} to {hi:+.4f}); "
                     f"model better on {100 * (test.loc[test.africa == (lab == 'Africa'), 'adv'] > 0).mean():.0f}% of changes")
    lines.append("")

g = pd.read_csv(OUT / "15_prediction_groups.csv")
g["africa"] = g.iso3.isin(africa)
lines.append("Table A4 groups (version 3), share of countries:")
ok = g.group.isin(["roughly as predicted", "stayed, as predicted"])
for lab, sel in (("Africa", g.africa), ("rest", ~g.africa)):
    sub = g[sel]
    lines.append(f"  {lab:<7} n={len(sub)}: followed (roughly or stayed) {ok[sel].sum()} = {100 * ok[sel].mean():.0f}%; "
                 + "; ".join(f"{k} {v}" for k, v in sub.group.value_counts().items()))
a24 = pd.read_csv(OUT / "13_predicted_2024.csv")
a24["africa"] = a24.iso3.isin(africa)
lines.append("")
lines.append("2024 democracy error, median (model vs average-change baseline):")
for lab, sel in (("Africa", a24.africa), ("rest", ~a24.africa)):
    sub = a24[sel]
    em, eb = (sub.D_sim - sub.D_obs).abs(), (sub.D_base - sub.D_obs).abs()
    lines.append(f"  {lab:<7} n={len(sub)}: model {em.median():.3f}, baseline {eb.median():.3f}; "
                 f"model closer for {(em < eb).sum()} of {len(sub)}")
lines.append("")
lines.append("African countries by group:")
for k, sub in g[g.africa].groupby("group"):
    lines.append(f"  {k}: " + ", ".join(sorted(sub.name)))
text = "\n".join(lines)
print(text)
(OUT / "17_africa_prediction.txt").write_text(text + "\n")
