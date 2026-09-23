# Data Analysis Collaboration Instructions

## Workspace Contract

Use this folder as the single source of truth for the analysis. Keep work in the locations below.

| Location | Purpose |
| --- | --- |
| `Attachments/` | Source data, reference files, exports, and other inputs supplied for analysis. Do not modify originals. |
| `Code/` | All executable analysis code, notebooks and generated outputs. Arrives with the environment (`setup_env.sh`, `pyproject.toml`, `uv.lock`, `check_env.py`) and `viz_style.py`, which carries the figure conventions. Analysis scripts and `outputs/` are yours to add. |
| `Setup.md` | How to install and run the workspace: Obsidian, `uv`, the Python environment, and the everyday commands. |
| `Report.md` | The final report, built up across the steps rather than written at the end: research questions into the `Introduction` in step 2, figures into `Results` in step 3, the `Methods` and `Results` paragraphs in step 4, the `Discussion` in step 5, and the background and `Abstract` in step 6. Nothing enters a section before the step that owns it, and interim workings never enter at all. |
| `Appendix.md` | The running record of the work, written as you go from the first step. Six sections in this order: `Data Summary` (the data actually used), `Research Question` (what is being asked and how that was arrived at), `Analysis` (the workings, one sub-heading per sub-question), `Analysis Log` (a numbered row per step taken), `Code Summary` (a guide to the analysis code), and `References` last. Both documents arrive as templates with these headings and an italic note under each saying when it is filled; replace the note with the content. |
| `Sample Report/` | A finished analysis, kept as an illustration of what the documents look like when complete. Self-contained: its own `Code/` and `Attachments/` beside the two documents. Its source data is not committed, since the publisher gives no redistribution terms; `Sample Report/Attachments/SOURCE.md` says how to download it. Never edited as part of a new analysis. |
| `Sample Report/Analysis Steps.md` | A walkthrough of the sample analysis with the prompts used, for showing someone how the folder works. Not part of a new analysis. |

## Step-by-Step Working

This workspace is for working through a data analysis **one step at a time, with the user directing each step**. It is not for producing a finished analysis in a single pass, however capable you are of doing so.

- **Do one step per request.** When it is done, say what changed, say what you found, and propose the next step. Then stop and wait for direction.
- **Do not run ahead.** Do not add analysis, statistics, charts, findings, conclusions or report prose that were not asked for — even when the next step looks obvious, and even when you can see the whole path to an answer.
- **Stop and ask** when a step turns out to be bigger than it looked, when the data forces a choice between approaches, or when a question is ambiguous. A question is cheaper than unpicking unwanted work.
- **Prefer the smallest honest step.** If asked to load a file, load the file. Describe what is actually there; do not start interpreting it.
- **Say which step you are on, and announce every transition.** When a step's work is finished, say so: name what has been completed, name the step now beginning, and state what that step involves before starting it. Steps must not blur into one another — the user should never have to infer which step you think you are on. If you believe a step is finished and the user has not said so, propose closing it rather than moving on.
- **Answer sub-questions one at a time.** Work through the sub-questions agreed in step 2 in order, and finish one before starting the next. Do not batch them, and do not answer a later one because it happens to fall out of the same code.
- **Agree the method before applying it.** For each sub-question, say what you propose to do and why, name the assumptions it rests on, and get the user's agreement before producing the result. If a method turns out to be unsound once started, stop and say so rather than quietly switching to another.
- **`Report.md` is built up as the work proceeds, not written at the end.** Each step adds only its own part: the research questions in step 2, the figures in step 3, the `Methods` and `Results` paragraphs in step 4, the `Discussion` in step 5, the background and `Abstract` in step 6. Nothing enters a section ahead of the step that owns it, and interim results, workings and observations always go in `Appendix.md` instead.
- **The `Disclaimer` section is already written, and it stays.** `Report.md` arrives with a disclaimer between `Discussion` and `Appendix` saying the report was written with the help of agentic AI at every stage. It is not a placeholder and no step fills it in.
  - Do not remove it, do not soften it, and do not move it further down. If the user rewrites the wording, keep theirs.
  - It is in the template from the start rather than added at the end for the same reason the research questions go in early: a fact about how the document was produced should not depend on anyone remembering to disclose it once the work is done.
- **Do not leave markers in the report for work that was not done.** If a sub-question is dropped, a test abandoned, or a method considered and rejected, take it out of `Report.md` completely. Do not replace it with a note saying it was set aside. *"A fourth question was framed and then set aside without being tested"* reports on the process rather than the findings, and leaves the reader wondering what the answer would have been.
  - This includes the `Introduction`. When a question is dropped after step 2, remove it, renumber the rest, and do not annotate the gap.
  - A sentence or two in `Appendix.md` is the right record, in the `Analysis Log`. That is where a reader who wants to know what was tried and abandoned should look, and it is enough.
- **At the stages where a document is yours to write, write it — do not ask first.** Then say what you changed and invite the user to edit it or to ask you for changes.
- **Never undo the user's changes.** They edit these documents directly, often while you are working.
  - Re-read a file from disk immediately before editing it. Never write from a copy held earlier in the conversation.
  - Never revert, overwrite, reformat or "tidy" text the user wrote. Add alongside it.
  - If what you need to write conflicts with something they have written, keep theirs and raise the conflict.
  - Never restore a document from another branch or an earlier commit without asking — that silently discards whatever they had done since.
  - Stage named files rather than everything, so an unfinished edit of theirs is not swept into your commit.
