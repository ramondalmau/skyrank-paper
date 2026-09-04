# TR-C extension — Learning airline route preferences from flight-plan revisions

Journal extension of `../sid2026` for Transportation Research Part C.
`trc2026.tex` is the manuscript; `SUBMISSION_NOTES.md` the evidence map and
the list of things a human must verify before submission; `OUTLINE.md` the
original plan (its section numbering predates the current structure and is
kept for the record only).

Build:

```bash
mkdir -p "$TMPDIR/trc"
~/.local/bin/tectonic -X compile trc2026.tex --outdir "$TMPDIR/trc"
```

Currently 46 pages, zero errors, zero undefined references. The
`latex_sanity.py` brace-delta warning on this file is a known false positive
of that naive counter; do not chase it.

## Structure (settled, do not re-churn)

- **Class**: `elsarticle` preprint, 12pt, author-year (`elsarticle-harv`),
  single column.
- **Sections**: 1 Introduction · 2 Background (revisions as preference data;
  two operational use cases; revealed preference and the construction of
  pairs) · 3 Related work · 4 Data and pair construction (the archive,
  including its composition; stay pairs; encoding and leakage control;
  splits) · 5 Model, training and calibration · 6 Predictive performance
  (accuracy, coverage and baselines; accuracy by stratum; ablation and change
  bias; error analysis; feature attribution) · 7 Proposal channel (policy and
  operating points; concentration of the value; sensitivity to the bias
  correction; a worked example) · 8 Model ageing · 9 Threats to validity ·
  10 Conclusions, then the Disclaimer and the elsarticle declarations.
  Headings are plain noun phrases; every section opens with a lead-in
  paragraph.
- **The SID prose is the core.** Sections shared with the conference paper
  were carried over nearly verbatim and the journal material written around
  them. The abstract is held at 250 words under the strictest count: strip
  macros and braces, treat `\,` as a space, and replace `\%` BEFORE dropping
  `%` comments (a naive comment strip deletes the rest of every line with a
  percentage and under-counts by ~20; that mistake was made once).
- **Neutrality**: no operator, waypoint, volume or city pair is named in any
  table; the per-city-pair and per-waypoint tables of the study were
  deliberately left out. The introduction keeps the Amsterdam–Barcelona
  anecdote already published at SID.
- **Figures** are re-rendered at the elsarticle text width (390 pt) by
  `make_trc_figures.py`, which overrides `style.SIZES` from the SID drivers
  and copies the results into `figures/`; `fig_horizon.pdf` comes from
  `make_horizon_figure.py`. `fig_pipeline.png` is the image-model figure
  shared with the SID (see `figures-src/`; 341 dpi at its `0.95\textwidth`
  include). Nothing is scaled at include time. See
  `../REPRODUCING.md` for the order of operations, because this driver
  overwrites the shared staging directory used by the SID.

## What the 2026-09 revision changed, and why

A review pass in September 2026 (four independent reviewers on the rendered
PDFs, a code audit of the pair construction, and an adjudicated debate on the
stay-pair masking) produced four corrections and four additions. They are
recorded here because each one is a claim that used to read differently.

**Corrections.**

1. *The proposal policy.* Section 7.1 said the channel proposes "an
   alternative burning less planned fuel than the filed route", and that
   eligible flights were those having one. The code
   (`studies/2026-07-fuel-study/code/run_09_muac_policy.py`, line 59) makes a
   pair eligible whenever its two routes differ in planned fuel at all, which
   is 275,907 of 281,720, and proposes whichever of the two is cheaper. In
   55.1 % of eligible pairs that is the route the airline was abandoning, so
   the no-model base rate is 44.9 %, not something near one. The section now
   states the arithmetic, and 44.9 % → 79.2 % is the lift the model buys.
2. *The best simple baseline.* A rule scoring 45.0 % scores 55.0 % inverted,
   so "prefer the route that burns more planned fuel" beats the delay rule's
   53.2 %. Both papers said fifteen points over the best single-feature rule;
   it is thirteen.
3. *Model ageing.* "Roughly a year of staleness" was wrong. The aged model's
   data ends three months earlier than the fresh model's and covers four
   fewer months, and the experiment cannot separate the two. What it does
   measure directly is six months beyond a training cutoff. The annual
   retraining recommendation has gone with it.
4. *Calibration error.* 0.8 / 1.7 percentage points were 0.9 / 1.8
   (`results/calibration.json`). Both papers carried the old pair.

**A fifth correction, caught by the final verification pass**: the score-gap
to probability table was first built from the pipeline's `p_pref`, which is
oriented to the route the airline chose rather than to the one the model ranks
first. That understated the two lowest bands by three to four points and made
the caption claim an agreement the table itself refuted. `run_22` now emits the
column and documents the trap.

**Additions**: a full baseline ladder from a coin toss to the model, a
score-gap to probability table, a decision-context table pairing what each
revision did to the delay with the model's accuracy on it, the stay-weight
sweep as a table rather than as prose, and a figure showing which way each
feature pushes the score (delay is penalised sharply, planned fuel is rewarded
weakly, which is the model-internal counterpart of the below-chance cost
rules). Three limitations that three reviewers found unacknowledged were added
to Section 9: where a deployed channel's candidates would come from, that the
alternative's attributed delay is a query rather than an observation before
filing, and that non-revision has causes other than contentment.

**The stay-pair masking was removed, and the reasoning replaced.** The old
text said a model with access to the delay features could score well on stay
pairs "for the same empty reason" as the trivial rule, and masked the seven
regulation-derived features whenever a change-bias figure was quoted. Both
halves were wrong.

