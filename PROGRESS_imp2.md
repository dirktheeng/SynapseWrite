# imp2 progress log
Started from master 40524cd. test/imp2_tr.js and imp2_seq.js print cost per state, imp2_prof.js per neuron (COUNT engine).

## Typing regression: what the numbers were
98ffb6c `type at end` 16 ticks, 420 edges: far typing halted with no paint at all; the keystroke was invisible until the background ended. 9549d49 added the paint on a provisional page (a user visible fix). So the old number was not reachable with a visible key; the aim is the cheapest visible key.
Measured at 40524cd second key: C1 10.5 K, status bar chain about 100 K (35 glyphs at 2 to 3 K each), font and size boxes 16 K. First key: six paragraphs, 1183 glyphs at about 1100 edges each.
select all at 40524cd: 179 ticks because it painted NOTHING: screenshot build/tr3.png was a blank gray document area with "Page 0 of 1". Cause: scroll stayed at the provisional page, the viewport search landed on paragraphs after the background with no saved place. The measurement was right, the behavior was broken. Wheel was blank the same way (192 K).

## Fix 1 (commit "Far typing paints...")
Provisional page draws cp-1 and cp, not cp-6. Status bar memo stp stg stw stm, RE3 skips the chain on a fast event when unchanged. tbm memo for B I U, font and size boxes in TB0.
RD1: impf without impk (set only by the fast far key) redraws around the caret if the caret is past the background and no selection, else IMP_X restores the saved view (impsc, impyt). WH restores from impsc too.
Result t4: first key 1,388,705 to 342,324 edges, 2824 to 604 ticks; next keys 123,143 to 3,871 and 112,124 to 5,103, 156 to 65 ticks. select all 2374 ticks, 2.24 M, paints again. wheel 1.94 M, paints. imp_far all pass.

## Bisect (test/t4 on every generator commit, /root/imp2_bis/sweep.log, 17 commits)
8be4f20 pitch: jump 2160 to 2380 ticks, 1.759 M to 1.942 M; enter 1.699 M to 1.882 M; undo 1.791 M to 1.973 M; wheel 2144 to 2364. Edges per tick unchanged (815): 22 px lines became 19.33 px so about 10 percent more glyphs fit on the screen. No per glyph regression, lcar is 12 bits at EM only and does not show up. So those three stay near 1.9 M: more text on screen. Not a defect; not "fixed".
9549d49 far path: first key 303 edges to 1.40 M, next 108 K; select all 2154 ticks to 179 and wheel 2144 to 547 (blank, see above).

## Second finding: the background painted over the provisional page
Screenshot imp2_far2 after 4 timer ticks showed paragraphs 85 to 94 where the provisional page was: the background's walk passes scroll=_P and paints. A key after that would have drawn over it. BG clip is empty while impf. New check: page hash unchanged across slices.

## Bars (item 2)
IMP_F0 sets pagesT=bpg+1, the page number on the provisional page bpg+1, thumb at (pagesT-1)*PST. IMP_C0 after each slice while impc: pagesT, pcp, repaint scrollbar and status; costs about 100 K edges per slice, only after a far edit. Screenshot: Page 12 of 12, 5671 words mid background, was "Page 5 of 1". The counts are what has been laid out so far, and reach the true values when the background ends.
RE1 sets pcp=pagesT while impf, else a key after a slice set pcp back and repainted the status bar each key (t4 second key 96 K).

## Item 3
Scratch record starts PLSP=6 (single) in T3_Z6n, record 0 PLSP=6 at the same place, and record 0 takes the docDefaults value when DEFREC is saved or when styles.xml ends with no style. test/imp2: no styles 18 px, Normal without spacing 18, docDefaults 360 27, docDefaults 259 19, Normal 480 36; saves w:line=240.

## Item 4
Dry read: A12_OV2 goes to IMP_V0, which inflates word/document.xml into OUTB with vdry on before OP0. Missing part, bad block type, bad code, or output not equal to the directory's size (unless the output limit was hit) reach IMP_VF: message, document untouched. On success OP0 runs as before; styles and numbering now inflate to OUTP and the main part is not inflated again (IMP_DD2 jumps to PX with vob), so an open costs about what it did.
Limit: a flipped bit that still decodes to the stated size is not caught; that needs CRC32, one XOR per byte, too dear for the 10 M open bound. First test of that case opened with garbage text. Other members (styles, comments) that fail are still dropped silently.
Copy: COPYE refuses at 589900 with its own message and clears the network's own clip (the buffer was overwritten). Cut clears it too.

## Full run 1, stopped after e2e: 200/210
All ten differences in the box (113,65)-(275,107): font and size boxes gray, B I U missing. The ribbon display list paints placeholders and halts; the next event's TB chain fills them. The memo skipped that fill. Fix: UI clears tbm. Test edits: none.
