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
from .pen import (UPM, CAP, XH, ASC, DESC, ASCENDER, DESCENDER, wall, SPUR,
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
        harai_r((392, 172), (700, -196), 80),
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
    """か -- a swept bowl and a stem that flicks away."""
    return [
        Stroke([("M", 468, 482), ("Q", 300, 566, 176, 470),
                ("Q", 62, 376, 130, 212), ("Q", 206, 34, 400, 60),
                ("Q", 470, 72, 486, 130)], WT * 1.02, "fude_in"),
        hane([("M", 506, XH + 20), ("Q", 486, 300, 498, 120),
              ("Q", 508, 26, 626, 62)], WT * 0.96),
    ], 700


def _b():
    """ほ -- an ascender with a bowl swung off its foot."""
    return (tate(140, ASC, 24, WT * 0.96, "tate_tail")
            + [Stroke([("M", 134, 404), ("Q", 320, 500, 452, 400),
                       ("Q", 570, 302, 486, 152), ("Q", 400, 18, 216, 58),
                       ("Q", 152, 74, 128, 116)], WT * 1.00, "fude_in")]), 660


def _c():
    """く, but the exit trails off rather than stopping."""
    return [
        Stroke([("M", 566, 508), ("Q", 360, 596, 200, 476),
                ("Q", 62, 366, 140, 196), ("Q", 220, 28, 430, 54),
                ("Q", 524, 72, 596, 158)], WT * 1.06, "fude"),
    ], 636


def _d():
    """た -- bowl swung off a descending ascender."""
    return (tate(524, ASC, 24, WT * 0.96, "tate_tail")
            + [Stroke([("M", 530, 404), ("Q", 344, 500, 212, 400),
                       ("Q", 94, 302, 178, 152), ("Q", 264, 18, 448, 58),
                       ("Q", 512, 74, 536, 116)], WT * 1.00, "fude_in")]), 660


def _e():
    """え -- a bar, then a stroke that curls under and sweeps out."""
    return [
        yoko(96, 542, 340, WY * 0.9),
        Stroke([("M", 520, 470), ("Q", 340, 588, 184, 478),
                ("Q", 58, 376, 134, 208), ("Q", 218, 30, 430, 62),
                ("Q", 542, 84, 594, 176)], WT * 1.02, "fude"),
    ], 648


def _f():
    """千's flag and crossbar, on a stem that sweeps away like り."""
    return [
        Stroke([("M", 366, 836), ("Q", 366, 470, 364, 186),
                ("Q", 362, 100, 314, 66), ("Q", 276, 40, 232, 46)],
               WT * 0.94, "ri"),
        yoko(366, 610, 828, WY * 0.96),
        yoko(92, 626, XH),
    ], 616


def _g():
    """が -- bowl, then a descender that swings away."""
    return [
        Stroke([("M", 470, 470), ("Q", 300, 562, 176, 466),
                ("Q", 62, 372, 130, 210), ("Q", 206, 32, 400, 58),
                ("Q", 468, 70, 486, 126)], WT * 1.02, "fude_in"),
        Stroke([("M", 508, XH + 18), ("Q", 502, 260, 496, -120),
                ("Q", 490, -222, 432, -258), ("Q", 386, -288, 338, -280)],
               WT * 0.94, "ri"),
    ], 700


def _h():
    """は -- an ascender with a shoulder that springs and falls away."""
    return (tate(140, ASC, 0, WT * 0.96)
            + [Stroke([("M", 128, 318), ("Q", 190, 556, 372, 560),
                       ("Q", 540, 564, 548, 330), ("Q", 552, 170, 540, 14)],
                      WT * 1.02, "fude_in")]), 664


def _i():
    return (tate(206, XH, 10)
            + [ten(150, 800)]), 430


def _j():
    """り carried below the line."""
    return [
        Stroke([("M", 300, XH), ("Q", 300, 220, 298, -120),
                ("Q", 296, -210, 246, -244), ("Q", 208, -272, 164, -266)],
               WT * 0.94, "ri"),
        ten(238, 792),
    ], 440


def _k():
    return (tate(150, ASC, 0)
            + [sweep((636, XH - 2), (88, 278), 78, amount=0.105),
               harai_r((152, 332), (648, 2), 82)]), 672


def _l():
    """り -- and り is not レ.

    レ turns a corner and fires off.  り never corners: the stem holds
    vertical, bows late, and the brush leaves.  Two things have to be
    true at once.  The hook must COMPLETE ITS TURN -- an earlier cut had
    no kink in it and still read as angular, because it stopped near
    -150 degrees, still travelling diagonally.  And the RADIUS must stay
    small: completing that turn over a wide arc puts stem and hook on
    one slant and the eye reads a diagonal.  Vertical for the top ~78%,
    then a tight quarter turn at the foot.
    """
    return [
        Stroke([("M", 268, ASC), ("Q", 268, 420, 266, 190),
                ("Q", 264, 96, 214, 62), ("Q", 176, 36, 132, 40)],
               WT * 0.96, "ri"),
    ], 452


def _m():
    """two shoulders, each springing and falling."""
    return (tate(118, XH, 0, WT * 0.94)
            + [Stroke([("M", 108, 326), ("Q", 164, 556, 320, 560),
                       ("Q", 468, 564, 476, 334), ("Q", 480, 176, 470, 14)],
                      WT * 1.00, "fude_in"),
               Stroke([("M", 466, 340), ("Q", 518, 558, 672, 562),
                       ("Q", 820, 566, 828, 336), ("Q", 832, 176, 822, 14)],
                      WT * 1.00, "fude_in")]), 950


def _n():
    """の's shoulder: it springs off the stem and falls away, rather than
    turning a corner."""
    return (tate(124, XH, 0, WT * 0.94)
            + [Stroke([("M", 114, 322), ("Q", 174, 556, 350, 560),
                       ("Q", 520, 564, 528, 330), ("Q", 532, 172, 520, 14)],
                      WT * 1.02, "fude_in")]), 650


def _o():
    """の -- two swept halves, not a chamfered box."""
    return [
        Stroke([("M", 356, 566), ("Q", 170, 552, 106, 380),
                ("Q", 48, 194, 210, 74), ("Q", 300, 20, 370, 16)],
               WT * 1.02, "fude_in"),
        Stroke([("M", 352, 566), ("Q", 540, 552, 604, 380),
                ("Q", 662, 194, 500, 74), ("Q", 410, 20, 346, 16)],
               WT * 1.02, "fude_in"),
    ], 712


def _p():
    """bowl swung off a descending stem."""
    return (tate(140, XH, DESC, WT * 0.96, "tate_tail")
            + [Stroke([("M", 134, 448), ("Q", 320, 552, 456, 448),
                       ("Q", 578, 344, 490, 182), ("Q", 400, 40, 214, 84),
                       ("Q", 152, 100, 128, 144)], WT * 1.00, "fude_in")]), 664


def _q():
    """the mirror of p."""
    return (tate(524, XH, DESC, WT * 0.96, "tate_tail")
            + [Stroke([("M", 530, 448), ("Q", 344, 552, 208, 448),
                       ("Q", 86, 344, 174, 182), ("Q", 264, 40, 450, 84),
                       ("Q", 512, 100, 536, 144)], WT * 1.00, "fude_in")]), 664


def _r():
    """ら -- a stem and an arm that lifts away."""
    return (tate(124, XH, 0, WT * 0.94)
            + [Stroke([("M", 114, 340), ("Q", 190, 566, 368, 558),
                       ("Q", 460, 552, 504, 486)], WT * 1.02, "fude")]), 512


def _s():
    """ろ -- one flowing stroke that changes its mind twice."""
    return [
        Stroke([("M", 530, 500), ("Q", 400, 590, 236, 548),
                ("Q", 110, 514, 214, 424), ("Q", 320, 336, 452, 282),
                ("Q", 566, 232, 472, 118), ("Q", 372, 12, 190, 68),
                ("Q", 114, 92, 86, 148)], WT * 1.00, "fude"),
    ], 600


def _t():
    """り carrying 十's crossbar."""
    return [
        Stroke([("M", 362, 788), ("Q", 362, 440, 360, 180),
                ("Q", 358, 96, 310, 64), ("Q", 272, 38, 228, 44)],
               WT * 0.94, "ri"),
        yoko(96, 612, XH),
    ], 586


def _u():
    """う -- the left stroke swings through the floor and up."""
    return ([Stroke([("M", 128, XH), ("Q", 116, 256, 152, 130),
                     ("Q", 216, -14, 400, 46), ("Q", 500, 82, 520, 210)],
                    WT * 1.02, "fude_in")]
            + tate(536, XH, 0, WT * 0.94, "tate_tail")), 672


def _v():
    return [
        sweep((104, XH), (322, 6), 82, amount=0.10),
        sweep((584, XH), (340, 6), 82, amount=-0.10),
    ], 694


def _w():
    return [
        sweep((88, XH), (230, 6), 72, amount=0.10),
        sweep((386, XH - 14), (244, 6), 72, amount=-0.10),
        sweep((394, XH - 14), (534, 6), 72, amount=0.10),
        sweep((690, XH), (548, 6), 72, amount=-0.10),
    ], 786


def _x():
    """乂"""
    return [
        sweep((610, XH), (86, 2), 82, amount=0.09),
        harai_r((94, XH - 10), (610, 2), 82),
    ], 700


def _y():
    """メ, with the second sweep carrying on into the descender."""
    return [
        sweep((104, XH), (376, 140), 82, amount=0.09),
        Stroke([("M", 606, XH), ("Q", 448, -14, 318, -152),
                ("Q", 258, -216, 200, -230), ("Q", 150, -242, 116, -222)],
               WT * 0.82, "ri"),
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


# ---------------------------------------------------------------- はね
#
# Hiragana ends a stroke three ways: 止め a stop, はね a flick back up,
# 払い a sweep away.  Every terminal in the lowercase used to be a stop,
# which is a large part of why it read as mechanical -- the letters had
# been redrawn on curves while still finishing like boxes.  These flick
# the way い and け do.
#
# The wrapping happens HERE, on the table, rather than around glyph().
# glyph() switches to the lowercase cut, calls the function, and switches
# back; a Stroke captures gain, ornament scale and overshoot at
# CONSTRUCTION.  Building the flick outside that window hands it the
# capitals' cut -- gain 1.40 against the lowercase's 0.70, which turns a
# kana_out terminal (0.30) into 0.02 rather than 0.51, a 5-unit needle
# where a 94-unit taper belongs.

_FLICK = {"n": (150, 118, 0.86), "m": (150, 118, 0.86), "h": (150, 118, 0.86),
          "i": (138, 112, 0.80), "d": (150, 118, 0.86), "u": (128, 96, 0.78),
          "a": (140, 104, 0.82), "r": (132, 100, 0.80)}


def _with_flick(fn, dx, dy, wm):
    """Spring a はね off whichever stroke finishes lowest."""
    def wrapped():
        strokes, adv = fn()
        best, besty = None, 1e9
        for st in strokes:
            if not hasattr(st, "path"):
                continue
            end = _stroke.flatten(st.path)[-1]
            if end[1] < besty:
                best, besty = st, end[1]
        if best is None or besty > 110:
            return strokes, adv
        x, y = _stroke.flatten(best.path)[-1]
        # Pulling the control well along x and low in y bends the flick
        # instead of firing it off straight -- the same "finish the turn"
        # point as the り hooks.
        tick = Stroke([("M", x, y),
                       ("Q", x + dx * 0.74, y + dy * 0.14, x + dx, y + dy)],
                      WT * wm, "kana_out")
        return strokes + [tick], max(adv, int(x + dx) + 40)
    return wrapped


for _ch, (_dx, _dy, _wm) in _FLICK.items():
    _TABLE[_ch] = (_with_flick(_TABLE[_ch][0], _dx, _dy, _wm), _TABLE[_ch][1])

ALL_NAMES = list(_TABLE.keys())
CMAP = {uni: name for name, (_, uni) in _TABLE.items()}
_BY_CHAR = {chr(uni): name for name, (_, uni) in _TABLE.items()}


_LOWER = set("abcdefghijklmnopqrstuvwxyz")


def glyph(name):
    """Return (strokes, advance_width) for a glyph name, in the active cut.

    A cut may carry a second spec for the lowercase (`Weight.lower`); a
    glyph is then drawn under whichever spec belongs to its case.  Widths
    are baked in when a Stroke is constructed, so switching the active
    cut around the call is all it takes.
    """
    if name in _KANA_NAMES:
        # Kana are full-width by definition: one em, no weight padding.
        return _TABLE[name][0](), _kana.KADV

    cut = _stroke.ACTIVE
    sub = getattr(cut, "lower", None)
    if sub is not None and name in _LOWER:
        _stroke.set_weight(sub)
        try:
            strokes, adv = _TABLE[name][0]()
        finally:
            _stroke.set_weight(cut)
        return strokes, adv + sub.adv_pad

    strokes, adv = _TABLE[name][0]()
    return strokes, adv + cut.adv_pad


def char_to_name(ch):
    return _BY_CHAR.get(ch)
