# The author's review of 2026-09-07, and what it changed

The author read the conference paper and returned fourteen comments, covering
the abstract, the introduction, the background, the methodology, the results
and the conclusions, with the standing instruction that anything applicable be
changed in the journal paper too. This file records what each comment produced,
what a fresh zero-context reader panel found alongside it, what had to leave the
conference paper to make room, and the one choice left open.

Both papers build clean: the conference paper is exactly 8 pages with a
224-word abstract, the journal paper 50; no overfull boxes, no unresolved
references, and the neutrality sweep names no operator, waypoint, volume or
city pair beyond the authorised Amsterdam–Barcelona anecdote.

## The author's comments

| # | Comment | Disposition |
|---|---------|-------------|
| 1 | The abstract's "a stronger record of preference than earlier work had" is unclear and unrelated to the paper | **removed**; the claim is argued properly in Section II-A, which is where it belongs |
| 2 | The abstract reads as a summary of results; it should be an overview of the paper | **rewritten**: 249 → 224 words, eleven result figures down to two (68.1 and 55.0), the channel described rather than tabulated |
| 3 | Introduction, first paragraph: what about route charges? | **added**, and verified: that flight also paid 466 euros more in en-route charges |
| 4 | Introduction, second paragraph: not only the network — reactionary delay and turnaround slack, changed weather, "it is not that simple" | **rewritten** around four prompts: a regulation, an aircraft late off its previous leg, an updated forecast, and a route that ceased to be filable, the last of which makes the revision not a choice at all |
| 5 | Introduction, third paragraph: do not blame the airlines; we are EUROCONTROL | **rewritten**, both papers: the extra distance is now the cost of respecting a capacity that has to be respected, the trade is the operator's judgement, and the archive shows it made in both directions |
| 6 | Introduction, fourth paragraph: "generated candidates" is used before it is explained | **glossed in place** |
| 7 | Background: the "each filing is a separate message" sentence is not clear; it is simpler than that | **rewritten**, both papers: every filing is a message, so is every change, the network keeps them all, and a route change is a pair of consecutive messages |
| 8 | Background, Section A: say that most route changes are **not** about delay | **added**, both papers, before the regulation material rather than after it |
| 9 | The real objection to generated alternatives is that we do not know whether they ever reached the dispatcher's screen; with a revision pair both routes were seen for certain | **rebuilt**, both papers: that argument now leads, and the older "the model need only recognise a filed plan" argument follows from it |
| 10 | Is Fig. 1 referenced anywhere? | It was, once, as a bare parenthetical a page before the figure. It is now a sentence that sends the reader to it |
| 11 | Methodology: "escapes" is not clear | **defined in place**; a `% Cut for space` comment had removed the only explanation of what an escape is and why it mirrors a stay pair |
| 12 | Methodology: the calibration is confusing, the second paragraph too long and dense | **redrafted** as five paragraphs from one, opening on a real pair scored −2.82 and +0.90 |
| 13 | Results: tedious, dense, difficult to follow, long | **restructured**; see below |
| 14 | Conclusions: state the limits of the bag of words, and the route-embedding attempt that failed but is worth investigating | **added** to both papers, from the record |

## What "tedious" turned out to be

A panel of eight zero-context readers read the version the author reviewed, and
one of them measured Section V: 2 220 words carrying 90 numeric tokens, about
one number every 25 words. Three structural causes, all now addressed.

- **Numbers delivered as prose with the arithmetic left to the reader.** The
  worst case was a 121-word sentence carrying four baselines and an inline
  equation; it is now four sentences. Where the text asked the reader to
  subtract, it now prints the answer: 13.1 points over the best single rule,
  26.0 points between the first and last rows of the third block.
- **Paragraph length ran inverse to paragraph importance.** Eight of
  twenty-four paragraphs were a single sentence carrying no result, while three
  carried a third of the section's words. The stubs are folded into what they
  announced; the 325-word stratum paragraph is now three.
- **Paragraphs opened with a verdict and closed with a caveat, so the number
  was always in the middle.** The openers are inverted: the per-month
  paragraph, the change-bias paragraph and the stay-pair paragraph now begin
  with their findings.

## Corrected against the record

Each carries a dated `% CORRECTED` comment beside it in the source.

1. **En-route charges were missing from the introduction's list of what the
   detour cost.** The pair is `ich_dataset_2026-05.parquet`, `pair_id` 1421263:
   `kpiRouteChargeIndicator` 1274 → 1740 EUR, a difference of 466. Units per
   `run_01_eda.py:41`. Both papers.
