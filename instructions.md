# Dynamical Systems of Social Data: Collaboration Instructions

This branch, `socio-dynamical-systems`, is for one kind of analysis: country-level social and economic indicators, a dynamical system fitted to how they change from year to year, and a short article reporting it. The user names the variables or a question; the agent proposes the standard analysis below; the two work through it one step at a time. Everything in this document serves that purpose. Rules that would apply to any data analysis are kept only where this kind of work depends on them.

## Workspace

| Location | Purpose |
| --- | --- |
| `Attachments/` | Source data and the papers the method comes from. Never modified. Literature PDFs go in `Attachments/literature/`, which is gitignored. Large or third-party files are gitignored too, with `Attachments/SOURCE.md` saying how to download them and their checksums. |
| `Code/` | Analysis scripts, numbered in run order, and `outputs/`. `sds_common.py` holds the locked figure style, the representative countries and the phase-portrait arrows. The environment files (`setup_env.sh`, `pyproject.toml`, `uv.lock`, `check_env.py`) and `16_export_report.py` arrive with the template. |
| `Report.md` | The short article, built up step by step. |
| `Appendix.md` | The running record: `Data Summary`, `Research Question`, `Analysis` (the workings), `Analysis Log` (a numbered row per step), `Code Summary`, `References`. |
| `Setup.md` | Installing and running the workspace. |
| `Sample Report/` | An earlier finished analysis of another kind, kept to show what complete documents look like. Never edited. |

## Working step by step

The work goes one step at a time, with the user directing each step.

- **One step per request.** Do the step, say what changed and what was found, then stop. Do not run ahead into analysis, figures, findings or prose that were not asked for, even when the next step is obvious.
- **Announce every step.** Say which step is starting and what it involves. When its work is done, do not propose the next one. Ask whether anything is missing from this one, and make the question concrete: list what the step covered, what is settled, what was never discussed, and what the comparison with the sample turned up. Wait for an answer, not an absence of objection. A user who answers one item has not closed the others.
- **From step 3 onwards, compare with a finished example before asking.** Compare the shape, not the content, of the matching part of `Sample Report/Happiness.md`: how captions explain the figure, how much of `Methods` is choices rather than procedure, where a limitation sits. Once this branch has a finished analysis of its own, compare with that instead. Say what the comparison found, including when it found nothing. A difference is not a fault; propose and let the user decide.
- **Stop and ask** when a step turns out bigger than it looked, when the data forces a choice, or when a request is ambiguous.
- **Where a document is yours to write, write it, then say so.** Do not ask first. Tell the user what changed and that they can edit it or ask for changes.
- **Never undo the user's changes.** Re-read a file from disk immediately before editing it. Never revert, reformat or tidy their text. If what you need conflicts with what they wrote, keep theirs and raise the conflict. Stage named files, never everything, and check a commit if a file changed under you.
- **Check what the user writes.** Check each number against the output, each claim against what was tested, and each citation against its source. Quote any error and give the correct value, but leave the change to them. Say plainly when everything is correct.
- **When the user says they are rewriting a document, leave it alone until they say `done`.** Then read the `git diff` as a whole, turn the edits into checkable style rules with before and after examples, add them under `Writing`, and apply them to the rest of the work.
- **The `Disclaimer` is already written and stays.** It says the report was written with agentic AI at every stage. Never remove it, soften it or move it down. If the user rewrites it, keep their wording.
- **No markers for work not done.** A dropped question, an abandoned test or a rejected method leaves the report completely. Record it in the `Analysis Log`.

## Changing this contract

A message beginning **FRAMEWORK** changes this document.

- Apply the change here at once, in a commit of its own that touches no analysis content.
- Apply it to the analysis in progress at the same time, retrospectively where it affects work already done.
- If it conflicts with something already here, say so rather than leaving the contract contradicting itself.
- **Everything stays on this branch.** Nothing is promoted to `main`, and `main` is not touched. One rule (scanning for missing-value codes) went to `main` before this rule was made, and stays there. If a change looks useful for `main`, say so; carrying it across is the user's decision.

