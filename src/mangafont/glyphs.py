"""Glyph skeletons.

Every letter is assembled from the stroke vocabulary of Japanese writing
and laid into a square the way a kanji is.  Three things do most of the
work of making a Latin alphabet read as kana:

  * contrast -- 横画 are hairlines, 縦画 are slabs, at roughly 0.4;
  * corners -- there are almost no curves in kanji, so every arch and
    bowl is a 折れ fold with a 肩 shoulder, never a quadratic;
  * fit -- the glyphs fill the em square, with a very high x-height and
    tight, near-uniform side bearings.
"""

from .stroke import Stroke, kata, kihitsu

# ------------------------------------------------------------- metrics

UPM = 1000
CAP = 790          # cap height / figure height
XH = 600           # x-height -- 0.76 of cap, so lowercase fills a square
ASC = 858
DESC = -170
ASCENDER = 900
DESCENDER = -250

WT = 104           # 縦画  the stem
WY = 46            # 横画  the hairline -- 0.44 of the stem
WD = 84            # 払い  the sweep
WC = 70            # corner connectors

RISE = 0.030       # horizontals climb ~1.7 degrees to the right

L, R = 64, 700     # the character face
ADV = 768


# ----------------------------------------------------------- shorthands

def yoko(x0, x1, y, w=WY, prof="yoko", flag=True):
    """横画 -- a hairline horizontal climbing to the right.

    `flag` is the うろこ at the stop.  It is switched off wherever the
    stroke turns down into a stem, because that corner wears a 肩
    instead; carrying both stacks two ornaments on one corner.
    """
    return Stroke([("M", x0, y), ("L", x1, y + (x1 - x0) * RISE)], w, prof,
                  uroko_end=None if flag else (0, 0))


def yoko_in(x0, x1, y, w=WY):
    """A horizontal that dies into a stem: pressed entry, no うろこ."""
    return yoko(x0, x1, y, w, "yoko_in")


def tate(x, ytop, ybot, w=WT, prof="tate", drift=-5, head=True):
    """縦画 -- a stem, with its flared 起筆 head."""
    out = [Stroke([("M", x, ytop), ("L", x + drift, ybot)], w, prof)]
    if head:
        out.append(kihitsu(x, ytop, w))
    return out


def fold(x0, x1, ytop, ybot, wt=WT, wy=WY):
    """横折 -- a horizontal turning down into a stem, carrying its 肩.

    Rendered as two strokes because the two halves are different
    weights: that weight change across the corner is the whole point.
    """
    rx = x1 - wt * 0.5
    rise = (x1 - x0) * RISE
    return ([yoko(x0, x1, ytop, wy, flag=False)]
            + tate(rx, ytop + rise, ybot, wt, head=False)
            + [kata(rx, ytop + rise, wt)])


def box(x0, x1, ybot, ytop, wt=WT, wy=WY):
    """口 -- three strokes: left 竖, 横折, bottom 横."""
    return (tate(x0 + wt * 0.5, ytop, ybot, wt)
            + fold(x0, x1, ytop, ybot, wt, wy)
            + [yoko(x0, x1, ybot, wy)])


def ring(x0, x1, ybot, ytop, wt=WT, wy=WY, cx=0.20, cy=0.15):
    """A 口 with its corners cut, for O / o / 0 / 8."""
    dx = (x1 - x0) * cx
    dy = (ytop - ybot) * cy
    lx, rx = x0 + wt * 0.5, x1 - wt * 0.5
    out = []
    out += tate(lx, ytop - dy, ybot + dy, wt, head=False)
    out += tate(rx, ytop - dy + 8, ybot + dy, wt, head=False)
    rise = (x1 - x0 - 2 * dx) * RISE
    out.append(yoko(x0 + dx, x1 - dx, ytop, wy, flag=False))
    out.append(yoko(x0 + dx, x1 - dx, ybot, wy, flag=False))
    taper = [(0.0, 0.52), (1.0, 1.42)]
    for a, b in (((x0 + dx + 10, ytop), (lx, ytop - dy - 12)),
                 ((x1 - dx - 10, ytop + rise), (rx, ytop - dy - 12)),
                 ((x0 + dx + 10, ybot), (lx, ybot + dy + 12)),
                 ((x1 - dx - 10, ybot + rise), (rx, ybot + dy + 12))):
        out.append(Stroke([("M", a[0], a[1]), ("L", b[0], b[1])],
                          WC, taper))
    return out


