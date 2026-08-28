"""Redraw the data figures from their CSVs in the paper's own style.

Green for the route the airline chose and the fuel it saves, red for what that
costs in precision, one cool accent for everything else.
"""
from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import style
from style import ACCENT, GREEN, GREY, INK, LW, RED, apply, clean

apply()
T = Path("/home/rdcodina/projects/skyrank/studies/2026-07-fuel-study/tables")
OUT = Path("/data/rdcodina/skyrank/_audit/paper/figures")

# --- 1. accuracy against coverage ----------------------------------------
d = pd.read_csv(T / "coverage_accuracy.csv").sort_values("coverage")
x, y = d.coverage * 100, d.accuracy * 100
fig, ax = plt.subplots(figsize=style.size("fig_coverage"), layout="constrained")
# a faint body under the curve gives the figure weight; the darker band is
# the confidence interval and is the only shading that carries information
ax.fill_between(x, 50, y, color=ACCENT, alpha=0.07, lw=0)
ax.fill_between(x, d.ci_lo * 100, d.ci_hi * 100, color=ACCENT, alpha=0.22,
                lw=0)
ax.plot(x, y, color=ACCENT, lw=LW, solid_capstyle="round", zorder=4)
ax.axhline(50, color=GREY, ls=(0, (1, 2.6)), lw=1.0, zorder=2)
ax.text(1.5, 51.4, "chance", fontsize=style.FS_TICK, color="#8a8884",
        ha="left", va="bottom")
# the two points the text quotes, and nothing else: the caption explains them
for cov, tx, ty, ha in ((20, 25.0, 97.0, "left"), (100, 97.0, 71.5, "right")):
    row = d.iloc[(d.coverage * 100 - cov).abs().argmin()]
    px, py = row.coverage * 100, row.accuracy * 100
    ax.plot(px, py, "o", ms=5.4, mfc="white", mec=ACCENT, mew=1.6, zorder=6)
    ax.text(tx, ty, f"{py:.0f} %", fontsize=style.FS_ANNOT, color=ACCENT,
            ha=ha, va="bottom", zorder=6)
ax.set_xlabel("cases answered [%]")
ax.set_ylabel("accuracy [%]")
ax.set_xlim(-2, 106)
ax.set_ylim(46, 103)
ax.set_yticks([50, 60, 70, 80, 90, 100])
ax.set_xticks([0, 20, 40, 60, 80, 100])
clean(ax)
fig.savefig(OUT / "fig_coverage.pdf"); plt.close(fig)

# --- 2. the fuel/precision trade-off --------------------------------------
# The grid sweeps two knobs: the acceptance threshold and a minimum-saving
# filter. Only the unfiltered slice belongs on a curve against tau.
g = pd.read_csv(T / "muac_grid.csv")
g = g[(g.min_saving_kg == 0) & g.tau.between(0.45, 0.90)].sort_values("tau")
fig, ax = plt.subplots(figsize=style.size("fig_tradeoff"),
                       layout="constrained")
ax.plot(g.tau, g.realized_kg / 1e6, color=GREEN, lw=LW)
ax.set_xlabel("acceptance threshold")
ax.set_ylabel("fuel confirmed [kt / quarter]", color=GREEN)
ax.tick_params(axis="y", colors=GREEN)
ax2 = ax.twinx()
ax2.plot(g.tau, g.precision * 100, color=RED, lw=LW, ls=(0, (4, 2)),
         dash_capstyle="round")
ax2.plot(0.60, g.iloc[(g.tau - 0.60).abs().argmin()].precision * 100, "o",
         ms=5, mfc="white", mec=RED, mew=1.5, zorder=5)
ax2.set_ylabel("precision [%]", color=RED)
ax2.tick_params(axis="y", colors=RED)
ax2.spines[["top"]].set_visible(False)
op = g.iloc[(g.tau - 0.60).abs().argmin()]
ax.axvline(0.60, color=INK, lw=0.8, ls=":")
ax.plot(0.60, op.realized_kg / 1e6, "o", ms=5, mfc="white", mec=GREEN,
        mew=1.5, zorder=5)