- **Check what the user has written, and tell them if anything is wrong.** Leaving their text alone is not the same as letting an error stand. When they write or rewrite a section, read it and check it: every number against the generated output, every claim against what was actually tested, every citation against the source.
  - **Report the error; do not quietly correct it.** Quote the sentence, say what is wrong, give the right value or phrasing, and leave the change to them. Silently fixing their prose is a form of undoing it.
  - **Separate an error from a disagreement.** A number that does not match the output is wrong. A claim the analysis does not support is wrong. A phrasing you would not have chosen is theirs, and saying so is noise.
  - **Say plainly when it is all correct.** A check that reports nothing has to be distinguishable from a check that was never run.
- The steps below are the agreed order of work. Announce which step you are on when it is not obvious.

## Changing This Contract

When the user prefixes a message with **FRAMEWORK**, they are changing this document.

- Apply the change to `instructions.md` immediately.
- Apply it to the analysis in progress at the same time, including retrospectively where it affects work already done. A rule that only takes effect next time is not in force.
- Keep the edit to `instructions.md` in its own commit, touching no analysis content, so it can be promoted to the template branch cleanly.
- If the change conflicts with something already written here, say so rather than leaving the contract self-contradictory.

## The Eight Steps

Work proceeds through these steps in order. Each is one or more separate exchanges. **Do not begin a step until the user asks for it**, and do not do a later step's work while carrying out an earlier one.

### Step 1 — Import and scope the data

Get the data in and establish what will be used.

- Put source files in `Attachments/`. Never modify them.
- Record provenance: where the file came from, when, and a checksum. Say why this file and not another, if that was a choice.
- **Ask whether this is the best available form of the data, not merely the most visible.** A publisher's current download page is often not its best file: series get withdrawn, replaced by summaries, or reissued as modelled outputs with the raw values removed. Check what was published previously, and whether an archived copy of a fuller version exists. Record the answer either way, so a later reader can see the question was asked.
- **Describe the file before judging it.** These are two passes and preferably two outputs: what is in the file — shape, columns, units, coverage, completeness, oddities — and then whether it can answer the question. The describing pass draws no conclusions by design. Merged into one, it produces a summary that argues for a decision the user has not yet been asked to make.
- Write the `Data Summary` section of `Appendix.md`: shape, columns and what they mean, coverage, completeness, and anything unexpected.
- **Do not touch `Report.md` at this stage.**
- When the user decides which subset to use, record the decision and its reasoning — then **delete the description of the data that will not be used**. The `Data Summary` documents only the data the analysis will actually use. A brief note of what was excluded and what that costs belongs with the decision; a full description of discarded data does not.

**Every decision taken in step 1 goes in `Data Summary`**, each with its reasoning and what it cost. The test is simple: *could a later step be misled by not knowing this?* If so, record it. At minimum:

| Decision | What to record |
| --- | --- |
| **Provenance** | Where the file came from, when, its checksum, and why this file rather than another. Note it explicitly if the source is not the publisher's live one. |
| **Units** | The unit of every column, and whether it is a **measurement or model output**. A plausible column name is not a unit — check the documentation. |
| **Scope** | Which rows are used, why, what was excluded, and what that exclusion costs. |
| **Missing data** | Whether values are imputed or left missing, and the evidence for the choice. Check whether gaps are systematic before deciding. |
| **Panel structure** | Whether analyses need the same units observed throughout, and what requiring that would cost. |
| **Cleaning** | Every value altered or set to missing, with the reason and the count. Prefer setting known-wrong values to missing over correcting them. |
| **Accepted as-is** | Problems found and deliberately *not* fixed, and why. A known flaw left in place is a decision and must be visible. |

A decision that is later reversed **stays in the record, marked superseded**. The `Analysis Log` should show what was tried and abandoned, not only what survived — a reader cannot judge a choice without knowing the alternatives that were rejected.

### Step 2 — Frame the research question

Agree what is being asked, before looking at what the answer might be.

- **Ask the user what the research question is.** That is the framing to ask for.
- They may well answer with a hypothesis, a hunch, or a claim they expect to hold — that is welcome, and often sharper than a question. Record it in their own terms rather than translating it. "Research question" names the section and the prompt, not a required grammatical form for the answer.
- Discuss how it might be answered, and whether the data can support it.
- **Do not test anything.** No statistics, no plots, no correlations, no group comparisons, no "just to check" calculations.
- **Work from metadata only**: column names, their documented meanings, and the `Data Summary` already written in step 1. Do not look at relationships between variables or compute anything new.
- The reason is bias. This is exploratory work, but a question chosen after seeing which patterns happen to be present is not really being tested — the answer was already known when the question was picked. Committing to the question first is what keeps the later steps honest.
- Brainstorm with the user. If they have no clear idea, suggest candidate questions — still without looking at the numbers, so suggestions come from what the variables *mean*, not from what they happen to show.
- Assess feasibility: is the needed variable present, is coverage adequate, would the data structure undermine the answer, is the question answerable with this file at all.
- Keep it at that level. Do not design specific visualisations or choose statistical tests yet — steps 3 and 4 exist for that.
- Record the outcome in the `Research Question` section of `Appendix.md`, which has three parts: `Discussion` — how the question was arrived at, what was considered and ruled out, and what the data can support; `Question` — the single main thing being asked, specific enough to have a definite answer, phrased as a question or as a hypothesis, whichever the user chose; `Sub-questions` — the separately answerable parts, each naming the variables involved and what would count as an answer either way.
- Write it before anything is tested, so it is on the record that the question preceded the result.
- **Then, before any analysis starts, write the research questions into the `Introduction` of `Report.md`.** Insert a brief text setting out the questions — do not ask permission first. Then tell the user it is there, that they can edit it themselves, and that they can ask you to change it. This is the one thing that enters `Report.md` early: it fixes in the report itself what was asked, before any result is known, so the write-up cannot quietly become a report of whatever turned out to be interesting.
- **The `Introduction` never anticipates its conclusions.** It says what is being examined and how it will be approached. It does not say what was found, and it does not say what the analysis will turn out not to support. Two sentences of this kind were written into an introduction and had to come out: *"Neither approach settles the direction of cause."* and *"As we discuss later, the way the data is constructed limits how far the first question can be taken."* Both are results, moved early.
  - **This holds even when the motive is honesty.** A pointer forward to a limitation feels like candour — it stops the introduction promising more than the report delivers. It is still a finding stated before the reader has seen any evidence for it, and it pre-empts the judgement the reader is entitled to make on reaching the discussion.
  - **Every limitation has a proper place, and it is not here.** In `Methods`, beside the model whose defect it is. In `Discussion`, beside the conclusion it qualifies. Step 5 already requires the second of those.
  - **Naming the approach is not anticipating the result.** *"We ask whether a change in one variable follows the level of the other"* is method, and belongs. *"This cannot establish which came first"* is a conclusion, and does not. The test is whether the sentence would have to change if the numbers came out differently.
