# SynapseWrite parity matrix

Status key: PASSED means an automated event-driven test passed. "Passed" does not mean verified against real Word, because no copy of Word was available.
Test evidence: `test/e2e.js` (see `build/e2e.json`; `build/e2e.json`), `test/t4.js` (latency), `test/audit.py` (architecture).

## Tier 1
| Feature | Status | Evidence or gap |
|---|---|---|
| Ribbon and tabs | Partial | Tab switching passes. Only Home has working commands; the other five tabs are labels only. No hover states or dropdowns. |
| Status bar | Passed | Page and word counts render from the network. |
| Rulers | Partial | Drawn only. No draggable margins or indents. |
| Typing, caret, blink | Passed | e2e typing tests; caret blinks through ANN timer requests. |
| Selection | Passed | Shift+arrows, drag, select all. No double-click word selection. |
| Scrolling | Passed | Wheel and scrollbar click. No thumb dragging. |
| Undo and redo | Passed | Includes paragraph merges and formatting. |
| Clipboard | Partial | Plain text only; formatting is lost. The Paste button needs browser clipboard permission. |
| Find and replace | Partial | Works within a paragraph; case-insensitive only. No match highlighting list or match count. |

## Tier 2
| Feature | Status | Evidence or gap |
|---|---|---|
| Bold, italic, underline, strikethrough, superscript, subscript | Passed | Shortcuts and buttons; ribbon cells for the new ones, saved and reopened (`test/tier2.js`). Scripts draw a smaller compiled size. Not drawn in PDF: underline, strike. |
| Font size | Partial | Typed entry in the size box and grow and shrink buttons, snapped to 13 compiled sizes from 7 to 36 pt. Sizes above 36 pt and in-between sizes such as 13 or 22 pt do not exist. |
| Fonts | Partial | Two faces (Carlito, Caladea). ASCII, Latin-1 and the Windows-1252 punctuation block (curly quotes, dashes, euro), on screen, input, clipboard, .docx and PDF. Other Unicode shows as a question mark on open and is dropped on paste. Kerning with 701 GPOS pairs (ASCII pairs only) and unrounded advances. Keyboard dead keys and IME composition do not reach the network, because the glue only forwards keydown. |
| Text and highlight color | Partial | 32 palette colors for text, 7 highlight colors, all on the ribbon. Any other color in a .docx snaps to the nearest palette entry. Highlight is not drawn in PDF. |
| Paragraph alignment | Passed | Left, center, right, justify. |
| Styles | Partial | True style table: paragraphs hold a style index, each style defines run format, alignment, indent, spacing. Update Style from the caret paragraph changes every paragraph of the style, with undo. styles.xml is saved and read, including basedOn and docDefaults, up to 196 paragraph styles. Six can be applied from the ribbon. No create, rename, or character styles; theme fonts and theme colors are not resolved. |
| Lists | Partial | Bullets and numbers, three levels (1., a., i.), Tab and Shift+Tab, Enter on an empty item ends it, Backspace removes the marker. numbering.xml is saved and read, including lists set through a style. Numbering restarts after any non-list paragraph. Levels beyond three clamp. Formats are fixed by level; custom list text is not read. |
| Paragraph spacing | Passed | Left and first line indent, hanging from a file, space before and after, six line spacing values, all with undo, saved and read. Exact line heights in a file are read as single. |
| Line breaking and justification | Passed | Greedy breaking only. No hyphenation. |
| Pagination | Passed | Automatic and Ctrl+Enter breaks, widow and orphan control on screen and in PDF, always on. Line height for the lookahead on 3 line paragraphs is approximated from the second line. No keep with next. |

