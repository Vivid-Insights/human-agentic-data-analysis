"""Step 3 preparation: build the cleaned country-year panel. Fits nothing.

Applies the step 1 decisions recorded in Appendix.md (Data Summary):
  - World Bank NY.GDP.PCAP.KD, countries only (aggregates have a blank Region)
  - wel_citrig from QoG Jan 2015; -99 set to missing; values must lie in [0, 1]
  - join on ISO3 (World Bank Country Code = QoG ccodealp), years 1981-2006
  - G = ln(GDP per capita) / 12; D = wel_citrig unchanged
  - a country-year enters only if both variables are present (no imputation)
  - changes use every pair of consecutive years present (dD = D(t+1) - D(t))

Writes
  Code/outputs/panel.csv            one row per country-year with both variables,
                                    plus next-year values and changes where t+1 exists
  Code/outputs/02_panel_counts.txt  counts used in captions and in the appendix
"""
import numpy as np
import pandas as pd

from sds_common import ROOT, OUT, PANEL, COUNTS, YEARS, G_SCALE, REP

ATT = ROOT / "Attachments"
WB = ATT / "worldbank" / "API_NY.GDP.PCAP.KD_DS2_en_csv_v2_71952.csv"
WB_META = ATT / "worldbank" / "Metadata_Country_API_NY.GDP.PCAP.KD_DS2_en_csv_v2_71952.csv"
QOG = ATT / "qog_std_ts_jan15.csv"

y0, y1 = YEARS

# World Bank: countries only
wb = pd.read_csv(WB, skiprows=4)
meta = pd.read_csv(WB_META)
countries = set(meta.loc[meta["Region"].notna(), "Country Code"])
years = [str(y) for y in range(y0, y1 + 1)]
gdp = (wb[wb["Country Code"].isin(countries)]
       .melt(id_vars=["Country Name", "Country Code"], value_vars=years,
             var_name="year", value_name="gdppc")
       .rename(columns={"Country Name": "name", "Country Code": "iso3"}))
gdp["year"] = gdp["year"].astype(int)
gdp = gdp.dropna(subset=["gdppc"])

# QoG: wel_citrig, -99 -> missing
q = pd.read_csv(QOG, usecols=["ccodealp", "year", "wel_citrig"],
                encoding="latin-1", low_memory=False)
q = q[q.year.between(y0, y1)]
n_minus99 = int((q.wel_citrig == -99).sum())
q.loc[q.wel_citrig == -99, "wel_citrig"] = np.nan
assert q.wel_citrig.dropna().between(0, 1).all(), "wel_citrig outside [0,1] after -99 removal"
q = q.dropna(subset=["wel_citrig", "ccodealp"]).rename(columns={"ccodealp": "iso3", "wel_citrig": "D"})
assert not q.duplicated(["iso3", "year"]).any(), "duplicate country-years in QoG"

# Join (inner): a country-year needs both variables
p = gdp.merge(q, on=["iso3", "year"], how="inner")
p["G"] = np.log(p["gdppc"]) / G_SCALE
p = p.sort_values(["iso3", "year"]).reset_index(drop=True)

# Consecutive-year changes
nxt = p[["iso3", "year", "D", "G"]].copy()
nxt["year"] -= 1
nxt = nxt.rename(columns={"D": "D_next", "G": "G_next"})
p = p.merge(nxt, on=["iso3", "year"], how="left")
p["dD"] = p["D_next"] - p["D"]
p["dG"] = p["G_next"] - p["G"]

# Balanced set for the mean: both variables in every year
n_years = y1 - y0 + 1
per_c = p.groupby("iso3").year.count()
balanced = sorted(per_c[per_c == n_years].index)
p["balanced"] = p["iso3"].isin(balanced)

p = p[["iso3", "name", "year", "gdppc", "G", "D", "D_next", "G_next", "dD", "dG", "balanced"]]
OUT.mkdir(parents=True, exist_ok=True)
p.to_csv(PANEL, index=False)

ch = p.dropna(subset=["dD"])
last = p[p.year == y1]
lines = [
    f"years: {y0}-{y1}",
    f"-99 values set to missing in wel_citrig, {y0}-{y1}: {n_minus99}",
    f"country-years with both variables: {len(p)}",
    f"countries: {p.iso3.nunique()}",
    f"consecutive-year changes: {len(ch)}",
    f"countries contributing at least one change: {ch.iso3.nunique()}",
    f"balanced countries (both variables all {n_years} years): {len(balanced)}",
    f"countries with both variables in {y1}: {len(last)}",
    f"G range: {p.G.min():.3f}-{p.G.max():.3f}",
    f"D range: {p.D.min():.3f}-{p.D.max():.3f}",
    f"D exact zeros: {(p.D == 0).sum()}",
]
for iso, name in REP.items():
    r = p[p.iso3 == iso]
    lines.append(f"rep {iso} {name}: {len(r)} years, changes {r.dD.notna().sum()}, "
                 f"years present {r.year.min()}-{r.year.max()}")
txt = "\n".join(lines)
print(txt)
COUNTS.write_text(txt + "\n")