2. **The feature table claimed every rotation and context feature carries the
   same value on both routes.** The outbound connection time does not, by
   design: `_harmonize_pair_features` adjusts it by the within-pair duration
   delta, and `run_02_leakage_audit.py:30` records that it is deliberately
   excluded from `_HARMONIZE_COPY`. Both captions now state the exception, and
   the conference paper's attribution paragraph no longer says all four
   flight-level entries are identical.
3. **The journal paper said a probe "recovered the waypoint identities".** It
   did not. The classifier was fitted on the difference between the two routes'
   embeddings and asked to separate the preferred route from the abandoned one,
   scoring about 0.54 and 0.574 in the two trials, both near chance
   (`studies/2026-06-improvement/docs/research_ideas.md`, sections 1 and 4).
4. **Harmonisation did not say to which value.** It says now: both routes take
   the value carried by the later message, which is why the filing-time feature
   ends up at the pair minimum.
5. **An example refuted the claim it illustrated.** "A generated candidate may
   cross airspace the operator never uses, or follow a track its own system
   would discard on company policy" offers two facts about preference and then
   says no knowledge of preference is involved. Both papers now use a surface
   cue instead.
6. **The conference paper's flagship worked case carried no atypicality
   caveat** while the journal's did. Moot in the end: the case was cut for
   space, and the caveat travelled with it.

## The bag of words, and the encoder that did not replace it

Written from `studies/2026-06-improvement/docs/research_ideas.md` (sections 1,
4 and 9) and commit `5485bd5`, which removed the encoder from the codebase.

The waypoint sequence enters as a bag of published identifiers, so what the
model holds about route structure is a vocabulary and not a geometry. Two
limits follow: the identifiers are European, so little of the 1.4 points the
text is worth would survive a move to another region; and identifiers are
revised from time to time as the route network is republished, so a piece of
airspace can return under a name the model has never met.

The remedy tried was a neural encoder over a translation-, rotation- and
scale-invariant description of the route's shape. On its own it scored worse
than the tokens; supplied alongside them it was worth a fraction of a point,
far too little to repay a second model in the serving path. A linear classifier
on the encoder's own representation separated preferred from abandoned routes
barely better than chance, which places the limit on the geometric input rather
than on the training objective — richer per-step geometric channels were tested
later and did not help either, being deterministic functions of the base
sequence. The per-route shape statistics of that proposal (detour ratio, turn
statistics) were never tested, and are where the direction still has room.

**The accuracies of those trials are deliberately not quoted in either paper.**
They predate the 2026-09-01 archive repair and are not comparable with anything
these papers report; only their ordering is claimed.

## What left the conference paper, and why

The author's additions came to about 66 lines on a paper that was already
exactly 8 pages, and the panel's load-bearing repairs added roughly 15 more.
Everything below is in a `% Cut for space 2026-09-07` comment in the source,
verbatim, and can be restored the moment a page is available. Nothing that
left is a finding; every number the abstract or the conclusions rely on is
still in the body.

| Cut | Lines | Why it could go |
|-----|------:|-----------------|
| The worked proposal, one flight followed end to end (Section V-D) | 28 | The largest single block in the section the author asked to shorten; the journal carries the same case in full, with its distance and its median comparison. τ = 0.600, the 79.2 %, the one-in-five proposal rate and the meaning of the validation are all stated elsewhere |
| The confident-error case study, the 124-minute flight (V-C) | 11 | A second single-case narrative in one section |
| The attribution caution on rotation and context features (V-C) | 9 | A caution about an artefact of the exhibit, not a finding |
| The ceiling caveat, "68.1 % is not near the ceiling" (V-A) | 8 | The least load-bearing of the paper's twelve "this does not establish" moves |
| The stay-weight sweep trade-off, w = 30 and w = 100 (V-B) | 7 | Four bare decimals in one sentence; five of eight readers failed on it. The journal reports the sweep as a table |
| The 2025 replication (V-A) | 6 | The journal measures ageing directly, month by month over half a year |
| Two invitations to skip ahead (Sections II and IV) | 4 | Both pointed past load-bearing material; one reader took the second and skimmed the rest of the paper |
| Assorted restatements: the composition figures now given in Section II, the delay rule's coverage, the harmonisation rule, two announcement stubs | 12 | Said once already, within a page |

## The re-verification round, and what it caught

Seven fresh readers, none of whom had seen any earlier version, read the
revised conference paper. The calibration subsection, which one reader of the
first panel had rated "not at all", came back understood on the definition, on
the worked scores and on why the worse-calibrated mapping was kept. Five
defects survived or were newly exposed, and all five are fixed.

