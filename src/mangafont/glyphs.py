"""Glyph skeletons.

Every letter is assembled from the stroke vocabulary of Japanese writing
-- 横画, 縦画, 折れ, 払い, はね, 点 -- laid into a notional square the way
a kanji is.  Horizontals rise to the right, verticals are plumb, curves
are reduced to chamfered knees, and counters are squared.
"""

from .stroke import Stroke

# ------------------------------------------------------------- metrics

UPM = 1000
CAP = 700          # cap height / figure height
XH = 470           # x-height (kept low, so lowercase sits in a square)
ASC = 726          # ascender letters: b d f h k l
DESC = -186        # descender letters: g j p q y
ASCENDER = 800     # font-wide ascent
DESCENDER = -200

WT = 66            # 縦画  vertical stem
WY = 52            # 横画  horizontal (thinner -- Mincho-style contrast)
WD = 60            # diagonal

RISE = 0.038       # horizontals climb ~2 degrees to the right


# ----------------------------------------------------------- shorthands

def yoko(x0, x1, y, w=WY, rise=None, prof="yoko"):
    """横画 -- a horizontal, tilted up to the right."""
    r = (x1 - x0) * (RISE if rise is None else rise)
    return Stroke([("M", x0, y), ("L", x1, y + r)], w, prof)


def tate(x, y0, y1, w=WT, prof="tate", drift=-8):
    """縦画 -- a vertical, drifting very slightly left as it descends."""
    return Stroke([("M", x, y0), ("L", x + drift, y1)], w, prof)


def ring(x0, x1, yb, yt, w=WD, chamfer=0.30, knee=0.22, prof="ore"):
    """A squared-off ring: the 口 / 回 counter, corners cut like a brush.

    Written as two strokes meeting at top-centre and bottom-centre, the
    way 口 is built from 竖 + 横折 + 横.
    """
    xm = (x0 + x1) * 0.5
    cx = (x1 - x0) * chamfer
    cy = (yt - yb) * knee
    r = (x1 - x0) * RISE * 0.5
    ov = (x1 - x0) * 0.13          # halves run past centre so the seam closes
    left = Stroke([("M", xm + ov, yt + r * 0.5), ("L", x0 + cx, yt - r * 0.2),
                   ("L", x0, yt - cy), ("L", x0, yb + cy),
                   ("L", x0 + cx, yb - r * 0.2), ("L", xm + ov, yb)],
                  w, prof, cap_start=0.0, cap_end=0.0,
                  uroko_start=(0.0, 0.0), uroko_end=(0.0, 0.0))
    right = Stroke([("M", xm - ov, yt + r * 0.5), ("L", x1 - cx, yt + r),
                    ("L", x1, yt - cy + r), ("L", x1, yb + cy + r),
                    ("L", x1 - cx, yb + r), ("L", xm - ov, yb)],
                   w, prof, cap_start=0.0, cap_end=0.0,
                   uroko_start=(0.0, 0.0), uroko_end=(0.0, 0.0))
    return [left, right]


def ten(x, y, dx=66, dy=-68, w=64):
    """点 -- the brush tick, landing as it travels down-right."""
    return Stroke([("M", x, y), ("L", x + dx, y + dy)], w, "ten")


# ---------------------------------------------------------------- CAPS
# Cap frame: x 86..548, y 0..700.

def _A():
    return [
        Stroke([("M", 332, 700), ("Q", 236, 352, 92, 10)], WD, "harai_l"),
        Stroke([("M", 344, 690), ("Q", 436, 344, 548, 6)], WD, "harai_r"),
        yoko(160, 478, 234, WY * 0.94),
    ], 632


def _B():
    return [
        tate(140, 700, 6),
        Stroke([("M", 156, 700), ("L", 414, 712), ("Q", 450, 708, 448, 648),
                ("L", 442, 380)], 56, "ore"),
        yoko(134, 488, 356, 50),
        tate(492, 368, 44, 58),
        yoko(132, 502, 6, 54),
    ], 652


def _C():
    return [
        yoko(150, 500, 694),
        Stroke([("M", 152, 700), ("Q", 96, 688, 94, 430), ("L", 98, 176),
                ("Q", 102, 58, 208, 42), ("L", 466, 26), ("L", 526, 78)],
               WD, "hane"),
    ], 634


