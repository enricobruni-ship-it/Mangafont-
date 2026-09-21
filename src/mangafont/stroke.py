"""Brush-stroke engine.

A glyph is a set of *strokes*, exactly as a kanji is.  Each stroke is a
centreline (the path the brush tip travels) plus a *pressure profile*
(how hard the brush presses along that path) plus *terminal angles*.
Rendering offsets the centreline by half the local width to produce one
closed, clockwise contour per stroke.

Strokes are never booleaned together: they are simply stacked as
same-winding contours and the non-zero fill rule unions them.  Counters
(the hole in `o`, `B`, `8`) are therefore just regions that no stroke
covers -- which is exactly how a CJK glyph's counters come about.
"""

import math

from .weights import DISPLAY

# ---------------------------------------------------------------- vectors

def _sub(a, b):  return (a[0] - b[0], a[1] - b[1])
def _add(a, b):  return (a[0] + b[0], a[1] + b[1])
def _mul(a, s):  return (a[0] * s, a[1] * s)
def _dot(a, b):  return a[0] * b[0] + a[1] * b[1]
def _hyp(a):     return math.hypot(a[0], a[1])
def _perp(a):    return (-a[1], a[0])


def _unit(a):
    n = _hyp(a)
    return (a[0] / n, a[1] / n) if n > 1e-9 else (0.0, 0.0)


# --------------------------------------------------------------- profiles
#
# Keyframes are (normalised arc length, width multiplier).  The names are
# the Japanese calligraphic terms for the stroke shapes they describe.

PROFILES = {
    # flat ribbon, no modulation
    "uniform":   [(0.00, 1.00), (1.00, 1.00)],

    # 横画 -- the horizontal.  In Mincho this is a HAIRLINE: roughly a
    # third the weight of a stem.  It lands with a heavy angled press
    # (起筆), runs thin, and thickens into the stop that carries the
    # uroko.  The press is what keeps a 40-unit stroke from looking weak.
    "yoko":      [(0.00, 1.55), (0.10, 0.94), (0.48, 0.86),
                  (0.84, 0.98), (1.00, 1.28)],

    # a horizontal that dies into a stem (an inner bar of 目, the left
    # end of a crossbar) -- pressed entry, no swollen stop.
    "yoko_in":   [(0.00, 1.50), (0.11, 0.94), (0.60, 0.88), (1.00, 0.94)],

    # 縦画 -- the vertical.  Heavy and near-even; the head flares (起筆)
    # and the foot swells into the 垂露 stop.
    "tate":      [(0.00, 1.34), (0.07, 1.01), (0.55, 0.95),
                  (0.90, 1.02), (1.00, 1.12)],

    # 懸針 -- a vertical that runs off to a needle point.
    "tate_tail": [(0.00, 1.34), (0.08, 1.02), (0.50, 0.92),
                  (0.80, 0.58), (1.00, 0.04)],

    # はね -- the flick.  The taper is late and abrupt, so the hook
    # reads as a spike rather than a fade.
    "hane":      [(0.00, 1.34), (0.07, 1.01), (0.62, 0.96),
                  (0.84, 0.86), (0.94, 0.44), (1.00, 0.03)],

    # 左払い -- sweep down-left, pressing early, gone to a point.
    "harai_l":   [(0.00, 1.20), (0.16, 1.06), (0.46, 0.84),
                  (0.72, 0.54), (0.90, 0.24), (1.00, 0.02)],

    # 右払い -- sweep down-right, entering thin, pressing into a stop.
    "harai_r":   [(0.00, 0.16), (0.24, 0.48), (0.60, 0.82),
                  (0.90, 1.16), (1.00, 1.22)],

    # 点 -- the tick: a teardrop that swells as the brush lands.
    "ten":       [(0.00, 0.16), (0.42, 0.86), (0.82, 1.28), (1.00, 1.42)],

    # diagonals that meet at a vertex (A, V, W, M, Y).
    "diag":      [(0.00, 1.12), (0.55, 0.92), (1.00, 0.42)],

    # 払い, katakana length.  The signature stroke of ノ ソ ク ス メ:
    # presses early, then runs a long way out to a needle point.  Much
    # more dramatic than the kanji sweep, because katakana have so few
    # strokes that each one has to carry the character.
    "sweep":     [(0.00, 1.06), (0.12, 1.14), (0.40, 0.94),
                  (0.66, 0.62), (0.87, 0.26), (1.00, 0.02)],

    # the rising stroke of シ ン ミ: enters thin at the foot, presses as
    # it climbs, flicks off at the top.
    "nobi":      [(0.00, 0.20), (0.40, 0.72), (0.80, 1.10),
                  (0.93, 0.80), (1.00, 0.08)],

    # an angular sweep entering thin off a previous stroke and finishing
    # in a flick -- S, s, e, 2, 3.
    "sori":      [(0.00, 0.30), (0.09, 0.98), (0.42, 0.82),
                  (0.72, 0.94), (0.90, 0.60), (1.00, 0.03)],
}

