# PROGRESS p3

Branch p3 in /root/p3, from main 76ede1a. Area: .docx reader and writer, zip and deflate, equations, PDF. Goal: close the Tier 4 rows PARITY.md marks Partial.

## Baseline (76ede1a, measured here)
- ./make.sh: page build/index.html 2,953,717 bytes.
- test/a5_docx.js a01 open: 6,784,308 edges (limit 7 M per the task).
- test/flops.js with build/engine_count.wasm: /tmp/claude-0/p3/flops_base.json. Background layout 556,832,631 FLOPs, type at end 718,971, select all 6,405,696, wheel 7,304,280, bold 7,311,745 (all 15 events kept in the file).

## Reading the rows
- .docx open: PARITY lists caps, small caps, double strike, hidden, spacing, shading, widow, contextual spacing, links and bookmarks as lost, but feat1 already reads and writes them (test/feat1.js). Still lost: emboss, imprint, outline, shadow, character scale (w:w), language, outline level; secondary parts are not CRC checked.
- Print to PDF: missing internal links and bookmarks as destinations and outline items.
- Equations: matrix columns not aligned, two rows only, no nesting except between delimiters.
- .docx save: lists no gap besides real Word.

## Step 1: PDF destinations (gen/p3_pdf.py, group 'p3 pdf destinations')
Design: the catalog gets /Dests, a reserved object right after the outline root (DROOT=OROOT+1, so the first page moves one number up). A printed chunk whose style entry carries a bookmark id writes, for the first chunk of that bookmark in this export, the page object and line top into a table at 1196000 (entry: export serial, object, top; the serial is bumped at PDF start so no clearing pass is needed). Unless the name starts with _ (Word's hidden bookmarks), the same chunk adds an outline record at level 1, in document order with the heading records of rv_a6; its title is the bookmark name (rv_a6's title loop now stops at a zero for those records). Links of kind 2 (w:anchor) now get boxes like external ones and are written as /Dest/name; names are PDF name objects with #hh for bytes outside letters, digits, _ - and '.'.
- Link field decode in feat2_pdf.py now takes the low 8 bits for the link id (F1N is 255) and 24 bits in all, ready for the bits step 2 adds.
- First build ok, page 2,955,441 bytes (+1,724).
- test/p3.js pdf first run 7/10: the three failures were the test's (pypdf names keep a leading slash). Fixed in the test, then 10/10: pypdf and pdfinfo -dests both see sec1, _Toc99 and Odd_name.2 on their pages; the destination top is the bookmarked line within 4 pt of pdftotext's box; outline has sec1 and Odd_name.2 but not _Toc99; internal link boxes cover their words; the external link is still a URI action; qpdf clean.
