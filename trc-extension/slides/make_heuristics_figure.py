"""Real chart replacing the "45%" hero-number slide: every cost-only rule
against a coin flip. Data from trc2026.tex Table~tab:heuristics (accuracy
column, undecided pairs scored as a coin toss).
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

rules = [
    "prefer less planned fuel",
    "prefer less flight time",
    "prefer shorter distance",
    "prefer lower route charges",
    "prefer less attributed delay",
]
acc = [44.9, 46.6, 46.0, 47.0, 53.3]
colors = [GREEN if a >= 50 else RED for a in acc]

fig, ax = plt.subplots(figsize=(10.2, 4.6), dpi=220)
# bars diverge from 50% (chance), not from zero: chance is the meaningful
# baseline for this comparison, and a zero-based or truncated axis would
# misrepresent how close these rules are to a coin flip
deltas = [a - 50 for a in acc]
bars = ax.barh(rules, deltas, left=50, color=colors, height=0.55, zorder=3)
for b, v in zip(bars, acc):
    ax.text(v + (0.4 if v >= 50 else -0.4), b.get_y() + b.get_height() / 2,
             f"{v:.1f}%", va="center", ha="left" if v >= 50 else "right",
             fontsize=13, color=INK)

ax.axvline(50, color=INK, lw=1.2, zorder=2)
ax.text(50, -0.85, "chance = 50%", ha="center", fontsize=12, color=INK)

ax.set_xlim(42, 56)
ax.set_xlabel("accuracy [%]", fontsize=12)
ax.invert_yaxis()
ax.tick_params(axis="y", labelsize=13, length=0)
ax.tick_params(axis="x", labelsize=11)
for side in ("top", "right", "left"):
    ax.spines[side].set_visible(False)
ax.spines["bottom"].set_color(BORDER)
ax.set_axisbelow(True)

fig.tight_layout(rect=(0, 0.03, 1, 1))
fig.savefig("figures/fig_heuristics.png", facecolor="white")
print("wrote figures/fig_heuristics.png")
