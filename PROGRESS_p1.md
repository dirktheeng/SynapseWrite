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