def _D():
    return [
        tate(140, 700, 6),
        Stroke([("M", 156, 700), ("L", 380, 710), ("Q", 500, 700, 508, 470),
                ("L", 510, 236), ("Q", 506, 40, 380, 22), ("L", 132, 10)],
               58, "ore"),
    ], 648


def _E():
    return [
        tate(140, 700, 6),
        yoko(130, 498, 692),
        yoko(134, 452, 354, 50),
        yoko(130, 512, 10, 54),
    ], 624


def _F():
    return [
        tate(140, 700, 6),
        yoko(130, 498, 692),
        yoko(134, 456, 354, 50),
    ], 600


def _G():
    return [
        yoko(150, 500, 694),
        Stroke([("M", 152, 700), ("Q", 96, 688, 94, 430), ("L", 98, 176),
                ("Q", 102, 58, 208, 42), ("L", 432, 28),
                ("Q", 520, 34, 518, 112), ("L", 516, 254)], 60, "ore"),
        yoko(356, 532, 266, 50),
    ], 650


def _H():
    return [
        tate(136, 700, 6),
        tate(508, 700, 6),
        yoko(126, 512, 350),
    ], 648


def _I():
    """Built like 工 -- the square asks for the slab bars."""
    return [
        yoko(96, 412, 692),
        tate(258, 700, 18),
        yoko(78, 430, 10, 54),
    ], 508


def _J():
    return [
        yoko(198, 488, 692, 50),
        Stroke([("M", 420, 700), ("L", 412, 182), ("Q", 408, 50, 298, 40),
                ("Q", 194, 34, 166, 124)], 64, "hane"),
    ], 604


def _K():
    return [
        tate(140, 700, 6),
        Stroke([("M", 516, 690), ("Q", 366, 520, 108, 332)], 56, "harai_l"),
        Stroke([("M", 156, 404), ("Q", 372, 212, 544, 8)], WD, "harai_r"),
    ], 642


def _L():
    """乚 -- one stroke, turning and flicking up."""
    return [
        Stroke([("M", 148, 700), ("L", 140, 140), ("Q", 140, 36, 250, 28),
                ("L", 452, 16), ("L", 518, 68)], WT, "hane"),
    ], 592


def _M():
    return [
        tate(122, 700, 6, 64),
        tate(620, 700, 6, 64),
        Stroke([("M", 126, 688), ("L", 366, 296)], 58, "diag"),
        Stroke([("M", 614, 688), ("L", 374, 296)], 58, "diag"),
    ], 760


def _N():
    return [
        tate(128, 700, 6, 64),
        tate(514, 700, 6, 64),
        Stroke([("M", 134, 686), ("L", 512, 58)], 58,
               [(0.0, 1.10), (0.50, 0.90), (1.00, 1.02)]),
    ], 654


def _O():
    return ring(92, 546, 6, 700, WD), 662


def _P():
    return [
        tate(140, 700, 6),
        Stroke([("M", 156, 700), ("L", 420, 712), ("Q", 480, 708, 482, 640),
                ("L", 480, 404), ("Q", 478, 340, 418, 336), ("L", 134, 324)],
               56, "ore"),
    ], 628


def _Q():
    return ring(92, 546, 6, 700, WD) + [
        Stroke([("M", 348, 158), ("Q", 452, 64, 566, -68)], 56, "harai_r"),
    ], 662


def _R():
    return [
        tate(140, 700, 6),
        Stroke([("M", 156, 700), ("L", 420, 712), ("Q", 480, 708, 482, 640),
                ("L", 480, 404), ("Q", 478, 340, 418, 336), ("L", 134, 324)],
               56, "ore"),
        Stroke([("M", 182, 330), ("Q", 396, 172, 540, 4)], 58, "harai_r"),
    ], 644


def _S():
    return [
        Stroke([("M", 506, 630), ("Q", 498, 704, 396, 710), ("L", 188, 700),
                ("Q", 98, 694, 100, 600), ("Q", 102, 514, 214, 472),
                ("L", 408, 400), ("Q", 514, 360, 510, 262),
                ("Q", 504, 38, 158, 42), ("Q", 92, 46, 90, 122)],
               62, "sori"),
    ], 628


