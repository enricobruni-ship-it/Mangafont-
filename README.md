# Mangafont

A Latin alphabet drawn with the stroke vocabulary of Japanese writing.

Every letter is built the way a kanji is built — from a small, fixed set of
brush strokes laid into a notional square — rather than from continuous
curves. The result reads as ordinary A–Z but carries the rhythm, the
terminals and the counters of hiragana, katakana and kanji.

![specimen](build/proof.png)

## The design system

Four things carry the resemblance. Gesture alone does not: a brushy sans is
still a sans. What makes a Latin alphabet read as kana is structural.

**1. Contrast.** In Mincho a 横画 is a *hairline* and a 縦画 is a *slab* —
46 units against 104, a ratio of 0.44. This is the single loudest signal in
the whole script, and getting it wrong is what makes a Japanese-styled Latin
look merely brushy.

**2. Corners, not curves.** Kanji have almost no smooth curves. So there are
none here: every arch in `n m h r` is a 冂 fold, every bowl in `b d p q o` is
a 口, and each fold turns through a **肩** — the small peaked shoulder that
sits at the outer corner of 口 and 日, rather than a mitre.

Because the two halves of a 折れ are different weights, a fold is built from
two strokes that meet at the corner. That weight change across the corner is
the entire point of the shape.

**3. Fit.** The glyphs fill the square. Cap height is 790 of a 1000 em and
the x-height is 600 — **0.76 of the cap**, far higher than any Latin face —
so lowercase sits in a square the way kana do. Side bearings are tight and
near-uniform, which makes a line of text *block up* rather than flow.

**4. Overshoot.** In 十 土 王 廾 a horizontal crosses a vertical and runs
past it. So the crossbars of `A H t f e` and `+` overshoot their stems
instead of stopping politely at them.

### The stroke vocabulary

Every letter is spelled out of the same strokes Japanese uses:

| Stroke | Name | Behaviour |
|---|---|---|
| 横画 | `yoko` | the hairline horizontal; heavy angled press at the entry, thin waist, swelling into the stop |
| 縦画 | `tate` | the slab vertical, plumb and near-even |
| 懸針 | `tate_tail` | a vertical running off to a needle point |
| 折れ | `fold` | a horizontal turning down into a stem, through a 肩 |
| 左払い | `harai_l` | sweep down-left, pressing early, gone to a point |
| 右払い | `harai_r` | sweep down-right, entering thin, pressing into a stop |
| はね | `hane` | the flick — tapered late and abruptly, so it reads as a spike, not a fade |
| 点 | `ten` | the tick: a teardrop that swells as the brush lands |

### The three terminals

Mincho terminals are separate wedges of ink, not fattened stroke ends, so
each is its own contour:

- **うろこ** — the "scale": the fin left at the stop of a 横画. Sized in
  *absolute* units, because scaling it off the stroke's own width makes it
  vanish on exactly the hairlines that need it most.
- **肩** — the shoulder at a fold.
- **起筆** — the flared head where a 縦画 begins.

Horizontals also climb about 1.7° to the right, as a hand naturally draws
them, while verticals stay plumb.

## Letters that lean hardest on the source

Some Latin letters have an exact kanji or kana counterpart, and those are
drawn as the kanji, not as the Latin letter:

- **C**, **c** → 匚 : a top horizontal, then one fold down and along the floor.
- **I** → 工 : slab top and bottom, because the square wants filling.
- **L** → 乚 : one stroke that turns and flicks up.
- **T** → 丁 : horizontal, then a vertical down the centre.
- **X**, **x** → 乂 : 左払い crossed by 右払い.
- **Y** → 丫 : two sweeps into a stem.
- **U**, **u** → 凵 / リ : the left stroke turns along the floor.
- **H** → 廾 : the bar crosses both stems and runs past them.
- **n**, **h** → 冂 : a fold hung on a stem.
- **m** → 川 under one bar: three evenly spaced stems.
- **o**, **b**, **d**, **p**, **q** → 口.
- **S**, **s**, **$** → 己 : the fold chain, squared off.
- **t** → 十 : crossbar and a stem that hooks at the foot.
- **f** → 千. **Z**, **z** → 乙. **y** → メ with a tail. **r** → ケ.
- **@** → 回, left open at the foot.
- **#** → 井 : it already was this glyph.
- **+**, **=** → 十, 二.
- **[ ]** → 「 」: the corner bracket shares the skeleton exactly.

`l` is deliberately レ — a flick at the foot — so it can never be confused
with `I` (工). `O` and `o` have their corners cut while `D` is square on the
left and cut only on the right, which is what keeps the three apart.

## Metrics

| | |
|---|---|
| Units per em | 1000 |
| Cap height | 790 |
| x-height | 600 — 0.76 of the cap, so lowercase sits in a square |
| Ascender / descender | 858 / −170 |
| Stem / horizontal weight | 104 / 46 — a contrast ratio of 0.44 |
| Sweep / corner weight | 84 / 70 |

## Coverage

100 glyphs: A–Z, a–z, 0–9, the whole printable ASCII range, en/em dash, plus
、 (U+3001) and 。 (U+3002) for when you want the real thing.

## Download

| Format | File | Use |
|---|---|---|
| TrueType | [`build/Mangafont-Regular.ttf`](build/Mangafont-Regular.ttf) | installing on Windows, macOS, Linux |
| OpenType/CFF | [`build/Mangafont-Regular.otf`](build/Mangafont-Regular.otf) | design apps — Illustrator, InDesign, Figma, Affinity |
| WOFF2 | [`build/Mangafont-Regular.woff2`](build/Mangafont-Regular.woff2) | the web |

On GitHub, open the file and use the **Download raw file** button. Both the
TTF and the OTF are the same outlines; the OTF is the CFF/PostScript build
(cubic curves), the TTF is quadratic.

## Building

```sh
make            # builds build/Mangafont-Regular.{ttf,otf,woff2}
make proof      # regenerates the PNG proof sheet
make specimen   # opens specimen/index.html
```

Requires `fonttools`, `brotli` (for woff2) and `skia-pathops` (to boolean the
overlapping stroke contours into single outlines):

```sh
pip install fonttools brotli skia-pathops
```

## How the code is laid out

```
src/mangafont/stroke.py   the brush engine: centreline + profile -> contour
src/mangafont/glyphs.py   every glyph, as a list of strokes
src/mangafont/build.py    compiles the strokes to TrueType
tools/preview.py          pure-stdlib rasteriser, for the proof sheets
tools/render_ttf.py       renders from the compiled .ttf, as an independent check
```

Glyph sources quote widths in design units at weight 1.0; `stroke.WEIGHT`
scales the whole family at once, so a Light or Bold is a one-line change
followed by a round of spacing work.

## Licence

SIL Open Font License 1.1. See [OFL.txt](OFL.txt).
