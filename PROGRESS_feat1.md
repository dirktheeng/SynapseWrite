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