def _T():
    return [
        yoko(86, 546, 692, 54),
        tate(324, 700, 10),
    ], 634


def _U():
    return [
        Stroke([("M", 138, 700), ("L", 132, 170), ("Q", 132, 40, 250, 32),
                ("L", 356, 28), ("Q", 476, 26, 486, 190)], 64, "ore"),
        tate(504, 700, 176, 64),
    ], 648


def _V():
    return [
        Stroke([("M", 106, 700), ("Q", 196, 356, 314, 12)], 62, "diag"),
        Stroke([("M", 540, 700), ("Q", 450, 356, 330, 12)], 62, "diag"),
    ], 648


def _W():
    return [
        Stroke([("M", 92, 700), ("Q", 146, 356, 216, 12)], 56, "diag"),
        Stroke([("M", 388, 688), ("Q", 330, 348, 228, 12)], 56, "diag"),
        Stroke([("M", 398, 688), ("Q", 454, 348, 558, 12)], 56, "diag"),
        Stroke([("M", 698, 700), ("Q", 642, 356, 570, 12)], 56, "diag"),
    ], 800


def _X():
    """乂 -- 左払い crossed by 右払い."""
    return [
        Stroke([("M", 542, 700), ("Q", 332, 352, 106, 8)], 60, "harai_l"),
        Stroke([("M", 118, 690), ("Q", 328, 350, 530, 10)], 60, "harai_r"),
    ], 650


def _Y():
    """丫"""
    return [
        Stroke([("M", 112, 700), ("Q", 202, 540, 310, 382)], 58, "diag"),
        Stroke([("M", 540, 700), ("Q", 448, 540, 338, 382)], 58, "diag"),
        tate(326, 402, 10),
    ], 644


def _Z():
    return [
        yoko(112, 518, 690),
        Stroke([("M", 500, 698), ("Q", 330, 378, 124, 32)], 58,
               [(0.0, 0.92), (0.50, 0.80), (1.00, 0.96)]),
        yoko(104, 534, 12, 54),
    ], 644


# ----------------------------------------------------------- LOWERCASE
# Lowercase leans on hiragana: fewer strokes, more flicks, open forms.

def _a():
    """Single-storey: a squared ring plus a stem that flicks away (か)."""
    return ring(104, 398, 14, XH, 58) + [
        Stroke([("M", 442, 468), ("L", 434, 92), ("Q", 438, 18, 528, 32)],
               62, "hane"),
    ], 592


def _b():
    return [
        tate(140, ASC, 8),
        Stroke([("M", 158, 452), ("L", 334, 470), ("Q", 470, 466, 476, 332),
                ("L", 476, 162), ("Q", 472, 38, 338, 24), ("L", 134, 10)],
               58, "ore"),
    ], 612


def _c():
    return [
        yoko(162, 478, 452, 50),
        Stroke([("M", 164, 458), ("Q", 112, 446, 110, 320), ("L", 112, 164),
                ("Q", 116, 44, 214, 32), ("L", 452, 18), ("L", 508, 66)],
               60, "hane"),
    ], 596


def _d():
    return [
        tate(468, ASC, 8),
        Stroke([("M", 466, 452), ("L", 264, 470), ("Q", 128, 466, 122, 332),
                ("L", 122, 162), ("Q", 126, 38, 260, 24), ("L", 464, 10)],
               58, "ore"),
    ], 612


def _e():
    """え -- crossbar first, then the sweep that flicks out."""
    return [
        yoko(118, 444, 268, 50),
        Stroke([("M", 474, 366), ("Q", 454, 466, 300, 470),
                ("Q", 136, 472, 124, 318), ("L", 126, 178),
                ("Q", 130, 44, 250, 30), ("L", 418, 20), ("L", 492, 70)],
               58, "sori"),
    ], 606


def _f():
    return [
        Stroke([("M", 470, 646), ("Q", 466, 722, 382, 724),
                ("Q", 298, 726, 296, 638), ("L", 286, 10)], 62, "tate"),
        yoko(120, 452, 452, 50),
    ], 562


def _g():
    return ring(106, 412, 14, XH, 58) + [
        Stroke([("M", 452, 468), ("L", 444, 28), ("Q", 440, -150, 296, -160),
                ("Q", 196, -166, 162, -96)], 62, "hane"),
    ], 600


