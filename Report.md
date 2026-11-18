# [Title]

*Suggested at the end of step 6, once the argument is settled.*

## Abstract

*Written last, in step 6, after every other section is final.*

## Introduction

*Background and prior literature to be added later.*

We look at how democracy and national income change together, using two country-level variables between 1981 and 2006. The first is GDP per capita, from the World Bank, in constant 2015 US dollars. It runs from about \$160 to \$140,000 per person. For the model we take its natural logarithm and divide by 12, so that it runs from about 0.4 to 1. Figures show it in dollars on a logarithmic scale. The second is the citizen rights index of Welzel (2013). It combines Freedom House ratings of political rights and civil liberties with Cingranelli–Richards scores of how far rights are respected in practice, and runs from 0, no citizen rights, to 1. It's one way of measuring democracy, and it is built from expert codings, not measured directly.

Rather than relating the level of one variable to the level of the other, we model the yearly change in each as a function of the current levels of both. The two equations together describe a dynamical system. Following Ranganathan, Spaiser and Sumpter (2013), each change is written as a sum of terms from a fixed set of polynomials in the two variables. The data choose which terms enter: the best-fitting model is found for each number of terms, and models with different numbers of terms are compared by their Bayesian evidence. All countries are pooled, so we assume that every country follows the same dynamics from wherever it starts. The questions we look at are of association rather than cause. A term in the equation for the change in democracy says how that change varies with income, not that income drives it.

1. How does the yearly change in democracy depend on the current levels of democracy and GDP per capita?
2. How does the yearly change in GDP per capita depend on the current levels of democracy and GDP per capita?
3. What do the two equations imply together: where does change stop, which way do countries move, and do their trajectories converge onto a common path?

## Methods

*Written in step 4, one sub-heading per sub-question, in step with `Results`.*

## Results

Figures 1 and 2 show the same data in two ways. Figure 1 plots each variable against time. Figure 2 plots the two variables against each other, so that a country's path through the figure is the sequence of states it passed through between 1981 and 2006. In Figure 2, a line moving up is a country becoming more democratic, and a line moving right is a country becoming richer. GDP is on a logarithmic scale, so equal distances are equal proportional changes: moving from \$1,000 to \$2,000 is the same distance as moving from \$10,000 to \$20,000.

![Figure 1](Code/outputs/figures/fig1_trajectories_time.png)

<small><b>Figure 1.</b> Democracy, <em>D</em> (left), and GDP per capita in constant 2015 US dollars on a logarithmic scale (right), from 1981 to 2006. Lines are six countries: Italy, Sweden, India, Chile, Albania and Nigeria. Albania has no observations for 1985–1989, shown as a gap.</small>

![Figure 2](Code/outputs/figures/fig2_trajectories_plane.png)

<small><b>Figure 2.</b> Democracy, <em>D</em>, against GDP per capita in constant 2015 US dollars on a logarithmic scale. Grey points are the 181 countries with both variables in 2006. Coloured lines are the paths of the six countries in Figure 1 from 1981 to 2006, with a filled circle at 1981.</small>

Figure 3 summarises all 3,423 observed yearly changes on the same axes as Figure 2. The plane is divided into a grid of cells, and each arrow stands for the country-years in one cell. It starts at their average position and points along their average yearly change, drawn over 3⅓ years so that its direction is easy to see. The longest arrows are shortened to a maximum length, with their direction unchanged. An arrow pointing up is a cell in which democracy rose on average. An arrow pointing right is a cell in which GDP per capita grew, and because the GDP axis is logarithmic, the arrow's horizontal length is proportional growth.

![Figure 3](Code/outputs/figures/fig3_data_phase_portrait.png)

<small><b>Figure 3.</b> Observed yearly changes in democracy and GDP per capita (constant 2015 US dollars, logarithmic scale), averaged within cells of a grid. Each cell spans a factor of about 1.6 in GDP per capita and 0.1 in democracy. Each arrow starts at the average position of the country-years in its cell, marked by a dot, and points along their average yearly change. Arrows are drawn at 3⅓ times the yearly change, and the 33 longest are shortened to 0.47 cm, with their direction unchanged. Cells with fewer than 10 yearly changes have no arrow; the 83 cells with arrows hold 3,289 of the 3,423 changes. Faint lines are the paths of the six countries in Figures 1 and 2.</small>

## Discussion

*Written in step 5, organised by theme rather than by sub-question.*

## Limitations

*Written in step 5, alongside the discussion. What qualifies the findings taken together, collected in one place.*

## Disclaimer

This report was written with the help of agentic AI at every stage: importing and describing the data, cleaning it, framing the questions, choosing and fitting the models, producing the figures, and drafting the text. Each step was directed and reviewed by the author, who agreed every method before it was applied, and each number reported here comes from code that can be re-run. The record of what was done, including what was tried and abandoned, is in the appendix.

## Appendix

*A pointer to [Appendix.md](Appendix.md), where the data, the decisions and the full workings are recorded.*

## References

Ranganathan, S., Spaiser, V. and Sumpter, D. J. T. (2013). [A Bayesian approach to modeling dynamical systems in the social sciences](https://doi.org/10.5220/0004480901250131). In *Proceedings of the 3rd International Conference on Simulation and Modeling Methodologies, Technologies and Applications (SIMULTECH 2013)*, pp. 125–131. SCITEPRESS.

Welzel, C. (2013). *Freedom Rising: Human Empowerment and the Quest for Emancipation*. Cambridge University Press. [Open-access PDF](https://cambridge.org/de/files/8613/8054/8416/FreedomRising_OA.pdf).
