"""Compile the stroke skeletons into a TrueType font."""

import os

from fontTools.fontBuilder import FontBuilder
from fontTools.pens.ttGlyphPen import TTGlyphPen

from . import glyphs as G
from .stroke import contours as stroke_contours

FAMILY = "Mangafont"
STYLE = "Regular"
VERSION = "1.000"


def _notdef():
    pen = TTGlyphPen(None)
    for box in ((60, 0, 500, 700), (130, 70, 430, 630)):
        x0, y0, x1, y1 = box
        pen.moveTo((x0, y0))
        pen.lineTo((x0, y1))
        pen.lineTo((x1, y1))
        pen.lineTo((x1, y0))
        pen.closePath()
    return pen.glyph()


def build_glyphs():
    order = [".notdef"] + G.ALL_NAMES
    glyf, metrics = {".notdef": _notdef()}, {".notdef": (560, 60)}

    for name in G.ALL_NAMES:
        strokes, adv = G.glyph(name)
        pen = TTGlyphPen(None)
        xs = []
        for contour in stroke_contours(strokes):
            pen.moveTo(contour[0])
            for pt in contour[1:]:
                pen.lineTo(pt)
            pen.closePath()
            xs.extend(p[0] for p in contour)
        glyf[name] = pen.glyph()
        lsb = int(round(min(xs))) if xs else 0
        metrics[name] = (int(round(adv)), lsb)
    return order, glyf, metrics


def build(out_dir="build"):
    order, glyf, metrics = build_glyphs()

    fb = FontBuilder(G.UPM, isTTF=True)
    fb.setupGlyphOrder(order)
    fb.setupCharacterMap(G.CMAP)
    fb.setupGlyf(glyf)
    fb.setupHorizontalMetrics(metrics)
    fb.setupHorizontalHeader(ascent=G.ASCENDER, descent=G.DESCENDER,
                             lineGap=120)

    ps = "%s-%s" % (FAMILY, STYLE)
    fb.setupNameTable({
        "familyName": FAMILY,
        "styleName": STYLE,
        "uniqueFontIdentifier": "%s; %s" % (ps, VERSION),
        "fullName": "%s %s" % (FAMILY, STYLE),
        "psName": ps,
        "version": "Version " + VERSION,
        "copyright": "SIL Open Font License 1.1",
        "designer": "Generated from stroke skeletons",
        "description": ("A Latin alphabet drawn with the stroke vocabulary "
                        "of hiragana, katakana and kanji."),
        "licenseDescription": (
            "This Font Software is licensed under the SIL Open Font "
            "License, Version 1.1."),
        "licenseInfoURL": "https://scripts.sil.org/OFL",
    })
    fb.setupOS2(
        sTypoAscender=G.ASCENDER, sTypoDescender=G.DESCENDER,
        sTypoLineGap=120, usWinAscent=G.ASCENDER, usWinDescent=-G.DESCENDER,
        sxHeight=G.XH, sCapHeight=G.CAP,
        achVendID="MNGA", fsType=0,
        panose=dict(bFamilyType=2, bSerifStyle=2, bWeight=6,
                    bProportion=3, bContrast=0, bStrokeVariation=0,
                    bArmStyle=0, bLetterForm=0, bMidline=0, bXHeight=0),
    )
    fb.setupPost(isFixedPitch=0, underlinePosition=-150,
                 underlineThickness=90)

    font = fb.font

    # The glyphs are stacks of overlapping stroke contours -- exactly how a
    # kanji is built.  Boolean them into single outlines so every renderer
    # agrees, and keep OVERLAP_SIMPLE set as a belt-and-braces fallback.
    try:
        from fontTools.ttLib.removeOverlaps import removeOverlaps
        removeOverlaps(font)
        merged = True
    except ImportError:
        merged = False
    _set_overlap_flag(font)

    os.makedirs(out_dir, exist_ok=True)
    ttf = os.path.join(out_dir, "%s-%s.ttf" % (FAMILY, STYLE))
    font.save(ttf)

    font.flavor = "woff2"
    woff2 = os.path.join(out_dir, "%s-%s.woff2" % (FAMILY, STYLE))
    font.save(woff2)

    return ttf, woff2, merged, len(order)


def _set_overlap_flag(font):
    glyf = font["glyf"]
    for name in glyf.keys():
        g = glyf[name]
        if g.numberOfContours > 0 and getattr(g, "flags", None) is not None \
                and len(g.flags):
            g.flags[0] |= 0x40          # OVERLAP_SIMPLE


if __name__ == "__main__":
    ttf, woff2, merged, n = build()
    print("%s  (%d glyphs, overlaps %s)"
          % (ttf, n, "merged" if merged else "flagged only"))
    print(woff2)
