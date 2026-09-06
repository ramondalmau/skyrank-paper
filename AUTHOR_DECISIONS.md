# What the 2026-09-06 pass changed, and what is left to the authors

This file is the record of the follow-up pass on both manuscripts. It began
as a list of items the 2026-09-05 zero-context reader panels had raised and
that had been settled against the study's own artefacts but not acted on. It
now records what was repaired, what was checked and found sound, what is
blocked on a service this machine cannot reach, and what is a judgement the
authors have to make rather than a fact the record can settle.

Every number quoted here is in
`studies/2026-07-fuel-study/tables/referee_checks_summary.csv`, written by
`code/run_23_referee_checks.py`, or in the table named beside it. Nothing was
re-derived: the model's accuracy is always the mean of the pipeline's own
`correct` column, and the policy frame is built by
`run_09_muac_policy.build_policy_frame`. Every repair to a sentence carries a
dated `% CORRECTED` comment in the source beside it, and every passage cut to
stay inside a page or word budget is kept verbatim in a `% Cut for space`
comment.

| # | Item | Disposition |
|---|------|-------------|
| 1 | The 0-of-3 stratum is not "worse on every indicator" | **repaired**, both papers |
| 2 | "Almost always a move with a strong non-cost reason" | **repaired**, both papers |
| 3 | "Half a point of run-to-run variation" | **repaired**: measured at 0.17, four places |
| 4 | The 2025 replication is not "the same recipe" | **repaired**, conference paper |
| 5 | Fig. 2 states a loss and a gate the papers deny | **regenerated 2026-09-06**: five of six fixed, four label errors left |
| 6 | Fig. 3's lower map: the redaction and its premise | **settled by the content rule**; caption and code repaired |
| 7 | Data availability vs. the operator table | **repaired**: de-identified release set, statement amended |
| 8 | The stay weight was selected on held-out data | **measured**: the sweep now reports the tuning month |
| 9 | The quarter is not the archive | **stated** in the journal paper |
| 10 | Three "untouched share" figures that look alike | verified sound — do not touch |
| 11 | The stay-pair disclosures | verified exact; the tension is now cross-referenced |
| 12 | "The strongest simple rule is an inverted one at 55.0 %" | verified sound; the caption now states its tie convention |
| 13 | A subject swallowed by a comment (conference paper) | **repaired** — see the warning at the end |
| 14 | The journal abstract was 311 words against a 250 limit | **repaired**: 249, four passages cut into comments |
| 15 | Numbers that disagreed with themselves | **repaired**: five of them |
| 16 | What the venue reader challenged | **routed to the authors** |

---

## Repaired against the record

### 1. The 0-of-3 stratum (both papers)

Both papers read the third block of the strata table as revisions that "moved
onto a route worse on every one of" the cost indicators. The block is built
by `run_07_performance_analysis.py:200-206` as `(delta < 0)` summed over three
indicators, so an indicator counts against the newly filed route whenever
that route is not *strictly* cheaper on it, ties included. Route charges are
identical on **46.4 %** of held-out pairs, distance on 18.9 %, so only
**38,990 of the 90,961 pairs (42.9 %)** are strictly worse on all three.

The prose now says what the row is and gives the strict sub-population, on
which the model scores **86.3 %** rather than 79.9 %. The caption of the
strata table in each paper states the tie convention with the 46.4 %, and the
journal caption adds what a referee would otherwise construct for himself:
the block is keyed on agreement with the route the airline actually filed, so
a rule that follows the indicators is wrong by construction in the first row
and right by construction in the last. `tables/kpi_agreement_context.csv`.

### 2. The regulation explanation (both papers)

"A move against all the indicators is almost always a move with a strong
non-cost reason, typically a regulation" is not carried by the counts: a
regulation is attributed to one of the two routes on **42.2 %** of the
0-of-3 row and **63.5 %** of its strictly worse core, against **33.7 %** of
the 3-of-3 row. Both papers now state the three shares, give the difference
as 8.5 points, and say that nothing in the archive connects it to the 26
points of accuracy that separate the rows, so the size of the contrast is
observed rather than explained. The direction, which is what the paragraph
is for, is unchanged.

