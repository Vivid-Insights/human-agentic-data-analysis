# Appendix

*The running record. Filled from the first step, not at the end. Everything that does not belong in the report belongs here: the workings, the diagnostics, the decisions and what each one cost.*

## Data Summary

The analysis uses one dataset, `Code/outputs/analysis_dataset.csv`: 135 countries, one row each, covering 2001–2024. It is built by `Code/07_build_analysis_dataset.py` from four source files in `Attachments/`, and every later script reads it rather than the sources, so the sample is defined in exactly one place.

### The analysis dataset

| Column | Unit | What it is |
| --- | --- | --- |
| `iso3` | ISO 3166-1 alpha-3 | Country identifier |
| `country` | — | Country name, from World Bank metadata |
| `income_group` | Four categories | World Bank income classification, **current vintage, not the classification during the period**. Used only to select the eight cases for sub-question 3. |
| `extent_2000_ha` | Hectares | Tree cover in 2000 at ≥30 percent canopy density. The denominator for both outcomes. |
| `permanent_loss_ha` | Hectares | Loss 2001–2024 attributed to permanent agriculture, hard commodities, or settlements and infrastructure |
| `shifting_loss_ha` | Hectares | Loss 2001–2024 attributed to shifting cultivation. Held for the sensitivity check only. |
| `total_loss_ha` | Hectares | Loss 2001–2024, all eight driver classes |
| `permanent_loss_share` | Proportion | `permanent_loss_ha / extent_2000_ha`. **Outcome for sub-question 1.** |
| `total_loss_share` | Proportion | `total_loss_ha / extent_2000_ha`. **Outcome for sub-question 2.** |
| `permanent_plus_shifting_share` | Proportion | Outcome for the sensitivity check on sub-question 1 |
| `gdp_pc_mean` | Constant 2021 international $, PPP | Arithmetic mean of GDP per capita over 2001–2024. **Predictor for both sub-questions.** |
| `gdp_pc_geomean` | Same | Geometric mean, held as a robustness check |
| `log_gdp_pc_mean` | Natural log | `log(gdp_pc_mean)` |
| `gdp_years_used` | Count | Years of GDP data behind the mean, out of 24 |

### Sample rule

A country enters if it has at least 100,000 ha of tree cover in 2000, is a non-aggregate country in the World Bank metadata, and has at least one GDP observation in 2001–2024. Of the 183 countries meeting the last two conditions, 135 clear the forest floor.

| Income group | Countries |
| --- | --- |
| Low income | 15 |
| Lower middle income | 36 |
| Upper middle income | 40 |
| High income | 44 |

### The variables as built

| Variable | Min | Median | Mean | Max |
| --- | --- | --- | --- | --- |
| `permanent_loss_share` | 0.0007 | 0.0134 | 0.0485 | 0.3198 |
| `total_loss_share` | 0.0024 | 0.1057 | 0.1254 | 0.5442 |
| `permanent_plus_shifting_share` | 0.0007 | 0.0213 | 0.0647 | 0.3857 |
| `gdp_pc_mean` | 1,013 | 13,263 | 21,546 | 129,432 |
| `log_gdp_pc_mean` | 6.921 | 9.493 | 9.435 | 11.771 |

Integrity checks, all run by the build script: no share falls outside [0, 1]; permanent loss never exceeds total loss; no missing value in any column used; one country has fewer than 24 years of GDP behind its mean. The arithmetic and geometric means of income rank countries at Spearman 0.999629 and differ by at most 19.4 percent, so the choice between them is immaterial.

### Provenance

