# imp1 progress log
Started from master 98ffb6c. Build baseline: 442,592 neurons, duplicates 160976, dead 161832, 959,404 lazy, page 3.16 MB.

## Open cost: why duplicate pruning doubled it
Tool: test/oprof.js (per neuron edges during open with generator file:line, needs NETDBG=1 build and COUNT engine). Compared 41.08 M (prune on) and 26.14 M (NODUP=1): the whole 15 M is glyph unit, snapping layer and outline weights, lines glyphnet 293, 295, 510.
Cause: not lazy skipping in general. In a glyph, two outline heights can map to one snapped height. Merging makes ge[Y0] and ge[Y1] the same neuron, and relu(ex+(ge[Y0]-ge[Y1])*M-M) then has its enables cancel. With no enable left, compile treats every input as push, so s, kn and dy registers wake 309 such neurons on all 16318 generator ticks, and the dy wires can not be pull any more.
Fix: prune recognises a closed gate with no big positive input (bias<=-2^39, no weight>=2^39): it can never open, so it gets no inputs and consumers drop it. Iterated with merging. Result: never open 309, duplicates 161285, neurons 442,283 (a bit fewer than before), page 3,134,807 (was 3,157,647), open 41.08 M to 26.12 M edges, ticks unchanged 561,910.
