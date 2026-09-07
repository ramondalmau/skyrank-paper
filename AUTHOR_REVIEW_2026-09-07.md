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

## A third round, and what it confirmed against the source

The seven fresh readers' findings were ranked by an eighth agent, which checked
several against the source rather than taking the readers' word. Four were
confirmed as real, not misreadings, and all four are now fixed.

- **The abstract said the model is fitted on the first fifteen months** while
  Section IV says fourteen, the fifteenth being the tuning month. Introduced by
  this pass's abstract rewrite; now stated as fourteen, tuned on the fifteenth.
- **Four readers explained the 55.0 % baseline back wrongly**, taking it for a
  sensible cost heuristic. It is the inverse of one, and the abstract says so.
- **The delay rule's 14.6 % against Table III's 24.0 %** — the omitted
  "and the two differ" condition, above.
- **τ was used in Section IV-B and given a value only three pages later.**

Six more were fixed because a reader failed on them rather than disliked them:
"the pairs that cost fuel lie elsewhere", whose antecedent this pass had moved
two pages away; the `therefore` in "route structure therefore carries
information", whose premise lived only inside Fig. 4 until the three attribution
values were put on the page; the change-bias sentence, which opened on a
before-and-after of an unnamed metric; "could not have been filed at all", which
two readers could not interpret at all and which now names a restriction or an
unavailable conditional route; 67.5 % denoting both the tuning month and the
low end of the test range, now with the months named; and "a demonstrated
alternative" in the stay-pair construction, which claimed more than same-day,
same-city-pair, same-type matching supports — the journal now discloses the
availability limit alongside the regulation confound.

One correction of domain fact, in both papers: **a regulation is attributed to
a flight, not to a route.** The papers said a route counts as regulated when a
regulation was attributed to *it*; they now say when the flight, while filed on
that route, had one attributed.

Paying for those cost one more cut: the Conclusions' second finding restated
the label-construction argument that the Introduction claims and Section II-A
argues over three paragraphs, and a reader reported meeting it three times. It
is replaced by a result the Introduction cannot state, namely that the model's
margin is widest where cost logic fails.

**The panel's verdict is that the paper is still not clean by the zero-context
standard**, and that is reported honestly rather than smoothed over: seven
readers returned thirty "confusing" verdicts between them, most on the second
and third readings of dense material. What survives is listed below and is
either fenced or structural.

## Surviving, and why each was not acted on

1. **Table III's strata are defined on quantities derived from the label**, so
   conditioning accuracy on them and reading the spread as evidence about the
   model is arguably circular. The reader's proposed test — report the inverted
   fuel rule's own accuracy inside each stratum — would settle it and would
   strengthen the finding if the model wins everywhere. That is new analysis and
   a change to what a results table presents.
2. **Section IV-A carries twelve ideas in one undifferentiated run**, and the
   proposed fix is to split it into two subsections. That is a structure change.
3. **Fig. 2's stage-1 annotation says "same flight, same day, same airline"**,
   which contradicts the stay-pair construction drawn two boxes to its right,
   and stage 3 draws one bar per indicator where the caption promises a pair.
   The figure was closed on 2026-09-06 after three generation rounds; this needs
   a fourth.
4. **The provenance of the four cost indicators is never given** — no
   performance model, no forecast source, no charging formula or unit-rate
   vintage. Since the two routes of a pair are costed hours apart, part of a
   fuel difference may be the forecast update rather than the route. Neither
   paper can answer this from the record; the authors can.
5. **The compelled-revision share is unquantified.** Both papers now say a
   revision need not be a choice, and the journal says the archive holds no
   field that separates the two. A bound would need work outside this archive.

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
4. **The journal abstract kept its results.** The sentence the author objected
   to is not in it, and a 50-page paper's abstract carries more result detail by
   convention than a conference paper's, so it was not turned into an overview.
   It has since been corrected on the two points of the fourth round below, and
   it remains an open offer to give it the conference paper's treatment.
