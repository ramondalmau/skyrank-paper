# TR-C submission notes — what is verified and what is not

## Journal requirements: provenance

ScienceDirect returns HTTP 403 to automated access, so the current Guide
for Authors could NOT be read directly on 2026-08-21. The requirements
below come from two secondary sources (a search summary of the official
page, and manusights.com's August 2026 submission guide) and MUST be
verified against the live page by a human before submission:

- elsarticle class, editable source (.tex), single-column layout
- abstract ~250 words (current draft: check with `texcount`)
- highlights file: 3-5 bullets, <=85 characters each (`highlights.tex`)
- graphical abstract required (candidate: `figures/fig_method.png`)
- CRediT authorship statement (stub in the manuscript, to be completed)
- data availability statement (drafted)
- declaration of competing interests (drafted)
- generative-AI use declaration per Elsevier policy (NOT yet drafted —
  author decision on wording)
- ORCID iDs at submission; suggested reviewers with affiliations
- review model and any page limit: NOT verified

## Author decisions still open

1. **Neutrality**: the manuscript names no operator, waypoint, volume or
   city pair (the per-city-pair and per-waypoint tables were deliberately
   kept out of the paper). The intro anecdote names Amsterdam–Barcelona,
   as in the SID paper.
2. CRediT roles and author order.
3. Generative-AI disclosure wording.
4. Whether TR-C requires a statement that the paper extends SID 2026,
   and the overlap declaration format.

## Evidence map (every number -> source)

- 68.3%, 225,181 pairs, CIs, 95.2% top fifth, 53.3% delay rule, tau=0.600,
  78.4%, 45,912, 16.4 kt, 51.9 kt CO2, 130 kg median, 65% top decile,
  change-bias figures (66.2/45.7/57.3), sweep (91.6->98.0, 58.6->60.0,
  68.2->66.7), ECE 0.8/1.7, screening ablations, error anatomy
  (27.4/5.4%), worked examples: SID 2026 paper (same study lineage).
- Composition table: `studies/2026-07-fuel-study/tables/composition_ich.csv`
  (all five contexts of the CSV are in the paper as of 2026-08-22; an
  earlier draft dropped the "took on delay" row, whose 51.9% fuel-saving
  share also falsified the then-claim that no context reaches one half —
  the observation now reads "only the smallest context exceeds one half")
- Stay-pair facts (6,672; 31 min; 47.5%; -3 kg): `composition_stay.csv`
- Heuristics table: `heuristic_baselines.csv`
- Strata table: `strata_accuracy.csv`
- Operating points table: `muac_operating_points.csv`
- Annualisation (56-66 kt at 0.8; 68-80 kt at 0.6): `muac_annualised.csv`
- Concentration (815/6/28; 10,020/145): `fuel_concentration.csv`
- Monthly fuel (4.8-5.9 kt): `muac_breakdown_month.csv`
- No-stay sensitivity (69.9% vs 68.7%; 20.4 vs 19.9 kt at tau 0.500):
  `muac_sweep_nostay.csv` and `muac_operating_points.csv`
- Horizon section: `studies/2026-08-trc-horizon/tables/` (run of
  2026-08-21; splits 692,754 / 96,325 / 370,496 pairs)
- New bib entries (mcfadden1974, benakiva1985, joachims2002, train2009):
  canonical works added from author knowledge — verify bibliographic
  metadata against the sources before submission, per the evidence
  workflow. All other entries carried over from the SID paper.

## Camera-ready pass (2026-08-21, second commit)

- CRediT statement: INFERRED from author order/affiliations; marked in
  the .tex with a comment. Every author must confirm.
- Generative-AI declaration added per the Elsevier template wording.
- **Policy risk — Fig. 2 (fig_method.png)**: the methodology schematic
  is a Gemini-generated raster. Elsevier policy generally does not
  permit generative-AI-created images in manuscripts (illustrations
  may be treated differently from photographic data, but this is an
  editor's call). A human-authored-code TikZ redraw of the same layout
  is preserved at `figures-src/fig_pipeline.tex` as the fallback; the
  swap is one figure include if TR-C objects. Same consideration
  applies to using fig_method as the graphical abstract.
- Highlights bullet 1 reworded (was a tailing fragment).
