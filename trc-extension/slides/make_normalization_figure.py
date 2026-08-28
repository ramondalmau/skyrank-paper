"""One custom concept figure for the team deck: why within-pair encoding matters.

Matches the palette and type used by the paper's own figures
(paper/sid2026/style.py) so it sits next to them without looking foreign.
"""

from __future__ import annotations

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

INK = "#2f2f2f"
GREY = "#c8c6c1"
ACCENT = "#3b6ea5"
BORDER = "#cbc8c2"

plt.rcParams.update(
    {
        "font.family": "serif",
        "font.serif": ["STIXGeneral", "DejaVu Serif"],
        "mathtext.fontset": "stix",
        "axes.edgecolor": INK,
        "text.color": INK,
        "axes.labelcolor": INK,
        "xtick.color": INK,
        "ytick.color": INK,
    }
)

fig, (axL, axR) = plt.subplots(1, 2, figsize=(10.4, 4.0), dpi=220)

routes = ["route A", "route B"]

# --- left: raw magnitudes ------------------------------------------------
raw = [2000, 2300]
barsL = axL.barh(routes, raw, color=[ACCENT, GREY], height=0.5)
for b, v in zip(barsL, raw):
    axL.text(v + 40, b.get_y() + b.get_height() / 2, f"{v:,} kg", va="center", fontsize=13)
axL.set_xlim(0, 2900)
axL.set_title("what a route-only model sees", fontsize=13, pad=12)
axL.set_xlabel("planned fuel [kg]", fontsize=11)
axL.invert_yaxis()

# --- right: within-pair difference ---------------------------------------
rel = [0, 300]
barsR = axR.barh(routes, rel, color=[ACCENT, GREY], height=0.5)
for b, v in zip(barsR, rel):
    label = "same value" if v == 0 else f"+{v} kg"
    axR.text(v + 40, b.get_y() + b.get_height() / 2, label, va="center", fontsize=13)
axR.set_xlim(0, 2900)
axR.set_title("what the model is trained on", fontsize=13, pad=12)
axR.set_xlabel("difference within the pair [kg]", fontsize=11)
axR.invert_yaxis()

for ax in (axL, axR):
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color(BORDER)
    ax.spines["bottom"].set_color(BORDER)
    ax.tick_params(length=0)
    ax.set_yticklabels(routes, fontsize=12)

fig.text(
    0.503, 0.5, "→", fontsize=30, color=INK, ha="center", va="center",
)

fig.tight_layout(rect=(0, 0, 1, 1))
fig.savefig("figures/fig_normalization.png", facecolor="white")
print("wrote figures/fig_normalization.png")
