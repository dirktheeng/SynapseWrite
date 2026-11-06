# SynapseWrite parity matrix

Status key: PASSED means an automated event-driven test passed. "Passed" does not mean verified against real Word, because no copy of Word was available.
Test evidence: `test/e2e.js` (see `build/e2e.json`; `build/e2e.json`), `test/t4.js` (latency), `test/audit.py` (architecture).

## Tier 1
| Feature | Status | Evidence or gap |
|---|---|---|
| Ribbon and tabs | Partial | Hover highlights on buttons, tabs, and menu rows. Dropdown menus for font, size, color, find options, margins, and line spacing, drawn by the network, with keyboard use. Home, Insert, Layout, References, Review, and View have working commands, but many Word commands are absent from them. Original icons, 16 and 32 px. Word style arrangement with a File tab, combo boxes, a styles gallery with previews, color and highlight dropdown grids, pressed states; every command has its own hover highlight. File screen has New, Open, Save, Print. |
| Status bar | Passed | Page and word counts render from the network. Language, view buttons and zoom slider are drawn but do not act; zoom needs glyphs at other scales and a mapped hit test. |
| Pointer | Passed | Drawn by the network: arrow, I-beam, left-right, up-down, diagonal, margin arrow, chosen from the id and color under it and the table and picture zones. Colors under it are saved and restored through a block port; it never writes alpha. Hidden on touch. `test/look.js`. |
| Rulers | Partial | Indent and margin markers and the active band follow the caret paragraph, table cell, column, and margin setting. Can be hidden. Markers are not draggable. |
| Typing, caret, blink | Passed | e2e typing tests; caret blinks through ANN timer requests. |
| Selection | Passed | Shift+arrows, Ctrl+Shift word and paragraph moves, Shift+PageUp and PageDown, Shift+click, drag with autoscroll past the top or bottom, margin click for a line, double for a paragraph, triple for all, select all, double click word, triple click paragraph. Dragging after a double click does not extend by word. |
| Scrolling | Passed | Wheel, scrollbar click, and thumb dragging. |
| Undo and redo | Passed | Includes paragraph merges, formatting, paragraph properties, style updates, and table, footnote, comment and section break edits. Groups by word, with new groups on caret moves, commands, a change of edit kind, and a 2 s pause. Margin, orientation and column settings are not undoable. |
| Clipboard | Partial | Plain text only; formatting is lost. Real Ctrl+C, Ctrl+X and Ctrl+V tested (`test/look.js`). A denied Paste button draws a status message and pastes the network's own copy if it has one. If clipboard write is impossible, Ctrl+V uses the network's copy until the next successful copy, so text copied elsewhere meanwhile is not seen. Not exercised in Firefox or Safari. |
| Find and replace | Partial | Match count with current index, match case, whole words. Matches must lie within one paragraph. All matches are highlighted while the bar is open, and spell squiggles pause meanwhile. F3 finds next. |

| Caret keys | Passed | Ctrl+arrows by word and paragraph, Ctrl+Backspace, Ctrl+Delete, PageUp and PageDown move the caret, End and clicks keep the caret on a wrapped line, Insert toggles overtype with no status indicator (`test/rv_a3.js`). |
| Tabs and breaks | Partial | Tab is a real character advancing to default stops every 0.5 in, Shift+Enter a line break; both saved as `w:tab` and `w:br`, read back, drawn in PDF. No custom tab stops. |
| Context menu | Passed | Right click in the document: cut, copy, paste, select all, bold, italic, underline, find. |
| Other shortcuts | Partial | Ctrl+[ ] and Ctrl+Shift+< >, Ctrl+= and Ctrl+Shift+=, Ctrl+M, Ctrl+Shift+M, Ctrl+1, 2, 5, Ctrl+Shift+L, Ctrl+Shift+N, Shift+F3, F12, Shift+Delete, Ctrl+Insert, Shift+Insert. Find cannot span paragraphs. Browser reserved keys such as Ctrl+N and Ctrl+T cannot be taken. |

