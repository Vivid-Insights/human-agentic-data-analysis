# Data Analysis Workspace

A folder for working through a data analysis with an agent, one step at a time, and coming out with a report you can defend.

It is an Obsidian vault with [Claudian](https://github.com/YishenTu/claudian) installed, so the conversation happens beside the documents it is writing. The agent's working contract is [instructions.md](instructions.md), which it reads automatically.

## What makes this different from just asking

Ask an agent to analyse a dataset and it will hand you a finished report in one pass: statistics run, charts drawn, conclusions written. It will look right. You will have no idea which choices were made on your behalf.

This folder is built to stop that. The agent does one step per request and then stops. It does not add analysis, findings or prose you did not ask for. It agrees the method with you before applying it, and it answers one sub-question at a time. The parts that require judgement stay with you, which is the whole point.

## Getting started

1. Install the environment — [Setup.md](Setup.md) covers Obsidian, `uv` and Python.
2. Put your data in `Attachments/`.
3. Open a Claudian conversation and ask for step 1: import and describe the data.
4. Work through the eight steps, one request at a time.

If you want to see where this ends up before you start, read [Sample Report/Happiness.md](Sample%20Report/Happiness.md).

## The eight steps

| Step | What happens | What it fills in |
| --- | --- | --- |
| 1 | Import and scope the data | `Data Summary` in the appendix |
| 2 | Frame the research question | `Research Question` in the appendix; the questions go into the report |
| 3 | Visualisation | Figures into the report's `Results` |
| 4 | Statistical tests | `Methods` and `Results` in the report |
| 5 | Conclusions and limitations | `Discussion` in the report |
| 6 | Background and abstract | `Introduction` background and `Abstract` |
| 7 | Read through | A list of what is still wrong |
| 8 | Export | A Word file or a PDF for someone without the vault |

Nothing enters a section before the step that owns it. The report is built up as the work proceeds rather than written at the end, so by step 7 there is no write-up left to do — only a read-through, and then an export if you need one.

The report also carries a standing disclaimer, between `Discussion` and `Appendix`, saying it was written with the help of agentic AI at every stage. It is in the template from the outset rather than added at the end, and the agent will not remove it.

## What is in the folder

| Location | What it is |
| --- | --- |
| [CLAUDE.md](CLAUDE.md) | Imports the contract so the agent picks it up automatically. Nothing to edit here. |
| [instructions.md](instructions.md) | The working contract. The agent reads this; you change it by prefixing a message with `FRAMEWORK`. |
| [Report.md](Report.md) | Empty template. Section headings, with a note under each saying which step fills it. |
| [Appendix.md](Appendix.md) | Empty template. The running record: data, question, workings, log, code guide. |
| `Attachments/` | Your data. Never modified. |
| `Code/` | The environment and `viz_style.py`, which carries the figure conventions. Your scripts and outputs go here. |
| [Setup.md](Setup.md) | Installation and the everyday commands. |
| [Sample Report/](Sample%20Report/) | A finished analysis, self-contained, as an illustration — with its own code, outputs and walkthrough. The source data is not included; see its `Attachments/SOURCE.md` to download it. |
| [Sample Report/Analysis Steps.md](Sample%20Report/Analysis%20Steps.md) | A walkthrough of that analysis with the prompts used, for showing someone how the folder works. |

## Report and appendix

Two documents, two readers.

`Report.md` is the argument: what was asked, what was done, what was found, and what it does not support. It stays short, carries no diagnostic detail, and every number in it comes from generated output rather than from anyone's memory.

`Appendix.md` is the record, and it fills up from the first step. Every decision with its reasoning and what it cost, every workings, every check that changed nothing, and every decision that was later reversed — marked superseded rather than deleted, because a reader cannot judge a choice without seeing the alternatives.

## The sample

[Sample Report/](Sample%20Report/) holds one finished analysis: whether people in healthier countries rate their lives more highly, worked through all eight steps on World Happiness Report data. It has its own `Code/` and `Attachments/`, so it is complete and touches nothing else. The WHR data file itself is not redistributed here; `Sample Report/Attachments/SOURCE.md` says how to download it if you want to re-run the code.

It is there to look at, not to copy. The templates' headings are a sensible default and not a requirement — a different question may want a different structure entirely. Where the sample and the contract disagree, the contract is right; the sample was written while the rules were still being worked out.

## Changing the contract

Prefix a message with `FRAMEWORK` and the agent treats it as a change to `instructions.md` rather than a request about the analysis. It applies the rule, applies it retrospectively to work already done, and commits it on its own so the rule can travel to another project without the analysis coming with it.

That is how the current contract was built: twenty-one rules, each one written the moment the agent did something that was not wanted.

## Version control

Commit as you go. The agent stages named files rather than everything, so an unfinished edit of yours is never swept into its commit, and it will not commit or push unless you ask.

## Licence

This template — the contract, the documents, the code and the sample report — is licensed under [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/). See [LICENSE](LICENSE).

Third-party material is not covered: the World Happiness Report and Gallup data the sample analyses, and the articles it cites, remain under their owners' terms and are not included in the repository.
