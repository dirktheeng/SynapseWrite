# rv_a2 progress: document canvas look
Started from annword head 10efbe6. Plan: build, make sample documents through events, compare to how Word looks, fix.

## First pass (baseline shots vs Word's look)
Found: doubled table rules, tracked underline with holes, list items spaced like paragraphs and markers 4 px off, headings with space after and gallery previews not matching, header 9 pt, footnote and comment typing invisible (no bar), find fields borderless with low text and no caret, yellow balloon, solid blue picture handles, no change bars, no paragraph mark in selection.
Fixed each; shots in shots_a2. First attempt at shared table rule (yy:rowmax) lost the last bottom rule since next paragraph's line fill erases it; now peek next paragraph (A2_TB*).
Not fixed: rom.metrics rounds line pitch to 22 px for 11 pt (Word about 19.3 px); rom.py is off limits. Empty paragraph left before an inserted table or picture is baked into test coordinates.

## Scroll limit
Short document could not reach its page foot: a wheel past the last text snapped back, so footnotes and footers on page one were unreachable. ytot now holds the end of the last page; scroll clamps to end of page plus a small gap.

## Test runs under load (load average 25 to 40, other agents building)
a2_canvas 19 of 19 once corrected (two earlier failures were my test: the caret and page edge counted as ink).
Under load, image hash comparisons fail when the caret blink fires between two shots. Checked m1 against m1c for 'footnote redo restores': the only difference is the caret column. Baseline build also failed differently under load ('Ctrl+V pastes text from outside', and suites killed).
Crashes ('Target crashed', goto aborted, download timeouts) occur on both builds and are memory or time pressure.
Not fixed: selection does not fill space after paragraphs, overlapping balloons do not stack, picture has three grips (only those work), find field text can run past its field.
