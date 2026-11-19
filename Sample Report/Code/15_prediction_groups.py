"""Which countries followed the 1981-2006 model's prediction for 2024? (rule, version 3)

For each of the 168 countries observed in both 2006 and 2024 (V-Dem): predicted change in
democracy 2006->2024 (stepping the 1981-2006 model forward from the 2006 state, from
13_predict.py) against observed change. Groups (agreed with the user; revised twice, see
Appendix.md):
  predicted change smaller than STABLE (0.02) either way -- the model predicts stability:
    stayed, as predicted          |observed change| < MOVED (0.05)
    rose / fell, despite predicted stability   otherwise
  otherwise, by ratio r = observed change / predicted change:
    opposite direction            r < 0
    much less than predicted      0 <= r < 0.5
    roughly as predicted          0.5 <= r <= 2
    much more than predicted      r > 2
Superseded: version 1 grouped by |observed - predicted| <= 0.10 and the sign of the change
from 2006; it called Italy "followed" (predicted +0.04, observed -0.05) and India
"same direction" (predicted -0.03, observed -0.32).
GDP is listed (predicted and observed growth 2006-2024) but not used for grouping.

Reads outputs/13_predicted_2024.csv, outputs/panel_vdem.csv.
Writes outputs/15_prediction_groups.csv and 15_prediction_groups.txt.
"""
import numpy as np
import pandas as pd

from sds_common import G_SCALE, OUT

STABLE, MOVED, LO, HI = 0.02, 0.05, 0.5, 2.0
r = pd.read_csv(OUT / "13_predicted_2024.csv")
p = pd.read_csv(OUT / "panel_vdem.csv")
d06 = p[p.year == 2006].set_index("iso3")[["name", "D", "G"]]
r = r.join(d06, on="iso3")
r["pred_change"] = r.D_sim - r.D
r["obs_change"] = r.D_obs - r.D
r["error"] = r.D_obs - r.D_sim
r["ratio"] = r.obs_change / r.pred_change


def group(row):
    if abs(row.pred_change) < STABLE:
        if abs(row.obs_change) < MOVED:
            return "stayed, as predicted"
        return "rose, despite predicted stability" if row.obs_change > 0 else "fell, despite predicted stability"
    if row.ratio < 0:
        return "opposite direction"
    if row.ratio < LO:
        return "much less than predicted"
    if row.ratio <= HI:
        return "roughly as predicted"
    return "much more than predicted"


r["group"] = r.apply(group, axis=1)
r["gdp_growth_pred_pct"] = 100 * (np.exp(G_SCALE * (r.G_sim - r.G)) - 1)
r["gdp_growth_obs_pct"] = 100 * (np.exp(G_SCALE * (r.G_obs - r.G)) - 1)
out = r[["iso3", "name", "group", "D", "D_sim", "D_obs", "pred_change", "obs_change", "ratio", "error",
         "gdp_growth_pred_pct", "gdp_growth_obs_pct"]].rename(
    columns={"D": "D_2006", "D_sim": "D_2024_predicted", "D_obs": "D_2024_observed"})
out = out.sort_values(["group", "ratio"]).round(3)
out.to_csv(OUT / "15_prediction_groups.csv", index=False)

ORDER = ["roughly as predicted", "stayed, as predicted", "much less than predicted",
         "much more than predicted", "opposite direction",
         "rose, despite predicted stability", "fell, despite predicted stability"]
lines = [f"Countries: {len(out)}; stable if |predicted change| < {STABLE}; moved if |observed| >= {MOVED}; "
         f"roughly as predicted if ratio in [{LO}, {HI}]",
         f"predicted rise: {(out.pred_change > 0).sum()}; predicted fall: {(out.pred_change < 0).sum()}; "
         f"observed fall: {(out.obs_change < 0).sum()}"]
for g in ORDER:
    s_ = out[out.group == g]
    up = (s_.pred_change > 0).sum()
    lines.append(f"\n{g}: {len(s_)} (predicted rise {up}, predicted fall {len(s_) - up}; "
                 f"observed fall {(s_.obs_change < 0).sum()})")
    lines.append("  " + "; ".join(f"{n} ({pc:+.3f} -> {oc:+.3f})" for n, pc, oc in
                                    zip(s_.name, s_.pred_change, s_.obs_change)))
txt = "\n".join(lines)
print(txt)
(OUT / "15_prediction_groups.txt").write_text(txt + "\n")