def _h():
    return [
        tate(140, ASC, 8),
        Stroke([("M", 142, 320), ("Q", 152, 472, 290, 474),
                ("Q", 430, 476, 434, 332), ("L", 428, 10)], 58, "arch"),
    ], 618


def _i():
    return [
        tate(180, XH, 12, 64),
        ten(142, 656),
    ], 366


def _j():
    return [
        Stroke([("M", 240, XH), ("L", 232, 10), ("Q", 228, -150, 112, -158),
                ("Q", 50, -162, 26, -108)], 62, "hane"),
        ten(200, 656),
    ], 376


def _k():
    return [
        tate(140, ASC, 8),
        Stroke([("M", 470, 452), ("Q", 336, 360, 108, 250)], 56, "harai_l"),
        Stroke([("M", 152, 300), ("Q", 336, 164, 490, 6)], 58, "harai_r"),
    ], 586


def _l():
    """レ -- the ascender turns and flicks, so it never reads as I (工)."""
    return [
        Stroke([("M", 198, ASC), ("L", 190, 130), ("Q", 190, 34, 286, 28),
                ("L", 356, 24)], 64, "hane"),
    ], 406


def _m():
    return [
        tate(126, XH, 10, 62),
        Stroke([("M", 130, 320), ("Q", 140, 472, 262, 474),
                ("Q", 386, 476, 390, 332), ("L", 384, 10)], 58, "arch"),
        Stroke([("M", 388, 332), ("Q", 398, 474, 520, 474),
                ("Q", 644, 476, 648, 332), ("L", 642, 10)], 58, "arch"),
    ], 772


def _n():
    return [
        tate(140, XH, 10, 62),
        Stroke([("M", 142, 320), ("Q", 152, 472, 290, 474),
                ("Q", 430, 476, 434, 332), ("L", 428, 10)], 58, "arch"),
    ], 618


def _o():
    return ring(112, 494, 14, XH, 60), 608


def _p():
    return [
        tate(140, XH, DESC, 64),
        Stroke([("M", 158, 452), ("L", 330, 470), ("Q", 466, 466, 472, 334),
                ("L", 472, 170), ("Q", 468, 46, 334, 32), ("L", 134, 18)],
               58, "ore"),
    ], 612


def _q():
    return [
        Stroke([("M", 468, XH), ("L", 458, -128), ("Q", 460, -184, 542, -170)],
               64, "hane"),
        Stroke([("M", 466, 452), ("L", 268, 470), ("Q", 132, 466, 126, 334),
                ("L", 126, 170), ("Q", 130, 46, 264, 32), ("L", 464, 18)],
               58, "ore"),
    ], 612


def _r():
    """The arm flicks up and away, like the tail of り."""
    return [
        tate(140, XH, 10, 62),
        Stroke([("M", 142, 322), ("Q", 156, 474, 306, 476), ("L", 396, 470),
                ("L", 456, 520)], 56, "hane", cap_start=0.0,
               uroko_start=(0.0, 0.0)),
    ], 474


def _s():
    return [
        Stroke([("M", 452, 388), ("Q", 446, 466, 354, 470), ("L", 184, 462),
                ("Q", 110, 458, 112, 392), ("Q", 114, 330, 204, 300),
                ("L", 386, 246), ("Q", 466, 216, 462, 148),
                ("Q", 458, 22, 196, 26), ("Q", 112, 28, 110, 88)],
               58, "sori"),
    ], 574


def _t():
    """十 / ナ -- the crossbar and a stem that turns at the foot."""
    return [
        Stroke([("M", 250, 640), ("L", 242, 118), ("Q", 242, 30, 330, 26),
                ("L", 396, 22)], 62, "hane"),
        yoko(96, 430, 452, 50),
    ], 524


def _u():
    """り -- left stroke turns along the floor, right stem drops beside it."""
    return [
        Stroke([("M", 140, XH), ("L", 132, 140), ("Q", 132, 40, 246, 32),
                ("L", 336, 28), ("Q", 442, 26, 450, 170)], 62, "hane"),
        tate(454, XH, 12, 62),
    ], 618


def _v():
    return [
        Stroke([("M", 104, XH), ("Q", 184, 248, 288, 14)], 58, "diag"),
        Stroke([("M", 492, XH), ("Q", 414, 248, 300, 14)], 58, "diag"),
    ], 600


