# How democracy and national income change together

## Abstract

Richer countries tend to be more democratic, but whether rising income brings democracy, or democracy brings growth, remains disputed (Barro, 1996; Acemoglu et al., 2008; Acemoglu et al., 2019). We model the yearly change in democracy and in GDP per capita as functions of the current levels of both, letting Bayesian model selection choose the form of each equation, and fit the model to 1981–2006. Democracy moves towards a level that rises with income, and countries with more democracy grew faster, as did poorer ones. These are associations, and the model explains only a small part of the year-to-year variation. With a second measure of democracy the selected terms differ, but democracy again moves towards a level that rises with income and again goes with faster growth, of the same size. We then asked whether the model fitted to 1981–2006 predicts 2007–2024. It does not: year by year it predicts changes no better than each variable's average change, the relationships it describes became weaker, and countries moved away from the level of democracy it predicts instead of towards it. The model describes how democracy and income moved together in one period, not a relationship that held after it.

## Introduction

Richer countries tend to be more democratic, and the correlation between income and democracy across countries is strong (Acemoglu et al., 2008). What lies behind it is less clear. Barro (1999) found that rises in the standard of living predict rises in democracy, but Acemoglu et al. (2008) found that the association disappears when each country is compared only with itself over time. The relationship in the other direction is contested too. Barro (1996) found the overall effect of democracy on growth to be weakly negative once the rule of law, markets and initial income are held constant, while Acemoglu et al. (2019) report that democratisation raises GDP per capita by about a fifth in the long run. Findings also rest on how democracy is measured: indices differ in how they define democracy, measure its parts and combine them, and even the most widely used have important weaknesses (Munck & Verkuilen, 2002).

Growth also depends on where a country starts: poorer countries tend to grow faster once differences in schooling are allowed for (Barro, 1991). Most studies estimate one direction of the relationship at a time, with a functional form fixed in advance. Ranganathan, Spaiser and Sumpter (2013) instead model the yearly change in each variable as a function of the current levels of both, and let the data choose the form. The approach has since been applied to democracy and human development (Spaiser et al., 2014). It allows relationships in both directions, and non-linear ones, to appear in the same model. A model of how countries change can also be tested on years it was not fitted to.

We look at how democracy and national income change together across countries, fitting the model to 1981–2006 and testing it on 2007–2024. Income is GDP per capita from the World Bank, in constant 2015 US dollars, shown on a logarithmic scale. Our main measure of democracy is the citizen rights index of Welzel (2013). It runs from 0 to 1 and combines expert ratings of political rights and civil liberties with scores of how far those rights are respected in practice. The second is the electoral democracy index of the V-Dem project (Coppedge et al., 2025), which also runs from 0 to 1 and is estimated by a statistical model from many experts' ratings. Both are ways of measuring democracy built from expert codings rather than measured directly.

We model the yearly change in each variable as a function of the current levels of both, so that the two equations together describe a dynamical system. Each change is a sum of terms from a fixed set of polynomials in the two variables, and the data choose which terms enter. All countries are pooled, so we assume that every country follows the same dynamics from wherever it starts. The questions we look at are of association rather than cause. A term in the equation for the change in democracy says how that change varies with income, not that income drives it.

We ask two questions:

1. What model best describes the yearly changes in democracy and GDP per capita, and what dynamics does it imply?
2. Do the results hold with a different measure of democracy, and does the model fitted to 1981–2006 predict the changes from 2007 to 2024?

## Methods

### Data

GDP per capita comes from the World Bank (2026; indicator NY.GDP.PCAP.KD), in constant 2015 US dollars. Democracy is the citizen rights index of Welzel (2013), from the Quality of Government dataset (Teorell et al., 2015). It combines Freedom House ratings of political rights and civil liberties with Cingranelli–Richards scores of how far those rights are respected in practice. The second measure is V-Dem's electoral democracy index (Coppedge et al., 2025; indicator v2x_polyarchy). A yearly change is the difference between consecutive years in which a country has both variables. With Welzel's index this gives 3,423 changes from 183 countries between 1981 and 2006. With V-Dem it gives 3,955 changes from 171 countries for 1981–2006, and 3,088 from 174 countries for 2007–2024. In the model, GDP enters as $G = \ln(\text{GDP per capita})/12$, so a yearly change of $x$ in $G$ is growth of about $12x$, or exactly $e^{12x} - 1$.

### Model

