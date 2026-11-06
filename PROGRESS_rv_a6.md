# rv_a6 progress: Tier 4 functional gaps
Baseline: head 10efbe6 builds 426,964 neurons, 2,457,244 edges. Build gets OOM killed when others build; I wait for 3 GB free and retry.
Plan, most used first: PDF highlight and bookmarks; spelling suggestions and user dictionary; track changes date and paragraph marks; fields refresh; MERGEFIELD; equations.
Note: I once ran a scratchpad build script by a colliding name, and it belonged to rv_a9; it rebuilt that clone's build folder once. My scripts now live in scratchpad/a6.
## Spelling
Suggestion walk reuses the paint automaton through state A6S_W. "helo" opens in 2,962 ticks with hello, halo, hero, hell, helot. Row order: swap, delete, doubled, replace, insert, capped per kind.
Add to Dictionary is a bank table checked before the squiggle, kept in localStorage at the network's command. Ignore sets noProof. Screenshots checked.
## PDF
Multiply blend highlight is drawn after the chunk (no chunk measuring). Outline objects: nested by heading level; pypdf reads titles and destinations; qpdf clean.
## Track changes
First run: 11 of 17. Date index bug (dd fell on the dash), reader carried the mark to the next paragraph because a read SPLIT happens at the next w:p; fixed with a no-carry flag. Field refresh left a stale anchor, so the next key replaced a one digit selection and ate the field; fixed by syncing the anchor. Now 17 of 17.
## Equations
OMML written per character with script groups; python-docx parses it; save and open pixel identical. libreoffice-math is not installed here, so LibreOffice drops math: an honest gap in the stand-in.
## Built up math
One character (code 300 up) stands for a record with kind, widths and two texts, modelled on the footnote marker: layout takes width and taller line from it, paint draws rect, rule and small glyphs. Parser turns (a)/(b), x/y and sqrt(x) into records from Equation and from m:oMath closing in a file. 5 of 5 then 9 of 9 after test fix; screenshots and PDF checked.
Date bug: bits(year,2) is not a low bit extract, it needs full width; caught by t4_docx second save check.
## Full run, machine load 10 to 42
Counts against baseline (20 paragraphs): typing 77,037 to 77,074 edges; save 11.47 M to 11.91 M; PDF 103.70 M to 103.81 M.
Passed: rv_a6 6/6, rv_a6_pdf 4/4, rv_a6_track 17/17, rv_a6_eq 9/9, tier2 49/49, t4_pdf 7/7, t3_misc 13/13, t3_table 9/9, look 31/31, roundtrip no false entries. Those needing downloads ran with a longer local timeout (not committed), since 30 s was too short at load 40.
e2e 207/210 in the full run. Date and hover passed alone; mail merge failed twice alone at high load, passed twice at load 15. Differences were one caret column.
t4_docx 17/18: styles.xml check differs by one caret column. A repeated timing script fails on both builds: baseline 1 of 3, mine 2 of 3.
t3_pic 8/9: resize redo differs by one caret column at x 319, three of three in the suite here; the same steps without the suite's state check pass. Baseline passed once. Likely blink timing, not proven.
Final builds used a memo of rom.face_program, same values; the plain make.sh was not rerun after the first baseline.
