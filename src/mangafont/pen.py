"""Shared drawing vocabulary: metrics, and the strokes every glyph is
spelled out of.

Kept apart from the glyph sets so that both the Latin (glyphs.py) and the
kana (katakana.py) can build on it without importing each other.
"""

from .stroke import (Stroke, kata, kihitsu, w_of, transform,      # noqa: F401
                     bow, round_corners, curl_tip)

# ------------------------------------------------------------- metrics

UPM = 1000
CAP = 790          # cap height / figure height
XH = 600           # x-height -- 0.76 of cap, so lowercase fills a square
ASC = 858
DESC = -238        # descenders: shallow ones read as runic
ASCENDER = 900
DESCENDER = -300

WT = 104           # 縦画  the stem
WY = 46            # 横画  the hairline -- 0.44 of the stem
WD = 84            # 払い  the sweep
WC = 70            # corner connectors

RISE = 0.030       # horizontals climb ~1.7 degrees to the right

# How far the first stroke of n / m / r / u rises above its own shoulder.
# Stopping it flush with the arch gives a squat 冂 with nothing to
# distinguish stem from bar, which is most of what reads as runic.
SPUR = 88

L, R = 64, 700     # the character face
ADV = 768


# ----------------------------------------------------------- shorthands

# How much of a heavy cut's extra stroke weight is allowed to eat into
# the counter rather than spilling outside the frame.
BLEED = 0.30


def wall(wt=WT):
    """Half-width to position a bowl's wall by.

    Anchoring a stem by its OUTER edge marches it inward as weight rises,
    so the counter closes: at display weight the lowercase a and e shut
    completely.  Position by the REFERENCE width instead and let the
    extra ink spill outside the frame -- which is what a separately drawn
    bold master does, and why a real bold is not a fattened regular.
    """
    return wt * 0.5 + (w_of(wt) - wt) * 0.5 * BLEED


def yoko(x0, x1, y, w=WY, prof="yoko", flag=True):
    """横画 -- a hairline horizontal climbing to the right.

    `flag` is the うろこ at the stop.  It is switched off wherever the
    stroke turns down into a stem, because that corner wears a 肩
    instead; carrying both stacks two ornaments on one corner.
    """
    return Stroke([("M", x0, y), ("L", x1, y + (x1 - x0) * RISE)], w, prof,
                  uroko_end=None if flag else (0, 0))


def yoko_in(x0, x1, y, w=WY):
    """A horizontal that dies into a stem: pressed entry, no うろこ."""
    return yoko(x0, x1, y, w, "yoko_in")


def tate(x, ytop, ybot, w=WT, prof="tate", drift=-5, head=True):
    """縦画 -- a stem, with its flared 起筆 head."""
    out = [Stroke([("M", x, ytop), ("L", x + drift, ybot)], w, prof)]
    if head:
        out.append(kihitsu(x, ytop, w))
    return out


def fold(x0, x1, ytop, ybot, wt=WT, wy=WY):
    """横折 -- a horizontal turning down into a stem, carrying its 肩.

    Rendered as two strokes because the two halves are different
    weights: that weight change across the corner is the whole point.
    """
    rx = x1 - wall(wt)
    rise = (x1 - x0) * RISE
    return ([yoko(x0, x1, ytop, wy, flag=False)]
            + tate(rx, ytop + rise, ybot, wt, head=False)
            + [kata(rx, ytop + rise, wt)])


def box(x0, x1, ybot, ytop, wt=WT, wy=WY):
    """口 -- three strokes: left 竖, 横折, bottom 横."""
    return (tate(x0 + wall(wt), ytop, ybot, wt)
            + fold(x0, x1, ytop, ybot, wt, wy)
            + [yoko(x0, x1, ybot, wy)])


# On a cut corner no stroke actually begins, so the ring's bars and stems
# must not wear a 起筆 press or an end swell there -- that wedge is what
# shows up as a nub poking off each chamfer.
FLAT = [(0.00, 0.97), (0.50, 0.93), (1.00, 0.99)]


