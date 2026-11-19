# Session Notes: Building a Specialised Statistical Agent

Notes on how we work, starting from a session on 18 November 2026, written for explaining the method in a video. The analysis record is in [[Appendix]], the rules are in [[instructions]]; these notes are about the working method behind both.

They follow three threads that run through the same exchanges:

1. **Working on the replication problem.** Reproducing Ranganathan, Spaiser and Sumpter (2013) on democracy and GDP per capita: finding the data, reading the papers, deciding what to do with it.
2. **Creating the agent.** Turning a general data-analysis agent into one specialised in a single method: Bayesian dynamical systems on World Bank data, written up as a short article.
3. **Using the replication to make the framework solid.** The replication is a test bed. Every place where the data or the papers forced a decision shows something the framework had not covered, and that becomes a rule. Because the replication has a known answer, the rules are tested against a published result before the agent is used on new questions.

The third thread is what joins the other two, and it is the focus. Section 0 places the threads on the levels of the picture. Section 2 tags each exchange by level. Section 5 lists, item by item, what the replication taught and which rule came from it.

## 0. The levels

![[framework_levels_nested.png]]

The work happens on nested levels, like the dream levels in *Inception*. Every event in the session belongs to at least one of them, and the interesting moments are when something moves between them.

| Level | What it is about | In this session |
| --- | --- | --- |
| 1. The problem | The data and the question in front of us | Democracy and GDP per capita: finding the series, the −99 codes, the zeros, the rescaling |
| 2. How the agent helps | What the agent does inside a step | Reading papers, searching archives, probing files, laying out options with a recommendation, catching errors (including its own) |
| 3. How the framework is organised | The contract that governs the agent | `instructions.md`: the branch rules, `Statistical Framework`, `Report Format`, `The Standard Analysis`, the step rewrites, promotion to `main` |
| 4. How you see the field | The stance on what good analysis is | Social change as a dynamical system; likelihood and Bayesian inference rather than significance tests; a specialised agent rather than a general one; new questions as the usual case and replication as a check |
| 5. Keeping these notes | Watching and recording the other four, so the method can be explained | This document, written for a video |

Level 5 is not in the picture, but it is a level of its own. Writing these notes is work about the work. It changes what gets noticed: an exchange that was routine at level 1 becomes, at level 5, an example of a level-1 discovery becoming a level-3 rule.

Two directions of movement recur.

- **Up the levels.** A problem met in the data becomes a rule in the framework. The −99 codes (level 1) became "scan for missing-value codes" (level 3). The zeros in democracy (level 1) became the rule on inverse terms (level 3).
- **Down the levels.** A view of the field fixes how the framework works, and that constrains what the agent does with the problem. "We always go for this dynamical system" (level 4) became `The Standard Analysis` (level 3). Under it, the agent now proposes a model instead of asking for one (level 2), and the only open choices left are about the data (level 1).

The three threads sit on the levels like this. The replication problem lives on levels 1 and 2. Creating the agent lives on levels 3 and 4. Using the replication to make the framework solid is the upward move between them, and level 5 is where that move becomes visible.

## 1. The starting point

The workspace is a template for data analysis done by a person and an AI agent together. It runs on two ideas.

- **A written contract.** `instructions.md`, imported through `CLAUDE.md`, tells the agent how to work. It sets out eight steps (import data, frame the question, visualise, test, discuss, background and abstract, read-through, export), says which section of the report each step fills, and imposes working rules: one step per request, propose before doing, never undo the user's edits, record every decision with its reasoning.
- **The contract can be changed in conversation.** A message starting with `FRAMEWORK` is an instruction to change the contract itself. The agent edits `instructions.md` immediately, in a commit of its own, and applies the change retrospectively to the analysis in progress. "A rule that only takes effect next time is not in force."

The branch `main` holds the general template. Each analysis lives on a branch of its own. A worked example, a report on happiness and health (`Sample Report/Happiness.md`), shows what a finished report looks like.

The aim of the session was to make a second template: a branch where the agent is specialised to one family of methods, the Bayesian dynamical-systems approach developed by Shyam Ranganathan, David Sumpter and colleagues, and to test it by replicating the first paper in that series.

## 2. Timeline

Each entry gives the prompt as typed, what the agent did, and what came out of it. Commit hashes refer to the `socio-dynamical-systems` branch unless stated.

How the entries sit on the levels in section 0. "→" marks a move between levels.

| Entry | Level | Movement |
| --- | --- | --- |
| 2.1 Creating the branch | 3 | — |
| 2.2 Declaring the specialisation | 4 → 3 | A view of the field ("only a well-defined set of methods") turns into a contract problem: this branch must differ from `main`. |
| 2.3 Choosing (b), bringing in the papers | 3, 2 | The promotion rule is settled at level 3; the agent finds and files the papers at level 2. |
| 2.4 Reading the 2013 paper | 2 → 1 | The agent's reading identifies the problem's open details. |
| 2.5 Committing to the 2013 paper | 2 | The `bdsm` check: the agent finds the method must be rebuilt. |
| 2.6 Finding the democracy data | 1, 2 | — |
| 2.7 Our World in Data | 1 → 3 | A question about one dataset becomes a source rule. |
| 2.8 Reversing the source rule | 4 → 3 | A view of which source is standard replaces the rule. |
| 2.9 Intervals | 4 ↔ 3 | Whether "Bayesian" already covers uncertainty; the independence assumption pulls it back down to the panel data (1). |
| 2.10 Fixing the statistical framework | 4 → 3 | "A Bayesian and likelihood approach is to be kept here." |
| 2.11 Report format; gaps from PLOS ONE | 3, 2 | — |
| 2.12 Data decisions and download | 1, 2 | The −99 codes and the zeros surface here. |
| 2.13–2.15 Inverse terms in the papers | 2 → 1 | Reading the whole series settles a choice about this dataset. |
| 2.16 Two decisions on zeros | 1 | The user's mind changes twice; the record keeps both. |
| 2.17 Turning lessons into rules | 1 → 3 | The clearest upward move: every step-1 detour becomes a rule. |
| 2.18 The central idea | 4 → 3 → 2 | "We always go for this dynamical system" reshapes the contract, which changes what the agent does. |
| 2.19 What goes back to `main` | 3 | Which rules are general and which belong to this specialisation. |
| 2.20 Closing step 1 | 2 | — |
| 2.21 Replication is the exception | 4 → 3 | What the branch is for, in the usual case. |
| 2.22 Notes as a level of their own | 5 | The notes become a level of the work. |
| 2.23 Keeping everything on the branch | 4 → 3 | The specialised agent is cut loose from the general template: nothing flows back. |
| 2.24 Step 2: framing the question | 1, 2 | The first use of `The Standard Analysis`: the agent proposes the model, and the open choices left are about the data. |
| 2.25 A standalone introduction | 4 → 1 | A view of what a report is for: an investigation of the problem, not an account of checking a paper. The replication's criteria move out of the report into the appendix. |
| 2.26 The report as a future template | 4 → 3 → 1 | The finished report will teach the agent by example, so it must show the usual case. That becomes a rule, and the rule strips "replication" from the report. |
| 2.27 Rethinking the standard figures | 1 → 3 | A figure copied from the paper is questioned and replaced. The replacement becomes the standard for every analysis. |
| 2.28 Building the first figures | 1, 2 | The agent builds, looks at its own output, and fixes what it sees before showing the user. |
| 2.29 Seeing it in money | 4 → 3 → 1 | Figures should speak in the reader's units: a rule, applied at once to both figures. |
| 2.30 Locking the format | 4 → 3 | After several rounds of looking and adjusting, the user fixes the figure format as the branch's standard. |
| 2.31 The data phase portrait | 1, 2 | First figure made under the locked format: the agent tunes it against the data's own scale, then checks its shape against the sample report. |
| 2.32 Step 4: the first fit | 1, 2, 4 | The fixed method meets the data. The method was agreed before any fit, the checks were planned in advance, and the replication comparison was kept out of the report. |
| 2.33 Sub-question 2: GDP | 1, 2 | The same script and method on the second equation. The checks find a different kind of problem this time, and say so. |
| 2.34 Sub-question 3: the system | 1, 2 | The two equations become a dynamical system. The agent computes rather than reads off the figure, then compares its shape with the sample report before asking whether step 4 is done. |
| 2.35 Did it replicate? And a simpler Figure 4 | 1, 4 | The user asks the replication question directly, then simplifies the model figure: the model figure shows the model only. |
| 2.36 One results section | 4 → 1 | A view of what this kind of report is: fit the model, look at the dynamics. Three sub-question sections become one. |
| 2.37 One question, a locked model figure, no grid | 4 → 3 → 1 | The simpler shape becomes the rule. A rule about counts (one to four questions) replaces a fixed template (three sub-questions). |
| 2.38 Does the uniform prior matter? | 4 → 1 | The user tests the one place our method departs from the paper. The answer differs by equation, and the agent hands back the decision. |
| 2.39 The normal prior, fixed | 4 → 3 | A sensitivity the user did not want leads to a fixed rule, not a caveat in every report. |
| 2.40 Tidying the contract | 4 → 3 | The specialised agent sheds its general inheritance. What is left is only what this kind of analysis needs. |
| 2.41 Choices given reasons | 2 | The comparison with a finished example turns into two sentences that explain choices, not procedure. |
| 2.42 Step 5: a discussion of growth | 4 → 1 | The user narrows the discussion to one theme. The agent writes it, then compares its shape with the finished example. |
| 2.43 Step 6: background from checked sources | 1, 2, 4 | The one part of the report not from data. Every claim is traced to a source that was actually read, and the user trims numbers and coding detail as a matter of style. |
| 2.44 The abstract | 2 | The one section that must be true of every other: written last, then checked against the body claim by claim. |
| 2.45 A second question: another measure, and the future | 1, 2, 4 | The replication becomes a test bed in a second sense: of the measure, and of time. The model fitted to the past is scored on the years it never saw. |
| 2.46 Say it in words | 4 → 1 | The user's view of what a short article is for overrides a format rule: the report explains, the appendix holds the numbers. |
| 2.47 One visual convention across figures | 3 | A fix to one figure becomes a convention for all: the dash means "model". |
| 2.48 Headings that ask | 4 → 3 | Section headings carry the question in words, so a reader of the report never meets internal numbering. |
| 2.49 Two worlds: before and after 2006 | 4 → 1 | The user brings in what political science knows about the period. The literature places its turning point exactly where our test begins. |
| 2.50 The framing catches up with the work | 4 → 1 | The user reframes the paper as what it really is: replicate, change the data, test prediction. The agent changes the writing, not the analysis. |
| 2.51 The user edits, the agent checks | 1, 3 | The user now writes directly in the report. The agent's job shifts to checking their edits and keeping the contract in step. |
| 2.52 Step 7: the read-through | 2 | Reading the whole report in order catches faults that no section-by-section check could: stale references, a missing index name, a caveat lost between edits. |
| 2.53 Who followed the prediction? | 1, 2 | A question about countries is answered with a rule fixed before the countries are seen. |
| 2.54 The user's eye corrects the rule | 1, 2 | A rule agreed in advance turns out to measure the wrong thing. The user's knowledge of particular countries exposes it, and the revision is recorded as a revision. |
| 2.55 A hypothesis from a table, tested | 1, 2 | A pattern the user noticed in a list is turned into a test with a criterion fixed in advance, and it does not hold. |
| 2.56 The brief, restated | 4 → 3 | The user restates what the project is: a fixed method, flexible questions. What the analysis actually did becomes the standard. |
| 2.57 Making it reusable | 3 | The analysis becomes the template's sample, the contract gains a way in, and the code a map for adapting it. |
| These notes | 5 | Watching all of the above. |

