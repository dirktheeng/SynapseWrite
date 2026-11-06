# Tier 3 progress log (branch tier3)

Baseline: e2e 43/43, roundtrip all true, build 15 s, 142k neurons.

## Plan
Fields added to a paragraph slot at META=3673: CW, CX, CSH, SECN, TOCF, TSRC, TPG, SSI.
A generic undo op 6 swaps one slot cell with the log entry, so every metadata write is undoable and redoable.
New ribbon commands share button id 54 and are told apart by comparing tab, x and y in the network (gen/t3_btn.py).

## Log
1. Tables first. Cell width, offset and shade became slot cells; layout reads them instead of the equal width decode. Row and column commands are a structural pass (SPLIT or kill cell) plus a field pass over every cell, all through the undo log. Hang found: registers with no assignment do not hold a value, so the section registers needed the load states at once.
2. Name collisions: `rm`, `off`, `hlen` are reassigned later in app.py and docx_read.py. Fixed by renaming the port and taking `off_`, `hlen_` aliases before the readers run. `pat` has an 8 cell window, so long attribute names were shortened.
3. Zip writer replaced by a member table: header with holes, CRC and size patch, central directory written from the table. Inflate got movable input and output bases so a member can be inflated while the document scan is paused.
4. Pictures: blend in PG_N3, handles with hit zones compared in the network before the pixel hit test (no alpha id needed), resampling into fresh image memory, native copy kept for quality. First test used wrong handle coordinates; handles overhung the image and left marks after a fast repaint, so they now sit inside it.
5. Footnotes moved to a marker character 1000+id with a text store. Each line stores its note height, so page breaks reserve room. Notes are drawn when a page ends or the walk ends, from an order table filled during the walk.
6. LibreOffice maps footnotes by position in footnotes.xml, not by id. Save now numbers references 1,2,3 in text order and writes only referenced notes.
7. Page breaks were never saved; added pageBreakBefore and reading of w:br page. TOC number was read a tick late; moved into TX3. A later section's empty first header overwrote the first one on read; a loaded string now stays.
8. Latency against the 44e1d6b baseline (test/t4.js, same machine): typing 4.2 ms vs 4.1, wheel 40 vs 31, jump to top 44 vs 39, enter 49 vs 72 (noisy), paste 1900 paragraphs 19.9 s vs 13.9 s. Network 193k neurons vs 142k, page 3.5 MB.
