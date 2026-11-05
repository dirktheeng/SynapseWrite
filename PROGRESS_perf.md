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

## Step 2: engine and file format
Bitmap scheduler (neurons are numbered in layer order, so two level bitmap gives a valid order; no layer table, no per-edge layer load). Each neuron's edges sorted, recurrent ones first. Weights through u16 dictionary (605 unique values) for edges, lazy reads share it. Sizes and targets delta coded, decoded by finish(). Ports indexed by enable, patch port walks the live list instead of the full 672/3840 cell block. Display copies only dirty rows.
Page 2.14 MB -> 1.08 MB (gz 1.59 -> 0.80 MB). Paste 10100 -> 8400 ms.

## Step 3: evaluation modes in compile (gen/nn.py), engine read side
Trigger mode: if one input being zero forces the output to zero, only that input wakes the neuron, others are read lazily. Pull mode: a neuron all of whose consumers read lazily is evaluated only when read, memoised per tick (fan-in up to 12). Sticky registers: a register whose only activity is holding itself keeps the value in v and is only touched when written. All the same function; every framebuffer checkpoint stayed pixel identical.
Paste 8400 -> 3300 ms (edges 734M -> 133M), png 5800 -> 1130 ms (edges 442M -> 55M), wheel 24 -> 15.5 ms.

## Step 4: block paste, one tick per character
PASTE reads a 32 cell window, weights control characters by position so one threshold layer finds the leading run, and writes characters, styles and 6 x 32 undo log cells in one tick. Log format unchanged so undo and redo work as before. Layout (L2) and paint (C1) read the next character in the same tick instead of a separate state.
Bugs on the way: first version added a state between read and use, so cells were stale. Caught by pixel comparison against baseline. Paste 3300 -> 1340 ms.

## Step 5: binary glyph tree, cheaper AND wake up
Character digit tree (64 visits) replaced by binary tree per face (25 visits). Page +20 KB, layout work -24%. Kept. Pull neurons with a trigger read it first and stop on zero, so the 11 style bits cost nothing for default style. AND inputs are boolean by construction, so any may wake the AND; state chosen first. Removes registers' per tick pushes (registers seen in AND inputs were checked by hand, all 0 or 1).
Wall clock on this shared machine is noisy, so test/work.sh gives a deterministic work count (edges + visits + lazy reads + pull evaluations). Paste work 256M -> 146M.
