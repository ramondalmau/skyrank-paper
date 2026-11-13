# Response to Reviewers — SIDs 2026
"Learning Airline Route Preferences from Flight-Plan Revisions to Support Fuel-Efficient Alternatives"

We thank the reviewers and the editor for the careful reading. Point by point below.

---

## Reviewer 1

**R1-1 (template and page numbers).** *The submission was set in the wrong template and is missing page numbers.*
We have re-set the manuscript in the official SESAR Innovation Days 2026 template (IEEEtran conference, A4), keeping only the paper's own deliberate typesetting settings on top of the venue preamble. Page numbers are now present on every page.

**R1-2 (weather / winds of the day).** *It is unclear whether the flight time of the flown route uses the winds of the day.*
The model never recomputes a route's flight time against the winds of the day, nor does it take the day's weather as a separate input. Both flight time and planned fuel are read exactly as the filed plan projected them, so weather enters a comparison only through the plan it already shaped. This is now stated plainly at the start of the Data and pair-construction subsection (Section III-A): the four route indicators are the plan's own estimates, and the model learns which of two recorded plans an airline kept, given the plans as filed — not what the weather that day would have favoured.

**R1-3 (references).** *The reference list is somewhat limited; please add NASA work on the most-used waypoints / route analysis.*
The reference list has been expanded, and the related-work section now engages directly with the NASA line of work the reviewer points to: predicting the operational acceptance of airborne reroute requests (Evans, Lee, Sridhar 2018; Evans and Lee 2019), demonstrating airline-based airborne reroute operations with trajectory option sets (Lee et al. 2021), defining and visualising dynamic route structure and traffic corridors (Zelinski and Jastrzebski 2011; Paradis and Davies 2022), and measuring the cost of confining optimisation to published waypoints (Karr, Vivona and Wing 2018). We also add the discrete-choice economics of European route choice (Sha et al. 2015) and machine-learning prediction of pre-tactical routes and flight levels from the UPC group (Mateos Villar et al. 2020), and fold two collaborative-ATFM references (Castelli et al. 2012; Pilon et al. 2021) that were previously held in a cut note. Ten new references were added; all were verified against CrossRef, the arXiv API, OpenAlex or the issuing body's own records.

**R1-4 (hard to follow / dense ML terminology).** *Well written but hard to follow; very specific ML terms are used extensively.*
We have run the method and results sections through a zero-context reader pass and redrafted the passages that did not make themselves clear on a first read — see the interpretability revisions below (also responsive to R3-1).

---

## Reviewer 2

**R2-1 (recommendation).** We are grateful for the positive assessment.

**R2-2 (references).** The list has been expanded as described under R1-3.

**R2-3 (caption explanations).** *The explanations carried in the captions of Table I, Table II and Figure 4 should be moved into the main text.*
The operational content of those captions — what "regulated" means in Table I, which feature groups are route-level versus flight-level in Table II, and that Figure 4 shows the *difference* in Shapley value between the two routes — has been carried into the body text where each table and figure is first discussed, so a reader following the paper linearly meets the explanation before the float. See the interpretability revisions below.

---

## Reviewer 3

**R3-1 (method not easily interpretable).** *The method is very detailed yet complicated and not easily interpretable.*
We have redrafted the method and results for readability: the leakage-and-harmonisation explanation is now carried in a single connected thread rather than split across three paragraphs, undefined group labels are introduced where they first appear, and the interpretability results (feature attributions) are stated once, plainly. See the interpretability revisions below.

**R3-2 (Table I appears two pages after it is referred).**
In the current manuscript Table I is referred to at the foot of page 3 and appears at the top of page 4 — adjacent, not two pages apart. The earlier draft the reviewer saw had the table deferred by content that has since been cut; the current build places it immediately after its first reference.

