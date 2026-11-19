"""Step 1: describe the two source files. Draws no conclusions.

Reads
  Attachments/worldbank/API_NY.GDP.PCAP.KD_DS2_en_csv_v2_71952.csv
  Attachments/worldbank/Metadata_Country_API_NY.GDP.PCAP.KD_DS2_en_csv_v2_71952.csv
  Attachments/qog_std_ts_jan15.csv  (columns ccode, cname, year, ccodealp, wel_citrig)
Prints a description to stdout and writes Code/outputs/01_describe_data.txt.
"""
from pathlib import Path
import io
import contextlib
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
ATT = ROOT / "Attachments"
OUT = ROOT / "Code" / "outputs"
OUT.mkdir(parents=True, exist_ok=True)

WB = ATT / "worldbank" / "API_NY.GDP.PCAP.KD_DS2_en_csv_v2_71952.csv"
WB_META = ATT / "worldbank" / "Metadata_Country_API_NY.GDP.PCAP.KD_DS2_en_csv_v2_71952.csv"
QOG = ATT / "qog_std_ts_jan15.csv"

buf = io.StringIO()
with contextlib.redirect_stdout(buf):
    # ---------------- World Bank ----------------
    wb = pd.read_csv(WB, skiprows=4)
    wb = wb.loc[:, ~wb.columns.str.startswith("Unnamed")]
    meta = pd.read_csv(WB_META)
    years = [c for c in wb.columns if c.isdigit()]
    print("=== World Bank NY.GDP.PCAP.KD ===")
    print(f"rows (economies incl. aggregates): {len(wb)}; year columns {years[0]}-{years[-1]}")
    is_country = meta["Region"].notna()
    countries = set(meta.loc[is_country, "Country Code"])
    print(f"of which countries (Region not blank): {len(countries)}; aggregates: {(~is_country).sum()}")
    long = wb.melt(id_vars=["Country Name", "Country Code"], value_vars=years,
                   var_name="year", value_name="gdppc")
    long["year"] = long["year"].astype(int)
    long = long[long["Country Code"].isin(countries)]
    w = long[(long.year >= 1980) & (long.year <= 2006)]
    print(f"country-years 1980-2006: {len(w)}; non-missing: {w.gdppc.notna().sum()}")
    per_c = w.groupby("Country Code").gdppc.count()
    print(f"countries with any value 1980-2006: {(per_c > 0).sum()}; with all 27 years: {(per_c == 27).sum()}")
    print("non-missing countries per year, 1980-2006:")
    print(w.groupby("year").gdppc.count().to_string())
    print("gdppc 1980-2006 summary (constant 2015 US$):")
    print(w.gdppc.describe().to_string())
    print(f"values <= 0: {(w.gdppc <= 0).sum()}")

    # ---------------- QoG / Welzel ----------------
    q = pd.read_csv(QOG, usecols=["ccode", "cname", "year", "ccodealp", "wel_citrig"],
                    encoding="latin-1", low_memory=False)
    print("\n=== QoG Jan 2015: wel_citrig ===")
    print(f"rows in file: {len(q)}; years {q.year.min()}-{q.year.max()}; units: {q.ccode.nunique()}")
    d = q[q.wel_citrig.notna()]
    print(f"non-missing wel_citrig: {len(d)} country-years, {d.ccode.nunique()} units, years {d.year.min()}-{d.year.max()}")
    print("wel_citrig summary:")
    print(d.wel_citrig.describe().to_string())
    out = d[(d.wel_citrig < 0) | (d.wel_citrig > 1)]
    print(f"values outside [0,1]: {len(out)}; distinct such values: {sorted(out.wel_citrig.unique())}")
    print(f"  -99 by year: {out.groupby('year').size().to_dict()}")
    print(f"  units with any -99: {out.ccode.nunique()}")
    d = d[(d.wel_citrig >= 0) & (d.wel_citrig <= 1)]
    print(f"after treating -99 as missing: {len(d)} country-years, {d.ccode.nunique()} units")
    print(d.wel_citrig.describe().to_string())
    dup = q.dropna(subset=["ccodealp"]).groupby(["ccodealp", "year"]).size()
    dup = dup[dup > 1]
    print(f"(ccodealp, year) pairs appearing more than once in QoG: {len(dup)}")
    if len(dup):
        dd = q.set_index(["ccodealp", "year"]).loc[dup.index].reset_index()
        print(dd[dd.wel_citrig.notna()].groupby(["ccodealp", "cname"]).year.agg(["min", "max", "count"]).to_string())
    dw = d[(d.year >= 1980) & (d.year <= 2006)]
    z = dw[dw.wel_citrig == 0]
    print(f"\n1980-2006: {len(dw)} country-years, {dw.ccode.nunique()} units")
    print(f"exact zeros 1980-2006: {len(z)} country-years in {z.ccode.nunique()} units")
    print(f"values in (0, 0.01): {((dw.wel_citrig > 0) & (dw.wel_citrig < 0.01)).sum()}")
    print("smallest positive values:", sorted(dw.loc[dw.wel_citrig > 0, "wel_citrig"].unique())[:8])
    print("zeros by country (count, years):")
    for (cc, name), g in z.groupby(["ccodealp", "cname"]):
        print(f"  {cc} {name}: {len(g)} [{g.year.min()}-{g.year.max()}]")
    print("non-missing wel_citrig units per year, 1980-2006:")
    print(dw.groupby("year").wel_citrig.count().to_string())

    # ---------------- overlap ----------------
    both = dw.merge(w.rename(columns={"Country Code": "ccodealp"}), on=["ccodealp", "year"], how="inner")
    both = both[both.gdppc.notna()]
    print("\n=== overlap on ISO3 code, 1980-2006, both non-missing ===")
    print(f"country-years: {len(both)}; countries: {both.ccodealp.nunique()}")
    unmatched_q = sorted(set(dw.ccodealp.dropna()) - countries)
    print(f"QoG codes with wel_citrig not among WB countries: {unmatched_q}")
    print(f"QoG rows with blank ccodealp but wel_citrig: {dw.ccodealp.isna().sum()}")

text = buf.getvalue()
print(text)
(OUT / "01_describe_data.txt").write_text(text)