def harai_l(p0, p1, w=WD):
    """左払い -- the sweep down to the left."""
    return Stroke([("M", p0[0], p0[1]), ("L", p1[0], p1[1])], w, "harai_l")


def harai_r(p0, p1, w=WD):
    """右払い -- the sweep down to the right."""
    return Stroke([("M", p0[0], p0[1]), ("L", p1[0], p1[1])], w, "harai_r")


def ten(x, y, dx=86, dy=-92, w=76):
    """点 -- the tick."""
    return Stroke([("M", x, y), ("L", x + dx, y + dy)], w, "ten")


def hane(path, w=WT):
    """A stroke finishing in a sharp はね flick."""
    return Stroke(path, w, "hane")


# ---------------------------------------------------------------- CAPS

def _A():
    return [
        harai_l((406, CAP), (70, 8)),
        harai_r((420, CAP - 18), (700, 8)),
        yoko(140, 636, 246),                      # crosses and overshoots
    ], ADV


def _B():
    return (tate(L + 50, CAP, 0)
            + fold(L, 636, CAP, 424)
            + [yoko(L, 664, 410)]
            + fold(L + 40, 690, 410, 0)
            + [yoko(L, 700, 0)]), ADV


def _C():
    """匚"""
    return ([yoko(L, R, CAP)]
            + tate(L + 50, CAP, 40)
            + [yoko(L, R, 0)]), ADV


def _D():
    x1, dy = 690, 154
    rx = x1 - WT * 0.5
    taper = [(0.0, 0.52), (1.0, 1.42)]
    return (tate(L + WT * 0.5, CAP, 0)
            + [yoko(L, x1 - 96, CAP, flag=False),
               yoko(L, x1 - 96, 0, flag=False)]
            + tate(rx, CAP - dy + 6, dy, WT, head=False)
            + [Stroke([("M", x1 - 104, CAP + 4), ("L", rx, CAP - dy - 14)],
                      WC, taper),
               Stroke([("M", x1 - 104, 6), ("L", rx, dy + 14)], WC, taper)]
            ), ADV


def _E():
    return (tate(L + 50, CAP, 0)
            + [yoko(L, 684, CAP), yoko(L, 588, 404), yoko(L, R, 0)]), ADV


def _F():
    return (tate(L + 50, CAP, 0)
            + [yoko(L, 684, CAP), yoko(L, 600, 404)]), 720


def _G():
    return ([yoko(L, R, CAP)]
            + tate(L + 50, CAP, 40)
            + [yoko(L, R, 0)]
            + tate(650, 392, 30, WT, head=False)
            + [yoko(420, 690, 382)]), ADV


def _H():
    """廾 -- the bar crosses both stems and runs past them."""
    return (tate(160, CAP, 0) + tate(610, CAP, 0)
            + [yoko(70, 700, 430)]), ADV


def _I():
    """工"""
    return ([yoko(70, 700, CAP)]
            + tate(384, CAP, 10)
            + [yoko(L, 706, 0)]), ADV


def _J():
    """了"""
    return [
        yoko(140, R, CAP),
        hane([("M", 570, CAP), ("L", 560, 168), ("L", 400, 40),
              ("L", 190, 60), ("L", 150, 150)], 96),
    ], 740


