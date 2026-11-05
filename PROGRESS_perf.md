# Performance log (perf branch)

Numbers are headless (test/bench.js, node, no canvas) unless stated.

## Baseline (44e1d6b)
1.70M edges, 142K neurons, 2.905 MB page, 2.17 MB gz. init 28 ms. paste1900 13900 ms, 3.05M ticks, 1134M edges.
typing 1.5 ms (browser 3.9 ms, the difference is the display copy), wheel 28 ms, enter 37.5 ms, png 6390 ms, 1.74M ticks.
Added test/bench.js (timing, per state profile), test/nprof.js (per neuron fan-out after a named state), test/fbdump.js + test/fbcmp.py
(event script, pixel comparison against a build of the baseline).

## Profile findings
- A measured character in layout (tick after L1) costs 1426 edges against a 200 edge idle tick. Decoders fire 96 hot lines each with 168 fan-out, 8 x 11 x 96 AND neurons.
- Measuring also lights up the whole coverage plane since g_draw only gates the colour stage.
- Small plane weights are written three times (normal, fast white, fast selection).
- Colour planes: each selected colour enable fans out to every pixel neuron.

## Step 1: glyph network rewritten (gen/app.py glyph section)
Decision tree over size, font, bold, italic, then hi and lo hex digit of the character. Each node is enabled by its parent and reads its selector lazily (lazy read = existing compile feature), so a lookup visits a path, not the table.
Advance is taken from the glyph node before a lazily gated draw node. One coverage plane per patch size; ink pixel enables colour neurons (lazy read of colour). Black on white takes only one extra visit per ink pixel. Pixels no glyph covers keep only their output cells (small 375 of 672, large 2121 of 3840).
Tried and rejected: hash-consing identical pixel rows between glyphs. Would save only 36K of 857K edges, and adds a visit per row.
Result: 1.11M edges, 94K neurons, page 2.14 MB. paste 10100 ms (734M edges), wheel 24 ms (1.74M edges), typing 0.8 ms, png unchanged 442M edges. All framebuffer checkpoints pixel identical to baseline.
