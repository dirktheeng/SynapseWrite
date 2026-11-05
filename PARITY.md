# SynapseWrite parity matrix

Status key: PASSED means an automated event-driven test passed. "Passed" does not mean verified against real Word, because no copy of Word was available.
Test evidence: `test/e2e.js` (see `build/e2e.json`; `build/e2e.json`), `test/t4.js` (latency), `test/audit.py` (architecture).

## Tier 1
| Feature | Status | Evidence or gap |
|---|---|---|
| Ribbon and tabs | Partial | Hover highlights on buttons, tabs, and menu rows. Dropdown menus for font, size, color, find options, margins, and line spacing, drawn by the network, with keyboard use. Home, Insert, Layout, References, Review, and View have working commands, but many Word commands are absent from them. Pixel art icons are original. |
| Status bar | Passed | Page and word counts render from the network. |
| Rulers | Partial | Indent and margin markers and the active band follow the caret paragraph, table cell, column, and margin setting. Can be hidden. Markers are not draggable. |
| Typing, caret, blink | Passed | e2e typing tests; caret blinks through ANN timer requests. |
| Selection | Passed | Shift+arrows, drag, select all, double click word, triple click paragraph. Dragging after a double click does not extend by word. |
| Scrolling | Passed | Wheel, scrollbar click, and thumb dragging. |
| Undo and redo | Passed | Includes paragraph merges, formatting, and paragraph properties. Groups by word, with new groups on caret moves, commands, a change of edit kind, and a 2 s pause. Margin and column settings are not undoable. |
| Clipboard | Partial | Plain text only; formatting is lost. The Paste button needs browser clipboard permission. |
| Find and replace | Partial | Match count with current index, match case, whole words. Matches must lie within one paragraph. Other matches are not highlighted. |

## Tier 2
| Feature | Status | Evidence or gap |
|---|---|---|
| Bold, italic, underline | Passed | Shortcuts and buttons. |
| Font size | Partial | 11 sizes through grow and shrink buttons; no typed size. |
| Fonts | Partial | Two faces (Carlito, Caladea), Latin ASCII only. No Unicode. |
| Text color | Partial | 8 palette colors in the network, 4 on the ribbon. No highlight color command. |
| Paragraph alignment | Passed | Left, center, right, justify. |
| Styles | Partial | Normal, Title, Heading 1 and 2 as direct formatting; no style definitions or editing. |
| Lists | Partial | Bullets and numbering, one level only. |
| Line breaking and justification | Passed | Greedy breaking only. No hyphenation or kerning. |
| Pagination | Passed | Automatic and Ctrl+Enter breaks. No widow control. |

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
| .docx save | Partial | Zip, CRC32, and XML written by the network; passes a zip CRC check and opens in LibreOffice (`test/roundtrip.js`). Not verified in real Word. Tables flatten to paragraphs; lists and headers are not saved; members are stored uncompressed. |
| .docx open | Partial | Network walks the zip central directory, inflates deflate (fixed and dynamic Huffman, LZ77), and matches XML tags. Reads text, bold, italic, underline, size, palette colors, Caladea, alignment, paragraphs. Save, open, and open after a LibreOffice re-save are pixel identical in the document area. Not tested on files written by real Word. Tables flatten; images, lists, styles, and non-ASCII text are dropped; 400 KB file limit. |
| Track changes, mail merge, equations, fields, spell check, print to PDF | Missing | Not implemented. Not shown to be infeasible. |

## Deployment targets
| Target | Result |
|---|---|
| Static page | Self-contained HTML, 2.7 MB, about 134,000 neurons, about 1.5 million weights |
| Browsers | Tested in headless Chromium only. Edge and Firefox not tested. |
| Typing, 126 pages | 4 ms at document end, 10 ms at top. CPU in this container, no GPU. |
| Enter, undo near the top, 126 pages | 39 ms each. Page totals finish in the background. |
| Wheel, caret jump to top, 126 pages | 30 ms and 37 ms. |
| Select all, 126 pages | 93 ms in the latest run. |
| Paste of 1,900 paragraphs | About 14 s. |

## Limits
About 3,000 paragraphs, 1,000 characters per paragraph, 200 characters per line, and no memory reclaim for deleted paragraphs.

## Blockers and caveats
- **Lazy gates:** the engine reads a gated neuron's value inputs only after its enable fires. This is an evaluation order choice; the neuron computes the same function.
- **Real Word:** no copy is available here, so pixel comparisons and .docx verification against Word were not run. Those verification items are open.
- **Screenshot use:** the network reads the last output image for hit testing, using the hidden alpha channel as an object ID. It does not compare the whole screen against document state.
- **Compiled logic:** this is a circuit-style network (287 control states) written by a generator. It is not a CPU emulator, but it is much closer to compiled hardware than to a conventional learned model.
- **Ports:** memory block copy and rectangle fill run inside the engine as ports the network commands. The network supplies every address, length, color, and enable signal. A stricter reading could count the copy loops as non-ANN work.

- **Audit exception:** the glue creates one anchor element and one file input, only to pass .docx bytes out of and into the browser. The audit's blanket ban on `createElement` was removed for this reason.