### 3. Run-to-run variation (journal paper, four places)

Three passages rested on a spread inferred from a single repeat. The spread
had never been measured because `run_05_seed_ensemble.py` read each member's
accuracy from a `metrics` key that `fit_model` never writes, so
`ensemble_summary.json` carried `test_acc: null` for every seed but the main
model. That is fixed, and the four seeds of the adopted configuration score
68.08, 68.09, 68.12 and 68.25 — a spread of **0.17 points**, against the 0.50
the manuscripts asserted. The claim was conservative, so nothing built on it
was wrong; the measured figure is the stronger one, because it makes the
ablation differences more decisive rather than less. `tables/seed_spread.csv`.

### 4. The 2025 replication (conference paper)

"A replication of the same recipe on 2025 alone scores 67.3 % and 67.5 %":
those numbers come from `model_repl_nostay_seed42`, whose metadata says
`"stay_augmented": false`. The sentence now says the replication is fitted
without the stay-pair correction and compares it with the no-stay headline of
**68.9 %**, which is the like-for-like figure, rather than leaving it beside
the 68.1 % of the adopted model.

The alternative repair — training the stay-augmented replication, which
`run_10_report_assets.py` expected under the name `model_repl_sw10_seed42` —
was not taken, because it would add a result to the paper rather than correct
a sentence. The dead expectation has been removed from `run_10`.

### 6. The unlabelled map (journal paper)

`make_maps.py` withheld the endpoints of the fuel-saver map because naming
them "would point at a single operator". The archive does not support that:
the mapped city pair is flown by **four distinct operators** in each
direction over the held-out quarter, exactly as many as Amsterdam–Barcelona,
which the upper map labels in full, in a quarter where 70 % of the 36,897
city pairs are served by one operator.

What settles the item is not that argument but the content rule: the
introduction's anecdote is the only city pair these papers may identify, so
the lower map stays unlabelled whatever the re-identification arithmetic
says. Two things were wrong and are repaired. The caption never mentioned the
omission the code claimed it mentioned, and now states which map is
unlabelled and why. The code's false justification is replaced by the real
one, with a note that withholding two words does not withhold the geography:
the 10 m coastlines place both routes unambiguously.

### 7. Data availability (journal paper)

The statement offered "aggregated tables underlying every figure". Five
tracked tables name what the manuscripts withhold: `muac_breakdown_operator`
and `muac_breakdown_citypair`, the `operator_top15` and `citypair_top15`
blocks of `strata_accuracy`, and the two waypoint tables. Two more
(`free_fuel_confirmed`, `free_fuel_opportunities`) carry one row per revision
pair with `ifplid`.

`run_24_release_tables.py` now writes `tables/release/`: the same aggregates
with each identity replaced by its rank within its own table, which preserves
every number and every ordering, plus a manifest naming the two row-level
tables as withheld. The stage asserts that the release copy of the operator
table drives the concentration figure identically. The statement in the paper
now says the tables are released in that form and that per-flight tables are
not part of the offer.

The related claim, "6 fly half of the confirmed fuel and 28 fly four fifths",
identifies by rank rather than by name and stands. Both ranks are measured
counts from `fuel_concentration.csv`; the concentration figure's caption said
they were part of an interpolation, and now says correctly that the two
points are measured and only the curve between them is drawn.

### 9. Composition of the quarter (journal paper)

One sentence, at the end of the strata discussion: the held-out quarter
carries no regulation on either route in 63.3 % of pairs against 70.6 % of
the archive, and reweighting the four regulation strata to the archive's mix
gives **67.1 %** against the 68.1 % headline, so about one point of the
headline is composition rather than skill. Nothing was wrong; a referee will
ask. `tables/composition_reweighted.csv`.

### 13. A subject swallowed by a comment (conference paper)

