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

## Code Summary

| File | What it does | Reads | Writes |
| --- | --- | --- | --- |
| `Code/01_describe_data.py` | Describes the two source files: shape, coverage per year, ranges, the −99 code, zeros, duplicate codes, and the overlap. It changes no data and draws no conclusions. Run with `cd Code && uv run python 01_describe_data.py`. | `Attachments/worldbank/API_NY.GDP.PCAP.KD_DS2_en_csv_v2_71952.csv` and its country metadata; `Attachments/qog_std_ts_jan15.csv` (columns `ccode`, `cname`, `year`, `ccodealp`, `wel_citrig`) | `Code/outputs/01_describe_data.txt` |
| `Code/sds_common.py` | Shared constants and style: years, the GDP scale (12), the six representative countries and their fixed colours, figure sizing and saving. Imported by the scripts below. | — | — |
| `Code/02_build_panel.py` | Applies the step 1 decisions and builds the panel: countries only, −99 set to missing, join on ISO3, $G = \ln(\text{GDP})/12$, 1981–2006, consecutive-year changes, and the balanced-country flag. Fits nothing. Run with `cd Code && uv run python 02_build_panel.py`. | Both source files, as above | `Code/outputs/panel.csv` (gitignored: row-level QoG data); `Code/outputs/02_panel_counts.txt` |
| `Code/03_fig_trajectories_time.py` | Figure 1: democracy and GDP per capita (dollars, log axis) against year for the six countries. Light and dark. | `Code/outputs/panel.csv` | `Code/outputs/figures/fig1_trajectories_time.png`, `…/dark/…` |
| `Code/04_fig_trajectories_plane.py` | Figure 2: the six countries' paths in the GDP–democracy plane (dollars, log axis), over all countries in 2006. Light and dark. | `Code/outputs/panel.csv` | `Code/outputs/figures/fig2_trajectories_plane.png`, `…/dark/…` |

Run order: `01_describe_data.py` (description only), then `02_build_panel.py`, then the figure scripts in any order. The scripts in `Code/` import `sds_common.py` from their own directory, so they are run without Python's isolated mode (`-I`). No downloaded file is on the import path.

## References

Ranganathan, S., Spaiser, V., Mann, R. P. and Sumpter, D. J. T. (2014). [Bayesian dynamical systems modelling in the social sciences](https://doi.org/10.1371/journal.pone.0086468). *PLOS ONE*, 9(1), e86468.

Ranganathan, S., Spaiser, V. and Sumpter, D. J. T. (2013). [A Bayesian approach to modeling dynamical systems in the social sciences](https://doi.org/10.5220/0004480901250131). In *Proceedings of the 3rd International Conference on Simulation and Modeling Methodologies, Technologies and Applications (SIMULTECH 2013)*, pp. 125–131. SCITEPRESS.

Ranganathan, S., Nicolis, S. C., Spaiser, V. and Sumpter, D. J. T. (2015b). [Understanding democracy and development traps using a data-driven approach](https://doi.org/10.1089/big.2014.0066). *Big Data*, 3(1), 22–33.

Spaiser, V., Ranganathan, S., Mann, R. P. and Sumpter, D. J. T. (2014). [The dynamics of democracy, development and cultural values](https://doi.org/10.1371/journal.pone.0097856). *PLOS ONE*, 9(6), e97856. Supporting information: [File S1](https://journals.plos.org/plosone/article/file?type=supplementary&id=10.1371/journal.pone.0097856.s001).

Teorell, J., Dahlberg, S., Holmberg, S., Rothstein, B., Hartmann, F. and Svensson, R. (2015). [The Quality of Government Standard Dataset, version Jan15](https://www.qogdata.pol.gu.se/dataarchive/qog_std_ts_jan15.csv). University of Gothenburg: The Quality of Government Institute. [Codebook](https://www.qogdata.pol.gu.se/dataarchive/qog_std_jan15.pdf).

Welzel, C. (2013). *Freedom Rising: Human Empowerment and the Quest for Emancipation*. Cambridge University Press. [Open-access PDF](https://cambridge.org/de/files/8613/8054/8416/FreedomRising_OA.pdf).

World Bank (2026). [GDP per capita (constant 2015 US$), NY.GDP.PCAP.KD](https://api.worldbank.org/v2/en/indicator/NY.GDP.PCAP.KD?downloadformat=csv). World Development Indicators, release last updated 11 November 2026; downloaded 18 November 2026.
