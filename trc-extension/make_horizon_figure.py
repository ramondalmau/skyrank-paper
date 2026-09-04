"""Fig: what a fixed model loses as the months since training pile up.

Two stacked panels on one month axis, the same construction as
fig_tradeoff: (a) pairwise accuracy, (b) proposal precision and the
coverage that produced it.

The single-panel version drew accuracy and precision only. Both are flat,
so the figure said "nothing happens" while the text beside it said that
the cost of ageing is paid in coverage rather than in precision -- the one
series that was not drawn. Coverage is now on the same axis as the
precision it belongs to, which is the only honest place for it: a
precision quoted at a fixed threshold means nothing without the share of
cases the threshold still admits.

Drawn at print size for the elsarticle preprint layout, same conventions as
the SID figures: STIX text, no scaling at include time, colour never the
only cue.
"""
from __future__ import annotations

from pathlib import Path

import sys

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.ticker import MaxNLocator

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "sid2026"))
import style  # noqa: E402  (the shared style module)

T = Path(__file__).resolve().parents[2] / "studies/2026-08-trc-horizon/tables"
OUT = Path(__file__).resolve().parent / "figures"

# The journal body is 12 pt; the SID scale was calibrated against 10 pt.
# make_trc_figures.py sets the same five sizes before it re-runs the SID
# generators, and this figure is drawn by its own driver, so it has to make
# the same statement itself.
style.FS_PANEL, style.FS_TICK, style.FS_LABEL, style.FS_ANNOT, \
    style.FS_SMALL = 9.5, 9.0, 10.0, 9.5, 8.5

# This figure used to carry its own near-copies of the palette and the rc
# block, so it drifted a shade away from every other figure in the paper.
# It now takes both from the shared module, like the rest of the set.
style.apply()
ACCENT, RED, GREEN, INK = style.ACCENT, style.RED, style.GREEN, style.INK

acc = pd.read_csv(T / "horizon_accuracy.csv")
pol = pd.read_csv(T / "horizon_policy.csv")
a = acc[acc.stratum == "all"].sort_values("horizon_months")
p = pol.sort_values("horizon_months")
# every number in the figure comes from these two tables and nothing here
# re-derives one; the threshold is a single fixed value by design
assert p.tau.nunique() == 1, "the policy panel assumes one fixed threshold"
assert (a.horizon_months.to_numpy() == p.horizon_months.to_numpy()).all()

# 270 x 215 TeX pt (1 pt = 1/72.27 in); matplotlib inches are 1/72 in
W, H = 270 / 72.27, 215 / 72.27
fig, (axA, axB) = plt.subplots(2, 1, sharex=True, figsize=(W, H),
                               layout="constrained",
                               gridspec_kw=dict(height_ratios=[1, 1.15]))
# as in fig_tradeoff: squeeze the gap between the panels, keep about a point
# of outer pad so the rotated y label is not shaved off at the page edge
fig.get_layout_engine().set(h_pad=0.018, hspace=0.05, w_pad=0.018, wspace=0.0)

# --- (a) pairwise accuracy -------------------------------------------------
axA.fill_between(a.horizon_months, a.ci_lo * 100, a.ci_hi * 100,
                 color=ACCENT, alpha=0.20, lw=0)
axA.plot(a.horizon_months, a.accuracy * 100, color=ACCENT, lw=style.LW,
         marker="o", ms=4, mfc="white", mew=1.3, solid_capstyle="round",
         zorder=4)
axA.set_ylabel("[%]")
style.panel(axA, "a", "pairwise accuracy")

# --- (b) proposal precision and the coverage behind it ---------------------
axB.fill_between(p.horizon_months, p.ci_lo * 100, p.ci_hi * 100,
                 color=RED, alpha=0.15, lw=0)
axB.plot(p.horizon_months, p.precision * 100, color=RED, lw=style.LW,
         ls=(0, (4, 2)), marker="s", ms=3.6, mfc="white", mew=1.3,
         dash_capstyle="round", zorder=4)
# Coverage carries no interval in the policy table: it is a count over the
# eligible cases, not an estimate, so it is drawn as a bare line. Dash-dot
# with triangles keeps it apart from the dashed precision series without
# relying on colour.
axB.plot(p.horizon_months, p.coverage * 100, color=GREEN, lw=style.LW,
         ls=(0, (5, 1.6, 1, 1.6)), marker="^", ms=3.8, mfc="white", mew=1.2,
         dash_capstyle="round", zorder=4)
axB.set_ylabel("[%]")
axB.set_xlabel("months beyond the training cutoff")
style.panel(axB, "b", "proposal precision and coverage")

for ax in (axA, axB):
    style.clean(ax)
    ax.set_xticks(a.horizon_months.tolist())
    ax.yaxis.set_major_locator(MaxNLocator(integer=True, nbins=5))
axB.set_ylim(6, 92)
fig.align_ylabels([axA, axB])

# Direct labels on the curves instead of a legend box. Both are anchored at
# the first month and read left to right, so no label can be crossed by the
# curve it names: the earlier centred label had the descending red curve
# drawn through the tau glyph, half erasing it.
style.tag(axB, 1, p.precision.iloc[0] * 100 + 2.0,
          "proposal precision at fixed $\\tau$", colour=RED, ha="left",
          va="bottom", size=style.FS_SMALL)
style.tag(axB, 1, p.coverage.iloc[0] * 100 + 2.0, "coverage", colour=GREEN,
          ha="left", va="bottom", size=style.FS_SMALL)

# The one reading the panel is for, in words, on a hairline leader: the
# precision holds and the coverage does not.
c0, c1 = p.coverage.iloc[0] * 100, p.coverage.iloc[-1] * 100
style.note(axB, f"{c0:.0f}% of eligible cases at month 1,\n{c1:.0f}% at "
                f"month {int(p.horizon_months.iloc[-1])}",
           xy=(p.horizon_months.iloc[-1], c1), xytext=(5.85, 40.0),
           colour=GREEN, ha="right")

style.save(fig, OUT / "fig_horizon.pdf")
print("wrote fig_horizon.pdf")
