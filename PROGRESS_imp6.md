# PROGRESS imp6

Base: main at 041931a. Baseline build: page 3,791,181 bytes.

## 1. Zip CRC check on open
Why: PARITY .docx open row: no CRC check, so a corruption that still inflates to the stated size opens with wrong text.
What: gen/imp6_crc.py, group 'zip crc check'. After the dry inflate of the main part (IMP_V1 in a12_guard), the network reads the CRC from the central directory entry (offset 16), runs the inflated bytes at OUTB through the save CRC network (A7_CR, the four byte table walk), and continues to OP0 only if CRC plus stored CRC is all ones in both halves. Otherwise IMP_VF refuses with the message and keeps the document. A part cut at the output limit is not checked.
Run: test/imp6.js crc, first try 9 passed, 0 failed: a stored part with one changed byte and a deflated part with a wrong CRC field are both refused, the document stays and edits on; the right CRC opens, stored and deflated; a 400 paragraph file opens.
Cost: a5_docx's open of a01_format went from 9.95 M (imp5 report) to 10,374,573 edges: the CRC is about 400 edges per four bytes (4,022 bytes here).

## Open cost back under 10 M
Tool: a scratch engine built from host/engine.c with each firing neuron's pushed edge count added to its work cell, and a script that sums them by group and lists the top neurons (not committed; same totals as e.edges()).
- docx crc (400 K): each leaf of the four byte trees pushed into four threshold neurons per output bit to get the parity of a count 0..4. The parity is now the count minus twice two thresholds (1.5 and 3.5), so the leaves push into two. 400 K to 271 K; the save CRC gains the same.
- Tried: net.lt(nb,1) for net.eq(nb,0) in the bit reader: no change in edges at all, reverted.
- Found: T2_FS1, the style id search, fired 28,616 times for 524 lookups. 196 of them came from A5_TS, which took w:tblStyleRowBandSize and w:tblStyleColBandSize for style references and searched every style for the id "1". Only w:tblStyle itself (a space after the name) now looks up a style. Result: 10,246,153 to 9,912,561 edges, 495,405 to 466,299 ticks.

## 2. F4 repeat
Why: Other shortcuts row: no F4 repeat.
What: gen/imp6_keys.py (key rule, register i6lk) and gen/imp6_feat.py (group 'repeat last command'). F4 is key name 139 in the network's key table. i6lk is set on entry to FMTS (except fm 8, the style path's own run pass), SETAL, T2_SA0 and T2_LI; IMP6_RP enters that state again, and its registers still hold the last arguments.
Runs: test/imp6.js f4: first run 3 of 4; the "nothing to repeat" check compared screen hashes and the caret blink differs. Changed to compare the saved document after typing one more character: 4 passed (bold on a new selection, one undo takes it back, centering in the next paragraph, F4 with nothing to repeat). Screenshot build/imp6_f4.png: "one" and "two" bold.

## 3. Recent colors
Why: Text color row: no list of recent colors.
What: gen/imp6_recent.py (registers, menu row and rule) and gen/imp6_feat.py (group 'recent colors'). Eight registers hold color+1, newest first; on V4_HY (the More Colors path, which typed hex, the picker and now the recent row use) the new color goes first and the others shift down only up to an equal entry, so nothing is doubled. The text color menu has a third extra row of eight framed cells (row ids 48..55); two states paint the swatches from the registers through four rect ports each. A click on a filled cell sends its color into V4_HY; on an empty one it only closes the menu.
Runs: test/imp6.js recent: first run 6 of 7, "drawn in that color" found 11 pixels: the text was still selected and only five letters. Clicked away and typed a longer line as imp5 does: 7 passed. Screenshot build/imp6_rc1.png shows teal then red in the new row.

## Not done
Automatic hyphenation: needs a pattern set (Liang's English patterns are about 4,500 entries) or a dictionary of break points; not compact, not attempted.
.docx fidelity probe (scratch, a file with one of each property): lost on save are caps, smallCaps, dstrike, vanish, w:spacing and w:w on runs, run w:shd, emboss, outline, shadow, lang, widowControl, contextualSpacing, outlineLvl, hyperlinks (text kept, link lost) and bookmarks. The style record's 24 bits and the slot cells are all used, so these need a wider record; not done. Written into the PARITY .docx open row.

## Full run at cdbdb9b
All exit 0: imp6 20/20, e2e 210/210, tier2 49/49, look 31, t3_table 9, t3_pic 9, t3_misc 13, t4_docx 18/18, t4_pdf 7/7, roundtrip, touch, a4 50/50, a5_docx 37/37 (open 9,912,563 edges), imp2 45, imp3 49, imp4 101, imp5 49, t4; audit 67/67. Two builds byte identical. Page 3,795,433 bytes (base 3,791,181).