- **The `Introduction` has a fixed shape.** In order:
  1. **Background** — one or two paragraphs setting the scene: what is already known about the problem, what is unresolved, and why it is worth asking about, with references. This comes first, because a reader needs the problem before they need the method. Written in step 6, since it needs the literature rather than the data.
  2. **Framing the problem** — two or three paragraphs: what the variables are and how they are measured, whether the question is one of association or of cause, and what approach is taken. Written in step 2, from the framing already agreed.
  3. **The sub-questions**, as a numbered list.
- **Do not open with a sentence about the report.** *"This report examines whether X is associated with Y"* describes the document rather than the problem, and tells a reader nothing they will not get from the sub-questions a few lines later. Open on the question itself — what is unresolved, and why anyone should care that it is.
- **Put the background placeholder in the opening position**, so that the gap sits where the background will go. Use exactly: `*Background and prior literature to be added later.*` Step 6 replaces it.

### Step 3 — Visualisation

Show what the data looks like for each sub-question, before testing it. One sub-question at a time.

- **Propose the chart before making it.** Say what it would plot, on which axes, over which rows, and what a reader would be able to see in it. Get the user's agreement before producing it. A chart is cheap to describe and expensive to argue about once it exists.
- **Let the data's job choose the form.** Comparing magnitudes across categories is a bar chart; a relationship between two continuous measures is a scatter; movement over time is a line; a distribution is a histogram. Choose from what has to be shown, not from what is easiest to produce.
- **Plot the observations before the model.** The data goes in first and the fitted line or curve on top. A figure showing only a fit hides how well it describes anything.
- **When the orientation is genuinely open, produce both and let the user choose.** If it is not obvious which variable belongs on which axis, or which should define the contour lines, make each version rather than arguing for one. Say which you would keep and why. The test is which version makes the claim in the accompanying paragraph visible: a figure whose axes hide the effect the text asserts is the wrong figure, however correct its numbers.
- **One script per figure**, writing to `Code/outputs/figures/`, reading only from the cleaned data or from exported model coefficients. A figure must never refit a model that is reported elsewhere, or it can drift from the numbers in the text.
- **Once the data the plot will use is settled, add the plot to `Results` in `Report.md`.** Do not ask first. Number the figures, give each a caption saying what it shows, and put it in the report as soon as it exists.
- Then tell the user it is there and that they can decide whether to keep it. A plot is easier to judge in the report, at the size and in the place a reader will meet it, than as a file in `Code/outputs/`.
- **Number figures in the order they appear.** If one is dropped or inserted, renumber the rest and update every reference to them in both documents.
- Caption what the figure shows, not what it means. Interpretation is step 5.
- **Set captions in a smaller font than the body text**, so a reader distinguishes figure legend from argument at a glance. Wrap the caption in `<small>…</small>`.
- **Do not put Markdown inside inline HTML.** Obsidian does not parse it, so `<small>**Figure 1.**</small>` renders with the asterisks visible. Use HTML tags inside the HTML: `<small><b>Figure 1.</b> …</small>`, and `<em>` where italics are wanted.
- **Explain how to read the figure in the text where it is not self-evident.** A reader who cannot tell what one point represents, or what the difference between the lines is, cannot check the claim being made from it. Say what a single point is, what each line is, and what feature of the picture carries the result.
- **Make the type big enough to read at the size the figure appears in the note.** Obsidian scales an embedded image down to the width of the pane, so labels that look right in the raw file are often unreadable in the report. Size axis labels, tick labels and legends generously relative to the figure, and judge them in the rendered note rather than in the file.
- **Assign a colour to a variable, not to a rank.** A variable keeps its colour across every figure in the report, and a series never takes the colour of the position it happens to occupy. Otherwise adding or dropping one series silently repaints the others, and two figures side by side contradict each other about what blue means. Keep a neutral grey for residual and "other" terms.
- **Give figures an opaque background, and generate a variant for each theme the documents are read in.** A transparent background inverts with the reader's theme and takes the labels with it; a light-only image is unreadable in a dark vault. Produce both and embed the one matching the document's default.
- **Put nothing on the figure but its title, axes, legend and data.** No subtitle, no description block, no explanatory note inside the frame. The caption below carries what the figure shows and the surrounding text carries the argument; repeating that inside the image duplicates it and crowds the plot.
- **Tie every label to the thing it names.** A label sitting near a point but not joined to it floats free, and the reader cannot tell which point it belongs to. Use a leader line, and mark the labelled point so the target is visible. Keep labels inside the axes.
- **Watch for the figure growing to fit its own text.** Saving to a tight bounding box expands the canvas around anything that overruns it, so a long note or a label near the edge silently widens the image — and everything in it then renders smaller once the image is scaled to the pane. Check the output's dimensions are what you asked for.
- **Take every number in the text from the computed output, never from the figure.** Reading a value off a plot is the most reliable way to get a wrong number into prose, and it is invisible to a reader who trusts the figure.
- **When a figure is regenerated, remind the user that Obsidian may still show the old image.** It caches the rendered file, so clicking away to another note and back refreshes it. Without that they may judge a figure they have already asked you to change.
- If the user drops a figure, remove it from `Results` but leave the script and the generated file in place — the working stays in `Appendix.md` and `Code/outputs/` regardless.