### 2.1 Creating the branch

> I want to start a new branch called socio-dynamical systems

The agent created `socio-dynamical-systems` from `main`. Git branch names cannot contain spaces, so it used hyphens and said so. It pointed out that uncommitted Obsidian settings changes had come along with the switch.

### 2.2 Declaring the specialisation

> FRAMEWORK This branch is going to contain different instructions than the earlier branch. I am going to build agents specifically suited to reading in world bank data, building a dynamical system to describe change in this data and writing a short summarising report. We will keep a lot of the steps but we will only use a well-defined set of methods which we now set up

The agent did not edit yet. It found a conflict in the contract: the promotion rules said every change to `instructions.md` must be copied to `main`, but the point of this branch was to differ from `main`. It offered two options, (a) never promote anything from this branch, or (b) keep framework-specific changes here but still promote general improvements, recommended (b), and asked what the method set should be rather than guessing.

Point for the video: the agent's first move on a contract change was to check the change against the existing contract, and to raise the contradiction instead of resolving it silently.

### 2.3 Choosing (b), and bringing in the papers

> FRAMEWORK 1, Lets do (b) although double check before you change main, this should mainly be a new Instruction set 2, In my Davids Vault folder, I have a series of papers I co-authored with Shyam Ranganathan about this question. Bring these across. We will start by replicating the first of these. Another relevant document is the Happiness report which serves as a template for how we would like to write up and present our work.

- The agent wrote a new contract section, "The `socio-dynamical-systems` template branch": framework-specific changes stay on the branch, general ones are promoted to `main`, and the agent must ask before touching `main`. Commit `693af0d`.
- It searched the user's other vault (`Davids-Vault`), found the papers under `Social dynamics research/Attachments`, read the first page of each to identify it, and copied six into `Attachments/literature/` with author–year names. This folder is gitignored because published PDFs are licensed material.
- It left out a co-authored paper on school segregation as off-topic, and said so.
- It noted the Happiness report was already on the branch as the sample.
- It asked which paper counted as "the first": by date, the 2013 conference paper; by completeness, the 2014 PLOS ONE paper.

The papers:

| File | Paper |
| --- | --- |
| `Ranganathan2013_Bayesian_approach.pdf` | Ranganathan, Spaiser & Sumpter (2013), *A Bayesian Approach to Modeling Dynamical Systems in the Social Sciences*, SIMULTECH |
| `Ranganathan2014_Data_driven_modeling.pdf` | *Data-driven Modeling in the Social Sciences: A pragmatic approach for policy-makers* |
| `Ranganathan2014b_Bayesian_dynamical_systems.pdf` | Ranganathan, Spaiser, Mann & Sumpter (2014), *Bayesian Dynamical Systems Modelling in the Social Sciences*, PLOS ONE |
| `Ranganathan2015a_Dynamical_systems_human_development.pdf` | Ranganathan, Bali Swain & Sumpter, *A Dynamical Systems Approach to Modeling Human Development* (manuscript) |
| `Ranganathan2015b_Democracy_development_traps.pdf` | Ranganathan, Nicolis, Spaiser & Sumpter (2015), *Understanding Democracy and Development Traps Using a Data-Driven Approach*, Big Data |
| `Ranganathan2015c_Demographic_transition.pdf` | Ranganathan, Bali Swain & Sumpter (2015), *The demographic transition and economic growth*, Palgrave Communications |

Later in the session a seventh was added, Spaiser, Ranganathan, Mann & Sumpter (2014), *The Dynamics of Democracy, Development and Cultural Values*, PLOS ONE, with its supporting File S1.

### 2.4 Reading the 2013 paper

> What is in Ranganathan2013_Bayesian_approach.pdf

The agent extracted the full text and summarised it.

- **The idea.** Model the yearly change in each variable as a polynomial function of the current values of all the variables, $dx_i/dt = f_i(x_1,\dots,x_N)$, pooling all countries as different starting points of one shared system.
- **The term library.** For two variables, 13 terms of degree −1, 0, 1 and 2, so $2^{13} = 8{,}192$ candidate models per equation.
- **Two-stage selection.** Best model by likelihood within each number of terms, then compare sizes by Bayesian marginal likelihood (called the "Bayes factor" in the paper).
- **Extra checks.** Seemingly unrelated regressions for correlated errors; pruning for larger models.
- **The application.** Democracy and log GDP per capita, 189 countries, 1980–2006, with the selected models $dD/dt = 0.0003G^2 - 0.4031\,D/G$ and $dG/dt = 0.0246D + 0.0017G - 0.0002G^2$.

It also listed what the paper does not say: GDP units and log base, prior ranges, number of Monte Carlo draws, how terms like $1/D$ behave when democracy is zero, and the number of observations. And it noted the democracy index is not World Bank data.

### 2.5 Committing to the 2013 paper, and proposing the method set

> Lets start with the 2013 article.

The agent checked whether the paper's R package `bdsm` could fill the gaps. It could not: the name on CRAN now belongs to an unrelated 2025 package, and every archived version is that package. So the paper is the only specification, and the method must be reimplemented.

It then proposed a fixed method set, M1–M6: differences and states; the term library; stage 1 (likelihood); stage 2 (evidence); correlated-error check; simulation and phase portrait. It also proposed the standard figures, and asked four questions: whether to add intervals, which democracy data to use, how short the report should be, and how to fill the paper's gaps.

### 2.6 Finding the democracy data

> Can we get the democracy data from Welzel

The agent searched and found that the Quality of Government (QoG) Institute in Gothenburg had republished Welzel's *Freedom Rising* variables. It then probed the files directly.

- The current QoG release (January 2026) has no Welzel columns.
- The archived January 2015 release has them.
- The codebook lists three candidate variables. Only `wel_citrig` (citizen rights) matches the paper: it is on a 0–1 scale and covers 1981–2010. The other two, `wel_edi` and `wel_dr`, start in 1996.
- The coverage start of 1981 also explains why the paper's own Figure 2 starts in 1981 although its text says 1980.

### 2.7 Our World in Data, and the first download

> Yes. And FRAMEWORK Is this data in "Our World in Data". Maybe that would be the best source

- The agent downloaded the QoG 2015 time-series file (66 MB) and codebook into `Attachments/`, with SHA-256 checksums and the date.
- It checked Our World in Data. A search for "Welzel" returned nothing; it validated the search with "democracy", which did return results, so the empty answer was real. OWID's World Bank GDP series turned out to be the purchasing-power-adjusted one, which starts in 1990 and so loses the 1980s.
- It wrote the rule as asked, "check Our World in Data first", but reported that for this replication OWID failed on both variables. Commit `ac980a1`.

### 2.8 Reversing the source rule

> FRAMEWORK Actually, World Bank should be standard.

The agent replaced the OWID rule rather than adding a second rule beside it. The new rule: take every variable the World Bank publishes from World Development Indicators by indicator code, record code, units, base year and download date (since WDI series are revised), go elsewhere only for variables the World Bank does not publish, and in a replication agree whether to use today's version or the paper's. Commit `99a9000`.

It confirmed through the World Bank API that `NY.GDP.PCAP.KD` (GDP per capita, constant 2015 US$) exists and reaches back to 1980.

Point for the video: the user changed their mind within minutes. Because each contract change is its own commit, the reversal is clean and visible in the history.

### 2.9 Intervals and the Bayesian approach

> This interval question? We are going to use a Bayesian approach so that should cover interval estimation?

The agent answered "partly". In the 2013 paper the Bayesian step only chooses the number of terms; the coefficients are least-squares point estimates. Carried one step further, the same prior and likelihood give posterior credible intervals for coefficients and posterior probabilities for model size. The catch is that the likelihood treats every country-year as independent, while each country appears about 25 times. If errors are correlated within a country, the intervals are too narrow. It offered three options and recommended the middle one: report the posterior intervals, and check the independence assumption by testing residual correlation and refitting on resampled countries.

### 2.10 Fixing the statistical framework

> Lets do 2. I want to build about the likelihood approach.
> FRAMEWORK remember that a Bayesian and likelihood approach is to be kept here.

New contract section, "Statistical Framework". Commit `b43d139`.

- Likelihood and Bayesian inference is fixed. Other frameworks (p-values as the basis of a claim, selection by information criteria alone, machine-learning fits) are not substituted, even as a "check", without explicit agreement.
- Maximum likelihood within a model size; marginal likelihood across sizes; report the posterior probability of each size.
- Uncertainty is the posterior credible interval; the prior and how the integral was computed are always stated.
- Independence is checked, not assumed.

The agent found that step 4's rule on clustered standard errors now contradicted this, and resolved it with a note rather than leaving the contract inconsistent.

### 2.11 Report format, and filling gaps from PLOS ONE

> 3. Yes. We want a short article with a consistent format. This is also for FRAMEWORK.
> 4. Yes. Take from PLOS One

New contract section, "Report Format". Commit `f0678c9`.

- All eight steps kept; the report is what is short.
- Fixed sections in the template order.
- About 2,000 words from Abstract to Limitations; abstract at most 200 words; background at most two paragraphs.
- Methods sub-headings fixed: `Data`, `Model`, `Model selection and uncertainty`.
- Results: one sub-heading per sub-question, each giving the equation with credible intervals, the posterior probability of the model size, and the sample.
- Four standard figures: the two variables in one year; the means over time; the data phase portrait; the model phase portrait with trajectories. At most five figures.

