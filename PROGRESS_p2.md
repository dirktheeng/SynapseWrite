# PROGRESS_p2: formatting, fonts, styles, lists, layout, line breaking, columns

## Baseline (main 76ede1a, built here)
- Page build/index.html: 2,953,717 bytes. Build about 58 s.
- FLOPs per event (test/flops.js, engine_count.wasm): start 6,471,503; paste 1900 paragraphs 118,777,849; background layout 556,832,631; type at end 718,971; type again 54,012; select all 6,405,696; jump to top 6,174,822; type at top 916,426; down 600,832; enter at top 6,242,180; undo 6,540,707; wheel 7,304,280; click 7,480,902; mouse move 27,533; bold 7,311,745.

## 1. Small capitals at their own size (extended run properties row)
Why: PARITY said small capitals drew at the script size (0.72), smaller than Word's. Word's spec note (MS-OI29500 smallCaps) says Word draws them a little smaller than the run, not 2 pt smaller, and gives no number; LibreOffice uses 0.8. Chose 0.8.
What: F1_SPLIT (gen/feat1_glyph.py) now returns three leaves per size: normal, script, small capital; the small capital leaf feeds size_hot[smc_size(i)] (gen/app.py). sel_sum reads a third branch for the small capital size. pdf_write.py has ptc, the small capital size in pixels, selected when f2smc is set and the run is not raised or lowered.
Run: build ok, page 2,954,793 (+1,076 bytes). feat1 24/24, feat2 35/35. New test/p2.js: 24 pt small caps run is pixel equal in heights and width to a 24 pt S beside 19 pt capitals; ratio of heights 0.750 (before, 17 pt, it would be about 0.70); PDF Tf sizes 32 and 25 px. 3/3 passed. Screenshot looked at: clean small capitals.

## 2. Full suite run 1, and a FLOPs fix
Run 1 (commit after PARITY edit): two builds byte identical (2,954,793). All suites passed: e2e 210/210, tier2 49/49, look 31/31, t3_table 9, t3_pic 9, t3_misc 13, t4_docx 18/18, t4_pdf 7/7, roundtrip and touch all true, a4 50/50, a5_docx 37 PASS (6,784,308 edges), fonts 23/23, imp2 45, imp3 49/49, imp4 101/101, imp5 49, imp6 20, feat1 24/24, feat2 35/35, t4 ran, p2 3/3, audit 67/67.
But FLOPs rose: background layout +4,332,776 (0.8%), bold and click +27,854. Cause: the third sel_sum branch added a gate per size whose gate input is raw_hot, which changes on every glyph.
Fix: no third branch. Inside the script branch each size's value is val(script)+gate(val(smc)-val(script), _smo), where _smo is a step of the small capital flag that rests at zero for plain text, so its lazy pull stops at once. The F1_SPLIT selector is a step of the same flag, not an and_ with ONE.
Result: FLOPs identical to baseline on all 15 events. Page 2,955,265 (+1,548 bytes over baseline).

## 3. Full suite run 2 (final code a43a321 plus PARITY text)
Two builds byte identical, 2,955,265 bytes. Every suite passed as in run 1; p2 3/3; audit 67/67; flops identical to baseline on all events.
Not done on this branch, for lack of time, not for a rule: links drawn or followed, highlight colors past 7 (needs a fourth highlight bit; the 24 bit style record is full), styles gaps, list levels past three, column line and third column (the 8 field section record is full), Fonts gaps. Hyphenation: pattern set measured, network not built.

## 4. Continuing after the coordinator's note (keep going; widen records rather than call them blockers)