def _K():
    return (tate(150, CAP, 0)
            + [harai_l((690, CAP - 14), (96, 396), 80),
               harai_r((166, 442), (700, 8), 88)]), ADV


def _L():
    """乚"""
    return [
        hane([("M", 164, CAP), ("L", 158, 96), ("L", 268, 16),
              ("L", 640, 6), ("L", 706, 86)], 98),
        kihitsu(164, CAP, 98),
    ], 740


def _M():
    return (tate(124, CAP, 0) + tate(752, CAP, 0)
            + [Stroke([("M", 130, CAP - 20), ("L", 424, 230)], 80, "diag"),
               Stroke([("M", 746, CAP - 20), ("L", 440, 230)], 80, "diag")]
            ), 830


def _N():
    return (tate(130, CAP, 0) + tate(652, CAP, 0)
            + [Stroke([("M", 136, CAP - 22), ("L", 650, 104)], 82,
                      [(0.0, 1.10), (0.5, 0.92), (1.0, 1.04)])]), 790


def _O():
    return ring(L + 6, R - 6, 0, CAP), ADV


def _P():
    return (tate(L + 50, CAP, 0)
            + fold(L, 620, CAP, 404)
            + [yoko(L, 648, 392)]), 740


def _Q():
    return ring(L + 6, R - 6, 0, CAP) + [
        harai_r((392, 182), (690, -132), 80),
    ], ADV


def _R():
    return (tate(L + 50, CAP, 0)
            + fold(L, 620, CAP, 404)
            + [yoko(L, 648, 392),
               harai_r((156, 400), (700, 6), 86)]), ADV


def _S():
    """己 -- the fold chain, squared off."""
    return ([yoko(110, 678, CAP)]
            + tate(160, CAP, 470)
            + [yoko(110, 690, 424)]
            + tate(636, 424, 96, WT, head=False)
            + [kata(636, 424, WT), yoko(76, 672, 16)]), ADV


def _T():
    """丁"""
    return ([yoko(L, 706, CAP)] + tate(384, CAP, 10)), ADV


def _U():
    """凵"""
    return (tate(160, CAP, 86, WT)
            + [yoko(110, 666, 14)]
            + tate(614, CAP, 86, WT)), ADV


def _V():
    return [
        Stroke([("M", 112, CAP), ("L", 372, 14)], 86, "diag"),
        Stroke([("M", 660, CAP), ("L", 400, 14)], 86, "diag"),
    ], ADV


def _W():
    return [
        Stroke([("M", 96, CAP), ("L", 254, 14)], 76, "diag"),
        Stroke([("M", 430, CAP - 24), ("L", 274, 14)], 76, "diag"),
        Stroke([("M", 442, CAP - 24), ("L", 604, 14)], 76, "diag"),
        Stroke([("M", 776, CAP), ("L", 622, 14)], 76, "diag"),
    ], 872


def _X():
    """乂"""
    return [
        harai_l((684, CAP), (92, 6), 86),
        harai_r((100, CAP - 16), (684, 6), 86),
    ], ADV


def _Y():
    """丫"""
    return ([Stroke([("M", 116, CAP), ("L", 360, 420)], 82, "diag"),
             Stroke([("M", 658, CAP), ("L", 414, 420)], 82, "diag")]
            + tate(386, 440, 10, WT, head=False)), ADV


def _Z():
    """乙"""
    return [
        yoko(96, 684, CAP),
        Stroke([("M", 650, CAP - 20), ("L", 128, 60)], 84,
               [(0.0, 0.96), (0.5, 0.84), (1.0, 1.0)]),
        yoko(76, 700, 0),
    ], ADV


# ----------------------------------------------------------- LOWERCASE
# x-height 600 of a 790 cap: lowercase sits in a square, as kana do.
# Every arch is a 冂 fold, every bowl a 口.

LADV = 706


