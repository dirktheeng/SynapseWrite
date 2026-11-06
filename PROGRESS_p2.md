# PROGRESS_p2: formatting, fonts, styles, lists, layout, line breaking, columns

## Baseline (main 76ede1a, built here)
- Page build/index.html: 2,953,717 bytes. Build about 58 s.
- FLOPs per event (test/flops.js, engine_count.wasm): start 6,471,503; paste 1900 paragraphs 118,777,849; background layout 556,832,631; type at end 718,971; type again 54,012; select all 6,405,696; jump to top 6,174,822; type at top 916,426; down 600,832; enter at top 6,242,180; undo 6,540,707; wheel 7,304,280; click 7,480,902; mouse move 27,533; bold 7,311,745.

## 1. Small capitals at their own size (extended run properties row)
Why: PARITY said small capitals drew at the script size (0.72), smaller than Word's. Word's spec note (MS-OI29500 smallCaps) says Word draws them a little smaller than the run, not 2 pt smaller, and gives no number; LibreOffice uses 0.8. Chose 0.8.
What: F1_SPLIT (gen/feat1_glyph.py) now returns three leaves per size: normal, script, small capital; the small capital leaf feeds size_hot[smc_size(i)] (gen/app.py). sel_sum reads a third branch for the small capital size. pdf_write.py has ptc, the small capital size in pixels, selected when f2smc is set and the run is not raised or lowered.
Run: build ok, page 2,954,793 (+1,076 bytes). feat1 24/24, feat2 35/35. New test/p2.js: 24 pt small caps run is pixel equal in heights and width to a 24 pt S beside 19 pt capitals; ratio of heights 0.750 (before, 17 pt, it would be about 0.70); PDF Tf sizes 32 and 25 px. 3/3 passed. Screenshot looked at: clean small capitals.