# The active cut.  Glyph sources are drawn once, in the units of the
# reference cut; the Weight carries every stroke into the current one.
ACTIVE = DISPLAY


def set_weight(w):
    """Switch the cut every subsequent Stroke is built in."""
    global ACTIVE
    ACTIVE = w


def w_of(width):
    """A reference-unit width, in the active cut -- for positioning."""
    return ACTIVE.remap(width)

MIN_WIDTH = 5.0      # never let a ribbon collapse to nothing
MITER_LIMIT = 3.2


def profile_at(keys, t):
    """Linear interpolation through a keyframe list."""
    if t <= keys[0][0]:
        return keys[0][1]
    for i in range(1, len(keys)):
        t0, v0 = keys[i - 1]
        t1, v1 = keys[i]
        if t <= t1:
            f = 0.0 if t1 - t0 < 1e-9 else (t - t0) / (t1 - t0)
            return v0 + (v1 - v0) * f
    return keys[-1][1]


# --------------------------------------------------------------- flatten

def flatten(cmds, flatness=7.0):
    """Turn a path description into a dense polyline.

    Commands: ("M", x, y) ("L", x, y) ("Q", cx, cy, x, y)
              ("C", c1x, c1y, c2x, c2y, x, y)
    """
    pts, cur = [], None
    for c in cmds:
        op = c[0]
        if op == "M":
            cur = (c[1], c[2])
            pts.append(cur)
        elif op == "L":
            p = (c[1], c[2])
            # Straight runs are subdivided too, so that the pressure
            # profile has somewhere to modulate.
            n = max(2, min(40, int(_hyp(_sub(p, cur)) / flatness)))
            for i in range(1, n + 1):
                t = i / n
                pts.append((cur[0] + (p[0] - cur[0]) * t,
                            cur[1] + (p[1] - cur[1]) * t))
            cur = p
        elif op == "Q":
            c1, p = (c[1], c[2]), (c[3], c[4])
            span = _hyp(_sub(c1, cur)) + _hyp(_sub(p, c1))
            n = max(5, min(56, int(span / flatness)))
            for i in range(1, n + 1):
                t = i / n
                m = 1.0 - t
                pts.append((m * m * cur[0] + 2 * m * t * c1[0] + t * t * p[0],
                            m * m * cur[1] + 2 * m * t * c1[1] + t * t * p[1]))
            cur = p
        elif op == "C":
            c1, c2, p = (c[1], c[2]), (c[3], c[4]), (c[5], c[6])
            span = (_hyp(_sub(c1, cur)) + _hyp(_sub(c2, c1))
                    + _hyp(_sub(p, c2)))
            n = max(6, min(64, int(span / flatness)))
            for i in range(1, n + 1):
                t = i / n
                m = 1.0 - t
                pts.append((m**3 * cur[0] + 3 * m * m * t * c1[0]
                            + 3 * m * t * t * c2[0] + t**3 * p[0],
                            m**3 * cur[1] + 3 * m * m * t * c1[1]
                            + 3 * m * t * t * c2[1] + t**3 * p[1]))
            cur = p
        else:
            raise ValueError("unknown path op %r" % (op,))

    out = [pts[0]]
    for p in pts[1:]:
        if _hyp(_sub(p, out[-1])) > 1e-6:
            out.append(p)
    if len(out) < 2:
        raise ValueError("degenerate path")
    return out


def arc_params(pts):
    """Normalised cumulative arc length for each polyline vertex."""
    acc, total = [0.0], 0.0
    for i in range(1, len(pts)):
        total += _hyp(_sub(pts[i], pts[i - 1]))
        acc.append(total)
    if total < 1e-9:
        return [0.0] * len(pts)
    return [a / total for a in acc]


# ---------------------------------------------------------------- ribbon

