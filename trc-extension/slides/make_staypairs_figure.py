"""Real chart for the stay-pairs / bias-correction slide. Data from
trc2026.tex sec:changebias: regulation-blind accuracy on held-out stay pairs
(the flight kept its route despite a demonstrated, comparably priced
alternative), with and without the stay-pair correction.
"""

from __future__ import annotations

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

INK = "#2f2f2f"
GREEN = "#2e7d5b"
RED = "#b5484d"
BORDER = "#cbc8c2"

plt.rcParams.update(
    {
        "font.family": "serif",
        "font.serif": ["STIXGeneral", "DejaVu Serif"],
        "mathtext.fontset": "stix",
        "text.color": INK,
        "axes.labelcolor": INK,
        "xtick.color": INK,
        "ytick.color": INK,
    }
)

rows = ["before this fix", "after this fix"]
acc = [45.7, 57.3]
colors = [RED, GREEN]

fig, ax = plt.subplots(figsize=(10.2, 3.2), dpi=220)
deltas = [a - 50 for a in acc]
bars = ax.barh(rows, deltas, left=50, color=colors, height=0.5, zorder=3)
for b, v in zip(bars, acc):
    ax.text(v + (0.4 if v >= 50 else -0.4), b.get_y() + b.get_height() / 2,
             f"{v:.1f}%", va="center", ha="left" if v >= 50 else "right",
             fontsize=14, color=INK)

ax.axvline(50, color=INK, lw=1.2, zorder=2)
ax.text(50, -0.8, "chance = 50%", ha="center", fontsize=12, color=INK)

ax.set_xlim(40, 63)
ax.set_xlabel("accuracy on flights that stayed put [%]", fontsize=12)
ax.invert_yaxis()
ax.tick_params(axis="y", labelsize=14, length=0)
ax.tick_params(axis="x", labelsize=11)
for side in ("top", "right", "left"):
    ax.spines[side].set_visible(False)
ax.spines["bottom"].set_color(BORDER)
ax.set_axisbelow(True)

fig.tight_layout(rect=(0, 0.05, 1, 1))
fig.savefig("figures/fig_staypairs.png", facecolor="white")
print("wrote figures/fig_staypairs.png")
