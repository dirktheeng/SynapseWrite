# Tier 2 progress log

Each entry says what was tried, why, and what the run showed.

1. Read the compiler, engine, glue, tests. Baseline: 142,109 neurons, 1,695,836 edges, 2.9 MB page; e2e 43/43; roundtrip all true.
2. Measured glyph ink. ASCII ink was 158k weights across small sizes but tripled by three separate coverage planes (475k), and 693k across large sizes. Raw Latin-1 would add 217k+936k.
3. Decision: one coverage plane with gated routes, plus accented letters compiled as base letter plus shared pixel delta (differences of one level ignored), so Latin-1 adds about 678k and tripling removal gives back 317k.
4. Palettes moved to a 4 bit per channel grid so a pixel forms any color from 24 channel bit gates. That also removes per-color planes, gives 32 foreground colors and 12 background colors for about the same neuron count. Ribbon grays and blues were moved to the same grid.
5. First latency run: wheel 120 ms, type at end 535k edges. Cause: color bit lines fan out to every pixel gate of the plane on each slow glyph. Fix: the coverage threshold became the gate's enable and color lines are read lazily, so only inked pixels are visited. Wheel back to about 70 ms, type at end 100k edges.
6. Advances became font table values in ems per face scaled by the size, so glyph positions no longer accumulate rounding error. Kerning: 701 GPOS pairs above 1.4 percent of an em, ASCII only, applied between the previous and current character in both layout and paint.
7. Style cell grew to 19 bits: strike bit 11, vertical 12-13, highlight 14-16, color high bits 17-18. Superscript and subscript draw a smaller compiled size, the line keeps nominal metrics. Two sizes added (7, 8 pt) for scripts.
8. Paragraph properties at slot offsets 3693 to 3698, loaded with one 6 cell port. LIST cell packs kind and level. Changes are logged with a new undo op 6 (paragraph field) and op 7 (absolute cell for the style table).
9. Style table at bank 40000, 48 cells per record, ROM image at 26000 restored on open. Apply, update-from-paragraph (walks every paragraph of the style), TOC by style index, next paragraph Normal.
10. Docx writer rewritten as t2_write.py: static members, dynamic styles.xml and document.xml each with crc and size patched by a shared subroutine, UTF-8 output, numbering.xml, numPr, pStyle, spacing, ind, strike, vertAlign, highlight.
11. Docx reader walks numbering, styles, document in three passes. Attribute parsers for spacing and ind, twips to pixels by subtraction, on/off property values, UTF-8 decode through the code map, nearest palette color through a compiled 512 line table, basedOn, docDefaults.
12. Parser offset bugs found by tests: numFmt value offset, line and left attribute quote handling, styleId offset. Ctrl+Home and Ctrl+End were missing and added, which also fixed caret blink flakiness in the image tests.
13. Foreign file test built with python-docx (its template comes from Word): headings, Latin-1, run formats, style based lists all read. Found: style table too small (32) so moved to 196 records; numbered list after bullets saved under the bullet numId; palette lacked Office theme colors and got them.
