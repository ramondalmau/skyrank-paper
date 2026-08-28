"""Real chart for the "where the accuracy lives" slide. Data from
trc2026.tex Table~tab:strata: pairwise accuracy against the delay carried by
the abandoned route -- monotonic, which is the paper's own reading (bigger
delay, clearer incentive, easier call).
"""

from __future__ import annotations

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

INK = "#2f2f2f"
BORDER = "#cbc8c2"
GREY_LINE = "#9a9a9a"

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

labels = ["none", "≤ 15 min", "15–30 min", "30–60 min", "> 60 min"]
acc = [63.9, 69.9, 78.7, 84.6, 84.6]
# sequential blue, darker = more delay on the abandoned route
blues = ["#aac4dc", "#7ba3c4", "#4c82ac", "#3b6ea5", "#2a5480"]

fig, ax = plt.subplots(figsize=(10.2, 4.6), dpi=220)
bars = ax.bar(labels, acc, color=blues, width=0.6, zorder=3)
for b, v in zip(bars, acc):
    ax.text(b.get_x() + b.get_width() / 2, v + 1.2, f"{v:.1f}%",
             ha="center", fontsize=13, color=INK)

ax.axhline(50, color=GREY_LINE, lw=1.2, ls=(0, (4, 3)), zorder=2)
ax.text(4.65, 51.3, "chance", ha="right", fontsize=11, color=GREY_LINE)

ax.set_ylim(45, 92)
ax.set_ylabel("accuracy [%]", fontsize=12)
ax.set_xlabel("delay on the route it left behind", fontsize=12)
ax.tick_params(axis="x", labelsize=13, length=0)
ax.tick_params(axis="y", labelsize=11)
for side in ("top", "right"):
    ax.spines[side].set_visible(False)
ax.spines["left"].set_color(BORDER)
ax.spines["bottom"].set_color(BORDER)
ax.set_axisbelow(True)

fig.tight_layout()
fig.savefig("figures/fig_strata.png", facecolor="white")
print("wrote figures/fig_strata.png")
