# SESAR Innovation Days 2026 paper

*Which Reroute Will an Airline Accept? Surfacing Fuel Savings from Flight-Plan Revisions*

Dalmau, Perez, Belkoura, Taverniers, Deransy, Cramet, Gustin (EUROCONTROL).

## Status

Draft, 8 of 8 permitted pages. **Not yet submitted.** See `COMPLIANCE.md` for the
venue rules and the two items that must be settled before upload:

1. `sid2026.tex` is a *drafting scaffold*, not the official SID class. The
   submission must be transplanted into the official LaTeX template from
   EasyChair, and the page count re-checked there. The paper currently sits at
   exactly 8 pages, so a denser official template will overflow.
2. The public venue page describes a triple-blind review; the organisers told the
   authors that author details are not withheld for this edition. The paper is
   built with `\blindfalse` (authors visible). Re-confirm before upload.

## Building

```bash
~/.local/bin/tectonic -X compile sid2026.tex --outdir /tmp/sid
```

The committed `figures/*.pdf` are sufficient to build. There is no system
`pdflatex` on the analysis host; use tectonic.

## Regenerating the figures

The figure scripts read the study's output tables and, for the maps, the
prepared parquet datasets. Neither is in this repository:

- tables: `studies/2026-07-fuel-study/tables/*.csv`
- datasets and navigation database: the leak-fixed working tree used for the
  retrain, under `/data/rdcodina/skyrank/_audit/worktree`

With those present:

```bash
python make_data_figures.py    # fig_coverage, fig_tradeoff (fig_concentration
                               # is still produced but no longer used; see below)
python make_shap_figure.py     # fig_shap
python make_maps.py            # map_escape, map_saver
python make_pair_figure.py     # pair_idea
```

`style.py` holds the single palette and type scale. Every figure imports from
it; no script sets its own colour. Figures are drawn at the width they are
printed at, because drawing wider and letting LaTeX scale down halves every
font on the figure.

## The prose voice

The text was passed through the author's measured writing profile
(`~/.claude/skills/my-writing-style`) on 2026-08-20. That pass is why the prose
reads the way it does: discourse markers open roughly one sentence in five,
procedural steps stay in the passive, prior work is cited as "the authors of
[n]" rather than by surname, and the conclusions run First/Secondly/Thirdly and
close on "Last but not least,". Do not "tighten" those back out.

The voice costs length (it cashes out general claims and avoids short punch
sentences), so ~700 words of duplicated material were cut to stay inside the
8-page limit, and `fig_concentration` was dropped: its two numbers are stated
in the Addressable fuel prose, and its curve was interpolated beyond the top 15
operators. `make_data_figures.py` still produces it if it is ever wanted back.

## Conventions that are deliberate

- **Green** is the route the operator chose or kept, **red** the route it
  abandoned, one blue accent for everything else, grey for context.
- No operator, flight, waypoint or airspace volume is identified anywhere in the
  paper. The worked example on a thin sector has unlabelled map endpoints and no
  aircraft type, because route plus type on such a sector identifies a single
  carrier.
- Deployment is written in the conditional throughout, and the paper carries an
  explicit disclaimer that it commits to no operational service. IEEEtran
  conference mode silently drops `\thanks`, so the disclaimer is a
  `\section*{Disclaimer}` rather than a footnote.

## The method figure

`fig_method.png` (Fig. 3) was produced with an image model, driven through the
paperbanana loop: the prompt planned the five stages, the label text and the
palette; the image model rendered it; two critic rounds fixed a duplicated tick
on the stay row, a doubled arrow and the fit/tune/test segment widths.
`fig_method.jpg` is the untouched model output. The `.png` the paper uses is the
same image with its white margins cropped and re-encoded losslessly, because
JPEG fringes around small black-on-white text.

Two things to know before touching it. It is placed at `0.85\textwidth`, which
puts it at 274 dpi; at full width it falls to 233, below the IEEE floor of 300
for raster art, so do not widen it without re-rendering the source at higher
resolution. And the word `calibration` overlaps `Proposal` slightly: the image
model refused that edit twice, and it is the one defect a vector redraw would
fix. A TikZ transcription of this exact layout exists if the raster ever has to
go.

The figure costs about 460 column-points, which was paid for entirely from
prose. Nothing was cut that carried a finding: the argument that generated
negatives are a weaker label than revisions was being made four separate times
(introduction, twice in Related work, and Fig. 2's caption) and now appears
once; the "methodological side" paragraph of Related work cited five works that
are all cited again where they are actually used; the shadow-mode trial was
stated in both Section V-I and the Conclusions. Citation keys and numeric
tokens were diffed before and after: none were lost.

## The figures

`style.py` owns every colour and font size; no figure sets its own. Four
things about the current figures are deliberate and easy to undo by accident.

**Figures are drawn at the size they print.** `style.SIZES` gives each figure
its width and height in points, and `sid2026.tex` includes it at exactly
`style.frac(name)` of `\columnwidth`, so nothing is scaled. This matters: the
figures used to be drawn 3.4 in wide and squeezed to about 2 in by
`\includegraphics`, which silently reduced 7.5 pt labels to roughly 4.5 pt on
the page. If you change a size, change it in `SIZES` and regenerate; do not
change the width in the `.tex`.

**Type is STIXGeneral, not Times New Roman.** Times New Roman is not installed
on this machine, and asking for it fell back to DejaVu Serif, which does not
match the captions. STIXGeneral ships with matplotlib and is Times-metric.
The body text of the paper is NimbusRomNo9L (IEEEtran's Times); no clone of it
is installed, so STIXGeneral is the closest available match.

**Maps are ETRS89-LAEA (EPSG:3035) over Natural Earth 10 m**, from the cartopy
cache. The previous version plotted degrees against degrees with a hand-fitted
aspect correction, over the 110 m fixture bundled in pyogrio's test suite.
`style.basemap` clips the geometry to the window and simplifies it to about
half a printed pixel: without that the 10 m Eurasia polygon made the paper
16 MB.

**Line style, not colour, separates the routes.** The abandoned route is
dashed and the chosen route solid, and two SHAP families carry thin hatching,
because the palette's blue, red and green sit at L\* 45.4, 45.6 and 47.0 —
the same shade of grey. The captions say "dashed red" and "solid green" for
the same reason. Do not "simplify" those back to colour alone.

Neither case map is used any more, and `make_maps.py` still produces both.
`map_saver.pdf` went first: its two routes were nearly coincident at column
width, and the saving in that case came from a different track rather than a
shorter one, which is precisely what the map could not show. `map_escape.pdf`
followed. Both cases are narrated in the prose instead, the first in the
opening paragraph and the second end to end in Section V-G, so the paper now
carries no case-study map at all. That is a deliberate choice, not an
oversight.

What the two of them paid for: three explanations the paper needed more (the
leakage trap in the filing-time feature, why the indicators are carried as
within-pair differences, and what a generated candidate set cannot establish),
and promoting `pair_idea` to a full-width `figure*`. That last one is why the
pair panels are four times the area they were, and it is the figure the whole
labelling argument rests on.