### Styles: Update on a character style (gen/p2_style.py, p2_regs.py, one-word hook in app.py, filter in rv_a7_bulk.py)
Why: PARITY said Update Style does not update a character style. Word's Update to Match Selection does.
What: Update (TB 52) now enters P2_UA, which reads the caret's run; if it has a character style, the caret record becomes the style's record, its exact color and font name go to STYX, and its mask is the fields that differ from the default (as New Char Style computes it), each with an undo record. Then the format walk (FMTS machinery, fm 16, wm 2) runs over the whole document with the selection set to all of it and given back at P2_CE; the bulk walker A7_FW skips runs whose RSY differs from the style (p2fon, p2fys). The skip test is behind net.gate(e,p2fon), so it is never read otherwise.
Snag: wo is rebound to a write port later in app.py; added the alias p2_wo next to its definition.
Runs: headless test (test/p2_lib.js part cstyle) 5/5: definition gets b and i, both runs of the style take italic, other runs untouched, page equals a file written that way, one undo takes back definition and the second run. FLOPs identical to baseline on all events.

### Styles: basedOn for a character style takes its base's mask (t2_features.py T2_AP)
Why: PARITY said a based-on character style took the base's values but not its mask, so a run of the child lost the base's fields.
What: T2_AP also reads the base's mask (STYX+2) and ORs its bits into v4m.
Runs: part based 3/3; with the fix stashed, 2 of 3 fail (no base color drawn, run saved without it). FLOPs unchanged.

### Text and highlight color: Word's eight further highlight values (p2_color.py, t2_features.py T2_HL, t2_write.py T2R9, app.py paint, pdf_write.py)
Why: only seven highlights were read; darkBlue, darkCyan, darkGreen, darkMagenta, darkRed, darkYellow, darkGray and black were dropped.
Storage: the record's 3 bit field is full; feat1's extended field (entry cell 4) had bits 14 to 23 free, so bits 14 to 17 hold the further highlight. Every decode of that field (x_decode, F1_XB, F1_SPW, feat2 PDF) is widened to 18 bits so the new bits do not spill into the old ones. F1_XB used 4 bits, which would also have misread a field with spacing set; now 18.
Screen: the exact run shade value is the shade or the highlight's exact color; costs nothing for plain text (push neurons, gates closed). FLOPs identical.
Tried and dropped, with numbers:
- white automatic text over dark highlights (Word does this): any new input to the color decode is read for every glyph; +2,538 to +73,548 FLOPs per event. Dropped under the FLOPs rule.
- 8 new palette background entries for clean glyph edges: +54 to +85,806 FLOPs (buses and palette lines are read on every draw); a gated second decoder was worse. Dropped.
- Kept: the shade neuron on the selection bus carries the nearest existing background entry in its value, so edge pixels blend into a dark entry instead of the light selection one. Zero FLOPs. Letters are readable; edge pixels take that entry's tint.
The same light fringe exists on main for a dark run shade (feat1); seen in a comparison screenshot.
PDF: the chunk's shade value includes the highlight's exact color. White text in PDF is impossible as written: the shade is drawn after the text with Multiply.
Writer: names written where the record highlight is written; a record highlight (ribbon) wins, so one highlight per run.
Runs: part hl 14/14 (eight colors drawn exactly, yellow intact, names saved, reopen pixel identical, ribbon yellow over darkBlue saves once, caps and spacing kept with it). p2.js PDF darkBlue exact color pass.
Gap: ribbon No Color over a further highlight leaves the further one (clearing it in the format walk costs a read per run).

### Fonts: synthesized italic for Oswald and Caveat (tried, reverted)
Word slants a family that has no italic face. Two compliant routes tried:
1. Slanted faces built at generation time (rom.py: fontTools shear of the upright glyf outlines, components moved by the slant of their offsets, advances kept), so screen and PDF need no change. Built and drew, but the page grew from 2,958,397 to 3,280,201 bytes (+321,804 for four faces), over the 3.0 MB limit by about 280 KB. Reverted.
2. Slant at draw time in the glyph unit (each row's patch x moved by 0.2 times its height above the baseline, cached rows shared with the upright face, a new call argument sl). The italic leaves of the face tree are lazily evaluated, so a pushed wire never sees them; reading them behind the draw gate costs reads on every draw: +22 to +32,879 FLOPs per event (background layout +32,879, bold +22,176), and the slant did not yet show. Reverted.
Blocker under the rules: route 1 breaks the page size limit, route 2 the FLOPs limit. Closest compliant result: unchanged (italic draws upright in these two families).