def _w():
    return [
        Stroke([("M", 96, XH), ("Q", 140, 246, 200, 14)], 54, "diag"),
        Stroke([("M", 340, 462), ("Q", 298, 240, 210, 14)], 54, "diag"),
        Stroke([("M", 348, 462), ("Q", 392, 240, 482, 14)], 54, "diag"),
        Stroke([("M", 596, XH), ("Q", 552, 246, 492, 14)], 54, "diag"),
    ], 696


def _x():
    return [
        Stroke([("M", 492, XH), ("Q", 300, 246, 104, 10)], 56, "harai_l"),
        Stroke([("M", 112, 462), ("Q", 300, 246, 484, 12)], 56, "harai_r"),
    ], 600


def _y():
    """メ with a tail: the second sweep carries on into the descender."""
    return [
        Stroke([("M", 104, XH), ("Q", 192, 288, 294, 100)], 58, "diag"),
        Stroke([("M", 496, XH), ("Q", 398, 196, 288, -44),
                ("Q", 240, -150, 110, -136)], 58, "hane"),
    ], 600


def _z():
    return [
        yoko(114, 488, 452, 50),
        Stroke([("M", 470, 462), ("Q", 300, 240, 124, 32)], 56,
               [(0.0, 0.92), (0.50, 0.80), (1.00, 0.96)]),
        yoko(106, 506, 14, 52),
    ], 600


# -------------------------------------------------------------- FIGURES
# Tabular: every figure advances 636.

FIG_ADV = 636


def _zero():
    return ring(126, 508, 6, CAP, WD), FIG_ADV


def _one():
    return [
        tate(306, 700, 18),
        Stroke([("M", 300, 694), ("Q", 240, 650, 156, 602)], 54, "harai_l"),
        yoko(146, 470, 12, 52),
    ], FIG_ADV


def _two():
    return [
        Stroke([("M", 124, 594), ("Q", 132, 704, 268, 710),
                ("Q", 424, 714, 430, 596), ("Q", 434, 492, 298, 372),
                ("L", 128, 34)], 58, "ore"),
        yoko(108, 522, 14, 54),
    ], FIG_ADV


def _three():
    return [
        Stroke([("M", 140, 676), ("L", 300, 690), ("Q", 452, 694, 456, 562),
                ("Q", 458, 464, 316, 400)], 56, "ore"),
        Stroke([("M", 246, 394), ("L", 356, 398), ("Q", 512, 392, 508, 218),
                ("Q", 504, 44, 318, 30), ("Q", 174, 20, 136, 98)],
               58, "hane"),
    ], FIG_ADV


def _four():
    return [
        Stroke([("M", 386, 700), ("Q", 250, 418, 110, 212)], 56,
               [(0.0, 1.02), (1.00, 0.82)]),
        yoko(94, 524, 208, 54),
        tate(404, 700, 12, 62),
    ], FIG_ADV


def _five():
    return [
        yoko(166, 520, 690, 52),
        tate(168, 696, 398, 62),
        Stroke([("M", 152, 402), ("L", 330, 394), ("Q", 492, 388, 496, 236),
                ("Q", 500, 48, 320, 32), ("Q", 178, 20, 140, 96)],
               58, "hane"),
    ], FIG_ADV


def _six():
    return [
        Stroke([("M", 470, 694), ("Q", 258, 616, 172, 400),
                ("Q", 134, 302, 134, 202)], 58,
               [(0.0, 0.96), (0.55, 0.92), (1.00, 1.00)]),
    ] + ring(120, 502, 8, 340, 58), FIG_ADV


def _seven():
    return [
        yoko(102, 524, 690, 54),
        Stroke([("M", 500, 700), ("Q", 382, 396, 300, 12)], 58,
               [(0.0, 1.00), (0.60, 0.86), (1.00, 0.52)]),
        yoko(190, 406, 330, 46),
    ], FIG_ADV


def _eight():
    return (ring(160, 472, 380, CAP, 56, knee=0.24)
            + ring(126, 506, 6, 366, 58, knee=0.24)), FIG_ADV