The yearly change in each variable is modelled as a sum of terms in the current levels of both, $\Delta D = f_D(D, G) + \varepsilon$ and $\Delta G = f_G(D, G) + \varepsilon$, where $\varepsilon$ is normally distributed noise. Following Ranganathan, Spaiser and Sumpter (2013), the terms are drawn from a fixed set: $1, D, G, 1/G, D/G, DG, D^2, G^2$ and $1/G^2$. Terms with democracy in the denominator are left out, because democracy is exactly zero in 108 country-years. All countries and years are pooled, so each country is treated as a different starting point in one shared system. This is what lets countries at different levels of democracy and income together trace out how change depends on the current state. It assumes that two countries in the same state can expect the same change. V-Dem's index is never zero, but we use the same nine terms with it, so that the two measures are compared on the same model.

### Model selection and uncertainty

For each equation we fitted all 512 combinations of terms by least squares and kept the best-fitting combination of each size. We compared sizes by their Bayesian evidence, the probability of the observed changes averaged over the prior (Ranganathan et al., 2014). The noise standard deviation is fixed at the standard deviation of the observed changes. The prior on the coefficients is normal: each term is first divided by its root-mean-square value, and the prior standard deviation is again the standard deviation of the observed changes, so that a term at its typical size is expected to move the variable by about one typical yearly change. The evidence and the posterior distribution of the coefficients then have closed forms. We report the size with the highest evidence, its posterior probability with every size equally likely beforehand, and 95% credible intervals for its coefficients. The fit treats every yearly change as independent, but each country contributes up to 25 of them. For GDP these are not independent: a country that grows faster than the model predicts in one year tends to do so the next, with a correlation of 0.26 between the residuals of consecutive years. For democracy the correlation is −0.14. With V-Dem the correlations are 0.21 for democracy and 0.31 for GDP. To allow for this, we refitted on 500 samples of the countries drawn with replacement. Resampling whole countries keeps each country's years together, so the spread of the refitted coefficients includes this dependence, which the credible intervals do not.

### Dynamics

From the selected equations, we computed for each level of GDP the level of democracy at which the yearly change in democracy is zero, the democracy nullcline, and whether changes on either side point towards it or away. We repeated this for 1,000 draws of the coefficients from their posterior distribution to give a 95% band. We also checked whether the yearly change in GDP is zero anywhere in the observed range. To see where the equations take countries, we stepped them forward one year at a time from each country's first observed state to 2006. We then measured each country's distance from the democracy nullcline, at the start and at the end. We measured the same distance for the observed paths.

### Prediction

For the second question we fitted the model with V-Dem's index to 1981–2006 only, and scored it on the 3,088 changes from 2007 to 2024. Year by year, we computed the probability the fitted model gives to each observed change, allowing for the uncertainty in its coefficients. We compared it with an average-change model, fitted to the same years, that predicts each variable's mean change regardless of a country's state. We also compared it with the same terms refitted to 2007–2024, which is the best those terms could have done. Over the whole period, we stepped each of the 168 countries observed in both 2006 and 2024 forward from its 2006 state and compared its predicted 2024 state with the observed one.

## Results

Figures 1 and 2 show the same data in two ways. Figure 1 plots each variable against time. Figure 2 plots the two variables against each other, so that a country's path through the figure is the sequence of states it passed through between 1981 and 2006. In Figure 2, a line moving up is a country becoming more democratic, and a line moving right is a country becoming richer. GDP is on a logarithmic scale, so equal distances are equal proportional changes: moving from \$1,000 to \$2,000 is the same distance as moving from \$10,000 to \$20,000.

![Figure 1](Code/outputs/figures/fig1_trajectories_time.png)

<small><b>Figure 1.</b> Democracy, <em>D</em> (left), and GDP per capita in constant 2015 US dollars on a logarithmic scale (right), from 1981 to 2006. Lines are six countries: Italy, Sweden, India, Chile, Albania and Nigeria. Albania has no observations for 1985–1989, shown as a gap.</small>

![Figure 2](Code/outputs/figures/fig2_trajectories_plane.png)

<small><b>Figure 2.</b> Democracy, <em>D</em>, against GDP per capita in constant 2015 US dollars on a logarithmic scale. Grey points are the 181 countries with both variables in 2006. Coloured lines are the paths of the six countries in Figure 1 from 1981 to 2006, with a filled circle at 1981.</small>

