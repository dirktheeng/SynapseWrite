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
| .docx save | Partial | Zip, CRC32, and XML written by the network; passes a zip CRC check and opens in LibreOffice (`test/roundtrip.js`). Not verified in real Word. Tables flatten to paragraphs; lists and headers are not saved; members are deflated. |
| .docx open | Partial | Network walks the zip central directory, inflates deflate (fixed and dynamic Huffman, LZ77), and matches XML tags. Reads text, bold, italic, underline, size, palette colors, Caladea, alignment, paragraphs, styles.xml, tracked marks, fields. Save, open, and open after a LibreOffice re-save are pixel identical in the document area. Not tested on files written by real Word. Tables flatten; images, lists, and non-ASCII text are dropped; 400 KB file limit. |
| Spell check | Passed | 79,339 word list (SCOWL via npm wordlist-english, license in `gen/words_en.COPYRIGHT`) written into weights as a minimized letter automaton, 28,403 nodes and 66,940 edges. Red squiggles while painting; contractions and possessives; capitals, digits and math not flagged; toggle on Review. No suggestions or custom dictionary. `test/e2e.js`. |
| Fields | Passed | Page number, word count, and date from a time vector the glue encodes, shaded, Update All, saved as `w:fldSimple`. Values refresh on Update All, not live. Date valid 1970 to 2099, format M/D/YYYY only. `test/e2e.js`, `test/t4_docx.js`. |
| Track changes | Passed | Insert and delete marks, accept and reject for a selection or all, undo, saved and reopened as `w:ins`, `w:del`, `w:delText`, reject after reopen works. Paragraph marks are not tracked, one fixed author, no date, no per-author colors. LibreOffice reads the file; real Word not tested. `test/t4_docx.js`. |
| Mail merge | Passed | Pasted CSV with quotes, header row, `{Name}` placeholders, one copy of the document per row with page breaks, up to 500 rows and 32 columns. Replaces the document and clears undo. Not Word MERGEFIELD. `test/e2e.js`. |
| Equations | Partial | Linear form with `^`, `_`, and `{}` grouping: italic letters, Caladea, shifted small script, undoable. Saved as run formatting with `w:vertAlign` and `w:noProof`, not as OMML. No fractions, roots, or Greek because the glyph set is Latin ASCII. `test/e2e.js`. |
| Print to PDF | Partial | Embedded subset TrueType Carlito and Caladea, positions from the screen layout in pixels, underline, strike, colors, lists, two columns, inline pictures, header and footer number. Page ink within 2 pixels of the screen for over 90 percent, tested against poppler at 96 dpi. Letter spacing inside a word is the font's own, not the screen's rounded one. Table borders, footnotes, and comments are not drawn. `pdfinfo`, `pdffonts`, `qpdf --check`, `pdftotext` in `test/t4_pdf.js`. |
| .docx deflate | Passed | Greedy LZ77 with a hash head table and fixed Huffman codes. 87,469 bytes to about 2.3 KB on a repetitive document. Zip CRC checks and own inflate rereads it. No dynamic Huffman blocks. |
| styles.xml | Passed | Second zip pass reads docDefaults, `w:style`, `basedOn`, `pStyle`, `rStyle`, `jc`; `w:b w:val="0"` handled. Matches direct formatting pixel for pixel (`test/t4_docx.js`). Character styles replace rather than overlay the paragraph style. Other parts (numbering, theme) are not read. |

## Deployment targets
| Target | Result |
|---|---|
| Static page | Self-contained HTML, 4.6 MB, about 308,000 neurons, about 2.1 million weights |
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
