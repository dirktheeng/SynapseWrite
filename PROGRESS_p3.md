# PROGRESS p3

Branch p3 in /root/p3, from main 76ede1a. Area: .docx reader and writer, zip and deflate, equations, PDF. Goal: close the Tier 4 rows PARITY.md marks Partial.

## Baseline (76ede1a, measured here)
- ./make.sh: page build/index.html 2,953,717 bytes.
- test/a5_docx.js a01 open: 6,784,308 edges (limit 7 M per the task).
- test/flops.js with build/engine_count.wasm: /tmp/claude-0/p3/flops_base.json. Background layout 556,832,631 FLOPs, type at end 718,971, select all 6,405,696, wheel 7,304,280, bold 7,311,745 (all 15 events kept in the file).

## Reading the rows
- .docx open: PARITY lists caps, small caps, double strike, hidden, spacing, shading, widow, contextual spacing, links and bookmarks as lost, but feat1 already reads and writes them (test/feat1.js). Still lost: emboss, imprint, outline, shadow, character scale (w:w), language, outline level; secondary parts are not CRC checked.
- Print to PDF: missing internal links and bookmarks as destinations and outline items.
- Equations: matrix columns not aligned, two rows only, no nesting except between delimiters.
- .docx save: lists no gap besides real Word.

## Step 1: PDF destinations (gen/p3_pdf.py, group 'p3 pdf destinations')
Design: the catalog gets /Dests, a reserved object right after the outline root (DROOT=OROOT+1, so the first page moves one number up). A printed chunk whose style entry carries a bookmark id writes, for the first chunk of that bookmark in this export, the page object and line top into a table at 1196000 (entry: export serial, object, top; the serial is bumped at PDF start so no clearing pass is needed). Unless the name starts with _ (Word's hidden bookmarks), the same chunk adds an outline record at level 1, in document order with the heading records of rv_a6; its title is the bookmark name (rv_a6's title loop now stops at a zero for those records). Links of kind 2 (w:anchor) now get boxes like external ones and are written as /Dest/name; names are PDF name objects with #hh for bytes outside letters, digits, _ - and '.'.
- Link field decode in feat2_pdf.py now takes the low 8 bits for the link id (F1N is 255) and 24 bits in all, ready for the bits step 2 adds.
- First build ok, page 2,955,441 bytes (+1,724).
- test/p3.js pdf first run 7/10: the three failures were the test's (pypdf names keep a leading slash). Fixed in the test, then 10/10: pypdf and pdfinfo -dests both see sec1, _Toc99 and Odd_name.2 on their pages; the destination top is the bookmarked line within 4 pt of pdftotext's box; outline has sec1 and Odd_name.2 but not _Toc99; internal link boxes cover their words; the external link is still a URI action; qpdf clean.

## Step 2: run and paragraph properties in .docx (gen/p3_regs.py, gen/p3_docx.py; groups 'p3 docx properties', 'p3 docx writer')
Design, no new style cell (so STYCAP, the interner and the style port are untouched, which keeps clear of p2's area): the link field of a style entry already had spare bits, since link ids stop at 255. Layout now: link id bits 0-7, language id 8-11, bookmark id 12-19, outline, shadow, emboss, imprint 20-23. The extended field's free bits 14-23 hold the character scale in percent. Every decoder of these two fields now takes 24 bits (feat1 reader and writer, glyph x_decode, PDF chunk path), so the new bits never overflow into the old ones; x_decode's extra bits sit behind its one nonzero test, so plain text pays nothing.
- Language: w:lang's attribute text is copied to a scratch entry and compared with up to 15 known ones (table at 1197100); same text, same id. Written back as `<w:lang ` + text + `/>` after vertAlign.
- Outline level: kept as (level+1)/32 in feat1's paragraph extras cell. Why a fraction: every reader of that cell tests its two flag bits with thresholds at whole numbers minus a half, and a fraction under 0.5 changes none of them, so layout is untouched (no FLOPs change). Only the document part's outlineLvl is read; styles keep theirs out of this cell. Written after jc.
- Writer: outline, shadow, emboss, imprint after dstrike; w after spacing; lang after vertAlign. ins_h is cleared before style definitions are written so a run's flags cannot leak into styles.xml.
- Not drawn: emboss, imprint, outline, shadow and scale are kept but text draws as plain on screen and in PDF. Drawing them belongs to the glyph network, which is p2's area.
- Secondary part CRC: not done. The CRC network costs about 67 edges a byte (imp6 log: 271 K edges for 4,022 bytes); a01's secondary parts would add far more than the 216 K edges left under the 7 M open limit.
- Build ok, page 2,959,181 bytes (+3,740 over step 1).
- test/p3.js docx first run 15/16: my test expected a plain run with no rPr, but the writer always writes sz. Test now checks that the plain run has none of the new properties. Then 16/16: each property saved, plain run clean, schema check OK, save and reopen pixel identical, second save XML identical, LibreOffice (stand-in, not Word) keeps them all. test/feat1.js 24/24.

## Step 3: matrices (gen/p3_eq.py, group 'p3 matrix')
Design: the scan takes a third and more groups after `mat(..)(..)`: the record's second text runs from the second group to the last, rows apart by ")(" as typed, so the copy and the 27 character limit are unchanged. Cell 6 (unused by matrices) holds the row count; layout makes a matrix line taller by a half pitch of ascent and a pitch of height per row past two. One walker over the two texts (a '&' at depth 0 ends a cell; the end of the first text, or a ')' at depth 0 in the second, ends a row) runs a column pass (widest cell per column, up to 8) and then, per cell, measures the cell and either draws it centred in its column or prints it in the PDF as one text object. The same column pass sets the record's width at build. OMML: one m:mr per row from the same row rule. The reader already typed `mat(` then `(` per row, so a foreign matrix of any size scans into one record.
- First build: NameError, A9Q is defined after the layout state; used rom.metrics(9)[0]. Second: two states named P3_W0 (my docx scale writer and the walker); renamed the writer's to P3_SW*, and the feat1 hooks that pointed at P3_W0 (they had silently pointed at the walker after the rename) to P3_SW0. Page 2,961,821 bytes.
- test/p3.js eq first run 6/10: every failure was my image analysis (it took the caret line as the matrix). Viewed build/p3/mat3.png and mat4.png: three and four rows, columns centred. Analysis now takes the matrix between the first and last marker words with the caret moved to the line end. Then 10/10: OMML of three rows; three ink rows of two cells with column centres within 1.5 px; reopen pixel identical; PDF qpdf clean, every cell in three rows, centres within 1 pt (pdftotext boxes); a foreign 4 by 3 OMML matrix keeps every cell and draws aligned; a four row matrix line is taller than a two row one.
- test/feat2.js eq 25/25, test/rv_a6_eq.js 9/9 (two row matrices now use the aligned layout too).
- Nesting not done: it needs measure, paint, print and the OMML writer of a form to call themselves on an inner record with all their registers saved and restored; not built in this pass. PARITY says so.
- Secondary part CRC: a01's secondary XML parts are 57,447 bytes; at about 67 edges a byte that is about 3.8 M edges, against 216 K left under the 7 M limit. Not done; PARITY states the blocker.