def ribbon(pts, widths, cap_start=0.0, cap_end=0.0):
    """Offset a polyline into a closed clockwise contour."""
    n = len(pts)
    dirs = [_unit(_sub(pts[i + 1], pts[i])) for i in range(n - 1)]

    left, right = [], []
    for i in range(n):
        d_in = dirs[i - 1] if i > 0 else dirs[0]
        d_out = dirs[i] if i < n - 1 else dirs[-1]
        n_in, n_out = _perp(d_in), _perp(d_out)
        bis = _add(n_in, n_out)
        h = max(widths[i], MIN_WIDTH) * 0.5
        if _hyp(bis) < 1e-6:                 # 180 degree reversal
            left.append(_add(pts[i], _mul(n_in, h)))
            right.append(_sub(pts[i], _mul(n_in, h)))
            continue
        bis = _unit(bis)
        cosang = max(_dot(bis, n_in), 1e-3)
        s = h / cosang
        if s <= h * MITER_LIMIT:             # miter join
            left.append(_add(pts[i], _mul(bis, s)))
            right.append(_sub(pts[i], _mul(bis, s)))
        else:                                # bevel join
            left.append(_add(pts[i], _mul(n_in, h)))
            left.append(_add(pts[i], _mul(n_out, h)))
            right.append(_sub(pts[i], _mul(n_in, h)))
            right.append(_sub(pts[i], _mul(n_out, h)))

    # Terminal shear: slides one flank forward and the other back so the
    # cut across the stroke end is oblique, the way a brush leaves it.
    if abs(cap_start) > 1e-6:
        k = max(widths[0], MIN_WIDTH) * 0.5 * math.tan(math.radians(cap_start))
        left[0] = _add(left[0], _mul(dirs[0], k))
        right[0] = _sub(right[0], _mul(dirs[0], k))
    if abs(cap_end) > 1e-6:
        k = max(widths[-1], MIN_WIDTH) * 0.5 * math.tan(math.radians(cap_end))
        left[-1] = _add(left[-1], _mul(dirs[-1], k))
        right[-1] = _sub(right[-1], _mul(dirs[-1], k))

    return left + right[::-1]


# ------------------------------------------------------------- simplify

def _perp_dist(p, a, b):
    d = _sub(b, a)
    L = _hyp(d)
    if L < 1e-9:
        return _hyp(_sub(p, a))
    return abs(d[0] * (a[1] - p[1]) - d[1] * (a[0] - p[0])) / L


def simplify(pts, tol=1.6):
    """Ramer-Douglas-Peucker, to keep the point count sane."""
    if len(pts) < 3:
        return list(pts)
    keep = [False] * len(pts)
    keep[0] = keep[-1] = True
    stack = [(0, len(pts) - 1)]
    while stack:
        i, j = stack.pop()
        if j <= i + 1:
            continue
        worst, wi = -1.0, i
        for k in range(i + 1, j):
            d = _perp_dist(pts[k], pts[i], pts[j])
            if d > worst:
                worst, wi = d, k
        if worst > tol:
            keep[wi] = True
            stack.append((i, wi))
            stack.append((wi, j))
    return [p for p, k in zip(pts, keep) if k]


def signed_area(pts):
    a = 0.0
    for i in range(len(pts)):
        x0, y0 = pts[i]
        x1, y1 = pts[(i + 1) % len(pts)]
        a += x0 * y1 - x1 * y0
    return a * 0.5


def dedupe_closed(pts, eps=0.9):
    out = [pts[0]]
    for p in pts[1:]:
        if _hyp(_sub(p, out[-1])) > eps:
            out.append(p)
    while len(out) > 3 and _hyp(_sub(out[0], out[-1])) <= eps:
        out.pop()
    return out


# ---------------------------------------------------------- ornaments
#
# Mincho terminals are separate wedges of ink, not fattened stroke ends.
# They are sized in ABSOLUTE font units: a 40-unit hairline has to carry
# the same 55-unit uroko as anything else, so scaling the ornament off
# the stroke's own width -- which is what the first version did -- makes
# it vanish exactly where it matters most.

class Poly:
    """A bare polygon, used for the terminal ornaments."""

    def __init__(self, pts):
        self.pts = list(pts)

    def contours(self, tol=1.6):
        pts = list(self.pts)
        if signed_area(pts) > 0:
            pts.reverse()
        return [pts]


