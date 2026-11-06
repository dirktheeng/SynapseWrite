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

## 3. Glyph unit idle work
During the ~113 ticks of a glyph's own clock, the latch "fast" (black on white) woke a wire, an AND, a step and two port
enables every tick, and slow0 was an AND over a step of (ONE - empty) that the domain's constant woke every tick. Now
those read the latches behind the gates that open them (hit, s1g, bwr). Repeat key 64,449 to 61,190.

## 4. Per face sums pushed by the open face
per_face(), fx() and the descender sum were read lazily by their floors, which pulled one closed gate per face (47 to 188
of them) each time. New helper net.pushed(e) (gen/nn.py): a wire that its inputs push (kept from the pull pass through
the duplicate merger's representative), so only the drawn face's gate fires. Repeat key 61,190 to 59,392; page smaller
(2,921,533).

## 5. Coverage: the row read also clears
The neuron that reads a pixel's row sum (gated by clr = wr or the tick after done) now also subtracts it from the
accumulator, so the separate clear relu and the second tier chain (wr) are gone. Repeat key 59,392 to 56,557.

## 6. Half blocks
The crossing's block is split once more: only the crossing's half takes ramps (4 instead of 8), the other half is whole.
Repeat key 56,557 to 55,193; page 2,929,165 (+7.7 K).

flops.js after 1 to 6 (before, after, ratio): start 7,479,327 6,539,911 0.874; paste 0.995; background 1.000;
type at end 723,101 718,683; repeat key 69,995 55,193 0.789; select all 0.988; jump 0.982; type at top 0.970; down 0.981;
enter 0.983; undo 0.982; wheel 0.982; click 0.975; mouse move 0.961; bold 0.982. Every event is cheaper.
Screenshots again: same 16 pixels as after step 2.

## 7. Whole blocks as deltas summed once per row
Before, every sample line pushed +1 into every whole block right of a crossing (a chain of block neurons, then 8 edges
per block into the pixel accumulators), and a right edge pushed the same number of -1 back. Now a crossing adds one unit
into a per block delta register at the block after its own; at the row's read (clr) a running sum over the block deltas
gives each block's whole share F, which is added before the pixel's one relu and given back to the accumulator and the
deltas by the same pushes. First try added F after the relu: a right edge's partial share is negative inside a block that
is whole from the left, so the relu cut it and bars ran to the right (screenshot showed it); fixed by adding F inside.
Repeat key 55,193 to 53,992. a01_format open 7,915,329 to 7,705,825 edges. Page 2,928,785. Screenshot: same 16 pixels.
