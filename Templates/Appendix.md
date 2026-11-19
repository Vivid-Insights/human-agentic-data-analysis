# Appendix

*The running record, filled from the first step. Everything that does not belong in the report belongs here: the workings, the diagnostics, the decisions and what each one cost.*

## Data Summary

*Step 1, covering only the data the analysis uses. For each variable: source and indicator code, download date and SHA-256 checksum, unit, and whether it is a measurement, an estimate or a constructed index. Then: missing-value codes found and set to missing, zeros and near-zeros, the join (unmatched countries, historical units), the scaling constant, the panel rule and the resulting counts. A decision later reversed stays, marked superseded.*

## Research Question

*Step 2, before anything is fitted. `Discussion`: how the question was reached, what was set aside, feasibility. `Question`: the questions, each with what would count as an answer either way. The standard-analysis proposal: variables, transformations, system, term library (with removed terms), search, prior, checks, figures, and representative countries, with any departures.*

## Analysis

*Steps 3 and 4, one sub-heading per question: the best model of each size with log-likelihood, log-evidence and posterior probability; the selected coefficients with intervals; the prior and noise sensitivity; residual correlations; resampling counts; joint checks; nullclines and their second-route check; convergence; prediction scores; and every check that changed nothing.*

## Analysis Log

*A numbered row per step taken, added as the work happens: what was done, what it changed, and where the output is. Superseded decisions stay, marked as such.*

| # | What was done | Output |
| --- | --- | --- |

## Code Summary

*Kept current whenever code changes: what each script does, how to run it, what it reads and writes, and its parameters and seeds. Installation belongs in [Setup.md](Setup.md).*

## References

*Added as sources are cited. Always the last section.*