def uroko(pt, tangent, normal, h, rise, run):
    """うろこ -- the scale: the fin a brush leaves at the stop of a 横画.

    A right triangle sitting on the stroke: its upright edge at the very
    end, its hypotenuse sloping back down along the top of the stroke.
    """
    tip = _add(pt, _mul(normal, h - 2.0))
    peak = _add(tip, _mul(normal, rise))
    tail = _sub(tip, _mul(tangent, run))
    return Poly([tail, peak, tip])


def kata(x, y, wt, rise=None, drop=None):
    """肩 -- the shoulder at a 折れ, where a horizontal turns down into a
    stem.  In 口 and 日 this corner is peaked, not mitred: a small
    triangle rising to the outer edge of the stem."""
    k = ACTIVE.orn_scale
    rise = 34 * k if rise is None else rise
    drop = 30 * k if drop is None else drop
    half = ACTIVE.remap(wt) * 0.5
    return Poly([(x - half - 8, y + 1),
                 (x + half + 2, y + rise),
                 (x + half + 2, y - drop)])


def kihitsu(x, y, wt, out=None, rise=None, drop=None):
    """起筆 -- the flared head of a 縦画: the brush lands from the upper
    left, so the stem wears a small slanted hat on that side."""
    k = ACTIVE.orn_scale
    out = 26 * k if out is None else out
    rise = 22 * k if rise is None else rise
    drop = 20 * k if drop is None else drop
    half = ACTIVE.remap(wt) * 0.5
    return Poly([(x - half - out, y + rise * 0.30),
                 (x - half + 6, y + rise),
                 (x + half, y + rise * 0.42),
                 (x + half, y - drop),
                 (x - half, y - drop * 0.4)])


# ----------------------------------------------------------------- Stroke

# Terminal flags per stroke family, in absolute units: (rise, run).
_UROKO_END = {"yoko": (36, 84)}
_UROKO_START = {}


class Stroke:
    """One brush stroke: centreline + pressure profile + terminals."""

    def __init__(self, path, width, profile="tate",
                 cap_start=None, cap_end=None, uroko_end=None,
                 uroko_start=None, scale=1.0, modulated=True,
                 overshoot=True):
        self.path = path
        self.overshoot = overshoot
        # A profile normally describes brush PRESSURE, which the heavier
        # and text cuts damp via the weight's gain.  A few strokes use the
        # same mechanism to describe GEOMETRY instead -- a corner
        # connector that must land on a hairline at one end and a stem at
        # the other.  Damping those corrupts the joint, so they opt out.
        self.modulated = modulated
        self.width = ACTIVE.remap(width * scale)
        self.profile = (PROFILES[profile] if isinstance(profile, str)
                        else profile)
        name = profile if isinstance(profile, str) else ""
        if cap_start is None:
            cap_start = {"yoko": -20.0, "yoko_in": -20.0, "tate": -16.0,
                         "tate_tail": -20.0, "hane": -20.0,
                         "harai_l": -26.0, "ten": -24.0}.get(name, 0.0)
        if cap_end is None:
            cap_end = {"yoko": -10.0, "harai_r": -32.0,
                       "ten": 26.0}.get(name, 0.0)
        self.cap_start = cap_start
        self.cap_end = cap_end
        self.uroko_end = (_UROKO_END.get(name) if uroko_end is None
                          else uroko_end)
        self.uroko_start = (_UROKO_START.get(name) if uroko_start is None
                            else uroko_start)

    def contours(self, tol=1.6):
        pts = flatten(self.path)
        over = getattr(ACTIVE, "overshoot", 0.0)
        if over and len(pts) > 1 and self.overshoot:
            d0 = _unit(_sub(pts[0], pts[1]))
            d1 = _unit(_sub(pts[-1], pts[-2]))
            pts = ([_add(pts[0], _mul(d0, over))] + pts
                   + [_add(pts[-1], _mul(d1, over))])
        ts = arc_params(pts)
        gain = ACTIVE.gain if self.modulated else 1.0
        widths = [self.width * (1.0 + (profile_at(self.profile, t) - 1.0) * gain)
                  for t in ts]
        body = dedupe_closed(simplify(
            ribbon(pts, widths, self.cap_start, self.cap_end), tol))
        if signed_area(body) > 0:         # TrueType wants clockwise outers
            body.reverse()
        out = [body]

        # A flag only belongs where the brush was actually travelling
        # along a horizontal.
        if self.uroko_end and self.uroko_end[0]:
            d = _unit(_sub(pts[-1], pts[-2]))
            if d[0] > 0.90:
                rise, run = self.uroko_end
                k = ACTIVE.orn_scale
                h = max(widths[-1], MIN_WIDTH) * 0.5
                out.extend(uroko(pts[-1], d, _perp(d), h, rise * k, run * k)
                           .contours(tol))
        return out

    def contour(self, tol=1.6):
        return self.contours(tol)[0]


