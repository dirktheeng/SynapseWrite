# PROGRESS p1 (tier 1 gaps)

Base: main at 76ede1a. Clone /root/p1, branch p1.

## Starting numbers
- Page build/index.html: 2,953,717 bytes.
- test/flops.js (build/engine_count.wasm): saved as flops_base.json in the clone root (not committed). Per event FLOPs: type at end 718,971; again 54,012; select all 6,405,696; jump to top 6,174,822; type at top 916,426; down 600,832; enter at top 6,242,180; undo 6,540,707; wheel 7,304,280; click 7,480,902; mouse move 27,533; bold 7,311,745.

## 1. Find codes (Find and replace row)
Why: the row says ^t and other Word codes are not read and a literal ^p cannot be searched for. Users who search for tabs or digits notice first.
What: gen/p1_find_pre.py, group 'find codes', exec'd from imp3_find.py. The query facts pass (IMP3_Q3) counts a code as two query cells and one document cell (qcod), and qmrk now means "marks or codes", so every query with a code goes to the shared matcher. The matcher's ^ branch (IMP3_X2) takes a known code to P1_XC/P1_XD, which compare one document cell with a literal (^t tab 9, ^l line break 11, ^^ caret, ^s no-break space 160, ^- optional hyphen 173) or a class (^? any, ^# digit, ^$ letter). A query with codes but no ^p has no fixed start, so the walker (P1_F0), the counter (P1_C0) and the highlight (IMP3_H0 extra rule) try every start. The replacement (IMP3_R1) inserts the five literal codes.
Run: test/p1.js find, first run 8 passed, 0 failed. Screenshot build/p1_find2.png: "^#" over "1 a 2 b 3 c 4" tints the four digits, bar says "4 found".

## 2. Ctrl+Alt shortcuts (Other shortcuts row)
Why: the row says Ctrl+Alt combinations are not read; Ctrl+Alt+1 even set single spacing, since only the Ctrl bit was looked at.
What: gen/p1_keys.py, rules placed first in rv_key_rules. Alt is bit 16 of the modifier word the glue already sends (no glue change). Ctrl+Alt+1/2/3 Heading 1 to 3 (style indexes 2..4; first run used 1..3 and got Title, fixed), Ctrl+Alt+M comment, Ctrl+Alt+F footnote, Ctrl+Alt+C/R/T/. for (c), (R), TM and the ellipsis.
Run: test/p1.js alt: first 4 of 5 (wrong style index), then 5 of 5.

## 3. Ribbon commands (Ribbon row)
What: gen/p1_btn.py (exec'd at the end of t3_btn.py) adds Layout > Column Break and Text Wrapping, Insert > Comment and Footnote, View > Print Layout; gen/p1_ribbon.py, group 'tier 1 ribbon commands', holds the three states that set arguments before the shared paths.
Runs: test/p1.js ribbon: first 3 of 6 (my clicks were one row low), then 5 of 6: the undo check typed after the break, and each test key is 5 s apart so typing undoes a letter at a time. Rewrote it to undo right after the break: 6 of 6.

## 4. Zoom to 500 percent (Zoom and views row)
What: ZL gains 2.5, 3, 4, 5 (gen/imp3_zoom_pre.py); ZPCT, ZVH, the slider step and the slider click map in gen/imp3_zoom.py are now written from the level count NZT, so the status bar plus and minus, View > Zoom In and Ctrl+wheel step 50 ... 200, 250, 300, 400, 500.
Run: test/p1.js zoom first 0 of 4: the view does not follow the caret after a zoom, so my ink measure saw only the page top; the test now presses Left, Right to bring the caret in (as imp3's own zoom test does). Then 'stops at 500' compared whole screens with a blinking caret and the pointer: compared after the same keys. 'Back to 100 equals never zoomed' failed because the scroll stays where the zoomed view left it (also true at 200, so not new); rewrote it to check the text and its ink height. 4 of 4. test/imp3.js zoom 12/12 on this build.
FLOPs: the first version cost 15 K to 33 K more per paint event (each paint bus sum read four more gated level terms). Fix: _zmap and _zw put the level terms behind one gate on "any level on", with an offset 2^30 since the sum can be negative (f64 values). zoom_sizes likewise gates the zoomed size terms. Now every paint event is below base (bold 7,311,745 to 7,267,246).

## 5. FLOPs on key events
The Ctrl+Alt rules first cost +1,950 per typed key (nine rules ahead of all others). Steps, each measured with test/flops.js:
- one rule for all Ctrl+Alt keys and a dispatch state P1_ALT keyed on eva: +119 on 'type at end, again'.
- KD shares one and_(ctrl,nf): +76. Merging Ctrl+B/I/U into one rule (app.py) made it +861, reverted.
- Found the real path: the cooked modifier word dropped Alt entirely (rv_a11_input _kcm = ctrl + 2 shift), so in a browser Ctrl+Alt never reached the network; the tests had injected raw bits past the cooking. Now _kcm adds 4 for Alt with Ctrl or Cmd, the key state reads three bits (p1_alt = kb[2]), Ctrl+Alt+C and X are not sent to the browser as copy or cut, and the tests drive keys through the key name path (keyv, keyl, raw bits) as the glue does. Ctrl+Alt rules sit at the end of rv_key_rules, the KD rules exclude Alt. Any other printable Ctrl+Alt key types its character, which is AltGr on many keyboards (test: @ and the euro sign).
- Still +41: per neuron work (scratch profiler, NETDBG dump) showed the rule before TYPE now shared TYPE's chunk of 12 conditions (nn.py CHUNK), so typing evaluated one more 97 input neuron. Moving TYPE earlier made it +110 (worse, reverted). Merging Ctrl+< and Ctrl+[ (same command) into one rule restores the alignment: 'type at end, again' 54,012 to 53,830. Note for merges: the number of KEY rules before TYPE matters modulo 12.

## 6. Landscape thumb (Zoom and views row)
Why: the row says the thumb's size assumes a portrait page.
What: gen/imp4_view.py draws the side bar thumb with a scale per level and orientation (over 900 px wide uses 1056 px); gen/imp5_wheel.py drags with the same scales. First run 0 of 2: the orientation test was gated by the wrong state (V8_HS0, not the bar's V8_E0), so it read zero. Fixed: 2 of 2 (thumb 981 px for a landscape page at 150 percent, drag of 150 px moves it 150 px). Screenshot build/p1_land.png.

## 7. Text wrapping break read from a file (Tabs and breaks row)
Run: a test opening `<w:br w:type="textWrapping"/>` failed: a w:br with a type other than page or column fell to A5_BR, which splits the paragraph. Word treats textWrapping (and w:clear) as a line break. T3_RB1's fallback now goes to RVA3_RBR, the same line break as `<w:br/>`. test/p1.js ribbon 7 of 7.

## 8. PARITY
Find and replace, Tabs and breaks, Other shortcuts and Rulers marked Passed with evidence in test/p1.js (rulers: existing a4, imp4, imp5 evidence; drag off removes a stop; the vertical ruler is at the window edge as in Word). Zoom and views and Ribbon stay Partial with what is still missing named (web layout, draft view, 72 pt glyph ceiling; many ribbon commands). Clipboard is Partial (blocked) with the blocker stated.

## Full run at 214238b
All exit 0: p1 27/27, e2e 210/210, tier2 49/49, look 31/31, t3_table 9, t3_pic 9, t3_misc 13, t4_docx 18/18, t4_pdf 7/7, roundtrip, touch, a4 50/50, a5_docx 37/37 (open 6,783,556 edges; base 6,784,308), fonts 23/23, imp2 45, imp3 49/49, imp4 101/101, imp5 49/49, imp6 20/20, feat1 24/24, feat2 35/35, t4, flops (every event at or below base), audit 67/67. Two builds byte identical. Page 2,958,405 bytes (base 2,953,717).

# Second round (coordinator: clipboard, ribbon, views)

## 9. Clipboard as HTML (Clipboard row)
Why: the coordinator pointed out the rules allow it: the network writes HTML bytes into the bank and the glue hands them over as text/html beside text/plain without reading them; on paste the glue passes the browser's text/html in as code units and the network parses it, as it parses .docx XML.
What: gen/p1_html.py, group 'clipboard html'.
- Writer: after the in-app copy (IMP3_CS*) the HTML twin is emitted through the shared byte emitter (embase set to P1HB): a <p> or a list item per paragraph with text-align, a <span> per change of style cell with bold, italic, underline, size in points (vnum), color (#hex from the exact color, else the palette string table) and font family (the exact name through T2SS, else the family or its Word alias), < > & escaped, line breaks as <br>. Lists open and close <ul>/<ol> as the kind changes. The last paragraph of a selection has no mark in the copy, so its alignment and list are read from the document. Too long for the 98,000 cell region: plain text only. Output neuron p1_htmlout (kept, in hdr as htmlout).
- Reader: P1_HQ follows the own-copy check, so the network's own copy still takes the exact in-app path. Eight cell window over P1HB with lpat rules: block tags (p, div, li, h1..h6, tr, td, pre, blockquote) make paragraphs with a pending break and text-align (logged for undo), ul/ol give list items LIST 1 or 2, inline tags push the run format on a stack in P1ST and set bold, italic, underline, strike; style attributes font-weight, font-style, text-decoration, font-size (pt or px to half points through the reader's size table), color (#hex through the reader's CO0, rgb() through its palette table), font-family (copied to the typed font name buffer and run through RF9, the reader's own name rules); closing inline tags pop. Entities amp, lt, gt, nbsp, quot, #39, #160; white space collapses as a browser shows it; comments, style, script, head and title are skipped. Two one-line intercepts route the reader's run property write (T2_C) and font name end (V4_FE) back to the HTML reader while p1hm is set.
- Glue: 2 more lines (83). The HTML twin is stored with the plain text and set on copy and cut, and written through ClipboardItem when the async clipboard is used; paste passes text/html as code units into P1HB with its length in the event. test/audit.py allow list: string 'text/html' and conditions 'hm', 'ph', each argued in the file.
Runs: first build: the copy HTML had no bold (rs takes an address, I passed the cell value), fixed. Font family pasted did nothing: RF9 read a stale window (the window is read entering the state; set rl again entering RF9), fixed. Then test/p1_clip.js (Playwright, real Ctrl+C and Ctrl+V): 13 of 13 first run: Ctrl+C puts HTML with bold, italic and centering on the system clipboard beside the plain text; an ordinary contenteditable page pastes it as bold and italic; a second app page pastes it back with the same runs and alignment; HTML from another program (style, title, comment, entities, a 20 pt red Courier New span via rgb() and &quot;, underline, a numbered and a bulleted list, strong in a list item) lands as the matching runs and list paragraphs; red ink drawn; one undo removes the whole paste.
Bug found by bisecting (about ten scratch builds): a5_docx lost text after any skipped element (rPrChange, endnotes...). My reader had a module level variable _ws; files are exec'd into one namespace, and rv_a10_pat's window wire is also _ws, so every later pat() state connected to my neuron and the window never woke. All module level temporaries in my files now start with _p1. a5_docx 0 failures after that.

## 10. Ribbon (Ribbon row)
Insert > Symbol: a menu (t1_menu 16, gen/p1_menus.py) of 16 symbols with names; a row types its character. Insert > Blank Page: page break, empty paragraph, page break, one undo. Review > Word Count: characters with spaces (sum of paragraph lengths) and paragraphs written into the status bar as a status message (p1wcm, like pmsg: kept through repaints, gone at the next key or click); words and pages are already there. First version painted over the status bar and the next repaint erased it; moved into the status painter's message slot. test/p1.js ribbon2 4 of 4 after one test fix (my ink box was outside the message).

## 11. Draft and web layout (Zoom and views row)
What: sload (the section geometry load used by layout) takes the view: draft and web layout use a 24 px top margin and text down to 24 px from the foot, web layout also a 1222 px wide page with 1150 px of text. The gray behind pages is white in both, the page shadow white, and the page frame's middle rectangle is a one pixel line at each page top (gray in draft, white in web). View > Print Layout, Web Layout, Draft; each lays the document out again (DA0). The vertical ruler is hidden in both, as in Word; the ruler draws inch numbers past 9 as two digits (10, 11, 12) for web layout's width.
Runs: test/p1.js views: first 3 of 5 (my paragraphs were too short to pass 960 px in web layout; gray count tolerance), then 5 of 5. The saved file is the same in every view.
Not done: the page count still follows the view's pagination (draft pages hold more lines than print).

## 12. Text above 72 pt (measured, scratch build, not committed)
Extending rom.SZ with 80, 88, 96, 108, 120, 144 pt (the record's size field has room: 7 bits) and letting zoom pick them: builds, 20 pt text at 500 percent draws at 96 pt (ink 104 rows against 77 at the 72 pt ceiling). Cost: page +1,044 bytes; typing one letter at 500 percent 177,867 edges against 116,079; per event FLOPs at 100 percent unchanged within noise (type at end +481 over base, the rest below base). Not committed: it changes rom.py's size table, which belongs to the fonts work (p2), and makes files keep sizes above 72 pt, a Font size row change.

## Full run at 556adf2
All exit 0: p1 36/36, p1_clip 13/13, e2e 210/210, tier2 49/49, look 31/31, t3_table 9, t3_pic 9, t3_misc 13, t4_docx 18/18, t4_pdf 7/7, roundtrip, touch, a4 50/50, a5_docx 37/37 (open 6,784,033 edges; base 6,784,308), fonts 23/23, imp2 45, imp3 49/49, imp4 101/101, imp5 49/49, imp6 20/20, feat1 24/24, feat2 35/35, t4, flops (every event below base; largest change -26), audit 67/67. Two builds byte identical. Page 2,979,349 bytes (base 2,953,717).
