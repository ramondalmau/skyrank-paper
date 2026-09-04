# SESAR Innovation Days 2026 paper

*Which Reroute Will an Airline Accept? Learning Route Preferences from
Revisions*

Dalmau, Perez, Ballerini, Belkoura, Taverniers, Marin, Deransy, Cramet,
Gustin
(EUROCONTROL).

## Status

Exactly 8 of 8 permitted pages. **Not yet submitted.** See `COMPLIANCE.md` for
the venue rules and the two items to settle before upload:

1. `sid2026.tex` is a *drafting scaffold* on IEEEtran, not the official SID
   class. The submission must be transplanted into the official template from
   EasyChair and the page count re-checked there; a denser template will
   overflow.
2. The public venue page describes a triple-blind review; the organisers told
   the authors that author details are not withheld for this edition. The
   paper is built with `\blindfalse`. Re-confirm before upload.

The journal extension of this paper lives in `../trc-extension/`. Anything
the conference paper only sketches (the fuel channel, heuristic baselines,
model ageing, threats to validity) is there.

## Building

```bash
mkdir -p "$TMPDIR/sid"
~/.local/bin/tectonic -X compile sid2026.tex --outdir "$TMPDIR/sid"
```

The committed `figures/*.pdf` and `figures/fig_pipeline.png` are sufficient to build. There is no `pdflatex`
on the analysis host; use tectonic. Check after every build: page count 8, no
`Overfull` lines, no `??` in the PDF.

## Structure

Introduction; Background (revisions as preference data, including the
pairs-versus-generated-candidates argument; two operational use cases);
Related work; Methodology (data and pair construction; model, training and
calibration); Results (predictive performance; ablation and change bias;
error analysis and feature attribution; a worked proposal and the conditions
for deployment); Conclusions; Disclaimer. Headings are plain noun phrases and
every section opens with a lead-in paragraph before its first subsection.
Text cut for the page limit is kept in `% Cut for space:` comments in the
source, never deleted.

## Corrections made in the 2026-09-04 revision pass

Four claims in this paper were wrong and are now fixed. They are listed
because each was carried in a submitted-looking draft.

1. **The best single-feature rule is 55.0 %, not 53.2 %.** A rule scoring
   45.0 % scores 55.0 % when its sign is reversed, so "prefer the route that
   burns *more* planned fuel" beats the delay rule. The model's margin is
   thirteen points, not fifteen; the abstract, Section V-A and the
   conclusions all said fifteen.
2. **The abstract annualised CO2 as fuel.** "220 to 250 kt on a planned-fuel
   basis" is 220 to 250 kt of CO2; the body had it right.
3. **Expected calibration error is 0.9 / 1.8 percentage points**, not
   0.8 / 1.7 (`results/calibration.json`).
4. **Two domain statements were wrong.** The network does not assign a delay
   to every flight crossing a regulated volume: it allocates departure slots
   at the rate the volume can absorb, and the delay is the difference from
   the requested time. And airlines do not weigh delay against the published
   European reference values; those give the order of magnitude for analysis
   and are not any operator's own cost function.

Also rewritten: the description of how a pair is built. There is no record of
a "route change event" holding both messages. There is a message that changed
the route and the message that preceded it, and the pair is assembled from
those two. Removed: a debugging anecdote about a train/validation mixture
mismatch, and an equity aside about the second use case, neither of which
affected the science. The Shapley tutorial and one duplicated paragraph moved
into `% Cut for space:` comments to hold the paper at exactly 8 pages.

A fifth correction was made on 2026-09-04, after the author asked why the
conference paper carried neither the dataset composition nor results by
stratum. **The proposal policy's eligibility rule was stated wrongly**: the
paper said a flight is eligible when its candidate set holds a route burning
less fuel *than the filed route*, whereas `run_09_muac_policy.py:59` makes a
pair eligible whenever the two routes differ in planned fuel at all (97.9 %
of held-out pairs) and proposes whichever is cheaper. In 55.1 % of eligible
pairs the cheaper route is the one being abandoned, so a channel proposing
the fuel saver everywhere would be right 44.9 % of the time, below chance.
That base rate is now stated, because it is what the model's 79.2 % is
measured against.

## Two tables added on 2026-09-04

At the author's request the conference paper now carries what only the
journal extension had:

- **Table I, the revision archive by decision context** (`composition_ich.csv`),
  in Section III-A. It is what makes the paper's motivating claim checkable:
  the revisions that escape or reduce a delay are 18.4 % of the archive and
  their new route burns a median 101 and 65 kg more.