def _nine():
    return ring(126, 490, 366, CAP, 58) + [
        Stroke([("M", 490, 686), ("L", 480, 104), ("Q", 476, 24, 388, 18),
                ("L", 268, 12)], 62, "hane"),
    ], FIG_ADV


# ---------------------------------------------------------- PUNCTUATION

def _space():
    return [], 430


def _period():
    return [ten(146, 142, 74, -76, 80)], 340


def _comma():
    return [Stroke([("M", 186, 146), ("Q", 176, 44, 96, -72)], 58, "hane")], 340


def _colon():
    return [ten(146, 142, 74, -76, 80), ten(146, 434, 74, -76, 80)], 340


def _semicolon():
    return [Stroke([("M", 186, 146), ("Q", 176, 44, 96, -72)], 58, "hane"),
            ten(146, 434, 74, -76, 80)], 340


def _exclam():
    return [
        tate(252, 700, 216, 74, "tate_tail", drift=-14),
        ten(212, 136, 74, -76, 80),
    ], 400


def _question():
    return [
        Stroke([("M", 92, 588), ("Q", 96, 700, 236, 706),
                ("Q", 384, 710, 388, 592), ("Q", 390, 496, 280, 424),
                ("Q", 226, 388, 224, 286)], 58, "ore"),
        ten(192, 152, 74, -76, 80),
    ], 500


def _hyphen():
    return [yoko(98, 422, 300, 54)], 520


def _endash():
    return [yoko(70, 490, 300, 54)], 560


def _emdash():
    return [yoko(40, 960, 300, 54)], 1000


def _quotesingle():
    return [Stroke([("M", 148, 716), ("Q", 140, 640, 108, 540)],
                   56, "tate_tail")], 300


def _quotedbl():
    return [Stroke([("M", 122, 716), ("Q", 114, 640, 82, 540)],
                   56, "tate_tail"),
            Stroke([("M", 300, 716), ("Q", 292, 640, 260, 540)],
                   56, "tate_tail")], 460


def _parenleft():
    return [Stroke([("M", 330, 760), ("Q", 126, 500, 128, 264),
                    ("Q", 130, 36, 326, -200)], 56, "tate_tail",
                   cap_start=-30)], 420


def _parenright():
    return [Stroke([("M", 96, 760), ("Q", 300, 500, 298, 264),
                    ("Q", 296, 36, 100, -200)], 56, "tate_tail",
                   cap_start=-30)], 420


def _slash():
    return [Stroke([("M", 460, 740), ("Q", 300, 300, 130, -160)],
                   56, "harai_l")], 560


def _asterisk():
    return [
        tate(280, 700, 400, 50, "tate_tail"),
        Stroke([("M", 130, 664), ("L", 420, 452)], 46, "harai_r"),
        Stroke([("M", 430, 664), ("L", 140, 452)], 46, "harai_l"),
    ], 560


def _ideographic_comma():
    """、 -- the Japanese comma, for when you want the real thing."""
    return [Stroke([("M", 300, 340), ("Q", 250, 210, 110, 96)],
                   72, "hane")], 1000


def _ideographic_full_stop():
    """。"""
    return ring(300, 560, 60, 320, 46, chamfer=0.32, knee=0.26), 1000


def _numbersign():
    """井 already is this glyph; lean on it."""
    return [
        tate(226, 704, -6, 54, drift=-28),
        tate(432, 704, -6, 54, drift=-28),
        yoko(76, 556, 468, 50),
        yoko(66, 546, 218, 50),
    ], 640


def _dollar():
    return [
        Stroke([("M", 452, 578), ("Q", 444, 646, 356, 652), ("L", 178, 642),
                ("Q", 100, 636, 102, 556), ("Q", 104, 484, 200, 446),
                ("L", 376, 378), ("Q", 464, 342, 460, 254),
                ("Q", 454, 60, 160, 64), ("Q", 102, 68, 100, 132)],
               58, "sori"),
        tate(286, 752, -52, 50, "tate_tail", drift=-10),
    ], 600


def _percent():
    return (ring(86, 286, 430, 660, 44, knee=0.26)
            + ring(320, 520, 30, 260, 44, knee=0.26)
            + [Stroke([("M", 500, 700), ("Q", 300, 350, 110, 4)],
                      52, "harai_l")]), 640