## The standard analysis

The user names a question or just a set of variables, and the agent proposes the analysis without asking which model to use. The model is always the same kind: the yearly change in each variable is a polynomial function of the current levels of all of them, pooled over countries and years, selected and fitted as in `Statistical framework`. What changes between analyses is the variables and the data decisions.

The usual analysis asks how a chosen set of variables drive each other's change, using variables not modelled this way before. Replicating a published model is the exception, used to check the method against a known result. The first analysis on this branch replicated Ranganathan, Spaiser and Sumpter (2013) on democracy and GDP per capita.

- **One to four questions.** One is the default. For two variables $X$ and $Y$: *"What model best describes the yearly changes in $X$ and $Y$, and what dynamics does it imply?"*
  - Add a question only where the user wants a separate answer, for example whether $Y$ enters the equation for $X$ at all.
  - Each question says what would count as an answer either way, such as whether the other variable enters each selected equation, and whether nullclines or fixed points exist within the observed range.
- **The proposal, made straight away and recorded in `Research Question` once agreed:**
  1. **Variables.** Each with its World Bank indicator code or other source, its unit, and whether it is a measurement, an estimate or a constructed index.
  2. **Transformations.** Logs for variables spanning orders of magnitude, such as GDP. Rescaling to roughly 0–1 by a fixed constant (see step 1).
  3. **The system.** One equation per variable, $\Delta x_i(t) = x_i(t+1) - x_i(t) = f_i(x_1(t), \dots, x_N(t))$, pooled over countries and years.
  4. **The term library.** For two variables, the 13 terms of Ranganathan, Spaiser and Sumpter (2013): $1, 1/X, 1/Y, X, Y, 1/(XY), Y/X, X/Y, XY, X^2, Y^2, 1/X^2, 1/Y^2$. Remove every term with a variable in the denominator if that variable reaches zero, and say which.
  5. **The search.** Every subset; the best of each size by likelihood; sizes compared by evidence.
  6. **The prior.** The normal prior in `Statistical framework`.
  7. **The checks.** Residual correlation within countries, residual correlation between the equations, and refits on resampled countries.
  8. **The figures.** The standard figures in `Report format`, with the six representative countries named.
- **Two variables is the default.** A third variable uses the 33-term three-variable library, searched up to five terms (Ranganathan et al., 2014). Lagged variables are an extension. Both need the user's agreement.
- **The user agrees the proposal or changes parts of it.** Changes are recorded as departures. Nothing outside this section and `Statistical framework` comes in without agreement.
- **Replications.** The variables, years and library are the paper's, and every departure (data vintage, library, prior) is recorded before anything is fitted.
  - **The report never mentions replication.** It reads as a standalone investigation, because finished reports serve as templates and must show the usual case. The paper is cited only as the source of the method.
  - The paper's equations, what counts as reproducing them, and the comparison all go in `Appendix.md`. Convert the published equations to this analysis's scale before fitting, so the comparison is defined in advance.

## Statistical framework

Inference is by likelihood and Bayesian evidence, following Ranganathan, Spaiser and Sumpter (2013), with unstated details from Ranganathan, Spaiser, Mann and Sumpter (2014). This is fixed. P-values, selection by information criteria alone and machine-learning fits are not used, not even as a check, without the user's explicit agreement.

- **Within a size, models are ranked by likelihood.** Under Gaussian noise this is least squares.
- **Across sizes, models are compared by evidence.** Compute the posterior probability of each size, not only the winner, with every size equally likely beforehand. It goes in the report's `Appendix` tables, not its text.
- **The prior is normal, always,** and the same in every analysis.
  - Each term is divided by its root-mean-square value. The rescaled coefficients are independent normals centred on zero, with standard deviation $\lambda = \text{sd}(\Delta x)$.
  - The noise standard deviation $\sigma$ is fixed at the same $\text{sd}(\Delta x)$ (Ranganathan et al., 2014).
  - The evidence is closed-form, $\Delta x \sim N(0, \sigma^2 I + \lambda^2 X X^\top)$, computed through $m \times m$ matrices. The posterior is Gaussian. Coefficients and 95% credible intervals are on the original scale, and go in the report's `Appendix` tables.
  - Record the selection with $\lambda$ ten times smaller and larger, and with $\sigma$ from the residuals, in `Appendix.md`.
  - A uniform prior was tested in the first analysis (`Code/10_uniform_prior_check.py`). Its evidence depends on an arbitrary range, and the selected democracy model changed at the widest range tried. That is why the prior is fixed.
