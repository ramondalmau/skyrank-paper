"""One palette and one style for every figure in the paper.

Every figure imports from here. Nothing sets its own colour or font size.

Two notes on choices that are not obvious:

* The body text of the paper is Times. Times New Roman is not installed on
  this machine, so asking for it silently fell back to DejaVu Serif and the
  figure labels did not match the captions beside them. STIXGeneral ships
  with matplotlib and is metric-compatible with Times, so it matches.
* The maps are drawn in ETRS89-LAEA (EPSG:3035), the standard equal-area
  projection for Europe, rather than plotting longitude against latitude and
  correcting the aspect by hand. Coastlines come from Natural Earth 10 m;
  the 110 m fixture bundled with pyogrio is a test asset and is visibly
  blocky at column width.
"""
from __future__ import annotations

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.patheffects as pe  # noqa: E402
import matplotlib.pyplot as plt  # noqa: E402

# --- the palette ----------------------------------------------------------
# GREEN = the route the airline chose / the good outcome
# RED   = the route it abandoned / the cost
# INK   = neutral emphasis;  GREY = context;  LAND/COAST = map background
# Hexes are the muted print-safe academic palette of the PaperOrchestra
# plotting doctrine (chart-patterns.md). The MEANINGS are this paper's and
# do not move: green is the route the airline chose, red the one it
# abandoned, blue the neutral accent for everything that is neither.
GREEN = "#208040"
RED = "#cc3030"
INK = "#2f2f2f"
GREY = "#c8c6c1"
LAND = "#e8e6e1"
COAST = "#a9a6a0"
BORDER = "#cbc8c2"
SEA = "#f6f8f9"
ACCENT = "#2060cc"          # a single cool accent, used sparingly

# Figure text is set at the size it will be READ at. Every figure is drawn
# at exactly the size it occupies on the page (see SIZES), and included
# without scaling, so 8.5 pt here is 8.5 pt on paper. The previous figures
# were drawn 3.4 in wide and squeezed to about 2 in by \includegraphics,
# which silently reduced 7.5 pt labels to roughly 4.5 pt.
# One type family (STIX/Times) and four deliberate steps. Nothing is bold:
# emphasis comes from position and colour, not from weight.
FS_PANEL = 8.5              # panel letter (a), (b)
FS_TICK = 8.0
FS_LABEL = 9.0
FS_ANNOT = 8.5
FS_SMALL = 7.4              # secondary annotation, band labels
LW = 1.5                    # the doctrine draws light; 2.0 pt read as heavy

# Two auxiliary inks, both desaturated so they never compete with the three
# semantic colours. FAINT is for reference lines the reader must not read as
# data; MUTED is for context series (candidate routes, equal-share lines).
FAINT = "#dedbd5"
MUTED = "#666666"           # the doctrine's neutral series grey

COL_PT = 252.0              # IEEE single-column width, points

# name -> (width, height) in points, as printed. Nothing is scaled in LaTeX.
SIZES = {
    "map_escape":        (156, 152),
    "map_saver":         (202, 100),
    "pair_idea":         (516, 138),
    "fig_coverage":      (239, 148),
    "fig_shap":          (239, 178),
    "fig_tradeoff":      (239, 142),
    "fig_concentration": (239, 150),
}


def size(name):
    """Figure size in inches, for the figure that prints as SIZES[name]."""
    w, h = SIZES[name]
    return w / 72.0, h / 72.0


def frac(name):
    """The \columnwidth fraction that reproduces SIZES[name] at 1:1."""
    return SIZES[name][0] / COL_PT


COL_W = 3.4                 # kept for anything not yet on the size table
COL_H = 2.35

# Natural Earth, from the cartopy cache already on this machine.
_NE = Path.home() / ".local/share/cartopy/shapefiles/natural_earth"
LAND_SHP = _NE / "physical/ne_10m_land.shp"
BORDER_SHP = _NE / "cultural/ne_50m_admin_0_boundary_lines_land.shp"
CRS_EU = "EPSG:3035"        # ETRS89-LAEA, the standard European equal-area grid


