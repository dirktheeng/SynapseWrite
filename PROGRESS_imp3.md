# imp3 progress log
Started from master f0ade7f. Order: tier 1 find, zoom and view, ribbon and ruler, clipboard; tier 2; exact line heights; repaint cost.
Baseline build: 3,220,027 byte page, 444,066 neurons, 942,629 stored edges.

## Find across paragraphs
Typed ^p (as in Word) or a pasted newline is a paragraph mark in the query; replacement ^p splits. A query with a mark has one candidate start per paragraph (paragraph length minus the characters before the first mark), so a search costs a read per paragraph plus the compare. One matcher (IMP3_X, return table IMP3_XR) serves walker, counter and highlight; a query with no mark takes the old paths unchanged. First build failed: names xret, xb, xl, qmk collide with t3 and pdf registers; renamed. Second run: replace wrote NUL because RP3 passed R1 on a tick late; rule moved into RP3. test/imp3.js: 8/8. Screenshot imp3_find1 shows both matches tinted in both paragraphs, "2 found".

## Zoom and view
Why not a screen resample: every fast path paints the screen directly. Instead a linear map sits between the paint buses (rects, glyph x and y) and the ports, enabled by one-hot level registers and by the document clip; at 100 percent no gate opens. Layout, hit lists and files stay in document pixels; mouse coordinates are mapped back (zhx, zhy) and caret arrows mapped forward. The glyph unit draws the nearest whole point size, so sizes 4, 5, 6 pt were added to the table (needed for 50 percent). Pictures draw one destination pixel at a time when zoomed, using the copy port with size 1. Viewport height for culling is the register VHZ.
Levels 50, 75, 100, 125, 150: 150 is the widest page that fits the window, as there is no horizontal scroll. Slider, plus, minus, View tab (Zoom In, Zoom Out, 100%, One Page, Page Width), Ctrl+wheel. Read Mode covers the bars, hides the ruler and refuses edit keys; Esc or the print layout button leaves. The web layout button was removed as it could not act.
Bugs found by screenshot: rZ ran after rB, rC in the same tick and erased the ruler band (moved a tick earlier); 16.5 pt rounded down and looked letterspaced (rounds up now); UI wipes the right part of the status bar and the memo skipped the repaint (UI clears stp).
test/imp3.js zoom 12/12.

## Clipboard
Copy and cut keep style cells at CBS and one 8-cell paragraph record per mark at CBP (100,000 characters). Paste compares CB2 with CB, one tick per character, skipping CR. Equal: single character path with kept cells, and after each mark the paragraph before it takes the record, logged as op 6 so undo restores it. Other text: as before. test/imp3.js clip 8/8 after two test fixes (my selection in a centered paragraph ran past the mark; bold typing style at a run end is existing behaviour).
