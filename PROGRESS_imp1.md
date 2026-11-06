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

## Line pitch and Heading 2
a5_docx in browser after open work: 37 pass, 'under 10 M' PASS at 9,976,002 edges.
metrics_sz now reads OS/2 winAscent and winDescent (Carlito (1950+550)/2048 = 1.2207) at true px 14.667, times 1.08: 19.34 px. Old table used PIL rounded metrics at px 15: 22.
Lines stay on whole pixels: EM rounds with a fraction carried to the next line of the paragraph (lcar), measured pitch 19,20,19,19,20 = 19.33 mean; paragraph step 30 to 31 with 11 px after.
Line spacing: index 0 is the default 1.08 and saves w:line=259; index 6 is true single (menu 1.0, Ctrl+1, reader w:line<=250, saves 240); the rest absolute, lxtra linear, no decode of 128 heights.
Heading 2: record now 13 pt through a pt argument (was PTS index 2, 14 pt).
Not done: a file with no w:line anywhere opens at 1.08 where Word would use single unless docDefaults or Normal say otherwise.

## Typing below the view
AFTER_ED halted when the edit was past the background frontier (cp>=bpi, a7_far). Now it draws a provisional page after bptop, from cp-6, at once (IMP_F0, IMP_F1, impf); caret shows. Next keys in the paragraph use the fast path. BGD redraws in the true place. test/imp_far.js: all pass, first key 571,742 edges, next 106,968 and 114,315; same final image as typing after the background ends. a7_type stays under 1 M.
e2e run 1 at the pitch commit: 197/210, all same-image failures from the squiggle's last row falling below the 19 px line; squiggle moved up one row. e2e run 2: 210/210.

## Item 4
Done: empty paragraph takes inserted table or picture; reader first table takes first paragraph; find field replaced on reopen; refusal message (pfile); selection highlight across space after and before; balloons stack (cbb, full walks only); cut of 589900+ refused with a message and no deletion.
Not done: a valid zip with broken deflate still replaces the document (would need a snapshot of the page table and registers or a dry inflate).
Test edits: t3_table yb 335 to 305 and t3_pic by 472 to 435, because table and picture now sit one paragraph higher.

## Full run 1 and follow up
Full run 1: e2e 207/210 (row above then delete row, delete column then undo, delete row then undo), a4 48/50, tier2 48/49, the others clean, audit 67/67.
Cause of e2e and a4 failures: a table in paragraph 0. Row and column operations and MERGE assume a paragraph before the table. So at cp 0 a table keeps the leading empty paragraph, and the reader change is reverted; only cp>0 reuses the empty paragraph. Pictures reuse it everywhere. t3_table edit reverted.
tier2 stranded line: 46 fillers encoded the old 33 px step; at 30 px no position in the ten crosses a page. Now 49 fillers, same check.