5. **The journal is now 50 pages, up from 49**, from the additions above.

## A fourth round: the abstract's limitation, and the third paragraph

The author read the revised conference paper and made two points. First, that
the abstract's closing limitation is one the paper itself refutes: *"but we
prove that this is not a problem"*. Second, that the third paragraph of the
introduction is still confusing. Both are upheld, and both applied to the
journal as well.

### The abstract described a model the paper does not use

What it said:

> The archive is built from flights that changed route, however, so the model
> is largely untested on the majority that stay, and it may propose change more
> readily than airlines would accept it.

What the body reports, in Section V-B: a model trained on revisions alone is
right on **34.8 %** of the held-out stay pairs, so it prefers the alternative in
65.2 % of the cases where the flight demonstrably kept its own route. Adding
stay pairs at group weight 10 raises that to **90.0 %**, at a cost of 0.8 points
on the revision metric (68.1 against 68.9). The same model scores **88.0 %** on
the 30 953 escapes, which no rule keyed on regulation status can do, since such
a rule is right on every stay pair and wrong on every escape by construction.

So "largely untested" was false — the model is tested on that population, and
the correction is the largest any design choice in the paper makes. A
zero-context sceptic asked to compare abstract against body reached the same
verdict independently: *"It understates, and the wrong word is 'most'... the
corrected model is more accurate on staying traffic (90.0 %) than on its own
headline population (68.1 %)."*

Two further defects in the same three sentences, both found by readers:

- **"recommends change too readily" understates the defect.** The revisions-only
  model is not over-eager, it is inverted: 34.8 % is fifteen points worse than a
  coin toss. The abstract now says the model *"urges change on flights that in
  fact kept their route, and does so more often than not."*
- **Neither abstract let a reader build the object.** Two readers, one of them
  the ATM practitioner, stopped at the same place: *"A pair means two routes; if
  the airline kept its route, where does the second route come from?"* — and the
  practitioner added that if the answer were a generated route, it would
  reintroduce the label problem Section II-A spends a page rejecting. Both
  abstracts now say the pair matches *a kept route against one a similar flight
  flew that day*.

The conference abstract is 249 words, the journal's 250; the journal paid for
the addition with four wording trims, listed in the edit scripts.

### Paragraph three, and why it was worse than unclear

A zero-context ATM reader rated it **the weakest passage in the two pages** and
gave four reasons, three of which are about correctness rather than style.

1. **The PRC indicator was mislabelled.** The paragraph reported the figure as
   an excess over *"the shortest available track"*. The reported horizontal
   flight-efficiency indicators are measured against a direct reference between
   the points at which traffic enters and leaves the airspace. The reader also
   showed the paragraph fails either way: if the reference genuinely were a
   shortest *available* route, then routes closed by a restriction or an
   unavailable conditional route are netted out of the reference already, and
   the paragraph's own clause about them describes something the figure excludes
   by construction. **Corrected in both papers, and flagged in the source for
   the author to confirm against the report's own wording.**
2. **It split the published figure into two bins**, unavoidable capacity
   protection and recoverable opportunity, which omits airspace structure,
   reserved airspace, wind-optimal routing that flies further on purpose and
   charging-zone avoidance. The paragraph now says only that many things
   contribute to the figure and that this archive speaks to one of them.
3. **The attribution was one-sided, which is the author's own comment
   recurring.** The unavoidable share was described neutrally, "what respecting
   that capacity costs", while the residual was attributed to the operator:
   *"nobody had reason to look for them in time"*. The reader's objection is
   that European flight-planning systems already optimise against the full route
   network, RAD and CRAM, repeatedly, up to dispatch. The sentence now states
   the assumption without naming a party at fault.
4. **"Candidate routes, in short, are not the scarce thing"** claimed to
   summarise a sentence that had just said some candidates were closed and
   unavailable. Both readers lost the thread there. The summary marker is gone
   and the two ideas are in the order that makes them agree.

