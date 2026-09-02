"""Fig: accuracy and proposal precision against months since training cutoff.

Drawn at print size for the elsarticle preprint layout (0.7\\textwidth of
about 406 pt), same conventions as the SID figures: STIX text, no scaling
at include time, colour never the only cue.
"""
from __future__ import annotations

from pathlib import Path

import sys

import matplotlib.pyplot as plt
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "sid2026"))
import style  # noqa: E402  (the shared style module)

T = Path(__file__).resolve().parents[2] / "studies/2026-08-trc-horizon/tables"
OUT = Path(__file__).resolve().parent / "figures"

# This figure used to carry its own near-copies of the palette and the rc
# block, so it drifted a shade away from every other figure in the paper.
# It now takes both from the shared module, like the rest of the set.
style.apply()
ACCENT, RED, INK = style.ACCENT, style.RED, style.INK

acc = pd.read_csv(T / "horizon_accuracy.csv")
pol = pd.read_csv(T / "horizon_policy.csv")
a = acc[acc.stratum == "all"].sort_values("horizon_months")
p = pol.sort_values("horizon_months")

# 270 x 160 TeX pt (1 pt = 1/72.27 in); matplotlib inches are 1/72 in
W, H = 270 / 72.27, 160 / 72.27
fig, ax = plt.subplots(figsize=(W, H), layout="constrained")
ax.fill_between(a.horizon_months, a.ci_lo * 100, a.ci_hi * 100,
                color=ACCENT, alpha=0.20, lw=0)
ax.plot(a.horizon_months, a.accuracy * 100, color=ACCENT, lw=style.LW,
        marker="o", ms=4, mfc="white", mew=1.3, solid_capstyle="round",
        zorder=4)
ax.fill_between(p.horizon_months, p.ci_lo * 100, p.ci_hi * 100,
                color=RED, alpha=0.15, lw=0)
ax.plot(p.horizon_months, p.precision * 100, color=RED, lw=style.LW,
        ls=(0, (4, 2)), marker="s", ms=3.6, mfc="white", mew=1.3,
        dash_capstyle="round", zorder=4)
ax.set_xlabel("months beyond the training cutoff")
ax.set_ylabel("[%]")
ax.set_xticks(a.horizon_months.tolist())
style.clean(ax)

# Two series, both flat and well separated: name them on the curves and drop
# the legend box entirely. Round markers plus a solid line against square
# markers plus a dashed line keep them apart without colour.
xa = a.horizon_months.iloc[len(a) // 2]
style.tag(ax, xa, a.accuracy.iloc[len(a) // 2] * 100 + 1.6,
          "pairwise accuracy", colour=ACCENT, ha="center", va="bottom",
          size=style.FS_SMALL)
xp = p.horizon_months.iloc[len(p) // 2]
style.tag(ax, xp, p.precision.iloc[len(p) // 2] * 100 - 1.6,
          "proposal precision at fixed $\\tau$", colour=RED, ha="center",
          va="top", size=style.FS_SMALL)
style.save(fig, OUT / "fig_horizon.pdf")
print("wrote fig_horizon.pdf")