def _a():
    """A squared bowl whose floor runs past the stem and flicks up."""
    x0, x1 = 72, 556
    rx = x1 - WT * 0.5
    return (tate(x0 + WT * 0.5, XH, 14)
            + [yoko(x0, x1, XH, flag=False), kata(rx, XH + 14, WT)]
            + tate(rx, XH + 14, 14, WT, head=False)
            + [hane([("M", x0, 12), ("L", 590, 30), ("L", 700, 104)], 58)]
            ), 744


def _b():
    return (tate(L + 50, ASC, 0)
            + fold(L, 592, 450, 0)
            + [yoko(L, 620, 0)]), LADV


def _c():
    """匚"""
    return ([yoko(72, 636, XH)]
            + tate(122, XH, 40)
            + [yoko(72, 646, 0)]), 690


def _d():
    return (tate(592, ASC, 0)
            + [yoko(L, 620, 450)]
            + tate(L + 50, 464, 0)
            + [yoko(L, 620, 0)]), LADV


def _e():
    """The bowl closes at the top and opens at the foot."""
    return (tate(122, XH, 46)
            + [yoko(72, 604, XH)]
            + tate(558, XH + 16, 336, WT, head=False)
            + [kata(558, XH + 16, WT),
               yoko(72, 640, 322),
               yoko(72, 650, 6)]), 700


def _f():
    """千 -- a stem, a flag, and a crossbar that runs past it."""
    return (tate(352, 832, 0)
            + [yoko(352, 606, 830, 44),
               yoko(84, 622, XH)]), 660


def _g():
    """The bowl's right stem carries straight on into the descender."""
    x0, x1 = 72, 556
    rx = x1 - WT * 0.5
    return (tate(x0 + WT * 0.5, XH, 16)
            + [yoko(x0, x1, XH, flag=False), kata(rx, XH + 14, WT),
               hane([("M", rx, XH + 14), ("L", rx - 10, -46),
                     ("L", 366, -162), ("L", 162, -140), ("L", 108, -46)],
                    WT),
               yoko(x0, x1 - 34, 16)]), 744


def _h():
    """冂 hung on a tall stem."""
    return (tate(L + 50, ASC, 0)
            + fold(L, 592, XH, 0)), LADV


def _i():
    return (tate(206, XH, 10)
            + [ten(150, 800)]), 430


def _j():
    return [
        hane([("M", 268, XH), ("L", 258, -38), ("L", 150, -150),
              ("L", 40, -130), ("L", 6, -46)], 96),
        kihitsu(268, XH, 96),
        ten(212, 800),
    ], 440


def _k():
    return (tate(150, ASC, 0)
            + [harai_l((620, XH - 6), (96, 288), 76),
               harai_r((158, 328), (636, 6), 82)]), 672


def _l():
    """レ"""
    return [
        hane([("M", 208, ASC), ("L", 202, 96), ("L", 300, 18),
              ("L", 430, 40), ("L", 468, 110)], 96),
        kihitsu(208, ASC, 96),
    ], 500


def _m():
    """川 under one bar -- three stems, evenly spaced."""
    return (tate(L + 50, XH, 0)
            + [yoko(L, 776, XH, flag=False)]
            + tate(414, XH + 21, 0, WT, head=False)
            + [kata(414, XH + 21, WT)]
            + tate(726, XH + 23, 0, WT, head=False)
            + [kata(726, XH + 23, WT)]), 840


def _n():
    """冂"""
    return (tate(L + 50, XH, 0)
            + fold(L, 592, XH, 0)), LADV


def _o():
    return ring(72, 636, 10, XH, 96, cx=0.21), 708


def _p():
    return (tate(L + 50, XH, DESC)
            + fold(L, 592, XH, 24)
            + [yoko(L, 620, 16)]), LADV


def _q():
    return (tate(592, XH, DESC)
            + [yoko(L, 620, XH)]
            + tate(L + 50, XH + 18, 16)
            + [yoko(L, 620, 8)]), LADV


