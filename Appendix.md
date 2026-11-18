# Appendix

*The running record. Filled from the first step, not at the end. Everything that does not belong in the report belongs here: the workings, the diagnostics, the decisions and what each one cost.*

## Data Summary

This analysis replicates Ranganathan, Spaiser and Sumpter (2013), which models the joint change of democracy and log GDP per capita across countries. Where the 2013 paper leaves a detail out, it is taken from Ranganathan et al. (2014). The data comes from two sources, joined on ISO 3166 alpha-3 country code and year.

### Provenance

| Variable | Source | File in `Attachments/` | Downloaded | SHA-256 |
| --- | --- | --- | --- | --- |
| GDP per capita | World Bank, World Development Indicators, indicator `NY.GDP.PCAP.KD`, release last updated 2026-11-11 (World Bank, 2026) | `worldbank/API_NY.GDP.PCAP.KD_DS2_en_csv_v2_71952.csv` (with the country and indicator metadata files and the original `.zip`) | 2026-11-18 | `5008f829…a761552e` (CSV); `2c10c3b5…a63ca152d6` (zip) |
| Democracy | Welzel's citizen rights index `wel_citrig` (Welzel, 2013), as republished in the Quality of Government Standard Time-Series dataset, January 2015 release (Teorell et al., 2015) | `qog_std_ts_jan15.csv`, with the codebook `qog_std_jan15_codebook.pdf` | 2026-11-18 | `07ab1722…ef466758` (CSV); `59e23c5c…fa22c8` (codebook) |

- **Why these sources.** The contract makes the World Bank the standard source, and both papers took GDP per capita from it. The World Bank doesn't publish a democracy index, so that came from elsewhere.
- **The democracy index is the papers' own.** Ranganathan et al. (2014) describe it as Welzel's (2013) index: Freedom House political rights and civil liberties, weighted by two Cingranelli–Richards human-rights indices. `wel_citrig` is that index (codebook §4.85.5).
- **The democracy file is an archived republication, not the publisher's live file.** Quality of Government dropped Welzel's variables from later releases; the January 2026 time-series file has no `wel_` columns. The January 2015 release is the latest that carries them.
- **Our World in Data was checked and has neither series in usable form.** A search for "Welzel" returns nothing. Its World Bank GDP series is the purchasing-power-adjusted one, which starts in 1990.
- **The World Bank vintage differs from the papers'.** They used an edition current around 2012–13 (Ranganathan et al. 2014 cite WDI accessed September 2013). Constant-price series have since been rebased to 2015 dollars and revised. Coefficients involving GDP are therefore not expected to match the papers exactly.

### Columns used

| Column | Source column | Unit | Measurement or model output |
| --- | --- | --- | --- |
| country | World Bank `Country Code`; QoG `ccodealp` | ISO 3166 alpha-3 | identifier |
| year | year columns (World Bank); `year` (QoG) | calendar year | identifier |
| GDP per capita | `NY.GDP.PCAP.KD` | constant 2015 US$ per person | National accounts, compiled by national statistical offices with World Bank staff estimates where those are missing. It's a statistical estimate rather than a direct observation. |
| Democracy | `wel_citrig` | index from 0 (no citizen rights) to 1 (full citizen rights) | A constructed index: Freedom House ratings, themselves expert judgements, multiplied by human-rights scores. It's an expert-coded index, not a measurement. |

### What the files contain

From `Code/01_describe_data.py`; full output in `Code/outputs/01_describe_data.txt`.

- **World Bank file.**
  - 266 economies, of which 217 are countries and 48 are aggregates such as regions and income groups; 1960–2025.
  - 1980–2006: 204 countries have at least one value, and 159 have all 27 years.
  - Coverage rises from 159 countries in 1980 to 204 in 2006. The largest jump is in 1990, from 174 to 192, as former Soviet and Yugoslav states enter.
  - Values range from 165 to 140,615 dollars, median 3,645. None is zero or negative.