def _ampersand():
    return [
        Stroke([("M", 500, 604), ("Q", 496, 690, 372, 694),
                ("Q", 236, 698, 232, 590), ("Q", 230, 500, 350, 400),
                ("L", 200, 288), ("Q", 92, 206, 96, 118),
                ("Q", 100, 20, 252, 22), ("Q", 400, 24, 510, 180)],
               56, "ore"),
        Stroke([("M", 288, 330), ("Q", 420, 176, 560, 8)], 54, "harai_r"),
    ], 660


def _at():
    return ring(258, 434, 244, 420, 40, knee=0.26) + [
        # the tail of the spiral: 口 wrapped by an open 囗
        Stroke([("M", 524, 272), ("L", 524, 190), ("Q", 526, 126, 452, 122),
                ("L", 346, 120), ("Q", 196, 124, 192, 300), ("L", 194, 380),
                ("Q", 198, 550, 350, 552), ("L", 456, 554),
                ("Q", 540, 550, 556, 488)], 42, "ore"),
        Stroke([("M", 596, 494), ("L", 596, 238), ("Q", 594, 62, 400, 56),
                ("L", 268, 54), ("Q", 96, 60, 92, 268), ("L", 94, 414),
                ("Q", 98, 626, 286, 630), ("L", 434, 632),
                ("Q", 560, 628, 596, 560)], 46, "ore"),
    ], 720


def _plus():
    """十"""
    return [yoko(96, 544, 330, 54), tate(322, 546, 108, 62)], 640


def _equal():
    """二"""
    return [yoko(96, 544, 430, 54), yoko(96, 544, 230, 54)], 640


def _less():
    return [
        Stroke([("M", 500, 546), ("Q", 280, 400, 110, 322)], 54, "harai_l"),
        Stroke([("M", 112, 316), ("Q", 284, 238, 500, 96)], 54, "harai_r"),
    ], 600


def _greater():
    return [
        Stroke([("M", 100, 546), ("Q", 320, 400, 490, 322)], 54, "harai_r"),
        Stroke([("M", 488, 316), ("Q", 316, 238, 100, 96)], 54, "harai_l"),
    ], 600


def _underscore():
    return [yoko(20, 560, -140, 56)], 580


def _asciicircum():
    return [
        Stroke([("M", 300, 706), ("Q", 210, 578, 104, 452)], 52, "harai_l"),
        Stroke([("M", 312, 700), ("Q", 400, 578, 500, 452)], 52, "harai_r"),
    ], 600


def _grave():
    return [Stroke([("M", 130, 726), ("Q", 210, 668, 300, 604)],
                   56, "harai_r")], 420


def _backslash():
    return [Stroke([("M", 120, 740), ("Q", 290, 300, 450, -160)],
                   56, "harai_r")], 560


def _bar():
    return [tate(250, 760, -190, 54, "uniform", drift=-14)], 500


def _bracketleft():
    """The corner bracket 「 shares this skeleton exactly."""
    return [
        tate(214, 752, -178, 58, "uniform", drift=0),
        yoko(206, 400, 726, 52),
        yoko(206, 400, -176, 52),
    ], 440


def _bracketright():
    return [
        tate(226, 752, -178, 58, "uniform", drift=0),
        yoko(40, 234, 726, 52),
        yoko(40, 234, -176, 52),
    ], 440


def _braceleft():
    return [
        Stroke([("M", 388, 752), ("Q", 246, 748, 244, 620),
                ("L", 242, 420), ("Q", 240, 312, 130, 292),
                ("Q", 240, 272, 242, 164), ("L", 244, -46),
                ("Q", 246, -174, 388, -178)], 50, "uniform"),
    ], 460


def _braceright():
    return [
        Stroke([("M", 72, 752), ("Q", 214, 748, 216, 620),
                ("L", 218, 420), ("Q", 220, 312, 330, 292),
                ("Q", 220, 272, 218, 164), ("L", 216, -46),
                ("Q", 214, -174, 72, -178)], 50, "uniform"),
    ], 460


def _asciitilde():
    return [
        Stroke([("M", 92, 316), ("Q", 176, 428, 300, 360),
                ("Q", 424, 292, 512, 400)], 52, "ore"),
    ], 604


# ---------------------------------------------------------------- table

_TABLE = {
    # name: (builder, unicode)
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
