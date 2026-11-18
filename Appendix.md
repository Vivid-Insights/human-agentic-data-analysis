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
- **The democracy index is the papers' own.** Ranganathan et al. (2014) describe it as Welzel's (2013) index: Freedom House political rights and civil liberties, weighted by two Cingranelli–Richards human-rights indices. `wel_citrig` is that index (codebook §4.85.5). Spaiser et al. (2014, File S1, §S12.2) give the construction: Freedom House political rights plus CIRI empowerment rights give political participation; Freedom House civil liberties plus CIRI personal integrity rights give personal autonomy; the two are multiplied. That matches the codebook's definition, CitRig = PAR × PPR.
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
| Countries | Every country with both variables, before any panel-completeness rule | The user's choice ("use countries you have"). The 2013 paper used 189 countries and the 2014 paper 74, and neither lists them. Panel rule, the contract's default: a change needs both of its years, so every pair of consecutive years present for a country is used. Countries are not required to be observed throughout. Gaps from the −99 codes, notably in 2000 and 2002, mean those countries contribute fewer changes rather than none. |
| Unmatched units | Dropped | Czechoslovakia (`CSK`) and Taiwan (`TWN`) have democracy values but no World Bank GDP. The German Democratic Republic (`DDR`) has no valid democracy value in 1981–2006. |
| Coverage dips in 2000 and 2002 | Accepted as-is | Valid democracy values for 129 and 154 countries, against 185 in 2001. The cause is the source's −99 codes. Nothing is interpolated to fill them. |
| Interpolation | None | Both variables are published yearly. Neither is interpolated by us, and neither source documents interpolation for these series. |
| −99 in `wel_citrig` | Set to missing (840 values in 1981–2006) | It's a documented missing-data code, not an index value. Left in, it would be read as a democracy level of −99. |
| GDP transform | $G = \ln(\text{GDP per capita}) / 12$ | The user chose a natural log, then rescaling. Dividing by 12 is the series' own procedure, stated in Spaiser et al. (2014, File S1, §S12.4) and Ranganathan et al. (2015b). In our data $G$ runs from 0.43 to 0.99. Min–max scaling was rejected because it would put the poorest country-year at $G=0$, where the $1/G$-type terms are undefined. |
| Zeros in `wel_citrig` | Keep all values, including the 141 exact zeros. Remove from the term library every term with $D$ in the denominator: $1/D$, $1/D^2$, $G/D$ and $1/(DG)$. That leaves 9 of the 13 terms: $1,\ D,\ G,\ 1/G,\ D/G,\ DG,\ D^2,\ G^2,\ 1/G^2$, so $2^9 = 512$ candidate models per equation. | The user's choice. Those four terms are undefined at $D=0$. Near zero they are dominated by a few points: $1/D$ is about 450 at the smallest positive value. None of the six papers checked says how zeros were handled: the 2013 and 2014 method papers, the two 2015 papers by Ranganathan, Bali Swain and Sumpter, the democracy-traps paper (2015b), and Spaiser et al. (2014) including File S1. No democracy equation reported in any of them contains an inverse-$D$ term. Every inverse term they did select divides by a variable bounded away from zero, such as GDP, fertility or life expectancy. So the reduced library still contains every model those papers report. The cost is a smaller candidate set than the papers searched, so this is no longer a 13-term replication. No observations are lost. |
| Zeros: superseded | ~~Keep the zeros and replace $D$ by $D+\tfrac12$ wherever it is in a denominator, e.g. $1/(\tfrac12+D)$~~ | Proposed by the user, then replaced by removing the inverse-$D$ terms before anything was fitted. The shift would have kept all 13 terms and bounded $1/(\tfrac12+D)$ between 0.67 and 2. Also considered and not taken: dropping the 141 zero country-years, which would lose the most autocratic states. |
| Missing values | Left missing, not imputed | Nothing is interpolated. A country-year missing either variable contributes no observation. |


## Research Question

*Written in step 2, before anything is tested. Three parts: `Discussion` — how the question was arrived at and what was ruled out; `Question` — the single main thing being asked; `Sub-questions` — the separately answerable parts, each naming its variables and what would count as an answer either way.*

## Analysis

*The workings, one sub-heading per sub-question, added as steps 3 and 4 proceed. Diagnostics, alternative specifications, checks that changed nothing, and anything computed but not reported.*

## Analysis Log

*A numbered row per step taken, added as the work happens. What was done, what it changed, and where the output is. Superseded decisions stay, marked as such — a reader cannot judge a choice without seeing the alternatives.*

