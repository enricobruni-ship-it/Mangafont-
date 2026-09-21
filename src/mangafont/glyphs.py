"""The Latin alphabet.

Drawn in the stroke vocabulary of katakana -- the script Japanese uses
for foreign words -- rather than of kanji.  Four things carry the
resemblance:

  * sweeps -- katakana have so few strokes that each runs the width of
    the square and tapers to a needle, so every diagonal here is a 払い
    at katakana length, not a short Latin stroke;
  * the フ turn -- a hairline that meets a hard 肩 corner and sweeps
    away, which is how フ ア ク ス ヌ マ ワ ラ all begin.  7, 2, Z, z and
    J are built on it;
  * contrast -- 横画 are hairlines, 縦画 are slabs, at roughly 0.44;
  * fit -- the glyphs fill the square, with a very high x-height and
    tight, near-uniform side bearings.

Where a Latin letter has an exact kana or kanji counterpart it is drawn
as that character: X and x are メ, t is ナ, u is リ, l is レ, I is エ,
7 is フ, o is ロ.
"""

from .stroke import Stroke, kata, kihitsu, w_of
from . import stroke as _stroke
from .pen import (UPM, CAP, XH, ASC, DESC, ASCENDER, DESCENDER, wall,
                  WT, WY, WD, WC, RISE, L, R, ADV, FLAT,
                  yoko, yoko_in, tate, fold, box, ring, fusweep, sweep,
                  nobi, harai_l, harai_r, ten, hane)


# ---------------------------------------------------------------- CAPS

def _A():
    return [
        sweep((406, CAP), (58, 4)),
        harai_r((424, CAP - 22), (712, 4)),
        yoko(140, 636, 246),                      # crosses and overshoots
    ], ADV


def _B():
    return (tate(L + 50, CAP, 0)
            + fold(L, 636, CAP, 424)
            + [yoko(L, 664, 410)]
            + fold(L + 40, 690, 410, 0)
            + [yoko(L, 700, 0)]), ADV


def _C():
    """匚, finishing with the はね of ヒ."""
    return ([yoko(L, R, CAP)]
            + tate(L + 50, CAP, 40)
            + [hane([("M", L, 4), ("L", 648, 22), ("L", 716, 104)], 58)]), ADV


def _D():
    x1, dy = 690, 154
    rx = x1 - wall(WT)
    taper = [(0.0, w_of(WY) / w_of(WT)), (1.0, 1.0)]
    return (tate(L + wall(WT), CAP, 0)
            + [yoko(L, x1 - 96, CAP, flag=False),
               yoko(L, x1 - 96, 0, flag=False)]
            + tate(rx, CAP - dy + 6, dy, WT, head=False)
            + [Stroke([("M", x1 - 104, CAP + 4), ("L", rx, CAP - dy - 14)],
                      WT, taper, modulated=False),
               Stroke([("M", x1 - 104, 6), ("L", rx, dy + 14)], WT, taper,
                      modulated=False)]
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
    """フ, carried on into a hook."""
    rx = R - w_of(WT) * 0.5
    return ([yoko(140, R, CAP, flag=False), kata(rx, CAP + 17, WT)]
            + [hane([("M", rx, CAP + 17), ("L", 560, 168), ("L", 396, 38),
                     ("L", 186, 60), ("L", 144, 152)], 96)]), 740


def _K():
    return (tate(150, CAP, 0)
            + [sweep((704, CAP - 10), (88, 386), 82),
               harai_r((160, 446), (714, 2), 88)]), ADV


def _L():
    """乚"""
    return [
        hane([("M", 164, CAP), ("L", 158, 96), ("L", 268, 16),
              ("L", 640, 6), ("L", 706, 86)], 98),
        kihitsu(164, CAP, 98),
    ], 740


def _M():
    return (tate(124, CAP, 0) + tate(752, CAP, 0)
            + [sweep((130, CAP - 16), (420, 196), 82),
               sweep((746, CAP - 16), (444, 196), 82)]
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
               harai_r((150, 404), (712, 2), 86)]), ADV


def _S():
    """己 -- the fold chain, squared off."""
    return ([yoko(110, 678, CAP)]
            + tate(160, CAP, 470)
            + [yoko(110, 690, 424)]
            + tate(636, 424, 96, WT, head=False)
            + [kata(636, 424, WT),
               hane([("M", 76, 12), ("L", 596, 30), ("L", 700, 116)], 58)]), ADV


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
        sweep((108, CAP), (376, 8), 88),
        sweep((664, CAP), (396, 8), 88),
    ], ADV


