# Appendix

*Part of the [Data Analysis Workspace](../README.md) — conclusions in [Report.md](Happiness.md), environment in [Setup.md](../Setup.md).*

## Data Summary

Generated description: [Code/outputs/data_summary.md](Code/outputs/data_summary.md). Provenance, units and checksum: [Attachments/SOURCE.md](Attachments/SOURCE.md).

### Source

The World Happiness Report's panel of **raw** underlying variables — measures in their own natural units, rather than the modelled contributions in ladder points that the Figure 2.1 workbooks publish.

| | |
| --- | --- |
| File | `Attachments/DataForTable2.1.xls` |
| Edition | World Happiness Report **2024** |
| Retrieved from | Internet Archive snapshot of 2 December 2024, of `happiness-report.s3.amazonaws.com/2024/DataForTable2.1.xls` |
| Retrieved | 2026-09-02 |
| Sheet | `Sheet1` (the only sheet) |
| SHA-256 | `dd5d9c737f86a05eec5ddaef644c37e3528fca125d9716ec51eb48697fff8349` |
| Citation | Helliwell, J. F., Layard, R., Sachs, J. D., De Neve, J.-E., Aknin, L. B., & Wang, S. (Eds.). (2024a). *World Happiness Report 2024*. University of Oxford: Wellbeing Research Centre. |

Underlying survey data is the Gallup World Poll (Gallup, n.d.).

**Provenance caveat.** WHR stopped publishing this panel after the 2024 edition, so it came from an archive snapshot rather than the publisher's live site and cannot currently be re-downloaded from `worldhappiness.report` to confirm. The checksum pins exactly what was used. Variable definitions are taken from the report's statistical appendix (Helliwell et al., 2024b), which *is* still on the live site.

### Shape

**2,247 rows × 12 columns**, one row per country-year. 164 countries, 17 consecutive years **2007–2023**, no gaps. No duplicate (`Country name`, `year`) pairs.

