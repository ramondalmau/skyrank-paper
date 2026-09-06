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

READER PANELS OF 2026-09-05 AND 2026-09-06
See `../AUTHOR_DECISIONS.md`, which records every item and its disposition.
Repaired in this paper: the reading of the 0-of-3 stratum (item 1), the
"almost always a regulation" explanation (item 2), the 2025 replication
described as "the same recipe" when the model behind those numbers is the
no-stay variant (item 4), a sentence whose subject a `% Cut for space`
comment had swallowed (item 13), and five numbers that disagreed with
themselves or with the journal paper (item 15). Each carries a dated
`% CORRECTED` comment in the source.

FIG. 2 (2026-09-06): regenerated with Gemini and accepted by the author; it
is the same raster the journal paper uses. Five of the six defects that made
it disagree with the text are gone and the caption's disclaimer with them.
Three label errors remain, listed in
`../trc-extension/SUBMISSION_NOTES.md`; none contradicts a claim in the text,
the wrong test-set count having been corrected in a second round. At this paper's
full-column-span include width the raster is 199 dpi, below IEEE's 300 dpi
guidance for raster art and below the 287 the previous one gave, so the
re-render that fixes the labels should also come back at roughly twice the
linear size.

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
