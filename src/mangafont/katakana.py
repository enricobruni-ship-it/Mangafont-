"""The katakana themselves.

Katakana is the script Japanese uses for foreign words, so a Latin
alphabet drawn to look Japanese is really drawn to look like *this* --
not like kanji.  Having the real kana in the same file does two things:
it lets ラーメン and RAMEN be set in one face, and it is the reference
the Latin is calibrated against.

They are drawn from the same stroke vocabulary as the Latin, at the same
weights, so they carry across the whole weight axis for free.
"""

from .stroke import Stroke, kata, kihitsu, transform
from .pen import (yoko, tate, box, ring, fusweep, sweep, nobi,
                  harai_l, harai_r, ten, hane, WT, WY, WD, RISE)

# Katakana are full-width: one em, with generous margins.  They sit
# larger than the Latin, exactly as they do in a real Japanese family.
KADV = 1000
KL, KR = 120, 880
KB, KT = 40, 792


def _a():
    """ア"""
    return fusweep(168, 812, 700, 268, 84) + tate(452, 688, 366, WT * 0.9)


def _i():
    """イ"""
    return [sweep((726, 748), (286, 404))] + tate(512, 624, 60, WT * 0.95)


def _u():
    """ウ"""
    return ([ten(468, 792, 52, -86, WT * 0.82), sweep((292, 636), (186, 452))]
            + fusweep(262, 808, 612, 596, 96))


def _e():
    """エ -- the same 工 the Latin I is built on."""
    return ([yoko(216, 792, 692)] + tate(504, 700, 154)
            + [yoko(140, 866, 96)])


def _o():
    """オ"""
    return ([yoko(170, 838, 606)]
            + [hane([("M", 566, 764), ("L", 548, 186), ("L", 404, 84)], WT)]
            + [kihitsu(566, 764, WT), sweep((494, 570), (188, 128))])


def _ka():
    """カ"""
    rx = 706 - WT * 0.5
    return ([yoko(178, 706, 638, flag=False), kata(rx, 654, WT)]
            + [hane([("M", rx, 654), ("L", 630, 214), ("L", 456, 96)], WT)]
            + [sweep((440, 634), (152, 80))])


def _ki():
    """キ"""
    return [yoko(196, 806, 618), yoko(152, 856, 428),
            Stroke([("M", 612, 750), ("L", 438, 62)], WT * 0.92, "tate_tail")]


def _ku():
    """ク"""
    return fusweep(306, 800, 698, 306, 96) + [sweep((322, 704), (162, 404))]


def _ke():
    """ケ"""
    return ([sweep((424, 762), (176, 424)), yoko(250, 828, 632)]
            + [Stroke([("M", 664, 642), ("L", 596, 74)], WT * 0.95,
                      "tate_tail")])


def _ko():
    """コ -- a 口 with the left side left off: the katakana habit of
    leaving a form open."""
    return ([yoko(180, 806, 676, flag=False), kata(806 - WT * 0.5, 692, WT)]
            + tate(806 - WT * 0.5, 692, 178, WT, head=False)
            + [yoko(180, 800, 158)])


def _sa():
    """サ"""
    return (tate(332, 724, 404, WT * 0.9)
            + [yoko(148, 862, 548)]
            + [Stroke([("M", 664, 724), ("L", 612, 66)], WT * 0.95,
                      "tate_tail")])


def _shi():
    """シ -- two ticks down the left, then the rising stroke."""
    return [ten(192, 700, 104, -62, WT * 0.86),
            ten(172, 474, 104, -62, WT * 0.86),
            nobi((186, 158), (796, 596))]


def _su():
    """ス"""
    return fusweep(186, 808, 700, 196, 70) + [harai_r((452, 392), (836, 76))]


def _se():
    """セ"""
    return ([yoko(158, 830, 558)]
            + [hane([("M", 386, 726), ("L", 366, 196), ("L", 706, 120),
                     ("L", 832, 212)], WT)]
            + [kihitsu(386, 726, WT)])


def _so():
    """ソ"""
    return [ten(296, 702, 96, -94, WT * 0.86), sweep((758, 700), (296, 148))]


def _ta():
    """タ"""
    return (fusweep(306, 800, 698, 296, 84)
            + [sweep((322, 704), (162, 404)),
               harai_r((432, 428), (712, 154))])


def _chi():
    """チ"""
    return ([sweep((744, 744), (290, 630))]
            + [yoko(172, 830, 512)]
            + [hane([("M", 544, 606), ("L", 508, 150), ("L", 372, 66)], WT)])


