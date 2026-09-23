# Analysis Steps

A walkthrough of the analysis in this folder, for showing someone how this folder is used. Each entry is something I asked for, the prompt I used, and what came back. The eight headings are the eight steps in [instructions.md](../instructions.md).

The point of the walkthrough is the shape of the exchange, not the subject. I asked for one thing at a time, looked at what came back, and often changed my mind. Several of the most useful moments were the agent telling me something was wrong.

*Where the prompts come from.* They are the ones from the original session, with typing errors tidied so they can be re-entered. A few are reconstructed: where the original was a reply like "yes" or "1, (a) 2" it made no sense out of context, so it is written out in full. Prompts that changed the working contract rather than the analysis are left out; this is a walkthrough of the analysis, not of how the contract was built.

*Why a re-run will not match exactly.* These prompts assume the contract as it now stands, and several of the original exchanges took more turns than appear here because the relevant rule did not exist yet. The figures needed three separate passes before they were legible, the discussion had to be rewritten once for plain language, and the background was first written from abstracts rather than from the papers. Those lessons are now rules in [instructions.md](../instructions.md), so a fresh run should get closer on the first attempt and may need fewer prompts than are listed. Entries 8, 15 and 17 are the likeliest to differ, because each of them exists precisely because something went wrong before the rule was written.

*Where the substance is.* Two moments carry more than the rest, and both are the agent disagreeing rather than complying: entry 12, where it produces a null result and then explains why that result is worthless, and entry 15, where it checks a discussion I wrote by hand and finds eleven errors in it. The rest of the walkthrough is the machinery that makes those two possible.

## Step 1 — Import and scope the data

**1. Say what the subject is, and get the data in.** The agent found the panel behind the report's own analysis, recorded where it came from with a checksum, and wrote a description of what was in the file — shape, columns, coverage, what was missing.

```
In this session I want to analyse World Happiness data. For now, all I want you to do is download the dataset.
```

**2. Ask what the units are.** This was the most valuable question of the whole analysis, and it came early. The first file had columns named after the six factors the report discusses. They looked like data. They were modelled contributions — a regression coefficient multiplied by a distance from a baseline — with no natural units at all, and the underlying values could not be recovered from them. We abandoned that file and switched to the raw panel, which the publisher had stopped distributing and which the agent recovered from the Internet Archive.

Ask what the units are before you ask anything else. A plausible column name is not a unit.

```
So there are no values for Log GDP per capita, Social support, Healthy life expectancy, Freedom to make life choices, Generosity or Perceptions of corruption before 2019?
```

```
What are the units on GDP?
```

```
I would like all of the data in relatable units please. So let's go back to the data stage and look at that.
```

**3. Choose the years.** I asked which years had usable coverage, and picked 2007 to 2023 as the balance between length and completeness. 164 countries.

```
What years do we have good data for?
```

```
I feel 2007 to 2023 is a good balance?
```

**4. Decide what to do about gaps and bad values.** Gaps could stay as gaps rather than being filled — the agent had found that the sparsest column was missing precisely where the subject was politically sensitive, so imputing would have invented data in the cases that mattered most. Two countries had values that were plainly wrong rather than missing: one country's health series rose in exact steps of 5.32 years per year, which is what interpolation between two distant anchors looks like, and another's income series collapsed by 98%. Both were set to missing rather than corrected, and both decisions were written down with a count of the cells affected.

```
We don't need the same countries every year. We can leave NaNs.
```

```
Forecast GDP is OK. NaN Haiti for now. What was the Venezuelan problem?
```

```
NaN Venezuelan GDP entirely.
```

Later in the analysis I came back and widened the first of those rules, because two more years sat on the same fabricated ramp and had been left in for being individually plausible. Everything downstream was refitted.

```
Remove Haiti's 2013 and 2014 rows.
```

## Step 2 — Frame the research question

**5. Say what the question is, before looking at any relationship.** The agent discussed how it might be answered and whether the data could support it, working only from what the columns meant — no correlations, no plots, nothing computed.

