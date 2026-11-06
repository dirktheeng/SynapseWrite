# rv_a7: interactive performance in worst cases
All numbers are deterministic counts from test/a7_bench.js (ticks, edges, work = edges + visits + lazy reads + pull evaluations) on the headless engine. On a quiet machine 1M work is about 1.5 ms. The machine was at load 20 to 30, so wall clock numbers were ignored.

## First survey (base 10efbe6)
Already well under target (work under 15M, so under about 25 ms): typing in a 990 char paragraph (2.3M), 9 pt and 36 pt pages (3 to 4M), tables, pictures, spell check heavy page (2M to 9M), two columns, tracked typing (3M, backspace 13M), hover (1.5K in the document, 1.1M over the ribbon), pointer drag (3.2M), typing during repagination (3.6M), background slice.
Far over target:
- select all then bold: 452M, undo 692M
- delete all: 477M, undo 1088M, redo 967M
- copy all: 98M
- save 1900 paragraphs: 4526M (600M edges). 760 edges per emitted byte, all of it the CRC parity network.
- find with no match over the whole document: about 1M ticks
Bugs found while measuring:
- Enter with more than 1100 paragraphs after the caret lost a paragraph and left slot pointer 0 at the end of the table, because the block port clamps at 1100 cells. Ctrl+End then pointed into the table itself.
- Undo of delete all in 1900 paragraphs lost everything after paragraph 1126: each undone merge allocated a new slot and slots ran out (3027) silently. Screenshot build/x_undo.png showed the document ending at paragraph 1126.
- Slots were never reused at all, so about 3000 Enter and undo actions in a session broke Enter.

## Log format
Records may now hold a payload: [header][payload][footer], footer equal to header, so undo reads the footer and redo the header. op 9: paragraph pointers removed. op 10: block of characters and styles deleted. op 11: style run old to new. op 12: block of characters inserted, single style.

## What changed
- Selection delete: each paragraph tail or head is one block record. Whole paragraphs in the middle leave the table as pointers in the log, so undo puts pointers back and their line breaks stay valid. Table cells stay on the old path, which keeps them.
- Formatting: windows of 32 style cells, equal run found by one threshold layer, one record per run. Color, highlight, underline, strike and tracked delete no longer mark the paragraph dirty, since they do not change metrics.
- Paste log: one record per paragraph run, characters only.
- Copy, find: 32 cell windows. Find looks for the first query character in both cases in the window.
- Paragraph table moves are chunked. Merged slots go on a free stack, reused slots are zeroed by block.
- Save: CRC moved off the byte stream. A word at a time over the finished member: four 256 entry tables held as weights behind binary trees. Pictures keep the byte network because they need running chunk CRCs. Text copied to the output by window. Hash table cleared by blocks, 6 hash inserts inside a match at most.
- Open: text runs by window.
- Walk stops at the viewport when the caret is above it, or under a selection without autoscroll.
- Layout budget: one event lays out at most 15000 dirty characters, then the viewport is painted from cached positions and the rest goes to background slices. The caret hides until the background reaches it. Background slices now count dirty characters as well as paragraphs.

## Runs
See the report at the end of this file once finished.
