# Source data

The World Bank files in `worldbank/` are committed. They are World Development Indicators data, published under CC BY 4.0.

The Quality of Government files are not committed. One is large (66 MB), and both are a republication of third-party data. Download them into this folder and check the checksums:

| File | URL | SHA-256 |
| --- | --- | --- |
| `qog_std_ts_jan15.csv` | https://www.qogdata.pol.gu.se/dataarchive/qog_std_ts_jan15.csv | `07ab1722a1bb4a8a1044cb2fca3464bf418107060b672f248c468b03ef466758` |
| `qog_std_jan15_codebook.pdf` | https://www.qogdata.pol.gu.se/dataarchive/qog_std_jan15.pdf | `59e23c5cf931c1b69b780b4d83fae421932592c64c90ffeeaf039f5c43ab22c8` |

```sh
cd Attachments
curl -o qog_std_ts_jan15.csv https://www.qogdata.pol.gu.se/dataarchive/qog_std_ts_jan15.csv
curl -o qog_std_jan15_codebook.pdf https://www.qogdata.pol.gu.se/dataarchive/qog_std_jan15.pdf
shasum -a 256 qog_std_ts_jan15.csv qog_std_jan15_codebook.pdf
```

## V-Dem (question 2)

Not committed (204 MB unzipped). V-Dem Country-Year Core dataset, version 15 (Coppedge et al., 2025), downloaded 18 November 2026:

| File | URL | SHA-256 |
| --- | --- | --- |
| `vdem/V-Dem-CY-Core-v15_csv.zip` | https://v-dem.net/media/datasets/V-Dem-CY-Core-v15_csv.zip | `bd6430d6b78785c7422acee7d75bef1b852f2ce1baa5f673ae40ffca64ffe51b` |

```sh
mkdir -p Attachments/vdem && cd Attachments/vdem
curl -L -o V-Dem-CY-Core-v15_csv.zip https://v-dem.net/media/datasets/V-Dem-CY-Core-v15_csv.zip
unzip V-Dem-CY-Core-v15_csv.zip V-Dem-CY-Core-v15.csv codebook.pdf suggested_citation.pdf
```
