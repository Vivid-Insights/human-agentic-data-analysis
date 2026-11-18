# [Title]

*Suggested at the end of step 6, once the argument is settled.*

## Abstract

*Written last, in step 6, after every other section is final.*

## Introduction

*Background and prior literature to be added later.*

This is a replication of Ranganathan, Spaiser and Sumpter (2013).

We look at how democracy and national income change together, using two country-level variables between 1981 and 2006. The first is GDP per capita, from the World Bank, in constant 2015 US dollars. We take its natural logarithm and divide by 12, so that it runs from about 0.4 to 1. The second is the citizen rights index of Welzel (2013). It combines Freedom House ratings of political rights and civil liberties with Cingranelli–Richards scores of how far rights are respected in practice, and runs from 0, no citizen rights, to 1. It's one way of measuring democracy, and it is built from expert codings, not measured directly.

Rather than relating the level of one variable to the level of the other, we model the yearly change in each as a function of the current levels of both. The two equations together describe a dynamical system. Each change is written as a sum of terms from a fixed set of polynomials in the two variables. The data choose which terms enter: the best-fitting model is found for each number of terms, and models with different numbers of terms are compared by their Bayesian evidence. All countries are pooled, so we assume that every country follows the same dynamics from wherever it starts. The questions we look at are of association rather than cause. A term in the equation for the change in democracy says how that change varies with income, not that income drives it.

1. How does the yearly change in democracy depend on the current levels of democracy and GDP per capita?
2. How does the yearly change in GDP per capita depend on the current levels of democracy and GDP per capita?
3. What do the two equations imply together: where does change stop, which way do countries move, and do their trajectories converge onto a common path?

## Methods

*Written in step 4, one sub-heading per sub-question, in step with `Results`.*

## Results

*Figures go in as they are produced in step 3; the findings that go with them in step 4.*

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
