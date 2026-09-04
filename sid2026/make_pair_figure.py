"""The central figure: where the training label comes from.

Both panels draw real route geometry from the archive, in the same visual
language as the case-study maps, so the reader compares labelling schemes
rather than drawing styles.

Left  -- prior work ranks the filed route against a set of candidates. The
         candidates are produced by a route generator and the airspace user
         may never have evaluated them. They are drawn here from other routes
         actually observed on the same city pair, which shows the geometric
         spread a candidate set spans without inventing geometry.
Right -- a revision gives two routes the same operator filed for the same
         flight, one of which it abandoned. The preference is expressed.
"""
from __future__ import annotations

import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import pandas as pd  # noqa: E402
import style  # noqa: E402
from style import GREEN, INK, RED, apply  # noqa: E402

WT = Path("/home/rdcodina/projects/skyrank")
sys.path.insert(0, str(WT / "src"))
from skyrank.analysis.visualise import _airac_from_snapshot  # noqa: E402
from skyrank.aviation.waypoints import load_waypoints  # noqa: E402
from skyrank.geo.routes import route_linestring  # noqa: E402

apply()
OUT = Path("/data/rdcodina/skyrank/_audit/paper/figures")
CITY, ADEP, ADES = "EGLL-LGAV", "EGLL", "LGAV"
N_CANDIDATES = 7

d = pd.read_parquet(WT / "data/ich_dataset/ich_dataset_2026-04.parquet",
                    columns=["pair_id", "ifplid", "label", "icaoRoutePoints",
                             "flightCityPair", "snapshot_date", "kpiLength"])
d = d[d.flightCityPair == CITY]
snap = int(d.snapshot_date.iloc[0])
wp = load_waypoints(WT / "data/env/waypoints_2025.parquet",
                    min(_airac_from_snapshot(snap), 538))


def line(route_text):
    try:
        ls = route_linestring(route_text.split(), wp, ADEP, ADES)
    except Exception:
        return None
    return None if ls.is_empty or len(ls.coords) < 3 else ls


# --- the revision pair: pick the one whose two routes differ most ----------
d["uid"] = d.pair_id.astype(str) + "_" + d.ifplid
best = None
for uid, g in d.groupby("uid"):
    if set(g.label) != {0, 1}:
        continue
    r0 = line(g[g.label == 0].icaoRoutePoints.iloc[0])
    r1 = line(g[g.label == 1].icaoRoutePoints.iloc[0])
    if r0 is None or r1 is None:
        continue
    sep = r0.hausdorff_distance(r1)
    if 1.0 < sep < 3.2 and (best is None or sep > best[0]):
        best = (sep, r0, r1)
_, aband, chosen = best

# --- the candidate pool: distinct observed routes, widest spread first -----
seen, cands = set(), []
for txt in d.icaoRoutePoints.drop_duplicates():
    ls = line(txt)
    if ls is None:
        continue
    key = round(ls.centroid.y, 2)
    if key in seen or ls.hausdorff_distance(chosen) < 0.25:
        continue
    seen.add(key)
    cands.append(ls)
# Sorting by proximity to the chosen route collapsed the fan into one band.
# Sample across the spread instead, so the panel shows the range a candidate
# set spans rather than seven near-copies of the same track.
cands = sorted(cands, key=lambda l: l.hausdorff_distance(chosen))
if len(cands) > N_CANDIDATES:
    step = (len(cands) - 1) / (N_CANDIDATES - 1)
    cands = [cands[round(i * step)] for i in range(N_CANDIDATES)]

fig = plt.figure(figsize=style.size("pair_idea"))
# explicit axes rectangles: the panels fill the figure apart from the strip
# the titles need, so nothing is letterboxed and no space is wasted
TOP, GAP, SIDE = 0.135, 0.030, 0.004
_w = (1 - 2 * SIDE - GAP) / 2
axA = fig.add_axes([SIDE, 0.0, _w, 1 - TOP])
axB = fig.add_axes([SIDE + _w + GAP, 0.0, _w, 1 - TOP])
allx = [c[0] for l in cands + [aband, chosen] for c in l.coords]
ally = [c[1] for l in cands + [aband, chosen] for c in l.coords]
mx, my = (max(allx) - min(allx)) * 0.08 + 0.4, (max(ally) - min(ally)) * 0.12 + 0.4
BBOX = (min(allx) - mx, min(ally) - my, max(allx) + mx, max(ally) + my)
PANEL_ASPECT = _w * style.SIZES["pair_idea"][0] / ((1 - TOP) * style.SIZES["pair_idea"][1])

