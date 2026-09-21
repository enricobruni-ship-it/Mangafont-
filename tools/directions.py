"""Build the comic-lettering candidates for side-by-side comparison.

    python3 tools/directions.py build/

Writes one .woff2 per candidate plus a dirs.css with them embedded, for
dropping into a comparison page.  These are candidates, not shipped
cuts -- see weights.CANDIDATES.
"""
import base64
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from fontTools.fontBuilder import FontBuilder
from fontTools.ttLib.removeOverlaps import removeOverlaps

from mangafont import build as B, stroke as ST
from mangafont.weights import CANDIDATES


def main(out_dir):
    os.makedirs(out_dir, exist_ok=True)
    css = []
    for w in CANDIDATES:
        ST.set_weight(w)
        order, glyf, metrics = B.build_glyphs()
        fb = FontBuilder(1000, isTTF=True)
        fb.setupGlyf(glyf)
        B._common(fb, w, order, metrics)
        font = fb.font
        removeOverlaps(font)
        B._set_overlap_flag(font)
        font.flavor = "woff2"
        stem = w.family.replace(" ", "")
        path = os.path.join(out_dir, stem + ".woff2")
        font.save(path)
        data = base64.b64encode(open(path, "rb").read()).decode()
        css.append('@font-face{font-family:"%s";font-weight:400;'
                   'font-style:normal;font-display:block;'
                   'src:url("data:font/woff2;base64,%s") format("woff2");}'
                   % (w.family, data))
        print("%-20s contrast %.2f  stem %3.0f  overshoot %2d  %d KB"
              % (w.family, w.contrast, w.stem, w.overshoot,
                 os.path.getsize(path) // 1024))
    open(os.path.join(out_dir, "dirs.css"), "w").write("\n".join(css))
    print("wrote", os.path.join(out_dir, "dirs.css"))


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "build")