def _W():
    return [
        sweep((92, CAP), (256, 8), 78),
        sweep((434, CAP - 20), (272, 8), 78),
        sweep((442, CAP - 20), (606, 8), 78),
        sweep((780, CAP), (620, 8), 78),
    ], 872


def _X():
    """乂"""
    return [
        sweep((694, CAP), (84, 2), 88),
        harai_r((94, CAP - 12), (694, 2), 88),
    ], ADV


def _Y():
    """丫"""
    return ([sweep((112, CAP), (362, 408), 84),
             sweep((662, CAP), (412, 408), 84)]
            + tate(386, 440, 10, WT, head=False)), ADV


def _Z():
    """乙"""
    """ス"""
    return fusweep(96, 690, CAP, 122, 18) + [yoko(76, 704, 0)], ADV


# ----------------------------------------------------------- LOWERCASE
# x-height 600 of a 790 cap: lowercase sits in a square, as kana do.
# Every arch is a 冂 fold, every bowl a 口.

LADV = 706


def _a():
    """A squared bowl whose floor runs past the stem and flicks up."""
    x0, x1 = 72, 556
    rx = x1 - wall(WT)
    return (tate(x0 + wall(WT), XH, 14)
            + [yoko(x0, x1, XH, flag=False), kata(rx, XH + 14, WT)]
            + tate(rx, XH + 14, 14, WT, head=False)
            + [hane([("M", x0, 12), ("L", 590, 30), ("L", 700, 104)], 58)]
            ), 744


def _b():
    return (tate(L + 50, ASC, 0)
            + fold(L, 592, 450, 0)
            + [yoko(L, 620, 0)]), LADV


def _c():
    """匚, with ヒ's flick."""
    return ([yoko(72, 636, XH)]
            + tate(122, XH, 40)
            + [hane([("M", 72, 4), ("L", 596, 22), ("L", 664, 100)], 54)]), 690


def _d():
    return (tate(592, ASC, 0)
            + [yoko(L, 620, 450)]
            + tate(L + 50, 464, 0)
            + [yoko(L, 620, 0)]), LADV


def _e():
    """The bowl closes at the top and opens at the foot.

    The hardest letter to hold at display weight: a crossbar splitting a
    bowl leaves two counters where every other letter has one.  So it is
    drawn wider than the rest of the lowercase, with a thinner bar.
    """
    return (tate(60 + wall(WT), XH, 46)
            + [yoko(60, 648, XH)]
            + tate(648 - wall(WT), XH + 18, 352, WT, head=False)
            + [kata(648 - wall(WT), XH + 18, WT),
               yoko(60, 676, 338, WY * 0.78),
               hane([("M", 60, 2), ("L", 620, 20), ("L", 710, 98)], 54)]), 744


def _f():
    """千 -- a stem, a flag, and a crossbar that runs past it."""
    return (tate(352, 832, 0)
            + [yoko(352, 606, 830, 44),
               yoko(84, 622, XH)]), 660


def _g():
    """The bowl's right stem carries straight on into the descender."""
    x0, x1 = 72, 556
    rx = x1 - wall(WT)
    return (tate(x0 + wall(WT), XH, 16)
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
            + [sweep((636, XH - 2), (88, 278), 78),
               harai_r((152, 332), (648, 2), 82)]), 672


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
            + [kata(556, 328, WT),
               hane([("M", 56, 8), ("L", 540, 26), ("L", 632, 106)], 54)]), 660


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
        sweep((104, XH), (322, 6), 82),
        sweep((584, XH), (340, 6), 82),
    ], 694


def _w():
    return [
        sweep((88, XH), (230, 6), 72),
        sweep((386, XH - 14), (244, 6), 72),
        sweep((394, XH - 14), (534, 6), 72),
        sweep((690, XH), (548, 6), 72),
    ], 786


def _x():
    """乂"""
    return [
        sweep((610, XH), (86, 2), 82),
        harai_r((94, XH - 10), (610, 2), 82),
    ], 700


def _y():
    """メ, with the second sweep carrying on into the descender."""
    return [
        sweep((104, XH), (376, 140), 82),
        hane([("M", 606, XH), ("L", 300, -46), ("L", 150, -152),
              ("L", 40, -120)], 82),
    ], 700


