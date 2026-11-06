# imp1 progress log
Started from master 98ffb6c. Build baseline: 442,592 neurons, duplicates 160976, dead 161832, 959,404 lazy, page 3.16 MB.

## Open cost: why duplicate pruning doubled it
Tool: test/oprof.js (per neuron edges during open with generator file:line, needs NETDBG=1 build and COUNT engine). Compared 41.08 M (prune on) and 26.14 M (NODUP=1): the whole 15 M is glyph unit, snapping layer and outline weights, lines glyphnet 293, 295, 510.
Cause: not lazy skipping in general. In a glyph, two outline heights can map to one snapped height. Merging makes ge[Y0] and ge[Y1] the same neuron, and relu(ex+(ge[Y0]-ge[Y1])*M-M) then has its enables cancel. With no enable left, compile treats every input as push, so s, kn and dy registers wake 309 such neurons on all 16318 generator ticks, and the dy wires can not be pull any more.
Fix: prune recognises a closed gate with no big positive input (bias<=-2^39, no weight>=2^39): it can never open, so it gets no inputs and consumers drop it. Iterated with merging. Result: never open 309, duplicates 161285, neurons 442,283 (a bit fewer than before), page 3,134,807 (was 3,157,647), open 41.08 M to 26.12 M edges, ticks unchanged 561,910.

## Open cost: from 26.1 M to under 10 M
Each run below is a full build, then test/oprof.js on a01_format, counting engine.
- tag() as one OR neuron; and_ bounds any input with two positive terms (a sum of exclusive lines had no input that decides, so all lines pushed), tick budget counts by its own bias through one self edge (was 5 edges a tick), column tiers (cells of the glyph) in ramp and coverage, live program wakes its own clear (was fan 5139 from done): 20.6 M, then 19.96 M.
- pull limit 12 to 300, big ORs over window lines go lazy: 17.24 M. Paints no slower (bench same).
- Ramp bank in blocks of 8: nothing opens left of a crossing, one neuron for whole columns right of it: 14.7 M. Lazy reads 98 M.
- FSM: rule lists of 24+ are chunked by 12, so a state wakes chunks, lazy reads 94 M to 12 M; a write r+const is the rule line with a weight; r+growth gates only the growth: 12.86 M, 11.59 M. Dec(r,k) for proved decrements, Shift for bit buffer.
- Text skip one tick per window; style id search one tick per compare; two digit return decoder from 6 targets; ticks 561,910 to 492,733.
- Closing enables read lazily outside outline edges: 10.94 M. Not on outline edges: that costs 200 KB of page.
- One whole column sum per block, edges that cancel wake no column: 10.18 M.
- Height thresholds in groups of 16: 9.976 M. Tried a full chain: page 4.85 MB and 332 layers, dropped. Groups of 8: 9.965 M at 3.265 MB; groups of 16: 3.215 MB, kept. Blocks of 4 worse (10.46 M).
Regress (a10_regress on a01 and a02 fixtures, /tmp/fx) base 98ffb6c vs now: every screen hash and docx hash equal, PDF differ only in embedded font stream as expected (same size). Total ticks 5,931,802 to 5,786,983, total edges 644.6 M to 301.7 M.