## Tier 2
| Feature | Status | Evidence or gap |
|---|---|---|
| Bold, italic, underline, strikethrough, superscript, subscript | Passed | Shortcuts and buttons; ribbon cells for the new ones, saved and reopened (`test/tier2.js`). Scripts draw a smaller compiled size. |
| Font size | Partial | Typed entry in the size box and grow and shrink buttons, snapped to 13 compiled sizes from 7 to 36 pt. Sizes above 36 pt and in-between sizes such as 13 or 22 pt do not exist. |
| Fonts | Partial | Two faces (Carlito, Caladea). ASCII, Latin-1 and the Windows-1252 punctuation block (curly quotes, dashes, euro), on screen, input, clipboard, .docx and PDF. Other Unicode shows as a question mark on open and is dropped on paste. Kerning with 701 GPOS pairs (ASCII pairs only) and unrounded advances. Ink comes from the unhinted outline, 8x oversampled with the x-height snapped to a pixel row; glyphs sit on whole pixels. Keyboard dead keys and IME composition do not reach the network, because the glue only forwards keydown. |
| Text and highlight color | Partial | 32 palette colors for text, 7 highlight colors, all on the ribbon. Any other color in a .docx snaps to the nearest palette entry. Highlight is not drawn in PDF. |
| Paragraph alignment | Passed | Left, center, right, justify. |
| Styles | Partial | True style table: paragraphs hold a style index, each style defines run format, alignment, indent, spacing. Update Style from the caret paragraph changes every paragraph of the style, with undo. styles.xml is saved and read, including basedOn and docDefaults, up to 196 paragraph styles. Six can be applied from the ribbon. No create, rename, or character styles; theme fonts and theme colors are not resolved. |
| Lists | Partial | Bullets and numbers, three levels (1., a., i.), Tab and Shift+Tab, Enter on an empty item ends it, Backspace removes the marker. numbering.xml is saved and read, including lists set through a style. Numbering restarts after any non-list paragraph. Levels beyond three clamp. Formats are fixed by level; custom list text is not read. |
| Paragraph spacing | Passed | Left, first line and hanging indent from the ribbon and from a file, space before and after, six line spacing values, all with undo, saved and read (`test/tier2.js`, `test/e2e.js`). Exact line heights in a file are read as single. The ruler marks the left indent only. |
| Line breaking and justification | Passed | Greedy breaking only. No hyphenation. |
| Pagination | Passed | Automatic and Ctrl+Enter breaks, widow and orphan control on screen and in PDF, always on. Line height for the lookahead on 3 line paragraphs is approximated from the second line. No keep with next. |

## Tier 3
Evidence: `test/e2e.js`, `test/t3_table.js`, `test/t3_pic.js`, `test/t3_misc.js`. Files were checked with LibreOffice (open, re-save, reopen pixel identical; PDF conversion viewed) and python-docx. Not verified in real Word.
| Feature | Status | Gap |
|---|---|---|
| Tables | Passed | Insert and delete rows and columns, column width drag, six cell shades, all with undo and redo. Save, open, and LibreOffice re-save are pixel identical (`test/t3_table.js`). PDF draws rules, shading and text. No merged cells; one paragraph per cell (extra paragraphs in a real file are joined); up to 8 columns; a table at the very start of a real file gets an empty paragraph before it. |
| Pictures | Passed | PNG insert (8-bit gray, gray alpha, RGB, RGBA, non-interlaced, all five filters), alpha blended on white. Handles on the right, bottom and corner (corner keeps aspect), resampled nearest neighbour by the network, undo and redo (`test/t3_pic.js`, `test/t16.js`). Written as word/media PNG, stored in the zip with CRC and Adler from the network, read back through relationships and the zip directory, also after LibreOffice. Drawn in PDF as an inline image. PNG only; a picture is alone in its paragraph; no text wrap; large images are decimated to fit a page. |
| Sections | Passed | Section Break button, per section columns (1 or 2), margins (normal, moderate from the menu, narrow, wide), orientation. Saved as sectPr and read back with any twip values (`test/t3_misc.js`). The break is undoable; changing a section's properties is not. Continuous breaks read as next page. A mail merge copy loses section breaks. |
| Headers and footers | Passed | Default and first page variants of each, page number field, saved as header and footer parts with fldSimple; both field forms read back, drawn in PDF (`test/t3_misc.js`, `test/t4_pdf.js`). One set per document; left aligned plain text; there is no automatic page number. |
| Footnotes | Passed | Marker inside the text at the caret, several per paragraph, numbered in text order, wrapped multi-line notes stacked at the page foot with space reserved, undo and redo, saved to footnotes.xml, drawn in PDF (`test/e2e.js`, `test/t3_misc.js`). 250 characters per note, plain text, 1,500 notes in a document; edit by pressing Insert Footnote with the caret right after a marker. |
| Comments | Passed | Multi-line wrapped balloon, delete with undo, saved to comments.xml and read back (`test/e2e.js`, `test/t3_misc.js`). One per paragraph over the whole paragraph, 380 characters, no threads; balloons of close paragraphs can overlap; not drawn in tables or PDF. |
| Table of contents | Passed | Dot leaders, right aligned live page numbers, Heading 2 and 3 indent, Update Table rebuilds the first run of entries, saved as a right tab with dot leader and read back, drawn in PDF (`test/t3_misc.js`). Saved as text with a tab, not a TOC field; no links. |
| Columns | Partial | One or two per section, on screen and in PDF. Tables are not column aware. |