We settled on one main question and three sub-questions: the association across countries, whether it survives accounting for income, and whether the year-to-year record shows which moves first. Those went straight into the report's introduction, before anything was tested, so the write-up could not drift toward whatever turned out to be interesting.

```
OK. What is the next stage?
```

```
I want to look at the relationship between happiness and life expectancy. Do countries with higher life expectancy have higher levels of happiness?
```

```
Let's do sub-questions 1 to 4.
```

## Step 3 — Visualisation

**6. Plot the data for one sub-question.** A scatter of happiness against healthy life expectancy, one point per country. The agent put it in the report as soon as it existed, at the size a reader would meet it, which is a much better way to judge a figure than looking at a file.

```
Let's do the most recent year available for each country. Start by plotting the data as a scatter.
```

```
Can you add two or three countries from the middle of the cloud too.
```

**7. Ask for it the other way round.** For the growth model later on I could not tell which variable belonged on which axis, so I asked for both versions. I picked one, then changed my mind several steps later and picked the other — because the claim in the paragraph beside it was about the slope, and only one orientation showed that slope at all.

```
The x-axis in the plot should be life expectancy and the contours current life ladder. Make this plot too and we will see which we keep.
```

```
While writing I realised that you were right about figure 3. It is more intuitive to put happiness on the x-axis and the contours defined by life expectancy. Can you do that again.
```

That change caught something. The paragraph explaining how to read the figure still described the old picture, three paragraphs away from the caption, and every local check had passed.

**8. Make the figures readable.** The type was too small once Obsidian scaled the images to the width of the pane. Then the labels needed leader lines, because at the larger size a country name sat nowhere near its own point.

```
The font on the figures is much too small to be readable. Please remove the subheader with details — this is covered in the text. Drop figure 2.
```

```
I can't see what Finland, Japan and CAR refer to.
```

## Step 4 — Statistical tests

**9. Quantify the first sub-question.** A regression, with the slope reported per decade so it could be read against the ladder's own scale: 1.47 points per decade across 160 countries.

```
Now quantify sub-question 1. Fit a line and report the slope per decade.
```

**10. Account for income.** Adding income cut that to 0.59 points per decade, with an interval that still excluded zero. The two predictors correlate at 0.84, so the agent said plainly that how much credit each takes depends on the specification rather than on anything in the data.

```
OK. Let's do sub-question 2.
```

```
Isn't there a better way of controlling for income here, whereby you first fit GDP and then make a regression on the residuals? Is that different from what you have done?
```

**11. Change the question, and fix the model.** I decided the third sub-question should be about growth, not levels: does happiness grow faster where health is better? I proposed one form of the model, then corrected it — the health term should enter additively rather than multiplied by happiness. Refitted.

```
I want to change sub-question 3. Identify all instances in the data where there are two consecutive years for life ladder, GDP and life expectancy, and calculate the yearly difference. Then model the growth of the life ladder. First update the sub-question description, then propose a model.
```

```
Please fit it with a constant term k which models growth independent of all other factors, so not a percentage increase.
```

```
I realised I am fitting the wrong model. Could you repeat with a_2 times E_t instead of the product. Rewrite methods and results.
```

```
Could you change the variable names and use Happiness in the figures. Use H for happiness (life ladder) and E for life expectancy.
```

**12. Test the other direction, and find out the data cannot.** Does happiness predict how fast health improves? The answer came back as no, and then the agent explained why that answer was worthless: the health series is interpolated between sparse observations, so its year-on-year change takes 151 distinct values across 1,872 observations and is nearly a country-specific constant. A model whose outcome barely varies cannot detect anything. The null follows from how the data was built.

This is the single most important thing in the analysis, and it is a fact about the data rather than about the world.

```
Now, still as sub-question 3, fit a model dE = k + a_1 E + a_2 E^2 + a_3 H to test if there is a relationship in the other direction. Make a figure showing this.
```

