# Provenance of the SynapseWrite network

Written by gen/rv_a11_prov.py at every build, from net.groups. Every weight comes from the listed generator files; none is trained, fitted or searched.

419777 neurons, 2457713 edges, 139 layers, 2426 control states.

| Sub-network | Purpose | Generator files (neurons) | Neurons | Inputs |
|---|---|---|---|---|
| bank and port wiring | The memory, image and event ports and their shared wires. | gen/app.py (1281) | 1281 | 27491 |
| glyph network | Selects and addresses a character cell for drawing. | gen/app.py (184) | 184 | 16388 |
| glyph patch | Assembles glyph coverage into a color patch for the patch port. | gen/app.py (95293) | 95293 | 1935616 |
| glyph metrics | Character advance and kerning trees. | gen/app.py (6327) | 6327 | 18352 |
| glyph weights (font outlines) | Font outlines stored as weights, drawn by the glyph network. | gen/app.py (47952) | 47952 | 99870 |
| shared control registers | Editor state registers and the selection order comparators. | gen/app.py (215), gen/t1_features.py (45) | 260 | 2702 |
| event dispatch | Routes each cooked event to its handler; timer, wheel and move handling. | gen/app.py (1) | 1 | 3 |
| pointer | Draws the mouse pointer, saves and restores the colors under it, and chooses its shape from the screen. | gen/pointer.py (3417), gen/pointer2.py (45), gen/app.py (16) | 3478 | 2639 |
| raw event interpretation | Turns raw browser events (key name code units, button masks, pointer types, field text, touch positions) into cooked events and browser commands. | gen/rv_a11_input.py (202), gen/app.py (46) | 248 | 1006 |
| character maps | Unicode to internal code tables and back (Windows-1252 block). | gen/app.py (89) | 89 | 182 |
| key handling | Maps each key and modifier to its editing command. | gen/app.py (585), gen/t1_features.py (10) | 595 | 2286 |
| screenshot hit test | Reads object ids from the screen image and maps a click to a document position; also the blink tick check of the screen against the line table. | gen/t1_features.py (141), gen/app.py (75) | 216 | 534 |
| edit primitives | Character and paragraph insert and delete with undo logging. | gen/app.py (168) | 168 | 436 |
| undo | Undo and redo walkers over the log. | gen/app.py (94) | 94 | 289 |
| range walker | Walks a selection for copy, cut, delete and formatting. | gen/app.py (235), gen/t1_features.py (34) | 269 | 1185 |
| find and replace | Search automaton over the document and replace. | gen/t1_features.py (199), gen/app.py (80) | 279 | 691 |
| paste | Inserts clipboard text with paragraph splitting. | gen/app.py (645) | 645 | 3060 |
| layout and paint | Walks paragraphs, places lines and words, draws text, selection, pictures. | gen/app.py (800), gen/t4_spell.py (15) | 815 | 2682 |
| spell dictionary | Word list stored as an automaton in weights, with word marks. | gen/t4_spell.py (90510) | 90510 | 191147 |
| line breaking | Greedy line breaker and alignment. | gen/app.py (347) | 347 | 1138 |
| chrome | Autoscroll, caret, scrollbar and status bar. | gen/app.py (1269), gen/t1_features.py (62) | 1331 | 10879 |
| ribbon actions | Maps button ids to commands. | gen/app.py (177) | 177 | 279 |
| docx writer | Writes the document XML parts. | gen/t2_write.py (2912), gen/t3_pre.py (364), gen/app.py (343) | 3619 | 299859 |
| pdf writer | Writes PDF objects, text and pictures. | gen/pdf_write.py (130348) | 130348 | 147744 |
| docx reader | Unzips, inflates and parses document XML. | gen/docx_read.py (3603) | 3603 | 9729 |
| png reader | Decodes PNG files to pixel words. | gen/docx_read.py (341) | 341 | 1002 |
| tier 4 features | Tracked changes, fields, equations, mail merge. | gen/t4_features.py (1432) | 1432 | 5516 |
| docx deflate | LZ77 with fixed Huffman compression for the zip container. | gen/t4_features.py (802) | 802 | 1481 |
| docx reader tier 4 | Reads tracked marks and fields. | gen/t4_features.py (63) | 63 | 138 |
| tier 2 | Styles, paragraph commands, lists and typed sizes. | gen/t2_features.py (386) | 386 | 854 |
| docx reader tier 2 | Reads styles, numbering, run and paragraph properties. | gen/t2_features.py (947) | 947 | 2386 |
| tier3 | Remaining tier 3 commands and undo op 8. | gen/t3_features.py (26) | 26 | 50 |
| tables | Table scan, insert, row and column edits, shading, border hit zones and drag. | gen/t3_features.py (635) | 635 | 1535 |
| sections | Section records, breaks and page setup. | gen/t3_features.py (102) | 102 | 231 |
| zip container | Zip member table, central directory, and table XML for saving. | gen/t3_features.py (4956) | 4956 | 16723 |
| docx reader tier 3 | Reader additions for parts walking. | gen/t3_features.py (371) | 371 | 944 |
| pdf tables | PDF page size, table rules and shading. | gen/t3_features.py (500) | 500 | 714 |
| pictures | Picture handles, resizing by resampling, PNG writing, and reading pictures from a file. | gen/t3_features.py (2973) | 2973 | 16810 |
| notes and balloons | Wrapped text, comment balloons and footnotes. | gen/t3_features.py (304) | 304 | 631 |
| headers and footers | Header and footer strings and their edit bar. | gen/t3_features.py (113) | 113 | 397 |
| table of contents | Builds and updates the table of contents. | gen/t3_features.py (187) | 187 | 531 |
| docx writer tier 3 | Writes section properties, tabs, markers, comments, notes, headers and footers. | gen/t3_features.py (3777) | 3777 | 4029 |
| docx reader notes | Reads note, comment and header parts. | gen/t3_features.py (1226) | 1226 | 3307 |
| late commands | File screen, table and picture ribbon commands, clipboard notices. | gen/app.py (323) | 323 | 9109 |
| ribbon display list | Token chain whose weights hold each ribbon draw item. | gen/ui.py (5081), gen/t1_features.py (2264), gen/pointer3.py (64) | 7409 | 21549 |
| file output command | Selects the length, data base and file name the glue saves. | gen/rv_a11_out.py (5) | 5 | 8 |
| screen check | Compares one line of the screen id plane against the line table on each blink tick and repairs by repainting. | gen/app.py (4747), gen/rv_a11_out.py (23) | 4770 | 22460 |
