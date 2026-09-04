"""Redraw the data figures from their CSVs in the paper's own style.

Green for the route the airline chose and the fuel it saves, red for what that
costs in precision, one cool accent for everything else.

The design rules are the shared ones in style.py: one type family with four
size steps, direct labels instead of legend boxes, no top or right spine, one
light grid direction, and a written reading of the one number that carries
each figure. Nothing here filters, rescales or re-bins: every value is taken
straight from the study tables.
"""
from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import style
from style import ACCENT, GREEN, GREY, INK, LW, MUTED, RED, apply, clean

apply()
T = Path("/home/rdcodina/projects/skyrank/studies/2026-07-fuel-study/tables")
OUT = Path("/data/rdcodina/skyrank/_audit/paper/figures")

# --- 1. accuracy against coverage ----------------------------------------
d = pd.read_csv(T / "coverage_accuracy.csv").sort_values("coverage")
x, y = d.coverage * 100, d.accuracy * 100
fig, ax = plt.subplots(figsize=style.size("fig_coverage"), layout="constrained")
# The band is the only shading left. The earlier version also washed the whole
# area under the curve in accent, which read as a second quantity and made the
# interval hard to see against it.
ax.fill_between(x, d.ci_lo * 100, d.ci_hi * 100, color=ACCENT, alpha=0.20,
                lw=0)
ax.plot(x, y, color=ACCENT, lw=LW, solid_capstyle="round", zorder=4)
ax.axhline(50, color=GREY, ls=(0, (1, 2.6)), lw=1.0, zorder=2)
style.tag(ax, 104, 50.6, "chance", colour=MUTED, ha="right", va="bottom",
          size=style.FS_SMALL)

# the two points the text quotes, and nothing else: the caption explains them
pts = {}
for cov in (20, 100):
    row = d.iloc[(d.coverage * 100 - cov).abs().argmin()]
    pts[cov] = (row.coverage * 100, row.accuracy * 100)
    ax.plot(*pts[cov], "o", ms=5.0, mfc="white", mec=ACCENT, mew=1.6, zorder=6)

# A written reading of each anchor, on a hairline leader, rather than a bare
# percentage the reader has to relate back to the x axis themselves.
style.note(ax, f"{pts[20][1]:.0f}% on the fifth\nit is surest about",
           xy=pts[20], xytext=(46, 98.5), colour=ACCENT, ha="left")
style.note(ax, f"{pts[100][1]:.0f}% if it must\nanswer everything",
           xy=pts[100], xytext=(70, 58.5), colour=ACCENT, ha="center")

# The band needs naming once, but a leader pointing at it would point at
# something the reader cannot find: over most of the range the interval is
# narrower than the line is thick. Say that, and draw no leader.
# low and left, the one quadrant no curve, leader or note occupies
style.tag(ax, 8, 70.0, "95% CI, narrower\nthan the line", colour=ACCENT,
          ha="left", va="top", size=style.FS_SMALL, linespacing=1.3)

ax.set_xlabel("cases answered [%]")
ax.set_ylabel("accuracy [%]")
ax.set_xlim(-2, 106)
ax.set_ylim(46, 103)
ax.set_yticks([50, 60, 70, 80, 90, 100])
ax.set_xticks([0, 20, 40, 60, 80, 100])
clean(ax)
style.save(fig, OUT / "fig_coverage.pdf"); plt.close(fig)

# --- 2. the fuel/precision trade-off --------------------------------------
# The grid sweeps two knobs: the acceptance threshold and a minimum-saving
# filter. Only the unfiltered slice belongs on a curve against tau.
g = pd.read_csv(T / "muac_grid.csv")
g = g[(g.min_saving_kg == 0) & g.tau.between(0.45, 0.90)].sort_values("tau")
op = g.iloc[(g.tau - 0.60).abs().argmin()]

# Two aligned panels on a shared threshold axis, not one panel with two y
# axes. A dual axis lets the crossing point of the two curves be moved by
# choosing the scales, and the crossing means nothing here: the quantities
# are a percentage and a mass. Stacked panels keep both readings honest and
# put the operating point on a single vertical line through the figure.
fig, (axP, axF) = plt.subplots(
    2, 1, sharex=True, figsize=style.size("fig_tradeoff"),
    layout="constrained", gridspec_kw=dict(height_ratios=[1, 1]))
# hspace is squeezed to buy the two panels their height back, but the outer
# pads stay at about a point: at w_pad=0 the constrained solver lets the
# rotated y-label and the descenders of the x-label sit exactly on the page
# boundary, and at the journal size they were being shaved off.
fig.get_layout_engine().set(h_pad=0.018, hspace=0.05, w_pad=0.018,
                            wspace=0.0)

axP.plot(g.tau, g.precision * 100, color=RED, lw=LW, ls=(0, (4, 2)),
         dash_capstyle="round", zorder=4)
axP.set_ylabel("precision [%]")
style.panel(axP, "a")

axF.plot(g.tau, g.realized_kg / 1e6, color=GREEN, lw=LW,
         solid_capstyle="round", zorder=4)
