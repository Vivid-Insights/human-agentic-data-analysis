## Abstract

Whether environmental damage falls once a country is rich enough has a long history as a question. Stern (2004), reviewing that literature, found the statistical evidence for it weak. Forests are a case where the answer depends on what is being counted. We ask whether heavy forest clearing follows an inverted U in income across countries, whether the answer changes when all tree cover loss is counted however it was caused, and how the rate of clearing has moved since 2001. The data is a global satellite record of tree cover loss in which each loss carries a label for its direct cause, set against income per person. We find no inverted U. The chance that a country permanently converted a large share of its forest falls steadily as income rises, with the odds roughly halving for each doubling of income. Counting all tree cover loss, however, we find that richer countries lose about as much of their forest as poorer ones and convert much less of it. Loss is rising in several countries, and not for the same reason in each. 

***This report was generated as part of a course in using Agentic AI to do statistics and data science.***

## Introduction

Forests hold and release carbon on a scale that matters for the climate. Over 2001 to 2019 emissions from deforestation and other forest disturbance ran at about 8 billion tonnes of carbon dioxide equivalent a year, against gross removals roughly twice that (Harris et al., 2021). Where forest is cleared, and why, therefore matters well beyond the places it happens. One long-standing question is whether clearing is a stage a country passes through rather than a settled feature of it. The environmental Kuznets curve proposes that indicators of environmental degradation first rise and then fall as income per capita increases (Stern, 2004). The evidence usually cited for it comes from air and water rather than forests. Grossman and Krueger (1995) examined urban air pollution and river contamination across countries and found, for most of their indicators, a phase of deterioration followed by a phase of improvement. Whether the pattern generalises is disputed. Stern's review of the literature concludes that the results have a very flimsy statistical foundation, and that some developing countries have adopted developed-country standards with only a short lag instead of passing through a dirty phase first. For forests there is a further difficulty: what counts as a loss is itself a choice, and the answer may depend on which choice is made.

This report tests that shape on forest loss over the period 2001 to 2024. We don't attempt a review of the question and we don't try to settle it. The analysis is a worked example, and the forest data is here as much to illustrate the method as for its own sake: how a model is specified, what would count as evidence for it either way, and what a test of it can and cannot establish.

There are different ways in which forest can be lost. A satellite records that tree cover has gone, but the land underneath may have been cleared for soy and fenced, burned in a wildfire that will grow back, or harvested on a forestry rotation and replanted the next season. Only the first is deforestation (Curtis et al., 2018). Of all the tree cover lost across the world since 2001, about a third is land that changed use permanently, and most of the rest is fire and logging (Global Forest Watch, 2026). We measure the share of each country's year-2000 forest that it permanently converted, and set that against GDP per person over the same years.

Applied to forests, the Kuznets curve implies that the poorest countries clear little, middle-income countries clear most, and the richest clear least. We test that shape across the 135 countries with enough forest to lose and a published income figure, asking how clearing and income are associated rather than trying to show that one causes the other. Two further questions follow. Counting only permanent conversion rests on a model that classifies each loss by its cause, so we run the same comparison on all tree cover loss however it was caused. And a comparison between countries describes how countries differ rather than how any of them changed, so we also look at the annual rate of clearing in eight countries chosen in advance to span the income range.

The questions we set out to answer are:

1. Across countries, does the chance that a country permanently converted more than 2 percent of its year-2000 forest between 2001 and 2024 follow an inverted U in average income over those years, rising among poorer countries, peaking at middle income, and falling among the richest?
2. What relationship do we see when the measure of degradation is all tree cover loss however caused, with the threshold set at 10 percent?
3. How has the rate of permanent forest loss changed since 2001 in countries at different income levels?

## Methods

### Data

