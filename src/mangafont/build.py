"""Compile the stroke skeletons into TrueType and OpenType, one file per cut."""

import os

from fontTools.fontBuilder import FontBuilder
from fontTools.pens.ttGlyphPen import TTGlyphPen

from . import glyphs as G
from . import stroke as ST
from . import weights as WGT
from .stroke import contours as stroke_contours

VERSION = "2.000"

# Rebuilds should be byte-identical when nothing has been redrawn.
# fontTools stamps head.created/modified from the wall clock, which
# rewrote every binary on every build and buried real changes in noise.
EPOCH = 3872800000          # fixed project timestamp

FS_REGULAR = 0x40 | 0x80          # REGULAR + USE_TYPO_METRICS
FS_BOLD = 0x20 | 0x80             # BOLD + USE_TYPO_METRICS


def _notdef():
    pen = TTGlyphPen(None)
    for x0, y0, x1, y1 in ((70, 0, 560, 790), (150, 80, 480, 710)):
        pen.moveTo((x0, y0))
        pen.lineTo((x0, y1))
        pen.lineTo((x1, y1))
        pen.lineTo((x1, y0))
        pen.closePath()
    return pen.glyph()


def build_glyphs():
    """Draw every glyph in whichever cut is currently active."""
    order = [".notdef"] + G.ALL_NAMES
    glyf, metrics = {".notdef": _notdef()}, {".notdef": (620, 70)}

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
        metrics[name] = (int(round(adv)), int(round(min(xs))) if xs else 0)
    return order, glyf, metrics


def _names(w):
    full = "%s %s" % (w.family, w.style)
    return {
        "familyName": w.family,
        "styleName": w.style,
        "uniqueFontIdentifier": "%s; %s" % (w.ps_name, VERSION),
        "fullName": full,
        "psName": w.ps_name,
        "version": "Version " + VERSION,
        "copyright": "SIL Open Font License 1.1",
        "designer": "Generated from stroke skeletons",
        "description": ("A Latin alphabet drawn with the stroke vocabulary "
                        "of hiragana, katakana and kanji."),
        "licenseDescription": (
            "This Font Software is licensed under the SIL Open Font "
            "License, Version 1.1."),
        "licenseInfoURL": "https://scripts.sil.org/OFL",
    }


def _os2(w):
    return dict(
        sTypoAscender=G.ASCENDER, sTypoDescender=G.DESCENDER,
        sTypoLineGap=110, usWinAscent=G.ASCENDER, usWinDescent=-G.DESCENDER,
        sxHeight=G.XH, sCapHeight=G.CAP,
        version=4,          # USE_TYPO_METRICS (bit 7) needs v4 or later
        usWeightClass=w.os2, usWidthClass=5,
        fsSelection=FS_BOLD if w.bold else FS_REGULAR,
        achVendID="MNGA", fsType=0,
        panose=dict(bFamilyType=2, bSerifStyle=2, bWeight=w.panose_weight,
                    bProportion=3, bContrast=0, bStrokeVariation=0,
                    bArmStyle=0, bLetterForm=0, bMidline=0, bXHeight=0),
    )


def _common(fb, w, order, metrics):
    fb.setupGlyphOrder(order)
    fb.setupCharacterMap(G.CMAP)
    fb.setupHorizontalMetrics(metrics)
    fb.setupHorizontalHeader(ascent=G.ASCENDER, descent=G.DESCENDER,
                             lineGap=110)
    fb.setupNameTable(_names(w))
    fb.setupOS2(**_os2(w))
    fb.setupPost(isFixedPitch=0, underlinePosition=-160,
                 underlineThickness=int(round(w.stem * 0.8)))
    if w.bold:
        fb.font["head"].macStyle |= 0x01
    fb.font["head"].created = EPOCH
    fb.font["head"].modified = EPOCH


def to_otf(ttf, out_path, w, order, metrics):
    """Derive the CFF build from the finished TrueType outlines.

    Overlaps are already booleaned away by this point, so this only has to
    change curve flavour (quadratic to cubic) and winding: PostScript wants
    outer contours counter-clockwise, the opposite of TrueType.
    """
    from fontTools.pens.t2CharStringPen import T2CharStringPen
    from fontTools.pens.qu2cuPen import Qu2CuPen

    glyph_set = ttf.getGlyphSet()
    charstrings = {}
    for name in order:
        t2 = T2CharStringPen(metrics[name][0], None)
        pen = Qu2CuPen(t2, max_err=0.5, reverse_direction=True, all_cubic=True)
        glyph_set[name].draw(pen)
        charstrings[name] = t2.getCharString()

    fb = FontBuilder(G.UPM, isTTF=False)
    fb.setupGlyphOrder(order)
    fb.setupCharacterMap(G.CMAP)
    fb.setupCFF(w.ps_name, {
        "version": VERSION,
        "FullName": "%s %s" % (w.family, w.style),
        "FamilyName": w.family,
        "Weight": w.style,
    }, charstrings, {})
    _common(fb, w, order, metrics)
    fb.font.save(out_path)
    return out_path


def _set_overlap_flag(font):
    glyf = font["glyf"]
    for name in glyf.keys():
        g = glyf[name]
        if g.numberOfContours > 0 and getattr(g, "flags", None) is not None \
                and len(g.flags):
            g.flags[0] |= 0x40          # OVERLAP_SIMPLE


def build_one(w, out_dir="build"):
    ST.set_weight(w)
    order, glyf, metrics = build_glyphs()

    fb = FontBuilder(G.UPM, isTTF=True)
    fb.setupGlyf(glyf)
    _common(fb, w, order, metrics)
    font = fb.font

    # Glyphs are stacks of overlapping stroke contours -- exactly how a
    # kanji is built.  Boolean them into single outlines so every renderer
    # agrees, and keep OVERLAP_SIMPLE set as a fallback.
    try:
        from fontTools.ttLib.removeOverlaps import removeOverlaps
        removeOverlaps(font)
        merged = True
    except ImportError:
        merged = False
    _set_overlap_flag(font)

    os.makedirs(out_dir, exist_ok=True)
    ttf = os.path.join(out_dir, w.file_stem + ".ttf")
    font.save(ttf)

    otf = to_otf(font, os.path.join(out_dir, w.file_stem + ".otf"),
                 w, order, metrics)

    font.flavor = "woff2"
    woff2 = os.path.join(out_dir, w.file_stem + ".woff2")
    font.save(woff2)
    return ttf, otf, woff2, merged, len(order)


def build(out_dir="build"):
    results = []
    for w in WGT.ALL:
        results.append((w,) + build_one(w, out_dir))
    return results


if __name__ == "__main__":
    for row in build():
        w, ttf, otf, woff2, merged, n = row
        print("%-24s contrast %.2f  %d glyphs  overlaps %s"
              % (w.family + " " + w.style, w.contrast, n,
                 "merged" if merged else "flagged"))
        print("    " + "  ".join(os.path.basename(p)
                                 for p in (ttf, otf, woff2)))
