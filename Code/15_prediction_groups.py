"""Which countries roughly followed the 1981-2006 model's prediction for 2024? (agreed rule)

For each of the 168 countries observed in both 2006 and 2024 (V-Dem), compare observed
2024 democracy with the value predicted by stepping the 1981-2006 model forward from the
country's 2006 state (from 13_predict.py). Groups, fixed before looking at countries:
  followed          |observed - predicted| <= 0.10
  missed, same      off by more than 0.10, but democracy moved the way the model
                    predicted (sign of observed and predicted change from 2006 agree)
  missed, opposite  off by more than 0.10 and moved the opposite way
GDP is listed (predicted and observed growth 2006-2024) but not used for grouping.

Reads outputs/13_predicted_2024.csv, outputs/panel_vdem.csv.
Writes outputs/15_prediction_groups.csv and 15_prediction_groups.txt.
"""
import numpy as np
import pandas as pd

from sds_common import G_SCALE, OUT

TOL = 0.10
r = pd.read_csv(OUT / "13_predicted_2024.csv")
p = pd.read_csv(OUT / "panel_vdem.csv")
d06 = p[p.year == 2006].set_index("iso3")[["name", "D", "G"]]
r = r.join(d06, on="iso3")
r["pred_change"] = r.D_sim - r.D
r["obs_change"] = r.D_obs - r.D
r["error"] = r.D_obs - r.D_sim
same = np.sign(r.pred_change) == np.sign(r.obs_change)
r["group"] = np.where(r.error.abs() <= TOL, "followed",
                      np.where(same, "missed, same direction", "missed, opposite direction"))
r["gdp_growth_pred_pct"] = 100 * (np.exp(G_SCALE * (r.G_sim - r.G)) - 1)
r["gdp_growth_obs_pct"] = 100 * (np.exp(G_SCALE * (r.G_obs - r.G)) - 1)
out = r[["iso3", "name", "group", "D", "D_sim", "D_obs", "pred_change", "obs_change", "error",
         "gdp_growth_pred_pct", "gdp_growth_obs_pct"]].rename(
    columns={"D": "D_2006", "D_sim": "D_2024_predicted", "D_obs": "D_2024_observed"})
out = out.sort_values(["group", "error"]).round(3)
out.to_csv(OUT / "15_prediction_groups.csv", index=False)

lines = [f"Countries: {len(out)}; tolerance {TOL} on V-Dem democracy in 2024"]
for g in ("followed", "missed, same direction", "missed, opposite direction"):
    s = out[out.group == g]
    lines.append(f"\n{g}: {len(s)}")
    if g != "followed":
        up = s[s.obs_change > 0]; down = s[s.obs_change <= 0]
        lines.append(f"  democracy rose: {len(up)}; fell or unchanged: {len(down)}")
        lines.append(f"  predicted to rise but fell: {((s.pred_change > 0) & (s.obs_change <= 0)).sum()}; "
                     f"predicted to fall but rose: {((s.pred_change <= 0) & (s.obs_change > 0)).sum()}")
    lines.append("  " + "; ".join(f"{n} ({e:+.2f})" for n, e in zip(s.name, s.error)))
txt = "\n".join(lines)
print(txt)
(OUT / "15_prediction_groups.txt").write_text(txt + "\n")