Forest loss comes from the Global Forest Watch record of tree cover loss by driver, version `v20260424` (Global Forest Watch, 2026). Loss is detected from Landsat imagery at about 30 m and recorded as a stand-replacement disturbance (Hansen et al., 2013), so degradation that leaves a stand standing does not appear in it. Each 1 km cell carries one label for the dominant direct cause of its loss over the whole period, assigned by a neural network trained on interpreted high-resolution imagery (Sims et al., 2025; World Resources Institute and Google DeepMind, 2026).

We use two measures of loss, both summed over 2001 to 2024 and both divided by the same denominator, the country's tree cover in 2000 at a canopy density of 30 percent or more. The first counts only loss attributed to permanent agriculture, hard commodities, or settlements and infrastructure, which are the three classes in which the land does not return to forest. The second counts loss from all eight classes, and so does not depend on the driver classifier at all. Income is GDP per capita at purchasing power parity in constant 2021 international dollars, averaged over the same years (World Bank, 2026).

The sample is the 135 countries that held at least 100,000 hectares of tree cover in 2000 and have a published income figure. Of the 194 countries with a tree cover and loss record, the floor removes 54 whose entire tree cover is a few dozen hectares, where a loss share is an artefact of the 30 m classification rather than a measurement; between them they account for 0.01 percent of global tree cover loss. Five forested countries are lost instead to missing income data, among them Venezuela and South Sudan. Any finding here is therefore a finding about forested countries with published national accounts, not about countries in general.

### Testing for an inverted U in income

We code each of the 135 countries 1 if it permanently converted more than 2 percent of its year-2000 tree cover between 2001 and 2024, and 0 otherwise. The cut falls at the 54th percentile of the sample and splits it 62 above and 73 below. Income is the mean of GDP per capita at purchasing power parity over the same years, in logs.

Write $x$ for log income and $p(x)$ for the probability that a country lies above the threshold. The model is

$$\ln\left(\frac{p(x)}{1-p(x)}\right) = \beta_0 + \beta_1 x + \beta_2 x^2$$

fitted by maximum likelihood. We ask three things of it in turn. First, whether the probability rises or falls with income at all: we set $\beta_2 = 0$ and report $\beta_1$ as an odds ratio per doubling of income. Second, whether that answer survives without a threshold: we give Spearman's rank correlation between the untruncated loss share and log income, which puts no cut anywhere in the outcome, so if the logistic result were an artefact of where we drew the line the two would disagree. Third, whether the relationship turns rather than running one way throughout: we also fit $\beta_2$, which potentially allows an inverted U.

Everything in that third step comes from one expression. The slope of the fitted curve is

$$\frac{d}{dx}\ln\left(\frac{p}{1-p}\right) = \beta_1 + 2\beta_2 x$$

which is itself a straight line in $x$. It passes through zero at

$$x^* = -\frac{\beta_1}{2\beta_2}$$

and the sign of $\beta_2$ says what sort of turning point that is: negative means the slope falls through zero, so $x^*$ is a maximum, and positive means it is a minimum. 

In order to say there is an inverted U, we require two things of the fit. Firstly, the turning point has to fall inside the observed income range, which runs from about 1,000 to about 129,000 dollars. Secondly, the slope has to be positive at the bottom of that range and negative at the top:

$$s_{\text{lo}} = \beta_1 + 2\beta_2 x_{\text{lo}} > 0 \qquad\text{and}\qquad s_{\text{hi}} = \beta_1 + 2\beta_2 x_{\text{hi}} < 0$$

The two conditions have to hold together, so the test only rejects if both of the one-sided tests do, which makes the joint p-value the larger of the two rather than the smaller (Lind and Mehlum, 2010). These conditions are illustrated in Figure 1.

\begin{center}
\includegraphics[width=0.95\linewidth,keepaspectratio]{Code/outputs/figures/fig_ushape_test.png}
\end{center}

\begin{quote}
\small\textbf{Figure 1.} Illustrative curves, not data. Each panel plots the log odds of heavy forest loss against log income as a quadratic with a negative squared term. The green segments are the slope $\beta_1 + 2\beta_2 x$ at the lowest and highest income observed, with their signs. On the left it changes sign within the range, so the curve turns at $x^*$ and an inverted U holds; on the right both slopes are negative and $x^*$ lies below the range.
\end{quote}

