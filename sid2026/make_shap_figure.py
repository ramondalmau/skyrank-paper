"""What the model actually leans on, by mean absolute SHAP value.

Colour carries the feature family, so the reader sees at a glance that the
route itself and the regulation picture dominate the cost indicators.
"""
from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.patches import Patch
import matplotlib as mpl
import style
from style import ACCENT, GREEN, GREY, INK, RED, apply

apply()
mpl.rcParams["hatch.linewidth"] = 0.35
T = Path("/home/rdcodina/projects/skyrank/studies/2026-07-fuel-study/tables")
OUT = Path("/data/rdcodina/skyrank/_audit/paper/figures")

FAMILY = {
    "icaoRoutePoints": ("the route itself", ACCENT),
    "atfmDelay": ("regulation", RED),
    "numberOfRegulations": ("regulation", RED),
    "lookAheadTime": ("rotation and context", GREY),
    "kpiConsumedFuelIndicator": ("cost", GREEN),
    "kpiRouteChargeIndicator": ("cost", GREEN),
    "kpiLength": ("cost", GREEN),
    "kpiDuration": ("cost", GREEN),
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

# Colour alone separated the families, which fails in greyscale: the blue,
# red and green sit at L* 45.4, 45.6 and 47.0, i.e. the same shade of grey.
# Two opposed thin diagonals separate them; the light grey family needs no
# hatch because it already separates by lightness (L* 79.9).
HATCH = {"the route itself": "", "regulation": "//",
         "cost": "\\\\", "rotation and context": ""}

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
ax.set_xlabel("mean effect on the score")
ax.set_xlim(0, d.mean_abs_shap.max() * 1.06)
ax.spines[["top", "right", "left"]].set_visible(False)
ax.tick_params(axis="y", length=0)
ax.grid(axis="x", color="#cfcdc8", lw=0.45, alpha=0.6)
ax.set_axisbelow(True)

seen, handles = set(), []
for f in reversed(d.feature.tolist()):
    lab, col = FAMILY[f]
    if lab not in seen:
        seen.add(lab)
        handles.append(Patch(fc=col, ec="white", lw=0.5, hatch=HATCH[lab],
                             label=lab))
ax.legend(handles=handles, fontsize=style.FS_TICK, frameon=False,
          loc="lower right",
          handlelength=1.0, handleheight=0.9, labelspacing=0.35,
          borderaxespad=0.2)

fig.savefig(OUT / "fig_shap.pdf")
print("wrote fig_shap.pdf")
