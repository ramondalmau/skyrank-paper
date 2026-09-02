# SESAR Innovation Days 2026 paper

*Which Reroute Will an Airline Accept? Learning Route Preferences from
Flight-Plan Revisions*

Dalmau, Perez, Ballerini, Belkoura, Taverniers, Deransy, Cramet, Gustin
(EUROCONTROL).

## Status

Exactly 8 of 8 permitted pages. **Not yet submitted.** See `COMPLIANCE.md` for
the venue rules and the two items to settle before upload:

1. `sid2026.tex` is a *drafting scaffold* on IEEEtran, not the official SID
   class. The submission must be transplanted into the official template from
   EasyChair and the page count re-checked there; a denser template will
   overflow.
2. The public venue page describes a triple-blind review; the organisers told
   the authors that author details are not withheld for this edition. The
   paper is built with `\blindfalse`. Re-confirm before upload.

The journal extension of this paper lives in `../trc-extension/`. Anything
the conference paper only sketches (the fuel channel, heuristic baselines,
strata, model ageing, threats to validity) is there.

## Building

```bash
mkdir -p "$TMPDIR/sid"
~/.local/bin/tectonic -X compile sid2026.tex --outdir "$TMPDIR/sid"
```

The committed `figures/*.pdf` and `figures/fig_pipeline.png` are sufficient to build. There is no `pdflatex`
on the analysis host; use tectonic. Check after every build: page count 8, no
`Overfull` lines, no `??` in the PDF.

## Structure

Introduction; Background (revisions as preference data, including the
pairs-versus-generated-candidates argument; two operational use cases);
Related work; Methodology (data and pair construction; model, training and
calibration); Results (predictive performance; ablation and change bias;
error analysis and feature attribution; a worked proposal and the conditions
for deployment); Conclusions; Disclaimer. Headings are plain noun phrases and
every section opens with a lead-in paragraph before its first subsection.
Text cut for the page limit is kept in `% Cut for space:` comments in the
source, never deleted.

## Regenerating the figures

`../REPRODUCING.md` is the authoritative runbook (environment, inputs that
live outside the repository, regeneration order, the shared output directory
trap). In short: the drivers in this directory write to
`/data/rdcodina/skyrank/_audit/paper/figures/`, from which the PDFs are copied
into `figures/`. Run the SID drivers, copy, and only then run the journal
driver, because the latter overwrites the staging directory with
journal-sized renders.

```bash
python make_data_figures.py    # fig_coverage, fig_tradeoff, fig_concentration
python make_shap_figure.py     # fig_shap
python make_maps.py            # map_escape, map_saver
python make_pair_figure.py     # pair_idea
```

`fig_pipeline.png` (Fig. 2) is a raster made with an image model, shared by
both papers: the author ran PaperBanana's own Planner, Stylist, Visualizer
and Critic prompts by hand in ChatGPT
(`../trc-extension/figures-src/fig_pipeline_paperbanana_chatgpt.md` is the
exact prompt bundle; `fig_pipeline_chatgpt_original.png` next to it is the
untouched model output). The installed PNG is that output with its white
margin trimmed, re-encoded losslessly. At `0.85\textwidth` it sits at
287 dpi (IEEE asks for 300 for raster art; the earlier raster went in at
274); its smallest labels are about 4.5 pt on the page. Every label was
checked against the method text before installation.
The SID uses `fig_coverage`, `fig_shap`, `pair_idea` and `fig_pipeline`;
`fig_tradeoff`, `fig_concentration` and the two maps are produced by the same
drivers but appear only in the journal paper.

## Conventions that are deliberate

- **Green** is the route the airline chose or kept, **red** the route it
  abandoned, one blue accent for everything else, grey for context.
- **Line style, not colour, separates the routes** (abandoned dashed, chosen
  solid), and two SHAP groups carry thin hatching, because the palette's blue,
  red and green sit at L\* 45.4, 45.6 and 47.0 — the same shade of grey. The
  captions say "dashed red" and "solid green" for the same reason. Do not
  simplify those back to colour alone.
- **Figures are drawn at the size they print.** `style.SIZES` gives each
  figure its width and height in points and the `.tex` includes it at exactly
  `style.frac(name)` of `\columnwidth`. Change sizes in `SIZES` and
  regenerate; never in the `.tex`. Verify the MediaBox after every copy.
- **Type is STIXGeneral** (Times-metric, ships with matplotlib); Times New
  Roman is not installed and falls back to DejaVu.
- **Maps are ETRS89-LAEA (EPSG:3035) over Natural Earth 10 m** from the
  cartopy cache, clipped and simplified by `style.basemap` to about half a
  printed pixel (without it the Eurasia polygon made the paper 16 MB).
- **Neutrality.** No operator, flight, waypoint or airspace volume is
  identified anywhere; map endpoints are unlabelled; the worked example names
  no aircraft type. The Amsterdam–Barcelona introduction anecdote is the sole
  authorised exception. Deployment is written in the conditional, and the
  `\section*{Disclaimer}` stays verbatim (IEEEtran conference mode silently
  drops `\thanks`, hence a section rather than a footnote).
- **No number is typed by hand.** Every figure in the prose traces to
  `studies/2026-07-fuel-study/report/macros.tex` or the results JSONs. Never
  re-derive a metric; call the study's own code.

## The prose voice

The text follows the author's measured writing profile
(`~/.claude/skills/my-writing-style`): discourse markers open roughly one
sentence in five, procedural steps stay in the passive, prior work is cited
as "the authors of [n]", conclusions run First/Secondly/Thirdly and close on
"Last but not least,". Do not "tighten" those back out. Clarity is judged
only by zero-context readers (`/coldread`), never by the writer.