- **Independence is checked, not assumed.** Each country appears many times.
  - Test the lag-1 correlation of residuals within countries, and the correlation of residuals between the equations. For the latter, an iterated seemingly-unrelated-regressions re-estimate shows whether it matters.
  - Refit on 500 resamples of whole countries, with a fixed seed, to see how often the same terms are selected and how far the coefficient ranges exceed the credible intervals.
  - These go in `Appendix.md`, and in the report only if they change how a result should be read. There are no clustered or robust standard errors on this branch.
- **The dynamics are computed, not read off figures.**
  - Solve each nullcline from the fitted equations, exactly where possible, and check by a second route.
  - Determine stability from the sign of the derivative of the change in each variable with respect to that variable, along its nullcline.
  - Give nullclines a 95% band from 1,000 posterior draws.
  - Step trajectories forward a year at a time, $x_{t+1} = x_t + f(x_t)$, from each country's first observed state.
  - Measure convergence for all countries: the distance to the nullcline at the start against the end, simulated and observed.

## Report format

Every report is a short article in the same format, so reports on different variables can be read side by side.

- **Sections, in order:** Title, `Abstract`, `Introduction`, `Methods`, `Results`, `Discussion`, `Limitations`, `Disclaimer`, `Appendix`, `References`.
- **Length.** About 1,300 words from `Abstract` to `Limitations`, excluding captions, equations, tables and references. The `Abstract` is one paragraph of at most 200 words, and the background at most two paragraphs.
- **`Introduction`.**
  1. The background placeholder, `*Background and prior literature to be added later.*`, replaced in step 6.
  2. Two or three paragraphs on the variables and how they are measured, that the question is one of association, and the approach.
  3. The question, or the questions numbered.

  It never anticipates a result: would the sentence change if the numbers came out differently? Do not open with a sentence about the report.
- **`Methods`** has the sub-headings `Data`, `Model`, `Model selection and uncertainty` and `Dynamics`. The method is described once. Choices get a reason. A weakness of one model goes beside that model. `Methods` describes only what `Results` reports.
- **Explain in words what the model says; put the details in the `Appendix`.** This is the approach of this branch.
  - **`Results`** opens with the figures of the data and how to read them, then one section per question. With one question that section is "The fitted model and its dynamics". It gives the selected equations, then says in words what they mean, for example:
    - which way each variable moves and towards what
    - where change stops, or that it does not
    - whether each variable enters the other's equation
    - which parts of the model are stable across resampled countries
    - whether simulated and observed countries converge.

    Use few numbers, and only those a reader needs, in the variables' own units: "about 2% a year faster", "from about a quarter of the scale in the poorest countries to near the top in the richest".
  - **The report's own `Appendix`** holds the details in compact tables, so that a reader of an exported report has them: for each equation the selected terms, coefficients with 95% credible intervals, the posterior probability of the chosen size against its rival, the number of countries and yearly changes, and how often the terms are selected across resamples; the nullclines at stated levels of the other variable, in its units; convergence counts; and any prediction scores. It ends with a pointer to `Appendix.md` for the full workings.
  - **`Methods` is brief:** what was done and why, not the settings. Priors, $\lambda$, seeds and checks are in `Appendix.md`.
- **Units, always, wherever available,** in figures, captions, text, tables and the abstract. A log or a rescaling is for fitting, not a unit.
  - Plot a logged variable on a log axis labelled in its original units: constant US dollars of the stated base year, with ticks such as \$1k and \$10k.
  - Label an index with its range, for example "index, 0 to 1".
  - In text, give levels in original units, for example "about \$5,000 per person". Coefficients are on the model's scale, with the conversion stated once in `Methods`. For GDP, a yearly change $x$ in $\ln(\text{GDP})/12$ is growth of $e^{12x} - 1$.