def ring(x0, x1, ybot, ytop, wt=WT, wy=WY, cx=0.20, cy=0.15):
    """A 口 with its corners cut, for O / o / 0 / 8."""
    dx = (x1 - x0) * cx
    dy = (ytop - ybot) * cy
    lx, rx = x0 + wall(wt), x1 - wall(wt)
    out = []
    out += tate(lx, ytop - dy, ybot + dy, wt, FLAT, head=False)
    out += tate(rx, ytop - dy + 8, ybot + dy, wt, FLAT, head=False)
    rise = (x1 - x0 - 2 * dx) * RISE
    for y in (ytop, ybot):
        out.append(Stroke([("M", x0 + dx, y), ("L", x1 - dx, y + rise)],
                          wy, FLAT, cap_start=0.0, cap_end=0.0,
                          uroko_end=(0, 0)))
    taper = [(0.0, w_of(wy) / w_of(wt)), (1.0, 1.0)]
    for a, b in (((x0 + dx + 10, ytop), (lx, ytop - dy - 12)),
                 ((x1 - dx - 10, ytop + rise), (rx, ytop - dy - 12)),
                 ((x0 + dx + 10, ybot), (lx, ybot + dy + 12)),
                 ((x1 - dx - 10, ybot + rise), (rx, ybot + dy + 12))):
        out.append(Stroke([("M", a[0], a[1]), ("L", b[0], b[1])],
                          wt, taper, modulated=False))
    return out


def fusweep(x0, x1, ytop, xend, yend, wy=WY, ws=WD, wt=WT, amount=None):
    """フ -- a hairline horizontal that turns a hard corner and sweeps
    away down-left to a point.

    The commonest gesture in katakana: フ ア ク ス ヌ マ ワ ラ ヲ タ all
    turn on it.  Built as three pieces because the weight changes across
    the corner -- hairline in, 肩 at the knee, sweep out.
    """
    rise = (x1 - x0) * RISE
    cx = x1 - wall(wt)
    return [yoko(x0, x1, ytop, wy, flag=False),
            kata(cx, ytop + rise, wt),
            Stroke(bow((cx, ytop + rise), (xend, yend),
                       BOW if amount is None else amount), ws, "sweep")]


# How much hiragana is let into the katakana structure.  These are the
# only three knobs: a bow on the long sweeps, rounded corners inside a
# stroke, and a curl on the flick.
BOW = 0.052        # 払い bend
CURVE = 78         # radius of a rounded corner within a stroke
CURL = 0.19        # how far a はね turns back on itself


def sweep(p0, p1, w=WD, amount=BOW):
    """払い at katakana length -- ノ -- bent like a hiragana stroke."""
    return Stroke(bow(p0, p1, amount), w, "sweep")


def nobi(p0, p1, w=WD):
    """The rising stroke of シ ン: thin at the foot, flicking off the top."""
    return Stroke([("M", p0[0], p0[1]), ("L", p1[0], p1[1])], w, "nobi")


def harai_l(p0, p1, w=WD):
    """左払い -- the sweep down to the left."""
    return Stroke([("M", p0[0], p0[1]), ("L", p1[0], p1[1])], w, "harai_l")


def harai_r(p0, p1, w=WD):
    """右払い -- the sweep down to the right."""
    return Stroke([("M", p0[0], p0[1]), ("L", p1[0], p1[1])], w, "harai_r")


def ten(x, y, dx=86, dy=-92, w=76):
    """点 -- the tick."""
    return Stroke([("M", x, y), ("L", x + dx, y + dy)], w, "ten")


def hane(path, w=WT, r=CURVE, curl=CURL):
    """A stroke that rounds its corners and curls off at the tip.

    Where the katakana version turned a corner and fired straight away,
    this rolls through the turn and lets the flick curve back -- which is
    the difference between レ and し.
    """
    return Stroke(curl_tip(round_corners(path, r), curl), w, "hane")


