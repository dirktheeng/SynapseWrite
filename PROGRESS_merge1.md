# Merge 1 progress log: Tier 1 into master (Tier 4 + performance)
Merge produced 9 conflict hunks as expected.
Plan and why:
- fm: T4's mark-delete moved from fm 9 to fm 11, because T1's menu rows set fm 9 and 10. fmh decodes 16, so room exists.
- Button ids: T4 raw 35, 54, 55 clash with T1's global find options, menu rows and thumb. Insert now uses raw 1..5, References raw 1, Review raw 1..4, all under TB(id,tab) rules placed before the generic B[] rules. Ribbon geometry kept so T4 test coordinates hold.
- Found while merging, not in the brief: T1 made low() depend on the Match case option, and T4 uses low() for spell check, equations and mail merge headers. Added low0() for T4.
- Found while merging: formatting mark on a tracked space would have driven rC twice with T1's ONE-SD['und']; it now excludes the merged underline signal.
- Found while merging: mail merge copies paragraph properties, so it now copies T1 indent, space after and line spacing as well.
- Hover range extended to raw 51..53 so Footnote, Picture and PDF highlight.
- Added 13 regression tests for these collisions at the end of e2e (first full run in progress used the file before they were added).
- First full run: e2e 134/134, roundtrip 3 true, t4_docx 18/18, t4_pdf 7/7, audit no failures. t16 needed build/p_rgb.png, a build-only fixture; copied it from master's build folder, picture loads in 1088 ms, 589704 ticks.
- Added tests: 146/147, then a different one of the find-option tests failed on rerun. Image diff was a one pixel column at the caret, so it is the 530 ms blink racing the screenshot. New tests now end with End, which resets the blink, as older tests do.
- One t4 run showed wheel 73 ms. Three repeats on the same build gave 14.8, 16.5, 15.1 ms with identical edges, so it was machine noise.
- Final e2e: 147/147 twice after the blink fix.
