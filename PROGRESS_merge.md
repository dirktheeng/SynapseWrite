# Merge log: a6 and a7 onto integ (fonts + a1..a5)
## region()
Added region(name,start,end,space='bank') to gen/nn.py; it asserts no two declared ranges overlap in one space. Declared the bank map in app.py from the brief and the constants; slot cell offsets use space='slot'. Checked by hand that an overlap raises. a9's ROM and a10's ROM not taken, so not declared.
## a6 decisions
- Math mark: one definition, is_math(D) in app.py: family MATHFAM=1 (Caladea, raw field MATHRAW=128) AND flag nop. All three uses in a6 are boolean via is_math. Consequence: Caladea text with noProof set reads as math on save. Same conflation as a6's own design under old styles; recorded as a known limit.
- Reader: _eqstyle could not return a cell in one tick under interning. It now interns the record during the state and hands flags over; state A6E_IS inserts with ROUT+flags. oret is set before A6E_IS. m:r now uses ics:t2ps and resets rnop like w:r.
- _qst records use rom.lit(9) and MATHRAW. a6's size literal 9 is the old index for 9 pt.
- Style cells: all decode sites moved to rs, RSC, RSR. A6S_TD and A6S_IG1 waiting states removed, a read lasts one tick.
- PDF: OROOT=3+3*NFC, FIRST=OROOT+1. Catalog /Outlines names OROOT. /F6 replaced by the name of FACES.index((1,0,1)), marked used in PUS at A6Q_P1. ExtGState added before the per face font resources. A6P_B0 chains to A4_QL rather than T2_PM, so a4 borders still draw. qhl stays on PD_F.
- Menu: decode width 21 in T1_M0, T1_MK, T1_MR; rows 12 (a3), 9,10,11 (a4), 20 (a6).
- Keys: ContextMenu is 141 (undefined in cp1252, so no typed character can reach it). 138 and 140 are Windows-1252 letters, and 136 is Insert.
- Right click, both a3 and a6 built it: a6's glue contextmenu dispatch removed. RVA3_CM2 keeps a3's menu for a selection or a click past the word's end; otherwise it asks A6S_0 with a6cm. A word with nothing to offer goes to a3's menu through A6S_NO, so right click always opens one. Menu key on a correct word opens a3's menu at the caret. Spelling off also goes to a3's menu.
- Duplicate a5 and a6 math text: a5 read m:t as plain text, a6 reads it as equation characters. Kept a6, removed a5's rule.
- a5 regression found by a4.js (borders and shading survive reopen): a5 gated w:shd on a5tcp, which dropped a4's paragraph shading. Now tcPr, or in document.xml outside tblPr and outside a cell.
- SVr: a6em close first, then a4 tab, then math (a tab never counts as math), then fields, merge field, default.
- Dictionary persists: glue reads localStorage to e.bset at load, and copies h.dsave cells with e.bget when commanded.
## a6 test edits
- rv_a3.js 'menu select all then bold': 'abc' to 'cat', since a flagged word now gets suggestions; intent unchanged.
- rv_a6_eq.js: Control+Home before the two reference images, since open leaves the caret at the document start.
- a5_docx.js: 72 pt regex now 144 per the brief; math text check strips tags, since math is written one m:r per character.
## a6 test runs
t4_docx 18/18, t4_pdf 7/7, tier2 49/49, rv_a6 6/6, rv_a6_pdf 4/4, rv_a6_track 17/17, rv_a6_eq 7/9 then 9/9 after the test edit, rv_a3 48/49 then 49/49, e2e 210/210 (before the shading fix), a4 49/50 then 50/50 after the shading fix, a5_docx see below.
a5_docx after edits: one known failure left, `and under 10 M edges` at 19.3 M edges. t3_table no false entries.
## a7 decisions
- W3 keeps a7's window routes. Formatting window A7_FW could not write newst, which is a record. It now reads the first cell through rs too, interns once per run, and new state A7_FX fills ROUT plus the flags (fm 11 adds ST_DEL). Op 11 stores raw cells.
- Copy, save and reader windows hand off to single cell paths through rs. Save window stops on any cell other than t2psv, so math (t2psv 99999), tabs, fields and merge fields go the slow route.
- Reader window TX3: fills csi+rhi, cap is 950 minus clen so a5's split at a space near 1000 still decides long paragraphs.
- Paste: a7's TST (keeps tracked insert) and a4's tab rule in PS3. wplg is gone.
- Glue clip: a7's Uint16Array with e.bget, replacing a spread that overflows on a large copy.
- region: a7's reservation is now named. rv_a7 bank 1384000-1389100.
## a7 known regression, fixed in the network
Before: typing while the background was behind the caret cost 3.6 M edges a key in test/a7_type.js (11 M in a7's longer paragraphs), because each key walked up to 15000 dirty characters.
After: while a7_far holds and cp >= bpi the caret is below the viewport, so AFTER_ED halts with no paint and sets a7_jmp; the background lays it out and jumps to it. 0.12 M edges a key, image identical to typing after the background finished. Other events in that window walk the viewport only (a7_vw), without overwriting the background's saved position, and clear a7_far if the walk passes the caret. The caret shows as soon as it is reached; typed text below the viewport appears when the background ends.
New test: test/a7_type.js.
## a7 test runs
a7_bulk ALL PASS, a7_save ALL PASS, a7_type ALL PASS, e2e 210/210, t3_table no false, roundtrip no false, rv_a6_eq 9/9, rv_a6_track 17/17, rv_a6 6/6, rv_a3 49/49, t4_docx 18/18; tier2, t4_pdf, a4, a5_docx: see the report.

# Merge log: step list after a7 (head 0cc05a5)
## Step 1: math mark
Records have all 24 bits taken and the 5 flag bits with kind 1, 2, 3 are all in use, and a bank cell is 32 bit float so bit 24 cannot sit beside low bits. STYCAP is 4096, so the index only needs 12 bits. Bit 18 of the cell moved from the index to a new flag: ST_MATH. IDXM and the rs port mask are now 18 bits, flag_decode starts at bit 18 and FD['flags'] carries it, so all flag preserving paths keep it. Ignore sets only ST_NOP, so ordinary text cannot get it. is_math is the flag AND family Caladea, so choosing another font makes an equation ordinary text as before. Writers of the mark: Equation command (T4_EM) and reader (_eqstyle). Equation characters keep ST_NOP too, the spell checker reads it.
New test test/rv_math_mark.js, 6/6. Same test on the previous head: 1/6, which confirms it catches the defect. rv_a6_eq 9/9.
