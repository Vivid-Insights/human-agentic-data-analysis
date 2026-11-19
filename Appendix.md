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


### V-Dem electoral democracy index (question 2)

Added in step 1 for question 2. Description from `Code/11_describe_vdem.py`, output in `Code/outputs/11_describe_vdem.txt`.

- **Provenance.** V-Dem Country-Year Core dataset, version 15 (Coppedge et al., 2025), `V-Dem-CY-Core-v15_csv.zip`, from v-dem.net, downloaded 2026-11-18, SHA-256 `bd6430d6…ffe51b`. It is gitignored (204 MB unzipped); `Attachments/SOURCE.md` gives the download. The dataset DOI resolves.
  - **Source choice.** Not World Bank data, so it comes from the publisher. It is chosen as the standard alternative to Welzel's index: built differently, and covering 1981–2024.
- **Variable.** `v2x_polyarchy`, the electoral democracy index. The codebook (version 15, p. 47) gives it an interval scale from 0 to 1 and describes it as an aggregate of five sub-indices: freedom of association, clean elections, freedom of expression, elected officials and suffrage.
  - It is a constructed index. Each value is an estimate from V-Dem's measurement model of many expert ratings, not a direct measurement.
- **What the file contains.**
  - 27,913 rows, 202 countries, 1789–2024. For 1981–2024: 7,618 rows, 181 countries, 7,617 values present.
  - Values run from 0.013 to 0.923 (median 0.445). There are no zeros, no values below 0.01, no negative codes and no values outside [0, 1].
  - Countries with a value per year: 157 in 1981, 173 in 1991, 177 in 2006, and 179 in 2024. There are no duplicate country-years.
- **Overlap with World Bank GDP.** 7,217 country-years in 174 countries for 1981–2024: 4,126 in 171 countries for 1981–2006, and 3,091 in 174 for 2007–2024. V-Dem codes with no World Bank country: `DDR`, `PSG`, `SML`, `TWN`, `YMD`, `ZZB`, all dropped.
- **Decisions.**
  - **Same library as the main analysis.** The same nine terms, even though V-Dem is never zero and could take the inverse-democracy terms, so the two measures are compared on the same model (agreed choice 2).
  - **No rescaling.** The index is already 0 to 1.
  - **Panel rule as before.** Built by `Code/12_build_panel_vdem.py`: 3,955 changes from 171 countries to fit (1981–2006), and 3,088 changes from 174 countries to test (2007–2024). 168 countries have both variables in 2006 and in 2024.
- **The World Bank GDP file** already covered 1960–2025, so no new GDP download was needed. 2025 is not used, because V-Dem ends in 2024.

## Research Question

Written in step 2, on 18 November 2026, before anything was fitted or plotted. Nothing in this section was computed from the data. The only arithmetic is a change of scale applied to the paper's published coefficients.

### Discussion

This analysis is a replication, and it checks the method this branch is built on. The question is taken from the introduction of Ranganathan, Spaiser and Sumpter (2013), as the user asked. That introduction makes three moves.

- Social scientists usually relate variables through regression, and read the results statically: the level of one variable against the level of another.
- Social systems are dynamic, so it is more natural to model how each variable changes as a function of the current state of all of them, and to let the data choose the form of that function from a pool of candidates instead of fixing it from theory.
- The test case is the relationship between a country's income and its level of democracy. The paper says political scientists have debated it for 50 years, citing Lipset (1959), Barro (1996, 1999), Boix and Stokes (2003) and Krieckhaus (2003). These are given as the paper cites them; we have not yet opened them, which is step 6's work. The paper reads Barro (1996) as concluding that GDP per capita raises democracy while democracy has no direct effect on growth, and more recent work as suggesting the relationship is non-linear and dynamic.

The question here is therefore the paper's own. Its framing of the background is recorded here and taken up in step 6. The step 6 background will cite the original works, not the 2013 paper's summary of them.

Feasibility, from the `Data Summary`:

- Both variables are present for 1981–2006: 3,679 country-years in 184 countries before the panel rule.
- Both are yearly, so the year-to-year changes are not interpolated.
- The democracy index is the one the paper used. GDP comes from a later World Bank release, in constant 2015 dollars, so coefficients involving GDP are not expected to match exactly.
- One structural limit: pooling all countries assumes they share one set of dynamics. The paper names this "mean-field" assumption itself, so it is part of what is being replicated, not a reason to change the question.

Considered and set aside:

- Lagged GDP and the three-variable models of Ranganathan et al. (2014). These are extensions of the 2013 model, not part of it.
- The PLOS ONE version of the same application (74 countries, a 17-term library). The user chose the 2013 paper.

### Question

When the yearly changes in democracy and in GDP per capita are each modelled as a polynomial function of the current levels of both, as in Ranganathan, Spaiser and Sumpter (2013), are the equations selected the same as those the paper reports, and do they imply the same dynamics?

### The paper's answers, on our scale

The paper uses $G_p$, the natural log of GDP per capita. We use $G = G_p/12$, so $G_p = 12G$ and $\Delta G_p = 12\,\Delta G$. Substituting into the paper's two equations gives:

| Equation | As published, in $G_p$ | On our scale, in $G$ |
| --- | --- | --- |
| Change in democracy | $\Delta D = 0.0003\,G_p^2 - 0.4031\,D/G_p$ | $\Delta D = 0.0432\,G^2 - 0.0336\,D/G$ |
| Change in GDP | $\Delta G_p = 0.0246\,D + 0.0017\,G_p - 0.0002\,G_p^2$ | $\Delta G = 0.00205\,D + 0.0017\,G - 0.0024\,G^2$ |

This conversion rests on the paper having used natural logs without rescaling. That is inferred from its axes, which run from about 5 to 12, but it is not stated. Every term in both equations is in our 9-term library: $G^2$, $D/G$, $D$ and $G$. So removing the inverse-$D$ terms does not take the paper's models out of reach.

### Sub-questions

*Superseded in step 4 (log row 25): at the user's request the report now asks a single question, "What model best describes the yearly changes in democracy and GDP per capita, and what dynamics does it imply?" The three sub-questions below are kept as the record of what was framed in step 2. Their reproduction criteria still apply to the comparison with the 2013 paper, which this appendix records under each sub-question heading in `Analysis`.*

These are the branch's three default sub-questions. In a replication, "an answer either way" means reproducing the paper or not.

1. **How does the yearly change in democracy depend on the current levels of democracy and GDP?**
   - Variables: $\Delta D$ against $D$ and $G$.
   - The paper is reproduced if the selected model has the same terms ($G^2$ and $D/G$) with the same signs (positive, negative). It is not reproduced if different terms are selected, or the same terms with a different sign.
   - The coefficients are compared with the converted values above, and we report whether each lies inside our 95% credible interval. The vintage difference means this comparison is reported, not used to decide the answer.
   - The posterior probability of the paper's model size against the selected one is also reported.
2. **How does the yearly change in GDP depend on the current levels of democracy and GDP?**
   - Variables: $\Delta G$ against $D$ and $G$.
   - The paper is reproduced if the selected model has the terms $D$, $G$ and $G^2$, with signs positive, positive, negative. It is not reproduced otherwise.
   - Whether democracy enters at all is the point of substance in the debate the paper addresses. If it does not, we report how firmly it is excluded: the evidence for the best model that includes $D$ against the selected one.
   - Coefficients are compared as in sub-question 1.
3. **What do the two equations imply together?**
   - Variables: the fitted vector field over the observed range of $D$ and $G$, and trajectories integrated from each country's first observed state.
   - The paper is reproduced if the fitted system has an attracting curve running from low $D$, low $G$ to high $D$, high $G$, onto which trajectories converge, with countries high in democracy and low in GDP losing democracy until they reach it. It is not reproduced if there is no such curve within the observed range, or if trajectories do not converge onto it.
   - This is judged from the phase portrait, with the curves where each change is zero computed from the fitted equations, not read off the figure.

### Standard analysis proposal

The eight parts of `The Standard Analysis` for this replication. Departures from the 2013 paper are marked.