**13. Draw the two models as one system.** I asked for a phase portrait, following a paper I knew, showing both variables' expected movement as a vector field. The agent flagged that the horizontal component rests on the interpolated series and should not be read as measured movement.

```
Now can you add a new figure, like figure 5 in https://journals.plos.org/plosone/article/file?id=10.1371/journal.pone.0086468&type=printable showing change in both variables as a vector space. Add a description, with the reference, to methods.
```

```
Let's change the axis on life expectancy to -0.5 to 1.5 for change, and make a note in the legend that some points are excluded.
```

```
In the phase portrait, it isn't quite true that happiness is unchanging, is it, because dE is positive. It is the stable nullcline, isn't it?
```

**14. Cut the report back.** Repeatedly. Diagnostics, alternative specifications, a check I had asked about that changed nothing — all of it out of the report and into the appendix. A test can produce a page of statistics; the report takes the number that answers the question.

```
This paragraph seems to be about something not in the results. I want these reports to be clean and not to add a lot of technical detail which we don't use.
```

## Step 5 — Conclusions and limitations

**15. Write the discussion, then rewrite it plainly.** The first version was full of metaphor and throat-clearing, so I named the faults and had them fixed. Then I wrote a version myself and asked the agent to check it. It found eleven errors, four of which changed the meaning — including a direction of motion I had inverted, and three values I had read off a chart by eye instead of taking from the output.

```
Write three paragraphs in the discussion. One about sub-questions 1 and 2, showing there is a relationship between life expectancy and happiness. Then one about model fit, why it gives some information on health leading to happiness as a plausible relationship, and the limitation because of how the data came about. Then another about how we can, even with this limitation, understand something about the dynamics.
```

```
I wrote up the discussion. Do tell me if I have written anything wrong.
```

## Step 6 — Background and abstract

**16. Write the background last, from sources.** The background is the one part of the report that does not come out of the data. The agent proposed which claims it needed to establish, found candidate sources, and told me what each actually said.

```
Do the background now. See if you can keep it to one paragraph with 4 or 5 references, since we already cover a fair bit in the introduction.
```

**17. Make it read the papers.** The first draft was written from abstracts. I asked for the articles, downloaded four of them, and the load-bearing citation turned out to say more than its abstract did — the level of life expectancy did not predict life evaluations, but changes in it did. That was the distinction the whole analysis rested on, sitting in the closest prior work.

```
Downloaded them all. Please read them.
```

```
Can you check the Deaton claim is correct.
```

**18. Write the abstract, then take the numbers out.** The first version carried fifteen figures. An abstract is read to decide whether to read the report, and none of them helped with that decision. It now gives direction and rough size in words.

```
Now write the abstract.
```

```
The abstract should avoid using numbers as much as possible. We can also suggest a title at this point.
```

## Step 7 — Read through

**19. Read the whole thing, in order, and list what is wrong.** Every reference verified against the publisher's record, every link checked, every number traced back to the output that produced it. It found a reference listed but never cited, a list out of alphabetical order, forward references to a sub-question that had been dropped before it was asked, and one claim left standing with no uncertainty attached.

None of those were visible from inside the section that contained them.

```
Read through the whole report and check all the sections, and identify any problems. Then do a careful check of the references.
```

## Step 8 — Export

**20. Turn it into a file for someone without the vault.** I asked for Word, since that is what a reader who wants to comment on it will open. The four figures came through embedded, and every unusual character survived — the superscripts, the times sign, the rho, and the superscript minus in `p = 1 × 10⁻¹³`.

One thing did not survive. The captions arrive at body size and weight, because the `<small>` and `<b>` tags that make them read as captions in Obsidian have no equivalent that comes through the conversion. Nothing looks broken; the legend simply stops looking like a legend.

A PDF would need a LaTeX engine installed as well, and the default font drops characters like `ρ` and `⁻` without saying so — which can turn a p-value into a different number. Worth asking for only when someone actually needs one.

```
Export the report to Word.
```
