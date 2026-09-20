"""Stack the same string in every cut, for comparing them."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

import preview
from mangafont import stroke as ST, glyphs as G
from mangafont.weights import ALL


def stack(path, text, size=104, pad=26, gap=30):
    scale = size / 1000.0
    rows, widest = [], 0
    for w in ALL:
        ST.set_weight(w)
        items, x = [], 0
        for ch in text:
            nm = G.char_to_name(ch)
            if nm is None:
                x += 480
                continue
            strokes, adv = G.glyph(nm)
            items.append((ST.contours(strokes), x))
            x += adv
        rows.append((w, items))
        widest = max(widest, x)

    rowh = int(1.20 * 1000 * scale) + gap
    W = int(widest * scale) + pad * 2 + 200
    H = rowh * len(rows) + pad * 2
    px = [255] * (W * H)
    for i, (w, items) in enumerate(rows):
        base = pad + i * rowh + int(0.90 * 1000 * scale)
        for polys, gx in items:
            preview.fill(px, W, H, polys, pad + 190 + gx * scale, base, scale)
    preview.write_png(path, W, H, px)
    print("wrote", path, W, "x", H)
    for w in ALL:
        print("   %-24s contrast %.2f" % (w.family + " " + w.style, w.contrast))


if __name__ == "__main__":
    stack(sys.argv[1], sys.argv[2], int(sys.argv[3]) if len(sys.argv) > 3 else 104)
