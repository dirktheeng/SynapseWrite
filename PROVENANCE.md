# Provenance of the SynapseWrite network

Written by gen/rv_a11_prov.py at every build, from net.groups. Every weight comes from the listed generator files; none is trained, fitted or searched.

247135 neurons, 490060 edges, 188 layers, 3947 control states.

| Sub-network | Purpose | Generator files (neurons) | Neurons | Inputs |
|---|---|---|---|---|
| bank and port wiring | The memory, image and event ports and their shared wires. | gen/app.py (1299) | 1299 | 7957 |
| glyph network | Selects and addresses a character cell for drawing. | gen/app.py (391), gen/imp3_zoom_pre.py (155) | 546 | 9650 |
| glyph metrics | Character advance and kerning trees. | gen/app.py (20453) | 20453 | 58638 |
| glyph unit | Draws a character from its edge network into the glyph store, in its own clock domain. | gen/glyphnet.py (10800) | 10800 | 40090 |
| glyph pixel records | A small glyph drawn black on white is recorded off the row plane, so later draws are one read and one patch. | gen/glyphnet.py (19104) | 19104 | 38324 |
| snapping layer | Fits outline heights to the pixel grid for a given size. | gen/glyphnet.py (331) | 331 | 1314 |
| glyph geometry | Scales outline coordinates by the drawn size. | gen/glyphnet.py (231) | 231 | 809 |
| glyph store | Keeps drawn glyphs in memory and copies them to the screen. | gen/glyphnet.py (17) | 17 | 54 |
| stem units | Stem position units for the hinting of letters. |  | 0 | 0 |
| row sequencer | Steps the glyph unit through the rows of a character. | gen/glyphnet.py (29) | 29 | 72 |
| glyph weights (outline edges) | Font outlines as edges in weights, one group per glyph program. | gen/glyphnet.py (143996) | 143996 | 718257 |
| ramp bank | Coverage ramps for the edge network. | gen/glyphnet.py (4978) | 4978 | 10819 |
| coverage | Adds edge coverage into pixel coverage. | gen/glyphnet.py (1816), gen/imp3_zoom_pre.py (582), gen/app.py (38) | 2436 | 12958 |
| style interner | Finds or adds a style record in the interned table, in its own clock domain. | gen/app.py (103) | 103 | 232 |
| glyph patch | Assembles glyph coverage into a color patch for the patch port. | gen/app.py (9) | 9 | 127 |
| shared control registers | Editor state registers and the selection order comparators. | gen/app.py (242), gen/rv_a4_regs.py (81), gen/imp4_regs.py (55), gen/t1_features.py (45), gen/imp3_regs.py (40), gen/rv_a3_pre.py (38), gen/imp3_zoom_pre.py (13), gen/imp5_regs.py (12), gen/imp4_list.py (3) | 529 | 5041 |
| ribbon display list | One sequencer that plays draw records for the ribbon, menus and labels from read only memory, one item per tick. | gen/rv_a9_dl.py (150) | 150 | 431 |
| event dispatch | One neuron left from the first dispatcher; routing now lives in raw event interpretation and the state rules. | gen/app.py (1) | 1 | 3 |
| pointer | Draws the mouse pointer, saves and restores the colors under it, and chooses its shape from the screen. | gen/pointer2.py (55), gen/pointer.py (48), gen/app.py (15) | 118 | 789 |
| raw event interpretation | Turns raw browser events (key name code units, button masks, pointer types, field text, touch positions) into cooked events and browser commands. | gen/rv_a11_input.py (221), gen/app.py (91), gen/imp3_zoom_pre.py (12), gen/imp5_vr_md.py (5) | 329 | 1334 |
| view: wheel and thumb drag | Shift+wheel and sideways wheel deltas slide a wide page; the thumb of the bar at the foot drags at its drawn scale. | gen/imp5_wheel.py (22) | 22 | 62 |
| character maps | Unicode to internal code tables and back (Windows-1252 block). | gen/app.py (94) | 94 | 220 |
| key handling | Maps each key and modifier to its editing command. | gen/app.py (466), gen/rv_a3_pre.py (127), gen/imp3_zoom_pre.py (12), gen/t1_features.py (2) | 607 | 6607 |
| screenshot hit test | Reads object ids from the screen image and maps a click to a document position; also the blink tick check of the screen against the line table. | gen/t1_features.py (150), gen/app.py (117), gen/rv_a7_regs.py (115) | 382 | 1118 |
| edit primitives | Character and paragraph insert and delete with undo logging. | gen/app.py (194), gen/rv_a7_regs.py (2) | 196 | 578 |
| undo | Undo and redo walkers over the log. | gen/app.py (111) | 111 | 474 |
| range walker | Walks a selection for copy, cut, delete and formatting. | gen/app.py (362), gen/rv_a4_regs.py (76), gen/t1_features.py (29) | 467 | 2243 |
| find and replace | Search automaton over the document and replace. | gen/t1_features.py (197), gen/app.py (82) | 279 | 747 |
| paste | Inserts clipboard text with paragraph splitting. | gen/app.py (208) | 208 | 2643 |
| bulk edits | Window walkers for bulk formatting, copy, save, paste and find. | gen/rv_a7_bulk.py (659) | 659 | 6762 |
| find across paragraphs | One matcher for queries holding paragraph marks, used by the walker, the counter and the highlight. | gen/imp3_find.py (205), gen/imp3_find_paint.py (28) | 233 | 649 |
| clipboard formatting | Keeps style cells and paragraph records of the own copy and puts them back when the pasted text equals it. | gen/imp3_clip.py (103) | 103 | 242 |
| layout and paint | Walks paragraphs, places lines and words, draws text, selection, pictures. | gen/app.py (977), gen/rv_a3_paint.py (96), gen/imp4_list.py (31), gen/rv_a3_pre.py (30), gen/t4_spell.py (26), gen/rv_a4_regs.py (20) | 1180 | 4717 |
| spell dictionary | Walks a word automaton held as a read only table, one read per painted letter, and marks words. | gen/t4_spell.py (67) | 67 | 165 |
| line breaking | Greedy line breaker and alignment. | gen/app.py (268), gen/rv_a3_pre.py (30) | 298 | 862 |
| chrome | Autoscroll, caret, scrollbar and status bar. | gen/app.py (1661) | 1661 | 11788 |
| zoom | Zoom levels and read mode commands, status bar controls, and pictures at other scales. | gen/imp3_zoom.py (457) | 457 | 3692 |
| view: side scroll and vertical ruler | Slides a page wider than the window, its bar, and draws the vertical ruler. | gen/imp4_view.py (301), gen/app.py (212), gen/t1_features.py (44) | 557 | 3209 |
| ribbon actions | Maps button ids to commands. | gen/app.py (155) | 155 | 256 |
| docx writer | Writes the document XML parts. | gen/t2_write.py (648), gen/app.py (341), gen/rv_a10_num.py (79), gen/rv_a10_rom.py (23) | 1091 | 9261 |
| docx crc | CRC of the bytes written to the zip container. | gen/rv_a7_save.py (2707), gen/app.py (4) | 2711 | 41587 |
| pdf writer | Writes PDF objects, text and pictures. | gen/pdf_write.py (1395) | 1395 | 4413 |
| docx reader | Unzips, inflates and parses document XML. | gen/docx_read.py (2829) | 2829 | 16385 |
| png reader | Decodes PNG files to pixel words. | gen/docx_read.py (311), gen/a12_guard.py (61) | 372 | 4192 |
| zip crc check | Zip CRC check on open: the inflated main part runs through the save CRC network and must match the central directory. | gen/a12_guard.py (18) | 18 | 104 |
| prompt bar | One bar that takes a short text for a color, a style name or a font name. | gen/imp4_prompt.py (524) | 524 | 2033 |
| extended characters | UTF-8 and code units for characters past Latin-1. | gen/imp4_prompt.py (131) | 131 | 881 |
| tier 4 features | Tracked changes, fields, equations, mail merge. | gen/t4_features.py (702) | 702 | 1918 |
| docx deflate | LZ77 with fixed Huffman compression for the zip container. | gen/t4_features.py (242) | 242 | 863 |
| docx reader tier 4 | Reads tracked marks and fields. | gen/t4_features.py (1368) | 1368 | 3424 |
| tier 2 | Styles, paragraph commands, lists and typed sizes. | gen/t2_features.py (391) | 391 | 1023 |
| docx reader tier 2 | Reads styles, numbering, run and paragraph properties. | gen/t2_features.py (813) | 813 | 3004 |
| tier3 | Remaining tier 3 commands and undo op 8. | gen/t3_features.py (22) | 22 | 46 |
| tables | Table scan, insert, row and column edits, shading, border hit zones and drag. | gen/t3_features.py (637) | 637 | 1785 |
| sections | Section records, breaks and page setup. | gen/t3_features.py (112) | 112 | 326 |
| zip container | Zip member table, central directory, and table XML for saving. | gen/t3_features.py (210) | 210 | 465 |
| docx reader tier 3 | Reader additions for parts walking. | gen/t3_features.py (127) | 127 | 411 |
| pdf tables | PDF page size, table rules and shading. | gen/t3_features.py (55) | 55 | 98 |
| pictures | Picture handles, resizing by resampling, PNG writing, and reading pictures from a file. | gen/t3_features.py (926) | 926 | 4354 |
| notes and balloons | Wrapped text, comment balloons and footnotes. | gen/t3_features.py (257) | 257 | 614 |
| headers and footers | Header and footer strings and their edit bar. | gen/t3_features.py (112) | 112 | 404 |
| table of contents | Builds and updates the table of contents. | gen/t3_features.py (175) | 175 | 521 |
| docx writer tier 3 | Writes section properties, tabs, markers, comments, notes, headers and footers. | gen/t3_features.py (306) | 306 | 665 |
| docx reader notes | Reads note, comment and header parts. | gen/t3_features.py (819) | 819 | 2442 |
| style create and rename | New and renamed styles, and applying character styles. | gen/imp4_style.py (177) | 177 | 687 |
| list formats | The list format menu and reading numFmt and lvlText. | gen/imp4_list2.py (151) | 151 | 543 |
| column breaks | Column breaks: typed with Ctrl+Shift+Enter, read and written as w:br of type column, laid out as a move to the second column. | gen/imp5_breaks.py (22) | 22 | 44 |
| vertical ruler drag | Top and bottom margin drags on the vertical ruler, released through the section edit with undo. | gen/imp5_vruler.py (9) | 9 | 92 |
| repeat last command | F4 repeats the last character format, alignment, paragraph style or list command. | gen/imp6_feat.py (21) | 21 | 47 |
| recent colors | Recent colors: the last eight exact text colors, drawn under Color Picker and applied again with a click. | gen/imp6_feat.py (276) | 276 | 2793 |
| canvas look | Page shadow and the canvas around the page. | gen/rv_a2_canvas.py (82) | 82 | 197 |
| a4 commands | Word commands: repeat, format painter, keep rules and others. | gen/rv_a4_features.py (344) | 344 | 1272 |
| a4 keep | Keep with next and keep lines in pagination. | gen/rv_a4_features.py (56) | 56 | 144 |
| a4 borders | Paragraph borders and shading on screen and in PDF. | gen/rv_a4_features.py (387) | 387 | 1416 |
| a4 docx | Reads and writes the a4 paragraph properties. | gen/rv_a4_features.py (271) | 271 | 700 |
| a4 tabs | Tab stops. | gen/rv_a4_features.py (160) | 160 | 510 |
| a4 ruler | Ruler display and drag. | gen/rv_a4_features.py (332) | 332 | 1447 |
| a4 merge | Merged table cells. | gen/rv_a4_features.py (639) | 639 | 1414 |
| a4 pagenum | Page number formats and section start values. | gen/rv_a4_features.py (254) | 254 | 583 |
| docx reader rv_a5 | Reader fidelity (nested tables, row spans, spacing, truncation), plus spell suggestions and the saved list of added words. | gen/rv_a6_spell.py (845), gen/rv_a5_docx.py (345), gen/app.py (303) | 1493 | 13742 |
| rv a3 interaction | Editing keys, word and page motion, right click, autoscroll, context menu, and the late tier 1 features. | gen/t1_features.py (2039), gen/rv_a3_keys.py (655), gen/pointer3.py (86), gen/rv_a4_features.py (79), gen/ui.py (42) | 2901 | 25112 |
| file output command | Selects the length, data base and file name the glue saves. | gen/rv_a11_out.py (5) | 5 | 8 |
| screen check | Compares one line of the screen id plane against the line table on each blink tick and repairs by repainting. | gen/rv_a11_out.py (23) | 23 | 56 |
| compiled control | Every state rule compiled together: the gated sums that give each register its next value, and the return dispatchers. | gen/app.py (9992) | 9992 | 54942 |
