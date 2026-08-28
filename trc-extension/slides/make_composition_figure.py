"""Real chart for the archive-composition slide. Data from trc2026.tex
Table~tab:composition. Grounds the "1.16M pairs" scale inside an actual
breakdown instead of a standalone number, and calls back to the two anecdote
maps already shown (map_escape = "escaped", map_saver = "unregulated").
"""

from __future__ import annotations

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

INK = "#2f2f2f"
GREEN = "#2e7d5b"
RED = "#b5484d"
ACCENT = "#3b6ea5"
GREY = "#c8c6c1"
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

# ordered by share, descending -- labels are plain-language, not the paper's
# technical context names (unregulated/escaped/reduced delay/...), so a
# first-time viewer doesn't need "regulation" defined to read this chart
rows = [
    ("no delay involved", 69.4, GREEN),
    ("cut the delay", 11.0, GREY),
    ("delay didn't improve", 9.8, GREY),
    ("dodged the delay entirely", 8.3, RED),
    ("chose to accept delay", 1.4, GREY),
]
labels = [r[0] for r in rows]
shares = [r[1] for r in rows]
colors = [r[2] for r in rows]

fig, ax = plt.subplots(figsize=(10.4, 4.6), dpi=220)
bars = ax.barh(labels, shares, color=colors, height=0.58, zorder=3)
for b, v in zip(bars, shares):
    ax.text(v + 1.2, b.get_y() + b.get_height() / 2, f"{v:.1f}%", va="center", fontsize=13)

i_unreg = labels.index("no delay involved")
i_escape = labels.index("dodged the delay entirely")
y_unreg = bars[i_unreg].get_y() + bars[i_unreg].get_height() / 2
y_escape = bars[i_escape].get_y() + bars[i_escape].get_height() / 2
ax.text(69.4 + 8.5, y_unreg, "the fuel saver\n(previous slide)",
         va="center", fontsize=11, color=GREEN, style="italic")
ax.text(8.3 + 8.5, y_escape, "the escape\n(two slides ago)",
         va="center", fontsize=11, color=RED, style="italic")

ax.set_xlim(0, 100)
ax.set_xlabel("share of revisions, Jan 2025–Jun 2026 [%]", fontsize=12)
ax.invert_yaxis()
ax.tick_params(axis="y", labelsize=13, length=0)
ax.tick_params(axis="x", labelsize=11)
for side in ("top", "right", "left"):
    ax.spines[side].set_visible(False)
ax.spines["bottom"].set_color(BORDER)
ax.set_axisbelow(True)

fig.tight_layout()
fig.savefig("figures/fig_composition.png", facecolor="white")
print("wrote figures/fig_composition.png")