def _r():
    """ケ -- a hairline arm that lifts into a flick."""
    return (tate(L + 50, XH, 0)
            + [yoko(L, 416, XH),
               Stroke([("M", 372, XH - 30), ("L", 470, XH + 96)], 78,
                      [(0.0, 1.12), (0.55, 0.78), (1.0, 0.04)])]), 530


def _s():
    """己, at x-height."""
    return ([yoko(84, 596, XH)]
            + tate(134, XH, 366)
            + [yoko(84, 606, 328)]
            + tate(556, 328, 74, WT, head=False)
            + [kata(556, 328, WT), yoko(56, 592, 12)]), 660


def _t():
    """十 -- the bar crosses the stem and runs past both sides."""
    return [
        hane([("M", 338, 780), ("L", 330, 118), ("L", 420, 32),
              ("L", 530, 56), ("L", 566, 126)], 96),
        kihitsu(338, 780, 96),
        yoko(88, 604, XH),
    ], 640


def _u():
    """リ"""
    return (tate(L + 50, XH, 86)
            + [yoko(L, 616, 16)]
            + tate(578, XH, 0)), 726


def _v():
    return [
        Stroke([("M", 108, XH), ("L", 318, 12)], 80, "diag"),
        Stroke([("M", 580, XH), ("L", 344, 12)], 80, "diag"),
    ], 694


def _w():
    return [
        Stroke([("M", 92, XH), ("L", 228, 12)], 70, "diag"),
        Stroke([("M", 382, XH - 18), ("L", 246, 12)], 70, "diag"),
        Stroke([("M", 394, XH - 18), ("L", 532, 12)], 70, "diag"),
        Stroke([("M", 686, XH), ("L", 550, 12)], 70, "diag"),
    ], 786


def _x():
    """乂"""
    return [
        harai_l((600, XH), (94, 6), 80),
        harai_r((100, XH - 14), (600, 6), 80),
    ], 700


def _y():
    """メ, with the second sweep carrying on into the descender."""
    return [
        Stroke([("M", 108, XH), ("L", 372, 150)], 80, "diag"),
        hane([("M", 606, XH), ("L", 300, -46), ("L", 150, -152),
              ("L", 40, -120)], 82),
    ], 700


def _z():
    """乙"""
    return [
        yoko(88, 610, XH),
        Stroke([("M", 580, XH - 18), ("L", 126, 58)], 78,
               [(0.0, 0.96), (0.5, 0.84), (1.0, 1.0)]),
        yoko(70, 636, 0),
    ], 700


# -------------------------------------------------------------- FIGURES

FADV = 764


def _zero():
    return ring(120, 644, 0, CAP, cx=0.24), FADV


def _one():
    """A stem with its entry tick and a 工 foot."""
    return (tate(382, CAP, 14)
            + [harai_l((378, CAP - 10), (196, 590), 72),
               yoko(140, 640, 0)]), FADV


def _two():
    return ([yoko(128, 636, CAP)]
            + tate(586, CAP + 16, 470, WT, head=False)
            + [kata(586, CAP + 16, WT),
               Stroke([("M", 566, 468), ("L", 140, 70)], 82,
                      [(0.0, 0.94), (0.5, 0.84), (1.0, 1.0)]),
               yoko(96, 676, 0)]), FADV


def _three():
    return ([yoko(120, 620, CAP)]
            + tate(576, CAP + 16, 452, WT, head=False)
            + [kata(576, CAP + 16, WT),
               yoko(214, 620, 430)]
            + tate(588, 430, 96, WT, head=False)
            + [kata(588, 430, WT), yoko(104, 640, 14)]), FADV


def _four():
    return ([harai_l((470, CAP), (104, 262), 78),
             yoko(76, 700, 250)]
            + tate(490, CAP, 12)), FADV


