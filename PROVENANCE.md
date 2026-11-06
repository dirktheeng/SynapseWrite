# Provenance of the SynapseWrite network

Written by gen/rv_a11_prov.py at every build, from net.groups. Every weight comes from the listed generator files; none is trained, fitted or searched.

238966 neurons, 466904 edges, 187 layers, 4556 control states.

| Sub-network | Purpose | Generator files (neurons) | Neurons | Inputs |
|---|---|---|---|---|
| bank and port wiring | The memory, image and event ports and their shared wires. | gen/app.py (1302) | 1302 | 8630 |
| glyph network | Selects and addresses a character cell for drawing. | gen/feat1_glyph.py (347), gen/app.py (253), gen/imp3_zoom_pre.py (155) | 755 | 10225 |
| feat1 run effects | Decodes the extended field of a style entry for the glyph network: caps and small caps draw and measure the capital, small capitals take a smaller size, hidden text takes no width or ink, character spacing joins the advance. | gen/feat1_glyph.py (39) | 39 | 174 |
| glyph metrics | Character advance and kerning trees. | gen/app.py (20757) | 20757 | 61819 |
| glyph unit | Draws a character from its edge network into the glyph store, in its own clock domain. | gen/glyphnet.py (10799) | 10799 | 40089 |
| glyph pixel records | A small glyph drawn black on white is recorded off the row plane, so later draws are one read and one patch. | gen/glyphnet.py (19104) | 19104 | 38324 |
| snapping layer | Fits outline heights to the pixel grid for a given size. | gen/glyphnet.py (338) | 338 | 1137 |
| glyph geometry | Scales outline coordinates by the drawn size. | gen/glyphnet.py (235) | 235 | 813 |
| glyph store | Keeps drawn glyphs in memory and copies them to the screen. | gen/glyphnet.py (17) | 17 | 54 |
| stem units | Stem position units for the hinting of letters. |  | 0 | 0 |
| row sequencer | Steps the glyph unit through the rows of a character. | gen/glyphnet.py (29) | 29 | 72 |
| glyph weights (outline edges) | Font outlines as edges in weights, one group per glyph program. | gen/glyphnet.py (130598) | 130598 | 609146 |
| ramp bank | Coverage ramps for the edge network. | gen/glyphnet.py (5475) | 5475 | 10959 |
| coverage | Adds edge coverage into pixel coverage. | gen/glyphnet.py (1312), gen/imp3_zoom_pre.py (583), gen/app.py (36) | 1931 | 14975 |
| style interner | Finds or adds a style record in the interned table, in its own clock domain. | gen/app.py (151) | 151 | 340 |
| glyph patch | Assembles glyph coverage into a color patch for the patch port. | gen/app.py (12) | 12 | 188 |
| shared control registers | Editor state registers and the selection order comparators. | gen/app.py (245), gen/rv_a4_regs.py (81), gen/imp4_regs.py (55), gen/t1_features.py (45), gen/imp3_regs.py (40), gen/rv_a3_pre.py (38), gen/feat1_regs.py (26), gen/imp3_zoom_pre.py (13), gen/imp5_regs.py (12), gen/p2_regs.py (10), gen/imp4_list.py (3) | 568 | 5242 |
| ribbon display list | One sequencer that plays draw records for the ribbon, menus and labels from read only memory, one item per tick. | gen/rv_a9_dl.py (150) | 150 | 431 |
| event dispatch | One neuron left from the first dispatcher; routing now lives in raw event interpretation and the state rules. | gen/app.py (1) | 1 | 3 |
| pointer | Draws the mouse pointer, saves and restores the colors under it, and chooses its shape from the screen. | gen/pointer2.py (55), gen/pointer.py (48), gen/app.py (15) | 118 | 793 |
| raw event interpretation | Turns raw browser events (key name code units, button masks, pointer types, field text, touch positions) into cooked events and browser commands. | gen/rv_a11_input.py (221), gen/app.py (91), gen/imp3_zoom_pre.py (12), gen/imp5_vr_md.py (5) | 329 | 1334 |
| view: wheel and thumb drag | Shift+wheel and sideways wheel deltas slide a wide page; the thumb of the bar at the foot drags at its drawn scale. | gen/imp5_wheel.py (22) | 22 | 62 |
| character maps | Unicode to internal code tables and back (Windows-1252 block). | gen/app.py (94) | 94 | 220 |
| key handling | Maps each key and modifier to its editing command. | gen/app.py (466), gen/rv_a3_pre.py (127), gen/imp3_zoom_pre.py (12), gen/t1_features.py (2) | 607 | 6608 |
| screenshot hit test | Reads object ids from the screen image and maps a click to a document position; also the blink tick check of the screen against the line table. | gen/t1_features.py (150), gen/app.py (117), gen/rv_a7_regs.py (115) | 382 | 1118 |
| edit primitives | Character and paragraph insert and delete with undo logging. | gen/app.py (194), gen/rv_a7_regs.py (2) | 196 | 578 |
| undo | Undo and redo walkers over the log. | gen/app.py (111) | 111 | 474 |
| range walker | Walks a selection for copy, cut, delete and formatting. | gen/app.py (374), gen/rv_a4_regs.py (76), gen/t1_features.py (29) | 479 | 2280 |
| find and replace | Search automaton over the document and replace. | gen/t1_features.py (197), gen/app.py (82) | 279 | 747 |
| paste | Inserts clipboard text with paragraph splitting. | gen/app.py (208) | 208 | 2643 |
| bulk edits | Window walkers for bulk formatting, copy, save, paste and find. | gen/rv_a7_bulk.py (668) | 668 | 6785 |
| find across paragraphs | One matcher for queries holding paragraph marks, used by the walker, the counter and the highlight. | gen/imp3_find.py (205), gen/imp3_find_paint.py (28) | 233 | 649 |
| clipboard formatting | Keeps style cells and paragraph records of the own copy and puts them back when the pasted text equals it. | gen/imp3_clip.py (103) | 103 | 242 |
| layout and paint | Walks paragraphs, places lines and words, draws text, selection, pictures. | gen/app.py (1022), gen/rv_a3_paint.py (96), gen/imp4_list.py (31), gen/rv_a3_pre.py (31), gen/t4_spell.py (26), gen/rv_a4_regs.py (20), gen/feat1_regs.py (1) | 1227 | 5189 |
| spell dictionary | Walks a word automaton held as a read only table, one read per painted letter, and marks words. | gen/t4_spell.py (67) | 67 | 165 |
| line breaking | Greedy line breaker and alignment. | gen/app.py (268), gen/rv_a3_pre.py (31) | 299 | 863 |
| chrome | Autoscroll, caret, scrollbar and status bar. | gen/app.py (1661) | 1661 | 11788 |
| zoom | Zoom levels and read mode commands, status bar controls, and pictures at other scales. | gen/imp3_zoom.py (457) | 457 | 3692 |
| view: side scroll and vertical ruler | Slides a page wider than the window, its bar, and draws the vertical ruler. | gen/imp4_view.py (301), gen/app.py (212), gen/t1_features.py (44) | 557 | 3209 |
| ribbon actions | Maps button ids to commands. | gen/app.py (155) | 155 | 256 |
| docx writer | Writes the document XML parts. | gen/t2_write.py (652), gen/app.py (341), gen/rv_a10_num.py (79), gen/rv_a10_rom.py (23) | 1095 | 11224 |
| docx crc | CRC of the bytes written to the zip container. | gen/rv_a7_save.py (2707), gen/app.py (4) | 2711 | 41587 |
| pdf writer | Writes PDF objects, text and pictures. | gen/pdf_write.py (1438) | 1438 | 4717 |
| feat2 pdf run effects | Prints character spacing, run shading, double strike and external links as link annotations. | gen/pdf_write.py (290) | 290 | 1106 |
| docx reader | Unzips, inflates and parses document XML. | gen/docx_read.py (2911) | 2911 | 17051 |
| png reader | Decodes PNG files to pixel words. | gen/docx_read.py (311), gen/a12_guard.py (61) | 372 | 4755 |
| zip crc check | Zip CRC check on open: the inflated main part runs through the save CRC network and must match the central directory. | gen/a12_guard.py (18) | 18 | 104 |
| prompt bar | One bar that takes a short text for a color, a style name or a font name. | gen/imp4_prompt.py (524) | 524 | 2033 |
| extended characters | UTF-8 and code units for characters past Latin-1. | gen/imp4_prompt.py (131) | 131 | 881 |
| tier 4 features | Tracked changes, fields, equations, mail merge. | gen/t4_features.py (705) | 705 | 1927 |
| docx deflate | LZ77 with fixed Huffman compression for the zip container. | gen/t4_features.py (242) | 242 | 863 |
| docx reader tier 4 | Reads tracked marks and fields. | gen/t4_features.py (1722) | 1722 | 4788 |
| feat2 built up math | Builds, measures, paints, saves as OMML, reads and prints the newer equation forms: root with an index, n-ary with limits, accents, delimiters as tall as their line, two row matrix. | gen/t4_features.py (1788) | 1788 | 4610 |
| tier 2 | Styles, paragraph commands, lists and typed sizes. | gen/t2_features.py (391) | 391 | 1026 |
| docx reader tier 2 | Reads styles, numbering, run and paragraph properties. | gen/t2_features.py (836) | 836 | 3077 |
| tier3 | Remaining tier 3 commands and undo op 8. | gen/t3_features.py (22) | 22 | 46 |
| tables | Table scan, insert, row and column edits, shading, border hit zones and drag. | gen/t3_features.py (637) | 637 | 1785 |
| sections | Section records, breaks and page setup. | gen/t3_features.py (112) | 112 | 326 |
| zip container | Zip member table, central directory, and table XML for saving. | gen/t3_features.py (210) | 210 | 466 |
| docx reader tier 3 | Reader additions for parts walking. | gen/t3_features.py (127) | 127 | 411 |
| pdf tables | PDF page size, table rules and shading. | gen/t3_features.py (55) | 55 | 98 |
| pictures | Picture handles, resizing by resampling, PNG writing, and reading pictures from a file. | gen/t3_features.py (926) | 926 | 4362 |
| notes and balloons | Wrapped text, comment balloons and footnotes. | gen/t3_features.py (257) | 257 | 614 |
| headers and footers | Header and footer strings and their edit bar. | gen/t3_features.py (112) | 112 | 404 |
| table of contents | Builds and updates the table of contents. | gen/t3_features.py (175) | 175 | 521 |
| docx writer tier 3 | Writes section properties, tabs, markers, comments, notes, headers and footers. | gen/t3_features.py (306) | 306 | 669 |
| docx reader notes | Reads note, comment and header parts. | gen/t3_features.py (819) | 819 | 2442 |
| style create and rename | New and renamed styles, and applying character styles. | gen/imp4_style.py (177) | 177 | 687 |
| list formats | The list format menu and reading numFmt and lvlText. | gen/imp4_list2.py (151) | 151 | 543 |
| column breaks | Column breaks: typed with Ctrl+Shift+Enter, read and written as w:br of type column, laid out as a move to the second column. | gen/imp5_breaks.py (22) | 22 | 44 |
| vertical ruler drag | Top and bottom margin drags on the vertical ruler, released through the section edit with undo. | gen/imp5_vruler.py (9) | 9 | 92 |
| repeat last command | F4 repeats the last character format, alignment, paragraph style or list command. | gen/imp6_feat.py (21) | 21 | 47 |
| recent colors | Recent colors: the last eight exact text colors, drawn under Color Picker and applied again with a click. | gen/imp6_feat.py (276) | 276 | 2793 |
| p2 character style update | Update on a character style: the caret format becomes its definition and is laid over every run of the style, with undo. | gen/p2_style.py (97) | 97 | 458 |
| canvas look | Page shadow and the canvas around the page. | gen/rv_a2_canvas.py (82) | 82 | 197 |
| a4 commands | Word commands: repeat, format painter, keep rules and others. | gen/rv_a4_features.py (344) | 344 | 1272 |
| a4 keep | Keep with next and keep lines in pagination. | gen/rv_a4_features.py (55) | 55 | 143 |
| a4 borders | Paragraph borders and shading on screen and in PDF. | gen/rv_a4_features.py (387) | 387 | 1416 |
| a4 docx | Reads and writes the a4 paragraph properties. | gen/rv_a4_features.py (271) | 271 | 700 |
| a4 tabs | Tab stops. | gen/rv_a4_features.py (160) | 160 | 510 |
| a4 ruler | Ruler display and drag. | gen/rv_a4_features.py (330) | 330 | 1443 |
| a4 merge | Merged table cells. | gen/rv_a4_features.py (639) | 639 | 1414 |
| a4 pagenum | Page number formats and section start values. | gen/rv_a4_features.py (254) | 254 | 583 |
| docx reader rv_a5 | Reader fidelity (nested tables, row spans, spacing, truncation), plus spell suggestions and the saved list of added words. | gen/rv_a6_spell.py (845), gen/rv_a5_docx.py (355), gen/app.py (303) | 1503 | 13761 |
| feat1 docx reader | Reads caps, small caps, double strike, hidden text, character spacing, run shading, links with their targets, bookmarks, contextual spacing and widow control from a .docx. | gen/feat1_docx.py (249) | 249 | 648 |
| feat1 docx writer | Writes those run and paragraph properties back, opens and closes links and bookmarks around runs, and lists external link targets as relationships. | gen/feat1_docx.py (228) | 228 | 965 |
| rv a3 interaction | Editing keys, word and page motion, right click, autoscroll, context menu, and the late tier 1 features. | gen/t1_features.py (2039), gen/rv_a3_keys.py (655), gen/pointer3.py (86), gen/rv_a4_features.py (79), gen/ui.py (42) | 2901 | 25112 |
| file output command | Selects the length, data base and file name the glue saves. | gen/rv_a11_out.py (5) | 5 | 8 |
| screen check | Compares one line of the screen id plane against the line table on each blink tick and repairs by repainting. | gen/rv_a11_out.py (23) | 23 | 56 |
| compiled control | Every state rule compiled together: the gated sums that give each register its next value, and the return dispatchers. | gen/app.py (11337) | 11337 | 60200 |