| File | Source | Retrieved | SHA-256 |
| --- | --- | --- | --- |
| `gfw_tree_cover_loss_by_driver.csv` | Global Forest Watch Data API, `gadm__tcl__iso_change`, version `v20260424` | 2026-09-25 | `d0ca30c24536fa37c9f85a36a949c9c0572be33309fbd3d2671113cdea51f5b1` |
| `gfw_tree_cover_extent_2000.csv` | Global Forest Watch Data API, `gadm__tcl__iso_summary`, version `v20260424` | 2026-09-25 | `71efdbf254b637b92028c62109b1e172e182b801fa994492f6a275a68628fed0` |
| `worldbank_gdp_per_capita_ppp.csv` | World Bank WDI, `NY.GDP.PCAP.PP.KD`, series updated 2026-07-13 | 2026-09-25 | `0aaa80593d77a3b3ddcc61e825e5eb7ce52cf58f51fce6e2b502907dd9b82f1c` |
| `worldbank_country_metadata.csv` | World Bank country list, region and income group | 2026-09-25 | `028b150152824119404b4a30094d3c79c74fe29897abfa015532b720d31844d4` |

**Why this form of the forest data.** The FAO Forest Resources Assessment series, reached through FAOSTAT, the World Bank or Our World in Data, was rejected: countries report only every five years and FAO fills the intervening years by linear interpolation, so annual change is mostly the shape of the interpolation rather than a measured change. Our World in Data's published file gives Afghanistan's 1991 change as exactly zero. It is also net, so planting in one place cancels clearing in another. The headline Global Forest Watch loss series was rejected as the sole measure because it counts logging rotation, wildfire and plantation harvest alongside permanent clearing; the driver-disaggregated form separates them, and both the disaggregated and the headline totals are used, for sub-questions 1 and 2 respectively.

**Why version `v20260424`.** The API's `latest` alias resolves to `v20250515`, which stops at 2024 and carries the older six-class Curtis et al. (2018) taxonomy. Version `v20260424` is served at the same endpoint without being flagged: it runs to 2025 and carries the eight-class WRI/Google taxonomy. The two agree to the hectare on every overlapping year — Brazilian primary forest at the 30 percent threshold gives 1,772,215 ha for 2022, 1,136,251 for 2023 and 2,823,647 for 2024 in both — and the 2024 figure matches the 2.8 Mha Global Forest Watch published. It is the same loss data with a richer classification, not a revision.

**Corroboration against the publisher.** Permanent agriculture, hard commodities, and settlements and infrastructure over 2001–2024 across all countries total 176.1 Mha, 34.1 percent of all tree cover loss, with permanent agriculture 94.6 percent of that. The World Resources Institute publishes 177 Mha, 34 percent and 95 percent for the same quantity, so the extraction and the driver scoping agree with the publisher to within half a percent.

### Units and what is a measurement

`tree_cover_loss_ha` and `extent_2000_ha` are **remotely sensed classifications**, not ground measurements: Landsat imagery at roughly 30 m, classified as stand-replacement disturbance by the algorithm of Hansen et al. (2013). The `driver` label is a **model output** — a ResNet trained on visually interpreted high-resolution imagery, assigning one dominant driver per 1 km cell for the whole 2001–2025 period. `gdp_pc_mean` is **partly a model output**: PPP conversion factors come from International Comparison Program benchmark surveys in benchmark years and are extrapolated to the rest.

Two consequences follow, and both belong in `Methods`. First, `permanent_loss_share` depends on the driver classifier while `total_loss_share` does not, since the latter sums over every class. Second, Hansen stores one loss year per pixel, so a pixel lost, regrown and lost again is counted once; the outcomes are therefore the share of year-2000 forest disturbed **at least once**, and repeat disturbance in fast-rotation plantations — which sit in richer countries — is undercounted.

### Source columns present but not used

`natural_forest_class` is Unknown for 43 percent of loss hectares, too much to build an outcome on. `is_primary_forest` would have cut most of Europe from the sample, and the driver split already isolates permanent conversion. `area_ha` is unused because the denominator is a country's own forest rather than its territory. `region` is unused. All four remain in `Attachments/`.

### What the loss data contains