def _five():
    return ([yoko(160, 640, CAP)]
            + tate(210, CAP, 452)
            + [yoko(160, 626, 430)]
            + tate(594, 430, 96, WT, head=False)
            + [kata(594, 430, WT), yoko(110, 650, 14)]), FADV


def _six():
    return ([harai_l((606, CAP - 6), (188, 300), 84)]
            + ring(150, 646, 0, 404, 92, cx=0.24)), FADV


def _seven():
    return [
        yoko(96, 684, CAP),
        Stroke([("M", 636, CAP - 18), ("L", 366, 12)], 84,
               [(0.0, 1.0), (0.6, 0.86), (1.0, 0.50)]),
        yoko(232, 520, 430),
    ], FADV


def _eight():
    return (ring(188, 586, 424, CAP, 84, cx=0.24)
            + ring(140, 634, 0, 408, 92, cx=0.24)), FADV


def _nine():
    return (ring(128, 618, 386, CAP, 92, cx=0.24)
            + tate(568, 400, 14)), FADV


# ---------------------------------------------------------- PUNCTUATION

def _space():
    return [], 440


def _period():
    return [ten(176, 172, 92, -98, 92)], 400


def _comma():
    return [Stroke([("M", 216, 188), ("L", 116, -96)], 76, "hane")], 400


def _colon():
    return [ten(176, 172, 92, -98, 92), ten(176, 520, 92, -98, 92)], 400


def _semicolon():
    return [Stroke([("M", 216, 188), ("L", 116, -96)], 76, "hane"),
            ten(176, 520, 92, -98, 92)], 400


def _exclam():
    return (tate(280, CAP, 262, 92, "tate_tail", drift=-22)
            + [ten(228, 168, 92, -98, 92)]), 460


def _question():
    taper = [(0.0, 0.62), (1.0, 1.30)]
    return ([yoko(104, 536, CAP, flag=False)]
            + tate(486, CAP + 13, 512, WT, head=False)
            + [kata(486, CAP + 13, WT),
               Stroke([("M", 470, 528), ("L", 330, 384)], WC, taper)]
            + tate(324, 404, 222, 90, head=False)
            + [ten(268, 168, 92, -98, 92)]), 604


def _hyphen():
    return [yoko(110, 520, 340, 46)], 630


def _endash():
    return [yoko(70, 590, 340, 46)], 660


def _emdash():
    return [yoko(30, 970, 340, 46)], 1000


def _quotesingle():
    return [Stroke([("M", 186, CAP + 30), ("L", 130, 560)], 74,
                   "tate_tail")], 340


def _quotedbl():
    return [Stroke([("M", 156, CAP + 30), ("L", 100, 560)], 74, "tate_tail"),
            Stroke([("M", 372, CAP + 30), ("L", 316, 560)], 74,
                   "tate_tail")], 540


def _parenleft():
    return [Stroke([("M", 372, 860), ("L", 168, 540), ("L", 168, 80),
                    ("L", 372, -230)], 68, "uniform")], 460


def _parenright():
    return [Stroke([("M", 96, 860), ("L", 300, 540), ("L", 300, 80),
                    ("L", 96, -230)], 68, "uniform")], 460


def _slash():
    return [harai_l((520, 850), (120, -210), 76)], 640


def _backslash():
    return [harai_r((120, 850), (520, -210), 76)], 640


def _asterisk():
    return (tate(330, CAP, 470, 66, "tate_tail")
            + [harai_l((560, CAP - 40), (110, 520), 58),
               harai_r((110, CAP - 40), (560, 520), 58)]), 660


def _numbersign():
    """井"""
    return (tate(268, CAP, 20, 78, drift=-52)
            + tate(516, CAP, 20, 78, drift=-52)
            + [yoko(84, 690, 550, 48), yoko(70, 676, 260, 48)]), 764


