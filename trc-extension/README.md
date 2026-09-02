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

Currently 36 pages, zero overfull boxes, zero undefined references. The
`latex_sanity.py` brace-delta warning on this file is a known false positive
of that naive counter; do not chase it.

## Structure (settled, do not re-churn)

- **Class**: `elsarticle` preprint, 12pt, author-year (`elsarticle-harv`),
  single column.
- **Sections**: 1 Introduction · 2 Background (revisions as preference data;
  two operational use cases; discrete choice and the construction of pairs)
  · 3 Related work · 4 Data and pair construction (the archive, including its
  composition; stay pairs; encoding and leakage control; splits) · 5 Model,
  training and calibration · 6 Predictive performance (accuracy, coverage and
  baselines; accuracy by stratum; ablation and change bias; error analysis;
  feature attribution) · 7 Proposal channel (policy and operating points;
  concentration of the value; sensitivity to the bias correction; a worked
  example) · 8 Model ageing · 9 Threats to validity · 10 Conclusions, then
  the Disclaimer and the elsarticle declarations. Headings are plain noun
  phrases; every section opens with a lead-in paragraph.
- **The SID prose is the core.** Sections shared with the conference paper
  were carried over nearly verbatim and the journal material written around
  them. The abstract is held at 250 words (count with LaTeX markup stripped;
  agents counting braces report ~10 too many).
- **Neutrality**: no operator, waypoint, volume or city pair is named in any
  table; the per-city-pair and per-waypoint tables of the study were
  deliberately left out. The introduction keeps the Amsterdam–Barcelona
  anecdote already published at SID.
- **Figures** are re-rendered at the elsarticle text width (390 pt) by
  `make_trc_figures.py`, which overrides `style.SIZES` from the SID drivers
  and copies the results into `figures/`; `fig_horizon.pdf` comes from
  `make_horizon_figure.py`. Nothing is scaled at include time. See
  `../REPRODUCING.md` for the order of operations, because this driver
  overwrites the shared staging directory used by the SID.

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