### Step 4 — Statistical tests

Answer each sub-question with a number and an interval. One sub-question at a time.

- **Propose the test before running it.** Name what it estimates, the assumptions it rests on, and whether this data meets them. Get the user's agreement, then run it. If a method turns out to be unsound once started, stop and say so rather than quietly switching to another.
- **Check the assumptions against the data rather than asserting them.** An assumption named and not checked is worse than one not mentioned, because it reads as though it were verified. If a test assumes independent samples and the observations are paired, it is the wrong test: say so and name the paired equivalent.
- **Establish that the outcome is a measurement before interpreting any coefficient on it.** A series the source has interpolated, extrapolated, forecast or modelled is not an observation. Differencing such a series returns the gradient of the construction, not a measured change. Check this before the fit rather than after, because it determines what a coefficient could mean: a null on a constructed outcome follows from how the series was built and says nothing about the world.
- **Use standard errors that match the structure of the data.** Cluster them where observations repeat within a unit; use heteroscedasticity-robust errors where the spread varies with the predictor. Say which was used and why.
- **Report the estimate, its uncertainty, and the sample it came from.** A coefficient without an interval is not a result, and an interval without the number of observations behind it cannot be judged.
- **Where the answer is a null, say what the test was able to detect.** Report that as a fact about the data — how much the outcome varies, and over how many observations — and let the reader weigh it. Do not characterise the null itself.
- **Re-derive the number that carries the claim, independently, wherever that is cheap.** Solve the equation from the coefficients rather than reading the value out of a generated table. Two routes to the same figure catch both arithmetic slips and stale output; one route catches neither.
- **Every number in the report comes from the generated output.** Never from memory, never read off a figure, never carried over from an earlier version of the analysis.
- **Write the finding as a short paragraph in `Results`.** One paragraph per sub-question, added as soon as the numbers exist.
- **Keep `Methods` in step with `Results`, using the same sub-headings in the same order.** When a sub-question gets a paragraph in `Results`, it gets one in `Methods` at the same time. The two sections are written in parallel, so a reader can move between what was done and what was found without hunting.
- `Methods` says what was done and why that choice; `Results` says what came out. Sample definition, model, and the choices a reader needs to reproduce or challenge the number belong in `Methods`, not in the result paragraph.
- **`Methods` describes only what `Results` reports.** If a diagnostic, statistic or robustness check does not appear in `Results`, it does not appear in `Methods` either — it goes in `Appendix.md`. Naming a test in `Methods` and never reporting its outcome leaves the reader hunting for a result that is not there.
- **Keep the report clean.** It should read as an argument, not a technical log. Diagnostic values, alternative specifications, and anything computed but not used belong in the appendix, however much work they took. A test may produce a page of statistics; the report takes the one number that answers the question.
- **Do not write up a check that changed nothing.** If something was queried, investigated, and the method and result stayed as they were, record it in the appendix and leave it out of the report entirely — not even in `Methods`. The report explains the choices that shape the reported numbers, not every alternative that was examined and found equivalent. A user asking a question in conversation is not a request for a paragraph in the report.
- **Keep it short and to the point, and tie it to the sub-question it answers.** Name the sub-question, give the estimate with its uncertainty, and stop. Do not restate the method, do not narrate the process, and do not interpret — step 5 does that.
- Full workings, diagnostics and anything that did not make the paragraph go in `Appendix.md`.
- **Do not grade the evidence.** Report what was found and what it cannot support; do not tell the reader how to weigh it. *"This null is uninformative rather than reassuring"* is a judgement. *"The outcome varies little within units, so the test has little power to detect an effect of this size"* is a fact the reader can judge for themselves. Avoid words that score evidence — reassuring, striking, worrying, encouraging, damning, impressive, remarkable.
  - Statements about what an analysis *can and cannot establish* are different, and belong: they are claims about inference, not about how to feel. "This cannot distinguish the direction of causation" stays.
  - The user makes the normative calls. Give them the magnitudes, the intervals and the limitations.
- **No emphasis in `Results`** — see the document-wide rule under `Writing`. Emphasis tells the reader which numbers matter, which is the reader's judgement to make.

### Step 5 — Conclusions and limitations

Write the `Discussion` section of `Report.md`.

- Interpret what the results support, and state plainly what they do not. Keep the two distinguishable in the reader's mind.
- **Organise by theme, not by sub-question.** Results are reported sub-question by sub-question; a discussion earns its place by drawing them together. Agree the paragraph structure with the user before writing.
- **Put each limitation beside the conclusion it qualifies**, not in a list at the end where it can be read past.
- **No new analysis.** If a question arises that needs computing, say so and stop — that is a new step, not part of this one.
- Interpretation belongs here; that is what the section is for. Grading the evidence still does not. Say what the data supports and what it cannot; do not tell the reader how much to be impressed.
- Nothing enters the `Discussion` that is not already established in `Results` or `Appendix.md`.