Figure 3 summarises all 3,423 observed yearly changes on the same axes as Figure 2. The plane is divided into a grid of cells, and each arrow stands for the country-years in one cell. It starts at their average position and points along their average yearly change, drawn over 3⅓ years so that its direction is easy to see. The longest arrows are shortened to a maximum length, with their direction unchanged. An arrow pointing up is a cell in which democracy rose on average. An arrow pointing right is a cell in which GDP per capita grew, and because the GDP axis is logarithmic, the arrow's horizontal length is proportional growth.

![Figure 3](Code/outputs/figures/fig3_data_phase_portrait.png)

<small><b>Figure 3.</b> Observed yearly changes in democracy and GDP per capita (constant 2015 US dollars, logarithmic scale), averaged within cells of a grid. Each cell spans a factor of about 1.6 in GDP per capita and 0.1 in democracy. Each arrow starts at the average position of the country-years in its cell, marked by a dot, and points along their average yearly change. Arrows are drawn at 3⅓ times the yearly change, and the 33 longest are shortened to 0.47 cm, with their direction unchanged. Cells with fewer than 10 yearly changes have no arrow; the 83 cells with arrows hold 3,289 of the 3,423 changes. Faint lines are the paths of the six countries in Figures 1 and 2.</small>

### Question 1: the fitted model and its dynamics

The selected equations, fitted to 3,423 yearly changes from 183 countries, are

$$\Delta D = 0.267\,D - 0.144\,\frac{D}{G} - 0.118\,D^2 + 0.0030\,\frac{1}{G^2}$$

$$\Delta G = 0.00185\,D + 0.00027\,\frac{1}{G^2}$$

The 95% credible intervals are 0.209 to 0.325 for $D$, −0.174 to −0.113 for $D/G$, −0.150 to −0.085 for $D^2$ and 0.0014 to 0.0046 for $1/G^2$ in the democracy equation, and 0.00146 to 0.00224 for $D$ and 0.00019 to 0.00035 for $1/G^2$ in the GDP equation. The posterior probability of the selected size is 0.68 for the democracy equation and 0.75 for the GDP equation, against 0.19 for the next most probable size in each. Democracy enters the GDP equation: a country at democracy 1 grows about 2.2% a year faster than one at democracy 0 (1.8% to 2.7%), and the best GDP model without democracy has a log-evidence 14.9 lower. When the countries are resampled, $D/G$ and $D^2$ are selected for the democracy equation in at least 488 of 500 samples, and a democracy term for the GDP equation in 492, but the other terms vary, and the coefficient ranges are up to about one and a half times as wide as the credible intervals.

Together, the two equations make the yearly change in democracy zero along a curve that rises with GDP per capita, the democracy nullcline (Figure 4). On the nullcline, democracy is 0.27 at \$500 per person, 0.47 at \$2,000, 0.63 at \$5,000, 0.73 at \$10,000, 0.83 at \$20,000 and 0.95 at \$50,000, with a 95% band about 0.11 wide. Below it democracy rises and above it democracy falls, at every level of GDP in the observed range. GDP per capita grows everywhere in that range, by 0.3% to 4.1% a year, so there is no point where both changes stop. Stepped forward from their first observed states to 2006, 168 of the 183 countries end closer to the nullcline than they started, and their median distance from it falls from 0.23 to 0.08. In the observed data, 104 countries end closer, and the median distance falls from 0.23 to 0.15.

Figure 4 is read like Figure 3, but the arrows now show the change predicted by the two equations at the same positions, not the observed average. The grey line is the democracy nullcline, where the predicted change in democracy is zero, and the light grey band is its 95% interval. The coloured lines with a dot are where the equations take each of the six countries from its 1981 state; their observed paths are in Figure 2.

![Figure 4](Code/outputs/figures/fig4_model_phase_portrait.png)

<small><b>Figure 4.</b> Yearly changes in democracy and GDP per capita (constant 2015 US dollars, logarithmic scale) predicted by the selected models. Arrows show the predicted change at the positions of the arrows in Figure 3, drawn at 3⅓ times the yearly change; 14 of the 83 are shortened to 0.47 cm with their direction unchanged. The grey line is the democracy nullcline, where the predicted yearly change in democracy is zero, drawn where it lies between 0 and 1 and within the observed range of GDP, with its 95% band from 1,000 posterior draws. Coloured lines with a dot are the six countries' paths simulated year by year from their 1981 states to 2006.</small>

### Question 2: a second measure, and prediction

With V-Dem's index for 1981–2006, the selected equations, fitted to 3,955 yearly changes from 171 countries, are

