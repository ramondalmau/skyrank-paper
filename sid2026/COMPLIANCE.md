# SID 2026 submission compliance note

Target: SESAR Innovation Days 2026 (SIDs 2026), full paper
Official source: https://www.sesarju.eu/SIDS2026
Checked: 2026-08-06

VERIFIED FROM THE OFFICIAL PAGE
- Page limit: "up to 8 pages"
- Review: the public page describes a "triple-blind peer review", but the
  organisers confirmed to the authors (2026-08-06) that author details are NOT
  withheld for this edition. The paper is therefore submitted with the author
  block visible (\blindfalse). RESOLVED: this file previously said the paper
  must be anonymised; that instruction was wrong and has been corrected.
  Re-confirm with the organisers before upload.
- Template: "Templates in word and latex format are available for download on the
  submission page and shall be used to create the submission."
- Submission: EasyChair, https://easychair.org/conferences/?conf=sids20260
- Paper deadline: 21 September 2026
- Notification: 12 November 2026
- Proceedings indexed in Scopus

NOT VERIFIED / MUST BE CONFIRMED BEFORE SUBMISSION
- Whether references count toward the 8 pages (not stated on the public page)
- The exact template style (the page says templates exist but does not name the
  style; the official file must be downloaded from the submission page)
- Required sections, if any
- Anonymisation specifics (author block, self-citation phrasing, metadata)

CONSEQUENCE FOR THIS DRAFT
The .tex here is a DRAFTING SCAFFOLD, not the official template. Before
submission the text must be transplanted into the official SID LaTeX template
downloaded from EasyChair, and the page count re-checked in that template.
The author block is VISIBLE (\blindfalse), per the organisers' 2026-08-06
confirmation above. (An earlier version of this line wrongly said the block
was anonymised.)

AUTHOR REVIEW OF 2026-09-07
Fourteen comments from the author, all acted on, plus the findings of an
eight-reader zero-context panel run on the version he read. The full record,
including what had to be cut to hold 8 pages and the one choice left open, is
`../AUTHOR_REVIEW_2026-09-07.md`.

Changed here: the abstract is now an overview of the paper rather than a
summary of its results (224 words, down from 249, and two result figures
instead of eleven); the introduction gives the en-route charge the opening
flight also paid and four reasons a plan gets revised rather than one; the
extra-distance paragraph no longer reads as attributing that distance to
airlines; Section II-A says before the regulation material that most revisions
carry no regulation at all, and leads the label argument with the fact that
nobody knows whether a generated route ever reached the dispatcher; Fig. 1 is
referred to by a sentence rather than a parenthesis; "escapes" is defined where
it is used; the calibration subsection is five paragraphs from one, opening on
a real scored pair; Section V is restructured against the three causes a reader
measured for its density; and the Conclusions state the limits of the
bag-of-words route encoding and the encoder trial that failed to replace it.

The paper is exactly 8 pages. Everything removed to keep it there is in a
`% Cut for space 2026-09-07` comment in the source, verbatim and restorable;
the largest is the worked proposal of Section V-D, which the journal carries
in full.

READER PANELS OF 2026-09-05 AND 2026-09-06
See `../AUTHOR_DECISIONS.md`, which records every item and its disposition.
Repaired in this paper: the reading of the 0-of-3 stratum (item 1), the
"almost always a regulation" explanation (item 2), the 2025 replication
described as "the same recipe" when the model behind those numbers is the
no-stay variant (item 4), a sentence whose subject a `% Cut for space`
comment had swallowed (item 13), and five numbers that disagreed with
themselves or with the journal paper (item 15). Each carries a dated
`% CORRECTED` comment in the source.

FIG. 2 (2026-09-06, unchanged 2026-09-07): regenerated with Gemini over three rounds and accepted
by the author; it is the same raster the journal paper uses. Every defect the
original carried is gone and the caption carries no disclaimer. Two labels the
image model would not correct were repaired by hand in the raster, a
misspelling and a pair of legend labels set against the wrong tracks; the
journal paper's generative-AI declaration records both.

Print quality is the one open point: at this paper's full-width include the
raster is 200 dpi, below IEEE's 300 dpi guidance for raster art and below the
287 the previous one gave. The figure's type is large, and it is legible at
printed size, but a larger render would settle it.

CAMERA-READY STATUS (2026-09-02; supersedes 2026-08-21)
- Build verified: exactly 8 pages, 0 overfull boxes, 0 undefined references,
  figures drawn at print size (see README). Section structure simplified to
  plain IMRAD headings on 2026-09-02.
- Fig. 2 (`fig_pipeline.png`) is an image-model raster at 287 dpi at its
  0.85\textwidth include; IEEE's guidance for raster art is 300 dpi. The
  author chose to keep the raster (no vector fallback is held). Elsevier-
  style restrictions on generative-AI images do not apply to SID, but the
  figure's origin should be disclosed if the venue asks.
- Official page re-checked 2026-08-21: 8-page limit, PDF-only, deadline
  21 September 2026, notification 12 November 2026 — all unchanged.
- The template download requires an EasyChair login, so the transplant is
  the one remaining HUMAN step; historically the SID style is close to the
  IEEEtran conference layout used here, so the transplant is expected to be
  near-mechanical, but the page count must be re-verified in the official
  class before upload.