- **The standard figures for two variables, in order:**
  1. **Trajectories over time.** One panel per variable against year, with the representative countries as lines. No mean.
  2. **Trajectories in the plane.** All countries in the last year as faint points, and the representative countries' paths with a filled circle at the start. No mean. Same axes as the phase portraits.
  3. **The data phase portrait.**
  4. **The model phase portrait.**

  At most five figures. Evidence and likelihood plots go in the appendix. With three or more variables, the figures may be repeated per pair of variables or per slice, as agreed with the user.
- **Representative countries.** Six, fixed before plotting from metadata and coverage, not from how their paths look. A replication uses the paper's. Each keeps one colour in every figure, and missing years are left as gaps.
- **The figure format is locked,** with the first analysis as the reference: `Code/03_…`, `04_…`, `05_…` and `09_…`, and `Code/sds_common.py`. Only the user changes it.
  - **Style.** Sizes in cm, text 11 pt, legends 10 pt, 300 dpi. Light and dark versions on opaque backgrounds, with a fixed canvas checked after saving. No top or right spines and no background grid.
  - **Colours.** The six-colour palette, one colour per country, in list order.
  - **Axes.** Each axis label names the variable and its unit, for example "GDP per capita (2015 US\$)" or "Democracy (index, 0 to 1)". Figures 2–4 share one fixed range.
  - **Legend.** Off the data, with no frame.
  - **Nothing else in the frame.** The caption carries what is shown.
  - **Phase-portrait arrows.**
    - Changes are averaged over a grid of about 14 by 10 cells over the state (0.04 in log GDP ÷ 12; 0.1 in a 0-to-1 index), and a cell needs at least 10 changes.
    - Each arrow starts at the cell's mean state, marked with a dot, and points along its mean change, drawn at 3⅓ times the yearly change.
    - Any arrow longer than 0.47 cm on the page is shortened to that, with one factor on both components so the direction is exact. Arrows are in the theme's ink.
    - Legend: "Mean change, 3⅓ years (capped)", or "Model change …", on two lines.
  - **Data phase portrait.** It also shows the representative countries' paths, faint.
  - **Model phase portrait.** The model only:
    - model arrows at the same cells
    - each nullcline as a light grey line named "<Variable> nullcline", with a lighter 95% band, drawn only within the observed range and the variable's own scale
    - simulated paths, dashed, in the countries' colours. The dash marks a prediction, in every figure: observed paths are solid, model paths dashed.

    No data: the text points to figure 2 for where countries actually went. A nullcline that does not exist in range is reported in the text.
- **Captions** say what is shown, not what it means. Use `<small><b>Figure n.</b> …</small>`, with HTML (not Markdown) inside. A phase-portrait caption states the arrow length, how many arrows were capped, the minimum per cell, and how many changes are covered. Text before each figure says how to read it.

## The eight steps

Each step is begun only when the user asks for it.

### Step 1: Import and scope the data

- **The World Bank is the standard source.** Take each variable it publishes from the World Development Indicators by indicator code, recording the code, units, base year and download date (which fixes the vintage).
  - Go elsewhere only for a variable the World Bank does not publish. Use the original publisher, or an archived copy if it has been withdrawn, and say why.
  - Use the current release, except in a replication, which may need the paper's vintage, by agreement.