Loss over the analysis window 2001–2024, all countries, totals 517,279,499 ha. Sub-question 1 takes the first three classes; sub-question 2 takes all eight. Both divide by the same denominator, `extent_2000_ha`.

| Driver | Mha, 2001–2024 | Share | In sub-question 1 | In sub-question 2 |
| --- | --- | --- | --- | --- |
| Permanent agriculture | 166.6 | 32.2% | yes | yes |
| Hard commodities | 4.9 | 0.9% | yes | yes |
| Settlements & Infrastructure | 4.7 | 0.9% | yes | yes |
| Wildfire | 151.6 | 29.3% | no | yes |
| Logging | 129.5 | 25.0% | no | yes |
| Shifting cultivation | 50.2 | 9.7% | no | yes |
| Other natural disturbances | 8.0 | 1.5% | no | yes |
| Unknown | 1.8 | 0.4% | no | yes |
| **Sub-question 1 numerator** | **176.1** | **34.1%** | | |
| **Sub-question 2 numerator** | **517.3** | **100%** | | |

Driver attribution is near-complete: 0.4 percent of hectares are Unknown.

The two outcomes are not a rescaling of each other. `permanent_loss_share` is at or below `total_loss_share` for every country by construction, the median ratio between them is 0.207, and they rank the 135 countries at Spearman 0.533. Portugal is the widest divergence, at 0.0159 against 0.5442, because almost all its tree cover loss is eucalyptus rotation and fire; Cambodia is the narrowest, at 0.3198 against 0.3309, because almost all of its loss was permanent clearing.

**Driver definitions.** Three are quoted from the publisher: wildfire is fire loss "with no visible human conversion or agricultural activity afterward"; permanent agriculture is clearing where agricultural use persists "following the tree cover loss event"; logging is loss "often with evidence of forest regrowth or planting in subsequent years". Verbatim definitions for hard commodities, settlements and infrastructure, shifting cultivation, and other natural disturbances have not yet been retrieved and are needed before `Methods` is written.

### What the sample excludes, and what that costs

**The forest floor removes 67 countries and 0.02 percent of global forest loss.** Without it the rate measure is dominated by artefacts: Mauritania's entire tree cover in 2000 is 33.3 ha, of which 33.2 ha was lost, a rate of 99.8 percent; Burkina Faso's is 130.3 ha, Eritrea's 4.6 ha, Niger's 2.3 ha. At a 30 m classification these are rounding effects. The countries excluded have almost no forest to lose, so the cost in the quantity being studied is near zero. The cost in coverage is not: the sample is a sample of forested countries, and any finding is a finding about forested countries rather than countries in general. A 10,000 ha floor (180 countries) and no floor with extent-weighted observations were both considered and not taken.

**Six forested countries are lost to missing GDP, not to the floor:** Venezuela, Cuba, North Korea, Eritrea, South Sudan and Taiwan. The World Bank publishes no PPP GDP for them. Venezuela and South Sudan in particular have meaningful forest loss, and their absence is a gap in the sample rather than a tidying-up. A further 27 codes with loss but no GDP are dependencies and territories with no separate GDP, or the GFW API's own non-country codes.

**2025 is excluded.** The release is five months old, its conversion total is the lowest since 2003, and World Bank GDP for 2025 is provisional. Including it moves the mean cumulative share from 0.0453 to 0.0473 and reorders the sample at Spearman 0.9997.

### Accepted as-is

The `Unknown` driver class, 0.3 percent of hectares, is retained as published rather than dropped or reassigned. Loss is gross: tree cover gain is not subtracted, so forest lost and regrown still counts as lost, and no annual gain layer exists to correct it. Income group is the current World Bank vintage applied to a period ending in 2024, which is acceptable because it is used only to select cases and never as an analysis variable.

## Research Question

### Discussion

The framing is the environmental Kuznets curve: the proposition that environmental damage rises with income while a country is industrialising and falls once it is rich enough to afford something cleaner. Applied to forests it implies that the poorest countries clear little, middle-income countries clear most, and the richest clear least. We test that shape across 135 countries, and then test it again with a broader measure of degradation.

