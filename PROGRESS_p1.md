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