The agent read the PLOS ONE paper for the missing details. It settled the democracy index's construction, the World Bank as GDP source, and the noise variance (set to the data variance). It offered two priors, uniform with Monte Carlo or normal $N(0,\lambda^2 I)$ with a closed-form evidence. It also gave the iterated seemingly-unrelated-regressions procedure. It noticed that the PLOS ONE coefficients only make sense if GDP was rescaled to about 0–1, which the paper does not say.

### 2.12 The data decisions, and the download

> Lets do prior range as Normal. It is on a log base. And yes the rescaling.
> Check the zeros. Use countries you have. 13 terms.
> Download data.

- The agent downloaded the World Bank GDP series, checksummed it, and committed it (World Bank data is openly licensed). It gitignored the large QoG file and wrote `Attachments/SOURCE.md` with download instructions and checksums.
- It wrote a describe-only script, `Code/01_describe_data.py`. On its first run the democracy index had a mean of −15.3 on a 0–1 scale. That exposed 852 values of exactly −99, a missing-value code. In 1981–2006, 840 of them fell across 83 countries, unevenly by year, which also explained sudden coverage dips in 2000 and 2002.
- It checked for duplicate country codes from historical units (two Ethiopias, West Germany) and confirmed the join was one-to-one.
- It counted 141 exact zeros in democracy, in 22 countries, and 83 more values below 0.01.
- It wrote the `Data Summary` in `Appendix.md`: provenance, units (and whether each variable is a measurement or a constructed index), what the files contain, and a decisions table. Commit `82ec01f`.

### 2.13 Do the other papers use inverse terms?

> Do the other papers use inverse terms?

The agent read the method sections of all the papers. Every one keeps inverse terms; none says how zeros were handled. The democracy-traps paper (2015b) settled the rescaling, though: log GNI, about 5 to 12, divided by 12.

### 2.14 The 2014 Spaiser paper

> Here is 2014 https://journals.plos.org/plosone/article/file?id=10.1371/journal.pone.0097856&type=printable

The agent downloaded the paper and, by guessing PLOS's URL pattern, its supporting File S1.

- §S12.2 gave the exact construction of the democracy index: Freedom House plus CIRI rights scores, combined by multiplication. That matches the QoG codebook's definition of `wel_citrig`, confirming the series.
- §S12.4 stated the rescaling: divide log GDP by 12.
- Neither the paper nor the supplement says anything about zeros. Commit `13a6959`.

### 2.15 Do the inverse terms survive selection?

> But do the inverse terms ultimately fit well in papers

The agent tabulated every selected equation across the papers. Inverse terms are selected often, for example $D/G$, $1/(CG)$, $1/A$ and $1/L$. But every one divides by a variable bounded away from zero: GDP, child mortality, fertility, life expectancy. No reported democracy equation has $D$ in a denominator. So removing the inverse-$D$ terms would cost nothing any paper reported, while keeping them risks a term being selected to fit a handful of extreme points ($1/D \approx 450$ at the smallest positive value).

### 2.16 Two decisions on zeros

> I think we add 1/2. So 1/(1/2+D)

The agent recorded this: keep all data, and replace $D$ by $D+\tfrac12$ wherever it is a denominator, which bounds $1/(\tfrac12+D)$ between 0.67 and 2. While writing the record it found an error in its own earlier messages. It had said six terms divide by $D$; in fact there are four ($1/D$, $1/D^2$, $G/D$, $1/(DG)$). The user interrupted the correction:

> Actually, I decided to drop 1/D

The agent recorded the new decision: keep all observations, remove the four inverse-$D$ terms, giving a 9-term library and 512 models per equation. The $D+\tfrac12$ decision stays in the record marked superseded, as the contract requires. It flagged its reading that "drop 1/D" means all four terms and asked to be told if only $1/D$ was meant, and it corrected the six-versus-four error openly. Commit `7dce731`.

### 2.17 Turning lessons into rules

> Thats good. But What rules are in FRAMEWORK next time we choose data and are there any rules we should drop on this branch.

The agent listed the data rules now in force, then proposed six new ones learned in step 1 and five rules to drop or rewrite, without editing.

New rules proposed:

1. Scan for missing-value codes.
2. Join on ISO codes, excluding aggregates and checking historical units.
3. Rescale by a fixed constant, never by min–max.
4. Count zeros, and remove inverse terms in any variable that reaches zero.
5. Default panel rule: use every pair of consecutive years.
6. A question for the user: how to treat interpolated series.

Rules to drop or rewrite:

- The clustered-standard-error rule.
- The hypothesis-testing language of step 4.
- Step 3's general chart-form rule, now replaced by the standard figures.
- How step 2 works for a replication.
- Noted for later: this replication could become the branch's own sample report.

### 2.18 The central idea

> Looks good. The main thing is that we should be able to specify a question or variables and it suggests what model and method is used. This is the big difference. We always go for this dynamical system¨

This is the defining change. New contract section, "The Standard Analysis". Commit `9252614`.

- The user names a question or a set of variables. The agent proposes the analysis straight away, without asking which model to use. The model is always the same kind; only the variables and data decisions change.
- The proposal has eight fixed parts: variables (with indicator codes and whether each is measured or constructed); transformations; the system of change equations; the term library minus inverse terms in variables that reach zero; the search; the normal prior with $\lambda$ stated; the checks; the figures.
- Two variables is the default. A third variable or lags need agreement.

The same commit added the step 1 rules and rewrote steps 2–4. Step 4 became "Model fitting", the README was updated to match, the standard-error rule was deleted outright, and "where the answer is a null" became "how firmly a variable was left out". The agent then applied the new rules to the analysis in progress: the panel rule, dropping three unmatched units, accepting the coverage dips, and noting that neither variable is interpolated. Commit `ee06f5e`.

### 2.19 What goes back to main

> Scanning missing codes should go on main, but not the ISO codes. Its specific to this example.

- The rule was in a commit mixed with framework-specific changes, so a cherry-pick would have dragged those onto `main`. The agent instead made a fresh one-line commit on `main`, using a separate git worktree so the user's uncommitted files were not disturbed. `main` commit `f014007`, pushed.
- It merged `main` back into the branch with the "ours" strategy (merge `a537e46`), recording the rule as already present so that a later merge cannot duplicate or conflict with it.
- It pushed the branch to GitHub for the first time. Licensed PDFs and the large QoG file were excluded by `.gitignore`.

### 2.20 Closing step 1

> Yes. Ready to go on

The agent logged the closure (commit `660607a`), announced step 2, set out what it would involve, and waited. It raised in advance the one point step 2 has to settle: because GDP is rescaled, "reproducing the paper" cannot mean matching its coefficients exactly. It would mean the same terms, the same signs and the same qualitative phase portrait.

### 2.21 Replication is the exception

> FRAMEWORK So we won't always be doing replication. In the furture we will use this approach to look at dynamic relation between variables

Commit `89d2254`.

- The contract now says the usual analysis is new: how chosen variables drive each other's change. Replication is an occasional check of the method against a known result, and the replication rules apply only during one.
- Default sub-questions for two variables $X$ and $Y$: how the change in $X$ depends on $X$ and $Y$; the same for $Y$; and what the two equations imply together (fixed points, directions of movement, convergence). Each states what would count as an answer either way.
- The current replication was reframed as the method check, and it fits the three default sub-questions directly.

### 2.22 Notes as a level of their own

> I realised I need full notes on what we have done in this session. I am going to use this in a video to explain the method of building a specialised statistical agent. So make full notes.
>
> As you make the notes keep the picture in mind … These are meta levels (think Inception) for how we work. The leeping of these notes is also a meta level
>
> So keep the notes focussed on how we work both with the replication problem, creating the agent and using the replication to set up a very solid specific framework.

The agent wrote this document. Prompted by the picture, it reorganised it around the levels, adding keeping the notes as a fifth level. It then focused the notes on three threads: the replication problem, creating the agent, and using the replication to make the framework solid. Section 5 became the record of the third thread.

### 2.23 Keeping everything on the branch

> FRAMEWORK Lets not make any changes on main at all. Keep it all here.

Commit `bec6a1d`. The contract now says every change stays on `socio-dynamical-systems`: nothing is promoted, and `main` is not touched at all, even for changes that would apply to a general analysis. If something here looks useful for `main`, the agent says so and leaves the decision to the user, outside this branch. This replaces option (b) from 2.3.

The missing-code rule had already been committed to `main` and pushed in 2.19 (`f014007`). The agent did not revert it, because a revert would itself be a change to `main`, and asked the user instead.

> Leave the rule but no more

So `f014007` stays on `main` as the only change this work made there.

### 2.24 Step 2: framing the question

> Yes. Use the intro to frame a question

This was the first run of the standard analysis. The agent did not ask which model to use: the contract now fixes it. It did four things. Commit `49ba4de`.

- **Framed the question from the 2013 paper's introduction:** static regression against dynamic modelling, and the 50-year debate over income and democracy. It quoted the works the paper cites as the paper cites them, marked them unread, and left reading them to step 6.
- **Converted the paper's published equations to our scale.** With $G = \ln(\text{GDP})/12$, the paper's $\Delta D = 0.0003\,G_p^2 - 0.4031\,D/G_p$ becomes $\Delta D = 0.0432\,G^2 - 0.0336\,D/G$, and similarly for $\Delta G$. This uses only the paper's numbers, not our data, so it is allowed in step 2. It turns "same model?" into something checkable. It also confirmed that every term the paper selected is still in the 9-term library.
- **Defined reproduction before any fitting.** The same terms with the same signs counts as reproduced. Coefficients are compared with the converted values via our credible intervals, and reported, not used to decide. For the joint dynamics, the test is an attracting curve from low–low to high–high that trajectories converge onto, with the zero-change curves computed, not read off a figure.
- **Filled in the eight-part proposal,** marking each departure from the paper: data vintage, rescaling, start year, 9 terms, normal prior, the added resampling check, and the added data phase portrait. It then wrote the framing and the three sub-questions into the report's `Introduction`, with the background placeholder first.

### 2.25 A standalone introduction

> I want the introduction to stand alone as if it is an investigation into the problem. So remove the replication statements apart from saying at the start this is a replication of the paper. Make the thing standalone.