**The outcome is measured as a cumulative share, not an annual rate.** For each country we take the forest permanently converted between 2001 and 2024 and divide it by the tree cover that country had in 2000. Income is the arithmetic mean of GDP per capita over the same years. This is a cross-section: one row per country, no time dimension.

**Two outcomes are used, and the pair is the point.** Sub-question 1 counts only permanent conversion, which depends on a classification model assigning a driver to each loss. Sub-question 2 counts all tree cover loss, which is the raw satellite record and does not depend on that model at all. Running the same specification on both shows whether the answer survives a broader definition of degradation, and whether it depends on trusting the driver classifier.

**Shifting cultivation is excluded from the headline outcome.** It is 9.8 percent of all loss and is temporary clearing that regrows, so it is not permanent loss. It is also concentrated in low-income countries, which is the rising limb of the curve, so the exclusion is not neutral. Sub-question 1 will be re-run with it included and the check reported here.

Four limitations are known before any result exists, and each belongs in `Methods` beside the number it qualifies.

**The resource is bounded.** A country cannot clear more forest than it has. Once remaining forest is small the loss rate is mechanically small, so a falling right-hand limb is exactly what would be produced by rich countries having completed their deforestation before the data begins — the forest transition described by Mather and Needle (1998). No specification separates "grew richer and chose to conserve" from "ran out of forest to clear".

**Income contains part of the outcome.** Clearing forest for agriculture and timber contributes to GDP, so the period-mean predictor is partly caused by the thing it is predicting. The relationship is an association, not a causal estimate.

**Driver labels are coarser than the loss they label.** The dominant driver is one label per 1 km cell for the whole 2001–2025 period, while loss is recorded at roughly 30 m and by year. The publisher states the product "does not show multiple drivers if they occur in the same cell at smaller scales, nor does it detail the sequence of drivers if multiple occurred at different times within the period." This affects sub-question 1 and not sub-question 2.

**Repeat disturbance is undercounted, and the bias has a direction.** Hansen stores one loss year per pixel, so forest lost, regrown and lost again counts once. Both outcomes are therefore the share of year-2000 forest disturbed at least once, not a count of disturbance events. Repeat disturbance inside a 24-year window happens in fast-rotation plantation forestry, which sits in richer countries, so degradation is understated at the rich end and the right-hand limb will fall more steeply than the truth. Its direction favours the hypothesis being tested. Nothing is double-counted: numerator and denominator are drawn from the same year-2000 pixel set, and in the data the highest cumulative total-loss share is Portugal at 0.544, with no country above 0.60. Portugal is the sharpest test available, since eucalyptus rotates on roughly ten to twelve years and a stand could be cut twice inside the window.

**The statistical method is not settled here.** Step 2 fixes what is being asked and what would count as an answer; the estimator, the functional form and the test belong to step 4. The outcome is a proportion bounded at zero and one, with skew 2.10 raw and −0.02 in logs, and that will bear on the choice when it is made.

*The sequence of framings this question passed through, including one claim that was made and later found to be false, is recorded in the `Analysis Log` rather than here.*

### Question

Does permanent forest loss follow the inverted-U path in national income that the environmental Kuznets curve describes — rising with income among poorer countries, peaking at middle income, and falling among the richest?

### Sub-questions

**1. The curve across countries.** Across the 135 sample countries, is the share of year-2000 forest permanently converted between 2001 and 2024 an inverted U in mean GDP per capita over the same period? *Variables:* outcome is cumulative loss attributed to permanent agriculture, hard commodities, and settlements and infrastructure, divided by tree cover extent in 2000; predictor is the arithmetic mean of GDP per capita at PPP in constant 2021 international dollars over 2001–2024, in logs, with its square. *What counts as an answer either way:* an inverted U requires the relationship to rise across the poorer part of the observed income range and fall across the richer part, with the peak inside the range rather than beyond either end. A relationship that only decelerates as income rises, with its implied peak outside the observed data, is a monotone relationship and will be reported as one. The estimator and the specific test are step 4's to choose; the requirement that the peak be interior is recorded here because it is a criterion for what counts as an answer, not a choice of method.

