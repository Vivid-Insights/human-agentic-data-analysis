"""Step 1 (question 2): describe the V-Dem electoral democracy index. Draws no conclusions.

Reads Attachments/vdem/V-Dem-CY-Core-v15.csv (columns country_name, country_text_id,
year, v2x_polyarchy) and the World Bank GDP file. Writes outputs/11_describe_vdem.txt.
"""
import io
import contextlib

import pandas as pd

from sds_common import OUT, ROOT

VD = ROOT / "Attachments" / "vdem" / "V-Dem-CY-Core-v15.csv"
WB = ROOT / "Attachments" / "worldbank" / "API_NY.GDP.PCAP.KD_DS2_en_csv_v2_71952.csv"
WB_META = ROOT / "Attachments" / "worldbank" / "Metadata_Country_API_NY.GDP.PCAP.KD_DS2_en_csv_v2_71952.csv"

buf = io.StringIO()
with contextlib.redirect_stdout(buf):
    v = pd.read_csv(VD, usecols=["country_name", "country_text_id", "year", "v2x_polyarchy"],
                    low_memory=False)
    print(f"rows: {len(v)}; countries: {v.country_text_id.nunique()}; years {v.year.min()}-{v.year.max()}")
    w = v[v.year.between(1981, 2024)]
    print(f"1981-2024: {len(w)} rows, {w.country_text_id.nunique()} countries; "
          f"v2x_polyarchy non-missing {w.v2x_polyarchy.notna().sum()}")
    print("v2x_polyarchy 1981-2024 summary:"); print(w.v2x_polyarchy.describe().to_string())
    print(f"outside [0,1]: {((w.v2x_polyarchy < 0) | (w.v2x_polyarchy > 1)).sum()}; "
          f"exact zeros: {(w.v2x_polyarchy == 0).sum()}; below 0.01: {(w.v2x_polyarchy < 0.01).sum()}")
    print(f"distinct negative values (possible codes): {sorted(w.loc[w.v2x_polyarchy < 0, 'v2x_polyarchy'].unique())[:5]}")
    print("countries with a value, by year (every 5 years):")
    print(w.dropna(subset=['v2x_polyarchy']).groupby('year').size().loc[list(range(1981, 2025, 5)) + [2024]].to_string())
    dup = w.groupby(["country_text_id", "year"]).size()
    print(f"duplicate (code, year): {(dup > 1).sum()}")
    meta = pd.read_csv(WB_META)
    countries = set(meta.loc[meta["Region"].notna(), "Country Code"])
    wb = pd.read_csv(WB, skiprows=4)
    g = wb[wb["Country Code"].isin(countries)].melt(
        id_vars=["Country Code"], value_vars=[str(y) for y in range(1981, 2025)],
        var_name="year", value_name="gdppc").dropna()
    g["year"] = g.year.astype(int)
    m = w.dropna(subset=["v2x_polyarchy"]).merge(g, left_on=["country_text_id", "year"],
                                                 right_on=["Country Code", "year"])
    print(f"overlap with World Bank GDP, 1981-2024: {len(m)} country-years, {m.country_text_id.nunique()} countries")
    for lo, hi in ((1981, 2006), (2007, 2024)):
        mm = m[m.year.between(lo, hi)]
        print(f"  {lo}-{hi}: {len(mm)} country-years, {mm.country_text_id.nunique()} countries")
    unmatched = sorted(set(w.dropna(subset=['v2x_polyarchy']).country_text_id) - countries)
    print(f"V-Dem codes with values but not World Bank countries: {unmatched}")

text = buf.getvalue()
print(text)
(OUT / "11_describe_vdem.txt").write_text(text)
