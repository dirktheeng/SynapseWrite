# rv_a5 progress: .docx fidelity
## Baseline corpus run (annword head, 19 files from test/a5_corpus.py)
Open costs about 1.0 M ticks and 10 M edges on every python-docx file, nearly all of it scanning styles.xml (349 KB).
Findings by viewing against the LibreOffice PDF, and by test/a5_validate.py and test/a5_lost.py on the saved file:
- a02: merged or short rows produce a saved document.xml that is NOT well formed (</w:tbl> before </w:tr>). Word would refuse it.
- a02: paragraphs in one cell joined with no space. Table styles ignored, so grid tables inherit 10 pt after and are twice too tall.
- a05: file with a large PNG does not finish in 240 s. A paragraph with text and a picture loses the text.
- a06: endnotes dropped with their references. Multi paragraph notes joined.
- a07: second comment on a paragraph replaces the first.
- a10: rPrChange and pPrChange old values applied as if current; moveFrom and moveTo read as plain text.
- a12: <w:br/> dropped (words run together). A dot leader tab in a non-TOC paragraph drops all text after it. Page break inside a run moved the whole paragraph.
- a13: nested tables scramble the outer table.
- a14: theme fonts ignored (python-docx body is Cambria, shown sans). sz of 1 or 3 digits misread (72 pt drawn tiny, 4.5 pt drawn huge). <w:color> with val not first makes text invisible. Paragraph or run shd paints a band past the page. Numeric character references shown literally.
- a15: mc:Fallback text duplicated, math text dropped.
- Every open leaves caret and view at the end of the document.
- Saved packages have no word/settings.xml.
## Second pass
Run results on the rebuilt network: every saved file checked so far passes the ISO 29500 schemas. Viewed against LibreOffice: tables tight, serif body, nested tables flattened into the outer cell, 72 pt large.
a23 (corrupt deflate) was a real hang: zero bits past the input decode forever. Inflate now stops at the end of the file or the end of its buffer and scans what it has.
a16 profile: 44 percent of work was the ribbon display list reached through the shared OR return, once per character read. Plain text now writes directly in TX3, one tick per byte.
Machine is out of memory at times, so Chromium tabs crash ("Target crashed"); those runs are not results. test/a5_node.js opens files with no browser for tick counts.