**2. The same curve, with all loss as the degradation measure.** Across the same countries, is the share of year-2000 forest lost to tree cover loss of any cause between 2001 and 2024 an inverted U in mean GDP per capita over the same period? *Variables:* outcome is cumulative tree cover loss summed over all eight driver classes, divided by tree cover extent in 2000; predictor is identical to sub-question 1. *Method:* whatever specification and test sub-question 1 settles on, applied unchanged, so that the two outcomes are directly comparable. *What counts as an answer either way:* the same criterion as sub-question 1, and the comparison between the two fitted relationships. Agreement would mean the shape does not depend on restricting the outcome to permanent conversion. Disagreement would locate the difference in the non-permanent drivers, which are logging, wildfire, shifting cultivation and natural disturbance. *Why this outcome is worth running alongside the first:* the first sub-question's outcome rests on a classification model, whereas total loss is the raw satellite record and is independent of how the classifier assigned drivers. The comparison therefore also shows whether the answer depends on trusting that model.

**3. Trends in individual countries.** How has the rate of permanent forest loss changed over 2001–2024 in countries at different income levels? *This is a descriptive comparison and not a test.* A trend is fitted to each selected country's annual rate and the fitted trends are compared. *Case selection, fixed 2026-09-25 before any trend was fitted:* the two countries with the highest cumulative permanent conversion share within each of the four World Bank income groups. The rule uses a quantity established in step 1 and was stated before the cases were known. Applying it gives:

| Income group | Country | `permanent_loss_share` | `gdp_pc_mean` |
| --- | --- | --- | --- |
| Low income | Chad | 0.1968 | 2,500 |
| Low income | Guinea-Bissau | 0.1301 | 2,253 |
| Lower middle income | Cambodia | 0.3198 | 4,458 |
| Lower middle income | Benin | 0.2789 | 2,983 |
| Upper middle income | Paraguay | 0.2780 | 13,116 |
| Upper middle income | Malaysia | 0.2495 | 25,686 |
| High income | Panama | 0.0734 | 25,541 |
| High income | Costa Rica | 0.0674 | 20,088 |

Written to `Code/outputs/h3_cases.csv`. Panama and Costa Rica are classified high income on the current World Bank vintage, which is why two tropical countries appear in that row; the classification is a present-day label applied to a period ending in 2024, and it selects cases rather than entering the analysis.

## Analysis

*The workings, one sub-heading per sub-question, added as steps 3 and 4 proceed. Diagnostics, alternative specifications, checks that changed nothing, and anything computed but not reported.*

## Analysis Log