- **Table III, accuracy by stratum** (`strata_accuracy.csv`), in Section V-A,
  with the regulation, delay-band and cost-indicator blocks. The operator and
  city-pair blocks of the artefact are deliberately not carried, on the
  neutrality rule.

Both tables were paid for out of breadth, not by compressing what remained:
the occlusion study, the archive-composition sentence the new table
supersedes, the feedback-loop paragraph, three related-work sentences and the
introduction's "channel that is ignored" aside are now `% Cut for space:`
comments. The paper is again exactly 8 pages with no overfull boxes. The
leakage and harmonisation paragraph moved from Background into Methodology in
the same pass, which is where the author had asked for it.

The journal extension carries the same corrections plus its own; see
`../trc-extension/README.md`.

## Regenerating the figures

`../REPRODUCING.md` is the authoritative runbook (environment, inputs that
live outside the repository, regeneration order, the shared output directory
trap). In short: the drivers in this directory write to
`/data/rdcodina/skyrank/_audit/paper/figures/`, from which the PDFs are copied
into `figures/`. Run the SID drivers, copy, and only then run the journal
driver, because the latter overwrites the staging directory with
journal-sized renders.

```bash
python make_data_figures.py    # fig_coverage, fig_tradeoff, fig_concentration
python make_shap_figure.py     # fig_shap
python make_maps.py            # map_escape, map_saver
python make_pair_figure.py     # pair_idea
```

`fig_pipeline.png` (Fig. 2) is a raster made with an image model, shared by
both papers: the author ran PaperBanana's own Planner, Stylist, Visualizer
and Critic prompts by hand in ChatGPT
(`../trc-extension/figures-src/fig_pipeline_paperbanana_chatgpt.md` is the
exact prompt bundle; `fig_pipeline_chatgpt_original.png` next to it is the
untouched model output). The installed PNG is that output with its white
margin trimmed, re-encoded losslessly. At `0.85\textwidth` it sits at
287 dpi (IEEE asks for 300 for raster art; the earlier raster went in at
274); its smallest labels are about 4.5 pt on the page. Every label was
checked against the method text before installation.
The SID uses `fig_coverage`, `fig_shap`, `pair_idea` and `fig_pipeline`;
`fig_tradeoff`, `fig_concentration` and the two maps are produced by the same
drivers but appear only in the journal paper.

## Typesetting settings that are deliberate

Both papers set `\clubpenalty`, `\widowpenalty`, `\displaywidowpenalty` and
`\brokenpenalty` to 10000, so no single line of a paragraph is ever stranded
at the top or the foot of a page or column and no word is hyphenated across a
page break. In a paper of this length a paragraph must still be allowed to
continue on the next page; what these forbid is the stray line.

The conference paper additionally sets `\raggedbottom`. Once those penalties
hold, two columns cannot both be filled to the last line, and the alternative
to a slightly short column is a stretched one, which shows as visible gaps
between paragraphs. Do not remove it and then wonder why the columns gape.
Check after every build: `Underfull \vbox ... while \output is active` means
the setting was lost.

## Conventions that are deliberate

- **Green** is the route the airline chose or kept, **red** the route it
  abandoned, one blue accent for everything else, grey for context.
- **Line style, not colour, separates the routes** (abandoned dashed, chosen
  solid), and two SHAP groups carry thin hatching, because the palette's blue,
  red and green sit at L\* 45.4, 45.6 and 47.0 — the same shade of grey. The
  captions say "dashed red" and "solid green" for the same reason. Do not
  simplify those back to colour alone.
- **Figures are drawn at the size they print.** `style.SIZES` gives each
  figure its width and height in points and the `.tex` includes it at exactly
  `style.frac(name)` of `\columnwidth`. Change sizes in `SIZES` and
  regenerate; never in the `.tex`. Verify the MediaBox after every copy.
- **Type is STIXGeneral** (Times-metric, ships with matplotlib); Times New
  Roman is not installed and falls back to DejaVu.
- **Maps are ETRS89-LAEA (EPSG:3035) over Natural Earth 10 m** from the
  cartopy cache, clipped and simplified by `style.basemap` to about half a
  printed pixel (without it the Eurasia polygon made the paper 16 MB).
- **Neutrality.** No operator, flight, waypoint or airspace volume is
  identified anywhere; map endpoints are unlabelled; the worked example names
  no aircraft type. The Amsterdam–Barcelona introduction anecdote is the sole
  authorised exception. Deployment is written in the conditional, and the
  `\section*{Disclaimer}` stays verbatim (IEEEtran conference mode silently
  drops `\thanks`, hence a section rather than a footnote).
