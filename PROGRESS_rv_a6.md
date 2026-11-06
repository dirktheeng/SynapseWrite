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
