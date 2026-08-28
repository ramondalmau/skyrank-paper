# TR-C extension of the SID 2026 paper — working outline

Target venue: Transportation Research Part C: Emerging Technologies (Elsevier).
Base paper: `paper/sid2026/sid2026.tex` (8 pages, SESAR Innovation Days 2026).
Evidence base: `studies/2026-07-fuel-study/tables/` (22 tables, all cited numbers
below are read from those files, none from memory). Items marked **[NEW RUN]**
require computation that does not exist yet; items marked **[VERIFY]** require a
check against the journal's current Guide for Authors before submission.

---

## 1. Why TR-C, and what the journal will ask of us

TR-C publishes methodological work on emerging technologies applied to
transport operations, and machine-learning papers on air traffic management
(delay prediction, trajectory prediction, demand modelling) appear there
regularly. The fit is the method: a revealed-preference labelling scheme that
turns an administrative archive (flight-plan revisions) into supervised
ranking data without a route generator. The fuel case study is the
application that proves the method matters, not the headline.

What the journal will demand beyond the conference paper:

1. A genuine literature review (the SID paper folds prior work into one
   column; TR-C expects a section situating revealed preference, learning to
   rank, and route-choice modelling, including the discrete-choice literature
   that TR-C readers know well).
2. At least one generalisation experiment beyond the single MUAC quarter.
3. A full treatment of label semantics and threats to validity (the material
   the 8-page limit forced us to compress into single sentences).
4. Formal statistical care: paired tests for ablations (already computed,
   McNemar in `ablations.csv`), confidence intervals everywhere (already in
   the tables).

[VERIFY] Current TR-C Guide for Authors: highlights format, abstract word
limit, declaration sections, data-availability policy, and whether a
conference-extension statement is required. Do not assume any of these.

[VERIFY] EUROCONTROL neutrality review: `muac_breakdown_citypair.csv` and
`waypoint_preferences.csv` name airports and waypoints. The operator
breakdown must remain anonymised (ranks, not names) as in the SID paper;
whether named city pairs and waypoints pass the neutrality constraint is an
author decision to take before drafting Section 7.

---

## 2. Title candidates (his patterns: plain noun phrase or direct question)

1. "Learning airline route preferences from flight-plan revisions"
2. "What filed flight plans reveal about route preferences, and what that
   knowledge is worth in fuel"
3. "Do airlines prefer the routes we compute for them? Revealed preference
   from flight-plan revisions versus generated candidates"

Recommendation: (1) as the sober default; (3) if the generation-baseline
comparison (Section 8, stretch goal) is actually run.

## 3. The contribution statement (threefold, prose ordinals)

The contribution of this paper is threefold: first, a labelling scheme that
extracts pairwise route preferences from the revision history of filed
flight plans, requiring no route generator and no stated-preference survey;
second, a bias analysis showing that pairs in which the airline kept its
route despite a regulation ("stay pairs") are indispensable for unbiased
deployment even though they cost screening accuracy; third, a deployment
analysis at the level of a European area control centre, quantifying the
fuel that confirmed proposals would save at operating points chosen for
precision, together with how that value concentrates across operators.

---

## 4. Section skeleton, with the evidence behind every section

### S1. Introduction
Reuse the SID introduction's operational opening, expanded. The predecessor
limitation (a generated candidate may cross airspace the operator never
uses) is already written at journal quality in the SID §III; it moves here
and becomes the motivating problem. Roadmap paragraph at the end.

### S2. Literature review **[mostly NEW TEXT]**
Three threads, chronological within each: route-choice and discrete-choice
modelling in transport (the TR-C-native thread); learning to rank
(Burges/PairLogit lineage); ATM route prediction with generated candidate
sets (the thread the SID paper cites). Each closes by tying back to the gap:
none of them learns from what airlines actually filed and then withdrew.

### S3. Data and the pair-construction method
Expanded from SID §II with the room the journal gives us:
- Corpus composition (`composition_ich.csv`): 1.14 M revision pairs, of
  which 69.4 % unregulated, 8.3 % escaped a regulation, 11.0 % reduced
  delay, 9.8 % kept or raised delay. The four decision contexts get the
  worked examples the conference cut.
- Stay pairs (`composition_stay.csv`): 6 672 pairs; the flight that stayed
  faced a median peak delay of 31 min; in 47.5 % of them the kept route
  burns more fuel than the alternative (median −3 kg), which is the
  cleanest evidence that fuel alone does not explain filing behaviour.
- Monthly corpus profile (`eda_monthly.csv`): lateral-change share and
  regulated rate per month, the seasonal structure the SID paper had no
  space to show.
- Missingness (`missingness.csv`), restored case-study maps
  (`figures/map_escape`, `map_saver`, scripts already in the repo).

### S4. Why leakage is the central design problem **[promoted to its own section]**
The SID §II-A leakage passage (time-to-departure gives away the label)
expands with the ablation that proves the point with a number: removing the
relative encoding (`no_norm` in `ablations.csv`) drops screening accuracy
by 9.7 pp, from 60.6 % to 50.8 %, i.e. to chance. The section the user asked
for at SID ("why feature normalisation matters, with examples") becomes a
full journal section with the worked 2 000 kg / 300 kg example and the
stay-pair giveaway rule.

### S5. Model, calibration, and ablations
- Model and pairwise objective (SID §IV, expanded derivation).
- Full ablation table (`ablations.csv`) with McNemar tests: no_stay
  +3.8 pp on screening (stay pairs are hard, and the accuracy they cost is
  the price of removing deployment bias, which is the fairness argument);
  no_rp (waypoint tokens removed) +0.2 pp yet p = 0.001, discussed
  honestly: the tokens buy almost nothing on average screening accuracy and
  their value is in specific volumes (`shap_waypoint_tokens.csv`, e.g.
  removing EPM shifts the score by −2.4 on average across the 375 rows
  containing it).