ax.annotate("operating point", xy=(0.60, op.realized_kg / 1e6),
            xytext=(0.71, op.realized_kg / 1e6 + 2.6),
            fontsize=style.FS_ANNOT, color=INK, ha="center",
            arrowprops=dict(arrowstyle="->", color=INK, lw=0.9))
ax.spines[["top"]].set_visible(False)
ax.set_axisbelow(True)
fig.savefig(OUT / "fig_tradeoff.pdf"); plt.close(fig)

# --- 3. where the value sits ----------------------------------------------
# A stacked bar hid the point: the head of the distribution was a sliver next
# to 787 operators. The cumulative curve shows the concentration directly.
# The per-operator table covers the top 15, which is 71% of the fuel; beyond
# that the curve is drawn through the two published anchors and marked.
c = pd.read_csv(T / "fuel_concentration.csv")
r = c[c.dimension == "operator"].iloc[0]
n50, n80, tot = int(r.n_for_50pct), int(r.n_for_80pct), int(r.entities_total)

op = pd.read_csv(T / "muac_breakdown_operator.csv").sort_values(
    "realized_kg", ascending=False)
TOTAL_KG = pd.read_csv(T / "muac_grid.csv").query(
    "min_saving_kg == 0 and tau == 0.60").realized_kg.iloc[0]
cum = (op.realized_kg.cumsum() / TOTAL_KG * 100).tolist()
xs_m, ys_m = list(range(1, len(cum) + 1)), cum

# Six operators out of 815 is invisible on a linear axis: the curve becomes a
# vertical spike against the y-axis. A log rank axis puts the head where the
# reader can see it and still shows the whole fleet.
fig, ax = plt.subplots(figsize=style.size("fig_concentration"),
                       layout="constrained")
eq_x = [1, 3, 10, 30, 100, 300, tot]
ax.plot(eq_x, [x / tot * 100 for x in eq_x], color=GREY, ls=(0, (3, 3)), lw=1.1)
ax.text(190, 14, "if every operator\ncontributed equally", fontsize=7,
        color=INK, ha="center", va="top", linespacing=1.3)
ax.plot(xs_m, ys_m, color=ACCENT, lw=LW, solid_capstyle="round")
ax.plot([xs_m[-1], n80, tot], [ys_m[-1], 80, 100], color=ACCENT, lw=1.3,
        ls=(0, (2, 2)))
ax.annotate(f"{n50} operators\nfly half of it", xy=(n50, ys_m[n50 - 1]),
            xytext=(22, 30), fontsize=7.4, color=ACCENT, ha="center",
            va="center", linespacing=1.3,
            arrowprops=dict(arrowstyle="->", color=ACCENT, lw=0.8))
ax.annotate(f"{n80} operators\nfly 80%", xy=(n80, 80), xytext=(110, 62),
            fontsize=7.4, color=ACCENT, ha="center", va="center",
            linespacing=1.3,
            arrowprops=dict(arrowstyle="->", color=ACCENT, lw=0.8))
for n, y in ((n50, ys_m[n50 - 1]), (n80, 80)):
    ax.plot(n, y, "o", ms=4.8, mfc="white", mec=ACCENT, mew=1.5, zorder=6)
ax.set_xscale("log")
ax.set_xlabel(f"operators, ranked by fuel confirmed (of {tot})")
ax.set_ylabel("cumulative fuel [%]")
ax.set_xlim(1, tot); ax.set_ylim(0, 104)
ax.set_xticks([1, 3, 10, 30, 100, 300, 800])
ax.set_xticklabels(["1", "3", "10", "30", "100", "300", "800"])
ax.minorticks_off()
clean(ax)
fig.savefig(OUT / "fig_concentration.pdf"); plt.close(fig)

for f in ("fig_coverage", "fig_tradeoff", "fig_concentration"):
    print("wrote", f)
