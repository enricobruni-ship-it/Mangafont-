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

CANDIDATES = [BRUSH, BLOCK, GOTHIC]