- **No number is typed by hand.** Every figure in the prose traces to
  `studies/2026-07-fuel-study/report/macros.tex` or the results JSONs. Never
  re-derive a metric; call the study's own code.

## The prose voice

The text follows the author's measured writing profile
(`~/.claude/skills/my-writing-style`): discourse markers open roughly one
sentence in five, procedural steps stay in the passive, prior work is cited
as "the authors of [n]", conclusions run First/Secondly/Thirdly and close on
"Last but not least,". Do not "tighten" those back out. Clarity is judged
only by zero-context readers (`/coldread`), never by the writer.

## The narrative-edit pass of 2026-09-04

Nine zero-context readers and hunters were run on the LaTeX source (three
readers, one SESAR-typical practitioner, one skimmer, four hunters). Their
findings, and what was done, are summarised here so a later pass does not
undo them.

**Two claims were wrong and are now corrected**, each with a dated
`% CORRECTED` comment in the source:

1. *The error-concentration statistic.* The sentence read "27.7 % of them
   fall within a quarter of the median score margin and only 5.6 % in the top
   quarter of the margin, against the 25 % that would obtain if error were
   independent of confidence". The 25 % reference describes the quartile
   statistic alone. The 27.7 % is a threshold, errors whose score gap is at
   most a quarter of the median gap
   (`run_07_performance_analysis.py:367`), so no quartile reference applies
   to it. Each number now carries its own comparator.
2. *Why delay outranks fuel in the attribution.* The paper explained it as "a
   matter of magnitude rather than of economics", citing tens of minutes
   against a few hundred kilogrammes. A gradient-boosted tree is invariant to
   the scale of a feature, so the units cannot be the reason. The study does
   not establish what is, and the claim is now confined to what was measured.

**Five reader-blocking inconsistencies were repaired.** "Those six months"
counted three test months in 2026 and two in 2025, which is five. The
thirteen-point margin was attributed to "prefer less delay", a rule scoring
53.2 %, when it is measured against the inverted fuel rule at 55.0 %. The
delay rule's 53.2 % and its 14.6 % coverage now say that it is right 71.6 %
of the time on the pairs where both routes carry a delay figure, and is
scored as a coin toss elsewhere. The error-analysis sentence said the channel
"would have said nothing at all" in a case the eligibility rule counts; it
now says why a deployed channel, which knows what is on file, would be
silent there. The 68.2 % in the ablation is marked as a separate run of the
adopted configuration, within the half point these figures vary by.

**Structure.** The feature-count sentence, the data-governance note and the
leakage paragraph were three unrelated one-topic paragraphs in a row, which
the choppiness hunter called the most bullet-like stretch in the paper; the
governance note now closes the data subsection instead. The "third
condition" promised in Section V-D was never delivered and is now written.

**Layout.** `stfloats` is loaded so that one of the two full-width figures
can sit at the foot of a page. Without it both landed at the top of the same
page and left it three-quarters empty, which cost the paper its eighth-page
budget. Do not remove it, and do not move `fig:method` back to `[t]`.

### Second round of readers (same day)

Six fresh readers on the fixed build found four more defects, now repaired:

- **The feature table's caption contradicted the paper's own mechanism.** It
  said everything but the indicators is "identical on both routes and act as
  context", when the regulation rows and the waypoint sequence differ within a
  pair, which is what the escape-versus-stay argument rests on. The caption now
  separates route-level groups from flight-level ones.
- **"the network declares a regulation"** put the decision with the wrong
  actor and gave demand over capacity as the only cause. An ATM practitioner
  reading cold stopped on it. Rewritten around what happens rather than who
  does it, since naming the actors correctly costs a line the paper does not
  have.
- **The error-analysis inference** ("the flight-level context is identical, so
  the preference can only have come from the waypoint sequence") does not
  follow: the regulation features are route-level too. It now says that every
  route-level quantity except the waypoints pointed the other way.
- **The abstract promised "accepted" proposals.** Acceptance is never observed
  in this study; the abstract now says what is measured, which is the airline's
  own next filing.

**What the eighth page cost.** The corrections above added about thirteen
lines to a paper that was at exactly eight pages. They were paid for, in the
order the clarity skill prescribes, out of: one duplicated restatement in the
stay-pair paragraph, three patch sentences, the repeated
acceptance-is-unobserved caveat, and finally one whole secondary point, the
sentence placing UDPP and airline-collaboration work outside route choice,
which is preserved in a `% Cut for space:` comment with both citations. **If
the author would rather keep those two citations, something else on pages 7-8
has to go instead**; the cut is the only one in this pass that touches the
bibliography.