The report now reads as an investigation of how democracy and income change together. One sentence at the start says it is a replication of Ranganathan, Spaiser and Sumpter (2013). The replication paragraph and the "is it the dependence they selected" clauses came out of the sub-questions. The criteria for reproducing the paper, and the converted equations, stay in the appendix.

This splits the replication across the two documents. The report answers the substantive question; the appendix holds the check against the paper. The agent raised where the comparison with the paper's equations should appear once results exist, since the report no longer frames it.

### 2.26 The report as a future template

> FRAMEWORK Yes. Put in discussion. I am not intrested in the report about the accuracy of replication because I want to use it more as a template when its done. So it shouldn't mention replication at all or it will confuse the way the agent works.

The message starts by agreeing to put the comparison in the discussion, then says the report shouldn't mention replication at all. The agent took the stronger, later instruction and said so. Contract commit `e44c4df`; report commit `19e8ca4`.

- **New rule:** the report of a replication never mentions replication. It is written exactly as a new analysis would be. The paper is cited only as the source of the method. The paper's equations, the reproduction criteria and the comparison all live in the appendix.
- **The reason is about how the agent learns.** A finished report on this branch becomes an example the agent works from. A report full of "the paper found…" would teach it to frame every question as a replication.
- **Applied retrospectively:** the replication sentence was removed, and the paper is cited once as the method's source.

Step 2 was then closed ("Looks good"), with the reproduction criteria agreed as proposed.

This is the clearest instance so far of the third thread. The replication is used to build and test the framework, and is then made invisible in the product, so the product can serve as a clean template.

### 2.27 Rethinking the standard figures

> Why do we need a mean of each variable as a plot

The agent answered honestly. The mean-over-time figure was in the standard set only because the 2013 paper had one. It answers none of the sub-questions, the paper itself uses it as a foil, and an average shifts as countries enter the data. It suggested dropping it.

> I would like to see trajectories of 6 different representative countries and the mean in a combined figure 1 and 2

The agent offered two readings: (A) each variable over time in its own panel, and (B) paths in the democracy–GDP plane. It recommended (B), because it shares axes with the phase portraits. It proposed the paper's six countries, so they were not chosen from how their paths look. And it proposed a mean over the 84 countries observed every year, so the mean cannot move because countries enter or leave.

> FRAMEWORK Lets keep these as relatively standard figures but we might have more for higher dimensions

Contract commit `cb0119d`. The standard figures are now:

1. trajectories over time
2. trajectories in the plane
3. the data phase portrait
4. the model phase portrait

with these rules:

- **Representative countries:** six by default, fixed before plotting from metadata and coverage, the same countries and colours in every figure, and gaps left as gaps.
- **The mean:** over countries observed in every year, with the count in the caption.
- **Higher dimensions:** with three or more variables, the figures may be repeated per pair of variables or per slice, and the five-figure limit is relaxed.

A figure inherited from the paper (level 1) was questioned, and what replaced it became the standard for every analysis (level 3). The replication supplied the starting point, and the user's judgement improved on it.

### 2.28 Building the first figures

> Yes. Build
>
> Yes. Make them

Commit `2e2e76c`.

- **Two style guides met.** The user's personal graph-style skill (sizes in cm, 11 pt text, a six-colour palette, 300 dpi) and the workspace's `viz_style.py` (light and dark themes, opaque backgrounds) both apply. The agent combined them: the user's sizes and palette inside the workspace themes. The palette has exactly six colours, one per representative country, fixed in a shared module so a country keeps its colour in every figure.
- **A panel script before any figure.** It applies every step 1 decision in one place and writes the counts the captions use. It reproduced the step 1 overlap exactly (3,679 country-years, 184 countries). It also turned up one new fact: 33 of the 141 democracy zeros fall in country-years with no World Bank GDP, so only 108 enter the model.
- **The agent looked at its own figures before showing them.** In Figure 2 the legend covered data, so it was moved outside the axes. "GDP per capita" on the axis hid that $G$ is log GDP divided by 12, so the label now says so. It also checked that the saved images were the sizes requested, as the contract requires.
- **Into the report without asking,** as step 3 requires. A short paragraph says how to read the figures: what a line is, what moving up or right means. The captions say what is shown, not what it means.

### 2.29 Seeing it in money

