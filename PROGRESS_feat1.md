# PROGRESS feat1

Branch feat1 in /root/feat1, from main bd00ad8. Task: keep more run and paragraph properties through open, display and save; more equation structures; PDF gaps.

## Baseline (bd00ad8, measured here)
- ./make.sh: page build/index.html 3,795,433 bytes; 533,330 neurons.
- test/a5_docx.js a01 open: 9,912,549 edges (limit 10 M), all passing.

## Step 1: widen the interned style entry
Why: the style record is a 24 bit float32 integer and every bit is used, and the bank is float32, so new properties cannot go in the record. An entry grows from 4 cells (record, exact color, font name, character style) to 7: feat1 adds an extended field (caps, small caps, double strike, hidden, character spacing), a link and bookmark id field, and a run shade field (exact RGB plus one).
- StylePort reads 7 cells per entry (engine port kind 10 already takes stride and length from the record, so no engine change).
- Interner compares and writes the three extra fields; Interned carries them; a bare 4 tuple leaves them zero.
- Format commands (W4, bulk A7, equation apply) and typing style (TYS2, FTY) keep the extra fields.
- Capacity: STYT stays at 1100000 but would run into STYX at 1120000 at 4096 entries of 7, so STYCAP is now 2856 entries (was 4096).
- Build: ok, 3,795,777 bytes.

## Step 2: properties through open, display, save (commit after this)
- Reader rules F1_PX (gen/feat1_regs.py) ahead of the paragraph spacing rule; states in gen/feat1_docx.py. Links: r:id resolved through the existing relationship lookup (T3_BR1) and copied into a link table at 1130000; w:anchor kept as a name. Bookmarks: start opens an id the runs carry, end closes it; names at 1264100.
- Display (gen/feat1_glyph.py, hooks in the glyph network and C1 paint): caps and small caps draw and measure the capital, small capitals at 0.8 size, hidden text no width and no ink (Word with marks off), spacing joins the advance, double strike as a second line through rZ, run shade as a rect under darker wins.
- Writer: rPr in schema order (caps, smallCaps before strike, dstrike after, vanish after noProof, spacing after color, shd after u); links and bookmarks opened and closed around runs; external targets listed in document.xml.rels as rIdL<n>; contextualSpacing and widowControl w:val="0" from slot cell 4095.
- First run of test/feat1.js: 15/22. Fixes: number() pads with zeros and has no sign, so spacing is written as an optional minus and vnum; test pixel helpers had swapped arguments. Then 22/22.
- Contextual spacing is applied the way rv_a5 applies a style's: the gap is dropped at the end of open (values lost on save, flag kept).

## Step 3: FLOPs per event (coordinator request; main merged in for test/flops.js)
- First measure: background layout +14%, most events +8%. gprof wheel: glyph metrics +15% (small caps had its own size leaf, so every size's gate gained inputs), feat1 group 86k (enable neuron on every glyph call), paint +27k.
- Fixes: small capitals share the script size leaf (0.72, not 0.8; one split before the normal leaf, so plain text pays nothing); the glyph network reads RSX from the style port directly (no bus gate woken per character); every decoded flag is a gate on the one nonzero test, so pulls stop there; paint gates on the shade and double strike flags.
- After: gprof wheel work 5,658,461 vs 5,618,241 on main (+0.7%); flops.js: every event within +1.0% of docs/flops_baseline.json (background layout +0.98%, typing +0.24 to 0.78%).
- test/feat1.js 22/22 after the changes.

## Final full run (background, one at a time)
e2e 210/210, tier2 49/49, look 31/31, t3_table, t3_pic, t3_misc no FAIL, t4_docx 18/18, t4_pdf 7/7, roundtrip and touch no FAIL, a5_docx no FAIL (a01 open 9,943,745 edges, was 9,912,549), imp2 all pass, imp3 49/49, imp4 101/101, imp5 49/0, imp6 20/0, t4 ran, feat1 24/24, audit 67/67.
a4 first crashed inside its LibreOffice text conversion (execSync of soffice failed, likely a busy shared machine); rerun alone: 0 failed of 50.
Two builds byte identical. Page 3,806,957 bytes (was 3,795,433).
Not done: equations (task 2) and the PARITY PDF gaps (task 3).