def _dollar():
    """The 己 of S, run through by a stem."""
    return ([yoko(146, 590, 716, flag=False)]
            + tate(196, 716, 460, 92)
            + [yoko(146, 600, 432, flag=False)]
            + tate(552, 448, 150, 92, head=False)
            + [kata(552, 448, 92), yoko(112, 612, 104)]
            + [Stroke([("M", 368, 846), ("L", 362, -56)], 62, "uniform")]
            ), 716


def _percent():
    return (ring(96, 340, 470, CAP, 66, cx=0.24)
            + ring(400, 644, 10, 340, 66, cx=0.24)
            + [harai_l((620, CAP), (110, 4), 68)]), 740


def _ampersand():
    """A small 口 over a stem, a floor and a sweeping tail."""
    return (box(200, 512, 424, CAP, 84, WY)
            + tate(170, 416, 104, 92)
            + [yoko(120, 574, 16),
               harai_r((286, 296), (706, 6), 80)]), 764


def _at():
    """回, with the outer ring left open at the foot."""
    return (tate(146, 706, 70, 72)
            + [yoko(112, 648, 706, 44, flag=False), kata(602, 722, 72)]
            + tate(602, 722, 252, 72, head=False)
            + [yoko(112, 524, 70, 44)]
            + box(262, 496, 300, 502, 64, 38)), 764


def _plus():
    """十"""
    return [yoko(96, 668, 390, 48)] + tate(384, 690, 90, 82), 764


def _equal():
    """二"""
    return [yoko(96, 668, 520, 48), yoko(96, 668, 250, 48)], 764


def _less():
    return [harai_l((620, 640), (140, 372), 64),
            harai_r((140, 362), (620, 90), 64)], 700


def _greater():
    return [harai_r((120, 640), (600, 372), 64),
            harai_l((600, 362), (120, 90), 64)], 700


def _underscore():
    return [yoko(30, 660, -180, 52)], 690


def _asciicircum():
    return [harai_l((372, CAP + 20), (120, 500), 62),
            harai_r((384, CAP + 20), (636, 500), 62)], 756


def _grave():
    return [harai_r((150, CAP + 60), (350, 640), 70)], 460


def _bar():
    return [Stroke([("M", 250, 880), ("L", 250, -240)], 62, "uniform")], 500


def _bracketleft():
    """「"""
    return ([yoko(210, 470, 856, 48)]
            + tate(244, 862, -200, 68, head=False)
            + [yoko(210, 470, -200, 48)]), 490


def _bracketright():
    """」"""
    return ([yoko(50, 310, 856, 48)]
            + tate(276, 862, -200, 68, head=False)
            + [yoko(50, 310, -200, 48)]), 490


def _braceleft():
    return [Stroke([("M", 420, 858), ("L", 262, 796), ("L", 258, 400),
                    ("L", 130, 330), ("L", 258, 262), ("L", 262, -136),
                    ("L", 420, -200)], 56, "uniform")], 500


def _braceright():
    return [Stroke([("M", 80, 858), ("L", 238, 796), ("L", 242, 400),
                    ("L", 370, 330), ("L", 242, 262), ("L", 238, -136),
                    ("L", 80, -200)], 56, "uniform")], 500


def _asciitilde():
    return [Stroke([("M", 96, 330), ("L", 260, 440), ("L", 430, 250),
                    ("L", 600, 360)], 60, "uniform")], 700


def _ideographic_comma():
    """、"""
    return [Stroke([("M", 380, 420), ("L", 150, 120)], 92, "hane")], 1000


def _ideographic_full_stop():
    """。"""
    return ring(330, 590, 70, 330, 54, cx=0.26), 1000


# ---------------------------------------------------------------- table

