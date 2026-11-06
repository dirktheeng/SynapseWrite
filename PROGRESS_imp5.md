# PROGRESS imp5

Base: main at b1e876b. Baseline build: page 3,787,439 bytes, gz weights 2,813,152.

## 1. Side scroll by wheel and by dragging the thumb
Why: PARITY Zoom row said the thumb cannot be dragged and the wheel does not move sideways.
What: glue now encodes the wheel's raw sideways delta (ev_a = deltaX+1000) and raw modifier bits (Ctrl 1, Shift 2), as it already did for mousedown; it interprets nothing.
Network: gen/imp5_wheel.py. In WH, zoom now keys on modifier bit 0 only; Shift (bit 1) on a wide page routes the vertical delta into the slide register hsv; a sideways delta at least as large as the vertical one does the same. Both go through V8_HS0, which clamps and repaints. A press on the thumb (the default branch of V8_HC) now holds v8dg with press x and slide; MV with v8dg sets hsv = slide at press + travel / k, k the same per zoom scale that draws the thumb; mouse up clears v8dg.
Run: test/imp5.js side: 8 passed, 0 failed first try (thumb 0..952 to 226..1178 on Shift+wheel 300; drag of 150 px moves thumb exactly 150 px; past the end clamps at 1261). Screenshot build/imp5_d1.png looked right.

## 2. Undo of style creation
Why: Styles row said creating a style is not undone, only its use.
What: undo op 13 (gen/app.py undo and redo decoders widened from 13 to 14 lines) sets the style count register nsty to the record's old or new value. gen/imp4_style.py logs it in V5_N2. First try: the creation and its use landed in different undo groups, so it took two undos. Dumped the log records (op,p,o,ch,st,grp): creation grp 8, use grp 9. The paragraph path opens a group twice (T2_SA1, then FMTS over the paragraph text when it has any), the character path once (FMTS). V5_N6 now steps grp back by one on the character path, and on the paragraph path holds T2_SA1 with a4cfq and steps back by one only when the paragraph has text.
Runs: imp5 style 6 passed 0 failed (including an empty paragraph); imp4 style 15/15.

## 3. Other shortcuts
Why: Other shortcuts row is Partial. Added rules to the key rule table (gen/imp5_keys.py, spliced into rv_key_rules): Ctrl+Shift+Space no-break space, Ctrl+Shift+- no-break hyphen U+2011, Ctrl+Shift+E tracking on and off, Ctrl+Shift+8 show marks, F9 update fields (key name F9 added to the network's key table as 138), Ctrl+Shift+F and Ctrl+Shift+P open the font and size menus.
Runs: first try, the no-break hyphen went through TYPE and was lost: code units past Latin-1 must enter through T2_KU and the character map. Fixed. Then it drew a box: Carlito's subsets have neither U+2011 nor U+2010; gen/rom.py ext_cmap now aliases U+2011 to the face's hyphen, as Word draws it. Screenshot crop confirmed "a b-c". A test regex for "tracking off" was wrong (spanned two runs); corrected before it was ever committed.
imp5 keys: 9 passed, 0 failed.
