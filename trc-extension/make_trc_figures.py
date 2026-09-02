"""Re-render the SID figures at TR-C print size (390 pt text width).

The elsarticle preprint text block is 390 pt wide against IEEEtran's
516 pt, so including the SID PDFs would scale them 0.76x and shrink
their 8 pt fonts to ~6 pt. The SID machinery draws at whatever
style.SIZES says, so this driver overrides the sizes and re-runs the
generators; the manuscript then includes every figure at its natural
size, with no scaling at include time.

Aspect ratios are preserved so annotation layouts survive. Outputs are
copied into paper/trc-extension/figures/; the SID staging directory
(/data/rdcodina/skyrank/_audit/paper/figures) ends up holding the TR-C
sizes afterwards -- the committed copies in paper/sid2026/figures/
remain the authoritative SID versions.
"""
from __future__ import annotations

import os
import runpy
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SID = HERE.parent / "sid2026"
sys.path.insert(0, str(SID))

import style  # noqa: E402  (the SID style module)

# width x height in TeX pt; same aspect ratios as the SID sizes.
# style.size() divides by 72, i.e. it treats these numbers as big points
# (1/72 in), while LaTeX's \textwidth is measured in TeX points
# (1/72.27 in). Without the conversion below a "390 pt" figure comes out
# 390 bp = 391.46 TeX pt and overflows the 390 pt text block by 1.46 pt.
PT2BP = 72.0 / 72.27
TRC_SIZES_PT = {
    "pair_idea":         (390, 104),
    "fig_coverage":      (270, 167),
    "fig_shap":          (270, 201),
    "fig_tradeoff":      (270, 160),
    "fig_concentration": (270, 169),
    "map_escape":        (195, 190),
    "map_saver":         (250, 124),
}
style.SIZES.update({
    name: (w * PT2BP, h * PT2BP) for name, (w, h) in TRC_SIZES_PT.items()
})

for script in ("make_pair_figure.py", "make_data_figures.py",
               "make_shap_figure.py", "make_maps.py"):
    print(f"== {script}")
    runpy.run_path(str(SID / script), run_name="__main__")

OUT = Path("/data/rdcodina/skyrank/_audit/paper/figures")
for name in ("pair_idea", "fig_coverage", "fig_shap", "fig_tradeoff",
             "fig_concentration", "map_escape", "map_saver"):
    # copy through a temporary name in the destination directory and rename
    # over the target: an interrupted copy then leaves the previous good
    # figure in place instead of a truncated PDF the build cannot read
    dst = HERE / "figures" / f"{name}.pdf"
    tmp = dst.with_name(f".{name}.partial.pdf")
    shutil.copyfile(OUT / f"{name}.pdf", tmp)
    os.replace(tmp, dst)
    print(f"copied {name}.pdf")