- **QoG file.**
  - 14,559 rows, 211 units, 1946–2014.
  - `wel_citrig` is present for 1981–2010, so the 1980 start given in the 2013 paper's text can't be reproduced. That paper's own Figure 2 begins in 1981.
- **Missing-value code in `wel_citrig`.**
  - 852 values are exactly −99, a missing-value code, not an index value. 840 of them fall in 1981–2006, across 83 units.
  - They are unevenly spread over the years: 35–42 a year in 1981–1999, 59 in 2000, then 3 in 2001, 34 in 2002, and 3–5 a year after that.
  - After treating them as missing there are 4,533 valid values in 191 units. 3,785 of them, in 190 units, fall in 1981–2006.
  - Valid coverage per year in 1981–2006 is 120 countries in 1981, 130 in 1990, 129 in 2000, 185 in 2001, 154 in 2002, and 183–185 in 2003–2006.
- **Zeros in `wel_citrig`.**
  - 141 country-years in 1981–2006 are exactly 0, in 22 countries.
  - The most are Iraq (19), North Korea (17), Afghanistan (16), Sudan (13), Saudi Arabia (12) and Myanmar (11).
  - The smallest positive value is 0.0022, and 83 values lie strictly between 0 and 0.01.
- **Duplicate country codes in QoG.** QoG keeps historical units, for example Ethiopia before and after 1993 and West Germany, some under the same ISO code. No (country, year) pair in 1981–2006 has more than one valid `wel_citrig` value, so the join is one-to-one.
- **Overlap.**
  - With both variables valid in 1981–2006 there are 3,679 country-years in 184 countries.
  - Three QoG units have `wel_citrig` but no World Bank counterpart: Czechoslovakia (`CSK`), Taiwan (`TWN`), and the German Democratic Republic (`DDR`). The GDR's values are all −99 in this window.

### Decisions

| Decision | Choice | Reasoning and cost |
| --- | --- | --- |
| Sources | World Bank for GDP; QoG archive for democracy | See Provenance. Cost: the GDP vintage is later than the papers'. |
| Years | 1981–2006 | 1981 is the first year of `wel_citrig`. 2006 is the papers' last year. One-year changes therefore run from 1981→1982 to 2005→2006. |
| Countries | Every country with both variables, before any panel-completeness rule | The user's choice ("use countries you have"). The 2013 paper used 189 countries and the 2014 paper 74, and neither lists them. Whether a country needs consecutive years to contribute a change is settled when the changes are built. |
| −99 in `wel_citrig` | Set to missing (840 values in 1981–2006) | It's a documented missing-data code, not an index value. Left in, it would be read as a democracy level of −99. |
| GDP transform | Natural log of GDP per capita, then rescaled | The user's choice. The 2013 paper's axes (about 5 to 12) fit natural logs of dollars. Ranganathan et al. (2014) evidently rescaled GDP, since their coefficients only make sense for GDP of order 1. **Open:** how to rescale. See the note below. |
| Zeros in `wel_citrig` | **Open.** Reported above, not yet decided | Terms such as $1/D$, $G/D$ and $1/D^2$ in the 13-term library are undefined at $D=0$. Neither paper says how this was handled. |
| Missing values | Left missing, not imputed | Nothing is interpolated. A country-year missing either variable contributes no observation. |

The rescaling method is open because the choice interacts with the $1/G$-type terms. Min–max scaling of log GDP to $[0,1]$ would put the poorest country-year at exactly 0 and make those terms undefined. Dividing log GDP by its maximum keeps every value strictly positive, at about 0.43–1.

## Research Question

*Written in step 2, before anything is tested. Three parts: `Discussion` — how the question was arrived at and what was ruled out; `Question` — the single main thing being asked; `Sub-questions` — the separately answerable parts, each naming its variables and what would count as an answer either way.*

## Analysis