While paying for new prose inside the eight-page limit, a `% Cut for space`
comment was opened mid-line and swallowed the three words that followed it on
that line. The printed sentence read "One entry is a caution rather than a
finding: appears fourth even though…". Two independent zero-context readers
caught it; no proofreading pass would have, because the source looks correct.
This is the second time this trap has been hit on this project. **When a
replacement ends in a comment, the anchor must end at a line boundary, and
the rendered text must be checked afterwards.**

### 14. The journal abstract (311 words against a 250-word limit)

`SUBMISSION_NOTES.md` recorded 231 words on 2026-09-04 and the abstract had
grown to 311 since. Four passages were cut, each kept verbatim in a comment
immediately above `\begin{abstract}`: the comparison with earlier work's
generated alternatives; the sentence saying a channel offering the cheaper
route to everyone would be wrong more often than right (its second half was
kept and re-opened); the 44.9 % comparator, which only the simulation's
blindfold makes available and which the venue reader argued misleads in an
abstract; and "on the two extrapolation bases available", which no reader
could interpret without the body. The abstract is now 249 words by the
project's own strict count. Restoring any of the four costs the words back.

### 15. Numbers that disagreed with themselves

- The annualised CO2 range was "220 to 255 kt" in both abstracts and the
  conference conclusions, and "222 to 254 kt" in the journal body. The
  artefact (`tables/muac_annualised.csv`) gives 70.4 to 80.4 kt of fuel and
  254.0 kt of CO2 at the ×4 basis, so **222 to 254** is the pair with an
  artefact behind it. All four places now say it, and the conference abstract
  says "over the quarter", without which its arithmetic was impossible.
- The maximum contribution of the delay term appeared as "2.3 points" in one
  paragraph and "up to two and a half points" two paragraphs later. The
  maximum in `tables/shap_dependence.csv` is 2.324. Both now say 2.3.
- The stay-weight trade was quoted as "seven further points … a point and a
  half" in the journal paper and "7.6 … 1.4" in the conference paper, because
  the two compared different run families. Both now compare inside the sweep:
  **7.3 points of stay accuracy against 1.5 of revision accuracy**.
- The conference paper said operator identity "enters the model as an
  anonymous code only". It enters as a categorical feature whose values are
  ICAO designators, which is what the journal paper says and what the
  conference paper now says.
- The conference abstract said the model is untested beyond "6,672 pairs in
  which a flight kept its route". Only **1,093** of those are held out.

Also repaired, from the same reader flags: **seven section labels attached to
no sectioning command**, which resolve to whatever counter LaTeX last stepped.
One (`sec:calibration`) was referenced from nowhere and one (`sec:composition`)
likewise; both are deleted. The other five sat after a figure, a table or a
paragraph of body text and happened to render correctly, which is luck rather
than design: `\ref{sec:heuristics}` in the journal paper sits immediately
after `\end{figure}`, and a caption added above it would have turned every
"Section 6.1" in the paper into a figure number. All five are now attached to
their headings, and the rendered cross-references are unchanged — 4 to
Section 2.3, 7 to 6.3, 4 to 6.1 in the journal paper, and the conference
paper's "Sections IV-B and V" still reads as before. Further: two "so" clauses that asserted a causal
link between a data-handling arrangement and a modelling choice; the claim
that the waypoint sequence is the largest single term, which stood unhedged
in the background section nineteen pages before the section that shows it is
smaller than the four cost indicators together; and "the cleanest isolation
of pure ageing", which the same page had already said could not be isolated
from the difference in training volume.

---

## Fig. 2, regenerated (item 5)

The schematic carried **nine defects**, each verified by opening the PNG and
reading the panel. They were turned into an editing prompt, Gemini was given
the old raster as a reference, and the author accepted what came back on
2026-09-06. Five of the six that made the figure disagree with the
manuscripts are gone: the hinge-condition box (now an inset of penalty
against gap, falling smoothly and never reaching zero), the impossible fuel
precondition and its AND gate, the fourth cost indicator that was named but
not drawn, the grey routes in the proposal box, and the training labels
carried on the model's own outputs.