def _tsu():
    """ツ -- the same two ticks as シ, stood up on the shoulder."""
    return [ten(248, 716, 88, -96, WT * 0.86),
            ten(486, 716, 88, -96, WT * 0.86),
            hane([("M", 790, 702), ("L", 386, 208), ("L", 240, 150)],
                 WD * 0.95)]


def _te():
    """テ"""
    return ([yoko(238, 766, 716), yoko(158, 844, 514)]
            + [hane([("M", 546, 530), ("L", 506, 140), ("L", 384, 62)], WT)])


def _to():
    """ト"""
    return tate(398, 756, 62, WT) + [harai_l((772, 618), (394, 424))]


def _na():
    """ナ -- the Latin t is built on this."""
    return ([yoko(160, 838, 614)]
            + [hane([("M", 622, 754), ("L", 466, 152), ("L", 336, 70)], WT)]
            + [kihitsu(622, 754, WT)])


def _ni():
    """ニ"""
    return [yoko(238, 764, 592), yoko(152, 850, 244)]


def _nu():
    """ヌ"""
    return fusweep(182, 808, 700, 210, 64) + [harai_r((392, 452), (808, 72))]


def _ne():
    """ネ"""
    return ([ten(466, 792, 62, -78, WT * 0.82)]
            + [yoko(186, 812, 608)]
            + [sweep((628, 620), (196, 176))]
            + [Stroke([("M", 568, 470), ("L", 528, 62)], WT * 0.92,
                      "tate_tail")]
            + [harai_r((566, 392), (802, 158))])


def _no():
    """ノ -- one stroke, and the whole character."""
    return [sweep((766, 758), (198, 62))]


def _ha():
    """ハ"""
    return [sweep((448, 722), (176, 122)), harai_r((562, 722), (836, 122))]


def _hi():
    """ヒ"""
    return ([hane([("M", 346, 726), ("L", 326, 164), ("L", 748, 84),
                   ("L", 852, 186)], WT)]
            + [kihitsu(346, 726, WT), harai_l((714, 616), (342, 474))])


def _fu():
    """フ -- the turn-and-sweep on its own."""
    return fusweep(184, 806, 700, 238, 66)


def _he():
    """ヘ"""
    return [Stroke([("M", 158, 316), ("L", 466, 606), ("L", 876, 208)],
                   WD * 0.92,
                   [(0.00, 0.30), (0.34, 0.86), (0.52, 1.04),
                    (0.84, 0.66), (1.00, 0.18)])]


def _ho():
    """ホ"""
    return ([yoko(156, 846, 594)]
            + [hane([("M", 524, 752), ("L", 502, 146), ("L", 384, 62)], WT)]
            + [kihitsu(524, 752, WT),
               sweep((402, 462), (178, 124)), harai_r((616, 462), (846, 124))])


def _ma():
    """マ"""
    return fusweep(190, 802, 690, 316, 348) + [harai_r((352, 392), (704, 70))]


def _mi():
    """ミ"""
    return [harai_r((196, 690), (762, 606), WD * 0.9),
            harai_r((178, 448), (744, 364), WD * 0.9),
            harai_r((158, 206), (788, 104), WD * 0.9)]


def _mu():
    """ム"""
    return [sweep((656, 742), (306, 384)),
            Stroke([("M", 286, 452), ("L", 498, 126), ("L", 880, 196)],
                   WD * 0.95,
                   [(0.00, 0.44), (0.26, 0.94), (0.70, 0.92), (1.00, 1.18)])]


def _me():
    """メ -- the Latin x and X are this."""
    return [sweep((782, 726), (214, 78)), harai_r((246, 646), (806, 80))]


def _mo():
    """モ"""
    return ([yoko(246, 768, 668), yoko(152, 840, 438)]
            + [hane([("M", 520, 756), ("L", 468, 198), ("L", 706, 96),
                     ("L", 856, 210)], WT)]
            + [kihitsu(520, 756, WT)])


def _ya():
    """ヤ"""
    return ([sweep((398, 596), (236, 388))]
            + [hane([("M", 258, 402), ("L", 746, 548), ("L", 828, 650)],
                    WY * 1.8)]
            + [Stroke([("M", 606, 726), ("L", 540, 58)], WT * 0.95,
                      "tate_tail")])


def _yu():
    """ユ"""
    return ([Stroke([("M", 358, 686), ("L", 344, 352)], WT, "tate")]
            + [kihitsu(358, 686, WT)]
            + [yoko(322, 848, 336), yoko(132, 868, 108)])