Three things limit what these models can tell us. The threshold is a choice and not a measurement, and we picked it after seeing the distribution of the outcome. We treat countries as independent observations, which they aren't — neighbouring countries share commodity frontiers and forest types — and with one row per country there is no grouping to correct for, so the intervals are narrower than the dependence warrants. And coding the outcome as above or below a line discards the difference between a country at 3 percent and one at 32 percent, so the model answers whether a country is a heavy clearer and not how heavy.

To see how much the answer depends on where the cut is put, we refit the straight-line model at ten thresholds spaced logarithmically from 0.005 to 0.05, which brackets the cut we use and runs from well below the median to roughly three times it.

We repeat the straight-line model and the rank correlation on tree cover loss from all eight driver classes, with the threshold at 10 percent. That cut falls at the 48th percentile and splits the sample 70 above and 65 below. The threshold differs from the one above because the outcomes do. Their medians are 1.3 percent and 10.6 percent, so a single cut applied to both would separate the heaviest third of countries on one measure and the lightest fifth on the other, and the two models would not be answering the same question. Setting each threshold near its own median is what makes the pair comparable.

### Loss over time

Figures 3 and 4 show loss year by year rather than summed over the period. The annual series uses the same denominator as the tests, each country's tree cover in 2000, so a country's twenty-four annual values add up to its cumulative share. The year a loss is assigned to is derived rather than observed: the disturbance is detected first and then allocated to a year by heuristic, so the level of a series and the direction it moves over the period carry information while the step from one year to the next does not. We fit no trend to these and report no statistic from them. The eight countries in Figure 3 are the two with the highest cumulative permanent conversion in each World Bank income group, fixed before any series was examined; the four in Figure 4 are named rather than selected, and are not representative of Europe. They are there to show the contrast between the two measures of loss inside a country over time, rather than across countries as the tests do.

## Results

### Testing for an inverted U in income

Figure 2 shows the two outcomes against income, each with its own threshold marked.

\begin{center}
\includegraphics[width=0.95\linewidth,keepaspectratio]{Code/outputs/figures/fig2_outcomes_vs_income.png}
\end{center}

\begin{quote}
\small\textbf{Figure 2.} Each point is one of the 135 countries. Left: permanent conversion. Right: tree cover loss from all eight driver classes. The panels share both axes and the same year-2000 denominator, so heights can be compared across them. The horizontal line in each is that model's threshold, 0.02 and 0.10. Labelled countries are the highest and lowest in each panel. No curve is fitted.
\end{quote}

The chance that a country permanently converted more than 2 percent of its year-2000 forest falls as income rises. The slope on log income is −1.067, with a 95% confidence interval from −1.475 to −0.659 (p = $3 \times 10^{-7}$). The odds of being above the threshold roughly halve for each doubling of income: an odds ratio of 0.48, with an interval from 0.36 to 0.63. That is across 135 countries, of which 62 are above the threshold. Spearman's rank correlation between the untruncated loss share and log income is −0.44 (p = $7 \times 10^{-8}$).

Adding the square of log income does not establish an inverted U. The quadratic term is −0.320, with a 95% confidence interval from −0.679 to +0.039. The fitted curve turns at about 1,900 dollars a year, close to the bottom of the observed range, and its 95% confidence interval is unbounded, so the data doesn't locate the turning point. The joint condition isn't met (p = 0.32): the slope is negative at the top of the income range, at −2.71 (p = 0.003), but at the bottom it is +0.39 and we can't distinguish it from zero (p = 0.32). This is the right-hand case of Figure 1. By the criterion we fixed before fitting, we report it as a decline across the income range. Over that range the fitted probability runs from 0.78 at the poorest end to 0.011 at the richest. The decline also holds wherever the cut is put: the slope is negative at all ten thresholds, from −1.07 to −0.74, with the whole 95% interval below zero at every one, and the joint condition for an inverted U is met at none.