| # | What was done | Output |
| --- | --- | --- |
| 1 | Created branch `deforestation` from `main` at the clean template state. | — |
| 2 | Established the measure of deforestation and the measure of income, after comparing the FAO net forest area series, the headline GFW tree cover loss series and the GFW loss-by-driver series. The user chose loss by driver, and GDP per capita at PPP in constant 2021 international dollars. Reasoning and the rejected alternatives are in `Data Summary`. | `Data Summary` |
| 3 | Compared GFW API versions `v20250515` (flagged `latest`) and `v20260424` (published but unflagged). Chose `v20260424`: one further year, finer driver taxonomy, SBTN natural-forest class, and exact agreement with the older version on all overlapping years. | `Data Summary` |
| 4 | Downloaded the three source files and recorded SHA-256 checksums. | `Attachments/*.csv`, `Code/01_download_data.py` |
| 5 | Described the three files without drawing conclusions: shape, columns, units, coverage, completeness, overlap. | `Code/02_describe_data.py` |
| 6 | Checked the reference links. The FAO, GFW and World Bank links resolve. The two `doi.org` links return 403 to scripted requests, which is science.org blocking automation rather than a dead link; their bibliographic details were verified against the Crossref API instead. **Neither Curtis et al. (2018) nor Hansen et al. (2013) has been opened.** They are cited here for the provenance of the dataset, on the strength of Crossref metadata and the GFW dataset documentation. Both would need reading in full before any claim drawn from their text enters `Report.md`. | `Appendix.md` References |
| 7 | Characterised the denominator problem after the user raised it: country size and forest endowment vary too much for absolute hectares to be comparable. Found that absolute loss and loss as a share of own forest rank countries only at Spearman 0.508, and that the top of the rate table is an artefact of countries with a few dozen hectares of tree cover. | `Code/03_denominator_options.py`, `Data Summary` |
| 8 | **Decision.** Minimum forest stock set at 100,000 ha of tree cover in 2000: 148 countries, 135 with GDP, retaining 99.98 percent of global loss. Choice of denominator deferred to step 2, since it depends on the question. Rejected alternatives recorded in `Comparability across countries`. | `Data Summary` |
| 9 | Step 2 feasibility. 135 countries carry both the outcome and GDP, split 15 low / 36 lower-middle / 40 upper-middle / 44 high income. Income spans 4.81 log points, a 123-fold range. GDP is complete for all 25 years in 132 of 135 countries. | `Code/04_feasibility.py` |
| 10 | First framing of the curve found to be underspecified and its test too weak; the criterion corrected to require the peak to lie inside the observed income range. The specific test named at the time, the Lind–Mehlum joint condition with a Fieller interval, was removed again at row 22 as premature for step 2. Recorded in `Research Question` → `Discussion`. | `Research Question` |
| 11 | Examined the denominator for an annual rate and found that subtracting all prior loss over-depletes rotation-forestry countries: Portugal loses 56.9 percent of 2000 tree cover but only 1.6 percent to permanent conversion. **Superseded** when the user chose a cross-section, which removes the problem. | `Code/05_outcome_definition.py` |
| 12 | **Decision.** Cross-sectional design on cumulative loss 2001–2024, by the user. Outcome is cumulative permanent conversion as a share of 2000 tree cover extent; predictor is mean GDP per capita over the period, in logs. 2025 excluded: release five months old, conversion total lowest since 2003, GDP provisional; costs Spearman 0.9997 in reordering. | `Code/06_cumulative_outcome.py` |
| 13 | **Decision.** Shifting cultivation excluded from the outcome, to be re-run as a sensitivity check. Wildfire question generalised from Europe to all countries at the user's direction. Third sub-question demoted from hypothesis to descriptive trend comparison, with the eight cases fixed by rule before any trend was fitted. | `Research Question` |
| 14 | Checked the WRI/Google driver methodology and found that the driver is the direct cause of a loss event, that a pixel is recorded lost only once, and that the driver is assigned per 1 km cell for the whole period. Post-fire conversion is therefore invisible, which fixes what a null on sub-question 2 can mean. Recorded in the sub-question itself. | `Research Question` |
| 15 | Corroborated the outcome against the publisher: our 2001–2024 permanent loss is 176.1 Mha, 34.1 percent of all loss, agriculture 94.6 percent of it; WRI publishes 177 Mha, 34 percent, 95 percent. Agreement within half a percent. | `Research Question` |
| 16 | Wrote the research questions into the `Introduction` of `Report.md`, before anything was tested. | `Report.md` |
| 17 | **Correction.** Verified the WRI/Google driver methodology against the Earth Engine catalogue and the Zenodo record. The claim recorded at row 14 — that post-fire conversion is invisible — is false: the classifier uses post-loss imagery and defines wildfire as fire loss with no human conversion afterward, so burnt-then-farmed land is classified as permanent agriculture. Row 14 is superseded and the discussion corrected. The real limitation is resolution: one driver label per 1 km cell for the whole period, with sequence and sub-kilometre mixtures collapsed to a majority. | `Research Question` |
| 18 | **Decision.** Sub-question 2 replaced at the user's direction. It no longer asks whether fire and permanent loss coincide; it repeats sub-question 1 with all tree cover loss, all drivers, as the degradation variable. Same specification, same test, directly comparable. | `Research Question`, `Report.md` |
| 19 | Checked whether sub-question 2 could double-count forest burnt more than once. It cannot: Hansen stores one loss year per pixel, and numerator and denominator share the same year-2000 pixel set. Confirmed in the data — maximum cumulative total-loss share is 0.544 (Portugal, fast eucalyptus rotation), none above 0.60, none above 1.00. The exposure runs the other way as undercounted repeat disturbance, biasing the rich end downward and so favouring the hypothesis. Recorded against the sub-question for `Methods`. | `Research Question` |
| 20 | Built the analysis dataset: 135 countries, one row each, from the four source files. Integrity checks all pass — no share outside [0,1], permanent never exceeds total, no missing values, one country with fewer than 24 GDP years. Arithmetic and geometric mean income rank at Spearman 0.999629, so the choice between them is immaterial. | `Code/07_build_analysis_dataset.py`, `Code/outputs/analysis_dataset.csv` |
| 21 | Applied the case-selection rule fixed at row 13 and recorded the eight resulting countries: Chad, Guinea-Bissau, Cambodia, Benin, Paraguay, Malaysia, Panama, Costa Rica. | `Code/outputs/h3_cases.csv` |
| 22 | Rewrote `Data Summary` around the analysis dataset at the user's request: the data actually used is described, unused source columns are named as unused, superseded decisions are condensed and marked. Removed the commitment to a specific statistical test from the sub-questions, since the method belongs to step 4. | `Data Summary`, `Research Question` |