The sixth was resolved differently from the way the prompt asked. The
encoding panel now shows a single illustrative pair in which the chosen route
is the costlier on all four indicators. That is the commoner direction on
this archive rather than a universal one, and both captions now say exactly
that, which is more honest than the alternating pattern requested.

**Four label errors remain**, none of them repairable outside the image
model, and the first is a hard blocker because the number is quoted
throughout both papers:

1. the timeline reads **280 720** pairs where the test set is **281 720**;
2. stage 4 reads `gap ΔS = S+`, which is not an equation;
3. stage 3's upper token row repeats a token, `WP₁ · WP₂ · WP₂ · …`;
4. stage 2 reads "Balanced weights" where the stay pairs enter at an
   *increased* group weight of 10, so that the smaller set is not balanced
   away.

Two smaller things also survive: the "same flight · same day · same airline"
sub-label still sits in the archive panel, where it holds for revision pairs
only; and the raster is 1424 × 726, which is 278 dpi at the journal include
width but 199 at the conference one, against a 300 dpi guidance. A re-render
at twice the linear size settles that with the labels.

Two blocks the old raster carried are absent from the new one, the leakage
control and the "regulated flight" marker on the stay pair. Both are stated
in the text, and the simplification was the author's choice.

## Verified sound — do not "fix" these

### 10. Three "untouched share" figures

| figure | population | keyed on |
|---|---|---|
| 70.6 % | the eighteen-month archive | a regulation attributed to either route |
| 71.0 % | the held-out quarter | a delay attributed to either route |
| 63.3 % | the held-out quarter | a regulation attributed to either route |

"Seven revisions in ten carry no regulation on either route" sits under the
composition table and is the first row; "seven revisions in ten touch no
delay on either route" sits under the context table and is the second. The
two agree to within 0.4 points by coincidence and the third is the trap. Both
captions state their keying, and a third caption states that the ageing table
uses a fourth convention.

### 11. The stay-pair disclosures

All four disclosed properties hold exactly on the 1,093 test stay pairs
(1.000 each): the two routes belong to two different flights, the kept route
carries a delay and at least one regulation, and the alternative carries
neither. The text says "with no exceptions" and there are none.

The tension a reader will find — the model section argues that a score means
nothing except against another route for the same flight, and the stay
construction does exactly what that argument rejects — is now stated where
the bound is disclosed, in the threats section, rather than left for the
reader to assemble. It was first added to the calibration paragraph, where
two readers called it an orphan, and moved.

### 12. The strongest simple rule at 55.0 %

Scoped to rules preferring the route cheaper on one of the four planning
indicators, the claim is right. A referee can build a stronger rule from the
strata table — a majority sign vote over the indicators, inverted, reaching
63.3 % — but only because that table counts a tied indicator against the
newly filed route. Scored tie-neutrally, the best sign vote reaches **54.8 %**,
below the published 55.0 %. The claim survives under any tie-neutral
convention, and the caption now states the convention that invited the
construction. `tables/sign_vote_baselines.csv`.

---

## 8. The stay weight, measured

The papers state that "every threshold, calibrator and stopping decision is
taken on the tuning month alone", and `run_16_stay_weight_sweep.py` reported
each candidate weight's accuracy on the held-out quarter only, so the adopted
weight could not be shown to have followed that discipline. The sweep now
reports the tuning month as well, and was re-run.

The answer is favourable and it is now in the journal paper. Scored on the
tuning month alone, the three candidate weights rank exactly as they do on
the held-out quarter:

| stay weight | revisions, tuning month [%] | revisions, held-out quarter [%] |
|---|---|---|
| **10** | **67.46** | **68.19** |
| 30 | 67.08 | 67.75 |
| 100 | 66.59 | 66.47 |

A validation-only selection would therefore have adopted `STAY_WEIGHT = 10`,
the value in `_paths.py`, and the stay-side indicator does not argue
otherwise either: reg-blind stay accuracy on the tuning month is 53.6, 53.6
and 51.8. `tables/stay_weight_selection.csv`.

