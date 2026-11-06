# imp4 progress log
Started from imp3 51aba01. Order: tier 2 (custom colors, style create and rename, character styles, list formats, font names and Unicode), tier 1 (vertical ruler, zoom above 150), hyphenation, select all cost.
Baseline build: 3,234,739 byte page, 946,543 stored edges.

## Style table entries, first commit
Records are full at 24 bits in a float32 cell. Why a wider table entry and not free bits in the cell: an entry of four cells (record, exact color plus one, font name id, character style id plus one) keeps every cell copy, undo log and clipboard path unchanged, since they only move indices, and the engine's read through an index cell already takes a stride and a length. So the style port returns all four with no engine change; the interner keys on all four.
Exact color: the glyph unit gets the color beside the nearest palette entry, and has 24 more channel lines weighted as binary digits, so the screen color is exact, not on the 4 bit grid. First run: no file color reached the cell, because the interner's new four cell write port was not in an aligned group, so its data neurons were not consecutive; fixed by aligning it.
Prompt bar: mode 8, one bar with many duties (color, new style, rename, font name). Bad hex leaves it open.