| Part | This analysis |
| --- | --- |
| Variables | $D$: Welzel's citizen rights index `wel_citrig`, 0–1, an expert-coded index. $G$: World Bank `NY.GDP.PCAP.KD`, constant 2015 US$, a national-accounts estimate. Departure: GDP vintage and base year. |
| Transformations | $G = \ln(\text{GDP per capita})/12$. $D$ unchanged. Departure: the paper does not rescale; its coefficients are converted above. |
| The system | $\Delta D(t) = f_D(D(t), G(t))$ and $\Delta G(t) = f_G(D(t), G(t))$, pooled over countries, using every pair of consecutive years present in 1981–2006. Departure: years start in 1981, not 1980. |
| Term library | 9 terms, the paper's 13 without the four with $D$ in the denominator: $1, D, G, 1/G, D/G, DG, D^2, G^2, 1/G^2$. That gives 512 models per equation. Departure: 9 terms, not 13. |
| Search | Every model of every size; best by likelihood within each size; sizes compared by evidence. As in the paper. |
| Prior | Normal, $N(0, \lambda^2 I)$, with closed-form evidence (Ranganathan et al., 2014). $\lambda$ set and stated in step 4. Noise variance as in Ranganathan et al. (2014). Departure: the paper used a uniform prior with Monte Carlo integration. |
| Checks | Within-country correlation of residuals; correlation of errors between the two equations (the paper's seemingly unrelated regressions check); refits on resampled countries. Departure: the resampling refits are an addition. |
| Figures | The standard figures, as revised in step 3: trajectories over time; trajectories in the $(G, D)$ plane; the data phase portrait; the model phase portrait. Representative countries: the paper's six (Italy, Sweden, India, Chile, Albania, Nigeria), chosen because they are the paper's, not from how their paths look. Albania has 21 of 26 years and is drawn with gaps. No mean is drawn. GDP is shown in constant 2015 US dollars on a log axis. Departures: the paper has a one-year scatter, an all-country mean over time, and the model phase portrait. Here the scatter is folded into the plane figure, the mean is dropped, and the data phase portrait is added. (Superseded: the four figures first proposed, with a one-year scatter and the mean over time in place of the two trajectory figures; then a mean over the 84 countries observed every year, drawn as a thick line and then dropped.) |

### Question 2 (added at the end of step 6, at the user's request)

> "Lets use a different democracy measure and see if the results up to 2006 replicate, but also lets look to see if the model up to 2006 truely predicts what happened the last 20 years?"

- **Question.** Do the results hold with a different measure of democracy, and does the model fitted to 1981–2006 predict the changes from 2007 to 2024?
- **What counts as an answer either way.**
  - **Measure.** The results hold if, with V-Dem's index, democracy again enters the GDP equation, and the democracy nullcline again rises with income and attracts. Different terms do not count against this. A nullcline that does not rise, or democracy dropping out of the GDP equation, would.
  - **Prediction.** The model predicts 2007–2024 if its predictive density for the yearly changes is higher than the average-change model's, and if its 2024 states are closer to those observed than the average-change projection. It does not if it scores no higher.
- **Choices agreed before any data was seen.**
  1. The measure: V-Dem's `v2x_polyarchy`.
  2. The same nine-term library.
  3. Judging prediction by year-by-year predictive density against the average-change model and the same terms refitted to 2007–2024, and by 2024 states from stepping forward from 2006.
  4. One new figure, Figure 5.
- **Working.** The user asked for steps 1–6 for this question in one pass ("Do it all"), departing from one step per request; recorded in log row 38.
- **Why 2006 now has a reason.** The report ends the fit at 2006 because 2007–2024 is held back to test it. This replaces the gap noted earlier, where the cut-off had no reason the report could give.

## Analysis

### The analysis panel

Built by `Code/02_build_panel.py` from the step 1 decisions. Counts from `Code/outputs/02_panel_counts.txt`.

- 3,679 country-years with both variables, in 184 countries, 1981–2006. These match the step 1 overlap.
- 3,423 consecutive-year changes, from 183 countries. These are the observations the model will be fitted to.
- 84 countries have both variables in all 26 years. They defined the mean first drawn in Figures 1 and 2; the mean was then dropped (log row 15). The `balanced` flag stays in the panel but is not used by any figure.
- 181 countries have both variables in 2006. They are the grey points in Figure 2.
- $G$ runs from 0.425 to 0.988, and $D$ from 0 to 1.
- 108 of the 141 exact zeros in democracy survive the join. The other 33 are in country-years with no World Bank GDP, among them North Korea, Iraq and Somalia.
- Representative countries: Italy, Sweden, India, Chile and Nigeria have all 26 years (25 changes each). Albania has 21 years, 1981–1984 and 1990–2006, giving 19 changes.

### Figures 1 and 2 (step 3)

- **Style.** David's graph style inside the workspace themes: sizes in cm, 11 pt text with 10 pt legends, 300 dpi, no top or right spines, minor ticks every year on time axes. The six-colour palette from that style gives one fixed colour per representative country, set in `Code/sds_common.py`. The mean is drawn in the theme's ink, not a series colour. Each figure has light and dark versions, with opaque backgrounds and fixed canvas sizes. They render at 2124 × 1002 and 2007 × 1239 pixels, checked after saving.
- **Changes after the first render.** The GDP axis was relabelled from "GDP per capita" to "Log GDP per capita ÷ 12", so the axis says what $G$ is. Figure 2's legend was moved outside the axes, because inside it covered India's starting point and the mean's path.
- **Units (contract rule added after the first render).** GDP is now plotted in constant 2015 US dollars on a logarithmic axis, with ticks from \$500 to \$100k. Democracy is labelled "index, 0 to 1". Positions are unchanged, because the axis is linear in $\ln(\text{GDP})$ and so in $G$. The plotted dollars are computed as $e^{12G}$, which matches the source's GDP per capita to within $4 \times 10^{-10}$. The GDP mean is $e^{12\bar G}$, the geometric mean of GDP per capita over the 84 countries. Two layout fixes followed: the first dollar labels overlapped in Figure 2, so ticks are written \$1k, \$10k and so on; and the long axis label was cut off in Figure 1, so it reads "GDP per capita (2015 US\$)", with "constant" stated in the captions. Superseded: the "Log GDP per capita ÷ 12" axis label above.
- **Orientation.** GDP across and democracy up, as proposed and agreed, so the phase portraits can share these axes. The 2013 paper's phase portrait has democracy across and GDP up.

### Figure 3: the data phase portrait (step 3)

Made by `Code/05_fig_data_phase_portrait.py`. Counts from `Code/outputs/05_phase_portrait_counts.txt`; cell values in `Code/outputs/05_phase_cells.csv`.

- **Design.** The 3,423 yearly changes are averaged within a grid over the state.
  - Cells are 0.04 wide in $G$, a factor of $e^{0.48} \approx 1.62$ in GDP per capita, and 0.1 high in democracy. That gives 14 by 10 cells, 114 of them occupied.
  - Each arrow starts at the mean $(G, D)$ of the cell's country-years and points along their mean $(\Delta G, \Delta D)$ times $K$.
  - Both components are scaled by the same $K$ in model units, so directions are true on these axes. On the dollar axis the horizontal length is proportional GDP growth.
- **Choices after the first render.** The first draft used $K = 5$ years and at least 5 changes per cell. Arrows ran through neighbouring cells, and cells with few changes gave erratic averages (for example near \$100k). The cell-average $|\Delta D|$ has median 0.013 and 90th percentile 0.044. With $K = 2$, the 90th percentile arrow is about one cell high (0.09). Raising the minimum from 5 to 10 changes per cell drops 15 cells: from 98 to 83 arrows, and from 3,397 to 3,289 changes represented. Superseded: $K = 5$, at least 5 changes.
- **Longer, capped arrows (at the user's request).** "The arrows should be longer, but with a max on them. So we can better see the direction." Arrows are now drawn at $K = 5$ years. Any arrow longer than 0.7 cm on the page (about one cell, `CAP_CM`) is shortened to 0.7 cm by one factor applied to both components. The horizontal axis is linear in $G$, so the direction on the page is unchanged. 33 of the 83 arrows are shortened. The cap is measured after layout, in centimetres on the page, so the count depends on the axes' size. Widening the legend label to "(capped)" first narrowed the axes, changing the count from 31 to 29 and making the \$50k and \$100k ticks collide. The label was split over two lines to restore the width (33 capped). Superseded: $K = 2$ with no cap. Then, at the user's request ("two thirds of length and it is perfect"), both the length and the cap were multiplied by 2/3: $K = 3\tfrac13$ years and a cap of 0.467 cm. The same 33 of 83 arrows are capped, because both scale together. This version is locked in the contract (`Report Format`). Superseded: $K = 5$, cap 0.7 cm.
- **Shared axis range.** Figures 2 and 3 now share a fixed GDP range, \$150 to \$170,000 (`USD_XLIM` in `sds_common.py`), so the two can be laid over each other. The first draft of Figure 3 was cut at the grid edges, and with its longer legend label the \$50k and \$100k ticks collided.
- **Not used in the report.** Over all changes, the mean yearly change is 0.0023 in democracy and 0.00141 in $G$, which is 1.70% growth in GDP per capita a year.

### Sub-question 1: the yearly change in democracy (step 4)

Fitted by `Code/06_fit_change_model.py D`. Full output in `Code/outputs/06_fit_D.txt` and `06_fit_D.json`.

- **Setup, as agreed.** 3,423 changes from 183 countries. $\sigma$ is fixed at $\text{sd}(\Delta D) = 0.07194$. The prior is normal on RMS-scaled coefficients, with $\lambda = 0.07194$.
- **Best model of each size:**

| Size | Log-likelihood | Log-evidence | P(size) | $R^2$ | Terms |
| --- | --- | --- | --- | --- | --- |
| 1 | 4159.68 | 4155.61 | 0.0000 | 0.0041 | $D^2$ |
| 2 | 4194.02 | 4186.94 | 0.0000 | 0.0242 | $DG, D^2$ |
| 3 | 4209.91 | 4199.41 | 0.1882 | 0.0334 | $D/G, DG, D^2$ |
| 4 | 4216.31 | 4200.69 | 0.6816 | 0.0372 | $D, D/G, D^2, 1/G^2$ |
| 5 | 4217.00 | 4198.24 | 0.0584 | 0.0376 | $D, 1/G, D/G, D^2, G^2$ |
| 6 | 4217.14 | 4197.00 | 0.0170 | 0.0377 | $D, G, D/G, D^2, G^2, 1/G^2$ |
| 7 | 4220.22 | 4196.89 | 0.0152 | 0.0395 | $1, D, G, 1/G, DG, D^2, G^2$ |
| 8 | 4221.41 | 4195.90 | 0.0057 | 0.0402 | all but $D/G$ |
| 9 | 4221.41 | 4197.69 | 0.0340 | 0.0402 | all nine |

- **Selected model.** Four terms, with log Bayes factor 1.29 over the best three-term model. Posterior means and 95% intervals: $D$ +0.26653 [+0.20851, +0.32455]; $D/G$ −0.14365 [−0.17401, −0.11328]; $D^2$ −0.11760 [−0.15047, −0.08474]; $1/G^2$ +0.00303 [+0.00141, +0.00464].
- **Prior sensitivity.** With $\lambda \times 10$ the selection is unchanged. With $\lambda \times 0.1$ the nine-term model is selected. A prior that narrow expects each term to move democracy by at most about 0.007 a year, so it shrinks every coefficient hard and barely penalises extra terms. Reported here only; the agreed $\lambda$ stands.
- **Noise variance.** Estimating $\sigma$ from the residuals (0.07062 against 0.07194) selects the same four terms.
- **Within-country residual correlation, lag 1:** −0.141 over 3,201 pairs. The negative sign means a year with a larger-than-predicted change tends to be followed by a smaller one, as measurement noise in a level would produce. It is not the positive persistence that would make the posterior intervals too narrow.
- **Country resampling** (500 draws, seed 20261118).
  - The four-term model is selected in 184 of 500 draws. $D^2$ is selected in 500, $D/G$ in 488, $D$ in 327, $1/G^2$ in 253, $DG$ in 233 and $G^2$ in 113.
  - The 2.5–97.5 percentile ranges of the selected model's coefficients are 1.55, 1.41 and 1.51 times the posterior interval widths for $D$, $D/G$ and $D^2$, and 0.87 times for $1/G^2$.
  - Because it changes how the uncertainty should be read, this check is reported in one sentence in `Results` and named in `Methods`.
- **Comparison with Ranganathan, Spaiser and Sumpter (2013)** (`Code/outputs/06_fit_D_paper_model.txt`; replication only, not in the report).
  - **Not reproduced on the agreed criterion.** The paper's model has $G^2$ and $D/G$; the selected model shares $D/G$, with the same negative sign, but not $G^2$.
  - **The paper's model on our data.** Imposed on our data, it gives $G^2$ +0.0383 [+0.0293, +0.0473] and $D/G$ −0.0297 [−0.0362, −0.0231]. The paper's coefficients converted to our scale (+0.0432 and −0.0336) lie inside both intervals.
  - **How it ranks.** Its log-evidence is 4184.02, against 4200.69 for the selected model, a log Bayes factor of 16.7. It is also below our best two-term model ($DG$, $D^2$, 4186.94).
  - **So** the paper's equation describes our data with almost the same coefficients, but our search, with its larger data and different vintage, prefers a model with more terms in democracy.
- **Re-derived independently** (`Code/outputs/06_fit_D_rederive.txt`). The selected model's log-evidence, computed directly from the full 3,423 × 3,423 covariance matrix, is 4200.6944. The script's shortcut gives the same value. The posterior means are 0.93 to 1.01 times the least-squares estimates (OLS: +0.28789, −0.15404, −0.12707, +0.00299), the expected shrinkage from a prior as wide as the noise.

### Sub-question 2: the yearly change in GDP per capita (step 4)

Fitted by `Code/06_fit_change_model.py G`. Joint checks by `Code/07_joint_checks.py`. Output in `Code/outputs/06_fit_G.txt`, `06_fit_G.json` and `07_joint_checks.txt`.

- **Setup, as agreed for sub-question 1.** $\sigma = \lambda = \text{sd}(\Delta G) = 0.00492$, on RMS-scaled terms.
- **Best model of each size:**

| Size | Log-likelihood | Log-evidence | P(size) | $R^2$ | Terms |
| --- | --- | --- | --- | --- | --- |
| 1 | 13335.58 | 13331.47 | 0.0000 | 0.0020 | $D/G$ |
| 2 | 13351.22 | 13343.28 | 0.7476 | 0.0112 | $D, 1/G^2$ |
| 3 | 13352.04 | 13341.90 | 0.1891 | 0.0116 | $G, DG, G^2$ |
| 4 | 13352.47 | 13340.20 | 0.0344 | 0.0119 | $G, DG, D^2, G^2$ |
| 5 | 13358.12 | 13339.76 | 0.0223 | 0.0152 | $1, G, 1/G, DG, G^2$ |
| 6 | 13358.55 | 13338.10 | 0.0042 | 0.0154 | $1, G, 1/G, DG, D^2, G^2$ |
| 7 | 13359.27 | 13337.26 | 0.0018 | 0.0159 | $1, D, G, 1/G, D/G, DG, G^2$ |
| 8 | 13359.66 | 13335.63 | 0.0004 | 0.0161 | all but $1/G^2$ |
| 9 | 13359.79 | 13334.85 | 0.0002 | 0.0162 | all nine |

- **Selected model.** Two terms, with log Bayes factor 1.37 over the best three-term model. $D$ +0.00185 [+0.00146, +0.00224]; $1/G^2$ +0.00027 [+0.00019, +0.00035].
  - In GDP units, $D$ from 0 to 1 is $e^{12 \times 0.00185} - 1 = 2.24\%$ a year (interval 1.77% to 2.72%).
- **Democracy's inclusion.** The best model without any democracy term is $G$ alone, with log-evidence 13328.34, a log Bayes factor of 14.94 against the selected model.
- **Prior sensitivity.** $\lambda \times 0.1$ and $\times 10$ both select the same two terms.
- **Noise variance.** $\sigma$ from the residuals (0.00490) selects the same model.
- **Within-country residual correlation, lag 1:** +0.256 over 3,201 pairs.
  - This is the positive persistence that makes posterior intervals from an independent likelihood too narrow: a country growing faster than predicted one year tends to do so the next.
  - Country resampling keeps each country's years together, so its ranges absorb this persistence. That is why the resampling result is in `Results`.
- **Country resampling** (500 draws, seed 20261118).
  - The exact two-term set is selected in 54 of 500 draws; the most frequent set is $G, DG, G^2$, in 60. Some term containing $D$ is selected in 492.
  - Term frequencies: $1/G^2$ 183, $G^2$ 174, $G$ 171, $D$ 169, $DG$ 169, $D/G$ 152, $D^2$ 117, $1/G$ 100, $1$ 75.
  - Coefficient ranges against posterior widths: 1.04 times for $D$, 1.56 times for $1/G^2$.
  - Selection among the GDP terms is unstable, as warned: $G$, $1/G$, $G^2$ and $1/G^2$ are nearly interchangeable over the observed range. The presence of democracy is not unstable.
- **Errors between the two equations.** The correlation of the two selected models' residuals is +0.011. Iterated seemingly unrelated regressions converged in 3 iterations and changed no coefficient by more than 0.1%. This check changed nothing, so it is not in the report.
- **Comparison with Ranganathan, Spaiser and Sumpter (2013)** (replication only, not in the report).
  - **Not reproduced on the agreed criterion.** The paper's model has $D$, $G$ and $G^2$; ours has $D$ and $1/G^2$. The democracy term matches.
  - **The paper's model on our data.** Imposed on our data, it gives $D$ +0.00194 [+0.00130, +0.00257], $G$ +0.00393 [+0.00248, +0.00537] and $G^2$ −0.00430 [−0.00645, −0.00215]. The converted published values are $D$ +0.00205, inside its interval, and $G$ +0.0017 and $G^2$ −0.0024, both outside theirs.
  - **How it ranks.** Its log-evidence is 13341.48 against 13343.28 for the selected model, a log Bayes factor of only 1.80.
  - **So** the paper's GDP model is a close competitor on our data, and its democracy coefficient is reproduced almost exactly. The GDP terms differ, as expected given how interchangeable they are.
- **Re-derived independently** (`Code/outputs/06_fit_G_rederive.txt`): the evidence computed from the full 3,423 × 3,423 covariance matrix matches the script's value.

### Sub-question 3: the two equations together (step 4)

Computed by `Code/08_joint_dynamics.py`; drawn by `Code/09_fig_model_phase_portrait.py` from exported results only. Output in `Code/outputs/08_dynamics.txt`, `08_nullcline.csv`, `08_simulated_paths.csv`, `08_model_field.csv` and `09_model_portrait_counts.txt`.

- **Posterior.** Mean and covariance are recomputed from the 06 formulas, and an assertion checks them against the exported means.
- **Democracy zero-change curve.** Solved on a fine grid (sign change from + to −) and, for the selected term set, exactly from the quadratic $-0.1176D^2 + (0.2665 - 0.1437/G)D + 0.00303/G^2 = 0$. The two routes agree to $4.3 \times 10^{-7}$.
  - Values on the curve: 0.267 at \$500, 0.360 at \$1,000, 0.473 at \$2,000, 0.627 at \$5,000, 0.734 at \$10,000, 0.832 at \$20,000, 0.945 at \$50,000. It passes 1 at about \$84,000 ($G$ = 0.945). The data's GDP range is \$165 to \$132,253; the grid used to draw the curve runs from \$169 to \$130,590 inside it.
  - The slope of $f_D$ in $D$ on the curve is at most −0.068 over the grid, so the curve attracts everywhere.
- **GDP.** Over the observed range of $G$, with $D$ in [0, 1], the predicted $\Delta G$ runs from +0.00028 to +0.00335, which is 0.34% to 4.10% growth a year. It is never zero, so there is no fixed point of the system in range. The lowest growth is at $D = 0$ and the richest $G$; at $D = 0$ and the poorest $G$ it is 1.81%.
- **Bands.** The median width over the observed GDP range is 0.113 from 1,000 posterior draws and 0.106 from 500 country resamples (ratio 0.94). The resampled band is not wider, so the report uses the posterior band and does not mention the resampling.
- **Trajectories.** 183 countries, each stepped yearly from its first observed state to 2006.
  - Distance to the curve, $|D - D^*(G)|$: simulated median 0.225 at the start and 0.082 at the end, closer at the end for 168 of 183. Observed median 0.225 at the first year and 0.151 at the last, closer for 104 of 183.
  - 6 simulated country-years leave [0, 1]. They are left as computed, not clipped.
  - Simulated 2006 GDP runs from \$302 to \$170,562.
- **The six countries,** simulated 2006 against observed 2006:

| Country | Simulated | Observed |
| --- | --- | --- |
| Italy | $D$ 0.89 at \$39,898 | $D$ 0.81 at \$33,873 |
| Sweden | 0.94 at \$54,315 | 0.90 at \$48,078 |
| India | 0.30 at \$670 | 0.25 at \$1,008 |
| Chile | 0.42 at \$6,495 | 0.87 at \$10,612 |
| Albania | 0.25 at \$2,462 | 0.51 at \$2,894 |
| Nigeria | 0.52 at \$2,990 | 0.19 at \$1,949 |

- **Figure 4.**
  - Arrows are model changes at the 83 cell positions of Figure 3, in the locked format; 14 are capped (`09_model_portrait_counts.txt`).
  - The arrow-drawing code moved into `sds_common.draw_capped_arrows` so Figures 3 and 4 share one implementation. Figure 3 was redrawn with it and is unchanged (33 of 83 capped).
  - The first render drew the curve over the whole observed GDP range, so it rose past the index's maximum of 1. It is now drawn only where it is between 0 and 1. Superseded: the curve drawn over the full GDP range.
  - At the user's request ("too messy"), the observed paths were removed from Figure 4, so only the simulated paths remain. The curve was named "Democracy nullcline" in the legend and text, and drawn in light grey with a lighter band. Superseded: faint observed paths, the darker curve, and the legend entries "Simulated path" and "Observed path".
- **Comparison with Ranganathan, Spaiser and Sumpter (2013)** (replication only, not in the report).
  - The paper reports a stable curve from low democracy and low GDP to high democracy and high GDP, onto which countries converge. Countries high in democracy and low in GDP lose democracy until they reach it.
  - **Reproduced on the agreed criterion.** The fitted curve rises from low–low to high–high, attracts everywhere in range, and lies below countries that are high in democracy and low in GDP, so their democracy falls towards it. The simulated paths converge on it: 168 of 183 end closer.
  - **One difference.** In our fit GDP grows everywhere in range, so movement along the curve never stops. The paper's $\Delta G$ has a $-G^2$ term that limits growth at high GDP.

### Prior check: uniform against normal (step 4, at the user's request)

Run by `Code/10_uniform_prior_check.py`; output in `Code/outputs/10_uniform_prior_check.txt`. The best model of each size does not depend on the prior, so only the comparison across sizes changes. The evidence uses a uniform prior $U(-a, a)$ on each RMS-scaled coefficient, as in Ranganathan, Spaiser and Sumpter (2013), with $\sigma$ fixed as before. The integral is closed-form, with the share of the likelihood inside the box estimated by Monte Carlo (200,000 draws, seed 20261118). Neither paper states the range, so three widths were tried: $a = \sqrt3\,\lambda$, which gives the same variance as the agreed normal prior, then 10 and 100 times that.

| Equation | Normal (agreed) | Uniform, $a = \sqrt3\lambda$ | Uniform, ×10 | Uniform, ×100 |
| --- | --- | --- | --- | --- |
| $\Delta D$ | 4 terms ($D, D/G, D^2, 1/G^2$), P 0.68 | same 4, P 0.46 (3 terms 0.42) | same 4, P 0.69 | **3 terms ($D/G, DG, D^2$), P 0.81** (4 terms 0.19) |
| $\Delta G$ | 2 terms ($D, 1/G^2$), P 0.75 | same 2, P 0.74 | same 2, P 0.97 | same 2, P 0.996 |

- **GDP equation.** Insensitive to the prior: the same two terms win under every prior, more firmly the wider the box.
- **Democracy equation.** It depends on the width.
  - At the variance-matched width, only 5% of the four-term model's likelihood lies inside the box. Its coefficient on $D$, about 0.14 on the scaled axis, is beyond the box's edge of 0.125. So the three-term model comes close (0.42 against 0.46).
  - At 100 times the width, the $-m\log 2a$ penalty for each extra term dominates, and the three-term model $D/G, DG, D^2$ is selected. It was the runner-up under the agreed normal prior (P 0.19).
  - $D/G$ and $D^2$ are in the selected model under every prior.
- **What the alternative would change.** The three-term model has no $1/G^2$ term, so $\Delta D = 0$ whenever $D = 0$. A country at zero democracy would stay there, which the selected four-term model does not imply. The nullcline and simulated paths under the three-term model were not computed. The user chose the normal prior throughout (log row 27), so this check stays in the appendix and is not mentioned in the report.

### Question 2: V-Dem and prediction (steps 3–4)

- **V-Dem fits, 1981–2006** (`06_fit_D_vdem.txt`, `06_fit_G_vdem.txt`). $\sigma = \lambda$ = sd of changes: 0.04448 for democracy, 0.00585 for GDP.
  - **Democracy equation.** Selected terms $1, DG, D^2$, P(size) = 0.72 (next: size 4, $D, 1/G, D/G, D^2$, 0.14). Coefficients: +0.00748 [+0.00421, +0.01075]; +0.06256 [+0.02994, +0.09519]; −0.07078 [−0.09924, −0.04233].
    - Prior ×0.1 selects 6 terms; ×10 the same three. $\sigma$ from the residuals gives the same three.
    - Lag-1 residual correlation +0.213. In resamples, $D^2$ is selected 466 times of 500, $DG$ 332, and the exact set 178.
  - **GDP equation.** Selected terms $D^2, 1/G^2$, P = 0.67 (next: size 1, $D/G$, 0.26). Coefficients: +0.00226 [+0.00173, +0.00279]; +0.00025 [+0.00016, +0.00033].
    - Prior ×0.1 selects the same two; ×10 selects $D/G$ alone, which is still a democracy term. $\sigma$ from the residuals gives the same two.
    - Lag-1 residual correlation +0.314. Some democracy term is selected in 492 of 500 resamples.
  - **Joint checks** (`07_joint_checks_vdem.txt`). Democracy in the GDP equation: the best model without it is $G$ alone, log Bayes factor 12.96. The residual correlation between the equations is +0.006, and SUR changes nothing.
  - **Dynamics** (`08_dynamics_vdem.txt`).
    - The nullcline attracts (largest slope −0.0529), and the grid and exact roots agree to $3.3 \times 10^{-7}$. Values on it: 0.626 at \$500, 0.667 at \$1k, 0.709 at \$2k, 0.765 at \$5k, 0.809 at \$10k, 0.853 at \$20k, 0.913 at \$50k. It stays at or below 1 over the observed range (\$165–\$113,153).
    - GDP growth in range is 0.31% to 4.44%. The band is 0.096 from the posterior and 0.066 from resampling.
    - Convergence to 2006: simulated 158 of 171 closer (median 0.475 → 0.220); observed 119 of 171 (0.475 → 0.171).
  - **Growth from the $D^2$ term.** From democracy 0.013 to 0.9, $e^{12 \times 0.00226 \times (0.81 - 0.00017)} - 1 = 2.22\%$ (1.70% to 2.75%).
  - **Against the Welzel results.** The terms differ: democracy $1, DG, D^2$ against $D, D/G, D^2, 1/G^2$, and GDP $D^2$ against $D$. The features named in the answer criteria hold: democracy enters the GDP equation, and the nullcline rises and attracts. The V-Dem nullcline is flatter and higher at low income, 0.63 against 0.27 at \$500.
- **Prediction, 2007–2024** (`Code/13_predict.py`, output `13_predict.txt`).
  - **Year by year,** 3,088 changes from 174 countries. Mean log predictive density per change:

| | Model | Average change | Refit on 2007–2024 |
| --- | --- | --- | --- |
| Democracy | 1.8391 | 1.8402 | 1.9020 |
| GDP | 3.9050 | 3.9087 | 3.9570 |

- Model minus baseline, in total: −3.3 and −11.3. Refit minus model: +194.2 and +160.4.
- The model beats the baseline on 42.9% and 44.4% of changes.
- Variance explained out of sample: −7.1% and −1.2%, against 1.6% and 0.9% in sample for 1981–2006.
- Refitted coefficients: democracy −0.00161, +0.02429, −0.02809; GDP +0.00069, +0.00050.
  - **Whole period,** 168 countries stepped 18 years from 2006.
    - Democracy: median error 0.146 against 0.171 for the baseline; the model is closer for 106.
    - GDP: median error 27.0% against 22.0%; the model is closer for 74.
    - Observed distance to the 1981–2006 nullcline rose from 0.171 to 0.257, with 48 of 168 closer; simulated distance by 2024 is 0.076.
    - Six countries: India 0.72 → observed 0.40, simulated 0.69. Italy's GDP is simulated at \$52.6k against \$34.5k observed.
  - **Re-derived independently** (`13_predict_rederive.txt`). Monte Carlo over 4,000 posterior draws gives 1.8390 and 3.9050, against 1.8391 and 3.9050 in closed form.
- **Figure 5** (`Code/14_fig_prediction.py`). The six countries from their 2006 states, observed solid and predicted dashed (the dash marks a prediction), with the 1981–2006 V-Dem nullcline and band. The first legend narrowed the axes and the \$50k and \$100k ticks touched, so the labels were shortened. Superseded: the long legend labels.
- **Pipeline changes for question 2.**
  - `06`, `07` and `08` take a measure option (`vdem`); with no option they reproduce the main analysis exactly (`.json` and joint checks unchanged).
  - `06` now writes term frequencies itself, and `08` the point where the nullcline passes 1 and the observed range. Both had earlier been added to the outputs by hand, and a re-run had dropped them.
  - The "observed range" in the main analysis is now the data's (\$165–\$132,253), not the calculation grid's (\$169–\$130,590).

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
| 8 | Step 2. Framed the question from the introduction of Ranganathan, Spaiser and Sumpter (2013), as the user asked. Recorded the question, the paper's equations converted to $G = \ln(\text{GDP})/12$, three sub-questions with what counts as reproducing the paper, and the standard analysis proposal with its departures. Wrote the framing and sub-questions into the report's `Introduction`. Nothing was computed from the data. | `Appendix.md` `Research Question`; `Report.md` `Introduction` |
| 9 | Step 2. At the user's request, rewrote the `Introduction` to stand alone as an investigation of the problem. It now opens by saying the work is a replication of Ranganathan, Spaiser and Sumpter (2013). The paragraph about replicating and the "is it the dependence they selected" clauses were removed from the sub-questions. The criteria for reproducing the paper stay here in `Research Question`. | `Report.md` `Introduction` |
| 10 | Step 2. A new contract rule says the report never mentions replication, because the finished report is to serve as a template. The opening sentence about replication was removed. The paper is now cited once, as the source of the method ("Following Ranganathan, Spaiser and Sumpter (2013)…"). The comparison with the paper's equations goes in `Analysis` in this appendix once results exist, not in the report's `Discussion`. Superseded: the plan in row 9's follow-up to put that comparison in `Discussion`. | `Report.md` `Introduction`; `instructions.md` |
| 11 | Step 2 closed by the user on 2026-11-18 ("Looks good"). Agreed with it: the reproduction criteria in `Research Question` (same terms and same signs decide; coefficients compared via 95% intervals, for information only), and two additions to the paper's method (resampling countries, and the data phase portrait). The log-base assumption behind the converted coefficients stands as recorded in `Research Question`. | — |
| 12 | Step 3 started. The user questioned the mean-over-time figure, which answers none of the sub-questions. A contract change replaced the first two standard figures (a one-year scatter and the mean over time) with trajectories of six representative countries plus the mean, over time and in the $(G, D)$ plane. Higher-dimensional analyses may have more figures. Counted from the data for this choice: 84 countries have both variables in all 26 years; of the paper's six, Albania has 21 years and the others all 26. | `instructions.md` `Report Format`; `Research Question` proposal |
| 13 | Step 3. Built the analysis panel: 3,679 country-years, 3,423 changes. Drew Figures 1 (trajectories over time) and 2 (trajectories in the $(G, D)$ plane) and added them to `Results` with captions and a paragraph saying how to read them. They sit above the sub-question sub-headings, because they describe the data for all three sub-questions. |
| 14 | Step 3. A contract rule says every variable is shown in interpretable units, so we see GDP in money. Figures 1 and 2 were redrawn with GDP in constant 2015 US dollars on a log axis. The captions and the `Results` paragraph were updated, and the `Introduction` now gives GDP's range in dollars (about \$160 to \$140,000 per person, from `panel.csv`: 164.7 to 140,615). | `instructions.md`; `Code/sds_common.py`; Figures 1–2; `Report.md` | `Code/02_build_panel.py`, `Code/03_fig_trajectories_time.py`, `Code/04_fig_trajectories_plane.py`; `Report.md` `Results` |
| 15 | Step 3. At the user's request, dropped the mean from Figures 1 and 2: "We don't need it". A contract change locks the figure format: no mean, the user's style in the workspace themes, dollar log axes, axis labels with units, the legend off the data. Figures 1 and 2 and their scripts are the reference. It also adds "always use units when available". Figures redrawn; the `Results` paragraph and captions updated. | `instructions.md`; Figures 1–2; `Report.md` |
| 16 | Step 3. Made Figure 3, the data phase portrait: cell-average yearly changes on a 14 × 10 grid, arrows scaled to 2 years, cells with at least 10 changes (83 cells, 3,289 of 3,423 changes). It was redrawn once after inspection (first draft: 5 years, at least 5 changes). Figures 2 and 3 now share a fixed GDP range. Added to `Results` with a reading paragraph and caption. | `Code/05_fig_data_phase_portrait.py`; `Report.md` `Results` |
| 17 | Step 3. At the user's request, made the arrows in Figure 3 longer, with a cap: 5 years, capped at 0.7 cm on the page with direction kept; 33 of 83 capped. Caption and reading paragraph updated. | `Code/05_fig_data_phase_portrait.py`; `Report.md` |
| 18 | Step 3. Arrows set to two thirds of that length (3⅓ years, capped at 0.47 cm; 33 of 83 capped), and the arrow format locked in the contract for both phase portraits. | `instructions.md`; `Code/05_fig_data_phase_portrait.py`; `Report.md` |
| 19 | Step 3 closed by the user on 2026-11-18. Figures 1–3 are in the report in the locked format. Offered and declined: a grid-sensitivity check of Figure 3, and data ranges in the captions. Figure 4, the model phase portrait, is deferred to step 4. | — |
| 20 | Step 4, sub-question 1. Agreed: $\sigma$ fixed at sd($\Delta D$) and a normal prior with $\lambda$ = sd($\Delta D$) on RMS-scaled terms. Selected four terms: $D$, $D/G$, $D^2$, $1/G^2$, P(size) = 0.68. Checks run: prior ×0.1 and ×10, $\sigma$ from residuals, lag-1 residual correlation, 500 country resamples. Comparison with the paper in the appendix only. Wrote `Methods` (`Data`, `Model`, `Model selection and uncertainty`) and the sub-question 1 paragraph in `Results`. | `Code/06_fit_change_model.py`; `Code/outputs/06_fit_D.*`; `Report.md` |
| 21 | Step 4, sub-question 2. Same method on $\Delta G$. Selected two terms: $D$, $1/G^2$, P(size) = 0.75. Democracy is included with a log Bayes factor of 14.9 over the best model without it. Lag-1 residual correlation +0.26, absorbed by the country resampling, which is reported. Cross-equation correlation +0.011; SUR changes nothing (appendix only). Comparison with the paper in the appendix only. Added the sub-question 2 paragraph to `Results`, and to `Methods` one sentence converting changes in $G$ to GDP growth. | `Code/06_fit_change_model.py`; `Code/07_joint_checks.py`; `Report.md` |
| 22 | Step 4, sub-question 3. Agreed: zero-change curves from posterior means; a 95% band from 1,000 posterior draws, with the resampled band in the appendix; yearly stepping from first observed states; a distance-to-curve convergence measure. Democracy's zero-change curve rises with GDP and attracts everywhere; GDP grows everywhere in range; 168 of 183 simulated and 104 of 183 observed countries end closer to the curve. Figure 4 made in the locked format, with the zero-change curve, its band and the simulated paths added; the curve is clipped to the range of the index after the first render. Added a `Methods` sub-heading and a `Results` paragraph with a reading paragraph. | `Code/08_joint_dynamics.py`, `Code/09_fig_model_phase_portrait.py`; `Report.md` |
| 23 | Step 4. Figure 4 simplified at the user's request: observed paths removed, the curve named "democracy nullcline" and drawn lighter. The text and caption were updated, and now point to Figure 2 for the observed paths. | `Code/09_fig_model_phase_portrait.py`; `Report.md` |
| 24 | Step 4. At the user's request, the three `Results` sub-sections were combined into one, "The fitted model and its dynamics", and simplified to fitting the model and looking at the dynamics. Removed from the report: the share of variance explained, the term sets of the next most probable sizes, and per-term resampling counts. All stay in this appendix under the sub-question headings. The `Methods` sub-heading "Sub-question 3" was renamed "Dynamics". The `Introduction` still lists three sub-questions. | `Report.md` |
| 25 | Step 4. At the user's request, the `Introduction` now asks one question in place of three sub-questions. The contract now allows one to four questions, with one as the default, and locks the model phase portrait: model only, light grey "<Variable> nullcline" with its band, simulated paths, no data. The background grid was removed from all figures, and Figures 1–4 were redrawn and checked (sizes unchanged; 33 and 14 arrows capped, as before). | `instructions.md`; `Code/sds_common.py`; Figures 1–4; `Report.md` |
| 26 | Step 4. At the user's request, a check of a uniform prior against the agreed normal prior, at three widths. The GDP equation is unchanged under all of them. The democracy equation is unchanged at the variance-matched and 10× widths, but at 100× it switches to the runner-up three-term model ($D/G$, $DG$, $D^2$), which has no $1/G^2$ term. The answer can change, so this goes to the user to decide how to report. | `Code/10_uniform_prior_check.py`; `Code/outputs/10_uniform_prior_check.txt` |
| 27 | Step 4. The user chose to keep the normal prior. A contract change fixes it for every analysis: RMS-scaled terms, $\lambda = \sigma = \text{sd}(\Delta x)$, closed-form evidence, and $\lambda$ ×0.1 and ×10 recorded in the appendix. The uniform-prior check stays in the appendix only; the report is unchanged. | `instructions.md` |
| 28 | Contract tidied at the user's request to dynamical systems on social data, from about 15,600 to 4,500 words (commit `b045975`). Checked against this analysis: it already follows the tidied rules (`Methods` with `Data`, `Model`, `Model selection and uncertainty`, `Dynamics`; one `Results` section; locked figures), so no report change was needed. | `instructions.md`, `CLAUDE.md` |
| 29 | Step 4. Added to `Methods`, at the user's request after the comparison with the sample: why changes are pooled, in `Model`; and why resampling is by country, in `Model selection and uncertainty`. The latter states the within-country residual correlations, +0.26 for GDP and −0.14 for democracy, taken from `06_fit_G.txt` and `06_fit_D.txt`. `Dynamics` now uses "democracy nullcline", as `Results` does. | `Report.md` |
| 30 | Step 4 closed by the user on 2026-11-18. The report's length (about 1,650 words before the discussion, limitations, background and abstract) is left for steps 5 and 6. | — |
| 31 | Step 5. Proposed a three-paragraph `Discussion` (democracy settling towards an income-set level; democracy and growth; the joint dynamics) and four limitations. The user dropped the first theme and asked for the discussion to cover only the relationships in growth. Wrote a two-paragraph `Discussion` on democracy, income and GDP growth, with its qualifications, and `Limitations` as one paragraph with the four proposed items and no count. Numbers are from `06_fit_G.txt` (R² 0.0112; a democracy term in 492 of 500 resamples) and `08_dynamics.txt` (growth 0.34% to 4.10%; 1.81% at democracy 0 and the poorest income). | `Report.md` |
| 32 | Step 5 closed by the user on 2026-11-18. Offered and declined: a closing "taken together" sentence, and a mention of the democracy equation in the `Discussion`. The report is about 1,930 words before the background and abstract. | — |
| 33 | Step 6, background. Structure agreed with the user: four claims in two paragraphs. Sources checked: bibliographic details from Crossref metadata for every DOI, and the claims from abstracts (Crossref, OpenAlex, and EconPapers for Barro 1996, whose publisher page blocks scripts). Read from abstracts only: Acemoglu et al. (2008), Acemoglu et al. (2019), Barro (1991, 1996, 1999). Read in full: Spaiser et al. (2014) and Ranganathan et al. (2013). Every claim cited is stated in the abstract. Lipset (1959) was dropped: the claim needs the body of the paper, which was not obtained; the correlation is cited to Acemoglu et al. (2008) instead. Barro (1999) is cited only for income predicting democracy, not for democracy adjusting towards a target set by income. Democracy and growth is framed as contested. Publisher DOIs return 403 to scripts (bot-blocking) and resolve in the metadata. | `Report.md` `Introduction`, `References` |
| 34 | Step 6. At the user's request: the `Introduction`'s framing paragraph was shortened and stripped of numbers (GDP range, model scale); the method sentence that repeated the background was trimmed; the index's components moved to `Methods`. `Methods` › `Data` was shortened and stripped of coding details (the indicator code, the −99 rule, the range of $G$, the worked conversion example). The code stays in the reference list, which identifies the series. | `Report.md` |
| 35 | Step 6. At the user's request, the World Bank indicator code is back in `Methods` › `Data`, in parentheses: "(2026; indicator NY.GDP.PCAP.KD)". Superseded: dropping it in row 34. The −99 rule and the other coding details stay out. This resolves the question about the contract: `Report format` already asks for indicator codes in `Data`, so it is unchanged. | `Report.md` |
| 36 | Step 6. Wrote the `Abstract`: one paragraph of 180 words, in the contract's order, with results in words. Each claim was checked against the body. "Variation in either variable" was narrowed to "in growth", because the report states the share explained only for growth (democracy's 3.7% is in the appendix only). Cites Barro (1996) and Acemoglu et al. (2008, 2019) for the dispute. The report totals about 2,190 words from `Abstract` to `Limitations`. | `Report.md` |
| 37 | Step 6. Title chosen by the user from three options: "How democracy and national income change together". Not chosen: "Democracy and income as a dynamical system, 1981–2006" and "Democracy moves with income, and goes with faster growth". | `Report.md` |
| 38 | The user kept 1981–2006 for the main analysis, then added question 2: a second democracy measure, and whether the 1981–2006 model predicts 2007–2024. Four choices were agreed before any data was seen (`Research Question`, question 2). The user asked for steps 1–6 for it in one pass ("Do it all"), departing from one step per request. | — |
| 39 | Question 2, step 1. Downloaded V-Dem version 15 (gitignored, `SOURCE.md` updated) and described it: no zeros or codes; 4,126 (1981–2006) and 3,091 (2007–2024) country-years overlap with GDP. | `Code/11_describe_vdem.py` |
| 40 | Question 2, step 3. Built the V-Dem panel: 3,955 fit changes and 3,088 test changes. | `Code/12_build_panel_vdem.py` |
| 41 | Question 2, step 4. V-Dem fits for 1981–2006, joint checks and dynamics, through a measure option added to `06`–`08`; main outputs re-run unchanged. Prediction test and independent re-derivation. Figure 5. | `Code/06`–`08`, `13_predict.py`, `14_fig_prediction.py` |
| 42 | Question 2, steps 2, 5 and 6, written into the report. The `Introduction` gains a measurement sentence (Munck & Verkuilen, 2002, checked from its abstract), a sentence on testing by prediction, V-Dem in the framing, and two numbered questions. `Methods` gains V-Dem in `Data`, the same-library choice in `Model`, V-Dem correlations, and a `Prediction` sub-heading. `Results` gains question 2 and Figure 5. The `Discussion` gains a paragraph, `Limitations` is updated, the `Abstract` is rewritten (198 words), and references are added (Coppedge et al., 2025; Munck & Verkuilen, 2002). The report is now about 3,150 words against a target of about 2,000. | `Report.md` |
| 43 | At the user's request, the report was cut by about 60%, from about 3,150 to about 1,300 words (`Abstract` to `Limitations`). `Results` now describes in words what each model says; the credible intervals, posterior probabilities, resampling counts, nullcline values in dollars, convergence counts and prediction scores were taken out of the report and remain in this appendix under `Analysis`. The equations, figures and captions are unchanged. Three sentences were corrected on checking: the baseline is the overall average change, not each country's own; the resampling sentence now names all the stable terms; and "chooses clearly" became "favours", to avoid grading the evidence. The previous version is in git (`e3e14db`). | `Report.md` |

## Code Summary

| File | What it does | Reads | Writes |
| --- | --- | --- | --- |
| `Code/01_describe_data.py` | Describes the two source files: shape, coverage per year, ranges, the −99 code, zeros, duplicate codes, and the overlap. It changes no data and draws no conclusions. Run with `cd Code && uv run python 01_describe_data.py`. | `Attachments/worldbank/API_NY.GDP.PCAP.KD_DS2_en_csv_v2_71952.csv` and its country metadata; `Attachments/qog_std_ts_jan15.csv` (columns `ccode`, `cname`, `year`, `ccodealp`, `wel_citrig`) | `Code/outputs/01_describe_data.txt` |
| `Code/sds_common.py` | Shared constants and style: years, the GDP scale (12), the six representative countries and their fixed colours, figure sizing and saving, the dollar log axis, and the locked phase-portrait arrows (`ARROW_K`, `ARROW_CAP_CM`, `draw_capped_arrows`). Imported by the scripts below. | — | — |
| `Code/02_build_panel.py` | Applies the step 1 decisions and builds the panel: countries only, −99 set to missing, join on ISO3, $G = \ln(\text{GDP})/12$, 1981–2006, consecutive-year changes, and the balanced-country flag. Fits nothing. Run with `cd Code && uv run python 02_build_panel.py`. | Both source files, as above | `Code/outputs/panel.csv` (gitignored: row-level QoG data); `Code/outputs/02_panel_counts.txt` |
| `Code/03_fig_trajectories_time.py` | Figure 1: democracy and GDP per capita (dollars, log axis) against year for the six countries. Light and dark. | `Code/outputs/panel.csv` | `Code/outputs/figures/fig1_trajectories_time.png`, `…/dark/…` |
| `Code/04_fig_trajectories_plane.py` | Figure 2: the six countries' paths in the GDP–democracy plane (dollars, log axis), over all countries in 2006. Light and dark. | `Code/outputs/panel.csv` | `Code/outputs/figures/fig2_trajectories_plane.png`, `…/dark/…` |
| `Code/05_fig_data_phase_portrait.py` | Figure 3: cell-average observed yearly changes as arrows on the GDP–democracy plane, with the six countries' paths faint. Parameters: `LENGTH = 2/3`, giving `K = 5 × 2/3 = 3⅓` (arrow years) and `CAP_CM = 0.7 × 2/3 ≈ 0.467` (maximum arrow length on the page, direction kept), `MIN_N = 10` (minimum changes per cell), $G$ bins of 0.04 from 0.42 to 1.00, $D$ bins of 0.1. | `Code/outputs/panel.csv` | `Code/outputs/figures/fig3_data_phase_portrait.png`, `…/dark/…`; `Code/outputs/05_phase_cells.csv`; `Code/outputs/05_phase_portrait_counts.txt` |
| `Code/06_fit_change_model.py` | Fits the change model for one outcome (`D` or `G`, given as the argument). Runs all 512 term subsets, finds the best of each size by least squares, computes closed-form evidence and the Gaussian posterior with $\sigma$ = sd($\Delta x$) and $\lambda$ = sd($\Delta x$) on RMS-scaled terms, then runs the checks: $\lambda$ ×0.1 and ×10, $\sigma$ from residuals, lag-1 residual correlation, and 500 country resamples. Seed 20261118. Run with `cd Code && uv run python 06_fit_change_model.py D`. | `Code/outputs/panel.csv` | `Code/outputs/06_fit_<outcome>.txt`, `.json` |
| `Code/07_joint_checks.py` | The checks that need both equations: how firmly democracy enters $\Delta G$ (best model without a democracy term, by evidence); the residual correlation between the two selected models and the iterated SUR re-estimate; the 2013 paper's $\Delta G$ model on our data (replication only). Run after both `06_…` fits. | `Code/outputs/panel.csv`, `06_fit_D.json`, `06_fit_G.json` | `Code/outputs/07_joint_checks.txt` |
| `Code/08_joint_dynamics.py` | Sub-question 3 computations. Democracy's zero-change curve: grid root plus an exact quadratic check, and its stability. Whether $\Delta G$ is zero anywhere in range. A 95% band from 1,000 posterior draws and from 500 country resamples. Yearly simulation from each country's first state to 2006. Distance to the curve at the start and end, simulated and observed. The model field at the Figure 3 cells. Seed 20261118. | `Code/outputs/panel.csv`, `06_fit_D.json`, `06_fit_G.json`, `05_phase_cells.csv` | `Code/outputs/08_dynamics.txt`, `08_nullcline.csv`, `08_simulated_paths.csv`, `08_model_field.csv` |
| `Code/09_fig_model_phase_portrait.py` | Figure 4 from the `08_…` exports only, in the locked format: model arrows, the zero-change curve with its band (only where it is between 0 and 1), simulated paths solid, observed paths faint. Light and dark. | `08_model_field.csv`, `08_nullcline.csv`, `08_simulated_paths.csv`, `panel.csv` | `Code/outputs/figures/fig4_model_phase_portrait.png`, `…/dark/…`; `09_model_portrait_counts.txt` |
| `Code/10_uniform_prior_check.py` | Sensitivity of the comparison across sizes to a uniform prior $U(-a,a)$ on RMS-scaled coefficients, at $a = \sqrt3\lambda$, ×10 and ×100. Closed-form integral with a Monte Carlo share in the box (200,000 draws, seed 20261118). | `Code/outputs/panel.csv`, `06_fit_D.json`, `06_fit_G.json` | `Code/outputs/10_uniform_prior_check.txt` |
| `Code/11_describe_vdem.py` | Describes the V-Dem `v2x_polyarchy` index: coverage, range, codes and overlap with GDP. | `Attachments/vdem/V-Dem-CY-Core-v15.csv`, World Bank files | `Code/outputs/11_describe_vdem.txt` |
| `Code/12_build_panel_vdem.py` | The V-Dem panel for 1981–2024, built with the main panel's rules; `period` marks fit (changes ending by 2006) and test (2007–2024). | as above | `Code/outputs/panel_vdem.csv` (gitignored), `12_panel_vdem_counts.txt` |
| `Code/13_predict.py` | The prediction test: year-by-year predictive density against the average-change model and a refit on 2007–2024; 18-year projections from 2006 against observed 2024; distance to the nullcline. | `panel_vdem.csv`, `06_fit_*_vdem.json` | `13_predict.txt`, `13_predicted_paths.csv`, `13_predicted_2024.csv` |
| `Code/14_fig_prediction.py` | Figure 5: the six countries' observed and predicted paths for 2006–2024, with the 1981–2006 V-Dem nullcline. | `13_predicted_paths.csv`, `08_nullcline_vdem.csv` | `figures/fig5_prediction.png`, `…/dark/…` |

The scripts `06_fit_change_model.py`, `07_joint_checks.py` and `08_joint_dynamics.py` take an optional `vdem` argument (`06` takes it after the outcome), which writes `…_vdem` outputs. Run order for question 2: `11`, `12`, `06 D vdem`, `06 G vdem`, `07 vdem`, `08 vdem`, `13`, `14`.

Run order: `01_describe_data.py` (description only), then `02_build_panel.py`, then the figure scripts in any order. The scripts in `Code/` import `sds_common.py` from their own directory, so they are run without Python's isolated mode (`-I`). No downloaded file is on the import path.

## References

Coppedge, M., Gerring, J., Knutsen, C. H., Lindberg, S. I., Teorell, J., Altman, D., et al. (2025). [V-Dem Country-Year Dataset v15](https://doi.org/10.23696/vdemds25). Varieties of Democracy (V-Dem) Project. Downloaded 18 November 2026.

Ranganathan, S., Spaiser, V., Mann, R. P. and Sumpter, D. J. T. (2014). [Bayesian dynamical systems modelling in the social sciences](https://doi.org/10.1371/journal.pone.0086468). *PLOS ONE*, 9(1), e86468.

Ranganathan, S., Spaiser, V. and Sumpter, D. J. T. (2013). [A Bayesian approach to modeling dynamical systems in the social sciences](https://doi.org/10.5220/0004480901250131). In *Proceedings of the 3rd International Conference on Simulation and Modeling Methodologies, Technologies and Applications (SIMULTECH 2013)*, pp. 125–131. SCITEPRESS.

Ranganathan, S., Nicolis, S. C., Spaiser, V. and Sumpter, D. J. T. (2015b). [Understanding democracy and development traps using a data-driven approach](https://doi.org/10.1089/big.2014.0066). *Big Data*, 3(1), 22–33.

Spaiser, V., Ranganathan, S., Mann, R. P. and Sumpter, D. J. T. (2014). [The dynamics of democracy, development and cultural values](https://doi.org/10.1371/journal.pone.0097856). *PLOS ONE*, 9(6), e97856. Supporting information: [File S1](https://journals.plos.org/plosone/article/file?type=supplementary&id=10.1371/journal.pone.0097856.s001).

Teorell, J., Dahlberg, S., Holmberg, S., Rothstein, B., Hartmann, F. and Svensson, R. (2015). [The Quality of Government Standard Dataset, version Jan15](https://www.qogdata.pol.gu.se/dataarchive/qog_std_ts_jan15.csv). University of Gothenburg: The Quality of Government Institute. [Codebook](https://www.qogdata.pol.gu.se/dataarchive/qog_std_jan15.pdf).

Welzel, C. (2013). *Freedom Rising: Human Empowerment and the Quest for Emancipation*. Cambridge University Press. [Open-access PDF](https://cambridge.org/de/files/8613/8054/8416/FreedomRising_OA.pdf).

World Bank (2026). [GDP per capita (constant 2015 US$), NY.GDP.PCAP.KD](https://api.worldbank.org/v2/en/indicator/NY.GDP.PCAP.KD?downloadformat=csv). World Development Indicators, release last updated 11 November 2026; downloaded 18 November 2026.