Working dataset: [Code/outputs/whr_2007_2023.csv](Code/outputs/whr_2007_2023.csv). Scope reasoning: [Scope decision](#scope-decision-20072023).

Values are **annual**, not multi-year averages, so observations in different years are independent — unlike the Figure 2.1 workbooks, whose three-year rolling averages overlap.

### Columns and units

| Column | Unit | Non-null | Min | Max |
| --- | --- | ---: | ---: | ---: |
| `Country name` | — | 2,247 | — | — |
| `year` | — | 2,247 | 2007 | 2023 |
| `Life Ladder` | 0–10 Cantril, single year | 2,247 | 1.281 | 7.971 |
| `Log GDP per capita` | log of PPP constant-2017 int'l $ | 2,220 | 5.527 | 11.676 |
| `GDP per capita (PPP 2017 int$)` | dollars — **derived**, `exp` of the above | 2,220 | 251 | 117,664 |
| `Social support` | proportion 0–1 | 2,234 | 0.228 | 0.987 |
| `Healthy life expectancy at birth` | years | 2,186 | 17.36 | 74.60 |
| `Freedom to make life choices` | proportion 0–1 | 2,216 | 0.228 | 0.985 |
| `Generosity` | unitless residual | 2,200 | −0.340 | 0.700 |
| `Perceptions of corruption` | proportion 0–1 | 2,130 | 0.035 | 0.983 |
| `Positive affect` | proportion 0–1 | 2,225 | 0.179 | 0.884 |
| `Negative affect` | proportion 0–1 | 2,233 | 0.083 | 0.705 |

`GDP per capita (PPP 2017 int$)` is added by `02_select_scope.py` as `exp(Log GDP per capita)` — a lossless, reversible unit change so the figure is readable. The log column is retained, because equal increments in it correspond to equal *proportional* differences in income.

**What the columns mean**, per the statistical appendix (Helliwell et al., 2024b):

- `Life Ladder` — national average response to the Cantril ladder question (Cantril, 1965): imagine a ladder from 0 (worst possible life) to 10 (best possible life); which step do you feel you stand on?
- `Log GDP per capita` — natural log of GDP per capita, PPP, at constant 2017 international dollars. World Development Indicators v23 (World Bank, n.d.), except Taiwan, Syria, Palestinian Territories, Venezuela, Djibouti and Yemen, which come from Penn World Table 10.01 (Feenstra et al., 2015). **It is a log**: exponentiated, the observed range is **$251 – $117,664** per capita, and equal increments correspond to equal *proportional* differences in income.
- `Social support` — share answering yes to "if you were in trouble, do you have relatives or friends you can count on to help you whenever you need them?"
- `Healthy life expectancy at birth` — years, from the WHO Global Health Observatory (World Health Organization, n.d.), interpolated and extrapolated by WHR to cover years the WHO series does not reach.
- `Freedom to make life choices` — share satisfied with "your freedom to choose what you do with your life".
- `Generosity` — **not a measure of giving.** It is the residual of regressing the national average of "have you donated money to a charity in the past month?" on GDP per capita, so it is already income-adjusted and can be negative. It answers "how generous, given this country's income?"
- `Perceptions of corruption` — average of two yes/no items on whether corruption is widespread in government and in business.
- `Positive affect` — average of three yes/no items: laughter, enjoyment, and doing something interesting yesterday.
- `Negative affect` — average of three yes/no items: worry, sadness, anger yesterday.

### Coverage

| Year | Countries | Complete rows | Rows with key 5 | % complete |
| ---: | ---: | ---: | ---: | ---: |
| 2007 | 102 | 91 | 97 | 89 |
| 2008 | 110 | 100 | 105 | 91 |
| 2009 | 114 | 105 | 107 | 92 |
| 2010 | 124 | 111 | 115 | 90 |
| 2011 | 146 | 132 | 139 | 90 |
| 2012 | 141 | 121 | 135 | 86 |
| 2013 | 136 | 124 | 132 | 91 |
| 2014 | 144 | 129 | 133 | 90 |
| 2015 | 142 | 128 | 135 | 90 |
| 2016 | 141 | 125 | 134 | 89 |
| 2017 | 147 | 132 | 141 | 90 |
| 2018 | 141 | 129 | 137 | 91 |
| 2019 | 143 | 129 | 138 | 90 |
| 2020 | 116 | 105 | 111 | 91 |
| 2021 | 122 | 114 | 117 | 93 |
| 2022 | 140 | 127 | 131 | 91 |
| 2023 | 138 | 120 | 126 | 87 |

"Key 5" is `Life Ladder`, `Log GDP per capita`, `Social support`, `Healthy life expectancy` and `Freedom to make life choices` — the columns most analyses will need. Corruption and generosity are the sparsest.

- Completeness is uniform: 86–93% in every year. No weak year inside the scope.
- Countries per year rises from 102 to about 140, dipping to 116 and 122 in **2020 and 2021** as Gallup fieldwork was disrupted.
- Years observed per country: median 16, minimum 1. **54 countries appear in all 17 years** at any level of completeness.

#### Balanced-panel options

Some comparisons over time need the same countries in every year. The cost is country count:

| Requirement | Countries in all 17 years | Country-years |
| --- | ---: | ---: |
| Every column present | 40 | 680 |
| Five key variables present | 46 | 782 |

The 40 are: Argentina, Bolivia, Cameroon, Chile, Colombia, Costa Rica, Denmark, Dominican Republic, Ecuador, El Salvador, Georgia, Ghana, India, Indonesia, Israel, Italy, Kazakhstan, Kenya, Kyrgyzstan, Lithuania, Mexico, Moldova, Nepal, Nicaragua, Pakistan, Peru, Philippines, Russia, Senegal, South Africa, Spain, Sweden, Tanzania, Thailand, Türkiye, Uganda, Ukraine, United Kingdom, Uruguay, Zimbabwe.

That set is not obviously skewed — in 2023 its median GDP per capita is $13,324 against $15,536 for excluded countries, and its median ladder 5.91 against 5.80, so it spans rich and poor. **But it excludes the United States, China, Germany, France, Japan, Brazil, Canada, Australia and Nigeria**, each missing at least one value in at least one year. A strictly balanced panel leaves out most of the largest economies, which is worth weighing against what it buys.

### Completeness

2,022 of 2,247 rows (90%) have every column present; 2,133 (95%) have all five key variables.

| Column | Missing rows |
| --- | ---: |
| `Perceptions of corruption` | 117 |
| `Healthy life expectancy at birth` | 67 |
| `Generosity` | 47 |
| `Freedom to make life choices` | 31 |
| `Log GDP per capita` | 27 |
| `Positive affect` | 22 |
| `Negative affect` | 14 |
| `Social support` | 13 |

`Life Ladder`, `Country name` and `year` are complete for every row. Missing values are absent rather than zero-filled — checked, because a zero in any of these columns would read as a real measurement.

#### Gaps are systematic, not random

They concentrate in particular countries. The ten worst, by missing cells: Taiwan Province of China, United Arab Emirates, China, Kosovo, State of Palestine, Jordan, Kuwait, Saudi Arabia, Bahrain, Qatar.

More consequentially, several countries have a column missing in **every** year they appear, so there is nothing within that country to interpolate from:

| Column | Countries with no observation at all |
| --- | --- |
| `Perceptions of corruption` | China, Maldives, Oman, Turkmenistan |
| `Healthy life expectancy at birth` | Hong Kong S.A.R. of China, Kosovo, Somaliland region, State of Palestine |
| `Log GDP per capita` | Somaliland region, South Sudan |
| `Generosity` | Somaliland region, South Sudan |
| `Positive affect` | Maldives, Oman |
| `Social support` | Oman |
| `Negative affect` | Maldives |

For `Perceptions of corruption` the mechanism matters: WHR's appendix notes the questions were not asked in some countries, and the affected set is dominated by Gulf states, China and Turkmenistan — places where asking whether government corruption is widespread is politically sensitive. **The data is missing because of what it measures.** That is the pattern under which imputation does most damage, since any filled value would be a guess in exactly the cases where the truth is least knowable from a survey.

Two crude checks find no wealth gradient: rows with a gap have a median life ladder of 5.50 against 5.44 for complete rows, and median GDP $13,974 against $13,470. Reassuring about income; silent about the political mechanism.

Note also that `Healthy life expectancy at birth` is interpolated and extrapolated by WHR across the whole period, so part of that column is already model output rather than measurement.

### Missing-data and panel decisions

**Decided 2026-09-07.**

- **No balanced panel.** Countries need not appear in every year. Analyses run on an unbalanced panel, using whatever rows are available. This keeps the United States, China, Germany, France, Japan, Brazil, Canada, Australia and Nigeria in play, all of which a strictly balanced panel would have excluded.
- **No imputation.** Missing values are left missing. Each analysis uses the rows that carry the variables it needs — 2,022 of 2,247 rows (90%) are complete, and 2,133 (95%) have the five key variables.
- **Where a variable is systematically absent, name the excluded countries and state the likely bias**, rather than inventing a number for them. Any question involving `Perceptions of corruption` loses China, the Maldives, Oman and Turkmenistan outright.
- Consequence to carry forward: sample size and composition will differ between analyses. Each result must state what it was computed on.

### Known defects in the source

- **Haiti's healthy life expectancy is corrupted**, in six rows inside the scope: 17.36 (2008), 28.00 (2010), 33.32 (2011), 38.64 (2012), 43.96 (2013) and 49.28 (2014) years. From 2010 to 2015 the series rises in exact steps of +5.32 years per year, reaching 54.60 in 2015, after which the steps become +0.30. A constant increment is what linear interpolation between two anchor observations produces, and the change of step locates the anchor: 2015 is observed and the ramp before it is constructed. Haiti's actual healthy life expectancy is around 55 years throughout, so the early values are implausible on their own terms as well. A seventh and worse row, 6.72 years in 2006, falls outside the scope.
- **2023 GDP is partly forecast, not measured.** The statistical appendix (Helliwell et al., 2024b) states 2023 GDP per capita was unavailable when the file was built and was extended from 2022 using OECD and World Bank growth forecasts. 2023 also has the most missing GDP of any year in scope.
- **Venezuelan GDP is unreliable** across the whole series, falling to an implied $251 per capita by 2019. Venezuela is one of six countries whose GDP comes from the Penn World Table rather than WDI. Removed — see [Cleaning decisions](#cleaning-decisions).
- `Healthy life expectancy at birth` is interpolated and extrapolated throughout, so early values for some countries are model output rather than measurement.

None of these have been altered. Whether to exclude or correct them is a cleaning decision, not yet taken.

### Scope decision: 2007–2023

**Decided 2026-09-02.** Keep `2007 <= year <= 2023`; applied by [Code/02_select_scope.py](Code/02_select_scope.py), full report in [Code/outputs/scope.md](Code/outputs/scope.md).

*Reason.* 2005 held 27 countries and exactly one row with every column present. 2006 held 89 countries at 83% completeness — the weakest of any usable year. From 2007 the panel runs at 102 or more countries and 86–93% completeness every year. Starting at 2007 keeps 17 consecutive years without carrying the two thin ones.

*What was excluded, and what it costs.* 116 rows from 2005 and 2006, and one country entirely — **Cuba**, which appears in neither year from 2007 on. Two years of history, both thin. Nothing else.

### Cleaning decisions

**Decided 2026-09-07.** Applied by [Code/03_clean.py](Code/03_clean.py); full report in [Code/outputs/cleaning.md](Code/outputs/cleaning.md). Analysis dataset: [Code/outputs/whr_clean.csv](Code/outputs/whr_clean.csv).

Cleaning here means one thing only: **setting values that are known to be wrong to missing.** Nothing is imputed, estimated or overwritten, consistent with the no-imputation decision above. Cells are blanked, never rows dropped, so a country keeps every other variable for that year.

| Rule | Effect |
| --- | --- |
| **Haiti, `Healthy life expectancy at birth`, 2008/2010/2011/2012/2013/2014 → missing.** The whole span is a broken backwards extrapolation: from 2010 to 2015 the series rises in exact steps of +5.32 years per year to 54.60 in 2015, after which the steps become +0.30. The change of increment locates the anchor, so 2015 is observed and everything before it on the ramp is constructed. Haiti's true figure over this period is around 55 years. 2015 onwards is kept. <br><br>**Supersedes an earlier version of this rule, decided the same day**, which blanked only 2008/2010/2011/2012 — the values below 40 years — on a plausibility test alone. That left 2013 (43.96) and 2014 (49.28) on the same fabricated ramp, because they are individually plausible for Haiti and only the constant increment reveals them. The constant-increment test is the sounder one and replaces it. | 6 cells. `Healthy life expectancy` missing rises from 61 to 67. |
| **Venezuela, both GDP columns, all years → missing.** The series falls from $19,197 (2012) to $251 (2019), a 98.7% cumulative collapse ending far below the poorest country in the panel — Niger was $1,217 the same year. Venezuela's real contraction was severe but nearer 75–80%. WHR sources Venezuelan GDP from the Penn World Table rather than the World Bank; Venezuela stopped publishing national accounts around 2014 and then hyperinflated, so any price-based conversion explodes. The divergence grows from about 2014 with no clean breakpoint visible inside the file, so the whole series is blanked rather than a cut-off guessed. | 24 cells across 12 rows. Both GDP columns rise from 27 missing to 39. |

**Consequence.** Venezuela is now absent from any analysis involving GDP — 16 rows in scope, none with an income figure. It keeps its life ladder and every survey-based measure, so it remains available for anything not using GDP. Its ladder is intact and plausible throughout (6.55 in 2013, falling to 4.04 in 2016, recovering to 5.77 by 2023), which is worth remembering: the country's collapse *is* visible in the wellbeing data even though its income data is unusable.

**Accepted as-is, not cleaned:**

- **2023 GDP is partly forecast.** WHR extended 2023 from 2022 using OECD and World Bank growth forecasts. Accepted: a one-year-ahead forecast is a reasonable estimate, and dropping 2023 would cost the most recent year of the panel. Any result that depends on 2023 GDP should say so.
- **`Healthy life expectancy at birth` is interpolated throughout**, for every country and not only Haiti. WHR extends the WHO series across the sample period, so the whole column is part measurement, part model output.

All cleaning decisions are now settled.

### Not yet done

No country scoping, and no validation beyond the range checks above. Step 1 is otherwise complete: the data is acquired, described, scoped and cleaned. No research question has been framed.

## Research Question

*Step 2, settled 2026-09-07. Written before anything was tested: no statistic, chart or calculation has been produced from these variables.*

### Discussion

**Origin.** The question was posed as: *"I want to look at the relationship between happiness and life expectancy. Do countries with higher life expectancy have higher levels of happiness?"*

**The variable is healthy life expectancy, not life expectancy.** The file carries `Healthy life expectancy at birth` — expected years lived *in good health* — and has no plain life-expectancy column. The two differ by however many years a population lives in poor health, which varies by country. Healthy life expectancy is arguably the better variable for a wellbeing question, but the question must be stated in those terms. Answering it about total lifespan would require a second source, which was not pursued.

**Descriptive, not causal.** Recorded as a question about association: do these two things go together across countries, and how strongly? It is *not* a claim that longer healthy life causes happiness, and the analysis will not support one. Countries are not randomly assigned life expectancies; and the causation plausibly runs both ways, since wellbeing is itself associated with health and longevity. No design available in this data separates the directions.

**Ecological level.** Every observation is a national average. A country-level association says nothing directly about individuals — a country where longer-lived people are happier and a country where the two are unrelated within the population can produce the same national figures. Conclusions must stay at the level of countries.

**Why the question is not trivial even though the answer is nearly certain.** WHR's own published model already uses healthy life expectancy as one of six factors explaining the ladder, so a positive association is close to a foregone conclusion. The content lies in the three refinements: how large the association is in interpretable units, whether any of it stands independently of income, and whether it holds within countries over time as well as between them.

**Income is the obvious confound.** Richer countries have both longer healthy lives and higher ladder scores, so a raw association may substantially reflect income acting on both. Hence sub-question 2. Note that `Log GDP per capita` is a log, so it carries proportional rather than absolute income differences.

**Between countries and within countries are different questions.** "Countries with higher X have higher Y" is a between-country claim. "A country whose X rises sees Y rise" is a within-country claim. They can differ in size and even in sign, and the data supports both, so they are separated into sub-questions 1 and 3.

**Known feasibility limits, from step 1:**

- `Healthy life expectancy at birth` is **interpolated and extrapolated by WHR** across the whole period, for every country. That is tolerable when the variable is one control among six; it matters more when it is the centre of the question. It particularly threatens sub-question 3, because smoothing may leave within-country year-to-year variation that is largely an artefact of the interpolation rather than real change.
- **Four countries have no healthy life expectancy at all** — Hong Kong S.A.R. of China, Kosovo, Somaliland region, State of Palestine — and drop out of all four sub-questions.
- **Haiti's 2008/2010/2011/2012/2013/2014 values were blanked** in cleaning, so Haiti contributes fewer years.
- **Venezuela has no income data** after cleaning, so it drops out of sub-question 2 specifically.
- Sample size and composition will therefore differ between sub-questions. Each result must state what it was computed on.

**Considered and dropped.** A fifth sub-question — whether healthy life expectancy relates differently to *evaluative* wellbeing (the ladder) than to *experiential* wellbeing (`Positive affect`, `Negative affect`) — was proposed and not taken up. The two affect columns remain available if it is revisited.

### Question

**Do countries with higher healthy life expectancy have higher levels of happiness?**

Happiness is `Life Ladder`, the national average Cantril ladder score (0–10). Healthy life expectancy is `Healthy life expectancy at birth`, in years. The claim under examination is one of association across countries, not of cause.

### Sub-questions

To be answered **one at a time**, in order, with the method agreed before each is applied.

**1. Across countries, is higher healthy life expectancy associated with higher life-ladder scores?**

- Variables: `Life Ladder`, `Healthy life expectancy at birth`.
- What counts as an answer: the direction and size of the association, reported in ladder points per additional decade of healthy life expectancy, judged against the spread of ladder scores across countries. A positive association large relative to that spread supports the claim; one near zero, or negative, contradicts it.

**2. Does that association survive accounting for income?**

- Variables: as above, plus `Log GDP per capita`.
- What counts as an answer: the association reported both before and after accounting for income. If it attenuates substantially toward zero, healthy life expectancy carries little that income does not already capture. If it largely persists, it stands partly on its own.
- Venezuela is excluded here, having no income data.

**3. Year to year within countries, does the growth rate of happiness depend on healthy life expectancy, and does it slow as happiness rises?** *(Revised 2026-09-07 — see below.)*

- **Data:** every pair of consecutive calendar years in which `Life Ladder`, `Log GDP per capita` and `Healthy life expectancy at birth` are all present in both years. Income is required for sample selection even though the first model does not use it, so that adding income later does not change the sample.
- **Notation:** $H$ is happiness, the national average Cantril life ladder; $E$ is healthy life expectancy at birth, in years.
- **Model, as specified by the user** *(revised three times — see below)*:

  $$H_{t+1} - H_t \;=\; k + H_t\,(a_0 + a_1 H_t) + a_2 E_t$$

  Multiplied out, this is linear in the parameters and fitted by ordinary least squares on the change itself:

  $$\Delta H \;=\; k + a_0 H_t + a_1 H_t^2 + a_2 E_t + \varepsilon$$

  Healthy life expectancy enters **additively**, so its effect on growth is the same at every level of happiness. The constant $k$ admits growth that does not scale with the current level, so the left-hand side is a change in ladder points rather than a percentage.

  **Superseded forms**, kept on the record:

  1. $\Delta H / H_t = a_0 + a_1 H_t + a_2 E_t$ — proportional growth, no constant. Rejected in favour of fitting the change itself, which places the additive error on the change rather than on the change-per-unit-of-level.
  2. $\Delta H = k + a_0 H_t + a_1 H_t^2 + a_2 (H_t E_t) + \varepsilon$ — with healthy life expectancy multiplied by happiness. Fitted, then superseded: the interaction made every regressor a function of the same two variables, so $E$'s coefficient was poorly identified (VIF 20 against 2.1 in the additive form), and it forced the effect of healthy life expectancy to scale with happiness rather than testing whether it does.
  3. The variables were first written $L$ for the life ladder and $H$ for healthy life expectancy. Renamed to $H$ and $E$ so that the symbol matches the concept being reported.

- **What counts as an answer:**
  - $a_2 > 0$ would mean happiness grows faster in countries with longer healthy lives — the dynamic counterpart of sub-question 1.
  - $a_0 + 2a_1 H < 0$ over the observed range would mean growth slows as happiness rises, so happiness is self-limiting and tends toward an equilibrium rather than rising without bound.
  - If both hold, there is an equilibrium where $\Delta H = 0$. With $k$ present this condition is quadratic in $H$, so it may have two roots; the relevant one is the stable root, where $a_0 + 2a_1 H < 0$. Implicit differentiation gives the long-run response of happiness to healthy life expectancy, $\mathrm{d}H^*/\mathrm{d}E = -a_2 / (a_0 + 2a_1 H^*)$, which varies with the level and so must be evaluated at a stated $H$. It can then be compared against the +1.47 per decade found across countries.
  - Intervals spanning zero for $a_2$ would mean the growth rate carries no detectable signal from healthy life expectancy, which is a real answer and not a failure.

**Superseded original wording.** The question was first framed as *"Within a country over time, does rising healthy life expectancy accompany rising happiness?"*, to be answered by comparing within-country and between-country associations. It was flagged then as the weakest of the four, because healthy life expectancy is interpolated across the period and much of its within-country movement is smoothing rather than measurement. That concern still applies to the level of $H$ used as a regressor, but the revised question asks something different and more specific: it puts the *growth rate of happiness* on the left-hand side rather than differencing healthy life expectancy, so it no longer depends on year-to-year movement in $H$ being real.

**4. Is the relationship uniform, or does it flatten at high healthy life expectancy? — DROPPED 2026-09-07, not attempted.**

- Variables would have been: as sub-question 1.
- What would have counted as an answer: whether a straight line describes the relationship adequately, or whether the association weakens at the top of the healthy-life-expectancy range.
- **Why dropped.** By the user's decision, on the view that the linear relationship describes the data well enough. **It was not tested.** The straight line in Figure 1 reaches R² = 0.586 and the rank correlation agrees with it, which is consistent with adequacy but does not establish it — no curvature term was fitted and no lack-of-fit test was run. The vertical spread of the scatter is visibly wider at high healthy life expectancy, which remains unexamined.
- Recorded rather than deleted, so it is visible that the question was asked and set aside for a stated reason. Nothing here should be read as evidence that the relationship *is* uniform.

## Analysis

Sub-questions are worked one at a time, with the method agreed before it is applied. Each records what was done, on what, and what is visible — separately from what it means, which is step 5.

### Sub-question 1: across countries, is higher healthy life expectancy associated with higher life-ladder scores?

**Step 3, visualisation. 2026-09-07.** Generated report: [Code/outputs/sq1_scatter.md](Code/outputs/sq1_scatter.md). Script: [Code/04_sq1_scatter.py](Code/04_sq1_scatter.py).

#### Cross-section

**Method, as agreed:** one row per country, at its **most recent year in which both `Life Ladder` and `Healthy life expectancy at birth` are present**. Cross-section written to [Code/outputs/latest_by_country.csv](Code/outputs/latest_by_country.csv).

- **160 countries** of the 164 in the cleaned panel.
- **4 excluded** — Hong Kong S.A.R. of China, Kosovo, Somaliland region, State of Palestine — each lacking healthy life expectancy in every year, so no row exists for them at any date.
- `Life Ladder` spans 1.45–7.70; `Healthy life expectancy at birth` spans 45.3–74.6 years.

**The cross-section mixes years.** "Most recent available" is not the same year for every country: 135 of 160 (84%) contribute 2023, while 25 contribute something earlier, back to Guyana in 2007. A country whose coverage stopped early contributes an older observation, so this is not a snapshot of any single year. The full year-by-year breakdown and the list of the 25 are in the generated report.

**Decision, 2026-09-07: keep them.** All 160 countries are retained, including the 25 whose most recent year is earlier than 2023. This buys 25 countries at the cost of comparing observations up to 16 years apart. It was preferred to a clean 2023 snapshot because those 25 are not a random selection — coverage tends to stop for reasons connected to instability, so dropping them would quietly bias the cross-section toward countries stable enough to keep being surveyed.

The cost to carry forward: this cross-section is not a snapshot of a single year, and any statement drawn from it describes countries at their most recent observation rather than at a common date. Where a country's healthy life expectancy or happiness has moved since, that movement is invisible here.

#### Scatter

![sq1_scatter](Code/outputs/figures/sq1_scatter.png)

*One point per country at its most recent year with both measures (n = 160). Labels mark the extremes on each axis. Dark-theme version: `Code/outputs/figures/dark/sq1_scatter.png`.*

At step 3 no line was fitted and no correlation reported, so the relationship could be seen before it was summarised. The figure above now carries the fitted line added at step 4; the unfitted version is in the repository history.

What is visible, as description only:

- The points slope upward from bottom-left to top-right: countries with longer healthy lives do tend to report higher ladder scores.
- The scatter is wide. At the upper end of healthy life expectancy, roughly 65–72 years, ladder scores run from about 3.6 to about 7.7 — nearly the full range of the variable. Longer healthy life is plainly not sufficient for a high score.
- The vertical spread looks narrower at low healthy life expectancy than at high, which is what the heteroscedasticity-robust standard errors are for. It says nothing about the shape of the relationship, and the shape was never tested.
- Afghanistan sits far below everything else, at a ladder score of 1.45 against a healthy life expectancy near the middle of the range.

These are observations about the figure, not findings. Nothing here has been tested.

#### Step 4: the fit

**2026-09-07.** Generated report: [Code/outputs/sq1_regression.md](Code/outputs/sq1_regression.md). Script: [Code/05_sq1_regression.py](Code/05_sq1_regression.py).

**Method, as agreed.** OLS of `Life Ladder` on `Healthy life expectancy at birth` across the 160-country cross-section, with heteroscedasticity-robust (HC3) standard errors because the scatter showed unequal vertical spread. Slope reported per decade so its size is interpretable. Spearman's rank correlation as a robustness check that assumes no functional form. Influence measured rather than assumed.

Note that OLS does not assume the relationship is truly linear — it estimates the best linear approximation to whatever shape is present. Whether a line describes it adequately was not tested.

| Quantity | Value |
| --- | --- |
| n | 160 countries |
| Slope | **+1.47 ladder points per decade** (95% CI +1.26 to +1.68) |
| Slope per single year | +0.1472 ladder points |
| Robust *p* | 9.9 × 10⁻⁴³ |
| R² | **0.586** |
| Residual SD | 0.767 ladder points, against a ladder SD of 1.188 |
| Spearman's ρ | **0.769** (*p* = 1.5 × 10⁻³²) |

Over the full observed span of healthy life expectancy — 29.3 years, from 45.3 to 74.6 — the fitted line rises 4.31 ladder points, about 69% of the observed ladder range.

**Influence.** Each row refits the same model on a reduced sample.

| Sample | n | Slope per decade | R² |
| --- | ---: | ---: | ---: |
| All countries | 160 | 1.472 | 0.586 |
| Excluding Afghanistan | 159 | 1.431 | 0.589 |
| Excluding healthy life expectancy < 50 | 157 | 1.562 | 0.582 |
| Excluding the 25 pre-2023 observations | 135 | 1.550 | 0.567 |

Largest Cook's distances: Afghanistan 0.128, Mozambique 0.108, Somalia 0.099, Guyana 0.042, Central African Republic 0.039. Nine countries exceed the conventional 4/n threshold of 0.025. No single exclusion moves the slope outside the confidence interval of the full fit.

**Which countries are labelled.** Both label sets are chosen by rule, so neither is picked to make a point:

- The extreme country on each axis — Central African Republic (lowest healthy life expectancy), Japan (highest), Afghanistan (lowest ladder), Finland (highest).
- The three nearest the centre of the distribution, measured in standardised units so the two axes count equally despite their different scales: **Iraq, Georgia and Azerbaijan**, against a centre of 64.3 years and 5.49 ladder points. These three sit almost on top of one another, so their labels are fanned out with leader lines.

Note the centroid rule happens to return three neighbouring countries in the Caucasus and Middle East. They are genuinely the closest to the centre, but they are not a geographic cross-section of typical countries.

**Assumptions and limits.**

- **Unequal spread** was expected from the scatter, so standard errors are HC3-robust. The slope estimate itself is unaffected by heteroscedasticity; only its interval would be.
- **Measurement error in the predictor.** Healthy life expectancy is interpolated and extrapolated by WHR, so it is partly model output. Classical measurement error in a predictor attenuates a slope toward zero, so +1.47 is a **lower bound** on the association.
- **Countries are not independent draws.** Neighbours share institutions, health systems and history, so the effective sample is smaller than 160 and the interval is optimistic. No fix is available at this level of aggregation.
- **The cross-section mixes years**, adding noise that cannot be separated from the relationship.
- **Association, not cause**, and **countries, not people**, as fixed in the research question.
- **Whether a line is the right shape is not settled here**, and it is not settled anywhere in this analysis: no test of curvature was carried out.

### Sub-question 2: does the association survive accounting for income?

**Steps 3 and 4 together, 2026-09-07.** Generated report: [Code/outputs/sq2_income.md](Code/outputs/sq2_income.md). Script: [Code/06_sq2_income.py](Code/06_sq2_income.py).

#### Sample

**Method, as agreed — option (a).** The sub-question 1 cross-section, reduced to rows that also carry income, with every country left at the same year it had there. This keeps the two sub-questions describing the same country-years, at the cost of a smaller sample. The alternative — rebuilding as "most recent year with all three variables" — was rejected because a country whose latest healthy-life-expectancy year lacks GDP would have shifted to an earlier year, so the two sub-questions would no longer be comparable.

- **152 countries**, down from 160.
- Dropped for having no income figure: Afghanistan, Cyprus, Libya, Malta, Singapore, South Sudan, Venezuela, Yemen. Venezuela's absence follows from the cleaning decision; its GDP was blanked in full.
- **Afghanistan's exit matters more than the count suggests.** It was the largest outlier in Figure 1, so its removal is a change in the sample's character, not just its size. The healthy-life-expectancy-only model was therefore refitted on these 152 countries, so the before/after comparison is not contaminated by the sample having changed: that refit gives +1.42 against the +1.47 reported on the full 160.

#### How separable are the two predictors?

Reported before the fits, because it governs how much the fits can be trusted to divide credit between the two variables.

Pearson correlation between log GDP per capita and healthy life expectancy: **r = 0.835** (r² = 0.70).

![sq2_collinearity](Code/outputs/figures/sq2_collinearity.png)

<small><b>Figure A1.</b> Healthy life expectancy against income across the same 152 countries, income on a log scale. Diagnostic figure, not part of the report.</small>

#### The fits

All with HC3 robust standard errors; intervals are 95%.

| Model | n | HLE per decade | log GDP coefficient | R² |
| --- | ---: | --- | --- | ---: |
| A — healthy life expectancy only | 152 | +1.42 [+1.22, +1.61] | — | 0.575 |
| B — plus log GDP per capita | 152 | **+0.59 [+0.18, +1.00]** | +0.507 [+0.318, +0.696] | 0.659 |
| Income only, for symmetry | 152 | — | +0.759 [+0.674, +0.844] | 0.629 |

- The healthy-life-expectancy slope falls from +1.42 to +0.59 — **42% of it survives** — and the interval excludes zero.
- R² rises from 0.575 to 0.659 when income is added, an increase of 0.085.
- Income alone (R² = 0.629) accounts for more of the cross-country variance than healthy life expectancy alone (R² = 0.575).
- The income-only model is reported so that neither predictor is silently treated as the explanation and the other as the control.

**Collinearity diagnostics.** VIF = 3.31 for both predictors, meaning each standard error is 1.82× wider than it would be if the two were unrelated. Conventional thresholds put 5 as a concern and 10 as serious, so the coefficients are separable — but not sharply, and the split between them should not be read as a precise apportionment.

![sq2_added_variable](Code/outputs/figures/sq2_added_variable.png)

<small><b>Figure A2.</b> Added-variable plot. Both variables residualised on log GDP per capita, so the slope shown is exactly the partial coefficient from model B. Was Figure 2 of the report until 2026-09-08, when it was dropped; kept here because the two-stage equivalence below refers to it.</small>

#### Is the two-stage route different?

Checked because the question was raised, and recorded here rather than in the report: the answer changed nothing about the method or the result. Adjusting for income can be done in one step — the multiple regression reported above — or in two: residualise the life ladder on log GDP, residualise healthy life expectancy on log GDP, then regress the first residual on the second.

| Method | Slope per decade | 95% CI (HC3) |
| --- | ---: | --- |
| One step: `ladder ~ HLE + logGDP` | +0.5894 | [+0.176, +1.003] |
| Two stage: **both** residualised on log GDP | +0.5894 | [+0.177, +1.002] |
| Two stage: **only the outcome** residualised, regressed on raw HLE | +0.178 | [−0.034, +0.390] |

- The first two agree to **7.6 × 10⁻¹⁷** — floating-point zero. This is the Frisch–Waugh–Lovell theorem: regressing residualised outcome on residualised predictor recovers the multiple-regression coefficient exactly. They are one method, not two, and Figure A2 is the two-stage version of it.
- The third is **not** equivalent, and the difference is not cosmetic: at +0.178 with an interval spanning zero it would have supported the opposite conclusion. It fails because healthy life expectancy's own correlation with income (r = 0.835) is removed from the outcome but left in the predictor.
- The naive two-stage version also mis-counts degrees of freedom — 150 rather than 149, since it does not know a parameter was spent in the first stage — giving a non-robust standard error of 0.1619 against the correct 0.1625. Negligible at this sample size, wrong in principle, and worse with more controls.

Two genuinely different ways to control for income were considered and **not** run, by the user's decision: letting income enter flexibly through a spline or quadratic in log GDP, which would test whether +0.59 depends on forcing income to be linear; and stratifying or matching within income bands, which would answer "among countries of similar income" without assuming any functional form. Both remain open.

#### What this does and does not establish

- The partial coefficient answers a narrow question: **among countries with similar income, do those with longer healthy lives report higher ladder scores?** It is not a claim that healthy life expectancy matters independently of income in any causal sense.
- **Adjusting for income is not a neutral operation here.** Income and health are both partly produced by the same development processes, so income is not a confounder sitting outside the relationship. Removing it may remove part of the pathway by which longer healthy lives arise, which would make the adjusted slope an understatement rather than a correction. Equally, the unadjusted slope may overstate. The two numbers do not bracket a true value; they answer two different questions.
- **Measurement error still attenuates.** Healthy life expectancy is partly interpolated, so its coefficient remains a lower bound — and in a multivariable fit, error in one predictor can bias the other's coefficient in either direction.
- Unequal spread, non-independent countries and the mixed-year cross-section all carry over from sub-question 1.

### Sub-question 3: the growth of happiness

**2026-09-07.** Generated report: [Code/outputs/sq3_growth.md](Code/outputs/sq3_growth.md). Script: [Code/07_sq3_growth.py](Code/07_sq3_growth.py). Paired sample: [Code/outputs/consecutive_pairs.csv](Code/outputs/consecutive_pairs.csv).

#### Sample

Every pair of consecutive **calendar** years with `Life Ladder`, `Log GDP per capita` and `Healthy life expectancy at birth` present in both: **1,872 pairs from 151 countries**, start years 2007–2022, median 14 pairs per country. The change in ladder has mean +0.014 and SD 0.375, ranging −2.00 to +1.66.

Pairs overlap by construction — each year ends one pair and begins the next — so errors are serially correlated within a country and standard errors are clustered by country throughout.

#### Estimates

$$\Delta H = k + a_0 H_t + a_1 H_t^2 + a_2 E_t + \varepsilon$$

| Term | Estimate | 95% low | 95% high | *p* |
| --- | ---: | ---: | ---: | ---: |
| $k$ (constant) | +0.390 | −0.017 | +0.797 | 0.061 |
| $a_0$ — $H_t$ | −0.3927 | −0.5464 | −0.2390 | 5.6 × 10⁻⁷ |
| $a_1$ — $H_t^2$ | +0.02415 | +0.01134 | +0.03696 | 2.2 × 10⁻⁴ |
| $a_2$ — $E_t$ | **+0.01575** | +0.01145 | +0.02005 | 7.0 × 10⁻¹³ |

n = 1,872, clustered on 151 countries. R² = 0.0715; residual SD 0.361 against an outcome SD of 0.374. Joint test that $a_0 = a_1 = a_2 = 0$: F = 26.30, *p* = 1.0 × 10⁻¹³.

R² builds up as 0 (constant only) → 0.031 (+ $H_t$) → 0.038 (+ $H_t^2$) → 0.072 (+ $E_t$). It is low throughout, which is expected: year-on-year change in a national survey mean is mostly noise. The question is whether any systematic part of it tracks the level and healthy life expectancy, not whether the model predicts individual changes.

**Note the constant is not distinguishable from zero** (*p* = 0.061). It was included at the user's request to relax the restriction that the growth curve pass through the origin; the data does not demand it, but nor does it rule it out, and dropping it would force a restriction the evidence does not support either way.

Note also the sign of $a_1$ is **positive**, which does not mean growth accelerates with happiness. The slope of the growth curve is $a_0 + 2a_1 H$, negative across the whole observed range — −0.286 at the lowest observed happiness, −0.007 at the highest. The positive $a_1$ only means the slowing is slightly less steep at high levels.

#### Collinearity

| Term | VIF |
| --- | ---: |
| $H_t$ | 78.3 |
| $H_t^2$ | 75.8 |
| $E_t$ | **2.1** |

$H$ and $H^2$ are necessarily collinear, being functions of the same variable, so their individual coefficients are imprecise and are best read together as the shape of the growth curve. **$E$ is now well identified** — a VIF of 2.1 against 20.0 in the superseded interaction form, where every regressor was a function of the same two variables.

#### Implied equilibrium

Setting $\Delta H = 0$ at the median healthy life expectancy (65.2 years) gives roots at $H$ = 5.57 and 10.64. The second is outside the observed range of 2.18–7.97 and is disregarded. The stable root is $H^* = 5.57$.

| $E$ (years) | Stable $H^*$ | $\mathrm{d}H^*/\mathrm{d}E$ per decade |
| ---: | ---: | ---: |
| 54.0 (10th pct) | 4.40 | +0.88 |
| 65.2 (median) | 5.57 | +1.29 |
| 71.1 (90th pct) | 6.50 | +2.02 |

The long-run response still varies with the level, because the equilibrium condition remains quadratic in $H$ — but now through $a_0 + 2a_1 H^*$ alone, not through $E$ as well.

**This is an equilibrium of the happiness equation at a fixed healthy life expectancy**, not of the two-variable system. Put both equations together and there is no equilibrium at all, because the fitted $\Delta E$ never reaches zero — see [Phase portrait](#phase-portrait-the-two-models-as-one-system). $H^*$ is the level happiness would settle at *if* healthy life expectancy stopped moving, which in this fit it never does.

**The agreement with sub-question 1 is a consistency check, not independent confirmation.** At the median, the dynamics imply +1.29 ladder points per decade against +1.47 measured across countries. That the two are close is what one would expect if countries sit near their equilibrium levels, since in that case the cross-sectional relationship *is* the equilibrium relationship. It is reassuring about the specification rather than a second piece of evidence for the same conclusion.

**And note what the table implies about shape.** The long-run response rises with healthy life expectancy — +0.88 per decade at 54 years against +2.02 at 71. That is convex, which is the opposite of the diminishing returns that a test for flattening at high healthy life expectancy would have been looking for. It is one model's implication rather than a test of curvature, but it is a reason to doubt that the question was as settled as it looked when it was set aside.

#### Where growth stops

Solving $\Delta H = 0$ for $E$ at a fixed level of happiness gives the healthy life expectancy at which the model predicts no further change — the zero crossings visible in Figure A3, where $E$ is on the horizontal axis.

| Happiness $H$ | Percentile | $E$ where growth stops (years) |
| ---: | --- | ---: |
| 4.1 | 10th | 50.3 |
| 5.5 | 50th | 64.4 |
| 7.1 | 90th | 73.5 |

#### Measurement error in $H_t$

$H_t$ enters $\Delta H = H_{t+1} - H_t$ negatively and the regressors positively, so sampling error in the ladder induces a negative correlation between them and pushes $a_0$ downward whether or not growth genuinely slows.

Simulated by adding fresh noise to the ladder once per country-year in the underlying panel, then rebuilding the pairs and refitting — so the same draw enters $\Delta H$ for one pair and the regressor for the next, as real sampling error does. Averaged over 40 draws per row:

| Assumed SE of ladder | $k$ | $a_0$ | $a_1$ | $a_2$ |
| ---: | ---: | ---: | ---: | ---: |
| 0 (as fitted) | +0.406 | −0.3917 | +0.0242 | +0.01575 |
| 0.05 | +0.379 | −0.3956 | +0.0241 | +0.01653 |
| 0.10 | +0.342 | −0.4027 | +0.0238 | +0.01785 |
| 0.15 | +0.300 | −0.4146 | +0.0234 | +0.01975 |

The bias runs in the predicted direction and is modest: at a sampling SE of 0.10 ladder points, $a_0$ moves by about 3% and $a_2$ by about 11%. This is a sensitivity check, not a correction — the panel publishes no intervals, so the ladder's actual sampling error is unknown.

*An earlier version of this check added independent noise to the regressor alone, which tests classical attenuation rather than the shared-error mechanism, and understated the effect. Corrected.*

#### With year effects

| Term | Pooled | With year effects | 95% low | 95% high |
| --- | ---: | ---: | ---: | ---: |
| $a_0$ — $H_t$ | −0.3927 | −0.3837 | −0.5384 | −0.2291 |
| $a_1$ — $H_t^2$ | +0.02415 | +0.02341 | +0.01059 | +0.03624 |
| $a_2$ — $E_t$ | +0.01575 | +0.01561 | +0.01121 | +0.02002 |

Year effects absorb anything that moved global happiness in a given year, the pandemic being the obvious case. The coefficients are essentially unchanged, so the result is not an artefact of a common time pattern. Reported here rather than in the report, since it changed nothing.

#### The alternative orientation

![sq3_growth_by_hle](Code/outputs/figures/sq3_growth_by_hle.png)

<small><b>Figure A3.</b> The same fitted model with the axes exchanged: change in happiness against healthy life expectancy, with lines at three levels of happiness. At a fixed level of happiness the model is linear in $E$, so the lines are straight and parallel. This was the report's growth figure until 2026-09-08, when the orientation now in the report replaced it.</small>

#### Second model: the reverse direction

**2026-09-07.** Generated report: [Code/outputs/sq3b_life_expectancy.md](Code/outputs/sq3b_life_expectancy.md). Script: [Code/08_sq3b_life_expectancy.py](Code/08_sq3b_life_expectancy.py).

$$\Delta E = k + a_1 E_t + a_2 E_t^2 + a_3 H_t + \varepsilon$$

The mirror of the model above, on the same 1,872 pairs, testing whether happiness predicts how fast healthy life expectancy rises.

**Is $\Delta E$ a measurement?** Asked before the fit, because the answer governs what a coefficient could mean. WHR interpolates and extrapolates healthy life expectancy across the whole period, and differencing an interpolation returns its gradient.

- $\Delta E$ takes only **151 distinct values across 1,872 country-years**.
- Per country the median is **4 distinct values** across a median of 14 pairs; **72 of 151 countries** have three or fewer.
- **83% of the variance in $\Delta E$ is between countries** rather than within them. For $\Delta H$ the figure is 4%.

The series make it plainest. Japan: +0.12 in every one of sixteen years. Kenya: +0.52 for eight years, then +0.40 for eight more. Brazil: +0.16 eight times, then +0.17 or +0.18. These are gradients of straight lines between anchor points, not annual observations.

**The fit.**

| Term | Estimate | 95% low | 95% high | *p* |
| --- | ---: | ---: | ---: | ---: |
| $k$ (constant) | +6.405 | +2.564 | +10.245 | 0.0011 |
| $a_1$ — $E_t$ | −0.1241 | −0.1900 | −0.0583 | 0.00022 |
| $a_2$ — $E_t^2$ | +0.000834 | +0.000310 | +0.001357 | 0.0018 |
| $a_3$ — $H_t$ | **+0.0089** | −0.0216 | +0.0394 | **0.57** |

n = 1,872, clustered on 151 countries. R² = 0.383; joint test F = 52.39, *p* = 3.2 × 10⁻²³.

**How to read the null.** The R² of 0.38 is not evidence of a good model — it comes almost entirely from $E$ and $E^2$, which track the interpolation's own structure. Happiness adds essentially nothing.

The null on $a_3$ is **uninformative, not reassuring**. It is not evidence that happiness fails to lengthen healthy life. An outcome that is 83% country-constant carries little year-on-year signal for anything to predict, so the test has little power. Absence of evidence here is close to absence of a measurement.

Three problems, any one sufficient to withhold a conclusion:

1. **The outcome barely varies within a country.** This is close to a cross-sectional regression of a country's average interpolated gain on its happiness level, even though the specification is dynamic.
2. **Serial dependence is extreme.** A country repeating one value for eight years contributes eight rows carrying the information of one. Clustering widens the intervals correctly but cannot recover information the data does not hold.
3. **Direction would not be identified even with a clean outcome.** Happier countries are richer, better governed and better served medically.

**On the apparent asymmetry.** Healthy life expectancy predicts the growth of happiness; happiness does not detectably predict the growth of healthy life expectancy. The asymmetry follows from **which variable each model has to predict**, not from any asymmetry in the world.

| | Outcome | Within-country share of its variance |
| --- | --- | ---: |
| First model | change in happiness — a survey measurement | 96% |
| Second model | change in healthy life expectancy — interpolated | 17% |

An outcome that is close to a per-country constant cannot be predicted by any regressor. The second model would return a null whether or not happiness lengthens healthy life, so the two results cannot be compared as though both tests were equally able to detect an effect.

The two R² values invite the same mistake in reverse: 0.38 for the health model against 0.072 for the happiness model makes the former look better specified, when its R² comes almost entirely from $E$ and $E^2$ tracing the interpolation's own structure.

*An earlier version of this paragraph located the asymmetry on the predictor side, saying the well-measured variable was the one appearing as a predictor. That was inside out: in the model that finds an effect, the survey measure is the outcome and the interpolated series is the predictor. The asymmetry is on the outcome side. Corrected.*

The first model does not share the defect: there the interpolated variable sits on the right-hand side as a level, and the outcome is the survey measure, which genuinely moves.

#### Phase portrait: the two models as one system

**2026-09-07.** Generated report: [Code/outputs/phase_portrait.md](Code/outputs/phase_portrait.md). Script: [Code/09_phase_portrait.py](Code/09_phase_portrait.py).

Method after Ranganathan et al. (2014), whose Figure 5 plots democracy against log GDP per capita the same way. The two fitted models define a system in the $(E, H)$ plane, and at each point the pair $(\Delta E, \Delta H)$ is one year's expected movement:

$$\Delta H = +0.3899 - 0.3927\,H + 0.0242\,H^2 + 0.0161\,E$$

$$\Delta E = +4.6614 - 0.1241\,E + 0.000834\,E^2 + 0.0089\,H$$

Coefficients are read from JSON written by `07_sq3_growth.py` and `08_sq3b_life_expectancy.py` rather than refitted here, so the figure cannot silently diverge from the fits reported above.

**No fixed point.** $\Delta H = 0$ traces a rising curve across the plane — the stable branch of the happiness nullcline — but $\Delta E$ has no zero anywhere in range — its minimum over the observed span is about +0.09 years per year, at $E \approx 74$ — so healthy life expectancy never stops rising and the arrows always drift rightward. The best numerical residual was 0.105, at $E$ = 72.9, $H$ = 6.92, which is not a solution.

That absence is itself informative, and it is a property of the source rather than of the world: a monotonically interpolated series cannot stop rising. It is the same defect described in the second model, seen from a different angle.

**The nullcline is not a curve of stasis.** A state sitting on it is only momentarily stationary in happiness. Because $\Delta E > 0$ the state moves rightward, and because the curve rises with $E$ it is then below the curve, so happiness resumes climbing. Trajectories are attracted to the nullcline *vertically* and then slide along it, with the sliding driven entirely by the change in healthy life expectancy — the component resting on an interpolated series.

**What is trustworthy.** The vertical flow is the result; the horizontal flow is largely an artefact.

- Vertical movement is the change in happiness — a survey measure, 96% of whose variance is within countries.
- Horizontal movement is the change in healthy life expectancy, which the source interpolates: 151 distinct values across 1,872 country-years, 83% of variance between countries.

The consequence for the trajectories is direct: their vertical path carries meaning, their horizontal path carries the interpolation. They illustrate the fitted system; they are not a forecast.

**On reading the arrow angles.** Components are plotted in data units, so the angle on the page reflects movement as a fraction of each plotted axis — the direction a country moves *on this figure*. The axes carry different units, so the angle is not a ratio of years to ladder points. Arrows are drawn only over grid points within 2.6 years and 0.65 ladder points of an observation, because the quadratics extrapolate steeply outside the data.

![phase_portrait](Code/outputs/figures/phase_portrait.png)

<small><b>Figure 4</b> (as in the report)<b>.</b> Arrows magnified twice; the magnification is set automatically so a typical arrow spans about 4% of the vertical axis.</small>

#### What this does and does not establish

- **Still association, not cause.** The level of healthy life expectancy is measured before the change in happiness, but that does not establish that health caused the change: a country's health and its wellbeing are both shaped by things this data does not contain, and the interpolation means the recorded level is calculated partly from later observations.
- **$E_t$ is a level, not a change.** The revision to this sub-question avoided differencing healthy life expectancy, which is interpolated by the source. The level is still partly model output, but the estimate does not depend on year-to-year movement in $E$ being real.
- **Pooled dynamics.** All countries are assumed to share the same growth relationship. Country fixed effects would test that but require a dynamic panel estimator.
- The equilibrium is an implication of a fitted model over a 16-year window, not an observed destination. No country was seen to settle anywhere.
- **Not a Granger-causality test, though it has the form of one.** The pair of models asks, in each direction, whether one variable's past improves prediction of the other beyond that variable's own past (Granger, 1969). Two things prevent that reading. The recorded value of healthy life expectancy for a year is calculated partly from observations in later years, so the predictor is not purely a past quantity — and filtering a series before testing it can produce apparent causality absent from the underlying process, shown for the analogous case of temporal aggregation by Breitung and Swanson (2002). In the reverse direction the outcome is nearly determined by its own past, leaving almost nothing for happiness to explain.
- **A stricter test is recoverable from this file, and was not attempted.** Interpolation between two observations produces a constant annual increment, so the increment changes only at an observed year: Haiti's run of +5.32 followed by +0.30 locates one. Detecting those break points per country would identify the years the WHO series was actually observed, and restricting the analysis to spans between them would give measured rather than constructed changes — at the cost of far fewer observations, irregularly spaced. A source publishing annual estimates would serve better.

## Analysis Log

| Step | What was done | Outcome |
| --- | --- | --- |
| 1 | Downloaded `WHR26_Data_Figure_2.1.xlsx` (Helliwell, Layard, et al., 2026), the only panel on the WHR data-sharing page, concluding it was the only machine-readable option. That conclusion was wrong — see step 4. Provenance and checksum recorded. | Superseded by step 4. |
| 2 | Confirmed the six factor columns, the residual and both whiskers were entirely absent before 2019 in that file (0 non-null in 1,094 rows). Restricted it to 2019–2025. | Superseded by step 4. |
| 3 | Established that the `Explained by:` columns are **modelled contributions in ladder points**, not measurements: each is a regression coefficient times a distance from a baseline. No dollars, years or proportions anywhere in that file, and the raw values cannot be recovered from it without coefficients WHR does not publish. | Units documented from the WHR 2026 statistical appendix (Helliwell, Aknin, et al., 2026). |
| 4 | Searched for the raw panel in natural units. WHR stopped publishing it after the 2024 edition; recovered `DataForTable2.1.xls` from an Internet Archive snapshot. **Switched the analysis to this file and dropped the Figure 2.1 workbook.** Trade-off accepted: loses 2024–2025, gains 2005–2023 annual rather than overlapping observations, real units, and two extra variables (positive and negative affect). | `Attachments/DataForTable2.1.xls`; see [Data Summary](#data-summary). |
| 5 | Described the new file and range-checked every column. Found Haiti's healthy life expectancy corrupted for 2006–2012 and Venezuelan GDP implausible. Neither altered. | [Known defects in the source](#known-defects-in-the-source). |

| 6 | Assessed coverage year by year. 2005 is unusable (27 countries, 1 complete row) and 2006 is the weakest usable year (89 countries, 83%). **Scoped to 2007–2023**: 17 consecutive years, 164 countries, 2,247 rows, 86–93% complete throughout. Added a derived dollar column so GDP is readable. | `Code/outputs/whr_2007_2023.csv`; see [Scope decision](#scope-decision-20072023). |
| 7 | Characterised the missingness. It is concentrated by country, and for `Perceptions of corruption` is plausibly caused by the subject itself — the questions were not asked in several Gulf states, China and Turkmenistan. Four countries have no corruption observation at all. **Decided: unbalanced panel, no imputation.** | [Missing-data and panel decisions](#missing-data-and-panel-decisions). |

| 8 | Applied the cleaning rules. Haiti's four corrupted healthy-life-expectancy values and Venezuela's entire GDP series set to missing. Accepted 2023's partly-forecast GDP as-is. | `Code/outputs/whr_clean.csv`; see [Cleaning decisions](#cleaning-decisions). |

| 9 | **Step 2.** Framed the research question with the user, before computing anything: does higher healthy life expectancy accompany higher happiness across countries? Recorded as descriptive rather than causal, with four sub-questions and what would count as an answer to each. Noted that the file holds healthy life expectancy, not life expectancy. | [Research Question](#research-question). |

| 10 | **Step 3, sub-question 1.** Built the agreed cross-section — one row per country at its most recent year with both variables — and plotted happiness against healthy life expectancy. No line fitted, no statistic computed. Recorded that the cross-section mixes years: 135 countries contribute 2023, 25 contribute earlier years back to 2007. | [Sub-question 1](#sub-question-1-across-countries-is-higher-healthy-life-expectancy-associated-with-higher-life-ladder-scores). |
| 11 | Kept all 160 countries rather than restricting to a 2023 snapshot, since the 25 with older observations are not a random selection. | [Cross-section](#cross-section). |
| 12 | **Step 4, sub-question 1.** OLS with robust standard errors, plus rank correlation and influence checks. **+1.47 ladder points per decade** (95% CI +1.26 to +1.68), R² = 0.586. Added the fitted line to the figure and the finding to `Report.md`. | [Step 4: the fit](#step-4-the-fit). |

| 13 | **Sub-question 2.** On the 152 countries with income too, the healthy-life-expectancy slope falls from +1.42 to **+0.59 per decade** (95% CI +0.18 to +1.00) once log GDP is added — 42% surviving, interval excluding zero. The two predictors correlate at r = 0.835, so the split between them is not a sharp apportionment. | [Sub-question 2](#sub-question-2-does-the-association-survive-accounting-for-income). |

| 14 | Checked whether the two-stage route to controlling for income differs from the one-step multiple regression. It does not — the coefficients agree to 7.6 × 10⁻¹⁷ — but residualising *only* the outcome does differ, returning +0.178 with an interval spanning zero. Recorded so the distinction is not lost. | [Is the two-stage route different?](#is-the-two-stage-route-different). |
| 15 | Wrote `Methods` for both answered sub-questions, mirroring the `Results` sub-headings. | `Report.md` `Methods`. |
| 16 | **Dropped sub-question 4** (uniformity of the relationship), by the user's decision and without testing it, on the view that a straight line describes the data well enough. Marked as dropped here, with the point recorded that this is not evidence the relationship is uniform. An earlier version of this entry mistakenly dropped sub-question 3; corrected. | [Research Question](#research-question). |

| 17 | **Sub-question 3**, revised as a growth model, first with healthy life expectancy multiplied by the ladder level. Superseded at step 19. | [Sub-question 3](#sub-question-3-the-growth-of-happiness). |

| 18 | Compared two orientations of the growth figure and kept the one with healthy life expectancy on the horizontal axis. **Superseded at entry 25.** | `Report.md` Figure 2. |
| 19 | **Refitted sub-question 3 with healthy life expectancy entering additively** rather than multiplied by the ladder level, the interaction having been specified in error. $a_2$ = **+0.0161** ladder points of annual growth per year of healthy life expectancy (95% CI +0.0117 to +0.0204), and $H$ is now well identified (VIF 2.1 against 20.0). Implied long-run response at the median: **+1.29 per decade**, against +1.47 across countries. | [Sub-question 3](#sub-question-3-the-growth-of-happiness). |

| 20 | **Sub-question 3, reverse direction.** Fitted $\Delta E = k + a_1 E + a_2 E^2 + a_3 H$ to test whether happiness predicts health gains. **Null: $a_3$ = +0.009, 95% CI −0.022 to +0.039.** Established first that $\Delta E$ is largely not a measurement — 151 distinct values across 1,872 country-years, 83% of its variance between countries — so the null is uninformative rather than reassuring. | [Second model: the reverse direction](#second-model-the-reverse-direction). |
| 21 | Drew the two growth models as a single dynamical system, after Ranganathan et al. (2014). Happiness is attracted vertically to the stable branch of its nullcline, then slides along it as healthy life expectancy rises; the system has **no fixed point**, because the fitted $\Delta E$ never reaches zero — a property of the interpolated series. | [Phase portrait](#phase-portrait-the-two-models-as-one-system). |

| 22 | Corrected the phase portrait's labelling. The $\Delta H = 0$ curve had been called "happiness unchanging", which is wrong while $\Delta E > 0$: a state on it is only momentarily stationary and then slides rightward. Relabelled as the **stable branch of the $H$-nullcline**, and made explicit that sub-question 3's equilibrium is an equilibrium of the happiness equation at fixed $E$, not of the two-variable system. | [Phase portrait](#phase-portrait-the-two-models-as-one-system). |

| 23 | **Step 5.** Wrote the `Discussion` as three paragraphs organised by theme rather than by sub-question: the cross-sectional relationship and its survival of income adjustment; what the growth model does and does not license about direction, with the interpolation limitation beside it; and what the dynamics still support given that limitation. Every figure quoted was checked against the generated outputs. No new analysis. | `Report.md` `Discussion`. |
| 24 | **Extended the Haiti cleaning rule to 2013 and 2014**, at the user's direction. The original rule blanked only healthy-life-expectancy values below 40 years, which left 43.96 (2013) and 49.28 (2014) in place even though the exact +5.32 annual increment shows them to be the same constructed ramp. Refitted sub-question 3 on the reduced sample: 1,874 pairs to 1,872, $a_2$ +0.01607 to +0.01575, implied long-run response +1.30 to +1.29 per decade, and the between-country share of $\Delta E$ variance 68% to 83%. No sub-question 1 or 2 result moved, Haiti's latest year being 2018. | [Cleaning decisions](#cleaning-decisions); `Code/outputs/sq3_growth.md` |
| 25 | **Reversed the growth figure's orientation**, at the user's direction while rewriting: happiness on the horizontal axis, with contours at the 10th, 50th and 90th percentile of healthy life expectancy (54, 65 and 71 years). This is the form that shows the growth curve sloping down across the observed range, which is the claim the paragraph makes. No refit — `07_sq3_growth.py` already produced both variants. Supersedes entry 18; the rejected orientation is kept as Figure A3. | `Report.md` Figure 2; [The alternative orientation](#the-alternative-orientation) |
| 26 | **Checked the user's own write-up of the discussion and corrected eleven things.** Four changed meaning: the direction of motion around the resting point was inverted (happiness rises *below* it, not above); the resting points were 4.3/5.5/6.3 at 54/65/72 years rather than 4.40/5.57/6.50 at 54/65.2/71.1; the 96%-within-country figure was cited as evidence that the fit is noisy, when it is what makes the change in happiness a usable outcome and R² = 0.07 is the noise figure; and "resting point depends on age" conflated age with healthy life expectancy. The hedge "all but the happiest countries" was replaced by the count — 79 of 151 sit below their resting point, 72 above, Denmark (7.54 vs 6.55) and Finland (7.73 vs 6.52) among the latter. Remainder were typos and two dangling verbs. All corrected values re-derived from the coefficients rather than read off the generated tables. | `Report.md` Discussion |
| 27 | **Removed the marker for the dropped fourth sub-question from the report's introduction**, under the framework rule that work not done leaves no trace in `Report.md`. The record stays here: the question itself at [Research Question](#research-question), the decision at entry 16. Also corrected +0.89 and +2.06 to +0.88 and +2.02 in the prose beside the equilibrium table, which the step 32 refit had updated in the table but not in the sentence citing it. | `Report.md` Introduction; `Appendix.md` |
| 28 | **Dropped Figure 2 (the added-variable plot) from the report and renumbered the rest**, at the user's direction; the script and the PNG stay, and the plot is kept here as Figure A2 because the two-stage equivalence refers to it. Report figures are now 1–4. Appendix figures renumbered A1–A3 to run in document order. **Also caught a paragraph left stale by entry 25**: the how-to-read text beside the growth figure still described the old orientation — upward-sloping parallel lines, contours by happiness, zero crossings on the life-expectancy axis — every claim of which the reorientation had falsified. Rewritten and each claim checked against the fitted model. Fixed the same error at [Where growth stops](#where-growth-stops), whose "zero crossings visible in Figure 3" now points to Figure A3, the only figure with $E$ on the horizontal axis. | `Report.md`; `Appendix.md` |
| 29 | **Tied every point label to its point.** At the enlarged type sizes the labels floated free of the data, so it was not clear which country each named, and two ran outside the axes. Each labelled point is now ringed and joined to its label by a leader line; labels are thrown into the empty corner nearest their own extreme so no two compete for the same space, and flip inward when the point sits within 12% of the top or bottom of the axes. Factored into `viz_style.label_extremes()` and `pick_extremes()`, so Figures 1, A1 and A2 share one implementation. Required moving `set_ylim` ahead of labelling in `05_sq1_regression.py`, since the helper reads the final axis limits. | `Code/viz_style.py`; Figures 1, A1, A2 |
| 30 | **Completed the introduction's account of the approach**, at the user's direction, naming the two frames the report actually uses: Granger causality (Granger, 1969) for the question of whether a change in one variable follows the level of the other, and the dynamical-system representation of Ranganathan et al. (2014) for the phase portrait. Both were already cited in the methods and discussion but not in the introduction, so the report described its approach only after applying it. **The forward pointer to the interpolation limit was then removed at the user's direction**, on the ground that an introduction should not anticipate its conclusions: it says what will be done, not what will be found. The limitation is stated in the methods, where the second model is introduced, and again in the discussion. | `Report.md` Introduction |
| 31 | **Wrote the background paragraph of the `Introduction`** (step 6), replacing the placeholder. One paragraph, five references, each verified through the Crossref API for bibliographic detail. Initially written from abstracts; the four load-bearing sources were then obtained in full and read (see entry 32), which changed the paragraph. The framing rests on Deaton (2008), who examined the same survey against objective health measures and found life evaluations did not respond strongly to life expectancy — which is what makes the first sub-question an open one rather than a formality. Chose the references for their relevance to what the analysis found, and wrote the text without stating any of it. | `Report.md` Introduction |
| 32 | **Read the four background sources in full and corrected the paragraph.** The user downloaded them; they are in `Attachments/literature/`, which is gitignored as licensed material. The correction that mattered was Deaton (2008): the abstract says only that life evaluations do not respond strongly to objective health measures, but the article is more specific — the *level* of life expectancy "does not show up significantly in any of the regressions" while the change in it does, at 0.044 ladder points per year, "no matter whether life expectancy is high or low". That distinction between levels and changes is the one this analysis is built on, and it was reached here independently. It also removes the need to cite the NBER working paper, since the published version carries the result. Steptoe (2019) supplied a stronger statement than expected — observational studies "can never convincingly establish causality, even when multiple covariates are taken into account" — now reflected in the paragraph. Diener and Chan (2011) claim causal influence explicitly, so "contributes to" is their own framing and not a softening. **Also moved the background to the opening position** and removed the sentence describing what the report examines. | `Report.md` Introduction; `Attachments/literature/` |
| 33 | **Wrote the `Abstract`** (step 6), to the order the user specified: the field, the narrowing question, the questions and method, the results, then limitations and what would settle them. Rewritten the same day to carry no numbers at all: direction and rough size in words, with the estimates, intervals and sample sizes left to `Results`. No citations, no figure references. Note that it does **not** report $a_2$, the coefficient on healthy life expectancy in the growth model, because the user removed that estimate and its interval from `Results` — that gap is now moot, since the abstract reports no coefficients either way. This completes step 6 and the report. | `Report.md` Abstract |
| 34 | **Replaced the abstract with the user's rewrite**, 268 words to 153. Their edit cut the method-plumbing sentence and the statistical detail, and marked the reference to earlier work `[which!]`. Resolving that turned up two errors of attribution in the sentence, both corrected and both reported: the work is Deaton (2008) on the **Gallup World Poll**, not on the World Happiness Report 2024, which did not exist then; and what he found was that *changes in life expectancy* raise the *level* of life satisfaction, not that life expectancy explains *changes in happiness* — the latter being this report's own question, and the reverse pairing of outcome and predictor. | `Report.md` Abstract |
| 35 | **Verified the Deaton claim against the paper.** Every clause of the abstract sentence holds. The survey is the 2006 Gallup World Poll and the measure is the same 0–10 "worst to best possible life" ladder the WHR panel uses. The level result is near-verbatim — "conditional on income, longer life expectancy has no apparent effect on life satisfaction" — and Table 2 gives −0.011 (SE 0.012), t = −0.92. The change result is +0.044 (SE 0.016), t = +2.75. Our wording keeps plain "life expectancy" for Deaton and "healthy life expectancy" for this analysis, which is the right distinction: his measure is period life expectancy from survival rates, not HALE. **One correction followed.** The background had said changes mattered "whether the level was high or low", quoting Deaton's discussion. His table splits by income rather than by life expectancy, and above $12,000 the coefficient is −0.062 (SE 0.076), t = −0.82 — the effect is concentrated in poorer countries. Clause removed; the abstract's weaker "did appear to raise them" needed no change. | `Report.md` Abstract, Introduction |
| 36 | **Restructured the abstract to the revised order**: limitations now sit with the result they qualify at sentence 6, and sentence 7 is a closing summary. Two changes followed. The dynamical-systems sentence had been last, where it read as a method statement in the summary position, so it moved up to the method slot. And a closing sentence was added, checked against the discussion so that it claims no more — health and happiness travel together, the sequence is consistent with health leading, and that is not established. | `Report.md` Abstract |
| 37 | **Step 7 read-through and reference check.** All 13 `Report.md` references verified against Crossref: authors, journal, volume, issue, pages and year match for every DOI-bearing entry. All 18 reference URLs across both documents resolve — six return 403 to a scripted request but redirect to the correct publisher article page, which was confirmed individually. Every `Report.md` reference is cited and every citation is listed. **Three defects found in `Appendix.md`**, two fixed here: the reference list was out of order, with Granger before Feenstra; and the provenance table cited the WHR 2024 report inline as `(2024)` while the list letters it `(2024a)`. The third is left for the user: `Helliwell et al. (2026a)`, the WHR 2026 report, is listed but never cited, and the `2026a`/`2026b` pair carries letters despite having different author lists. | `Appendix.md` References |
| 38 | **Step 7 read-through, structural checks.** Each sub-question is asked in the `Introduction`, described in `Methods`, answered in `Results` and drawn on in `Discussion`. No orphans: four figures, all defined and all referred to; no empty headings; no reference uncited in `Report.md`. Every number in the report traced to the generated output, the four that did not match directly being roundings (5.6 from 5.57, 0.009 from 0.008896, −0.022 from −0.021614) and the sub-question 1 sample size. `Discussion` introduces no number absent from `Results`. Wrote the `Appendix` section the user added to `Report.md`, linking `Appendix.md`, `Code/` and `Setup.md`, and restored the blank line before `## References`. | `Report.md` |
| 39 | **Corrected the title typo and the reference defects.** Title: "and a country level" to "at a country level", and the trailing full stop dropped. `Helliwell et al. (2026a)` was listed but never cited: the WHR 2026 report is now cited where its workbook is described, at log entry 1. The `2026a`/`2026b` letters are gone, since the two works have different author lists — they are disambiguated by name, as the 2024 chapter already was; the `2024a`/`2024b` pair keeps its letters because those two share an author list. Cantril (1965) was the one reference with no link and the one work cited without being opened: bibliographic details verified against OpenLibrary (Hadley Cantril, 1965, Rutgers University Press) and an Internet Archive record now linked, but the copy is lending-only and search-inside was unreachable, so the ladder's wording continues to rest on the WHR statistical appendix, which was read. All 13 report and 12 appendix references now carry a resolving link, both lists are in order, and `References` is the last section of each. | `Report.md`; `Appendix.md` |
| 40 | **Removed the forward references to the untested fourth sub-question.** Four passages pointed at it as the place a question would be settled — "should be tested there", "is sub-question 4", "that is sub-question 4" — when it was dropped before being asked. Each now states what is unresolved without naming a destination that does not exist: the spread observation is attributed to the robust standard errors it justifies, and the two shape notes say the shape was not tested. The convexity observation beside the equilibrium table keeps its substance, since it is a real implication of the fitted model, but no longer treats the dropped question as live. The record itself is untouched — the question is still listed as dropped under [Research Question](#research-question), and entry 16 still carries the decision and its reasoning. | `Appendix.md` |
| 41 | **Restored the uncertainty on the growth model's coefficient in `Results`.** "The curve sits higher where healthy life expectancy is greater" had been the only quantitative claim in the report with no interval behind it, the estimate having been cut in an earlier writing pass. It now reads: each additional year is associated with +0.016 ladder points of annual growth, 95% CI +0.011 to +0.020. This matters because the joint test that had been carrying the paragraph tests all three terms together and so does not isolate healthy life expectancy. Values checked against both the generated table and the exported coefficients. | `Report.md` Results |
| 42 | **Finalised the folder.** The two documents moved to `Sample Report/` with their own `Code/` and `Attachments/`, and the root `Report.md` and `Appendix.md` became empty templates carrying the same headings. Verified the sample still regenerates from its new location, byte for byte. That run exposed a miss from entry 40: the dangling references to the untested fourth sub-question had been corrected in this document but not in `04_sq1_scatter.py` and `05_sq1_regression.py`, which generate them — so the linked output still carried the old wording. Scripts corrected and outputs regenerated. The same failure as ever: the prose was fixed and the thing that produces it was not. | `Sample Report/Code/` |

*Step 5 complete. Next: step 6 — the `Abstract`, and the background for the `Introduction`.*
| 43 | **Added the `Disclaimer` section** between `Discussion` and `Appendix`, stating that the report was written with the help of agentic AI at every stage. It is standing text in the report template rather than something a step fills in, so any analysis started from this folder carries it from the outset. Also **reordered this log**: entries 20 and 21, and 41 and 42, had been written out of sequence by insertions that keyed off the wrong marker row. | `Report.md`; this log |
| 44 | **Exported the report to Word** (step 8), to `Code/outputs/Happiness.docx` with pandoc 3.10.2. Verified rather than assumed: four figures embedded, and every non-ASCII character in the source present in the output, checked one by one against `word/document.xml`. Captions arrive at body size and weight — the paragraph is there and the `<small>` and `<b>` tags are gone, with no bold run and no size override — so a legend no longer reads as one. No PDF: that needs a LaTeX engine, and its default font drops `ρ` and `⁻` without failing. | `Sample Report/Code/outputs/Happiness.docx` |

## Code Summary

A guide to the analysis code: what each file does, how to run it, and any logic worth reading on its own. Installing the environment is covered in [Setup.md](../Setup.md).

### Project Structure

| Path | Role |
| --- | --- |
| `Attachments/DataForTable2.1.xls` | The source file. Never modified. |
| `Attachments/SOURCE.md` | Where it came from, its units, and its checksum. |
| `Code/01_describe_data.py` | Describes the source file as delivered. |
| `Code/02_select_scope.py` | Applies the 2007–2023 scope, adds the derived dollar column, writes the working dataset. |
| `Code/03_clean.py` | Sets known-wrong values to missing. Writes the analysis dataset. |
| `Code/04_sq1_scatter.py` | Sub-question 1, step 3: builds and documents the latest-year cross-section. |
| `Code/05_sq1_regression.py` | Sub-question 1, step 4: fits the association, runs diagnostics, draws the figure. |
| `Code/06_sq2_income.py` | Sub-question 2: nested fits with income, collinearity diagnostics, two figures. |
| `Code/07_sq3_growth.py` | Sub-question 3: builds consecutive-year pairs, fits the growth model, draws Figure 2. |
| `Code/08_sq3b_life_expectancy.py` | Sub-question 3, reverse direction: tests whether happiness predicts health gains. Draws Figure 3. |
| `Code/09_phase_portrait.py` | Draws the two models as one dynamical system. Reads their exported coefficients. Draws Figure 4. |
| `Code/viz_style.py` | Shared chart styling: palette, ink, mark geometry, light and dark themes. |
| `Code/palette_validation.txt` | Recorded output of the chart-palette accessibility validator. Not regenerated by the pipeline. |
| `Code/outputs/data_summary.md` | Generated description of the source file. |
| `Code/outputs/scope.md` | What the scope keeps and costs, and the balanced-panel options. |
| `Code/outputs/whr_2007_2023.csv` | The scoped dataset, before cleaning. |
| `Code/outputs/cleaning.md` | Every cleaning rule, its reason, and the rows it touched. |
| `Code/outputs/whr_clean.csv` | **The analysis dataset.** Later steps read this. |
| `Code/outputs/latest_by_country.csv` | Sub-question 1 cross-section: one row per country, most recent year. |
| `Code/outputs/sq1_scatter.md` | What that cross-section is, and the scatter. |
| `Code/outputs/figures/` | Figures, light theme; `figures/dark/` holds the dark-theme versions. |

Everything under `Code/outputs/` is generated and safe to delete and rebuild.

### Key Scripts and Notebooks

#### `01_describe_data.py`

- **What it does** — reports what is in the file: structure, columns with their units, coverage by year, completeness, and any value outside a plausible range. Draws no conclusions and tests nothing.
- **How to run it** — `cd Code && uv run python 01_describe_data.py`
- **What it reads** — `Attachments/DataForTable2.1.xls`
- **What it produces** — `Code/outputs/data_summary.md`, and the same text on stdout.
- **Parameters** —
  - `EXPECTED_SHA256`: the checksum recorded at retrieval. The script reports whether the file still matches, so a swapped or re-downloaded file is visible rather than assumed.
  - `UNITS`: the unit of each column, transcribed from the WHR 2024 statistical appendix, so the generated summary states units rather than leaving a reader to infer them from column names.
  - `PLAUSIBLE`: the range each column should fall in. Values outside are reported, never altered. `Healthy life expectancy` is bounded at 40–90 years, which is what surfaces the corrupted Haiti rows.

Its output is summarised in [Data Summary](#data-summary).

#### `02_select_scope.py`

- **What it does** — keeps 2007–2023, adds `GDP per capita (PPP 2017 int$)` as `exp(Log GDP per capita)`, writes the working dataset, and reports what the scope keeps, what it costs, and the balanced-panel trade-off. Selects and derives only: nothing cleaned or imputed, published column names untouched.
- **How to run it** — `cd Code && uv run python 02_select_scope.py`
- **What it reads** — `Attachments/DataForTable2.1.xls`
- **What it produces** — `Code/outputs/whr_2007_2023.csv` and `Code/outputs/scope.md`
- **Parameters** — `FIRST_YEAR`/`LAST_YEAR` set the window; `KEY` lists the five variables the balanced-panel report treats as essential. Change either and re-run; every figure in `scope.md` is derived, so the report follows.

Reasoning recorded in [Scope decision](#scope-decision-20072023).

#### `04_sq1_scatter.py`

- **What it does** — builds the sub-question 1 cross-section (one row per country, its most recent year with both variables) and plots happiness against healthy life expectancy. Reports how many countries contribute which year, since "most recent available" is not one date.
- **How to run it** — `cd Code && uv run python 04_sq1_scatter.py`
- **What it reads** — `Code/outputs/whr_clean.csv`
- **What it produces** — `Code/outputs/latest_by_country.csv`, `Code/outputs/sq1_scatter.md`, and `sq1_scatter.png` in both themes
- **Deliberately absent** — no statistics and no figure. It defines and documents the data; `05` fits and draws.

#### `05_sq1_regression.py`

- **What it does** — fits OLS of life ladder on healthy life expectancy across the cross-section, with HC3 robust standard errors; reports the slope per decade with its interval, R², Spearman's ρ, and influence diagnostics; and draws the figure with the fitted line.
- **How to run it** — `cd Code && uv run python 05_sq1_regression.py`
- **What it reads** — `Code/outputs/latest_by_country.csv`
- **What it produces** — `Code/outputs/sq1_regression.md` and `sq1_scatter.png` in both themes
- **Parameters** — none to set. Influence is checked against three fixed reduced samples (excluding the lowest-ladder country, excluding healthy life expectancy under 50, excluding the pre-2023 observations) rather than against samples chosen after seeing the result.

#### `03_clean.py`

- **What it does** — sets values known to be wrong to missing. Each rule is declared in a `RULES` list with the country, columns, years, a reason and the date it was decided, and the generated report states exactly which rows it touched. Imputes nothing.
- **How to run it** — `cd Code && uv run python 03_clean.py`
- **What it reads** — `Code/outputs/whr_2007_2023.csv`
- **What it produces** — `Code/outputs/whr_clean.csv` and `Code/outputs/cleaning.md`
- **Parameters** — the `RULES` list. Adding a rule is the only way to change what gets blanked, so the diff of this file is the history of every cleaning decision. A rule matching no rows reports that fact rather than passing silently.

Reasoning recorded in [Cleaning decisions](#cleaning-decisions).

### Reproducible Workflow

Assumes the environment is already built — see [Setup.md](../Setup.md).

```bash
cd Code
uv run python 01_describe_data.py    # what the source file contains
uv run python 02_select_scope.py     # -> outputs/whr_2007_2023.csv
uv run python 03_clean.py            # -> outputs/whr_clean.csv
uv run python 04_sq1_scatter.py      # -> outputs/latest_by_country.csv
uv run python 05_sq1_regression.py   # -> outputs/sq1_regression.md + Figure 1
uv run python 06_sq2_income.py       # -> outputs/sq2_income.md + Figures A1, A2
uv run python 07_sq3_growth.py       # -> outputs/sq3_growth.md + Figure 2, A3
uv run python 08_sq3b_life_expectancy.py   # -> outputs/sq3b_life_expectancy.md + Figure 3
uv run python 09_phase_portrait.py   # -> outputs/phase_portrait.md + Figure 4
```

**Export (step 8).** Run from `Sample Report/`, so the figure paths inside the document resolve:

```bash
pandoc Happiness.md --from markdown --toc -o Code/outputs/Happiness.docx
```

Produced with pandoc 3.10.2. All four figures embed and every non-ASCII character in the source survives, including the superscript minus in `p = 1 × 10⁻¹³`. Figure captions lose their `<small>` and `<b>` styling and arrive at body size, since neither tag has an equivalent that survives the conversion. No PDF was produced: that needs a LaTeX engine, whose default font drops `ρ` and `⁻` silently.

`01` and `02` read the source file directly and are independent. `03` reads `02`'s output and `04` reads `03`'s, so they must run in order. A second or so each, and deterministic: no sampling, no randomness.

### Important Snippets

*Nothing yet worth excerpting — the one script so far is short enough to read whole.*

## References

Breitung, J., & Swanson, N. R. (2002). Temporal aggregation and spurious instantaneous causality in multiple time series models. *Journal of Time Series Analysis*, 23(6), 651–665. [https://doi.org/10.1111/1467-9892.00284](https://doi.org/10.1111/1467-9892.00284)

Cantril, H. (1965). *The Pattern of Human Concerns*. New Brunswick, NJ: Rutgers University Press. [https://archive.org/details/patternofhumanco0000cant](https://archive.org/details/patternofhumanco0000cant)

Feenstra, R. C., Inklaar, R., & Timmer, M. P. (2015). The next generation of the Penn World Table. *American Economic Review*, 105(10), 3150–3182. [https://doi.org/10.1257/aer.20130954](https://doi.org/10.1257/aer.20130954). Database: [Penn World Table](https://www.rug.nl/ggdc/productivity/pwt/)

Gallup. (n.d.). *Gallup World Poll*. [https://www.gallup.com/analytics/318875/global-research.aspx](https://www.gallup.com/analytics/318875/global-research.aspx)

Granger, C. W. J. (1969). Investigating causal relations by econometric models and cross-spectral methods. *Econometrica*, 37(3), 424–438. [https://doi.org/10.2307/1912791](https://doi.org/10.2307/1912791)

Helliwell, J. F., Layard, R., Sachs, J. D., De Neve, J.-E., Aknin, L. B., & Wang, S. (Eds.). (2024a). *World Happiness Report 2024*. University of Oxford: Wellbeing Research Centre. [https://www.worldhappiness.report/ed/2024/](https://www.worldhappiness.report/ed/2024/)

Helliwell, J. F., Layard, R., Sachs, J. D., De Neve, J.-E., Aknin, L. B., & Wang, S. (Eds.). (2024b). *Statistical appendix for Chapter 2*. In *World Happiness Report 2024*. University of Oxford: Wellbeing Research Centre. [https://files.worldhappiness.report/WHR24_Statistical_Appendix.pdf](https://files.worldhappiness.report/WHR24_Statistical_Appendix.pdf)

Helliwell, J. F., Layard, R., Sachs, J. D., De Neve, J.-E., Aknin, L. B., & Wang, S. (Eds.). (2026). *World Happiness Report 2026*. University of Oxford: Wellbeing Research Centre. [https://www.worldhappiness.report/ed/2026/](https://www.worldhappiness.report/ed/2026/)

Helliwell, J. F., Aknin, L. B., Huang, H., Rojas, M., Wang, S., Guerra, V., & Danyluk, A. (2026). *Statistical appendix for Chapter 2*. In *World Happiness Report 2026*. University of Oxford: Wellbeing Research Centre. [https://files.worldhappiness.report/WHR26_Statistical_Appendix.pdf](https://files.worldhappiness.report/WHR26_Statistical_Appendix.pdf)

Ranganathan, S., Spaiser, V., Mann, R. P., & Sumpter, D. J. T. (2014). Bayesian dynamical systems modelling in the social sciences. *PLoS ONE*, 9(1), e86468. [https://doi.org/10.1371/journal.pone.0086468](https://doi.org/10.1371/journal.pone.0086468)

World Bank. (n.d.). *World Development Indicators*. [https://databank.worldbank.org/source/world-development-indicators](https://databank.worldbank.org/source/world-development-indicators)

World Health Organization. (n.d.). *Global Health Observatory*. [https://www.who.int/data/gho](https://www.who.int/data/gho)