### Step 6 — Background and abstract

By this point `Report.md` holds everything but these two. Steps 2 to 5 have put in the research questions, the figures, the `Methods` and `Results` paragraphs and the `Discussion`. Step 6 adds the background and the `Abstract`, and nothing else — if a section still looks unfinished, that is the earlier step's work to complete, not this one's.

**Help the user write the background.** It replaces the `*Background and prior literature to be added later.*` placeholder, and it is the one part of the report that does not come out of the analysis, so it cannot be written from the data.

- **Do not write it alone from memory.** Everything else in the report is checkable against the generated output. A background is checkable only against the literature, and a plausible-sounding sentence about what a field has found is the easiest thing in the document to get wrong.
- **Propose the structure first and agree it.** Say which claims the background needs to establish for the research question to make sense, and in what order. Usually a handful: what the outcome measure is and why it is taken seriously, what is already known about the relationship being tested, and what remains open — the gap the report addresses.
- **Then find the sources and read them.** Search, open what the search returns, and take the claim from the source rather than from the abstract or from what you expected it to say. The rules in `References and Citation` apply in full: verify every bibliographic detail, check every link resolves, and never cite a work you have not opened.
- **Bring the user the sources before the prose.** Say what each one establishes and let them judge whether it belongs, whether it is the right authority, and whether they know a better one. They may well know the literature better than the search does.
- **Choose the references for their relevance to the findings; write the text as though the findings were not yet in.** These pull in opposite directions and both matter. Knowing how the analysis came out is what tells you which literature is worth citing — a background assembled before the results is padded with work that turned out to be beside the point. But the prose must not carry the results, by statement or by implication.
  - Cite the paper whose question the analysis ended up answering. Do not write a sentence that only makes sense to someone who already knows the answer.
  - *"Whether the association survives adjustment for the main confounder has been contested (…)"* frames the question. *"The confounder accounts for much of the apparent effect (…)"* announces the result and does not belong, even with a citation attached to it.
  - The test from step 2 applies here too: would the sentence have to change if the numbers had come out the other way? If so it is a finding, not background.
- **The background explains why the questions were worth asking**, and the questions were fixed in step 2 so that the report could not drift toward whatever turned out to be interesting. Keep that protection: the background motivates the questions as asked, it does not quietly restate them to fit the answers.
- **Mark what could not be supported.** If a claim the structure needs turns out to have no source behind it, say so and leave it out rather than softening it into something vague enough to pass. A gap the user can see is worth more than a sentence they cannot check.

**Write the `Abstract` last**, once the background is settled and every other section is final.

- **It is the one place that states the findings up front.** The rule against anticipating conclusions governs the `Introduction`; the abstract exists to give the answer before the argument, so the two are not in conflict.
- **Follow this order, roughly a sentence to each.** One paragraph.
  1. The field in general — what kind of question this is.
  2. Narrowing to the specific question, and what is unresolved about it.
  3–4. The research questions, and the data and method that answered them.
  5–6. The results. A limitation belongs here too, attached to the result it qualifies rather than held back — a null that follows from the data rather than from the world is reported alongside the null, not after it.
  7. A closing summary: what the reader should take away, in one sentence.
- **Short sentences, to the point, no fluff.** Every sentence carries a fact, a finding or a limitation. A sentence that only announces what the next one will say comes out. So does any adjective that would survive the results being different.
- **Avoid numbers.** State the direction and the rough size of what was found in words — *"about half the association remains once income is accounted for"* — and leave the estimates and intervals to `Results`. An abstract is read to decide whether to read the report, and a reader deciding that does not need three decimal places. Sample sizes, test statistics and confidence intervals do not belong here at all.
- **Suggest a title once the abstract is written.** By then the report's argument is settled, which is the first point at which a title can describe it. Offer two or three, say what each puts first, and let the user choose — a title is the most visible authorial choice in the document and it is theirs. Keep them plain and literal; a title that states the subject is more use than one that is memorable.
- **Nothing in it is new.** No figure reference, no finding that is not in `Results`, no caveat that is not in `Discussion`. If writing the abstract turns up something the report should have said, put it in the section it belongs to and then summarise it.
- **Name the prior work you refer to.** *"Earlier work has found that…"* leaves the reader unable to check it or to know which literature is being disputed. Cite it: `Deaton (2008)` or `(Deaton, 2008)`. This is the one place a citation belongs in an abstract, and it comes with the usual obligation to state what that work actually found — including which measure was the outcome and which the predictor, since those are easy to swap round.
- **No method plumbing.** Which section answers which question, what the source file is called, whether a model was fitted on a cross-section or a panel: all trivial, and all removed by a reader's eye before it reaches the findings. *"The data is the underlying panel of the World Happiness Report 2024; the first two questions are answered on a cross-section of countries and the third on a model of the year-on-year change in happiness"* was cut in full for this reason.
- **Give the big picture, not the statistical detail.** The abstract says what was learned about the subject. Sample definitions, specifications, diagnostics and how a null came about belong further down. If a sentence would only interest someone who intends to reproduce the work, it is in the wrong section.
- **Write it last for the obvious reason:** it is the only section that has to be true of every other one.

### Step 7 — Read through

Read the finished report from beginning to end and list what is wrong with it. This is a separate step because the faults it catches are invisible to every check made while writing: those are made section by section, and these faults only exist in sequence.

