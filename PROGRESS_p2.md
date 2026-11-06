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
