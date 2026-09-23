# Source Data Provenance

**Not included in this repository.** The World Happiness Report publishes no licence or redistribution terms for this file, and its survey data belongs to Gallup, so neither the file nor the row-level CSVs derived from it in `Code/outputs/` are committed. The sample's documents, figures and summary outputs are complete without it. To re-run the sample's code, download the file from the archive snapshot below into this folder and check its SHA-256 matches:

```bash
curl -L -o DataForTable2.1.xls 'https://web.archive.org/web/20241202221257id_/https://happiness-report.s3.amazonaws.com/2024/DataForTable2.1.xls'
shasum -a 256 DataForTable2.1.xls
```

## DataForTable2.1.xls

The World Happiness Report's panel of **raw** underlying variables — the measures in their own natural units, rather than the modelled contributions published in the Figure 2.1 workbooks.

| Field | Value |
| --- | --- |
| Retrieved from | `https://web.archive.org/web/20241202221257/https://happiness-report.s3.amazonaws.com/2024/DataForTable2.1.xls` |
| Original URL | `https://happiness-report.s3.amazonaws.com/2024/DataForTable2.1.xls` |
| Archive snapshot | 2 December 2024 |
| Workbook last saved | 14 March 2024 (file metadata) |
| Retrieved | 2026-09-02 |
| Size | 521,216 bytes |
| SHA-256 | `dd5d9c737f86a05eec5ddaef644c37e3528fca125d9716ec51eb48697fff8349` |
| Sheet | `Sheet1` (the only sheet) |
| Shape | 2,363 rows × 11 columns |
| Edition | World Happiness Report **2024** |

### Why this file, retrieved this way

WHR no longer publishes a machine-readable panel of raw factor values. Checked 2026-09-02: the data-sharing page offers only `Figure 2.1` workbooks, which contain **modelled contributions in ladder points** rather than measurements, and the 2026 Chapter 2 statistical appendix is PDF only. Raw Gallup World Poll variables otherwise require a Gallup request or subscription.

This file was published by WHR up to the 2024 edition and remains available through the Internet Archive. It is used because the analysis requires variables in interpretable units — dollars, years, proportions.

**Provenance caveat.** This came from an archive snapshot, not from the publisher's live site. The file cannot currently be re-downloaded from `worldhappiness.report` to confirm it. The checksum above pins exactly what was used.

### Citation

Helliwell, J. F., Layard, R., Sachs, J. D., De Neve, J.-E., Aknin, L. B., & Wang, S. (Eds.). (2024). *World Happiness Report 2024*. University of Oxford: Wellbeing Research Centre.

Underlying survey data is the Gallup World Poll. Documentation of the variables is in `WHR24_Statistical_Appendix.pdf`, available from <https://www.worldhappiness.report/data-sharing/>.

### Units, per the WHR 2024 statistical appendix

| Column | Unit |
| --- | --- |
| `Life Ladder` | 0–10 Cantril ladder. National average for that **single year** — not a 3-year average. |
| `Log GDP per capita` | Natural log of GDP per capita, PPP, at **constant 2017 international dollars**. World Development Indicators v23; Taiwan, Syria, Palestinian Territories, Venezuela, Djibouti and Yemen from Penn World Table 10.01. |
| `Social support` | Proportion, 0–1. National average of yes/no answers to "If you were in trouble, do you have relatives or friends you can count on to help you whenever you need them?" |
| `Healthy life expectancy at birth` | **Years.** WHO Global Health Observatory, interpolated and extrapolated to cover the sample period. |
| `Freedom to make life choices` | Proportion, 0–1. National average of satisfied/dissatisfied with "your freedom to choose what you do with your life". |
| `Generosity` | Unitless **residual** of regressing the national average of "Have you donated money to a charity in the past month?" on GDP per capita. Already income-adjusted, and can be negative. |
| `Perceptions of corruption` | Proportion, 0–1. Average of two yes/no items on whether corruption is widespread in government and in business. |
| `Positive affect` | Proportion, 0–1. Average of three yes/no items: laughter, enjoyment, and doing something interesting yesterday. |
| `Negative affect` | Proportion, 0–1. Average of three yes/no items: worry, sadness, anger yesterday. |

Note that `Log GDP per capita` is a **log**, so exponentiate to recover dollars, and equal increments correspond to equal proportional differences in income.

### Handling

Do not modify this file. All derived data is written to `Code/outputs/`.