- **Record provenance.** Give the source, date and SHA-256 checksum for every file. Ask whether a fuller or earlier version exists, and record the answer.
- **Describe before judging.** First what the files contain (shape, coverage by year, ranges, oddities), with no conclusions; then whether they can answer the question.
- **Scan for missing-value codes** such as −99, −999 or 9999, and for values outside the documented range. Count them by year and country, and set them to missing.
- **Join on ISO 3166 alpha-3 codes.** Exclude World Bank aggregates; the metadata gives them a blank region. Check historical units (West Germany, Ethiopia before 1993, Czechoslovakia) and duplicate country-years, and list the countries on each side that do not match.
- **Scaling.** Rescale to roughly 0–1 by a fixed, stated constant: 12 for the natural log of a per-capita dollar income, 100 for a percentage or for life expectancy in years. Never use min–max scaling, which makes coefficients incomparable and puts an observation at zero, where inverse terms are undefined.
- **Zeros.** Count zeros and near-zeros in every variable. Where a variable reaches zero, remove the terms with it in the denominator.
- **Interpolated series.** A series published every few years and filled in by interpolation has constructed year-to-year changes. Use it only by agreement, flagged beside the variable. Its modelled changes say nothing about the world.
- **Panel rule.** A change needs both of its years. Use every consecutive pair present, and report how many changes each country contributes.
- **`Data Summary`.** Record provenance, units (a measurement, an estimate or a constructed index), years and countries, missing data and its pattern, every cleaning step with counts, problems accepted as they are, and the transformations. Keep superseded decisions, marked as such. Describe only the data actually used.
- Do not touch `Report.md` in this step.

### Step 2: Frame the question

- **Fix the variables and questions from what the variables mean,** before looking at any relationship between them. No statistics, plots or "just to check" calculations. A question chosen after seeing the data is not tested by it.
- **Agree the proposal** from `The standard analysis`, including the questions and what would count as an answer either way.
- **Record it in `Research Question`:** `Discussion` (how the question was reached, what was set aside, feasibility from the `Data Summary`), `Question`, and the proposal with any departures.
- **Then write the `Introduction`'s framing paragraphs and the question into `Report.md`** without asking first, and tell the user it is there.
- In a replication, the question is the paper's. Its equations, converted to this scale, and the criteria for reproducing them go in the appendix only.

### Step 3: Figures of the data

- **Build the panel first.** One script applies every step 1 decision and writes the counts the captions use, and these must match step 1.
- **Make the standard figures 1–3 in the locked format,** each from its own script that reads the panel and refits nothing. Propose any extra figure before making it.
- **Look at every figure after rendering, and check its size.** Fix overlapping labels, data hidden by the legend, and lines leaving the meaningful range before showing the user.
- **Add each figure to `Results`** with a caption and a sentence on how to read it, without asking first. Remind the user that Obsidian may show the old image until they click away and back.
- **Take every number in the text from the output,** never from a figure.

### Step 4: Fit the model and compute the dynamics

- **Confirm before fitting.** Restate the library, prior and departures, and run only once the user agrees.
- **One script fits any outcome** (`Code/06_fit_change_model.py`), and its checks run alongside: the prior ×0.1 and ×10, $\sigma$ from the residuals, lag-1 residual correlation, and country resampling.
- **Check that each modelled change is measured,** not interpolated or modelled by the source, before interpreting a coefficient on it.
- **Then the joint checks and the dynamics,** as in `Statistical framework`. Draw figure 4 from exported results only.
- **Re-derive the number that carries each claim by a second route:** for example, the evidence from the full $n \times n$ covariance matrix, or a nullcline both exactly and on a grid.
- **Where a variable is left out of an equation, say how firmly,** from the evidence of the best model including it.
- **`Methods`, `Results` and the report's `Appendix` tables are written as the numbers arrive.** `Results` says in words what the model says and stops; the numbers go in the `Appendix` tables. No interpretation, and no words that grade the evidence (striking, reassuring, worrying). Statements of what the analysis can and cannot establish do belong.
- **Appendix only:** a check that changed nothing; diagnostics; alternative specifications; and, in a replication, the comparison with the paper.

### Step 5: Discussion and limitations

- **The `Discussion` interprets the results,** organised by theme. Agree its paragraphs first. Keep what the results support distinct from what they do not.
- **`Limitations` collects what qualifies the findings as a whole.** Examples: pooling all countries into one system, democracy as an expert-coded index, how little of the yearly variance is explained, and selection that varies across resamples. A weakness of one model stays in `Methods` and is not repeated here.
- **No new analysis.** Nothing enters that is not already in `Results` or the appendix. If a count is given ("three limitations"), keep it right.

### Step 6: Background, abstract and title

