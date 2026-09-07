# TR-C submission notes — what is verified and what is not

## Journal requirements: provenance

ScienceDirect returns HTTP 403 to automated access, so the current Guide
for Authors could NOT be read directly on 2026-08-21. The requirements
below come from two secondary sources (a search summary of the official
page, and manusights.com's August 2026 submission guide) and MUST be
verified against the live page by a human before submission:

- elsarticle class, editable source (.tex), single-column layout
- abstract at most 250 words (**249 on 2026-09-06**, strict count; see README.
  The 231 recorded here on 2026-09-04 went stale: the abstract stood at 311
  words when it was recounted on 2026-09-06, and four passages were cut back
  out of it, each kept verbatim in a `% Cut for space` comment above
  `\begin{abstract}`. Recount after any edit; do not trust this line alone.)
- highlights file: 3-5 bullets, <=85 characters each (`highlights.tex`)
- graphical abstract required (candidate: `figures/fig_pipeline.png` —
  **but see the blocker below: that raster carries nine known defects**)
- CRediT authorship statement (stub in the manuscript, to be completed)
- data availability statement (drafted)
- declaration of competing interests (drafted)
- generative-AI use declaration per Elsevier policy (DRAFTED in the
  manuscript, covering both the text and the image-model schematic; the
  wording still needs the authors' sign-off)
- ORCID iDs at submission; suggested reviewers with affiliations
- review model and any page limit: NOT verified

## Fig. 2: regenerated 2026-09-06, no label errors left

The methodology schematic was regenerated with Google's Gemini image model
over three editing rounds, each prompt built out of the defects the previous
raster carried and each result checked panel by panel against the text. Every
defect the original carried is gone: the hinge-condition box (now an inset of
penalty against gap, falling smoothly), the impossible fuel precondition and
its AND gate, the missing fourth cost indicator, the grey routes in the
proposal box, the training labels on the model's own outputs, the test-set
size (281 720), the repeated waypoint token, "Balanced weights" (now "group
weight w (10 here)"), the incomplete gap equation (now $\Delta S = S^+ - S^-$)
and a stray fragment in the stay-pair panel.

Two labels the image model would not correct after two attempts were repaired
by hand in the raster itself, both on flat backgrounds and neither involving
new type: the penalty inset's vertical axis, which read "Penslty", was
replaced with the word "Penalty" lifted from the inset's own caption, scaled
and rotated; and the two route labels in stage 5, which sat level with the
wrong tracks, were exchanged by moving the rendered text blocks. The
generative-AI declaration records both. The patched raster is kept as
`figures-src/fig_pipeline_gemini_2026-09-06c_patched.png` beside the three
Gemini originals.

One thing is left, and it is a print-quality question rather than a defect:
the raster is 1425 x 724, which is 278 dpi at the TR-C include width but
**200 dpi at the SID one**, against IEEE's 300 dpi guidance for raster art
(the pre-regeneration raster gave 287). All three rounds came back at
1440 x 736 whatever size was asked for. Either ask for the size on its own,
without other edits, or accept 200 dpi for the conference paper, where the
figure's type is large and legible at printed size.

## The author review of 2026-09-07

Fourteen comments on the conference paper, with the instruction to mirror
whatever applied here. Full record in `../AUTHOR_REVIEW_2026-09-07.md`.

Changed in this manuscript: the opening flight's en-route charge (466 EUR,
verified in the archive); four reasons a plan gets revised in place of one,
including a route that ceased to be filable and is therefore not a choice;
the extra-distance paragraph reframed so it does not attribute that distance
to airlines; the filing-message explanation simplified; a statement in the
Background that most revisions carry no regulation at all; the label argument
led by the fact that nobody knows whether a generated route ever reached the
dispatcher; and a new limitation in Section 10 on the route being carried as
a vocabulary rather than a geometry.

Three corrections against the record, each with a dated `% CORRECTED` comment:
the feature table's claim that every rotation and context feature is identical
within a pair (the outbound connection time is not, by design); the
description of the encoder probe as recovering waypoint identities (it
separated preferred from abandoned routes, near chance); and an example that
refuted the claim it illustrated. The manuscript is now 50 pages, up from 49.

Open, and the authors': whether the worked example of Section 7.4 needs its
vertical caveat. Its chosen route burns 2 016 kg less planned fuel, a quarter
of the trip fuel, at essentially the same distance and flight time, which a
domain reader called physically incoherent at a fixed cruise level; the
archive holds no vertical profile, so the paper cannot attribute it.

## Author decisions

Everything the 2026-09-05 and 2026-09-06 reader panels raised is settled in
`../AUTHOR_DECISIONS.md`, which covers both manuscripts: what was repaired
and against which artefact, what was checked and found sound, and what is
left to the authors' judgement rather than to the record.

1. **Neutrality**: the manuscript names no operator, waypoint, volume or
   city pair (the per-city-pair and per-waypoint tables were deliberately
   kept out of the paper). The intro anecdote names Amsterdam–Barcelona,
   as in the SID paper.
2. CRediT roles and author order.
3. Generative-AI disclosure wording (drafted in the manuscript; confirm).
4. Whether TR-C requires a statement that the paper extends SID 2026,
   and the overlap declaration format.

## Evidence map (every number -> source)

RE-BASELINED 2026-09-01 on the corrected archive (the pre-7075cd3
completeness key had silently dropped ~25% of valid pairs — recycled
pair_ids; test pairs 225,181 -> 281,720). Every number below re-verified
against the tables regenerated by the full study + horizon re-run of
2026-09-01.

- 68.1%, 281,720 pairs, CIs, 94.9% top fifth, 53.2% delay rule, tau=0.600,
  79.2%, 56,162, 20.1 kt, 63.5 kt CO2, 130 kg median, 64% top decile,
  change-bias figures (65.2/47.8/58.1), sweep (90.3->97.6, 58.5->59.7,
  68.2->66.7), ECE 0.9/1.8, screening ablations, error anatomy
  (27.7/5.6%), worked examples: `report/macros.tex` + `results/examples.json`
  (same study lineage as the SID paper).
- Baseline table (coin toss, five single-feature rules, the inverted fuel
  rule at 55.0%, four logistic models, the model): rules from
  `tables/heuristic_baselines.csv`; the inverted figure is
  `decided_share*(1-accuracy_on_decided) + (1-decided_share)*0.5` on the same
  row; learned models from `tables/logistic_baselines.csv`, regenerated
  2026-09-04 after `run_18` was changed to read its two comparator rows from
  the artefacts instead of hand-copied literals (the literals said 0.6830 and
  0.4486, both void since the 2026-09-01 re-baseline).
- Decision-context table (what the revision did to the delay, with accuracy):
  `tables/context_accuracy_test.csv`, produced by
  `run_20_decision_context_accuracy.py`. Keys on the DELAY, not on regulation
  membership; the caption says so, because the composition table keys the
  other way and the counts differ.
- Score-gap to probability table: `tables/calibration_bands.csv`, produced by
  `run_22_calibration_bands.py`. The manuscript's column is that file's
  `stated_probability` (0.55/0.72/0.88/0.96/0.99/1.00) and its caption's
  "4.4 points in the worst band, 1.7 on average" is that file's `gap_pp`. The stated-probability column is the
  calibrated probability for the TOP-RANKED route, not for the chosen one; a
  draft of this table used `p_pref` directly and was wrong in its two lowest
  bands by three to four points. The caption's "4.4 points in the worst band,
  1.7 on average" comes from the same stage's JSON, and the 1.7 agrees with
  the isotonic ECE of 1.8 as it should. The worked example's -2.82 / +0.90 and
  its 0.99 probability are pair `827759_AA82551344` in
  `data/cache/study2026/calibrated_test.parquet`.
- Stay-weight sweep table: `results/weight_decision.json` plus the no-stay row
  from `results/analysis.json` (`stay_bias`, `headline.nostay_test_accuracy`).
- Eligibility figures (275,907 eligible, 97.9%, 55.1% old route cheaper,
  44.9% base rate): `results/muac_summary.json` (`test_eligible_pairs`,
  `test_base_rate_fs_accepted`) and `run_09_muac_policy.py` line 59.
- Sensitivity at tau=0.600: `tables/muac_sweep.csv` and
  `tables/muac_sweep_nostay.csv` (the manuscript previously quoted only
  tau=0.500, which is the 60% operating point and not the one used elsewhere).
- Which way each feature pushes (Fig. 6): `tables/shap_dependence.csv` from
  `run_21_shap_direction.py`. Delay: Spearman rho -0.645, median SHAP
  difference +2.32 at -109 min. Fuel: rho +0.785, monotone from -0.21 at
  -1155 kg to +0.37 at +1122 kg.
- The worked example is atypical, and now says so: 2016 kg on 8469 kg is a
  23.8% fuel difference at 17 km and 1.3 min apart. Among held-out pairs whose
  routes lie within 50 km and 5 min, 4.26% differ by more than 10% on fuel and
  1.07% by more than 20%. OPEN FOR THE AUTHORS: planned fuel is evidently not
  determined by horizontal geometry alone, and what else enters it (cruise
  level, assumed weight, wind pack) is not stated in the paper. An ATM
  reviewer flagged the example as physically implausible from routing alone.
- Mean confirmed saving 452 kg: `realized_kg` at tau=0.600 in
  `tables/muac_sweep.csv` divided by proposals times precision from the same
  row. Arithmetic on two published values; the median 88 kg over all eligible
  pairs and 130 kg over accepted ones are in `results/muac_summary.json` and
  `report/macros.tex`.
- ECE 0.9 / 1.8 pp: `results/calibration.json` (`raw.test_ece` 0.008990,
  `isotonic.test_ece` 0.017830). Both manuscripts previously said 0.8 / 1.7.
- Composition table: `studies/2026-07-fuel-study/tables/composition_ich.csv`
  (all five contexts of the CSV are in the paper; an earlier draft
  dropped the "took on delay" row, whose 51.8% fuel-saving share also
  falsified the then-claim that no context reaches one half — the
  observation now reads "only the smallest context exceeds one half")
- Change-bias figures, 2026-09-04 framing: direct stay accuracy 34.8% ->
  90.0% (`analysis.json:stay_bias`, Wilson [88.1, 91.7] on 1,093 pairs); the
  escape control 88.0% on 30,953 pairs is `strata_accuracy.csv`
  (table=regulation, stratum="escaped (old only)"); the 0.8-point revision
  cost is 68.1 vs 68.9 (`analysis.json:headline`). The withheld-feature
  figures (`analysis.json:regulation_blind_accuracy`, 47.8% -> 58.1%) are
  deliberately NOT reported: the author ruled that hiding the regulation
  features is the same masking experiment under another name.
- Stay-pair facts (6,672; 31 min; 47.5%; -3 kg): `composition_stay.csv`
  (unchanged by the re-baseline; the stay archive was never affected)
- Heuristics table: `heuristic_baselines.csv`
- Strata table: `strata_accuracy.csv` (note: accuracy no longer rises
  monotonically into the >60 min delay band — 84.5 then 83.5 — and the
  prose now says the climb levels off)
- Operating points table: `muac_operating_points.csv`
- Annualisation (70-80 kt at 0.8; 85-97 kt at 0.6): `muac_annualised.csv`
- Concentration (882/6/28; 10,939/153): `fuel_concentration.csv`
- Monthly fuel (5.9-7.5 kt): `muac_breakdown_month.csv`
- No-stay sensitivity (64.4% vs 65.8%; 24.4 vs 24.3 kt at tau 0.500 —
  the precision direction flipped vs the old archive, now slightly in
  the corrected model's favour): `muac_sweep_nostay.csv` and
  `muac_operating_points.csv`
- SHAP: `shap_importance.csv` (the old "waypoint text outweighs the four
  cost indicators combined" claim is FALSE on the corrected archive —
  fuel importance grew; caption weakened to "largest single term"),
  `shap_waypoint_tokens.csv` (max token shift 2.5)
- Confident-error worked example: `results/examples.json` archetype
  `confident_error` (a NEW case on the corrected archive — business jet,
  152 kg, 124 min; the old 44 kg / 74 min narrative no longer exists in
  the selection and was rewritten in both papers)
- Horizon section: `studies/2026-08-trc-horizon/tables/` (re-run of
  2026-09-01; splits 880,139 / 128,113 / 474,865 pairs; precision band
  77.2-78.9 unchanged, tau*=0.600 again, early stop 9,386)
- New bib entries (mcfadden1974, benakiva1985, joachims2002, train2009):
  canonical works added from author knowledge — verify bibliographic
  metadata against the sources before submission, per the evidence
  workflow. All other entries carried over from the SID paper.

## Camera-ready pass (2026-08-21, second commit)

- CRediT statement: INFERRED from author order/affiliations; marked in
  the .tex with a comment. Every author must confirm. Franck Ballerini
  (Innovation Hub) added 2026-09-02 as third author, after David Perez, with roles Validation
  and Writing -- review & editing, INFERRED: to be confirmed by him.
- Generative-AI declaration added per the Elsevier template wording.
- **Policy risk — Fig. 2 (fig_pipeline.png)**: the methodology schematic
  is an image-model raster (OpenAI, via ChatGPT, driven by PaperBanana's
  agent prompts; bundle and untouched output in `figures-src/`). Elsevier
  policy generally does not permit generative-AI-created images in
  manuscripts (illustrations may be treated differently from photographic
  data, but this is an editor's call). The author decided on 2026-09-02
  to keep the raster and to hold NO vector fallback (the earlier TikZ
  redraw was deleted; git 376c929 has it). The generative-AI declaration
  in the manuscript carries an explicit clause on this figure (schematic,
  no data, author-directed, label-checked, editor decides whether a
  manual redraw is required), added 2026-09-02 at the author's request.
  If TR-C objects, the options are to redraw by hand or to drop the
  figure. Same consideration
  applies to using it as the graphical abstract.
- Highlights bullet 1 reworded (was a tailing fragment).