> FRAMEWORK LogGDP should have units (even if we didn't in the artcile!)
>
> So we see it in money

Contract commit `1446a69`; figures and text `4870ccc`.

- **The rule.** Every variable is shown in units a reader can interpret. A log or a rescaling is a convenience for fitting, not a unit.
  - Logged GDP goes on a logarithmic axis labelled in constant dollars, never "log GDP ÷ 12".
  - An index is labelled with its range.
  - Text gives levels in money; the model's scale is used only where a coefficient is reported, with the conversion stated once in `Methods`.
  - "Even if we didn't in the article" went into the rule as written: it applies even when the source paper had no units.
- **Why it costs nothing.** A log axis in dollars puts every point exactly where the $G$ axis did, because $G$ is linear in $\ln(\text{GDP})$. Only the labels change. The agent checked that $e^{12G}$ gives back the source's dollars to within $4 \times 10^{-10}$, and drew the mean as the geometric mean so it sits where the model's mean state is.
- **The agent looked again after redrawing.** The dollar ticks overlapped and the long axis label was cut off, so it shortened both: \$1k, \$10k, and "GDP per capita (2015 US\$)", with "constant" kept in the captions.
- **Applied retrospectively** to Figures 1 and 2, their captions, the `Results` paragraph (which now explains that equal distances on a log scale are equal proportional changes), and the `Introduction` (GDP's range, about \$160 to \$140,000 per person).

This is the levels in miniature. A detail the 2013 paper skipped (level 1) became a rule for every analysis (level 3), reflecting a view that figures should speak in the reader's units, not the model's (level 4).

### 2.30 Locking the format

> Drop the mean. We don't need it.
>
> FRAMEWORK Lock this format in. Always use units when available

Contract commit `d342dea`; figures and text `bc37ace`.

- **The mean went.** The mean line had replaced a whole figure in 2.27; now it was dropped as well. What remains is six countries, their paths, and the 2006 cross-section.
- **The format is locked.** Figures 1 and 2 and their scripts are now the reference for every later figure on the branch:
  - the user's style inside the workspace themes
  - one fixed colour per representative country
  - dollar log axes with \$1k-style ticks
  - axis labels naming the variable and its unit
  - legends off the data
  - nothing else in the frame.

  Only the user changes it.
- **Units became unconditional:** "always, wherever units are available", in figures, captions, text, tables and the abstract.
- **Applied at once:** both figures redrawn and checked by eye, the paragraph and captions cleared of the mean, and the appendix updated with the earlier mean marked superseded.

This closes a loop that ran through 2.27 to 2.30, showing how the format was found:

1. A figure inherited from the paper was questioned.
2. A replacement was proposed.
3. It was built and inspected.
4. Units were added.
5. A redundant element was removed.
6. The result was locked.

Each round was cheap because the figure existed and could be looked at. Locking it means the next analysis starts from the end of this loop, not the beginning.

### 2.31 The data phase portrait

> Yes. Do it!

Commit `6895d1d`. The user asked for the figure to be made, not proposed, so the agent built it to the design it had described: average yearly change within the cells of a grid, as arrows, on the locked axes, with the six countries' paths kept faint.

- **The first draft failed on inspection.** At 5 years the arrows ran through neighbouring cells, and cells with only 5 changes gave erratic averages. The long legend label had narrowed the axes until the \$50k and \$100k ticks collided.
- **The fix came from the data's own scale, not taste.** The agent measured the cell-average changes (median 0.013 in democracy, 90th percentile 0.044). It chose 2 years, so a large arrow is about one cell high, and at least 10 changes per cell, which keeps 83 cells and 3,289 of the 3,423 changes. Both drafts are in the appendix, with the first marked superseded.
- **A consistency fix spread back.** Figures 2 and 3 now share one fixed GDP range, so they can be laid over each other. This is the same "change one, re-check the others" discipline as the contract's `When Something Changes` section.
- **The user asked for longer arrows with a cap** ("so we can better see the direction"). Commit `a6d6d7f`. Arrows are now drawn at 5 years, and any arrow longer than about one cell is shortened, by one factor on both components, so its direction is exactly as observed. The cap is measured in centimetres on the page, after layout. A side effect showed why the agent checks every render: a longer legend label narrowed the axes, which both re-collided the ticks and changed how many arrows hit the cap. A two-line label fixed both.
- **"Two thirds of length and it is perfect. Put this in FRAMEWORK."** Contract commit `f63c469`; figure and text `3aa572b`. The length and the cap were both scaled by 2/3 (3⅓ years, 0.47 cm), so the same arrows stay capped. The whole arrow recipe is now locked, and it covers the model phase portrait to come: cells, minimum count, length, cap, ink, faint country paths, two-line legend, shared axes, and what the caption must state. The tuning took four renders (2 years; 5 years; 5 years capped; two thirds of that). Locking it means no later analysis repeats them.
- **Then the contract's step 3 check.** Before asking whether step 3 was done, the agent read the sample report's figures and captions and compared their shape with ours, not their content.

### 2.32 Step 4: the first fit

> Yes. Do it
>
> yes

- **Proposal before running.** The agent measured only scales: the spread of the yearly changes, and the typical size of each term. From those it proposed the two open choices, $\sigma$ fixed at the spread of the changes (the 2014 convention) and a normal prior of the same width on rescaled terms. It warned in advance that the GDP terms are nearly interchangeable over the observed range. The user agreed, and only then was anything fitted.
- **One script, both outcomes.** `06_fit_change_model.py` takes the outcome as an argument, so sub-question 2 reuses exactly the same method.
- **Result.** Four terms: $\Delta D = 0.267D - 0.144D/G - 0.118D^2 + 0.0030/G^2$, with posterior probability 0.68 for that size. It is written into `Results` with intervals and sample, and no interpretation.
- **The checks did their job.**
  - Resampling countries showed that the core terms ($D^2$, $D/G$) are nearly always selected while the full four-term set is selected in only 37% of resamples. It also showed intervals about 1.5 times wider than the posterior. Because that changes how the uncertainty should be read, it went into the report as one sentence.
  - Residuals within countries are negatively correlated (−0.14), which is not the kind of correlation that would make the intervals too narrow.
  - A tenfold narrower prior flips the selection to all nine terms. That is recorded in the appendix, not hidden.
- **The replication thread, kept in the appendix.** On the agreed criterion the 2013 model is not reproduced: it has $G^2$, and the selected model does not. Yet the paper's two-term model, imposed on our data, gives coefficients matching the converted published values. Our search simply prefers a richer model, by a log Bayes factor of 16.7. None of this appears in the report.
- **Re-derived independently.** The evidence was recomputed from the full 3,423 × 3,423 covariance matrix and matched to four decimal places.

### 2.33 Sub-question 2: the yearly change in GDP

> paragraph good for now. Go on to 2

Commits `addfae0` and the re-derivation that follows it.

- **Nothing new to agree.** The method agreed for sub-question 1 applied unchanged: the same script, run with `G` instead of `D`.
- **Result.** $\Delta G = 0.00185D + 0.00027/G^2$, with posterior probability 0.75 for two terms.
  - Democracy enters, with a log Bayes factor of 14.9 over the best model without it.
  - The agent converted the coefficient into money as the units rule requires: a country at democracy 1 grows about 2.2% a year faster than one at 0. It added the conversion to `Methods` once.
- **The checks found a different problem from sub-question 1.**
  - Residuals are positively correlated within countries (+0.26): GDP growth is persistent. This is exactly the failure of independence that the `Statistical Framework` says must be checked, not assumed. The country resampling absorbs it, so that is what the report cites.
  - Selection among the GDP terms is unstable (the exact pair in 54 of 500 resamples), as warned before fitting. Democracy's presence is not (492 of 500).
- **A check that changed nothing stayed out of the report.** Errors between the two equations are uncorrelated (+0.011), and seemingly unrelated regressions moved no coefficient by more than 0.1%. It is recorded in the appendix only, as the contract requires.
- **The replication thread.** The paper's democracy coefficient for GDP growth is reproduced almost exactly (0.00194 against a converted 0.00205), and its whole model trails ours by a log Bayes factor of only 1.8. The difference lies in which of the interchangeable GDP terms is chosen. This is in the appendix only.

### 2.34 Sub-question 3: the two equations together

> yes (to the paragraph for sub-question 2, and to a detailed proposal)
>
> yes (to the proposal)

Commit `ef5e28b`.

- **Proposal first, with three choices named:** stepping forward one year at a time (the scale the model was fitted on), a posterior band with the resampled band kept in the appendix, and three additions to the locked figure format: the zero-change curve, its band, and solid simulated paths beside faint observed ones.
- **Computed, not read off.**
  - The democracy curve was solved two ways, on a grid and exactly from the quadratic, and the two agree to $4 \times 10^{-7}$. It rises with GDP (0.27 at \$500, 0.63 at \$5,000, 0.95 at \$50,000) and attracts everywhere in range.
  - GDP growth is positive everywhere (0.3% to 4.1% a year), so there is no point where both changes stop.
- **Convergence as a number, not an impression.** For all 183 countries, the distance to the curve shrinks in simulation for 168 of them, and in the observed data for 104.
- **One render, one fix.** The curve was first drawn over the whole GDP range, rising past the index's maximum of 1. It is now clipped to where it is meaningful, and the clipping is recorded.
- **Shared code for locked formats.** The arrow drawing moved into the shared module so Figures 3 and 4 cannot drift apart. Figure 3 was redrawn to confirm it was unchanged.
- **The replication thread closes.** On the step 2 criteria, sub-questions 1 and 2 are not reproduced term for term, but sub-question 3, the paper's central qualitative claim (an attracting curve from low–low to high–high), is. This is in the appendix only; the report reads as an investigation in its own right.

### 2.35 Did it replicate? And a simpler Figure 4

> Did it replicate
>
> Figure 4 is too messy. Remove the data and just keep the simulated. Call it Democracy nullcline and make it lighter colour

- **The answer came from the appendix, not the report.** Partly. The paper's central qualitative claim replicated: an attracting curve from low democracy and income to high, which countries converge onto. Its exact equations did not. The paper's own equations still fit our data with near-identical coefficients; our search ranks other terms higher, and where GDP terms are concerned it is unstable among near-interchangeable forms. Because the replication thread was kept in the appendix throughout, the question could be answered in full without touching the report.
- **The model figure shows the model only.** Observed paths came out of Figure 4, since they are already in Figure 2. The curve got its proper name, the democracy nullcline, and a lighter colour so the arrows and simulated paths carry the eye. The text now points to Figure 2 for where countries actually went. Commit `4ca1705`.

### 2.36 One results section

> Combine sub-questions 1 to 3 into a single section and simplify. Lets just keep it a simple case of fitting the model and looking at the dynamics

Commit `1d47850`.

- The three `Results` sections became one, "The fitted model and its dynamics": the two equations, their intervals and sample, then what they imply together.
- **Simplified.** Detail that does not change the reading moved out of the report into the appendix: the share of variance explained, which terms the runner-up sizes had, and per-term resampling counts. `Results` went from about 790 words to about 620.
- **What stayed is what the format requires:** the equations, credible intervals, the posterior probability of the chosen size against its rival, the sample, democracy's place in the GDP equation, the nullcline in dollars, and convergence as numbers.
- **A conflict raised, not resolved silently.** The contract's `Report Format` still says one `Results` sub-heading per sub-question, and the `Introduction` still lists three sub-questions. The agent asked whether this simpler shape should become the standard (a `FRAMEWORK` change) and whether the three questions should be merged too.

### 2.37 One question, a locked model figure, no grid

> Yes. Lets just have one question here. I think FRAMEWORK in general can have 1 to 4 questions about variables.
>
> FRAMEWORK Lock this figure although rmove the grid in the background on all figures.

Contract commit `0ca0507`; report and figures `7970a0d`.

- **Questions.** The fixed three sub-questions became "one to four questions about the variables", with one as the default: *what model best describes the yearly changes in X and Y, and what dynamics does it imply?* `Results` has one section per question.
  - The agent did not rewrite every inherited "sub-question" in the general rules. It added one terminology sentence saying what the word means on this branch, and fixed the one rule (the `Introduction`'s numbered list) that assumed several.
- **The model phase portrait is locked.** It shows the model only: arrows in the locked format, a light grey "<Variable> nullcline" with its band, simulated paths from the representative countries, and no data. A nullcline that does not exist in range is reported in text, not drawn.
- **No background grid on any figure.** One line in the shared style turned it off for all four figures at once, light and dark. The figures were redrawn and checked, and their sizes and arrow counts were unchanged.
- **Applied here.** The `Introduction` now states the single question. The appendix keeps the three step 2 sub-questions, marked superseded, because the replication criteria hang on them.
- **Checking its own commit.** `Report.md` had changed on disk mid-edit, so the agent inspected the commit to confirm it had not swept up an edit of the user's.

### 2.38 Does the uniform prior matter?

> I still want to test if the uniform prior might make a difference

Commit `bf740c2`.

- **Stated, then run.** The user asked for a test, not a change of method, so the agent ran it straight away with its choices stated. The first stage (best model of each size) does not depend on the prior, so only the comparison across sizes was redone. No paper gives the uniform range, and with a uniform prior every extra term costs $\log 2a$, so the agent tried three widths: matched to the normal prior's variance, then 10 and 100 times wider.
- **The answer differs by equation.**
  - GDP: the same two terms under every prior.
  - Democracy: the same four terms at the matched and 10× widths. At 100× it switches to the runner-up three-term model, which lacks the $1/G^2$ term. That would make zero democracy a resting state: a country with none would gain none.
- **Handed back, not decided.** Because the result can change the answer, the contract says it may belong in the report. The agent recorded it in full in the appendix and asked the user how to report it, and whether to compute the alternative model's dynamics, without editing the report.

### 2.39 The normal prior, fixed

> OK go back to Normal prior and FRAMEWORK use the normal prior throughout.

Contract commit `006fa5f`.

- **The report did not change**, since it already used the normal prior. The uniform-prior check stays in the appendix, and the alternative model's dynamics were not computed.
- **The contract now pins the whole prior down,** not just "normal with $\lambda$ stated": terms rescaled by their root mean square, $\lambda$ and $\sigma$ both equal to the spread of the observed changes, closed-form evidence, and the tenfold sensitivity recorded in the appendix.
- **It also says why.** With a uniform prior the evidence depends on an arbitrary range, and here it changed the democracy model at the widest range. A reader of the contract can see the rule came from a test, not from habit.
- **A pattern worth naming for the video.** A check that exposed a sensitivity did not end up as a caveat repeated in every future report. It ended up as a fixed choice, with the evidence for the choice kept where it can be found.

### 2.40 Tidying the contract

> FRAMEWORK I want you to tidy through the instructions and take away anything too general. This is very specifically about dynamical systems fixed to social data

Commit `b045975`.

- **Read in full first.** All 512 lines, about 15,600 words, were read before anything was cut.
- **The test for each rule:** does this kind of work (country indicators, yearly changes, a fitted dynamical system, a short article) depend on it?
- **Removed:**
  - the promotion-to-`main` machinery, now one line saying nothing goes to `main`
  - generic chart advice (bar charts for magnitudes and so on)
  - generic statistics advice (paired tests, null results phrased for hypothesis testing)
  - examples quoted from the happiness analysis
  - three catch-all sections that repeated rules found elsewhere: `Working Method`, `Analysis Standards` and `Agent Operating Rules`.
- **Kept, nearly intact:** the standard analysis, the statistical framework (now including how the dynamics are computed), and the locked report and figure format.
- **Rewritten specifically.** The eight steps became steps about this work, for example "Step 3: Figures of the data" and "Step 4: Fit the model and compute the dynamics". The data rules from step 1 are kept, and the writing and citation rules condensed.
- **The result is about 4,500 words,** less than a third of the original.
- **`CLAUDE.md`** now describes the workspace as a template for dynamical systems on social data. The README still describes the general workspace, which the agent left for the user to decide.
- **For the video.** This is the end of the specialisation arc. The agent began as a general data-analysis contract with a specialisation bolted on. It ends as a contract that is only the specialisation, with the general rules kept where the specialisation needs them.

### 2.41 Choices given reasons

> Add the methods suggested

Commit `e02f4bb`.

- **Two sentences, both from the step 4 comparison with the sample report**, which had found that our `Methods` stated procedure where the sample gave reasons.
  - **Why pool:** each country is a different starting point in one shared system, and pooling assumes countries in the same state can expect the same change.
  - **Why resample by country:** GDP growth is persistent within countries (residual correlation +0.26 between consecutive years; −0.14 for democracy), and resampling whole countries carries that dependence into the spread of the coefficients, which the credible intervals do not.
- **The numbers came from the fit output files,** not from memory. The agent searched the files for them before writing.
- **The same term throughout.** `Methods` now says "democracy nullcline", as `Results` and Figure 4 do.
- **Checked the commit again.** `Report.md` had changed on disk, so the agent confirmed that the commit contained only its three paragraph edits.

### 2.42 Step 5: a discussion of growth

> Lets go to step 5
>
> Drop point 1 and just discuss the relationships in growth

Commit `c19e367`.

- **Structure agreed before prose,** as the contract requires. The agent proposed three discussion themes and four limitations. The user dropped the theme of democracy settling towards an income-set level and narrowed the discussion to the relationships in growth.
- **The `Discussion`, two paragraphs.**
  - Democracy is associated with faster GDP growth (about 2.2% a year from 0 to 1), and poorer countries grow faster. The combined range runs from about 4.1% a year in poor, democratic countries to 0.3% in rich ones with no democracy, all in units.
  - The qualifications: association, not cause; about 1% of yearly variance explained; growth persists within countries; democracy's presence in the equation is stable, but the form of the income term is not.
- **`Limitations`, one paragraph:** pooling into one system, an expert-coded democracy index, unstable term selection, and association within 1981–2006 and the observed range. No count is given, so adding an item cannot make one wrong.
- **Everything already established.** Every number was taken from the fit and dynamics output files before writing, and nothing new was computed.
- **Then the comparison with the sample.** The sample's discussion ties its findings to named literature and ends with a "taken together, what we can say is" sentence. Both were offered to the user as possible changes, not made.

### 2.43 Step 6: background from checked sources

> Yes. (to the structure) Yes. It makes sense. We are using that method
>
> This paragraph contains too many numbers. It can be much shorter. Adjust this when you rewrite
>
> Coding details like "−99 are missing" or World Bank indicator NY.GDP.PCAP.KD should be dropped. The data section can be briefer and to the point

Commit `29b8429`.

- **Structure first, sources second, prose last.** Four claims were agreed: the correlation; the dispute over income → democracy; the dispute over democracy → growth; and why modelling changes helps. Candidate sources were named from memory but explicitly marked as unchecked.
- **Every source checked before use.**
  - Bibliographic details came from the publishers' DOI metadata.
  - Each claim was checked against the source's own abstract (Crossref, OpenAlex, and EconPapers where the publisher blocks scripts).
  - The agent wrote down which sources were read only in abstract and which in full.
- **A source dropped rather than cited unread.** Lipset (1959), the classic citation for the modernisation argument, makes the claim only in its body. The full text was not obtained, so the correlation is cited to Acemoglu et al. (2008), whose abstract states it.
- **The background frames, it does not foreshadow.** Barro (1999) also describes democracy adjusting towards a target set by income, close to our own nullcline. The agent flagged this and cited Barro only for "income predicts democracy", because the user had dropped that theme from the `Discussion`. Democracy and growth is written as contested between Barro (1996) and Acemoglu et al. (2019), without lining our result up with either.
- **The user's two style cuts.**
  - The framing paragraph lost its numbers: the GDP range and the model scale.
  - `Methods` › `Data` lost its coding details: the indicator code, the −99 rule, and the range and worked example of the scale conversion.

  The detail went to the appendix and the reference list, where it identifies the series. The report now stands at about 2,020 words, before the abstract.
- **A conflict that resolved itself.** `Report format` still asked for indicator codes in `Data`, and the agent raised whether the cut should become the rule. The user decided the cut had been a mistake ("add it back in parenthesis"). The code went back as "(2026; indicator NY.GDP.PCAP.KD)", the contract stayed as it was, and the reversal is in the log. Raising a conflict instead of silently rewriting the contract gave the user the chance to catch their own over-correction.

### 2.44 The abstract

> yes

Commit `d7cc238`.

- **Written in the contract's order:** the field, the question and what is disputed, the data and method, the results in words, a limitation attached to the result it qualifies, and a closing sentence. It is 180 words, with no numbers beyond the period of the data.
- **Checked claim by claim against the body.** One phrase failed: "the model explains only a small part of the variation in either variable". The report states that only for growth; democracy's share is in the appendix. The phrase was narrowed to "in growth". An abstract may not say anything the report does not.
- **Titles are offered, not chosen.** The title is the user's most visible choice, so the agent offered three plain options: method-first, question-first and findings-first. It recommended question-first, because it makes no claim the reader has not yet seen supported. The user chose it: *How democracy and national income change together*.

### 2.45 A second question: another measure, and the future

> Did this democracy index stop in 2006? … I want to keep it that way. Another question is the 2014 paper the same as the 2013 but with HDI instead?
>
> OK. I wonder if we could add a second research question to this paper? Lets use a different democracy measure and see if the results up to 2006 replicate, but also lets look to see if the model up to 2006 truely predicts what happened the last 20 years? Add this as a new research question and work through all the steps
>
> Yes. Do it all.

Commit `e3e14db`.

- **A gap became a design.** The democracy index ran to 2010, but the report stopped at 2006 with no reason it was allowed to give, since replication cannot be mentioned. The second question turned 1981–2006 into the fit period and 2007–2024 into the test period. The cut-off now has a reason.
- **One round of decisions, then the whole run.** The user asked for steps 1–6 in one go. The agent first checked that a second measure was obtainable (V-Dem, through 2024). It then put the four choices it would otherwise have stopped for in a single message: the measure, the same library, how to judge prediction, and one new figure. Only then did it run. The departure from one step per request is recorded in the log.
- **The pipeline was generalised without changing the past.** The fit, joint-check and dynamics scripts gained a `vdem` option, and the main outputs were re-run and diffed against the old ones. That re-run exposed lines that had been appended to output files by hand and were now lost, so the scripts now write them. A number recorded earlier (the observed GDP range) turned out to be the range of the calculation grid, not the data's, and was corrected.
- **Result 1: the growth association survives the change of measure.** With V-Dem the terms differ, but democracy enters the GDP equation again (log Bayes factor 13), with the same size: about 2.2% a year from the bottom to the top of the index. The democracy nullcline again rises with income and attracts.
- **Result 2: the model does not predict the future.**
  - Year by year, the 1981–2006 model scores slightly below a model that predicts each variable's average change.
  - Refitted on 2007–2024, its coefficients are less than half their earlier size.
  - Countries moved away from the predicted level of democracy rather than towards it; India, for example, fell from 0.72 to 0.40.
  - The key number was re-derived by Monte Carlo before anything was written.
- **The report changed its conclusion honestly.** The abstract now ends: the model describes how democracy and income moved together in one period, not a relationship that held after it. A replication meant to validate the method ended up testing the claim the method makes, and the claim did not survive out of sample.
- **Cost.** The report is now about 3,150 words against a target of about 2,000. The agent flagged this for step 7, rather than cutting on its own.

### 2.46 Say it in words

> Before we read through, lets shorten by two thirds. Many of the results paragraphs contain lots of numbers and data that is unhelpful. Explain in words instead what the models say.

Commit `4e12ff3`.

- **From about 3,150 to about 1,300 words.** `Results` went from about 1,350 words to about 370; the other sections were tightened.
- **The numbers moved, they were not lost.** Intervals, posterior probabilities, resampling counts, nullcline values, convergence counts and prediction scores are all in the appendix. The report keeps the equations and the figures, and says in words what the models do: democracy moves towards a level set by income; growth is faster in democratic and in poorer countries; the model fitted to the past does not predict the future.
- **Rewriting in words was checked like numbers would be.** Three sentences were corrected before committing:
  - the baseline is the *overall* average change, not each country's
  - "survives resampling best" overstated one term against another
  - "clearly" graded the evidence.
- **A format rule now conflicts with the user's wish.** The contract's `Report format` requires intervals, posterior probabilities and counts in `Results`. The agent raised whether the "say it in words" approach should replace that rule.
- **It became the rule.**

  > FRAMEWORK. Good idea. Put details in an appendix and explain what model says in text. This is a new approach for this directory

  Contract commit `7fc25c1`. `Results` explains in words what the model says; the numbers go in compact tables in the report's *own* `Appendix` section. The agent pointed out that `Appendix.md` does not travel with an exported report, so a reader of the Word or PDF file would otherwise never see the details. Three tables: the selected models, what they imply, and the prediction scores. The length target dropped from about 2,000 words to about 1,300. This is the most significant change to the report format: the branch's articles now read as explanations, with the evidence one section away.

### 2.47 One visual convention across figures

> In figure 4 the predition lines should be dashed to match figure 5.

Contract commit `60d6278`; figure and text `66fbb13`.

- Figure 4's simulated paths and their legend lines are now dashed, as the predicted paths in Figure 5 are. The figure was redrawn and checked; its size and arrow counts are unchanged.
- **One request, one rule.** The locked format had said simulated paths were solid. Since only the user changes the locked format, their request was written into the contract as a convention for every figure: observed paths solid, model paths dashed. The caption and reading sentence were updated to say "dashed".

### 2.48 Headings that ask

> FRAMEWORK I don't wangt headers that refer to "Question 2" just write "Did the model predict the future?"

- **The rule.** `Results` headings say in plain words what the section asks; never "Question 2".
- **Applied, with one judgement call.** Question 2 had two parts, so it became two sections: "Does another measure of democracy give the same picture?" and the user's "Did the model predict the future?". The question 1 heading became "What does the model say?", for consistency. The agent said so rather than leaving the first heading in the old style.
- **The numbered list stays where numbering helps.** The `Introduction` still lists the questions as 1 and 2.

### 2.49 Two worlds: before and after 2006

> One thing that is missing here is a stressing of a pre 2006 world and post 2006. The intro too is also about a pre-2000 world. We should add citations about how the world changed post-2012ish.
>
> I have downloaded pdf

- **Sources before prose.** The agent found four candidates on democratic recession and backsliding, checked their details and abstracts, and brought them to the user with draft sentences and where each would go. One of them, Diamond (2015), made its central claim only in the paywalled body.
- **The user fetched the paper, and it was decisive.** Diamond writes that "around 2006, the expansion of freedom and democracy in the world came to a prolonged halt" and that "the world has been in a mild but protracted democratic recession since about 2006". So the literature places the turning point exactly where the replication had (arbitrarily) ended its fitting period. The agent moved the PDF into the gitignored literature folder and quoted the passages in the appendix.
- **The report now has two worlds.** The `Introduction` frames 1981–2006 as the last decades of democratic expansion and 2007–2024 as the democratic recession. The `Discussion` ties the model's failure to predict to that break, saying explicitly "our data cannot say why". The `Abstract` closes: the model describes the expansion, not the recession that followed.
- **The user was editing at the same time.** Their new first sentence of the `Discussion` was found uncommitted, checked against the results, kept as written, and committed with the agent's changes, which was disclosed to the user.
- **Format kept.** The new background passage was merged into an existing paragraph to stay within the two-paragraph limit.
- **For the video.** A design choice made for replication (stop at 2006) turned out, through the user's knowledge of the field, to match a real historical break. The agent could check the citation, but the user supplied the connection.

### 2.50 The framing catches up with the work

> Yes. I am changing the framing of the paper. It is now more a look again at whether the description of increase in democracy we found in the original could predict the future. First we replicate the original study. Then we change data source (to collected data) and then we look at the future prediction based on what we knew from 2006 data
>
> Yes. The data is V-Dem But don't do more replication stuff. Essentially I was just describing what is done. I just want the writing to reflect this

- **A contract conflict was raised before any writing.** The rule "the report of a replication never mentions replication" was the user's own. The agent asked whether this was a one-off or a framework change. It also asked what "collected data" meant, rather than guessing.
- **The user cut the agent's plan back.** The agent had proposed moving the comparison with the paper's equations into the report, and listing every departure from the paper. The user said: just describe what was done. So the writing changed and the analysis did not. One sentence in `Results` says the refit gives the original picture, though the equations differ in form.
- **The paper now tells its real story:** the original description; refit to the same data; a different measure; prediction from 2006. There are three questions, and three headings that ask them.
- **The contract keeps its rule** for new analyses, with this report noted as the exception.
- **A slip, owned.** A later scripted edit failed its own check and changed nothing, but the agent's commit still went ahead and swept in an uncommitted rewrite of the abstract by the user. The agent showed exactly what the commit contained (only the user's text). It then checked that text, as the contract requires, and reported one inaccuracy without changing it: "the original model" was not the model tested on 2007–2024. Afterwards it made the requested edit, citing Diamond in the `Introduction`.
- **For the video.** The specialisation was built by replicating a paper, then hiding the replication so the report could serve as a template. At the end the user decided the replication *is* the story. The framework bent once, explicitly, without being rewritten.

### 2.51 The user edits, the agent checks

> Add (Diamond, 2015) to intro (not abstract)
>
> FRAMEWORK drop the listed three questions

- **By now the user was editing `Report.md` directly,** in parallel with the agent. Each time, the agent found the uncommitted edit, showed it, checked it against the results and the contract, and committed it with a log entry.
  - The user's rewritten `Abstract` called the tested model "the original model". The agent reported this, because the tested model was the V-Dem refit, and left the change to the user.
  - The user's removal of "The questions are about association, not cause." conflicted with the contract's `Introduction` rule. The agent reported the conflict and kept the user's text.
- **The contract followed.** The numbered list of questions is gone: the framing prose states the questions, and the `Results` headings ask them.
- **The title** became the user's choice: *Did the rise of democracy predict its future?*
- **Then one more link in the chain.**

  > FRAMEWORK the results should refer to the appendix

  Each `Results` section now names the `Appendix` table holding its numbers, (Table A1), (Table A2) or (Table A3), so the text in words and the evidence in tables are one step apart. It is written into the contract as a rule.

### 2.52 Step 7: the read-through

> Yes readthrough.
>
> All as suggested

Commits `6a8ec8a` (the list) and the fixes after it.

- **List first, fix later.** The agent read the whole report once, in order, re-derived every descriptive count from the outputs (all correct), checked every figure, table and reference link (none orphaned), and then listed ten faults without touching the text. The user approved all of them.
- **What only a read in order catches.** Every one of these came from edits made at different times, and none was visible inside the section that contained it:
  - "the third question" left pointing at a list the user had since deleted
  - figures captioned "Democracy" in a report that now uses two democracy indices
  - "the original model" for a model that was in fact a refit
  - the association caveat lost from both the `Abstract` and the `Introduction` across two separate user edits.
- **A fix that created a fault, caught at once.** Cutting the Barro (1991) sentence left its reference uncited, so the reference was removed too.
- **Length did not fall.** At 1,562 words the fixes added slightly more than the cuts removed. The agent reported this rather than cutting further unasked.

### 2.53 Who followed the prediction?

> Could we make a list of countries that did roughly follow the predictions and those that didn't
>
> Sounds good

- **Rule before results.** The agent proposed what "roughly followed" means, before computing anything: within 0.1 of the predicted 2024 democracy score, with misses split by direction. The user agreed. Choosing the threshold after seeing the countries would have let it be tuned to a story.
- **The answer is lopsided.**
  - 67 countries followed, mostly long-established democracies.
  - 28 moved the predicted way but further or less far.
  - 73 moved the opposite way, and in every one of them the model predicted a gain in democracy and democracy fell: Turkey, Hungary, Russia, Venezuela, Nicaragua, Mali and others.
  - The model predicted a rise for 153 of 168 countries; democracy fell in 111.
- **Into the report** as three sentences and Table A4, and into the appendix as the full 168-country list.
- **One sentence corrected on checking.** "Most of North America" became "the United States, Canada", because Mexico was in the opposite group.

### 2.54 The user's eye corrects the rule

> India moved in the same direction in only a trivial sense. It vastly overshot the nullcline!
>
> I think we need relative difference. For example Nigeria has a large change predicted and roughly follows it, while Italy had a small increase predicted and decreased. It feels wrong to say Italy followed model
>
> Yes. DO that

- **The agreed rule was wrong, and the user saw why from two countries.** An absolute tolerance (within 0.1) calls a country "followed" whenever the model predicted only a small change, whatever the country then did. That made Italy, which moved the wrong way, "followed". Judging direction from the 2006 value made India's collapse "the predicted direction".
- **The agent proposed, the user chose.** The agent proposed a grouping against the nullcline. The user asked for relative difference instead. The agent then showed the four countries under discussion (Nigeria, Italy, India, Sweden) and used Sweden to show why a pure ratio needs a floor where the model predicts almost no change.
- **Version 3:** stable where the predicted change is below 0.02; otherwise grouped by the ratio of observed to predicted change (opposite, much less, roughly, much more).
  - 35 countries behaved as the model said (roughly as predicted, or stable).
  - 95 lost democracy where it predicted a rise or stability. They include the United States, the United Kingdom, Japan and Italy, with small falls, as well as Turkey, Hungary and Russia.
- **Honesty about revising after the fact.** The thresholds were set after seeing four countries. The appendix says so, keeps version 1 and the unrun version 2 marked superseded, and calls the grouping descriptive, not a test. Nigeria sits exactly on a boundary, and the report does not lean on it.
- **For the video.** A rule fixed in advance protects against cherry-picking, but it can still measure the wrong thing. The defence is not to refuse revision. It is to revise openly, keep the earlier versions, and say what the new rule can and cannot claim.

### 2.55 A hypothesis from a table, tested

> I am intrested to see if maybe Africa did follow the model. Can you use the test to look at that hypothesis
>
> yes

- **Fixed before computing:** which countries count as Africa (World Bank Sub-Saharan Africa plus five North African countries), what "followed" would mean (beats the baseline year by year with a resampled interval above zero, *and* a clearly higher share of followers), and a note that the hypothesis was post hoc, prompted by Table A4.
- **The answer: no.** The democracy predictions for Africa are no better than the baseline (the interval spans zero), and the share of followers is 22% against 21% elsewhere. By 2024 the model is in fact further off for African countries than the baseline is.
- **An observation kept separate from the finding.** The model predicts African GDP growth no worse than the baseline, and growth elsewhere clearly worse. It is recorded as outside the hypothesis, not promoted to a finding.
- **What went in the report, and what stayed out.**

  > The report shouldn't mention it. We should have a discussion summarising these results and listing some countries which did continue as predicted and some that didn't from all over the world.

  The Africa test stays in the appendix. The `Discussion` gained a paragraph naming countries from every region that did and did not continue as predicted. Before writing, all 32 names were checked against their group in Table A4.
- **For the video.** A list invites the eye to find patterns: several African countries sat among the "followers". Turning the impression into a test with a criterion set in advance showed it came from which names stood out, not from Africa as a whole.

### 2.56 The brief, restated

> The length is OK.
>
> FRAMEWORK We have moved a bit away from our original brief. The instudctions should ensure that this project is about fitting dynamical systems to socioeconomic variables. But the questions and discussion can vary a bit. In this case, we compared two types of democracy measure and we split at 2006 to see how the future played out. This is valid inside this project.
>
> The writeup as it stands is good for now. This is what we should aim for in terms of non-technical langauge with full models in appendix. Write this in to your instructions

Contract commit `baef5d5`.

- **Fixed core, flexible questions.** The contract now says plainly that the project is always about fitting dynamical systems to socioeconomic variables, and that the questions and discussion may vary.
- **What the analysis improvised became method.** These are now valid question types, each written in with its method:
  - refitting a published model
  - comparing two measures of one variable
  - hold-out prediction, split at a year with a reason from the subject (2006, after Diamond)
  - grouping countries by the ratio of observed to predicted change, with the thresholds, and the reason an absolute tolerance fails
  - post-hoc looks, kept in the appendix with a criterion fixed in advance.
- **A rule retired, not bent.** "The report never mentions replication" is marked superseded. The finished report now says plainly that it refits the original model.
- **The report becomes the reference.** *Did the rise of democracy predict its future?* is named as the standard for the level of language: non-technical text, equations once, few numbers and in units, full models in the `Appendix` tables, `Results` pointing to them. The length target moved from 1,300 to about 1,800 words to match.
- **For the video.** The specialised agent began with a method set and a replication target. Over the session the user found, by doing, what the reports should look like and what questions are worth asking. The last framework change writes that experience back into the contract, so the next analysis starts where this one ended.

### 2.57 Making it reusable

> FRAMEWORK read through instrcutions now and really make sure we will be able to help people fit dynamical systems in the future.
>
> Also, replace Happiness report with this one as the sample.

Commits `c5a36b8` (sample and templates) and `a8e75d3` (contract and README).

- **The gaps a newcomer would hit.** The agent read the contract top to bottom as a new user would, and named six:
  1. no way in for a new analysis
  2. code written for democracy and GDP with no guide to adapting it
  3. references to "the first analysis" that would go stale
  4. a sample comparison still pointing at the Happiness report
  5. no general rule for grids, axes or countries with other variables
  6. the prediction figure and appendix tables not described as standard.
- **The sample replaced, and proven self-contained.** The analysis was copied into `Sample Report/` and every script re-run from there. All outputs, figures included, came out identical. One apparent failure turned out to be the shell (zsh does not split a variable into words), not the code, and that became a line in the contract.
- **Nothing lost.** The Happiness sample stays in git history. Its uncommitted data was moved out of the vault to a backup folder, not deleted.
- **A way in.** A new "Starting a new analysis" section covers branching from the template, starting from blank documents in `Templates/`, and copying the sample's scripts. A table says, script by script, what to change for new variables. It also flags where the code relies on something specific: the exact nullcline root needs the change to be quadratic in that variable.
- **General rules where there had been democracy-specific ones:** a grid of about 14 by 10 cells over the observed range; log axes in original units for money, linear for indices; the sample's six countries as the default for comparability; the prediction figure and Tables A1–A4 as standard pieces.
- **For the video.** This is the step that turns one good analysis into a tool. The specialised agent's knowledge now lives in three places a newcomer can use: the contract (what to do), the templates (where to write it) and the sample (what good looks like, and code to start from).

## 3. The specialised agent at the end of the session

What `instructions.md` on `socio-dynamical-systems` now adds to the general template:

| Section | What it fixes |
| --- | --- |
| The template branch | This branch is a second template. Every change stays here; nothing is promoted to `main`. |
| The Standard Analysis | Question or variables in, standard dynamical-system proposal out. Eight-part proposal. Two variables by default. Default sub-questions. Usual case is new analysis; replication is the exception. |
| Statistical Framework | Likelihood and Bayesian inference only. Evidence across model sizes, posterior intervals for coefficients, independence checked. |
| Report Format | Short article, fixed sections, about 2,000 words, fixed Methods sub-headings, four standard figures, at most five. |
| Step 1 additions | World Bank as standard source; missing-value codes; ISO joins; fixed-constant scaling; zeros and inverse terms; interpolated series flagged; default panel rule. |
| Steps 2–4 rewritten | Step 2 ends with the standard proposal agreed; step 3 uses the standard figures; step 4 is model fitting. |

What reached `main`: the rule to scan for missing-value codes (`f014007`), before the rule in 2.23 stopped all changes to `main`.

## 4. The replication's data, as decided

| Decision | Choice |
| --- | --- |
| GDP | World Bank `NY.GDP.PCAP.KD`, constant 2015 US$, release of 11 November 2026 |
| Democracy | Welzel's citizen-rights index `wel_citrig` (0–1), from the archived QoG January 2015 release |
| Years | 1981–2006 |
| Countries | All with both variables: 3,679 country-years in 184 countries before the panel rule |
| −99 codes | Set to missing (840 in the period) |
| GDP transform | $G = \ln(\text{GDP per capita})/12$, giving 0.43 to 0.99 |
| Zeros in democracy | Kept. The four inverse-$D$ terms removed, leaving a 9-term library (superseded: the $D+\tfrac12$ shift) |
| Prior | Normal, $N(0,\lambda^2 I)$; $\lambda$ to be set in step 4 |
| Panel rule | Every pair of consecutive years present |
| Dropped | Czechoslovakia and Taiwan (no World Bank GDP); East Germany (no valid democracy values) |
| Accepted as-is | Coverage dips in 2000 and 2002, caused by the source's −99 codes |

## 5. What the replication taught the framework

This is the third thread item by item. Each row starts from something the replication ran into (level 1), records what was decided for this analysis, and gives the rule it became (level 3), so the next analysis meets it already settled.

| What the replication ran into | Decided for this analysis | Rule it became | Where it lives |
| --- | --- | --- | --- |
| The paper's R package `bdsm` is gone; the name now belongs to an unrelated package | Rebuild the method in Python, with the papers as the only specification | The method is written out in full in the contract instead of relying on a package | `The Standard Analysis`, `Statistical Framework` |
| The 2013 paper leaves the prior, noise variance and fitting details unstated | Fill gaps from the PLOS ONE paper (2014) and its sister papers | Name the source paper and its fallback for unstated details | `Statistical Framework` |
| The democracy index is not World Bank data; Our World in Data lacks it; the current QoG release has dropped it | World Bank for GDP, archived QoG 2015 release for democracy | World Bank is the standard source; elsewhere only for variables it lacks; archived copies allowed; a replication may need the paper's vintage | Step 1 |
| The paper reports point estimates only | Posterior credible intervals, plus a check of the independence assumption | Likelihood and Bayesian inference only; uncertainty is the posterior interval; independence within countries is checked | `Statistical Framework` |
| 852 values of −99 in the democracy index; the first summary averaged −15 on a 0–1 scale | Set to missing | Scan for missing-value codes before summarising, counted by year and unit | Step 1 (also committed to `main` in 2.19, before 2.23) |
| Coverage dips in 2000 and 2002 caused by those codes | Accepted as-is and recorded | Covered by counting missing codes by year | Step 1 |
| Historical units share country codes (two Ethiopias, West Germany); the World Bank file includes 48 aggregates | Checked one-to-one; three unmatched units dropped | Join on ISO codes, exclude aggregates, check historical units and duplicates | Step 1, this branch only |
| The rescaling of GDP is unstated in the 2013 paper and found only in a supplement (divide log GDP by 12) | $G = \ln(\text{GDP})/12$ | Rescale by a fixed, documented constant; never min–max, which creates zeros | Step 1 |
| 141 zeros in democracy make four of the 13 terms undefined; no paper says what was done | Remove the inverse-$D$ terms (after first choosing a $D+\tfrac12$ shift, now superseded) | Count zeros in every variable; remove inverse terms in any variable that reaches zero | Step 1, `The Standard Analysis` |
| The sister papers linearly interpolated five-yearly series | Not needed here: both variables are yearly | Flag interpolated series; use them only with agreement | Step 1 |
| Countries have gaps in their yearly records | Use every pair of consecutive years present | Default panel rule | Step 1 |
| The replication's question comes from a paper, but most future questions will not | The replication is treated as a check of the method | Replication rules apply only during a replication; default sub-questions for new analyses | `The Standard Analysis`, step 2 |
| The paper's coefficients use unscaled log GDP, so ours cannot match them number for number | Convert the paper's equations to our scale. Reproduced means same terms and signs; coefficients compared via credible intervals, reported but not decisive; joint dynamics judged from computed zero-change curves | Proposed in step 2, awaiting the user's agreement. A candidate rule for replications: convert the published model to the analysis's scale, and define reproduction before fitting | `Appendix.md` `Research Question` |

### How the agent kept the framework honest while building it

- **It checked each new rule against the old ones.** It found three contradictions and raised each: promotion to `main` against a branch meant to differ; clustered standard errors against Bayesian intervals; Methods sub-headings mirroring Results against the new fixed sub-headings.
- **It corrected its own errors in the open.** It had said six inverse-$D$ terms when there are four.
- **It kept reversed decisions in the record.** OWID-first was replaced by World Bank-first. The $D+\tfrac12$ shift was replaced by removing the terms. Both reversals are visible in the commits and in the appendix.
- **It kept the branches apart.** At first only the missing-code rule went to `main`, and the user ruled the ISO-code rule specific to this example. Then the user stopped all changes to `main` (2.23).

## 6. Themes for the video, level by level

### Level 4: how you see the field

- **A specialised agent embodies a view of the field.** "We always go for this dynamical system" and "a Bayesian and likelihood approach is to be kept here" are not technical settings. They are positions on how social change should be studied, and the agent inherits them.
- **Replication checks the method; new questions are the point.** The first analysis replicates a known result so the method can be trusted before it is pointed at new variables.

### Level 3: how the framework is organised

- **The contract is the agent.** The specialisation lives in a plain document the user can read and edit. Nothing about the agent's behaviour is hidden in a prompt the user cannot see.
- **Specialise by branching.** The general template stays on `main`. The specialised agent is a branch with a rewritten contract. At first, general improvements were to flow back to `main` after asking. In the end the user cut the branch loose: everything stays on it, and `main` is not touched.
- **Change the rules in conversation.** `FRAMEWORK` turns a remark into a rule. Each rule is its own commit, applied retrospectively, so reversing a decision (OWID, then the World Bank) is clean and visible.
- **Keep the contract consistent.** Each new rule was checked against the old ones, and contradictions were raised, not left in place.

### Level 2: how the agent helps

- **Ground the method in the sources.** The method was specified by reading the papers themselves, and the gaps in one paper were filled from its sister papers and supplements, not from the agent's memory.
- **The agent proposes; the user decides.** Every choice that shaped the analysis was put to the user with a recommendation and its cost.
- **Report mistakes, including your own.** The "six inverse terms" error was corrected in the open, not quietly.
- **The end state is a different kind of help.** The user supplies a question or a pair of variables and gets back a complete, standard analysis plan. The agent stopped asking "what model?" and started proposing one.

### Level 1: the problem

- **The data pushes back.** −99 codes, zeros, a renamed R package, an archived dataset, historical country codes. None of these was in the paper, and each needed a decision.
- **Decisions are recorded with their costs, and reversals are kept.** The user changed their mind twice on zeros, and both versions are in the record.

### Level 5: keeping these notes

- **Keeping notes is a level of its own.** Recording the session changes what gets noticed. It turns individual exchanges into examples of movement between levels, and that movement is what the video explains.
- **The upward move is the method.** A specialised agent is built by repeatedly lifting what was learned on the problem (level 1) into the framework (level 3), under a view of the field (level 4) that decides what to keep.

## 7. Where everything is

| Item | Location |
| --- | --- |
| The contract | `instructions.md` |
| The analysis record | `Appendix.md`: Data Summary, Analysis Log, Code Summary, References |
| Source data | `Attachments/worldbank/` (committed); `Attachments/qog_std_ts_jan15.csv` (gitignored; see `Attachments/SOURCE.md`) |
| Papers | `Attachments/literature/` (gitignored) |
| Describe script and output | `Code/01_describe_data.py`, `Code/outputs/01_describe_data.txt` |
| Commit history | `git log 6a53683..socio-dynamical-systems` |

## 8. Where the session stopped

Step 1 of the replication is closed. Step 2 has been announced, not started. Still open:

- the prior's $\lambda$ (step 4)
- what counts as reproducing the paper, given the rescaling (step 2)
- the user's uncommitted Obsidian settings files.