def _yo():
    """ヨ"""
    return ([yoko(198, 806, 694, flag=False), kata(806 - WT * 0.5, 710, WT)]
            + tate(806 - WT * 0.5, 710, 166, WT, head=False)
            + [yoko(284, 796, 442), yoko(198, 796, 166)])


def _ra():
    """ラ"""
    return [yoko(300, 768, 722)] + fusweep(196, 790, 528, 286, 70)


def _ri():
    """リ -- the Latin u is this."""
    return (tate(310, 706, 258, WT)
            + [hane([("M", 704, 726), ("L", 684, 190), ("L", 512, 74)], WT)]
            + [kihitsu(704, 726, WT)])


def _ru():
    """ル"""
    return ([Stroke([("M", 344, 662), ("L", 300, 200)], WT * 0.92,
                    "tate_tail")]
            + [hane([("M", 646, 704), ("L", 618, 226), ("L", 812, 126),
                     ("L", 880, 246)], WT)]
            + [kihitsu(646, 704, WT)])


def _re():
    """レ -- the Latin l is this."""
    return ([hane([("M", 312, 752), ("L", 292, 232), ("L", 436, 112),
                   ("L", 844, 630)], WT)]
            + [kihitsu(312, 752, WT)])


def _ro():
    """ロ -- the only katakana that closes."""
    return box(206, 806, 152, 700)


def _wa():
    """ワ"""
    return tate(258, 684, 306, WT * 0.92) + fusweep(236, 808, 692, 414, 86)


def _wo():
    """ヲ"""
    return ([yoko(198, 806, 702, flag=False), kata(806 - WT * 0.5, 718, WT)]
            + tate(806 - WT * 0.5, 718, 470, WT, head=False)
            + [yoko(284, 796, 452)]
            + [sweep((806 - WT * 0.5, 470), (300, 78))])


def _n():
    """ン"""
    return [ten(236, 678, 104, -62, WT * 0.86), nobi((212, 244), (792, 616))]


# ------------------------------------------------------------- marks

def _chouonpu():
    """ー -- the long-vowel bar.  Foreign words are full of it:
    ラーメン, コーヒー, ビール."""
    return [Stroke([("M", 108, 404), ("L", 892, 418)], WD * 0.92,
                   [(0.00, 0.62), (0.16, 0.82), (0.62, 0.92), (1.00, 1.18)])]


def _nakaguro():
    """・ -- the separator between foreign given and family names."""
    return [Stroke([("M", 456, 432), ("L", 512, 380)], WT * 1.34, "ten")]


def _dakuten():
    """゛"""
    return [ten(596, 782, 74, -96, WT * 0.8), ten(760, 782, 74, -96, WT * 0.8)]


def _handakuten():
    """゜"""
    return ring(624, 856, 620, 800, WT * 0.5, WY * 0.9, cx=0.26)


# ---------------------------------------------- voiced and small kana
#
# Foreign words cannot be written without these: ブルーニ needs ブ, and
# ティ / ヴィ / ジェ need the small kana.  Both sets are derived from the
# base drawings rather than redrawn, so they follow the weight axis and
# any later correction to a base form for free.

def _marks(handaku=False):
    if handaku:
        return ring(672, 878, 664, 830, WT * 0.46, WY * 0.86, cx=0.26)
    return [ten(684, 830, 66, -84, WT * 0.76),
            ten(820, 830, 66, -84, WT * 0.76)]


def _voiced(base, handaku=False):
    """A base kana squeezed a little to make room for its 濁点."""
    return (lambda: transform(base(), sx=0.90, sy=0.955, dx=6, dy=2)
            + _marks(handaku))


def _small(base):
    """ァィゥェォッャュョ -- scaled down, sitting low in the square."""
    return (lambda: transform(base(), sx=0.62, sy=0.62, dx=182, dy=20,
                              wmul=0.84))