## Code Summary

All scripts run from `Code/` with `uv run python <script>.py`. Environment as shipped: Python 3.12.13, pandas 3.0.5, numpy 2.5.2, scipy 1.18.1, statsmodels 0.15.0, matplotlib 3.11.1. No package has been added.

**`01_download_data.py`** — downloads the three source files to `Attachments/` and prints a SHA-256 for each. Reads nothing from the repository; writes `gfw_tree_cover_loss_by_driver.csv`, `gfw_tree_cover_extent_2000.csv` and `worldbank_gdp_per_capita_ppp.csv`. Two constants govern what is pulled: `GFW_VERSION = "v20260424"` pins the Global Forest Watch dataset version, and `CANOPY_THRESHOLD = 30` selects the canopy-density threshold. Re-running overwrites the files. The GFW API serves these queries without a key through its `download/csv` endpoint; the `query` endpoint does require one.

**`07_build_analysis_dataset.py`** — builds the one dataset the analysis uses. Reads all four files in `Attachments/`; writes `outputs/analysis_dataset.csv` (135 rows) and `outputs/h3_cases.csv` (8 rows). Applies the sample rule, computes both outcomes and the sensitivity outcome, takes the arithmetic and geometric means of income, and runs the integrity checks reported in `Data Summary`. Constants at the top: `FOREST_FLOOR_HA = 100_000`, the window `Y0, Y1 = 2001, 2024`, and the `PERMANENT` and `SHIFTING` driver lists. Every later script should read its output rather than the sources, so the sample is defined once.

**`04_feasibility.py`** — step 2 feasibility counts. Reads the loss, extent and country-metadata files; writes nothing. Reports sample size after the forest floor, breakdown by World Bank region and income group, GDP series completeness, and the spread of income. Reports no relationship between loss and income by design.

**`05_outcome_definition.py`** — makes the outcome concrete and tests how the denominator behaves across years. Written while an annual panel was under consideration; its finding that subtracting all prior loss over-depletes rotation-forestry countries is what is recorded in the discussion above. Superseded as a specification by the cross-sectional design, retained because the finding stands.

