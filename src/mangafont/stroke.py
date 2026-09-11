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

    # 横画 -- horizontal.  Angled press at the entry (起筆), a thin waist,
    # then a swell into the blunt stop (終筆).
    "yoko":      [(0.00, 1.26), (0.09, 0.92), (0.46, 0.80),
                  (0.80, 0.92), (0.94, 1.16), (1.00, 1.24)],

    # 縦画 -- vertical, ending in a blunt 垂露 stop.
    "tate":      [(0.00, 1.26), (0.09, 0.99), (0.55, 0.90),
                  (0.88, 1.00), (1.00, 1.10)],

    # 懸針 -- vertical that tapers off the page to a needle point.
    "tate_tail": [(0.00, 1.34), (0.10, 1.02), (0.55, 0.90),
                  (0.84, 0.52), (1.00, 0.04)],

    # はね -- any stroke finishing in an upward flick.
    "hane":      [(0.00, 1.30), (0.09, 0.99), (0.58, 0.94),
                  (0.80, 0.86), (0.93, 0.46), (1.00, 0.04)],

    # 左払い -- sweep down to the left, thick to a point.
    "harai_l":   [(0.00, 1.28), (0.18, 1.02), (0.55, 0.70),
                  (0.82, 0.38), (1.00, 0.03)],

    # 右払い -- sweep down to the right, thin then pressing into a stop.
    "harai_r":   [(0.00, 0.22), (0.22, 0.52), (0.58, 0.84),
                  (0.88, 1.14), (1.00, 1.20)],

    # 点 -- the dot/tick, a teardrop that grows as the brush lands.
    "ten":       [(0.00, 0.20), (0.40, 0.88), (0.80, 1.26), (1.00, 1.38)],

    # 折れ -- a stroke that turns a corner (top + side of 口).
    "ore":       [(0.00, 1.26), (0.09, 0.94), (0.45, 0.88),
                  (0.80, 0.94), (1.00, 1.10)],

    # 折れ launched off an existing stem (the shoulder of n/m/h/r).  It
    # starts *inside* another stroke, so it gets no entry press and no
    # flag -- either would poke out sideways into white space.
    "arch":      [(0.00, 0.96), (0.25, 0.90), (0.60, 0.88),
                  (0.85, 0.96), (1.00, 1.10)],

    # diagonals of A/V/W/M: press at the top, relax towards the vertex.
    "diag":      [(0.00, 1.10), (0.60, 0.92), (1.00, 0.48)],

    # a stroke that enters thin (picking up from a previous stroke) and
    # finishes in a flick -- used for S/s/e.
    "sori":      [(0.00, 0.38), (0.10, 0.98), (0.40, 0.80),
                  (0.70, 0.92), (0.90, 0.66), (1.00, 0.04)],
}

# Global weight knob.  Glyph sources quote widths in "design units at
# weight 1.0"; this scales the whole family at once.
WEIGHT = 1.46

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


# ------------------------------------------------------------- uroko
#
# うろこ ("scale") -- the little triangular flag a brush leaves when it
# lifts.  On a 横画 it sits above the right-hand stop; on a 縦画 it sits
# at the top of the entry.  It is the single loudest Mincho/kanji cue,
# so it gets its own contour rather than being faked in the profile.

def uroko(pt, tangent, normal, h, bump, run, forward=True):
    tip = _add(pt, _mul(normal, h))
    lean = run * 0.30
    if forward:
        peak = _add(_add(tip, _mul(normal, bump)), _mul(tangent, lean))
        tail = _add(tip, _mul(tangent, run))
        tri = [tip, peak, tail]
    else:
        peak = _sub(_add(tip, _mul(normal, bump)), _mul(tangent, lean))
        tail = _sub(tip, _mul(tangent, run))
        tri = [tail, peak, tip]
    if signed_area(tri) > 0:
        tri.reverse()
    return tri


# ----------------------------------------------------------------- Stroke

# Which stroke families carry which terminal flags by default.
_UROKO_END = {"yoko": (0.42, 1.45), "ore": (0.42, 1.45)}
_UROKO_START = {"tate": (0.26, 1.05), "tate_tail": (0.26, 1.05),
                "hane": (0.26, 1.05), "ore": (0.34, 1.20)}


class Stroke:
    """One brush stroke: centreline + pressure profile + terminals."""

    def __init__(self, path, width, profile="tate",
                 cap_start=None, cap_end=None, uroko_end=None,
                 uroko_start=None, scale=1.0):
        self.path = path
        self.width = width * scale * WEIGHT
        self.profile = (PROFILES[profile] if isinstance(profile, str)
                        else profile)
        name = profile if isinstance(profile, str) else ""
        # Sensible default terminal shears per stroke family.
        if cap_start is None:
            cap_start = {"yoko": -26.0, "ore": -26.0, "tate": -16.0,
                         "tate_tail": -16.0, "hane": -16.0,
                         "harai_l": -24.0, "ten": -22.0}.get(name, 0.0)
        if cap_end is None:
            cap_end = {"yoko": -12.0, "harai_r": -30.0,
                       "ten": 24.0}.get(name, 0.0)
        self.cap_start = cap_start
        self.cap_end = cap_end
        self.uroko_end = (_UROKO_END.get(name) if uroko_end is None
                          else uroko_end)
        self.uroko_start = (_UROKO_START.get(name) if uroko_start is None
                            else uroko_start)

    def contours(self, tol=1.6):
        pts = flatten(self.path)
        ts = arc_params(pts)
        widths = [self.width * profile_at(self.profile, t) for t in ts]
        body = dedupe_closed(simplify(
            ribbon(pts, widths, self.cap_start, self.cap_end), tol))
        if signed_area(body) > 0:         # TrueType wants clockwise outers
            body.reverse()
        out = [body]

        # A flag only belongs where the brush was actually travelling
        # along a horizontal (the 横画 stop) or straight down (the 縦画
        # entry).  An arch that launches upwards, as in n/m/h/r, would
        # otherwise sprout a barb into empty space.
        if self.uroko_end:
            d = _unit(_sub(pts[-1], pts[-2]))
            if d[0] > 0.90:
                bump, run = self.uroko_end
                h = max(widths[-1], MIN_WIDTH) * 0.5
                out.append(uroko(pts[-1], d, _perp(d), h,
                                 h * bump, h * run, forward=False))
        if self.uroko_start:
            d = _unit(_sub(pts[1], pts[0]))
            if d[0] > 0.90 or d[1] < -0.90:
                bump, run = self.uroko_start
                h = max(widths[0], MIN_WIDTH) * 0.5
                out.append(uroko(pts[0], d, _perp(d), h,
                                 h * bump, h * run, forward=True))
        return out

    # Back-compat single-contour accessor (body only).
    def contour(self, tol=1.6):
        return self.contours(tol)[0]


def contours(strokes, tol=1.6):
    out = []
    for s in strokes:
        out.extend(s.contours(tol))
    return out