| # | What was done | Output |
| --- | --- | --- |
| 1 | Step 1. Chose to replicate Ranganathan, Spaiser and Sumpter (2013), with gaps filled from Ranganathan et al. (2014). Method choices agreed with the user before any data was seen: normal prior on coefficients, natural log of GDP per capita then rescaled, the 2013 paper's 13-term library (superseded in row 5), and all countries with both variables. | `instructions.md` (`Statistical Framework`, `Report Format`) |
| 2 | Step 1. Looked for the democracy index. Our World in Data doesn't carry Welzel's index, and the current Quality of Government release has dropped it. Downloaded the archived January 2015 Quality of Government time-series file and its codebook. | `Attachments/qog_std_ts_jan15.csv`, `Attachments/qog_std_jan15_codebook.pdf` |
| 3 | Step 1. Downloaded World Bank `NY.GDP.PCAP.KD` (release of 2026-11-11). An earlier plan to check Our World in Data first was superseded by the rule that the World Bank is the standard source. | `Attachments/worldbank/` |
| 4 | Step 1. Described both files. Found the −99 missing-value code in `wel_citrig` (840 values in 1981–2006) and 141 zeros. Duplicate ISO codes in the Quality of Government file don't produce duplicate country-years. | `Code/01_describe_data.py`, `Code/outputs/01_describe_data.txt` |
| 5 | Step 1. Zeros in democracy. The user first proposed replacing $D$ by $D+\tfrac12$ in denominators, then chose to remove the four inverse-$D$ terms instead. The library is now 9 terms, 512 models per equation. Before deciding, checked all six papers: none says how zeros were handled, and no selected democracy equation in any of them has an inverse-$D$ term. Rescaling settled as $\ln(\text{GDP per capita})/12$, from Spaiser et al. (2014, File S1). | `Appendix.md` `Data Summary`, decisions table |
| 6 | Step 1. Contract changes from what this step taught: scan for missing-value codes; join and aggregate checks; fixed-constant scaling; zero checks with inverse-term removal; flag interpolated series; default panel rule. Applied here: the panel rule, dropping the unmatched units, and accepting the coverage dips. | `instructions.md` (`The Standard Analysis`, step 1) |
| 7 | Step 1 closed by the user on 2026-11-18. Everything in its checklist is settled. The prior's $\lambda$ is left to step 4. | — |

## Code Summary

| File | What it does | Reads | Writes |
| --- | --- | --- | --- |
| `Code/01_describe_data.py` | Describes the two source files: shape, coverage per year, ranges, the −99 code, zeros, duplicate codes, and the overlap. It changes no data and draws no conclusions. Run with `cd Code && uv run python 01_describe_data.py`. | `Attachments/worldbank/API_NY.GDP.PCAP.KD_DS2_en_csv_v2_71952.csv` and its country metadata; `Attachments/qog_std_ts_jan15.csv` (columns `ccode`, `cname`, `year`, `ccodealp`, `wel_citrig`) | `Code/outputs/01_describe_data.txt` |

## References

Ranganathan, S., Spaiser, V., Mann, R. P. and Sumpter, D. J. T. (2014). [Bayesian dynamical systems modelling in the social sciences](https://doi.org/10.1371/journal.pone.0086468). *PLOS ONE*, 9(1), e86468.

Ranganathan, S., Spaiser, V. and Sumpter, D. J. T. (2013). [A Bayesian approach to modeling dynamical systems in the social sciences](https://doi.org/10.5220/0004480901250131). In *Proceedings of the 3rd International Conference on Simulation and Modeling Methodologies, Technologies and Applications (SIMULTECH 2013)*, pp. 125–131. SCITEPRESS.

Ranganathan, S., Nicolis, S. C., Spaiser, V. and Sumpter, D. J. T. (2015b). [Understanding democracy and development traps using a data-driven approach](https://doi.org/10.1089/big.2014.0066). *Big Data*, 3(1), 22–33.

Spaiser, V., Ranganathan, S., Mann, R. P. and Sumpter, D. J. T. (2014). [The dynamics of democracy, development and cultural values](https://doi.org/10.1371/journal.pone.0097856). *PLOS ONE*, 9(6), e97856. Supporting information: [File S1](https://journals.plos.org/plosone/article/file?type=supplementary&id=10.1371/journal.pone.0097856.s001).

Teorell, J., Dahlberg, S., Holmberg, S., Rothstein, B., Hartmann, F. and Svensson, R. (2015). [The Quality of Government Standard Dataset, version Jan15](https://www.qogdata.pol.gu.se/dataarchive/qog_std_ts_jan15.csv). University of Gothenburg: The Quality of Government Institute. [Codebook](https://www.qogdata.pol.gu.se/dataarchive/qog_std_jan15.pdf).

Welzel, C. (2013). *Freedom Rising: Human Empowerment and the Quest for Emancipation*. Cambridge University Press. [Open-access PDF](https://cambridge.org/de/files/8613/8054/8416/FreedomRising_OA.pdf).

World Bank (2026). [GDP per capita (constant 2015 US$), NY.GDP.PCAP.KD](https://api.worldbank.org/v2/en/indicator/NY.GDP.PCAP.KD?downloadformat=csv). World Development Indicators, release last updated 11 November 2026; downloaded 18 November 2026.