_TABLE = {
    "A": (_A, 0x41), "B": (_B, 0x42), "C": (_C, 0x43), "D": (_D, 0x44),
    "E": (_E, 0x45), "F": (_F, 0x46), "G": (_G, 0x47), "H": (_H, 0x48),
    "I": (_I, 0x49), "J": (_J, 0x4A), "K": (_K, 0x4B), "L": (_L, 0x4C),
    "M": (_M, 0x4D), "N": (_N, 0x4E), "O": (_O, 0x4F), "P": (_P, 0x50),
    "Q": (_Q, 0x51), "R": (_R, 0x52), "S": (_S, 0x53), "T": (_T, 0x54),
    "U": (_U, 0x55), "V": (_V, 0x56), "W": (_W, 0x57), "X": (_X, 0x58),
    "Y": (_Y, 0x59), "Z": (_Z, 0x5A),

    "a": (_a, 0x61), "b": (_b, 0x62), "c": (_c, 0x63), "d": (_d, 0x64),
    "e": (_e, 0x65), "f": (_f, 0x66), "g": (_g, 0x67), "h": (_h, 0x68),
    "i": (_i, 0x69), "j": (_j, 0x6A), "k": (_k, 0x6B), "l": (_l, 0x6C),
    "m": (_m, 0x6D), "n": (_n, 0x6E), "o": (_o, 0x6F), "p": (_p, 0x70),
    "q": (_q, 0x71), "r": (_r, 0x72), "s": (_s, 0x73), "t": (_t, 0x74),
    "u": (_u, 0x75), "v": (_v, 0x76), "w": (_w, 0x77), "x": (_x, 0x78),
    "y": (_y, 0x79), "z": (_z, 0x7A),

    "zero": (_zero, 0x30), "one": (_one, 0x31), "two": (_two, 0x32),
    "three": (_three, 0x33), "four": (_four, 0x34), "five": (_five, 0x35),
    "six": (_six, 0x36), "seven": (_seven, 0x37), "eight": (_eight, 0x38),
    "nine": (_nine, 0x39),

    "space": (_space, 0x20),
    "period": (_period, 0x2E), "comma": (_comma, 0x2C),
    "colon": (_colon, 0x3A), "semicolon": (_semicolon, 0x3B),
    "exclam": (_exclam, 0x21), "question": (_question, 0x3F),
    "hyphen": (_hyphen, 0x2D), "endash": (_endash, 0x2013),
    "emdash": (_emdash, 0x2014),
    "quotesingle": (_quotesingle, 0x27), "quotedbl": (_quotedbl, 0x22),
    "parenleft": (_parenleft, 0x28), "parenright": (_parenright, 0x29),
    "slash": (_slash, 0x2F), "asterisk": (_asterisk, 0x2A),
    "numbersign": (_numbersign, 0x23), "dollar": (_dollar, 0x24),
    "percent": (_percent, 0x25), "ampersand": (_ampersand, 0x26),
    "at": (_at, 0x40), "plus": (_plus, 0x2B), "equal": (_equal, 0x3D),
    "less": (_less, 0x3C), "greater": (_greater, 0x3E),
    "underscore": (_underscore, 0x5F), "asciicircum": (_asciicircum, 0x5E),
    "grave": (_grave, 0x60), "backslash": (_backslash, 0x5C),
    "bar": (_bar, 0x7C), "bracketleft": (_bracketleft, 0x5B),
    "bracketright": (_bracketright, 0x5D),
    "braceleft": (_braceleft, 0x7B), "braceright": (_braceright, 0x7D),
    "asciitilde": (_asciitilde, 0x7E),
    "ideographiccomma": (_ideographic_comma, 0x3001),
    "ideographicfullstop": (_ideographic_full_stop, 0x3002),
}

ALL_NAMES = list(_TABLE.keys())
CMAP = {uni: name for name, (_, uni) in _TABLE.items()}
_BY_CHAR = {chr(uni): name for name, (_, uni) in _TABLE.items()}


def glyph(name):
    """Return (strokes, advance_width) for a glyph name."""
    return _TABLE[name][0]()


def char_to_name(ch):
    return _BY_CHAR.get(ch)
