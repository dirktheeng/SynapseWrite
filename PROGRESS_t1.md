# Tier 1 progress log

Baseline on clone: build 15 s, 142109 neurons, e2e 43/43, t4 worst 54 ms.

Finding: the alpha channel is 8 bit (engine clamps to 255), so button ids are limited to 200+id <= 255.
Ids 60 to 79 cannot be written to alpha. Plan: keep the raw alpha id small, and map (tab, raw id) to a
virtual id 60..79 with a small network before the button decoder. Home raw 40..43 -> 60..63,
Layout raw 1..8 -> 64..71, View raw 1..8 -> 72..79. Raw 35, 54, 55 are global: find options, menu row, scrollbar thumb.
