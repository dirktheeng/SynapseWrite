# cmp2: the last two FAST targets (typing repeat key, file open)

## Baseline (e053426, main)
- Page 2,919,845 bytes. flops.js: typing repeat (type at end, again) 69,995; select all 6,481,622; jump 6,285,618;
  type at top 944,987; down 612,154; enter 6,348,238; undo 6,662,710; wheel 7,437,108; click 7,679,083; bold 7,445,988;
  mouse move 28,639; start 7,479,327; paste 119,334,231; background layout 557,044,343; type at end 723,101.
- a01_format open (eprof, node): 8,928,039 edges, 454,498 ticks. docx reader 3.93 M, ramp bank 1.16 M,
  compiled control 1.00 M, coverage 0.71 M, glyph unit 0.71 M, docx reader tier 2 0.35 M, outline edges 0.31 M, crc 0.27 M.

## Where a typed key goes (new tool test/cmp2_trace.js: per tick FSM state and FLOPs of the repeat key)
- 65 ticks. One tick, C1 (the paint of the new character), is 46,929 of the 69,995 FLOPs: the repeat key types 'y',
  which no glyph in the document has used, so the glyph unit generates it (about 113 ticks of its own clock domain).
- Typing an 'e' instead (cached glyph): 26,927 FLOPs in all. So about 43 K of the 70 K is drawing one new glyph.
- Inside that tick (work units, = multiply-adds + activations): ramp bank 9,126, outline edges 5,485, coverage 4,490,
  glyph unit (hit path, latches) 3,969, row sequencer 1,335, snapping 851, geometry 820, pixel records 758.
- Experiment: K (sample lines per row) 4 to 3: repeat key 62,655. Not enough alone, and it costs vertical antialiasing,
  so it was reverted. It showed about 14 K FLOPs of the glyph's cost do not scale with the sample lines.

## 1. Coverage without a clamp per sample line
The K sample lines now sum straight into the pixel's accumulator; the clamp to 1 is applied once per row (the winding
of a sample line is 0 or 1 within one outline, so this is the same except where two contours overlap inside a pixel).
Repeat key 69,995 to 69,183.

## 2. Ramp bank: blocks found left to right
Old: per crossing and sample line, a chain of AND neurons over width tiers, then per block three neurons (full, a second
threshold, an AND), then the crossing block's 8 ramps. New: a chain of thresholds x >= a that stops at the crossing's
block; one neuron per block for "crossing is in this block"; whole blocks right of it get one neuron each, chained, read
behind a latch "glyph is this wide". Repeat key 69,183 to 64,449. Page 2,922,661.
Screenshots (11 lines: Carlito 9/11/24, Arimo 11, Tinos 11/36, Caladea 14, Open Sans 14, Caveat 14, Cousine 11, Oswald 18)
against the base build: 16 pixels differ by more than 10 levels, 4 by more than 40 (max 74); by eye identical.
