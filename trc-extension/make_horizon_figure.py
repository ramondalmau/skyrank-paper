"""Fig: accuracy and proposal precision against months since training cutoff.

Drawn at print size for the elsarticle preprint layout (0.7\\textwidth of
about 406 pt), same conventions as the SID figures: STIX text, no scaling
at include time, colour never the only cue.
"""
from __future__ import annotations

from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd

T = Path(__file__).resolve().parents[2] / "studies/2026-08-trc-horizon/tables"
OUT = Path(__file__).resolve().parent / "figures"

ACCENT, RED, INK = "#31688e", "#c03a2b", "#2b2a28"
mpl.rcParams.update({
    "font.family": "serif",
    "font.serif": ["STIXGeneral", "DejaVu Serif"],
    "mathtext.fontset": "stix",
    "font.size": 9.0, "xtick.labelsize": 8.0, "ytick.labelsize": 8.0,
    "axes.labelsize": 9.0, "legend.fontsize": 8.0,
    "pdf.fonttype": 42, "savefig.bbox": "standard", "savefig.pad_inches": 0.0,
    "axes.linewidth": 0.7,
})

acc = pd.read_csv(T / "horizon_accuracy.csv")
pol = pd.read_csv(T / "horizon_policy.csv")
a = acc[acc.stratum == "all"].sort_values("horizon_months")
p = pol.sort_values("horizon_months")

# 270 x 160 TeX pt (1 pt = 1/72.27 in); matplotlib inches are 1/72 in
W, H = 270 / 72.27, 160 / 72.27
fig, ax = plt.subplots(figsize=(W, H), layout="constrained")
ax.fill_between(a.horizon_months, a.ci_lo * 100, a.ci_hi * 100,
                color=ACCENT, alpha=0.22, lw=0)
ax.plot(a.horizon_months, a.accuracy * 100, color=ACCENT, lw=2.0,
        marker="o", ms=4, mfc="white", mew=1.3, solid_capstyle="round",
        label="pairwise accuracy")
ax.fill_between(p.horizon_months, p.ci_lo * 100, p.ci_hi * 100,
                color=RED, alpha=0.15, lw=0)
ax.plot(p.horizon_months, p.precision * 100, color=RED, lw=2.0,
        ls=(0, (4, 2)), marker="s", ms=3.6, mfc="white", mew=1.3,
        dash_capstyle="round", label="proposal precision at fixed $\\tau$")
ax.set_xlabel("months beyond the training cutoff")
ax.set_ylabel("[%]")
ax.set_xticks(a.horizon_months.tolist())
ax.spines[["top", "right"]].set_visible(False)
ax.grid(axis="y", color="#cfcdc8", lw=0.45, alpha=0.6)
ax.set_axisbelow(True)
ax.legend(frameon=False, loc="best", handlelength=1.8)
fig.savefig(OUT / "fig_horizon.pdf")
print("wrote fig_horizon.pdf")