Income doesn't account for which countries lost more than 10 percent of their year-2000 forest to tree cover loss of any cause. The slope on log income is +0.005, with a 95% confidence interval from −0.295 to +0.305 (p = 0.98) — an odds ratio of 1.00 per doubling of income, with an interval from 0.82 to 1.24. The rank correlation on the untruncated share is −0.02 (p = 0.80). Over 135 countries spanning a 128-fold range of income, that rules out a change in the odds larger than about a fifth either way per doubling. Whatever produces the decline in permanent conversion does not show up once the other drivers of loss are counted alongside it.

### Loss over time

\begin{center}
\includegraphics[width=0.95\linewidth,keepaspectratio]{Code/outputs/figures/fig3_annual_cases.png}
\end{center}

\begin{quote}
\small\textbf{Figure 3.} Permanent conversion in each year, as a share of the country's year-2000 tree cover. Panels share a y-axis and run in order of mean income, lowest first, with each country's World Bank income group in its title. No trend is fitted.
\end{quote}

Figure 3 shows changes in forest conversion across the world. The two poorest countries, Guinea-Bissau and Chad, cleared roughly three times as much and six times as much, respectively, in their last six years as in their first. Cambodia has also cleared more in recent years. Benin, Malaysia and Costa Rica run the other way and end lower than they started, while Paraguay and Panama end about where they began.

\begin{center}
\includegraphics[width=0.95\linewidth,keepaspectratio]{Code/outputs/figures/fig4_europe_annual.png}
\end{center}

\begin{quote}
\small\textbf{Figure 4.} Tree cover loss from all eight driver classes in each year, as a share of each country's year-2000 tree cover. The panels share a scale to 0.04; a break across a bar marks a year that runs past it. No trend is fitted.
\end{quote}

Figure 4 shows that annual tree cover loss, including temporary loss, has tended to increase in the four countries. Germany changes most: there is little loss before 2018 and its heaviest year is 2021. Spain drifts upward across the whole period. Sweden is the steadiest of the four, but still increases year on year. Portugal sits above the other three throughout and is dominated by 2016 to 2018, when three consecutive years run off the top of the scale. 

## Discussion

We set out to test whether heavy forest clearing follows an inverted U in income, and it doesn't. What we found instead is a decline across the whole income range. The odds that a country permanently converted more than 2 percent of its year-2000 forest halve for each doubling of average income. This result does not depend critically on the choice of 2 percent as a threshold: other thresholds gave the same result and the rank correlation on permanent forest clearance and GDP shows the same pattern. When we count all tree cover loss, however it was caused, income predicts nothing. Richer countries lose about as much of their forest as poorer ones do, and convert much less of it to another use. Sweden is one of the clearest cases: it lost 22 percent of its year-2000 forest over the period, while permanent conversion came to 0.24 percent of that same starting forest. 

Loss is rising in several of the countries we looked at, and not for the same reason in each. Among the eight we looked at in Figure 3, the two poorest clear more now than they did at the start: Chad's permanent conversion over its last six years runs about six times its first six, and Guinea-Bissau's about three times. Cambodia has also cleared more in recent years, while Benin, Malaysia and Costa Rica end lower than they started. The four European countries in Figure 4 are also losing more tree cover than they were, but almost none of what they lose is conversion. Between about 1 and 5 percent of their loss over the whole period was permanent, and the rest is forestry, fire, shifting cultivation and natural disturbance. 

## Limitations

There are three things we'd be careful about in reading this. We have compared countries rather than followed them, so nothing here establishes that a country clears less as it grows richer. The split between permanent conversion and temporary loss comes from a model that labels each loss by its cause rather than from the satellite record itself. The second result doesn't rest on that model, but the contrast between the two does. And the eight countries shown in Figure 3 were picked to span the income range, while the four in Figure 4 were picked by name, so neither set is a sample of anything and care should be taken interpreting these results. 

