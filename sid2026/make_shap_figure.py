"""What the model actually leans on, by mean absolute SHAP value.

Colour carries the feature group of Table 1, so the reader sees at a glance
that the route itself and the regulation picture dominate the cost
indicators. The groups are named in the plot area, on the leading bar of each
group, rather than in a legend the eye has to travel to and match by swatch.
"""
from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import matplotlib as mpl
from matplotlib.patches import Patch
import style
from style import ACCENT, GREEN, GREY, INK, RED, apply

apply()
mpl.rcParams["hatch.linewidth"] = 0.35
T = Path("/home/rdcodina/projects/skyrank/studies/2026-07-fuel-study/tables")
OUT = Path("/data/rdcodina/skyrank/_audit/paper/figures")

# Group names are the groups of Table 1 (tab:features) verbatim, so the
# figure and the table can be read against each other without translation.
# lookAheadTime is a rotation-and-context feature, not a cost indicator.
FAMILY = {
    "icaoRoutePoints": ("route", ACCENT),
    "atfmDelay": ("regulation", RED),
    "numberOfRegulations": ("regulation", RED),
    "lookAheadTime": ("rotation and context", GREY),
    "kpiConsumedFuelIndicator": ("indicators", GREEN),
    "kpiRouteChargeIndicator": ("indicators", GREEN),
    "kpiLength": ("indicators", GREEN),
    "kpiDuration": ("indicators", GREEN),
    "turnaroundInbound": ("rotation and context", GREY),
    "turnaroundOutbound": ("rotation and context", GREY),
    "calendarHour": ("rotation and context", GREY),
}
PRETTY = {
    "icaoRoutePoints": "route (waypoint sequence)",
    "atfmDelay": "attributed ATFM delay",
    "lookAheadTime": "time to departure",
    "kpiConsumedFuelIndicator": "planned fuel",
    "turnaroundInbound": "inbound connection",
    "turnaroundOutbound": "outbound connection",
    "calendarHour": "hour of day",
    "kpiRouteChargeIndicator": "route charges",
    "numberOfRegulations": "number of regulations",
    "kpiLength": "distance",
    "kpiDuration": "flight time",
}

# Colour alone separated the groups, which fails in greyscale: the blue,
# red and green sit at L* 45.4, 45.6 and 47.0, i.e. the same shade of grey.
# Two opposed thin diagonals separate them; the light grey group needs no
# hatch because it already separates by lightness (L* 79.9). The direct
# group labels are the third, and strongest, non-colour cue.
HATCH = {"route": "", "regulation": "//",
         "indicators": "\\\\", "rotation and context": ""}

d = pd.read_csv(T / "shap_importance.csv")
d = d[d.feature.isin(FAMILY)].nlargest(11, "mean_abs_shap")
d = d.sort_values("mean_abs_shap")

fig, ax = plt.subplots(figsize=style.size("fig_shap"),
                       layout="constrained")
cols = [FAMILY[f][1] for f in d.feature]
hats = [HATCH[FAMILY[f][0]] for f in d.feature]
bars = ax.barh(range(len(d)), d.mean_abs_shap, color=cols, height=0.72,
               edgecolor="white", linewidth=0.5)
for b, h in zip(bars, hats):
    b.set_hatch(h)
ax.set_yticks(range(len(d)))
ax.set_yticklabels([PRETTY[f] for f in d.feature],
                   fontsize=style.FS_TICK)
# "mean effect on the score" left a reader asking what the numbers are in.
# They are mean absolute SHAP values, and SHAP is additive in the units of
# the quantity explained, so they are increments of the ranking score
# itself. Printing each bar's value as well gives the scale an anchor that
# does not depend on reading a gridline back to the axis.
ax.set_xlabel("mean |SHAP| value [score units]")
XMAX = d.mean_abs_shap.max() * 1.20
ax.set_xlim(0, XMAX)
ax.spines[["top", "right", "left"]].set_visible(False)
ax.tick_params(axis="y", length=0)
ax.set_axisbelow(True)
for i, val in enumerate(d.mean_abs_shap):
    ax.text(val + XMAX * 0.016, i, f"{val:.2f}", fontsize=style.FS_SMALL,
            color=INK, va="center", ha="left", zorder=6)

# A small key, not labels written across the bars. Direct labelling is the
# better instrument when a series owns a region of the plot; here the
# groups interleave, because the bars are ordered by value and not by
# group, so every direct label had to be written on top of a coloured bar.
# Two zero-context readers reported the result as unreadable and could not
# tell that colour encoded a group at all. A titled, frameless key in the
# empty lower-right corner states the mapping once and touches nothing.
handles = []
for lab in ("route", "regulation", "indicators", "rotation and context"):
    col = next(c for l, c in FAMILY.values() if l == lab)
    handles.append(Patch(fc=col, ec="white", lw=0.5, hatch=HATCH[lab],
                         label=lab))
leg = ax.legend(handles=handles, title="feature group",
                fontsize=style.FS_SMALL, loc="lower right",
                handlelength=1.0, handleheight=0.9, labelspacing=0.3,
                borderaxespad=0.2, alignment="left")
leg.get_title().set_fontsize(style.FS_SMALL)
leg.get_title().set_color(INK)

style.save(fig, OUT / "fig_shap.pdf")
print("wrote fig_shap.pdf")