$$\Delta D = 0.0075 + 0.063\,DG - 0.071\,D^2$$

$$\Delta G = 0.00226\,D^2 + 0.00025\,\frac{1}{G^2}$$

The 95% credible intervals are 0.0042 to 0.0108 for the constant, 0.030 to 0.095 for $DG$ and −0.099 to −0.042 for $D^2$ in the democracy equation, and 0.00173 to 0.00279 for $D^2$ and 0.00016 to 0.00033 for $1/G^2$ in the GDP equation. The posterior probability of the selected size is 0.72 for the democracy equation and 0.67 for the GDP equation, against 0.14 and 0.26 for the next most probable. The terms differ from those selected with Welzel's index. But $D^2$ is again in the democracy equation, selected in 466 of 500 resamples, and democracy is again in the GDP equation: the best GDP model without it has a log-evidence 13.0 lower, and a democracy term is selected in 492 of 500 resamples. A country near the top of V-Dem's index, at 0.9, grows about 2.2% a year faster than one at its bottom (1.7% to 2.8%). The democracy nullcline again rises with income and attracts at every level in the observed range, but it is flatter: democracy on it is 0.63 at \$500 per person, 0.71 at \$2,000, 0.77 at \$5,000, 0.81 at \$10,000 and 0.91 at \$50,000, with a 95% band about 0.10 wide. GDP grows everywhere in range. Stepped forward to 2006, 158 of the 171 countries end closer to the nullcline than they started, and in the observed data 119 do.

The model fitted to 1981–2006 does not predict the yearly changes from 2007 to 2024 better than the average-change model. Its mean log predictive density per change is 1.839 for democracy and 3.905 for GDP, against 1.840 and 3.909 for the average-change model, and it scores higher than that model on 43% and 44% of the changes. Out of sample it explains none of the variance in either change. Refitted to 2007–2024, the same terms have coefficients less than half their earlier size: 0.024 for $DG$ and −0.028 for $D^2$ in the democracy equation, and 0.00069 for $D^2$ in the GDP equation. Over the whole period, the model's predicted 2024 democracy is closer to the observed value than the average-change prediction for 106 of the 168 countries, with a median error of 0.15 against 0.17. Its predicted GDP is closer for 74, with a median error of 27% against 22%. The model has countries converging on the democracy nullcline, to a median distance of 0.08 by 2024. The observed countries moved away from it instead: their median distance rose from 0.17 in 2006 to 0.26 in 2024, and 48 of the 168 ended closer (Figure 5).

Figure 5 starts each of the six countries at its 2006 state. Solid lines are where the countries went, dashed lines are where the 1981–2006 model predicted they would go, and the grey line is that model's democracy nullcline.

![Figure 5](Code/outputs/figures/fig5_prediction.png)

<small><b>Figure 5.</b> Electoral democracy (V-Dem index, 0 to 1) against GDP per capita (constant 2015 US dollars, logarithmic scale), 2006–2024, for the six countries of Figures 1–4, each from a filled circle at its 2006 state. Solid lines are observed. Dashed lines are predicted, by stepping the model fitted to 1981–2006 forward year by year. The grey line and light grey band are that model's democracy nullcline and its 95% band from 1,000 posterior draws.</small>

## Discussion

The clearest relationship in growth is between democracy and income. Countries with more democracy grew faster: a country at democracy 1 grows about 2.2% a year faster than a country at democracy 0 with the same income, and a democracy term enters the GDP equation in almost every resample of the countries. Poorer countries also grew faster. At democracy 0 the model predicts growth of about 1.8% a year at the lowest incomes in the data and 0.3% at the highest. Together the two terms put the fastest growth, about 4.1% a year, in poor countries with high democracy, and the slowest in rich countries with none.

These are associations between the level of democracy and the growth that followed, not evidence that democracy causes growth. The model accounts for about 1% of the variance in yearly growth, so most of what makes one country grow faster than another in a given year lies outside it. Growth also persists within countries from one year to the next in a way the model does not describe. The presence of democracy in the GDP equation is one of the most stable parts of the fit. The form the income term takes is not: $1/G^2$, $G$ and $G^2$ trade places across resamples.

The association between democracy and growth does not depend on the measure. With V-Dem's index, as with Welzel's, democracy enters the GDP equation, and a country at the top of the index grows about 2.2% a year faster than one at the bottom. It did not carry over in time. Refitted to 2007–2024, the democracy term in the GDP equation is about a third of its size in 1981–2006, and the 1981–2006 model predicts yearly changes no better than average changes. Countries also moved away from the level of democracy the model gives for their income, as India's fall in Figure 5 shows. What we can say is that the model describes how democracy and income moved together between 1981 and 2006, not a relationship that held in the years since.