**R3-3 (Table III appears before Table II).**
In the current build the tables are numbered I, II, III and IV in order of appearance (verified in the build's `.aux`), and the rendered order on the page is I, II, III left-to-right and top-to-bottom. The inversion the reviewer saw was an artefact of float deferral in an earlier draft; it does not reproduce in the current build.

---

## Editor's note

**E-1 (page limit).** The page limit has been raised to nine; the manuscript now runs to nine pages.

**E-2 (Use of AI disclosure).** A voluntary "Use of artificial intelligence" statement has been added at the end of the paper, describing the two limited roles in which generative tools were used (initial artwork for the workflow diagram, checked and corrected by hand; and language/clarity assistance with the prose), and affirming that the scientific content is the authors' own and was verified against the study's code and records.

---

## Interpretability revisions (responsive to R1-4 and R3-1)

To test readability we ran the method and results sections past four
zero-context readers — researchers who had seen neither the project nor a
draft — asking each to read linearly and quote any sentence they had to
re-read. We then redrafted every passage they flagged, and the changes
below are the ones that cleared the bar (a redraft is accepted only when a
fresh reader can follow it on one pass). The most-convergent flags — the
weather sentence, the flight-level/route-level split, and the group labels —
were raised by all four readers.

**Data and pair construction (Section III-A).**

- *Weather / winds of the day (R1-2; all four readers).* The opening
  paragraph now leads with the simple point — planned fuel is the estimate
  attached to the recorded plan, not a post-flight measurement — names the
  four route indicators (flight time, distance, planned fuel, route
  charges), and states plainly that the model reads them as the plan filed
  them and never recomputes flight time against the winds of the day. The
  earlier "weather reaches a comparison only through the plan it already
  shaped" and "bears directly on the travel-time difference" sentences were
  removed.
- *What a pair is.* The pair is now introduced as two plans for one flight,
  filed weeks apart, the second replacing the first; the undefined "the
  later message" is replaced throughout by "the later filing."
- *Leakage.* "It would be invisible in the accuracy figure" is replaced by
  "a high accuracy would hide this — the model would look skilled while
  merely reading the filing dates," which says what was meant.
- *Flight-level vs route-level features (flagged by all four).* A single
  connected paragraph now defines the two feature classes: route-level
  features (the four indicators, the regulation fields, the waypoint tokens)
  differ within a pair; flight-level features (operator, aircraft type, city
  pair, connection times, time to departure) are harmonised by taking each
  one's value from the later filing, which leaves both routes carrying the
  smaller time to departure and closes the timing shortcut. The Table II
  caption explanation (which features are route-level vs flight-level) is
  folded into this paragraph per R2-3.
- *Normalisation.* The three paragraphs that split the normalisation and
  harmonisation story are merged into one; the hedge about "a common earlier
  decision time" and the unsupported "every operator values a 300 kg
  difference equally" sentence are removed.
- *Regulation groups.* "Regulated" is defined where first used; the group
  labels are made consistent (the earlier broken quote around "left
  regulation" is fixed), and the two-percentage mapping is made explicit so
  the median-fuel increase and the share of replacements burning less fuel
  are clearly the two tails of the same distributions.
- *Table I caption.* Its operational content (what "regulated" means, the
  row structure) moves into the body per R2-3; the caption is trimmed to one
  sentence.

**Results.**

- *Group weight.* The phrase "their greater group weight increases their
  contribution to the ranking loss," which appeared nine paragraphs before
  the concept was ever explained, now reads "each stay pair carries a larger
  group weight, so it contributes more to the ranking loss than a revision
  pair does."
- *"Old route only" stratum.* The parenthetical now defines it: "the stratum
  where only the abandoned route carried a regulation."
- *Baseline arithmetic.* The 53.2% figure now shows the blend it is —
  "weighting the two groups gives 53.2% overall (0.146 × 71.6% + 0.854 ×
  50%)" — so the reader need not reconstruct it.
- *Terminology.* "Cost indicator," which had displaced the method section's
  "route indicator" for the same four quantities, is restored to "route
  indicator" in both remaining uses.
- *"The channel."* The three prose uses of "channel," never defined, are
  replaced by the paper's own established term — the policy that selects and
  proposes (it already reads "the policy selects" and "the policy proposes"
  elsewhere).
- *Two confidence slices.* The top-25%-by-gap error-share figure now states
  it counts "the same high-confidence pairs … by where their errors fall
  rather than by their accuracy," distinguishing it from the earlier
  top-20%-by-confidence accuracy figure and removing the appearance of an
  inconsistency between "fifth" and "quarter."