## Step 4: FLOPs and the final run
- First full run: all suites passed except test/p3.js eq 34/36, a test isolation bug (the eq part typed into the document the docx part had left open). The eq part now opens a blank file first.
- flops.js after step 3: every event +20 to +1,082 FLOPs over base. gprof wheel, base vs p3: compiled control +77. Neuron traced through NETDBG to fsm.finish: the reader's trap level fans out to every guarded edge, and my new reader states added guarded edges. Generator change in nn.py: guard only the back edges of a depth first walk from the trap roots, plus edges into the bar. Every cycle still holds a guarded edge. Guarded edges 3,147 (base) to 1,391. Also gated two expressions of mine that read port outputs ungated.
- After: every event at or below base (background layout -158,109, wheel -642, type at end -34). Page 2,946,417 bytes (base 2,953,717). a5 a01 open 6,761,936 edges (base 6,784,308). Two builds byte identical.
- Final full run, one at a time: e2e 210/210, tier2 49/49, look, t3_table, t3_pic, t3_misc, roundtrip, touch, t4 exit 0 with no FAIL, t4_docx 18/18, t4_pdf 7/7, a4 0 failed of 50, a5_docx no FAIL, fonts, imp2, imp4 no FAIL, imp3 49/49, imp5 49/0, imp6 20/0, feat1 24/24, feat2 35/35, rv_a6_eq 9/9, rv_a6_pdf 4/4, p3 36/36, flops all events at or below base, audit 67/67.

## Round 2 (after merging main at 46eef8b)
### Secondary part CRC: measured, not kept
- Built the check: at the end of each inflated member that is not the main part, the bytes go through the save CRC network (four bytes a step) and a mismatch skips the part as if missing (gen/p3_crc.py, hooked before the A12_S0 sentinel).
- test/a5_docx.js: a01 open FAIL, 34,482,942 browser edges against the 7 M limit (6,761,936 without it).
- test/a5_node.js (node, open only): 8,051,314 edges and 160,369 ticks, against 4,025,308 and 133,602 on base 76ede1a. A stepped node run counted 5 parts checked, 14,752 four byte steps (59,008 bytes), so about 68 edges a byte, as imp6 measured.
- Cheaper design, reasoned: the 7 M limit leaves about 238 K edges, under 4 edges a byte for 59 K bytes. Each four byte step must at least read the four bytes and push them into a 32 bit result, which already costs tens of edges in any layout of thresholds; table driven CRC through read only bank tables needs XORs, which again need bits, and byte wise lookups add 3 or more ticks a byte (another 177 K ticks against a 600 K tick test limit). Checking only the parts that are read does not help: all 5 checked parts (styles, numbering, rels, footnotes, comments with headers and footers) are read. No compliant design fits; code removed, PARITY states the measured cost.