## Disclaimer

This report was written with the help of agentic AI at every stage: importing and describing the data, cleaning it, framing the questions, choosing and fitting the models, producing the figures, and drafting the text. Each step was directed and reviewed by the author, who agreed every method before it was applied, and each number reported here comes from code that can be re-run. The record of what was done, including what was tried and abandoned, is in the appendix.

## Appendix

*A pointer to Appendix.md, where the data, the decisions and the full workings are recorded.*

## References

Curtis, P. G., Slay, C. M., Harris, N. L., Tyukavina, A. and Hansen, M. C. (2018) '[Classifying drivers of global forest loss](https://doi.org/10.1126/science.aau3445)', *Science*, 361(6407), pp. 1108–1111.

Global Forest Watch (2026) *[Tree cover loss by driver, country level](https://data-api.globalforestwatch.org/dataset/gadm__tcl__iso_change)*, dataset `gadm__tcl__iso_change` version `v20260424`. World Resources Institute. Accessed 25 September 2026.

Grossman, G. M. and Krueger, A. B. (1995) '[Economic Growth and the Environment](https://doi.org/10.2307/2118443)', *The Quarterly Journal of Economics*, 110(2), pp. 353–377.

Hansen, M. C., Potapov, P. V., Moore, R., Hancher, M., Turubanova, S. A., Tyukavina, A., Thau, D., Stehman, S. V., Goetz, S. J., Loveland, T. R., Kommareddy, A., Egorov, A., Chini, L., Justice, C. O. and Townshend, J. R. G. (2013) '[High-resolution global maps of 21st-century forest cover change](https://doi.org/10.1126/science.1244693)', *Science*, 342(6160), pp. 850–853.

Harris, N. L., Gibbs, D. A., Baccini, A., Birdsey, R. A., de Bruin, S., Farina, M., Fatoyinbo, L., Hansen, M. C., Herold, M., Houghton, R. A., Potapov, P. V., Suarez, D. R., Roman-Cuesta, R. M., Saatchi, S. S., Slay, C. M., Turubanova, S. A. and Tyukavina, A. (2021) '[Global maps of twenty-first century forest carbon fluxes](https://doi.org/10.1038/s41558-020-00976-6)', *Nature Climate Change*, 11(3), pp. 234–240.

Lind, J. T. and Mehlum, H. (2010) '[With or Without U? The Appropriate Test for a U-Shaped Relationship](https://doi.org/10.1111/j.1468-0084.2009.00569.x)', *Oxford Bulletin of Economics and Statistics*, 72(1), pp. 109–118.

Sims, M. J., Stanimirova, R., Raichuk, A., Neumann, M., Richter, J., Follett, F., MacCarty, J., Lister, K., Randle, C., Sloat, L., Esipova, E., Jupiter, J., Stanton, C., Morris, D., Slay, C. M., Purves, D. and Harris, N. (2025) '[Global drivers of forest loss at 1 km resolution](https://doi.org/10.1088/1748-9326/add606)', *Environmental Research Letters*, 20(7), 074027.

Stern, D. I. (2004) '[The Rise and Fall of the Environmental Kuznets Curve](https://doi.org/10.1016/j.worlddev.2004.03.004)', *World Development*, 32(8), pp. 1419–1439.

World Bank (2026) *[GDP per capita, PPP (constant 2021 international $)](https://data.worldbank.org/indicator/NY.GDP.PCAP.PP.KD)*, indicator `NY.GDP.PCAP.PP.KD`, World Development Indicators. Series last updated 13 July 2026; accessed 25 September 2026.

World Resources Institute and Google DeepMind (2026) *[Global drivers of forest loss at 1 km resolution](https://doi.org/10.5281/zenodo.19485190)*, version 1.3, covering 2001–2025. Zenodo. Released 29 April 2026; accessed 6 October 2026.
