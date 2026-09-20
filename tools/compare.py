"""Stack one string across several compiled fonts at one size."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import preview, render_ttf
from fontTools.ttLib import TTFont


def compare(out, fonts, text, size=44, pad=22, gap=22, label_w=250):
    scale = size / 1000.0
    rows, widest = [], 0
    for path in fonts:
        f = TTFont(path)
        gs, cmap, hmtx = f.getGlyphSet(), f.getBestCmap(), f["hmtx"]
        items, x = [], 0
        for ch in text:
            nm = cmap.get(ord(ch))
            if nm is None:
                x += 480
                continue
            pen = render_ttf.FlattenPen(gs)
            gs[nm].draw(pen)
            items.append((pen.polys, x))
            x += hmtx[nm][0]
        rows.append((os.path.basename(path), items))
        widest = max(widest, x)

    rowh = int(1.25 * 1000 * scale) + gap
    W = int(widest * scale) + pad * 2 + label_w
    H = rowh * len(rows) + pad * 2
    px = [255] * (W * H)
    for i, (name, items) in enumerate(rows):
        base = pad + i * rowh + int(0.92 * 1000 * scale)
        for polys, gx in items:
            preview.fill(px, W, H, polys, pad + label_w + gx * scale, base, scale)
    preview.write_png(out, W, H, px)
    print("wrote", out, "|", " / ".join(n for n, _ in rows))


if __name__ == "__main__":
    compare(sys.argv[1], sys.argv[3:], sys.argv[2], 44)