- Calibration: isotonic mapping from score gap to acceptance probability;
  add reliability diagrams **[NEW RUN, cheap: predictions are on disk]**.
- SHAP analysis (existing figure) plus `waypoint_preferences.csv` if it
  passes the neutrality review.

### S6. What the model knows and does not know **[NEW SECTION, tables exist]**
The heterogeneity story the conference had one sentence for:
- Heuristic baselines (`heuristic_baselines.csv`): picking the route with
  lower planned fuel scores 44.9 %, lower duration 46.6 %, lower distance
  46.0 %, all below chance; revealed preference actively contradicts the
  cost indicators, which is the single most striking table we own.
  Interestingly, "pick lower ATFM delay" reaches 72.0 % on the 15 % of
  pairs where it decides at all, which previews the regulation stratum.
- Strata (`strata_accuracy.csv`): 63.9 % on unregulated pairs against
  87.7 % on escape pairs; accuracy monotone in the old route's delay
  (63.9 % at 0 min to 84.6 % above 30 min); accuracy falling from 79.9 %
  to 53.8 % as more cost indicators favour the new route (the model earns
  its keep exactly where the cost indicators disagree with the choice).
- Temporal stability (`monthly_accuracy.csv`): 67.7-69.0 % across six
  months spanning two seasons, surprisingly stable.

### S7. Deployment: the MUAC fuel case, in full
- Operating-point table (`muac_operating_points.csv`): precision targets
  0.6/0.7/0.8/0.9 map to thresholds 0.500-0.825, coverage 35.8 % down to
  10.5 %, and confirmed fuel 19.9 down to 11.3 kt per quarter (63.0 down
  to 35.6 kt CO2).
- Annualisation (`muac_annualised.csv`, cut from SID): 64-80 kt fuel and
  236-252 kt CO2 per annum depending on the precision target and the
  extrapolation basis; both bases reported, the difference explained.
- Sensitivity without stay pairs (`muac_sweep_nostay.csv`): the whole case
  recomputed with the bias correction removed, showing what a naive model
  would have promised.
- Concentration (`fuel_concentration.csv`, restored figure): 6 of 815
  operators fly half of the confirmed fuel, 28 fly 80 %; by city pair, 145
  of 10 020 carry half. Monthly breakdown (`muac_breakdown_month.csv`)
  shows the quarter is not carried by one month (4.8-5.9 Mkg each).

### S8. Generalisation **[NEW RUN, the only expensive addition]**
Two experiments, in order of importance:
1. Strict year-forward split. The audit (2026-08-05) established that the
   production SplitConfig separates by month-of-year only; a journal
   referee will find this. Train on the first year, test on the following
   season, report the same strata as S6. This is the experiment that
   converts the audit's criticism into a section.
2. Second-region case study. The pair corpus is Network-Manager-wide; only
   the fuel case is MUAC-specific. Recompute S7 for a second area control
   centre to show the deployment analysis transfers. Region choice is an
   author decision (neutrality constraint applies).
Stretch, only if time allows: a generated-candidate baseline on a common
city-pair subset, making title (3) honest.

### S9. Threats to validity and limitations **[NEW SECTION, material exists]**
Written from the audit findings rather than discovered by referees: what
the ICH label does and does not encode (partial temporal-order encoding);
what "92 % label noise" means definitionally and why it is not noise in
the usual sense; revealed preference reflects the filing system and the
dispatcher, not a pure airline utility; CI-blindness of the archive;
fuel deltas are planned, not burned. Close on the caveat, per his style.

### S10. Conclusions
Prose ordinals; concrete future work (acceptance feedback loop, more
regions, burned-fuel validation); "Last but not least," closes.

---

## 5. Delta over the conference paper (the statement editors ask for)

New relative to SID 2026: the literature review (S2); the leakage section
with its ablation evidence (S4); the ablation and calibration analysis
(S5); the entire skill-heterogeneity section (S6: heuristic baselines,
strata, monthly stability); the annualised and sensitivity variants of the
fuel case plus concentration analysis (S7 beyond its SID half-column); both
generalisation experiments (S8); the threats-to-validity section (S9); the
two case-study maps and the concentration figure, cut from SID for space.
Rough accounting: of the ~22 tables in the study, the conference paper
used 5; the extension uses all of them plus two new runs. Well past the
customary 30-50 % new-material bar [VERIFY the exact TR-C policy].

## 6. Honest risks

1. The screening-accuracy headline (60-69 % depending on stratum) will look
   modest to a referee used to 90 %+ classification papers; the answer is
   S6 (the task is hard exactly where it is valuable) and the
   below-chance heuristics table, and it must be made early, not in
   rebuttal.
2. MUAC-only deployment: answered by S8.2, which is why that run is not
   optional.
3. The month-of-year split: answered by S8.1 before any referee asks.
4. Planned versus burned fuel: scoped, not rebutted; it stays a limitation.

## 7. Work plan

1. Neutrality decisions (city pairs, waypoints, second region) — author.
2. S8.1 year-forward split run — needs GO before launching (long job).
3. S8.2 second-region case — after (2), same pipeline, new region filter.
4. Reliability diagrams — cheap, any time.
5. Draft S2-S4 (pure writing, no computation) while (2)-(3) run.
6. Assemble in the Elsevier template [VERIFY current template/class].
7. Full-draft voice pass, then figure pass at print size (the SID
   `style.py` machinery transfers; TR-C is single-column, so `SIZES`
   changes but the print-at-size rule stands).