def apply() -> None:
    plt.rcParams.update({
        "font.family": "serif",
        # STIXGeneral is Times-metric and ships with matplotlib; Times New
        # Roman is not installed here and would fall back to DejaVu Serif.
        "font.serif": ["STIXGeneral", "DejaVu Serif"],
        "mathtext.fontset": "stix",
        "axes.labelsize": FS_LABEL,
        "axes.titlesize": FS_LABEL,
        "xtick.labelsize": FS_TICK,
        "ytick.labelsize": FS_TICK,
        "legend.fontsize": FS_ANNOT,
        "axes.edgecolor": INK,
        "axes.linewidth": 0.7,
        "xtick.color": INK,
        "ytick.color": INK,
        "xtick.major.width": 0.6,
        "ytick.major.width": 0.6,
        "xtick.major.size": 2.6,
        "ytick.major.size": 2.6,
        "text.color": INK,
        "axes.labelcolor": INK,
        # the doctrine frames a key faintly rather than floating it
        "legend.frameon": True,
        "legend.framealpha": 0.95,
        "legend.edgecolor": "#cccccc",
        "axes.titleweight": "bold",
        "lines.linewidth": 1.3,
        "grid.alpha": 0.15,
        "grid.linewidth": 0.5,
        "figure.dpi": 200,
        # never "tight": it changes the page size of the output, and these
        # figures are sized deliberately so that they need no scaling
        "savefig.bbox": "standard",
        "savefig.pad_inches": 0.0,
        "pdf.fonttype": 42,     # embed TrueType so the text stays selectable
        "ps.fonttype": 42,
    })


def save(fig, path) -> None:
    """Write a figure atomically, so a crash cannot leave half a PDF.

    matplotlib truncates the target the moment it opens it, so an
    interrupted render used to leave an unreadable file where a good figure
    had been, and LaTeX then failed on a figure nobody had touched. Render
    to a neighbouring temporary name and rename over the target instead:
    os.replace is atomic within a directory.
    """
    import os
    path = Path(path)
    # the temporary name keeps the .pdf suffix: matplotlib picks the writer
    # from the extension, and ".pdf.tmp" is not a format it knows
    tmp = path.with_name(f".{path.stem}.partial{path.suffix}")
    fig.savefig(tmp)
    os.replace(tmp, path)


def clean(ax, axis: str = "y") -> None:
    """Strip the chartjunk: no top/right spines, one light grid direction.

    Only the gridlines a reader needs to recover a value survive, and they
    are drawn light enough to sit behind the data rather than beside it.
    Pass axis="none" for panels where the annotation already gives the
    value and the grid would only add ruling.
    """
    ax.spines[["top", "right"]].set_visible(False)
    if axis != "none":
        ax.grid(axis=axis, color=INK, lw=0.5, alpha=0.15)
    ax.set_axisbelow(True)


def panel(ax, letter: str, text: str = "", pad: float = 2.5) -> None:
    """Panel letter in the same corner of every multi-panel figure.

    Written as a left-aligned title rather than free text in axes
    coordinates: constrained layout reserves room for titles, so the letter
    can never be clipped at the figure edge or land on the panel above,
    and it sits at the identical height in every panel of every figure.
    """
    label = f"({letter})" + (f"  {text}" if text else "")
    ax.set_title(label, loc="left", fontsize=FS_PANEL, color=INK, pad=pad)


def tag(ax, x, y, text, colour=INK, ha="left", va="center",
        size: float | None = None, halo_lw: float = 0.0, **kw):
    """A direct label in the plot area, legible over whatever it lands on.

    Direct labels replace a legend wherever the plot has room: the reader
    names the series where the series is, instead of matching swatches.

    halo_lw defaults to zero, and that default is deliberate. A path-effect
    outline makes matplotlib draw the label as vector outlines rather than
    as text, which costs the PDF its selectable, searchable and
    screen-reader-visible copy of the words. Pay that price only where the
    label really does land on busy geometry, as on the maps; on a clean
    axes background it buys nothing.
    """
    return ax.text(x, y, text, color=colour, ha=ha, va=va,
                   fontsize=size or FS_ANNOT, zorder=8,
                   path_effects=halo(halo_lw) if halo_lw > 0 else None, **kw)