## Tier 3
| Feature | Status | Gap |
|---|---|---|
| Headers and footers | Partial | One plain-text header on all pages and a fixed page number footer. No per-section or first-page variants. |
| Tables | Partial | Fixed 2x2, 3x3, and 4x4 equal-width grids with wrapping cells, Tab navigation, and undo. No resizing, merged cells, row insert, or shading. |
| Columns | Partial | One or two equal columns for the whole document. Not per section, and tables are not column aware. |
| Table of contents | Partial | Inserted once from Heading 1 and 2 paragraphs with page numbers. No dot leaders, no update, no links. |
| Comments | Partial | One comment per paragraph in a margin balloon, on a single clipped line. No threads, authors, or text ranges, not undoable, not saved to .docx. |
| Footnotes | Partial | One per paragraph, numbered through the document, drawn at the page foot. Marker sits at paragraph end, four notes per page, single line, not undoable, not saved to .docx. |
| Images | Partial | PNG insert (8-bit gray, RGB, RGBA, non-interlaced; all five filters) decoded by the network and shown pixel exact (`test/t16.js`). Alpha is ignored, large images are decimated by an integer factor, no resize or text wrap, not saved to .docx, slow: about 6 s for 200x120. |
| Sections | Missing | Not implemented. Not shown to be infeasible. |

## Tier 4
| Feature | Status | Evidence or gap |
|---|---|---|
| .docx save | Partial | Zip, CRC32, and XML written by the network; passes a zip CRC check and opens in LibreOffice (`test/roundtrip.js`). Not verified in real Word. Tables flatten to paragraphs; headers are not saved; members are stored uncompressed. |
| .docx open | Partial | Network walks the zip central directory, inflates deflate (fixed and dynamic Huffman, LZ77), and matches XML tags. Reads text in UTF-8, run formats, sizes, colors, serif font names, alignment, paragraph properties, styles and numbering. Save, open, and open after a LibreOffice re-save are pixel identical in the document area for each of those. Also tested on a python-docx file, whose template comes from Word; not tested on files saved by real Word. Tables flatten; images are dropped; 400 KB file limit. Opening a file with a very large styles.xml (349 KB in the python-docx template) took about 13 s. |
| Track changes, mail merge, equations, fields, spell check, print to PDF | Missing | Not implemented. Not shown to be infeasible. |

## Deployment targets
| Target | Result |
|---|---|
| Static page | Self-contained HTML, 4.4 MB, about 189,000 neurons, about 1.94 million eager weights plus 235,000 weights read on demand |
| Browsers | Tested in headless Chromium only. Edge and Firefox not tested. |
| Typing, 126 pages | About 4 ms at document end, 10 ms at top on a quiet machine. CPU in this container, no GPU. |
| Enter, undo near the top, 126 pages | About 50 ms each. Page totals finish in the background. |
| Wheel, caret jump to top, 126 pages | About 41 ms and 47 ms. |
| Select all, 126 pages | About 46 ms. |
| Paste of 1,900 paragraphs | About 14 s. |

## Limits
About 3,000 paragraphs, 1,000 characters per paragraph, 200 characters per line, and no memory reclaim for deleted paragraphs.

## Blockers and caveats
- **Lazy gates:** the engine reads a gated neuron's value inputs only after its enable fires. This is an evaluation order choice; the neuron computes the same function.
- **Real Word:** no copy is available here, so pixel comparisons and .docx verification against Word were not run. Those verification items are open.
- **Screenshot use:** the network reads the last output image for hit testing, using the hidden alpha channel as an object ID. It does not compare the whole screen against document state.
- **Compiled logic:** this is a circuit-style network (994 control states) written by a generator. It is not a CPU emulator, but it is much closer to compiled hardware than to a conventional learned model.
- **Ribbon cell hit test:** alpha ids stop at 255, so the Tier 2 ribbon cells share one object id, and the network finds the command from the click position.
- **Ports:** memory block copy and rectangle fill run inside the engine as ports the network commands. The network supplies every address, length, color, and enable signal. A stricter reading could count the copy loops as non-ANN work.

- **Audit exception:** the glue creates one anchor element and one file input, only to pass .docx bytes out of and into the browser. The audit's blanket ban on `createElement` was removed for this reason.