def _z():
    """乙"""
    """ス at x-height."""
    return fusweep(88, 616, XH, 116, 16) + [yoko(70, 640, 0)], 700


# -------------------------------------------------------------- FIGURES

FADV = 764


def _zero():
    return ring(120, 644, 0, CAP, cx=0.24), FADV


def _one():
    """A stem with its entry tick and a 工 foot."""
    return (tate(382, CAP, 14)
            + [sweep((382, CAP - 6), (186, 578), 74),
               yoko(140, 640, 0)]), FADV


def _two():
    """ス, but the knee drops into a stem first -- otherwise 2 and Z
    come out as the same drawing."""
    rx = 648 - w_of(WT) * 0.5
    return ([yoko(128, 648, CAP, flag=False), kata(rx, CAP + 16, WT)]
            + tate(rx, CAP + 16, 468, WT, head=False)
            + [sweep((rx - 8, 470), (146, 30), 84), yoko(96, 680, 0)]), FADV


def _three():
    return ([yoko(120, 620, CAP)]
            + tate(576, CAP + 16, 452, WT, head=False)
            + [kata(576, CAP + 16, WT),
               yoko(214, 620, 430)]
            + tate(588, 430, 96, WT, head=False)
            + [kata(588, 430, WT), yoko(104, 640, 14)]), FADV


def _four():
    return ([sweep((486, CAP), (96, 252), 80),
             yoko(76, 700, 250)]
            + tate(490, CAP, 12)), FADV


def _five():
    return ([yoko(160, 640, CAP)]
            + tate(210, CAP, 452)
            + [yoko(160, 626, 430)]
            + tate(594, 430, 96, WT, head=False)
            + [kata(594, 430, WT), yoko(110, 650, 14)]), FADV


def _six():
    return ([sweep((622, CAP - 2), (178, 288), 86)]
            + ring(150, 646, 0, 404, 92, cx=0.24)), FADV


def _seven():
    """フ -- the figure seven simply is this katakana."""
    return fusweep(96, 690, CAP, 330, 8) + [yoko(228, 524, 424)], FADV


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
    taper = [(0.0, w_of(WY) / w_of(WT)), (1.0, 1.0)]
    return ([yoko(104, 536, CAP, flag=False)]
            + tate(486, CAP + 13, 512, WT, head=False)
            + [kata(486, CAP + 13, WT),
               Stroke([("M", 470, 528), ("L", 330, 384)], WT, taper, modulated=False)]
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
    return [sweep((526, 856), (114, -216), 78)], 640


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
            + [sweep((628, CAP), (104, 0), 70)]), 740


def _ampersand():
    """The one Latin letter that already wants a 結び: a single stroke
    that crosses itself, the way あ ま ほ ね ぬ close."""
    return [
        hane([("M", 598, 660), ("L", 330, CAP), ("L", 168, 596),
              ("L", 330, 404), ("L", 566, 236), ("L", 372, 40),
              ("L", 176, 150), ("L", 214, 300)], 80, r=104, curl=0.24),
        harai_r((362, 296), (716, 4), 78),
    ], 764


def _at():
    """回, with the outer ring left open at the foot."""
    return (tate(146, 706, 70, 72)
            + [yoko(112, 648, 706, 44, flag=False), kata(602, 722, 72)]
            + tate(602, 722, 252, 72, head=False)
            + [yoko(112, 524, 70, 44)]
            + box(246, 516, 288, 516, 58, 36)), 764


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
    return ring(316, 604, 62, 350, 50, cx=0.26), 1000


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

from . import katakana as _kana                                  # noqa: E402

_KANA_NAMES = set(_kana.TABLE)
for _n, (_fn, _uni) in _kana.TABLE.items():
    _TABLE[_n] = (_fn, _uni)

ALL_NAMES = list(_TABLE.keys())
CMAP = {uni: name for name, (_, uni) in _TABLE.items()}
_BY_CHAR = {chr(uni): name for name, (_, uni) in _TABLE.items()}


def glyph(name):
    """Return (strokes, advance_width) for a glyph name, in the active cut."""
    if name in _KANA_NAMES:
        # Kana are full-width by definition: one em, no weight padding.
        return _TABLE[name][0](), _kana.KADV
    strokes, adv = _TABLE[name][0]()
    return strokes, adv + _stroke.ACTIVE.adv_pad


def char_to_name(ch):
    return _BY_CHAR.get(ch)