## Limitations

The model pools all countries into one system, so it assumes that two countries in the same state can expect the same change. Differences in institutions, region or natural resources are outside it. Democracy is measured by indices built from expert codings. With a second index the selected terms changed, so the exact form of the equations depends on the measure. Which terms are selected is not stable across samples of countries, especially among the terms in income, which are nearly interchangeable over the observed range. The equations describe how changes varied with levels between 1981 and 2006, and they did not continue to hold from 2007 to 2024. They do not establish what drives what, and they say nothing outside the observed range of income and democracy.

## Disclaimer

This report was written with the help of agentic AI at every stage: importing and describing the data, cleaning it, framing the questions, choosing and fitting the models, producing the figures, and drafting the text. Each step was directed and reviewed by the author, who agreed every method before it was applied, and each number reported here comes from code that can be re-run. The record of what was done, including what was tried and abandoned, is in the appendix.

## Appendix

*A pointer to [Appendix.md](Appendix.md), where the data, the decisions and the full workings are recorded.*

## References

Acemoglu, D., Johnson, S., Robinson, J. A. and Yared, P. (2008). [Income and democracy](https://doi.org/10.1257/aer.98.3.808). *American Economic Review*, 98(3), 808–842.

Acemoglu, D., Naidu, S., Restrepo, P. and Robinson, J. A. (2019). [Democracy does cause growth](https://doi.org/10.1086/700936). *Journal of Political Economy*, 127(1), 47–100.

Barro, R. J. (1991). [Economic growth in a cross section of countries](https://doi.org/10.2307/2937943). *Quarterly Journal of Economics*, 106(2), 407–443.

Barro, R. J. (1996). [Democracy and growth](https://doi.org/10.1007/BF00163340). *Journal of Economic Growth*, 1(1), 1–27.

Barro, R. J. (1999). [Determinants of democracy](https://doi.org/10.1086/250107). *Journal of Political Economy*, 107(S6), S158–S183.

Coppedge, M., Gerring, J., Knutsen, C. H., Lindberg, S. I., Teorell, J., Altman, D., et al. (2025). [V-Dem Country-Year Dataset v15](https://doi.org/10.23696/vdemds25). Varieties of Democracy (V-Dem) Project.

Munck, G. L. and Verkuilen, J. (2002). [Conceptualizing and measuring democracy: evaluating alternative indices](https://doi.org/10.1177/001041400203500101). *Comparative Political Studies*, 35(1), 5–34.

Ranganathan, S., Spaiser, V., Mann, R. P. and Sumpter, D. J. T. (2014). [Bayesian dynamical systems modelling in the social sciences](https://doi.org/10.1371/journal.pone.0086468). *PLOS ONE*, 9(1), e86468.

Ranganathan, S., Spaiser, V. and Sumpter, D. J. T. (2013). [A Bayesian approach to modeling dynamical systems in the social sciences](https://doi.org/10.5220/0004480901250131). In *Proceedings of the 3rd International Conference on Simulation and Modeling Methodologies, Technologies and Applications (SIMULTECH 2013)*, pp. 125–131. SCITEPRESS.

Spaiser, V., Ranganathan, S., Mann, R. P. and Sumpter, D. J. T. (2014). [The dynamics of democracy, development and cultural values](https://doi.org/10.1371/journal.pone.0097856). *PLOS ONE*, 9(6), e97856.

Teorell, J., Dahlberg, S., Holmberg, S., Rothstein, B., Hartmann, F. and Svensson, R. (2015). [The Quality of Government Standard Dataset, version Jan15](https://www.qogdata.pol.gu.se/dataarchive/qog_std_ts_jan15.csv). University of Gothenburg: The Quality of Government Institute.

Welzel, C. (2013). *Freedom Rising: Human Empowerment and the Quest for Emancipation*. Cambridge University Press. [Open-access PDF](https://cambridge.org/de/files/8613/8054/8416/FreedomRising_OA.pdf).

World Bank (2026). [GDP per capita (constant 2015 US$), NY.GDP.PCAP.KD](https://api.worldbank.org/v2/en/indicator/NY.GDP.PCAP.KD?downloadformat=csv). World Development Indicators, release last updated 11 November 2026.
