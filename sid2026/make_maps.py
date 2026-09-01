"""Clean route maps for the paper.

The study's maps are annotated for a 40-page report. At two-column width that
annotation is unreadable and ugly. These carry no text at all beyond the two
endpoint names: two routes, the coastline, the endpoints. The caption
explains them.

Three things here are deliberate:

* The maps are drawn in ETRS89-LAEA (EPSG:3035) rather than plotting degrees
  of longitude against degrees of latitude. The previous version corrected
  the aspect with a hand-fitted factor, which stretched Europe.
* Coastlines are Natural Earth 10 m. The previous version used the 110 m
  fixture bundled inside pyogrio's test suite, which is visibly blocky.
* The abandoned route is dashed and the chosen route solid, so the pair is
  still readable when the paper is printed in greyscale. Colour alone was
  the only cue before.
"""
from __future__ import annotations

import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import pandas as pd  # noqa: E402

sys.path.insert(0, str(Path(__file__).parent))
import style  # noqa: E402

WT = Path("/home/rdcodina/projects/skyrank")
sys.path.insert(0, str(WT / "src"))
sys.path.insert(0, str(WT / "studies/2026-07-fuel-study/code"))

from skyrank.analysis.visualise import _airac_from_snapshot  # noqa: E402
from skyrank.aviation.waypoints import load_waypoints  # noqa: E402
from skyrank.geo.routes import route_linestring  # noqa: E402

OUT = Path("/data/rdcodina/skyrank/_audit/paper/figures")
OLD, NEW = style.RED, style.GREEN

CASES = {
    "map_escape": ("1421263_AA82577455", "EHAM", "LEBL"),
    "map_saver": ("827759_AA82551344", "LTBS", "EGCC"),
}
NAMES = {"EHAM": "Amsterdam", "LEBL": "Barcelona",
         "LTBS": "Bodrum", "EGCC": "Manchester"}


def routes_for(pair_uid: str) -> tuple[list[str], list[str], int]:
    for ym in ("2026-04", "2026-05", "2026-06"):
        f = WT / "data/ich_dataset" / f"ich_dataset_{ym}.parquet"
        d = pd.read_parquet(f, columns=["pair_id", "ifplid", "label",
                                        "icaoRoutePoints", "snapshot_date"])
        d["pair_uid"] = d.pair_id.astype(str) + "_" + d.ifplid
        s = d[d.pair_uid == pair_uid]
        if len(s) == 2:
            r0 = s[s.label == 0].icaoRoutePoints.iloc[0].split()
            r1 = s[s.label == 1].icaoRoutePoints.iloc[0].split()
            return r0, r1, int(s.snapshot_date.iloc[0])
    raise SystemExit(f"pair {pair_uid} not found")


style.apply()

for name, (uid, adep, ades) in CASES.items():
    r0, r1, snap = routes_for(uid)
    # the bundled navigation database ends at cycle 538; a 2026 snapshot maps
    # to a later cycle that is not in the file, so clamp as the study does
    wp = load_waypoints(WT / "data/env/waypoints_2025.parquet",
                        min(_airac_from_snapshot(snap), 538))
    l0 = route_linestring(r0, wp, adep, ades)
    l1 = route_linestring(r1, wp, adep, ades)
    if l0.is_empty or l1.is_empty:
        print(f"{name}: geometry empty, skipped")
        continue

    lons = [c[0] for l in (l0, l1) for c in l.coords]
    lats = [c[1] for l in (l0, l1) for c in l.coords]
    pad_lon = (max(lons) - min(lons)) * 0.10 + 0.9
    pad_lat = (max(lats) - min(lats)) * 0.10 + 0.9
    bbox = (min(lons) - pad_lon, min(lats) - pad_lat,
            max(lons) + pad_lon, max(lats) + pad_lat)

    # The axes fills the figure exactly: these maps carry no ticks and no
    # axis labels, so any margin is wasted paper. The frame is then grown to
    # the figure's own aspect, which means the view is never letterboxed and
    # never stretched.
    fig = plt.figure(figsize=style.size(name))
    ax = fig.add_axes([0, 0, 1, 1])
    aspect = style.SIZES[name][0] / style.SIZES[name][1]
    style.basemap(ax, bbox)

    # abandoned first, so the chosen route sits on top where they overlap
    for line, colour, dash in ((l0, OLD, (0, (4.2, 2.0))), (l1, NEW, None)):
        X, Y = style.project(*line.xy)
        ax.plot(X, Y, color=colour, lw=style.LW, solid_capstyle="round",
                dash_capstyle="round",
                linestyle=dash if dash else "solid",
                path_effects=style.halo(style.LW + 1.5), zorder=3)

    # The saver case sits on a thin seasonal sector, where naming both ends
    # plus the geometry would point at a single operator. Its endpoints stay
    # unlabelled; the caption says so.
    label_ends = name != "map_saver"
    for (lon, lat), icao in ((l1.coords[0], adep), (l1.coords[-1], ades)):
        px, py = style.project([lon], [lat])
        style.endpoint(ax, px[0], py[0])
        if not label_ends:
            continue
        up = lat > (min(lats) + max(lats)) / 2
        ax.annotate(NAMES[icao], (px[0], py[0]), (0, 10 if up else -10),
                    textcoords="offset points", ha="center",
                    va="bottom" if up else "top",
                    fontsize=style.FS_ANNOT, color=style.INK, zorder=7,
                    bbox=dict(fc="white", ec="none", alpha=0.82, pad=1.1))

    BX, BY = style.project([bbox[0], bbox[2], bbox[0], bbox[2]],
                           [bbox[1], bbox[3], bbox[3], bbox[1]])
    x0, x1, y0, y1 = min(BX), max(BX), min(BY), max(BY)
    # grow the deficient axis until the frame reaches the target aspect
    w, h = x1 - x0, y1 - y0
    if w / h < aspect:
        g = (aspect * h - w) / 2
        x0, x1 = x0 - g, x1 + g
    else:
        g = (w / aspect - h) / 2
        y0, y1 = y0 - g, y1 + g
    ax.set_xlim(x0, x1)
    ax.set_ylim(y0, y1)
    ax.set_aspect("equal")
    style.frame(ax)
    fig.savefig(OUT / f"{name}.pdf")
    plt.close(fig)
    print(f"wrote {name}.pdf")