axF.set_ylabel("fuel confirmed\n[kt / quarter]")
axF.set_xlabel("acceptance threshold")
style.panel(axF, "b")

for ax, val, colour in ((axP, op.precision * 100, RED),
                        (axF, op.realized_kg / 1e6, GREEN)):
    # GREY, not FAINT: at print size the faint rule vanished and the two
    # panels lost the vertical line that ties their operating points together
    ax.axvline(0.60, color=GREY, lw=0.9, zorder=1)
    ax.plot(0.60, val, "o", ms=5.0, mfc="white", mec=colour, mew=1.6, zorder=6)
    clean(ax)
    ax.set_xlim(0.44, 0.91)

axP.set_xticks([0.5, 0.6, 0.7, 0.8, 0.9])
# One written reading, in the panel where the threshold is chosen; the
# vertical rule carries it down into the fuel panel.
style.note(axP, f"operating point\n$\\tau$ = {op.tau:.3f}, {op.precision * 100:.0f}%",
           xy=(0.60, op.precision * 100), xytext=(0.735, 71.0), colour=INK,
           ha="center")
style.tag(axF, 0.615, op.realized_kg / 1e6,
          f"{op.realized_kg / 1e6:.1f} kt", colour=GREEN, ha="left",
          va="bottom", size=style.FS_SMALL)
# the two y labels are different lengths, so without this they start at
# different x and the panels look mis-stacked
fig.align_ylabels([axP, axF])
style.save(fig, OUT / "fig_tradeoff.pdf"); plt.close(fig)

# --- 3. where the value sits ----------------------------------------------
# A stacked bar hid the point: the head of the distribution was a sliver next
# to 787 operators. The cumulative curve shows the concentration directly.
# The per-operator table covers the top 15, which is 71% of the fuel; beyond
# that the curve is drawn through the two published anchors and marked.
c = pd.read_csv(T / "fuel_concentration.csv")
r = c[c.dimension == "operator"].iloc[0]
n50, n80, tot = int(r.n_for_50pct), int(r.n_for_80pct), int(r.entities_total)

op_t = pd.read_csv(T / "muac_breakdown_operator.csv").sort_values(
    "realized_kg", ascending=False)
TOTAL_KG = pd.read_csv(T / "muac_grid.csv").query(
    "min_saving_kg == 0 and tau == 0.60").realized_kg.iloc[0]
cum = (op_t.realized_kg.cumsum() / TOTAL_KG * 100).tolist()
xs_m, ys_m = list(range(1, len(cum) + 1)), cum

# Six operators out of 815 is invisible on a linear axis: the curve becomes a
# vertical spike against the y-axis. A log rank axis puts the head where the
# reader can see it and still shows the whole fleet.
fig, ax = plt.subplots(figsize=style.size("fig_concentration"),
                       layout="constrained")
eq_x = [1, 3, 10, 30, 100, 300, tot]
ax.plot(eq_x, [x / tot * 100 for x in eq_x], color=MUTED, ls=(0, (3, 3)),
        lw=1.0, zorder=2)
# left of the knee, where both curves are flat and the corner is empty;
# at the right-hand end this label ran into the frame edge
style.tag(ax, 1.6, 14.0, "if every operator\ncontributed equally",
          colour=MUTED, ha="left", va="top", size=style.FS_SMALL,
          linespacing=1.3)
# solid = measured from the per-operator table, dashed = the same curve
# continued through the two published anchors. The change of dash is the
# cue; colour alone would not say which part is tabulated.
ax.plot(xs_m, ys_m, color=ACCENT, lw=LW, solid_capstyle="round", zorder=4)
ax.plot([xs_m[-1], n80, tot], [ys_m[-1], 80, 100], color=ACCENT, lw=1.3,
        ls=(0, (2, 2)), zorder=3)
style.note(ax, f"{n50} operators\nfly half of it", xy=(n50, ys_m[n50 - 1]),
           xytext=(15, 33), colour=ACCENT)
style.note(ax, f"{n80} operators\nfly 80%", xy=(n80, 80), xytext=(115, 60),
           colour=ACCENT)
for n, yv in ((n50, ys_m[n50 - 1]), (n80, 80)):
    ax.plot(n, yv, "o", ms=4.8, mfc="white", mec=ACCENT, mew=1.5, zorder=6)
ax.set_xscale("log")
ax.set_xlabel(f"operators, ranked by fuel confirmed (of {tot})")
ax.set_ylabel("cumulative fuel [%]")
ax.set_xlim(1, tot); ax.set_ylim(0, 104)
ax.set_xticks([1, 3, 10, 30, 100, 300, 800])
ax.set_xticklabels(["1", "3", "10", "30", "100", "300", "800"])
ax.minorticks_off()
clean(ax)
style.save(fig, OUT / "fig_concentration.pdf"); plt.close(fig)

for f in ("fig_coverage", "fig_tradeoff", "fig_concentration"):
    print("wrote", f)
