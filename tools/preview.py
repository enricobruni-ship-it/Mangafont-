"""Render glyph contours to a PNG proof sheet (non-zero winding, 4x4 AA).

Pure stdlib so it works anywhere; used as the design feedback loop.
"""
import sys, os, zlib, struct
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from mangafont import glyphs as G
from mangafont import stroke as ST


def fill(px, W, H, polys, ox, oy, scale, ss=4):
    """Scanline fill with the non-zero winding rule, ss x ss supersampled."""
    edges = []
    for poly in polys:
        n = len(poly)
        for i in range(n):
            x0, y0 = poly[i]
            x1, y1 = poly[(i + 1) % n]
            X0 = ox + x0 * scale
            Y0 = oy - y0 * scale
            X1 = ox + x1 * scale
            Y1 = oy - y1 * scale
            if Y0 != Y1:
                edges.append((X0, Y0, X1, Y1))
    if not edges:
        return
    ymin = max(0, int(min(min(e[1], e[3]) for e in edges)))
    ymax = min(H - 1, int(max(max(e[1], e[3]) for e in edges)) + 1)

    cov = {}
    for py in range(ymin, ymax + 1):
        for sy in range(ss):
            y = py + (sy + 0.5) / ss
            xs = []
            for X0, Y0, X1, Y1 in edges:
                if (Y0 <= y < Y1) or (Y1 <= y < Y0):
                    t = (y - Y0) / (Y1 - Y0)
                    xs.append((X0 + (X1 - X0) * t, 1 if Y1 > Y0 else -1))
            if not xs:
                continue
            xs.sort()
            wind = 0
            spans = []
            for i in range(len(xs) - 1):
                wind += xs[i][1]
                if wind != 0:
                    spans.append((xs[i][0], xs[i + 1][0]))
            for xa, xb in spans:
                ia = int(xa * ss)
                ib = int(xb * ss)
                for sx in range(max(0, ia), min(W * ss - 1, ib) + 1):
                    px_x = sx // ss
                    cov[(px_x, py)] = cov.get((px_x, py), 0) + 1
    m = ss * ss
    for (x, y), c in cov.items():
        if 0 <= x < W and 0 <= y < H:
            v = 255 - int(255 * min(1.0, c / m))
            i = y * W + x
            px[i] = min(px[i], v)


def write_png(path, W, H, gray):
    raw = b"".join(b"\x00" + bytes(gray[y * W:(y + 1) * W]) for y in range(H))

    def chunk(tag, data):
        c = struct.pack(">I", len(data)) + tag + data
        return c + struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF)

    png = (b"\x89PNG\r\n\x1a\n"
           + chunk(b"IHDR", struct.pack(">IIBBBBB", W, H, 8, 0, 0, 0, 0))
           + chunk(b"IDAT", zlib.compress(raw, 9))
           + chunk(b"IEND", b""))
    open(path, "wb").write(png)


def sheet(path, names, cols=13, cell=96, scale=None, show_box=True):
    scale = scale or cell / 1150.0
    rows = (len(names) + cols - 1) // cols
    W, H = cols * cell, rows * cell
    px = [255] * (W * H)

    def hline(y, x0, x1, v=214):
        if 0 <= y < H:
            for x in range(max(0, x0), min(W, x1)):
                px[y * W + x] = min(px[y * W + x], v)

    def vline(x, y0, y1, v=214):
        if 0 <= x < W:
            for y in range(max(0, y0), min(H, y1)):
                px[y * W + x] = min(px[y * W + x], v)

    for idx, nm in enumerate(names):
        r, c = divmod(idx, cols)
        ox = c * cell + cell * 0.10
        oy = r * cell + cell * 0.80          # baseline
        if show_box:
            hline(int(oy), c * cell, (c + 1) * cell)                   # baseline
            hline(int(oy - G.CAP * scale), c * cell, (c + 1) * cell, 232)
            hline(int(oy - G.XH * scale), c * cell, (c + 1) * cell, 232)
            vline(c * cell, r * cell, (r + 1) * cell, 236)
        try:
            strokes, adv = G.glyph(nm)
        except KeyError:
            continue
        if show_box:
            vline(int(ox + adv * scale), r * cell, (r + 1) * cell, 236)
        polys = ST.contours(strokes)
        fill(px, W, H, polys, ox, oy, scale)
    write_png(path, W, H, px)
    print("wrote", path, W, "x", H)


def line(path, text, size=120, pad=24):
    scale = size / 1000.0
    adv_total = 0
    items = []
    for ch in text:
        nm = G.char_to_name(ch)
        if nm is None:
            adv_total += 520
            continue
        strokes, adv = G.glyph(nm)
        items.append((strokes, adv_total))
        adv_total += adv
    W = int(adv_total * scale) + pad * 2
    H = int(1100 * scale) + pad * 2
    px = [255] * (W * H)
    base = pad + int(860 * scale)
    for strokes, x in items:
        fill(px, W, H, ST.contours(strokes), pad + x * scale, base, scale)
    write_png(path, W, H, px)


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "build/proof.png"
    which = sys.argv[2] if len(sys.argv) > 2 else "all"
    if which == "all":
        sheet(out, G.ALL_NAMES)
    else:
        sheet(out, [G.char_to_name(c) for c in which if G.char_to_name(c)])
