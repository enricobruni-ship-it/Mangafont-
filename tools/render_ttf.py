"""Render text from a compiled .ttf -- an independent check on the file
that actually ships, not on the source skeletons."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))

from fontTools.ttLib import TTFont
from fontTools.pens.basePen import BasePen
import preview


class FlattenPen(BasePen):
    """Collect closed polygons, subdividing curves."""

    def __init__(self, glyphSet, steps=12):
        super().__init__(glyphSet)
        self.polys, self.cur, self.steps = [], [], steps

    def _moveTo(self, pt):
        self.cur = [pt]

    def _lineTo(self, pt):
        self.cur.append(pt)

    def _curveToOne(self, c1, c2, p):
        s = self._getCurrentPoint()
        for i in range(1, self.steps + 1):
            t = i / self.steps
            m = 1 - t
            self.cur.append((
                m**3 * s[0] + 3 * m * m * t * c1[0] + 3 * m * t * t * c2[0] + t**3 * p[0],
                m**3 * s[1] + 3 * m * m * t * c1[1] + 3 * m * t * t * c2[1] + t**3 * p[1]))

    def _qCurveToOne(self, c, p):
        s = self._getCurrentPoint()
        for i in range(1, self.steps + 1):
            t = i / self.steps
            m = 1 - t
            self.cur.append((m * m * s[0] + 2 * m * t * c[0] + t * t * p[0],
                             m * m * s[1] + 2 * m * t * c[1] + t * t * p[1]))

    def _closePath(self):
        if len(self.cur) > 2:
            self.polys.append(self.cur)
        self.cur = []

    _endPath = _closePath


def render(ttf_path, text, out, size=120, pad=30):
    font = TTFont(ttf_path)
    gs = font.getGlyphSet()
    cmap = font.getBestCmap()
    hmtx = font["hmtx"]
    upm = font["head"].unitsPerEm
    scale = size / upm

    items, x = [], 0
    for ch in text:
        name = cmap.get(ord(ch))
        if name is None:
            x += 520
            continue
        pen = FlattenPen(gs)
        gs[name].draw(pen)
        items.append((pen.polys, x))
        x += hmtx[name][0]

    W = int(x * scale) + pad * 2
    H = int(1.15 * upm * scale) + pad * 2
    px = [255] * (W * H)
    base = pad + int(0.88 * upm * scale)
    for polys, gx in items:
        preview.fill(px, W, H, polys, pad + gx * scale, base, scale)
    preview.write_png(out, W, H, px)
    print("rendered", out, "from", os.path.basename(ttf_path))


if __name__ == "__main__":
    render(sys.argv[1], sys.argv[2], sys.argv[3],
           int(sys.argv[4]) if len(sys.argv) > 4 else 120)