1. **The training objective was self-contradictory on a first read.** "the
   model is penalised according to how far the abandoned route's score sits
   above the chosen one's, and the penalty shrinks as the gap between them
   grows" uses "gap" in two opposite orientations in one sentence, and the
   only available first reading is a contradiction. Rewritten in both papers to
   hold one orientation throughout, and "never quite reaches zero" now attaches
   to the penalty, where it is true, instead of to the gap, where it is not.
   This sentence predates this pass.
2. **The delay rule's coverage was stated with one of its two conditions.**
   The paper said the rule can decide the pairs on which "both routes carry a
   delay figure at all", which is 24.0 % of the quarter by Table III, and then
   gave 14.6 %. The rule's own definition is
   `decided = a.notna() & b.notna() & (a != b)` (`run_01_eda.py:107`): the two
   delay figures must also **differ**. A reader found the clash and could not
   resolve it. The conference paper now states both conditions; the journal
   already did ("only ever decides on the 14.6 % of pairs where delay differs
   at all"), which is how the omission was confirmed rather than guessed.
3. **A participle attached to the wrong antecedent** in "better calibrated than
   the isotonic fit chosen to correct it, missing the observed rate by 0.9
   percentage points on average against 1.8", so a reader taking proximity gets
   the two numbers the wrong way round and concludes the fitted mapping is the
   better one. Split into two sentences with each number named.
4. **Cutting the attribution caution orphaned Fig. 4.** Three of its bars are
   flight-level features that the methodology says are identical on both
   routes, and the paragraph explaining that they measure interaction was the
   9-line cut above. A reader could not tell whether the figure or the
   methodology was wrong. The explanation is now two lines of the caption,
   which is cheaper than the paragraph and sits where the question arises.
5. **Two referents in the Conclusions went nowhere.** "the four together
   outweigh it" had no antecedent on the page, where everything said three, and
   "one of the deployment conditions above" pointed at a condition that is not
   one of the three. Both named explicitly. A third fix: "supports operation at
   a selected precision ... it is right 94.9 % of the time" attached an
   accuracy figure to the word precision, which the same paper is careful to
   distinguish from accuracy.

Two further changes came from the same round. The introduction gave three
reasons for revising a plan, two of them delay, so page 1 taught the opposite
of what page 2 says; the regulation prompt is now marked as the most visible
but not the commonest. And the channel's fuel total now says at first mention
that it is counted only where the airline's own later filing chose the route
proposed, which is what one reader could not establish.

## The one choice left open

Holding 8 pages cost the worked proposal. There is exactly one alternative of
the same size, measured rather than estimated:

- **as it stands** — the worked proposal is cut, Fig. 1 stays: 8 pages.
- **the swap** — restore the worked proposal and cut Fig. 1, the two-panel map
  contrasting the label constructions: also 8 pages, verified by building it.

The worked proposal was chosen for the cut because the author's own comment
asked for Section V to be shorter, because it duplicates the journal, and
because removing a figure the author had asked to have *referenced* seemed the
wrong reading of that comment. The swap is one instruction if the author
prefers the concrete case to the figure.

Both were measured. Cutting either alone leaves the paper at 9 pages unless the
other trims below are also made, which they are.

## Routed to the authors

1. **The worked case's physics.** In the journal's worked example (Section 7.4) the chosen
   route burns 2 016 kg less planned fuel, about a quarter of the trip fuel, at
   essentially the same distance (1 707 against 1 690 NM) and flight time
   (258.2 against 259.5 min). A domain reader on the panel called that
   physically incoherent at a fixed cruise level and cost index, and the archive
   holds no vertical profile, so the paper cannot say whether the difference is
   a level cap, a mass difference or the wind on a different track. The journal
   already says the case is far from typical. The options are to state the
   vertical caveat, to choose a different case, or to leave it: all three change
   what a result presents, so none was taken here.
2. **Table IV could carry the sweep and the full-scale figures as columns**
   rather than as prose and caption retractions. That changes what the table
   presents, so it is proposed, not applied.
3. **The title asks what an airline will accept**, while the paper says plainly
   that acceptance is never observed and every figure rests on what the airline
   filed next. Two readers noticed and respected the admission; one thought the
   title then promises what the paper declines to deliver.
4. **The journal abstract was left alone.** The sentence the author objected to
   is not in it, and a 50-page paper's abstract carries more result detail by
   convention than a conference paper's. Say the word and it gets the same
   treatment.
5. **The journal is now 50 pages, up from 49**, from the additions above.
