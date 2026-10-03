"""Download the source data for the deforestation / GDP-per-person analysis.

Writes three files to ``Attachments/`` and prints a SHA-256 for each.
Re-running overwrites them; the printed checksums are what the Data Summary records.

Sources
-------
1. Global Forest Watch (UMD/Hansen) tree cover loss, country x year x driver,
   from the GFW Data API dataset ``gadm__tcl__iso_change``.
2. The matching tree-cover extent denominator from ``gadm__tcl__iso_summary``.
3. World Bank GDP per capita, PPP, constant 2021 international $
   (indicator ``NY.GDP.PCAP.PP.KD``).

Run with:  cd Code && uv run python 01_download_data.py
"""

from __future__ import annotations

import hashlib
import json
import urllib.parse
import urllib.request
from pathlib import Path

ATTACH = Path(__file__).resolve().parent.parent / "Attachments"

# Pinned deliberately. The API's ``latest`` alias points at v20250515, which stops at
# 2024 and carries the older six-class Curtis driver taxonomy. v20260424 runs to 2025,
# carries the finer eight-class WRI/Google driver taxonomy and the SBTN natural-forest
# class, and reproduces v20250515 exactly on every overlapping year.
GFW_VERSION = "v20260424"
GFW_BASE = "https://data-api.globalforestwatch.org/dataset"

# GFW's conventional definition of "forest" for loss statistics.
CANOPY_THRESHOLD = 30

WB_INDICATOR = "NY.GDP.PCAP.PP.KD"


def gfw_csv(dataset: str, sql: str) -> bytes:
    url = (
        f"{GFW_BASE}/{dataset}/{GFW_VERSION}/download/csv?"
        + urllib.parse.urlencode({"sql": sql})
    )
    with urllib.request.urlopen(url, timeout=600) as r:
        body = r.read()
    if body.lstrip().startswith(b"{"):
        raise RuntimeError(f"API returned an error for {dataset}: {body[:400]!r}")
    return body


def write(name: str, body: bytes) -> None:
    path = ATTACH / name
    path.write_bytes(body)
    digest = hashlib.sha256(body).hexdigest()
    rows = body.count(b"\n") - 1
    print(f"{name}\n  sha256 {digest}\n  {len(body):,} bytes, {rows:,} data rows")


def main() -> None:
    ATTACH.mkdir(exist_ok=True)

    loss_sql = (
        "SELECT iso, "
        "umd_tree_cover_loss__year AS year, "
        "wri_google_tree_cover_loss_drivers__driver AS driver, "
        "sbtn_natural_forests__class AS natural_forest_class, "
        "is__umd_regional_primary_forest_2001 AS is_primary_forest, "
        "SUM(umd_tree_cover_loss__ha) AS tree_cover_loss_ha "
        "FROM results "
        f"WHERE umd_tree_cover_density_2000__threshold = {CANOPY_THRESHOLD} "
        "GROUP BY iso, year, driver, natural_forest_class, is_primary_forest "
        "ORDER BY iso, year, driver"
    )
    write("gfw_tree_cover_loss_by_driver.csv", gfw_csv("gadm__tcl__iso_change", loss_sql))

    extent_sql = (
        "SELECT iso, "
        "sbtn_natural_forests__class AS natural_forest_class, "
        "is__umd_regional_primary_forest_2001 AS is_primary_forest, "
        "SUM(umd_tree_cover_extent_2000__ha) AS tree_cover_extent_2000_ha, "
        "SUM(area__ha) AS area_ha "
        "FROM results "
        f"WHERE umd_tree_cover_density_2000__threshold = {CANOPY_THRESHOLD} "
        "GROUP BY iso, natural_forest_class, is_primary_forest "
        "ORDER BY iso"
    )
    write("gfw_tree_cover_extent_2000.csv", gfw_csv("gadm__tcl__iso_summary", extent_sql))

    # --- World Bank -----------------------------------------------------------
    rows: list[dict] = []
    page = 1
    while True:
        url = (
            f"https://api.worldbank.org/v2/country/all/indicator/{WB_INDICATOR}?"
            + urllib.parse.urlencode({"format": "json", "per_page": 20000, "page": page})
        )
        with urllib.request.urlopen(url, timeout=300) as r:
            payload = json.load(r)
        header, batch = payload[0], payload[1]
        rows.extend(batch or [])
        if page >= header["pages"]:
            last_updated = header["lastupdated"]
            break
        page += 1

    lines = ["iso3,country,year,gdp_per_capita_ppp_const2021_intl_usd"]
    for row in rows:
        iso3 = row.get("countryiso3code") or ""
        country = (row["country"]["value"] or "").replace('"', "")
        value = row["value"]
        lines.append(f'{iso3},"{country}",{row["date"]},{"" if value is None else value}')
    write("worldbank_gdp_per_capita_ppp.csv", ("\n".join(lines) + "\n").encode())
    print(f"  World Bank indicator {WB_INDICATOR}, lastupdated {last_updated}")

    # Country metadata: region and income group, used to define sub-samples.
    # Aggregates are identifiable because their region is "Aggregates".
    meta_rows: list[dict] = []
    page = 1
    while True:
        url = ("https://api.worldbank.org/v2/country?"
               + urllib.parse.urlencode({"format": "json", "per_page": 400, "page": page}))
        with urllib.request.urlopen(url, timeout=300) as r:
            payload = json.load(r)
        header, batch = payload[0], payload[1]
        meta_rows.extend(batch or [])
        if page >= header["pages"]:
            break
        page += 1

    mlines = ["iso3,country,region,income_group"]
    for row in meta_rows:
        iso3 = row.get("id") or ""
        name = (row.get("name") or "").replace('"', "")
        region = (row.get("region", {}).get("value") or "").replace('"', "")
        income = (row.get("incomeLevel", {}).get("value") or "").replace('"', "")
        mlines.append(f'{iso3},"{name}","{region}","{income}"')
    write("worldbank_country_metadata.csv", ("\n".join(mlines) + "\n").encode())


if __name__ == "__main__":
    main()