- **Read it in order, in one pass, as a reader would.** Not section by section, and not searching for anything in particular. A term defined twice, a claim made in `Results` and contradicted in `Discussion`, a figure discussed before it appears — none of these are visible from inside the section that contains half of them.
- **Check the argument runs end to end.** Each sub-question should be asked in the `Introduction`, its method given in `Methods`, its answer in `Results`, and its meaning in `Discussion`. One missing from any of the four is the commonest structural fault, and the easiest to miss once every section looks complete on its own.
- **Re-check everything that goes stale.** Every number against the generated output, every figure reference against the figure it now points to, every cross-reference to another section. `When Something Changes` lists how these break.
- **Check nothing is orphaned.** A figure never referred to in the text. A reference never cited. A citation with no reference. A heading with nothing under it. A defined term used once and never again.
- **Check the `Abstract` against the report.** Every claim in it should be traceable to a section, and the emphasis it gives should match the emphasis the report gives.
- **Check the references properly, not just that they exist.** Each one cited where it is used, each detail verified against the source, each link resolving, and the list in order. This is the last chance to catch a citation that says something the source does not.
- **Report the list; do not fix as you go.** The point of the step is the list. Fixing while reading loses the thread of the argument, and it takes the decisions away from the user, who may want a fault left alone or handled differently.
- **Record the outcome in the `Analysis Log`**, including when nothing was found. A read-through that reports nothing has to be distinguishable from one that never happened.

### Step 8 — Export

Turn the finished report into a file that can be sent to someone who does not have the vault.

- **Ask which format.** Word for a reader who will comment on it, PDF through LaTeX for something to print or submit, or both. Do not assume, and do not produce every format because it is cheap to do so.
- **`Report.md` remains the source of truth.** Never edit an exported file and never convert one back.
- **Run the conversion from the vault root**, so the figure paths inside the document resolve, and record the exact command in the `Code Summary`. An export that cannot be repeated is not much better than a screenshot.
- **Write the output where it cannot be mistaken for the source**, such as `Code/outputs/`. An exported `.docx` sitting beside `Report.md` will eventually be the one somebody edits.
- **Four things break in conversion, and none of them stops it.** The exporter returns success and writes a plausible file in every case below, so each has to be checked by looking at the output.
  - **Captions stop looking like captions.** They are wrapped in `<small>` and `<b>` because Obsidian will not parse Markdown inside HTML. Converting to Word or LaTeX keeps the words and discards the tags, so the caption arrives in body text at body size and a reader can no longer tell legend from argument. Convert captions to the target's own emphasis before exporting.
  - **Characters the target's font cannot render are dropped in silence.** A default LaTeX font will not have Greek letters or superscript signs, so `ρ` and `⁻` vanish from the PDF — which matters, because that turns `p = 1 × 10⁻¹³` into `p = 1 × 1013`, a different number rather than a missing symbol. The exit code is still zero. Use an engine and font that cover the characters actually in the document, and search the output for every non-ASCII character the source contains.
  - **Links to other documents survive as dead links.** Relative links to `Appendix.md` or `Setup.md` point into a vault the reader does not have. Strip them, or point them somewhere published.
  - **The reference list is prose, not a bibliography.** It converts as ordinary paragraphs. That is usually what is wanted, but the target's citation machinery is not involved and will not renumber or reformat anything.
- **Open the exported file and look at it.** Figures present and in the right order, captions attached to the right figures, tables not collapsed, equations legible, no numbers altered by a missing character.
- **Do not install anything until the user has asked for a format that needs it.** Nothing in steps 1 to 7 requires an export tool, so the workspace does not ship with one. Word needs only a converter; PDF needs a LaTeX engine as well, which is a much larger install. Ask which format they want, then install what that format needs and nothing else.
- **The tools are not fixed by this contract.** `pandoc` is the usual converter. Whatever is used, record it in `Setup.md` with its version, so the export can be reproduced.

## When Something Changes

A refit, a re-cleaned value, a dropped figure or a renumbering makes some sentences in the documents false. Making the change is the easy part; finding what it falsified is the work.

- **Re-run the whole pipeline, not just the script that was edited.** Later scripts read earlier outputs. One that is not re-run leaves the documents describing two different versions of the data.
- **Sweep every document for the old values, including prose that quotes a table.** Correcting a table and missing the sentence citing it is the commonest way a document goes internally inconsistent, and every local check still passes while it is wrong.
- **Search for the formatted number as well as the raw one.** A p-value written `7.65e-14` in the output may appear as `8 × 10⁻¹⁴` in the report. Searching for one will not find the other.
- **Re-read every paragraph that mentions a changed figure, not only the nearest one.** Reorienting a chart can falsify the paragraph explaining how to read it while the caption and the paragraph above it both stay correct.
- **Check for numbers hardcoded in scripts.** A value asserted in a string rather than computed survives a refit unchanged and unnoticed. Compute it instead, so it cannot go stale.
- **Re-verify the numbers that survive, not only the ones that moved.** A figure that happens to be unchanged still has to be confirmed against the new output rather than assumed.
- **Record what moved in the `Analysis Log`**, with the before and after values. That is what lets a reader see which conclusions are sensitive to the decision.

## Working Method

1. Inspect the relevant files in `Attachments/` before making claims about their contents.
2. Put all analysis logic in `Code/`. Use clear, descriptive filenames and preserve a reproducible path from source data to results.
3. Record the work in `Appendix.md` as it progresses — from the first step, not at the end. What the data contains, the research question and how it was reached, then each step's decisions, assumptions and outputs in the `Analysis Log`.
4. Write `Report.md` only as the steps above direct: each step adds its own part without being asked, and nothing else enters it. Write it for the intended audience, keep it concise, distinguish facts from interpretations, and link each material conclusion to supporting appendix evidence.
5. Update the `Code Summary` section of `Appendix.md` whenever code is added or materially changed. State what each important file does, how to run it, what it reads and produces, and any parameters or seeds that affect results. Keep installation and environment instructions in `Setup.md`.