The paragraph is seven words shorter than before and one line shorter in print.

### One reader's artefact hypothesis, checked against the code

The sceptic proposed a specific way the 90.0 / 88.0 argument could fail: if
flight-level features are harmonised only within revision pairs — the rule is
stated in terms of "the later message", which a stay pair does not have — then a
stay pair's two rows would differ in operator, hour and connection state, giving
the model a population flag, after which regulation status settles the label.

**The mechanism does not exist.** `build_stay_features()` calls
`build_features()`, which calls `_harmonize_pair_features()`
(`src/skyrank/data/features.py:295, 346-362`), so a stay pair's alternative row
takes the values of the flight that stayed, exactly as a revision pair's takes
the values of the later message. The journal now says so in the leakage
subsection, with the reason in a source comment. What the reader could not have
known from the paper is now on the page; what remains — that a model might
recognise the construction by some other cue — the paper already concedes in its
conclusions, and that concession stands unchanged.

### Routed to the authors from this round

These are domain judgements or changes to what the papers claim, so none was
applied.

1. **"The difference between a flight's calculated and requested take-off times
   is its attributed ATFM delay."** The ATM reader says there is no *requested*
   take-off time: ATFM delay is CTOT minus ETOT, the estimated take-off time.
   Both papers use the "requested" framing deliberately and consistently, so it
   was left alone; if it is a gloss rather than a term, saying "estimated
   take-off time" once would remove the objection.
2. **Re-filing re-triggers slot allocation.** A proposal accepted late can leave
   a regulated flight with a worse CTOT than the one it holds, so a proposal
   channel can create delay. The journal mentions "the departure slot it already
   holds" in the trade-off; neither paper states the mechanism. The reader calls
   this "a live operational objection left unaddressed".
3. **"File a route that avoids the constrained volume at the cost of distance,
   fuel and en-route charges"** is false as a general rule: charges depend on
   distance per charging zone at that zone's unit rate, so a longer detour that
   skirts an expensive zone can reduce the bill, and a longer track can burn
   less fuel on the day's winds. The reader notes this is consistent with the
   paper's own finding that the cheaper-fuel rule scores below chance.
4. **"The same delay on the last leg of the day may well be cheaper than the
   detour."** The reader argues the last rotation is where crew duty limits,
   curfews and out-of-base positioning bite, so it may be the expensive case
   rather than the cheap one.
5. **"Planning cost points the wrong way"**, standing alone in the journal
   abstract, reads as a claim that European airlines systematically choose to
   burn more fuel. The composition caveat that explains it is on page 2.
6. **"The network" is used for two different things** — the Network Manager as
   an actor and the airspace network as a system — three lines apart on page 2.
   Saying "Network Manager" once would settle it.
7. **90.0 % and 34.8 % are reported without confidence intervals**, where
   Table III gives Wilson intervals on everything else. On 1 093 pairs the
   interval is not negligible.
8. **"Precision", "calibrated", "operating point" and "the published points it
   uses"** were all flagged as load-bearing terms an ATM reader cannot cash. The
   first three carry whole contributions.

### Verdicts, quoted

- Outsider, full read of pages 1-2: abstract **mostly clear**; introduction ¶1
  **understood**, ¶2, ¶3 and ¶4 **mostly clear**. On flow: *"Mostly yes, and
  noticeably better than most technical prose... But there are three places
  where it is a list wearing a coat"* — the four revision prompts, the
  First/Secondly/Thirdly contributions, and the abstract, *"ten findings
  compressed into ten sentences at uniform pressure"*.
- ATM practitioner: both abstracts **mostly clear**, conference introduction
  **mostly clear**, paragraph three on its own **confusing / contestable**.
- The fixes above answer every load-bearing flag those verdicts rest on except
  the three list-shaped passages, which are structure rather than sentences.
