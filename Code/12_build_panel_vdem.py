"""Step 3 (question 2): build the V-Dem panel, 1981-2024. Same rules as 02_build_panel.py.

D = V-Dem v2x_polyarchy (electoral democracy index, 0-1); G = ln(GDP per capita)/12.
Countries only (World Bank aggregates excluded); join on ISO3; a country-year needs
both variables; changes use every consecutive pair present. Column `period` marks
changes in the fit window (t+1 <= 2006) and the test window (2007 <= t+1 <= 2024).

Writes outputs/panel_vdem.csv (gitignored, row-level) and outputs/12_panel_vdem_counts.txt.
"""
import numpy as np
import pandas as pd

from sds_common import G_SCALE, OUT, REP, ROOT

VD = ROOT / "Attachments" / "vdem" / "V-Dem-CY-Core-v15.csv"
WB = ROOT / "Attachments" / "worldbank" / "API_NY.GDP.PCAP.KD_DS2_en_csv_v2_71952.csv"
WB_META = ROOT / "Attachments" / "worldbank" / "Metadata_Country_API_NY.GDP.PCAP.KD_DS2_en_csv_v2_71952.csv"
Y0, Y_FIT, Y1 = 1981, 2006, 2024

meta = pd.read_csv(WB_META)
countries = set(meta.loc[meta["Region"].notna(), "Country Code"])
wb = pd.read_csv(WB, skiprows=4)
gdp = (wb[wb["Country Code"].isin(countries)]
       .melt(id_vars=["Country Name", "Country Code"], value_vars=[str(y) for y in range(Y0, Y1 + 1)],
             var_name="year", value_name="gdppc")
       .rename(columns={"Country Name": "name", "Country Code": "iso3"}).dropna(subset=["gdppc"]))
gdp["year"] = gdp.year.astype(int)
v = pd.read_csv(VD, usecols=["country_text_id", "year", "v2x_polyarchy"], low_memory=False)
v = v[v.year.between(Y0, Y1)].dropna().rename(columns={"country_text_id": "iso3", "v2x_polyarchy": "D"})
assert v.D.between(0, 1).all() and not v.duplicated(["iso3", "year"]).any()

p = gdp.merge(v, on=["iso3", "year"], how="inner")
p["G"] = np.log(p.gdppc) / G_SCALE
p = p.sort_values(["iso3", "year"]).reset_index(drop=True)
nxt = p[["iso3", "year", "D", "G"]].copy(); nxt["year"] -= 1
p = p.merge(nxt.rename(columns={"D": "D_next", "G": "G_next"}), on=["iso3", "year"], how="left")
p["dD"], p["dG"] = p.D_next - p.D, p.G_next - p.G
p["period"] = np.where(p.year + 1 <= Y_FIT, "fit", "test")
p.loc[p.dD.isna(), "period"] = ""
p.to_csv(OUT / "panel_vdem.csv", index=False)

ch = p.dropna(subset=["dD"])
fit, test = ch[ch.period == "fit"], ch[ch.period == "test"]
lines = [f"V-Dem panel {Y0}-{Y1}: {len(p)} country-years, {p.iso3.nunique()} countries",
         f"fit changes (to {Y_FIT}): {len(fit)} from {fit.iso3.nunique()} countries",
         f"test changes ({Y_FIT}->{Y_FIT + 1} to {Y1 - 1}->{Y1}): {len(test)} from {test.iso3.nunique()} countries",
         f"D range {p.D.min():.3f}-{p.D.max():.3f}; G range {p.G.min():.3f}-{p.G.max():.3f}",
         f"countries with both variables in {Y_FIT} and {Y1}: "
         f"{len(set(p[p.year == Y_FIT].iso3) & set(p[p.year == Y1].iso3))}"]
for iso, name in REP.items():
    r = p[p.iso3 == iso]
    lines.append(f"rep {iso} {name}: years {r.year.min()}-{r.year.max()} ({len(r)})")
txt = "\n".join(lines)
print(txt)
(OUT / "12_panel_vdem_counts.txt").write_text(txt + "\n")
