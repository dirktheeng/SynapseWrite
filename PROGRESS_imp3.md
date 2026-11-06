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

## Exact line heights
PLSP 4096+twips is exact, 8192+twips at least; rule read before or after w:line. Layout adds the difference to the line's extra; at least floors at the single height, not the 1.08 height (first run of the 6 pt case gave 20 px, wanted 18). Saved with its lineRule, reopens the same. test/imp3.js line 12/12.

## Repaint cost
Traced jump to top per state: C1 is 94 percent, 960 edges per glyph; the group split said 1.52 M of 1.99 M is the glyph unit: about 21 rows a glyph at 20 edges a row, plus 9 edges per ink cell in the row plane, though every pixel was already computed once.
Rewrite: the first black on white draw of a glyph up to 32 by 32 records the row plane's output to a ring (RECB 68 M to 75 M), and its store header takes the record's offset and generation. Later draws are one read and one patch, two ticks in the unit and no plane. No change to the generator or the store. First build no hit: fast latched one tick after the tag check; a wire fixed it. Engine page table grew from 1024 to 1152 pages. A test shows both paths give identical pixels.
Trace after: jump 1,986,258 to 788,351 edges, 2,386 ticks same paint state count; enter 2.06 M to 793,535; undo 2.18 M to 846,077; type at top 228,657 to 108,825; down 196,783 to 76,951.
Zoom gates: zdoc was waking on clip0 every glyph; it now reads clip0 only when a level is on.

## Full run 1 at 09a95fc
e2e, tier2, t3_table, t3_pic, t3_misc, t4_docx, t4_pdf, roundtrip, touch, a4, rv_a3, fonts, a5_docx, a7_type, imp_far, imp_misc, imp2, rv_a1, t4 exit 0. look 23/31, imp3 stopped on an unbuilt id (All Styles written after the build), audit 64/67 (new groups without a purpose, one ternary in the wheel listener).
look causes, in order found:
1. The right part of the status bar: a hover display list wipes it and halts with no status paint. The static rect now stops short of those cells and the zoom painter owns them.
2. Records one row low: rrow took +128 on the last row and kept it past the clear. Now counts bwr-blast, as bpy does.
3. A stray two pixels under the + of A+. Wrong guesses first (records, small sizes in sz_near, header cells); bisect pointed at the record commit, disabling records did not cure it. Watching the cell showed a pointer draw writing into the store: the tag table (500,000 keys) was too small once NSZ went from 66 to 69, as key = face*NSZ*256 + size*256 + code, so the pointer's face landed in the store. The tag table is now 600,000 cells, GSTORE starts at 61.6 M, and the build asserts the keys fit.
sz_near still leaves 4, 5, 6 pt out, so those sizes exist only for drawing at small zoom. Header zero cells now come from the resting record plane, as two plain zero wires could be merged by the optimizer.
All Styles menu: rows written from the style table, ten at a time, More styles moves on.
After: look 31/31, imp3 49/49, audit 67/67.
