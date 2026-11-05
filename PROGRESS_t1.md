# Tier 1 progress log

Baseline on clone: build 15 s, 142109 neurons, e2e 43/43, t4 worst 54 ms.

Finding: the alpha channel is 8 bit (engine clamps to 255), so button ids are limited to 200+id <= 255.
Ids 60 to 79 cannot be written to alpha. Plan: keep the raw alpha id small, and map (tab, raw id) to a
virtual id 60..79 with a small network before the button decoder. Home raw 40..43 -> 60..63,
Layout raw 1..8 -> 64..71, View raw 1..8 -> 72..79. Raw 35, 54, 55 are global: find options, menu row, scrollbar thumb.

Run log:
- First full build worked: hover, menus, click counting, thumb, find count, Layout and View tabs, ruler markers, restyle. 155495 neurons. Old 43 tests pass, roundtrip passes, t4 worst 89 ms.
- Added 56 tests. First run 90/99. Six failures were test mistakes (wrong expected state, a row y off by one row).
- Real fix found by tests: undo of a paragraph property moved the caret to offset 0. It now keeps the caret offset.
- Thumb tests: a single wheel event of -99999 did not reach the top of the document, so the drag started on the track. Test now uses several smaller wheel events. Not yet explained why the large event fell short.
- Explained the wheel shortfall: the network's gated registers clamp negative values to 0, so wheel up is capped at 1000 px per event (pre-existing, harmless for real wheels). Same clamp was a real bug in my margins: a negative line x0 became 0. Line x0 is now stored with +48 and painting and PDF subtract 48.