def bow(p0, p1, amount=0.055):
    """A straight run, bent into a brush curve.

    Hiragana are cursive -- derived from 草書 -- so nothing in them is
    dead straight.  The control point is pushed to the RIGHT of travel,
    which is the way a 払い actually falls: it leaves steeply and only
    sweeps outward near the end.
    """
    d = _sub(p1, p0)
    n = _perp(_unit(d))
    mid = _mul(_add(p0, p1), 0.5)
    c = _add(mid, _mul(n, _hyp(d) * amount))
    return [("M", p0[0], p0[1]), ("Q", c[0], c[1], p1[0], p1[1])]


def round_corners(path, r):
    """Turn the hard corners inside one stroke into curves.

    This is the し / つ / り gesture: where katakana turns a corner,
    hiragana rounds it.  It deliberately touches only corners WITHIN a
    stroke -- the structural 肩 of a 折れ is built from two separate
    strokes, so it stays as sharp as katakana wants it.
    """
    pts = [(path[0][1], path[0][2])]
    for c in path[1:]:
        if c[0] != "L":
            return path                  # leave anything already curved
        pts.append((c[1], c[2]))
    if len(pts) < 3:
        return path

    out = [("M", pts[0][0], pts[0][1])]
    for i in range(1, len(pts) - 1):
        a, b, c = pts[i - 1], pts[i], pts[i + 1]
        d1, d2 = _hyp(_sub(b, a)), _hyp(_sub(b, c))
        if d1 < 1e-6 or d2 < 1e-6:
            continue
        t = min(r, d1 * 0.45, d2 * 0.45)
        p_in = _add(b, _mul(_unit(_sub(a, b)), t))
        p_out = _add(b, _mul(_unit(_sub(c, b)), t))
        out.append(("L", p_in[0], p_in[1]))
        out.append(("Q", b[0], b[1], p_out[0], p_out[1]))
    out.append(("L", pts[-1][0], pts[-1][1]))
    return out


def curl_tip(path, amount=0.20):
    """Bend the last segment so the flick curls over instead of firing
    off straight -- the way し, り and つ finish."""
    if len(path) < 2 or path[-1][0] != "L":
        return path
    end = (path[-1][1], path[-1][2])
    prev_cmd = path[-2]
    prev = (prev_cmd[-2], prev_cmd[-1])
    d = _sub(end, prev)
    if _hyp(d) < 1e-6:
        return path
    mid = _mul(_add(prev, end), 0.5)
    c = _add(mid, _mul(_perp(_unit(d)), _hyp(d) * amount))
    return path[:-1] + [("Q", c[0], c[1], end[0], end[1])]


def transform(items, sx=1.0, sy=1.0, dx=0.0, dy=0.0, wmul=1.0):
    """Scale and shift a set of strokes.

    Used to derive the small kana (ァィゥェォッャュョ) from their full-size
    forms.  Stroke weight is scaled separately and much less than the
    geometry, because a small kana that thinned proportionally would look
    like a different, lighter font sitting inside the line -- real
    families keep small kana nearly full weight.
    """
    import copy as _copy
    out = []
    for item in items:
        if isinstance(item, Poly):
            out.append(Poly([(x * sx + dx, y * sy + dy) for x, y in item.pts]))
            continue
        path = []
        for cmd in item.path:
            nums = list(cmd[1:])
            for i in range(0, len(nums), 2):
                nums[i] = nums[i] * sx + dx
                nums[i + 1] = nums[i + 1] * sy + dy
            path.append((cmd[0],) + tuple(nums))
        clone = _copy.copy(item)
        clone.path = path
        clone.width = item.width * wmul
        out.append(clone)
    return out


def contours(items, tol=1.6):
    """Flatten strokes and ornaments alike into a list of contours."""
    out = []
    for item in items:
        out.extend(item.contours(tol))
    return out
