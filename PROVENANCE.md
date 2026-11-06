# Provenance of the SynapseWrite network

Written by gen/rv_a11_prov.py at every build, from net.groups. Every weight comes from the listed generator files; none is trained, fitted or searched.

443847 neurons, 941795 edges, 166 layers, 3501 control states.

| Sub-network | Purpose | Generator files (neurons) | Neurons | Inputs |
|---|---|---|---|---|
| bank and port wiring | The memory, image and event ports and their shared wires. | gen/app.py (1287) | 1287 | 6726 |
| glyph network | Selects and addresses a character cell for drawing. | gen/app.py (507) | 507 | 7843 |
| glyph metrics | Character advance and kerning trees. | gen/app.py (17875) | 17875 | 50620 |
| glyph unit | Draws a character from its edge network into the glyph store, in its own clock domain. | gen/glyphnet.py (19503) | 19503 | 59479 |
| snapping layer | Fits outline coordinates to the pixel grid for a given size. | gen/glyphnet.py (236) | 236 | 915 |
| glyph geometry | Scales outline coordinates by the drawn size. | gen/glyphnet.py (159) | 159 | 589 |
| glyph store | Keeps drawn glyphs in memory and copies them to the screen. | gen/glyphnet.py (16) | 16 | 50 |
| stem units | Stem position units for the hinting of letters. |  | 0 | 0 |
| row sequencer | Steps the glyph unit through the rows of a character. | gen/glyphnet.py (29) | 29 | 72 |
| glyph weights (outline edges) | Font outlines as edges in weights, one group per glyph program. | gen/glyphnet.py (360490) | 360490 | 1304004 |
| ramp bank | Coverage ramps for the edge network. | gen/glyphnet.py (4978) | 4978 | 10819 |
| coverage | Adds edge coverage into pixel coverage. | gen/glyphnet.py (1816), gen/app.py (11) | 1827 | 10496 |
| style interner | Finds or adds a style record in the interned table, in its own clock domain. | gen/app.py (53) | 53 | 122 |
| glyph patch | Assembles glyph coverage into a color patch for the patch port. | gen/app.py (6) | 6 | 84 |
| shared control registers | Editor state registers and the selection order comparators. | gen/app.py (240), gen/rv_a4_regs.py (81), gen/t1_features.py (45), gen/rv_a3_pre.py (38) | 404 | 4048 |
| ribbon display list | Token chain whose weights hold each ribbon draw item. | gen/app.py (9073), gen/rv_a9_dl.py (150) | 9223 | 34627 |
| event dispatch | Routes each cooked event to its handler; timer, wheel and move handling. | gen/app.py (1) | 1 | 3 |
| pointer | Draws the mouse pointer, saves and restores the colors under it, and chooses its shape from the screen. | gen/pointer2.py (51), gen/pointer.py (48), gen/app.py (15) | 114 | 731 |
| raw event interpretation | Turns raw browser events (key name code units, button masks, pointer types, field text, touch positions) into cooked events and browser commands. | gen/rv_a11_input.py (215), gen/app.py (84) | 299 | 1213 |
| character maps | Unicode to internal code tables and back (Windows-1252 block). | gen/app.py (89) | 89 | 182 |
| key handling | Maps each key and modifier to its editing command. | gen/app.py (414), gen/rv_a3_pre.py (69), gen/t1_features.py (2) | 485 | 4545 |
| screenshot hit test | Reads object ids from the screen image and maps a click to a document position; also the blink tick check of the screen against the line table. | gen/t1_features.py (151), gen/rv_a7_regs.py (115), gen/app.py (110) | 376 | 1023 |
| edit primitives | Character and paragraph insert and delete with undo logging. | gen/app.py (194), gen/rv_a7_regs.py (2) | 196 | 569 |
| undo | Undo and redo walkers over the log. | gen/app.py (107) | 107 | 438 |
| range walker | Walks a selection for copy, cut, delete and formatting. | gen/app.py (277), gen/rv_a4_regs.py (76), gen/t1_features.py (29) | 382 | 1682 |
| find and replace | Search automaton over the document and replace. | gen/t1_features.py (196), gen/app.py (82) | 278 | 719 |
| paste | Inserts clipboard text with paragraph splitting. | gen/app.py (199) | 199 | 2595 |
| bulk edits | Window walkers for bulk formatting, copy, save, paste and find. | gen/rv_a7_bulk.py (656) | 656 | 6750 |
| layout and paint | Walks paragraphs, places lines and words, draws text, selection, pictures. | gen/app.py (866), gen/rv_a3_paint.py (95), gen/rv_a3_pre.py (30), gen/t4_spell.py (26), gen/rv_a4_regs.py (20) | 1037 | 3814 |
| spell dictionary | Word list stored as an automaton in weights, with word marks. | gen/t4_spell.py (67) | 67 | 165 |
| line breaking | Greedy line breaker and alignment. | gen/app.py (249), gen/rv_a3_pre.py (30) | 279 | 810 |
| chrome | Autoscroll, caret, scrollbar and status bar. | gen/app.py (1737), gen/t1_features.py (44) | 1781 | 11845 |
| ribbon actions | Maps button ids to commands. | gen/app.py (152) | 152 | 250 |
| docx writer | Writes the document XML parts. | gen/t2_write.py (589), gen/app.py (341), gen/rv_a10_num.py (79), gen/rv_a10_rom.py (23) | 1032 | 8810 |
| docx crc | CRC of the bytes written to the zip container. | gen/rv_a7_save.py (2771), gen/app.py (4) | 2775 | 74350 |
| pdf writer | Writes PDF objects, text and pictures. | gen/pdf_write.py (1236) | 1236 | 3878 |
| docx reader | Unzips, inflates and parses document XML. | gen/docx_read.py (1843) | 1843 | 13612 |
| png reader | Decodes PNG files to pixel words. | gen/docx_read.py (311), gen/a12_guard.py (58) | 369 | 3907 |
| tier 4 features | Tracked changes, fields, equations, mail merge. | gen/t4_features.py (699) | 699 | 1910 |
| docx deflate | LZ77 with fixed Huffman compression for the zip container. | gen/t4_features.py (242) | 242 | 863 |
| docx reader tier 4 | Reads tracked marks and fields. | gen/t4_features.py (1368) | 1368 | 3425 |
| tier 2 | Styles, paragraph commands, lists and typed sizes. | gen/t2_features.py (354) | 354 | 846 |
| docx reader tier 2 | Reads styles, numbering, run and paragraph properties. | gen/t2_features.py (528) | 528 | 1657 |
| tier3 | Remaining tier 3 commands and undo op 8. | gen/t3_features.py (22) | 22 | 46 |
| tables | Table scan, insert, row and column edits, shading, border hit zones and drag. | gen/t3_features.py (619) | 619 | 1663 |
| sections | Section records, breaks and page setup. | gen/t3_features.py (106) | 106 | 284 |
| zip container | Zip member table, central directory, and table XML for saving. | gen/t3_features.py (210) | 210 | 465 |
| docx reader tier 3 | Reader additions for parts walking. | gen/t3_features.py (106) | 106 | 381 |
| pdf tables | PDF page size, table rules and shading. | gen/t3_features.py (55) | 55 | 98 |
| pictures | Picture handles, resizing by resampling, PNG writing, and reading pictures from a file. | gen/t3_features.py (918) | 918 | 4319 |
| notes and balloons | Wrapped text, comment balloons and footnotes. | gen/t3_features.py (253) | 253 | 606 |
| headers and footers | Header and footer strings and their edit bar. | gen/t3_features.py (112) | 112 | 404 |
| table of contents | Builds and updates the table of contents. | gen/t3_features.py (175) | 175 | 521 |
| docx writer tier 3 | Writes section properties, tabs, markers, comments, notes, headers and footers. | gen/t3_features.py (306) | 306 | 662 |
| docx reader notes | Reads note, comment and header parts. | gen/t3_features.py (819) | 819 | 2441 |
| canvas look | Page shadow and the canvas around the page. | gen/rv_a2_canvas.py (82) | 82 | 197 |
| a4 commands | Word commands: repeat, format painter, keep rules and others. | gen/rv_a4_features.py (320) | 320 | 1100 |
| a4 keep | Keep with next and keep lines in pagination. | gen/rv_a4_features.py (56) | 56 | 144 |
| a4 borders | Paragraph borders and shading on screen and in PDF. | gen/rv_a4_features.py (387) | 387 | 1414 |
| a4 docx | Reads and writes the a4 paragraph properties. | gen/rv_a4_features.py (268) | 268 | 694 |
| a4 tabs | Tab stops. | gen/rv_a4_features.py (160) | 160 | 510 |
| a4 ruler | Ruler display and drag. | gen/rv_a4_features.py (307) | 307 | 952 |
| a4 merge | Merged table cells. | gen/rv_a4_features.py (639) | 639 | 1414 |
| a4 pagenum | Page number formats and section start values. | gen/rv_a4_features.py (254) | 254 | 583 |
| docx reader rv_a5 | Reader fidelity: nested tables, row spans, spacing, truncation and others. | gen/rv_a6_spell.py (845), gen/rv_a5_docx.py (315), gen/app.py (282) | 1442 | 12424 |
| rv a3 interaction | Editing keys, word and page motion, right click, autoscroll, context menu. | gen/t1_features.py (1816), gen/rv_a3_keys.py (655), gen/rv_a4_features.py (79), gen/pointer3.py (74), gen/ui.py (42) | 2666 | 19960 |
| file output command | Selects the length, data base and file name the glue saves. | gen/rv_a11_out.py (5) | 5 | 8 |
| screen check | Compares one line of the screen id plane against the line table on each blink tick and repairs by repainting. | gen/rv_a11_out.py (23) | 23 | 56 |