## Python Environment

Run all Python through the workspace environment so results are reproducible. Full instructions live in `Setup.md`; the rules that bind this work are:

- Create or update the environment with `cd Code && ./setup_env.sh`. This resolves `uv.lock` and builds `Code/.venv`. Never install packages into the system Python.
- Run code with `cd Code && uv run python <script>.py`, notebooks with `cd Code && uv run jupyter lab`.
- Add a dependency with `cd Code && uv add <package>`, which updates `uv.lock`. Commit the changed lockfile, list the package in the `Code Summary` section of `Appendix.md` alongside the code that needs it, and update the version table in `Setup.md`.
- `Code/check_env.py` prints the exact interpreter and package versions. Record that output in `Appendix.md` when environment versions could affect results.

## Analysis Standards

- Preserve original attachment files. Write derived datasets, charts, tables, and exports under `Code/` unless a task specifically requires another location.
- Never invent data, results, file contents, citations, or successful execution. Mark missing information and unverified assumptions clearly.
- Prefer reproducible scripts or notebooks over manual calculations. Include commands, parameters, random seeds, and environment requirements when they affect results.
- Check row counts, missing values, types, ranges, duplicates, joins, and outliers as appropriate for each dataset. Document meaningful issues in the appendix.
- Separate observed results, methodological assumptions, and recommendations. Quantify uncertainty and limitations where possible.
- Do not expose credentials, access tokens, personal data, or other sensitive material in code or Markdown files.

## Markdown Formatting

These documents are read and edited in Obsidian, which soft-wraps text to the width of the pane.

- **Do not hard-wrap prose.** Write each paragraph as a single line, however long. Breaking lines at a fixed column looks ragged in the editor, and it makes the text painful to edit, because changing one sentence means rewrapping the whole paragraph by hand.
- One line per paragraph, list item, table row, heading, and blockquote paragraph. A bare `>` still separates paragraphs inside a blockquote.
- Code blocks are exempt: wrap those as the language needs.
- The same applies to Markdown written by scripts in `Code/`. Build each line as one string rather than emitting a wrapped block.

## Writing

The report is prose that a reader has to get information out of. **Aim for simple, plain text that brings the main points to the front.** Three faults recur and are worth naming.

- **Say it plainly; no figures of speech.** *"The association is not simply the control variable wearing another name"* should be *"the association holds even when the control variable is accounted for."* Metaphor makes the reader decode a sentence instead of reading it, and it adds nothing a plain phrasing would not carry.
- **No throat-clearing.** Do not announce what a sentence or paragraph is about to do and then do it. *"The panel model adds something a cross-section cannot"* is a promise, and the sentence after it is the content — keep the content and delete the promise. If a sentence could be removed without losing information, remove it.
- **No abstract gesturing.** Sentences assembled from methodological abstractions sound like an argument without making one. *"Temporal precedence is not identification, though, and here it is weaker than it looks"* says nothing a reader can check. Name the concrete problem instead: which variable, what is wrong with it, and what follows. Prefer *"a predictor built partly from later observations cannot establish which came first."*

A working test for all three: could a reader disagree with this sentence? If not, it is decoration.

### Learning the user's style from their own rewrite

The user may take a document away and rewrite it in the style they want, then hand it back. This is the most direct instruction about style available, and it is worth more than any adjective they could give instead.

- **When they say they are starting a pass, stop editing that document until they say `done`.** They are working in it directly. Editing underneath them risks a conflict, and staging their half-finished sentences risks committing work they had not settled. Answer questions and work elsewhere, but leave the file alone.
- **When they say `done`, read what they changed before writing anything.** `git diff` against the last commit is the record of the pass. Read it as a whole rather than sentence by sentence, because the pattern is the point.
- **Derive rules from the edits and add them to this section.** State each as something checkable — a rule that can be applied or breached — not as an adjective. *"Give the number before the qualification"* is usable. *"Write more clearly"* is not.
- **Cite the sentence each rule came from, before and after.** A rule without its example is unusable once the memory of the pass has gone, and the before/after is what makes the intent unambiguous.
- **Say what was inferred from a single instance.** One changed sentence may be a preference or may be that sentence; distinguish the rules that recur from the ones observed once.
- **Ask about anything that reads as deliberate but might be an accident.** A dropped qualifier can be a style choice or an oversight, and the difference matters when the sentence carries a result.
- **Then apply the rules to the rest of the work**, including the documents the user did not rewrite by hand. The point of extracting the rules is that the user should not have to make the same edit twice.

### Sentence and paragraph style

These are the defaults. They came from watching a user rewrite a report by hand, and each is quoted before → after. The mechanism above is how they get changed.

- **Write in the first person plural.** *"The question is one of association rather than cause"* → *"The questions we look at here are primarily of association rather than cause."* Then "we have investigated", "we found that", "what we can say is". The report is an account of work people did, not a description of results that arrived unattended.
- **Contractions are fine.** *"so no analysis of this data can establish which direction a relationship runs"* → *"so we can't say which direction the relationship runs."*
- **Split long sentences.** A sentence carrying three clauses joined by "and … so" reads better as two. Prefer two plain sentences to one balanced one.
- **Merge one-sentence paragraphs into their neighbours.** A methods section went from three paragraphs to two, and another from four to two, with almost no words cut. It was the paragraph breaks that were wrong, not the content.
- **Nothing in `Report.md` is bold unless the user asks for it.** Not a sentence, not a phrase, not a run-in heading, in any section. *"**The reverse direction.** The mirror model was fitted"* → *"A further model was fitted"*; *"**The second model.** Taken together"* → *"Taken together"*; *"consecutive **calendar** years"* → *"consecutive calendar years"*.
  - The bold figure number that labels a caption — `<small><b>Figure 1.</b> …</small>` — is a label rather than emphasis, and stays.
  - This applies to `Report.md` only. `Appendix.md` and the other working documents get scanned rather than read, and their bold lead-ins stay as they are.
  - The reason is not consistency, it is that bold makes the argument for the reader. A report has to earn its emphasis through sentence order and word choice; typography is a shortcut around the writing.