The archive contains its own control and nobody had used it. In an *escape*
the regulated route is the one abandoned, so "prefer the regulated route" is
always wrong there; in a *stay pair* it is always right. A model reading
regulation status alone must therefore score 100 % on one population and zero
on the other. The production model scores **88.0 %** on the 30,953 escapes of
the held-out quarter and **90.0 %** on its 1,093 stay pairs, for **0.8 points**
of revision accuracy (68.1 against 68.9 without stay pairs). No reading of
regulation status produces that pair of numbers, so the stay figure can be
read as it stands and the masking was unnecessary.

The papers now report the direct figures (34.8 % to 90.0 %) with the escape
comparison as the evidence. The withheld-feature figures (47.8 % to 58.1 %)
were briefly kept as a "conservative floor"; the author rejected that too, on
the grounds that hiding the regulation features is the same experiment under
another name, and they are gone from both papers along with the sweep table's
`stay, withheld` column. What stands in their place are the two bounds that
masking never addressed anyway: the stay set is small (1,093 test pairs) and
its two routes belong to two different flights.

## The horizon experiment (Section 8)

`studies/2026-08-trc-horizon/` (see its README): production configuration
trained on 2025-01→10, tuned and calibrated on 2025-11/12, evaluated month by
month on 2026-01→06. Heavy artefacts in `/data/rdcodina/skyrank/trc_horizon/`.

## Voice pipeline

PaperOrchestra steps (outline → plotting with critique loop → literature →
section writing → refinement), then `/coldread` with fresh zero-context
readers, then the author's voice profile applied last. Automated checks:
zero em dashes, contractions, And/But/So openers, American spellings and
AI vocabulary; a lead-in paragraph before every first subsection; abstract
at or under 250 words. All five references added in the 2026-09 pass were
verified against CrossRef/NTRS by hand, not only by the agent.

## Typesetting settings that are deliberate

Both papers set `\clubpenalty`, `\widowpenalty`, `\displaywidowpenalty` and
`\brokenpenalty` to 10000, so no single line of a paragraph is ever stranded
at the top or the foot of a page or column and no word is hyphenated across a
page break. In a paper of this length a paragraph must still be allowed to
continue on the next page; what these forbid is the stray line.

The two maps of Figure 3 are stacked in one float and are therefore drawn to
a common width (220 pt in `make_trc_figures.py`), each keeping its own aspect
ratio, so neither map's geographic extent moved when they were aligned.

## The narrative-edit pass of 2026-09-04

Nine zero-context readers and hunters were run on the LaTeX source. Four
claims were wrong and are corrected in place, each with a dated
`% CORRECTED` comment:

1. *The horizon experiment's own description.* Section 8 opened "The entire
   design of Section 4.4 is moved back one year", which Section 4.4 denies in
   as many words ("a shorter window ending three months sooner, not the same
   window moved back a year"). Three further sentences said the two splits
   were tuned "a year" apart; the tuning months are November-December 2025
   and March 2026.
2. *Which stratum is the easier one.* The recovery in June was explained by a
   shift towards regulated pairs, cross-referenced to the regulation-keyed
   strata table. The horizon table keys "regulated" on delay carried by the
   newly filed route (`run_horizon.py:174`), a different population. The
   figures now come from the horizon study's own strata: 71.4 % against
   67.0 % in June.
3. *Four kilogrammes.* 20.101 kt against 20.097 kt is four tonnes.
4. *Why delay outranks fuel in the attribution.* Explained by the relative
   magnitude of the two quantities, which cannot hold for a tree ensemble,
   invariant as it is to a feature's scale.

**Two calibration figures were reconciled.** The table caption called its
1.7-point average "the expected calibration error reported below", which the
text gives as 1.8. They are different statistics: 1.7 is the mean gap over
the table's six bands, 1.8 the expected calibration error over fifteen
equal-sized bands. The caption now says so, and the probability column is
printed to three decimals so that the 4.4-point worst band can be checked
against it (at two decimals it reads as 4.8).

**Structure.** Section 7.2 was a chain of three distribution facts whose
conclusion followed from only the first; it now opens on the question the
three answer. The head of Section 7.1 had three consecutive caveat
paragraphs, none of which said it was one of three consequences of the same
design decision. Section 2.3 claimed a route's score "depends only on the
route and the flight it belongs to", which the within-pair encoding of
Section 4.3 contradicts; it now says the score is taken against the other
candidates, and that every figure in the paper is measured on pairs.

**Do not restore**: the five "it is worth ..." framing openers that delayed their own
content were cut, leaving the eight where "worth" carries meaning; The author's own markers (Interestingly, Fortunately,
Opportunely, Needless to say, Last but not least) are voice and stay.

### Second round of readers (same day)

- **The abstract was 355 words**, against the 250 this project's own check
  enforces. It is now 240, with every headline number kept.
- **The feature table's caption** made the same false claim as the conference
  paper's and is fixed the same way.
- **"the network declares a regulation"** named the wrong actor; rewritten.
- **The training objective** was described as penalising the model "whenever
  the abandoned route scores at least as high as the chosen one, exactly as a
  binary logit would". A logistic pairwise loss never reaches zero and keeps
  pressing after the order is right, which the next sentence already said;
  the two now agree.
- **"Coverage"** carried two different meanings, one in the abstention curve
  and one in the ageing table. The ageing caption now says which it is.
- **The 1.7-point calibration average** is weighted by the pairs in each band,
  which the caption did not say; unweighted it is 2.1 and the reader cannot
  reproduce it.
- **A table caption compared 71.0 % against the eighteen-month 70.6 %** and
  then forbade the comparison in the next clause. The like-for-like figure for
  the same quarter is 63.3 %, which the caption now gives.
- **A repair to the archive** had been referred to without being described. It
  is now stated: pair completeness had been keyed on an identifier reused
  across days, which dropped about a quarter of the valid pairs.