**`06_cumulative_outcome.py`** — compares the candidate definitions of cumulative loss. Shows that the cumulative share and the constant annual depletion rate are related by a strictly monotone transform and rank countries identically at Spearman 1.000000, that the naive average understates the rate by up to 16.3 percent where loss is high, that the cumulative share has skew 2.10 while its log has skew −0.02, and that dropping 2025 reorders the sample at Spearman 0.9997. `CONVERSION`, `FOREST_FLOOR_HA` and the period bounds are constants at the top.

**`03_denominator_options.py`** — quantifies the comparability problem and the candidate denominators. Reads the three files in `Attachments/`; writes nothing. Reports the spread in country size and forest endowment, the rank correlations between absolute and normalised loss, the effect of candidate minimum-forest floors on sample size and on the extreme rates, matched denominators for the primary-forest subset, and a declining stock denominator for annual rates. `CONVERSION_DRIVERS` at the top is a provisional illustration of a driver scope, not a decision. Does not read the GDP values into any comparison; the relationship is step 2's to frame.

**`02_describe_data.py`** — the describing pass. Reads the three files in `Attachments/` and prints shape, dtypes, unit coverage, missing-value counts, driver and class totals, the largest countries, and the ISO3 overlap between the loss and GDP files. Writes nothing. Draws no conclusions by design; the content of `Data Summary` above comes from its output.

## References

Curtis, P. G., Slay, C. M., Harris, N. L., Tyukavina, A. and Hansen, M. C. (2018) '[Classifying drivers of global forest loss](https://doi.org/10.1126/science.aau3445)', *Science*, 361(6407), pp. 1108–1111.

Food and Agriculture Organization of the United Nations (2025) *[Global Forest Resources Assessment 2025](https://www.fao.org/forest-resources-assessment/en)*. Rome: FAO. Considered as a data source and not used; see `Data Summary`.

Global Forest Watch (2026) *[Tree cover loss by driver, country level](https://data-api.globalforestwatch.org/dataset/gadm__tcl__iso_change)*, dataset `gadm__tcl__iso_change` version `v20260424`. World Resources Institute. Accessed 25 September 2026.

Grossman, G. M. and Krueger, A. B. (1995) '[Economic Growth and the Environment](https://doi.org/10.2307/2118443)', *The Quarterly Journal of Economics*, 110(2), pp. 353–377.

Hansen, M. C., Potapov, P. V., Moore, R., Hancher, M., Turubanova, S. A., Tyukavina, A., Thau, D., Stehman, S. V., Goetz, S. J., Loveland, T. R., Kommareddy, A., Egorov, A., Chini, L., Justice, C. O. and Townshend, J. R. G. (2013) '[High-resolution global maps of 21st-century forest cover change](https://doi.org/10.1126/science.1244693)', *Science*, 342(6160), pp. 850–853.

Lind, J. T. and Mehlum, H. (2010) '[With or Without U? The Appropriate Test for a U-Shaped Relationship](https://doi.org/10.1111/j.1468-0084.2009.00569.x)', *Oxford Bulletin of Economics and Statistics*, 72(1), pp. 109–118.

Mather, A. S. and Needle, C. L. (1998) '[The forest transition: a theoretical basis](https://doi.org/10.1111/j.1475-4762.1998.tb00055.x)', *Area*, 30(2), pp. 117–124.

Stern, D. I. (2004) '[The Rise and Fall of the Environmental Kuznets Curve](https://doi.org/10.1016/j.worlddev.2004.03.004)', *World Development*, 32(8), pp. 1419–1439.

World Bank (2026) *[GDP per capita, PPP (constant 2021 international $)](https://data.worldbank.org/indicator/NY.GDP.PCAP.PP.KD)*, indicator `NY.GDP.PCAP.PP.KD`, World Development Indicators. Series last updated 13 July 2026; accessed 25 September 2026.