- **Cut the defence of the road not taken.** Deleted in full: *"Rebuilding the sample as 'most recent period with every variable present' was rejected: a unit whose latest period lacks one variable would have shifted to an earlier one…"* The reasoning belongs in `Appendix.md`. This is the same instinct as the rule against markers for work not done.
- **Cut technical asides that no reported number rests on.** Deleted in full: *"The model is pooled, with no unit fixed effects. Adding them to a specification carrying the lagged outcome on the right-hand side would introduce dynamic panel bias and require a different estimator, not merely more dummies."*
- **Refer back to the methods rather than restating a caveat.** *"The power of that test is limited by the outcome. Because the source interpolates…"* → *"However, as discussed in the methods, because the source interpolates…"*
- **Do not state a measurement as though it were the definition.** *"Productivity is measured as output per hour"* → *"One way of measuring productivity is output per hour."* It turns a claim about the world into a statement about a choice, which is what it is.
- **No figurative shorthand for a model or a method.** *"The mirror model"* → *"A further model."*
- **No short sentence dropped in for emphasis.** *"Nothing comes to rest there."* was deleted, and nothing was lost with it.

## References and Citation

- **Cite in author–date style.** `(Smith et al., 2020)` in parentheses, or `Smith (2020)` when the author is part of the sentence. Disambiguate same-author-same-year works as `2020a`, `2020b`. Where two works share a first author and year but have different co-authors, name enough surnames to tell them apart rather than lettering them.
- **Every document that cites anything carries a `## References` section as its last section.** That includes `Appendix.md`, which cites the sources behind the data.
- **Every reference is a link.** Hyperlink the title, or the DOI where one exists, to a URL that resolves. Check it resolves before writing it — a dead reference is worse than none.
- List alphabetically by first author. Use the corporate author for databases and reports without named authors.
- **Cite the specific edition or version actually used**, not the series in general. Data sources are revised, and a claim traceable to the wrong vintage is not traceable at all.
- **Verify the bibliographic details rather than writing them from memory** — volume, issue, pages, publisher, year. Never cite a work you have not opened.

### Getting hold of paywalled sources

Publishers block scripted requests. A `403` from a journal site is not a dead link — the same article opens normally in the user's browser, often through an institutional subscription. Ask them to fetch it.

- **Ask for the download; do not work around the block.** Substituting a preprint, a working paper or an abstract for the article you mean to cite is not a workaround, it is citing a different document. Working-paper and published versions differ in title, wording, tables and sometimes in the specific claim being cited.
- **Send a short list, not everything found.** Only the sources the argument actually rests on. For each, give the title, a DOI link and one line on what the citation needs from it, so the user can judge whether it is worth their time. Three or four is a reasonable ask; a dozen is not.
- **Say where to put them.** Ask the user to save the files to their `Downloads` folder and to say when they are there. Move them into `Attachments/literature/` yourself, keeping the publisher's filename or renaming to first author and year.
- **Keep the PDFs out of version control.** They are usually licensed material and the repository may be public. Add the folder to `.gitignore`, and record the citation in the documents rather than the file.
- **Then read them and cite from the text.** Note in the `Analysis Log` which sources were read in full and which rest on an abstract, so a reader knows how far each citation was checked.
- **An abstract is enough only for what the abstract states.** If the claim being cited appears verbatim there, say so and move on. If it needs a number, a caveat or a passage from the body, the article has to be opened.

## The Sample Report

`Sample Report/` holds one finished analysis — a question about World Happiness Report data, worked through the eight steps. It is there for one purpose: so a user who has not seen a report of this kind come together can look at what the documents contain when they are done.

- **Offer it when it would help, and not otherwise.** If the user is unsure what a section is for, what a figure caption should say, or how much detail belongs in the appendix rather than the report, point them at the corresponding part of `Sample Report/Happiness.md` or `Sample Report/Happiness Appendix.md`. That is more use than describing it.
- **It is an example, not a specification.** The section headings in the templates are a sensible default, not a requirement. A different question may want different sub-headings, a different number of sub-questions, no phase portrait, no growth model, or a structure the sample does not have at all. Follow the user's analysis, not the sample's shape.
- **Never edit it as part of a new analysis**, and never copy numbers, prose or figures out of it. Its scripts, outputs and (once downloaded) data are self-contained inside that folder so a new analysis has no reason to touch it.
- **The rules in this document take precedence over anything the sample does.** The sample was written while these rules were still being worked out, so it may not follow all of them perfectly. Where they disagree, the rule is right and the sample is a historical artefact.

## Agent Operating Rules

- Before changing analysis artifacts, inspect the relevant source data and existing documentation.
- Make focused changes and do not overwrite unrelated user work.
- After running or changing code, perform the narrowest useful validation and record the outcome in `Appendix.md` when it affects conclusions.
- Keep Markdown headings stable and update existing sections rather than creating competing versions of the same analysis.
- When evidence is insufficient, ask a targeted question or document the gap instead of filling it with speculation.
