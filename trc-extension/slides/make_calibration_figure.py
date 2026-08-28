"""Pictogram for the calibration slide: how a score gap becomes a
probability, shown as a plain count instead of a statistical curve --
no axes, no curve shape, no method name, just 10 cases and an outcome
each. The 8-out-of-10 split is the paper's own illustrative framing for
this exact score gap (trc2026.tex sec:calibration: "about eight times in
ten"). The minimum bar (6 of 10) is tau = 0.600 (Table~tab:operating, 80%
precision target), stated here as a plain count rather than the paper's
own decimal notation.
"""

from __future__ import annotations

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle

INK = "#2f2f2f"
GREEN = "#2e7d5b"
RED = "#b5484d"
GREY = "#c8c6c1"

plt.rcParams.update(
    {
        "font.family": "serif",
        "font.serif": ["STIXGeneral", "DejaVu Serif"],
        "mathtext.fontset": "stix",
        "text.color": INK,
    }
)

n = 10
picked = 8  # real: "about eight times in ten" for a +3.6 gap (sec:calibration)
threshold = 6  # real: tau = 0.600 -> need at least 6 of 10

fig, ax = plt.subplots(figsize=(10.4, 3.6), dpi=220)

for i in range(1, n + 1):
    color = GREEN if i <= picked else GREY
    ax.add_patch(Circle((i, 0), 0.38, facecolor=color, edgecolor="white",
                          linewidth=2.5, zorder=3))

ax.text((picked + 1) / 2, 0.78, f"{picked} of 10: airline picked the model's suggestion",
        ha="center", va="bottom", color=GREEN, fontsize=14.5, fontweight="bold")

ax.plot([threshold + 0.5, threshold + 0.5], [-0.55, 0.55], color=RED, lw=2.2,
         ls=(0, (5, 3)), zorder=2)
ax.text(threshold + 0.5, -0.75, "policy needs at least 6 of 10 to propose",
        ha="center", va="top", color=RED, fontsize=14.5)

ax.text((n + 1) / 2, -1.25, "for every 10 past cases with a lead around +3.6",
        ha="center", va="top", color=INK, fontsize=13.5, style="italic")

ax.set_xlim(0, n + 1)
ax.set_ylim(-1.45, 1.0)
ax.set_aspect("equal")
ax.axis("off")

fig.tight_layout()
fig.savefig("figures/fig_calibration.png", facecolor="white")
print("wrote figures/fig_calibration.png")