- **The background replaces the placeholder.**
  - Agree its structure first.
  - Find the sources, read them, and bring them to the user before writing prose.
  - Choose references for their relevance to the findings, but write as if the findings were not yet known. A sentence that would change if the numbers had differed is a result, not background.
  - Leave out a claim that has no source.
- **The abstract is one paragraph, in this order:** the field; the specific question and what is unresolved; the variables, data and method; the results, with any limitation attached to the result it qualifies; one sentence of conclusion.
  - Use words rather than numbers, give the big picture, and cite named prior work.
  - Nothing in it is new, and it contains no method detail.
- **Suggest two or three plain titles** once the abstract is written. The user chooses.

### Step 7: Read through

- **Read the report in one pass, in order, and list what is wrong.** Do not fix as you go.
- **Check:**
  - the question is asked, done, answered and discussed
  - every number against the output, including the descriptive counts from steps 1–2
  - the figure references, and that nothing is orphaned
  - the abstract against the body
  - the references against their sources.
- **Record the outcome in the `Analysis Log`,** even if nothing was found.

### Step 8: Export

- **Before anything, quote the `Disclaimer` in full and wait for the user to confirm they have read it.** Nothing earlier counts. Without confirmation there is no export. Record the confirmation in the log.
- **Ask which format:** Word, PDF, or both. Install only what that format needs.
- **Run `Code/16_export_report.py` from the vault root.** Write the export beside `Report.md`. `Report.md` stays the source of truth; never edit an export.
- **Check the output by reading it back:**
  - captions styled as captions
  - no dropped characters ($\lambda$, ⅓, minus signs)
  - no links into the vault
  - figures on the same page as their captions
  - every section present.

  Do not trust the exit code. Record the tool versions in `Setup.md`.

## When something changes

- **Re-run the pipeline from the changed script onward,** and redraw the figures that depend on it.
- **Sweep both documents** for every number, figure reference and count that depended on the change, in its formatted form as well as its raw one. Re-verify the numbers that did not move.
- **Never hardcode a number in a script's text.** Compute it.
- **Record what moved in the `Analysis Log`,** before and after.

## Code and environment

- **Run Python through the workspace environment:** `cd Code && uv run python <script>.py`. Add a package with `uv add`, and record it in the `Code Summary` and `Setup.md`.
- **Number scripts in run order.** Shared choices live in `sds_common.py`. Figures read exported results and never refit. Fix seeds and record them.
- **Keep the `Code Summary` current:** what each script does, what it reads and writes, and its parameters and seeds.
- **Never invent data, results or citations,** and never put credentials in files.

## Writing

Plain, short, first person plural. Contractions are fine.

- **Say it plainly.** No metaphor and no figurative names for models ("the mirror model" → "a further model").
- **No throat-clearing.** No sentence announcing the next one.
- **No abstract gesturing.** Name the variable and the concrete problem.
- **Split long sentences. Merge one-sentence paragraphs into their neighbours.** No short sentences for emphasis.
- **Nothing bold in `Report.md`** except the figure label in captions.
- **Keep reasoning about alternatives out of the report.** Cut the defence of the road not taken, and asides that no reported number rests on. Both go in `Appendix.md`. Refer back to `Methods` rather than repeating a caveat.
- **A measurement is a choice,** not a definition: "one way of measuring democracy is …".
- **Write each paragraph, list item and table row on one line.** No hard wrapping, and the same for Markdown written by scripts.

A test for any sentence: could a reader disagree with it? If not, cut it.

## References

- **Author–date citations.** Every document that cites anything ends with `## References`, in alphabetical order.
- **Every reference is a link,** to a DOI or URL that resolves. A `403` from a publisher is bot-blocking, not a dead link.
- **Cite the version used:** the data release and download date, and the edition. Verify every detail from the source itself, and never cite a work that has not been opened.
- **A quantity taken from another work keeps its units** (base year, denominator). If the units are unknown, drop the number.
- **Paywalled papers.** Ask the user for a short list of PDFs, save them to `Attachments/literature/` (gitignored), and note in the log which were read in full.
