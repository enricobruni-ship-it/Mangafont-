"""The weight axis.

Glyph sources quote every stroke in the units of one reference drawing
(the Display Regular cut).  A Weight carries those numbers into another
cut by remapping them through four anchors -- hairline, connector, sweep,
stem -- so adding a weight never means re-drawing a glyph.

Two things deliberately do NOT scale linearly, because they do not in
Mincho either:

  * Contrast falls as weight rises.  A bold 横画 is proportionally much
    thicker than a light one; holding the ratio at 0.44 into a bold would
    leave hairlines that snap at any real size.
  * Terminals grow sub-proportionally.  An うろこ scaled linearly into a
    bold swallows the letter, so ornaments run on a 0.72 power law.

Text cuts are an optical size, not a lighter weight: lower contrast,
sturdier terminals, quieter pressure modulation, a little more sidebearing.
"""


class Weight:
    """One cut: stroke anchors, modulation gain, ornament scale."""

    # The reference drawing's four stroke classes.
    REF = (46.0, 70.0, 84.0, 104.0)

    def __init__(self, family, style, anchors, gain=1.0, orn=1.0,
                 adv_pad=0, os2=400, bold=False, panose_weight=5,
                 overshoot=0.0, soft=None):
        self.family = family
        self.style = style
        self.anchors = tuple(float(a) for a in anchors)
        self.gain = gain          # how much pressure modulation survives
        self.orn = orn            # extra hand on the terminal ornaments
        self.adv_pad = adv_pad    # sidebearing added to every advance
        # Strokes running past their joins, in design units.  A large
        # part of why kanji read as kanji is that strokes cross and
        # stick out instead of stopping politely at the junction.
        self.overshoot = overshoot
        # Per-cut override of the hiragana softening (bow, curve, curl).
        self.soft = soft
        # An optional second spec used only for the lowercase.  Caps and
        # lowercase carrying different weights inside one face is normal
        # type practice -- caps are usually drawn a shade lighter so the
        # two colours match.  This just allows a larger split than usual,
        # so one register can serve the caps and another the lowercase.
        self.lower = None
        self.os2 = os2
        self.bold = bold
        self.panose_weight = panose_weight

    # ------------------------------------------------------------ widths

    def remap(self, w):
        """Carry a width quoted in reference units into this cut."""
        src, dst = self.REF, self.anchors
        if w <= src[0]:
            return w * dst[0] / src[0]
        if w >= src[-1]:
            return w * dst[-1] / src[-1]
        for i in range(1, len(src)):
            if w <= src[i]:
                f = (w - src[i - 1]) / (src[i] - src[i - 1])
                return dst[i - 1] + (dst[i] - dst[i - 1]) * f
        return w

    @property
    def stem(self):
        return self.anchors[3]

    @property
    def orn_scale(self):
        """Ornaments follow weight on a 0.72 power law, never linearly."""
        return (self.stem / self.REF[3]) ** 0.72 * self.orn

    @property
    def contrast(self):
        return self.anchors[0] / self.anchors[3]

    @property
    def ps_name(self):
        return "%s-%s" % (self.family.replace(" ", ""), self.style)

    @property
    def file_stem(self):
        return "%s-%s" % (self.family.replace(" ", ""), self.style)


# hairline, connector, sweep, stem
DISPLAY = Weight(
    "Mangafont", "Regular", (46, 70, 84, 104),
    gain=1.00, orn=1.00, adv_pad=0, os2=400, panose_weight=5)

DISPLAY_BOLD = Weight(
    "Mangafont", "Bold", (86, 118, 140, 168),
    gain=0.70, orn=0.88, adv_pad=24, os2=700, bold=True, panose_weight=8)

TEXT = Weight(
    "Mangafont Text", "Regular", (58, 76, 88, 96),
    gain=0.78, orn=1.12, adv_pad=14, os2=400, panose_weight=5)

TEXT_BOLD = Weight(
    "Mangafont Text", "Bold", (100, 126, 142, 156),
    gain=0.60, orn=0.92, adv_pad=32, os2=700, bold=True, panose_weight=8)

ALL = [TEXT, TEXT_BOLD, DISPLAY, DISPLAY_BOLD]


# --------------------------------------------------- comic candidates
#
# Three registers for comic lettering, which needs weight and punch that
# a reading face does not.  Not in ALL: they are built by
# tools/directions.py for comparison, and one gets promoted to a proper
# family once chosen.

BRUSH = Weight(
    "Mangafont Brush", "Regular", (62, 124, 176, 216),
    gain=1.40, orn=1.80, adv_pad=74, overshoot=10, os2=700, bold=True,
    panose_weight=9)

BLOCK = Weight(
    "Mangafont Block", "Regular", (168, 182, 192, 202),
    gain=0.14, orn=0.42, adv_pad=84, overshoot=36, os2=700, bold=True,
    panose_weight=9)

GOTHIC = Weight(
    "Mangafont Gothic", "Regular", (150, 156, 160, 164),
    gain=0.05, orn=0.0, adv_pad=58, overshoot=4, os2=700, bold=True,
    panose_weight=9)

# Brush caps over Block lowercase, exactly as asked.  The stems are
# close enough (216 against 202) for the two to sit on one line.
COMIC = Weight(
    "Mangafont Comic", "Regular", BRUSH.anchors,
    gain=BRUSH.gain, orn=BRUSH.orn, adv_pad=BRUSH.adv_pad,
    overshoot=BRUSH.overshoot, os2=800, bold=True, panose_weight=9)

# The lowercase used to render on BLOCK, and that was the real reason it
# read as "squared and mechanical" -- not only the box skeletons.  BLOCK
# is contrast 0.83 and gain 0.14: monoline by construction, and it throws
# 86% of any brush away.  Swapping stroke profiles under it moved almost
# no ink at all.  This keeps BLOCK's stem (202), so the two registers
# still sit on one line and match in colour, but opens the contrast and
# the gain far enough that the brush actually survives.
COMIC.lower = Weight(
    "Mangafont Comic", "Regular", (104, 150, 178, 202),
    gain=0.70, orn=1.25, adv_pad=BLOCK.adv_pad,
    overshoot=BLOCK.overshoot, os2=800, bold=True, panose_weight=9)

# The alternative: not two registers bolted together but one that takes
# Brush's dramatic terminals and Block's robustness -- the hairlines
# lifted far enough to survive, the flags kept large.
FUSED = Weight(
    "Mangafont Fused", "Regular", (108, 148, 182, 212),
    gain=1.00, orn=1.20, adv_pad=70, overshoot=20, os2=700, bold=True,
    panose_weight=9)

CANDIDATES = [BRUSH, BLOCK, GOTHIC, COMIC, FUSED]

# Shipped alongside the four text/display cuts: the comic face, whose
# caps and lowercase come from different registers on purpose.
ALL = ALL + [COMIC]