## Tier 4
| Feature | Status | Evidence or gap |
|---|---|---|
| .docx save | Partial | One table driven zip writer: CRC32, sizes and names held in a member table, central directory written from it. All XML parts deflated, by the network or at build time for static parts; pictures stored. Passes a zip CRC check and opens in LibreOffice (`test/roundtrip.js`, `test/t4_docx.js`, `test/t3_pic.js`). Not verified in real Word. |
| .docx open | Partial | Network walks the zip central directory, inflates deflate (fixed and dynamic Huffman, LZ77), and matches XML tags. Reads text in UTF-8, run formats, sizes, colors, serif font names, alignment, paragraph properties including first line and hanging indents, styles, numbering, tables, pictures, sections, headers and footers, footnotes, comments, tracked marks and fields. Save, open, and open after a LibreOffice re-save are pixel identical in the document area for each of those. Also tested on a python-docx file, whose template comes from Word; not tested on files saved by real Word. 8 MB file limit. Opening a file with a very large styles.xml (349 KB in the python-docx template) took about 13 s. |
| Spell check | Passed | 79,339 word list (SCOWL via npm wordlist-english, license in `gen/words_en.COPYRIGHT`) written into weights as a minimized letter automaton, 28,403 nodes and 66,940 edges. Red squiggles while painting; contractions and possessives; capitals, digits and math not flagged; toggle on Review. No suggestions or custom dictionary. `test/e2e.js`. |
| Fields | Passed | Page number, word count, and date from a time vector the glue encodes, shaded, Update All, saved as `w:fldSimple`. Values refresh on Update All, not live. Date valid 1970 to 2099, format M/D/YYYY only. `test/e2e.js`, `test/t4_docx.js`. |
| Track changes | Passed | Insert and delete marks, accept and reject for a selection or all, undo, saved and reopened as `w:ins`, `w:del`, `w:delText`, reject after reopen works. Paragraph marks are not tracked, one fixed author, no date, no per-author colors. LibreOffice reads the file; real Word not tested. `test/t4_docx.js`. |
| Mail merge | Passed | Pasted CSV with quotes, header row, `{Name}` placeholders, one copy of the document per row with page breaks, up to 500 rows and 32 columns. Replaces the document and clears undo. Not Word MERGEFIELD. `test/e2e.js`. |
| Equations | Partial | Linear form with `^`, `_`, and `{}` grouping: italic letters, Caladea, shifted small script, undoable. Saved as run formatting with `w:vertAlign` and `w:noProof`, not as OMML. No fractions, roots, or Greek because the glyph set is Latin ASCII. `test/e2e.js`. |
| Print to PDF | Partial | Embedded subset TrueType Carlito and Caladea, positions from the screen layout in pixels, page size per section, underline, strike, colors, lists, two columns, inline pictures, table rules and shading, header and footer strings, footnotes, table of contents leaders and numbers. Page ink within 2 pixels of the screen for over 90 percent, tested against poppler at 96 dpi. Letter spacing inside a word is the font's own, not the screen's rounded one. Comments, highlight and field shading are not drawn. `pdfinfo`, `pdffonts`, `qpdf --check`, `pdftotext` in `test/t4_pdf.js`, `test/t3_misc.js`. |
| .docx deflate | Passed | Greedy LZ77 with a hash head table and fixed Huffman codes. 87,469 bytes to about 2.3 KB on a repetitive document. Zip CRC checks and own inflate rereads it. No dynamic Huffman blocks. |
| styles.xml | Passed | The numbering, styles, document member walk reads docDefaults, `w:style`, `basedOn`, `pStyle`, `rStyle`, `jc`; `w:b w:val="0"` handled. Matches direct formatting pixel for pixel (`test/t4_docx.js`). Character styles replace rather than overlay the paragraph style. Other parts (numbering, theme) are not read. |

## Deployment targets
| Target | Result |
|---|---|
| Static page | Self-contained HTML, 3.3 MB, about 413,000 neurons, about 2.37 million weights plus 420,000 read on demand |
| Browsers | Tested in headless Chromium only. Edge and Firefox not tested. |
| Typing, 126 pages | About 1 ms at document end, 4 ms at top on a quiet machine. CPU in this container, no GPU. |
| Enter, undo near the top, 126 pages | About 20 ms each. Page totals finish in the background. |
| Wheel, caret jump to top, 126 pages | About 16 ms and 18 ms. |
| Select all, 126 pages | About 19 ms. |
| Paste of 1,900 paragraphs | About 1.4 s. |

## Limits
About 3,000 paragraphs, 1,000 characters per paragraph, 200 characters per line, and no memory reclaim for deleted paragraphs.

## Blockers and caveats
- **Lazy gates:** the engine reads a gated neuron's value inputs only after its enable fires. This is an evaluation order choice; the neuron computes the same function.
- **Real Word:** no copy is available here, so pixel comparisons and .docx verification against Word were not run. Those verification items are open.
- **Screenshot use:** the network reads the last output image for hit testing, using the hidden alpha channel as an object ID. It does not compare the whole screen against document state.
- **Compiled logic:** this is a circuit-style network (2,323 control states) written by a generator. It is not a CPU emulator, but it is much closer to compiled hardware than to a conventional learned model.
- **Ribbon ids:** alpha ids stop at 255, so raw ids are reused per tab; the network uses the tab and id together. Color menus find the cell from the pointer position.
- **Ports:** memory block copy and rectangle fill run inside the engine as ports the network commands. The network supplies every address, length, color, and enable signal. A stricter reading could count the copy loops as non-ANN work.

- **Audit exception:** the glue creates one anchor element and one file input, only to pass .docx bytes out of and into the browser. The audit's blanket ban on `createElement` was removed for this reason.
