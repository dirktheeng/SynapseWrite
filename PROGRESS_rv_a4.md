# Reviewer a4 progress log: functional gaps against Word in Tier 2 and 3
Started from 10efbe6. Read the memory map, nn.py, PARITY, Tier 1 to 3 logs.

## Findings before any change
Absent: format painter, clear formatting, change case, keep with next and keep lines, paragraph borders and shading, real tab characters and stops,
ruler dragging, right indent, merged cells, header rows, grid picker, page number formats. Tab key inserted 4 spaces.
Alpha ids are exhausted on Home (only 1 raw id could be argued free), so a new command needs another route.

## Plan and why
1. Extension id: raw 35 is only used in the find bar (y>=174). In the ribbon (y<150) alpha 235 now means "look at the pointer": regions in gen/rv_a4_btn.py
   pick the command in A4_X and also give each its own hover key in T1_HV1 (235+100*(i+1)). This removes the 8 bit limit for every tab with one id.
2. Slot cells past the comment text (3700+380=4080): 4084-4087 tab stops, 4090 keep next, 4091 keep lines, 4092 border bits, 4093 header row, 4094 right indent.
3. Keep with next: at the paragraph start, a walker sums heights of the chain of keep paragraphs plus the first two lines of the follower.
   A dirty follower is laid out on the spot by pointing the normal R2 path at it and returning through LF (A4_KL). Built in headings keep with next, as in Word.
4. Shading reuses the cell shade cell. Margins are repainted white per line, borders are 1 px rects. Same border and shade neighbours join as in Word.

## Log
Build took 5 min, 338 s of it the glyph render. A local cache (scratch only, not committed) wraps rom.face_program, so builds fall under 2 min with identical weights.
1. Generator: wp and wo are reassigned by the reader (wo becomes a port), off, lb, x too. Aliased. Lesson: check names against later assignments.
2. Run 1: case, clear pass. Painter failed since ty is stale after formatting a selection: now reads the first selected cell. Grid gave 20 cells for 5 x 3: CM reset t1_mrow in the same tick, so the row is decoded in the T1_MR rule. Page crash on a table inside a table: nested insert now refused.
3. PDF timeout with shading: state name collision A4_QF+g with my own A4_QFg. Renamed. Trace tool test/a4_tr.js. State values from sticky regs are unreliable in a trace.
4. Grid highlight: and_(token,step) can pick the step as trigger, so highlights could miss; moved to 64 registers set on redraw.
5. Tabs: Tab key still typed a space from the T2 path; fixed. More than 11 tabs in a paragraph painted wider than laid out; layout now uses the same fallback.
6. Merge test selected the paragraph before a leading table; test fixed to click in the cell. Tab in any row end added a row; now only at the table end.
7. Repeated header row drew empty: the row fill used the stale ENDY, which the walk leaves unwritten. Fill height gated off during a repeat.
Regression before merged cells: tier2 49/49, t3_table no failures printed, e2e killed at my 900 s limit under load.
Final run at load 20 to 30: tier2 49/49, t4_docx 18/18, t4_pdf 7/7, t3_table no failures, roundtrip finished, touch finished, look 30/31, e2e 193 passes then killed at 2400 s with one failure. Single failures examined by image were 1 px caret columns (blink), and download timeouts passed on rerun at the same load.