for ax, letter, title in ((axA, "a", "candidates"), (axB, "b", "a revision")):
    style.basemap(ax, BBOX, borders=True)
    BX, BY = style.project([BBOX[0], BBOX[2], BBOX[0], BBOX[2]],
                           [BBOX[1], BBOX[3], BBOX[3], BBOX[1]])
    x0, x1, y0, y1 = min(BX), max(BX), min(BY), max(BY)
    w, h = x1 - x0, y1 - y0
    if w / h < PANEL_ASPECT:
        g = (PANEL_ASPECT * h - w) / 2
        x0, x1 = x0 - g, x1 + g
    else:
        g = (w / PANEL_ASPECT - h) / 2
        y0, y1 = y0 - g, y1 + g
    ax.set_xlim(x0, x1); ax.set_ylim(y0, y1)
    ax.set_aspect("equal")
    style.frame(ax)
    style.panel(ax, letter, title, pad=3.0)

DASH = (0, (3.4, 1.6))
for ls in cands:
    axA.plot(*style.project(*ls.xy), color=style.MUTED, lw=0.75, alpha=0.9,
             zorder=2, solid_capstyle="round")
axA.plot(*style.project(*chosen.xy), color=GREEN, lw=1.5, zorder=4,
         solid_capstyle="round", path_effects=style.halo(2.9))

axB.plot(*style.project(*aband.xy), color=RED, lw=1.5, zorder=3,
         linestyle=DASH, dash_capstyle="round", path_effects=style.halo(2.9))
axB.plot(*style.project(*chosen.xy), color=GREEN, lw=1.5, zorder=4,
         solid_capstyle="round", path_effects=style.halo(2.9))

for ax in (axA, axB):
    for lon, lat in (chosen.coords[0], chosen.coords[-1]):
        px, py = style.project([lon], [lat])
        ax.plot(px[0], py[0], "o", ms=2.8, mfc="white", mec=INK, mew=0.8,
                zorder=6)

# Direct labels on the routes, not legend plates in the corner. The two
# opaque white boxes the panels used to carry were the heaviest objects in
# a figure whose subject is geometry, and they still made the reader match
# a swatch to a line. Each label goes at the vertex where its own route is
# furthest from the route it is being contrasted with, so it lands in the
# empty part of the panel by construction.
from shapely.geometry import Point  # noqa: E402


def label_route(ax, line, other, colour, word):
    # only the middle of the track is eligible: near an endpoint the two
    # routes are still together and the label crowded the terminal dot
    cs = list(line.coords)
    mid = cs[int(len(cs) * 0.25):max(int(len(cs) * 0.75), 2)] or cs
    pt = max(mid, key=lambda c: other.distance(Point(c)))
    px, py = style.project([pt[0]], [pt[1]])
    # The direction comes from the geometry, not from which half of the map
    # the point happens to sit in: with the old rule the "filed instead"
    # label of panel (b) was written across the abandoned track and its
    # white halo cut the red dashes in two.
    dx, dy, ha, va = style.away_offset(line, pt, other, dist=7.5)
    ax.annotate(word, (px[0], py[0]), (dx, dy),
                textcoords="offset points", ha=ha, va=va,
                fontsize=style.FS_SMALL,
                color=colour, zorder=8, path_effects=style.halo(2.2))


widest = max(cands, key=lambda l: l.hausdorff_distance(chosen))
label_route(axA, widest, chosen, style.MUTED, "candidates")
label_route(axA, chosen, widest, GREEN, "filed")
label_route(axB, aband, chosen, RED, "abandoned")
label_route(axB, chosen, aband, GREEN, "filed instead")

style.save(fig, OUT / "pair_idea.pdf")
print(f"wrote pair_idea.pdf  ({len(cands)} candidates, {CITY})")