def note(ax, text, xy, xytext, colour=INK, size: float | None = None,
         ha="center", va="center", **kw):
    """A plain-language reading of one point, on a hairline leader.

    Used where a single number carries the argument: saying it in words
    beats asking the reader to trace two axes back to it.
    """
    return ax.annotate(
        text, xy=xy, xytext=xytext, fontsize=size or FS_SMALL, color=colour,
        ha=ha, va=va, linespacing=1.32, zorder=8,
        arrowprops=dict(arrowstyle="-", color=colour, lw=0.6,
                        shrinkA=1.5, shrinkB=2.5,
                        connectionstyle="arc3,rad=0.0"), **kw)


def halo(lw: float = 2.4, colour: str = "white"):
    """A white outline under a line, so crossing routes stay separable.

    Returns a path_effects list. Without this, two routes that share most of
    their length render as one thick smear at column width.
    """
    return [pe.Stroke(linewidth=lw, foreground=colour), pe.Normal()]


def project(lons, lats):
    """Longitude/latitude to the European equal-area grid."""
    from pyproj import Transformer
    tr = Transformer.from_crs("EPSG:4326", CRS_EU, always_xy=True)
    return tr.transform(list(lons), list(lats))


def basemap(ax, bbox_lonlat, borders: bool = True) -> None:
    """Draw land, coast and (optionally) national boundaries into ax.

    bbox_lonlat is (west, south, east, north) in degrees.

    Two steps here are about file size, not looks. Reading with a bounding
    box returns whole features, and in the 10 m layer Eurasia is a single
    polygon, so the map carried the entire continent as invisible vector
    detail: the three maps alone made the PDF 16 MB. The geometry is
    therefore clipped to the window and then simplified to a tolerance of
    about half a printed pixel at 600 dpi, which is invisible at column
    width and cuts the figures to a few tens of kilobytes.
    """
    import geopandas as gpd
    from shapely.geometry import box

    ax.set_facecolor(SEA)
    # The clip window must be comfortably larger than the window the caller
    # asked for: the frame is grown to a target aspect after this runs, and
    # a clip drawn at the requested bounds leaves straight cuts across the
    # land inside the visible area. In LAEA those cuts are also slanted.
    w, s, e, n = bbox_lonlat
    gx, gy = (e - w) * 0.75, (n - s) * 0.75
    wide = (w - gx, s - gy, e + gx, n + gy)
    window = box(*wide)
    px, py = project([w, e], [s, n])
    tol = abs(px[1] - px[0]) / 1200.0     # ~half a pixel at final print size

    land = gpd.read_file(LAND_SHP, bbox=wide).clip(window).to_crs(CRS_EU)
    land = land[~land.is_empty]
    land.geometry = land.geometry.simplify(tol, preserve_topology=True)
    land.plot(ax=ax, color=LAND, edgecolor=COAST, linewidth=0.45, zorder=1)
    if borders and BORDER_SHP.exists():
        bd = gpd.read_file(BORDER_SHP, bbox=wide).clip(window).to_crs(CRS_EU)
        bd = bd[~bd.is_empty]
        bd.geometry = bd.geometry.simplify(tol, preserve_topology=True)
        bd.plot(ax=ax, color=BORDER, linewidth=0.35, zorder=2)


def frame(ax) -> None:
    """A hairline box around a map, and no ticks."""
    ax.set_xticks([])
    ax.set_yticks([])
    for s in ax.spines.values():
        s.set_edgecolor(COAST)
        s.set_linewidth(0.6)


def endpoint(ax, x, y, z: int = 6):
    ax.plot(x, y, "o", ms=4.4, mfc="white", mec=INK, mew=1.1, zorder=z,
            clip_on=False)
