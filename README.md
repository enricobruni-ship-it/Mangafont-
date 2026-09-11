# Mangafont

A Latin alphabet drawn with the stroke vocabulary of Japanese writing.

Every letter is built the way a kanji is built — from a small, fixed set of
brush strokes laid into a notional square — rather than from continuous
curves. The result reads as ordinary A–Z but carries the rhythm, the
terminals and the counters of hiragana, katakana and kanji.

![specimen](build/proof.png)

## The design system

Six rules do all the work. They are applied uniformly, which is what makes
the alphabet cohere.

**1. Strokes, not outlines.** A glyph is not a shape; it is a sequence of
brush strokes. Each stroke is a centreline, a pressure profile along that
centreline, and a pair of terminals. Outlines are derived by offsetting.
Nothing is drawn as a closed contour by hand.

**2. A fixed stroke vocabulary.** Every letter is spelled out of the same
strokes Japanese uses:

| Stroke | Name | Behaviour |
|---|---|---|
| 横画 | `yoko` | horizontal; presses on entry, thins at the waist, swells into a blunt stop |
| 縦画 | `tate` | vertical; plumb, even, ending in a blunt 垂露 stop |
| 懸針 | `tate_tail` | vertical tapering off the page to a needle point |
| 折れ | `ore` | a stroke that turns a corner — the top-and-side of 口 |
| 左払い | `harai_l` | sweep down-left, thick to a point |
| 右払い | `harai_r` | sweep down-right, thin then pressing into a stop |
| はね | `hane` | any stroke finishing in an upward flick |
| 点 | `ten` | the tick: a teardrop that grows as the brush lands |

**3. Horizontals rise.** Every horizontal climbs about 2° to the right, as a
brush held in the hand naturally does. Verticals stay plumb. That single
asymmetry is most of the "written, not drawn" feel.

**4. Modulated pressure.** Width is a function of distance along the stroke,
not a constant. A horizontal starts at 1.26× its nominal weight, thins to
0.80× at the waist, and swells back to 1.24× at the stop.

**5. うろこ terminals.** The small triangular flag a brush leaves when it
lifts — above the right-hand stop of a horizontal, at the top of a vertical
entry. It is the loudest Mincho cue, so it is a real contour rather than a
fake in the width profile. It is gated on stroke direction: a shoulder that
launches *upward* off a stem (n, m, h, r) gets none, or it would sprout a
barb into white space.

**6. Squared counters, square fit.** Bowls are chamfered rectangles — 口 and
日, not circles. Side bearings are wide and nearly uniform, so a line of text
blocks up the way Japanese text does instead of flowing.

## Letters that lean hardest on the source

Some Latin letters have an exact kanji or kana counterpart, and those are
drawn as the kanji, not as the Latin letter:

- **C** → 匚 : a top horizontal, then one fold down and along the floor.
- **I** → 工 : slab top and bottom, because the square wants filling.
- **L** → 乚 : one stroke that turns and flicks up.
- **T** → 丁 : horizontal, then a vertical down the centre.
- **X** → 乂 : 左払い crossed by 右払い.
- **Y** → 丫 : two sweeps into a stem.
- **U**, **u** → 凵 / り : the left stroke turns along the floor.
- **t** → 十 : crossbar and a stem that hooks at the foot.
- **#** → 井 : it already was this glyph.
- **+**, **=** → 十, 二.
- **[ ]** → 「 」: the corner bracket shares the skeleton exactly.

`l` is deliberately レ — a flick at the foot — so it can never be confused
with `I` (工). `a` is single-storey: a squared ring plus a stem that flicks
away, like か.

## Metrics

| | |
|---|---|
| Units per em | 1000 |
| Cap height | 700 |
| x-height | 470 (low, so lowercase sits in a square) |
| Ascender / descender | 726 / −186 |
| Stem / horizontal weight | 96 / 76 units — horizontals are thinner, Mincho-style contrast |

## Coverage

100 glyphs: A–Z, a–z, 0–9, the whole printable ASCII range, en/em dash, plus
、 (U+3001) and 。 (U+3002) for when you want the real thing.

## Building

```sh
make            # builds build/Mangafont-Regular.ttf and .woff2
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