*The workings, one sub-heading per sub-question, added as steps 3 and 4 proceed. Diagnostics, alternative specifications, checks that changed nothing, and anything computed but not reported.*

## Analysis Log

*A numbered row per step taken, added as the work happens. What was done, what it changed, and where the output is. Superseded decisions stay, marked as such — a reader cannot judge a choice without seeing the alternatives.*

| # | What was done | Output |
| --- | --- | --- |
| 1 | Step 1. Chose to replicate Ranganathan, Spaiser and Sumpter (2013), with gaps filled from Ranganathan et al. (2014). Method choices agreed with the user before any data was seen: normal prior on coefficients, natural log of GDP per capita then rescaled, the 2013 paper's 13-term library, and all countries with both variables. | `instructions.md` (`Statistical Framework`, `Report Format`) |
| 2 | Step 1. Looked for the democracy index. Our World in Data doesn't carry Welzel's index, and the current Quality of Government release has dropped it. Downloaded the archived January 2015 Quality of Government time-series file and its codebook. | `Attachments/qog_std_ts_jan15.csv`, `Attachments/qog_std_jan15_codebook.pdf` |
| 3 | Step 1. Downloaded World Bank `NY.GDP.PCAP.KD` (release of 2026-11-11). An earlier plan to check Our World in Data first was superseded by the rule that the World Bank is the standard source. | `Attachments/worldbank/` |
| 4 | Step 1. Described both files. Found the −99 missing-value code in `wel_citrig` (840 values in 1981–2006) and 141 zeros. Duplicate ISO codes in the Quality of Government file don't produce duplicate country-years. | `Code/01_describe_data.py`, `Code/outputs/01_describe_data.txt` |

## Code Summary

| File | What it does | Reads | Writes |
| --- | --- | --- | --- |
| `Code/01_describe_data.py` | Describes the two source files: shape, coverage per year, ranges, the −99 code, zeros, duplicate codes, and the overlap. It changes no data and draws no conclusions. Run with `cd Code && uv run python 01_describe_data.py`. | `Attachments/worldbank/API_NY.GDP.PCAP.KD_DS2_en_csv_v2_71952.csv` and its country metadata; `Attachments/qog_std_ts_jan15.csv` (columns `ccode`, `cname`, `year`, `ccodealp`, `wel_citrig`) | `Code/outputs/01_describe_data.txt` |

## References

Ranganathan, S., Spaiser, V., Mann, R. P. and Sumpter, D. J. T. (2014). [Bayesian dynamical systems modelling in the social sciences](https://doi.org/10.1371/journal.pone.0086468). *PLOS ONE*, 9(1), e86468.

Ranganathan, S., Spaiser, V. and Sumpter, D. J. T. (2013). [A Bayesian approach to modeling dynamical systems in the social sciences](https://doi.org/10.5220/0004480901250131). In *Proceedings of the 3rd International Conference on Simulation and Modeling Methodologies, Technologies and Applications (SIMULTECH 2013)*, pp. 125–131. SCITEPRESS.

Teorell, J., Dahlberg, S., Holmberg, S., Rothstein, B., Hartmann, F. and Svensson, R. (2015). [The Quality of Government Standard Dataset, version Jan15](https://www.qogdata.pol.gu.se/dataarchive/qog_std_ts_jan15.csv). University of Gothenburg: The Quality of Government Institute. [Codebook](https://www.qogdata.pol.gu.se/dataarchive/qog_std_jan15.pdf).

Welzel, C. (2013). *Freedom Rising: Human Empowerment and the Quest for Emancipation*. Cambridge University Press. [Open-access PDF](https://cambridge.org/de/files/8613/8054/8416/FreedomRising_OA.pdf).

World Bank (2026). [GDP per capita (constant 2015 US$), NY.GDP.PCAP.KD](https://api.worldbank.org/v2/en/indicator/NY.GDP.PCAP.KD?downloadformat=csv). World Development Indicators, release last updated 11 November 2026; downloaded 18 November 2026.
