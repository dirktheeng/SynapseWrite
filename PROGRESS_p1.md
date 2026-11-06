# PROGRESS p1 (tier 1 gaps)

Base: main at 76ede1a. Clone /root/p1, branch p1.

## Starting numbers
- Page build/index.html: 2,953,717 bytes.
- test/flops.js (build/engine_count.wasm): saved as flops_base.json in the clone root (not committed). Per event FLOPs: type at end 718,971; again 54,012; select all 6,405,696; jump to top 6,174,822; type at top 916,426; down 600,832; enter at top 6,242,180; undo 6,540,707; wheel 7,304,280; click 7,480,902; mouse move 27,533; bold 7,311,745.

## 1. Find codes (Find and replace row)
Why: the row says ^t and other Word codes are not read and a literal ^p cannot be searched for. Users who search for tabs or digits notice first.
What: gen/p1_find_pre.py, group 'find codes', exec'd from imp3_find.py. The query facts pass (IMP3_Q3) counts a code as two query cells and one document cell (qcod), and qmrk now means "marks or codes", so every query with a code goes to the shared matcher. The matcher's ^ branch (IMP3_X2) takes a known code to P1_XC/P1_XD, which compare one document cell with a literal (^t tab 9, ^l line break 11, ^^ caret, ^s no-break space 160, ^- optional hyphen 173) or a class (^? any, ^# digit, ^$ letter). A query with codes but no ^p has no fixed start, so the walker (P1_F0), the counter (P1_C0) and the highlight (IMP3_H0 extra rule) try every start. The replacement (IMP3_R1) inserts the five literal codes.
Run: test/p1.js find, first run 8 passed, 0 failed. Screenshot build/p1_find2.png: "^#" over "1 a 2 b 3 c 4" tints the four digits, bar says "4 found".
