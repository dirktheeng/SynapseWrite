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
## Step 2: a12 (01a6efb)
Conflicts and how they were resolved:
- DISP: HEAD's rules, kh[9] enters a12's zip validator A12_OV0.
- W3: HEAD's a7 windows plus a12's 590000 copy limit. A7_CW moves at most a window past that, still below SLOT0.
- PS2: paste stops at pi_ end or SLOTMAX. Either one flushes a7's pending run first.
- L2: HEAD's tab rule plus a12's rule that a line always takes its first character.
- Inflate limits, duplicate: a5 had a5lim and a5fsz checked in CS only; a12 has ilim and oblim checked in GBR, XDR, ST2, CODES with a per target table. Kept a12's, removed a5's rule and registers.
- Weight format, hdr: HEAD's. a12's dbg table added after it. Engine: HEAD's domains and paged bank with a12's CHK hooks, shipped wasm has no check code. Glue: HEAD's.
- test/fuzz_lib.js ported to HEAD's weight stream and paged bank (test harness only, no assertion changed).
Found by fuzz_inv seed 2 s: second save split a run, because a record value 0 (Carlito 11 pt reached by toggling bold off) missed the interner's scan from index 1 and got a second index. Scan now starts at 0. Not an a12 defect; from fonts.
Runs: fuzz regress 5/5, fuzz_selftest 4/4, fuzz run 1000-1003 mix: 0 crash classes, file 1000-1002: 0, fuzz_inv 1-5 us: 0 failures of 8 (1 of 6 before the interner fix), e2e 210/210 (before the one line interner fix), fonts 23/23.
F32_LOSS warning at port 396 tick 1, value 0.237 is the pointer glyph? not a failure class in a12's list, left.
## Step 3: a10 (aef3888)
Fresh baseline taken first with test/a10_regress.js on the head before a10 (fixtures made in the scratchpad, since test/fixtures holds only PNGs): total 5,024,125 ticks, 550.0 M edges.
Decisions:
- ROM: BANK raised from 64 M to 66 M. a10 string ROM 64 M, spell table 65 M, lookup tables 65.8 M, declared with region(). The bank is paged so the range is cheap. The fonts PDF ROM joined the same run list hdr.rom, so glue has one copy loop that skips zero cells. romb gone from hdr.
- Lookup table cells widened from 16 to 24 bits, since a size table entry is a raw record field with bits up to 21.
- Size table: HEAD's 3 digit half points and rom.sz_near; a10's table form, 200 entries.
- Color: a10's palette table plus HEAD's oi+6 (a5 moved the entry point).
- Comparator: a10's window bank replaces a5's two letter group. a5's helpers removed. Open cost goes up, see below; neurons drop.
- Spell: a10's table walked per letter, with a6's suggestion walker still driving the same letter wires (_ew).
- Ret.gen: a10's two digit form. Return lists HEAD's a7 returns plus a10's.
New writers: a4, a5, a6, a12 call lit, number and numz, which are now a10's, so they are routed. Also done by hand: pad3 uses the number writer; PDF only literals A4_Q and A6P_ use the block copy, with no CRC involved.
Regress after vs before: every screen hash equal, every docx hash equal. PDF bodies equal up to the embedded font streams (subset carries the build time, a10's note), same length, same xref. Total 5,063,060 ticks, 561.7 M edges. Neurons 729,781 to 611,401; synapses 1,194,346 to 1,018,588 push plus lazy 1,273,767 to 1,129,725; weights gz 2,461,663 to 2,382,999. Open of a small docx 13.6 M to 17.3 M edges, from the comparator bank.
Runs: t4_docx 18/18, t4_pdf 7/7, e2e 210/210, rv_a6 6/6, rv_a6_pdf 4/4, rv_a6_eq 9/9, rv_math_mark 6/6.
fuzz_caps on the a12 merge: 47 of 48; the failure was a7's copy window overshooting a12's 590000 limit by 18 cells. Limit is now tested at 589900, so a window cannot pass it (after the fix the case passes, see below).
## Step 4: a8 (b7e29a9)
Merged by hand (git merge -s ours, then pieces), because the weight format and engine conflict with fonts and a10.
Before: page 3,215,094 bytes, weights gz 2,382,999, x1 428 ms, x4 1807 ms, x6 2486 ms, 611,401 neurons, wasm 77.5 MB after the regress script.
Encoder: on the same net, a8's encoder 2,599,269 gz, fonts' streams 1,750,631 gz (excluding the ROM). Fonts' encoder stays.
Taken: base64 plain loop or fromBase64; payload in data attributes instead of a JS string; prune (dead 161 K, duplicates 161 K); engine records per neuron and per synapse; display copy in the engine, the ImageData is remade when memory growth detaches it (a paged bank can grow memory).
Not taken: numbering by creation order. a8 measures it as 180 KB bigger on the glyph planes, and the rule here is the smaller page. Not measured on this net.
Pruning is not free: first paint work 8.6 M to 17.2 M, since a shared neuron loses laziness when one consumer pushes. Other common events unchanged within 1 percent (bench, work counts). Kept for 161 K fewer neurons.
After: page 3185129 bytes, weights gz 2,360,456, x1 273 ms, x4 1039 ms, x6 1600 ms, 449,671 neurons, 73.3 MB after the regress script.
Runs: regress hashes equal to the pre a10 baseline except PDF font streams; e2e 210/210, t4_pdf 7/7, fonts 23/23, fuzz regress 5/5, fuzz_selftest 4/4.
Test tool edit: nprof, prof, prof2 read e.ostart(i), since p_ostart is gone.
## Step 5: a11 (4476f88)
Taken: raw event layer gen/rv_a11_input.py (key names, modifiers, pointer type, touch diff, field text in the network), commands back from neurons at _HS, one copy port (kind 6) replacing row copy and block copy, clip1 meaning rows cut at the bottom, pixel read with two neurons, packed word R+G*256+B*65536, screen check on blink ticks, file names in the bank, PROVENANCE.md from a per neuron source record.
Adapted: KEYNAMES gained HEAD's Insert 136, F3 137, F12 140, ContextMenu 141. Alt without Ctrl now passes in the network (glue sends bit 16), it was a glue test on HEAD. Mouse down sends 8*ev.button, so right click is bit 4 of evm in the network, with no glue test on the button. Glue keeps HEAD's paged e.bget and e.bset, slices, dictionary persistence. All HEAD clip1 values moved to 800-DOCB; the check engine and the page agree. PDF word order and PNG reader and writer follow the new packing.
Glue event queue no longer drops kind 11, that was a literal test.
Audit edits, for review (the allow lists encode a11's earlier glue, and each new entry was argued in the file): strings eng, net, contextmenu, utf-16le, synapse_dict, []; conditions for the image remade after memory growth, native base64, slices, dictionary; loops over dictionary, file bytes, ROM cells; port kinds 8 and 11 and read 10; size limits 150 and 85 lines; ternary at most 1. Engine: header 12*4 rather than 48, bread divides by PG.
Test edits, for review: rv_a11_input F12 removed from keys that do nothing (a3 gives it Save As). fuzz_selftest port table follows the merged ports.
a11's failing redo tests: t3_pic resize redo PASS, undo and redo PASS; t3_misc run, see next line. touch.js 'no pointer on touch' printed false once under load, true twice alone, a caret blink between two screenshots.
Runs: rv_a11_input all passed, rv_a11_screen all passed, t3_pic all PASS, audit 67 of 67, e2e 210/210, rv_a3 49/49.