_VOICED = [
    (_ka, 0x30AC), (_ki, 0x30AE), (_ku, 0x30B0), (_ke, 0x30B2), (_ko, 0x30B4),
    (_sa, 0x30B6), (_shi, 0x30B8), (_su, 0x30BA), (_se, 0x30BC), (_so, 0x30BE),
    (_ta, 0x30C0), (_chi, 0x30C2), (_tsu, 0x30C5), (_te, 0x30C7), (_to, 0x30C9),
    (_ha, 0x30D0), (_hi, 0x30D3), (_fu, 0x30D6), (_he, 0x30D9), (_ho, 0x30DC),
    (_u, 0x30F4),
]
_HANDAKU = [
    (_ha, 0x30D1), (_hi, 0x30D4), (_fu, 0x30D7), (_he, 0x30DA), (_ho, 0x30DD),
]
_SMALL = [
    (_a, 0x30A1), (_i, 0x30A3), (_u, 0x30A5), (_e, 0x30A7), (_o, 0x30A9),
    (_tsu, 0x30C3), (_ya, 0x30E3), (_yu, 0x30E5), (_yo, 0x30E7),
    (_wa, 0x30EE),
]


def _wi():
    """ヰ -- archaic, but a gap in the block is worse than an
    approximation of a character almost nobody sets."""
    return ([yoko(198, 812, 656), yoko(160, 852, 404)]
            + [Stroke([("M", 418, 742), ("L", 388, 132)], WT * 0.92,
                      "tate_tail")]
            + [Stroke([("M", 664, 716), ("L", 638, 132)], WT * 0.92,
                      "tate_tail")]
            + [yoko(150, 858, 148)])


def _we():
    """ヱ -- likewise archaic."""
    return ([Stroke([("M", 376, 692), ("L", 360, 430)], WT, "tate")]
            + [kihitsu(376, 692, WT)]
            + [yoko(336, 838, 416), yoko(224, 782, 268),
               yoko(134, 866, 110)])


TABLE = {
    "ka_a": (_a, 0x30A2), "ka_i": (_i, 0x30A4), "ka_u": (_u, 0x30A6),
    "ka_e": (_e, 0x30A8), "ka_o": (_o, 0x30AA),
    "ka_ka": (_ka, 0x30AB), "ka_ki": (_ki, 0x30AD), "ka_ku": (_ku, 0x30AF),
    "ka_ke": (_ke, 0x30B1), "ka_ko": (_ko, 0x30B3),
    "ka_sa": (_sa, 0x30B5), "ka_shi": (_shi, 0x30B7), "ka_su": (_su, 0x30B9),
    "ka_se": (_se, 0x30BB), "ka_so": (_so, 0x30BD),
    "ka_ta": (_ta, 0x30BF), "ka_chi": (_chi, 0x30C1), "ka_tsu": (_tsu, 0x30C4),
    "ka_te": (_te, 0x30C6), "ka_to": (_to, 0x30C8),
    "ka_na": (_na, 0x30CA), "ka_ni": (_ni, 0x30CB), "ka_nu": (_nu, 0x30CC),
    "ka_ne": (_ne, 0x30CD), "ka_no": (_no, 0x30CE),
    "ka_ha": (_ha, 0x30CF), "ka_hi": (_hi, 0x30D2), "ka_fu": (_fu, 0x30D5),
    "ka_he": (_he, 0x30D8), "ka_ho": (_ho, 0x30DB),
    "ka_ma": (_ma, 0x30DE), "ka_mi": (_mi, 0x30DF), "ka_mu": (_mu, 0x30E0),
    "ka_me": (_me, 0x30E1), "ka_mo": (_mo, 0x30E2),
    "ka_ya": (_ya, 0x30E4), "ka_yu": (_yu, 0x30E6), "ka_yo": (_yo, 0x30E8),
    "ka_ra": (_ra, 0x30E9), "ka_ri": (_ri, 0x30EA), "ka_ru": (_ru, 0x30EB),
    "ka_re": (_re, 0x30EC), "ka_ro": (_ro, 0x30ED),
    "ka_wa": (_wa, 0x30EF), "ka_wo": (_wo, 0x30F2), "ka_n": (_n, 0x30F3),
    "chouonpu": (_chouonpu, 0x30FC), "nakaguro": (_nakaguro, 0x30FB),
    "dakuten": (_dakuten, 0x309B), "handakuten": (_handakuten, 0x309C),
    "ka_wi": (_wi, 0x30F0), "ka_we": (_we, 0x30F1),
}

for _i, (_base, _uni) in enumerate(_VOICED):
    TABLE["kav_%02d" % _i] = (_voiced(_base), _uni)
for _i, (_base, _uni) in enumerate(_HANDAKU):
    TABLE["kap_%02d" % _i] = (_voiced(_base, handaku=True), _uni)
for _i, (_base, _uni) in enumerate(_SMALL):
    TABLE["kas_%02d" % _i] = (_small(_base), _uni)