Two things to know about that re-run. It was done on a GPU, because the
sweep is a three-hour job per model on this machine's CPUs, and it does not
reproduce the published sweep to the decimal: 68.19, 67.75 and 66.47 against
the committed 68.20, 67.71 and 66.71, with early stopping firing at 8,595
rather than 9,993 iterations on the largest weight. The ordering, which is
all the decision turns on, is identical, and the differences are inside the
0.17-point seed spread of item 3. Because Table 8 of the journal paper quotes
the committed run, the re-run was written to
`results/weight_decision_rerun.json` and the published
`results/weight_decision.json` was left exactly as it was;
`run_16_stay_weight_sweep.py` now refuses to overwrite it, so no later re-run
can silently invalidate a published table.

---

## 16. What the venue reader challenged, and did not settle

A practitioner reading the journal paper cold raised the following. None is
settled by any artefact in this repository, none has been acted on, and each
is a judgement for the authors. They are recorded because they are the
questions a referee from this venue is most likely to ask.

- **The channel proposes on fuel alone and never checks en-route charges**,
  which in Europe routinely dominate fuel differences of the size in play
  (the median confirmed proposal saves 130 kg). Either the policy screens on
  total cost and the paper does not say so, or the channel can propose routes
  that save fuel and cost the operator money.
- **The economics of delay against fuel are never compared**, though Cook and
  Tanner is cited: half an hour of ATFM delay is worth two orders of
  magnitude more than the fuel a median escape pays for it. The reader's
  reading is that "cost rules fail" because the paper's cost rules omit the
  term that dominates the decision, rather than because airline preferences
  are exotic.
- **The threshold, the calibrator and early stopping are all fixed on March
  2026**, whose regulated share (5.2 %) is far below the test quarter's 8.6,
  16.2 and 22.6 %. The paper reweights the accuracy headline for composition
  and never reweights the channel's precision.
- **The calibrator adopted is the one that scored worse on the held-out
  quarter** (1.8 points of expected calibration error against the raw
  sigmoid's 0.9), and every operating point is built on it.
- **There is no capacity feedback anywhere**: a channel that moves tens of
  thousands of flights onto the fuel-cheaper, more direct routes is loading
  demand back onto the constrained volumes, which is the second use case's
  own subject.
- **"A reordering of a decision taken in any case rather than a new
  intervention"** is, on a finite-capacity route, an allocation of advantage.
  For a EUROCONTROL-authored paper this is the sentence most likely to be
  quoted back.
- **Terms a reader of this venue needs and does not get**: "planned fuel" is
  never defined (trip, block, or with reserves), on which every fuel and CO2
  figure and the 3.16 factor depend; "precision" is defined twenty pages
  after the abstract uses it; "sector" is used once in the commercial sense
  in a paper that otherwise says "volume".
- **Terms over-explained for this venue**: revealed preference and discrete
  choice, aircraft rotation, curfews, slot swaps, Wilson intervals.
- **Six separate assurances that nothing was tuned on the test set**, where
  one would do.

---

## What this pass changed, by file

Manuscripts: `trc-extension/trc2026.tex` and `sid2026/sid2026.tex` — the
repairs above, each with a dated `% CORRECTED` comment; no figure, no results
table and no reported metric was altered. Both build clean: the conference
paper at exactly 8 pages, the journal paper at 49, no overfull box, no
unresolved reference, no operator, city pair or waypoint named.

Study code: `run_23_referee_checks.py` (the arithmetic behind the items
above), `run_24_release_tables.py` (new, the de-identified release set),
`run_05_seed_ensemble.py` (the null accuracies), `run_16_stay_weight_sweep.py`
(the tuning-month columns), `run_10_report_assets.py` (a macro for a model
that was never trained).

Figures and their sources: `sid2026/make_maps.py` (the false justification),
`trc-extension/figures-src/fig_pipeline_paperbanana_chatgpt.md` (the nine
defects and the corrected Methodology text).

Documentation: `REPRODUCING.md`, `studies/2026-07-fuel-study/README.md`,
`trc-extension/SUBMISSION_NOTES.md`, `sid2026/COMPLIANCE.md`.
