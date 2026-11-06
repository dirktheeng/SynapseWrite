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
Evidence: `test/e2e.js`, `test/t3_table.js`, `test/t3_pic.js`, `test/t3_misc.js`. Files were checked with LibreOffice (open, re-save, reopen pixel identical; PDF conversion viewed) and python-docx. Not verified in real Word.
| Feature | Status | Gap |
|---|---|---|
| Tables | Passed | Insert and delete rows and columns, column width drag, six cell shades, all with undo and redo. Save, open, and LibreOffice re-save are pixel identical. PDF draws rules, shading and text. No merged cells; one paragraph per cell (extra paragraphs in a real file are joined); up to 8 columns; a table at the very start of a real file gets an empty paragraph before it. |
| Pictures | Passed | Alpha blended on white by a shift and add network, gray alpha and RGBA. Handles on the right, bottom and corner (corner keeps aspect), resampled nearest neighbour by the network, undo and redo. Written as word/media PNG (stored deflate, CRC and Adler in the network), read back through relationships and the zip directory. PNG only; a picture is alone in its paragraph; no text wrap; not drawn in PDF. |
| Sections | Passed | Section Break button, per section columns (1 or 2), margins (three presets), orientation. Saved as sectPr and read back with any twip values. Break is undoable; changing a section's properties is not. Continuous breaks read as next page. |
| Headers and footers | Passed | Default and first page variants of each, page number field, saved as header and footer parts with fldSimple; both field forms read back. One set per document; left aligned plain text; the old automatic page number was removed; not drawn in PDF. |
| Footnotes | Passed | Marker inside the text at the caret, several per paragraph, numbered in text order, wrapped multi-line notes stacked at the page foot with space reserved, undo and redo, saved to footnotes.xml. 250 characters per note, plain text; edit by pressing Insert Footnote with the caret right after a marker; not drawn in PDF. |
| Comments | Passed | Multi-line wrapped balloon, delete with undo, saved to comments.xml and read back. One per paragraph over the whole paragraph, 199 characters, no threads; balloons of close paragraphs can overlap; not drawn in tables. |
| Table of contents | Passed | Dot leaders, right aligned live page numbers, Heading 2 indent, Update Table rebuilds the first run of entries, saved as a right tab with dot leader and read back. Saved as text with a tab, not a TOC field; no links; leaders not drawn in PDF. |
| Columns | Partial | One or two per section. Tables are not column aware. |

## Tier 4
| Feature | Status | Evidence or gap |
|---|---|---|
| .docx save | Partial | Zip, CRC32, and XML written by the network; passes a zip CRC check and opens in LibreOffice (`test/roundtrip.js`). Not verified in real Word. Lists are not saved; members are stored uncompressed. |
| .docx open | Partial | Network walks the zip central directory, inflates deflate (fixed and dynamic Huffman, LZ77), and matches XML tags. Reads text, bold, italic, underline, size, palette colors, Caladea, alignment, paragraphs. Save, open, and open after a LibreOffice re-save are pixel identical in the document area. Not tested on files written by real Word. Lists, styles, and non-ASCII text are dropped; 8 MB file limit. |
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
